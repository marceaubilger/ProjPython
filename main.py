
from functions import list_of_files
from functions import get_LastNames
from functions import add_FirstName
from functions import display_Names


directory = "C:\ProjPython\speeches"

files_names = list_of_files(directory, "txt")

liste_lastNames=get_LastNames(files_names)

dic_last_names=add_FirstName(liste_lastNames)

display_Names(dic_last_names)
