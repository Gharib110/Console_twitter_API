import oauth2
import urllib.parse as urlparse
import CONSTANTS
import json
from User_DB import User

consumer = oauth2.Consumer(CONSTANTS.Consumer_key,CONSTANTS.Consumer_Secret)

user_firstname = input('What is your firstname ? \n')
user_lastanme = input('What is your lastname ? \n')
user_email = input('Please enter your email : \n')
user = User.loading_from_DB(email=user_email)

if user is None:
    client = oauth2.Client(consumer)
    response, content = client.request(CONSTANTS.Request_Token_url, 'POST')

    if response.status != 200:
        print("there is some thing wrong :(( ")
        print(response)

    else:

        request_token_callback = dict(urlparse.parse_qsl(content.decode('utf-8')))

        print("Please Go th the following website : ")
        print("{}?oauth_token={}".format(CONSTANTS.Authorization_url, request_token_callback['oauth_token']))

        oauth_verifier = int(input("what is the pin-code ? \n"))
        token = oauth2.Token(request_token_callback['oauth_token'], request_token_callback['oauth_token_secret'])
        token.set_verifier(oauth_verifier)

        client = oauth2.Client(consumer, token)
        response, content = client.request(CONSTANTS.Access_Token_url, 'POST')
        access_token_callback = dict(urlparse.parse_qsl(content.decode('utf-8')))

        user = User(None, user_firstname, user_lastanme, user_email, access_token_callback['oauth_token'], access_token_callback['oauth_token_secret'])
        user.saving_to_DB()

user.loading_from_DB(user_email)
authorized_token = oauth2.Token(user.oauth_token, user.oauth_token_secret)
authorized_client = oauth2.Client(consumer, authorized_token)

while True:

    user_title = input('What do you want to search about it ? \n')
    user_number = int(input('How many tweets do you want to see ? (MAX : 100) \n'))

    while user_number > 100:

        user_number = user_number - 1

    response, content = authorized_client.request("https://api.twitter.com/1.1/search/tweets.json?q={}&result_type=popular&count={}".format(user_title, user_number), 'GET')
    tweets = json.loads(content.decode('utf-8'))

    if response.status != 200:
        print('Something went wrong, Please try again')

    else:
        print('this the text & images : \n')
        for tweet in tweets['statuses']:
            print(tweet['text'])
            print('\n')

    ans = input("Do you want to exit ? (yes/no)\n")
    if ans == "no":
        break
    else:
        continue
