import pandas as pd
import os


def clean_file(file_path):

    # Lecture du fichier
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path, header=None)
    else:
        df = pd.read_excel(file_path, header=None)

    # Récupérer les années
    years = df.iloc[0, 3:].tolist()

    # Garder les données
    df = df.iloc[1:].copy()

    # Renommer les colonnes
    columns = ["Milieu", "Région", "Sexe"] + years
    df.columns = columns

    # Compléter les valeurs manquantes
    df["Milieu"] = df["Milieu"].ffill()
    df["Région"] = df["Région"].ffill()

    # Supprimer les lignes inutiles
    df = df.dropna(subset=["Sexe"])
    df = df[df["Sexe"].isin(["Masculin", "Féminin", "Total"])]

    # Conversion numérique
    for col in years:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sauvegarder le fichier nettoyé
    output_folder = "../data/processed"
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "chomage_clean.csv")

    df.to_csv(output_file, index=False, encoding="utf-8")

    return output_file