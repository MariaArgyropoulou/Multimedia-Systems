import heapq
import ast

# node of the huffman tree
class node:
    def __init__(self, prob, symbol, left=None, right=None):
        self.prob = prob

        self.symbol = symbol

        self.left = left

        self.right = right

        # gets values 0 or 1
        self.huff = ''

    def __lt__(self, nxt):
        return self.prob < nxt.prob

codes = dict()

# return huffman codes
def all_nodes(node, val=''):

    # read current node huffman code
    new_val = val + str(node.huff)
    
    # if it is not a leaf node continue on the next until we reach leaf node
    if(node.left):
        all_nodes(node.left, new_val)
    if(node.right):
        all_nodes(node.right, new_val)

    # if we find a leaf node print its huffman code
    if(not node.left and not node.right):
        codes[node.symbol] = new_val

    return codes


# creates huffman tree 
# takes a dictionary as a parameter, which contains all the unique symbols with their frequency values 
def encode(probabilities):
    
    nodes=[]

    # push data into a heap
    for x in range(len(probabilities)):
        heapq.heappush(nodes, node(probabilities[list(probabilities.keys())[x]], list(probabilities.keys())[x]))

    # create huffman tree with given data
    while len(nodes)>1:
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)

        left.huff = 0
        right.huff = 1 

        # connect the 2 smallest nodes
        new_node = node(left.prob + right.prob, left.symbol+right.symbol, left, right)

        heapq.heappush(nodes, new_node)
        
    return all_nodes(nodes[0])


def decoder(bitstring):
    # making a list with the bitstring and the huffman codes of each image-error
    list_img_diff = []
    data = [x.split(' | ') for x in str(bitstring).split(' - ')]
    
    # recreate error-image
    for i in range(len(data)):

        img_diff = []
        j = 0

        huffman_bitstring = data[i][0]
        param_dict = data[i][1] 
        current_bitstring = ''
        
        # convert string of parameters to dictionary
        param_dict = ast.literal_eval(param_dict)

        while j < len(data[i][0]):
            
            if current_bitstring in param_dict.values():
                img_diff.append(list(param_dict.keys())[list(param_dict.values()).index(current_bitstring)])
                current_bitstring = ''
            else:
                current_bitstring = current_bitstring + huffman_bitstring[j]
                j = j + 1

        img_diff.append(0)
        list_img_diff.append(img_diff)
        
    return list_img_diff
