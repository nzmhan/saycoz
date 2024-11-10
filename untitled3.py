import numpy as np
import tkinter as tk
from tkinter import messagebox, Scrollbar, Text, Canvas

# Jacobi Yöntemi Fonksiyonları
def is_diagonally_dominant(A):
    for i in range(len(A)):
        row_sum = sum(abs(A[i][j]) for j in range(len(A)) if j != i)
        if abs(A[i][i]) <= row_sum:
            return False
    return True

def make_diagonally_dominant(A, b):
    n = len(A)
    steps = []
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(A[k][i]))
        if i != max_row:
            A[[i, max_row]] = A[[max_row, i]]
            b[i], b[max_row] = b[max_row], b[i]
            steps.append(f"{i + 1}. satır ile {max_row + 1}. satır değiştirildi.")
    return is_diagonally_dominant(A), steps

def jacobi_method(A, b, tolerance=1e-10, max_iterations=100):
    n = len(A)
    x = np.zeros(n)
    x_new = np.zeros(n)
    steps = []
    if not is_diagonally_dominant(A):
        is_dominant, make_steps = make_diagonally_dominant(A, b)
        steps.extend(make_steps)
        if not is_dominant:
            messagebox.showerror("Hata", "Matris köşegen baskın hale getirilemiyor, Jacobi yöntemi uygulanamaz.")
            return None, []
        steps.append("Matris köşegen baskın hale getirildi.")
    for iteration in range(max_iterations):
        iteration_steps = []
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
            iteration_steps.append(f"x[{i}] = ({b[i]} - {s}) / {A[i][i]} = {x_new[i]}")
        steps.append(f"Iterasyon {iteration + 1}: " + ", ".join(iteration_steps) + "\n")
        if np.linalg.norm(x_new - x, ord=np.inf) < tolerance:
            return x_new, steps
        x = x_new.copy()
    steps.append("Maksimum iterasyon sayısına ulaşıldı.")
    return x, steps

# Tkinter Arayüz Fonksiyonları
def create_matrix():
    try:
        size = int(entry_size.get())
        if size <= 0:
            raise ValueError("Matris boyutu pozitif bir sayı olmalıdır.")
    except ValueError as e:
        messagebox.showerror("Hata", str(e))
        return

    # Önceki girişleri temizle
    for widget in frame_matrix.winfo_children():
        widget.destroy()
    
    global entries, b_entries
    entries = [[tk.Entry(frame_matrix, width=5) for _ in range(size)] for _ in range(size)]
    b_entries = [tk.Entry(frame_matrix, width=5) for _ in range(size)]

    for i in range(size):
        for j in range(size):
            entries[i][j].grid(row=i, column=j, padx=5, pady=5)
        b_entries[i].grid(row=i, column=size + 2, padx=(20, 5), pady=5)

    lbl_b = tk.Label(frame_matrix, text="| Sonuc Vektoru")
    lbl_b.grid(row=0, column=size + 1)

    line = tk.Frame(frame_matrix, height=2, bg="black")
    line.grid(row=size, column=0, columnspan=size + 2, pady=5)

    # Canvas içindeki frame boyutunu güncelle
    frame_matrix.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def solve(event=None):
    size = len(entries)
    A = np.zeros((size, size))
    b = np.zeros(size)

    try:
        for i in range(size):
            for j in range(size):
                A[i][j] = float(entries[i][j].get())
            b[i] = float(b_entries[i].get())
    except ValueError:
        messagebox.showerror("Hata", "Lütfen tüm matris elemanlarını doğru girin.")
        return

    solution, steps = jacobi_method(A, b)
    if solution is not None:
        text_results.delete(1.0, tk.END)
        result_message = "Çözüm: " + str(solution) + "\n\nMatematiksel İşlemler:\n" + "\n".join(steps)
        text_results.insert(tk.END, result_message)

# Mouse kaydırma entegrasyonu
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Tkinter Pencere ve Arayüz Kurulumu
root = tk.Tk()
root.title("Jacobi Yöntemi Çözümleyici")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

frame_input_center = tk.Frame(frame_input)
frame_input_center.pack()

lbl_size = tk.Label(frame_input_center, text="Matris Boyutu (mxm): ")
lbl_size.grid(row=0, column=0)
entry_size = tk.Entry(frame_input_center, width=5)
entry_size.grid(row=0, column=1)

btn_create = tk.Button(frame_input_center, text="Matris Oluştur", command=create_matrix)
btn_create.grid(row=0, column=2)

frame_canvas = tk.Frame(root)
frame_canvas.pack(pady=10, fill=tk.BOTH, expand=True)

canvas = Canvas(frame_canvas)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_y = Scrollbar(frame_canvas, orient=tk.VERTICAL, command=canvas.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar_x = Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
scrollbar_x.pack(fill=tk.X)

canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

frame_matrix = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_matrix, anchor="nw")

btn_solve = tk.Button(root, text="Çözümü Hesapla", command=solve)
btn_solve.pack(pady=10)

result_frame = tk.Frame(root)
result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

lbl_result = tk.Label(result_frame, text="Sonuçlar ve İşlemler:")
lbl_result.pack()

text_results = Text(result_frame, width=60, height=15)
text_results.pack(fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(result_frame, command=text_results.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_results.config(yscrollcommand=scrollbar.set)

# Enter tuşuna basıldığında çözümü hesaplama
root.bind("<Return>", solve)

root.mainloop()
