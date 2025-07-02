use ring::signature::{Ed25519KeyPair, KeyPair};
use ring::rand::SystemRandom;
use base64::{Engine as _};
use sha2::{Digest, Sha256};

pub fn generate_keypair() -> (String, String) {
    let rng = SystemRandom::new();
    let pkcs8_bytes = Ed25519KeyPair::generate_pkcs8(&rng).unwrap();
    let key_pair = Ed25519KeyPair::from_pkcs8(pkcs8_bytes.as_ref()).unwrap();
    let public_key = base64::engine::general_purpose::STANDARD.encode(key_pair.public_key().as_ref());
    let private_key = base64::engine::general_purpose::STANDARD.encode(pkcs8_bytes.as_ref());
    (public_key, private_key)
}

pub fn hash(data: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(data.as_bytes());
    let result = hasher.finalize();
    hex::encode(result)
}