from .base_plugin import BasePlugin
import tkinter as tk
import re


class StatisticsPlugin(BasePlugin):
    def install(self):
        stat_menu = tk.Menu(self.view.menu, tearoff=0)
        stat_menu.add_command(label="Show statistics",
                              command=self.get_stats)
        self.view.menu.add_cascade(label="Stats", menu=stat_menu)

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
                                    self.view.text_info.get('1.0',
                                                            'end-1c'))
        st.insert(tk.END, f"Indents: {len(indent_matches)}")
