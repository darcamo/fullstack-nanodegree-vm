#
# Database access functions for the web forum.
#

import time
import psycopg2

# Database connection
#DB = []


# Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    try:
        DB = psycopg2.connect("dbname=forum")
    except:
        print("I'm unable to connect to the database")

    cur = DB.cursor()
    QUERY = "select content, time from posts order by time desc"
    cur.execute(QUERY)
    raw_posts = cur.fetchall()
    DB.close()

    posts = [{'content': str(row[0]), 'time': str(row[1])}
             for row in raw_posts]

    # posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    # posts.sort(key=lambda row: row['time'], reverse=True)
    return posts


# Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    # t = time.strftime('%c', time.localtime())

    try:
        DB = psycopg2.connect("dbname=forum")
    except:
        print("I'm unable to connect to the database")

    cur = DB.cursor()

    # Note that you are not addind the time value. That is because the tame
    # has a default value for the time column, which is "now()".
    INSERT = "insert into posts (content) values (%s)"
    # Note that replace "%s" with content will be done by the execute
    # function. It will also sanitize the content. That is "Curing Bobby
    # Tables"
    cur.execute(INSERT, (content,)) # Note that we pass a tuple. Thus the
                                    # comma after content.
    print(INSERT)
    DB.commit()
    DB.close()

    # DB.append((t, content))


# if __name__ == '__main__':
#     #AddPost('lalala')
#     posts = GetAllPosts()
#     print(posts)
#     pass
