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

# copies the contents of the base files into those of the files to be able to clean them
def copy_file(directory,list_names_cleaned):
    liste_sorted=list_of_files(directory,".txt")
    j=0
    for i in liste_sorted:
        file_path=os.path.join(directory,liste_sorted[j])
        with open (file_path,"r") as file:
            content=file.read()
            #copy text
        with open (list_names_cleaned[j],"w") as out_file:
            out_file.write(content)
            #and past it
        j+=1


#function to replace capital letters and punctuation
def clean_files(list_names_cleaned):
    for i in list_names_cleaned:
        with open (i,"r") as file:
            content=file.read()
            #copy text
        modified_content = ""
        for char in content:
            if ord(char)<=90 and ord(char)>=65:
                char=chr(ord(char)+32)
                #change the text by removing capital letters
            if (ord(char)<=47 and ord(char)>=33) or char==";" or char=="?":
                char=chr(32)
                #remove punctuation marks
            modified_content+=char
        with open (i,"w") as file:
            file.write(modified_content)
            #replaces the original text with the new text without capital letters

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


def who_spoke_first(dico_of_names):
    first="none"
    list_of_names=["Giscard dEstaing","Mitterand","Chirac","Sarkozy","Hollande","Macron"]
    for i in list_of_names:
        if dico_of_names[i]!=0:
            first=i
            break
    return first
#menu 1 as match thanks to algorithmics
def menu(dic_last_names, liste_names_cleaned):
    user_input = input("What would you like to do:\n"
                       "     1) Display list of names\n"
                       "     2) Display the list of unimportant word\n"
                       "     3) Display the word with the highest TF-IDF score\n"
                       "     4) Display the most repeated words by Chirac\n"
                       "     5) Display the list of president who spoke of the Nation\n"
                       "     6) Display the first president who talked about climate or ecology\n"
                       "     7) Display which non-unimportant words did all the presidents mention\n"
                       "     8) Exit\n"
                       "-> ")

    try:
        choice = int(user_input)
    except ValueError:
        print("Invalid input.\n")
        return menu(dic_last_names, liste_names_cleaned)

    match choice:
        case 1:
            display_Names(dic_last_names)
            print("\n")
        case 2:
            print(calculate_unimportant_word(liste_names_cleaned))
            print("\n")
        case 3:
            print("processing...")
            a = tfidf_of_main_dico(main_dico(liste_names_cleaned), liste_names_cleaned)
            max_score = max(a.values())
            max_score_words = [word for word, score in a.items() if score == max_score]
            print(f"Word(s) with the highest TF-IDF score(s): {max_score_words}")
            print("\n")
        case 4:
            print(most_repeated_words_Chirac(liste_names_cleaned))
            print("\n")
        case 5:
            print("Here is the list of the presidents who spoke about the nation and how many times they said it")
            print(spoke_of_("nation", liste_names_cleaned))
            print("\n")
        case 6:
            print("The first president to talk about climate is", who_spoke_first(spoke_of_("climate", liste_names_cleaned)))
            print("The first president to talk about ecology is", who_spoke_first(spoke_of_("écologie", liste_names_cleaned)))
            print("\n")
        case 7:
            print("If all the presidents mentioned a word then its IDF score would be 0, making it an unimportant word.")
            print("So there are no words that have been said by every president that aren't unimportant\n")
        case 8:
            exit()
        case _:
            print("Invalid choice. Please select a number between 1 and 8.\n")

    # Recall the menu unless the user chooses to exit (option 8)
    if choice != 8:
        menu(dic_last_names, liste_names_cleaned)
 