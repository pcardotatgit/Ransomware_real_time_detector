'''
    monitor files into a monitored directory and it's subdirectories and alert if any changes occur on files
    - File creation
    - File deletion
    - File modification / renaming
    - File move
'''
# pip install watchdog
# pip install requests
# pip install crayons
import watchdog.events
import watchdog.observers
import time
from send_alert_to_webex_room import send_alert
from crayons import *
import config as conf

file_types=conf.file_types
src_path =conf.src_path
ACCESS_TOKEN=conf.webex_bot_token
ROOM_ID=conf.webex_room_id
    
class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=file_types,ignore_directories=True, case_sensitive=False)
 
    def on_created(self, event):
        print("Watchdog received created event - % s." % event.src_path)
        # Event is created, you can process it now
 
    def on_modified(self, event):
        print("Watchdog received modified event - % s." % event.src_path)
        send_alert(ACCESS_TOKEN,ROOM_ID)
        # Event is modified, you can process it now
        
    def on_deleted(self, event):
        print("Watchdog received deleted event - % s." % event.src_path)
        # Event is modified, you can process it now
 
 
if __name__ == "__main__":
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    print()
    print(green(f"ACTIVE RANSOMWARE MONITORING STARTED ON DIRECTORY : {src_path}",bold=True))
    print()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
