import operator
import wikipedia
from stop_words import get_stop_words
from tabulate import tabulate

word = '0'
stopwordbool = '0'
stop_words = get_stop_words('en')
stop_words.append('the')

# taking the input search query
def query():
    global word
    word = input("\nEnter the query to seach for - ")
    if(len(word) <= 2):
        print("\n Enter a valid query Enter another query")
        query()

# taking input stop words boolean
def stop_words_bool():
    global stopwordbool
    stopwordbool = input('\nDo you want to include Stop Words (y or n)- ')
    if(stopwordbool=='y' or stopwordbool=='Y'):
        stopwordbool = True
    elif(stopwordbool=='n' or stopwordbool=='N'):
        stopwordbool = False
    else:
        print("\nEnter a valid input!!!")
        stop_words_bool()
# calling the input functions
query()
stop_words_bool()


# removing the unnecessary symbols and storing the results in a new list.
def clean_list(word_list):
    clean_word_list = []
    symbols = "~`!@#$%^&*()_-=+/*-|}{[]:;><,.?\'\""
    for item in word_list:
        for i in range(0,len(symbols)):
            item = item.replace(symbols[i],'')
        if len(item) > 0:
            clean_word_list.append(item.lower())
    if stopwordbool == False:
        remove_stop_words(clean_word_list)
    else:
        word_frequency(clean_word_list)

# if add_stop_words is false the stop words are removed
def remove_stop_words(clean_word_list):
    stop_word_removed = [x for x in clean_word_list if x not in stop_words]
    word_frequency(stop_word_removed)

# making a dictionary for storing word frequency and sorting it...
def word_frequency(clean_word_list):
    word_freq = {}
    for item in clean_word_list:
        if item not in word_freq:
            word_freq[item] = 1
        else:
            word_freq[item] += 1
    sorted_word_freq = sorted(word_freq.items(), key=operator.itemgetter(1), reverse=True)
    # printing the first 20 sorted elements of dictionary in table format.
    print(tabulate(sorted_word_freq[:20],headers=["Word","Count"],tablefmt = "fancy_grid"))


# getting the summary and storing each word in a list if the page is found. If multiple pages found then get the summary for the first page. If no page found then exit.
def get_summary(word_query):
    word_list = []
    try:
        summary = wikipedia.summary(word_query).split()
        for item in summary:
            word_list.append(item)
        # calling the function
        clean_list(word_list)
    # if multiple pages found
    except wikipedia.exceptions.DisambiguationError as e:
            get_summary(e.options[0])
    # if no pages found
    except wikipedia.exceptions.PageError:
        print("Sorry, No such page found. Try for another search.")
        quit()

# calling the function
get_summary(word)