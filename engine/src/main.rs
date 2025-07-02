mod block;
mod chain;
mod crypto;
mod rpc;
mod transaction;

use crate::chain::Blockchain;
use std::sync::{Arc, Mutex};

fn main() {
    let blockchain = Arc::new(Mutex::new(Blockchain::new()));
    rpc::start_rpc_server(blockchain);
}
