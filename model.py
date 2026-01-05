import time

class KSeFModel:
    def __init__(self):
        self.is_logged_in = False
        self.last_operation = "Gotowość systemu (V3)"
        self.invoices = [
            ("FV/2024/001", "2024-03-20", "ABC Corp", "Wysłana"),
            ("FV/2024/002", "2024-03-21", "XYZ Ltd", "Błąd"),
            ("FV/2024/003", "2024-03-22", "Janusz Pol", "W toku"),
            ("FV/2024/004", "2024-03-23", "Soft System", "Oczekuje"),
        ]
        self.available_themes = ["darkly", "superhero", "cosmo", "flatly", "journal", "pulse", "sandstone", "united"]

    def login(self):
        time.sleep(1)
        self.is_logged_in = True
        self.last_operation = "Zalogowano do KSeF"
        return True

    def logout(self):
        self.is_logged_in = False
        self.last_operation = "Wylogowano z systemu"
        return True

    def send_invoice(self, nr, date, client):
        time.sleep(1.2)
        new_invoice = (nr, date, client, "Wysłana")
        self.invoices.insert(0, new_invoice)
        self.last_operation = f"Faktura {nr} wysłana poprawnie"
        return True

    def delete_invoice(self, index):
        if 0 <= index < len(self.invoices):
            removed = self.invoices.pop(index)
            self.last_operation = f"Usunięto fakturę: {removed[0]}"
            return True
        return False

    def mock_action(self, action_name):
        time.sleep(0.8)
        self.last_operation = f"Akcja: {action_name} zakończona"
        return True
