---
tag: 9BR4W0
kind: algorithm
slug: blake2
name: BLAKE2
aliases:
- BLAKE2b
- BLAKE2s
area: cryptography/hash-functions
level: advanced
summary: A fast ARX hash from the SHA-3 finalist BLAKE, with a built-in key, salt and personalization. BLAKE2b uses 64-bit words and BLAKE2s 32-bit words; RFC 7693 specifies both.
model: word-ram
complexity:
  vars: {n: the input length in bytes, r: the number of rounds}
  time: {worst: Θ(r n), average: Θ(r n), best: Θ(r n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2012
  people: [Jean-Philippe Aumasson, Samuel Neves, Zooko Wilcox-O'Hearn, Christian Winnerlein]
  note: BLAKE2 was announced in December 2012 and presented at ACNS 2013 as a faster version of BLAKE. RFC 7693 (2015) by Saarinen and Aumasson specifies BLAKE2b and BLAKE2s.
prereqs: [cryptographic-hash-function, merkle-damgard-construction, chacha20]
see_also: [blake3, sha-3, sha-2, hmac, siphash, argon2, length-extension-attack, tree-hashing]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc7693"
    title: "M-J. Saarinen and J-P. Aumasson, RFC 7693, The BLAKE2 Cryptographic Hash and Message Authentication Code (MAC), November 2015"
    locator: Section 2 (parameters, IV, SIGMA), Section 3 (G, F and padding), Section 4 (parameter sets), Appendices A and B (traces of "abc"), Appendix E (self-test)
  - paper: "Jean-Philippe Aumasson, Samuel Neves, Zooko Wilcox-O'Hearn and Christian Winnerlein, BLAKE2: simpler, smaller, fast as MD5, ACNS 2013, LNCS 7954"
    locator: the description of the changes from BLAKE, the parameter block with salt, personalization and tree fields, and the security discussion
  - paper: "Jean-Philippe Aumasson, Willi Meier, Raphael C.-W. Phan and Luca Henzen, The Hash Function BLAKE, Springer, 2014"
    locator: the specification of BLAKE and its round function, derived from ChaCha
  - paper: "Atul Luykx, Bart Mennink and Samuel Neves, Security analysis of BLAKE2's modes of operation, IACR Transactions on Symmetric Cryptology 2016"
    locator: the indifferentiability and PRF proofs for the sequential and keyed modes in an ideal model
  - paper: "Jian Guo, Pierre Karpman, Ivica Nikolić, Lei Wang and Shuang Wu, Analysis of BLAKE2, CT-RSA 2014, LNCS 8366"
    locator: attacks on reduced-round versions and properties of the compression function
  - url: "https://www.blake2.net/"
    title: BLAKE2 website, with the specification, the BLAKE2bp, BLAKE2sp and BLAKE2X variants, and a list of users
    locator: the pages on the specification, the variants and the users
---

BLAKE2 is a family of cryptographic hash functions designed by Jean-Philippe Aumasson, Samuel Neves, Zooko Wilcox-O'Hearn and Christian Winnerlein in 2012. It is a faster version of BLAKE, one of the five finalists of the SHA-3 competition, and its round function comes from the [ChaCha](/chacha20/) stream cipher. BLAKE2b works on 64-bit words and returns up to 64 bytes; BLAKE2s works on 32-bit words and returns up to 32 bytes. Both take an optional key, so the same function is a hash and a MAC. RFC 7693 specifies both. Argon2, WireGuard, libsodium and the Linux random number generator use BLAKE2.

**Notation.** $w$ is the word size (64 for BLAKE2b, 32 for BLAKE2s), $r$ the number of rounds (12 or 10), $bb = 2w$ the block size in bytes (128 or 64). $nn$ is the digest length and $kk$ the key length, both in bytes, and $ll$ the input length in bytes. $h[0..7]$ is the chaining state, $v[0..15]$ the work vector, $m[0..15]$ the words of one block, $t$ the byte counter, $f$ the flag of the last block. $\boxplus$ is addition modulo $2^w$, $\oplus$ XOR, $\ggg$ rotation to the right. $IV$ is the SHA-512 (or SHA-256) initial value and $\sigma_i$ the message permutation of round $i$. The security goals are collision resistance, preimage resistance and, with a key, PRF security; there is no reduction to a simpler assumption for the full function.

## In plain words

BLAKE2 reads the input in blocks of 128 bytes (BLAKE2b). It keeps a state of eight words. For each block, it puts the state and eight fixed words into a grid of sixteen words, mixes the block into the grid with twelve rounds of additions, XORs and rotations, and folds the grid back into eight words. A counter of the bytes read so far and a flag for the last block also go into the grid, so two inputs that end at different places never give the same work.

The first state word includes the digest length and the key length. With a key, the key padded to a full block is the first block. This makes the hash a MAC with no extra construction, and the output for one digest length is not a prefix of the output for another.

## The problem

The goal is a hash function $H : \{0,1\}^{*} \to \{0,1\}^{8 nn}$ that is as fast as possible in software and as secure as an ideal hash of that output length: about $2^{4 nn}$ work to find a collision and $2^{8 nn}$ to find a preimage. With a key $K$, the function $H_K$ must be a [pseudorandom function](/pseudorandom-function/), so it is a MAC without [HMAC](/hmac/). It should also resist [length extension](/length-extension-attack/), which breaks the prefix MAC $H(K \| m)$ for SHA-256.

## The algorithm

```pseudo id=main
BLAKE2(data, nn, key)                         ▷ RFC 7693, Section 3.3
L1  h ← IV;  h[0] ← h[0] ⊕ 01010000 ⊕ (kk ≪ 8) ⊕ nn          ▷ the parameter block
L2  d ← (key padded with zero bytes to bb bytes, if kk > 0) ‖ data,
    padded with zero bytes to a multiple of bb (one zero block if empty);  dd ← the number of blocks
L3  for i ← 0 to dd − 2 do h ← F(h, d[i], (i + 1)·bb, false)
L4  h ← F(h, d[dd − 1], ll + (bb if kk > 0 else 0), true)
L5  return the first nn bytes of h, each word written little-endian

F(h, m, t, f)                                  ▷ Section 3.2
L6  v[0..7] ← h;  v[8..15] ← IV;  v[12] ← v[12] ⊕ (t mod 2^w);  v[13] ← v[13] ⊕ (t ≫ w)
    if f then v[14] ← v[14] ⊕ (all ones)
L7  for i ← 0 to r − 1 do
        s ← σ[i mod 10]
        G(v, 0, 4,  8, 12, m[s0],  m[s1]);   G(v, 1, 5,  9, 13, m[s2],  m[s3])      ▷ columns
        G(v, 2, 6, 10, 14, m[s4],  m[s5]);   G(v, 3, 7, 11, 15, m[s6],  m[s7])
        G(v, 0, 5, 10, 15, m[s8],  m[s9]);   G(v, 1, 6, 11, 12, m[s10], m[s11])     ▷ diagonals
        G(v, 2, 7,  8, 13, m[s12], m[s13]);  G(v, 3, 4,  9, 14, m[s14], m[s15])
L8  return h[i] ⊕ v[i] ⊕ v[i + 8] for i = 0..7

G(v, a, b, c, d, x, y)                         ▷ Section 3.1; (R1, R2, R3, R4) = (32, 24, 16, 63) or (16, 12, 8, 7)
L9  v[a] ← v[a] ⊞ v[b] ⊞ x;  v[d] ← (v[d] ⊕ v[a]) ⋙ R1;  v[c] ← v[c] ⊞ v[d];  v[b] ← (v[b] ⊕ v[c]) ⋙ R2
    v[a] ← v[a] ⊞ v[b] ⊞ y;  v[d] ← (v[d] ⊕ v[a]) ⋙ R3;  v[c] ← v[c] ⊞ v[d];  v[b] ← (v[b] ⊕ v[c]) ⋙ R4
```

Arrange $v$ as a 4 by 4 grid in row order. The first four calls to $G$ mix the columns, and the last four mix the diagonals, as in ChaCha. Line L1 is the only use of the parameter block in RFC 7693. The BLAKE2 paper defines a full 64-byte block (32 bytes for BLAKE2s) that also holds a salt, a personalization string and the fields for [tree hashing](/tree-hashing/); RFC 7693 sets those to zero. The code supports the salt and the personalization.

## Example

Appendix A of RFC 7693 hashes the 3 bytes `abc` with BLAKE2b-512. Here $nn = 64$ = `40`, $kk = 0$, $ll = 3$ and $dd = 1$.

| step | value |
|---|---|
| L1, $h[0] = IV[0] \oplus$ `01010040` | `6A09E667F3BCC908` ⊕ `01010040` = `6A09E667F2BDC948` |
| L2, $m[0]$ (the other 15 words are 0) | `0000000000636261` |
| L6, $v[12] = IV[4] \oplus 3$ | `510E527FADE682D1` ⊕ 3 = `510E527FADE682D2` |
| L6, $v[14] = IV[6] \oplus$ all ones ($f$ = true) | `E07C265404BE4294` |
| L7, $v[0]$ after round 0 | `86B7C1568029BB79` |
| L7, $v[0]$ and $v[8]$ after round 11 | `12EF8A641EC4F6D6` and `75AB709BD3DCBF24` |
| L8, $h[0] = h[0] \oplus v[0] \oplus v[8]$ | `0D4D1C983FA580BA` |
| L5, the first bytes of the digest | `BA 80 A5 3F 98 1C 4D 0D` ... `D4 00 99 23` |

The digest starts with $h[0]$ written little-endian, so `0D4D1C983FA580BA` becomes `BA 80 A5 3F 98 1C 4D 0D`. Appendix B gives the same trace for BLAKE2s-256: $h[0]$ is `6A09E667` ⊕ `01010020` = `6B08E647`, and the digest starts `50 8C 5E 8C`.

## Correctness

The code computes the function of RFC 7693: the tests check the work vector before round 0, after round 0 and after the last round, the final state and the digest of Appendices A and B, and the grand hash of Appendix E, which covers 24 unkeyed and 24 keyed hashes of each type. The security claims are of two kinds.

**The mode.** BLAKE2 is a Merkle-Damgård style iteration in the HAIFA form: each call to $F$ gets the number of bytes processed so far and a flag for the last block. Two different inputs give different sequences of $(d[i], t, f)$, and the final call has $f$ set while no other call does. So a collision of the hash gives a collision of $F$ on these extended inputs, as in the [Merkle-Damgård theorem](/merkle-damgard-theorem/), and an attacker cannot extend a digest, because the next call would need the same state with $f$ unset. Luykx, Mennink and Neves (2016) prove that the sequential and keyed modes are indifferentiable from a random oracle and are PRFs, assuming that the block cipher inside $F$ is ideal. Their bounds are of birthday type in the state size, so they are far above the claimed security level, but they assume an ideal primitive, which the real $F$ is not.

**The primitive.** The claim that BLAKE2 with an $nn$-byte digest gives about $2^{4 nn}$ collision resistance and $2^{8 nn}$ preimage resistance is a conjecture backed by cryptanalysis. BLAKE had four years of public analysis in the SHA-3 competition. Guo, Karpman, Nikolić, Wang and Wu (CT-RSA 2014) analysed BLAKE2 directly and found attacks only on versions with fewer rounds. No attack on full BLAKE2 is known.

## Complexity

The number of calls to $F$ is $dd = \lceil kk / bb \rceil + \lceil ll / bb \rceil$, or 1 for an empty input with no key. Each call to $F$ makes $8 r$ calls to $G$: 96 for BLAKE2b and 80 for BLAKE2s. Each $G$ has 6 additions, 4 XORs and 4 rotations of words. So BLAKE2b uses 96 calls to $G$ per 128 bytes, about 0.75 per byte, and BLAKE2s 80 per 64 bytes. The state is 8 words and the work vector 16 words. On 64-bit CPUs BLAKE2b is faster than BLAKE2s, and the paper reports that it is faster than MD5, SHA-1, SHA-2 and SHA-3 in software.

## Properties

- **Keyed by design.** $H_K(m)$ is a MAC and a PRF with no outer hash. The key is a separate first block, and $kk$ is in the parameter block, so a keyed hash of $m$ is not the unkeyed hash of the padded key followed by $m$.
- **No length extension**, because of the finalization flag.
- **The digest length is an input.** BLAKE2b-256 is not a prefix of BLAKE2b-512, so outputs of different lengths are independent.
- **Little-endian and zero padding.** There is no length field; the counter $t$ does that job.
- **ARX.** Only additions, rotations and XORs, so a C version runs in constant time without tables.

## Variants and improvements

- **Salt and personalization** (16 bytes each in BLAKE2b, 8 in BLAKE2s). They change the IV words $h[4..7]$, so one function gives many independent ones, for example one per protocol.
- **BLAKE2bp and BLAKE2sp.** 4 or 8 lanes hash interleaved blocks in parallel with the tree fields set, and a root node hashes the lane outputs. They use SIMD units or several cores.
- **BLAKE2X.** An [extendable-output function](/extendable-output-function/): BLAKE2 of the input gives a root, and the output is a sequence of BLAKE2 calls on the root with the node offset counting up.
- **[BLAKE3](/blake3/)** (2020). Seven rounds, 32-bit words, and a binary tree of 1 KiB chunks, so it is parallel and much faster.
- **BLAKE** (2008), the SHA-3 finalist: 14 or 16 rounds, constants added inside $G$, and a length field in the padding.

## When to use it

Use BLAKE2b where a fast general-purpose hash is needed and no standard requires SHA-2 or SHA-3: file checksums, content addressing, key derivation inside a protocol. Use keyed BLAKE2 as a MAC instead of HMAC when both sides have it. Use BLAKE2s on 8-bit and 32-bit microcontrollers. Where FIPS approval is needed, use [SHA-2](/sha-2/) or [SHA-3](/sha-3/). For hash tables use [SipHash](/siphash/), which is faster on short inputs.

## Pitfalls

- **Using the 64-byte BLAKE2b output as a 512-bit security level for every goal.** A key of $kk$ bytes gives at most $2^{8 kk}$ security against key search, and an $nn$-byte tag at most $2^{8 nn}$ against a forgery by guessing.
- **Truncating instead of setting $nn$.** Truncated BLAKE2b-512 is a correct hash, but it is a different function from BLAKE2b with that $nn$; two systems that pick different ways do not agree.
- **Confusing BLAKE2 with BLAKE.** They have different rounds, padding and outputs.
- **Assuming the salt is secret.** The salt and the personalization are public inputs; secrets go in the key.

## Implementations

The Python code is for study only, is not constant time, and must not protect real data. Use `hashlib.blake2b` and `hashlib.blake2s` in Python, or `crypto_generichash` of libsodium. The code gives `g` (line L9), `compress` (lines L6 to L8), `parameter_block`, `blake2` (lines L1 to L5), and the wrappers `blake2b` and `blake2s`. The tests check the traces of Appendices A and B and the Appendix E self-test against the values printed in RFC 7693. As a second check they compare with `hashlib` for inputs that cross block boundaries, with and without a key, salt and personalization. They also check that a wrong key gives a different tag, that a shorter digest is not a prefix of a longer one, and that a changed input bit changes about 256 of the 512 output bits.

## History

Aumasson, Henzen, Meier and Phan submitted BLAKE to the SHA-3 competition in 2008. It reached the final round with Grøstl, JH, Keccak and Skein, and NIST chose Keccak in October 2012. In December 2012 Aumasson, Neves, Wilcox-O'Hearn and Winnerlein announced BLAKE2, which drops rounds (from 16 to 12 for the 64-bit version and from 14 to 10 for the 32-bit version), removes the constants from $G$, changes the rotation counts for speed, and adds the parameter block. They presented it at ACNS 2013. RFC 7693 by Saarinen and Aumasson followed in November 2015. BLAKE2 went into libsodium, Argon2 (the winner of the Password Hashing Competition in 2015), WireGuard, Python's `hashlib` in version 3.6, and the Linux random number generator in version 5.17. BLAKE3 followed in 2020.

## References
