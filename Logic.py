import random


SizeX, SizeY = 15, 15
numV,numP,numW = 10,8,6


class Entity:
    PLifeTime = 2
    VLifeTime = 9


    def __init__(self, x, y,lifetime):
        self.x = x
        self.y = y
        self.lifetime = lifetime;
        self.borntime = 3;

class Field:
    #numV, numP, numW = 12, 8, 6
    def __init__(self, numV, numP, numW):
        self.numV, self.numP, self.numW = numV, numP, numW
        self.field = [ ['*'] * SizeY  for y in range( SizeX )]
        self.victims = []
        self.predators = []
        self.walls = []
        self.xy = [(x,y) for x in range( SizeX ) for y in range( SizeY )]

        num = self.numP
        while(num):
            x, y = random.choice(self.xy)
            if self.field[x][y] == '*':
                self.field[x][y] = 'P'
                self.predators.append(Entity(x,y,Entity.PLifeTime))
                num-=1

        num = self.numV
        while (num):
            x, y = random.choice(self.xy)
            if self.field[x][y] == '*':
                self.field[x][y] = 'V'
                self.victims.append(Entity( x, y, Entity.VLifeTime))
                num -= 1

        num = self.numW
        while (num):
            x, y = random.choice(self.xy)
            if self.field[x][y] == '*':
                self.field[x][y] = 'W'
                self.walls.append(Entity(x, y, 0))
                num -= 1
    def reinit(self):
        self.numV, self.numP, self.numW = numV, numP, numW
        self.field = [['*'] * SizeY for y in range(SizeX)]
        self.victims = []
        self.predators = []
        self.walls = []
        self.xy = [(x, y) for x in range(SizeX) for y in range(SizeY)]

        num = self.numP
        while (num):
            x, y = random.choice(self.xy)
            if self.field[x][y] == '*':
                self.field[x][y] = 'P'
                self.predators.append(Entity(x, y, Entity.PLifeTime))
                num -= 1

        num = self.numV
        while (num):
            x, y = random.choice(self.xy)
            if self.field[x][y] == '*':
                self.field[x][y] = 'V'
                self.victims.append(Entity(x, y, Entity.VLifeTime))
                num -= 1

        num = self.numW
        while (num):
            x, y = random.choice(self.xy)
            if self.field[x][y] == '*':
                self.field[x][y] = 'W'
                self.walls.append(Entity(x, y, 0))
                num -= 1
#изменение в след шаг
    def update(self):
       #заполняем поле вероятности
        pfield = self.setProbability()
        self.field = [['*'] * SizeY for x in range(SizeX)]


        for predator in self.predators:
            x, y = self.findtheway(predator, pfield)
            predator.x += x
            predator.y += y
            self.eat(predator)
        self.toField(self.predators,pfield,'P')
        for victim in self.victims:
            x, y = self.findtheway(victim, pfield)
            victim.x += x
            victim.y += y

        self.toField(self.victims, pfield, 'V')
        for wall in self.walls:
            self.field[wall.x][wall.y] = 'W'

    def toField(self,items,pfield, let):
        if let == 'V':
            lifetime = Entity.VLifeTime
        else:
            lifetime = Entity.PLifeTime
        for item in items:
            if item.borntime  <= 0:
                item.borntime = 3
                self.born(items,item, pfield,lifetime)
            else:
                item.borntime -= 1
            if item.lifetime <= 0:
                items.remove(item)
                continue
            else:
                item.lifetime-=1
            self.field[item.x][item.y] = let


    def eat(self, item):
        for victim in self.victims:
            if abs(item.x - victim.x) <= 1 and abs(item.y - victim.y) <= 1:
                victim.lifetime -= 3
                item.lifetime += 1
                item.borntime -= 1
                print('ate at ' + str(victim.x)+':'+str(item.x) +' '+ str(victim.y) + ':' + str(item.y) )

    def born(self,items, item, pfield,lifetime):
        way = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for w in way:
            x, y = w
            if not self.inXY(item.x + x,item.y + y) and \
                item.x + x >= 0 and item.x + x < SizeX and item.y + y >= 0 and item.y + y < SizeY \
                and not pfield[item.x + x][item.x + x] == -1:
                items.append(Entity(item.x+x,item.y+y,lifetime))
                return



    def findtheway(self,item,pfield):

        pway = [ -1 for x in range(4) ]
        way = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for w in way:
            x, y = w
            if item.x + x > 0 and item.x + x < SizeX and item.y + y > 0 and item.y + y < SizeY and not self.inXY(item.x + x,item.y + y):
                pway[way.index(w)] = pfield[item.x + x][item.y + y]
        p = max(pway)
        if p > 0 and p < SizeX+SizeY-1:
            return way[pway.index(p)]
        else:
            return (0, 0)



#заполняем поле вероятности для одного хищника
    def setProbabilityForOne(self, field, predX, predY):
        for x, y in self.xy:
            field[x][y] = field[x][y] + abs(x  - predX) + abs(y - predY)
        return field

#суммарное поле вероятности для всех хищников
    def setProbability(self):
        pfield = [[0] * SizeY for y in range(SizeX)]#сначала запихаем 0
        for predator in self.predators:
            pfield = self.setProbabilityForOne(pfield,predator.x,predator.y)#прогоняем каждого
        for walls in self.walls:
            pfield[walls.x][walls.y] = -1#в клетках со стенами -1
        return pfield

    def inXY(self,x,y):
        for v in self.victims:
            if v.x == x and v.y == y:
                return True
        for p in self.predators:
            if p.x == x and p.y == y:
                return True
        return False

#распечатка поля
    def print(self):
        for x in range(SizeX):
            s = ''
            for y in range(SizeY):
                s += self.field[y][x]
            print(s)