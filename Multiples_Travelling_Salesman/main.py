import random
import math
import sys 
import matplotlib.collections as mc #biblioteca para gráficos
import matplotlib.pylab as pl

n_cities = 5 #número de cidades
n_salesman = 6

def generate_coordinates(n_cities):
    coordinates = []
    for i in range(n_cities):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        coordinates.append((x,y))

    return coordinates


def create_random_problem(coordinates):
    n_cities = len(coordinates)

    distances = [[0 for _ in range(n_cities)] for _ in range(n_cities)]

    for i in range(n_cities):
        for j in range(i + 1, n_cities):
            x = coordinates[i][0] - coordinates[j][0]
            y = coordinates[i][1] - coordinates[j][1]
            distance = math.sqrt(x**2 + y**2) 
            distances[i][j] = distances[j][i] = distance
        
    return distances

def get_biggest_distance(distances, city, unvisited_cities):
    distance = 0
    ret = 0
    for i in unvisited_cities:                      
        dist = distances[city][i]
        if dist > distance:
            distance = dist
            ret = i
    return ret, distance

def get_cordinates_average(city, coordinates): #vetor de cidades
    cordinates = [[0 for _ in range(len(city))] for _ in range(len(city))]
    x = []
    y = []
    for i in city:
        x.append(coordinates[i][0])
        y.append(coordinates[i][1])
    average_x = int(sum(x) / len(city))
    average_y = int(sum(y)/ len(city)) 

    return average_x, average_y

def salesman_per_city():
    salesman_array = [0] * n_salesman
    n_salesman_copy = 0 
    for i in range(n_cities - 1): #5
        if n_salesman_copy < n_salesman: #2
            salesman_array[n_salesman_copy - 1] += 1 # [1][2][2]
            n_salesman_copy = n_salesman_copy + 1 # 1
            if n_salesman_copy == n_salesman:
                n_salesman_copy = 0             
    return salesman_array

def nearest_city(coordinates, x, y, unvisited):
    distances = 0
    dist = sys.maxsize
    city = 0
    for i in unvisited:
        distances = int(
                        math.sqrt(
                            (x - coordinates[i][0])**2 
                            + (y - coordinates[i][1])**2
                        )
                    )
        if distances < dist:
            dist = distances
            city = i
    return city, dist
    
def heuristic_centroide():
    unvisited = list(range(n_cities)) 
    tour = [random.choice(unvisited)] 
    unvisited.remove(tour[-1]) 
    coordinates = generate_coordinates(n_cities)
    distances = create_random_problem(coordinates)  
    city = 0
    distances_value = 0
    distances_array = []
    for i in salesman_per_city(): 
        tour_salesman = []
        tour_salesman.append(tour[0])
        cont = 0
        while cont < i: 
            x_av, y_av = get_cordinates_average(tour_salesman, coordinates)
            if cont == 0:
                city, distances_value = get_biggest_distance(distances, tour_salesman[-1], unvisited) 
                tour.append(city) 
                
            if cont >= 1: 
                city, distances_value = nearest_city(coordinates, x_av, y_av, unvisited)
                tour.append(city)
    
            tour_salesman.append(city)
            distances_array.append(distances_value)
            unvisited.remove(city)  
            
            cont = cont + 1 
        dist_zero = distances[tour[0]][tour[-1]]
        tour.append(tour[0])
        distances_array.append(dist_zero)
    return tour, unvisited, distances_array

def generate_lines(coordinates, tour):
    lines = []
    colors = []

    # Gerar uma cor aleatória para cada linha
    for _ in range(len(tour) - 1):
        colors.append((random.random(), random.random(), random.random()))

    for j in range(len(tour) - 1):
        lines.append([
            coordinates[tour[j]],
            coordinates[tour[j+1]]
        ])

    lines.append([
        coordinates[tour[-1]],
        coordinates[tour[0]] # vai do ultimo ao primeiro
    ])

    return lines, colors

def plot_tour(coordinates, tour):
    lines, colors = generate_lines(coordinates, tour)
    lc = mc.LineCollection(lines, colors=colors, linewidths=2)  # Adicionando as cores
    # subplot == uma folha em branco para desenharmos 
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale() # ajusta a figura para fazer caber o desenho
    ax.margins(0.1)
    # scatter == grafo
    pl.scatter([i[0] for i in coordinates], [i[1] for i in coordinates])
    pl.title("Tour")
    pl.xlabel("X")
    pl.ylabel("Y")
    pl.show()



coordinates = generate_coordinates(n_cities)
distances = create_random_problem(coordinates)
tour, unvisited, d = heuristic_centroide()
print(sum(d))
plot_tour(coordinates, tour)