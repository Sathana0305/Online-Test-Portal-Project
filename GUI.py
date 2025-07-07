import tkinter as tk
from tkinter import messagebox, simpledialog
import Test_functions as tf
def refresh_test_listbox():
    test_list.delete(0, tk.END)
    for name in tf.tests:
        test_list.insert(tk.END, name)
def create_test_gui():
    name = simpledialog.askstring("Create Test", "Name of the test:")
    if not name:
        return
    try:
        num_q = int(simpledialog.askstring("Create Test", "How many questions?"))
    except (TypeError, ValueError):
        return
    tf.tests[name] = []     
    for i in range(num_q):
        q_text = simpledialog.askstring(
            f"Question {i+1}",
            "Enter the question text:"
        )
        if not q_text:
            messagebox.showinfo("Cancelled", "Test creation cancelled.")
            del tf.tests[name]
            return
        opts = []
        for ltr in "ABCD":
            opt = simpledialog.askstring(
                f"Option {ltr}",
                f"Enter option {ltr}:"
            )
            if not opt:
                messagebox.showinfo("Cancelled", "Test creation cancelled.")
                del tf.tests[name]
                return
            opts.append(opt)
        ans = simpledialog.askstring(
            "Answer",
            "Which option is correct? (A/B/C/D)"
        )
        if ans is None or ans.upper() not in "ABCD":
            messagebox.showinfo("Cancelled", "Test creation cancelled.")
            del tf.tests[name]
            return
        tf.tests[name].append({"text": q_text, "opts": opts, "ans": ans.upper()})
    messagebox.showinfo("Saved", f"Test '{name}' created!")
    refresh_test_listbox()
def take_test_gui():
    sel = test_list.curselection()
    if not sel:
        messagebox.showwarning("Select Test", "Please select a test to take.")
        return
    name = test_list.get(sel[0])
    questions = tf.tests[name]
    quiz_win = tk.Toplevel(root)
    quiz_win.title(f"Taking: {name}")
    quiz_win.geometry("450x300")
    q_idx = tk.IntVar(value=0)
    score = tk.IntVar(value=0)
    selected = tk.StringVar()
    q_label = tk.Label(quiz_win, text="", wraplength=400, justify="left", font=("Arial", 12))
    q_label.pack(pady=15)
    opt_buttons = []
    for _ in "ABCD":
        rb = tk.Radiobutton(quiz_win, text="", variable=selected, value="", anchor="w", font=("Arial", 11))
        rb.pack(fill="x", padx=30, anchor="w")
        opt_buttons.append(rb)
    def load_q():
        idx = q_idx.get()
        q = questions[idx]
        q_label.config(text=f"Q{idx+1}. {q['text']}")
        for btn, txt, ltr in zip(opt_buttons, q["opts"], "ABCD"):
            btn.config(text=f"{ltr}. {txt}", value=ltr)
        selected.set(None)
    def next_q():
        if not selected.get():
            messagebox.showwarning("Answer", "Please choose an option.")
            return
        if selected.get() == questions[q_idx.get()]["ans"]:
            score.set(score.get() + 1)
        q_idx.set(q_idx.get() + 1)
        if q_idx.get() < len(questions):
            load_q()
        else:
            messagebox.showinfo(
                "Finished",
                f"You scored {score.get()} out of {len(questions)}"
            )
            quiz_win.destroy()
    next_btn = tk.Button(quiz_win, text="Next", command=next_q)
    next_btn.pack(pady=15)
    load_q()
def modify_test_gui():
    sel = test_list.curselection()
    if not sel:
        messagebox.showwarning("Select Test", "Please select a test to modify.")
        return
    name = test_list.get(sel[0])
    questions = tf.tests[name]
    idx_str = simpledialog.askstring(
        "Modify Test",
        f"Test '{name}' has {len(questions)} question(s).\nEnter question number to edit (1-{len(questions)}):"
    )
    if idx_str is None:
        return
    try:
        q_idx = int(idx_str) - 1
        assert 0 <= q_idx < len(questions)
    except (ValueError, AssertionError):
        messagebox.showerror("Invalid", "Invalid question number.")
        return
    q = questions[q_idx]
    new_q = simpledialog.askstring("Edit Question", "New question text:", initialvalue=q["text"])
    if new_q:
        q["text"] = new_q
    for i, ltr in enumerate("ABCD"):
        new_opt = simpledialog.askstring(
            "Edit Option",
            f"Option {ltr}:",
            initialvalue=q["opts"][i]
        )
        if new_opt:
            q["opts"][i] = new_opt
    new_ans = simpledialog.askstring(
        "Edit Answer",
        "Correct letter (A/B/C/D):",
        initialvalue=q["ans"]
    )
    if new_ans and new_ans.upper() in "ABCD":
        q["ans"] = new_ans.upper()
    messagebox.showinfo("Updated", "Question updated!")
root = tk.Tk()
root.title("Simple Quiz (GUI)")
root.geometry("600x350")
left_frame = tk.Frame(root)
left_frame.pack(side="left", fill="y", padx=10, pady=10)
tk.Label(left_frame, text="Your Tests", font=("Arial", 12, "bold")).pack()
test_list = tk.Listbox(left_frame, width=25, height=15, font=("Arial", 11))
test_list.pack(fill="y", expand=True)
right_frame = tk.Frame(root)
right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
tk.Button(right_frame, text="Create Test", width=20, command=create_test_gui)\
  .pack(pady=10)
tk.Button(right_frame, text="Take Test", width=20, command=take_test_gui)\
  .pack(pady=10)
tk.Button(right_frame, text="Modify Test", width=20, command=modify_test_gui)\
  .pack(pady=10)
tk.Button(right_frame, text="Quit", width=20, command=root.destroy)\
  .pack(pady=10)
refresh_test_listbox()
root.mainloop()
