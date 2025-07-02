use crate::crypto::hash;
use crate::transaction::Transaction;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Block {
    pub index: u64,
    pub timestamp: u128,
    pub prev_hash: String,
    pub transactions: Vec<Transaction>,
    pub nonce: u64,
    pub hash: String,
}

impl Block {
    pub fn new(index: u64, timestamp: u128, prev_hash: String, transactions: Vec<Transaction>, difficulty: usize) -> Self {
        let mut nonce = 0;
        let mut hash = Self::calculate_hash_static(
            index,
            timestamp,
            &prev_hash,
            &transactions,
            nonce,
        );

        while &hash[..difficulty] != "0".repeat(difficulty) {
            nonce += 1;
            hash = Self::calculate_hash_static(
                index,
                timestamp,
                &prev_hash,
                &transactions,
                nonce,
            );
        }

        Block {
            index,
            timestamp,
            prev_hash,
            transactions,
            nonce,
            hash,
        }
    }

    pub fn calculate_hash(&self) -> String {
        Self::calculate_hash_static(
            self.index,
            self.timestamp,
            &self.prev_hash,
            &self.transactions,
            self.nonce,
        )
    }

    pub fn calculate_hash_static(
        index: u64,
        timestamp: u128,
        prev_hash: &str,
        transactions: &Vec<Transaction>,
        nonce: u64,
    ) -> String {
        let tx_data: String = transactions
            .iter()
            .map(|tx| tx.get_canonical_string())
            .collect::<Vec<_>>()
            .join(";");

        let data = format!("{}{}{}{}{}", index, timestamp, prev_hash, tx_data, nonce);
        hash(&data)
    }
}
