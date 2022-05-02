import random
from math import dist
import csv

def hit(p):
    if random.random() < p:
        return True
    else:
        return False

def random_location():
    # Should not be same location
    p1_loc = (random.random(), random.random())
    p2_loc = (random.random(), random.random())
    p3_loc = (random.random(), random.random())
    return p1_loc, p2_loc, p3_loc

def run_sim():
    fields = ["p1_p2_dist", "p1_p3_dist", "p2_p3_dist", "p1_acc", "p2_acc", "p3_acc", "p1_target", "p2_target",
              "p3_target", "p1_survive", "p2_survive", "p3_survive"]
    rows = []

    iterations = 500
    for i in range(iterations):
        p1_loc, p2_loc, p3_loc = random_location()
        p1_p2_dist = dist(p1_loc, p2_loc)
        p1_p3_dist = dist(p1_loc, p3_loc)
        p2_p3_dist = dist(p2_loc, p3_loc)

        while p1_p2_dist == p1_p3_dist == p2_p3_dist:
            print("Rerunning due to equal distances")
            p1_loc, p2_loc, p3_loc = random_location()
            p1_p2_dist = dist(p1_loc, p2_loc)
            p1_p3_dist = dist(p1_loc, p3_loc)
            p2_p3_dist = dist(p2_loc, p3_loc)
    
        # Should not be same accuracy
        acccuracies = [random.random(), random.random(), random.random()]
        acccuracies.sort(reverse=True)
        p1_acc = acccuracies[0]
        p2_acc = acccuracies[1]
        p3_acc = acccuracies[2]

        hit_rates = [[0, p1_acc * p1_p2_dist, p1_acc * p1_p3_dist],
                     [p2_acc * p1_p2_dist, 0, p2_acc * p2_p3_dist],
                     [p3_acc * p1_p3_dist, p3_acc * p2_p3_dist, 0]]

        # i = player 1 shoots player i
        for i in range(3):
            if i != 0:
                # j = player 2 shoots player j
                for j in range(3):
                    if j != 1:
                        # k = player 3 shoots player k
                        for k in range(3):
                            if k != 2:
                                num_runs = 1000
                                player_survives = [0, 0, 0]
                                for _ in range(num_runs):
                                    players_alive = [0, 1, 2]
                                    while len(players_alive) == 3:
                                        if hit(hit_rates[0][i]) and i in players_alive:
                                            players_alive.remove(i)
                                        if hit(hit_rates[1][j]) and j in players_alive:
                                            players_alive.remove(j)
                                        if hit(hit_rates[2][k]) and k in players_alive:
                                            players_alive.remove(k)

                                    if len(players_alive) == 2:
                                        a = players_alive[0]
                                        b = players_alive[1]
                                        if hit(hit_rates[a][b]):
                                            players_alive.remove(b)
                                        if hit(hit_rates[b][a]):
                                            players_alive.remove(a)
                                    for player in players_alive:
                                        player_survives[player] += 1
                                    
                                rows.append([p1_p2_dist, p1_p3_dist, p2_p3_dist, p1_acc, p2_acc, p3_acc, i+1, j+1, k+1,
                                            player_survives[0]/num_runs,
                                            player_survives[1]/num_runs,
                                            player_survives[2]/num_runs])

    filename = "truel.csv"
    with open(filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields) 
            
        # writing the data rows 
        csvwriter.writerows(rows)



                                



def main():
    run_sim()

if __name__ == "__main__":
    main()
