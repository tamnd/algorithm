---
tag: SPPXKV
kind: definition
slug: collision-resistance
name: Collision resistance
aliases:
- collision-resistant hash
area: cryptography/hash-functions
level: intro
summary: "A hash is collision resistant when no efficient adversary can find two different inputs with the same digest. Generic attacks need about 2^(n/2) calls."
prereqs: [cryptographic-hash-function]
see_also: [second-preimage-resistance, preimage-resistance, collision-finding, birthday-attack, merkle-damgard-theorem, universal-hashing, multicollision-attack, random-oracle-model]
sources:
  - paper: "Phillip Rogaway and Thomas Shrimpton, Cryptographic hash-function basics: definitions, implications, and separations for preimage resistance, second-preimage resistance, and collision resistance, FSE 2004, LNCS 3017, pages 371 to 388"
    locator: Section 3 (the definition of Coll for a keyed family), Proposition 6 (Coll implies Sec and eSec), Theorem 7 (Coll implies Pre, up to 2^(n-m)), Theorem 13 (Coll does not imply ePre)
  - paper: "Phillip Rogaway, Formalizing human ignorance: collision-resistant hashing without the keys, VIETCRYPT 2006, LNCS 4341, pages 211 to 228"
    locator: Section 1 (the foundations-of-hashing dilemma) and the explicit reductions for unkeyed hash functions
  - paper: "Ivan B. Damgard, Collision free hash functions and public key signature schemes, EUROCRYPT 1987, LNCS 304, pages 203 to 216"
    locator: the first formal definition of collision-free hash families, with a public key
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Section 6.1 (hash functions and collision resistance as a keyed family, and the weaker notions)
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography
    locator: Chapter 8 (collision resistance and the birthday attack)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 9.2 (basic properties and definitions of hash functions)
---

Collision resistance is the property of a hash function that no efficient adversary can find two different inputs $M \ne M'$ with the same digest. It is the strongest of the three classic properties of a [cryptographic hash function](/cryptographic-hash-function/). Since the domain is larger than the range, collisions always exist, so the property is about the cost of finding one. For any hash with $n$-bit output, the [birthday attack](/birthday-attack/) finds a collision in about $2^{n/2}$ calls, so collision resistance can never exceed $n/2$ bits of security. It implies [second-preimage resistance](/second-preimage-resistance/), and it implies [preimage resistance](/preimage-resistance/) only when the hash compresses enough. Hash-then-sign, commitments and Merkle trees rely on it. The problem of breaking it is [collision finding](/collision-finding/).

## Definition

**Keyed form.** Let $H : \mathcal{K} \times \mathcal{M} \to \{0,1\}^n$ be a family of functions, with $H_K = H(K, \cdot)$. The key $K$ is public; it only selects one function from the family. For an adversary $A$, its collision advantage is

$$\mathrm{Adv}^{\mathrm{coll}}_H(A) = \Pr\left[K \leftarrow_\$ \mathcal{K};\ (M, M') \leftarrow A(K) : M \ne M' \text{ and } H_K(M) = H_K(M')\right].$$

$H$ is collision resistant if this advantage is small for every adversary with reasonable resources. Asymptotically, Katz and Lindell ask that it be negligible in the security parameter for every probabilistic polynomial-time $A$. Concretely, Rogaway and Shrimpton call it Coll and state bounds in terms of time.

**Why a key.** For a single fixed function such as SHA-256, a collision $(M, M')$ exists, so the adversary that prints it has advantage 1 and runs in constant time. Under the plain definition, no fixed hash is collision resistant. The key avoids this: the adversary must find a collision after the function is chosen.

**Unkeyed form.** Rogaway (2006) treats real, unkeyed hashes in another way. One cannot say that no efficient adversary finds a collision, but one can give an explicit reduction: an algorithm that turns any collision finder $A$ for $H$ into a solver $B$ for the problem of the scheme, with $B$ about as efficient as $A$. If nobody knows a collision of $H$, nobody can run such an $A$, so the scheme is as secure as our ignorance of collisions. This "human ignorance" view justifies proofs that use SHA-256 directly.

**Generic bound.** For a random function with $n$-bit output, an adversary with $q$ queries succeeds with probability at most $q(q-1)/2^{n+1}$, and the birthday attack achieves about $1 - e^{-q^2/2^{n+1}}$. So $n$-bit collision resistance means $n/2$ bits of security. For 128-bit security a hash needs $n \ge 256$.

## Examples and non-examples

- **Believed collision resistant.** SHA-256, SHA-512, SHA-3 and BLAKE2 with full output. No collision is known for any of them.
- **Broken.** MD5 and SHA-1 have practical collisions, found by cryptanalysis (2004 to 2005 for MD5, 2017 for SHA-1). MD4 collisions can be found by hand.
- **Too short.** SHA-256 cut to 64 bits is a good hash, but $2^{32}$ calls give a collision, so it is not collision resistant at any useful level.
- **Linear checksums.** CRC-32 is linear over GF(2), so collisions are solutions of a linear system. It is not collision resistant at all.
- **Injective but not compressing.** The identity map on $\{0,1\}^n$ has no collisions, so it is collision resistant in the trivial sense. It is useless as a hash and has no other property: anyone can invert it. This is why the implication to preimage resistance needs compression.
- **From hard problems.** $H(x, y) = g^x h^y$ in a group of prime order, with public $g$ and $h$, is collision resistant if discrete logarithms are hard, since a collision gives $\log_g h$. It is a keyed family with $K = (g, h)$.

## Related definitions

The diagram of Rogaway and Shrimpton for a keyed family, with Sec and Pre for random messages of length $m$:

| From | To | Holds? |
|---|---|---|
| Coll | Sec, eSec | yes (Proposition 6) |
| Coll | Pre | only up to an additive $2^{n-m}$ (Theorem 7) |
| Coll | ePre | no (Theorem 13) |
| Sec | Coll | no |
| Pre | Coll | no |

A counterexample for Sec not implying Coll: take a second-preimage-resistant family $H$ and fixed messages $c \ne c'$, and set $G_K(c) = H_K(c')$ and $G_K(x) = H_K(x)$ elsewhere. Then $(c, c')$ is a collision for every key, but a random target hits $c$ or $c'$ with tiny probability, so $G$ stays second-preimage resistant. A counterexample for Pre not implying Coll: $G_K(x_1 \cdots x_m) = H_K(x_1 \cdots x_{m-1})$, which collides on the last bit but is as hard to invert as $H$.

- **[Second-preimage resistance](/second-preimage-resistance/).** The target is given; weaker than collision resistance, with generic cost $2^n$ instead of $2^{n/2}$.
- **[Preimage resistance](/preimage-resistance/).** Only a digest is given.
- **Target collision resistance (eSec).** The adversary commits to $M$, then gets $K$, and must find $M' \ne M$ with the same hash. Also called a universal one-way hash function (Naor and Yung 1989). It is weaker than collision resistance, and it can be built from any one-way function, while collision resistance is not known to follow from one-way functions.
- **[Universal hashing](/universal-hashing/).** A statistical property of a family with a secret key: for $M \ne M'$, $\Pr_K[H_K(M) = H_K(M')]$ is small. It needs no computational assumption, but it is lost once the key is public.
- **Multicollision and near-collision resistance.** No efficient adversary finds $t$ inputs with one digest, or two inputs with close digests. See [multicollision attack](/multicollision-attack/).
- **Preservation.** The [Merkle-Damgard theorem](/merkle-damgard-theorem/) states that a Merkle-Damgard hash with length padding is collision resistant if its compression function is.

## References
