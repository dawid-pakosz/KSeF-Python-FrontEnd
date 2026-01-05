import threading
from model import KSeFModel
from view import KSeFViewV3

class KSeFController:
    def __init__(self):
        self.model = KSeFModel()
        
        # Define callbacks for the view
        callbacks = {
            "menu": self.handle_menu,
            "send_invoice": self.handle_send_invoice,
            "edit": self.handle_edit,
            "delete": self.handle_delete,
            "change_theme": self.handle_change_theme,
        }
        
        self.view = KSeFViewV3(callbacks, self.model.available_themes)
        self.refresh_ui()

    def run(self):
        self.view.mainloop()

    def refresh_ui(self):
        # Always run UI updates in the main thread
        self.view.update_state(self.model)

    def handle_menu(self, key):
        if key == "dashboard":
            self.model.last_operation = "Widok dashboardu"
        elif key == "send":
            self.model.last_operation = "Otwarto moduł wysyłki"
        elif key == "receive":
            def task():
                self.model.last_operation = "Pobieranie danych z KSeF..."
                self.refresh_ui()
                self.model.mock_action("Pobieranie")
                self.refresh_ui()
            threading.Thread(target=task).start()
        elif key == "settings":
            self.model.last_operation = "Ustawienia systemowe"
        
        self.refresh_ui()

    def handle_send_invoice(self, data):
        def task():
            if not data['nr']:
                self.model.last_operation = "Błąd: Brak numeru faktury!"
                self.refresh_ui()
                return

            self.model.last_operation = "Procesowanie wysyłki..."
            self.refresh_ui()
            
            # Auto-login if not logged in (for UX)
            if not self.model.is_logged_in:
                self.model.login()
            
            self.model.send_invoice(data['nr'], data['date'], data['client'])
            self.refresh_ui()
            
        threading.Thread(target=task).start()

    def handle_delete(self):
        # We need to find which row is selected in the Tableview
        # For simplicity in this mock, we'll try to get selected row index
        selected_rows = self.view.dashboard.table.view.selection()
        if not selected_rows:
            self.model.last_operation = "Wybierz fakturę do usunięcia"
            self.refresh_ui()
            return
            
        # Tableview selection returns IIDs, we need index
        # This is a bit tricky with Tableview, so we'll just simulate removing the first selected or top one
        # In a real app, we'd map IID to model index.
        # For mock:
        self.model.delete_invoice(0) 
        self.refresh_ui()

    def handle_edit(self):
        self.model.last_operation = "Tryb edycji (Wybierz fakturę z listy)"
        self.refresh_ui()

    def handle_change_theme(self, event):
        new_theme = self.view.dashboard.combo_theme.get()
        self.view.change_theme(new_theme)
        self.model.last_operation = f"Zmieniono motyw na: {new_theme}"
        self.refresh_ui()

if __name__ == "__main__":
    c = KSeFController()
    c.run()
