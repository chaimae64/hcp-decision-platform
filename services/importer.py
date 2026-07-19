from services.detector import Detector
from services.cleaner import Cleaner
from services.postgres import Postgres
from services.superset_api import SupersetAPI


class Importer:

    @staticmethod
    def run(filepath, table_name):

        # -------------------------
        # Analyse du fichier
        # -------------------------

        info = Detector.detect(filepath)

        if info["rows"] == 0:
            raise Exception("Le fichier ne contient aucune donnée.")

        if info["columns"] == 0:
            raise Exception("Aucune colonne détectée.")

        # -------------------------
        # Nettoyage
        # -------------------------

        dataframe = Cleaner.clean(info)

        if dataframe.empty:
            raise Exception("Le nettoyage a supprimé toutes les données.")

        # -------------------------
        # Insertion PostgreSQL
        # -------------------------

        postgres = Postgres()

        nb_lignes = postgres.save(
            dataframe,
            table_name
        )

        # -------------------------
        # Création du Dataset Superset
        # -------------------------

        superset = SupersetAPI()

        superset_result = superset.create_dataset(
            table_name
        )

        # -------------------------
        # Résultat
        # -------------------------

        return {

            "table": table_name,

            "rows": nb_lignes,

            "columns": len(dataframe.columns),

            "header": info["header_row"],

            "numeric_columns": len(info["numeric_columns"]),

            "text_columns": len(info["text_columns"]),

            "superset": superset_result

        }