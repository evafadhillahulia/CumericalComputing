import numpy as np # library untuk perhitungan numerik
import sympy as sp # untuk perhitungan simbolik, seperti mencari turunan analitik
from tabulate import tabulate # untuk membuat tabel output yang rapi 

# ===== PILIH FUNGSI SEDERHANA =====
def pilih_fungsi():   # fungsi untuk memilih fungsi yang akan digunakan
    print("Pilih fungsi f(x):")
    print("1. f(x) = x^2")
    print("2. f(x) = x^3")
    print("3. f(x) = 2 * x^2")
    pilihan = input("Masukkan nomor pilihan (1/2/3): ")

    if pilihan == '1':
        return lambda x: x**2, 'x^2', sp.sympify('x**2') # ** = pangkat 
    elif pilihan == '2':
        return lambda x: x**3, 'x^3', sp.sympify('x**3')
    elif pilihan == '3':
        return lambda x: 2 * x**2, '2 * x^2', sp.sympify('2 * x**2')
    else:
        raise ValueError("Pilihan tidak valid!")

# ===== INPUT =====
f, f_str, f_sympy = pilih_fungsi()  # f sebagai fungsi lambdanya (x:x**2), f_str sebagai string representasi fungsi (x^2), dan f_sympy untuk perhitungan simbolik (sp.sympify('x**3'))

x0 = float(input("Masukkan nilai x0 (titik awal): "))
h = float(input("Masukkan nilai h (step size): "))
orde = int(input("Masukkan orde turunan yang diinginkan (1 atau 2): "))  # memilih turunan ke-1 atau ke-2.

# ===== PERHITUNGAN DIFFERENSI MAJU =====
x_vals = [x0 + i * h for i in range(orde + 1)] # menghitung titik x yang dibutuhkan
fx_vals = [f(x) for x in x_vals]  # menghitung nilai fungsi pada titik-titik x yang telah dihitung

if orde == 1:
    diff = (fx_vals[1] - fx_vals[0]) / h
    formula_str = f"[f({x0} + {h}) - f({x0})] / {h}"
    formula_str_detail = f"[f({x_vals[1]:.2f}) - f({x_vals[0]:.2f})] / {h}"
elif orde == 2:
    diff = (fx_vals[2] - 2 * fx_vals[1] + fx_vals[0]) / h**2
    formula_str = f"[f({x0} + 2*{h}) - 2*f({x0} + {h}) + f({x0})] / {h}²"
    formula_str_detail = f"[f({x_vals[2]:.2f}) - 2*f({x_vals[1]:.2f}) + f({x_vals[0]:.2f})] / {h}²"
else:
    raise ValueError("Hanya mendukung turunan orde 1 atau 2.")

# ===== TURUNAN ANALITIK UNTUK PEMBANDING =====
x_sym = sp.Symbol('x')
turunan_analitik = sp.diff(f_sympy, x_sym, orde)
hasil_analitik = float(turunan_analitik.subs(x_sym, x0))

# ===== PERHITUNGAN ERROR =====
error_persen = abs((hasil_analitik - diff) / hasil_analitik) * 100

# ===== OUTPUT =====
print("\n=== DIFFERENSI MAJU ===")
print(f"f(x) yang digunakan         : {f_str}")
print(f"x₀                          : {x0}")
print(f"h (step size)               : {h}")
print(f"Turunan orde ke-{orde}      :")
print(f"Rumus differensi            : {formula_str}")
print(f"                           = {formula_str_detail}")
print(f"Hasil differensi numerik    : {diff:.6f}")
print(f"Hasil turunan analitik      : {hasil_analitik:.6f}")
print(f"Selisih (Numerik - Analitik): {diff - hasil_analitik:.6f}")
print(f"Error (%)                   : {error_persen:.6f}%")
