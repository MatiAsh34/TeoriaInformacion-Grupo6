import math

def fermat_factor(n):
    """Devuelve dos factores (p, q) de n usando el método de Fermat."""
    a = math.isqrt(n)
    if a * a < n:
        a += 1  # ceil(sqrt(n))
    while True:
        b2 = a * a - n
        if b2 < 0:
            a += 1
            continue
        b = math.isqrt(b2)
        if b * b == b2:
            p = a - b
            q = a + b
            return p, q
        a += 1

def egcd(a, b):
    """Algoritmo de Euclides extendido: devuelve (g, x, y) tal que ax + by = g = gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def modinv(e, phi):
    """Inverso modular de e módulo phi (e * d ≡ 1 mod phi)."""
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise ValueError("No existe inverso modular, e y phi(n) no son coprimos")
    return x % phi

def rsa_decrypt(C, d, n):
    """Descifra un bloque C usando RSA: M = C^d mod n."""
    return pow(C, d, n)

def main():
    print("=== Romper RSA con Fermat ===")
    n = int(input("Ingrese n: "))
    e = int(input("Ingrese e: "))

    c_input = input("Ingrese C (mensaje cifrado) o deje vacío si solo quiere calcular d: ").strip()
    C = int(c_input) if c_input != "" else None

    # 1) Factorizar n
    print("\nFactorizando n con Fermat...")
    p, q = fermat_factor(n)
    print(f"p = {p}")
    print(f"q = {q}")

    # 2) Calcular phi(n)
    phi = (p - 1) * (q - 1)
    print(f"phi(n) = {phi}")

    # 3) Calcular d
    d = modinv(e, phi)
    print(f"Clave privada d = {d}")
    print(f"Par (n, d) = ({n}, {d})")

    # 4) Si se ingresó C, descifrar
    if C is not None:
        M = rsa_decrypt(C, d, n)
        print(f"\nMensaje descifrado (valor numérico) = {M}")
        try:
            if 0 <= M <= 255:
                print(f"Carácter ASCII correspondiente = '{chr(M)}'")
            else:
                print("El valor descifrado está fuera del rango ASCII básico (0–255).")
        except ValueError:
            print("No se pudo convertir el valor a carácter ASCII.")

if __name__ == "__main__":
    main()
