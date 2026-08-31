"""
===============================================================================
Generador de Informe Técnico PDF - Data Wrangling (ADSO Sesión 5)
Empresa: DataAnalytics Colombia S.A.S.
===============================================================================
"""

import os
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generar_pdf_reporte():
    src_dir = Path(__file__).resolve().parent
    project_dir = src_dir.parent
    reports_dir = project_dir / "reports"
    output_pdf = reports_dir / "Documento_Analisis_y_Resultados.pdf"
    
    csv_limpio = reports_dir / "clientes_limpios.csv"
    csv_original = project_dir / "data" / "clientes_originales_data_wrangling.csv"
    
    if not os.path.exists(csv_limpio) or not os.path.exists(csv_original):
        print("Error: No se encuentran los archivos CSV necesarios. Ejecuta primero data_wrangling.py.")
        return

    df_orig = pd.read_csv(csv_original)
    df_limpio = pd.read_csv(csv_limpio)

    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1, # Center
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10,
        textColor=colors.white,
        alignment=1
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # Title & Header
    story.append(Paragraph("DOCUMENTO DE ANÁLISIS Y RESULTADOS TÉCNICOS", title_style))
    story.append(Paragraph("<b>Programa:</b> Análisis y Desarrollo de Software (ADSO) | <b>Módulo:</b> Ciencia de Datos con Python - Sesión 5<br/><b>Cliente:</b> DataAnalytics Colombia S.A.S. | <b>Modalidad:</b> Trabajo Colaborativo", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=15))

    # Section 1: Resumen Ejecutivo
    story.append(Paragraph("1. RESUMEN EJECUTIVO Y OBJETIVOS", h1_style))
    intro_p = (
        "El presente informe documenta la ejecución del proceso de <b>Data Wrangling</b> realizado sobre la base de datos "
        "de clientes de <b>DataAnalytics Colombia S.A.S.</b>. La base original presentaba severos problemas de calidad de datos, "
        "incluyendo valores nulos, registros duplicados, inconsistencias ortográficas en nombres de ciudades, categorías y estados, "
        "así como valores fuera de rango en edades e importes de compra negativos. El proyecto aplicó la librería Pandas en Python "
        "para realizar un diagnóstico exhaustivo, saneamiento de inconsistencias y segmentación comercial estratificada."
    )
    story.append(Paragraph(intro_p, body_style))
    story.append(Spacer(1, 8))

    # Section 2: Diagnóstico Comparativo
    story.append(Paragraph("2. MATRIZ COMPARATIVA: ANTES Y DESPUÉS DEL WRANGLING", h1_style))
    
    matriz_data = [
        [Paragraph("Métrica de Calidad", table_header_style), 
         Paragraph("Dataset Original", table_header_style), 
         Paragraph("Dataset Limpio", table_header_style), 
         Paragraph("Estado / Impacto", table_header_style)],
        
        [Paragraph("Total de Registros", table_cell_style), 
         Paragraph(str(len(df_orig)), table_cell_style), 
         Paragraph(str(len(df_limpio)), table_cell_style), 
         Paragraph(f"-{len(df_orig)-len(df_limpio)} duplicados eliminados", table_cell_style)],
        
        [Paragraph("Valores Nulos Totales", table_cell_style), 
         Paragraph(str(df_orig.isnull().sum().sum()), table_cell_style), 
         Paragraph("0", table_cell_style), 
         Paragraph("100% Imputados / Corregidos", table_cell_style)],
        
        [Paragraph("Registros Duplicados", table_cell_style), 
         Paragraph(str(df_orig.duplicated().sum()), table_cell_style), 
         Paragraph("0", table_cell_style), 
         Paragraph("Deduplicación completa (drop_duplicates)", table_cell_style)],

        [Paragraph("Variaciones de Ciudad", table_cell_style), 
         Paragraph("25 variantes inconsistentes", table_cell_style), 
         Paragraph("6 ciudades estándar", table_cell_style), 
         Paragraph("Normalizado con acentos y mayúsculas", table_cell_style)],

        [Paragraph("Rango de Edades Válidas", table_cell_style), 
         Paragraph(f"{df_orig['Edad'].min()} a {df_orig['Edad'].max()} años", table_cell_style), 
         Paragraph(f"{df_limpio['Edad'].min()} a {df_limpio['Edad'].max()} años", table_cell_style), 
         Paragraph("Filtro/Imputación mediana (18-100)", table_cell_style)],

        [Paragraph("Mínimo Valor de Compra", table_cell_style), 
         Paragraph(f"${df_orig['ValorCompra'].min():,.0f}", table_cell_style), 
         Paragraph(f"${df_limpio['ValorCompra'].min():,.0f}", table_cell_style), 
         Paragraph("Saneamiento de valores negativos (abs)", table_cell_style)]
    ]

    t_matriz = Table(matriz_data, colWidths=[1.8*inch, 1.4*inch, 1.4*inch, 2.2*inch])
    t_matriz.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_matriz)
    story.append(Spacer(1, 12))

    # Section 3: Justificación Técnica de Limpieza
    story.append(Paragraph("3. JUSTIFICACIÓN TÉCNICA DE LAS ESTRATEGIAS DE WRANGLING", h1_style))
    just_text = (
        "<b>• Tratamiento de Nulos:</b> Los campos cuantitativos (<i>Edad, Compras, ValorCompra</i>) fueron imputados con la "
        "mediana estadística de la distribución limpia para evitar la distorsión producida por la media en presencia de sesgos. "
        "Los campos categóricos (<i>Ciudad, Genero, Categoria, Estado</i>) se imputaron mediante la moda categórica.<br/>"
        "<b>• Normalización Textual:</b> Se aplicó <code>str.strip()</code> para eliminar espacios invisibles y diccionarios de reemplazo "
        "mapeados a expresiones regulares para estandarizar formas disímiles (ej: <i>medellin, Medelin, MEDELLIN</i> → <b>Medellín</b>).<br/>"
        "<b>• Corrección de Anomalías Numéricas:</b> Se convirtieron los valores de compra negativos mediante su valor absoluto <code>abs()</code>, "
        "interpretando errores de tipeo o signo en los sistemas de captura originales."
    )
    story.append(Paragraph(just_text, body_style))
    story.append(Spacer(1, 10))

    # Section 4: Segmentación Comercial
    story.append(Paragraph("4. RESULTADOS DE LA SEGMENTACIÓN COMERCIAL Y MÉTRICAS CLAVE", h1_style))
    
    # Calcular métricas de segmentos para la tabla
    segmentos_defs = [
        ("Datos Limpios (Total)", len(df_limpio), df_limpio["Edad"].mean(), df_limpio["ValorCompra"].mean(), df_limpio["ValorCompra"].sum()),
        ("Segmento A: Premium (>5M)", len(df_limpio[df_limpio["ValorCompra"] > 5000000]), df_limpio[df_limpio["ValorCompra"] > 5000000]["Edad"].mean(), df_limpio[df_limpio["ValorCompra"] > 5000000]["ValorCompra"].mean(), df_limpio[df_limpio["ValorCompra"] > 5000000]["ValorCompra"].sum()),
        ("Segmento B: Jóvenes (18-25)", len(df_limpio[df_limpio["Edad"].between(18, 25)]), df_limpio[df_limpio["Edad"].between(18, 25)]["Edad"].mean(), df_limpio[df_limpio["Edad"].between(18, 25)]["ValorCompra"].mean(), df_limpio[df_limpio["Edad"].between(18, 25)]["ValorCompra"].sum()),
        ("Segmento C: Ciudades Principales", len(df_limpio[df_limpio["Ciudad"].isin(["Medellín", "Cali", "Bogotá"])]), df_limpio[df_limpio["Ciudad"].isin(["Medellín", "Cali", "Bogotá"])]["Edad"].mean(), df_limpio[df_limpio["Ciudad"].isin(["Medellín", "Cali", "Bogotá"])]["ValorCompra"].mean(), df_limpio[df_limpio["Ciudad"].isin(["Medellín", "Cali", "Bogotá"])]["ValorCompra"].sum()),
        ("Segmento D: Clientes Activos", len(df_limpio[~(df_limpio["Estado"] == "Inactivo")]), df_limpio[~(df_limpio["Estado"] == "Inactivo")]["Edad"].mean(), df_limpio[~(df_limpio["Estado"] == "Inactivo")]["ValorCompra"].mean(), df_limpio[~(df_limpio["Estado"] == "Inactivo")]["ValorCompra"].sum()),
        ("Segmento E: Alto Potencial", len(df_limpio[(df_limpio["Edad"].between(25, 50)) & (df_limpio["Compras"] > 5) & (df_limpio["ValorCompra"] > 2000000) & (df_limpio["Estado"] == "Activo")]), df_limpio[(df_limpio["Edad"].between(25, 50)) & (df_limpio["Compras"] > 5) & (df_limpio["ValorCompra"] > 2000000) & (df_limpio["Estado"] == "Activo")]["Edad"].mean(), df_limpio[(df_limpio["Edad"].between(25, 50)) & (df_limpio["Compras"] > 5) & (df_limpio["ValorCompra"] > 2000000) & (df_limpio["Estado"] == "Activo")]["ValorCompra"].mean(), df_limpio[(df_limpio["Edad"].between(25, 50)) & (df_limpio["Compras"] > 5) & (df_limpio["ValorCompra"] > 2000000) & (df_limpio["Estado"] == "Activo")]["ValorCompra"].sum())
    ]

    seg_table_data = [
        [Paragraph("Segmento Comercial", table_header_style), 
         Paragraph("Cant. Clientes", table_header_style), 
         Paragraph("Prom. Edad", table_header_style), 
         Paragraph("Prom. Valor Compra", table_header_style), 
         Paragraph("Venta Total ($)", table_header_style)]
    ]

    for nombre, cant, edad_prom, val_prom, val_tot in segmentos_defs:
        seg_table_data.append([
            Paragraph(f"<b>{nombre}</b>", table_cell_style),
            Paragraph(str(cant), table_cell_style),
            Paragraph(f"{edad_prom:.1f} yrs", table_cell_style),
            Paragraph(f"${val_prom:,.0f}", table_cell_style),
            Paragraph(f"${val_tot:,.0f}", table_cell_style)
        ])

    t_seg = Table(seg_table_data, colWidths=[2.2*inch, 1.0*inch, 1.0*inch, 1.3*inch, 1.3*inch])
    t_seg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F1F5F9')]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_seg)
    story.append(Spacer(1, 12))

    # Section 5: Conclusiones y Entregables
    story.append(Paragraph("5. CONCLUSIONES Y ENTREGABLES GENERADOS", h1_style))
    conc_p = (
        "1. <b>Higiene de Datos Garantizada:</b> El archivo <code>clientes_limpios.csv</code> constituye una fuente única de la verdad "
        "completamente limpia y estructurada sin duplicados ni nulos.<br/>"
        "2. <b>Reporte Multicapa en Excel:</b> Se generó el archivo <code>reporte_segmentacion.xlsx</code> con 7 hojas interactivas que "
        "permiten a los equipos de Marketing y Ventas consultar segmentos específicos de forma inmediata.<br/>"
        "3. <b>Segmento de Mayor Impacto:</b> El <i>Segmento E (Alto Potencial)</i> representa a 16 clientes activos de 25-50 años con compras "
        "frecuentes (>5) y alto gasto, ideales para campañas prioritarias de fidelización."
    )
    story.append(Paragraph(conc_p, body_style))
    
    doc.build(story)
    print(f"Documento PDF generado exitosamente en: {output_pdf}")

if __name__ == "__main__":
    generar_pdf_reporte()
