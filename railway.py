import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random

users = {"kesar": "123"}

trains = [
    {"train_no": "IR101", "source": "Pune", "destination": "Mumbai", "price": 550},
    {"train_no": "IR202", "source": "Mumbai", "destination": "Nashik", "price": 450},
    {"train_no": "IR303", "source": "Nagpur", "destination": "Aurangabad", "price": 800},
    {"train_no": "IR404", "source": "Kolhapur", "destination": "Pune", "price": 400},
    {"train_no": "IR505", "source": "Solapur", "destination": "Nagpur", "price": 900},
    {"train_no": "IR606", "source": "Nashik", "destination": "Kolhapur", "price": 650},
]
bookings = []

def style_app():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="snow")
    style.configure("Header.TLabel", background="snow", foreground="darkblue", font=("Arial", 16, "bold"))
    style.configure("TLabel", background="snow", font=("Arial", 10))
    style.configure("Treeview", font=("Arial", 10), rowheight=26, background="snow", fieldbackground="snow")
    style.configure("Accent.TButton", background="darkblue", foreground="white", font=("Arial", 10, "bold"), padding=6)
    style.map("Accent.TButton", background=[("active", "blue")], foreground=[("active", "snow")])

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Indian Railways - Login / Register")
        self.root.geometry("470x360")
        self.root.configure(bg="snow")
        style_app()

        frame = ttk.Frame(root, padding=25, style="TFrame")
        frame.pack(expand=True)

        ttk.Label(frame, text="Indian Railways", style="Header.TLabel").pack(pady=15)
        ttk.Label(frame, text="Username:", background="snow").pack(anchor="w")
        self.username = ttk.Entry(frame, width=30)
        self.username.pack(pady=5)

        ttk.Label(frame, text="Password:", background="snow").pack(anchor="w")
        self.password = ttk.Entry(frame, show="*", width=30)
        self.password.pack(pady=5)

        btn_frame = ttk.Frame(frame, style="TFrame")
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Login", style="Accent.TButton", command=self.login).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Register", style="Accent.TButton", command=self.register).grid(row=0, column=1, padx=10)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()
        if user in users and users[user] == pwd:
            messagebox.showinfo("Success", f"Welcome, {user}!")
            self.root.destroy()
            open_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def register(self):
        user = self.username.get()
        pwd = self.password.get()
        if not user or not pwd:
            messagebox.showwarning("Warning", "Enter both username and password!")
            return
        if user in users:
            messagebox.showerror("Error", "User already exists!")
            return
        users[user] = pwd
        messagebox.showinfo("Success", "Registration successful! You can now log in.")

class Dashboard:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
      #  self.root.title(f"Indian Railways - Welcome {user}")
        self.root.geometry("900x550")
        self.root.configure(bg="snow")
        style_app()

        ttk.Label(self.root, text=f"Welcome {user}!", style="Header.TLabel", anchor="center").pack(fill="x", pady=10)

        filter_frame = ttk.Frame(self.root, style="TFrame")
        filter_frame.pack(pady=10)
        ttk.Label(filter_frame, text="Filter by Source:", background="snow").grid(row=0, column=0, padx=5)
        self.source_var = tk.StringVar()
        self.dest_var = tk.StringVar()
        src_list = ["All"] + sorted(set([t["source"] for t in trains]))
        dest_list = ["All"] + sorted(set([t["destination"] for t in trains]))

        src_box = ttk.Combobox(filter_frame, textvariable=self.source_var, values=src_list, width=15)
        src_box.current(0)
        src_box.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Destination:", background="snow").grid(row=0, column=2, padx=5)
        dest_box = ttk.Combobox(filter_frame, textvariable=self.dest_var, values=dest_list, width=15)
        dest_box.current(0)
        dest_box.grid(row=0, column=3, padx=5)

        ttk.Button(filter_frame, text="Apply Filter", style="Accent.TButton", command=self.refresh_trains).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("Train", "Source", "Destination", "Price"), show="headings", height=12)
        for col in ("Train", "Source", "Destination", "Price"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=200)
        self.tree.pack(padx=20, pady=10, fill="both")

        btn_frame = ttk.Frame(self.root, style="TFrame")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Book Selected Train", style="Accent.TButton", command=self.book_train).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Show My Bookings", style="Accent.TButton", command=self.show_bookings).grid(row=0, column=1, padx=10)

        self.refresh_trains()
        self.root.mainloop()

    def refresh_trains(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        src_filter = self.source_var.get()
        dest_filter = self.dest_var.get()
        for t in trains:
            if (src_filter == "All" or t["source"] == src_filter) and (dest_filter == "All" or t["destination"] == dest_filter):
                self.tree.insert("", "end", values=(t["train_no"], t["source"], t["destination"], f"₹{t['price']}"))

    def book_train(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a train to book!")
            return

        values = self.tree.item(selected, "values")
        train_no = values[0]
        train = next((t for t in trains if t["train_no"] == train_no), None)
        if not train:
            messagebox.showerror("Error", "Train not found!")
            return

        try:
            tickets = int(simpledialog.askstring("", "Enter number of tickets:"))
            if tickets <= 0:
                messagebox.showwarning("Warning", "Enter a valid number of tickets!")
                return
        except (TypeError, ValueError):
            return

        booking_id = f"BK{random.randint(1000, 9999)}"
        total_price = train["price"] * tickets
        booking = {
            "id": booking_id,
            "user": self.user,
            "train_no": train_no,
            "source": train["source"],
            "destination": train["destination"],
            "price": train["price"],
            "tickets": tickets,
            "total": total_price
        }
        bookings.append(booking)
        self.show_booking_popup(booking)

    def show_booking_popup(self, booking):
        win = tk.Toplevel(self.root)
        win.title("Booking Confirmation")
        win.geometry("350x420")
        win.configure(bg="snow")
        ttk.Label(win, text="Booking Confirmed!", style="Header.TLabel").pack(pady=10)
        ttk.Label(win, text=f"Booking ID: {booking['id']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"Passenger: {booking['user']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"Train No: {booking['train_no']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"From: {booking['source']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"To: {booking['destination']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"Tickets: {booking['tickets']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"Fare per ticket: ₹{booking['price']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"Total Fare: ₹{booking['total']}", background="snow").pack(pady=5)
        ttk.Button(win, text="OK", style="Accent.TButton", command=win.destroy).pack(pady=15)

    def show_bookings(self):
        win = tk.Toplevel(self.root)
        win.title("My Bookings")
        win.geometry("700x350")
        win.configure(bg="snow")
        ttk.Label(win, text=f"{self.user}'s Bookings", style="Header.TLabel").pack(pady=10)
        tree = ttk.Treeview(win, columns=("ID", "Train", "Source", "Destination", "Tickets", "Total"), show="headings", height=10)
        for col in ("ID", "Train", "Source", "Destination", "Tickets", "Total"):
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=110)
        tree.pack(padx=20, pady=10, fill="both")
        for b in bookings:
            if b["user"] == self.user:
                tree.insert("", "end", values=(b["id"], b["train_no"], b["source"], b["destination"], b["tickets"], f"₹{b['total']}"))

def open_dashboard(user):
    Dashboard(user)

root = tk.Tk()
LoginPage(root)
root.mainloop()
