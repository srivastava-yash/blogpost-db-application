import pymongo
from constants import *
import re
import datetime


class main:

    def __init__(self):
        self.myclient = pymongo.MongoClient(CONNECTION_STR)
        ## will create this db if it does not exists
        self.mydb = self.myclient['lab4']

        ## will create these collections if they do not exist
        self.blogs = self.mydb['blogs']
        self.posts = self.mydb['posts']
        self.comments = self.mydb['comments']
    
    def make_post(self, blog_name, user_name, title, post_body, tags, timestamp):
        blogs_result = self.blogs.find_one({'name': blog_name})
        blog_id = None
        
        if blogs_result is None:
            blog_dict = {'name': blog_name}
            blog = self.blogs.insert_one(blog_dict)
            blog_id = blog.inserted_id
        
        if blog_id is None:
            blog_id = blogs_result['_id']
        
        tags_list = tags.split(',')
        permalink  = blog_name+'.'+re.sub('[^0-9a-zA-Z]+', '_', title)
        post_dict = {
            'title': title,
            'author': user_name,
            'blog': blog_id,
            'permalink': permalink,
            'body': post_body,
            'tags': tags_list,
            'created_at': timestamp,
            'active': 1
        }
        post = self.posts.insert_one(post_dict)

        return title
    
    def add_comment(self, blog_name, permalink, user_name, comment_body, timestamp):

        post = self.posts.find_one({'permalink': permalink})
        blog = self.blogs.find_one({'name': blog_name})

        if post is None or blog is None:
            return ""
        
        comment_dict = {
            'blog': blog['_id'],
            'post': post['_id'],
            'permalink': datetime.datetime.now(),
            'user': user_name,
            'body': comment_body,
            'active': 1
        }
        comment = self.comments.insert_one(comment_dict)

        return f"Comment to {post['title']} added by {user_name}"
    

    def delete_post_comment(self, blog_name, permalink, user_name, timestamp):
        post = self.posts.find_one({'permalink': permalink})
        comment = self.comments.find_one({'permalink': permalink})

        post_query = {'permalink': permalink}
        post_new_values = {'$set': {'active': 0, 'timestamp': datetime.datetime.now()}}
        self.posts.update_one(post_query, post_new_values)
        
        comment_query = {'permalink': permalink}
        comment_new_values = {'$set': {'active': 0, 'timestamp': datetime.datetime.now()}}
        self.comments.update_one(comment_query, comment_new_values)

        if post is None and comment is None:
            return "No Post and Comment found with this permalink"
        
        if comment is None:
            return f"Post deleted by user: {user_name} \nNo comment found with this permalink"
        
        if post is None:
            return f"Comment deleted by user: {user_name} \nNo Post found with this permalink"
        
        return f"Post and Comment deleted by user: {user_name}"
    
    def get_post_comment_str(self, posts):
        blog_str = ""
        blog_str += "Posts:\n"
        for post in posts:
            permalink = post['permalink']
            blog_str += f"Title: {post['title']}\n"
            blog_str += f"username: {post['author']}\n"
            if len(post['tags']) > 0:
                blog_str += f"tags: {post['tags']}\n"
            blog_str += f"timestamp: {post['created_at']}\n"
            blog_str += f"permalink: {post['permalink']}\n"
            blog_str += f"body:\n{post['body']}\n"
            blog_str += "-------\n"
            comments = self.comments.find({'post': post['_id'], 'active': 1})
            comments_clone = comments.clone()
            if(len(list(comments_clone))) > 0:
                blog_str += "Comments:\n"
            for comment in comments:
                blog_str += f"username: {comment['user']}\n"
                blog_str += f"permalink: {comment['permalink']}\n"
                blog_str += f"comment:\n{comment['body']}\n\n"
        
        return blog_str

    def show_blog(self, blog_name):
        blog = self.blogs.find_one({'name': blog_name})
        if blog is None:
            return "No blog found"
        blog_id = blog['_id']
        posts = self.posts.find({'blog': blog_id, 'active': 1})

        return self.get_post_comment_str(posts)


    def find_blog(self, blog_name, search_str):
        blog = self.blogs.find_one({'name': blog_name})
        
        if blog is None:
            return "No blog found"
        
        blog_id = blog['_id']

        posts = self.posts.find({'blog': blog_id, 'active': 1})
        matching_posts = list()

        for post in posts:
            found = False
            if post['body'].find(search_str) != -1:
                matching_posts.append(post)
                found = True
            if found:
                continue
            for tag in post['tags']:
                if tag.find(search_str) != -1:
                    matching_posts.append(post)
                    found = True
                    break
            if found:
                continue
            comments = self.comments.find({'post': post['_id'], 'active': 1})
            for comment in comments:
                if comment['body'].find(search_str) != search_str:
                    matching_posts.append(post)
                    break
        
        return self.get_post_comment_str(matching_posts)
            
            

def get_input_array(input_str):
    command = input_str.split(' ')[0]
    current_str = ""
    is_open = False
    start_index = input_str.find("\"")
    input_arr = list()
    input_arr.append(command)
    for idx in range(start_index, len(input_str)):
        if is_open and input_str[idx] == '"':
            input_arr.append(current_str)
            is_open = False
            current_str = ""

        elif is_open is False and input_str[idx] == '"':
            is_open = True
        
        if is_open and input_str[idx] != '"':
            current_str += str(input_str[idx])
    
    return input_arr


if __name__ == "__main__":
    db = main()
    while True:
        input_str = input("Enter command(exit or quit to close application): ")

        if input_str.lower() == EXIT or input_str.lower() == QUIT:
                break
        
        input_arr = get_input_array(input_str)

        if input_arr[0] == POST:
            if len(input_arr) != 7:
                print(INVALID_COMMAND)
            else:
                output = db.make_post(input_arr[1], input_arr[2], input_arr[3], input_arr[4], input_arr[5], input_arr[6])
                if output == "":
                    print("Error while saving post / try again")
                else:
                    print(f"{output} posted successfully")
        
        elif input_arr[0] == COMMENT:
            if len(input_arr) != 6:
                print(INVALID_COMMAND)
            else:
                output = db.add_comment(input_arr[1], input_arr[2], input_arr[3], input_arr[4], input_arr[5])
                if output == "":
                    print("Error while adding the comment / Try again")
                else:
                    print(output)
        
        elif input_arr[0] == DELETE:
            if len(input_arr) != 5:
                print(INVALID_COMMAND)
            else:
                print(db.delete_post_comment(input_arr[1], input_arr[2], input_arr[3], input_arr[4]))
        
        elif input_arr[0] == SHOW:
            if len(input_arr) != 2:
                print(INVALID_COMMAND)
            else:
                print(db.show_blog(input_arr[1]))
        
        elif input_arr[0] == FIND:
            if len(input_arr) != 3:
                print(INVALID_COMMAND)
            else:
                print(db.find_blog(input_arr[1], input_arr[2]))
        
        else:
            print(INVALID_COMMAND)


