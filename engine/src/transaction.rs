use ring::signature::{UnparsedPublicKey, ED25519};
use serde::{Deserialize, Serialize};
use base64::engine::general_purpose::STANDARD;
use base64::Engine;

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Transaction {
    pub sender: String,      // base64 public key
    pub recipient: String,   // base64 public key
    pub amount: u64,
    pub timestamp: u64,
    pub signature: String,   // base64 signature
}

impl Transaction {
    pub fn get_canonical_string(&self) -> String {
        format!("{},{},{},{}", self.sender, self.recipient, self.amount, self.timestamp)
    }

    pub fn is_signature_valid(&self) -> bool {
        let canonical_string = self.get_canonical_string();
        let payload_bytes = canonical_string.as_bytes();

        let public_key_bytes = match STANDARD.decode(&self.sender) {
            Ok(bytes) => bytes,
            Err(_) => return false,
        };

        let signature_bytes = match STANDARD.decode(&self.signature) {
            Ok(bytes) => bytes,
            Err(_) => return false,
        };

        let public_key = UnparsedPublicKey::new(&ED25519, public_key_bytes);

        public_key.verify(payload_bytes, &signature_bytes).is_ok()
    }
}
