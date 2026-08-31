"""
Script para generar el conjunto de datos empresarial original (123 registros)
con problemas de calidad de datos para DataAnalytics Colombia S.A.S.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

def generar_dataset_original():
    np.random.seed(42)
    
    base_dir = Path(__file__).resolve().parent
    output_path = base_dir / "clientes_originales_data_wrangling.csv"
    
    nombres = [
        "Carlos Pérez", "Ana Gómez", "Luis Martínez", "María Rodríguez", "Juan López",
        "Laura Hernández", "Santiago Gómez", "Valentina Torres", "Andrés Castro", "Camila Morales",
        "Diego Ramírez", "Sofia Vargas", "Mateo Espinosa", "Daniela Mendoza", "Gabriel Ruiz",
        "Isabella Silva", "Alejandro Ríos", "Mariana Salazar", "David Guerrero", "Natalia Rojas",
        "Felipe Osorio", "Lucía Benítez", "Sebastián Franco", "Elena Paredes", "Nicolás Montoya",
        "Paula Beltrán", "Esteban Marín", "Juliana Suárez", "Samuel Giraldo", "Valeria Cepeda",
        "Jorge Isaacs", "Diana Uribe", "Hernán Cortés", "Gloria Valencia", "Óscar Córdoba",
        "Ximena Hoyos", "Camilo Sesto", "Ingrid Betancourt", "Gonzalo Jiménez", "Beatriz Pinzón"
    ]
    
    ciudades_variaciones = [
        "Medellín", "medellin", "Medelin", "MEDELLIN", "  Medellín  ", "medellín",
        "Bogotá", "bogota", "BOGOTA", "  Bogotá ", "bogotá",
        "Cali", "cali", "CALI", " Cali ",
        "Quibdó", "quibdo", "QUIBDO", " Quibdó ",
        "Bucaramanga", "bucaramanga", "  Bucaramanga ",
        "Cartagena", "cartagena"
    ]
    
    generos_variaciones = [
        "Masculino", "Femenino", "M", "F", "masculino", "femenino", "m", "f", " M ", " F "
    ]
    
    categorias_variaciones = [
        "VIP", "vip", "Estándar", "estandar", "ESTANDAR", "  Estándar  ", "Premium", "premium", " Premium "
    ]
    
    estados_variaciones = [
        "Activo", "ACTIVO", "activo", " Activo ", "Inactivo", "inactivo", "INACTIVO", " Inactivo "
    ]

    records = []
    
    # Generar 115 registros base únicos con variaciones sucias
    for i in range(1, 116):
        nombre = np.random.choice(nombres) if i % 17 != 0 else np.nan
        
        # Inyectar edades válidas e inválidas
        if i % 13 == 0:
            edad = np.random.choice([12, 15, 17, -5, 0]) # Edades inválidas bajas
        elif i % 19 == 0:
            edad = np.random.choice([105, 120, 150]) # Edades inválidas altas
        elif i % 23 == 0:
            edad = np.nan
        else:
            edad = int(np.random.randint(18, 75))
            
        ciudad = np.random.choice(ciudades_variaciones) if i % 21 != 0 else np.nan
        genero = np.random.choice(generos_variaciones) if i % 25 != 0 else np.nan
        categoria = np.random.choice(categorias_variaciones) if i % 29 != 0 else np.nan
        
        # Inyectar compras e importes válidos e inválidos
        if i % 11 == 0:
            compras = 0
        elif i % 31 == 0:
            compras = -2
        elif i % 37 == 0:
            compras = np.nan
        else:
            compras = int(np.random.randint(1, 15))
            
        if i % 9 == 0:
            valor_compra = float(np.random.choice([-1500000.0, -50000.0, -3200000.0])) # Valores negativos
        elif i % 41 == 0:
            valor_compra = np.nan
        else:
            # Rango variado para permitir clasificar Premium (> 5M), Alto Valor (> 3M), etc.
            valor_compra = float(np.random.choice([
                450000.0, 850000.0, 1200000.0, 2200000.0, 3100000.0, 
                4200000.0, 5500000.0, 6800000.0, 8900000.0, 12000000.0
            ]))
            
        estado = np.random.choice(estados_variaciones) if i % 43 != 0 else np.nan
        
        records.append({
            "ID": f"CLI-{1000 + i}",
            "Nombre": nombre,
            "Edad": edad,
            "Ciudad": ciudad,
            "Genero": genero,
            "Categoria": categoria,
            "Compras": compras,
            "ValorCompra": valor_compra,
            "Estado": estado
        })
        
    # Añadir 8 registros duplicados exactos/parciales para sumar 123 registros en total
    duplicados_indices = [5, 12, 24, 38, 45, 60, 78, 90]
    for idx in duplicados_indices:
        dup = records[idx].copy()
        records.append(dup)
        
    df = pd.DataFrame(records)
    
    # Asegurar exactamente 123 filas
    df = df.iloc[:123]
    
    os.makedirs(base_dir, exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Dataset original creado exitosamente con {len(df)} registros en: {output_path}")

if __name__ == "__main__":
    generar_dataset_original()
