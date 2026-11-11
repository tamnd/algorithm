---
tag: H6EF3Q
kind: definition
slug: second-preimage-resistance
name: Second-preimage resistance
aliases:
- weak collision resistance
area: cryptography/hash-functions
level: intro
summary: "A hash is second-preimage resistant when, given a random message M, no efficient adversary can find M' != M with the same digest. Generic cost 2^n, less for long messages."
prereqs: [cryptographic-hash-function]
see_also: [collision-resistance, preimage-resistance, second-preimage-finding, merkle-damgard-construction, multicollision-attack, digital-signature, sponge-construction, universal-hashing]
sources:
  - paper: "Phillip Rogaway and Thomas Shrimpton, Cryptographic hash-function basics: definitions, implications, and separations for preimage resistance, second-preimage resistance, and collision resistance, FSE 2004, LNCS 3017, pages 371 to 388"
    locator: Section 3 (Sec, eSec and aSec), Proposition 6 (Coll implies Sec and eSec, and aSec and eSec imply Sec), Theorem 7, and the separations of Section 5
  - paper: "John Kelsey and Bruce Schneier, Second preimages on n-bit hash functions for much less than 2^n work, EUROCRYPT 2005, LNCS 3494, pages 474 to 490"
    locator: the attack on Merkle-Damgard hashes in about k 2^(n/2+1) + 2^(n-k+1) work for a target of 2^k blocks
  - paper: "Moni Naor and Moti Yung, Universal one-way hash functions and their cryptographic applications, STOC 1989, pages 33 to 43"
    locator: the definition of universal one-way hash functions (eSec), and signatures built from them
  - paper: "Mihir Bellare and Phillip Rogaway, Collision-resistant hashing: towards making UOWHFs practical, CRYPTO 1997, LNCS 1294, pages 470 to 484"
    locator: target collision resistance and the domain extension of UOWHFs
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2021
    locator: Section 6.1 (second-preimage resistance between collision resistance and preimage resistance)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 9.2 (the term weak collision resistance)
---

Second-preimage resistance is the property of a hash function that, given a random message $M$, no efficient adversary can find a different message $M' \ne M$ with $H(M') = H(M)$. The older name is weak collision resistance. It sits between the other two classic properties of a [cryptographic hash function](/cryptographic-hash-function/). It is weaker than [collision resistance](/collision-resistance/), because the adversary does not choose $M$, so the birthday paradox does not help, and the generic cost is about $2^n$ instead of $2^{n/2}$. It differs from [preimage resistance](/preimage-resistance/) in that the adversary gets $M$ itself and must return a different message. For a [Merkle-Damgard](/merkle-damgard-construction/) hash, a long target of $2^k$ blocks lowers the generic cost to about $2^{n-k}$, by Kelsey and Schneier (2005). The problem of breaking it is [second-preimage finding](/second-preimage-finding/).

## Definition

Let $H : \mathcal{K} \times \{0,1\}^* \to \{0,1\}^n$ be a family with public keys, and fix a message length $m$. Rogaway and Shrimpton give three versions.

**Sec.** The key and the target are both random:

$$\mathrm{Adv}^{\mathrm{sec}[m]}_H(A) = \Pr\left[K \leftarrow_\$ \mathcal{K};\ M \leftarrow_\$ \{0,1\}^m;\ M' \leftarrow A(K, M) : M' \ne M \text{ and } H_K(M') = H_K(M)\right].$$

**eSec (everywhere).** The adversary first chooses $M$, then gets a random key. This is target collision resistance, and a family that has it is a universal one-way hash function (Naor and Yung 1989).

**aSec (always).** The adversary first chooses the key, then gets a random $M$. This asks that every function of the family be second-preimage resistant, and it fits a fixed hash such as SHA-256.

$H$ is second-preimage resistant if the advantage is small for every adversary with reasonable resources. As with preimage resistance, the notion makes sense for a single unkeyed function, since the target is random.

**Generic bound.** For a random function, $q$ queries succeed with probability at most about $q/2^n$. For a Merkle-Damgard hash and a target of $2^k$ blocks, the Kelsey and Schneier attack costs about $k \cdot 2^{n/2+1} + 2^{n-k+1}$, so the length of the target counts. Hash designs that remove this loss use a wide internal state, a block counter, or a [sponge](/sponge-construction/) with a large capacity.

## Examples and non-examples

- **Believed second-preimage resistant.** SHA-256, SHA-512, SHA-3 and BLAKE2. No practical second preimage attack is known for MD5 or SHA-1 either, although both are broken for collisions. Their broken collision resistance is enough reason not to use them.
- **Collision resistant hashes.** Every collision resistant family is second-preimage resistant (Coll implies Sec). A second preimage for $M$ is a collision $(M, M')$.
- **Ignoring part of the input.** $G(x_1 \cdots x_m) = H(x_1 \cdots x_{m-1})$ is preimage resistant if $H$ is, but flipping the last bit gives a second preimage of any message. So preimage resistance does not imply second-preimage resistance.
- **One planted collision.** For a second-preimage-resistant $H$ and fixed $c \ne c'$, let $G(c) = H(c')$ and $G(x) = H(x)$ for other $x$. The pair $(c, c')$ is a collision of $G$, known to all. But a random target is $c$ or $c'$ with probability $2^{1-m}$, and for any other target, a second preimage of $G$ gives one of $H$. So $G$ is second-preimage resistant but not collision resistant.
- **Linear checksums.** For CRC-32, a second preimage of any message is found by solving a linear system. It has no resistance.

## Related definitions

| From | To | Holds? |
|---|---|---|
| Coll | Sec, eSec | yes (Proposition 6) |
| eSec, aSec | Sec | yes (Proposition 6) |
| Sec | Pre | up to $2^{n-m}$: $\mathrm{Adv}^{\mathrm{pre}} \le 2\,\mathrm{Adv}^{\mathrm{sec}} + 2^{n-m}$ (Theorem 7) |
| Sec | Coll | no (the planted collision above) |
| Pre | Sec | no (the ignored bit above) |

- **[Collision resistance](/collision-resistance/).** The adversary chooses both messages. Stronger, with generic cost $2^{n/2}$.
- **[Preimage resistance](/preimage-resistance/).** Only the digest is given, and any preimage wins.
- **Target collision resistance (eSec).** Can be built from any one-way function (Rompel 1990), and suffices for hash-then-sign when the signer picks a fresh key for each message, as in randomized hashing. Bellare and Rogaway (1997) gave practical domain extensions for it.
- **Use in signatures.** A [signature](/digital-signature/) on $H(M)$ for a message $M$ chosen by an honest signer needs second-preimage resistance to stop forgery of other messages. If the attacker can influence $M$, collision resistance is needed, which is why MD5 certificates fell.
- **[Universal hashing](/universal-hashing/).** For a secret random key, $\Pr_K[H_K(M) = H_K(M')]$ is small for any fixed $M \ne M'$. It is a statistical cousin of eSec with the key kept secret.

## References
