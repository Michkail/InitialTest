use crate::block::Block;
use crate::transaction::Transaction;
use chrono::Utc;

pub struct Blockchain {
    pub chain: Vec<Block>,
    pub pending_transactions: Vec<Transaction>,
}

impl Blockchain {
    pub fn new() -> Self {
        let genesis = Block::new(
            0,
            Utc::now().timestamp_millis() as u128,
            "0".into(),
            vec![],
            4,
        );
        Self {
            chain: vec![genesis],
            pending_transactions: vec![],
        }
    }

    pub fn add_transaction(&mut self, tx: Transaction) {
        if tx.is_signature_valid() {
            self.pending_transactions.push(tx);
        } else {
            println!("Invalid signature for transaction from {}", tx.sender);
        }
    }

    pub fn mine_block(&mut self) -> &Block {
        let last_block = self.chain.last().unwrap();
        let block = Block::new(
            self.chain.len() as u64,
            Utc::now().timestamp_millis() as u128,
            last_block.hash.clone(),
            self.pending_transactions.clone(),
            4,
        );

        self.pending_transactions.clear();
        self.chain.push(block);
        self.chain.last().unwrap()
    }

    pub fn get_latest_block(&self) -> Block {
        self.chain.last().unwrap().clone()
    }

    pub fn is_chain_valid(&self) -> bool {
        for i in 1..self.chain.len() {
            let current = &self.chain[i];
            let prev = &self.chain[i - 1];

            if current.hash != current.calculate_hash() {
                return false;
            }

            if current.prev_hash != prev.hash {
                return false;
            }

            if !current.hash.starts_with("0000") {
                return false;
            }

            for tx in &current.transactions {
                if !tx.is_signature_valid() {
                    return false;
                }
            }
        }
        true
    }
}
