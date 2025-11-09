from tkinter import *
from tkinter import messagebox

users = {"kesar": "1234"}
bookings = [] 

def login():
    username = user_var.get()
    password = pass_var.get()

    if username in users and users[username] == password:
        login_window.destroy()
        open_booking_window(username)
    else:
        msg_label.config(text="Invalid Username or Password!", fg="red")

def open_register_window():
    def register_user():
        new_user = reg_user_var.get()
        new_pass = reg_pass_var.get()

        if new_user == "" or new_pass == "":
            reg_msg.config(text="Please fill all fields!", fg="red")
        elif new_user in users:
            reg_msg.config(text="Username already exists!", fg="red")
        else:
            users[new_user] = new_pass
            messagebox.showinfo("Registration Successful", "You can now log in!")
            register_window.destroy()

    register_window = Toplevel(login_window)
    register_window.title("Register")
    register_window.geometry("320x230")
    register_window.config(bg="snow")

    Label(register_window, text="REGISTER", font=("Arial", 12, "bold"), bg="snow", fg="red").pack(pady=10)

    reg_user_var = StringVar()
    reg_pass_var = StringVar()

    Label(register_window, text="New Username:", bg="snow").pack()
    Entry(register_window, textvariable=reg_user_var).pack(pady=5)

    Label(register_window, text="New Password:", bg="snow").pack()
    Entry(register_window, textvariable=reg_pass_var, show="*").pack(pady=5)

    Button(register_window, text="Register", command=register_user, bg="red", fg="white").pack(pady=10)
    reg_msg = Label(register_window, text="", bg="snow")
    reg_msg.pack()

def open_booking_window(username):
    def book_ticket():
        movie = movie_var.get()
        time = time_var.get()
        tickets = ticket_var.get()

        if movie == "" or time == "" or tickets == "":
            result_label.config(text="Please fill all the details!", fg="red")
        else:
            try:
                tickets = int(tickets)
                if tickets <= 0:
                    result_label.config(text="Enter a valid number of tickets!", fg="red")
                    return
                total = tickets * 150
                booking_info = f"{username} - Movie: {movie} | Time: {time} | Tickets: {tickets} | Total: Rs.{total}"
                bookings.append(booking_info)
                listbox.insert(END, booking_info)
                result_label.config(text="Booking Successful!", fg="green")
            except ValueError:
                result_label.config(text="Please enter a valid number!", fg="red")

    def reset_fields():
        movie_var.set("")
        time_var.set("")
        ticket_var.set("")
        result_label.config(text="")

    def show_bookings():
        if not bookings:
            messagebox.showinfo("Bookings", "No bookings made yet!")
        else:
            all_bookings = "\n\n".join(bookings)
            messagebox.showinfo("All Bookings", all_bookings)

    def delete_booking():
        selected = listbox.curselection()
        if not selected:
            messagebox.showinfo("Delete Booking", "Please select a booking to delete!")
            return
        index = selected[0]
        booking = bookings.pop(index)
        listbox.delete(index)
        messagebox.showinfo("Booking Deleted", f"Deleted:\n\n{booking}")

    root = Tk()
    root.title("Movie Ticket Booking System")
    root.geometry("450x500")
    root.config(bg="snow")

    movie_var = StringVar()
    time_var = StringVar()
    ticket_var = StringVar()

    Label(root, text=f"Welcome, {username}", font=("Arial", 11, "bold"), bg="snow", fg="red").pack(pady=5)
    Label(root, text="MOVIE TICKET BOOKING SYSTEM", font=("Arial", 12, "bold"), bg="snow", fg="red").pack(pady=5)

    frame = Frame(root, bg="snow", bd=2, relief="groove")
    frame.pack(pady=10, padx=20, fill="both", expand=False)

    Label(frame, text="Select Movie:", bg="snow", fg="black").pack(pady=5)
    OptionMenu(frame, movie_var, "Inception", "Avengers", "3 Idiots", "Harry Potter").pack(pady=5)

    Label(frame, text="Select Show Time:", bg="snow", fg="black").pack(pady=5)
    OptionMenu(frame, time_var, "10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM").pack(pady=5)

    Label(frame, text="Enter Number of Tickets:", bg="snow", fg="black").pack(pady=5)
    Entry(frame, textvariable=ticket_var).pack(pady=5)

    Button(frame, text="Book Ticket", command=book_ticket, bg="red", fg="white").pack(pady=5)
    Button(frame, text="Reset", command=reset_fields, bg="white", fg="red").pack(pady=3)
    Button(frame, text="Show All Bookings", command=show_bookings, bg="red", fg="white").pack(pady=5)

    result_label = Label(frame, text="", bg="snow", fg="red")
    result_label.pack(pady=5)

    Label(root, text="Your Bookings:", bg="snow", fg="black", font=("Arial", 10, "bold")).pack(pady=5)
    listbox = Listbox(root, width=60, height=7)
    listbox.pack(pady=5)

    Button(root, text="Delete Selected Booking", command=delete_booking, bg="white", fg="red").pack(pady=10)

    root.mainloop()

login_window = Tk()
login_window.title("Login Page")
login_window.geometry("320x260")
login_window.config(bg="snow")

user_var = StringVar()
pass_var = StringVar()

Label(login_window, text="LOGIN PAGE", font=("Arial", 12, "bold"), bg="snow", fg="red").pack(pady=10)

Label(login_window, text="Username:", bg="snow", fg="black").pack()
Entry(login_window, textvariable=user_var).pack(pady=5)

Label(login_window, text="Password:", bg="snow", fg="black").pack()
Entry(login_window, textvariable=pass_var, show="*").pack(pady=5)

Button(login_window, text="Login", command=login, bg="red", fg="white").pack(pady=5)
Button(login_window, text="Register", command=open_register_window, bg="white", fg="red").pack(pady=5)

msg_label = Label(login_window, text="", bg="snow", fg="red")
msg_label.pack()

login_window.mainloop()
