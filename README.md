# tiktok-telegram-bot

cookie and token is needed as environ

docker build --tag tt_bot .
docker run -e token=TOKEN -e cookie="COOKIE" tt_bot
