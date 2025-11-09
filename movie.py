from tkinter import *
from tkinter import messagebox

def login():
    username = user_var.get()
    password = pass_var.get()

    if username == "admin" and password == "1234":
        login_window.destroy()
        open_booking_window()
    else:
        msg_label.config(text="Invalid Username or Password!", fg="red")


bookings = [] 

def open_booking_window():
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
                booking_info = f"Movie: {movie}\nTime: {time}\nTickets: {tickets}\nTotal: Rs.{total}"
                bookings.append(booking_info)
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
            messagebox.showinfo("My Bookings", all_bookings)

    root = Tk()
    root.title("Movie Ticket Booking System")
    root.geometry("430x430")
    root.config(bg="snow")  

    movie_var = StringVar()
    time_var = StringVar()
    ticket_var = StringVar()

    Label(root, text="MOVIE TICKET BOOKING SYSTEM", font=("Arial", 12, "bold"), bg="snow", fg="red").pack(pady=10)

    frame = Frame(root, bg="snow", bd=2, relief="groove")
    frame.pack(pady=10, padx=20, fill="both", expand=True)

    Label(frame, text="Select Movie:", bg="snow", fg="black").pack(pady=5)
    OptionMenu(frame, movie_var, "Inception", "Avengers", "3 Idiots", "Harry Potter").pack(pady=5)

    Label(frame, text="Select Show Time:", bg="snow", fg="black").pack(pady=5)
    OptionMenu(frame, time_var, "10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM").pack(pady=5)

    Label(frame, text="Enter Number of Tickets:", bg="snow", fg="black").pack(pady=5)
    Entry(frame, textvariable=ticket_var).pack(pady=5)

    Button(frame, text="Book Ticket", command=book_ticket, bg="red", fg="white").pack(pady=5)
    Button(frame, text="Reset", command=reset_fields, bg="white", fg="red").pack(pady=3)
    Button(frame, text="Show My Bookings", command=show_bookings, bg="red", fg="white").pack(pady=5)

    result_label = Label(frame, text="", justify=LEFT, bg="snow", fg="red")
    result_label.pack(pady=10)

    root.mainloop()

login_window = Tk()
login_window.title("Login Page")
login_window.geometry("320x220")
login_window.config(bg="snow")

user_var = StringVar()
pass_var = StringVar()

Label(login_window, text="LOGIN PAGE", font=("Arial", 12, "bold"), bg="snow", fg="red").pack(pady=10)

Label(login_window, text="Username:", bg="snow", fg="black").pack()
Entry(login_window, textvariable=user_var).pack(pady=5)

Label(login_window, text="Password:", bg="snow", fg="black").pack()
Entry(login_window, textvariable=pass_var, show="*").pack(pady=5)

Button(login_window, text="Login", command=login, bg="red", fg="white").pack(pady=10)

msg_label = Label(login_window, text="", bg="snow", fg="red")
msg_label.pack()

login_window.mainloop()
