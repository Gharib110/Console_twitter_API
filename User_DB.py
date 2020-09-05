import psycopg2

class User:
    def __init__(self, id, firstname, lastname, email, oauth_token, oauth_token_secret):

        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

    def saving_to_DB(self):
        with psycopg2.connect(dbname="postgres",port="3310", user="postgres", password="", host="localhost") as conn:
            with conn.cursor() as cursor:
                cursor.execute("insert into public.twitterusers (firstname, lastname, email, oauth_token, oauth_token_secret) values ('%s', '%s', '%s', '%s', '%s')" %(self.firstname, self.lastname, self.email, self.oauth_token, self.oauth_token_secret))
                print("User add to the database")
    @classmethod
    def loading_from_DB(cls,email):
        with psycopg2.connect(dbname="postgres",port="3310", user="postgres", password="", host="localhost") as conn:
            with conn.cursor() as cursor:
                cursor.execute("select * from public.twitterusers where email='%s'" % (email))
                user_data = cursor.fetchone()
                try:
                    return cls(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5])
                except TypeError:
                    print("there is no something :((")

