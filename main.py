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

matrice_in_files=get_matrix(liste_names_cleaned,main_list(liste_names_cleaned))
copy_file(directory,liste_names_cleaned)

clean_files(liste_names_cleaned)


main_menu(liste_names_cleaned,directory,dic_last_names,matrice_in_files)
