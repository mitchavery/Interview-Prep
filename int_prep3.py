
# Implement trees like this 

class BinaryTree(object):

    def __init__(self, root):
        self.key = root
        self.leftChild = None
        self.rightChild = None
    
    def insertLeft(self, new_node):
        # No existing left child, add a node to the tree
        if self.leftChild == None:
            self.leftChild = BinaryTree(new_node)
        # Left child is existing, push existing one down 1 level
        else:
            # create temp binary tree and push down 1 level
            t = BinaryTree(new_node)
            t.leftChild = self.leftChild
            self.leftChild = t

    def insertRight(self, new_node):
        if self.rightChild == None:
            self.rightChild = new_node
        else:
            t = BinaryTree(new_node)
            t.rightChild = self.rightChild
            self.rightChild = t

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setRoot(self, new_root):
        self.key = new_root
    
    def getRoot(self):
        return self.key

    def preorder(self):
        print(self.key)
        if self.leftChild:
            self.leftChild.preorder()
        if self.rightChild:
            self.rightChild.preorder()

def preorder(tree):
    if tree:
        print(tree.getRoot())
        preorder(tree.getLeftChild())
        preorder(tree.getRightChild())

def postorder(tree):
    if tree != None:
        postorder(tree.getLeftChild())
        postorder(tree.getRightChild())
        print(tree.getRoot)

def inorder(self):
    if tree != None:
        inorder(tree.getLeftChild())
        print(tree.getRoot())
        inorder(tree.getRightChild())


tree = BinaryTree('a')
# print(tree.getRoot())
# print(tree.getLeftChild())
tree.insertLeft('b')
tree.insertRight('c')
tree.insertRight('d')
# print(tree.getRightChild().getRoot())
# tree.preorder()


# binary search trees

# Sorting/Searching 

def seq_search(arr, element):
    for num in arr:
        if element == num:
            return True
    return False


def seq_search2(arr, elemt):
    pos = 0
    found = False
    while pos <len(arr) and not found:
        if arr[pos] == elemt:
            return True
        else: 
            pos +=1
    return found

# print(seq_search2([1, 4, 5, 5, 5, 3], 3))

def seq_search2(arr, elemt):
    pos = 0
    found = False
    stopped = False
    while pos <len(arr) and not found and not stopped:
        if arr[pos] == elemt:
            return True
        elif arr[pos] > elemt:
            stopped = True
        else: 
            pos +=1
    return found


# binary search only used on sorted arrays
def binarySearch(arr,  target):
    if len(arr) == 0:
        return False
    else:
        mid = len(arr)//2
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            return binarySearch(arr[mid:], target)
        else: 
            return binarySearch(arr[mid:], target)


def mergeSort(arr): 
    if len(arr) >1: 
        mid = len(arr)//2 #Finding the mid of the array 
        L = arr[:mid] # Dividing the array elements  
        R = arr[mid:] # into 2 halves 
        mergeSort(L) # Sorting the first half 
        mergeSort(R) # Sorting the second half 
        i = j = k = 0
        while i < len(L) and j < len(R): 
            if L[i] < R[j]: 
                arr[k] = L[i] 
                i+=1
            else: 
                arr[k] = R[j] 
                j+=1
            k+=1
        while i < len(L): 
            arr[k] = L[i] 
            i+=1
            k+=1
          
        while j < len(R): 
            arr[k] = R[j] 
            j+=1
            k+=1





def bubbleSort(arr):
    for i in range(len(arr)-1, 0, -1):
        for j in range(i):
            if arr[j] > arr[j+1]:
                temp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = temp
                
                
                

def selectionSort(arr):
    for i in range(len(arr)-1, 0, -1):
        pos_of_max = 0
        for j in range(1, i+1):
            if arr[j] > arr[pos_of_max]:
                pos_of_max = j
            
        temp = arr[i]
        arr[i] = arr[pos_of_max]
        arr[pos_of_max] = temp

# quick sort runs worst when already sorted, sorted in reverse, pivot is largest, pivot is smallest

def quickSort(arr):
    quickSortHelper(arr, 0, len(arr)-1)

def quickSortHelper(arr, first, last):
    if first < last:
        splitpoint = partition(arr, first, last)
        quickSortHelper(arr, first, splitpoint-1)
        quickSortHelper(arr, splitpoint +1, last)

def partition(arr, first, last):
    pass

def getSecondLargest(arr):
    first = second = 0
    if len(arr) <2:
        return None
    for elem in arr:
        if elem > first:
            second = first 
            first = elem
        elif elem > second and elem != first:
            second = elem
    return second



practice = [1, 3, 4, 10, 6, 2, 3, 9, 2, 8, 11,  9]

print(getSecondLargest(practice))

print(sum(practice)/len(practice))