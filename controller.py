import tkinter as tk
from tkinter import font, messagebox


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def open_file(self):
        name, size = self.model.open_file(self.view.text_info, self.view.fonts,
                                          self.view.root)
        self.change_fonts(self.view.fonts, size)
        self.view.root.title(name)

    def create_file(self):
        name = self.model.create_file(self.view.text_info)
        self.view.root.title(name)

    def save_as_file(self):
        name = self.model.save_as_file(self.view.text_info, self.view.font_size)
        self.view.root.title(name)

    def save(self):
        name = self.model.save(self.view.text_info, self.view.font_size)
        self.view.root.title(name)

    def close_file(self):
        answer = tk.messagebox.askquestion("Save or close",
                                           "Do you want to save changes?")
        if answer == "yes":
            self.save()
        self.view.root.destroy()

    def export_to_docx(self):
        self.model.export_to_docx(self.view.text_info)

    def get_bold_text(self):
        self.view.text_info.tag_configure("bold", font=self.view.fonts["bold"])
        current_tags = self.view.text_info.tag_names("sel.first")
        if "bold" in current_tags:
            self.view.text_info.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.view.text_info.tag_add("bold", "sel.first", "sel.last")

    def get_italic_text(self):
        self.view.text_info.tag_configure("italic",
                                          font=self.view.fonts["italic"])
        current_tags = self.view.text_info.tag_names("sel.first")
        if "italic" in current_tags:
            self.view.text_info.tag_remove("italic", "sel.first",
                                           "sel.last")
        else:
            self.view.text_info.tag_add("italic", "sel.first", "sel.last")

    def get_underline_text(self):
        self.view.text_info.tag_configure("underline",
                                          font=self.view.fonts["underline"])
        current_tags = self.view.text_info.tag_names("sel.first")
        if "underline" in current_tags:
            self.view.text_info.tag_remove("underline", "sel.first",
                                           "sel.last")
        else:
            self.view.text_info.tag_add("underline", "sel.first",
                                        "sel.last")

    def get_overstrike_text(self):
        self.view.text_info.tag_configure("overstrike",
                                          font=self.view.fonts["overstrike"])
        current_tags = self.view.text_info.tag_names("sel.first")
        if "overstrike" in current_tags:
            self.view.text_info.tag_remove("overstrike", "sel.first",
                                           "sel.last")
        else:
            self.view.text_info.tag_add("overstrike", "sel.first",
                                        "sel.last")

    def change_size(self, event):
        selected_size = int(event.widget.get())
        self.change_fonts(self.view.fonts, selected_size)

    def change_fonts(self, fonts: dict, selected_size):
        self.view.text_info.config(font=('Helvetica', selected_size))
        index = self.view.sizes.index(selected_size)
        self.view.sizes_combobox.current(index)
        self.view.font_size = selected_size
        fonts.update({"default": font.Font(size=selected_size),
                      "bold": font.Font(size=selected_size, weight='bold'),
                      "italic": font.Font(size=selected_size, slant='italic'),
                      "underline": font.Font(size=selected_size, underline=1),
                      "overstrike": font.Font(size=selected_size,
                                              overstrike=1)})
        self.view.text_info.tag_configure("bold", font=fonts["bold"])
        self.view.text_info.tag_configure("italic", font=fonts["italic"])
        self.view.text_info.tag_configure("underline", font=fonts["underline"])
        self.view.text_info.tag_configure("overstrike",
                                          font=fonts["overstrike"])
