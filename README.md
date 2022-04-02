# tiktok-telegram-bot
### Setup
Token is needed as environ

docker build --tag tt_bot .\
docker run -e token=TOKEN -e DB_URL=sqlite:////db/prod.db -v /home/ubuntu/db:/db tt_bot


### Migration
auto: $alembic revision --autogenerate -m "Added account table"\
manual: $alembic revision -m 'create migration'\
alembic upgrade head



export $(cat dev.env | xargs) && 