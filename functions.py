import os
import math
from collections import defaultdict
from collections import Counter
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
            if (ord(char)<=47 and ord(char)>=33) or char==";" or char=="?":
                char=chr(32)
                #enleve les signes de ponctuations
            modified_content+=char
        with open (i,"w") as file:
            file.write(modified_content)
            #remplace le texte originel par le nouveau texte sans majuscule

def get_most_mentioned_words(word_count_dict):
    most_mentioned_word = max(word_count_dict, key=word_count_dict.get)
    max_count = word_count_dict[most_mentioned_word]
    most_mentioned_words = [word for word, count in word_count_dict.items() if count == max_count]
    return most_mentioned_words, max_count


def calculate_tf_single_file(word, document):
    with open(document,"r",encoding="utf-8") as file:
        txt=file.read()
    content=txt.split()
    word_count = content.count(word)
    total_words = len(content)
    return word_count / total_words if total_words > 0 else 0

def calculate_tf_all_files(word,all_doc):
    tf_value=0
    for i in all_doc:
        tf_value+=calculate_tf_single_file(word,i)
    return tf_value

def calculate_idf(word, all_documents):
    count = 0
    for file_name in all_documents:
        with open(file_name, "r", encoding="utf-8") as file:
            txt = file.read()
        content=txt.split()
        if word in content:
            count += 1
    return math.log(len(all_documents) / (count )) if count!=0 else 0

def calculate_tfidf(word,all_doc):
    a=calculate_tf_all_files(word,all_doc)
    val_idf=calculate_idf(word,all_doc)
    tfidf_word=(a*val_idf)
    return tfidf_word

def calculate_unimportant_word(all_doc):
    with open(all_doc[0],"r",encoding="utf-8") as file:
        txt=file.read()
    content=txt.split()
    list_unimportant=[]
    for i in content:
        a=calculate_idf(i,all_doc)
        if a==0:
            list_unimportant.append(i)
    return list_unimportant

def main_dico(all_doc):
    content=""
    for i in all_doc:
        with open(i,"r",encoding="utf-8") as file:
            txt=file.read()
        content+=txt
    word=content.split()
    words=Counter(word)

    main_dico = {word: count for word, count in words.items()}
    return main_dico

def tfidf_of_main_dico(main_dico,all_doc):
    main_dico_tfidf={}
    for i in main_dico:
        main_dico_tfidf[i]=calculate_tfidf(i,all_doc)
    return main_dico_tfidf

def highest_scores(main_dico_tfidf):
    max_score = max(main_dico_tfidf.values())
    max_score_words = [word for word, score in main_dico_tfidf.items() if score == max_score]

    return max_score_words

def most_repeated_words_Chirac(doc):
    content=""
    for i in doc[:2]:
        with open(i,"r",encoding="utf-8") as file:
            txt=file.read()
        content+=txt
    list_content=content.split()
    word_counts = Counter(list_content)
    most_common_words = word_counts.most_common()
    max_count = most_common_words[0][1]
    most_repeated_words = [word for word, count in most_common_words if count == max_count]

    return most_repeated_words

def spoke_of_(word,all_doc):
    dico_nation={}
    tmp=0
    for file_name in all_doc:
        with open(file_name, "r", encoding="utf-8") as file:
            txt = file.read()
        content=txt.split()
        for j in content:
            name=file_name
            if j==word:
                tmp+=1
            dico_nation[name.replace("Nominations_","").replace("1","").replace("2","").replace("_cleaned","")]=tmp
    return dico_nation


def menu(dic_last_names,liste_names_cleaned):
    maxi=8
    user_input=input("What would you like to do:\n"
          "     1) Display list of names\n"
          "     2) Display the list of unimportant word\n"
          "     3) Display the word with the highest TF-IDF score\n"
          "     4) Display the most repeated words by Chirac\n"
          "     5) Display the list of president who spoke of the Nation\n"
          "     6) Display the first president who talked about climate or ecology\n"
          "     7) Display wich non-unimportant words did all the presidents mentionned\n"
          "     8) Exit"
          "->")
    try:
        choice = int(user_input)
    except ValueError:
        print("Invalid input.")
        print("\n")
        menu(dic_last_names,liste_names_cleaned)
    if choice>maxi:
        print("Invalid input.")
        print("\n")
        menu(dic_last_names,liste_names_cleaned)
    if choice==1:
        display_Names(dic_last_names)
        print("\n")
        menu(dic_last_names,liste_names_cleaned)
    elif choice==2:
        print(calculate_unimportant_word(liste_names_cleaned))
        print("\n")
        menu(dic_last_names,liste_names_cleaned)
    elif choice==3:
        print("processing...")
        a=tfidf_of_main_dico(main_dico(liste_names_cleaned),liste_names_cleaned)
        max_score = max(a.values())
        max_score_words = [word for word, score in a.items() if score == max_score]
        print(f"Word(s) with the highest TF-IDF score(s): {max_score_words}")
        print("\n")
        menu(dic_last_names,liste_names_cleaned)
    elif choice==4:
        print(most_repeated_words_Chirac(liste_names_cleaned))
        print("\n")
    elif choice==5:
        print("Here is the liste of the presidents who spoke about the nation and how many times they said it")
        print(spoke_of_("nation",liste_names_cleaned))
        print("\n")
        menu(dic_last_names,liste_names_cleaned)
    elif choice==6:
        #print(spoke_of_("climat",liste_names_cleaned))
        #print(spoke_of_("écologie",liste_names_cleaned))
        print("The first president who spoke of climate is 'Mitterand'\n")
        menu(dic_last_names,liste_names_cleaned)
    elif choice==7:
        print("If all the presidents mentionned a word then it's IDF score would be 0, which would make it a unimportant word.")
        print("So there is no words that have been said by every presidents that isnt unimportant\n")
        menu(dic_last_names,liste_names_cleaned)
    elif choice==8:
        exit()

    