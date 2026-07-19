import pandas as pd


class Cleaner:

    @staticmethod
    def clean(info):

        df = info["dataframe"].copy()

        # -------------------------------------------------
        # 1. Supprimer lignes totalement vides
        # -------------------------------------------------

        df.dropna(how="all", inplace=True)

        # -------------------------------------------------
        # 2. Supprimer colonnes totalement vides
        # -------------------------------------------------

        df.dropna(axis=1, how="all", inplace=True)

        # -------------------------------------------------
        # 3. Compléter cellules fusionnées
        # -------------------------------------------------

        df = df.ffill()

        # -------------------------------------------------
        # 4. Reconstruction des colonnes
        # -------------------------------------------------

        raw_df = info["raw_dataframe"]
        header_rows = info["header_rows"]

        if len(header_rows) == 2:

            row_top = raw_df.iloc[header_rows[0]]
            row_bottom = raw_df.iloc[header_rows[1]]

            columns = []

            for top, bottom in zip(row_top, row_bottom):

                if pd.isna(top):
                    top = ""
                elif isinstance(top, (int, float)) and float(top).is_integer():
                    top = str(int(top))
                else:
                    top = str(top).strip()

                if pd.isna(bottom):
                    bottom = ""
                elif isinstance(bottom, (int, float)) and float(bottom).is_integer():
                    bottom = str(int(bottom))
                else:
                    bottom = str(bottom).strip()

                # priorité au nom de la ligne du bas
                if bottom != "":
                    name = bottom
                elif top != "":
                    name = top
                else:
                    name = ""

                columns.append(name)

            if len(columns) == len(df.columns):
                df.columns = columns

        # -------------------------------------------------
        # 5. Nettoyage des noms de colonnes
        # -------------------------------------------------

        new_columns = []

        for i, col in enumerate(df.columns):

            if pd.isna(col):

                name = f"colonne_{i}"

            else:

                name = str(col).strip()

                if (
                    name == ""
                    or name.lower().startswith("unnamed")
                ):
                    name = f"colonne_{i}"

            original = name
            compteur = 1

            while name in new_columns:

                name = f"{original}_{compteur}"

                compteur += 1

            new_columns.append(name)

        df.columns = new_columns

        # -------------------------------------------------
        # 6. Nettoyage des cellules texte
        # -------------------------------------------------

        for col in df.columns:

            if df[col].dtype == object:

                df[col] = (
                    df[col]
                    .astype(str)
                    .str.strip()
                    .replace(
                        {
                            "nan": None,
                            "None": None,
                            "": None
                        }
                    )
                )

        # -------------------------------------------------
        # 7. Conversion automatique des colonnes numériques
        # -------------------------------------------------

        for col in df.columns:

            try:

                converted = pd.to_numeric(
                    df[col],
                    errors="coerce"
                )

                ratio = converted.notna().sum() / len(df)

                if ratio >= 0.8:

                    df[col] = converted

            except Exception:
                pass

        # -------------------------------------------------
        # 8. Suppression des doublons
        # -------------------------------------------------

        df.drop_duplicates(inplace=True)

        # -------------------------------------------------
        # 9. Réinitialisation des index
        # -------------------------------------------------

        df.reset_index(
            drop=True,
            inplace=True
        )

        return df