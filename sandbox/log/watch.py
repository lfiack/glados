#!/usr/bin/python

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MonHandler(FileSystemEventHandler):
    def on_created(self, event):
        print("File %s as been created" % event.src_path)

    def on_deleted(self, event):
        print("File %s as been deleted" % event.src_path)

    def on_modified(self, event):
        print("File %s as been modified" % event.src_path)


observer = Observer()
observer.schedule(MonHandler(), path='/home/laurent/.eve/wineenv/drive_c/', recursive=True)

observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

