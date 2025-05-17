import tkinter as tk

def 显示选择():
    print(f"你选择了：苹果={苹果.get()}，香蕉={香蕉.get()}，橘子={橘子.get()}")

窗口 = tk.Tk()

苹果 = tk.IntVar()
香蕉 = tk.IntVar()
橘子 = tk.IntVar()

tk.Checkbutton(窗口, variable=苹果).pack()
tk.Checkbutton(窗口, text="香蕉", variable=香蕉).pack()
tk.Checkbutton(窗口, text="橘子", variable=橘子).pack()

tk.Button(窗口, text="确认", command=显示选择).pack()

窗口.mainloop()
