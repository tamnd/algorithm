# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blake3/. The authors are listed in prov/N2JG8C.jsonl.

import hashlib

import pytest

from blake3 import Hasher, blake3, derive_key

# Official vectors: test_vectors/test_vectors.json in github.com/BLAKE3-team/BLAKE3.
# The input of length n is bytes(i % 251 for i in range(n)).
KEY = b"whats the Elvish word for friend"
CONTEXT = b"BLAKE3 2019-12-27 16:29:52 test vectors context"

# The case "input_len": 0, all 131 bytes of the extended output of each mode.
EMPTY_HASH = (
    "af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262e00f03e7b69af26b7faaf09fcd333050338ddfe085b8cc"
    "869ca98b206c08243a26f5487789e8f660afe6c99ef9e0c52b92e7393024a80459cf91f476f9ffdbda7001c22e159b402631f277ca96f2"
    "defdf1078282314e763699a31c5363165421cce14d"
)
EMPTY_KEYED = (
    "92b2b75604ed3c761f9d6f62392c8a9227ad0ea3f09573e783f1498a4ed60d26b18171a2f22a4b94822c701f107153dba24918c4bae4d2"
    "945c20ece13387627d3b73cbf97b797d5e59948c7ef788f54372df45e45e4293c7dc18c1d41144a9758be58960856be1eabbe22c265319"
    "0de560ca3b2ac4aa692a9210694254c371e851bc8f"
)
EMPTY_DERIVE = (
    "2cc39783c223154fea8dfb7c1b1660f2ac2dcbd1c1de8277b0b0dd39b7e50d7d905630c8be290dfcf3e6842f13bddd573c098c3f17361f"
    "1f206b8cad9d088aa4a3f746752c6b0ce6a83b0da81d59649257cdf8eb3e9f7d4998e41021fac119deefb896224ac99f860011f73609e6"
    "e0e4540f93b273e56547dfd3aa1a035ba6689d89a0"
)

# Other cases: the first 32 bytes of "hash", "keyed_hash" and "derive_key".
CASES = {
    1: ("2d3adedff11b61f14c886e35afa036736dcd87a74d27b5c1510225d0f592e213",
        "6d7878dfff2f485635d39013278ae14f1454b8c0a3a2d34bc1ab38228a80c95b",
        "b3e2e340a117a499c6cf2398a19ee0d29cca2bb7404c73063382693bf66cb06c"),
    64: ("4eed7141ea4a5cd4b788606bd23f46e212af9cacebacdc7d1f4c6dc7f2511b98",
         "ba8ced36f327700d213f120b1a207a3b8c04330528586f414d09f2f7d9ccb7e6",
         "a5c4a7053fa86b64746d4bb688d06ad1f02a18fce9afd3e818fefaa7126bf73e"),
    1023: ("10108970eeda3eb932baac1428c7a2163b0e924c9a9e25b35bba72b28f70bd11",
           "c951ecdf03288d0fcc96ee3413563d8a6d3589547f2c2fb36d9786470f1b9d6e",
           "74a16c1c3d44368a86e1ca6df64be6a2f64cce8f09220787450722d85725dea5"),
    1024: ("42214739f095a406f3fc83deb889744ac00df831c10daa55189b5d121c855af7",
           "75c46f6f3d9eb4f55ecaaee480db732e6c2105546f1e675003687c31719c7ba4",
           "7356cd7720d5b66b6d0697eb3177d9f8d73a4a5c5e968896eb6a689684302706"),
    1025: ("d00278ae47eb27b34faecf67b4fe263f82d5412916c1ffd97c8cb7fb814b8444",
           "357dc55de0c7e382c900fd6e320acc04146be01db6a8ce7210b7189bd664ea69",
           "effaa245f065fbf82ac186839a249707c3bddf6d3fdda22d1b95a3c970379bcb"),
    2049: ("5f4d72f40d7a5f82b15ca2b2e44b1de3c2ef86c426c95c1af0b6879522563030",
           "9f29700902f7c86e514ddc4df1e3049f258b2472b6dd5267f61bf13983b78dd5",
           "2ea477c5515cc3dd606512ee72bb3e0e758cfae7232826f35fb98ca1bcbdf273"),
    3073: ("7124b49501012f81cc7f11ca069ec9226cecb8a2c850cfe644e327d22d3e1cd3",
           "68dede9bef00ba89e43f31a6825f4cf433389fedae75c04ee9f0cf16a427c95a",
           "72613c9ec9ff7e40f8f5c173784c532ad852e827dba2bf85b2ab4b76f7079081"),
    8193: ("bab6c09cb8ce8cf459261398d2e7aef35700bf488116ceb94a36d0f5f1b7bc3b",
           "954a2a75420c8d6547e3ba5b98d963e6fa6491addc8c023189cc519821b4a1f5",
           "af1e0346e389b17c23200270a64aa4e1ead98c61695d917de7d5b00491c9b0f1"),
}


def data(n: int) -> bytes:
    return bytes(i % 251 for i in range(n))


def test_empty_input_extended_output() -> None:
    assert blake3(b"", 131).hex() == EMPTY_HASH
    assert blake3(b"", 131, key=KEY).hex() == EMPTY_KEYED
    assert derive_key(CONTEXT, b"", 131).hex() == EMPTY_DERIVE
    # The default 32-byte output is a prefix of the extended output.
    assert blake3(b"").hex() == EMPTY_HASH[:64]


@pytest.mark.parametrize("n", sorted(CASES))
def test_official_vectors(n: int) -> None:
    want_hash, want_keyed, want_derive = CASES[n]
    x = data(n)
    assert blake3(x).hex() == want_hash
    assert blake3(x, key=KEY).hex() == want_keyed
    assert derive_key(CONTEXT, x).hex() == want_derive


@pytest.mark.parametrize("n", [0, 1, 1024, 1025, 2049, 3073, 8193])
def test_incremental_hasher_matches(n: int) -> None:
    x = data(n)
    h = Hasher()
    for i in range(0, n, 700):
        h.update(x[i:i + 700])
    assert h.finalize() == blake3(x)
    hk = Hasher(KEY).update(x)
    assert hk.finalize(40) == blake3(x, 40, key=KEY)


def test_stack_depth_is_logarithmic() -> None:
    h = Hasher().update(data(16 * 1024 + 1))  # 17 chunks
    assert h.max_stack <= 5
    assert h.finalize() == blake3(data(16 * 1024 + 1))


def test_wrong_key_fails() -> None:
    tag = blake3(b"message", key=KEY)
    bad = bytes([KEY[0] ^ 1]) + KEY[1:]
    assert blake3(b"message", key=bad) != tag
    assert blake3(b"message") != tag
    with pytest.raises(ValueError):
        blake3(b"message", key=b"short")


def test_modes_are_separated() -> None:
    # The same 32 bytes as a key, and as a derived key, give different functions.
    assert derive_key(KEY, b"m") != blake3(b"m", key=blake3(KEY))


def test_avalanche() -> None:
    msg = data(100)
    base = blake3(msg, 64)
    total = 0
    for i in range(0, 800, 5):
        m = bytearray(msg)
        m[i // 8] ^= 1 << (i % 8)
        total += sum(bin(a ^ b).count("1") for a, b in zip(base, blake3(bytes(m), 64)))
    assert 246 <= total / 160 <= 266  # about 256 of 512 bits


def test_not_blake2s() -> None:
    # BLAKE3 shares the IV and G of BLAKE2s, but it is a different function.
    assert blake3(b"abc") != hashlib.blake2s(b"abc").digest()
