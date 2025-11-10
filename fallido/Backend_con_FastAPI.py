# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from io import BytesIO
import base64
import scipy.integrate as spi

app = FastAPI(title="Ecuaciones Diferenciales API")

# Configurar CORS para permitir conexiones desde GeoGebra
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EcuacionDiferencial(BaseModel):
    a: float  # coeficiente de y''
    b: float  # coeficiente de y'
    c: float  # coeficiente de y
    f: float = 0  # término independiente
    y0: float = 0  # condición inicial y(0)
    yp0: float = 0  # condición inicial y'(0)
    x_min: float = 0
    x_max: float = 10
    puntos: int = 100

def resolver_ed_homogenea(a, b, c, y0, yp0, x_range):
    """Resuelve la ecuación homogénea ay'' + by' + cy = 0"""
    # Ecuación característica: ar² + br + c = 0
    discriminante = b**2 - 4*a*c
    
    t = sp.symbols('t')
    y = sp.Function('y')
    
    # Resolver la ecuación característica
    raiz1 = (-b + np.sqrt(discriminante)) / (2*a)
    raiz2 = (-b - np.sqrt(discriminante)) / (2*a)
    
    # Solución general según el tipo de raíces
    if discriminante > 0:  # Raíces reales distintas
        C1, C2 = sp.symbols('C1 C2')
        sol_general = C1 * sp.exp(raiz1 * t) + C2 * sp.exp(raiz2 * t)
    elif discriminante == 0:  # Raíz real doble
        C1, C2 = sp.symbols('C1 C2')
        r = -b / (2*a)
        sol_general = (C1 + C2 * t) * sp.exp(r * t)
    else:  # Raíces complejas
        alpha = -b / (2*a)
        beta = np.sqrt(-discriminante) / (2*a)
        C1, C2 = sp.symbols('C1 C2')
        sol_general = sp.exp(alpha * t) * (C1 * sp.cos(beta * t) + C2 * sp.sin(beta * t))
    
    # Aplicar condiciones iniciales
    dy_dt = sp.diff(sol_general, t)
    
    eq1 = sol_general.subs(t, 0) - y0
    eq2 = dy_dt.subs(t, 0) - yp0
    
    try:
        constantes = sp.solve([eq1, eq2], (C1, C2))
        sol_particular = sol_general.subs(constantes)
        return sol_particular
    except:
        # Si falla la solución simbólica, usar método numérico
        return None

def resolver_numericamente(a, b, c, f, y0, yp0, x_range):
    """Resuelve numéricamente usando scipy"""
    def ecuacion_sistema(X, t):
        x1, x2 = X
        dx1_dt = x2
        dx2_dt = (f - b*x2 - c*x1) / a
        return [dx1_dt, dx2_dt]
    
    t_vals = np.linspace(x_range[0], x_range[1], 100)
    X0 = [y0, yp0]
    
    sol = spi.odeint(ecuacion_sistema, X0, t_vals)
    return t_vals, sol[:, 0]

@app.post("/resolver")
async def resolver_ecuacion(ed: EcuacionDiferencial):
    try:
        x = np.linspace(ed.x_min, ed.x_max, ed.puntos)
        
        # Intentar solución analítica primero
        sol_analitica = resolver_ed_homogenea(ed.a, ed.b, ed.c, ed.y0, ed.yp0, 
                                            (ed.x_min, ed.x_max))
        
        if sol_analitica is not None:
            # Evaluar la solución analítica
            t_sym = sp.symbols('t')
            y_vals = [float(sol_analitica.subs(t_sym, xi)) for xi in x]
            metodo = "analítico"
        else:
            # Usar método numérico
            x, y_vals = resolver_numericamente(ed.a, ed.b, ed.c, ed.f, 
                                             ed.y0, ed.yp0, (ed.x_min, ed.x_max))
            metodo = "numérico"
        
        # Crear datos para GeoGebra
        puntos_geogebra = [[float(xi), float(yi)] for xi, yi in zip(x, y_vals)]
        
        # Crear gráfica
        plt.figure(figsize=(10, 6))
        plt.plot(x, y_vals, 'b-', linewidth=2, label='Solución')
        plt.grid(True, alpha=0.3)
        plt.xlabel('x')
        plt.ylabel('y(x)')
        plt.title(f'Solución: {ed.a}y\'\' + {ed.b}y\' + {ed.c}y = {ed.f}')
        plt.legend()
        
        # Convertir gráfica a base64 para mostrar en API
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        imagen_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return JSONResponse({
            "metodo": metodo,
            "puntos": puntos_geogebra,
            "grafica": f"data:image/png;base64,{imagen_base64}",
            "ecuacion": f"{ed.a}y'' + {ed.b}y' + {ed.c}y = {ed.f}",
            "condiciones_iniciales": f"y(0)={ed.y0}, y'(0)={ed.yp0}"
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": f"Error al resolver la ecuación: {str(e)}"}
        )

@app.get("/")
async def root():
    return {"message": "API para resolver ecuaciones diferenciales de segundo orden"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)