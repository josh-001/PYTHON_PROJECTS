import random
movie_list = ["inception", "avatar", "gladiator", "interstellar", 
              "titanic", "dangal", "bahubali", "shershaah", "pushpa"]
random_item = random.choice(movie_list)
def play_game():
    random_item = random.choice(movie_list)
    print("Guess the movie name : ","_ "*len(random_item))
    incorrect_attempt=1 # to check for the condition
    s=set() # it stores only unique values
    t=set()
    while incorrect_attempt <= 7 : # brks the loop if the user guessed wrong more than 7 times 
        # enter a character
        x=input("Guess a character").lower()
        if len(x)!=1: # check the lenght of input string if not 1 , break the loop
            print("Enter only one Character")
            break
        # empty string to compare both the movie_name and quess chars after joining
        result=""
        # if input is present in the radom_movie or not
        if x in  s:
            print("The character is already guessed!!")
            continue
        if x in random_item:
            # add  the input to the set
            s.add(x)
            # if present then we will iterate through random_movie 
            for char in random_item:
                # and also check the char is present in s (set), then we will add to the result.
                if char in s:
                    result+=char
                else:
                    result+="_ "
            print(result)
            # checks every time if result is equal to random_movie or not
            if result==random_item:
                print(f"Congratulations! You guessed the movie: {random_item}")
                # if want to play the game again
                # again=input("Want to play again 'y' or 'n':")
                # if again.lower() =='y':
                #     play_game()
                break
        else:
            # stores the input in t (set-unique values)
            if x not in t: # if user gave diff incorrect guess then only it will accept as incorrect_attempmt
                print(f"Incorrect Attempt!, remaining attempts are {7-incorrect_attempt}")
                incorrect_attempt+=1
            t.add(x)
    if incorrect_attempt ==8:
        print(f"Game Over! The movie was: {random_item}")
    # want to play the game again 
    again=input("Want to play again 'y' or 'n':")
    if again.lower() =='y':
        play_game()
play_game()