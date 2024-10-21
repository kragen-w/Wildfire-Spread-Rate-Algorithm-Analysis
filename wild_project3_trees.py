from random import random
import dudraw

"""
    This program creates a forest of given dimenstions and density, and can simulate if a fire will spread to the bottom.
    It also as functions that simulate many forest fires to find the probability of fire spreading for density, and also 
    what density gets a specific probability of fire spreading
    Filename: wild_project3_trees.py
    Author: Kragen Wild
    Date: 5-5-23
    Course: Data Structures and Alg
    Assignment: Project 3: Percolation - Part 2
    Collaborators: nada
    Internet Source: nada
"""

class SinglyLinkedListIterator:
    def __init__(self, start):
        self.current = start

    def __next__(self):
        if self.current is None:
            raise StopIteration("No more values.")
        to_return = self.current.value
        self.current = self.current.next
        return to_return

    def __iter__(self):
        return self

class SingleNode:
    def __init__(self, v, n):
        self.value = v
        self.next = n

    def __str__ (self):
        return f"{self.value}"

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def __iter__(self):
        return SinglyLinkedListIterator(self.head)

    def get_size(self):
        return self.size

    def is_empty(self):
        if self.head is None:
            return True
        return False
   
    def add_first(self, v):
        #step 1: create new node
        new_node = SingleNode(v, self.head)
        #step 2: change the referance point to new node
        self.head = new_node
        #step 3: incriment size
        self.size += 1

    def add_last(self, v):
        if self.size == 0:
            self.head = SingleNode(v,None)
        else:
            temp = self.head
            while temp.next is not None:
                temp = temp.next
            temp.next = SingleNode(v,None)
        self.size += 1

    def remove_first(self):
        #step 1: check is the list is empty
        if self.head is None:
            raise ValueError("List is empty")
        
        #step2: remember the value
        value_to_return = self.head.value

        #step 3: advance head
        self.head = self.head.next
        self.size -= 1

        #step 4: return value
        return value_to_return

    def remove_last(self):
        temp = self.head
        while temp.next.next is not None:
            temp = temp.next
        to_return = temp.next.value
        temp.next = temp.next.next
        self.size -= 1

        return to_return


    def __str__(self) -> str:
        if self.head is None:
            return "[]"
        result = '['
        temp_node = self.head
        while not temp_node.next is None:
            result += str(temp_node) + " "
            temp_node = temp_node.next
        result += str(temp_node) + "]"
        return result
    
    def find_min(self):
        temp_node = self.head
        min = self.head.value
        while not temp_node is None:
            if min > temp_node.value:
                min = temp_node.value
            temp_node = temp_node.next
        return min

    def remove_at_index(self, index: int):
        
        if self.head is None:
            raise IndexError("The list is empty.")
        temp_node = self.head
        if index == 0:
            return_value = temp_node.value
            self.head = temp_node.next
            return return_value
        for i in range(index):
            if temp_node.next is None:
                raise IndexError("Index does not exist.")
            if i != index-1:
                temp_node = temp_node.next
        return_value = temp_node.next.value
        temp_node.next = temp_node.next.next
        self.size -= 1

        return return_value

    def get(self, index):
        if self.head is None:
            raise IndexError("The list is empty.")
        temp_node = self.head
        for i in range(index):
            if temp_node is None:
                raise IndexError("Index does not exist.")
            
            temp_node = temp_node.next
            print(temp_node.value)
        return temp_node.value

    def rotate(self, n):
        if n <= 0:
            raise IndexError("Rotations must be at least 1")
        for i in range(n):
            value = self.remove_last()
            self.add_first(value)

class DoublyLinkedListIterator:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __next__(self):
        if self.current is self.end:
            raise StopIteration("No more values.")
        to_return = self.current.value
        self.current = self.current.next
        return to_return

    def __iter__(self):
        return self

class DoubleNode:
    def __init__(self, v, p, n):
        self.value = v
        self.prev = p
        self.next = n
    def __str__(self) -> str:
        return str(self.value)

class DoublyLinkedList:
    def __init__(self):
        self.header = DoubleNode(None,None,None)
        self.trailer = DoubleNode(None,self.header,None)
        self.header.next = self.trailer
        self.size = 0
        
    def __iter__(self):
        return DoublyLinkedListIterator(self.header.next, self.trailer)

    def add_between(self, v, n1, n2):
        if n1 is None or n2 is None:
            raise ValueError("Nodes cannot be none.")
        if n1.next is not n2:
            raise ValueError("Node 2 must follow node 1.")

        #step 1: make a new node, value v, prev is n1 next is n2
        newnode = DoubleNode(v,n1,n2)
        #step 2: n1.next points to new node
        n1.next = newnode
        #step 3: n2.prev points to new node
        n2.prev = newnode
        #step 4: size
        self.size += 1

    def add_first(self, v):
        self.add_between(v, self.header, self.header.next)

    def add_last(self,v):
        self.add_between(v, self.trailer.prev, self.trailer)

    def __str__(self) -> str:
        if self.header.next is self.trailer:
            return "[]"
        result = '['
        temp_node = self.header.next
        while not temp_node.next is self.trailer:
            result += str(temp_node) + " "
            temp_node = temp_node.next
        result += str(temp_node) + "]"
        return result

    def remove_between(self, n1, n2):
    # check if either node1 or node2 is None. Raise a ValueError if so.
        if n1 is None or n2 is None:
            raise ValueError("Nodes cannot be none.")
    # Check that node1 and node 2 has exactly 1 node between them, 
    # raise a ValueError if not
        if n1.next.next is not n2:
            raise ValueError("There is more than one node between the 2 nodes you entered.")

    # Everything is in order, so delete the node between node1 and node2, 
    # returning the value that was stored in it
        to_return = n1.next.value
        n1.next = n2
        n2.prev = n1
        self.size -= 1
        return to_return

    def remove_first(self):
        to_return = self.header.next.value
        self.remove_between(self.header, self.header.next.next)
        return to_return

    def remove_last(self):
        to_return = self.trailer.prev.value
        self.remove_between(self.trailer.prev.prev, self.trailer)
        return to_return

    def search(self, v):
        index = 0
        temp = self.header.next
        while temp.value is not v:
            temp = temp.next
            index += 1
            if temp.next is None:
                return -1
        return index
            
    def find_min(self):
        temp_node = self.head
        min = self.head.value
        while not temp_node is None:
            if min > temp_node.value:
                min = temp_node.value
            temp_node = temp_node.next
        return min

    def get_size(self):
        return self.size

    def first(self):
        return self.header.next.value

    def last(self):
        return self.trailer.prev.value

    def is_empty(self):
        if self.size == 0:
            return True
        else:
            return False

    def get(self, index):
        if self.size == 0:
            raise IndexError("The list is empty.")
        temp_node = self.header.next
        for i in range(index):
            if temp_node.next == None:
                raise IndexError("Index does not exist.")
            if i != index:
                temp_node = temp_node.next
        return temp_node.value

class Stack:
    def __init__(self):
        self.the_stack = SinglyLinkedList()

    def push(self, v):
        self.the_stack.add_first(v)

    def pop(self):
        self.the_stack.remove_first()
        return

    def top(self):
        return self.the_stack.get(0)

    def is_empty(self):
        return self.the_stack.is_empty()
    
    def get_size(self):
        return self.the_stack.get_size()

    def __str__(self):
        return self.the_stack.__str__()

class Queue:
    def __init__(self) -> None:
        self.the_queque = DoublyLinkedList()

    def enqueque(self, v):
        self.the_queque.add_last(v)

    def dequeque(self):
        v = self.the_queque.header.next.value
        self.the_queque.remove_first()
        return v

    def first(self):
        return self.the_queque.header.next.value
    
    def get_size(self):
        return self.the_queque.size
    
    def is_empty(self):
        return self.the_queque.size == 0

    def __str__(self):
        return self.the_queque.__str__()

    
class Forest:

    """
    this class creates a forest with a height and width set by the user, with a density also set by the user (between 0 and 1). 
    Two functions are created with different search algorithms are created which each light the top of the forest on fire, and see 
    if the fire spreads to the bottom of the forest. This fire spreading is also drawn with the help of the draw function
    """

    def __init__(self, width, height, density)->None:
        """
        The init function creates the three instance variables width, height, and density. It also initializes forest as an empty list.
        A nested for loop creates a nested list with the dimentions specified. Each value in the list has a "density" percent chance of being a 1,
        which means its a tree. Otherwise, it's a 0, so it's a empty piece of land.
        perameters: self, width: int, height: int, density: float
        return: None
        """
        self.w = width
        self.h = height
        self.d = density
        self.forest = []
        #nested for loop to create the forest
        for i in range(height):
            row = []
            for j in range(width):
                #a random value between 1 and 0 is determined and assigned
                rand = random()
                #if the random value plus the imputted density is above or equal to 1, then a tree is put into the list
                #this makes it so the density is the exact chance of one particular value in the list becoming a tree
                if rand + self.d >= 1:
                    row.append(1)
                else:
                    row.append(0)
            self.forest.append(row)

    def __str__(self)->str:
        """
        This string function prints every row, and a new line inbetween each one, causing a grid to be printed
        perameters: self
        return: str
        """
        to_return = ""
        for row in self.forest:
            to_return += f"{row}\n"
        return to_return

    def depth_first_search(self)->bool:
        """
        This function creates an empty stack, then takes a 2d list of numbers that are either 1 or 0 (the forest) and sets the trees on the first row on fire
        by changing each number 1 of the top row to 2 and adds each coordinate of the top row to the stack (the row is y, column is x). 
        Then, while the stack isn't empty, if any neigbors of the value of the top of the stack are 1, meaning that they are trees, they get
        turned into 2s and added to the stack as well. If the top of the stack has no neibors that are trees, the top of the stack gets deleted.
        This continues until either the stack runs out (returns false), or a the top of the stack is a value at the last row of the forest (returns true),
        meaning the fire spread to the bottom
        perameters: self
        return: bool
        """
        #a stack is created
        self.cells_to_explore = Stack()
        #all the trees of the forest on the first row (top of the forest) are turned into 2s
        for i in range(len(self.forest[0])):
            if self.forest[0][i] == 1:
                self.forest[0][i] = 2
            #the tree is put in the top of the stack
            self.cells_to_explore.push([0,i])

        #while the stack is not empty...
        while self.cells_to_explore.get_size() > 0:
            #the amount of neibors trees are set to 0
            neighbor_trees = 0
            #draw function is called (explained later)
            self.draw(self.cells_to_explore.top())
            
            #the variable "top" is set to the top of the stack
            top = self.cells_to_explore.top()
            #if the value at top[0] (which corresponds to the row) is one less than the height (the last row), then the bottom of the 
            #forest has caught fire, and true is returned
            if top[0] == self.h-1:
                return True

            #if the top of the stack has a neigbor tree above it and is not in the first row...
            if top[0] != 0 and self.forest[top[0]-1][top[1]] == 1:
                #the neigbor becoems 2 (meaning it's on fire)
                self.forest[top[0]-1][top[1]] = 2
                #the neighbor gets put to the top of the stack
                self.cells_to_explore.push([(top[0]-1),(top[1])])
                #neibor count goes up by one
                neighbor_trees += 1

            #if the top of the stack has a neigbor tree to the right of it and is not in the last colum...
            if top[1] != self.w-1 and (self.forest[top[0]][top[1]+1] == 1):
                #the neigbor becoems 2 (meaning it's on fire)                
                self.forest[top[0]][top[1]+1] = 2
                #the neighbor gets put to the top of the stack
                self.cells_to_explore.push([(top[0]),(top[1]+1)])
                #neibor count goes up by one
                neighbor_trees += 1
                
            #if the top of the stack has a neigbor tree to the left of it and is not in the first colum...
            if top[1] != 0 and (self.forest[top[0]][top[1]-1] == 1):
                #the neigbor becoems 2 (meaning it's on fire)                
                self.forest[top[0]][top[1]-1] = 2
                #the neighbor gets put to the top of the stack            
                self.cells_to_explore.push([(top[0]),(top[1]-1)])
                #neibor count goes up by one
                neighbor_trees += 1

            #if the top of the stack has a neigbor tree below it...
            if self.forest[top[0]+1][top[1]] == 1:
                #the neigbor becoems 2 (meaning it's on fire)                
                self.forest[top[0]+1][top[1]] = 2
                #the neighbor gets put to the top of the stack                            
                self.cells_to_explore.push([(top[0]+1),(top[1])])
                #neibor count goes up by one
                neighbor_trees += 1

            #if the top of the stack had no neigbors...
            if neighbor_trees == 0:
                #the top of the stack is removed
                self.cells_to_explore.pop()

        #if the while loop completes, that means the stack ran out, and the fire did not spread
        return False


    def breadth_first_search(self)->bool:
        """
        This function creates an empty queue, then takes a 2d list of numbers that are either 1 or 0 (the forest) and sets the trees on the first row on fire
        by changing each number 1 of the top row to 2 and adds each coordinate of the top row to the queue (the row is y, column is x). 
        Then, while the queue isn't empty, if any neigbors of the value of the beginning of the queue are 1, meaning that they are trees, they get
        turned into 2s and added to the queue as well. If the beginning of the queue has no neibors that are trees, the beginning of the queue gets deleted.
        This continues until either the queue runs out (returns false), or a the beginning of the queue is a value at the last row of the forest (returns true),
        meaning the fire spread to the bottom
        perameters: self
        return: bool
        """
        #a queue is created
        self.cells_to_explore = Queue()
        #all the trees of the forest on the first row (top of the forest) are turned into 2s
        for i in range(len(self.forest[0])):
            if self.forest[0][i] == 1:
                self.forest[0][i] = 2
            #the tree is put in the back of the queue
            self.cells_to_explore.enqueque([0,i])

        #while the stack is not empty...        
        while self.cells_to_explore.get_size() > 0:
            #the amount of neibors trees are set to 0
            neighbor_trees = 0
            #draw function is called (explained later)
            self.draw(self.cells_to_explore.first())
            
            #the variable "top" is set to the beginning of the queue
            top = self.cells_to_explore.first()
            #if the value at top[0] (which corresponds to the row) is one less than the height (the last row), then the bottom of the 
            #forest has caught fire, and true is returned
            if top[0] == self.h-1:
                return True

            #if the beginning of the queue has a neigbor tree above it and is not in the first row...
            if top [0] != 0 and self.forest[top[0]-1][top[1]] == 1:
                #the neigbor becoems 2 (meaning it's on fire)
                self.forest[top[0]-1][top[1]] = 2
                #the neighbor gets put to the back of the queue
                self.cells_to_explore.enqueque([(top[0]-1),(top[1])])
                #neibor count goes up by one
                neighbor_trees += 1

            #if the beginning of the queue has a neigbor tree to the right of it and is not in the last colum...
            if top[1] != self.w-1 and (self.forest[top[0]][top[1]+1] == 1):
                #the neigbor becoems 2 (meaning it's on fire)                
                self.forest[top[0]][top[1]+1] = 2
                #the neighbor gets put to the back of the queue
                self.cells_to_explore.enqueque([(top[0]),(top[1]+1)])
                #neibor count goes up by one
                neighbor_trees += 1
                
            #if the beginning of the queue has a neigbor tree to the left of it and is not in the first colum...
            if top[1] != 0 and (self.forest[top[0]][top[1]-1] == 1):
                #the neigbor becoems 2 (meaning it's on fire)                
                self.forest[top[0]][top[1]-1] = 2
                #the neighbor gets put to the back of the queue  
                self.cells_to_explore.enqueque([(top[0]),(top[1]-1)])
                #neibor count goes up by one
                neighbor_trees += 1

            #if the beginning of the queue has a neigbor tree below it...
            if self.forest[top[0]+1][top[1]] == 1:
                #the neigbor becoems 2 (meaning it's on fire)                
                self.forest[top[0]+1][top[1]] = 2
                #the neighbor gets put to the back of the queue                 
                self.cells_to_explore.enqueque([(top[0]+1),(top[1])])
                #neibor count goes up by one
                neighbor_trees += 1

            #if the beginning of the queue had no neigbors...
            if neighbor_trees == 0:
                #the beginning of the queue is removed
                self.cells_to_explore.dequeque()

        #if the while loop completes, that means the stack ran out, and the fire did not spread
        return False
        

    def draw(self, the_top: tuple)->None:
        """
        This function draws the forest, with green squares as grass, dark green squares as trees, and red squares
        as trees on fire
        perameters: self, the_top: tuple
        return: None
        """
        #nested for loop to access each element of the 2d list which is the forest
        for i in range(len(self.forest)):
            for j in range(len(self.forest[i])):
                #the pen color is set to green by default
                dudraw.set_pen_color(dudraw.GREEN)
                #if the element being looked at is a 1, that means it's a treem so the color is changed to dark green
                if self.forest[i][j] == 1:
                    dudraw.set_pen_color(dudraw.DARK_GREEN)
                #if the element being looked at is a 2, that means it's on fire so the color is changed to red
                elif self.forest[i][j] == 2:
                    dudraw.set_pen_color(dudraw.RED)
                #a square is drawn at the coordinate of the element of the forest being looked at
                dudraw.filled_rectangle(j/(self.w)+1/(2*self.w), (self.h-1-i)/(self.h)+1/(2*self.h), 1.1/(2*self.w),1.1/(2*self.h))
                #color set to white
                dudraw.set_pen_color(dudraw.WHITE)
                #a white outline is drawn around the beginning of the queue or the top of the stack 
                #(depending on what value is passed into the function)
                dudraw.rectangle(the_top[1]/(self.w)+1/(2*self.w), (self.h-1-the_top[0])/(self.h)+1/(2*self.h), 1.1/(2*self.w),1.1/(2*self.h))
        #the drawing is shown for a frame
        dudraw.show(1)
    

class FireProbability:
    
    """
    this class has classes that calculate the probability of a fire spreading based on the density of the forest, 
    and a function to find the tree density that has a .5 probability of fire spreading
    NOTE: there are two duplicates of each of the two function, one for depth and one for breadth algorithms
    """

    def probability_of_fire_spread_dfs(self, d)->float:
        """
        this function takes a density, and simulates a forest fire with that density 5000 times, and however many
        times the fire spread to the bottom / 5000 is the probability of the fire spreading for that density
        perameters: self, d: float
        return: float
        """
        trials = 5000
        fire_spread_count = 0
        #for loop 5000 times
        for i in range(trials):
            # a 20x20 forest with the given denisty is created
            f = Forest(20,20,d)
            #if the fire spreads, the spread count goes up by one
            if f.depth_first_search() == True:
                fire_spread_count += 1

        # the probability of fire spreading in forests of density "d" is:
        probability = (fire_spread_count / trials)
        return probability


    def probability_of_fire_spread_bfs(self, d)->float:
        """
        this function takes a density, and simulates a forest fire with that density 5000 times, and however many
        times the fire spread to the bottom / 5000 is the probability of the fire spreading for that density
        perameters: self, d: float
        return: float
        """
        trials = 5000
        fire_spread_count = 0
        #for loop 5000 times
        for i in range(trials):
            # a 20x20 forest with the given denisty is created
            f = Forest(20,20,d)
            #if the fire spreads, the spread count goes up by one
            if f.breadth_first_search() == True:
                fire_spread_count += 1

        # the probability of fire spreading in forests of density "d" is:
        probability = (fire_spread_count / trials)
        return probability


    def highest_Density_dfs(self):
        """
        this function does a binary searches between 0 and 1 to find the density that has the probibility of .5 of spreading 
        perameters: self
        return: none
        """
        low_density = 0.0
        high_density = 1.0


        for i in range(20):
        #check the midpoint
            density = (high_density + low_density) / 2.0

        #get probability of fire spreading in forests of 'density'
            p = self.probability_of_fire_spread_dfs(density)

        #check probability of fire spreading
            if p < .5:
            #low probability: density can be increased
                low_density = density
            else:
            #high probability: density should be decreased
                high_density = density

        # // the last value of "density" is the value we seek
        return density

    def highest_Density_bfs(self):
        """
        this function does a binary searches between 0 and 1 to find the density that has the probibility of .5 of spreading 
        perameters: self
        return: none
        """
        low_density = 0.0
        high_density = 1.0

        for i in range(20):
        #check the midpoint
            density = (high_density + low_density) / 2.0

        #get probability of fire spreading in forests of 'density'
            p = self.probability_of_fire_spread_bfs(density)

        #check probability of fire spreading
            if p < 0.5:
            #low probability: density can be increased
                low_density = density
            else:
            #high probability: density should be decreased
                high_density = density

        # // the last value of "density" is the value we seek
        return density



# #du scale is set for easy graph making
# dudraw.set_y_scale(-.01,1.01)
# #the list for graph coordinates with 0 at the beginning
# line_intersections = [0]
# #dudraw graph labeling
# dudraw.set_font_family("Courier")
# dudraw.set_font_size(12)
# dudraw.text(0.5, .05, "Tree Density")
# dudraw.text(0.2, .5, "Probability Of Fire Spread")
# #drawing the dashes for the x and y scales
# for i in range(-1, 50):
#     dudraw.line(i/50, -.01, i/50, -.005)
#     dudraw.line(0, i/50, .005, i/50)

# #a blue vertical line is drawn where the probability of fire spreading is .5, which is a .5879 density
# dudraw.set_pen_color(dudraw.BLUE)
# dudraw.line(0.5879, -.01, 0.5879, 1.01)
# dudraw.set_pen_color(dudraw.RED)

# #for loop for values 1 to 100
# for i in range(1, 101):
#     #a new class to calculate fire spread probability is made
#     f = FireProbability()
#     #the probability of spreading is set to the i value/100, which goes from 0.01 to 1.00
#     prob = f.probability_of_fire_spread_dfs(i/100)
#     #the list of line intersections gets that probabiliy at the end of it
#     line_intersections.append(prob)
#     #a red line is drawn from the previous probability to the current one, making up the line of the graph
#     dudraw.line((i-1)/100, line_intersections[i-1], i/100, line_intersections[i])
#     dudraw.show(1)

# dudraw.show(100000)


# f = Forest(50,50,.615) 
f = Forest(50,50,.60)   
f.depth_first_search()  
# f.depth_first_search()
        