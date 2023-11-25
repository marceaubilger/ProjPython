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

# copie le contenu des files de base dans ceux des fichiers pour pouvoir les clean
def copy_file(directory,list_names_cleaned):
    liste_sorted=list_of_files(directory,".txt")
    j=0
    for i in liste_sorted:
        file_path=os.path.join(directory,liste_sorted[j])
        with open (file_path,"r") as file:
            content=file.read()
            #copie le texte
        with open (list_names_cleaned[j],"w") as out_file:
            out_file.write(content)
            #colle le texte
        j+=1


#fonction pour remplacer les majuscules et la ponctuation
def clean_files(list_names_cleaned):
    for i in list_names_cleaned:
        with open (i,"r") as file:
            content=file.read()
            #copie le texte
        modified_content = ""
        for char in content:
            if ord(char)<=90 and ord(char)>=65:
                char=chr(ord(char)+32)
                #change le texte en enlevant les majuscules
            if ord(char)<=47 and ord(char)>=33:
                char=chr(32)
                #enleve les signes de ponctuations
            modified_content+=char
        with open (i,"w") as file:
            file.write(modified_content)
            #remplace le texte originel par le nouveau texte sans majuscule



def Calculate_TF(word):
    word_input=word.split()
    word_count={}
    for word in word_input:
        word_count[word]=word_count.get(word,0)+1
    return word_count

def Calculate_IDF(liste_names_cleaned):
    word_count_file={}
    for i in liste_names_cleaned:
        with open (i,"r",encoding="utf8") as file:
            content=file.read()
        word_count=Calculate_TF(content)
        for word,count in word_count.items():
            word_count_file[word] = word_count_file.get(word, 0) + count
    return word_count_file


def get_most_mentioned_words(word_count_dict):
    most_mentioned_word = max(word_count_dict, key=word_count_dict.get)
    max_count = word_count_dict[most_mentioned_word]
    most_mentioned_words = [word for word, count in word_count_dict.items() if count == max_count]
    return most_mentioned_words, max_count



def menu(dic_last_names,liste_names_cleaned):
    print("What would you like to do:\n"
          "     1) Display list of names\n"
          "     2) Display the most repeated words by Chirac\n"
          "     3) Display the names of the presidents who spoke of the nation")
    choice=int(input())
    if choice==1:
        display_Names(dic_last_names)
        menu(dic_last_names)
    elif choice==2:
        a=Calculate_IDF(liste_names_cleaned[:2])
        b,c=get_most_mentioned_words(a)
        print("The most repeated word by Chirac is :",b[0],", it is said",c,"times")
        menu(dic_last_names,liste_names_cleaned)

