import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

class Sidebar(tb.Frame):
    def __init__(self, master, callbacks):
        super().__init__(master, bootstyle="dark", width=200)
        self.pack_propagate(False)
        self.callbacks = callbacks
        
        # Logo Section
        header = tb.Frame(self, bootstyle="dark", padding=20)
        header.pack(fill=X)
        tb.Label(header, text="KSeF V3", font=("Helvetica", 18, "bold"), bootstyle="inverse-dark").pack()
        tb.Label(header, text="Data Entry Edition", font=("Helvetica", 9), bootstyle="inverse-dark").pack()

        tb.Separator(self, bootstyle="secondary").pack(fill=X, padx=10, pady=15)

        # Action Buttons (Sidebar items)
        menu_items = [
            ("📊 Dashboard", "dashboard"),
            ("📤 Wyślij fakturę", "send"),
            ("📥 Pobierz dane", "receive"),
            ("⚙️ Ustawienia", "settings")
        ]

        for text, key in menu_items:
            btn = tb.Button(
                self, 
                text=text, 
                bootstyle="link", 
                command=lambda k=key: callbacks['menu'](k)
            )
            btn.pack(fill=X, padx=20, pady=5)

class ActionForm(tb.Frame):
    def __init__(self, master, callbacks):
        super().__init__(master, padding=20, relief="solid", borderwidth=1)
        self.callbacks = callbacks
        
        tb.Label(self, text="Nowa Faktura", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=W)

        # Form Fields
        tb.Label(self, text="Numer FV:").grid(row=1, column=0, sticky=W, pady=5)
        self.ent_nr = tb.Entry(self)
        self.ent_nr.grid(row=1, column=1, sticky=EW, pady=5, padx=(10, 0))

        tb.Label(self, text="Data wyst.:").grid(row=2, column=0, sticky=W, pady=5)
        self.ent_date = tb.Entry(self)
        self.ent_date.grid(row=2, column=1, sticky=EW, pady=5, padx=(10, 0))

        tb.Label(self, text="Kontrahent:").grid(row=3, column=0, sticky=W, pady=5)
        self.ent_client = tb.Entry(self)
        self.ent_client.grid(row=3, column=1, sticky=EW, pady=5, padx=(10, 0))

        # Action Buttons
        btn_frame = tb.Frame(self)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky=EW)
        
        self.btn_send = tb.Button(btn_frame, text="Wyślij do KSeF", bootstyle="success", command=self.handle_send)
        self.btn_send.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        
        self.btn_clear = tb.Button(btn_frame, text="Wyczyść", bootstyle="secondary", command=self.clear_fields)
        self.btn_clear.pack(side=LEFT, fill=X, expand=True, padx=(5, 0))

        self.columnconfigure(1, weight=1)

    def handle_send(self):
        data = {
            "nr": self.ent_nr.get(),
            "date": self.ent_date.get(),
            "client": self.ent_client.get()
        }
        self.callbacks['send_invoice'](data)
        self.clear_fields()

    def clear_fields(self):
        self.ent_nr.delete(0, END)
        self.ent_date.delete(0, END)
        self.ent_client.delete(0, END)

class MainDashboard(tb.Frame):
    def __init__(self, master, callbacks):
        super().__init__(master, padding=20)
        self.callbacks = callbacks

        # Top Controls (Edit, Delete, Theme)
        self.top_controls = tb.Frame(self)
        self.top_controls.pack(fill=X, pady=(0, 20))

        self.btn_edit = tb.Button(self.top_controls, text="Edytuj", bootstyle="outline-primary", width=10, command=callbacks['edit'])
        self.btn_edit.pack(side=LEFT, padx=(0, 10))

        self.btn_delete = tb.Button(self.top_controls, text="Usuń", bootstyle="outline-danger", width=10, command=callbacks['delete'])
        self.btn_delete.pack(side=LEFT)

        # Theme Switcher (from reference)
        theme_frame = tb.Frame(self.top_controls)
        theme_frame.pack(side=RIGHT)
        
        tb.Label(theme_frame, text="Motyw:").pack(side=LEFT, padx=5)
        self.combo_theme = tb.Combobox(theme_frame, state="readonly", width=15)
        self.combo_theme.pack(side=LEFT)
        self.combo_theme.bind("<<ComboboxSelected>>", self.callbacks['change_theme'])

        # Main Layout (Form + Table)
        inner_container = tb.Frame(self)
        inner_container.pack(fill=BOTH, expand=True)

        # Left: Form
        self.action_form = ActionForm(inner_container, callbacks)
        self.action_form.pack(side=LEFT, fill=Y, padx=(0, 20))

        # Right: Table
        self.coldata = [
            {"text": "Numer", "stretch": True},
            {"text": "Data", "stretch": False, "width": 120},
            {"text": "Kontrahent", "stretch": True},
            {"text": "Status", "stretch": False, "width": 100},
        ]
        self.table = Tableview(
            master=inner_container,
            coldata=self.coldata,
            rowdata=[],
            paginated=True,
            searchable=True,
            bootstyle="info",
            height=15
        )
        self.table.pack(side=LEFT, fill=BOTH, expand=True)

    def set_table_data(self, data):
        self.table.build_table_data(coldata=self.coldata, rowdata=data)

class KSeFViewV3(tb.Window):
    def __init__(self, callbacks, themes):
        super().__init__(
            title="KSeF Client V3 - Professional Data Entry",
            themename="darkly",
            size=(1200, 750),
            resizable=(True, True)
        )
        self.callbacks = callbacks
        self.themes = themes
        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        self.sidebar = Sidebar(self, self.callbacks)
        self.sidebar.pack(side=LEFT, fill=Y)

        # Main Workspace Container
        self.workspace = tb.Frame(self)
        self.workspace.pack(side=RIGHT, fill=BOTH, expand=True)

        # Top Bar (Status)
        self.top_bar = tb.Frame(self.workspace, padding=10)
        self.top_bar.pack(fill=X)
        
        self.lbl_status = tb.Label(self.top_bar, text="🔴 Sesja nieaktywna", bootstyle="danger", font=("Helvetica", 10, "bold"))
        self.lbl_status.pack(side=RIGHT, padx=20)
        
        self.lbl_info = tb.Label(self.top_bar, text="Ready", font=("Helvetica", 10, "italic"), bootstyle="secondary")
        self.lbl_info.pack(side=LEFT, padx=20)

        tb.Separator(self.workspace, bootstyle="secondary").pack(fill=X)

        # Dashboard View
        self.dashboard = MainDashboard(self.workspace, self.callbacks)
        self.dashboard.pack(fill=BOTH, expand=True)
        
        # Populate themes
        self.dashboard.combo_theme.configure(values=self.themes)
        self.dashboard.combo_theme.set(self.style.theme.name)

        # Footer / Log
        self.footer = tb.Frame(self.workspace, bootstyle="secondary", padding=5)
        self.footer.pack(fill=X, side=BOTTOM)
        self.lbl_log = tb.Label(self.footer, text="Czekam na akcję...", bootstyle="inverse-secondary", font=("Consolas", 8))
        self.lbl_log.pack(side=LEFT, padx=10)

    def update_state(self, model):
        # Update Status Bar
        if model.is_logged_in:
            self.lbl_status.configure(text="🟢 Zalogowano", bootstyle="success")
        else:
            self.lbl_status.configure(text="🔴 Sesja nieaktywna", bootstyle="danger")
        
        self.lbl_info.configure(text=model.last_operation)
        self.lbl_log.configure(text=f"Log: {model.last_operation}")
        
        # Update Table
        self.dashboard.set_table_data(model.invoices)

    def change_theme(self, theme_name):
        self.style.theme_use(theme_name)
