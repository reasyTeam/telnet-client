#-*- coding: utf-8 -*-
import time, threading
from watchdog.observers import Observer
from watchdog.events import *
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff

class FileEventHandler(FileSystemEventHandler):
	def __init__(self, aim_path, call_back):
		FileSystemEventHandler.__init__(self)
		self.aim_path = aim_path
		self.timer = None
		self.call_back = call_back
		self.snapshot = DirectorySnapshot(self.aim_path)

	def on_any_event(self, event):
		if self.timer:
			self.timer.cancel()
		self.timer = threading.Timer(0.2, self.checkSnapshot)
		self.timer.start()

	def checkSnapshot(self):
		snapshot = DirectorySnapshot(self.aim_path)
		diff = DirectorySnapshotDiff(self.snapshot, snapshot)
		self.snapshot = snapshot
		self.timer = None
		#下面是应处理的各种事项
		# print("files_created:", diff.files_created)
		# print("files_deleted:", diff.files_deleted)
		# print("files_modified:", diff.files_modified)
		# print("files_moved:", diff.files_moved)
		# print("dirs_modified:", diff.dirs_modified)
		# print("dirs_moved:", diff.dirs_moved)
		# print("dirs_deleted:", diff.dirs_deleted)
		# print("dirs_created:", diff.dirs_created)
		# 接下来就是你想干的啥就干点啥，或者该干点啥就干点啥
		for file in diff.files_modified:
			print('[log][文件已修改]: %s' % file)
			if self.call_back:
				self.call_back(file)
			pass

class DirMonitor(object):
	"""文件夹监视类"""
	def __init__(self, aim_path):
		"""构造函数"""
		self.aim_path= aim_path
		self.observer = Observer()

	def start(self, call_back):
		"""启动"""
		event_handler = FileEventHandler(self.aim_path, call_back)
		self.observer.schedule(event_handler, self.aim_path, True)
		self.observer.start()

	def stop(self):
		"""停止"""
		self.observer.stop()

if __name__ == "__main__":
	monitor = DirMonitor(r"C:/Users/lenovo/Desktop/HG/test")
	monitor.start()

	try:
		while True:
			time.sleep(1)
	except:
		monitor.stop()

	monitor.observer.join()