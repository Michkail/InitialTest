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
            4
        );
        Self {
            chain: vec![genesis],
            pending_transactions: vec![],
        }
    }

    pub fn add_transaction(&mut self, tx: Transaction) {
        self.pending_transactions.push(tx);
    }

    pub fn mine_block(&mut self) -> &Block {
        let txs: Vec<String> = self.pending_transactions
            .iter()
            .map(|t| format!("{:?}", t))
            .collect();
    
        let last_block = self.chain.last().unwrap();
    
        let block = Block::new(
            self.chain.len() as u64,
            chrono::Utc::now().timestamp_millis() as u128,
            last_block.hash.clone(),
            txs,
            4, // difficulty: jumlah nol di awal hash
        );
    
        self.pending_transactions.clear();
        self.chain.push(block);
        self.chain.last().unwrap()
    }    

    pub fn get_latest_block(&self) -> Block {
        self.chain.last().unwrap().clone()
    }
}
