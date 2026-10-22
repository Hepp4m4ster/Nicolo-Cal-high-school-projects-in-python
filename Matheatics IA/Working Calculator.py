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
random.shuffle(rolls)

probabilities = []
for turns in range(0,turns_calculated):
    probabilities.append(0)
probabilities[len(probabilities)-1] += 1

branches = 0

def tree_diagram(p1,p2,turn,mm,st):
    global branches
    turn += 0.5
    prob = 0
    if turn != target-0.5 and turn%1 == 0.5 and p2-p1 <= 0:
        branches += 1
        return 0
    elif turn == target-0.5 and p2-p1 <= 0:
        branches += 1
        return 1
    elif turn == target-0.5:
        branches += 1
        return 0
    if turn%1 == 0.5: #player_after turn
        for roll in range(0,len(rolls)):
                p_new = p1+rolls[roll][0]
                roll_prob = rolls[roll][1]
                run = 0
                if p_new%40 == 30:
                    while p_new%40 != go_to_jail[0]:
                        p_new += go_to_jail[1]
                    prob += tree_diagram(p_new,p2,turn,mm.copy(),st.copy())*roll_prob
                elif p_new%40 == 2 or p_new%40 == 17 or p_new%40 == 33:
                    for card in range(0,len(mm)):
                        p_new = p1+rolls[roll][0]
                        chance_1 = mm.count(mm[card])/len(mm)
                        mm_copy = mm.copy()
                        if mm[card]:
                            while p_new%40 != mm[card][0]:
                                p_new += mm[card][1]
                            mm_copy.remove(mm[card])
                            prob += tree_diagram(p_new,p2,turn,mm_copy.copy(),st.copy())*(chance_1)*roll_prob
                        elif run == 0 and mm[card]==0:
                            run = 1
                            mm_copy.remove(mm[card])
                            prob += tree_diagram(p_new,p2,turn,mm_copy.copy(),st.copy())*(chance_1)*roll_prob
                elif p_new%40 == 7 or p_new%40 == 22 or p_new%40 == 36:
                    for card in range(0,len(st)):
                        p_new = p1+rolls[roll][0]
                        chance_2 = st.count(st[card])/len(st)
                        st_copy = st.copy()
                        if st[card]:
                            while p_new%40 != st[card][0]:
                                p_new += st[card][1]
                            st_copy.remove(st[card])
                            prob += tree_diagram(p_new,p2,turn,mm.copy(),st_copy.copy())*(chance_2)*roll_prob
                        elif run == 0 and mm[card]==0:
                            run = 1
                            st_copy.remove(st[card])
                            prob += tree_diagram(p_new,p2,turn,mm.copy(),st_copy.copy())*(chance_2)*roll_prob
                else:
                    prob += tree_diagram(p_new,p2,turn,mm.copy(),st.copy())*roll_prob
        return prob
    else: #player_before turn
        for roll in range(0,len(rolls)):
                p_new = p2+rolls[roll][0]
                roll_prob = rolls[roll][1]
                run = 0
                if p_new%40 == 30:
                    while p_new%40 != go_to_jail[0]:
                        p_new += go_to_jail[1]
                    prob += tree_diagram(p1,p_new,turn,mm.copy(),st.copy())*roll_prob
                elif p_new%40 == 2 or p_new%40 == 17 or p_new%40 == 33:
                    for card in range(0,len(mm)):
                        p_new = p2+rolls[roll][0]
                        chance_3 = mm.count(mm[card])/len(mm)
                        mm_copy = mm.copy()
                        if mm[card]:
                            while p_new%40 != mm[card][0]:
                                p_new += mm[card][1]
                            mm_copy.remove(mm[card])
                            prob += tree_diagram(p1,p_new,turn,mm_copy.copy(),st.copy())*roll_prob*(chance_3)
                        elif run == 0:
                            mm_copy.remove(mm[card])
                            prob += tree_diagram(p1,p_new,turn,mm_copy.copy(),st.copy())*roll_prob*(chance_3)
                            run = 1
                elif p_new%40 == 7 or p_new%40 == 22 or p_new%40 == 36:
                    for card in range(0,len(st)):
                        p_new = p2+rolls[roll][0]
                        chance_4 = st.count(st[card])/len(st)
                        st_copy = st.copy()
                        if st[card]:
                            while p_new%40 != st[card][0]:
                                p_new += st[card][1]
                            st_copy.remove(st[card])     
                            prob += tree_diagram(p1,p_new,turn,mm.copy(),st_copy.copy())*roll_prob*(chance_4)
                        elif run == 0:
                            run = 1
                            st_copy.remove(st[card])
                            prob += tree_diagram(p1,p_new,turn,mm.copy(),st_copy.copy())*roll_prob*(chance_4)
                else:
                    prob += tree_diagram(p1,p_new,turn,mm.copy(),st.copy())*roll_prob
        return prob

for prob in range(0,len(probabilities)-1):
    global target
    target = prob+1
    probabilities[prob] += tree_diagram(player_after,player_start,turns_simulated,magic_moments.copy(),show_time.copy())
    probabilities[len(probabilities)-1] -= probabilities[prob]

print(probabilities)
print(branches)
