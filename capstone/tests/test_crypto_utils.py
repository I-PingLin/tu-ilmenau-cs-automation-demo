from cs_capstone.security.crypto_utils import generate_key, encrypt, decrypt, sha256_hash, verify_hash


def test_crypto_roundtrip_and_hash():
    key = generate_key()
    msg = b"test-message"
    token = encrypt(msg, key)
    plain = decrypt(token, key)
    assert plain == msg

    digest = sha256_hash(msg)
    assert len(digest) == 64
    assert verify_hash(msg, digest)
