import os
import sys
import json
import sublime, sublime_plugin
import subprocess


def fread(filepath):
    with open(filepath, 'r') as f:
        return f.read()


def freadlines(filepath):
    with open(filepath, 'r') as f:
        return f.read().splitlines()


class LanguageFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit, error=True, save=True):
        syntax = self.view.settings().get('syntax')
        print(syntax)
        cmd = list()
        contents = str()

        languages = ['C', 'C++', 'Objective-C', 'Protobuf', 'C#', 'PXScript']
        if any((syntax.endswith((l + '.tmLanguage', l + '.sublime-syntax')) for l in languages)):
            # run clang-format
            package_path = os.path.split(os.path.dirname(__file__))[1]
            executable_path = os.path.join(sublime.packages_path(), package_path, "bin", sys.platform, "clang-format")
            contents = self.view.substr(sublime.Region(0, self.view.size()))
            cmd = [executable_path]
            style_path = os.path.join(sublime.packages_path(), package_path, "config", "clang.cfg")
            window = self.view.window()
            style = fread(style_path)
            cmd.append("-style")
            cmd.append(style)
            self.process(edit, cmd, contents)
            return

        languages = ['Lua']
        if any((syntax.endswith((l + '.tmLanguage', l + '.sublime-syntax')) for l in languages)):
            # run lua-format
            package_path = os.path.split(os.path.dirname(__file__))[1]
            executable_path = os.path.join(sublime.packages_path(), package_path, "bin", sys.platform, "lua-format")
            contents = self.view.substr(sublime.Region(0, self.view.size()))
            cmd = [executable_path]
            style_path = os.path.join(sublime.packages_path(), package_path, "config", "clang.cfg")
            cmd.append("-c")
            cmd.append(style_path)
            self.process(edit, cmd, contents)
            return

        languages = ['Python']
        if any((syntax.endswith((l + '.tmLanguage', l + '.sublime-syntax')) for l in languages)):
            # run yapf
            package_path = os.path.split(os.path.dirname(__file__))[1]
            style_path = os.path.join(sublime.packages_path(), package_path, "config", "yapf.cfg")
            executable_path = os.path.join('yapf')
            contents = self.view.substr(sublime.Region(0, self.view.size()))
            cmd = [executable_path]
            cmd.append("--style")
            cmd.append(style_path)
            self.process(edit, cmd, contents)
            return

        languages = ['JavaScript']
        if any((syntax.endswith((l + '.tmLanguage', l + '.sublime-syntax')) for l in languages)):
            # run js-beautify
            package_path = os.path.split(os.path.dirname(__file__))[1]
            style_path = os.path.join(sublime.packages_path(), package_path, "config", "js-beautify.cfg")
            executable_path = os.path.join('js-beautify')
            contents = self.view.substr(sublime.Region(0, self.view.size()))
            cmd = [executable_path]
            cmd.append("--config")
            cmd.append(style_path)
            self.process(edit, cmd, contents)
            return

        languages = ['HTML']
        if any((syntax.endswith((l + '.tmLanguage', l + '.sublime-syntax')) for l in languages)):
            # run js-beautify
            package_path = os.path.split(os.path.dirname(__file__))[1]
            style_path = os.path.join(sublime.packages_path(), package_path, "config", "js-beautify.cfg")
            executable_path = os.path.join('html-beautify')
            contents = self.view.substr(sublime.Region(0, self.view.size()))
            cmd = [executable_path]
            cmd.append("--config")
            cmd.append(style_path)
            self.process(edit, cmd, contents)
            return

        languages = ['CSS']
        if any((syntax.endswith((l + '.tmLanguage', l + '.sublime-syntax')) for l in languages)):
            # run js-beautify
            package_path = os.path.split(os.path.dirname(__file__))[1]
            style_path = os.path.join(sublime.packages_path(), package_path, "config", "js-beautify.cfg")
            executable_path = os.path.join('css-beautify')
            contents = self.view.substr(sublime.Region(0, self.view.size()))
            cmd = [executable_path]
            cmd.append("--config")
            cmd.append(style_path)
            self.process(edit, cmd, contents)
            return

        languages = ['JSON']
        sublime_configs = ['sublime-settings', 'sublime-keymap', 'sublime-commands', 'sublime-menu']
        sublime_filepath = self.view.file_name()
        if any((syntax.endswith((l + '.tmLanguage', l + '.sublime-syntax')) for l in languages)):
            package_path = os.path.split(os.path.dirname(__file__))[1]
            executable_path = os.path.join('js-beautify')
            style_path = str()
            contents = self.view.substr(sublime.Region(0, self.view.size()))
            cmd = [executable_path]
            # run js-beautify
            if sublime_filepath is not None and any((sublime_filepath.endswith(conf) for conf in sublime_configs)):
                style_path = os.path.join(sublime.packages_path(), package_path, "config", "sublime.cfg")
            else:
                style_path = os.path.join(sublime.packages_path(), package_path, "config", "json.cfg")
            cmd.append("--config")
            cmd.append(style_path)
            self.process(edit, cmd, contents)
            return

        languages = ['Vue', 'Vue Component']
        if any((syntax.endswith((l + '.tmLanguage', l + '.sublime-syntax')) for l in languages)):
            # run prettier
            package_path = os.path.split(os.path.dirname(__file__))[1]
            style_path = os.path.join(sublime.packages_path(), package_path, "config", "vue.cfg")
            styles = freadlines(style_path)
            executable_path = os.path.join('prettier')
            contents = self.view.substr(sublime.Region(0, self.view.size()))
            cmd = [executable_path]
            for i in styles:
                cmd.append(i)
            self.process(edit, cmd, contents)
            return

    def process(self, edit, cmd: list, contents: str):
        if len(cmd) == 0:
            sublime.error_message("Not Support.")
            return

        # print(cmd)
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.stdin.write(str.encode(contents))
        process.stdin.close()
        output = bytes.decode(process.stdout.read())
        error = bytes.decode(process.stderr.read())
        if error == "":
            self.view.replace(edit, sublime.Region(0, self.view.size()), output)
        else:
            sublime.error_message(error)
