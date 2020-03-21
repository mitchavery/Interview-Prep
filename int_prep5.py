import mysql.connector
from collections import OrderedDict
import hashlib

class mysql_fun(object):

    def __init__(self):
        self.mysql = mysql.connector.connect(
            host="localhost", user="root", passwd="Saxdude135", database="python")
        self.hash = hashlib.new('ripemd160')
        self.questions = self.login = OrderedDict()
        self.questions['User'] = 'What is your user name: '
        self.questions['Password'] = 'What is your password: '

    def get_input(self):
        vals = []
        for elem, keys in self.questions.items():
            if elem == 'Password': 
                vals.append(hash(input(keys)))
            else: 
                vals.append(input(keys)) 
        return vals
    
    def get(self):
        mycursor = self.mysql.cursor()
        query = "SELECT * from users"
        mycursor.execute(query)
        r = mycursor.fetchall()
        for elem in r:
            print(elem)

    def insert(self, values):
        mycursor = self.mysql.cursor()
        sql = "INSERT INTO users VALUES (%s, %s)"
        mycursor.execute(sql, values)
        self.mysql.commit()

if __name__ == '__main__':
    mysql_ = mysql_fun()
    vals = mysql_.get_input()
    mysql_.insert(vals)
    mysql_.get()
    



