"""
===============================================================================
Programa: Data Wrangling - Empresa DataAnalytics Colombia S.A.S.
Módulo: Ciencia de Datos con Python - Sesión 5 (ADSO)
Descripción: Diagnóstico, limpieza, transformación, filtros booleanos y 
             segmentación de datos empresariales con Pandas.
===============================================================================
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np


def cargar_datos_originales(ruta_archivo: str) -> pd.DataFrame:
    """
    Carga el conjunto de datos original.
    Garantiza que el archivo original permanezca intacto haciendo una copia.
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"No se encontró el archivo original en la ruta: {ruta_archivo}")
    
    print("=" * 80)
    print(" CARGANDO ARCHIVO ORIGINAL")
    print("=" * 80)
    df_original = pd.read_csv(ruta_archivo, encoding="utf-8-sig")
    print(f"-> Archivo cargado exitosamente desde: {ruta_archivo}")
    print(f"-> Registros cargados: {len(df_original)}")
    # Retornar una copia explícita para no alterar el DataFrame de referencia
    return df_original.copy()


def diagnosticar_datos(df: pd.DataFrame) -> None:
    """
    FASE 1: Diagnóstico inicial de calidad de los datos.
    Muestra estructura, tipos, nulos, duplicados y estadísticas básicas.
    """
    print("\n" + "=" * 80)
    print(" FASE 1 - DIAGNÓSTICO INICIAL DE LOS DATOS")
    print("=" * 80)
    
    print(f"\n1. Cantidad total de registros: {df.shape[0]}")
    print(f"2. Cantidad de columnas: {df.shape[1]}")
    print(f"3. Nombres de las columnas: {list(df.columns)}")
    
    print("\n4. Tipos de datos por columna:")
    print(df.dtypes)
    
    print("\n5. Primeros 5 registros:")
    print(df.head())
    
    print("\n6. Últimos 5 registros:")
    print(df.tail())
    
    print("\n7. Cantidad de valores nulos por columna:")
    print(df.isnull().sum())
    
    print(f"\n8. Cantidad de registros duplicados: {df.duplicated().sum()}")
    
    print("\n9. Valores únicos en 'Ciudad':")
    print(df["Ciudad"].unique())
    
    print("\n10. Valores únicos en 'Genero':")
    print(df["Genero"].unique())
    
    print("\n11. Valores únicos en 'Categoria':")
    print(df["Categoria"].unique())
    
    print("\n12. Valores únicos en 'Estado':")
    print(df["Estado"].unique())
    
    print(f"\n13. Rango de Edad -> Mínima: {df['Edad'].min()}, Máxima: {df['Edad'].max()}")
    print(f"14. Rango de ValorCompra -> Mínimo: ${df['ValorCompra'].min():,.2f}, Máximo: ${df['ValorCompra'].max():,.2f}")


def identificar_problemas(df: pd.DataFrame) -> dict:
    """
    FASE 2: Identificación y explicación técnica de problemas de calidad.
    """
    print("\n" + "=" * 80)
    print(" FASE 2 - IDENTIFICACIÓN DE PROBLEMAS DE CALIDAD DE DATOS")
    print("=" * 80)
    
    nulos = df.isnull().sum().to_dict()
    duplicados = df.duplicated().sum()
    
    # Identificar espacios en blanco en cadenas
    columnas_texto = [col for col in df.columns if df[col].dtype in ['object', 'string', 'O']]
    con_espacios = {}
    for col in columnas_texto:
        count = df[col].dropna().apply(lambda x: len(str(x)) != len(str(x).strip())).sum()
        if count > 0:
            con_espacios[col] = count
            
    # Edades inválidas (< 18 o > 100)
    edades_invalidas = df[(df["Edad"] < 18) | (df["Edad"] > 100)]["Edad"].count()
    
    # Compras inválidas (<= 0)
    compras_invalidas = df[df["Compras"] <= 0]["Compras"].count()
    
    # Valores de compra negativos
    valores_negativos = df[df["ValorCompra"] < 0]["ValorCompra"].count()
    
    problemas = {
        "Valores nulos por columna": nulos,
        "Registros duplicados exactos": duplicados,
        "Columnas con espacios innecesarios": con_espacios,
        "Edades fuera de rango (18-100 años)": edades_invalidas,
        "Compras menores o iguales a cero": compras_invalidas,
        "Valores de compra negativos": valores_negativos
    }
    
    print("RESUMEN TÉCNICO DE PROBLEMAS ENCONTRADOS:")
    for problema, detalle in problemas.items():
        print(f" - {problema}: {detalle}")
        
    return problemas


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    FASE 3: Limpieza, normalización y preparación de datos.
    Aplica técnicas de imputación, eliminación de duplicados y estandarización.
    """
    print("\n" + "=" * 80)
    print(" FASE 3 - LIMPIEZA Y PREPARACIÓN DE DATOS (DATA WRANGLING)")
    print("=" * 80)
    
    df_clean = df.copy()
    
    # 1. Eliminar registros duplicados
    filas_antes = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    duplicados_removidos = filas_antes - len(df_clean)
    print(f"1. Registros duplicados eliminados (drop_duplicates): {duplicados_removidos}")
    
    # 2. Eliminar espacios innecesarios de campos de texto
    cols_string = [col for col in df_clean.columns if df_clean[col].dtype in ['object', 'string', 'O']]
    for col in cols_string:
        df_clean[col] = df_clean[col].astype(str).str.strip()
        df_clean[col] = df_clean[col].replace("nan", np.nan)
    print("2. Espacios innecesarios eliminados en campos de texto (str.strip).")
    
    # 3. Normalizar Ciudades
    mapeo_ciudades = {
        "medellin": "Medellín", "medellín": "Medellín", "Medelin": "Medellín", "MEDELLIN": "Medellín",
        "bogota": "Bogotá", "bogotá": "Bogotá", "BOGOTA": "Bogotá",
        "cali": "Cali", "CALI": "Cali",
        "quibdo": "Quibdó", "quibdó": "Quibdó", "QUIBDO": "Quibdó",
        "bucaramanga": "Bucaramanga", "BUCARAMANGA": "Bucaramanga",
        "cartagena": "Cartagena", "CARTAGENA": "Cartagena"
    }
    df_clean["Ciudad"] = df_clean["Ciudad"].replace(mapeo_ciudades)
    print("3. Ciudades normalizadas con acentos y capitalización correcta.")
    
    # 4. Normalizar Género
    mapeo_genero = {
        "M": "Masculino", "m": "Masculino", "masculino": "Masculino",
        "F": "Femenino", "f": "Femenino", "femenino": "Femenino"
    }
    df_clean["Genero"] = df_clean["Genero"].replace(mapeo_genero)
    print("4. Campo 'Genero' estandarizado a 'Masculino' / 'Femenino'.")
    
    # 5. Normalizar Categoría
    mapeo_categoria = {
        "vip": "VIP", "VIP": "VIP",
        "estandar": "Estándar", "ESTANDAR": "Estándar", "Estándar": "Estándar",
        "premium": "Premium", "Premium": "Premium"
    }
    df_clean["Categoria"] = df_clean["Categoria"].replace(mapeo_categoria)
    print("5. Categorías normalizadas ('VIP', 'Estándar', 'Premium').")
    
    # 6. Normalizar Estado
    mapeo_estado = {
        "activo": "Activo", "ACTIVO": "Activo", "Activo": "Activo",
        "inactivo": "Inactivo", "INACTIVO": "Inactivo", "Inactivo": "Inactivo"
    }
    df_clean["Estado"] = df_clean["Estado"].replace(mapeo_estado)
    print("6. Campo 'Estado' estandarizado ('Activo', 'Inactivo').")
    
    # 7. Tratamiento de Edades inválidas o nulas
    # Convertir a numérico por seguridad
    df_clean["Edad"] = pd.to_numeric(df_clean["Edad"], errors="coerce")
    
    # Justificación de Estrategia: Imputación con la mediana de edades válidas (>=18 y <=100)
    mediana_edad = int(df_clean[(df_clean["Edad"] >= 18) & (df_clean["Edad"] <= 100)]["Edad"].median())
    mask_edad_invalida = (df_clean["Edad"] < 18) | (df_clean["Edad"] > 100) | (df_clean["Edad"].isna())
    edades_corregidas = mask_edad_invalida.sum()
    df_clean.loc[mask_edad_invalida, "Edad"] = mediana_edad
    df_clean["Edad"] = df_clean["Edad"].astype(int)
    print(f"7. Edades inválidas o nulas tratadas ({edades_corregidas} registros imputados con mediana = {mediana_edad} años).")
    
    # 8. Tratamiento de Compras inválidas (<= 0 o nulas)
    df_clean["Compras"] = pd.to_numeric(df_clean["Compras"], errors="coerce")
    mediana_compras = int(df_clean[df_clean["Compras"] > 0]["Compras"].median())
    mask_compras_invalidas = (df_clean["Compras"] <= 0) | (df_clean["Compras"].isna())
    compras_corregidas = mask_compras_invalidas.sum()
    df_clean.loc[mask_compras_invalidas, "Compras"] = mediana_compras
    df_clean["Compras"] = df_clean["Compras"].astype(int)
    print(f"8. Compras inválidas/nulas tratadas ({compras_corregidas} registros imputados con mediana = {mediana_compras}).")
    
    # 9. Tratamiento de ValorCompra negativo o nulo
    df_clean["ValorCompra"] = pd.to_numeric(df_clean["ValorCompra"], errors="coerce")
    # Convertir valores negativos a su valor absoluto
    df_clean["ValorCompra"] = df_clean["ValorCompra"].abs()
    mediana_valor = df_clean[df_clean["ValorCompra"] > 0]["ValorCompra"].median()
    df_clean["ValorCompra"] = df_clean["ValorCompra"].fillna(mediana_valor)
    print(f"9. Valores de compra negativos corregidos (abs()) y nulos imputados con mediana (${mediana_valor:,.2f}).")
    
    # 10. Imputación final de variables categóricas nulas con la moda
    df_clean["Nombre"] = df_clean["Nombre"].fillna("Cliente Registrado")
    df_clean["Ciudad"] = df_clean["Ciudad"].fillna(df_clean["Ciudad"].mode()[0])
    df_clean["Genero"] = df_clean["Genero"].fillna(df_clean["Genero"].mode()[0])
    df_clean["Categoria"] = df_clean["Categoria"].fillna(df_clean["Categoria"].mode()[0])
    df_clean["Estado"] = df_clean["Estado"].fillna("Activo")
    print("10. Campos categóricos nulos imputados con moda/valores por defecto.")
    
    # Re-verificación de calidad post-limpieza
    print("\n--- RE-VERIFICACIÓN DE CALIDAD POST-LIMPIEZA ---")
    print(f"-> Total registros limpios final: {len(df_clean)}")
    print(f"-> Nulos restantes: {df_clean.isnull().sum().sum()}")
    print(f"-> Duplicados restantes: {df_clean.duplicated().sum()}")
    print(f"-> Rango Edad final: Mín {df_clean['Edad'].min()} - Máx {df_clean['Edad'].max()}")
    print(f"-> Rango ValorCompra final: Mín ${df_clean['ValorCompra'].min():,.2f} - Máx ${df_clean['ValorCompra'].max():,.2f}")
    
    return df_clean


def aplicar_filtros_condicionales(df: pd.DataFrame) -> dict:
    """
    FASE 4: Filtros condicionales simples y múltiples usando &, | y ~.
    """
    print("\n" + "=" * 80)
    print(" FASE 4 - FILTROS CONDICIONALES Y LÓGICA BOOLEANA")
    print("=" * 80)
    
    # Filtro 1 – Clientes mayores de edad
    f1 = df[df["Edad"] >= 18]
    print(f"\nFiltro 1 - Clientes mayores de edad (Edad >= 18): {len(f1)} registros")
    
    # Filtro 2 – Clientes de Medellín
    f2 = df[df["Ciudad"] == "Medellín"]
    print(f"Filtro 2 - Clientes de Medellín: {len(f2)} registros")
    
    # Filtro 3 – Clientes de alto valor
    f3 = df[df["ValorCompra"] > 3000000]
    print(f"Filtro 3 - Clientes de alto valor (ValorCompra > $3,000,000): {len(f3)} registros")
    
    # Filtro 4 – Medellín y mayores de 25 años (&)
    f4 = df[(df["Edad"] > 25) & (df["Ciudad"] == "Medellín")]
    print(f"Filtro 4 - Medellín y mayores de 25 años: {len(f4)} registros")
    
    # Filtro 5 – Medellín o Cali (|)
    f5 = df[(df["Ciudad"] == "Medellín") | (df["Ciudad"] == "Cali")]
    print(f"Filtro 5 - Medellín o Cali: {len(f5)} registros")
    
    # Filtro 6 – No Bogotá (~)
    f6 = df[~(df["Ciudad"] == "Bogotá")]
    print(f"Filtro 6 - No Bogotá (~): {len(f6)} registros")
    
    return {
        "Filtro_1_Mayores_Edad": f1,
        "Filtro_2_Medellin": f2,
        "Filtro_3_Alto_Valor": f3,
        "Filtro_4_Medellin_Mayores_25": f4,
        "Filtro_5_Medellin_O_Cali": f5,
        "Filtro_6_No_Bogota": f6
    }


def aplicar_filtro_isin(df: pd.DataFrame) -> pd.DataFrame:
    """
    FASE 5: Uso obligatorio de isin() para selección categórica múltiple.
    """
    print("\n" + "=" * 80)
    print(" FASE 5 - USO OBLIGATORIO DE isin()")
    print("=" * 80)
    
    ciudades_objetivo = ["Medellín", "Cali", "Bogotá", "Quibdó"]
    df_isin = df[df["Ciudad"].isin(ciudades_objetivo)]
    
    print(f"Selección mediante .isin({ciudades_objetivo}): {len(df_isin)} registros encontrados.")
    print(df_isin[["ID", "Nombre", "Ciudad", "ValorCompra"]].head())
    
    return df_isin


def segmentar_clientes(df: pd.DataFrame) -> dict:
    """
    FASE 6: Segmentación comercial estratégica de clientes.
    """
    print("\n" + "=" * 80)
    print(" FASE 6 - SEGMENTACIÓN COMERCIAL DE CLIENTES")
    print("=" * 80)
    
    # Segmento A – Clientes premium (ValorCompra > 5.000.000)
    seg_a = df[df["ValorCompra"] > 5000000].copy()
    print(f"Segmento A - Clientes Premium (ValorCompra > $5,000,000): {len(seg_a)} clientes")
    
    # Segmento B – Clientes jóvenes (Edad entre 18 y 25 años)
    seg_b = df[df["Edad"].between(18, 25)].copy()
    print(f"Segmento B - Clientes Jóvenes (Edad 18 a 25 años): {len(seg_b)} clientes")
    
    # Segmento C – Ciudades principales (Medellín, Cali o Bogotá usando isin)
    seg_c = df[df["Ciudad"].isin(["Medellín", "Cali", "Bogotá"])].copy()
    print(f"Segmento C - Ciudades Principales (Medellín, Cali, Bogotá): {len(seg_c)} clientes")
    
    # Segmento D – Clientes activos (Estado diferente de Inactivo usando ~)
    seg_d = df[~(df["Estado"] == "Inactivo")].copy()
    print(f"Segmento D - Clientes Activos (~Inactivo): {len(seg_d)} clientes")
    
    # Segmento E – Clientes de alto potencial
    # Edad entre 25 y 50, más de 5 compras, ValorCompra > 2.000.000 y Estado Activo
    condicion_e = (
        (df["Edad"].between(25, 50)) & 
        (df["Compras"] > 5) & 
        (df["ValorCompra"] > 2000000) & 
        (df["Estado"] == "Activo")
    )
    seg_e = df[condicion_e].copy()
    print(f"Segmento E - Clientes de Alto Potencial: {len(seg_e)} clientes")
    
    return {
        "Datos_Limpios": df,
        "Segmento_Premium": seg_a,
        "Segmento_Joven": seg_b,
        "Ciudades_Principales": seg_c,
        "Clientes_Activos": seg_d,
        "Alto_Potencial": seg_e
    }


def generar_resumen_segmentos(segmentos: dict) -> pd.DataFrame:
    """
    Genera un cuadro de resumen consolidado de métricas e indicadores de negocio.
    """
    resumen_data = []
    
    for nombre_segmento, df_seg in segmentos.items():
        if nombre_segmento == "Datos_Limpios":
            nombre_display = "Total Base Limpia"
        else:
            nombre_display = nombre_segmento.replace("_", " ")
            
        cant_clientes = len(df_seg)
        promedio_edad = df_seg["Edad"].mean() if cant_clientes > 0 else 0
        total_compras = df_seg["Compras"].sum() if cant_clientes > 0 else 0
        promedio_valor_compra = df_seg["ValorCompra"].mean() if cant_clientes > 0 else 0
        venta_total = df_seg["ValorCompra"].sum() if cant_clientes > 0 else 0
        
        resumen_data.append({
            "Segmento": nombre_display,
            "Cantidad Clientes": cant_clientes,
            "Promedio Edad": round(promedio_edad, 1),
            "Total Compras (Unid)": int(total_compras),
            "Promedio Valor Compra": round(promedio_valor_compra, 2),
            "Venta Total ($)": round(venta_total, 2)
        })
        
    return pd.DataFrame(resumen_data)


def exportar_resultados(df_limpio: pd.DataFrame, segmentos: dict, ruta_reports: Path) -> None:
    """
    FASE 7: Generación y exportación de archivos CSV y Excel.
    """
    print("\n" + "=" * 80)
    print(" FASE 7 - GENERACIÓN Y EXPORTACIÓN DE RESULTADOS")
    print("=" * 80)
    
    os.makedirs(ruta_reports, exist_ok=True)
    
    # 1. Exportar clientes_limpios.csv
    ruta_csv = ruta_reports / "clientes_limpios.csv"
    df_limpio.to_csv(ruta_csv, index=False, encoding="utf-8-sig")
    print(f"1. Archivo CSV generado exitosamente: {ruta_csv}")
    
    # 2. Generar hoja de resumen
    df_resumen = generar_resumen_segmentos(segmentos)
    
    # 3. Exportar reporte_segmentacion.xlsx con múltiples pestañas
    ruta_excel = ruta_reports / "reporte_segmentacion.xlsx"
    with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
        for nombre_hoja, df_hoja in segmentos.items():
            df_hoja.to_excel(writer, sheet_name=nombre_hoja, index=False)
        df_resumen.to_excel(writer, sheet_name="Resumen", index=False)
        
    print(f"2. Archivo Excel generado exitosamente: {ruta_excel}")
    print("   Pestañas incluidas:")
    for hoja in list(segmentos.keys()) + ["Resumen"]:
        print(f"    - {hoja}")


def main():
    """
    Función principal que orquesta el flujo completo de Data Wrangling.
    """
    # Determinar rutas relativas al proyecto
    src_dir = Path(__file__).resolve().parent
    project_dir = src_dir.parent
    
    ruta_datos = project_dir / "data" / "clientes_originales_data_wrangling.csv"
    ruta_reportes = project_dir / "reports"
    
    # Verificar o generar dataset original si no existe
    if not os.path.exists(ruta_datos):
        print(f"El archivo original no existe en {ruta_datos}. Generándolo automáticamente...")
        sys.path.append(str(project_dir / "data"))
        import generate_dataset
        generate_dataset.generar_dataset_original()

    # Ejecución de fases
    df_original = cargar_datos_originales(str(ruta_datos))
    diagnosticar_datos(df_original)
    identificar_problemas(df_original)
    
    df_limpio = limpiar_datos(df_original)
    aplicar_filtros_condicionales(df_limpio)
    aplicar_filtro_isin(df_limpio)
    
    segmentos = segmentar_clientes(df_limpio)
    exportar_resultados(df_limpio, segmentos, ruta_reportes)
    
    print("\n" + "=" * 80)
    print(" PROCESO DE DATA WRANGLING FINALIZADO CON ÉXITO")
    print("=" * 80)


if __name__ == "__main__":
    main()
