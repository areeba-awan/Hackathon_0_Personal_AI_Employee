import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SimpleInboxWatcher(FileSystemEventHandler):
    def __init__(self, root_path):
        self.root = Path(root_path)
        self.needs_action = self.root / "Needs_Action"
        self.inbox = self.root / "Inbox"
        # Ensure both folders exist
        self.needs_action.mkdir(exist_ok=True)
        self.inbox.mkdir(exist_ok=True)

    def on_created(self, event):
        if event.is_directory:
            return
        
        source = Path(event.src_path)
        allowed_extensions = {'.txt', '.md', '.pdf', '.jpg', '.png'}
        
        if source.suffix.lower() not in allowed_extensions:
            print(f"Ignored: {source.name} (not an allowed file type)")
            return
        
        # Build base destination name
        dest_name = f"DROP_{source.name}"
        dest = self.needs_action / dest_name
        
        # If file already exists, add -1, -2, etc.
        counter = 1
        base_dest = dest
        while dest.exists():
            # Keep the original stem, add counter before extension
            stem = base_dest.stem
            if '-' in stem and stem.rsplit('-', 1)[1].isdigit():
                stem = stem.rsplit('-', 1)[0]
            dest = self.needs_action / f"{stem}-{counter}{base_dest.suffix}"
            counter += 1
        
        try:
            source.rename(dest)
            print(f"→ New task moved: {dest.name}")
        except Exception as e:
            print(f"Error moving file {source.name}: {e}")

if __name__ == "__main__":
    # Use current directory as root (where you run the script from)
    root = Path(".").resolve()
    
    print("Starting Inbox → Needs_Action watcher...")
    print(f"Watching folder: {root / 'Inbox'}")
    print("Allowed file types: .txt, .md, .pdf, .jpg, .png")
    print("Press Ctrl+C to stop\n")
    
    event_handler = SimpleInboxWatcher(root)
    observer = Observer()
    observer.schedule(event_handler, path=str(root / "Inbox"), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        observer.stop()
    except Exception as e:
        print(f"Watcher crashed: {e}")
    finally:
        observer.join()
        print("Watcher stopped.")