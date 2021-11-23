import ast
import re
from tkinter import font, Text, messagebox
import tkinter as tk
from tkinter import filedialog as fd
import codecs
from docx import Document
from tkinter.ttk import Combobox
import unicodedata


# filename = ""


class Model:
    def __init__(self, filename):
        self.filename = filename

    @staticmethod
    def write_tags(file, text_info):
        tags = text_info.dump("1.0", tk.END)
        tags_to_str = str(tags).strip('[]')
        file.write(tags_to_str)
        print(tags_to_str)

    def open_file(self, text_info, fonts):
        # global filename
        self.filename = fd.askopenfilename(filetypes=[("Text files", "*.txt")],
                                           initialdir='/')
        with codecs.open(self.filename, errors='ignore') as f:
            short_name = f.name.split('/')[-1]
            # root.title(short_name)
            r_text_file = f.read()
        tags_pos = r_text_file.find('(')
        if tags_pos != 1:
            text = r_text_file[:tags_pos]
        else:
            text = r_text_file
        text_info.delete(1.0, tk.END)
        text_info.insert(tk.END, text)
        if tags_pos != 1:
            tags = r_text_file[tags_pos:]
            self.get_format_from_tags(tags, text_info, fonts)

        return short_name

    @staticmethod
    def create_file(text_info):
        text_info.delete(1.0, tk.END)
        return "New"

    def save_as_file(self, text_info):
        file_types = [("Text File", "*.txt"), ("All files", "*.*")]
        # global filename
        self.filename = fd.asksaveasfilename(confirmoverwrite=True,
                                             defaultextension=file_types,
                                             filetypes=file_types)
        if self.filename is None:
            return
        content = str(text_info.get(1.0, tk.END))
        save_file = open(self.filename, 'w+')
        normalized_content = unicodedata.normalize('NFC', content)
        save_file.write(normalized_content)
        # tags = text_info.dump("1.0", tk.END)
        # tags_to_str = str(tags).strip('[]')
        self.write_tags(save_file, text_info)
        save_file.close()
        short_name = self.filename.split('/')[-1]

        return short_name
        # root.title(short_name)

    def save(self, text_info):
        # global filename
        print(self.filename)
        if self.filename == "":
            self.save_as_file(text_info)
        else:
            content = str(text_info.get(1.0, tk.END))
            normalized_content = unicodedata.normalize('NFC', content)
            save_file = open(self.filename, 'w+')
            save_file.write(normalized_content)
            self.write_tags(save_file, text_info)
            save_file.close()
            short_name = self.filename.split('/')[-1]
            # root.title(short_name)

            return short_name

    @staticmethod
    def export_to_docx(text_info):
        doc = Document()
        strings = [text_info.get('1.0', 'end-1c')]
        for string in strings:
            run = doc.add_paragraph(string).add_run()
            fontt = run.font
            fontt.italic = True
        doc.save("C:/Users/vlad0/OneDrive/Документы/tkdoc.docx")

    @staticmethod
    def get_format_from_tags(tags: str, text_info, fonts):
        tags_list = list(ast.literal_eval(tags))
        current_font = None
        start_symbol = None
        for t in tags_list:
            print(t)
            if t[0] == 'tagon' and t[1] in fonts:
                current_font = t[1]
                start_symbol = t[2]
                continue
            if t[0] == 'tagoff' and t[1] in fonts:
                text_info.tag_configure(current_font, font=fonts[current_font])
                text_info.tag_add(current_font, start_symbol, t[2])


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def open_file(self):
        name = self.model.open_file(self.view.text_info, self.view.fonts)
        self.view.root.title(name)

    def create_file(self):
        name = self.model.create_file(self.view.text_info)
        self.view.root.title(name)

    def save_as_file(self):
        name = self.model.save_as_file(self.view.text_info)
        self.view.root.title(name)

    def save(self):
        name = self.model.save(self.view.text_info)
        self.view.root.title(name)

    def close_file(self):
        answer = tk.messagebox.askquestion("Save or close",
                                           "Do you want to save changes?")
        if answer == "yes":
            self.save()
        self.view.root.destroy()

    def export_to_docx(self):
        self.model.export_to_docx(self.view.text_info)

    def get_stats(self):
        new_window = tk.Toplevel(self.view.root)
        new_window.title("Text statistics")
        new_window.geometry("400x400")
        tk.Label(new_window, text="Statistics").pack()
        st = tk.Text(new_window)
        st.pack()
        st.insert(tk.END,
                  f'Chars: {len(self.view.text_info.get("1.0", "end-1c"))}\n')
        space_regex = re.compile(r'\S+')
        space_matches = re.findall(space_regex,
                                   self.view.text_info.get('1.0', 'end-1c'))
        st.insert(tk.END, f"Words: {len(space_matches)}\n")
        indent_regex = re.compile(r'\n')
        indent_matches = re.findall(indent_regex,
                                    self.view.text_info.get('1.0', 'end-1c'))
        st.insert(tk.END, f"Indents: {len(indent_matches)}")

    def get_bold_text(self):
        self.view.text_info.tag_configure("bold", font=self.view.fonts["bold"])
        current_tags = self.view.text_info.tag_names("sel.first")
        if "bold" in current_tags:
            self.view.text_info.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.view.text_info.tag_add("bold", "sel.first", "sel.last")
        # print(text_info.dump("1.0", tk.END))
        # print(text_info.tag_cget(tagName="bold", option="font"))

    def get_italic_text(self):
        self.view.text_info.tag_configure("italic",
                                          font=self.view.fonts["italic"])
        current_tags = self.view.text_info.tag_names("sel.first")
        if "italic" in current_tags:
            self.view.text_info.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.view.text_info.tag_add("italic", "sel.first", "sel.last")

    def get_underline_text(self):
        self.view.text_info.tag_configure("underline",
                                          font=self.view.fonts["underline"])
        current_tags = self.view.text_info.tag_names("sel.first")
        if "underline" in current_tags:
            self.view.text_info.tag_remove("underline", "sel.first", "sel.last")
        else:
            self.view.text_info.tag_add("underline", "sel.first", "sel.last")

    def get_overstrike_text(self):
        self.view.text_info.tag_configure("overstrike",
                                          font=self.view.fonts["overstrike"])
        current_tags = self.view.text_info.tag_names("sel.first")
        if "overstrike" in current_tags:
            self.view.text_info.tag_remove("overstrike", "sel.first",
                                           "sel.last")
        else:
            self.view.text_info.tag_add("overstrike", "sel.first", "sel.last")

    def change_size(self, event):
        selected_size = int(event.widget.get())
        self.view.text_info.config(font=('Helvetica', selected_size))
        self.change_fonts(self.view.fonts, selected_size)

    def change_fonts(self, fonts: dict, selected_size):
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

    # def get_format_from_tags(self, tags: str):
    #     tags_list = list(ast.literal_eval(tags))
    #     current_font = None
    #     start_symbol = None
    #     for t in tags_list:
    #         print(t)
    #         if t[0] == 'tagon' and t[1] in self.view.fonts:
    #             current_font = t[1]
    #             start_symbol = t[2]
    #             continue
    #         if t[0] == 'tagoff' and t[1] in self.view.fonts:
    #             self.view.text_info.tag_configure(current_font, font=self.view.fonts[current_font])
    #             self.view.text_info.tag_add(current_font, start_symbol, t[2])


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
        # command=get_bold_text)
        self.bold_button.pack(side=tk.LEFT)

        self.italic_button_font = font.Font(size=10, slant='italic')
        self.italic_button = tk.Button(self.fontbar_frame, text="Italic",
                                       font=self.italic_button_font)
        # command=get_italic_text)
        self.italic_button.pack(side=tk.LEFT)

        self.underline_button_font = font.Font(size=10, underline=1)
        self.underline_button = tk.Button(self.fontbar_frame, text="Underline",
                                          font=self.underline_button_font)
        # command=get_underline_text)
        self.underline_button.pack(side=tk.LEFT)

        self.overstrike_button_font = font.Font(size=10, overstrike=1)
        self.overstrike_button = tk.Button(self.fontbar_frame, text="Strikeout",
                                           font=self.overstrike_button_font)
        # command=get_overstrike_text)
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

        self.sizes = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
        self.sizes_combobox = Combobox(self.fontbar_frame, values=self.sizes,
                                       state="readonly")
        self.sizes_combobox.current(2)
        self.sizes_combobox.pack(side=tk.LEFT)

        self.menu = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.stat_menu = tk.Menu(self.menu, tearoff=0)

    def set_controller(self, controller):
        self.file_menu.add_command(label="New", command=controller.create_file)
        self.file_menu.add_command(label="Open", command=controller.open_file)
        self.file_menu.add_command(label="Save", command=controller.save)
        self.file_menu.add_command(label="Save as",
                                   command=controller.save_as_file)
        self.file_menu.add_command(label="Close", command=controller.close_file)
        self.file_menu.add_command(label="To docx",
                                   command=controller.export_to_docx)
        self.stat_menu.add_command(label="Show statistics",
                                   command=controller.get_stats)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.menu.add_cascade(label="Stats", menu=self.stat_menu)
        self.root.config(menu=self.menu)
        self.sizes_combobox.bind("<<ComboboxSelected>>", controller.change_size)
        self.bold_button.configure(command=controller.get_bold_text)
        # self.bold_button.pack(side=tk.LEFT)
        self.italic_button.configure(command=controller.get_italic_text)
        # self.italic_button.pack(side=tk.LEFT)
        self.underline_button.configure(command=controller.get_underline_text)
        # self.underline_button.pack(side=tk.LEFT)
        self.overstrike_button.configure(command=controller.get_overstrike_text)
        # self.overstrike_button.pack(side=tk.LEFT)

        self.root.mainloop()


# region file methods

# def open_file():  # model
#     global filename
#     filename = fd.askopenfilename(filetypes=[("Text files", "*.txt")],
#                                   initialdir='/')
#     with codecs.open(filename, errors='ignore') as f:
#         short_name = f.name.split('/')[-1]
#         root.title(short_name)
#         r_text_file = f.read()
#     tags_pos = r_text_file.find('(')
#     if tags_pos != 1:
#         text = r_text_file[:tags_pos]
#     else:
#         text = r_text_file
#     text_info.delete(1.0, tk.END)
#     text_info.insert(tk.END, text)
#     if tags_pos != 1:
#         tags = r_text_file[tags_pos:]
#         get_format_from_tags(tags)


# def create_file():  # model
#     text_info.delete(1.0, tk.END)
#     root.title("New")


# def save_as_file():
#     file_types = [("Text File", "*.txt"), ("All files", "*.*")]
#     global filename
#     filename = fd.asksaveasfilename(confirmoverwrite=True,
#                                     defaultextension=file_types,
#                                     filetypes=file_types)
#     if filename is None:
#         return
#     content = str(text_info.get(1.0, tk.END))
#     save_file = open(filename, 'w+')
#     normalized_content = unicodedata.normalize('NFC', content)
#     save_file.write(normalized_content)
#     # tags = text_info.dump("1.0", tk.END)
#     # tags_to_str = str(tags).strip('[]')
#     write_tags(save_file)
#     save_file.close()
#     short_name = filename.split('/')[-1]
#     root.title(short_name)


# def save():  # model
#     global filename
#     if filename == "":
#         save_as_file()
#     else:
#         content = str(text_info.get(1.0, tk.END))
#         normalized_content = unicodedata.normalize('NFC', content)
#         save_file = open(filename, 'w+')
#         save_file.write(normalized_content)
#         write_tags(save_file)
#         short_name = filename.split('/')[-1]
#         root.title(short_name)


# def close_file():  # model
#     answer = tk.messagebox.askquestion("Save or close",
#                                        "Do you want to save changes?")
#     if answer == "yes":
#         save()
#     root.destroy()


# def export_to_docx():  # model
#     doc = Document()
#     strings = [text_info.get('1.0', 'end-1c')]
#     for string in strings:
#         run = doc.add_paragraph(string).add_run()
#         fontt = run.font
#         fontt.italic = True
#     doc.save("C:/Users/vlad0/OneDrive/Документы/tkdoc.docx")


# endregion

# def get_format_text(selected_font: str):
#     text_info.tag_configure(selected_font, font=fonts["selected_font"])
#     current_tags = text_info.tag_names("sel.first")
#     if selected_font in current_tags:
#         text_info.tag_remove(selected_font, "sel.first", "sel.last")
#     else:
#         text_info.tag_add(selected_font, "sel.first", "sel.last")


# region text_format methods

# def get_bold_text():
#     text_info.tag_configure("bold", font=fonts["bold"])
#     current_tags = text_info.tag_names("sel.first")
#     if "bold" in current_tags:
#         text_info.tag_remove("bold", "sel.first", "sel.last")
#     else:
#         text_info.tag_add("bold", "sel.first", "sel.last")
#     # print(text_info.dump("1.0", tk.END))
#     # print(text_info.tag_cget(tagName="bold", option="font"))
#
#
# def get_italic_text():
#     text_info.tag_configure("italic", font=fonts["italic"])
#     current_tags = text_info.tag_names("sel.first")
#     if "italic" in current_tags:
#         text_info.tag_remove("italic", "sel.first", "sel.last")
#     else:
#         text_info.tag_add("italic", "sel.first", "sel.last")
#
#
# def get_underline_text():
#     text_info.tag_configure("underline", font=fonts["underline"])
#     current_tags = text_info.tag_names("sel.first")
#     if "underline" in current_tags:
#         text_info.tag_remove("underline", "sel.first", "sel.last")
#     else:
#         text_info.tag_add("underline", "sel.first", "sel.last")
#
#
# def get_overstrike_text():
#     text_info.tag_configure("overstrike", font=fonts["overstrike"])
#     current_tags = text_info.tag_names("sel.first")
#     if "overstrike" in current_tags:
#         text_info.tag_remove("overstrike", "sel.first", "sel.last")
#     else:
#         text_info.tag_add("overstrike", "sel.first", "sel.last")
#
#
# # endregion
#
# def change_size(event):
#     selected_size = int(event.widget.get())
#     text_info.config(font=('Helvetica', selected_size))
#     change_fonts(fonts, selected_size)
#
#
# def change_fonts(fonts: dict, selected_size=int):
#     fonts.update({"default": font.Font(size=selected_size),
#                   "bold": font.Font(size=selected_size, weight='bold'),
#                   "italic": font.Font(size=selected_size, slant='italic'),
#                   "underline": font.Font(size=selected_size, underline=1),
#                   "overstrike": font.Font(size=selected_size, overstrike=1)})
#     text_info.tag_configure("bold", font=fonts["bold"])
#     text_info.tag_configure("italic", font=fonts["italic"])
#     text_info.tag_configure("underline", font=fonts["underline"])
#     text_info.tag_configure("overstrike", font=fonts["overstrike"])


# region stats

# def get_stats():
#     new_window = tk.Toplevel(root)
#     new_window.title("Text statistics")
#     new_window.geometry("400x400")
#     tk.Label(new_window, text="Statistics").pack()
#     st = tk.Text(new_window)
#     st.pack()
#     st.insert(tk.END, f'Chars: {len(text_info.get("1.0", "end-1c"))}\n')
#     space_regex = re.compile(r'\S+')
#     space_matches = re.findall(space_regex, text_info.get('1.0', 'end-1c'))
#     st.insert(tk.END, f"Words: {len(space_matches)}\n")
#     indent_regex = re.compile(r'\n')
#     indent_matches = re.findall(indent_regex, text_info.get('1.0', 'end-1c'))
#     st.insert(tk.END, f"Indents: {len(indent_matches)}")


# endregion

# region tags methods

# def get_format_from_tags(tags: str):
#     tags_list = list(ast.literal_eval(tags))
#     current_font = None
#     start_symbol = None
#     for t in tags_list:
#         print(t)
#         if t[0] == 'tagon' and t[1] in fonts:
#             current_font = t[1]
#             start_symbol = t[2]
#             continue
#         if t[0] == 'tagoff' and t[1] in fonts:
#             text_info.tag_configure(current_font, font=fonts[current_font])
#             text_info.tag_add(current_font, start_symbol, t[2])


# def write_tags(file):
#     tags = text_info.dump("1.0", tk.END)
#     tags_to_str = str(tags).strip('[]')
#     file.write(tags_to_str)
#     print(tags_to_str)


# endregion

# root = tk.Tk()
# root.geometry("1200x2400")
# root.minsize(400, 400)
# root.maxsize(1600, 3200)
# root.title("New")
# scrollbar = tk.Scrollbar(root)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# fontbar_frame = tk.Frame(root)
# fontbar_frame.pack(fill=tk.X)
#
# font_size = 12
# fonts = {
#     "default": font.Font(size=font_size),
#     "bold": font.Font(size=font_size, weight='bold'),
#     "italic": font.Font(size=font_size, slant='italic'),
#     "underline": font.Font(size=font_size, underline=1),
#     "overstrike": font.Font(size=font_size, overstrike=1)
# }
# #  region create_buttons
# bold_button_font = font.Font(size=10, weight='bold')
# bold_button = tk.Button(fontbar_frame, text="Bold", font=bold_button_font,
#                         command=get_bold_text)
# bold_button.pack(side=tk.LEFT)
#
# italic_button_font = font.Font(size=10, slant='italic')
# italic_button = tk.Button(fontbar_frame, text="Italic", font=italic_button_font,
#                           command=get_italic_text)
# italic_button.pack(side=tk.LEFT)
#
# underline_button_font = font.Font(size=10, underline=1)
# italic_button = tk.Button(fontbar_frame, text="Underline",
#                           font=underline_button_font,
#                           command=get_underline_text)
# italic_button.pack(side=tk.LEFT)
#
# overstrike_button_font = font.Font(size=10, overstrike=1)
# overstrike_button = tk.Button(fontbar_frame, text="Strikeout",
#                               font=overstrike_button_font,
#                               command=get_overstrike_text)
# overstrike_button.pack(side=tk.LEFT)
# # endregion
# text_info: Text = tk.Text(root, yscrollcommand=scrollbar.set,
#                           font=fonts["default"], undo=True)
# text_info.pack(fill=tk.BOTH)
#
# scrollbar.config(command=text_info.yview)
# # region undo-redo
# undo_icon = tk.PhotoImage(file="icons/undo_icon.png").subsample(9, 9)
# undo_button = tk.Button(fontbar_frame, image=undo_icon,
#                         command=text_info.edit_undo)
# redo_icon = tk.PhotoImage(file="icons/redo_icon.png").subsample(26, 26)
# redo_button = tk.Button(fontbar_frame, image=redo_icon,
#                         command=text_info.edit_redo)
#
# undo_button.pack(side=tk.LEFT)
# redo_button.pack(side=tk.LEFT)
# # endregion
#
# sizes = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
# sizes_combobox = Combobox(fontbar_frame, values=sizes, state="readonly")
# sizes_combobox.current(2)
# sizes_combobox.pack(side=tk.LEFT)
# sizes_combobox.bind("<<ComboboxSelected>>", change_size)
#
# menu = tk.Menu(root)
# file_menu = tk.Menu(menu, tearoff=0)
# stat_menu = tk.Menu(menu, tearoff=0)
# file_menu.add_command(label="New", command=create_file)
# file_menu.add_command(label="Open", command=open_file)
# file_menu.add_command(label="Save", command=save)
# file_menu.add_command(label="Save as", command=save_as_file)
# file_menu.add_command(label="Close", command=close_file)
# file_menu.add_command(label="To docx", command=export_to_docx)
# stat_menu.add_command(label="Show statistics", command=get_stats)
# menu.add_cascade(label="File", menu=file_menu)
# menu.add_cascade(label="Stats", menu=stat_menu)
# root.config(menu=menu)
# root.mainloop()

if __name__ == '__main__':
    # root = tk.Tk()
    model = Model("")
    view = View()
    controller = Controller(model, view)
    view.set_controller(controller)
    # root.mainloop()
