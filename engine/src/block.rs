use serde::{Serialize, Deserialize};
use sha2::{Sha256, Digest};

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Block {
    pub index: u64,
    pub timestamp: u128,
    pub prev_hash: String,
    pub hash: String,
    pub transactions: Vec<String>,
}

impl Block {
    pub fn new(index: u64, timestamp: u128, prev_hash: String, transactions: Vec<String>) -> Self {
        let tx_concat = transactions.join("");
        let data = format!("{index}{timestamp}{prev_hash}{tx_concat}");
        let hash = hex::encode(Sha256::digest(data.as_bytes()));
        Self { index, timestamp, prev_hash, hash, transactions }
    }
}
