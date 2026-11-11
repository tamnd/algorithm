---
tag: 1FR1YR
kind: algorithm
slug: triple-des
name: Triple DES
aliases:
- 3DES
- TDEA
area: cryptography/symmetric-ciphers
level: core
summary: DES applied three times, encrypt then decrypt then encrypt, with a bundle of three keys. It resists key search but keeps a 64-bit block; NIST disallows it for encryption after 2023.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {b: the number of 64-bit blocks}
  time: {worst: Θ(b), average: Θ(b), best: Θ(b)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1978
  people: [Walter Tuchman]
  note: Tuchman proposed the encrypt, decrypt, encrypt form with two keys in 1978. ANSI X9.52 (1998) and NIST SP 800-67 standardized TDEA.
prereqs: [data-encryption-standard, meet-in-the-middle-attack]
see_also: [exhaustive-key-search, key-whitening, birthday-attack, cbc-mode, advanced-encryption-standard, block-cipher, prp-prf-switching-lemma, ideal-cipher-model]
sources:
  - paper: doi:10.6028/NIST.SP.800-67r2
    title: NIST, SP 800-67 Rev. 2, Recommendation for the Triple Data Encryption Algorithm (TDEA) Block Cipher, November 2017, withdrawn January 1, 2024
    locator: Section 3.1 (the TDEA forward and inverse operations and the key bundle) and the limit of 2^20 blocks for each key bundle
  - url: "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-67r1.pdf"
    title: NIST, SP 800-67 Rev. 1, Recommendation for the Triple Data Encryption Algorithm (TDEA) Block Cipher, January 2012
    locator: Section 3.1 (keying options 1, 2 and 3) and Appendix B.1 (the TDEA ECB example used in the tests)
  - paper: doi:10.6028/NIST.SP.800-131Ar2
    title: NIST, SP 800-131A Rev. 2, Transitioning the Use of Cryptographic Algorithms and Key Lengths, March 2019
    locator: Section 2 and Table 1 (the status of two-key and three-key TDEA)
  - paper: "Whitfield Diffie and Martin E. Hellman, Exhaustive cryptanalysis of the NBS Data Encryption Standard, Computer 10(6), 1977"
    locator: the meet-in-the-middle attack on double encryption
  - paper: doi:10.1145/358699.358718
    title: Ralph C. Merkle and Martin E. Hellman, On the security of multiple encryption, Communications of the ACM 24(7), 1981
    locator: the attack on double DES and the chosen-plaintext attack on two-key triple DES
  - paper: "Paul C. van Oorschot and Michael J. Wiener, A known-plaintext attack on two-key triple encryption, Advances in Cryptology, EUROCRYPT 1990, LNCS 473, Springer, 1991"
    locator: the attack in time about 2^(120 - lg n) with n known plaintexts
  - paper: "Stefan Lucks, Attacking triple encryption, Fast Software Encryption, FSE 1998, LNCS 1372, Springer, 1998"
    locator: the improved attack on three-key triple DES
  - paper: doi:10.1145/2976749.2978423
    title: Karthikeyan Bhargavan and Gaëtan Leurent, On the practical (in-)security of 64-bit block ciphers, ACM CCS 2016
    locator: the Sweet32 birthday attacks on 3DES in TLS and Blowfish in OpenVPN
  - paper: "Mihir Bellare and Phillip Rogaway, The security of triple encryption and a framework for code-based game-playing proofs, Advances in Cryptology, EUROCRYPT 2006, LNCS 4004, Springer, 2006"
    locator: the bound for triple encryption in the ideal cipher model
---

Triple DES, or the Triple Data Encryption Algorithm (TDEA), is a [block cipher](/block-cipher/) that applies [DES](/data-encryption-standard/) three times to each 64-bit block: it encrypts with a key $K_1$, decrypts with $K_2$ and encrypts with $K_3$. The three keys form a *key bundle* of 168 effective bits. It was the standard way to extend the life of DES hardware after the 56-bit key became too short. Double encryption is not enough, because the [meet-in-the-middle attack](/meet-in-the-middle-attack/) breaks it with about $2^{57}$ DES calls; three-key Triple DES costs about $2^{112}$ against the same attack. The 64-bit block is the remaining weakness: the Sweet32 [birthday attacks](/birthday-attack/) of 2016 used it on live TLS traffic. NIST SP 800-131A Rev. 2 states that three-key TDEA encryption is "Deprecated through 2023" and "Disallowed after 2023", with decryption allowed for "Legacy use" only. NIST withdrew SP 800-67 Rev. 2, the TDEA standard, on January 1, 2024.

## In plain words

DES has a key that is too short to keep out a determined attacker who tries every key. The simplest fix is to run DES more than once with different keys.

Running it twice does not help much. An attacker who has one plaintext and its ciphertext can encrypt the plaintext under every first key, decrypt the ciphertext under every second key, and look for a value that appears in both lists. That costs about twice the work of breaking DES once.

Running it three times works. The middle step is a decryption, not an encryption. This choice lets old equipment that only knows single DES talk to new equipment: if all three keys are equal, the first two steps cancel and the result is plain DES.

## The problem

TDEA computes a permutation of $\{0,1\}^{64}$ for each key bundle $(K_1, K_2, K_3)$ of three 64-bit DES keys, and its inverse. Write $E_K$ and $D_K$ for DES encryption and decryption, called the forward and inverse DEA transformations in SP 800-67. Each key has 8 parity bits, so the bundle has $3 \cdot 56 = 168$ effective bits. As with any block cipher, longer messages need a mode of operation such as [CBC](/cbc-mode/) or CTR.

**Keying options.** SP 800-67 Rev. 1 (2012) defined three options.

| option | keys | effective key bits | name | status |
|---|---|---|---|---|
| 1 | $K_1, K_2, K_3$ independent | 168 | three-key TDEA (3TDEA) | encryption disallowed after 2023 |
| 2 | $K_1, K_2$ independent, $K_3 = K_1$ | 112 | two-key TDEA (2TDEA) | encryption disallowed |
| 3 | $K_1 = K_2 = K_3$ | 56 | equal to single DES | for backward compatibility only |

SP 800-67 Rev. 2 (2017) no longer numbers the options. It requires three distinct keys for 3TDEA, says that a bundle shall not have three equal keys, allows two-key TDEA for legacy use only, and lowers the limit for one bundle from $2^{32}$ to $2^{20}$ blocks.

## The algorithm

```pseudo id=main
TDEA-ENCRYPT(K1, K2, K3, x)
L1  a ← E_K1(x)
L2  b ← D_K2(a)
L3  return E_K3(b)

TDEA-DECRYPT(K1, K2, K3, y)
L4  a ← D_K3(y)
L5  b ← E_K2(a)
L6  return D_K1(b)
```

Each DES call expands its key with the [DES key schedule](/key-schedule/), so an implementation computes the three schedules once per bundle and reuses them.

**The attack that rules out double DES.** Let $y = E_{K_2}(E_{K_1}(x))$ for one known pair $(x, y)$. For every $k_1$, store $E_{k_1}(x)$ in a table. For every $k_2$, look up $D_{k_2}(y)$. Each match gives a candidate $(k_1, k_2)$; test it on a second pair. This uses $2 \cdot 2^{56}$ DES calls and a table of $2^{56}$ entries, against $2^{112}$ for trying every pair of keys. About $2^{112}/2^{64} = 2^{48}$ false candidates survive the first pair, and a second pair removes them (Diffie and Hellman 1977; Merkle and Hellman 1981).

## Example

**The SP 800-67 Rev. 1 vectors (Appendix B.1).** The key bundle is $K_1$ = 0123456789ABCDEF, $K_2$ = 23456789ABCDEF01, $K_3$ = 456789ABCDEF0123. The plaintext is the ASCII text "The quick brown fox jump", in three blocks.

| block | plaintext | after L1 | after L2 | ciphertext |
|---|---|---|---|---|
| 1 | 5468652071756663 | A28E91724C4BBA31 | 5A2EA7F983A2F53F | A826FD8CE53B855F |
| 2 | 6B2062726F776E20 | 167E47EC24F71D63 | EA141A7DD69701F0 | CCE21C8112256FE6 |
| 3 | 666F78206A756D70 | 2C1A917234425365 | 8059EE8212E22A79 | 68D5C05DD9B6B900 |

This is ECB mode, used only to show the block function. The implementation reproduces every column and decrypts each ciphertext back to its plaintext.

**Meet in the middle on a toy cipher.** The tests use a toy cipher of the author's own design with a 16-bit block, a 12-bit key and 4 rounds; it is not secure and is not DES. Double encryption with $k_1$ = 5A3 and $k_2$ = C17 maps 0123, 4567, 89AB to 83D0, 3F24, 302A. The attack makes $2^{12}$ encryptions of 0123 for the table and $2^{12}$ decryptions of 83D0, so $2 \cdot 2^{12} = 8192$ calls instead of $2^{24}$. The first pair leaves 291 candidates, close to the expected $2^{24}/2^{16} = 256$. The second pair leaves exactly one, $(k_1, k_2)$ = (5A3, C17), and the third confirms it.

## Correctness

TDEA-DECRYPT undoes TDEA-ENCRYPT for every key bundle, because each step undoes the matching step in reverse order: $D_{K_1} \circ E_{K_2} \circ D_{K_3} \circ E_{K_3} \circ D_{K_2} \circ E_{K_1}$ is the identity, as $D_K \circ E_K$ and $E_K \circ D_K$ are both the identity. With $K_1 = K_2 = K$, line L2 undoes line L1, so keying option 3 gives $E_{K_3}$, which is single DES. The full proof, and the proof that the meet-in-the-middle attack finds the true key pair, are given below.

## Complexity

Each block costs 3 DES calls, so 48 Feistel rounds, against 16 for DES. The time is $\Theta(b)$ for $b$ blocks and the extra space is $\Theta(1)$ beyond the three key schedules. Triple DES is about three times slower than DES and much slower than [AES](/advanced-encryption-standard/) with hardware support.

**Cost of attacks.** The figures are in DES calls.

| target | attack | data | time | memory |
|---|---|---|---|---|
| double DES | meet in the middle | 2 known pairs | $2^{57}$ | $2^{56}$ |
| two-key TDEA | Merkle and Hellman 1981 | $2^{56}$ chosen | $2^{56}$ | $2^{56}$ |
| two-key TDEA | van Oorschot and Wiener 1990 | $n$ known | about $2^{120 - \lg n}$ | $n$ |
| three-key TDEA | meet in the middle | 3 known pairs | about $2^{112}$ | $2^{56}$ |
| three-key TDEA | Lucks 1998 | $2^{32}$ known | about $2^{90}$ DES calls and $2^{108}$ simple steps | $2^{88}$ |
| any mode with 64-bit blocks | birthday collision (Sweet32) | about $2^{32}$ blocks | negligible | the traffic |

For three keys, the attacker stores $E_{k_1}(x)$ for all $k_1$, and for each pair $(k_2, k_3)$ computes $E_{k_2}(D_{k_3}(y))$ and looks it up. In the ideal cipher model, Bellare and Rogaway (2006) proved that an adversary needs about $2^{k + \min(k, n)/2} = 2^{78}$ queries to break the cascade of three encryptions, for $k = 56$ and $n = 64$.

## Properties

- **Backward compatible.** With $K_1 = K_2 = K_3$ the result is single DES. This was the reason for the EDE order.
- **Same structure as DES.** TDEA inherits the complementation property: $\mathrm{TDEA}_{\bar K_1, \bar K_2, \bar K_3}(\bar x)$ is the complement of $\mathrm{TDEA}_{K_1, K_2, K_3}(x)$, since $D_{\bar K}(\bar y) = \overline{D_K(y)}$ as well.
- **No group shortcut.** Since DES is not a group (Campbell and Wiener 1992), no single DES key equals a triple encryption, so the three layers really add key length.
- **64-bit block.** Under one key, about $q^2 / 2^{65}$ is the chance of a ciphertext block collision in $q$ blocks of CBC. A collision $C_i = C_j$ gives $P_i \oplus P_j = C_{i-1} \oplus C_{j-1}$. At $q = 2^{32}$, a collision is likely; at $q = 2^{20}$, the SP 800-67 Rev. 2 limit, the chance is about $2^{-25}$.

## Variants and improvements

- **EEE.** Three encryptions $E_{K_3}(E_{K_2}(E_{K_1}(x)))$. It has the same security against generic attacks, but loses the compatibility with single DES.
- **Two-key TDEA.** $K_3 = K_1$ saves key storage, but the Merkle and Hellman and the van Oorschot and Wiener attacks bring it well below 112 bits. NIST disallows it for encryption.
- **[DESX](/key-whitening/).** One DES call with whitening keys before and after. It is much faster than TDEA and also defeats exhaustive search in the ideal cipher model, but it is weaker against differential and linear cryptanalysis than TDEA.
- **AES.** The replacement. It has a 128-bit block, which removes the birthday problem, and is faster.

## When to use it

Use TDEA only to decrypt old data, or to work with legacy systems such as some payment card systems that cannot change yet. Do not use it for new encryption: NIST disallows three-key TDEA encryption after December 31, 2023. Use AES from a FIPS 140 validated module, or an authenticated cipher from libsodium.

## Pitfalls

- **Key order.** SP 800-67 encrypts with $K_1$ first and decrypts with $K_3$ first. Some libraries take the keys in the other order; test against the Appendix B vectors.
- **Two keys that are really one.** If $K_1 = K_2$ by accident, as in some 16-byte key formats that repeat 8 bytes, the result is single DES.
- **Too much data under one bundle.** Sweet32 recovered a two-block HTTP cookie from about 610 GB of 3DES-CBC traffic captured in 30.5 hours. Rekey well before $2^{32}$ blocks, and NIST says after $2^{20}$.
- **Parity bits.** As in DES, 24 of the 192 key bits do not affect the output.
- **Timing.** The DES S-box lookups leak through the cache. The study code with this page is not constant time and is for study only.

## Implementations

## History

Diffie and Hellman described the meet-in-the-middle attack on double encryption in 1977, in their paper on exhaustive search of DES. Walter Tuchman of IBM proposed the two-key encrypt, decrypt, encrypt scheme in 1978. Merkle and Hellman analyzed multiple encryption in 1981 and gave a chosen-plaintext attack on two-key TDEA; van Oorschot and Wiener gave a known-plaintext attack in 1990. ANSI X9.52 standardized TDEA in 1998, and NIST published SP 800-67 in 2004, with revisions in 2012 and 2017. Bhargavan and Leurent showed the Sweet32 attacks at ACM CCS 2016. NIST SP 800-131A Rev. 2 (2019) deprecated three-key TDEA encryption through 2023 and disallowed it after 2023, and NIST withdrew SP 800-67 Rev. 2 on January 1, 2024.

## References
