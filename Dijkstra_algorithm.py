import pygame
import heapq

N = 20
CELL_SIZE = 29
WIDTH = HEIGHT = N*CELL_SIZE
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (200,200,200)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

#Vamos a inicializar pygame

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  #Crea una ventana
pygame.display.set_caption("Dijkstra Pathfinding")      #Crea un título

#Ahora creamos la malla
grid = [[0 for _ in range(N)] for _ in range(N)]        #Interacción de creación de listas, es decir, crea N listas
start = None
end = None      #Aún no se establecieron unos puntos iniciales y finales (se establecerán luego)

##Quizá esto se pueda hacer mejor con arrays de numpy


#Función para dibujar
def draw_grid():
    for y in range(N):
        for x in range(N):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)      #Por qué x*CELL_SIZE??--> Indica la posición probablemente
            if grid[y][x] == 1:     #Si grid[y][x]==1 significa que es un MURO!!
                pygame.draw.rect(screen, BLACK, rect)   #Pinta de negro la esquina superior izquierda
            else:
                pygame.draw.rect(screen, WHITE, rect)   #Pinta de blanco el resto
            pygame.draw.rect(screen, GRAY, rect, 1)     #Ni idea
        if start:
            pygame.draw.rect(screen, GREEN, (start[0]*CELL_SIZE, start[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))     #Colorea la celda de inicio en la posición (start[0], start[1]) con tamaño CELL_SIZE de color verde
        
        if end:
            pygame.draw.rect(screen, RED, (end[0]*CELL_SIZE, end[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        
#Algoritmo de Dijkstra
def dijkstra(start,end):
    visited = set() #Crea un conjunto para meter todas las celdas por las que ya ha pasado
    distance = {start: 0} #Un diccionario que guarda la distancia acumulada hasta cada nodo, inicializa en d(start)=0 porque es el inicio
    prev = {} #Este diccionario va a ser el encargado de trackear el movimiento, guarda el nodo anterior (Cómo? De qué forma?)
    queue = [(0, start)] #Crea una lista de espera donde va comprobando todos los píxeles del frente de onda. Al principio, solo está el punto inicial.

    while queue:
        pygame.event.pump()
        dist_u, u =heapq.heappop(queue) #Extrae el nodo con menor distancia acumulada
        if u in visited:
            continue        #Comprueba los píxeles ya visitados??!?
        visited.add(u)

        # Pintar celda
        if u != start and u != end:
            pygame.draw.rect(screen, (100, 148, 186), (u[0]*CELL_SIZE, u[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        pygame.time.delay(5)  # Ajusta el retraso a tu gusto

        if u == end:
            break       #Evidentemente, si el pixel analizado es el objetivo ya se acabó.
        
        neighbors = get_neighbors(u)    #Función que definiremos más adelante
        for v in neighbors:
            if v in visited or grid[v[1]][v[0]] == 1:       #Si ya está visitado o es un muro
                continue
            alt = dist_u + 1    #La distancia de los vecinos es la d(u)+1
            if alt < distance.get(v, float("inf")):     #Imagina que llegamos a un punto por dos caminos, pues nos quedamos con el más corto (Rarete: aquí no se cumple que si llegamos antes, recorremos menos al ser la velocidad la misma?)
                distance[v] = alt
                prev[v] = u
                heapq.heappush(queue, (alt, v))     #Mete la nueva tubla (distancia, punto) en la lista de espera
    
    #reconstruir camino
    path = []
    u = end
    while u in prev:
        path.append(u)
        u = prev[u]     #Hazme una marcha atrás, va desde end hasta start basándose en el registro de prev
    path.append(start)
    path.reverse()
    for pos in path:
        if pos != start and pos != end:
            pygame.draw.rect(screen, (0, 0, 255), (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()
    return path


def get_neighbors(pos):
    x, y=pos
    neighbors = []
    for dx, dy in [(-1,0), (1,0), (0,-1),(0,1)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx <N and 0<= ny <N:
            neighbors.append((nx,ny))
    return neighbors

#Bucle principal
running = True
path = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #Cierra la ventana
            running = False
        
        elif pygame.mouse.get_pressed()[0]: #Botón izquierdo del ratón
            x, y = pygame.mouse.get_pos()
            grid[y//CELL_SIZE][x//CELL_SIZE] = 1
        
        elif pygame.mouse.get_pressed()[1]: #Botón central del ratón
            x, y = pygame.mouse.get_pos()
            grid[y//CELL_SIZE][x//CELL_SIZE] = 0
        
        elif pygame.mouse.get_pressed()[2]:  # Botón derecho
            x, y = pygame.mouse.get_pos()
            cell = (x // CELL_SIZE, y // CELL_SIZE)
            if not start:
                start = cell
            elif not end and cell != start:
                end = cell
            elif cell != start and cell != end:
                start = cell
                end = None  # reinicia el end para forzar que se elija de nuevo
        
        
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start and end:
                path = dijkstra(start, end)
            elif event.key == pygame.K_c:
                grid = [[0 for _ in range(N)] for _ in range(N)]
                start = end = None
                path = []
            elif event.key == pygame.K_r:
                grid = [[0 for _ in range(N)] for _ in range(N)]
                start = None
                end = None
                path = []
    
    screen.fill(WHITE)
    draw_grid()
    for pos in path:
        if pos != start and pos != end:
            pygame.draw.rect(screen, BLUE, (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

pygame.quit()