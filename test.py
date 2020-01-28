import tkinter as tk

APP_TITLE = "My first checkbox"

def series_callback(status):
    print("Checkbox Status:", status.get())

def main():
    app_win = tk.Tk()
    app_win.title(APP_TITLE)

    series_checked = tk.BooleanVar(app_win, True)
    series_checked.trace("w", lambda *_: series_callback(series_checked))

    tk.Checkbutton(app_win, text="Serie", variable=series_checked).pack()
    app_win.mainloop()


if __name__ == '__main__':
    main()