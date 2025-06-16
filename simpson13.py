import numpy as np
import sympy as sp
from tabulate import tabulate

# ===== PILIH FUNGSI SEDERHANA =====
def pilih_fungsi():
    print("Pilih fungsi f(x):")
    print("1. f(x) = x^2")
    print("2. f(x) = x^3")
    print("3. f(x) = 2 * x^2")
    pilihan = input("Masukkan nomor pilihan (1/2/3): ")

    if pilihan == '1':
        return lambda x: x**2, 'x^2', sp.sympify('x**2')
    elif pilihan == '2':
        return lambda x: x**3, 'x^3', sp.sympify('x**3')
    elif pilihan == '3':
        return lambda x: 2 * x**2, '2 * x^2', sp.sympify('2 * x**2')
    else:
        raise ValueError("Pilihan tidak valid!")

# ===== INPUT =====
f, f_str, f_sympy = pilih_fungsi()

a = float(input("Masukkan batas bawah a: "))
b = float(input("Masukkan batas atas b : "))
n = int(input("Masukkan jumlah subinterval (n genap): "))
if n % 2 != 0:
    raise ValueError("n harus genap untuk Simpson 1/3")

# ===== SIMPSON 1/3 =====
h = (b - a) / n
x_vals = [a + i * h for i in range(n + 1)]
fx_vals = [f(x) for x in x_vals]

rows = []

# Tambahkan i=0
rows.append([0, f"{x_vals[0]:.4f}", f"{fx_vals[0]:.4f}", 1, f"{fx_vals[0]:.4f}"])

integral_sum = fx_vals[0] + fx_vals[-1]

# Tengah-tengah
for i in range(1, n):
    xi = x_vals[i]
    fxi = fx_vals[i]
    coef = 4 if i % 2 != 0 else 2
    weighted = coef * fxi
    integral_sum += weighted
    rows.append([i, f"{xi:.4f}", f"{fxi:.4f}", coef, f"{weighted:.4f}"])

# Tambahkan i=n
rows.append([n, f"{x_vals[-1]:.4f}", f"{fx_vals[-1]:.4f}", 1, f"{fx_vals[-1]:.4f}"])

hasil_simpson = (h / 3) * integral_sum

# ===== ANALITIK =====
x = sp.symbols('x')
I_analitik = sp.integrate(f_sympy, (x, a, b))
hasil_analitik = float(I_analitik)

# ===== ERROR =====
selisih = hasil_simpson - hasil_analitik
error_persen = abs(selisih / hasil_analitik) * 100

# ===== OUTPUT =====
print("\n\n=== HASIL PERHITUNGAN ===")
print(f"f(x) yang digunakan       : {f_str}")
print(f"Batas bawah (a)           : {a}")
print(f"Batas atas (b)            : {b}")
print(f"Subinterval (n)           : {n}")
print(f"Lebar h                   : {h:.4f}")

print("\nTabel Perhitungan Simpson 1/3:")
print(tabulate(rows, headers=["i", "xᵢ", "f(xᵢ)", "Koefisien", "Koefisien * f(xᵢ)"], tablefmt="grid"))

print("\n=== METODE SIMPSON 1/3 ===")
print(f"Hasil Integral Simpson 1/3 = {hasil_simpson:.6f}")

print("\n=== METODE ANALITIK ===")
print(f"Integral simbolik dari {f_str} dari {a} hingga {b}")
print(f"Hasil Integral Analitik    = {hasil_analitik:.6f}")

print("\n=== PERBANDINGAN HASIL ===")
print(f"Selisih (Simpson - Analitik) = {selisih:.6f}")
print(f"Error (%)                    = {error_persen:.6f}%")
