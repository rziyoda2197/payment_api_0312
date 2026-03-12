# Payment Simulation API

Flask + SQLite asosida oddiy payment tizimi.

## Install
pip install -r requirements.txt

## Run
python app.py

## Endpoints

POST /users
GET /users
POST /transfer
GET /transactions

## Transfer body

{
  "sender_id": 1,
  "receiver_id": 2,
  "amount": 50
}
