import pandas as pd
import os


def analyze_file(file_path):

    print("Analyse du fichier :", file_path)

    # Lecture du fichier selon son extension
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)

    else:
        raise Exception("Format non supporté")


    # Informations générales
    info = {}

    info["rows"] = len(df)

    info["columns"] = list(df.columns)

    info["types"] = df.dtypes.astype(str).to_dict()


    # Colonnes vides
    empty_columns = df.columns[df.isna().all()].tolist()

    info["empty_columns"] = empty_columns


    return info