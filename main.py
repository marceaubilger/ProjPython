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

menu(dic_last_names,liste_names_cleaned)

'''
#### TEST des fonctions 
cleaned_liste=clean_question()
#print(cleaned_liste)

dico_tfidf=calculate_tfidf_question(cleaned_liste,liste_names_cleaned)
print(dico_tfidf)

matrix=get_matrix(liste_names_cleaned,main_list(liste_names_cleaned))

l_val_tfidf_in_files=calculate_tfidf_question_in_files(dico_tfidf,liste_names_cleaned,matrix)
#print(l_val_tfidf_in_files)
#print(len(l_val_tfidf_in_files))

l=complicatedd_formula(dico_tfidf,l_val_tfidf_in_files)
print(l)

print(find_file(l,files_names,dico_tfidf,directory))'''
