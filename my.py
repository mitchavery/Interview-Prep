import random as r

class Prime(object):

    def isPrime(self, n):
        if n == 1 or n == 0:
            return False
        for i in range(2, n):
            if (n % i) == 0:
                return False
        return True

# print(isPrime(13))


def toHex(num):
    return hex(num)[2:]


# print(toHex(123))


def multiply(str1, str2):
    nums = {}
    for elem in range(10):
        nums[str(elem)] = elem
    num1 = num2 = 0
    for char in str1:
        num1 = num1 * 10 + nums[char]
    for char in str2:
        num2 = num2 * 10 + nums[char]
    return str(num1 * num2)

# print(multiply('3', '3'))


P = Prime()


def findPrimes(num):
    ans = []
    for elem in range(num):
        if P.isPrime(elem):
            ans.append(elem)
    return ans

# print(findPrimes(14))


def decompresslist(nums):
        res = []
        windows = []
        for elem in range(0, len(nums)-1, 2):
            window = nums[elem: elem + 2]
            for elem in range(window[0]):
                res.append(window[1])      
        return res

# print(decompresslist([1, 2, 3, 4]))

def compress(chars):
        res = []
        d = {}
        count = 1
        for char in chars: 
            if char not in d:
                d[char] = count
            else:
                d[char] += count
        for keys, values in d.items():
            if len(str(values)) < 2:
                res.append(keys)
                res.append(str(values))
            else:
                res.append(keys)
                for elem in str(values):
                    res.append(elem)
        return res
        
# print(compress(["a","a","b","b","c","c","c"]))


def capitalize(text):
    new = ''
    for char in text:
        bit = r.randrange(0, 10)
        if bit == 1:
            new += char.upper()
        else:
            new += char.lower()     
    return new

print(capitalize('WHATS GOING ON HERE'))