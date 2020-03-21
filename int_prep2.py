from collections import OrderedDict
import unittest
a = [3, 34, 454, 123234, 4]


def RemoveDups(l):
    new_list = []
    d = OrderedDict()
    count = 1
    for element in l:
        if element in d.keys():
            d[element] += 1
        else:
            d[element] = count
    for keys, values in d.items():
        if values == 1:
            new_list.append(keys)
    return new_list


def isAnagram(s, t):
        if len(s) != len(t):
            return False
        values = {}
        count = 1
        for char in s:
            if char not in values:
                values[char] = count
            else:
                values[char] += 1
        for char in t:
            if char not in values:
                values[char] = count
            else:
                values[char] -= 1
        for k in values:
            if k != 0:
                return False

        return True


print(isAnagram('rat', 'car'))


def checkAnagram(s1, s2):
    s1 = s1.replace(' ', '')
    s2 = s2.replace(' ', '')

    if len(s1) != len(s2):
        return False
    count = {}
    for letter in s1:
        if letter in count:
            count[letter] += 1
        else:
            count[letter] = 1
    for letter in s2:
        if letter in count:
            count[letter] -= 1
        else:
            count[letter] = 1

    for k in count:
        if count[k] != 0:
            return False
    return True


def SortListOfChars(input_list):
    input_list.sort()
    return input_list


# print(SortListOfChars(['p', 'e', 'g']))


# print(checkAnagram("god", "dog"))

a = ["a", "c", "b"]

# bubble up the list and do exchanges along the way


def BubbleSort(alist):
    for j in range(len(alist)-1, 0, -1):
        for i in range(j):
            if alist[i] > alist[i+1]:
                temp = alist[i]
                alist[i] = alist[i+1]
                alist[i+1] = temp


def bubbleSort(arr):
    for i in range(len(arr)-1, 0, -1):
        for j in range(i):
            if arr[j] > arr[j+1]:
                temp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = temp


BubbleSort(a)
print(a)


def CheckPowerOfTwo(num):
    check = False
    if num == 0 or num == 1:
        return True
    i = 1
    while i <= num:
        if i == num:
            check = True
        i *= 2

    return check


def PairSum(input_list, sum):

    if len(input_list) < 2:
        return

    covered = []
    results = []
    # Use lists/sets to check if something exists or not or already covered
    for num in input_list:
        target = sum - num
        # Use this trick of doing sum - num for sum pair or product/num to get multiplication pair etc
        if target not in covered:
            covered.append(num)
        else:
            results.append((target, num))
    print(results)


def pairSum(input_list, sum):
    covered = []
    for elem in input_list:
        target = sum - elem
        if target not in covered:
            covered.append(elem)


def secondhighest(input_list):
    first = second = 0
    for elem in input_list:
        if elem > first:
            second = first
            first = elem
        elif elem > second and elem != first:
            second = elem
    return first, second


def PairMult(input_list, product):
    if len(input_list) < 2:
        return

    count = 0
    covered = []
    results = []

    for num in input_list:
        # For checking proudct / by
        target = product / num
        if target not in covered:
            covered.append(num)
        else:
            count += 1
            results.append((target, num))

    print(count)
    print(results)


def PairDiv(input_list, divisor):
    if len(input_list) < 2:
        return

    count = 0
    covered = []
    results = []

    for num in input_list:
        # For checking which pairs of numbers when divided in list = given number
        target = num / divisor
        if target in input_list:
            results.append((target, num))

    print(count)
    print(results)


def ReverseStringWithList(input_string):
    stack = []
    new_string = ''

    for char in input_string:
        stack.append(char)

    while stack:
        new_string += stack.pop()

    print(new_string)


def ReturnCommonChars(string_1, string_2):
    ans = ''
    seen = []
    if string_1 == string_2:
        return string_1

    for char in string_1:
            if char in string_2 and char not in seen:
                ans += " " + char
                seen.append(char)

    print(ans)


# ReturnCommonChars("aapples", "banpnnas")


# ReverseStringWithList("Mitchavery")

# PairDiv([1, 5, 25, 8, 9, 10, 3, 2], 5)

# reverses an array in place
def revereseIntsArray(arr):
    mid = len(arr) // 2
    for i in range(mid):
        otherside = len(arr) - 1 - i
        temp = arr[otherside]
        arr[otherside] = arr[i]
        arr[i] = temp
    return arr


def reverseinplace(arr):
    mid = len(arr) // 2
    for i in range(mid):
        end = len(arr) -1 -i
        temp = arr[end]
        arr[end] = arr[i]
        arr[i] = temp


l = [1, 5, 25, 8, 9, 10, 3, 2]

revereseIntsArray(l)
# print(l)

# Given two lists, write a program to determine if A is a subset of B


def listsubset(arr1, arr2):
    values_arr2 = {}
    for elem in arr2:
        values_arr2[elem] = True
    for elem in arr1:
        if elem not in values_arr2.keys() or values_arr2[elem] != True:
            return False


l = [1, 2]
l2 = [1, 2, 3]

# print(listsubset(l, l2))


def commonChars(input_string, input_string2):
    common = []
    for char in set(input_string):
        for char2 in set(input_string2):
            if char == char2:
                common.append(char)
    return common
