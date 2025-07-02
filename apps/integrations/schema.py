import graphene
import requests
import uuid
from graphql_jwt.decorators import login_required
from decouple import config

JSONRPC_URL = config('JSONRPC_URL')


class SubmitTransaction(graphene.Mutation):
    class Arguments:
        recipient = graphene.String(required=True)
        amount = graphene.Int(required=True)
        timestamp = graphene.Float(required=True)
        signature = graphene.String(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, recipient, amount, timestamp, signature):
        user = info.context.user

        if not user.public_key:
            return SubmitTransaction(ok=False, message="You must generate a keypair first.")

        tx = {
            "sender": user.public_key,
            "recipient": recipient,
            "amount": amount,
            "timestamp": int(timestamp),
            "signature": signature
        }

        try:
            res = requests.post(JSONRPC_URL, json={
                "jsonrpc": "2.0",
                "method": "submitTransaction",
                "params": tx,
                "id": str(uuid.uuid4())
            })
            data = res.json()

            if "error" in data:
                return SubmitTransaction(ok=False, message=data["error"].get("message", "Unknown error"))
            
            elif "result" in data:
                return SubmitTransaction(ok=True, message=data["result"])
            
            else:
                return SubmitTransaction(ok=False, message="Unexpected response from node")

        except Exception as e:
            return SubmitTransaction(ok=False, message=str(e))


class BlockType(graphene.ObjectType):
    index = graphene.Int()
    timestamp = graphene.Float()
    prev_hash = graphene.String()
    hash = graphene.String()
    nonce = graphene.Int()
    transactions = graphene.List(graphene.String)


class MineBlock(graphene.Mutation):
    class Arguments:
        pass

    ok = graphene.Boolean()
    block = graphene.Field(BlockType)

    @login_required
    def mutate(self, info):
        res = requests.post(JSONRPC_URL, json={
            "jsonrpc": "2.0",
            "method": "mineBlock",
            "params": [],
            "id": f"{uuid.uuid4()}"
        })

        if res.status_code == 200:
            return MineBlock(ok=True, block=res.json().get("result"))
        
        else:
            return MineBlock(ok=False, block=None)

class KeypairType(graphene.ObjectType):
    public_key = graphene.String()
    private_key = graphene.String()
    

class ChainValidationResultType(graphene.ObjectType):
    ok = graphene.Boolean()
    valid = graphene.Boolean()
    message = graphene.String()


class Query(graphene.ObjectType):
    latest_block = graphene.Field(BlockType)
    all_blocks = graphene.JSONString()
    generate_keypair = graphene.Field(KeypairType)
    validate_chain = graphene.Field(ChainValidationResultType)

    @login_required
    def resolve_latest_block(self, info):
        res = requests.post(JSONRPC_URL, json={
            "jsonrpc": "2.0",
            "method": "getLatestBlock",
            "params": [],
            "id": f"{uuid.uuid4()}"
        })

        return res.json().get("result")

    @login_required
    def resolve_all_blocks(self, info):
        res = requests.post(JSONRPC_URL, json={
            "jsonrpc": "2.0",
            "method": "getAllBlocks",
            "params": [],
            "id": f"{uuid.uuid4()}"
        })

        return res.json().get("result")

    @login_required
    def resolve_generate_keypair(self, info):
        user = info.context.user

        if user.public_key:
            raise Exception("Keypair already exists for this user.")

        res = requests.post(JSONRPC_URL, json={
            "jsonrpc": "2.0",
            "method": "generateKeypair",
            "params": [],
            "id": f"{uuid.uuid4()}"
        })
        data = res.json().get("result", {})
        user.public_key = data.get("publicKey")

        user.save(update_fields=["public_key"])

        return KeypairType(public_key=data.get("publicKey"),
                           private_key=data.get("privateKey"))
    
    @login_required
    def resolve_validate_chain(self, info):
        res = requests.post(JSONRPC_URL, json={
            "jsonrpc": "2.0",
            "method": "validateChain",
            "params": [],
            "id": f"{uuid.uuid4()}"
        })
        result = res.json().get("result", {})

        return ChainValidationResultType(ok=True,
                                         valid=result.get("valid", False),
                                         message=result.get("message", "No message"))


class Mutation(graphene.ObjectType):
    submit_transaction = SubmitTransaction.Field()
    mine_block = MineBlock.Field()
