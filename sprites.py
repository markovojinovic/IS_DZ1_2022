import math
import random

import pygame
import os
import config

from itertools import permutations

class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, x, y, file_name, transparent_color=None, wid=config.SPRITE_SIZE, hei=config.SPRITE_SIZE):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (wid, hei))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Surface(BaseSprite):
    def __init__(self):
        super(Surface, self).__init__(0, 0, 'terrain.png', None, config.WIDTH, config.HEIGHT)


class Coin(BaseSprite):
    def __init__(self, x, y, ident):
        self.ident = ident
        super(Coin, self).__init__(x, y, 'coin.png', config.DARK_GREEN)

    def get_ident(self):
        return self.ident

    def position(self):
        return self.rect.x, self.rect.y

    def draw(self, screen):
        text = config.COIN_FONT.render(f'{self.ident}', True, config.BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


class CollectedCoin(BaseSprite):
    def __init__(self, coin):
        self.ident = coin.ident
        super(CollectedCoin, self).__init__(coin.rect.x, coin.rect.y, 'collected_coin.png', config.DARK_GREEN)

    def draw(self, screen):
        text = config.COIN_FONT.render(f'{self.ident}', True, config.RED)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


class Agent(BaseSprite):
    def __init__(self, x, y, file_name):
        super(Agent, self).__init__(x, y, file_name, config.DARK_GREEN)
        self.x = self.rect.x
        self.y = self.rect.y
        self.step = None
        self.travelling = False
        self.destinationX = 0
        self.destinationY = 0

    def set_destination(self, x, y):
        self.destinationX = x
        self.destinationY = y
        self.step = [self.destinationX - self.x, self.destinationY - self.y]
        magnitude = math.sqrt(self.step[0] ** 2 + self.step[1] ** 2)
        self.step[0] /= magnitude
        self.step[1] /= magnitude
        self.step[0] *= config.TRAVEL_SPEED
        self.step[1] *= config.TRAVEL_SPEED
        self.travelling = True

    def move_one_step(self):
        if not self.travelling:
            return
        self.x += self.step[0]
        self.y += self.step[1]
        self.rect.x = self.x
        self.rect.y = self.y
        if abs(self.x - self.destinationX) < abs(self.step[0]) and abs(self.y - self.destinationY) < abs(self.step[1]):
            self.rect.x = self.destinationX
            self.rect.y = self.destinationY
            self.x = self.destinationX
            self.y = self.destinationY
            self.travelling = False

    def is_travelling(self):
        return self.travelling

    def place_to(self, position):
        self.x = self.destinationX = self.rect.x = position[0]
        self.y = self.destinationX = self.rect.y = position[1]

    # coin_distance - cost matrix
    # return value - list of coin identifiers (containing 0 as first and last element, as well)
    def get_agent_path(self, coin_distance):
        pass


class ExampleAgent(Agent):
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):
        path = [i for i in range(1, len(coin_distance))]
        random.shuffle(path)
        return [0] + path + [0]



#     POMOCNA STRUKTURA PODATAKA
class Data(object):

    def __init__(self, pri, arr):
        self.priority = pri
        self.list = arr

    def __str__(self):
        return ' '.join([str(self.priotiry) for i in self.list])

    def __lt__(self, other):
        selfPriority = (self.priority, len(self.list), self.list[len(self.list) - 1])
        otherPriority = (other.priority, len(other.list), other.list[len(self.list) - 1])
        return selfPriority < otherPriority



def cost_of_path(list, coin_distance):
    cost = 0
    for i in range(0, len(list) - 1):
        cost += coin_distance[list[i]][list[i + 1]]

    return cost



#     PO DEFINICIJI ZAMISLJENO DA SE PROSLEDJUJE PODATAK TIPA 'DATA'
#     I DA JE MANJI BROJ VECI PRIORITET
class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def delete(self):
        try:
            max_val = 0
            for i in range(len(self.queue)):
                if self.queue[i].priority < self.queue[max_val].priority:
                    max_val = i
            item = self.queue[max_val]
            del self.queue[max_val]
            return item
        except IndexError:
            print()
            exit()

    def top(self):
        try:
            max_val = 0
            for i in range(len(self.queue)):
                if self.queue[i].priority < self.queue[max_val].priority:
                    max_val = i
            item = self.queue[max_val]
            return item
        except IndexError:
            print()
            exit()



#   ALGORITAM ZA RACUNANJE OBUHVATNOG STABLA GRAFA
#   DIJKSTRIN ALGROITAM, KORISCEN KOD A* ALGORITMA ZA HEURISTIKU
def dijkstra(graph, start):
    """
    Implementation of dijkstra using adjacency matrix.
    This returns an array containing the length of the shortest path from the start node to each other node.
    It is only guaranteed to return correct results if there are no negative edges in the graph. Positive cycles are fine.
    This has a runtime of O(|V|^2) (|V| = number of Nodes), for a faster implementation see @see ../fast/Dijkstra.java (using adjacency lists)

    :param graph: an adjacency-matrix-representation of the graph where (x,y) is the weight of the edge or 0 if there is no edge.
    :param start: the node to start from.
    :return: an array containing the shortest distances from the given start node to each other node
    """
    # This contains the distances from the start node to all other nodes
    distances = [float("inf") for _ in range(len(graph))]

    # This contains whether a node was already visited
    visited = [False for _ in range(len(graph))]

    # The distance from the start node to itself is of course 0
    distances[start] = 0

    # While there are nodes left to visit...
    while True:

        # ... find the node with the currently shortest distance from the start node...
        shortest_distance = float("inf")
        shortest_index = -1
        for i in range(len(graph)):
            # ... by going through all nodes that haven't been visited yet
            if distances[i] < shortest_distance and not visited[i]:
                shortest_distance = distances[i]
                shortest_index = i

        # print("Visiting node " + str(shortest_index) + " with current distance " + str(shortest_distance))

        if shortest_index == -1:
            # There was no node not yet visited --> We are done
            return distances

        # ...then, for all neighboring nodes that haven't been visited yet....
        for i in range(len(graph[shortest_index])):
            # ...if the path over this edge is shorter...
            if graph[shortest_index][i] != 0 and distances[i] > distances[shortest_index] + graph[shortest_index][i]:
                # ...Save this path as new shortest path.
                distances[i] = distances[shortest_index] + graph[shortest_index][i]
                # print("Updating distance of node " + str(i) + " to " + str(distances[i]))

        # Lastly, note that we are finished with this node.
        visited[shortest_index] = True
        arr = []
        for i in range(0, len(visited)):
            if(visited[i]):
                arr.append(i)


        return arr



class Aki(Agent):   #TODO: Proveriti
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):    #   greedy

        path = [0]
        current_position = 0

        while(True):
            local_min = float('inf')
            min_index = 0

            for j in range(1, len(coin_distance)):
                if(coin_distance[current_position][j] < local_min and coin_distance[current_position][j] != 0 and j not in path):
                    local_min = coin_distance[current_position][j]
                    min_index = j

            current_position = min_index
            path.append(min_index)

            if(len(path) == len(coin_distance)):
                break


        return path + [0]



class Jocke(Agent): #TODO: Proveriti
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):    #   bruth - force

        list_of_permutations = list(permutations(range(1, len(coin_distance))))
        min_path = list_of_permutations[0]
        curr_path_cost = 0
        curr_pos = 0

        for j in min_path:
            curr_path_cost += coin_distance[curr_pos][j]
            curr_pos = j

        curr_path_cost += coin_distance[curr_pos][0]
        min_path_cost = curr_path_cost

        for i in list_of_permutations:
            curr_path_cost = 0
            curr_pos = 0

            for j in i:
                curr_path_cost += coin_distance[curr_pos][j]
                curr_pos = j
            curr_path_cost += coin_distance[curr_pos][0]

            if(min_path_cost > curr_path_cost):
                min_path_cost = curr_path_cost
                min_path = i

        curr = min_path
        min_path = [0]
        for i in curr:
            min_path.append(i)
        min_path.append(0)


        return min_path



class Uki(Agent):   #TODO: Proveriti
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):    #   branch and bounds

        min_path = []
        queue = PriorityQueue()
        queue.insert(Data(0,[0]))

        # uzmi iz cvora sa najmanjim prioritetom
        # ako je poslednji cvor liste krajnji - izadji, gotov algoritam
        # ako nije za svaki naslednik cvor poslednjeg iz liste dodaj po jednu novu parcijalnu listu u red

        while(True):
            curr = queue.delete()
            last_node = curr.list[len(curr.list) - 1]
            if(last_node == 0 and len(curr.list) > 2):
                min_path = curr.list
                break

            for i in range(0, len(coin_distance)):
                if(i in curr.list):
                    if(i == 0 and len(curr.list) == len(coin_distance)):
                        currrr = 1
                    else:
                        continue
                arr = []
                for x in curr.list:
                    arr.append(x)
                arr.append(i)

                cost = cost_of_path(arr, coin_distance)

                queue.insert(Data(cost, arr))


        return min_path



class Micko(Agent): #TODO: Proveriti
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):    #   A*

        #   isti djavo kao bnb samo se heuristika sabira sa cenama puta
        #   kad se racuna cena heuristike nekog stabla vadi se i stabla trenutni cvor i svi pre njega u podstablu

        min_path = []
        queue = PriorityQueue()
        queue.insert(Data(0, [0]))

        # uzmi iz cvora sa najmanjim prioritetom
        # ako je poslednji cvor liste krajnji - izadji, gotov algoritam
        # ako nije za svaki naslednik cvor poslednjeg iz liste dodaj po jednu novu parcijalnu listu u red

        while (True):
            curr = queue.delete()
            last_node = curr.list[len(curr.list) - 1]
            if (last_node == 0 and len(curr.list) > 2):
                min_path = curr.list
                break

            for i in range(0, len(coin_distance)):
                if (i in curr.list):
                    if (i == 0 and len(curr.list) == len(coin_distance)):
                        currrr = 1
                    else:
                        continue
                arr = []
                for x in curr.list:
                    arr.append(x)
                arr.append(i)

                cost = cost_of_path(arr, coin_distance)
                spt = dijkstra(coin_distance, 0)
                for x in arr:
                    if(x in spt):
                        spt.remove(x)
                if(len(spt) > 1):
                    heuristic = cost_of_path(spt)
                    cost += heuristic

                queue.insert(Data(cost, arr))

        return min_path
