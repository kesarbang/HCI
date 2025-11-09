import tkinter as tk
from tkinter import ttk, messagebox
import random

users = {"kesar": "123"}

rooms = [
    {"room_no": "101", "type": "Single", "price": 1500, "booked": False},
    {"room_no": "102", "type": "Double", "price": 2500, "booked": False},
    {"room_no": "103", "type": "Deluxe", "price": 3500, "booked": False},
    {"room_no": "201", "type": "Family", "price": 5000, "booked": False},
    {"room_no": "202", "type": "Single", "price": 1600, "booked": False},
    {"room_no": "203", "type": "Deluxe", "price": 4000, "booked": False},
]

bookings = []


def style_app():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="snow")
    style.configure("Header.TLabel", background="snow", foreground="navy", font=("Arial", 16, "bold"))
    style.configure("TLabel", background="snow", font=("Arial", 10))
    style.configure("Treeview", font=("Arial", 10), rowheight=26, background="snow", fieldbackground="snow")
    style.configure("Accent.TButton", background="darkblue", foreground="white", font=("Arial", 10, "bold"), padding=6)
    style.map("Accent.TButton", background=[("active", "navy")], foreground=[("active", "snow")])


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("HotelEase - Login / Register")
        self.root.geometry("470x360")
        self.root.configure(bg="snow")
        style_app()

        frame = ttk.Frame(root, padding=25, style="TFrame")
        frame.pack(expand=True)

        ttk.Label(frame, text="HotelEase Login", style="Header.TLabel").pack(pady=15)
        ttk.Label(frame, text="Username:", background="snow").pack(anchor="w")
        self.username = ttk.Entry(frame, width=30)
        self.username.pack(pady=5)

        ttk.Label(frame, text="Password:", background="snow").pack(anchor="w")
        self.password = ttk.Entry(frame, show="*", width=30)
        self.password.pack(pady=5)

        btn_frame = ttk.Frame(frame, style="TFrame")
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Login", style="Accent.TButton", command=self.login).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Register", style="Accent.TButton",command=self.register).grid(row=0, column=1, padx=10)

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
        self.root.title(f" HotelEase - Welcome {user}")
        self.root.geometry("850x550")
        self.root.configure(bg="snow")
        style_app()

        header = ttk.Label(self.root, text=f" Welcome {user}!", style="Header.TLabel", anchor="center")
        header.pack(fill="x", pady=10)

        filter_frame = ttk.Frame(self.root, style="TFrame")
        filter_frame.pack(pady=10)
        ttk.Label(filter_frame, text="Filter by Room Type:", background="snow").grid(row=0, column=0, padx=5)
        self.filter_var = tk.StringVar()
        filter_box = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=["All", "Single", "Double", "Deluxe", "Family"], width=15)
        filter_box.current(0)
        filter_box.grid(row=0, column=1, padx=5)
        ttk.Button(filter_frame, text="Apply Filter", style="Accent.TButton",command=self.refresh_rooms).grid(row=0, column=2, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("Room", "Type", "Price", "Status"), show="headings", height=12)
        for col in ("Room", "Type", "Price", "Status"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)
        self.tree.pack(padx=20, pady=10, fill="both")

        btn_frame = ttk.Frame(self.root, style="TFrame")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Book Selected Room", style="Accent.TButton", command=self.book_room).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Show My Bookings", style="Accent.TButton",command=self.show_bookings).grid(row=0, column=1, padx=10)

        self.refresh_rooms()
        self.root.mainloop()

    def refresh_rooms(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        selected_type = self.filter_var.get()
        for r in rooms:
            if not r["booked"]:
                if selected_type == "All" or r["type"] == selected_type:
                    self.tree.insert("", "end", values=(r["room_no"], r["type"], f"₹{r['price']}", "Available"))

    def book_room(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a room to book!")
            return
        values = self.tree.item(selected, "values")
        room_no = values[0]
        room = next((r for r in rooms if r["room_no"] == room_no), None)
        if not room or room["booked"]:
            messagebox.showerror("Error", "Room already booked!")
            return
        booking_id = f"B{random.randint(1000, 9999)}"
        room["booked"] = True
        booking = {"id": booking_id, "user": self.user, "room_no": room_no, "type": room["type"], "price": room["price"]}
        bookings.append(booking)
        self.refresh_rooms()
        self.show_booking_popup(booking)

    def show_booking_popup(self, booking):
        win = tk.Toplevel(self.root)
        win.title("Booking Confirmation")
        win.geometry("320x400")
        win.configure(bg="snow")
        ttk.Label(win, text="Booking Successful!", style="Header.TLabel").pack(pady=10)
        ttk.Label(win, text=f"Booking ID: {booking['id']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"Name: {booking['user']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"Room No: {booking['room_no']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"Type: {booking['type']}", background="snow").pack(pady=5)
        ttk.Label(win, text=f"Charges: ₹{booking['price']}", background="snow").pack(pady=5)
        ttk.Button(win, text="OK", style="Accent.TButton", command=win.destroy).pack(pady=10)

    def show_bookings(self):
        win = tk.Toplevel(self.root)
        win.title("My Bookings")
        win.geometry("600x350")
        win.configure(bg="snow")
        ttk.Label(win, text=f"{self.user}'s Bookings", style="Header.TLabel").pack(pady=10)
        tree = ttk.Treeview(win, columns=("ID", "Room", "Type", "Price"), show="headings", height=10)
        for col in ("ID", "Room", "Type", "Price"):
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)
        tree.pack(padx=20, pady=10, fill="both")
        for b in bookings:
            if b["user"] == self.user:
                tree.insert("", "end", values=(b["id"], b["room_no"], b["type"], f"₹{b['price']}"))


def open_dashboard(user):
    Dashboard(user)


root = tk.Tk()
LoginPage(root)
root.mainloop()
