import math

def resolver_ecuacion_segundo_orden(a, b, c):
    print(f"Ecuación: {a}y'' {b:+}y' {c:+}y = 0")
    discriminante = b**2 - 4*a*c

    # Usar match-case para los tres casos de raíces
    match discriminante:
        case d if d > 0:
            print("Caso 1: Raíces reales y distintas")
            r1 = (-b + math.sqrt(discriminante)) / (2*a)
            r2 = (-b - math.sqrt(discriminante)) / (2*a)
            print(f"Raíz 1: {r1}")
            print(f"Raíz 2: {r2}")
            print(f"Solución general: y(x) = C1*e^({r1}x) + C2*e^({r2}x)")
        case 0:
            print("Caso 2: Raíces reales e iguales")
            r = -b / (2*a)
            print(f"Raíz doble: {r}")
            print(f"Solución general: y(x) = (C1 + C2*x)*e^({r}x)")
        case _:
            print("Caso 3: Raíces complejas")
            real = -b / (2*a)
            imag = math.sqrt(-discriminante) / (2*a)
            print(f"Raíces: {real} ± {imag}i")
            print(f"Solución general: y(x) = e^({real}x) * [C1*cos({imag}x) + C2*sin({imag}x)]")

# Ejemplo para y'' - y' - 6y = 0
resolver_ecuacion_segundo_orden(1, -1, -6)
