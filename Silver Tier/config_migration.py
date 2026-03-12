"""
Silver Tier Configuration Migration Tool
Helps migrate and validate configuration between versions
"""

import json
import logging
from pathlib import Path
from datetime import datetime
import shutil

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('ConfigMigration')

class ConfigMigration:
    """Handles configuration migration and validation"""

    # Default configuration template
    DEFAULT_CONFIG = {
        "vault": {
            "root_path": ".",
            "folders": {
                "inbox": "Inbox",
                "needs_action": "Needs_Action",
                "pending_approval": "Pending_Approval",
                "approved": "Approved",
                "done": "Done",
                "rejected": "Rejected",
                "plans": "Plans",
                "logs": "Logs"
            }
        },
        "watchers": {
            "inbox": {
                "enabled": True,
                "watch_extensions": [".txt", ".md", ".pdf", ".jpg", ".png"],
                "prefix": "DROP_"
            },
            "gmail": {
                "enabled": False,
                "check_interval": 120,
                "credentials_file": "token.json",
                "query": "is:unread is:important"
            }
        },
        "processing": {
            "auto_plan": True,
            "auto_approve": False,
            "log_level": "INFO"
        }
    }

    def __init__(self, vault_path: str = '.'):
        self.vault_path = Path(vault_path)
        self.config_file = self.vault_path / 'config.json'
        self.backup_dir = self.vault_path / '.config_backups'
        self.backup_dir.mkdir(exist_ok=True)

    def load_config(self) -> dict:
        """Load current configuration"""
        if not self.config_file.exists():
            logger.warning('config.json not found, using defaults')
            return self.DEFAULT_CONFIG.copy()

        try:
            with open(self.config_file) as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f'Invalid JSON in config.json: {e}')
            return None

    def save_config(self, config: dict, backup: bool = True):
        """Save configuration with optional backup"""
        if backup and self.config_file.exists():
            self._create_backup()

        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f'Configuration saved to {self.config_file}')

    def _create_backup(self):
        """Create backup of current configuration"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.backup_dir / f'config_{timestamp}.json'
        shutil.copy(self.config_file, backup_file)
        logger.info(f'Backup created: {backup_file}')

    def validate_config(self, config: dict) -> tuple[bool, list]:
        """
        Validate configuration structure

        Returns:
            tuple: (is_valid, list_of_errors)
        """
        errors = []

        # Check required sections
        required_sections = ['vault', 'watchers', 'processing']
        for section in required_sections:
            if section not in config:
                errors.append(f'Missing section: {section}')

        # Validate vault section
        if 'vault' in config:
            vault = config['vault']
            if 'folders' not in vault:
                errors.append('Missing vault.folders')
            else:
                required_folders = ['inbox', 'needs_action', 'pending_approval',
                                  'approved', 'done', 'rejected', 'plans', 'logs']
                for folder in required_folders:
                    if folder not in vault['folders']:
                        errors.append(f'Missing vault.folders.{folder}')

        # Validate watchers section
        if 'watchers' in config:
            watchers = config['watchers']
            if 'inbox' in watchers:
                inbox = watchers['inbox']
                if 'enabled' not in inbox:
                    errors.append('Missing watchers.inbox.enabled')
                if 'watch_extensions' not in inbox:
                    errors.append('Missing watchers.inbox.watch_extensions')

        # Validate processing section
        if 'processing' in config:
            processing = config['processing']
            if 'auto_plan' not in processing:
                errors.append('Missing processing.auto_plan')
            if 'log_level' not in processing:
                errors.append('Missing processing.log_level')

        return len(errors) == 0, errors

    def migrate_from_v0_to_v1(self, old_config: dict) -> dict:
        """Migrate configuration from v0 to v1"""
        logger.info('Migrating configuration from v0 to v1...')

        new_config = self.DEFAULT_CONFIG.copy()

        # Migrate vault settings
        if 'vault' in old_config:
            if 'root_path' in old_config['vault']:
                new_config['vault']['root_path'] = old_config['vault']['root_path']

        # Migrate watcher settings
        if 'watchers' in old_config:
            if 'inbox' in old_config['watchers']:
                new_config['watchers']['inbox'].update(old_config['watchers']['inbox'])
            if 'gmail' in old_config['watchers']:
                new_config['watchers']['gmail'].update(old_config['watchers']['gmail'])

        # Migrate processing settings
        if 'processing' in old_config:
            new_config['processing'].update(old_config['processing'])

        logger.info('Migration complete')
        return new_config

    def merge_configs(self, base_config: dict, override_config: dict) -> dict:
        """Merge override config into base config"""
        import copy
        result = copy.deepcopy(base_config)

        def merge_dict(base, override):
            for key, value in override.items():
                if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                    merge_dict(base[key], value)
                else:
                    base[key] = value

        merge_dict(result, override_config)
        return result

    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        logger.info('Resetting configuration to defaults...')
        self.save_config(self.DEFAULT_CONFIG.copy())
        logger.info('Configuration reset to defaults')

    def list_backups(self):
        """List all configuration backups"""
        if not self.backup_dir.exists():
            logger.info('No backups found')
            return []

        backups = sorted(self.backup_dir.glob('config_*.json'), reverse=True)
        logger.info(f'Found {len(backups)} backups:')
        for backup in backups:
            logger.info(f'  - {backup.name}')
        return backups

    def restore_backup(self, backup_name: str):
        """Restore configuration from backup"""
        backup_file = self.backup_dir / backup_name
        if not backup_file.exists():
            logger.error(f'Backup not found: {backup_name}')
            return False

        self._create_backup()  # Backup current before restoring
        shutil.copy(backup_file, self.config_file)
        logger.info(f'Configuration restored from {backup_name}')
        return True

    def export_config(self, export_path: str):
        """Export configuration to file"""
        config = self.load_config()
        if config is None:
            logger.error('Cannot export invalid configuration')
            return False

        export_file = Path(export_path)
        with open(export_file, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f'Configuration exported to {export_path}')
        return True

    def import_config(self, import_path: str):
        """Import configuration from file"""
        import_file = Path(import_path)
        if not import_file.exists():
            logger.error(f'Import file not found: {import_path}')
            return False

        try:
            with open(import_file) as f:
                config = json.load(f)

            is_valid, errors = self.validate_config(config)
            if not is_valid:
                logger.error('Imported configuration is invalid:')
                for error in errors:
                    logger.error(f'  - {error}')
                return False

            self.save_config(config)
            logger.info(f'Configuration imported from {import_path}')
            return True

        except json.JSONDecodeError as e:
            logger.error(f'Invalid JSON in import file: {e}')
            return False

    def interactive_setup(self):
        """Interactive configuration setup"""
        logger.info('')
        logger.info('╔════════════════════════════════════════════════════════════╗')
        logger.info('║    Silver Tier Configuration Setup                         ║')
        logger.info('╚════════════════════════════════════════════════════════════╝')
        logger.info('')

        config = self.DEFAULT_CONFIG.copy()

        # Inbox watcher setup
        logger.info('📁 Inbox Watcher Configuration:')
        enable_inbox = input('Enable Inbox watcher? (y/n) [y]: ').lower() != 'n'
        config['watchers']['inbox']['enabled'] = enable_inbox

        # Gmail watcher setup
        logger.info('')
        logger.info('📧 Gmail Watcher Configuration:')
        enable_gmail = input('Enable Gmail watcher? (y/n) [n]: ').lower() == 'y'
        config['watchers']['gmail']['enabled'] = enable_gmail

        if enable_gmail:
            interval = input('Check interval in seconds [120]: ')
            if interval.isdigit():
                config['watchers']['gmail']['check_interval'] = int(interval)

        # Processing setup
        logger.info('')
        logger.info('⚙️  Processing Configuration:')
        auto_plan = input('Enable auto-plan generation? (y/n) [y]: ').lower() != 'n'
        config['processing']['auto_plan'] = auto_plan

        auto_approve = input('Enable auto-approve? (y/n) [n]: ').lower() == 'y'
        config['processing']['auto_approve'] = auto_approve

        log_level = input('Log level [INFO]: ').upper() or 'INFO'
        if log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            config['processing']['log_level'] = log_level

        # Save configuration
        logger.info('')
        self.save_config(config)
        logger.info('✅ Configuration setup complete!')

if __name__ == '__main__':
    import sys

    migration = ConfigMigration()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'validate':
            config = migration.load_config()
            if config:
                is_valid, errors = migration.validate_config(config)
                if is_valid:
                    logger.info('✅ Configuration is valid')
                else:
                    logger.error('❌ Configuration has errors:')
                    for error in errors:
                        logger.error(f'  - {error}')

        elif command == 'reset':
            migration.reset_to_defaults()

        elif command == 'backups':
            migration.list_backups()

        elif command == 'restore' and len(sys.argv) > 2:
            migration.restore_backup(sys.argv[2])

        elif command == 'export' and len(sys.argv) > 2:
            migration.export_config(sys.argv[2])

        elif command == 'import' and len(sys.argv) > 2:
            migration.import_config(sys.argv[2])

        elif command == 'setup':
            migration.interactive_setup()

        else:
            logger.info('Usage:')
            logger.info('  python config_migration.py validate    - Validate config')
            logger.info('  python config_migration.py reset       - Reset to defaults')
            logger.info('  python config_migration.py backups     - List backups')
            logger.info('  python config_migration.py restore <name> - Restore backup')
            logger.info('  python config_migration.py export <path> - Export config')
            logger.info('  python config_migration.py import <path> - Import config')
            logger.info('  python config_migration.py setup       - Interactive setup')
    else:
        migration.interactive_setup()
