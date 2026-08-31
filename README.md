# Proyecto Data Wrangling - DataAnalytics Colombia S.A.S.

**Programa:** Análisis y Desarrollo de Software (ADSO)  
**Módulo:** Ciencia de Datos con Python  
**Sesión:** 5  
**Modalidad:** Trabajo Colaborativo  

---

## 1. Descripción del Proyecto

El objetivo principal de esta solución en Python y Pandas es diagnosticar, limpiar, transformar y segmentar un conjunto de datos empresariales de 123 clientes de la empresa **DataAnalytics Colombia S.A.S.**, cuya información original provenía de múltiples sistemas heterogéneos y presentaba problemas críticos de calidad de datos.

La solución implementa una canalización (*pipeline*) reproducible de **Data Wrangling** estructurada modularmente en funciones, aplicando lógica booleana avanzada (`&`, `|`, `~`), el método categórico `.isin()`, tratamiento estricto de nulos, deduplicación y normalización ortográfica.

---

## 2. Estructura del Proyecto

```text
data-wrangling/
├── data/
│   ├── generate_dataset.py                    # Script auxiliar para generar el dataset de 123 registros
│   └── clientes_originales_data_wrangling.csv # Dataset fuente original (Inmutable)
├── src/
│   ├── data_wrangling.py                      # Script principal de diagnóstico, limpieza y segmentación
│   └── generate_pdf_report.py                 # Generador del documento técnico PDF de resultados
├── reports/
│   ├── clientes_limpios.csv                   # CSV resultante después del proceso de Data Wrangling
│   ├── reporte_segmentacion.xlsx              # Libro Excel con 7 hojas de trabajo (Segmentos + Resumen)
│   └── Documento_Analisis_y_Resultados.pdf   # Informe técnico ejecutivo listo para sustentación
├── README.md                                  # Guía del proyecto e investigación técnica
└── requirements.txt                           # Dependencias del proyecto
```

---

## 3. Requisitos e Instalación

### Requisitos Previos
- Python 3.8+ instalado en el sistema.
- Entorno de comandos (PowerShell, CMD o Terminal Bash).

### Instalación de Dependencias
Ejecuta el siguiente comando para instalar las librerías necesarias:

```bash
pip install -r requirements.txt
```

---

## 4. Instrucciones de Ejecución

1. **Generación del Dataset Original (Si no existe):**
   ```bash
   py data/generate_dataset.py
   ```

2. **Ejecución del Flujo Principal de Data Wrangling:**
   ```bash
   py src/data_wrangling.py
   ```
   *Salida:* El programa procesará las 7 Fases en consola y exportará automáticamente los archivos `reports/clientes_limpios.csv` y `reports/reporte_segmentacion.xlsx`.

3. **Generación del Informe PDF Técnico:**
   ```bash
   py src/generate_pdf_report.py
   ```
   *Salida:* Creará el entregable `reports/Documento_Analisis_y_Resultados.pdf`.

---

## 5. Descripción de las Fases del Proyecto

### Fase 1: Diagnóstico de los Datos
Se realiza una inspección visual y estructural inicial obteniendo la forma (`shape`), tipos de datos (`dtypes`), distribución de nulos por columna, conteo de duplicados, rango de edades y valores de compra, y listado de valores únicos para columnas categóricas.

### Fase 2: Identificación de Problemas
Se categorizaron y cuantificaron las siguientes anomalías:
- **8 Registros duplicados exactos.**
- **Valores nulos** distribuidos en `Nombre`, `Edad`, `Ciudad`, `Genero`, `Categoria`, `Compras`, `ValorCompra` y `Estado`.
- **Espacios innecesarios** al inicio y final de cadenas de texto (` Medellín `, ` Activo `).
- **Variaciones ortográficas en Ciudad:** 25 formas disímiles (`medellin`, `Medellín`, `Medelin`, `MEDELLIN`, `bogota`, `Bogotá`, `BOGOTA`, etc.).
- **Inconsistencias en Género:** 11 formas distintas (`M`, `F`, `Masculino`, `Femenino`, `masculino`, `femenino`, `m`, `f`).
- **Inconsistencias en Categoría y Estado:** Variantes en minúsculas y sin acentos (`vip`, `estandar`, `activo`, `inactivo`).
- **Edades inválidas:** Valores fuera del rango laboral/comercial legal (< 18 años o > 100 años, ej: -5, 12, 120 años).
- **Compras e importes inválidos:** `Compras <= 0` y `ValorCompra < 0` (valores negativos por error de tipeo).

### Fase 3: Limpieza y Preparación (Data Wrangling)
- **Deduplicación:** Aplicación de `drop_duplicates()`.
- **Remoción de espacios:** Aplicación de `str.strip()` en todas las columnas de texto.
- **Normalización categórica:** Mapeo mediante diccionarios explícitos para estandarizar `Ciudad`, `Genero`, `Categoria` y `Estado`.
- **Imputación Numérica:** Tratamiento de edades inválidas/nulas imputando la mediana estadística ($45$ años) y corrigiendo valores negativos de `ValorCompra` con `.abs()`.
- **Imputación Categórica:** Relleno de nulos residuales mediante la moda categórica.

### Fase 4: Filtros Condicionales y Lógica Booleana
Implementación de expresiones con operadores booleanos elementales:
- **Filtro 1 (Mayores de edad):** `df[df["Edad"] >= 18]`
- **Filtro 2 (Clientes de Medellín):** `df[df["Ciudad"] == "Medellín"]`
- **Filtro 3 (Alto valor):** `df[df["ValorCompra"] > 3000000]`
- **Filtro 4 (Medellín AND >25 años):** `df[(df["Edad"] > 25) & (df["Ciudad"] == "Medellín")]`
- **Filtro 5 (Medellín OR Cali):** `df[(df["Ciudad"] == "Medellín") | (df["Ciudad"] == "Cali")]`
- **Filtro 6 (NOT Bogotá):** `df[~(df["Ciudad"] == "Bogotá")]`

### Fase 5: Uso Obligatorio de `isin()`
Filtrado estratégico de clientes en ciudades prioritarias:
```python
df[df["Ciudad"].isin(["Medellín", "Cali", "Bogotá", "Quibdó"])]
```

### Fase 6: Segmentación Comercial
Estratificación del portafolio de clientes en 5 segmentos principales:
- **Segmento A (Premium):** `ValorCompra > 5.000.000`
- **Segmento B (Jóvenes):** `Edad.between(18, 25)`
- **Segmento C (Ciudades Principales):** `Ciudad.isin(["Medellín", "Cali", "Bogotá"])`
- **Segmento D (Clientes Activos):** `~(Estado == "Inactivo")`
- **Segmento E (Alto Potencial):** `(Edad.between(25, 50)) & (Compras > 5) & (ValorCompra > 2000000) & (Estado == "Activo")`

### Fase 7: Generación de Resultados
Exportación automatizada a `clientes_limpios.csv` y al libro Excel `reporte_segmentacion.xlsx` configurado con las pestañas: `Datos_Limpios`, `Segmento_Premium`, `Segmento_Joven`, `Ciudades_Principales`, `Clientes_Activos`, `Alto_Potencial` y `Resumen`.

---

## 6. Investigación Obligatoria de Métodos de Pandas

A continuación se detalla la documentación técnica de los **11 métodos fundamentales de Pandas** investigados y aplicados en la solución:

### 1. `dropna()`
- **Qué hace:** Elimina filas o columnas que contengan valores nulos (`NaN` / `None`).
- **Sintaxis:** `df.dropna(axis=0, how='any', subset=None, inplace=False)`
- **Ejemplo:** `df_sin_nulos = df.dropna(subset=['ID', 'ValorCompra'])`
- **Problema que resuelve:** Limpia filas incompletas cuando la imputación no es éticamente o técnicamente viable.
- **Uso en el proyecto:** Utilizado en diagnósticos preliminares para aislar registros con datos faltantes obligatorios.

### 2. `fillna()`
- **Qué hace:** Reemplaza los valores nulos (`NaN`) por un valor específico o calculado (como la media, mediana o moda).
- **Sintaxis:** `df[col].fillna(value=val, inplace=False)`
- **Ejemplo:** `df['Estado'] = df['Estado'].fillna('Activo')`
- **Problema que resuelve:** Evita la pérdida masiva de datos mediante técnicas de imputación controladas.
- **Uso en el proyecto:** Imputó valores faltantes en `ValorCompra` con la mediana y campos categóricos con la moda.

### 3. `drop_duplicates()`
- **Qué hace:** Identifica y remueve filas duplicadas en un DataFrame.
- **Sintaxis:** `df.drop_duplicates(subset=None, keep='first', inplace=False)`
- **Ejemplo:** `df_unico = df.drop_duplicates()`
- **Problema que resuelve:** Elimina registros repetidos que sobreestiman indicadores comerciales o métricas financieras.
- **Uso en el proyecto:** Eliminó 8 registros duplicados exactos presentes en el dataset original.

### 4. `replace()`
- **Qué hace:** Reemplaza valores explícitos o mediante diccionarios de equivalencia por nuevos valores estandarizados.
- **Sintaxis:** `df[col].replace(to_replace=diccionario_o_valor, value=nuevo_valor)`
- **Ejemplo:** `df['Ciudad'] = df['Ciudad'].replace({'medellin': 'Medellín', 'BOGOTA': 'Bogotá'})`
- **Problema que resuelve:** Normaliza inconsistencias ortográficas, variaciones de minúsculas/mayúsculas o sinónimos.
- **Uso en el proyecto:** Normalizó todas las ciudades, géneros, categorías y estados al formato corporativo oficial.

### 5. `astype()`
- **Qué hace:** Convierte una columna o Serie de Pandas a un tipo de dato numérico, categórico o texto específico.
- **Sintaxis:** `df[col] = df[col].astype(dtype)`
- **Ejemplo:** `df['Edad'] = df['Edad'].astype(int)`
- **Problema que resuelve:** Corrige tipos de datos incorrectos cargados desde archivos CSV (ej: números leídos como cadenas).
- **Uso en el proyecto:** Garantizó que `Edad` y `Compras` quedaran casteados explícitamente a enteros (`int`).

### 6. `str.strip()`
- **Qué hace:** Remueve espacios en blanco iniciales, finales o caracteres invisibles de cadenas de texto.
- **Sintaxis:** `df[col].str.strip()`
- **Ejemplo:** `df['Nombre'] = df['Nombre'].str.strip()`
- **Problema que resuelve:** Corrige fallas en comparaciones textuales provocadas por espacios accidentales (`" Activo "` != `"Activo"`).
- **Uso en el proyecto:** Se aplicó sobre todas las columnas categóricas para limpiar espacios ocultos.

### 7. `str.upper()` / `str.lower()`
- **Qué hace:** Transforma todos los caracteres de una cadena a mayúsculas sostenidas (`upper()`) o minúsculas (`lower()`).
- **Sintaxis:** `df[col].str.upper()` / `df[col].str.lower()`
- **Ejemplo:** `df['Estado_Min'] = df['Estado'].str.lower()`
- **Problema que resuelve:** Facilita la igualación insensible a mayúsculas/minúsculas antes de mapeos o filtros.
- **Uso en el proyecto:** Utilizado en fases intermedias de estandarización y filtrado insensible a mayúsculas.

### 8. `between()`
- **Qué hace:** Retorna una máscara booleana indicando si los valores de una Serie se encuentran dentro del rango inclusivo `[left, right]`.
- **Sintaxis:** `df[col].between(left, right, inclusive='both')`
- **Ejemplo:** `jovenes = df[df['Edad'].between(18, 25)]`
- **Problema que resuelve:** Simplifica filtros de rangos continuos evitando la sintaxis doble `(df[col] >= min) & (df[col] <= max)`.
- **Uso en el proyecto:** Construyó el *Segmento B (Clientes Jóvenes 18-25 años)* y filtró edades en el *Segmento E*.

### 9. `query()`
- **Qué hace:** Filtra las filas de un DataFrame evaluando una expresión condicional escrita en formato de cadena limpia.
- **Sintaxis:** `df.query('expresion_booleana')`
- **Ejemplo:** `df_alto_valor = df.query('ValorCompra > 3000000 and Ciudad == "Medellín"')`
- **Problema que resuelve:** Proporciona una sintaxis más legible y concisa para consultas complejas.
- **Uso en el proyecto:** Se utilizó para validaciones cruzadas rápidas y consultas dinámicas en la consola.

### 10. `loc[]`
- **Qué hace:** Accede y modifica un grupo de filas y columnas por etiquetas o mediante máscaras booleanas.
- **Sintaxis:** `df.loc[mascara_booleana, 'NombreColumna'] = nuevo_valor`
- **Ejemplo:** `df.loc[df['ValorCompra'] < 0, 'ValorCompra'] = df['ValorCompra'].abs()`
- **Problema que resuelve:** Permite la modificación directa y segura de celdas específicas evitando el aviso *SettingWithCopyWarning*.
- **Uso en el proyecto:** Imputó valores de edad fuera de rango y corrigió valores de compra negativos directamente en las posiciones afectadas.

---

## 7. Entregables del Proyecto

1. **`src/data_wrangling.py`**: Código fuente principal documentado y modularizado.
2. **`reports/clientes_limpios.csv`**: Dataset procesado sin nulos ni duplicados.
3. **`reports/reporte_segmentacion.xlsx`**: Reporte en Excel con 7 pestañas estructuradas.
4. **`reports/Documento_Analisis_y_Resultados.pdf`**: Documento de sustentación técnica institucional.
5. **`README.md`**: Manual técnico y marco de investigación de Pandas.
6. **`requirements.txt`**: Definición de librerías y versiones.
