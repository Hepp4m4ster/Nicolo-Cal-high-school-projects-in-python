import random
import sys
sys.setrecursionlimit(1000000000)
turns_calculated = 2 #int(input("How many turns (between 2-10) shall I calculate for you: "))
player_start = 0
player_after = 0
tile1 = [1,-1];back3 = [3,-1];tile11 = [11,1];tile24 = [24,1];tile0 = [0,1];tile39 = [39,1];tile15 = [15,1] #different cards [tile to which moved, direction]
magic_moments = [tile1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
show_time = [back3,tile11,tile24,tile0,tile39,tile15,0,0,0,0,0,0,0,0,0,0] #0 indicates no change in player position on the board
go_to_jail = [10,-1] #same as previous lists
turns_simulated = -0.5
differences = [[0,146],[1,140],[2,125],[3,104],[4,80],[5,56],[6,35],[7,20],[8,10],[9,4],[10,1],[-1,140],[-2,125],[-3,104],[-4,80],[-5,56],[-6,35],[-7,20],[-8,10],[-9,4],[-10,1]]
rolls = [[2,1/36],[3,1/18],[4,1/12],[5,1/9],[6,5/36],[7,1/6],[12,1/36],[11,1/18],[10,1/12],[9,1/9],[8,5/36]]

probabilities = []
for turns in range(0,turns_calculated):
    probabilities.append(0)
probabilities[len(probabilities)-1] += 1

def hit_something(p,mm,st):
    outcome = [[p,mm,st,1]]
    if p%40 == 30:
        while p%40 != go_to_jail[0]:
            p += go_to_jail[1]
        outcome = [[p,mm,st,1]]
    elif p%40 == 2 or p%40 == 17 or p%40 == 33:
        outcome = []
        if len(mm) != 0:
            run = 0 
            for card in range(0,len(mm)):
                mm_copy = mm.copy()
                if mm[card] != 0:
                    while p%40 != mm[card][0]:
                        p += mm[card][1]
                    mm_copy.remove(mm[card])
                    outcome.append([p,mm_copy,st,1/len(mm)])
                elif run == 0:
                    run += 1
                    mm_copy.remove(mm[card])
                    outcome.append([p,mm_copy,st,mm.count(0)/len(mm)])
    elif p%40 == 7 or p%40 == 22 or p%40 == 36:
        outcome = []
        if len(st) != 0:
            run = 0 
            for card in range(0,len(st)):
                st_copy = st.copy()
                if st[card] != 0:
                    while p%40 != st[card][0]:
                        p += st[card][1]
                    st_copy.remove(st[card])
                    outcome.append([p,mm,st_copy,1/len(st)])
                elif run == 0:
                    run += 1
                    st_copy.remove(st[card])
                    probs = st.count(0)/len(st)
                    outcome.append([p,mm,st_copy,probs])
    return outcome

branches = 0

def tree_diagram(p1,p2,turn,mm,st):
    global branches
    turn += 0.5
    prob = 0
    if turn%1 == 0.5:
        outcomes = hit_something(p2,mm,st)
    elif turn%1 == 0:
        outcomes = hit_something(p1,mm,st)
    if turn < target-0.5 and turn%1 == 0.5 and p2-p1 <= 0:
        branches += 1
        return 0
    elif turn == target-0.5 and p2-p1 <= 0:
        branches += 1
        return 1
    elif turn == target-0.5:
        branches += 1
        return 0
    if turn%1 == 0.5: #player_after turn
        for path in outcomes:
            if len(outcomes)==1 and path[0]-p1 <= 0:
                if turn == target-0.5:
                    return 1
                else: 
                    return 0
            elif len(outcomes)>1 and path[0]-p1 <= 0:
                if turn == target-0.5:
                    prob += path[3]
                    outcomes.remove(path)
                else:
                    outcomes.remove(path)
        for effect in outcomes:
            for roll in range(0,len(rolls)):
                prob += tree_diagram(p1+rolls[roll][0],effect[0],turn,effect[1],effect[2])*rolls[roll][1]*effect[3]
        return prob
    else: #player_before turn
        for effect in outcomes:
            for roll in range(0,len(rolls)):
                prob += tree_diagram(effect[0],p2+rolls[roll][0],turn,effect[1],effect[2])*rolls[roll][1]*effect[3]
        return prob

for prob in range(0,len(probabilities)-1):
    global target
    target = prob+1
    probabilities[prob] += tree_diagram(player_start,player_after,turns_simulated,magic_moments.copy(),show_time.copy())
    probabilities[len(probabilities)-1] -= probabilities[prob]

print(probabilities)
print(branches)

#11 branches for turn 1