import graphene
import requests
from decouple import config

JSONRPC_URL = config('JSONRPC_URL')

class SubmitTransaction(graphene.Mutation):
    class Arguments:
        sender = graphene.String(required=True)
        recipient = graphene.String(required=True)
        amount = graphene.Int(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, sender, recipient, amount):
        tx = {"sender": sender, "recipient": recipient, "amount": amount}
        try:
            res = requests.post(JSONRPC_URL, json={
                "jsonrpc": "2.0",
                "method": "submitTransaction",
                "params": tx,
                "id": 1,
            })

            return SubmitTransaction(ok=True, message=res.json().get("result"))
        
        except Exception as e:
            return SubmitTransaction(ok=False, message=str(e))

class MineBlock(graphene.Mutation):
    ok = graphene.Boolean()
    block = graphene.JSONString()

    def mutate(self, info):
        res = requests.post(JSONRPC_URL, json={
            "jsonrpc": "2.0",
            "method": "mineBlock",
            "params": [],
            "id": 2,
        })

        return MineBlock(ok=True, block=res.json().get("result"))

class Query(graphene.ObjectType):
    latest_block = graphene.JSONString()
    all_blocks = graphene.JSONString()

    def resolve_latest_block(self, info):
        res = requests.post(JSONRPC_URL, json={
            "jsonrpc": "2.0",
            "method": "getLatestBlock",
            "params": [],
            "id": 3,
        })
        
        return res.json().get("result")
    
    def resolve_all_blocks(self, info):
        res = requests.post(JSONRPC_URL, json={
            "jsonrpc": "2.0",
            "method": "getAllBlocks",
            "params": [],
            "id": 4,
        })

        return res.json().get("result")

class Mutation(graphene.ObjectType):
    submit_transaction = SubmitTransaction.Field()
    mine_block = MineBlock.Field()
