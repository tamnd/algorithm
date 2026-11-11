# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/noise-protocol-framework/. The authors are listed in prov/E0N5YS.jsonl.

import pytest

from noise_protocol_framework import HandshakeState, aead_decrypt, aead_encrypt, public_key, x25519

PROLOGUE = bytes.fromhex("4a6f686e2047616c74")
INIT_E = bytes.fromhex("893e28b9dc6ca8d611ab664754b8ceb7bac5117349a4439a6b0569da977c464a")
RESP_E = bytes.fromhex("bbdb4cdbd309f1a1f2e1456967fe288cadd6f712d65dc7b7793d5e63da6b375b")
INIT_S = bytes.fromhex("e61ef9919cde45dd5f82166404bd08e38bceb5dfdfded0a34c8df7ed542214d1")
RESP_S = bytes.fromhex("4a3acbfdb163dec651dfa3194dece676d437029c62a408b4c5ea9114246e4893")
PAYLOADS = [
    "4c756477696720766f6e204d69736573",
    "4d757272617920526f746862617264",
    "462e20412e20486179656b",
    "4361726c204d656e676572",
    "4a65616e2d426170746973746520536179",
    "457567656e2042f6686d20766f6e2042617765726b",
]
NN = {
    "hash": "9223fec1b892ec9d0dc2fb3bbeb261f170d1ea679f9c44ccf34aa131b4f5d97e",
    "ct": [
        "ca35def5ae56cec33dc2036731ab14896bc4c75dbb07a61f879f8e3afa4c79444c756477696720766f6e204d69736573",
        "95ebc60d2b1fa672c1f46a8aa265ef51bfe38e7ccb39ec5be34069f144808843a0ff96bdf86b579ef7dbf94e812a7470b903c20a85a87e3a1fe863264ae547",
        "eb1a3e3d80c1792b1bb9cb0e1382f8d8322bfb1ca7c4c8517bb686",
        "c781b198d2a974eb1da2c7d518c000cf6396de87ca540963c03713",
        "c77048eb6919fdfe8fe45842bfc5b8d1ff50d1e20c717453ccdfe6176d805b996d",
        "61834d7069dcfb7a1adf8d5ac910f83fa04c73a67789895c6f5f995c5db2ce88e49b124178",
    ],
}
XX = {
    "hash": "c8e5f64e846193be2a834104c2a009868d6c9f3bd3c186299888b488b2f1f58e",
    "ct": [
        "ca35def5ae56cec33dc2036731ab14896bc4c75dbb07a61f879f8e3afa4c79444c756477696720766f6e204d69736573",
        "95ebc60d2b1fa672c1f46a8aa265ef51bfe38e7ccb39ec5be34069f14480884381cbad1f276e038c48378ffce2b65285e08d6b68aaa3629a5a8639392490e5b9bd5269c2f1e4f488ed8831161f19b7815528f8982ffe09be9b5c412f8a0db50f8814c7194e83f23dbd8d162c9326ad",
        "c7195ffacac1307ff99046f219750fc47693e23c3cb08b89c2af808b444850a80ae475b9df0f169ae80a89be0865b57f58c9fea0d4ec82a286427402f113e4b6ae769a1d95941d49b25030",
        "96763ed773f8e47bb3712f0e29b3060ffc956ffc146cee53d5e1df",
        "3e40f15f6f3a46ae446b253bf8b1d9ffb6ed9b174d272328ff91a7e2e5c79c07f5",
        "eb3f3515110702e047a6c9da4478b6ead94873c11c0f2d710ddb3f09fce024b3a58502ae3f",
    ],
}


def test_x25519_rfc7748_vectors() -> None:
    k = bytes.fromhex("a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4")
    u = bytes.fromhex("e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c")
    assert x25519(k, u).hex() == "c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552"
    k = bytes.fromhex("4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d")
    u = bytes.fromhex("e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493")
    assert x25519(k, u).hex() == "95cbde9476e8907d7aade45cb4b873f88b595a68799fa152e6f8f7647aac7957"
    a = bytes.fromhex("77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a")
    b = bytes.fromhex("5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb")
    assert public_key(a).hex() == "8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a"
    assert public_key(b).hex() == "de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f"
    assert x25519(a, public_key(b)).hex() == "4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742"


def test_chacha20_poly1305_rfc8439_section_2_8_2() -> None:
    plain = b"Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the future, sunscreen would be it."
    key = bytes(range(0x80, 0xA0))
    nonce = bytes.fromhex("070000004041424344454647")
    ad = bytes.fromhex("50515253c0c1c2c3c4c5c6c7")
    out = aead_encrypt(key, nonce, ad, plain)
    assert out[-16:].hex() == "1ae10b594f09e26a7e902ecbd0600691"
    assert out[:16].hex() == "d31a8d34648e60db7b86afbc53ef7ec2"
    assert aead_decrypt(key, nonce, ad, out) == plain
    assert aead_decrypt(key, nonce, ad + b"x", out) is None


def run_vector(pattern: str, vec: dict, statics: bool) -> None:
    init = HandshakeState(pattern, True, PROLOGUE, s=INIT_S if statics else None, e=INIT_E)
    resp = HandshakeState(pattern, False, PROLOGUE, s=RESP_S if statics else None, e=RESP_E)
    for i, (payload, ct) in enumerate(zip(PAYLOADS, vec["ct"])):
        sender, receiver = (init, resp) if i % 2 == 0 else (resp, init)
        payload = bytes.fromhex(payload)
        if sender.handshake_hash is None:  # still in the handshake
            msg = sender.write_message(payload)
            assert msg.hex() == ct
            assert receiver.read_message(msg) == payload
        else:
            msg = sender.send.encrypt_with_ad(b"", payload)
            assert msg.hex() == ct
            assert receiver.recv.decrypt_with_ad(b"", msg) == payload
    assert init.handshake_hash.hex() == resp.handshake_hash.hex() == vec["hash"]
    if statics:
        assert init.rs == public_key(RESP_S) and resp.rs == public_key(INIT_S)


def test_noise_nn_cacophony_vector() -> None:
    run_vector("NN", NN, statics=False)


def test_noise_xx_cacophony_vector() -> None:
    run_vector("XX", XX, statics=True)


def test_tampering_and_wrong_prologue_are_detected() -> None:
    init = HandshakeState("XX", True, PROLOGUE, s=INIT_S)
    resp = HandshakeState("XX", False, b"another prologue", s=RESP_S)
    m1 = init.write_message(b"")
    resp.read_message(m1)
    m2 = resp.write_message(b"")
    with pytest.raises(ValueError):  # the transcript hashes differ, so the AEAD check fails
        init.read_message(m2)
    init = HandshakeState("XX", True, PROLOGUE, s=INIT_S)
    resp = HandshakeState("XX", False, PROLOGUE, s=RESP_S)
    resp.read_message(init.write_message(b""))
    m2 = bytearray(resp.write_message(b"hi"))
    m2[40] ^= 1  # inside the encrypted static key
    with pytest.raises(ValueError):
        init.read_message(bytes(m2))
