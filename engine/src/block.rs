use serde::{Serialize, Deserialize};
use sha2::{Sha256, Digest};

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Block {
    pub index: u64,
    pub timestamp: u128,
    pub prev_hash: String,
    pub hash: String,
    pub nonce: u64,
    pub transactions: Vec<String>,
}

impl Block {
    pub fn new(index: u64, timestamp: u128, prev_hash: String, transactions: Vec<String>, difficulty: usize) -> Self {
        let mut nonce = 0;
        let tx_data = format!("{:?}", transactions);
        loop {
            let data = format!("{index}{timestamp}{prev_hash}{tx_data}{nonce}");
            let hash = hex::encode(Sha256::digest(data.as_bytes()));
            if hash.starts_with(&"0".repeat(difficulty)) {
                return Self {
                    index,
                    timestamp,
                    prev_hash,
                    hash,
                    nonce,
                    transactions,
                };
            }
            nonce += 1;
        }
    }
}
