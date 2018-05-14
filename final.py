import wikipedia #wrapper for the wikipedia api that simplifies commands
import wptools   #wrapper for wikipedia api that specializes with getting wikidata
import re
import warnings
import atexit
from time import time, strftime, localtime
from datetime import timedelta



# Dawit Ocbai, calculates time for program execution while user is playing the game
def start_time(elapsed=None):
   if elapsed is None:
       return strftime("%Y-%m-%d %H:%M:%S", localtime())
   else:
       return str(timedelta(seconds=elapsed))

def log(s, elapsed=None):
   time = "="*40
   print(time)
   print(start_time(), '-', s)
   if elapsed:
       print("Elapsed time:", elapsed)
   print(time)
   print()

def game():
   end = time()
   elapsed = end-start
   log("End Program", start_time(elapsed))

start = time()
atexit.register(game)
log("Start Program")


#Sets the difficulty for the trivia game. Difficulty is based off the number of sentences shown from the wikipedia page's summary. 1 sentence=hard, 2 sentences= medium, 3 sentences= easy (more sentences give the user more information to guess from)-Stanford Chang
def difficulty_rating():
    difficulty=0
    ratings=["1","2","3"]
    rating=input("How difficult do you want your questions to be? Type '1' for Easy, '2' for Medium, and '3' for Hard. ")
    while not rating in ratings:
        rating=input("Please only enter '1','2', or '3'")
    else:
        if rating==str(1):
            difficulty+=3
        elif rating==str(2):
            difficulty+=2
        elif rating== str(3):
            difficulty+=1
        return difficulty
difficulty=difficulty_rating()


warnings.filterwarnings('ignore',category=UserWarning) #Get's rid of html parsing warning resulting from a bug in the wptool's wrapper

summary_list=[] #List of the first sentence from each gathered wikipedia page's summary tab. These will act as the "questions" for the trivia game
titles=[] #List of titles for wikipedia pages. These will act as the "answers" in the trivia game
user_input=""
excluded_aliases=['the','The','Of','of','and','And','name']

while user_input!="done":
  user_input = input("Please enter the items you want to be tested on. When finished, type 'done' ")
  if user_input!="done":
      try:
          search = str(wikipedia.page(user_input, auto_suggest=True, redirect=True)) #Uses wikipedia Api to search for closest page match to user input and then takes the tile from the page to append to the titles list
          for match in re.findall(r"[^']*'(.+)'", search):
              titles.append(match)
      except:
          wikipedia.exceptions.DisambiguationError
          print("sorry, your item, " + user_input + " ,was not a valid wikipedia entry. Please re-enter your values")


for item in titles:
   summ=wikipedia.summary(item,sentences=difficulty,auto_suggest=True, redirect=True) #takes the first sentence of the summary of the page that was matched to the user's input.
   page = wptools.page(item)
   print("\nGetting data from Wikidata...\n")
   page.get_wikidata(item) #gets the wikidata for the page
   aliases=page.data["aliases"] #gets the "aliases" from the page's wikidata, searches for any instance of an alias in the summary, and replaces it with question marks
   splitted_aliases=[]

   for item in aliases:
       splitted_aliases.extend(item.split())#Splits the aliases list by spaces so each word becomes an item
   splitted_aliases=[x for x in splitted_aliases if x not in excluded_aliases] #prevents common words from being hidden in the summary even if they were in aliases

   for item in splitted_aliases:
       if item in summ:
           summ=summ.replace(item,"???")
   summary_list.append(summ)

question_dict = dict(zip(summary_list, titles)) #dictionary containing the summaries as keys and titles as values


def questions(): #turns the summaries into questions that have to be answered with the correlating title/name.- James Geleta
    for key,value in list(question_dict.items()):
        value=value.lower()
        print(key)
        user_answer = input("\nWho/What do you think is being described? Type the exact name (no nicknames): ")
        user_answer = user_answer.lower()
        while user_answer != value:
            user_answer=(input("You're guess was wrong. Guess again:")).lower()
        else:
            print("Your guess was correct! Congratulations!")
            del question_dict[key]
        continue


questions()

# random pick a question and calculate score- Jiale Xu
import random
print("You have 5 chances!")
print(random.choice(summary_list))


# class for all users- Jiale Xu
class players:

   userCount = 0

   def __init__(self, name, score):
       self.name = name
       self.score = score
       players.userCount += 1

   def playCount(self):
       print("You totally play for 5 times")


   def displayplayer(self):
       print("Name : ", self.name, ", Score: ", self.score)

# calculate score
scores_total = 0
if user_answer = value:
   scores_total = difficulty * 10
else:
   scores_total = difficulty * 5

check_result = input("Do you want to see your ranking, enter yes or no: ")
if check_result == 'yes' or 'YES' or 'Yes':
   player_name = input("PLease enter your name: ")
   player_score = scores_total

   player1 = players(player_name, player_score)
   player1.displayplayer()
   print("Total players: " + players.userCount )

else:
   print("Thank you for playing the game!")

