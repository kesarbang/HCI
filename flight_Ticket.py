import tkinter as tk
from tkinter import ttk, messagebox
import random

users = {"kesar": "123"}

flights = [
    {"flight_no": "AI101", "source": "Pune", "destination": "Delhi", "price": 5500, "seats": 30},
    {"flight_no": "AI202", "source": "Mumbai", "destination": "Goa", "price": 3500, "seats": 25},
    {"flight_no": "AI303", "source": "Delhi", "destination": "Bangalore", "price": 6200, "seats": 40},
    {"flight_no": "AI404", "source": "Chennai", "destination": "Kolkata", "price": 7000, "seats": 35},
    {"flight_no": "AI505", "source": "Hyderabad", "destination": "Jaipur", "price": 4800, "seats": 20},
    {"flight_no": "AI606", "source": "Ahmedabad", "destination": "Pune", "price": 3900, "seats": 15},
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
    style.map("Accent.TButton", background=[("active", "navy")], foreground=[("active", "snow")])

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Book comfy flights with us - Login / Register")
        self.root.geometry("470x360")
        self.root.configure(bg="snow")
        style_app()

        frame = ttk.Frame(root, padding=25, style="TFrame")
        frame.pack(expand=True)

        ttk.Label(frame, text="Vistara", style="Header.TLabel").pack(pady=15)
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
        self.root.title(f"Kesari : Book comfy flights with us - Welcome {user}")
        self.root.geometry("900x550")
        self.root.configure(bg="snow")
        style_app()

        ttk.Label(self.root, text=f"Welcome {user}!", style="Header.TLabel", anchor="center").pack(fill="x", pady=10)

        filter_frame = ttk.Frame(self.root, style="TFrame")
        filter_frame.pack(pady=10)
        ttk.Label(filter_frame, text="Filter by Source:", background="snow").grid(row=0, column=0, padx=5)
        self.source_var = tk.StringVar()
        self.dest_var = tk.StringVar()
        src_list = ["All"] + sorted(set([f["source"] for f in flights]))
        dest_list = ["All"] + sorted(set([f["destination"] for f in flights]))

        src_box = ttk.Combobox(filter_frame, textvariable=self.source_var, values=src_list, width=15)
        src_box.current(0)
        src_box.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Destination:", background="snow").grid(row=0, column=2, padx=5)
        dest_box = ttk.Combobox(filter_frame, textvariable=self.dest_var, values=dest_list, width=15)
        dest_box.current(0)
        dest_box.grid(row=0, column=3, padx=5)

        ttk.Button(filter_frame, text="Apply Filter", style="Accent.TButton", command=self.refresh_flights).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("Flight", "Source", "Destination", "Price"), show="headings", height=12)
        for col in ("Flight", "Source", "Destination", "Price"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=200)
        self.tree.pack(padx=20, pady=10, fill="both")

        btn_frame = ttk.Frame(self.root, style="TFrame")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Book Selected Flight", style="Accent.TButton", command=self.book_flight).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Show My Bookings", style="Accent.TButton", command=self.show_bookings).grid(row=0, column=1, padx=10)

        self.refresh_flights()
        self.root.mainloop()

    def refresh_flights(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        src_filter = self.source_var.get()
        dest_filter = self.dest_var.get()
        for f in flights:
            if (src_filter == "All" or f["source"] == src_filter) and (dest_filter == "All" or f["destination"] == dest_filter):
                if f["seats"] > 0:
                    self.tree.insert("", "end", values=(f["flight_no"], f["source"], f["destination"], f"₹{f['price']}"))

    def book_flight(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a flight to book!")
            return
        values = self.tree.item(selected, "values")
        flight_no = values[0]
        flight = next((f for f in flights if f["flight_no"] == flight_no), None)
        if not flight or flight["seats"] <= 0:
            messagebox.showerror("Error", "No seats available!")
            return

        win = tk.Toplevel(self.root)
        win.title("Book Tickets")
        win.geometry("300x250")
        win.configure(bg="snow")
        ttk.Label(win, text="Enter Number of Tickets:", style="Header.TLabel").pack(pady=10)
        ticket_var = tk.IntVar(value=0)
        entry = ttk.Entry(win, textvariable=ticket_var, width=10)
        entry.pack(pady=10)
        entry.focus()

        def confirm_booking():
            count = ticket_var.get()
            if count <= 0:
                messagebox.showwarning("Warning", "Enter a valid number of tickets!")
                return
            if count > flight["seats"]:
                messagebox.showerror("Error", f"Only {flight['seats']} seats left!")
                return
            flight["seats"] -= count
            booking_id = f"BK{random.randint(1000, 9999)}"
            booking = {
                "id": booking_id,
                "user": self.user,
                "flight_no": flight_no,
                "source": flight["source"],
                "destination": flight["destination"],
                "price": flight["price"],
                "tickets": count
            }
            bookings.append(booking)
            self.refresh_flights()
            win.destroy()
            self.show_booking_popup(booking)

        ttk.Button(win, text="Confirm Booking", style="Accent.TButton", command=confirm_booking).pack(pady=10)

    def show_booking_popup(self, booking):
        win = tk.Toplevel(self.root)
        win.title("Booking Confirmation")
        win.geometry("350x420")
        win.configure(bg="snow")
        ttk.Label(win, text="Booking Confirmed!", style="Header.TLabel").pack(pady=10)
        ttk.Label(win, text=f"Booking ID: {booking['id']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"Passenger: {booking['user']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"Flight No: {booking['flight_no']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"From: {booking['source']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"To: {booking['destination']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"Tickets: {booking['tickets']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"Total Fare: ₹{booking['price'] * booking['tickets']}", background="snow").pack(pady=5)
        ttk.Button(win, text="OK", style="Accent.TButton", command=win.destroy).pack(pady=15)

    def show_bookings(self):
        win = tk.Toplevel(self.root)
        win.title("My Bookings")
        win.geometry("650x350")
        win.configure(bg="snow")
        ttk.Label(win, text=f"{self.user}'s Bookings", style="Header.TLabel").pack(pady=10)
        tree = ttk.Treeview(win, columns=("ID", "Flight", "Source", "Destination", "Tickets", "Price"), show="headings", height=10)
        for col in ("ID", "Flight", "Source", "Destination", "Tickets", "Price"):
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)
        tree.pack(padx=20, pady=10, fill="both")
        for b in bookings:
            if b["user"] == self.user:
                total = b["price"] * b["tickets"]
                tree.insert("", "end", values=(b["id"], b["flight_no"], b["source"], b["destination"], b["tickets"], f"₹{total}"))

def open_dashboard(user):
    Dashboard(user)

root = tk.Tk()
LoginPage(root)
root.mainloop()
