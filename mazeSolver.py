from colorama import Fore, Style,init
from sys import argv



# print(Fore.RED + 'some red text')
# print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim text')
# print(Style.RESET_ALL)
color=init()
class node:
    def __init__(self,state):
        self.state=state
        self.parent=None
        self.childs=[]

class StackFrontier:
    def __init__(self,node):
        self.nodes=[]
        self.insertNode(node)
    
    def insertNode(self,n):
        self.nodes.append(n)
    
    def deleteNode(self):
        node=None
        if len(self.nodes)==0:
            print("Empty List")
        else:
            node=self.nodes.pop()        
        return node
    
    def __len__(self):
        return self.nodes.__len__()

class QueueFrontier(StackFrontier):
    def deleteNode(self):
        node=None
        if len(self.nodes)==0:
            print("Empty List")
        else:
            node=self.nodes[0]
            self.nodes=self.nodes[1:]
        return node
    
def mazeToMatrix(filename):
    """
     For taking input as maze problem file
     which hase initial state 'A' and goal state
     'B' and it contains walls as '#' and movable path as ' '
     This Function will return Maze as Matrix(List)
    """
    f=open(filename)
    lines=f.readlines()
    for i in range(len(lines)):
        while lines[i].endswith("\n"):
            lines[i]=lines[i].split("\n")[0]
    init_state=None
    goal_state=None
    maze=[]
    for i in range(len(lines)):
        ch=[]
        for j in range(len(lines[i])):
            if lines[i][j]=='A':
                init_state=(i,j)
            elif lines[i][j]=='B':
                goal_state=(i,j)
            ch.append(lines[i][j])
        maze.append(ch)
    return maze,init_state,goal_state


mat,initial,goal=mazeToMatrix("maze4.txt")
if len(argv)>1:
    mat,initial,goal=mazeToMatrix(argv[1])

size_x=len(mat)
size_y=len(mat[0])
def printMaze(matrix):
    for i in matrix:
        for j in i:
            if j=='-':
                print(Fore.RED+j,end=" ")
            elif j=='*' or j=='A' or j=='B':
                print(Fore.GREEN+j,end=" ")
            else:
                print(Style.RESET_ALL,end="")
                print(j,end=" ")
        print()

def moveRight(state):
    if state[1]+1<len(mat[0]) and mat[state[0]][state[1]+1]!='#':
        return True
    return False
def moveLeft(state):
    if state[1]-1>=0 and mat[state[0]][state[1]-1]!='#':
        return True
    return False
def moveUp(state):
    if state[0]-1>=0 and mat[state[0]-1][state[1]]!='#':
        return True
    return False
def moveDown(state):
        if state[0]+1<len(mat) and mat[state[0]+1][state[1]]!='#':
            return True
        return False
def actions(state,nodeList):
    moves=[]
    if moveRight(state):
        for i in nodeList:
            if i.state==(state[0],state[1]+1):
                moves.append(i)
    if moveLeft(state):
        for i in nodeList:
            if i.state==(state[0],state[1]-1):
                moves.append(i)
    if moveUp(state):
        for i in nodeList:
            if i.state==(state[0]-1,state[1]):
                moves.append(i)
    if moveDown(state):
        for i in nodeList:
            if i.state==(state[0]+1,state[1]):
                moves.append(i)
    return moves
nodes=[]
for i in range(size_x):
    for j in range(size_y):
        n=node((i,j))
        if n.state==goal:
            goal_state=n
        elif n.state==initial:
            initial_state=n            
        nodes.append(n)

# Use StackFrontier for Depth First Search and
# Use QueueFrontier for Bredth First Search
def findSolution(frontier,show_state_searched=False):
    visited=[]
    path=[]
    while True:
        if len(frontier)==0:
            print(Fore.RED+"No Solutions Found")
            print(Style.RESET_ALL,end="")
            break
        else:
            temp=frontier.deleteNode()
            if temp!=goal_state and temp!=initial_state:
                mat[temp.state[0]][temp.state[1]]="-"
            visited.append(temp)
            if temp==goal_state:
                print(Fore.GREEN+"Reached Goal")
                print(Style.RESET_ALL,end="")
                while(temp!=None):
                    path.append(temp.state)
                    if temp!=goal_state and temp!=initial_state:
                        mat[temp.state[0]][temp.state[1]]='*'
                    temp=temp.parent
                break
            else:
                childs=[]
                moves=actions(temp.state,nodes)
                for i in moves:
                    childs.append(i)
                
                for node in childs:
                    if node not in visited:
                        node.parent=temp
                        frontier.insertNode(node)

frontier=QueueFrontier(initial_state)
findSolution(frontier)
printMaze(mat)