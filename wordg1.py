import os
import random
import string
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk


class WordlistApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Beginner-Friendly Wordlist Studio")
    self.root.geometry("720x780")
    self.root.configure(bg="#0f111a")

    # --- Modern Cyberpunk Palette ---
    self.bg_color = "#0f111a"
    self.panel_bg = "#161925"
    self.fg_color = "#e2e8f0"
    self.accent_color = "#00f5d4"
    self.accent_hover = "#70c1b3"
    self.entry_bg = "#1e2230"
    self.entry_fg = "#00f5d4"
    self.desc_color = "#8f9bb3"
    self.console_fg = "#38bdf8"

    self.apply_ttk_styles()
    self.create_widgets()

  def apply_ttk_styles(self):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "TProgressbar",
        thickness=12,
        troughcolor=self.entry_bg,
        background=self.accent_color,
        bordercolor=self.panel_bg,
        lightcolor=self.accent_color,
        darkcolor=self.accent_color,
    )
    # Custom Notebook & Tab styling
    style.configure("TNotebook", background=self.bg_color, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=self.panel_bg,
        foreground=self.fg_color,
        font=("Consolas", 8, "bold"),
        padding=[10, 6],
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", self.accent_color)],
        foreground=[("selected", "#0f111a")],
    )

  def create_widgets(self):
    # Title Header
    title_label = tk.Label(
        self.root,
        text="⚡ WORDLIST STUDIO (Beginner Friendly) ⚡",
        font=("Consolas", 11, "bold"),
        bg=self.bg_color,
        fg=self.accent_color,
    )
    title_label.pack(pady=4)

    # Main Frame container
    main_frame = tk.Frame(self.root, bg=self.bg_color)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=2)

    # --- Notebook Tabs ---
    self.notebook = ttk.Notebook(main_frame)
    self.notebook.pack(fill=tk.BOTH, expand=True, pady=2)

    # Create Tab Frames
    self.tab_inputs = tk.Frame(self.notebook, bg=self.panel_bg)
    self.tab_numbers = tk.Frame(self.notebook, bg=self.panel_bg)
    self.tab_symbols = tk.Frame(self.notebook, bg=self.panel_bg)
    self.tab_rules = tk.Frame(self.notebook, bg=self.panel_bg)

    self.notebook.add(self.tab_inputs, text="📁 1. Starting Words")
    self.notebook.add(self.tab_numbers, text="🔢 2. Add Numbers")
    self.notebook.add(self.tab_symbols, text="🔣 3. Add Symbols")
    self.notebook.add(self.tab_rules, text="⚙️ 4. Styles & Setup")

    # ==================== TAB 1: Starting Words ====================
    file_frame = tk.LabelFrame(
        self.tab_inputs,
        text=" Choose Where Your Starting Words Come From ",
        bg=self.panel_bg,
        fg=self.accent_color,
        font=("Consolas", 9, "bold"),
        bd=2,
        relief="groove",
    )
    file_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6, ipady=4)

    self.input_entry = self.add_file_row(
        file_frame,
        "📥 Text File:",
        "neword.txt",
        is_input=True,
        hint="Load an existing text file with words",
    )
    self.output_entry = self.add_file_row(
        file_frame,
        "📤 Save File As:",
        "klk.txt",
        is_input=False,
        hint="Name of your final output file",
    )
    self.manual_words_entry = self.add_input_row(
        file_frame,
        "✍️ Type Words:",
        "Type words separated by spaces or commas",
    )

    # Random Words Subsection Controls
    rand_chk_row = tk.Frame(file_frame, bg=self.panel_bg)
    rand_chk_row.pack(fill=tk.X, padx=6, pady=3)
    self.opt_random_words_var = tk.BooleanVar(value=False)
    tk.Checkbutton(
        rand_chk_row,
        text="🎲 Make Random Words",
        variable=self.opt_random_words_var,
        bg=self.panel_bg,
        fg=self.fg_color,
        selectcolor=self.entry_bg,
        activebackground=self.panel_bg,
        activeforeground=self.accent_color,
        width=22,
        anchor="w",
        font=("Consolas", 8, "bold"),
    ).pack(side=tk.LEFT)
    tk.Label(
        rand_chk_row,
        text="-> Let the computer create random letter combinations",
        bg=self.panel_bg,
        fg=self.desc_color,
        font=("Consolas", 8),
    ).pack(side=tk.LEFT)

    # Random Word Parameters (Count & Length Range - Cleared)
    rand_param_row = tk.Frame(file_frame, bg=self.panel_bg)
    rand_param_row.pack(fill=tk.X, padx=6, pady=3)
    tk.Label(
        rand_param_row,
        text="🔢 Random Count / Len:",
        width=22,
        anchor="w",
        bg=self.panel_bg,
        fg=self.fg_color,
        font=("Consolas", 8),
    ).pack(side=tk.LEFT)

    self.rand_count_entry = tk.Entry(
        rand_param_row,
        width=5,
        bg=self.entry_bg,
        fg=self.entry_fg,
        insertbackground="white",
        font=("Consolas", 9),
    )
    self.rand_count_entry.pack(side=tk.LEFT, padx=2)
    tk.Label(
        rand_param_row, text="words, size", bg=self.panel_bg, fg=self.fg_color
    ).pack(side=tk.LEFT)

    self.rand_min_len_entry = tk.Entry(
        rand_param_row,
        width=3,
        bg=self.entry_bg,
        fg=self.entry_fg,
        insertbackground="white",
        font=("Consolas", 9),
    )
    self.rand_min_len_entry.pack(side=tk.LEFT, padx=2)
    tk.Label(rand_param_row, text="to", bg=self.panel_bg, fg=self.fg_color).pack(
        side=tk.LEFT
    )
    self.rand_max_len_entry = tk.Entry(
        rand_param_row,
        width=3,
        bg=self.entry_bg,
        fg=self.entry_fg,
        insertbackground="white",
        font=("Consolas", 9),
    )
    self.rand_max_len_entry.pack(side=tk.LEFT, padx=2)
    tk.Label(
        rand_param_row,
        text="letters long",
        bg=self.panel_bg,
        fg=self.desc_color,
        font=("Consolas", 8),
    ).pack(side=tk.LEFT, padx=4)

    len_row = tk.Frame(file_frame, bg=self.panel_bg)
    len_row.pack(fill=tk.X, padx=6, pady=3)
    tk.Label(
        len_row,
        text="📏 Word Length Filter:",
        width=22,
        anchor="w",
        bg=self.panel_bg,
        fg=self.fg_color,
        font=("Consolas", 8),
    ).pack(side=tk.LEFT)
    self.min_len_entry = tk.Entry(
        len_row,
        width=5,
        bg=self.entry_bg,
        fg=self.entry_fg,
        insertbackground="white",
        font=("Consolas", 9),
    )
    self.min_len_entry.pack(side=tk.LEFT, padx=2)
    tk.Label(len_row, text="to", bg=self.panel_bg, fg=self.fg_color).pack(
        side=tk.LEFT
    )
    self.max_len_entry = tk.Entry(
        len_row,
        width=5,
        bg=self.entry_bg,
        fg=self.entry_fg,
        insertbackground="white",
        font=("Consolas", 9),
    )
    self.max_len_entry.pack(side=tk.LEFT, padx=2)
    tk.Label(
        len_row,
        text="(Keep words within this length)",
        bg=self.panel_bg,
        fg=self.desc_color,
        font=("Consolas", 8),
    ).pack(side=tk.LEFT, padx=4)

    self.custom_prefix_entry = self.add_input_row(
        file_frame,
        "📌 Fixed Start Prefix:",
        "Optional text added to the very beginning of every word",
    )

    # ==================== TAB 2: Add Numbers ====================
    num_frame = tk.LabelFrame(
        self.tab_numbers,
        text=" Select Number Options to Append or Insert ",
        bg=self.panel_bg,
        fg=self.accent_color,
        font=("Consolas", 9, "bold"),
        bd=2,
        relief="groove",
    )
    num_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6, ipady=4)

    self.opt_use_numbers_var = tk.BooleanVar(value=False)
    self.num_single_var = tk.BooleanVar(value=False)
    self.num_double_var = tk.BooleanVar(value=False)
    self.num_years_var = tk.BooleanVar(value=False)
    self.num_custom_var = tk.BooleanVar(value=False)

    def add_num_chk(parent, text, var, desc):
      row = tk.Frame(parent, bg=self.panel_bg)
      row.pack(fill=tk.X, padx=8, pady=4)
      tk.Checkbutton(
          row,
          text=text,
          variable=var,
          bg=self.panel_bg,
          fg=self.fg_color,
          selectcolor=self.entry_bg,
          activebackground=self.panel_bg,
          activeforeground=self.accent_color,
          width=24,
          anchor="w",
          font=("Consolas", 8),
      ).pack(side=tk.LEFT)
      tk.Label(
          row,
          text=desc,
          bg=self.panel_bg,
          fg=self.desc_color,
          font=("Consolas", 8),
      ).pack(side=tk.LEFT)

    add_num_chk(
        num_frame,
        "🔢 Turn On Numbers",
        self.opt_use_numbers_var,
        "-> Master switch: Check this to add numbers",
    )
    add_num_chk(
        num_frame,
        "  🔹 Single Digits",
        self.num_single_var,
        "-> Add numbers from 0 to 9",
    )
    add_num_chk(
        num_frame,
        "  🔹 Double Digits",
        self.num_double_var,
        "-> Add numbers from 00 to 99",
    )
    add_num_chk(
        num_frame,
        "  📅 Common Years",
        self.num_years_var,
        "-> Add years from 2020 to 2030",
    )
    add_num_chk(
        num_frame,
        "  ⚙️ Custom Range",
        self.num_custom_var,
        "-> Use your own custom number range below",
    )

    num_range_row = tk.Frame(num_frame, bg=self.panel_bg)
    num_range_row.pack(fill=tk.X, padx=8, pady=4)
    tk.Label(
        num_range_row,
        text="🔢 Custom Number Range:",
        width=24,
        anchor="w",
        bg=self.panel_bg,
        fg=self.fg_color,
        font=("Consolas", 8),
    ).pack(side=tk.LEFT)

    self.min_num_entry = tk.Entry(
        num_range_row,
        width=5,
        bg=self.entry_bg,
        fg=self.entry_fg,
        insertbackground="white",
        font=("Consolas", 9),
    )
    self.min_num_entry.pack(side=tk.LEFT, padx=2)
    tk.Label(num_range_row, text="to", bg=self.panel_bg, fg=self.fg_color).pack(
        side=tk.LEFT
    )
    self.max_num_entry = tk.Entry(
        num_range_row,
        width=6,
        bg=self.entry_bg,
        fg=self.entry_fg,
        insertbackground="white",
        font=("Consolas", 9),
    )
    self.max_num_entry.pack(side=tk.LEFT, padx=2)
    tk.Label(
        num_range_row,
        text="(Example: 0 to 9999)",
        bg=self.panel_bg,
        fg=self.desc_color,
        font=("Consolas", 8),
    ).pack(side=tk.LEFT, padx=4)

    # ==================== TAB 3: Add Symbols ====================
    sym_frame = tk.LabelFrame(
        self.tab_symbols,
        text=" Select Special Characters / Symbols ",
        bg=self.panel_bg,
        fg=self.accent_color,
        font=("Consolas", 9, "bold"),
        bd=2,
        relief="groove",
    )
    sym_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6, ipady=4)

    self.opt_use_symbols_var = tk.BooleanVar(value=False)
    self.sym_excl_var = tk.BooleanVar(value=False)
    self.sym_at_var = tk.BooleanVar(value=False)
    self.sym_hash_var = tk.BooleanVar(value=False)
    self.sym_doll_var = tk.BooleanVar(value=False)
    self.sym_perc_var = tk.BooleanVar(value=False)
    self.sym_amp_var = tk.BooleanVar(value=False)
    self.sym_star_var = tk.BooleanVar(value=False)
    self.sym_q_var = tk.BooleanVar(value=False)
    self.sym_under_var = tk.BooleanVar(value=False)
    self.sym_dash_var = tk.BooleanVar(value=False)

    add_num_chk(
        sym_frame,
        "🔣 Turn On Symbols",
        self.opt_use_symbols_var,
        "-> Master switch: Check this to add symbols",
    )

    grid_frame = tk.Frame(sym_frame, bg=self.panel_bg)
    grid_frame.pack(fill=tk.X, padx=8, pady=4)

    syms_defs = [
        ("❗ (!) Exclamation", self.sym_excl_var),
        ("👤 (@) At Sign", self.sym_at_var),
        ("#️⃣ (#) Hash/Pound", self.sym_hash_var),
        ("💵 ($) Dollar", self.sym_doll_var),
        ("📊 (%) Percent", self.sym_perc_var),
        ("🔗 (&) Ampersand", self.sym_amp_var),
        ("⭐ (*) Asterisk", self.sym_star_var),
        ("❓ (?) Question", self.sym_q_var),
        ("___ (_) Underscore", self.sym_under_var),
        ("➖ (-) Hyphen", self.sym_dash_var),
    ]

    for idx, (s_text, s_var) in enumerate(syms_defs):
      r = idx // 2
      c = idx % 2
      chk = tk.Checkbutton(
          grid_frame,
          text=s_text,
          variable=s_var,
          bg=self.panel_bg,
          fg=self.fg_color,
          selectcolor=self.entry_bg,
          activebackground=self.panel_bg,
          activeforeground=self.accent_color,
          anchor="w",
          width=22,
          font=("Consolas", 8),
      )
      chk.grid(row=r, column=c, sticky="w", padx=4, pady=3)

    self.custom_syms_entry = self.add_input_row(
        sym_frame,
        "➕ Extra Symbols:",
        "Type any custom symbols (e.g., +=/)",
    )

    # ==================== TAB 4: Styles & Setup ====================
    placement_frame = tk.LabelFrame(
        self.tab_rules,
        text=" Word Formatting & Where Numbers/Symbols Go ",
        bg=self.panel_bg,
        fg=self.accent_color,
        font=("Consolas", 9, "bold"),
        bd=2,
        relief="groove",
    )
    placement_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6, ipady=4)

    self.append_var = tk.BooleanVar(value=False)
    self.opt_lowercase_var = tk.BooleanVar(value=False)
    self.opt_capitalize_var = tk.BooleanVar(value=False)
    self.opt_uppercase_var = tk.BooleanVar(value=False)
    self.opt_reverse_var = tk.BooleanVar(value=False)
    self.opt_leet_var = tk.BooleanVar(value=False)

    self.pos_num_suffix_var = tk.BooleanVar(value=False)
    self.pos_num_prefix_var = tk.BooleanVar(value=False)
    self.pos_num_middle_var = tk.BooleanVar(value=False)

    self.pos_sym_suffix_var = tk.BooleanVar(value=False)
    self.pos_sym_prefix_var = tk.BooleanVar(value=False)
    self.pos_sym_wrapped_var = tk.BooleanVar(value=False)
    self.pos_sym_middle_var = tk.BooleanVar(value=False)

    add_num_chk(
        placement_frame,
        "📁 Append to File",
        self.append_var,
        "-> Add words to an existing file instead of replacing",
    )
    add_num_chk(
        placement_frame,
        "🔤 Keep Lowercase",
        self.opt_lowercase_var,
        "-> Keep letters small (e.g., word)",
    )
    add_num_chk(
        placement_frame,
        "🔠 Capitalize Word",
        self.opt_capitalize_var,
        "-> Make first letter big (e.g., Word)",
    )
    add_num_chk(
        placement_frame,
        "🔠 Uppercase Word",
        self.opt_uppercase_var,
        "-> Make all letters big (e.g., WORD)",
    )
    add_num_chk(
        placement_frame,
        "🔄 Reverse Word",
        self.opt_reverse_var,
        "-> Spell the word backwards (e.g., drow)",
    )
    add_num_chk(
        placement_frame,
        "💻 Leet Speak (1337)",
        self.opt_leet_var,
        "-> Replace letters with numbers (e.g., e->3, a->4)",
    )

    add_num_chk(
        placement_frame,
        "  📍 Put Number at End",
        self.pos_num_suffix_var,
        "-> Example: word123",
    )
    add_num_chk(
        placement_frame,
        "  📍 Put Number at Start",
        self.pos_num_prefix_var,
        "-> Example: 123word",
    )
    add_num_chk(
        placement_frame,
        "  📍 Put Number in Middle",
        self.pos_num_middle_var,
        "-> Example: wo123rd",
    )
    add_num_chk(
        placement_frame,
        "  📌 Put Symbol at End",
        self.pos_sym_suffix_var,
        "-> Example: word!",
    )
    add_num_chk(
        placement_frame,
        "  📌 Put Symbol at Start",
        self.pos_sym_prefix_var,
        "-> Example: !word",
    )
    add_num_chk(
        placement_frame,
        "  📌 Wrap Symbol Both Sides",
        self.pos_sym_wrapped_var,
        "-> Example: !word!",
    )
    add_num_chk(
        placement_frame,
        "  📌 Put Symbol in Middle",
        self.pos_sym_middle_var,
        "-> Example: wo!rd",
    )

    # Duplicate Multiplier Configuration Row (Cleared)
    dup_row = tk.Frame(placement_frame, bg=self.panel_bg)
    dup_row.pack(fill=tk.X, padx=8, pady=4)
    tk.Label(
        dup_row,
        text="🔁 Repeat Each Line:",
        width=24,
        anchor="w",
        bg=self.panel_bg,
        fg=self.accent_color,
        font=("Consolas", 8, "bold"),
    ).pack(side=tk.LEFT)

    self.duplicate_entry = tk.Entry(
        dup_row,
        width=5,
        bg=self.entry_bg,
        fg=self.entry_fg,
        insertbackground="white",
        font=("Consolas", 9, "bold"),
    )
    self.duplicate_entry.pack(side=tk.LEFT, padx=2)
    tk.Label(
        dup_row,
        text="(How many times to repeat each generated line)",
        bg=self.panel_bg,
        fg=self.desc_color,
        font=("Consolas", 8),
    ).pack(side=tk.LEFT, padx=4)

    # --- Action Button, Progress Bar & Console Log (Always Visible Below Tabs) ---
    self.generate_btn = tk.Button(
        main_frame,
        text="⚡ START GENERATING WORDLIST ⚡",
        command=self.start_generation_thread,
        bg=self.accent_color,
        fg="#0f111a",
        font=("Consolas", 9, "bold"),
        cursor="hand2",
        activebackground=self.accent_hover,
        activeforeground="#0f111a",
        bd=0,
        relief="flat",
    )
    self.generate_btn.pack(fill=tk.X, padx=2, pady=4, ipady=3)

    # Live Status Display Label
    self.status_label = tk.Label(
        main_frame,
        text="📌 Status: Ready. Pick your settings and click generate!",
        bg=self.bg_color,
        fg=self.accent_color,
        font=("Consolas", 8, "bold"),
        anchor="w",
    )
    self.status_label.pack(fill=tk.X, padx=2, pady=1)

    self.progress_bar = ttk.Progressbar(
        main_frame, orient="horizontal", mode="determinate"
    )
    self.progress_bar.pack(fill=tk.X, padx=2, pady=1)

    self.log_box = scrolledtext.ScrolledText(
        main_frame,
        height=3,
        bg="#0b0d14",
        fg=self.console_fg,
        font=("Consolas", 8),
        insertbackground="white",
        bd=1,
        relief="solid",
    )
    self.log_box.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    self.log_box.insert(
        tk.END,
        "[+] Ready! Go through tabs 1 to 4, check the options you want, and"
        " hit generate.\n",
    )

  def add_file_row(self, parent, label_text, default_val, is_input, hint):
    frame = tk.Frame(parent, bg=self.panel_bg)
    frame.pack(fill=tk.X, padx=8, pady=3)
    tk.Label(
        frame,
        text=label_text,
        width=16,
        anchor="w",
        bg=self.panel_bg,
        fg=self.fg_color,
        font=("Consolas", 8),
    ).pack(side=tk.LEFT)
    entry = tk.Entry(
        frame,
        bg=self.entry_bg,
        fg=self.entry_fg,
        insertbackground="white",
        font=("Consolas", 9),
    )
    entry.insert(0, default_val)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

    btn = tk.Button(
        frame,
        text="Browse",
        command=lambda: self.browse_file(entry, is_input),
        bg="#272d40",
        fg="white",
        font=("Consolas", 8),
        activebackground=self.accent_color,
        activeforeground="#0f111a",
        bd=0,
        cursor="hand2",
    )
    btn.pack(side=tk.RIGHT)
    return entry

  def add_input_row(self, parent, label_text, placeholder):
    frame = tk.Frame(parent, bg=self.panel_bg)
    frame.pack(fill=tk.X, padx=8, pady=3)
    tk.Label(
        frame,
        text=label_text,
        width=16,
        anchor="w",
        bg=self.panel_bg,
        fg=self.fg_color,
        font=("Consolas", 8),
    ).pack(side=tk.LEFT)
    entry = tk.Entry(
        frame,
        bg=self.entry_bg,
        fg=self.entry_fg,
        insertbackground="white",
        font=("Consolas", 9),
    )
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
    tk.Label(
        frame,
        text=placeholder,
        bg=self.panel_bg,
        fg=self.desc_color,
        font=("Consolas", 8),
    ).pack(side=tk.RIGHT)
    return entry

  def browse_file(self, entry_widget, is_input):
    if is_input:
      filename = filedialog.askopenfilename(title="Select Starting Wordlist File")
    else:
      filename = filedialog.asksavefilename(
          title="Save Output File", defaultextension=".txt"
      )
    if filename:
      entry_widget.delete(0, tk.END)
      entry_widget.insert(0, filename)

  def log(self, message):
    self.root.after(0, lambda: self._safe_log(message))

  def _safe_log(self, message):
    self.log_box.insert(tk.END, message + "\n")
    self.log_box.see(tk.END)

  def update_live_status(self, current, max_val, word_preview):
    self.root.after(
        0,
        lambda: [
            self.progress_bar.config(maximum=max_val, value=current),
            self.status_label.config(
                text=(
                    f"⚡ Processing [{current}/{max_val}] -> Current Word:"
                    f" '{word_preview}'"
                )
            ),
        ],
    )

  def start_generation_thread(self):
    self.generate_btn.config(state=tk.DISABLED, bg="#272d40", fg="#8f9bb3")
    self.progress_bar["value"] = 0
    threading.Thread(target=self.run_generator, daemon=True).start()

  def apply_leet(self, word):
    leet_map = {
        "a": "4",
        "e": "3",
        "i": "1",
        "o": "0",
        "s": "$",
        "t": "7",
        "A": "4",
        "E": "3",
        "I": "1",
        "O": "0",
        "S": "$",
        "T": "7",
    }
    return "".join(leet_map.get(c, c) for c in word)

  def run_generator(self):
    try:
      input_file = self.input_entry.get().strip()
      output_file = self.output_entry.get().strip() or "klk.txt"
      manual_input = self.manual_words_entry.get().strip()
      custom_prefix = self.custom_prefix_entry.get().strip()

      try:
        dup_count = int(self.duplicate_entry.get().strip())
      except ValueError:
        dup_count = 1
      if dup_count < 1:
        dup_count = 1

      all_words = []

      # 1. Read input file
      if input_file and os.path.exists(input_file):
        self.log(f"[+] Reading starting file: '{input_file}'...")
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
          file_words = [line.strip() for line in f if line.strip()]
          all_words.extend(file_words)

      # 2. Read manual words
      if manual_input:
        self.log(f"[+] Adding typed words: '{manual_input}'...")
        manual_list = [
            w.strip()
            for w in manual_input.replace(",", " ").split()
            if w.strip()
        ]
        all_words.extend(manual_list)

      # 3. Generate random words if enabled
      if self.opt_random_words_var.get():
        try:
          rand_count = int(self.rand_count_entry.get().strip())
        except ValueError:
          rand_count = 500
        try:
          rand_min = int(self.rand_min_len_entry.get().strip())
        except ValueError:
          rand_min = 4
        try:
          rand_max = int(self.rand_max_len_entry.get().strip())
        except ValueError:
          rand_max = 7

        if rand_min > rand_max:
          rand_min, rand_max = rand_max, rand_min

        self.log(
            f"[+] Creating {rand_count} random words (length"
            f" {rand_min}-{rand_max})..."
        )
        for _ in range(rand_count):
          length = random.randint(rand_min, rand_max)
          rand_word = "".join(
              random.choices(string.ascii_lowercase, k=length)
          )
          all_words.append(rand_word)

      if not all_words:
        self.log(
            "[-] Error: No starting words found! Please choose a file, type"
            " words, or enable random words in Tab 1."
        )
        self.root.after(
            0,
            lambda: self.generate_btn.config(
                state=tk.NORMAL, bg=self.accent_color, fg="#0f111a"
            ),
        )
        self.root.after(
            0,
            lambda: self.status_label.config(
                text="❌ Error: No starting words provided!"
            ),
        )
        return

      # Length filter
      try:
        min_l = int(self.min_len_entry.get().strip())
      except ValueError:
        min_l = 0
      try:
        max_l = int(self.max_len_entry.get().strip())
      except ValueError:
        max_l = 99

      words = sorted(
          list(set([w for w in all_words if min_l <= len(w) <= max_l]))
      )

      if not words:
        self.log(
            f"[-] Error: No words match the length range {min_l}-{max_l}!"
        )
        self.root.after(
            0,
            lambda: self.generate_btn.config(
                state=tk.NORMAL, bg=self.accent_color, fg="#0f111a"
            ),
        )
        self.root.after(
            0,
            lambda: self.status_label.config(text="❌ Error: Length mismatch!"),
        )
        return

      # --- Build Number Pool ---
      number_pool = []
      if self.opt_use_numbers_var.get():
        if self.num_single_var.get():
          number_pool.extend([str(i) for i in range(0, 10)])
        if self.num_double_var.get():
          number_pool.extend([f"{i:02d}" for i in range(0, 100)])
        if self.num_years_var.get():
          number_pool.extend([str(i) for i in range(2020, 2031)])
        if self.num_custom_var.get():
          try:
            min_n = int(self.min_num_entry.get().strip())
          except ValueError:
            min_n = 0
          try:
            max_n = int(self.max_num_entry.get().strip())
          except ValueError:
            max_n = 9999
          if min_n > max_n:
            min_n, max_n = max_n, min_n
          number_pool.extend([str(i) for i in range(min_n, max_n + 1)])
        number_pool = list(dict.fromkeys(number_pool))

      # --- Build Symbol Pool ---
      symbols = []
      if self.opt_use_symbols_var.get():
        if self.sym_excl_var.get():
          symbols.append("!")
        if self.sym_at_var.get():
          symbols.append("@")
        if self.sym_hash_var.get():
          symbols.append("#")
        if self.sym_doll_var.get():
          symbols.append("$")
        if self.sym_perc_var.get():
          symbols.append("%")
        if self.sym_amp_var.get():
          symbols.append("&")
        if self.sym_star_var.get():
          symbols.append("*")
        if self.sym_q_var.get():
          symbols.append("?")
        if self.sym_under_var.get():
          symbols.append("_")
        if self.sym_dash_var.get():
          symbols.append("-")

        custom_syms_str = self.custom_syms_entry.get().strip()
        if custom_syms_str:
          symbols.extend(list(custom_syms_str))
        symbols = list(dict.fromkeys(symbols))

      # Options flags
      do_append = self.append_var.get()
      use_lowercase = self.opt_lowercase_var.get()
      use_capitalize = self.opt_capitalize_var.get()
      use_uppercase = self.opt_uppercase_var.get()
      use_reverse = self.opt_reverse_var.get()
      use_leet = self.opt_leet_var.get()

      num_suffix = self.pos_num_suffix_var.get()
      num_prefix = self.pos_num_prefix_var.get()
      num_middle = self.pos_num_middle_var.get()

      sym_suffix = self.pos_sym_suffix_var.get()
      sym_prefix = self.pos_sym_prefix_var.get()
      sym_wrapped = self.pos_sym_wrapped_var.get()
      sym_middle = self.pos_sym_middle_var.get()

      if (
          not use_lowercase
          and not use_capitalize
          and not use_uppercase
          and not use_reverse
          and not use_leet
      ):
        self.log(
            "[-] Error: Please select at least one word style checkbox in"
            " Tab 4!"
        )
        self.root.after(
            0,
            lambda: self.generate_btn.config(
                state=tk.NORMAL, bg=self.accent_color, fg="#0f111a"
            ),
        )
        return

      # Build base variants list
      raw_variants = []
      for base_raw in words:
        if use_lowercase:
          raw_variants.append(base_raw.lower())
        if use_capitalize:
          raw_variants.append(base_raw.capitalize())
        if use_uppercase:
          raw_variants.append(base_raw.upper())
        if use_reverse:
          raw_variants.append(base_raw[::-1])

      base_variants = []
      for v in raw_variants:
        base_variants.append(v)
        if use_leet:
          leet_v = self.apply_leet(v)
          if leet_v != v:
            base_variants.append(leet_v)

      base_variants = list(dict.fromkeys(base_variants))
      total_variants = len(base_variants)

      self.log(
          f"[+] Generating wordlist across {total_variants} base words"
          f" (Repeat multiplier: {dup_count}x) -> Saving to '{output_file}'..."
      )

      current_step = 0
      file_mode = "a" if do_append and os.path.exists(output_file) else "w"
      buffer_size = 10000
      line_buffer = []

      with open(output_file, file_mode, encoding="utf-8") as out:
        for idx, base in enumerate(base_variants):
          full_base = f"{custom_prefix}{base}"

          self.update_live_status(current_step + 1, total_variants, full_base)

          def append_lines(text):
            for _ in range(dup_count):
              line_buffer.append(text + "\n")

          append_lines(full_base)

          if self.opt_use_numbers_var.get() and number_pool:
            for num in number_pool:
              if num_suffix:
                append_lines(f"{full_base}{num}")
              if num_prefix:
                append_lines(f"{custom_prefix}{num}{base}")
              if num_middle and len(base) > 1:
                mid = len(base) // 2
                append_lines(f"{custom_prefix}{base[:mid]}{num}{base[mid:]}")

          if self.opt_use_symbols_var.get() and symbols:
            for sym1 in symbols:
              if sym_suffix:
                append_lines(f"{full_base}{sym1}")
              if sym_prefix:
                append_lines(f"{custom_prefix}{sym1}{base}")
              if sym_middle and len(base) > 1:
                mid = len(base) // 2
                append_lines(f"{custom_prefix}{base[:mid]}{sym1}{base[mid:]}")
              for sym2 in symbols:
                if sym_wrapped:
                  append_lines(f"{custom_prefix}{sym1}{base}{sym2}")

          if len(line_buffer) >= buffer_size:
            out.writelines(line_buffer)
            line_buffer.clear()

          current_step += 1

        if line_buffer:
          out.writelines(line_buffer)

      self.log(
          f"=== SUCCESS! Wordlist successfully saved to '{output_file}' ==="
      )
      self.root.after(
          0,
          lambda: self.status_label.config(text="✅ Success! Wordlist is ready."),
      )
      self.root.after(
          0,
          lambda: messagebox.showinfo(
              "Success", f"Wordlist successfully saved to '{output_file}'!"
          ),
      )

    except Exception as e:
      self.log(f"[-] Error: {str(e)}")
      self.root.after(
          0, lambda: self.status_label.config(text=f"❌ Error: {str(e)}")
      )
      self.root.after(
          0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}")
      )

    finally:
      self.root.after(
          0,
          lambda: self.generate_btn.config(
              state=tk.NORMAL, bg=self.accent_color, fg="#0f111a"
          ),
      )


if __name__ == "__main__":
  root = tk.Tk()
  app = WordlistApp(root)
  root.mainloop()
