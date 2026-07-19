import pandas as pd
from pathlib import Path
import re


class Detector:

    @staticmethod
    def read_file(file_path):

        extension = Path(file_path).suffix.lower()

        if extension == ".xlsx":
            raw_df = pd.read_excel(file_path, header=None)

        elif extension == ".csv":
            raw_df = pd.read_csv(file_path, header=None)

        else:
            raise Exception("Format de fichier non supporté.")

        return raw_df, extension

    @staticmethod
    def score_row(row):

        score = 0

        values = row.dropna()

        if len(values) == 0:
            return -999

        # Nombre de cellules renseignées
        score += len(values)

        text = 0
        numeric = 0

        for value in values:

            if isinstance(value, str):

                v = value.strip().lower()

                if v.startswith("tableau"):
                    score -= 10

                if v.startswith("source"):
                    score -= 10

                if v.startswith("note"):
                    score -= 5

                # Année (2024, 2014...)
                if re.fullmatch(r"\d{4}", v):
                    score += 3

                text += 1

            else:

                numeric += 1

        score += text
        score -= numeric

        return score

    @staticmethod
    def detect_header(raw_df):

        best_score = -9999
        best_row = 0

        max_scan = min(20, len(raw_df))

        for i in range(max_scan):

            score = Detector.score_row(raw_df.iloc[i])

            if score > best_score:

                best_score = score
                best_row = i

        return best_row

    @staticmethod
    def detect_data_start(df):

        for i in range(len(df)):

            row = df.iloc[i]

            if row.notna().sum() >= max(2, len(df.columns) // 3):
                return i

        return 0

    @staticmethod
    def detect_columns(df):

        numeric_columns = []
        text_columns = []

        for col in df.columns:

            try:

                converted = pd.to_numeric(
                    df[col],
                    errors="coerce"
                )

                ratio = converted.notna().sum() / len(df)

                if ratio >= 0.7:
                    numeric_columns.append(str(col))
                else:
                    text_columns.append(str(col))

            except Exception:

                text_columns.append(str(col))

        return numeric_columns, text_columns

    @staticmethod
    def detect(file_path):

        # -------------------------
        # Lecture brute
        # -------------------------

        raw_df, extension = Detector.read_file(file_path)

        # -------------------------
        # Détection de l'en-tête
        # -------------------------

        header_row = Detector.detect_header(raw_df)

        # -------------------------
        # Lecture avec header détecté
        # -------------------------

        if extension == ".xlsx":

            df = pd.read_excel(
                file_path,
                header=header_row
            )

        else:

            df = pd.read_csv(
                file_path,
                header=header_row
            )

        # -------------------------
        # Détection structure
        # -------------------------

        data_start = Detector.detect_data_start(df)

        numeric_columns, text_columns = Detector.detect_columns(df)

        empty_rows = df.index[
            df.isna().all(axis=1)
        ].tolist()

        empty_columns = df.columns[
            df.isna().all()
        ].tolist()

        # -------------------------
        # Résultat
        # -------------------------

        return {

            "file_type": extension,

            "header_row": header_row,

            "header_rows": [
                max(0, header_row - 1),
                header_row
            ],

            "data_start": data_start,

            "rows": len(df),

            "columns": len(df.columns),

            "numeric_columns": numeric_columns,

            "text_columns": text_columns,

            "empty_rows": empty_rows,

            "empty_columns": empty_columns,

            # DataFrame brut
            "raw_dataframe": raw_df,

            # DataFrame analysé
            "dataframe": df

        }