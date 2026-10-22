import random
import sys
sys.setrecursionlimit(10000)

decks_number = input("Enter number of decks to use: ")
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]*(int(decks_number)*4)
card_reset_amount = int(input("When is the deck reshuffled, in terms of remaining cards. Minimum 52(75): "))
hands_to_play = int(input("How many hands should the AI play: "))
random.shuffle(deck)
wins = 0
losses = 0
hands_played = 0

def reset():
    global deck
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]*(int(decks_number)*4)
    random.shuffle(deck)

def deal(deck):
    hand = []
    for i in range(2):
        card = deck.pop()
        hand.append(card)
    return hand

def play_again():
    global hands_to_play;global hands_played
    hands_played += 1
    hands_to_play -= 1
    if len(deck) > card_reset_amount:
        again = "y"
    else:
        reset()
        again = "y"
    if again == "y" and hands_to_play != 0:
        global dealer_hand;global player_hand;global player_hand_2
        dealer_hand = []
        player_hand = []
        player_hand_2 = []
        game()
    else:
        print(wins,losses,wins/(losses+wins),hands_played)
        exit()


def total(hand):
    total = 0
    ace_minus_count = hand.count(11)
    for card in hand:
        total += card
    while total > 21 and ace_minus_count > 0:
        total -= 10
        ace_minus_count -= 1
    return total

def hit(hand):
    card = deck.pop()
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
    

def P_player_double(hand_of_player,placement_deck):
    p_of_player = [0,0,0,0,0,0,0]
    choices_3 = list(set(placement_deck))
    player_minustens = hand_of_player.count(11)
    for choice in choices_3:
        newer_minustens = int(str(player_minustens))
        total_2 = sum(hand_of_player) + choice
        if choice == 11:
                newer_minustens += 1
        while total_2 > 21 and newer_minustens > 0:
            total_2 -= 10
            newer_minustens -= 1
        if total_2 <= 16:
            p_of_player[0] += placement_deck.count(choice)/len(placement_deck)
        elif total_2 == 17:
            p_of_player[1] += placement_deck.count(choice)/len(placement_deck)
        elif total_2 == 18:
            p_of_player[2] += placement_deck.count(choice)/len(placement_deck)
        elif total_2 == 19:
            p_of_player[3] += placement_deck.count(choice)/len(placement_deck)
        elif total_2 == 20:
            p_of_player[4] += placement_deck.count(choice)/len(placement_deck)
        elif total_2 == 21:
            p_of_player[5] += placement_deck.count(choice)/len(placement_deck)
        elif total_2 > 21:
            p_of_player[6] += placement_deck.count(choice)/len(placement_deck)
    return p_of_player


def blackjack(dealer_hand, player_hand):
    global wins
    global losses
    if total(player_hand) == 21 == total(dealer_hand):
        print(wins, losses)
        dealer_hand = []
        player_hand = []
        game()
    elif total(player_hand) == 21:
        wins += 1.5
        print(wins, losses)
        global quit;quit=True
    elif total(dealer_hand) == 21:
        losses += 1
        print(wins, losses)
        quit=True
    

def score(dealer_hand, player_hand):
        # score function now updates to global win/loss variables
        global wins
        global losses
        if total(player_hand) == 21 == total(dealer_hand):
            print(wins, losses)
        elif total(player_hand) == 21:
            wins += 1
            print(wins, losses)
        elif total(dealer_hand) == 21:
            losses += 1
            print(wins, losses)
        elif total(player_hand) > 21:
            losses += 1
            print(wins, losses)
        elif total(dealer_hand) > 21:
            wins += 1
            print(wins, losses)
        elif total(player_hand) < total(dealer_hand):
            losses += 1
            print(wins, losses)
        elif total(player_hand) > total(dealer_hand):
            wins += 1
            print(wins, losses)
        elif total(player_hand) == total(dealer_hand):
            print(wins, losses)
def game():
    global wins;global losses;global player_hand;global quit;global quit_2;global player_hand_2 #stacked globals
    player_hand_2 = []
    quit=False
    quit_2=0
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
        hit(player_hand_2)
        while stop == 0:
            decision(player_hand_2, dealer_hand)
    play_again()

def stand_and_double(player_hand,dealerhand):
        starting_hands = []
        choices_2 = list(set(deck))
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
            starting_hands.append(dealerhand[0]+choice_2)
        dealer_p_bust = 0;dealer_p_17 = 0;dealer_p_18 = 0;dealer_p_19 = 0;dealer_p_20 = 0;dealer_p_21 = 0
        for hand in starting_hands:
                matching_deck = deck.copy()
                matching_deck.remove(choices_2[starting_hands.index(hand)])
                dealer_p_17 += P_dealer(hand,matching_deck,starting_minus_tens[starting_hands.index(hand)],[1,0,0,0,0,0]) * matching_probability[starting_hands.index(hand)]
                dealer_p_18 += P_dealer(hand,matching_deck,starting_minus_tens[starting_hands.index(hand)],[0,1,0,0,0,0]) * matching_probability[starting_hands.index(hand)]
                dealer_p_19 += P_dealer(hand,matching_deck,starting_minus_tens[starting_hands.index(hand)],[0,0,1,0,0,0]) * matching_probability[starting_hands.index(hand)]
                dealer_p_20 += P_dealer(hand,matching_deck,starting_minus_tens[starting_hands.index(hand)],[0,0,0,1,0,0]) * matching_probability[starting_hands.index(hand)]
                dealer_p_21 += P_dealer(hand,matching_deck,starting_minus_tens[starting_hands.index(hand)],[0,0,0,0,1,0]) * matching_probability[starting_hands.index(hand)]
                dealer_p_bust += P_dealer(hand,matching_deck,starting_minus_tens[starting_hands.index(hand)],[0,0,0,0,0,1]) * matching_probability[starting_hands.index(hand)]
        if total(player_hand) < 17 or total(player_hand) > 21:
            win_percentage_stand = [dealer_p_bust,0]
        elif total(player_hand) == 17:
            win_percentage_stand = [dealer_p_bust, dealer_p_17]
        elif total(player_hand) == 18:
            win_percentage_stand = [dealer_p_bust+dealer_p_17, dealer_p_18]
        elif total(player_hand) == 19:
            win_percentage_stand = [dealer_p_bust+dealer_p_17+dealer_p_18, dealer_p_19]
        elif total(player_hand) == 20:
            win_percentage_stand = [dealer_p_bust+dealer_p_17+dealer_p_18+dealer_p_19, dealer_p_20]
        elif total(player_hand) == 21:
            win_percentage_stand = [dealer_p_bust+dealer_p_17+dealer_p_18+dealer_p_19+dealer_p_20, dealer_p_21]
        hit_p = P_player_double(player_hand,deck)
        win_percentage_hit = hit_p[0]*dealer_p_bust+hit_p[1]*(dealer_p_bust)+hit_p[2]*(dealer_p_bust+dealer_p_17)+hit_p[3]*(dealer_p_bust+dealer_p_18+dealer_p_17)+hit_p[4]*(dealer_p_bust+dealer_p_17+dealer_p_18+dealer_p_19)+hit_p[5]*(dealer_p_bust+dealer_p_17+dealer_p_18+dealer_p_19+dealer_p_20)
        draw_percentage_hit = hit_p[1]*(dealer_p_17)+hit_p[2]*(dealer_p_18)+hit_p[3]*(dealer_p_19)+hit_p[4]*(dealer_p_20)+hit_p[5]*(dealer_p_21)
        return [win_percentage_stand[0],win_percentage_stand[1],win_percentage_hit,draw_percentage_hit,hit_p[6]]

def P_hitting(ph,dh,placementdeck):
    if total(ph) > 21:
        return 0
    starting_list = stand_and_double(ph,dh)
    if starting_list[4] == 0  and total(ph) <17 or starting_list[2] + starting_list[3] > starting_list[0] + starting_list[1]: #1 - obc to see the chance we dont go bust, so ofc we hi
        p_sum = 0
        choices = list(set(placementdeck))
        for choice in choices:
            new_deck = placementdeck.copy()
            new_deck.remove(choice)
            total_1 = []
            for i in range(len(ph)):
                total_1.append(ph[i])
            total_1.append(choice)
            p_sum += P_hitting(total_1,dh,new_deck)*(new_deck.count(choice)+1)/(len(new_deck)+1)
        return p_sum
    else:
        return starting_list[0]+starting_list[1]


def decision(playerhand, dealerhand):
        print(playerhand)
        deck.append(dealerhand[1]) 
        last_resort = 0
        stand_vs_double = stand_and_double(playerhand,dealerhand)
        if playerhand[0] == playerhand [1] and len(playerhand) == 2 and len(player_hand_2) == 0: #indicates a chance to split (options: D,h,st,sp)
            if playerhand[0] == 11 or playerhand[0] == 8:
                choice = "sp"
                #print("choice is split")
            elif playerhand[0] == 5 or playerhand[0] == 4:
                last_resort = 1 
            elif playerhand[0] == 10:
                choice = "st"
            elif dealerhand[0]<7:
                choice = "sp"
            elif dealerhand[0]>7 and playerhand[0]<8:
                last_resort = 1
            elif dealerhand[0]==7:
                if playerhand[0]<4 or playerhand[0]==7:
                    choice = "sp"
                else:
                    last_resort = 1
            else:
                w_p_h = 0;w_p_h_2 = 0 #split hand
                s_h = [];m_p = []
                s_h_2 = []
                c_2s = list(set(deck))
                for c_2 in c_2s:
                    n_h = []
                    n_h_2 = []
                    m_p.append(deck.count(c_2)/len(deck))
                    n_h.append(playerhand[0]);n_h.append(playerhand[1]);n_h.append(c_2)
                    n_h_2.append(playerhand[0]);n_h_2.append(c_2)
                    s_h.append(n_h)
                    s_h_2.append(n_h_2)
                for h in s_h:
                    m_d = deck.copy()
                    m_d.remove(c_2s[s_h.index(h)])
                    w_p_h += P_hitting(h,dealerhand,m_d) * m_p[s_h.index(h)]
                for h_2 in s_h_2:
                    m_d = deck.copy()
                    m_d.remove(c_2s[s_h_2.index(h_2)])
                    w_p_h_2 += P_hitting(h_2,dealerhand,m_d) * m_p[s_h.index(h)]
                if w_p_h_2 >= 0.5 and w_p_h_2 >= stand_vs_double[0]+stand_vs_double[1] - 0.1 or w_p_h_2 > w_p_h and w_p_h_2 > stand_vs_double[0]+stand_vs_double[1]:
                    choice = "sp"
                    #print("Choice sp")
                elif stand_vs_double[2] >= 0.5 and stand_vs_double[2] >= stand_vs_double[0] - 0.1 and len(player_hand_2)<1 and len(playerhand)<=3:
                    choice = "d"
                    #print("Choice d")
                elif w_p_h >= stand_vs_double[0]+stand_vs_double[1] or stand_vs_double[4] == 0:
                    choice = "h"
                    #print("Choice h")
                else:
                    choice = "st"
                    #print("Choice st")
                print(w_p_h,w_p_h_2)
        elif playerhand.count(11) > 0 and sum(playerhand) - (10*(playerhand.count(11)-1)) < 22: #indicates a soft hand
            if stand_vs_double[2] > 0.5 and stand_vs_double[2] >= stand_vs_double[0] - 0.1 and len(playerhand) <= 3 and len(player_hand_2)<1:
                choice = "d"
                #print("You should DoubleDown")
            elif stand_vs_double[2] + stand_vs_double[3] > stand_vs_double[0]+stand_vs_double[1] or stand_vs_double[0]+stand_vs_double[1] < 0.5:
                choice = "h"
                #print("You should hit")
            elif total(playerhand) < 17:
                choice = "h"
            elif stand_vs_double[0]+stand_vs_double[1] > 0.5:
                choice = "st"
            else:
                last_resort = 1
                #print("You should stand")
        else:
            last_resort = 1
        if last_resort==1:
            if playerhand[0] == 11 and playerhand[1] == 11 and len(playerhand)==2: #with a split hand and two aces, hitting is the best option, since 0% bust chance
                choice = "h"
            elif stand_vs_double[2] >= 0.5 and stand_vs_double[2] >= stand_vs_double[0] - 0.1 and len(player_hand_2)<1 and len(playerhand)<=3:
                choice = "d"
                    #print("Choice d")
            elif stand_vs_double[0]+stand_vs_double[1] >= 0.5:
                choice = "st"
                    #print("Choice st")
            elif total(playerhand) < 12:
                choice = "h"
                    #print("Choice h")
            elif total(playerhand) > 15:
                if stand_vs_double[0]+stand_vs_double[1] > stand_vs_double[2]+stand_vs_double[3]:
                    choice = "st"
                    #print("Choice st")
                else:
                    choice = "h"
            else:
                win_percentage_hit = 0
                starting_hands = [];matching_probability = []
                choices_2 = list(set(deck))
                for choice_2 in choices_2:
                    new_hand = []
                    matching_probability.append(deck.count(choice_2)/len(deck))
                    for i in range (len(playerhand)):
                        new_hand.append(playerhand[i])
                    new_hand.append(choice_2)
                    starting_hands.append(new_hand)
                for hand in starting_hands:
                    matching_deck = deck.copy()
                    matching_deck.remove(choices_2[starting_hands.index(hand)])
                    win_percentage_hit += P_hitting(hand,dealerhand,matching_deck) * matching_probability[starting_hands.index(hand)]
                if win_percentage_hit > stand_vs_double[0]+stand_vs_double[1]:
                    choice = "h"
                    #print("Choice h")
                else:
                    choice = "st"
                    #print("Choice st")
                print(win_percentage_hit)

        #print(choice)

        deck.pop()
        if choice == "h":
            global quit;global wins;global losses
            if len(player_hand_2) > 1:
                hit(player_hand_2)
                if total(player_hand_2) < 22:
                    print(player_hand_2)
                else:
                    #money -= bet
                    losses += 1
                    if total(player_hand) > 21:
                        #money -= bet
                        losses += 1
                    else:
                        while total(dealerhand)<17:
                            hit(dealerhand)
                            print(dealerhand)
                            if total(dealerhand)>21:
                                #money += bet
                                wins += 1
                        if total(dealerhand) < 22:
                            score(dealerhand,player_hand)
                    global stop
                    stop = 1
            elif len(player_hand_2)==1:
                hit(player_hand)
                print("First hand: "+str(total(player_hand)))
                if total(player_hand) > 21:
                    quit = True
            else:
                hit(player_hand)
                print(player_hand)
                print("Hand total: " + str(total(player_hand)))
                if total(player_hand)>21:
                    print('You busted')
                    #money -= bet
                    losses += 1
                    quit=True
        elif choice == "st":
            if len(player_hand_2)==1:
                print("next hand")
            elif len(player_hand_2) >= 2:
                stop = 1
                while total(dealerhand)<17:
                    hit(dealerhand)
                    print(dealerhand)
                    if total(dealerhand)>21:
                        #money += bet
                        wins += 1
                        if total(player_hand) < 21:
                            #money += bet
                            wins += 1
                        else:
                            #money -= bet
                            losses += 1
                if total(dealerhand) < 22: 
                    score(dealerhand,player_hand_2)
                    score(dealerhand,player_hand)
            else:
                while total(dealerhand)<17:
                    hit(dealerhand)
                    print(dealerhand)
                    if total(dealerhand)>21:
                        #money += bet
                        wins += 1
                if total(dealerhand) < 22: 
                    score(dealerhand,playerhand)
            quit=True
        elif choice == "sp" and len(playerhand)==2 and playerhand[0]==playerhand[1]:
            global quit_2
            player_hand_2.append(player_hand.pop())
            hit(player_hand)
            quit_2 = 1
        elif choice == "d" and len(playerhand) <= 3 and len(player_hand_2)<1:
                hit(playerhand)
                print(playerhand)
                print("Hand total: " + str(total(playerhand)))
                if total(player_hand)>21:
                    #money -= bet*2
                    losses += 2
                else:
                    while total(dealerhand)<17:
                        hit(dealerhand)
                        print(dealerhand)
                        if total(dealerhand)>21:
                            #money += bet*2
                            wins += 2
                    if total(dealerhand)<22:
                        score(dealerhand,playerhand);score(dealerhand,playerhand) #this takes into account the double risk
                quit=True
        elif choice == "q":
            print(wins,losses)
            quit=True;quit_2=0
            exit()


if __name__ == "__main__":
   game()
