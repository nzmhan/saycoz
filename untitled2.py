import numpy as np
from sympy import sympify, symbols
from fractions import Fraction

# Trapezoid kuralı ile integral hesaplama
def trapezoid_rule(f, a, b, n):
    x_vals = np.linspace(a, b, n+1)  # n bölmeli x değerleri
    y_vals = np.array([f(x) for x in x_vals])  # Fonksiyonun bu noktalardaki değerleri
    h = (b - a) / n  # Her bir trapezin genişliği
    integral = h * (0.5 * y_vals[0] + np.sum(y_vals[1:-1]) + 0.5 * y_vals[-1])
    return integral

# Hedeflenen hata toleransına ulaşana kadar n değerini artıran algoritma
def find_n_for_tolerance(f, a, b, tolerance):
    n = 1  # Küçük bir başlangıç bölme sayısı
    previous_integral = trapezoid_rule(f, a, b, n)  # İlk integral sonucu
    n += 1

    while True:
        # Yeni integral sonucunu hesapla
        current_integral = trapezoid_rule(f, a, b, n)
        error = abs(current_integral - previous_integral)  # Önceki ve şimdiki değer arasındaki fark (hata)
        
        # Eğer hata toleransın altındaysa döngüyü durdur
        if error <= tolerance:
            break
        
        # Sonucu güncelle ve n'yi artır
        previous_integral = current_integral
        n += 1
    
    return n, current_integral, error

# Kullanıcının girdiği fonksiyon ifadesini değerlendirir ve numpy ile uyumlu hale getirir
def convert_func_to_numpy(func_expr):
    x_sym = symbols('x')
    func_sympy = sympify(func_expr)  # Fonksiyonu sembolik olarak işliyoruz
    f_lambda = lambda x: float(func_sympy.evalf(subs={x_sym: x}))  # Nümerik hale getiriyoruz
    return f_lambda

# Kesirli ya da ondalıklı girdi alabilen güvenli giriş fonksiyonu
def safe_input(prompt):
    while True:
        try:
            user_input = input(prompt)
            # Fraction ile kesirli sayı ya da float dönüşümünü yapıyoruz
            return float(Fraction(user_input))
        except ValueError:
            print("Geçersiz giriş! Lütfen sayısal bir değer girin.")

# Ana program
def main():
    # Kullanıcıdan fonksiyon, aralık ve hata toleransı bilgilerini al
    func_expr = input("İntegralini almak istediğiniz fonksiyon (örn. 1 + x**2): ")
    f = convert_func_to_numpy(func_expr)  # Kullanıcının girdiği fonksiyonu dönüştürüyoruz
    
    # Kesirli ya da ondalıklı girdi kabul eden güvenli girişler
    a = safe_input("Alt sınır (a): ")
    b = safe_input("Üst sınır (b): ")
    tolerance = safe_input("Hedef hata payı (örneğin 0.001): ")

    # n değerini bul ve sonuca ulaş
    n, approx_integral, error = find_n_for_tolerance(f, a, b, tolerance)
    
    # Sonuçları göster
    print(f"Hedef hata payı için gerekli n değeri: {n}")
    print(f"Yaklaşık integral: {approx_integral}")
    print(f"Hata: {error}")

if __name__ == "__main__":
    main()
