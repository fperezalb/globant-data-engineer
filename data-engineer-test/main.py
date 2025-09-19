import pandas as pd
import sqlite3

# archivos .csv
DEPARTMENTS_CSV = "data/departments.csv"
JOBS_CSV = "data/jobs.csv"
EMPLOYEES_CSV = "data/hired_employees.csv"

# base de datos en SQLite
DB_FILE = "output/company.db"

def load_csv_to_sqlite(csv_file, table_name, conn, chunksize=1000):
    """
    Carga un CSV en una tabla SQLite en baches de 'chunksize' filas.
    Si la tabla no existe, pandas la crea automaticamente.
    """

    # fuerzo los nombres de las columnas segun el table_name
    if table_name == "departments":
        columns = ["id", "department"]
    elif table_name == "jobs":
        columns = ["id", "job"]
    elif table_name == "hired_employees":
        columns = ["id", "name", "datetime", "department_id", "job_id"]
    else:
        raise ValueError("Tabla desconocida")

    for chunk in pd.read_csv(csv_file, header=None, names=columns, chunksize=chunksize):
        chunk.to_sql(table_name, conn, if_exists="append", index=False)

    print(f"DONE - {table_name} cargada desde {csv_file}")


def hires_by_quarter_2021(conn):
    """
    Devuelve el numero de empleados contratados en 2021 por departamento y job, 
    dividido por trimestre
    """

    query = """
        SELECT 
            d.department,
            j.job,
            SUM(CASE WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 1 AND 3 THEN 1 ELSE 0 END) AS Q1,
            SUM(CASE WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 4 AND 6 THEN 1 ELSE 0 END) AS Q2,
            SUM(CASE WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 7 AND 9 THEN 1 ELSE 0 END) AS Q3,
            SUM(CASE WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 10 AND 12 THEN 1 ELSE 0 END) AS Q4
        FROM 
            hired_employees h
            JOIN 
            departments d 
                ON 
                    h.department_id = d.id
            JOIN 
            jobs j 
                ON 
                    h.job_id = j.id
        WHERE 
            strftime('%Y', h.datetime) = '2021'
        GROUP BY 
            d.department, 
            j.job
        ORDER BY 
            d.department, 
            j.job;
    """

    return pd.read_sql(query, conn)


def main():

    # conectar a la BD (si no exxiste, se crea el archivo .db)
    conn = sqlite3.connect(DB_FILE)

    # creo las tablas con el esquema correcto
    cursor = conn.cursor()
    cursor.executescript(
        """
        DROP TABLE IF EXISTS departments;
        DROP TABLE IF EXISTS jobs;
        DROP TABLE IF EXISTS hired_employees;

        CREATE TABLE departments (
            id INTEGER PRIMARY KEY,
            department TEXT
        );

        CREATE TABLE jobs (
            id INTEGER PRIMARY KEY,
            job TEXT
        );

        CREATE TABLE hired_employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            datetime TEXT,
            department_id INTEGER,
            job_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(id),
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        );
        """
    )

    # cargar todos los .csv
    load_csv_to_sqlite(DEPARTMENTS_CSV, "departments", conn)
    load_csv_to_sqlite(JOBS_CSV, "jobs", conn)
    load_csv_to_sqlite(EMPLOYEES_CSV, "hired_employees", conn)

    # ejemplo de consulta para contar empleados
    # df = pd.read_sql("SELECT COUNT(*) AS TOTAL_EMPLOYEES FROM hired_employees", conn)

    #print(df)

    # seccion SQL
    # apago el maximo de filas a mostrar
    pd.set_option("display.max_rows", None)
    df_quarterly = hires_by_quarter_2021(conn)
    print(df_quarterly)


    # vuelvo a encender el maximo de filas a mostrar
    pd.reset_option("display.max_rows")
    pd.reset_option("display.max_columns")
    
    # cerramos la conexion a la database
    conn.close()


if __name__ == "__main__":
    main()