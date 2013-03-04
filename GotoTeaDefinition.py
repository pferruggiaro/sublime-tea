import sublime, sublime_plugin
import os.path
import re
from collections import defaultdict
from collections import deque

settings = sublime.load_settings('SublimeTea.sublime-settings')

class GotoTeaDefinitionCommand(sublime_plugin.TextCommand):

	# def run_(self, args):
	# 	window = sublime.active_window()
	# 	view = self.view
	# 	edit = self.view.begin_edit(self.name(), args)
	# 	#print self.view.sel()[0]

	# 	old_sel = [r for r in self.view.sel()]
	# 	print args
	# 	self.view.run_command("drag_select", {'event': args['event']})
	# 	pos = self.view.sel()[0].begin()
	# 	# #sel = self.view.sel()
	# 	print pos
	# 	new_sel = self.view.sel()
	# 	click_point = new_sel[0].a
	# 	new_sel.clear()
	# 	map(new_sel.add, old_sel)
	# 	self.view.run_command("drag_select", args)
	# 	# self.view.end_edit(edit)
	# 	# self.view.sel().clear()
	# 	# self.view.end_edit(edit)

	def run(self, edit):
		window = sublime.active_window()
		view = self.view
		pos = view.sel()[0].end()
		syntax = view.scope_name(pos)

		if re.match(".*meta.template-call.tea", syntax):
			path = view.substr(view.extract_scope(pos))
			opened = self.resolve_path(window, view, path)

	def resolve_path(self, window, view, path):
		path = path.replace(".", "/") + ".tea"
		dirname = os.path.dirname(view.file_name())
		window.open_file(self.find_template(dirname, path))

	def find_template(self, dirname, filename):
		# first try the same folder as the current template
		absolute = os.path.join(dirname, filename)
		if (os.path.exists(absolute)):
			return absolute

		# second try from the root of the service
		service = self.find_service(dirname)
		if (service):
			absolute = os.path.join(service.get('path'), filename)
			if (os.path.exists(absolute)):
				return absolute

		# third try the inlcudes paths
		for includePath in service.get('include-paths'):
			absolute = os.path.join(includePath, filename)
			if (os.path.exists(absolute)):
				return absolute

	def find_service(self, dirname):
		for service in settings.get('template_paths'):
			path = service.get('path')
			if dirname.find(path) != -1:
				return service
