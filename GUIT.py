from tkinter import Tk, Toplevel, Label, ttk


def buttonOK(title, message):
    top = Toplevel()
    top.title(title)

    label = Label(top, text=message, font=('Helvetica', 14, 'bold'))
    label.pack(padx=10, pady=10)

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 16, 'bold'),
                    foreground='#ffffff', background='#4CAF50', padding=(20, 10))

    ok_button = ttk.Button(
        top, text="OK", command=top.destroy, style='TButton')
    ok_button.pack(pady=20)

    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()

    x_position = screen_width - top.winfo_reqwidth()
    y_position = screen_height - top.winfo_reqheight()

    top.geometry("+{}+{}".format(x_position, y_position))

    top.wait_window()


# Example usage:
root = Tk()
buttonOK("Title", "This is a message")
root.mainloop()
