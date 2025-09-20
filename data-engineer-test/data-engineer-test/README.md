# Data Engineer Technical Exercise

Este repositorio contiene la solucion del ejercicio tecnico propuesto para el rol de Data Engineer de Globant

## Decisiones de diseño

* En lugar de implementar una API REST completa con un framework (por ejemplo FastAPI), opte por una solucion alternativa mas simple, que me permitio concentrarme en la carga, mmodelado y consulta de datos:

    * Base de datos SQLite (por su simmpleza y portabilidad)
    * Script en Python para crear las tablas, cargar los archivos CSV y ejecutar las consultas solicitadas
    * Uso de pandas para simplificar la interaccion con la base de datos y mostrar los resultados

Esta decision fue tomada para poder entregar una solucion funcional y clara en el tiempo disponible, priorizando la calidad del SQL y la organizacion del codigo

En un entorno productivo, la solucion podria escalarse facilmente usando FastAPI como capa de servicio y una base de datos mas robusta (por ejemplo PostgreSQL, BigQuery, etc)


## Estructura del proyecto

data-engineer-test/
│
├── data/
│   ├── departments.csv
│   ├── jobs.csv
│   └── hired_employees.csv
│
├── main.py          # Script principal: crea tablas, carga CSVs y ejecuta queries
├── README.md        # Este archivo
└── requirements.txt # Dependencias del proyecto


## Ejecucion

Ejecutar el script principal:

python main.py


El script: 
    1. Crea una base de datos SQLite (`database.db`)
    2. Crea las tablas `departments`, `jobs` y `hired_employees`
    3. Carga los datos desde los CSV
    4. Ejecuta las consultas SQL pedidas en el enunciado


## Consultas implementadas

1. Empleados contratados por job y departammento en 2021, dividido por trimestre
* Query: `hires_by_quarter_2021()`
* Resultado: tabla con columnas `department`, `job`, `Q1`, `Q2`, `Q3`, `Q4`

2. Departamentos que contrataros mas empleados que la media en 2021
* Query: `departments_above_mean_2021()`
* Resultado: tabla con columnas `id`, `department`, `hired`



## Posibles mejoras

Si bien la solucion actual funciona correctamente, en un proyecto real se podrian aplicar mejoras:
* Implementar una API REST con FastAPI para exponer los resultados como endpoints
* Usar una base de datos mas robusta (por ejemplo PostgreSQL, BigQuery, etc)
* Automatizar la carga de archivos con un proceso ETL orquestado (por ejemplo Airflow)
* Agregar tests unitarios