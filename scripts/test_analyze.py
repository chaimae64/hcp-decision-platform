from analyze_file import analyze_file


file = "../uploads/Taux de chômage par sexe et région_2026-07-06.xlsx"


result = analyze_file(file)


print("\nRésumé du fichier")
print("----------------")

print("Nombre de lignes :", result["rows"])

print("Colonnes :")
for col in result["columns"]:
    print("-", col)


print("\nTypes :")
print(result["types"])


print("\nColonnes vides :")
print(result["empty_columns"])