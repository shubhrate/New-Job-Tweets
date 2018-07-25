from secrets import get_secret

{ 
    'consumer_key': get_secret('TWITTER_CONSUMER_KEY'),
    'consumer_secret': get_secret('TWITTER_CONSUMER_SECRET'),
    'access_token_key': get_secret('TWITTER_ACCESS_TOKEN_KEY'),
    'access_token_secret': get_secret('TWITTER_ACCESS_TOKEN_SECRET') 
}
