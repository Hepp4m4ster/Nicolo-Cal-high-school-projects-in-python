import random
import sys
sys.setrecursionlimit(1000000000)

simulations = int(input("How many simulations shall I run: "))
ceiling = int(input("What is the upper limit of turn simulated: "))

player_start = 0;player_start_round = 0;player_start_cards = []
player_start_paid = [0,0] #[amount of times paid, value of payings]
player_after = 0;player_after_round = 0;player_after_cards = [];player_after_paid = [0,0]
tile1 = [1,-1];back3 = [3,-1];tile11 = [11,1];tile24 = [24,1];tile0 = [0,1];tile39 = [39,1];tile15 = [15,1] #different cards [tile to which moved, direction]
magic_moments = [tile1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
show_time = [back3,tile11,tile24,tile0,tile39,tile15,0,0,0,0,0,0,0,0,0,0] #0 indicates no change in player position on the board
go_to_jail = [10,-1] #same as previous lists
cards = [[1,60,2],[3,60,4],[5,200,25],[6,100,6],[8,100,6],[9,120,8],[11,140,10],[12,150,28],[13,140,10],[14,160,12],[15,200,25],[16,180,14],[18,180,14],[19,200,16],[21,220,18],[23,220,18],[24,240,20],[25,200,25],[26,260,22],[27,260,22],[28,150,28],[29,280,24],[31,300,26],[32,300,26],[34,320,28],[35,200,25],[37,350,35],[39,400,50]]
cards_copy = [[1,60,2],[3,60,4],[5,200,25],[6,100,6],[8,100,6],[9,120,8],[11,140,10],[12,150,28],[13,140,10],[14,160,12],[15,200,25],[16,180,14],[18,180,14],[19,200,16],[21,220,18],[23,220,18],[24,240,20],[25,200,25],[26,260,22],[27,260,22],[28,150,28],[29,280,24],[31,300,26],[32,300,26],[34,320,28],[35,200,25],[37,350,35],[39,400,50]]
sets = [[1,3],[6,8,9],[11,13,14],[16,18,19],[21,23,24],[26,27,29],[31,32,34],[37,39]]
turns_simulated = -0.5
rolls = [2,3,3,4,4,4,5,5,5,5,6,6,6,6,6,7,7,7,7,7,7,8,8,8,8,8,9,9,9,9,10,10,10,11,11,12]

results = []
for turns in range(0,ceiling):
    results.append(0)

def tile_check(player,mamo,shti,round):
    lahto = 0
    if player >= 40*round:
        lahto = 200
    if player%40 == 30:
        while player%40 != go_to_jail[0]:
            player += go_to_jail[1]
    elif player%40 == 2 or player%40 == 17 or player%40 == 33:
        if len(mamo) == 0:
            for item in range(0,len(magic_moments)):
                mamo.append(magic_moments[item])
        random.shuffle(mamo)
        if mamo[0]:
            while player%40 != mamo[0][0]:
                player += mamo[0][1]
        mamo.remove(mamo[0])
    elif player%40 == 7 or player%40 == 22 or player%40 == 36:
        if len(shti) == 0:
            for item in range(0,len(show_time)):
                shti.append(show_time[item])
        random.shuffle(shti)
        if shti[0]:
            while player%40 != shti[0][0]:
                player += shti[0][1]
        shti.remove(shti[0])
    return [player,mamo,shti,lahto]

def roll_dice(p):
    outcomes = rolls.copy()
    random.shuffle(outcomes)
    p += outcomes[0]
    return p

def buy_cards(pelaaja,pelaaja_raha):
    for card in range(0,len(cards_copy)):
        if pelaaja%40 == cards_copy[card][0] and pelaaja_raha>=cards_copy[card][1]:
            return cards_copy[card]
    
def paying(payer,paids_list):
    for owned in range(0,len(paids_list)):
        if payer%40 == paids_list[owned][0]:
            return paids_list[owned][2]

def game_sim(p1,p2,turn,mm,st,limit):
    global player_after_paid;global player_start_paid;global p1_bankroll;global p2_bankroll;global player_after_round;global player_start_round
    while True:
        turn += 0.5
        if turn >= limit: #turn%1 == 0.5 and p2-p1 <= 0 or 
            return turn #+0.5
        if turn%1 == 0.5: #player_after turn
            p1 = roll_dice(p1)
            effects = tile_check(p1,mm,st,player_after_round)
            if effects[3] != 0:
                p1_bankroll += effects[3]
                player_after_round += 1
            tile = buy_cards(p1,p1_bankroll)
            if tile:
                p1_bankroll -= tile[1]
                player_after_cards.append(tile)
                cards_copy.remove(tile)
            cost_p1 = int(paying(p1,player_start_cards) or 0)
            player_after_paid[1] += cost_p1
            p2_bankroll += cost_p1
            p1_bankroll -= cost_p1
            if cost_p1 != 0:
                player_after_paid[0] += 1
            p1=effects[0];mm=effects[1];st=effects[2]
            if p1_bankroll < 0:
                return turn+0.5
        else: #player_before turn
            p2 = roll_dice(p2)
            effects = tile_check(p2,mm,st,player_start_round)
            if effects[3] != 0:
                p2_bankroll += effects[3]
                player_start_round += 1
            tile = buy_cards(p2,p2_bankroll)
            if tile:
                p2_bankroll -= tile[1]
                player_start_cards.append(tile)
                cards_copy.remove(tile)
            cost_p2 = int(paying(p2,player_after_cards) or 0)
            player_start_paid[1] += cost_p2
            p1_bankroll += cost_p2
            p2_bankroll -= cost_p2
            if cost_p2 != 0:
                player_start_paid[0] += 1
            p2=effects[0];mm=effects[1];st=effects[2]
            if p2_bankroll < 0:
                return turn

total_cards_bought_s = 0;total_cards_bought_a = 0;total_money_s = 0;total_money_a = 0;sets_s = 0;sets_a = 0;start_have_no_after = 0;after_have_no_start=0

def set_check(persons_cards):
    tiles_owned = []
    total_sets = 0
    for cards in range(0,len(persons_cards)):
        tiles_owned.append(persons_cards[cards][0])
    for combo in sets:
        if set(combo) == set(combo).intersection(set(tiles_owned)):
            total_sets += 1
    return total_sets

for sim in range(0,simulations):
    p1_bankroll = 1500
    p2_bankroll = 1500
    results[int(game_sim(player_after,player_start,turns_simulated,magic_moments.copy(),show_time.copy(),ceiling))-1] += 1
    cards_copy = cards.copy()
    total_cards_bought_a += len(player_after_cards)
    total_cards_bought_s += len(player_start_cards)
    for card_bought_a in player_after_cards:
        total_money_a += card_bought_a[1]
    total_money_a += p1_bankroll
    for card_bought_s in player_start_cards:
        total_money_s += card_bought_s[1]
    total_money_s += p2_bankroll
    sets_s += set_check(player_start_cards)
    sets_a += set_check(player_after_cards)
    if set_check(player_start_cards)>=1 and set_check(player_after_cards) == 0:
        start_have_no_after += 1
    if set_check(player_start_cards)==0 and set_check(player_after_cards) >= 1:
        after_have_no_start += 1
    player_after_cards = [];player_start_cards = [];player_after_round = 0;player_start_round = 0
#print(results)

probabilities = []
for x in range(0,len(results)):
    probabilities.append(results[x]/sum(results))

#print(probabilities)
print("Total cards bought per sim: (start,after)",total_cards_bought_s/simulations,total_cards_bought_a/simulations)
print("Percentage of cards bought by starting player: ",total_cards_bought_s/(total_cards_bought_s+total_cards_bought_a))
print("Total money earned/gained per sim: (start,after)",total_money_s/simulations-1500,total_money_a/simulations-1500)
print("Total money paid to other player per sim: (start,after)",player_start_paid[1]/simulations,player_after_paid[1]/simulations)
print("Number of times paid to other player per sim: (start,after)",player_start_paid[0]/simulations,player_after_paid[0]/simulations)
print("Number of sets per sim: (start,after)",sets_s/simulations,sets_a/simulations)
print("Percentage of games where player had set but other no: (start,after)",start_have_no_after,after_have_no_start)