# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmac-drbg/. The authors are listed in prov/8PDZN0.jsonl.

import hashlib
import hmac

import pytest

from hmac_drbg import MAX_REQUEST_BITS, HmacDRBG, ReseedRequired, rfc6979_k

h = bytes.fromhex

# Vectors from the NIST CAVP file drbgtestvectors.zip (CAVS 14.3, HMAC_DRBG.rsp), COUNT = 0 of each section.
# Procedure: instantiate, [reseed], generate, generate; ReturnedBits is the output of the second generate.

NO_RESEED = [
    ("sha1", "e91b63309e93d1d08e30e8d556906875", "f59747c468b0d0da", "", ("", ""),
     "b7928f9503a417110788f9d0c2585f8aee6fb73b220a626b3ab9825b7a9facc79723d7e1ba9255e40e65c249b6082a7bc5e3f129d3d8f69b04ed1183419d6c4f2a13b304d2c5743f41c8b0ee73225347"),
    ("sha256", "ca851911349384bffe89de1cbdc46e6831e44d34a4fb935ee285dd14b71a7488", "659ba96c601dc69fc902940805ec0ca8", "", ("", ""),
     "e528e9abf2dece54d47c7e75e5fe302149f817ea9fb4bee6f4199697d04d5b89d54fbb978a15b5c443c9ec21036d2460b6f73ebad0dc2aba6e624abf07745bc107694bb7547bb0995f70de25d6b29e2d3011bb19d27676c07162c8b5ccde0668961df86803482cb37ed6d5c0bb8d50cf1f50d476aa0458bdaba806f48be9dcb8"),
    ("sha256", "5d3286bc53a258a53ba781e2c4dcd79a790e43bbe0e89fb3eed39086be34174b", "c5422294b7318952ace7055ab7570abf",
     "2dba094d008e150d51c4135bb2f03dcde9cbf3468a12908a1b025c120c985b9d",
     ("793a7ef8f6f0482beac542bb785c10f8b7b406a4de92667ab168ecc2cf7573c6", "2238cdb4e23d629fe0c2a83dd8d5144ce1a6229ef41dabe2a99ff722e510b530"),
     "d04678198ae7e1aeb435b45291458ffde0891560748b43330eaf866b5a6385e74c6fa5a5a44bdb284d436e98d244018d6acedcdfa2e9f499d8089e4db86ae89a6ab2d19cb705e2f048f97fb597f04106a1fa6a1416ad3d859118e079a0c319eb95686f4cbcce3b5101c7a0b010ef029c4ef6d06cdfac97efb9773891688c37cf"),
]

WITH_RESEED = [
    ("sha256", "06032cd5eed33f39265f49ecb142c511da9aff2af71203bffaf34a9ca5bd9c0d", "0e66f71edc43e42a45ad3c6fc6cdc4df", "",
     ("01920a4e669ed3a85ae8a33b35a74ad7fb2a6bb4cf395ce00334a9c9a5a5d552", ""), ("", ""),
     "76fc79fe9b50beccc991a11b5635783a83536add03c157fb30645e611c2898bb2b1bc215000209208cd506cb28da2a51bdb03826aaf2bd2335d576d519160842e7158ad0949d1a9ec3e66ea1b1a064b005de914eac2e9d4f2d72a8616a80225422918250ff66a41bd2f864a6a38cc5b6499dc43f7f2bd09e1e0f8f5885935124"),
    ("sha256", "cdb0d9117cc6dbc9ef9dcb06a97579841d72dc18b2d46a1cb61e314012bdf416", "d0c0d01d156016d0eb6b7e9c7c3c8da8",
     "6f0fb9eab3f9ea7ab0a719bfa879bf0aaed683307fda0c6d73ce018b6e34faaa",
     ("8ec6f7d5a8e2e88f43986f70b86e050d07c84b931bcf18e601c5a3eee3064c82", "1ab4ca9014fa98a55938316de8ba5a68c629b0741bdd058c4d70c91cda5099b3"),
     ("16e2d0721b58d839a122852abd3bf2c942a31c84d82fca74211871880d7162ff", "53686f042a7b087d5d2eca0d2a96de131f275ed7151189f7ca52deaa78b79fb2"),
     "dda04a2ca7b8147af1548f5d086591ca4fd951a345ce52b3cd49d47e84aa31a183e31fbc42a1ff1d95afec7143c8008c97bc2a9c091df0a763848391f68cb4a366ad89857ac725a53b303ddea767be8dc5f605b1b95f6d24c9f06be65a973a089320b3cc42569dcfd4b92b62a993785b0301b3fc452445656fce22664827b88f"),
    ("sha512", "48c121b18733af15c27e1dd9ba66a9a81a5579cdba0f5b657ec53c2b9e90bbf6", "bbb7c777428068fad9970891f879b1af", "",
     ("e0ffefdadb9ccf990504d568bdb4d862cbe17ccce6e22dfcab8b4804fd21421a", ""), ("", ""),
     "05da6aac7d980da038f65f392841476d37fe70fbd3e369d1f80196e66e54b8fadb1d60e1a0f3d4dc173769d75fc3410549d7a843270a54a068b4fe767d7d9a59604510a875ad1e9731c8afd0fd50b825e2c50d062576175106a9981be37e02ec7c5cd0a69aa0ca65bddaee1b0de532e10cfa1f5bf6a026e47379736a099d6750ab121dbe3622b841baf8bdcbe875c85ba4b586b8b5b57b0fecbec08c12ff2a9453c47c6e32a52103d972c62ab9affb8e728a31fcefbbccc556c0f0a35f4b10ace2d96b906e36cbb72233201e536d3e13b045187b417d2449cad1edd192e061f12d22147b0a176ea8d9c4c35404395b6502ef333a813b6586037479e0fa3c6a23"),
]

PRED_RES = [
    ("sha256", "9969e54b4703ff31785b879a7e5c0eae0d3e309559e9fe96b0676d49d591ea4d", "07d20d46d064757d3023cac2376127ab", "",
     ("", ""), ("c60f2999100f738c10f74792676a3fc4a262d13721798046e29a295181569f54", "c11d4524c9071bd3096015fcf7bc24a607f22fa065c937658a2a77a8699089f4"),
     "abc015856094803a938dffd20da94843870ef935b82cfec17706b8f551b8385044235dd44b599f94b39be78dd476e0cf11309c995a7334e0a78b37bc9586235086fa3b637ba91cf8fb65efa22a589c137531aa7b2d4e2607aac27292b01c698e6e01ae679eb87c01a89c7422d4372d6d754ababb4bf896fcb1cd09d692d0283f"),
    ("sha256", "4294671d493dc085b5184607d7de2ff2b6aceb734a1b026f6cfee7c5a90f03da", "d071544e599235d5eb38b64b551d2a6e",
     "63bc769ae1d95a98bde870e4db7776297041d37c8a5c688d4e024b78d83f4d78",
     ("28848becd3f47696f124f4b14853a456156f69be583a7d4682cff8d44b39e1d3", "8bfce0b7132661c3cd78175d83926f643e36f7608eec2c5dac3ddcbacc8c2182"),
     ("db9b4790b62336fbb9a684b82947065393eeef8f57bd2477141ad17e776dac34", "4a9abe80f6f522f29878bedf8245b27940a76471006fb4a4110beb4decb6c341"),
     "e580dc969194b2b18a97478aef9d1a72390aff14562747bf080d741527a6655ce7fc135325b457483a9f9c70f91165a811cf4524b50d51199a0df3bd60d12abac27d0bf6618e6b114e05420352e23f3603dfe8a225dc19b3d1fff1dc245dc6b1df24c741744bec3f9437dbbf222df84881a457a589e7815ef132f686b760f012"),
]


@pytest.mark.parametrize("name,ent,nonce,pers,adds,expected", NO_RESEED)
def test_cavp_no_reseed(name, ent, nonce, pers, adds, expected):
    d = HmacDRBG(name, h(ent), h(nonce), h(pers))
    n = len(expected) // 2
    d.generate(n, h(adds[0]))
    assert d.generate(n, h(adds[1])).hex() == expected


@pytest.mark.parametrize("name,ent,nonce,pers,reseed,adds,expected", WITH_RESEED)
def test_cavp_with_reseed(name, ent, nonce, pers, reseed, adds, expected):
    d = HmacDRBG(name, h(ent), h(nonce), h(pers))
    d.reseed(h(reseed[0]), h(reseed[1]))
    n = len(expected) // 2
    d.generate(n, h(adds[0]))
    assert d.generate(n, h(adds[1])).hex() == expected


@pytest.mark.parametrize("name,ent,nonce,pers,adds,ents,expected", PRED_RES)
def test_cavp_prediction_resistance(name, ent, nonce, pers, adds, ents, expected):
    d = HmacDRBG(name, h(ent), h(nonce), h(pers))
    n = len(expected) // 2
    d.generate(n, h(adds[0]), entropy=h(ents[0]))
    assert d.generate(n, h(adds[1]), entropy=h(ents[1])).hex() == expected


def test_rfc6979_ecdsa_p256_sha256():
    # RFC 6979, Appendix A.2.5: P-256 with SHA-256, messages "sample" and "test"
    q = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
    x = 0xC9AFA9D845BA75166B5C215767B1D6934E50C3DB36E89B127B8A622B120F6721
    assert rfc6979_k(q, x, b"sample") == 0xA6E3C57DD01ABE90086538398355DD4C3B17AA873382B0F24D6129493D8AAD60
    assert rfc6979_k(q, x, b"test") == 0xD16B6AE827F17175E040871A1C7EC3500192C4C92677336EC2537ACAEE0008E0


def test_instantiate_matches_definition():
    ent, nonce = bytes(range(32)), bytes(range(32, 48))
    d = HmacDRBG("sha256", ent, nonce)
    mac = lambda k, m: hmac.new(k, m, hashlib.sha256).digest()
    K, V = bytes(32), b"\x01" * 32
    K = mac(K, V + b"\x00" + ent + nonce)
    V = mac(K, V)
    K = mac(K, V + b"\x01" + ent + nonce)
    V = mac(K, V)
    assert (d.K, d.V, d.reseed_counter) == (K, V, 1)


def test_generate_matches_definition():
    d = HmacDRBG("sha256", bytes(range(32)), bytes(16))
    K, V = d.K, d.V
    mac = lambda k, m: hmac.new(k, m, hashlib.sha256).digest()
    v1 = mac(K, V)
    v2 = mac(K, v1)
    out = d.generate(40)
    assert out == (v1 + v2)[:40]
    K2 = mac(K, v2 + b"\x00")  # Update with empty data: one round only
    assert (d.K, d.V, d.reseed_counter) == (K2, mac(K2, v2), 2)


def test_reseed_interval_and_limits():
    d = HmacDRBG("sha256", bytes(32), bytes(16), reseed_interval=3)
    for _ in range(3):
        d.generate(16)
    with pytest.raises(ReseedRequired):
        d.generate(16)
    d.reseed(b"\x07" * 32)
    assert len(d.generate(MAX_REQUEST_BITS // 8)) == MAX_REQUEST_BITS // 8
    with pytest.raises(ValueError):
        d.generate(MAX_REQUEST_BITS // 8 + 1)
    with pytest.raises(ValueError):
        HmacDRBG("sha256", bytes(16), bytes(16))


def test_determinism_and_separation():
    a = HmacDRBG("sha256", b"e" * 32, b"n" * 16, b"p1")
    b = HmacDRBG("sha256", b"e" * 32, b"n" * 16, b"p1")
    c = HmacDRBG("sha256", b"e" * 32, b"n" * 16, b"p2")
    x = a.generate(64)
    assert x == b.generate(64)
    assert x != c.generate(64)
    assert a.generate(64) != x  # the state moves between requests
    b.generate(64)
    assert a.generate(32, b"add") != b.generate(32)  # additional input changes the output


def test_byte_frequencies_chi_square():
    # 65536 bytes; chi-square with 255 degrees of freedom, 0.999 quantile 330.52
    d = HmacDRBG("sha256", bytes(range(32)), bytes(16))
    data = b"".join(d.generate(4096) for _ in range(16))
    counts = [0] * 256
    for byte in data:
        counts[byte] += 1
    e = len(data) / 256
    chi2 = sum((c - e) ** 2 / e for c in counts)
    assert chi2 < 330.52
