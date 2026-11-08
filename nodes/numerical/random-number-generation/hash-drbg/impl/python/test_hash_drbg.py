# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-drbg/. The authors are listed in prov/XX9PAT.jsonl.

import hashlib

import pytest

from hash_drbg import MAX_REQUEST_BITS, HashDRBG, ReseedRequired, hash_df

h = bytes.fromhex

# Vectors from the NIST CAVP file drbgtestvectors.zip (CAVS 14.3, Hash_DRBG.rsp), COUNT = 0 of each section.
# Procedure: instantiate, [reseed], generate, generate; ReturnedBits is the output of the second generate.

NO_RESEED = [
    ("sha1", "136cf1c174e5a09f66b962d994396525", "fff1c6645f19231f", "", ("", ""),
     "0e28130fa5ca11edd3293ca26fdb8ae1810611f78715082ed3841e7486f16677b28e33ffe0b93d98ba57ba358c1343ab2a26b4eb7940f5bc639384641ee80a25140331076268bd1ce702ad534dda0ed8"),
    ("sha256", "a65ad0f345db4e0effe875c3a2e71f42c7129d620ff5c119a9ef55f05185e0fb", "8581f9317517276e06e9607ddbcbcc2e", "", ("", ""),
     "d3e160c35b99f340b2628264d1751060e0045da383ff57a57d73a673d2b8d80daaf6a6c35a91bb4579d73fd0c8fed111b0391306828adfed528f018121b3febdc343e797b87dbb63db1333ded9d1ece177cfa6b71fe8ab1da46624ed6415e51ccde2c7ca86e283990eeaeb91120415528b2295910281b02dd431f4c9f70427df"),
    ("sha256", "68c43a008fe46a823d260a9d7fa388fb9e401f0197e7e758a744b4babb3f4651", "eb6825777856331884aaf3751b3e4006",
     "23ce0d32cbf2d26467f0d62acff1a3acbaa6d2746dc3ee7aa9d32c880788afc8",
     ("a31b9f13b58d4fa2f8d8ac42b62a207ff647339a146bd8b268b33d4aff57adbd", "d34fc6504eca4b568193c75357b0d3821a48c77ff80d6dbd21c6cf045ff489cf"),
     "abb4ecbacd4e8fa943c7221aed433861c3b203232657ec4c417d021f905d911db1058ff1e11e272232482ec96bae7cb4efc135502dbe41724077077f6de79b713670c385d04644e1281c3e582e0016255abbe5f8c06d0de57160559f0c08f7fb5be3563c649966190f8d3261364447537de2c7371c6e8c308933d27145bf90ab"),
]

WITH_RESEED = [
    ("sha256", "63363377e41e86468deb0ab4a8ed683f6a134e47e014c700454e81e95358a569", "808aa38f2a72a62359915a9f8a04ca68", "",
     ("e62b8a8ee8f141b6980566e3bfe3c04903dad4ac2cdf9f2280010a6739bc83d3", ""), ("", ""),
     "04eec63bb231df2c630a1afbe724949d005a587851e1aa795e477347c8b056621c18bddcdd8d99fc5fc2b92053d8cfacfb0bb8831205fad1ddd6c071318a6018f03b73f5ede4d4d071f9de03fd7aea105d9299b8af99aa075bdb4db9aa28c18d174b56ee2a014d098896ff2282c955a81969e069fa8ce007a180183a07dfae17"),
    ("sha256", "6c623aea73bc8a59e28c6cd9c7c7ec8ca2e75190bd5dcae5978cf0c199c23f4f", "e55db067a0ed537e66886b7cda02f772",
     "1e59d798810083d1ff848e90b25c9927e3dfb55a0888b0339566a9f9ca7542dc",
     ("9ab40164744c7d00c78b4196f6f917ec33d70030a0812cd4606c5a25387568a9", "4e8bead7cbba7a7bc9ae1e1617222c4139661347599950e7225d1e2faa5d57f5"),
     ("dcb22a5d9f149858636f3ede2253e419816fb7b1103194451ed6a573a8fe6271", "8f9d5c78cdabc32e71ac3b3c49239caddf96053250f4fd92056efbd0be487d36"),
     "6e98a3b1f686f6ffa79355c9d8a5ab7f93312159d52659a2298315f10007c71adabc0b5ccb4164c0949fbdb221b43acdb62bed3099596f2d7bd5d0048173dd2360a543b234ab61a441ddb9299af84ca45c6e618fd521366dbf509d4ec06174da924361d642b107e5564ac1b32340dd2f3158bf4c00bcb4dcf12c6d67af4b74ee"),
    ("sha512", "3144e17a10c856129764f58fd8e4231020546996c0bf6cff8e91c24ee09be333", "b16fcb1cf0c010f31feab733588b8e04", "",
     ("a0b3584c2c8412f618406834404d1eb0ce999ba28966054d7e497e0db608b967", ""), ("", ""),
     "efa35dd0362adb7626456b36fac74d3c28d01d926420275a28bea9c9dd7547c15e7931852ac1277076567535239c1f429c7f75cf74c2267deb6a3e596cf326156c796941283b8d583f171c2f6e3323f7555e1b181ffda30507210cb1f589b23cd71880fd44370cacf43375b0db7e336f12b309bfd4f610bb8f20e1a15e253a4fe511a027968df0b105a1d73aff7c7a826d39f640dfb8f522259ed402282e2c2e9d3a498f51725fe4141b06da5598a42ac1e0494e997d566a1a39b676b96a6003a4c5db84f246584ee65af70ff2160278166da16d91c9b8f2deb02751a1088ad6be4e80ef966eb73e66bc87cad87c77c0b34a21ba1da0ba6d16ca5046dc4abda0"),
    ("sha512", "4b23595b0a3640cfabb0ec34df6a613308b0448488a5d9ff99da4278e072eb34", "8e696bffd9ca3a71d2e2f05e600c8364",
     "010ba93ea68a3d4a200e5145859e299c5b5349b7645fb5bbcad687aba7d67313",
     ("04de4babdbe143bde99aa4452f9aa43b0a164eb927555c0496aa0fc9328a521c", "2b0c7c3efb36b71b917a44086d168313675b426b17c5ab3d0eb6af753f6040e0"),
     ("d0b7d1d12ab15d3bba8f4eba07fee0974838962b247be480683b8e3d4a91033a", "66c78ca12e45bdca003b49cb6440b977dd85b167e7c803890ed1a73666eaa869"),
     "4008cbd8281dc82fd6c368f650ef2609bb771e80c63d478a77fa938248dcbb8b79e54ead0265f6ff1ebfafe4e387c6e27df9f03e4a5225e86a4436e56ebf03b3be2cfbcb49c89c92ec1dfa5ee445dd4f6f64e02a2423a0b18ebd02eec52f5cc21bc3565e796b3ded6552f1b5a574a201c3b11018222806f9618d23d77fd02db879cf87fe24ed7ba11b3b108b559633db1f95c5121b28011aa4dd20399bd4978e1f8b8880c333a47ff1750679bf28d329347b26d347aae90ee562ae8029579cbe0336e066d6b8ba5e0169fec804c30189a4434c1bf8a5b0a249951d3d89554da38ff0751b8b1fef9ae18a0aa2bc477736d199a06f61d400039a4cc03869bb10ca"),
]


@pytest.mark.parametrize("name,ent,nonce,pers,adds,expected", NO_RESEED)
def test_cavp_no_reseed(name, ent, nonce, pers, adds, expected):
    d = HashDRBG(name, h(ent), h(nonce), h(pers))
    n = len(expected) // 2
    d.generate(n, h(adds[0]))
    assert d.generate(n, h(adds[1])).hex() == expected


@pytest.mark.parametrize("name,ent,nonce,pers,reseed,adds,expected", WITH_RESEED)
def test_cavp_with_reseed(name, ent, nonce, pers, reseed, adds, expected):
    d = HashDRBG(name, h(ent), h(nonce), h(pers))
    d.reseed(h(reseed[0]), h(reseed[1]))
    n = len(expected) // 2
    d.generate(n, h(adds[0]))
    assert d.generate(n, h(adds[1])).hex() == expected


def test_cavp_prediction_resistance():
    d = HashDRBG("sha256", h("29e1a42709b7e84dbe50788fbad8cb609c127eec3262636a513fd9059fb8bae4"),
                 h("f3a521f28dffbd97574c405b69b636ad"),
                 h("c99a1147d8db401f4fcf763867296758e26404a30a4a9fa496a717f21f5d749b"))
    d.generate(128, h("17254ea392aead0dc94992d867813497d3fd6dc7669667150afe6c28a2b89946"),
               entropy=h("d5266c01e10d72dd7e8a3bf717cccb8f643ca233314e3e74f106f46b090e5c73"))
    out = d.generate(128, h("157dde59ceb2c662c8665fbe623ec75873fd0c5ccce79a9f5b7098ec8ed77b67"),
                     entropy=h("c7e5f03d26bdf9553338e64ba64ce5b5751b04f9c69992221495f2227b9799d0"))
    assert out.hex() == (
        "e304de9ffd885cf917ead78f05939b8cf54709fc2d0c799a98b543486337204477b1060bceae2a22f7ff42b6cb4b4bc0"
        "610ae2b67558a7c54b65e45bb9f1a86981b74705b48cdbf7d8decf87868267bd948e9394aa4357f8dbbf30612a0eb5b1"
        "31884c220e442d36778e8d74091d8a27c070fe690469e07f3aabeef7c629bfab")


def test_hash_df_definition():
    data = b"abc"
    out = hash_df("sha256", data, 440)
    expect = (hashlib.sha256(b"\x01" + (440).to_bytes(4, "big") + data).digest()
              + hashlib.sha256(b"\x02" + (440).to_bytes(4, "big") + data).digest())[:55]
    assert out == expect and len(out) == 55
    assert len(hash_df("sha512", data, 888)) == 111


def test_state_update_formula():
    d = HashDRBG("sha256", bytes(32), bytes(16))
    V, C = d.V, d.C
    out = d.generate(40)
    vb = V.to_bytes(55, "big")
    blocks = hashlib.sha256(vb).digest() + hashlib.sha256(((V + 1) % 2 ** 440).to_bytes(55, "big")).digest()
    assert out == blocks[:40]
    H = int.from_bytes(hashlib.sha256(b"\x03" + vb).digest(), "big")
    assert d.V == (V + H + C + 1) % 2 ** 440 and d.reseed_counter == 2


def test_reseed_interval_and_limits():
    d = HashDRBG("sha256", bytes(32), bytes(16), reseed_interval=3)
    for _ in range(3):
        d.generate(16)
    with pytest.raises(ReseedRequired):
        d.generate(16)
    d.reseed(b"\x01" * 32)
    assert len(d.generate(16)) == 16
    with pytest.raises(ValueError):
        d.generate(MAX_REQUEST_BITS // 8 + 1)
    with pytest.raises(ValueError):
        HashDRBG("sha256", bytes(16), bytes(16))  # 128 entropy bits for a 256-bit strength
    with pytest.raises(ValueError):
        HashDRBG("md5", bytes(32), bytes(16))
    assert d.generate(0) == b""


def test_determinism_and_separation():
    a = HashDRBG("sha256", b"e" * 32, b"n" * 16, b"p1")
    b = HashDRBG("sha256", b"e" * 32, b"n" * 16, b"p1")
    c = HashDRBG("sha256", b"e" * 32, b"n" * 16, b"p2")
    x, y, z = a.generate(64), b.generate(64), c.generate(64)
    assert x == y and x != z
    x2, y2 = a.generate(64), b.generate(64, b"extra")
    assert x2 != x  # the state moved on
    assert x2 != y2  # additional input changes the output


def test_chi_square_bytes():
    # 65536 output bytes, 256 bins, 255 degrees of freedom; the 1% point is 310.46
    d = HashDRBG("sha256", bytes(range(32)), bytes(16))
    data = b"".join(d.generate(4096) for _ in range(16))
    counts = [0] * 256
    for byte in data:
        counts[byte] += 1
    chi2 = sum((c - 256) ** 2 / 256 for c in counts)
    assert chi2 < 310.46
