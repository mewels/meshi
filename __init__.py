import json
import os
import cmd

class Ingredient: 
    name = ''
    amount = ''

    def __init__(self, n, a) -> None:
        self.name = n
        self.amount = a
    
    def fromdict(self, d:dict): 
        pair = [(v,k) for (k,v) in d.items()]
        for p in pair:
            self.amount = p[0]
            self.name = p[1]
        
    def getname(self):
        return self.name
    
    def getamount(self):
        return self.amount
    
    def __repr__(self) -> str:
        return f"name: {self.name} amount: {self.amount}"
    
    def todict(self):
        return {self.name : self.amount}

class Step: 
    number = 0
    action = 'a string'

    def __init__(self, n, a) -> None:
        self.number = n
        self.action = a

    def __repr__(self) -> str:
        return f"{self.number} : {self.action}"
    
    def todict(self):
        return {self.number : self.action}
    
    def fromdict(self, d:dict): 
        pair = [(v,k) for (k,v) in d.items()]
        for p in pair:
            self.action = p[0]
            self.number = p[1]

class Recipe:
    name = ''
    id = 0
    ingredients = []
    steps = []

    def __init__(self, n:str, i:Ingredient, s:Step) -> None:
        self.name = n
        self.ingredients.append(i)
        self.steps.append(s)
    
    def addname(self, n:str):
        self.name = n

    def addid(self, i:int):
        self.id = i

    def generateuniqueid(self):
        x = 1
        directory = './recipes/'
        for filename in os.listdir(directory):
            id = int(filename.removesuffix('.json'))
            if x == id:
                x += 1
        self.addid(x)
 
    def addingredient(self, i):
        self.ingredients.append(i)

    def addstep(self, s):
        self.steps.append(s)

    def __repr__(self) -> str:
        print(f"[ {self.name} ]\n")
        print("ingredients:")
        for i in self.ingredients:
            print(f"{i.name.lower()} : {i.amount.lower()}")
        print("\nsteps:")
        for s in self.steps:
            print(f"{s.number} : {s.action}")
        return ''

    def printingredients(self):
        for i in self.ingredients:
            print(f"name: {i.name} amount: {i.amount}\n")

    def printsteps(self):
        for s in self.steps:
            print(f"{s.number} : {s.action}\n")
        
    def todict(self):
        r = {}
        r.update({'name' : self.name.lower()})
        il = []
        for i in self.ingredients:
            x = {i.name.lower() : i.amount.lower()}
            il.append(x)
        r.update({'ingredients' : il})
        sl = []
        for s in self.steps:
            y = {int(s.number) : s.action.lower()}
            sl.append(y)
        r.update({'steps' : sl})
        return r
    
    def fromdict(self, d:dict):
        self.name = ''
        self.ingredients = []
        self.steps = []
        for (k,v) in d.items():
            if (k == 'name'):
                self.name = v
            elif (k == 'ingredients'):
                for i in v:
                    x = Ingredient('','')
                    x.fromdict(i)
                    self.ingredients.append(x)
            elif (k == 'steps'):
                for s in v:
                    x = Step(0,'')
                    x.fromdict(s)
                    self.steps.append(x)

    def serialize(self):
        # to do : add a check to make sure id is unique/correct - otherwise doing this could overwrite wrong recipe. 
        with open(f'./recipes/{self.id}.json', 'w') as f:
            json.dump(self.todict(),f)
    
    def deserialize(self, id):
        self.id = id
        with open(f'./recipes/{id}.json','r') as f:
            self.fromdict(json.load(f))

    def totxt(self):
        with open(f"{self.id}.txt",'w') as f:
            f.write(f"{self.name}\n")
            f.write("\nIngredients\n")
            for i in self.ingredients:
                f.write(f"{i.name} : {i.amount}\n")
            f.write("\nSteps\n")
            for s in self.steps:
                f.write(f"[{s.number}] : {s.action}\n")
            
class Shell(cmd.Cmd):
    intro = '[Recipebook]\nType help or ? to list commands\n'
    prompt = ">> "

    def do_add(self, arg):
        'Add a recipe to the book via command line input'
        x = emptyrecipe()
        x.generateuniqueid()
        print("Input name of recipe\n")
        x.name = input(">> ")
        x.ingredients = ingredientinput()
        if x.ingredients == []:
            return
        os.system("clear")
        x.steps = stepinput()
        os.system("clear")
        x.serialize()

    def do_list(self, arg):
        'List recipes in book'
        directory = './recipes/'
        for filename in os.listdir(directory):
            id = filename.removesuffix('.json')
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                r = emptyrecipe()
                r.deserialize(id)
                print(f'[{id}] : {r.name}')

    def do_open(self, arg):
        'Open recipe with id: arg'
        id = int(arg)
        p = emptyrecipe()
        p.deserialize(id)
        p.totxt()
        os.system(f"code {p.id}.txt")

    def do_search(self, arg:str):
        'Search for recipe with search [name]'
        directory = './recipes/'
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            id = filename.removesuffix('.json')
            if os.path.isfile(f):
                r = emptyrecipe()
                r.deserialize(id)
                if arg.lower() in r.name.lower():
                    print(f'[{id}] : {r.name}')

    def do_isearch(self, arg:str):
        'Prints a list of recipes containing ingredient [arg]'
        directory = './recipes/'
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            id = filename.removesuffix('.json')
            if os.path.isfile(f):
                r = emptyrecipe()
                r.deserialize(id)
                for i in r.ingredients:
                    if arg.lower() in i.name.lower():
                        print(f'[{id}] : {r.name}')

    def do_remove(self, arg):
        'Remove recipe with id [arg]'
        directory = './recipes/'
        filename = f'{arg}.json'
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            os.remove(f)

    def do_exit(self, arg):
        'Exit the program'
        directory = './'
        for filename in os.listdir(directory):
            if filename.endswith('.txt') and filename != 'notes.txt':
                f = os.path.join(directory, filename)
                if os.path.isfile(f):
                    os.remove(f)
        print('bye :3')
        exit()

def ingredientinput() -> list:
    promptstring = "Input ingredient in the following form: 'Ingredient' : 'amount'\nInput '0' to stop input"
    r = []
    while True:
        print(promptstring)
        c = input(">> ")
        if c == '0':
            break
        elif len(c.partition(':')[1]) == 0:
            return []
        i = Ingredient('','')
        t = c.partition(':')
        i.name = t[0].strip()
        i.amount = t[2].strip()
        r.append(i)
    return r

def stepinput() -> list:
    promptstring = "Input steps in the following form: 'description of step action'\nInput '0' to stop input"
    r = []
    k = 1
    while True:
        print(promptstring)
        c = input(f"[{k}] >> ")
        if c == '0':
            break
        c = c.strip()
        s = Step(0,'')
        s.number = k
        s.action = c
        r.append(s)
        k += 1
    return r

def emptyrecipe() -> Recipe:
    n = ''
    i = Ingredient('','')
    s = Step(0,'')
    return Recipe(n,i,s)

Shell().cmdloop()