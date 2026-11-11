---
tag: YZD6T5
kind: definition
slug: block-cipher
name: Block cipher
aliases:
- keyed permutation
area: cryptography/symmetric-ciphers
level: intro
summary: A family of permutations of n-bit blocks, one for each k-bit key, that is fast to compute both ways. Its security goal is to look like a random permutation.
prereqs: [symmetric-encryption]
see_also: [pseudorandom-permutation, feistel-network, substitution-permutation-network, advanced-encryption-standard, data-encryption-standard, ecb-mode, ideal-cipher-model, key-schedule]
sources:
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 3 (pseudorandom permutations and block ciphers) and Chapter 7 (practical constructions of block ciphers)
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 4, block ciphers
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 7, block ciphers
  - paper: doi:10.6028/NIST.FIPS.197-upd1
    title: NIST, FIPS 197, Advanced Encryption Standard (AES), November 2001, updated May 2023
    locator: Section 1 and Section 5 (block length 128, key lengths 128, 192 and 256)
---

A block cipher is a family of permutations $E_K$ of the set of $n$-bit strings, one for each $k$-bit key $K$, such that both $E_K$ and its inverse are fast to compute. Its security goal is to be a strong [pseudorandom permutation](/pseudorandom-permutation/): with the key secret, $E_K$ and $E_K^{-1}$ must look like a random permutation and its inverse. A block cipher alone is not an [encryption scheme](/symmetric-encryption/): it is deterministic and fixes the input length, so it is used inside a mode of operation.

## Definition

**Notation.** $n$ is the block length and $k$ the key length, both in bits; $K$ is a key, $\mathcal{A}$ an adversary that makes $q$ queries and runs in time $t$, and $\mathrm{Perm}(n)$ is the set of all permutations of $\{0,1\}^n$.

A **block cipher** is a pair of deterministic algorithms $E, D : \{0,1\}^k \times \{0,1\}^n \to \{0,1\}^n$ such that for every key $K$, the map $E_K = E(K, \cdot)$ is a permutation of $\{0,1\}^n$ and $D_K = E_K^{-1}$. That is, $D_K(E_K(x)) = x$ for all $K$ and $x$.

**Security.** A block cipher is a fixed object with fixed $n$ and $k$, so its security is stated in the concrete form. The PRP advantage of $\mathcal{A}$ is

$$\mathrm{Adv}^{\mathrm{prp}}_E(\mathcal{A}) = \Bigl|\Pr_{K}\bigl[\mathcal{A}^{E_K} = 1\bigr] - \Pr_{\pi \leftarrow \mathrm{Perm}(n)}\bigl[\mathcal{A}^{\pi} = 1\bigr]\Bigr|,$$

and the strong PRP advantage $\mathrm{Adv}^{\mathrm{sprp}}_E(\mathcal{A})$ is the same with oracles $(E_K, E_K^{-1})$ and $(\pi, \pi^{-1})$. $E$ is a $(t, q, \varepsilon)$-secure (strong) PRP if each adversary with time $t$ and $q$ queries has advantage at most $\varepsilon$. The exact games are on the page [pseudorandom permutation](/pseudorandom-permutation/).

**What "secure" can mean.** Two generic attacks bound every block cipher from below:

- [Exhaustive key search](/exhaustive-key-search/): try $t$ keys on the answers to a few queries. The advantage is about $t/2^k$, with $t$ counted in evaluations of $E$.
- No birthday attack works against the PRP game itself, but a PRP used as a PRF can be told apart from a random function after about $2^{n/2}$ queries, by the [PRP/PRF switching lemma](/prp-prf-switching-lemma/).

A block cipher is called secure when no attack is known that does much better than these generic attacks.

**Size.** There are $(2^n)!$ permutations of $n$-bit strings, but only $2^k$ keys. For $n = 64$, $\log_2 (2^{64})! \approx 2^{69.97}$, while DES has $2^{56}$ keys. So a block cipher picks a tiny subset of all permutations, and its design must make this subset look random. The [ideal cipher model](/ideal-cipher-model/) replaces it by $2^k$ independent random permutations.

## Examples and non-examples

- **AES.** $n = 128$ and $k \in \{128, 192, 256\}$, built as a [substitution-permutation network](/substitution-permutation-network/). See [AES](/advanced-encryption-standard/).
- **DES.** $n = 64$ and $k = 56$ (the key has 64 bits, 8 of which are parity bits), built as a 16-round [Feistel network](/feistel-network/). It is broken by key search. See [DES](/data-encryption-standard/).
- **Triple DES.** $n = 64$ and a 168-bit key bundle, with about $2^{112}$ security against [meet-in-the-middle](/meet-in-the-middle-attack/) search. See [Triple DES](/triple-des/).
- **A toy cipher.** The 16-bit SPN of Heys's tutorial is a block cipher with $n = 16$. It meets the syntax but is not secure for any purpose: $2^{16}$ queries list the whole permutation.
- **Non-example: XOR with the key.** $E_K(x) = x \oplus K$ with $k = n$ is a family of permutations, so it meets the syntax. It is not a PRP. Query two distinct inputs $x, x'$ and output 1 when $E(x) \oplus E(x') = x \oplus x'$. Under $E_K$ this always holds. Under a random permutation $\pi$, the value $\pi(x')$ is uniform on the $2^n - 1$ values other than $\pi(x)$, so it holds with probability $1/(2^n - 1)$. The advantage is $1 - 1/(2^n - 1)$ with $q = 2$. Each cipher that is linear or affine over GF(2) in its input falls to the same kind of test.
- **Non-example: a hash function.** A keyed hash $H_K(x)$ with $n$-bit output is not a block cipher, because it is not a permutation and has no inverse.
- **Non-example: a block cipher in ECB mode as an encryption scheme.** $E_K$ is deterministic, so encrypting the same block twice gives the same output, and [ECB mode](/ecb-mode/) is not IND-CPA secure. The fault is in the use, not in the cipher.

## Related definitions

- **[Pseudorandom permutation](/pseudorandom-permutation/)** and **strong PRP.** The formal security goals of a block cipher.
- **[Pseudorandom function](/pseudorandom-function/).** The goal of a keyed function that need not be invertible. A PRP on large $n$ is also a good PRF.
- **[Ideal cipher model](/ideal-cipher-model/).** A model in which the block cipher is a family of independent random permutations, used to analyze hash and whitening constructions.
- **[Feistel network](/feistel-network/)** and **[substitution-permutation network](/substitution-permutation-network/).** The two main ways to build a block cipher from rounds.
- **[Key schedule](/key-schedule/).** The map from the cipher key to the round keys.
- **Modes of operation.** [ECB](/ecb-mode/), [CBC](/cbc-mode/), [CTR](/ctr-mode/), [GCM](/gcm-mode/) and [XTS](/xts-mode/) turn a block cipher into an encryption scheme for messages of any length.

## References
