import inspect
import os
import tkinter as tk
import plugins.base_plugin
from tkinter import font, Text
from tkinter.ttk import Combobox
from importlib import import_module


class View:
    def __init__(self):
        self.root = tk.Tk()
        self.scrollbar = tk.Scrollbar(self.root)
        self.root.geometry("1200x2400")
        self.root.minsize(400, 400)
        self.root.maxsize(1600, 3200)
        self.root.title("New")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.fontbar_frame = tk.Frame(self.root)
        self.fontbar_frame.pack(fill=tk.X)
        self.plugins = []

        self.font_size = 12
        self.fonts = {
            "default": font.Font(size=self.font_size),
            "bold": font.Font(size=self.font_size, weight='bold'),
            "italic": font.Font(size=self.font_size, slant='italic'),
            "underline": font.Font(size=self.font_size, underline=1),
            "overstrike": font.Font(size=self.font_size, overstrike=1)
        }
        #  region create_buttons
        self.bold_button_font = font.Font(size=10, weight='bold')
        self.bold_button = tk.Button(self.fontbar_frame, text="Bold",
                                     font=self.bold_button_font)
        self.bold_button.pack(side=tk.LEFT)

        self.italic_button_font = font.Font(size=10, slant='italic')
        self.italic_button = tk.Button(self.fontbar_frame, text="Italic",
                                       font=self.italic_button_font)
        self.italic_button.pack(side=tk.LEFT)

        self.underline_button_font = font.Font(size=10, underline=1)
        self.underline_button = tk.Button(self.fontbar_frame, text="Underline",
                                          font=self.underline_button_font)
        self.underline_button.pack(side=tk.LEFT)

        self.overstrike_button_font = font.Font(size=10, overstrike=1)
        self.overstrike_button = tk.Button(self.fontbar_frame, text="Strikeout",
                                           font=self.overstrike_button_font)
        self.overstrike_button.pack(side=tk.LEFT)
        # endregion
        self.text_info: Text = tk.Text(self.root,
                                       yscrollcommand=self.scrollbar.set,
                                       font=self.fonts["default"], undo=True)
        self.text_info.pack(fill=tk.BOTH)

        self.scrollbar.config(command=self.text_info.yview)
        # region undo-redo

        self.undo_icon = tk.PhotoImage(file="icons/undo_icon.png").subsample(9,
                                                                             9)
        self.undo_button = tk.Button(self.fontbar_frame, image=self.undo_icon,
                                     command=self.text_info.edit_undo)
        self.redo_icon = tk.PhotoImage(file="icons/redo_icon.png").subsample(26,
                                                                             26)
        self.redo_button = tk.Button(self.fontbar_frame, image=self.redo_icon,
                                     command=self.text_info.edit_redo)

        self.undo_button.pack(side=tk.LEFT)
        self.redo_button.pack(side=tk.LEFT)

        # endregion

        self.sizes = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
        self.sizes_combobox = Combobox(self.fontbar_frame, values=self.sizes,
                                       state="readonly")
        self.sizes_combobox.current(2)
        self.sizes_combobox.pack(side=tk.LEFT)

        self.menu = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu, tearoff=0)

    def install_plugins(self):
        for plugin in os.listdir("plugins"):
            if plugin.endswith('.py'):
                plugin_name = plugin[:-len('.py')]
                if plugin_name != "base_plugin" and plugin_name != "__init__":
                    self.plugins.append("plugins" + "." + plugin_name)
        for plugin in self.plugins:
            plugin_obj = import_module(plugin)
            for e in dir(plugin_obj):
                obj = getattr(plugin_obj, e)
                if inspect.isclass(obj):
                    if issubclass(obj, plugins.base_plugin.BasePlugin):
                        plugin_installer = obj(self)
                        plugin_installer.install()

    def set_controller(self, editor_controller):
        self.file_menu.add_command(label="New",
                                   command=editor_controller.create_file)
        self.file_menu.add_command(label="Open",
                                   command=editor_controller.open_file)
        self.file_menu.add_command(label="Save", command=editor_controller.save)
        self.file_menu.add_command(label="Save as",
                                   command=editor_controller.save_as_file)
        self.file_menu.add_command(label="Close",
                                   command=editor_controller.close_file)
        self.file_menu.add_command(label="To docx",
                                   command=editor_controller.export_to_docx)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.root.config(menu=self.menu)
        self.sizes_combobox.bind("<<ComboboxSelected>>",
                                 editor_controller.change_size)
        self.bold_button.configure(command=editor_controller.get_bold_text)
        self.italic_button.configure(command=editor_controller.get_italic_text)
        self.underline_button.configure(command=editor_controller.
                                        get_underline_text)
        self.overstrike_button.configure(command=editor_controller
                                         .get_overstrike_text)

        self.install_plugins()

        self.root.mainloop()
