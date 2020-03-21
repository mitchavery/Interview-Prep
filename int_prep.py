from collections import OrderedDict

list_1 = [1, 2, 3, 4, 5, 6, 7]
list_2 = [3, 7, 2, 1, 4, 6]


# Takes in 2 int lists and finds the missing element between them 
def FindMissingElement(list_1, list_2):
    tracker = {}
    tracker2 = {}
    ans = None
    count = 1

    for num in list_1:
        if num not in tracker.keys():
            tracker[num] = count
        else: 
            tracker[num] += 1
    for num2 in list_2:
        if num2 not in tracker2:
            tracker2[num2] = count
        else: 
            tracker2[num] += 1

    for keys in tracker.keys():
        for keys2 in tracker2.keys():
            if (keys == keys2 and (tracker[keys] != tracker2[keys])) or keys not in tracker2.keys():
                ans = keys
    print(ans)

# FindMissingElement(list_1, list_2)

def maxSlidingWindow(nums, k):
    s = []
    for elem in range(len(nums)-(k -1)):
        window = nums[elem: elem + k]
        total = sum(window)
        s.append(total)
    return max(s)

def LargestContSum(input_list):

    if len(input_list) == 0:
        return 0
    max_sum = current_sum = input_list[0]

    for num in input_list[1:]:
        current_sum = max(current_sum + num, num)
        max_sum = max(current_sum, max_sum)

    print(max_sum)


def largestContSum(input_list):
    if len(input_list) == 0:
        return 0
    max_sum = current = 0
    for num in input_list:
        current = max(current + num, num)
        max_sum = max(current, max)
    return max

# LargestContSum([1, 34, 5, -234, 523, 432, 3, -23, 34234])

def ReverseSent(input_sent):
    ans = ''
    stack = []
    if len(input_sent) == 1:
        ans = input_sent
    for char in input_sent.strip():
        stack.append(char)
    while stack:
        ans += stack.pop()
    print(ans)
# ReverseSent("  best the is This  ")

# takes in a string and compresses it to number of times character appears in string
def StringCompression(input_string):
    output_string = ''
    count = 1
    chars = {}

    for letter in input_string:
        if letter not in chars.keys():
            chars[letter] = count
        else: 
            chars[letter] += 1

    for keys, values in chars.items():
        output_string += keys + str(values) 

    print(output_string)

# StringCompression("AAB")

# Returns True if all characters are unique, false if not 
def UniqueChars(input_string):
    d = OrderedDict()
    count = 1
    for element in input_string:
        if element not in d.keys():
            d[element] = count
        else:
            d[element] +=1
    for values in d.values():
        if values != 1:
            return False
    return True

def UniqueChars2(input_string):
    chars = set()

    for let in input_string:
        if let not in chars:
            chars.add(let)
        else:
            return False
    return True

# print(UniqueChars2("mitchaverh"))

class Node:

    def __init__(self, data):
        self.data = data
        self.next = None
    
class LinkedList:
    
    def __init__(self):
        self.head = None
        self.tail = None
        
    def reverse(self):
        prev = None
        current = self.head
        while current:
            next = current.next
            current.next = prev
            prev = current 
            current = next 
        self.head = prev

    def pushToHead(self, new_data):
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node
    
    def pushToTail(self, new_data):
        new_node = Node(new_data)
        new_node.next = None
        self.tail.next = new_node
        self.tail = new_node
    
    def printList(self):
        temp = self.head
        while(temp):
            print (temp.data)
            temp = temp.next
"""
LinkedList = LinkedList()
LinkedList.push(20)
LinkedList.push(30)
LinkedList.push(40)
LinkedList.push(85)

LinkedList.printList()
LinkedList.reverse()
print('-' * 80)
LinkedList.printList()
"""


# last in first out stack 
class Stack(object):

    def __init__(self):
        self.items = []
    
    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peak(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)



def secondhigest(input_list):
        first = second = 0
        for elem in input_list:
            if elem > first:
                second = first
                first = elem
            elif second > first and second !=first:
                second = elem
        return second
        

        

stack = Stack()
stack.push(20)
stack.push(34)
stack.push(38)
# print(stack.isEmpty())


# first in first our queue
# first in first out
# FIFO 
class Queue(object):

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def deque(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)

# double ended queue can be added to front/rear, removed front/year
class Deque(object):

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def addFront(self, item):
        self.items.insert(0, item)
    
    def addRear(self, item):
        self.items.append(item)

    def removeFront(self):
        return self.items.pop()

    def removeRear(self):
        return self.items.pop(0)


def balanceParanthesis(input_string):
    if len(input_string) % 2 != 0:
        return False
    opening = set('([{')
    matches = set([('(', ')'), ('[', ']'), ('{', '}')])
    stack = []
    for elem in input_string:
        if elem in opening:
            stack.append(elem)
        else:
            if len(stack) == 0:
                return False
            last_elem = stack.pop()
            if (last_elem, elem) not in matches:
                return False
    return len(stack) == 0

# print(balanceParanthesis('[{}]'))

# implement a queue with 2 stacks
class Queue2Stacks(object):

    def __init__(self):
        self.in_stack = []
        self.out_stack = []
    
    def enqueue(self, element):
        self.in_stack.append(element)
    
    def dequeue(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
        return self.out_stack.pop()

class Node(object):

    def __init__(self, data):
        self.data = data
        self.next = None

# returns boolean if linkedlist contains a cycle
def cycle_check(node):
    marker1  = node
    marker2 = node
    while marker2 != None and marker2.next != None:
        marker1 = marker1.next
        marker2 = marker2.next.next
        if marker1 == marker2:
            return True
    return False

def reverse_linkedlist(head):
    prev = None
    next = None
    current = head
    while current:
        next = current.next
        current.next = prev
        prev = current
        current = next
    head = prev
    return head

def returnNthtoLastNode(node, head):
    pointer_left = head
    pointer_right = head

    for i in range(node-1):
        if not pointer_right.next:
            raise LookupError('Error')
        pointer_right = pointer_right.next
    while pointer_right.next:
        pointer_left = pointer_left.next
        pointer_right = pointer_right.next
    return pointer_left

# implement a stack with a linked list:
class Stack(object):

    def __init__(self):
        self.head = None

    def isEmpty(self):
        if not self.head:
            return False
        return True

    def push(self, data):
        if self.head is None:
            self.head = Node(data)
        else:
            new_node = Node(data)
            new_node.next = self.head
            self.head = new_node
    
    def pop(self):
        if self.isEmpty():
            return None
        else:
            pop_elem = self.head.data
            self.head = self.head.next
            return pop_elem

# implement a queue with a linkedlist
class Queue: 
      
    def __init__(self): 
        self.front = None
        self.rear = None
  
    def isEmpty(self): 
        return self.front == None
      
    # Method to add an item to the queue 
    def EnQueue(self, item): 
        temp = Node(item) 
        if self.rear == None: 
            self.front = self.rear = temp 
            return
        self.rear.next = temp 
        self.rear = temp 
  
    # Method to remove an item from queue 
    def DeQueue(self): 
        if self.isEmpty(): 
            return None 
        temp = self.front 
        self.front = temp.next
        if self.front == None: 
            self.rear = None
        return str(temp.data) 

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



l = [2, 3, 4, 10, 40]
# binarySearch(l,  0, len(l)-1, 4)

def factorial(n):
    if n < 1:
        return 1
    else:
        return n * factorial(n-1)



def CumSum(input_int):
    if input_int == 0:
        return 0
    else:
        return input_int + CumSum(input_int -1)

# print(CumSum(4))

# returns sum of all digits in that function
def SumOfDigits(input_digit):
    if len(str(input_digit)) == 1:
        return input_digit
    else:
        return input_digit%10 + SumOfDigits(input_digit//10)
    

# print(SumOfDigits(132))

# Given a phrase, returns boolean if it can be split amongst list of words
def word_split(phrase, list_of_words, output = None):
    if output is None:
        output = [] 
    for word in list_of_words:
        if phrase.startswith(word):
            output.append(word)
            return word_split(phrase[len(word):], list_of_words, output)
    return output


# hello world
# dlrow olleh
def ReverseStringWithRecursion(input_string):
    # base case
    if len(input_string) == 1: return input_string
    # recursive case
    else: return ReverseStringWithRecursion(input_string[1:]) + input_string[0]

# print(ReverseStringWithRecursion('abc'))


def findPermutations(string):
    results = []    
    if len(string) == 1:
        results = [string]
    else:
        for char, let in enumerate(string):
            for perm in findPermutations(string[:char] + string[char+1:]):
                results += [let + perm]
    return results

#print(findPermutations('abc'))

def fibonaci(input_int):
    if input_int == 1 or input_int == 0:
        return input_int
    else: 
        return fibonaci(input_int-1) + fibonaci(input_int-2)


# print(fibonaci(10))
# returns the first and last index of an element in the array 

a_list = [0, 1, 2, 2, 2, 2, 2, 2, 5]
def getRange(arr, target, left, right):
    new_list = []
    if left > right:
        return False
    else:
        mid = (left + right) // 2
        if target == arr[mid]:
            return mid
        elif target > arr[mid]:
            return binarySearch(arr, mid+1, right, target)
        else: 
            return binarySearch(arr, left, mid-1, target)


# print("First element: " + str(getRange(a_list, 2, 0, len(a_list)-1)))

a_list_t = [0, 1, 2, 5]
def getRange(arr, target, left, right):
    new_list = []
    if left > right:
        return False
    else:
        mid = (left + right) // 2
        if target == arr[mid]:
            return mid
        elif target > arr[mid]:
            arr2 = arr[::-1]
            return binarySearch(arr2, mid+1, right, target)
        else: 
            arr2 = arr[::-1]
            return binarySearch(arr2, left, mid-1, target)

a_list_t = a_list_t[::-1]
# print("last_elent: " + str((len(a_list_t)-1) - getRange(a_list_t, 2, 0, len(a_list_t)-1)))
# print(a_list_t)

def GetFirstAndLastIndex(arr, target):
    values = OrderedDict()
    return_list = []
    index_base = ''
    for index in range(len(arr)):
        key = arr[index]
        if key not in values:
            values[key] = str(index)
        else:
            values[key] += str(index)
    for keys in values.keys():
        if keys == target:
            one = values[keys][0]
            two = values[keys][-1]
            return_list.append(int(one))
            return_list.append(int(two))
    return return_list
test_list = [1, 2, 3, 3, 3, 3, 3, 3, 4, 5, 3, 7]

print(GetFirstAndLastIndex(test_list, 3))

def firstandlastindex(arr, target):
    