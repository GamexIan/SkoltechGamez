import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')


plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context('notebook')

file_path = 'Base de datos O3 para Nian.xlsx'
sheets = pd.read_excel(file_path, sheet_name=None)


cols_needed = ['Dia', 
               'AGUA SANTA O3 (ppm) Promedio Diario', 
               'NINFAS O3 (ppm) Promedio Diario']


dfs = {}
for sheet_name, df in sheets.items():
    if not all(col in df.columns for col in cols_needed):
        print(f"Hoja {sheet_name}: columnas incompletas. Se omite.")
        continue
    
    df_temp = df[cols_needed].copy()
    df_temp.columns = ['fecha', 'agua_santa', 'ninfas']
    
    df_temp['fecha'] = pd.to_datetime(df_temp['fecha'], errors='coerce')
    df_temp = df_temp.dropna(subset=['fecha'])
    
    df_temp = df_temp[df_temp['fecha'].dt.year.between(2021, 2025)]
    if not df_temp.empty:
        dfs[sheet_name] = df_temp


df_all = pd.concat(dfs.values(), ignore_index=True)
df_all = df_all.sort_values('fecha').reset_index(drop=True)


df_all['agua_santa'] = pd.to_numeric(df_all['agua_santa'], errors='coerce')
df_all['ninfas'] = pd.to_numeric(df_all['ninfas'], errors='coerce')

print(f"Rango de fechas: {df_all['fecha'].min()} a {df_all['fecha'].max()}")
print(f"Registros totales: {len(df_all)}")
print(f"NaN en AGUA SANTA: {df_all['agua_santa'].isna().sum()}")
print(f"NaN en NINFAS: {df_all['ninfas'].isna().sum()}")


df_complete = df_all.dropna(subset=['agua_santa', 'ninfas'])

if len(df_complete) >= 2:
    
    X = df_complete[['ninfas']].values
    y = df_complete['agua_santa'].values
    reg = LinearRegression().fit(X, y)
    print(f"\nModelo lineal: agua_santa = {reg.coef_[0]:.4f} * ninfas + {reg.intercept_:.4f}")
    print(f"R² = {reg.score(X, y):.4f}")
    
    
    df_all['agua_santa_imputed'] = np.nan
    
    
    mask_faltan_agua = df_all['agua_santa'].isna() & df_all['ninfas'].notna()
    if mask_faltan_agua.any():
        X_pred = df_all.loc[mask_faltan_agua, ['ninfas']].values
        df_all.loc[mask_faltan_agua, 'agua_santa_imputed'] = reg.predict(X_pred)
        print(f"Se imputaron {mask_faltan_agua.sum()} valores por regresión.")
    else:
        print("nop")

    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df_complete['ninfas'], df_complete['agua_santa'], 
               alpha=0.6, label='Datos completos')
    
    x_vals = np.linspace(df_complete['ninfas'].min(), df_complete['ninfas'].max(), 100)
    y_vals = reg.predict(x_vals.reshape(-1, 1))
    ax.plot(x_vals, y_vals, 'r--', label=f'Regresión (R²={reg.score(X, y):.3f})')
    ax.set_xlabel('NINFAS O3 (ppm)')
    ax.set_ylabel('AGUA SANTA O3 (ppm)')
    ax.set_title('Relación entre estaciones para imputar AGUA SANTA')
    ax.legend()
    plt.tight_layout()
    plt.show()
else:
    df_all['agua_santa_imputed'] = np.nan
    print("Nop")

serie = df_all['agua_santa_imputed'].copy()

serie_interp = serie.interpolate(method='linear', limit_area=None)

serie_interp = serie_interp.ffill().bfill()


df_all['agua_santa_final'] = serie_interp

print(f"NaN después de imputación completa: {df_all['agua_santa_final'].isna().sum()}")


fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# Serie original de AGUA SANTA (con NaN)
axes[0].plot(df_all['fecha'], df_all['agua_santa'], 'o-', markersize=3, 
             color='steelblue', label='AGUA SANTA original (con NaN)')
axes[0].set_ylabel('O3 (ppm)')
axes[0].set_title('Serie original de AGUA SANTA')
axes[0].legend()


axes[1].plot(df_all['fecha'], df_all['agua_santa_final'], 'o-', markersize=3,
             color='darkorange', label='AGUA SANTA imputada (regresión + interpolación)')

mask_reg = df_all['agua_santa'].isna() & df_all['ninfas'].notna()
if mask_reg.any():
    axes[1].scatter(df_all.loc[mask_reg, 'fecha'], 
                    df_all.loc[mask_reg, 'agua_santa_final'],
                    color='red', s=40, label='Imputado por regresión', zorder=5)

mask_interp = df_all['agua_santa'].isna() & df_all['ninfas'].isna()
if mask_interp.any():
    axes[1].scatter(df_all.loc[mask_interp, 'fecha'],
                    df_all.loc[mask_interp, 'agua_santa_final'],
                    color='limegreen', s=40, label='Imputado  interpolación temporal', zorder=5)
axes[1].set_ylabel('O3 (ppm)')
axes[1].set_title('Serie de AGUA SANTA imputada')
axes[1].legend()

plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(14, 6))


ax.plot(df_all['fecha'], df_all['agua_santa'], 'o-', markersize=4,
        color='steelblue', label='AGUA SANTA original (con NaN)', alpha=0.7)


ax.plot(df_all['fecha'], df_all['agua_santa_final'], '-', linewidth=1.5,
        color='darkorange', label='AGUA SANTA imputada (regresión + interpolación)')


mask_reg = df_all['agua_santa'].isna() & df_all['ninfas'].notna()
if mask_reg.any():
    ax.scatter(df_all.loc[mask_reg, 'fecha'],
               df_all.loc[mask_reg, 'agua_santa_final'],
               color='red', s=50, marker='s', label='Imputado  regresión', zorder=5)


mask_interp = df_all['agua_santa'].isna() & df_all['ninfas'].isna()
if mask_interp.any():
    ax.scatter(df_all.loc[mask_interp, 'fecha'],
               df_all.loc[mask_interp, 'agua_santa_final'],
               color='limegreen', s=50, marker='^', label='Imputado interpolación temporal', zorder=5)

ax.set_ylabel('O3 (ppm)')
ax.set_title('Comparación de la serie original y la imputada de AGUA SANTA')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()

# csv
metodo = []
for i in range(len(df_all)):
    if pd.notna(df_all.loc[i, 'agua_santa']):
        metodo.append('original')
    elif pd.notna(df_all.loc[i, 'ninfas']):
        metodo.append('regresión')
    else:
        metodo.append('interpolación')

df_all['metodo_imputacion'] = metodo


df_export = df_all[['fecha', 
                    'agua_santa',          
                    'agua_santa_final',    
                    'ninfas',              
                    'metodo_imputacion']].copy()


df_export.columns = ['fecha', 'aguasanta_original', 'aguasanta_imputada', 'ninfas', 'metodo']

output_path = 'serie_imputada_agua_santa.csv'
df_export.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"\nArchivo CSV exportado: {output_path}")
print(f"Registros exportados: {len(df_export)}")
