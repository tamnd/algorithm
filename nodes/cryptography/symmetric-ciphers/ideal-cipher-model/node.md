---
tag: 974R8X
kind: model
slug: ideal-cipher-model
name: Ideal cipher model
aliases:
- ideal block cipher model
area: cryptography/symmetric-ciphers
level: research
summary: A model in which the block cipher is a uniformly random family of permutations, one per key, that every party queries forward and backward. Proofs in it count queries; it is a heuristic.
history:
  year: 1949
  people: [Claude E. Shannon]
  note: Shannon analyzed a random cipher in 1949. The model became a tool for proofs from the 1990s, in work on DESX, Even-Mansour and block-cipher-based hash functions.
prereqs: [block-cipher, pseudorandom-permutation]
see_also: [random-oracle-model, indifferentiability-framework, key-whitening, davies-meyer-construction, feistel-network, exhaustive-key-search, triple-des, luby-rackoff-theorem]
sources:
  - paper: doi:10.1002/j.1538-7305.1949.tb00928.x
    title: Claude E. Shannon, Communication theory of secrecy systems, Bell System Technical Journal 28(4), 1949
    locator: the random cipher and its unicity distance
  - paper: "John Black, Phillip Rogaway and Thomas Shrimpton, Black-box analysis of the block-cipher-based hash-function constructions from PGV, Advances in Cryptology, CRYPTO 2002, LNCS 2442, Springer, 2002"
    locator: the collision and preimage bounds for the 64 PGV schemes in the ideal cipher model
  - paper: "Jean-Sébastien Coron, Jacques Patarin and Yannick Seurin, The random oracle model and the ideal cipher model are equivalent, Advances in Cryptology, CRYPTO 2008, LNCS 5157, Springer, 2008"
    locator: the claim that 6 Feistel rounds are indifferentiable from an ideal cipher and the attack on 5 rounds
  - paper: "Thomas Holenstein, Robin Künzler and Stefano Tessaro, The equivalence of the random oracle model and the ideal cipher model, revisited, STOC 2011, ACM, 2011"
    locator: the gap in the 6-round proof and the proof that 14 Feistel rounds are indifferentiable from an ideal cipher
  - paper: "Yuanxi Dai and John Steinberger, Indifferentiability of 8-round Feistel networks, Advances in Cryptology, CRYPTO 2016, LNCS 9814, Springer, 2016"
    locator: the proof for 8 rounds
  - paper: "Jean-Sébastien Coron, Yevgeniy Dodis, Cécile Malinaud and Prashant Puniya, Merkle-Damgård revisited: how to construct a hash function, Advances in Cryptology, CRYPTO 2005, LNCS 3621, Springer, 2005"
    locator: hash functions from an ideal cipher that are indifferentiable from a random oracle
  - paper: "John Black, The ideal-cipher model, revisited: an uninstantiable blockcipher-based hash function, Fast Software Encryption, FSE 2006, LNCS 4047, Springer, 2006"
    locator: a hash function that is secure in the ideal cipher model and insecure with every real block cipher
  - paper: doi:10.1007/s001450010015
    title: Joe Kilian and Phillip Rogaway, How to protect DES against exhaustive key search (an analysis of DESX), Journal of Cryptology 14(1), 2001
    locator: the ideal cipher model as used for the bound on DESX and FX
---

The ideal cipher model is a model of computation for cryptographic proofs in which a [block cipher](/block-cipher/) $E$ with $k$-bit keys and $n$-bit blocks is replaced by an oracle that, for every key $K$, computes an independent uniformly random permutation $E_K$ of $\{0,1\}^n$ and its inverse. Every party, including the adversary, may query $E_K(x)$ and $E_K^{-1}(y)$ for any key it likes. Security bounds in the model count oracle queries and allow unbounded computation. Shannon studied a random cipher in this sense in 1949, and the model is the standard setting for proofs about constructions that use a block cipher with keys the adversary knows or chooses: DESX, Even-Mansour, the PGV hash functions such as Davies-Meyer, and triple encryption. It is a heuristic: no real cipher is an ideal cipher, and there are schemes that are secure in the model but insecure with any real cipher. Through indifferentiability it is equivalent to the [random oracle model](/random-oracle-model/).

## The machine

**The oracle.** Let $\mathrm{BC}(k, n)$ be the set of all block ciphers with $k$-bit keys and $n$-bit blocks, that is, all maps $E : \{0,1\}^k \times \{0,1\}^n \to \{0,1\}^n$ with each $E_K$ a permutation. It has $((2^n)!)^{2^k}$ members. At the start, $E$ is chosen uniformly from $\mathrm{BC}(k, n)$. Equivalently, the $2^k$ permutations $E_K$ are independent and uniform in $\mathrm{Perm}(n)$.

**Queries.** Each party has two oracles.

- $E(K, x)$ returns $E_K(x)$.
- $E^{-1}(K, y)$ returns $E_K^{-1}(y)$.

**Lazy sampling.** A simulation keeps, for each key, a partial table of pairs $(x, y)$. A forward query $(K, x)$ not in the table gets $y$ uniform among the outputs not yet used under $K$; an inverse query gets $x$ uniform among the inputs not yet used under $K$. This gives exactly the same distribution of answers as a uniform $E$, and lets proofs use the identical-until-bad method of the [switching lemma](/prp-prf-switching-lemma/).

**Schemes and adversaries.** A scheme, such as a hash function $H^E$ or a cipher $\mathrm{FX}^E$, is an algorithm with oracle access to $E$. The secret keys of the scheme, if any, are chosen apart from $E$. The adversary is an algorithm with oracle access to $E$, $E^{-1}$ and the oracles of the security game, for example the encryption oracle of the scheme.

## What it counts

- **Queries to the ideal cipher.** The main resource is $q_E$, the number of queries to $E$ and $E^{-1}$. It stands for offline computation with the real cipher: each evaluation of AES by the attacker is one query.
- **Queries to the scheme.** The second resource is $q$ or $m$, the number of queries to the oracles of the game, such as known plaintext pairs. It stands for data.
- **Not time.** Computation between queries is free. Bounds hold for unbounded adversaries, so they are information-theoretic statements about query counts.
- **Success probability.** Results have the form: every adversary with $q_E$ cipher queries and $q$ game queries has advantage at most $\varepsilon(q_E, q)$. For example, a key recovery against $E$ itself succeeds with probability at most about $(q_E + q)/2^k$, which is what [exhaustive key search](/exhaustive-key-search/) achieves.

## Relation to other models

- **Standard model.** A proof in the standard model assumes only that $E$ is a [pseudorandom permutation](/pseudorandom-permutation/) under a secret uniform key. This covers modes of operation such as CTR and GCM. It says nothing when the adversary knows or chooses keys, as in hash functions built from a cipher, or when the key is short and the question is the cost of key search. The ideal cipher model covers these cases at the price of a stronger, idealized assumption.
- **Random permutation model.** The special case $k = 0$: one public random permutation $P$, queried both ways. Even-Mansour and sponge constructions are proved here.
- **Random oracle model.** A public uniformly random function $H$. Indifferentiability, defined by Maurer, Renner and Holenstein, makes the two models equivalent. A construction $C^P$ from an ideal primitive $P$ is indifferentiable from an ideal primitive $Q$ if a simulator $S^Q$ exists such that no distinguisher can tell $(C^P, P)$ from $(Q, S^Q)$ except with small advantage. Then any scheme secure with $Q$ in a single-stage game stays secure with $C^P$.
  - *From an ideal cipher to a random oracle.* Hash functions built from an ideal cipher in a suitable mode, for example Davies-Meyer compression in a prefix-free Merkle-Damgård mode, are indifferentiable from a random oracle (Coron, Dodis, Malinaud and Puniya 2005).
  - *From a random oracle to an ideal cipher.* A [Feistel network](/feistel-network/) whose round functions are random oracles, keyed through the oracle input, is indifferentiable from an ideal cipher if it has enough rounds. Coron, Patarin and Seurin (2008) claimed 6 rounds and showed that 5 are not enough. Holenstein, Künzler and Tessaro (STOC 2011) found a gap in the 6-round proof and proved the result for 14 rounds. Dai and Steinberger (CRYPTO 2016) proved it for 8 rounds. So the two models are equivalent: a scheme secure in one has a secure version in the other.
- **Note on the Luby-Rackoff theorem.** The [Luby-Rackoff theorem](/luby-rackoff-theorem/) needs only 3 or 4 rounds, because there the round functions are secret. Indifferentiability needs more rounds, because the adversary can query the round functions directly.
- **A heuristic.** The model treats a fixed, public algorithm such as AES as if it were a random family of permutations. Real ciphers have structure that no random cipher has: the complementation property of DES, the related-key differentials of AES-256, and known-key distinguishers. Black (2006) built a hash function that is secure in the ideal cipher model and insecure with every real block cipher, in the spirit of the result of Canetti, Goldreich and Halevi for random oracles. A proof in the model rules out generic attacks only.

## Known results in the model

| result | bound or statement |
|---|---|
| exhaustive key search | key recovery with $q_E$ cipher queries succeeds with probability at most about $(q_E + 1)/2^k$ |
| FX and DESX (Kilian and Rogaway 1996) | effective key length at least $k + n - 1 - \lg m$ with $m$ known pairs, so $119 - \lg m$ bits for DESX |
| Even-Mansour (random permutation model) | advantage at most $2 q_P q / 2^n$; Daemen's attack and the slide attack show this is tight. See [key whitening](/key-whitening/). |
| PGV hash functions (Black, Rogaway and Shrimpton 2002) | of the 64 schemes, 12 give collision-resistant compression functions, with advantage at most about $q^2/2^n$, and 8 more give collision-resistant hash functions when iterated; [Davies-Meyer](/davies-meyer-construction/) is among the 12 |
| triple encryption (Bellare and Rogaway 2006) | the cascade of three encryptions resists about $2^{k + \min(k, n)/2}$ queries, $2^{78}$ for DES |
| Feistel indifferentiability | 8 rounds with random oracles give an ideal cipher (Dai and Steinberger 2016); 5 rounds do not |

These results explain design choices in practice. SHA-1 and SHA-2 use Davies-Meyer compression, and its ideal cipher bounds are the main argument for that choice. DESX was a sound way to extend DES against key search. Triple DES with three keys was preferred over double DES because of the meet-in-the-middle attack, which also works in the model.

## References
