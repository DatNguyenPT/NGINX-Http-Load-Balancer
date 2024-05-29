import tkinter as tk
from tkinter import messagebox
import requests
from DBSetup import User, SessionLocal

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Login")

        self.label = tk.Label(master, text="Username")
        self.label.pack()

        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        self.label = tk.Label(master, text="Password")
        self.label.pack()

        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return

        try:
            session = SessionLocal()
            user = session.query(User).filter_by(username=username).first()

            if user and user.password == password:
                self.master.destroy()
                root = tk.Tk()
                DashboardWindow(root)
            else:
                messagebox.showerror("Login Failed", "Incorrect username or password")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

class DashboardWindow:
    def __init__(self, master):
        self.master = master
        master.title("Dashboard")

        self.status_label = tk.Label(master, text="Nginx Status")
        self.status_label.pack()

        self.status_text = tk.Text(master, height=10, width=50)
        self.status_text.pack()

        self.refresh_button = tk.Button(master, text="Refresh Status", command=self.refresh_status)
        self.refresh_button.pack()

        self.visualize_button = tk.Button(master, text="Visualize Data", command=self.open_visualization)
        self.visualize_button.pack()

        self.refresh_status()

    def refresh_status(self):
        try:
            response = requests.get("http://localhost:8080/nginx_status")
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, response.text)
        except requests.RequestException as e:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, "Server is down. Unable to fetch status.")
            messagebox.showerror("Error", f"Failed to fetch status: {e}")

    def open_visualization(self):
        open(["python", "visualization_app.py"]) 

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
