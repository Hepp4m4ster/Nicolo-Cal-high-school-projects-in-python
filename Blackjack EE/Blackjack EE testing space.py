import random


decks_number = input("Enter number of decks to use: ")
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]*(int(decks_number)*4)
calculator_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]*(int(decks_number)*4)
calculator_deck.sort()

wins = 0
losses = 0

def deal(deck):
    hand = []
    for i in range(2):
        random.shuffle(deck)
        card = deck.pop()
        calculator_deck.remove(card)
        if card == 11:card = "A"
        hand.append(card)
    return hand

def play_again():
    again = input("Do you want to play again? (Y/N) : ").lower()
    if again == "y":
        global dealer_hand;global player_hand
        dealer_hand = []
        player_hand = []
        game()
    else:
        print("Bye!")
        exit()

def total(hand):
    total = 0
    ace_minus_count = hand.count("A")
    for card in hand:
        if card == "A":
            total += 11
        else:
            total += card
    while total > 21 and ace_minus_count > 0:
        total -= 10
        ace_minus_count -= 1
    return total

def hit(hand):
    card = deck.pop()
    calculator_deck.remove(card)
    if card == 11:card = "A"
    hand.append(card)
    return hand

def P_dealer(n,placementdeck,minusten,goal):
    if n < 17:
        p_sum = 0
        choices = list(set(placementdeck))
        randomlist = []
        randomlist.append(minusten)
        for choice in choices:
            new_deck = placementdeck.copy()
            new_deck.remove(choice)
            new_minusten = randomlist[0]
            total = n + choice
            if choice == 11:
                    new_minusten += 1
            if total > 21 and new_minusten > 0:
                new_minusten -= 1
                total -= 10
            p_sum += P_dealer(total,new_deck,new_minusten,goal)*(new_deck.count(choice)+1)/(len(new_deck)+1)
        return p_sum
    elif n == 17:
        return goal[0]
    elif n == 18:
        return goal[1]
    elif n == 19:
        return goal[2]
    elif n == 20:
        return goal[3]
    elif n == 21:
        return goal[4]
    else:
        return goal[5]
    


def blackjack(dealer_hand, player_hand):
    global wins
    global losses
    if total(player_hand) == 21 == total(dealer_hand):
        print("Both you and the dealer have blackjack, which means play is pushed.\n")
        print(wins, losses)
        dealer_hand = []
        player_hand = []
        game()
    elif total(player_hand) == 21:
        print ("Congratulations! You got a Blackjack!\n")
        wins += 1.5
        print(wins, losses)
        global quit;quit=True
    elif total(dealer_hand) == 21:
        print ("Sorry, you lose. The dealer got a blackjack.\n")
        losses += 1
        print(wins, losses)
        quit=True
    

def score(dealer_hand, player_hand):
        # score function now updates to global win/loss variables
        global wins
        global losses
        if total(player_hand) == 21 == total(dealer_hand):
            print("Both you and the dealer have blackjack, which means play is pushed.\n")
            print(wins, losses)
            dealer_hand = []
            player_hand = []
            game()
        elif total(player_hand) == 21:
            print ("Congratulations! You got a Blackjack!\n")
            wins += 1
            print(wins, losses)
        elif total(dealer_hand) == 21:
            print ("Sorry, you lose. The dealer got a blackjack.\n")
            losses += 1
            print(wins, losses)
        elif total(player_hand) > 21:
            print ("Sorry. You busted. You lose.\n")
            losses += 1
            print(wins, losses)
        elif total(dealer_hand) > 21:
            print ("Dealer busts. You win!\n")
            wins += 1
            print(wins, losses)
        elif total(player_hand) < total(dealer_hand):
            print ("Sorry. Your score isn't higher than the dealer. You lose.\n")
            losses += 1
            print(wins, losses)
        elif total(player_hand) > total(dealer_hand):
            print ("Congratulations. Your score is higher than the dealer. You win\n")
            wins += 1
            print(wins, losses)
        elif total(player_hand) == total(dealer_hand):
            print("Both you and the dealer tie, which means play is pushed.\n")
            print(wins, losses)
            dealer_hand = []
            player_hand = []
            game()
def game():
    global wins;global losses;global player_hand;global quit;global quit_2;global player_hand_2 #stacked globals
    player_hand_2 = []
    quit=False
    quit_2=0
    choice = 0
    dealer_hand = deal(deck)
    player_hand = deal(deck)
    print ("The dealer is showing a " + str(dealer_hand[0]))
    print ("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))
    blackjack(dealer_hand, player_hand) 
    while not quit:
        decision(player_hand, dealer_hand)
    if quit_2==1:
        global stop
        stop = 0
        decision(player_hand_2, dealer_hand)
        while total(player_hand_2) < 22:
            decision(player_hand_2, dealer_hand)
            if stop == 1:
                break
    play_again()
def decision(playerhand, dealerhand):
        #deck.append(dealerhand[1])         #needs to be integrated later
        #Hit % win chance calculator
        #Stand % win chance calculator (dealer[0], player_hand[0,1] and deck)
            #dealer_bust_chance = (len(calculator_deck[calculator_deck.index(10)::]) / len(calculator_deck)) + 3 IDK what this is
        dealer_starting_hands = []
        choices_2 = [2,3,4,5,6,7,8,9,10,11]
        starting_minus_tens = []
        matching_probability = []
        for choice_2 in choices_2:
            matching_probability.append(deck.count(choice_2)/len(deck))
            if choice_2 == 11 and dealerhand[0] == 11:
                choice_2 = 1
                starting_minus_tens.append(1)
            elif choice_2 == 11 or dealerhand[0] == 11:
                starting_minus_tens.append(1)
            else:
                starting_minus_tens.append(0)
            dealer_starting_hands.append(dealerhand[0]+choice_2)
        dealer_probability_bust = 0;dealer_probability_17 = 0;dealer_probability_18 = 0;dealer_probability_19 = 0;dealer_probability_20 = 0;dealer_probability_21 = 0
        for hand in dealer_starting_hands:
                matching_deck = deck.copy()
                matching_deck.remove(choices_2[dealer_starting_hands.index(hand)])
                dealer_probability_17 += P_dealer(hand,matching_deck,starting_minus_tens[dealer_starting_hands.index(hand)],[1,0,0,0,0,0]) * matching_probability[dealer_starting_hands.index(hand)]
                dealer_probability_18 += P_dealer(hand,matching_deck,starting_minus_tens[dealer_starting_hands.index(hand)],[0,1,0,0,0,0]) * matching_probability[dealer_starting_hands.index(hand)]
                dealer_probability_19 += P_dealer(hand,matching_deck,starting_minus_tens[dealer_starting_hands.index(hand)],[0,0,1,0,0,0]) * matching_probability[dealer_starting_hands.index(hand)]
                dealer_probability_20 += P_dealer(hand,matching_deck,starting_minus_tens[dealer_starting_hands.index(hand)],[0,0,0,1,0,0]) * matching_probability[dealer_starting_hands.index(hand)]
                dealer_probability_21 += P_dealer(hand,matching_deck,starting_minus_tens[dealer_starting_hands.index(hand)],[0,0,0,0,1,0]) * matching_probability[dealer_starting_hands.index(hand)]
                dealer_probability_bust += P_dealer(hand,matching_deck,starting_minus_tens[dealer_starting_hands.index(hand)],[0,0,0,0,0,1]) * matching_probability[dealer_starting_hands.index(hand)]
        if total(playerhand) < 17:
            win_percentage_stand = [dealer_probability_bust,0]
        elif total(player_hand) == 17:
            win_percentage_stand = [dealer_probability_bust, dealer_probability_17]
        elif total(player_hand) == 18:
            win_percentage_stand = [dealer_probability_bust+dealer_probability_17, dealer_probability_18]
        elif total(player_hand) == 19:
            win_percentage_stand = [dealer_probability_bust+dealer_probability_17+dealer_probability_18, dealer_probability_19]
        elif total(player_hand) == 20:
            win_percentage_stand = [dealer_probability_bust+dealer_probability_17+dealer_probability_18+dealer_probability_19, dealer_probability_20]
        elif total(player_hand) == 21:
            win_percentage_stand = [dealer_probability_bust+dealer_probability_17+dealer_probability_18+dealer_probability_19+dealer_probability_20, dealer_probability_21]
        player_minustens = 0
        if playerhand[0] == "A" or playerhand[1] == "A":
            player_minustens = 1
        print(win_percentage_stand)
            #now we must figure out the chance he will beat us (looking at straight up wins plus hit wins, countinuing)
        win_percentage_hit = 0 
        choice = "st"
        if total(playerhand) < 12:
            choice = "h"    #later ofc adding the choice to doubledown
         
        #else:   #here we add the double down and hit calculation, useless if we have below 12 total
            #P_player(playerhand)
        #if dealerhand[0] != "A":
            #difference = total(player_hand) - dealerhand[0]
        #else:
            #difference = total(player_hand) - 11

        global wins;global losses
        if len(playerhand) <= 3:
            global double_choice
            double_choice = ", [D]oubleDown"
        else:
            double_choice = " "
        global split_choice
        split_choice = " "
        if len(playerhand) == 2 and playerhand[0] == playerhand[1]:
            split_choice = ", [Sp]lit "
        #choice = input("Do you want to [H]it, [St]and%s%sor [Q]uit: " % (double_choice, split_choice)).lower() #need to add split, doubling down and buying insurance
        if choice == "h":
            hit(playerhand)
            print(playerhand)
            print("Hand total: " + str(total(playerhand)))
            if total(playerhand)>21:
                print('You busted')
                losses += 1
                global quit;quit=True
        elif choice == "st":
            if len(player_hand_2) > 0:
                global stop
                stop = 1
            while total(dealerhand)<17:
                hit(dealerhand)
                print(dealerhand)
                if total(dealerhand)>21:
                    print('Dealer busts, you win!')
                    wins += 1
                    quit=True
            if total(dealerhand) < 22: 
                score(dealerhand,playerhand)
            quit=True
        elif choice == "sp" and split_choice == ", [Sp]lit ":
            global quit_2
            player_hand_2.append(player_hand.pop())
            quit_2 = 1
        elif choice == "d" and len(playerhand) <= 3:
            hit(playerhand)
            print(playerhand)
            print("Hand total: " + str(total(playerhand)))
            if total(playerhand)>21:
                print('You busted')
                losses += 2
                quit=True
            else:
                while total(dealerhand)<17:
                    hit(dealerhand)
                    print(dealerhand)
                    if total(dealerhand)>21:
                        print('Dealer busts, you win!')
                        wins += 2
                        quit=True
                score(dealerhand,playerhand);score(dealerhand,playerhand) #this takes into account the double risk
                quit=True
        elif choice == "q":
            quit=True;quit_2=0
            exit()


if __name__ == "__main__":
   game()
