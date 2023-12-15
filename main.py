import os
from functions import *
directory = "speeches"

liste_names_cleaned=["Nominations_Chirac1_cleaned","Nominations_Chirac2_cleaned","Nominations_Giscard dEstaing_cleaned","Nominations_Hollande_cleaned","Nominations_Macron_cleaned","Nominations_Mitterand1_cleaned","Nominations_Mitterand2_cleaned","Nominations_Sarkozy_cleaned"]
try:
    os.mkdir("cleaned")
except:
    print("")

files_names = list_of_files(directory, "txt")

liste_lastNames=get_LastNames(files_names)

dic_last_names=add_FirstName(liste_lastNames)


copy_file(directory,liste_names_cleaned)

clean_files(liste_names_cleaned)

#menu(dic_last_names,liste_names_cleaned)
a=clean_question("nation Je viens de déposer une version corrigée du projet en me basant sur les retours que m'ont fait vos enseignants de TP.")
b=is_word_in_corpus(a,main_set(liste_names_cleaned))
print(b)

print(calculate_tfidf_question(b,liste_names_cleaned))
print(len(calculate_tfidf_question(b,liste_names_cleaned)))

