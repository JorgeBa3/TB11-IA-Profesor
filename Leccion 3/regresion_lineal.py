import pandas as pd
import numpy as np                                                                          # pyright: ignore[reportMissingImports]
import matplotlib.pyplot as plt

# 1. Cargar el archivo .csv generado en la Lección 2
df = pd.read_csv('datos2.csv')

# 2. Configurar cuadrícula de gráficos (2x2)
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes = axes.flatten()

# Evaluar progresivamente de 5 en 5 datos
pasos = [5, 10, 15, len(df)]
x_rango = np.linspace(0, 4095, 100)

for i, num_puntos in enumerate(pasos):
    ax = axes[i]
    
    # Tomar la muestra de datos hasta 'num_puntos'
    sub_df = df.iloc[:num_puntos]
    x_sub = sub_df['brillo_raw']
    y_sub = sub_df['brillo_255']
    
    # Calcular pendiente (m) e intercepto (b) para esta muestra reducida
    m_paso, b_paso = np.polyfit(x_sub, y_sub, 1)
    
    # Graficar puntos activos
    ax.scatter(x_sub, y_sub, color='orange', edgecolor='black', s=50, label=f'{num_puntos} datos')
    
    # Graficar puntos aún no procesados en gris tenue
    if num_puntos < len(df):
        ax.scatter(df.iloc[num_puntos:]['brillo_raw'], df.iloc[num_puntos:]['brillo_255'], 
                   color='gray', alpha=0.2, s=25)
        
    # Dibujar la recta del modelo en este paso
    ax.plot(x_rango, m_paso * x_rango + b_paso, 'k--', 
            label=f'm = {m_paso:.4f}\nb = {b_paso:.1f}')
    
    ax.set_title(f'Etapa {i+1}: Evaluando primeros {num_puntos} datos')
    ax.set_xlabel('Lectura ADC')
    ax.set_ylabel('Brillo LED')
    ax.set_xlim(-100, 4200)
    ax.set_ylim(-15, 270)
    ax.grid(True, linestyle=':')
    ax.legend(loc='upper left')

plt.tight_layout()
plt.show()