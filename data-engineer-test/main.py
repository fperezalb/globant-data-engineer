import pandas as pd
import sqlite3

# archivos .csv
DEPARTMENTS_CSV = "data/departments.csv"
JOBS_CSV = "data/jobs.csv"
EMPLOYEES_CSV = "data/hired_employees.csv"

# base de datos en SQLite
DB_FILE = "output/company.db"

def load_csv_to_sqlite(csv_file, table_name, conn, chunksize = 1000):
    """
    Carga un CSV en una tabla SQLite en barches de 'chunksize' filas.
    Si la tabla no existe, pandas la crea automaticamente
    """

    for chunk in pd.read_csv(csv_file, chunksize = chunksize):
        chunk.to_sql(table_name, conn, if_exists = "append", index = False)

    print(f"DONE - {table_name} cargada desde {csv_file}")


def main():

    # conectar a la BD (si no exxiste, se crea el archivo .db)
    conn = sqlite3.connect(DB_FILE)

    # cargar .csv
    load_csv_to_sqlite(DEPARTMENTS_CSV, "departments", conn)
    load_csv_to_sqlite(JOBS_CSV, "jobs", conn)
    load_csv_to_sqlite(EMPLOYEES_CSV, "hired_employees", conn)

    # ejemplo de consulta para contar empleados
    df = pd.read_sql("SELECT COUNT(*) AS TOTAL_EMPLOYEES FROM hired_employees", conn)

    print(df)

    conn.close()


if __name__ == "__main__":
    main()