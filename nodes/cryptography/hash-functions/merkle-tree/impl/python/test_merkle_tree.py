# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-tree/. The authors are listed in prov/9FDHGB.jsonl.

import hashlib

import pytest

from merkle_tree import (
    audit_path,
    bitcoin_style_root,
    consistency_proof,
    leaf_hash,
    mth,
    naive_root,
    node_hash,
    verify_consistency,
    verify_inclusion,
)

# transparency-dev/merkle, testonly/constants.go: LeafInputs(), NodeHashes(), RootHashes().
LEAVES = [
    bytes.fromhex(x)
    for x in ["", "00", "10", "2021", "3031", "40414243", "5051525354555657", "606162636465666768696a6b6c6d6e6f"]
]
LEVEL0 = [
    "6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d",
    "96a296d224f285c67bee93c30f8a309157f0daa35dc5b87e410b78630a09cfc7",
    "0298d122906dcfc10892cb53a73992fc5b9f493ea4c9badb27b791b4127a7fe7",
    "07506a85fd9dd2f120eb694f86011e5bb4662e5c415a62917033d4a9624487e7",
    "bc1a0643b12e4d2d7c77918f44e0f4f79a838b6cf9ec5b5c283e1f4d88599e6b",
    "4271a26be0d8a84f0bd54c8c302e7cb3a3b5d1fa6780a40bcce2873477dab658",
    "b08693ec2e721597130641e8211e7eedccb4c26413963eee6c1e2ed16ffb1a5f",
    "46f6ffadd3d06a09ff3c5860d2755c8b9819db7df44251788c7d8e3180de8eb1",
]
LEVEL1 = [
    "fac54203e7cc696cf0dfcb42c92a1d9dbaf70ad9e621f4bd8d98662f00e3c125",
    "5f083f0a1a33ca076a95279832580db3e0ef4584bdff1f54c8a360f50de3031e",
    "0ebc5d3437fbe2db158b9f126a1d118e308181031d0a949f8dededebc558ef6a",
    "ca854ea128ed050b41b35ffc1b87b8eb2bde461e9e3b5596ece6b9d5975a0ae0",
]
LEVEL2 = [
    "d37ee418976dd95753c1c73862b9398fa2a2cf9b4ff0fdfe8b30cd95209614b7",
    "6b47aaf29ee3c2af9af889bc1fb9254dabd31177f16232dd6aab035ca39bf6e4",
]
ROOTS = [
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",  # SHA-256 of the empty string
    "6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d",
    "fac54203e7cc696cf0dfcb42c92a1d9dbaf70ad9e621f4bd8d98662f00e3c125",
    "aeb6bcfe274b70a14fb067a5e5578264db0fa9b51af5e0ba159158f329e06e77",
    "d37ee418976dd95753c1c73862b9398fa2a2cf9b4ff0fdfe8b30cd95209614b7",
    "4e3bbb1f7b478dcfe71fb631631519a3bca12c9aefca1612bfce4c13a86264d4",
    "76e67dadbcdf1e10e1b74ddc608abd2f98dfb16fbce75277b5232a127f2087ef",
    "ddb89be403809e325750d3d263cd78929c2942b7942a34b77e122c9594a74c8c",
    "5dc9da79a70659a9ad559cb701ded9a2ab9d823aad2f4960cfe370eff4604328",
]


def test_leaf_and_node_hashes() -> None:
    assert [leaf_hash(d).hex() for d in LEAVES] == LEVEL0
    for i, want in enumerate(LEVEL1):
        assert mth(LEAVES[2 * i : 2 * i + 2]).hex() == want
    for i, want in enumerate(LEVEL2):
        assert mth(LEAVES[4 * i : 4 * i + 4]).hex() == want


@pytest.mark.parametrize("n", range(9))
def test_root_hashes(n: int) -> None:
    assert mth(LEAVES[:n]).hex() == ROOTS[n]


def _rfc_names() -> dict[str, bytes]:
    # RFC 6962, Section 2.1.3: the tree with 7 leaves and its named nodes.
    a, b, c, d, e, f, j = (leaf_hash(x) for x in LEAVES[:7])
    g, h, i = node_hash(a, b), node_hash(c, d), node_hash(e, f)
    k, l = node_hash(g, h), node_hash(i, j)
    return {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "g": g, "h": h, "i": i, "j": j, "k": k, "l": l}


def test_rfc6962_example_audit_paths() -> None:
    nm = _rfc_names()
    d7 = LEAVES[:7]
    assert node_hash(nm["k"], nm["l"]) == mth(d7) == bytes.fromhex(ROOTS[7])
    assert audit_path(0, d7) == [nm["b"], nm["h"], nm["l"]]
    assert audit_path(3, d7) == [nm["c"], nm["g"], nm["l"]]
    assert audit_path(4, d7) == [nm["f"], nm["j"], nm["k"]]
    assert audit_path(6, d7) == [nm["i"], nm["k"]]


def test_rfc6962_example_consistency_proofs() -> None:
    nm = _rfc_names()
    d7 = LEAVES[:7]
    assert consistency_proof(3, d7) == [nm["c"], nm["d"], nm["g"], nm["l"]]
    assert consistency_proof(4, d7) == [nm["l"]]
    assert consistency_proof(6, d7) == [nm["i"], nm["j"], nm["k"]]


def test_inclusion_proofs_verify() -> None:
    for n in range(1, 9):
        root = mth(LEAVES[:n])
        for m in range(n):
            assert verify_inclusion(m, n, LEAVES[m], audit_path(m, LEAVES[:n]), root)


def test_inclusion_fails_on_changed_leaf_or_index() -> None:
    for n in range(2, 9):
        root = mth(LEAVES[:n])
        for m in range(n):
            path = audit_path(m, LEAVES[:n])
            assert not verify_inclusion(m, n, LEAVES[m] + b"x", path, root)
            assert not verify_inclusion((m + 1) % n, n, LEAVES[m], path, root)
            assert not verify_inclusion(m, n, LEAVES[m], path[:-1], root)
            bad = list(path)
            bad[0] = bytes(32)
            assert not verify_inclusion(m, n, LEAVES[m], bad, root)


def test_consistency_proofs_verify_and_reject() -> None:
    for n in range(2, 9):
        new = mth(LEAVES[:n])
        for m in range(1, n):
            old = mth(LEAVES[:m])
            proof = consistency_proof(m, LEAVES[:n])
            assert verify_consistency(m, n, old, new, proof)
            other = list(LEAVES[:m])
            other[0] = b"changed history"
            assert not verify_consistency(m, n, mth(other), new, proof)
            for i in range(len(proof)):
                bad = list(proof)
                bad[i] = bytes(32)
                assert not verify_consistency(m, n, old, new, bad)


def test_second_preimage_without_domain_separation() -> None:
    d = [b"tx0", b"tx1", b"tx2", b"tx3"]
    h = [hashlib.sha256(x).digest() for x in d]
    forged = [h[0] + h[1], h[2] + h[3]]  # two 64-byte "leaves" that are inner nodes
    assert naive_root(forged) == naive_root(d)  # a second preimage of the root
    assert mth(forged) != mth(d)  # the 0x00 and 0x01 prefixes stop it


def test_duplicated_last_node_cve_2012_2459() -> None:
    a, b, c = b"a", b"b", b"c"
    assert bitcoin_style_root([a, b, c]) == bitcoin_style_root([a, b, c, c])
    assert mth([a, b, c]) != mth([a, b, c, c])
