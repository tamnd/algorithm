---
tag: FWQ8A3
kind: definition
slug: preimage-resistance
name: Preimage resistance
aliases:
- one-wayness of hash
area: cryptography/hash-functions
level: intro
summary: "A hash is preimage resistant when, given the digest of a random input, no efficient adversary can find any input with that digest. Generic attacks need about 2^n calls."
prereqs: [cryptographic-hash-function]
see_also: [collision-resistance, second-preimage-resistance, preimage-finding, one-way-function, time-memory-tradeoff, password-hashing, commitment-scheme, random-oracle-model]
sources:
  - paper: "Phillip Rogaway and Thomas Shrimpton, Cryptographic hash-function basics: definitions, implications, and separations for preimage resistance, second-preimage resistance, and collision resistance, FSE 2004, LNCS 3017, pages 371 to 388"
    locator: Section 3 (Pre, ePre and aPre), Proposition 6 (aPre implies Pre), Theorem 7 (Sec, eSec, aSec and Coll imply Pre up to 2^(n-m)), Theorem 15 (the separations)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2021
    locator: Section 6.1 (preimage resistance as the weakest of the three notions) and Chapter 8 on one-way functions
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 9.2 (one-way hash functions, and the example of a collision resistant function that is not preimage resistant)
  - paper: "Gaetan Leurent, MD4 is not one-way, FSE 2008, LNCS 5086, pages 412 to 428"
    locator: a preimage attack on full MD4 in about 2^102
  - paper: "Yu Sasaki and Kazumaro Aoki, Finding preimages in full MD5 faster than exhaustive search, EUROCRYPT 2009, LNCS 5479, pages 134 to 152"
    locator: a preimage attack on full MD5 in about 2^123.4
---

Preimage resistance, or one-wayness, is the property of a hash function that, given the digest $y = H(M)$ of a random message $M$, no efficient adversary can find any message $M'$ with $H(M') = y$. It is the weakest of the three classic properties of a [cryptographic hash function](/cryptographic-hash-function/). The answer $M'$ may equal $M$, which is the difference from [second-preimage resistance](/second-preimage-resistance/). For a random function with $n$-bit output, the best attack is to try inputs, about $2^n$ calls, so preimage resistance can reach $n$ bits of security, against $n/2$ for [collision resistance](/collision-resistance/). It is defined for random inputs. It says nothing about inputs from a small set, such as passwords. The problem of breaking it is [preimage finding](/preimage-finding/).

## Definition

Let $H : \mathcal{K} \times \{0,1\}^* \to \{0,1\}^n$ be a family with public keys, and fix a message length $m$. Rogaway and Shrimpton give three versions.

**Pre.** The key and the message are both random:

$$\mathrm{Adv}^{\mathrm{pre}[m]}_H(A) = \Pr\left[K \leftarrow_\$ \mathcal{K};\ M \leftarrow_\$ \{0,1\}^m;\ Y \leftarrow H_K(M);\ M' \leftarrow A(K, Y) : H_K(M') = Y\right].$$

**ePre (everywhere).** The adversary first chooses the digest $Y$, then gets a random key, and must invert $Y$. This asks that every digest be hard to invert.

**aPre (always).** The adversary first chooses the key $K$, then gets $H_K(M)$ for a random $M$. This asks that every function of the family be one-way, which makes sense for a fixed hash such as SHA-256.

$H$ is preimage resistant if the advantage is small for every adversary with reasonable resources. For an unkeyed hash, aPre with the single key is the natural notion, and unlike collision resistance it is well defined, since a fixed hash still has a random target.

**Generic bound.** For a random function, $q$ queries succeed with probability about $q/2^n$. Grover search on a quantum computer needs about $2^{n/2}$ queries.

**Note on the distribution.** The target is $H(M)$ for uniform $M$, not a uniform $Y$. The two agree up to small factors for a good hash with $m \ge n$, but they differ for functions with uneven output.

## Examples and non-examples

- **Believed preimage resistant.** SHA-256, SHA-512, SHA-3 and BLAKE2. Also MD5 and SHA-1 in practice: the best preimage attacks are about $2^{123.4}$ for MD5 (Sasaki and Aoki 2009) and $2^{102}$ for MD4 (Leurent 2008), far beyond reach. MD5 is still broken for collisions and must not be used.
- **The identity map.** $H(x) = x$ on $\{0,1\}^n$ is collision resistant, since it is injective, but trivially invertible. So collision resistance alone does not give one-wayness.
- **A collision-resistant hash with easy preimages.** From the Handbook of Applied Cryptography: given a collision resistant $h$ with $n$-bit output, set $G(x) = 1 \,\|\, x$ if $x$ has $n$ bits and $G(x) = 0 \,\|\, h(x)$ otherwise. $G$ is collision resistant, and half of all digests, those that start with 1, are trivial to invert. So $G$ fails ePre. It does not contradict Theorem 7 below: for random long messages, the target almost never starts with 1.
- **Low-entropy inputs.** $H(\text{PIN})$ for a 4-digit PIN is inverted in $10^4$ tries, whatever the hash. Preimage resistance is about uniform inputs of length at least $n$. Password storage needs salts and slow [password hashing](/password-hashing/), and fixed functions inverted many times fall to a [time-memory tradeoff](/time-memory-tradeoff/).

## Related definitions

Implications from Rogaway and Shrimpton (with messages of $m$ bits and digests of $n$ bits):

| From | To | Holds? |
|---|---|---|
| aPre | Pre | yes (Proposition 6) |
| Coll, Sec, eSec, aSec | Pre | only up to $2^{n-m}$: $\mathrm{Adv}^{\mathrm{pre}} \le 2\,\mathrm{Adv}^{\mathrm{sec}} + 2^{n-m}$ (Theorem 7) |
| Coll | ePre | no (Theorem 13) |
| Pre | Sec, Coll | no (Theorem 15) |

The proof of Theorem 7: given a preimage finder $A$, pick a random $M$, give $A$ the digest $H(M)$, and output what it returns. If $H$ compresses by $m - n$ bits, most messages share their digest with many others, so $A$ returns a message different from $M$ with probability about $1/2$ or more. That is a second preimage. When $m \le n$, as for the identity map, the argument fails.

A counterexample for Pre not implying Sec: if $H$ is preimage resistant, so is $G(x_1 \cdots x_m) = H(x_1 \cdots x_{m-1})$, which ignores the last bit. But flipping the last bit of any message gives a second preimage of $G$.

- **[One-way function](/one-way-function/).** The general notion: a function easy to compute and hard to invert on random inputs. A preimage-resistant hash is a one-way function that also compresses.
- **[Second-preimage resistance](/second-preimage-resistance/).** The original message is given, and the answer must differ from it.
- **[Collision resistance](/collision-resistance/).** No target at all.
- **Hiding.** A [commitment](/commitment-scheme/) $H(r \,\|\, m)$ needs more than one-wayness: it must reveal nothing about $m$, not only resist full inversion. Proofs often use the [random oracle model](/random-oracle-model/) for this.

## References
