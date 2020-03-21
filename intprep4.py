from collections import OrderedDict


def listsubset(arr1, arr2):
    values_arr2 = {}
    for elem in arr2:
        values_arr2[elem] = True
    for elem1 in arr1:
        if elem1 not in values_arr2.keys() or not values_arr2[elem]:
            return False
    return True


l = [1, 2]
l2 = [1, 2, 3]

# print(listsubset(l, l2))


def findDuplicate(input_list):
    values = {}
    ans = []
    count = 1
    for elem in input_list:
        if elem not in values:
            values[elem] = count
        else: 
            values[elem] += 1
    for keys in values.keys():
        if values[keys] == 2:
            ans.append(keys)
    return ans


l = [4, 3, 2, 4, 1, 3, 2]
print('Find dup: ' + str(findDuplicate(l)))


def depthFirstSearch(graph, start):
    visited = set()
    stack = [start]

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited

# Given 2 dimensional array find where first column is product ID, second is sales, find total sales for eacj product id


def getTotalSales(two_d_arrayy):

    sales = OrderedDict()

    for i in range(len(two_d_arrayy)):
        product = two_d_arrayy[i][0]
        quantity = two_d_arrayy[i][1]

        if product not in sales:
            sales[product] = quantity
        else:
            sales[product] += quantity

#removes all even numbers from a stack


def removeEvenNumbersFromStack(stack):
    new_stack = []
    new_stack_2 = []
    while stack:
        elem = stack.pop()
        if elem % 2 != 0:
            new_stack.append(elem)
        else:
            new_stack_2.append(elem)
    while new_stack:
        stack.append(new_stack.pop())


first_stack = [1, 2, 4, 5, 6, 6, 9]
removeEvenNumbersFromStack(first_stack)
# print(first_stack)


def binarySearch(arr, target):
    mid = len(arr) // 2
    if mid == target:
        return mid
    elif arr[mid] > target:
        return binarySearch(arr[mid:], target)
    else:
        return binarySearch(arr[:mid], target)


graph = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}


def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for next in graph[start] - visited:
        dfs(graph, next, visited)
    return visited


def reverseList(node):
    next = None
    prev = None
    current = node
    while current:
        next = current.next
        curren.next = prev
        prev = current
        current = next
    prev = node
    return prev


def dfs2(node, x):
    if not node:
        return False
    elif node.data == x:
        return True


prices = [12, 11, 15, 3, 10]


def returnMaxProfit(input_list):
    min_stock = input_list[0]
    max_profit = 0
    for price in input_list:
        min_stock = min(min_stock, price)
        compare_profit = price - min_stock
        max_profit = max(max_profit, compare_profit)
    return max_profit


def CheckRectanglesOverlap(rect1, rect2):
    if rect1.left > rect2.right or rect1.right < rect2.left:
        return False
    if rect1.top < rect2.bottom or rect2.bottom > rect2.top:
        return False


# multiplies 2 string together and returns string product without using int() cast
def multiply(num1, num2):
    values = OrderedDict()
    for elem in range(10):
        values[str(elem)] = elem
    num1_new = None
    num2_new = None
    for char in num1:
        if num1_new is None:
            num1_new = values[char]
        else:
            num1_new = num1_new*10+values[char]
    for char in num2:
        if num2_new is None:
            num2_new = values[char]
        else:
            num2_new = num2_new*10+values[char]
    return num1_new * num2_new

# print(multiply('1234', '4567'))


def profitFromStocksBruteForce(input_list):
    max = 0
    for elem in range(len(input_list)-1):
        for elem2 in range(elem+1, elem+2):
            value = input_list[elem2] - input_list[elem]
            if value > max:
                max = value
    return max


stocks = [10, 11, 12, 3, 9]

# print(profitFromStocksBruteForce(stocks))


def productOfAllInts(input_list):
    return_list = []
    for index in range(len(input_list)):
        for index2 in range(len(input_list)):
            prod = 1
            prod *= input_list[index] * input_list[index2]
            print(prod)
            print('-------')
    return return_list


l = [1, 2, 3, 4, 5]

# validates a binary search treec


class Node:
    def __init__(self, value=None):
        self.value = value(int)
        self.left_child = None
        self.right_child = None

    def validateBST(self, node):
        if node is None:
            return True
        if node.left_child > node.value:
            return False
        if node.right_child < node.value:
            return False
        return validateBST(node.left_child) and validateBST(node.right_child)

    def Search(self, node, desired_value):
        if node.value == desired_value:  # Base Case
            return True
        if node.left and Search(node.left, desired_value):  # Subpart
            return True
        if node.right and Search(node.right, desired_value):  # Subpart
            return True
        return False

    def insertIntoBST(self, root, node):
        if root is None:
            root = node
        else:
            if root.value < node.value:
                if root.right_child is None:
                    root.right_child = node
                else:
                    insertIntoBST(root.right_child, node)
            else:
                if root.left_child is None:
                    root.left_child = node
                else:
                    insertIntoBST(root.left_child, node)


def nthfiboacinum(num):
    if num == 1 or num == 0:
        return num
    else:
        return nthfiboacinum(num-1) + nthfiboacinum(num-2)


def reverseWithRecursion(input_string):
    if len(input_string) <= 1:
        return input_string
    else:
        return reverseWithRecursion(input_string[1:] + input_string[0])


# 9

# check everything from 0 -4
# if that number squared equals num
# return True
# also check if that element square is less than inputnum, return one less

def findSquareRoot(input_num):
    if input_num == 1:
        return True
    for elem in range(1+(input_num//2)):
        if elem*elem == input_num:
            return elem
        elif elem*elem > input_num:
            return elem - 1

# print(9//2)

# print(findSquareRoot(121))


def binarySearch(input_string, left, right, target):
    if left > right:
        return False
    else:
        mid = (left + right) // 2
        if target == input_string[mid]:
            return mid
        elif target > input_string[mid]:
            return binarySearch(input_string, mid+1, right, target)
        else:
            return binarySearch(input_string, left, mid-1, target)


# binary search runs in O(logn) average, O(1) best when target is mid
def binarySearch(input_list, left, right, target):
    if left > right:
        return False
    else:
        mid = (left + right) // 2
        if input_list[mid] == target:
            return True
        elif input_list[mid] > target:
            return binarySearch(input_list, mid+1, right, target)
        else:
            return binarySearch(input_list, left, mid-1, target)


list1 = [1, 2, 234, 23, 4]


# input = "this is a sentence"
# ouput = "sentence a is this"
def reverseSentence(input_setence):
    l = input_setence.split()
    new_word = ''
    stack = []
    for word in l:
        stack.append(word)
    while stack:
        new_word += " " + stack.pop()
    return new_word


def findMaxProductOf3Ints(input_list):
    if len(input_list) < 3:
        return
    input_list = sorted(input_list)
    a = input_list[0] * input_list[1] * input_list[-1]
    b = input_list[-3] * input_list[-2] * input_list[-1]
    return max(a, b)


class Node:
    def __init__(self, val=None):
        self.val = None
        self.left = None
        self.right = None

    def validateBST(root):
        if root is None:
            return True
        if root.left > root.val:
            return False
        if root.right < root.val:
            return False
        return validateBST(root.left) and validateBST(root.right)


def removedupsfromstring(input_string):
    result = []
    seen = []
    for char in input_string:
        if char not in seen:
            seen.append(char)
            result.append(char)
    return "".join(result)


# print(removedupsfromstring('tree traversal'))


def findUniqueInt(input_list):
    values = {}
    count = 1
    for num in input_list:
        if num not in values:
            values[num] = count
        else:
            values[num] += 1
    for keys in values.keys():
        if values[keys] == 1:
            return keys

# print(findUniqueInt([1, 1, 2, 3, 2, 3, 4]))


# returns the most frequent number in an array
def findMostFrequentInt(input_list):
    values = OrderedDict()
    count = 1
    for num in input_list:
        if num not in values:
            values[num] = count
        else:
            values[num] += 1
    max = 0
    key = 0
    for keys, values in values.items():
        if values > max:
            max = values
            key = keys
    return key

listints = [1, 2, 3, 4]

# print(findMostFrequentInt(listints))

def isPalindromeInt(input_int):
    s = str(input_int)
    if len(s) == 1:
        return True
    stack = []
    for char in s: 
        stack.append(char)
    input_int_string = ''.join(reversed(stack))
    return int(input_int_string) == input_int

def isZero(n):
    return n == 0

def add(n, m):
    if isZero(m):
        return n
    return add(n, m-1) + 1



def mult(a, b):
    ans = 0
    for i in range(b):
        ans += a
    return ans

def mult(a, b):
    if b == 1:
       return a
    else:
        return a+mult(a, b-1)


def exp(x):
    if x == 0:
        return (x+1)
    else:
        return exp(x-1) * 2


print(exp(5))


def fibonaci(input_int):
    if input_int == 1 or input_int == 0:
        return input_int
    else:
        return fibonaci(input_int-1) + fibonaci(input_int-2)


def choose(n, k):
    if k == 0:
        return 1
    elif n<k:
        return 0
    else:
        return choose(n-1, k-1) + choose(n-1, k)

# print(choose(3, 2))

def runlengthalg(input_string):
    d = {}
    count = 1
    ans =''
    for char in input_string:
        if char not in d:
            d[char] = count
        else: 
            d[char] += count
    for keys, values in d.items():
        ans += keys + str(values)
    return ans


# print(runlengthalg("wwwwaaadexxxxxx"))


def findDups(input_list):
    seen = []
    for elem in input_list:
        if elem not in seen: 
            seen.append(elem)
        else: 
            return elem
        