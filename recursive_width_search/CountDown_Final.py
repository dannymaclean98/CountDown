#Countdown numbers game
import sys, random, itertools, time, cProfile, argparse

start = time.time()

parser = argparse.ArgumentParser(description="Solve the countdown numbers game")
parser.add_argument("-n", "--number_of_cards", type=int, default=6, choices=range(3,10), help="The number of cards drawn at random from the deck (default 6)")
parser.add_argument("-b", "--big_numbers", type=int, default=2, choices=range(5), help="The number of big numbers to include in the draw (default 2)")
parser.add_argument("-u", "--target_upper", type=int, default=999, help="The upper range of the randomly generated target number (default 999)")
parser.add_argument("-l", "--target_lower", type=int, default=100, help="The lower range of the randomly generated target number (default 100)")
parser.add_argument("-s", "--special_big_numbers", action='store_true', help="Whether to use the special set of big numbers [12, 37, 62, 87] instead of the usual [25, 50, 75, 100]")
parser.add_argument("-ot", "--override_target", type=int, help="Override for the target to be used (instead of random generation)")
parser.add_argument("-oc", "--override_cards", help="Override for the cards to be used instead of random generation (use Python list format, e.g. [3, 5, 6, 3, 75, 25])")

args = parser.parse_args()

#CONSTANTS
MAX_BIG = 4

#Set up some variables
if not args.special_big_numbers:
    big_numbers = [25,50,75,100]
else:
    big_numbers = [12, 37, 62, 87]
small_numbers = [x for x in range(1, 11)]*2
num_big = args.big_numbers
num_small = args.number_of_cards - num_big

#Do some checking - I'm happy to bail out in an ugly way!
assert(num_big >= 0)
assert(num_big <= MAX_BIG)
assert(num_small >= 0)
assert((num_big + num_small) == args.number_of_cards)

#Generate numbers
numbers = []
random.shuffle(big_numbers)
random.shuffle(small_numbers)
for ix in range(num_big):
    numbers.append(big_numbers[ix])

for ix in range(num_small):
    numbers.append(small_numbers[ix])

assert(len(numbers) == args.number_of_cards)
print("Cards: " + str(numbers))

#Generate 3-digit target 100 <= N <= 999
target = random.randint(args.target_lower, args.target_upper)
print("Target: " + str(target))

if args.override_target is not None:
    target = args.override_target
    print("Overriding target: " + str(target))

if args.override_cards is not None:
    numbers = eval(args.override_cards)
    print("Overriding cards: " + str(numbers))

# Class represents a Node in the search tree. 
#   - id is an ordered list of ops and permutations of indices that we used to get here from the root. It uniquely defines the node.
#   - state is a list of the current numbers 
#   - parent is a reference to the parent node.
#   - gen is a generator function for this node that gets the next one
class Node:

    def __init__(self, id, state, parent):
        self.id = id
        self.state = state
        self.parent = parent
        #This relies on the only number of interest in this node being the one calculated by 
        #combining 2 of the numbers in state (we'll have tested other numbers in the state
        # in parent nodes) - i.e. the last number in the list
        self.proximity_to_target = abs(target - self.state[-1])
        self.gen = None

    def __str__(self):
        if self.parent is None:
            return "Root node - nothing to show"
        else:
            return "Node\n  Id: " + str(self.id) + "\n  State: " + str(self.state) + "\n  Parent: " + str(self.parent.id) + "\n  Proximity: " + str(self.proximity_to_target)

    #This function is a generator that yields the next node to explore. It yields None if the 
    #next node is not worth exploring, e.g. if the op is divide and the numbers are not exactly divisible
    #or if it's subtract and the numbers are equal: we'll explore these trees elsewhere. It throws a 
    #StopIteration exception once we've finished - that's the trigger to grab the parent node and delete this one.
    #
    #It's this generator that does most of the work.
    def generate_next_node(self):
        if len(self.state) == 1:
            raise StopIteration
        #Note that though / and - depend on order, only one ordering is ever worth exploring - for a - b it's where a > b.
        #So we can use combinations rather than permutations. 
        for i, j in itertools.combinations(range(len(self.state)), 2):
            for op in ops:
                #Create the id
                new_id = self.id + [(i, j, op)]

                #Set the new parent to this guy
                new_parent = self
               
                #Prep the new state. Remove the numbers at indices i and j and assign them to x and y
                #Once we've calculated the effect of applying the op to x and y we'll 
                new_state = list(self.state)

                #It's crucial to pop these off in reverse order (or alternatively pop j-1). j is always greater than i due to the combinations function,
                #so if we popped i first, then the elements of the list above index i, including j, would be shuffled down and we'd be taking the wrong 
                #element from the list. Subtle!
                y = new_state.pop(j)
                x = new_state.pop(i)

                #Switch between ops and do the right thing.
                if op == "*":
                    new_state.append(x * y)
                elif op == "+":
                    new_state.append(x + y)
                elif op == "-":
                    if x != y:
                        new_state.append(max(x, y) - min(x, y))
                    else:
                        yield None
                        continue
                elif op == "/":
                    if ((max(x, y) % min(x, y)) == 0):
                        new_state.append(max(x, y) / min(x, y))
                    else:
                        yield None
                        continue
                
                # Yield a new node with this id, state and parent
                yield Node(new_id, new_state, new_parent)

    def get_generator(self):
        if self.gen is None:
            self.gen = self.generate_next_node()
        return self.gen

#The 4 ops
ops = ["*", "+", "-", "/"]

# Create the root node
root = Node([], numbers, None)

# States we've seen before will go in here (converted to a string). If we encounter any states on our search 
# that we've seen before we can throw away the entire subtree.
seen = set()
#This stores the node that contains the number that's closest to the target so far
best_node = None

# Now the main depth-first search. It's bizarrely simple!
current_node = root

#For fun, count how many operations are required (i.e. how many nodes we need to explore)
#And how many branches we skip due to the funky hashing.
op_counter = 0
skip_counter = 0
while True:
    op_counter += 1
    try:
        next_node = next(current_node.get_generator())

        #Is there actually a next node? If it was a / or - that resulted in nothing interesting, then we'll have returned None.
        #Just get the next one from the generator.
        if next_node is None:
            continue

        #Have we seen this node before? If so, no point in continuing down this path, just continue to next iteration of the loop
        state_as_string = str(sorted(next_node.state))
        if state_as_string in seen:
            skip_counter += 1
            continue
        else:
            #Not seen this node before. Add it to seen 
            seen.add(state_as_string)

        #Have we got it?
        if (next_node.proximity_to_target == 0):
            #Got solution!
            best_node = next_node
            break
        elif ((best_node is None) or (next_node.proximity_to_target < best_node.proximity_to_target)):
            best_node = next_node
        
        # Got to here and next_node is now our current node - going deeper!
        current_node = next_node
        

    except StopIteration:
        # Expanded all nodes under this one
        if (current_node is not root):
            #This node is done. Set the current node to parent, and continue
            current_node = current_node.parent
            continue
        else:
            #Root node has no further children. We're done!
            break

#This redoes the calculation for the solution using the id of the winning node,
#but that's really fast, and the occupancy hit of storing the string list in every
#node is prohibitive.
def get_calc_text(node, numbers):
    numbers_as_string = [str(x) for x in numbers]
    numbers_copy = list(numbers)
    for (i, j, op) in node.id:
        #Remember to pop in the opposite order because higher elements shuffle down and i<j (strictly)
        y_str = numbers_as_string.pop(j)
        x_str = numbers_as_string.pop(i)
        y = numbers_copy.pop(j)
        x = numbers_copy.pop(i)
        
        #Do the sum
        if op == "*":
            numbers_copy.append(x * y)
        elif op == "+":
            numbers_copy.append(x + y)
        elif op == "-":
            numbers_copy.append(max(x, y) - min(x, y))
            if (y > x):
                (x_str, y_str) = (y_str, x_str)
        elif op == "/":
            numbers_copy.append(max(x, y) / min(x, y))
            if (y > x):
                (x_str, y_str) = (y_str, x_str)            

        text_for_op = "(" + x_str + " " + op + " " + y_str + ")"
        numbers_as_string.append(text_for_op)
    
    return numbers_as_string[-1]

end = time.time()
# End game
if (best_node is not None):
    if (best_node.proximity_to_target == 0):
        print("Got a solution: " + str(best_node.state[-1]))
    else:
        print("No solution. Closest is: " + str(best_node.state[-1]))

    print("Here's how I got it: " + get_calc_text(best_node, numbers))
    print("It took me " + str(end - start) + " seconds")
    print("It took me " + str(op_counter) + " ops")
    print("I managed to skip " + str(skip_counter) + " subtrees via hashing")
else: 
    raise Exception("Something went wrong!")