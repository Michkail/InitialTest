use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Transaction {
    pub sender: String,
    pub recipient: String,
    pub amount: u64,
}
