#Python project : My first chatBot by Marceau Bilger and Paul Mahaut
#Here is the heart of the project, where all functions are and work together to satisfy main.py requests


# Import useful libraries for the rest of the programm
import os 
import math
from collections import defaultdict #Idk
from collections import Counter #Equivalent of incrementing a counter
directory = "C:\ProjPython" #We use the absolute path so the programm can work on any computer 


'''#Return list containing the names of all the files in the directory with the specified extension.
    Parameters:
    directory (str): The directory path to search in.
    extension (str): The file extension to filter files by.
    Returns:
    list: A list of filenames (str) that match the given extension.'''
def list_of_files(directory, extension): 
    files_names = [] 
    for filename in os.listdir(directory): 
        if filename.endswith(extension): 
            files_names.append(filename) 
    return files_names
   

'''#This function extracts and returns the last names of the presidents from the filenames (as a list).
    Parameters:
    files_names (list): A list of filenames (str) to extract last names from.
    Returns:
    list: A list of extracted last names (str).'''
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

'''#add_FirstName at the list_lastNames and return it as a dictionnary with complete president name as values 
    Parameters:
    liste_lastNames (list): A list of last names (str) to add first names to.
    Returns:
    dict: A dictionary with complete names (str) as values.'''
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
        with open (file_path,"r",encoding="utf-8") as file:
            content=file.read()
            #copy text
        with open (list_names_cleaned[j],"w",encoding="utf-8") as out_file:
            out_file.write(content)
            #and past it
        j+=1


#function to replace capital letters and punctuation
def clean_files(list_names_cleaned):
    for i in list_names_cleaned:
        with open (i,"r",encoding="utf-8") as file:
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
        with open (i,"w",encoding="utf-8") as file:
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
    #total_words = len(content)
    return word_count #/ total_words if total_words > 0 else 0

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
    return math.log10(len(all_documents) / (count )) if count!=0 else 0

def calculate_tfidf(word,all_doc): #Apply the compute of tf-idf
    a=calculate_tf_all_files(word,all_doc)
    val_idf=calculate_idf(word,all_doc)
    tfidf_word=(a*val_idf)
    return tfidf_word

def calculate_unimportant_word(all_doc):#Calculate unimportant words
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

def remove_duplicates_ordered(word_list):# remove repeating elements in a list
    seen = set()
    unique_words = []

    for i in word_list:
        if i not in seen:
            seen.add(i)
            unique_words.append(i)

    return unique_words

def main_list(all_doc): #Where we stock useful values 
    content=""
    for i in all_doc:
        with open(i,"r",encoding="utf-8") as file:
            txt=file.read()
        content+=txt
    word=content.split()
    main_list=remove_duplicates_ordered(word)
    #words=Counter(word)

    #main_dico = {word: count for word, count in words.items()}
    return main_list

def tfidf_of_main_dico(main_dico,all_doc): #Use the main dico for compute a pertinent tf-idf
    main_dico_tfidf={}
    for i in main_dico:
        main_dico_tfidf[i]=calculate_tfidf(i,all_doc)
    return main_dico_tfidf

def highest_scores(main_dico_tfidf): #finding the word(s) which has the highest tf-idf 
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
    j=0
    for i in list_content:
        j+=1
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

def get_matrix(liste_names_cleaned,main_list):
    matrix=[]
    for i in main_list:
        l=[]
        tmp_idf=calculate_idf(i,liste_names_cleaned)
        for j in liste_names_cleaned:
            l.append(tmp_idf*calculate_tf_single_file(i,j))
        matrix.append(l)
    return matrix

def transpose_matrix(matrix):
    rows, cols = len(matrix), len(matrix[0])
    
    transposed_matrix = [[0 for _ in range(rows)] for _ in range(cols)]

    for i in range(rows):
        for j in range(cols):
            transposed_matrix[j][i] = matrix[i][j]

    return transposed_matrix
    

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
                       "     8) Ask a question to our amazing chatbot"
                       "     9) Exit\n"
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
            a = tfidf_of_main_dico(main_list(liste_names_cleaned), liste_names_cleaned)
            max_score = max(a.values())
            max_score_words = [word for word, score in a.items() if score == max_score]
            print(f"Word(s) with the highest TF-IDF score(s): {max_score_words}")
            print("\n")
        case 4:
            print("The most repeated word by Chirac is:",most_repeated_words_Chirac(liste_names_cleaned))
            print("\n")
        case 5:
            print("Here is the list of the presidents who spoke about the nation and how many times they said it")
            print(spoke_of_("nation", liste_names_cleaned))
            print("\n")
        case 6:
            print("The first president to talk about climate is", who_spoke_first(spoke_of_("climat", liste_names_cleaned)))
            print("The first president to talk about ecology is", who_spoke_first(spoke_of_("écologie", liste_names_cleaned)))
            print("\n")
        case 7:
            print("If all the presidents mentioned a word then its IDF score would be 0, making it an unimportant word.")
            print("So there are no words that have been said by every president that aren't unimportant\n")
        case 8:
            #à programmer
       # case 9:
            exit()
        case _:
            print("Invalid choice. Please select a number between 1 and 9.\n")

    # Recall the menu unless the user chooses to exit (option 8)
    if choice != 8:
        user_decision=input("Do you want to make a new request ? 1:Yes  2:Go back to main menu  3:Exit ")
        if user_decision==1:
            menu(dic_last_names, liste_names_cleaned)
        elif user_decision==2:
            main_menu(liste_names_cleaned,directory,dic_last_names)
    else:
        exit()
def menu2(liste_names_cleaned,directory,dic_last_names):
    user_input=input("What would you like to do: \n"
                     "      1)Enter a question\n"
                     "      2)Go back to main menu\n"
                     "      3)Exit\n")
    choice=0
    try:
        choice = int(user_input)
    except ValueError:
        print("Invalid input.\n")
        menu2(liste_names_cleaned,directory,dic_last_names)
    if choice==1:
        question=input("Enter your question: \n")
        vector_question=calculate_tfidf_question(clean_question(question),liste_names_cleaned)
        non_zero=False
        for i in vector_question.values():# check if the tfidf vector of the question is 0
            if i!=0:
                non_zero=True
        if non_zero==True:
            matrice_in_files=calculate_tfidf_question_in_files(vector_question,liste_names_cleaned,get_matrix(liste_names_cleaned,main_list(liste_names_cleaned)))
            liste_val=complicatedd_formula(vector_question,matrice_in_files)
            files_names = list_of_files(directory, "txt")
            a,b=find_file(liste_val,files_names,vector_question,directory)
            print("And the answer is :",a,"\nIt is found in the file : \n",b)
        else:
            print("This question can not be computed as all of the words are either not in the corpus or are unimportant words\n")

    elif choice==2:
        main_menu(liste_names_cleaned,directory,dic_last_names)
    elif choice==3:
        exit()
    elif choice>3:
        print("Invalid input.\n")
        menu2(liste_names_cleaned,directory,dic_last_names)

    if choice != 3:
        second_choice=0
        user_decision=int(input("Do you want to make a new request ? 1:Yes  2:Go back to main menu  3:Exit "))
        try:
            second_choice=int(user_decision)
        except ValueError:
            print("Invalid input")
            menu2(liste_names_cleaned,directory,dic_last_names)
        if user_decision==1:
            menu2(liste_names_cleaned,directory,dic_last_names)
        elif user_decision==2:
            main_menu(liste_names_cleaned,directory,dic_last_names)
    else:
        exit()

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
    cleaned_liste=cleaned_string.split()
    cleaned_liste = [word for word in cleaned_liste if word not in ["comment", "pourquoi"]]
    return cleaned_liste

def is_word_in_corpus(cleaned_liste,main_list):# Not useful, we keep it in case.
    cleaned_liste_corpus = [word for word in cleaned_liste if word in main_list]
    return cleaned_liste_corpus

def calculate_tfidf_question(cleaned_liste,liste_names_cleaned):#takes the question and calculates the tfidf score of each word
    dico_tfidf={}
    unimprtant=calculate_unimportant_word(liste_names_cleaned)
    for i in cleaned_liste:
        if i in dico_tfidf.keys():
           dico_tfidf[i]+=1
        else:
            dico_tfidf[i]=1
    for i in dico_tfidf.keys():
        if i in unimprtant:
            dico_tfidf[i]=0
        else:
            dico_tfidf[i]=dico_tfidf[i]*calculate_idf(i,liste_names_cleaned)
    return dico_tfidf


def calculate_tfidf_question_in_files(dico_tfidf,liste_names_cleaned,matrix):#takes the value of each word of the question in the files using the matrix
    a=main_list(liste_names_cleaned)
    l_val_tfidf_in_files=[]
    for j in range(len(liste_names_cleaned)):
        l_tmp=[]
        for i in dico_tfidf.keys():
            if i in a:
                index_of_i=a.index(i)
                val_of_i=matrix[index_of_i][j]

            else:
                val_of_i=0
            l_tmp.append(val_of_i)
        l_val_tfidf_in_files.append(l_tmp)
    return l_val_tfidf_in_files #return a matrix with 8 rows and as many columns as there are words in the question

def scalar_product(dico_question,vecteur_files): #calculate the scalar product of the dico tfidf transformed into a list and the vector taken from the matrix
    vecteur_question=list(dico_question.values())
    summ=0
    for i in range(len(vecteur_files)):
        summ+=vecteur_question[i]*vecteur_files[i]
    return summ

def sum_square_vecteur(vecteur):# calculates the sum of the squared elements of a list
    sum_of_squares = 0
    for num in vecteur:
        sum_of_squares += num ** 2
    return sum_of_squares

def complicatedd_formula(dico_tfidf,l_val_tfidf_in_files):# calculate the formula with sums and roots
    liste_val_formula=[]
    for i in range(0,8):
        a=scalar_product(dico_tfidf,l_val_tfidf_in_files[i])
        b=math.sqrt(sum_square_vecteur(dico_tfidf.values()))*math.sqrt(sum_square_vecteur(l_val_tfidf_in_files[i])) 
        big_val=a/b
        liste_val_formula.append(big_val)
    return liste_val_formula

def find_file(liste_val_formula,files_names,dico_tfidf,directory):
    #takes the result of the formula, finds the maximum value, takes the file corresponding to the index of the value
    index=liste_val_formula.index(max(liste_val_formula))
    highest_word= max(dico_tfidf, key=dico_tfidf.get)
    full_file_path = os.path.join(directory, files_names[index])
    sentence=first_sentence_with_appearance(full_file_path,highest_word)
    return sentence,index

def first_sentence_with_appearance(file_path, target_word):#finds the first appearance of a word in a file and returns the corresponding phrase
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        sentences = text.split('.')
        for sentence in sentences:
            words = sentence.split()
            if target_word in words:
                return sentence.strip()

    return None 


def main_menu(liste_names_cleaned,directory,dic_last_names):
    user_input=input("Which functionnalities would you like to use: \n"
                     "      1)Part 1\n"
                     "      2)Part 2\n"
                     "      3)Exit\n")
    try:
        choice = int(user_input)
    except ValueError:
        print("Invalid input.\n")
        return main_menu(liste_names_cleaned,directory,dic_last_names)
    if choice==1:
        menu(dic_last_names,liste_names_cleaned)
    elif choice==2:
        menu2(liste_names_cleaned,directory,dic_last_names)
    elif choice==3:
        exit()
    elif choice>3:
        print("Invalid input.\n")
        main_menu(liste_names_cleaned,directory,dic_last_names)