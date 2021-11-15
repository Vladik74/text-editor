import ast
import re
from tkinter import font, Text, messagebox
import tkinter as tk
from tkinter import filedialog as fd
import codecs
from docx import Document
from tkinter.ttk import Combobox
import unicodedata

filename = ""

class Model:
    def __init__(self, filename):
        self.filename = filename

    def open_file(self):
        global filename
        filename = fd.askopenfilename(filetypes=[("Text files", "*.txt")],
                                      initialdir='/')
        with codecs.open(filename, errors='ignore') as f:
            short_name = f.name.split('/')[-1]
            root.title(short_name)
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
            get_format_from_tags(tags)



class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

# region file methods
def open_file(): # model
    global filename
    filename = fd.askopenfilename(filetypes=[("Text files", "*.txt")],
                                  initialdir='/')
    with codecs.open(filename, errors='ignore') as f:
        short_name = f.name.split('/')[-1]
        root.title(short_name)
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
        get_format_from_tags(tags)


def create_file(): # model
    text_info.delete(1.0, tk.END)
    root.title("New")


def save_as_file():
    file_types = [("Text File", "*.txt"), ("All files", "*.*")]
    global filename
    filename = fd.asksaveasfilename(confirmoverwrite=True,
                                    defaultextension=file_types,
                                    filetypes=file_types)
    if filename is None:
        return
    content = str(text_info.get(1.0, tk.END))
    save_file = open(filename, 'w+')
    normalized_content = unicodedata.normalize('NFC', content)
    save_file.write(normalized_content)
    # tags = text_info.dump("1.0", tk.END)
    # tags_to_str = str(tags).strip('[]')
    write_tags(save_file)
    save_file.close()
    short_name = filename.split('/')[-1]
    root.title(short_name)


def save(): #model
    global filename
    if filename == "":
        save_as_file()
    else:
        content = str(text_info.get(1.0, tk.END))
        normalized_content = unicodedata.normalize('NFC', content)
        save_file = open(filename, 'w+')
        save_file.write(normalized_content)
        write_tags(save_file)
        short_name = filename.split('/')[-1]
        root.title(short_name)


def close_file(): #model
    answer = tk.messagebox.askquestion("Save or close",
                                       "Do you want to save changes?")
    if answer == "yes":
        save()
    root.destroy()


def export_to_docx(): #model
    doc = Document()
    strings = [text_info.get('1.0', 'end-1c')]
    for string in strings:
        run = doc.add_paragraph(string).add_run()
        fontt = run.font
        fontt.italic = True
    doc.save("C:/Users/vlad0/OneDrive/Документы/tkdoc.docx")


# endregion

# def get_format_text(selected_font: str):
#     text_info.tag_configure(selected_font, font=fonts["selected_font"])
#     current_tags = text_info.tag_names("sel.first")
#     if selected_font in current_tags:
#         text_info.tag_remove(selected_font, "sel.first", "sel.last")
#     else:
#         text_info.tag_add(selected_font, "sel.first", "sel.last")


# region text_format methods
def get_bold_text():
    text_info.tag_configure("bold", font=fonts["bold"])
    current_tags = text_info.tag_names("sel.first")
    if "bold" in current_tags:
        text_info.tag_remove("bold", "sel.first", "sel.last")
    else:
        text_info.tag_add("bold", "sel.first", "sel.last")
    # print(text_info.dump("1.0", tk.END))
    # print(text_info.tag_cget(tagName="bold", option="font"))


def get_italic_text():
    text_info.tag_configure("italic", font=fonts["italic"])
    current_tags = text_info.tag_names("sel.first")
    if "italic" in current_tags:
        text_info.tag_remove("italic", "sel.first", "sel.last")
    else:
        text_info.tag_add("italic", "sel.first", "sel.last")


def get_underline_text():
    text_info.tag_configure("underline", font=fonts["underline"])
    current_tags = text_info.tag_names("sel.first")
    if "underline" in current_tags:
        text_info.tag_remove("underline", "sel.first", "sel.last")
    else:
        text_info.tag_add("underline", "sel.first", "sel.last")


def get_overstrike_text():
    text_info.tag_configure("overstrike", font=fonts["overstrike"])
    current_tags = text_info.tag_names("sel.first")
    if "overstrike" in current_tags:
        text_info.tag_remove("overstrike", "sel.first", "sel.last")
    else:
        text_info.tag_add("overstrike", "sel.first", "sel.last")


# endregion

def change_size(event):
    selected_size = int(event.widget.get())
    text_info.config(font=('Helvetica', selected_size))
    change_fonts(fonts, selected_size)


def change_fonts(fonts: dict, selected_size=int):
    fonts.update({"default": font.Font(size=selected_size),
                  "bold": font.Font(size=selected_size, weight='bold'),
                  "italic": font.Font(size=selected_size, slant='italic'),
                  "underline": font.Font(size=selected_size, underline=1),
                  "overstrike": font.Font(size=selected_size, overstrike=1)})
    text_info.tag_configure("bold", font=fonts["bold"])
    text_info.tag_configure("italic", font=fonts["italic"])
    text_info.tag_configure("underline", font=fonts["underline"])
    text_info.tag_configure("overstrike", font=fonts["overstrike"])


# region stats
def get_stats():
    new_window = tk.Toplevel(root)
    new_window.title("Text statistics")
    new_window.geometry("400x400")
    tk.Label(new_window, text="Statistics").pack()
    st = tk.Text(new_window)
    st.pack()
    st.insert(tk.END, f'Chars: {len(text_info.get("1.0", "end-1c"))}\n')
    space_regex = re.compile(r'\S+')
    space_matches = re.findall(space_regex, text_info.get('1.0', 'end-1c'))
    st.insert(tk.END, f"Words: {len(space_matches)}\n")
    indent_regex = re.compile(r'\n')
    indent_matches = re.findall(indent_regex, text_info.get('1.0', 'end-1c'))
    st.insert(tk.END, f"Indents: {len(indent_matches)}")


# endregion

# region tags methods
def get_format_from_tags(tags: str):
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


def write_tags(file):
    tags = text_info.dump("1.0", tk.END)
    tags_to_str = str(tags).strip('[]')
    file.write(tags_to_str)
    print(tags_to_str)


# endregion

root = tk.Tk()
root.geometry("1200x2400")
root.minsize(400, 400)
root.maxsize(1600, 3200)
root.title("New")
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
fontbar_frame = tk.Frame(root)
fontbar_frame.pack(fill=tk.X)

font_size = 12
fonts = {
    "default": font.Font(size=font_size),
    "bold": font.Font(size=font_size, weight='bold'),
    "italic": font.Font(size=font_size, slant='italic'),
    "underline": font.Font(size=font_size, underline=1),
    "overstrike": font.Font(size=font_size, overstrike=1)
}
#  region create_buttons
bold_button_font = font.Font(size=10, weight='bold')
bold_button = tk.Button(fontbar_frame, text="Bold", font=bold_button_font,
                        command=get_bold_text)
bold_button.pack(side=tk.LEFT)

italic_button_font = font.Font(size=10, slant='italic')
italic_button = tk.Button(fontbar_frame, text="Italic", font=italic_button_font,
                          command=get_italic_text)
italic_button.pack(side=tk.LEFT)

underline_button_font = font.Font(size=10, underline=1)
italic_button = tk.Button(fontbar_frame, text="Underline",
                          font=underline_button_font,
                          command=get_underline_text)
italic_button.pack(side=tk.LEFT)

overstrike_button_font = font.Font(size=10, overstrike=1)
overstrike_button = tk.Button(fontbar_frame, text="Strikeout",
                              font=overstrike_button_font,
                              command=get_overstrike_text)
overstrike_button.pack(side=tk.LEFT)
# endregion
text_info: Text = tk.Text(root, yscrollcommand=scrollbar.set,
                          font=fonts["default"], undo=True)
text_info.pack(fill=tk.BOTH)

scrollbar.config(command=text_info.yview)
# region undo-redo
undo_icon = tk.PhotoImage(file="icons/undo_icon.png").subsample(9, 9)
undo_button = tk.Button(fontbar_frame, image=undo_icon,
                        command=text_info.edit_undo)
redo_icon = tk.PhotoImage(file="icons/redo_icon.png").subsample(26, 26)
redo_button = tk.Button(fontbar_frame, image=redo_icon,
                        command=text_info.edit_redo)

undo_button.pack(side=tk.LEFT)
redo_button.pack(side=tk.LEFT)
# endregion

sizes = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
sizes_combobox = Combobox(fontbar_frame, values=sizes, state="readonly")
sizes_combobox.current(2)
sizes_combobox.pack(side=tk.LEFT)
sizes_combobox.bind("<<ComboboxSelected>>", change_size)

menu = tk.Menu(root)
file_menu = tk.Menu(menu, tearoff=0)
stat_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="New", command=create_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save)
file_menu.add_command(label="Save as", command=save_as_file)
file_menu.add_command(label="Close", command=close_file)
file_menu.add_command(label="To docx", command=export_to_docx)
stat_menu.add_command(label="Show statistics", command=get_stats)
menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Stats", menu=stat_menu)
root.config(menu=menu)
root.mainloop()


class TextWidget:
    pass
