#Import useful libraries for the rest of the programm
import os 
import math
from collections import defaultdict #Idk
from collections import Counter #Equivalent of incrementing a counter
directory = "C:\ProjPython" #We use the absolute path so the programm can work on any computer 

def list_of_files(directory, extension): #Return list containing the names of all the files in the directory with the specified extension.
    files_names = [] 
    for filename in os.listdir(directory): 
        if filename.endswith(extension): 
            files_names.append(filename) 
    return files_names

def get_LastNames(files_names):  #This function extracts and returns the last names of the presidents from the filenames (as a list).
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


def add_FirstName(liste_lastNames): #add_FirstName at the list_lastNames and return it as a dictionnary with complete president name as values 
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

def display_Names(dic_last_names):#Open result of our two last functions and display it
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

def get_most_mentioned_words(word_count_dict): #Compute and give the most mentioned words with how many times it have been pronounced
    most_mentioned_word = max(word_count_dict, key=word_count_dict.get)
    max_count = word_count_dict[most_mentioned_word]
    most_mentioned_words = [word for word, count in word_count_dict.items() if count == max_count]
    return most_mentioned_words, max_count


def calculate_tf_single_file(word, document): #calculate the tf of one single file
    with open(document,"r",encoding="utf-8") as file:
        txt=file.read()
    content=txt.split()
    word_count = content.count(word)
    total_words = len(content)
    return word_count / total_words if total_words > 0 else 0

def calculate_tf_all_files(word,all_doc): #make sum of all single tf 
    tf_value=0
    for i in all_doc:
        tf_value+=calculate_tf_single_file(word,i)
    return tf_value

def calculate_idf(word, all_documents): #Calculate idf
    count = 0
    for file_name in all_documents:
        with open(file_name, "r", encoding="utf-8") as file:
            txt = file.read()
        content=txt.split()
        if word in content:
            count += 1
    return math.log(len(all_documents) / (count )) if count!=0 else 0

def calculate_tfidf(word,all_doc): #Apply the compute of tf-idf
    a=calculate_tf_all_files(word,all_doc)
    val_idf=calculate_idf(word,all_doc)
    tfidf_word=(a*val_idf)
    return tfidf_word

<<<<<<< Updated upstream
def calculate_unimportant_word(all_doc):#Calculate unimportant words
=======

def calculate_unimportant_word(all_doc):
>>>>>>> Stashed changes
    with open(all_doc[0],"r",encoding="utf-8") as file:
        txt=file.read()
    content_liste=txt.split()
    content_set=set(content_liste)
    content_liste=list(content_set)
    list_unimportant=[]
    for i in content_liste:
        a=calculate_idf(i,all_doc)
        if a==0:
            list_unimportant.append(i)
    return list_unimportant

def main_dico(all_doc): #Where we stock useful values 
    content=""
    for i in all_doc:
        with open(i,"r",encoding="utf-8") as file:
            txt=file.read()
        content+=txt
    word=content.split()
    words=Counter(word)

    main_dico = {word: count for word, count in words.items()}
    return main_dico

def tfidf_of_main_dico(main_dico,all_doc): #Use the main dico for compute a pertinent tf-idf
    main_dico_tfidf={}
    for i in main_dico:
        main_dico_tfidf[i]=calculate_tfidf(i,all_doc)
    return main_dico_tfidf

def highest_scores(main_dico_tfidf): #finding the word(s) which has the highest tf-idf 
    max_score = max(main_dico_tfidf.values())
    max_score_words = [word for word, score in main_dico_tfidf.items() if score == max_score]

    return max_score_words

<<<<<<< Updated upstream
def most_repeated_words_Chirac(doc): #Finding the most_repeated words by Jacques Chirac
=======
def most_repeated_words_Chirac(doc,list_unimportant_word):
>>>>>>> Stashed changes
    content=""
    for i in doc[:2]:
        with open(i,"r",encoding="utf-8") as file:
            txt=file.read()
        content+=txt
    list_content=content.split()
    j=0
    for i in list_content:
        j+=1
        if i in list_unimportant_word:
            list_content.pop(j)
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


def who_spoke_first(dico_of_names):#take in argument the above function, use its but stop at the first word detection
    first="none"
    list_of_names=["Giscard dEstaing","Mitterand","Chirac","Sarkozy","Hollande","Macron"]
    for i in list_of_names:
        if dico_of_names[i]!=0:
            first=i
            break
    return first
#menu 1 as match thanks to algorithmics
def menu(dic_last_names, liste_names_cleaned): #Menu which permits access previous functions according to user request 
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

<<<<<<< Updated upstream
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
        user_decision=int(input("Do you want to make a new request ? 1: Yes 2: No "))
        if user_decision==1:
            menu(dic_last_names, liste_names_cleaned)
    else:
        exit()

 
=======
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
          "     8) Exit\n"
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
        list_unimportant_word=calculate_unimportant_word(liste_names_cleaned)
        print(list_unimportant_word)
        print(most_repeated_words_Chirac(liste_names_cleaned,list_unimportant_word))
        print("\n")
    elif choice==5:
        print("Here is the liste of the presidents who spoke about the nation and how many times they said it")
        print(spoke_of_("nation",liste_names_cleaned))
        print("\n")
        menu(dic_last_names,liste_names_cleaned)
    elif choice==6:
        print("The first president to talk about climat is",who_spoke_first(spoke_of_("climat",liste_names_cleaned)),"\n")
        print("The first president to talk about climat is",who_spoke_first(spoke_of_("écologie",liste_names_cleaned)),"\n")
        menu(dic_last_names,liste_names_cleaned)
    elif choice==7:
        print("If all the presidents mentionned a word then it's IDF score would be 0, which would make it a unimportant word.\n")
        print("So there is no words that have been said by every presidents that isnt unimportant\n")
        menu(dic_last_names,liste_names_cleaned)
    elif choice==8:
        exit()

    
def menu2(list_names_cleaned):
    maxi=2
    user_input=input("What would you like to do :\n"
                     "      1)Enter a question\n"
                     "      2)Go back to main menu")
    try:
        choice = int(user_input)
    except ValueError:
        print("Invalid input.")
        print("\n")
        menu2(list_names_cleaned)
    if choice>maxi:
        print("Invalid input.")
        print("\n")
        menu2(list_names_cleaned)
    elif choice==1:
        #tbd
        a=a
    elif choice==2:
        main_menu(list_names_cleaned,main_dico)

def clean_question(string):
    cleaned_string=""
    for char in string:
            if ord(char)<=90 and ord(char)>=65:
                char=chr(ord(char)+32)
                #change the text by removing capital letters
            if (ord(char)<=47 and ord(char)>=33) or char==";" or char=="?":
                char=chr(32)
                #remove punctuation marks
            cleaned_string+=char
    return cleaned_string

def remove_unimportant(cleaned_string,liste_unimportant_word):
    liste_cleaned = cleaned_string.split()
    result = [word for word in liste_cleaned if word not in liste_unimportant_word]

    return result

def calculate_tfidf_question(cleaned_liste,liste_names_cleaned):#calcule et return une liste contenant les valeurs tfidf de la question
    tf={}
    idf={}
    tfidf_question=[]
    for i in cleaned_liste:
        tf[i]=cleaned_liste.count(i)/len(cleaned_liste)
        idf[i]=calculate_idf(i,liste_names_cleaned)
        tfidf_question[i]=tf[i]*idf[i]
    return tfidf_question
"""
def calculate_tfidf_corpus(liste_names_cleaned,cleaned_liste,j):# calcule et return une liste avec les valeurs tfidf des mots de la question dans le corpus
    tfidf_liste=[]
    for i in cleaned_liste:
        score=calculate_tf_single_file(i,j)*calculate_idf(i,liste_names_cleaned)
        tfidf_liste.append(score)
    return tfidf_liste

def summ_tfidf(tfidf_liste,tfidf_question,liste_names_cleaned,cleaned_liste):#utilise les 2 fonctions précédentes pour calculer la somme des produits
    summ_all_files=[]
    for j in liste_names_cleaned:
        tfidf_question=calculate_tfidf_question(cleaned_liste,liste_names_cleaned)
        tfidf_liste=(calculate_tfidf_corpus(liste_names_cleaned,cleaned_liste,j))
        summ=[x*y for x, y in zip(tfidf_question,tfidf_liste)]
        summ_all_files.append(summ)
    return summ_all_files



def calculate_complicated_formula(tfidf_summ,cleaned_liste,tfidf_liste,tfidf_question,liste_names_cleaned):
    for i in range(len(liste_names_cleaned)):
        summ=summ_tfidf(tfidf_liste,tfidf_question,liste_names_cleaned,cleaned_liste)
        final_result=summ[i]/


def calculate_word_highest_tfidf(list_without_unimportant,liste_names_cleaned):
    liste_tfidf=[]
    for i in list_without_unimportant:
        liste_tfidf_single_word=[]
        for j in liste_names_cleaned:
            liste_tfidf_single_word.append(calculate_tf_single_file(i,j)*calculate_idf(i,liste_names_cleaned))
        liste_tfidf.append(max(liste_tfidf_single_word))
    return liste_tfidf
    
    
"""
>>>>>>> Stashed changes
