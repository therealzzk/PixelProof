from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()  # 加载环境变量

# 初始化Web3
w3 = Web3(Web3.HTTPProvider(os.getenv("POLYGON_RPC")))
private_key = os.getenv("PRIVATE_KEY")
contract_address = os.getenv("CONTRACT_ADDRESS")

# 加载合约ABI
with open("contracts/abi.json") as f:
    contract_abi = json.load(f)

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def register_image(img_hash: str) -> str:
    # 构建交易
    nonce = w3.eth.get_transaction_count(w3.eth.account.from_key(private_key).address)
    tx = contract.functions.registerImage(img_hash).build_transaction({
        'chainId': 80001,  # Polygon 链ID
        'gas': 200000,
        'gasPrice': w3.to_wei('30', 'gwei'),
        'nonce': nonce,
    })
    
    # 签名并发送
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()