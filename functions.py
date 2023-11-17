import os
directory = "C:\ProjPython"

def list_of_files(directory, extension): 
    files_names = [] 
    for filename in os.listdir(directory): 
        if filename.endswith(extension): 
            files_names.append(filename) 
    return files_names

def get_LastNames(files_names):
    names_files=open("names_files.txt","w+")
    for i in range(len(files_names)):
        names_files.write(files_names[i])
        names_files.write("\n")

    first_replace="Nomination_"
    sec_replace=".txt"
    liste_lastNames=[]
    names_files.seek(0)
    lines=names_files.readlines()
    for j in range(len(files_names)):
        content=lines[j]
        new_content=content.replace(first_replace,"").replace(sec_replace,"").replace("1","").replace("2","").replace("\n","")
        liste_lastNames.append(new_content)
    return liste_lastNames


def add_FirstName(liste_lastNames):
    dic_last_names=list(dict.fromkeys(liste_lastNames))
    firstNames=open("firstNames.txt","w")
    for i in range (len(dic_last_names)):
        if dic_last_names[i]=="Chirac":
            dic_last_names[i]="Jacques"+" "+dic_last_names[i]+"  "
        elif dic_last_names[i]=="Giscard dEstaing":
            dic_last_names[i]="Valerie"+" "+dic_last_names[i]+"  "
        elif dic_last_names[i]=="Hollande":
            dic_last_names[i]="Francois"+" "+dic_last_names[i]+"  "
        elif dic_last_names[i]=="Macron":
            dic_last_names[i]="Emannuel"+" "+dic_last_names[i]+"  "
        elif dic_last_names[i]=="Mitterand":
            dic_last_names[i]="Francois"+" "+dic_last_names[i]+"  "
        elif dic_last_names[i]=="Sarkozy":
            dic_last_names[i]="Nicolas"+" "+dic_last_names[i]+"  "
    for i in range(len(dic_last_names)):
        firstNames.write(dic_last_names[i])
        firstNames.write("\n")
    return dic_last_names

def display_Names(dic_last_names):
    firstNames=open("firstnames.txt","r")
    names=firstNames.readlines()
    for i in range(len(dic_last_names)):
        print(names[i])

#fonction pour remplacer les caracteres et les mettres dans les fichiers clean, probleme il ne trouve pas les fichiers .txt de base alors quils sont bien là
'''
def cleaned_sorted(directory,liste_names_cleaned):
    j=0
    list_sorted=list_of_files(directory,extension=".txt")

    for i in list_sorted:
        #list_sorted[j]=list_sorted[j].replace(".txt","")
        liste_names_cleaned[j]=open(liste_names_cleaned[j],"w")
        with open(list_sorted[j],"r") as file:
            content=file.read
        for char in content:
            print(char)
            if ord(char)>=65 or ord(char)<=90:
                char=chr(ord(char)-32)
                liste_names_cleaned[j].write(char)
        j+=1

'''