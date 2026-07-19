import pandas as pd
from sqlalchemy import create_engine


def load_to_postgres(csv_file, table_name):

    # Lecture du fichier nettoyé
    df = pd.read_csv(csv_file)

    # Connexion PostgreSQL
    engine = create_engine(
        "postgresql://postgres@localhost:5433/hcp_bi"
    )

    # Insertion dans PostgreSQL
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    return len(df)