---
tag: XRB4YB
kind: algorithm
slug: sphincs-plus
name: SPHINCS+
aliases:
- FIPS 205
- SLH-DSA
- SPHINCS plus
- Stateless Hash-Based Digital Signature Algorithm
area: cryptography/signatures
level: advanced
summary: "Stateless hash-based signature, standardized by NIST as SLH-DSA in FIPS 205. A random digest picks a FORS few-time key that a hypertree of XMSS trees certifies."
model: word-ram
complexity:
  vars: {d: the number of layers, h: the total height, k: the number of FORS trees, a: the height of a FORS tree, l: the number of WOTS+ chains, w: the chain length}
  time: {worst: Θ(d·2^(h/d)·l·w + k·2^a), average: Θ(d·2^(h/d)·l·w + k·2^a), best: Θ(d·2^(h/d)·l·w + k·2^a)}
  space: {extra: Θ(k·a + d·l + h)}
properties: {deterministic: false, randomized: true}
history:
  year: 2019
  people: [Daniel J. Bernstein, Andreas Hülsing, Stefan Kölbl, Ruben Niederhagen, Joost Rijneveld, Peter Schwabe]
  note: SPHINCS+ was submitted to the NIST post-quantum process in 2017 and described at CCS 2019. NIST published it as SLH-DSA in FIPS 205 in August 2024.
prereqs: [xmss, winternitz-one-time-signature]
see_also: [hash-based-signatures, merkle-signature-scheme, leighton-micali-signature, shake, crystals-dilithium, falcon, nist-pqc-standardization, post-quantum-cryptography]
sources:
  - paper: doi:10.1145/3319535.3363229
    title: "Daniel J. Bernstein, Andreas Hülsing, Stefan Kölbl, Ruben Niederhagen, Joost Rijneveld and Peter Schwabe, The SPHINCS+ signature framework, ACM CCS 2019, pages 2129 to 2146"
    locator: tweakable hash functions, FORS, the hypertree, the security proof, and the robust and simple instances
  - url: "https://doi.org/10.6028/NIST.FIPS.205"
    title: "NIST FIPS 205, Stateless Hash-Based Digital Signature Standard, August 2024"
    locator: Sections 4 to 9 (addresses, WOTS+, XMSS, hypertree, FORS, Algorithms 1 to 20), Section 10 (pure and pre-hash signing, Algorithms 21 to 25), Section 11 (Table 2 and the SHAKE and SHA2 instances), Appendix A (differences from the SPHINCS+ submission)
  - paper: doi:10.1007/978-3-662-46800-5_15
    title: "Daniel J. Bernstein, Daira Hopwood, Andreas Hülsing, Tanja Lange, Ruben Niederhagen, Louiza Papachristodoulou, Michael Schneider, Peter Schwabe and Zooko Wilcox-O'Hearn, SPHINCS: practical stateless hash-based signatures, Eurocrypt 2015, LNCS 9056"
    locator: the first practical stateless hash-based signature, with a hypertree and the HORST few-time signature
  - paper: doi:10.1007/978-3-031-22972-5_1
    title: "Andreas Hülsing and Mikhail Kudinov, Recovering the tight security proof of SPHINCS+, Asiacrypt 2022, LNCS 13794, pages 3 to 33"
    locator: the gap in the WOTS+ part of the earlier proof and the corrected tight proof
  - url: "https://github.com/usnistgov/ACVP-Server/tree/master/gen-val/json-files"
    title: NIST ACVP-Server, SLH-DSA-keyGen-FIPS205 and SLH-DSA-sigGen-FIPS205 test vectors
    locator: keyGen test case 31 and sigGen test case 58 (SLH-DSA-SHAKE-128f)
---

SPHINCS+ is a hash-based signature with no state. The signer keeps only two seeds, and each signature uses a one-time key that a hash of the message selects at random among $2^{h}$ keys, so a repeat is very unlikely. The bottom key is a FORS few-time signature, which stays secure if a few messages land on it. A hypertree, a tree of [XMSS](/xmss/)-like trees, certifies the FORS keys up to one root. NIST standardized SPHINCS+ as SLH-DSA in FIPS 205 (August 2024). Its keys are tiny (32 to 64 bytes) and its security rests on hash functions only, but signatures are 7.8 to 50 kilobytes and signing is slow.

**Notation.** The page follows FIPS 205. $n$ is the hash length in bytes, $h$ the total height of the hypertree, $d$ the number of layers, $h' = h/d$ the height of one XMSS tree, $k$ the number of FORS trees, $a$ their height, $w = 16$ the WOTS+ chain length, $len$ the number of WOTS+ chains ($2n + 3$), and $m$ the digest length in bytes. The keys are $SK = (SK.seed, SK.prf, PK.seed, PK.root)$ and $PK = (PK.seed, PK.root)$. The functions $F$, $H$, $T_\ell$, PRF, $PRF_{msg}$ and $H_{msg}$ are SHAKE256 or SHA-2 calls with a public seed and a 32-byte address. Security is EUF-CMA for at most $2^{64}$ signatures per key.

## In plain words

A Merkle scheme needs a counter because each one-time key may sign only once. SPHINCS+ removes the counter by using so many keys that the signer can pick one at random from a hash of the message.

There are $2^{66}$ bottom keys in the fast 128-bit set. Two messages will sometimes pick the same key, so the bottom key is a few-time signature. It reveals some secret values per message, and a forger needs a message whose values are all already revealed.

To prove a bottom key genuine, the signer cannot store a tree of $2^{66}$ leaves. It uses a stack of small trees: each tree signs the root of a tree below it, and every small tree is built again from the seed when needed. Nothing is stored, so nothing must be updated.

## The problem

Give a post-quantum signature whose security rests on hash functions only, as for [LMS](/leighton-micali-signature/) and XMSS, but with no state. A stateful scheme fails badly when its counter goes back (after a restore from a backup, a clone, or a crash), and the stateless scheme should remove that risk at the price of larger signatures and slower signing.

## The algorithm

```pseudo id=main
SLH_SIGN(M, ctx, SK)                                ▷ pure signing, |ctx| ≤ 255
L1  M' ← toByte(0, 1) ‖ toByte(|ctx|, 1) ‖ ctx ‖ M
L2  R ← PRF_msg(SK.prf, opt_rand, M')               ▷ opt_rand random, or PK.seed if deterministic
L3  digest ← H_msg(R, PK.seed, PK.root, M')         ▷ m bytes
L4  md ← first ⌈k·a/8⌉ bytes; idx_tree ← next h − h' bits; idx_leaf ← next h' bits
L5  SIG_FORS ← FORS_SIGN(md) with FORS key (idx_tree, idx_leaf)
L6  PK_FORS ← FORS_PK_FROM_SIG(SIG_FORS, md)
L7  SIG_HT ← HT_SIGN(PK_FORS, idx_tree, idx_leaf)
L8  return R ‖ SIG_FORS ‖ SIG_HT

FORS_SIGN(md)
L9  for i ← 0 to k − 1: q ← digit i of md in base 2^a; output the secret leaf i·2^a + q and its a sibling nodes in tree i

HT_SIGN(X, idx_tree, idx_leaf)
L10 for j ← 0 to d − 1: sign X with WOTS+ key idx_leaf of XMSS tree idx_tree on layer j, and add its authentication path
L11     X ← root of that tree; idx_leaf ← idx_tree mod 2^h'; idx_tree ← idx_tree ≫ h'

SLH_VERIFY(M, ctx, SIG, PK)
L12 check the length of SIG; compute M', digest, md, idx_tree and idx_leaf as in L1 to L4
L13 node ← FORS_PK_FROM_SIG(SIG_FORS, md)
L14 for j ← 0 to d − 1: node ← XMSS root from the WOTS+ signature and path of layer j on node; update the indices as in L11
L15 return node = PK.root
```

A FORS key has $k$ trees of $2^a$ secret leaves each, and its public key is the hash $T_k$ of the $k$ roots. Line L9 splits $md$ into $k$ numbers of $a$ bits and reveals one leaf per tree with its path. A WOTS+ chain step in SLH-DSA is $F(PK.seed, ADRS, x)$; there are no bitmasks, because the "simple" instance that FIPS 205 approves puts the address and the seed into each call instead. The WOTS+ public key is compressed with one call of $T_{len}$, not with an L-tree. Key generation computes only the top XMSS tree (layer $d - 1$, Algorithm 18); every other tree is computed again during signing from $SK.seed$ and its address.

## Example

For SLH-DSA-SHAKE-128f ($n = 16$, $h = 66$, $d = 22$, $h' = 3$, $a = 6$, $k = 33$, $m = 34$) the signature has 17,088 bytes:

| part | values of $n$ bytes | bytes |
|---|---|---|
| $R$ | 1 | 16 |
| FORS: 33 leaves and 33 paths of 6 nodes | $33 \cdot 7 = 231$ | 3,696 |
| hypertree: 22 WOTS+ signatures of 35 values and 22 paths of 3 nodes | $22 \cdot 35 + 66 = 836$ | 13,376 |

The digest of 34 bytes splits into $md$ (25 bytes, of which $33 \cdot 6 = 198$ bits are used), $idx_{tree}$ (8 bytes, of which 63 bits are kept) and $idx_{leaf}$ (1 byte, of which 3 bits are kept). In the test code, key generation of this set makes 4,495 SHAKE256 calls, signing makes 104,922, and verification makes 6,156: the signer builds 22 small trees and 33 FORS trees again for each signature.

## Correctness

**Correctness.** Every hash call is fixed by its address, so the verifier repeats the signer's computation from the revealed values. It computes the same digest from $R$, so it gets the same FORS key and indices; from the FORS leaves and paths it gets the same FORS public key; and from each WOTS+ signature and path it gets the root that the layer above signed. The top root is $PK.root$. The full proof is below.

**Security.** The SPHINCS+ paper reduces security to multi-target properties of the tweakable hash functions, the pseudorandomness of PRF and $PRF_{msg}$, and the interleaved target subset resilience of $H_{msg}$; Hülsing and Kudinov (2022) repaired a gap in the WOTS+ part of the proof. Collision resistance of the hash is not needed. Grover's algorithm halves the exponent of generic attacks, so $n = 16$ targets NIST category 1.

## Complexity

FIPS 205 Table 2 gives the approved sets ("s" for small signatures, "f" for fast signing). Each name exists with SHA2 and with SHAKE:

| parameter set | $n$ | $h$ | $d$ | $h'$ | $a$ | $k$ | category | public key | signature |
|---|---|---|---|---|---|---|---|---|---|
| SLH-DSA-128s | 16 | 63 | 7 | 9 | 12 | 14 | 1 | 32 | 7,856 |
| SLH-DSA-128f | 16 | 66 | 22 | 3 | 6 | 33 | 1 | 32 | 17,088 |
| SLH-DSA-192s | 24 | 63 | 7 | 9 | 14 | 17 | 3 | 48 | 16,224 |
| SLH-DSA-192f | 24 | 66 | 22 | 3 | 8 | 33 | 3 | 48 | 35,664 |
| SLH-DSA-256s | 32 | 64 | 8 | 8 | 14 | 22 | 5 | 64 | 29,792 |
| SLH-DSA-256f | 32 | 68 | 17 | 4 | 9 | 35 | 5 | 64 | 49,856 |

Signing builds $d$ trees of $2^{h'}$ WOTS+ keys and $k$ FORS trees of $2^a$ leaves, so its cost is $\Theta(d \cdot 2^{h'} \cdot len \cdot w + k \cdot 2^a)$ hash calls. The "s" sets have taller trees ($h' = 9$), so signing is many times slower than for the "f" sets, but the signatures are about half the size. Verification computes one path per tree and one WOTS+ key per layer: $\Theta(d \cdot len \cdot w + k \cdot a)$ calls. Key generation builds only the top tree: $\Theta(2^{h'} \cdot len \cdot w)$.

## Properties

- **Stateless.** No counter: the signer can be copied, restored and run in parallel without risk.
- **Small keys, large signatures.** The public key is $2n$ bytes, the smallest of the NIST post-quantum signatures; the signature is the largest.
- **Hedged or deterministic.** With a fresh $opt\_rand$ (the default), signing is randomized, which helps against fault and side-channel attacks. With $opt\_rand = PK.seed$ the signature is a function of the key and message.
- **Conservative assumptions.** Security needs only properties of hash functions, not a number-theoretic or lattice problem.
- **Limited signature count.** The parameter sets are designed for at most $2^{64}$ signatures per key, because FORS security drops slowly as more leaves are revealed.
- **Not message bound.** FIPS 205 Section 11 notes that the key owner can make two messages with one signature by finding a collision of $H_{msg}$, which is below the claimed category for all sets except the two 128f sets.

## Variants and improvements

- **Round 3 SPHINCS+ vs FIPS 205.** FIPS 205 Appendix A lists the changes from Version 3 of the submission: the new address types WOTS_PRF and FORS_PRF for secret values; $PK.seed$ added to PRF against multi-key attacks; SHA-512 instead of SHA-256 in $H_{msg}$, $PRF_{msg}$, $H$ and $T_\ell$ for the category 3 and 5 SHA2 sets; $R$ and $PK.seed$ added to MGF1 in the SHA2 $H_{msg}$; the bits that select the FORS key are read as in the round 3 reference code, while the FORS indices are read in a new way that is not compatible with that code; a corrected checksum shift; and only 12 of the 36 sets, all "simple". After the draft of August 2023, the final standard added the domain separation of pure and pre-hash signing with a context string (Appendix A.1).
- **Robust vs simple.** The submission also had a "robust" form with bitmasks from PRF, as in XMSS, whose proof needs weaker assumptions; FIPS 205 approves only "simple", which makes fewer hash calls and is faster.
- **HashSLH-DSA.** The pre-hash version (Algorithm 23) signs a hash or XOF digest of the message with its object identifier, for modules that cannot read a long message twice.
- **SPHINCS (2015).** The first practical stateless scheme used the few-time signature HORST and 41 KB signatures; SPHINCS+ replaced HORST with FORS and added the randomized choice of the key.
- **Fewer signatures.** A footnote of FIPS 205 Section 11 points to SP 800-230 for further parameter sets that allow fewer signatures per key.

## When to use it

Use SLH-DSA where long-term trust matters and signatures are few or their size is acceptable: root certificates, firmware and software signing, and documents that must stay valid for decades. Its security depends on hash functions only, so it is a hedge against a break of the lattice schemes [ML-DSA](/crystals-dilithium/) and [Falcon](/falcon/). Where a counter can be kept safely, LMS or XMSS give much smaller signatures; where signatures are frequent or must be small, use ML-DSA.

## Pitfalls

- **Fault attacks.** A fault during the computation of a tree root makes one WOTS+ key sign two different values, which can allow forgeries (Castelnovi, Martinelli and Prest, 2018). Recompute or verify a signature before release in hostile settings.
- **Index extraction.** The way to read the FORS indices and the key selection bits from the digest changed between the round 3 document and FIPS 205; code that follows the old document does not match the ACVP vectors.
- **Pure vs internal.** slh_sign prefixes $M$ with $0$, $|ctx|$ and $ctx$. Signing $M$ directly with slh_sign_internal gives signatures that standard verifiers reject.
- **Pre-hash collisions.** HashSLH-DSA is only as strong as the collision resistance of the pre-hash, unlike pure SLH-DSA.
- **Large signatures in protocols.** A 17 KB or 50 KB signature can break buffers and message size limits that were set for RSA or ECDSA.

## Implementations

The Python code is for study only. It is not constant time, and it must not protect real data. It implements only SLH-DSA-SHAKE-128f, with SHAKE256 from hashlib. The tests check the key pair of ACVP keyGen test case 31, and the deterministic signature of ACVP sigGen test case 58 (external interface, pure, with a 46-byte context); the 17,088-byte signature is compared by its SHA-256 digest and its first 16 bytes. All tests run in about 2 seconds.

## History

Merkle's scheme of 1979 was stateful, and Goldreich (1986) showed that a tree of one-time keys can be stateless if each key is derived from its position by a pseudorandom function, but with very large signatures. Bernstein, Hopwood, Hülsing, Lange, Niederhagen, Papachristodoulou, Schneider, Schwabe and Wilcox-O'Hearn made the idea practical in SPHINCS (Eurocrypt 2015). SPHINCS+ was submitted to the NIST post-quantum standardization in November 2017 and described by Bernstein, Hülsing, Kölbl, Niederhagen, Rijneveld and Schwabe at CCS 2019. NIST selected it in July 2022 and published it as SLH-DSA in FIPS 205 on 13 August 2024, together with ML-KEM (FIPS 203) and ML-DSA (FIPS 204).

## References
