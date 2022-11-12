import pymongo
from constants import *



myclient = pymongo.MongoClient(CONNECTION_STR)
## will create this db if it does not exists
mydb = myclient['lab4']

## will create these collections if they do not exist
blogs = mydb['blogs']
posts = mydb['posts']
comments = mydb['comments']


while True:
    
    input_str = input("Enter command(exit or quit to close application): ")

    if input_str.lower() == EXIT or input_str.lower() == QUIT:
            break
    
    

