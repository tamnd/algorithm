---
tag: CZN1Q6
kind: algorithm
slug: forward-secure-signature
name: Forward-secure signature
aliases:
- key-evolving signature
- forward secure signature
- KES
area: cryptography/signatures
level: research
summary: "A signature whose secret key evolves each period through a one-way update while the public key stays fixed, so a key stolen today cannot sign for an earlier period."
model: word-ram
complexity:
  vars: {h: the logarithm of the number of periods, b: the logarithm of the keys per period, l: the number of Winternitz chains, w: the chain length}
  time: {worst: Θ(2^(h+b)·l·w), average: Θ(2^(h+b)·l·w), best: Θ(2^(h+b)·l·w)}
  space: {extra: Θ(2^h + 2^b)}
properties: {deterministic: true}
history:
  year: 1999
  people: [Ross Anderson, Mihir Bellare, Sara K. Miner]
  note: Anderson proposed forward-secure signatures in talks in 1997 and 1998. Bellare and Miner gave the formal model and the first schemes at Crypto 1999.
prereqs: [signature-scheme, merkle-signature-scheme]
see_also: [xmss, winternitz-one-time-signature, hash-chain, existential-unforgeability, perfect-forward-secrecy, digital-signature, threshold-signature, hash-based-signatures]
sources:
  - url: "https://doi.org/10.48456/tr-549"
    title: "Ross Anderson, Two remarks on public key cryptology, University of Cambridge Computer Laboratory Technical Report UCAM-CL-TR-549, December 2002"
    locator: the first remark, forward-secure signatures, the written record of the talks of 1997 and 1998
  - paper: doi:10.1007/3-540-48405-1_28
    title: "Mihir Bellare and Sara K. Miner, A forward-secure digital signature scheme, Crypto 1999, LNCS 1666, pages 431 to 448"
    locator: the key-evolving model and the definition of forward security, the generic tree-based scheme, and the factoring-based scheme in the random oracle model
  - paper: doi:10.1007/3-540-44647-8_20
    title: "Gene Itkis and Leonid Reyzin, Forward-secure signatures with optimal signing and verifying, Crypto 2001, LNCS 2139, pages 332 to 354"
    locator: a scheme based on Guillou and Quisquater with signing and verification as fast as the ordinary scheme
  - paper: doi:10.1007/3-540-46035-7_27
    title: "Tal Malkin, Daniele Micciancio and Sara K. Miner, Efficient generic forward-secure signatures with an unbounded number of time periods, Eurocrypt 2002, LNCS 2332, pages 400 to 417"
    locator: sum and product composition, and a generic scheme without a fixed number of periods
  - paper: doi:10.1007/978-3-642-25405-5_8
    title: "Johannes Buchmann, Erik Dahmen and Andreas Hülsing, XMSS: A practical forward secure signature scheme based on minimal security assumptions, PQCrypto 2011, LNCS 7071"
    locator: XMSS with a forward-secure pseudorandom generator for the one-time keys
---

A forward-secure signature, or key-evolving signature, splits the lifetime of a key into periods $0, 1, \ldots, T - 1$. The public key never changes, but at the end of each period the signer runs a one-way update on its secret key and erases the old one. Each signature carries its period. If an attacker steals the secret key in period $\beta$, it can sign for periods $\beta$ and later, but not for any earlier period, so signatures made before the theft stay trustworthy. Anderson proposed the idea in 1997; Bellare and Miner (1999) defined it and gave the first schemes. This page shows a simple tree-based construction from hash functions.

**Notation.** $T = 2^h$ is the number of periods and $2^b$ the number of signatures per period. $s_t$ is the seed of period $t$, $G$ is a one-way function (here SHA-256 with a tag), $SK_t$ is the secret key of period $t$ and $PK$ the public key. A [Winternitz one-time signature](/winternitz-one-time-signature/) (a key made of hash chains that signs one message) has $l$ chains of length $w$. The security model is the forward-secure EUF-CMA game of Bellare and Miner.

## In plain words

An ordinary signing key that leaks makes every signature doubtful, even old ones, because nobody can tell whether the thief made them. Revocation does not help for old documents.

A forward-secure key changes every day, like a diary that burns yesterday's page. Today's key can be made from yesterday's key, but yesterday's key cannot be made from today's. Every signature says on which day it was made. A thief who takes the key today can sign for today and for the days that follow, until the key is revoked, but it cannot sign as if it were last week.

The public key stays the same for the whole life of the key, so verifiers do not need new certificates.

## The problem

A key-evolving signature scheme has four algorithms: key generation gives $PK$ and $SK_0$; the update maps $SK_t$ to $SK_{t+1}$ and erases $SK_t$; signing with $SK_t$ gives a signature $(t, \sigma)$; and verification checks $(t, \sigma)$ on a message with $PK$. In the forward-security game of Bellare and Miner, the attacker gets $PK$, asks for signatures in periods of its choice as the key evolves, and then breaks in at a period $\beta$ of its choice and gets $SK_\beta$. It wins if it outputs a valid signature for a period $t < \beta$ on a message that was not signed in period $t$. The scheme is forward secure if every efficient attacker wins with negligible chance. Signatures for periods $t \ge \beta$ are not protected.

## The algorithm

The construction below has a top Merkle tree with one leaf per period. Leaf $t$ is the root of a period tree of $2^b$ Winternitz keys that come from the seed $s_t$, and the seeds form a one-way chain.

```pseudo id=main
KEYGEN(h, b)
L1  s_0 ← random seed
L2  for t ← 0 to 2^h − 1: ρ_t ← root of the period tree of 2^b Winternitz keys made from s_t; s_{t+1} ← G(s_t)
L3  PK ← root of the Merkle tree on ρ_0, …, ρ_{2^h−1}; SK_0 ← (0, s_0, nodes of the top tree); erase s_1, s_2, …

UPDATE(SK_t)
L4  if t = 2^h − 1 then stop; s_{t+1} ← G(s_t); rebuild the period tree of t + 1 from s_{t+1}
L5  erase s_t; t ← t + 1

SIGN(SK_t, M)
L6  j ← next unused key of period t; fail if all 2^b keys are used
L7  σ ← Winternitz signature of H(M) with key (t, j) made from s_t
L8  return (t, j, σ, path of leaf j in the period tree, path of leaf t in the top tree)

VERIFY(PK, M, (t, j, σ, p, P))
L9  λ ← leaf from σ and H(M); ρ ← climb from λ with p and index j
L10 return climb from ρ with P and index t = PK
```

Every hash takes its position (period, key, chain, step, tree height and index) as input, so period $t$'s keys cannot stand in for those of another period. The nodes of the top tree are public and can be stored with the key. The secret part of $SK_t$ is only $s_t$ and the counter $j$.

## Example

Take $h = 3$ (8 periods) and $b = 1$ (2 signatures per period). The signer signs two messages in each of periods 0 to 3, updating at the end of each. In period 4, an attacker breaks in and copies $SK_4 = (4, s_4, \text{top tree})$.

- The attacker can sign for period 4, and also for period 7 by computing $s_7 = G(G(G(s_4)))$. Forward security does not protect the future; the key must be revoked.
- To sign for period 1 the attacker needs $s_1$, but $s_4 = G(G(G(s_1)))$, so it would have to invert $G$ three times. Using $s_4$ in place of $s_1$ makes keys whose leaves do not match the period tree of period 1, and verification fails.
- The eight signatures of periods 0 to 3 still verify, and the verifier can trust them.

With a fixed master seed and $s_t = H(\text{master}, t)$, as in the key generation of RFC 8391, the stolen key contains the master seed, and the attacker signs for period 0 at once. The tests show both cases.

## Correctness

**Correctness.** After $t$ updates the signer holds $s_t$, because each update applies $G$ once. The signature in period $t$ is a Winternitz signature with a key made from $s_t$, so the verifier rebuilds leaf $\lambda_{t,j}$; the period tree that the signer built from $s_t$ is the same one whose root key generation put at leaf $t$ of the top tree, so the two climbs end at $PK$.

**Forward security.** With $H$ and $G$ modelled as random oracles, the stolen key reveals $s_\beta$ and public nodes. The earlier seeds are linked to it only through $s_\beta = G^{\beta - t}(s_t)$, so they stay hidden unless the attacker inverts $G$. A forgery for an earlier period then needs a forged Winternitz signature or a collision in a tree. The full argument is in the proof below.

## Complexity

For the construction on this page, key generation builds all $2^{h+b}$ Winternitz keys, $\Theta(2^{h+b} \cdot l \cdot w)$ hash calls. An update rebuilds one period tree, $\Theta(2^b \cdot l \cdot w)$; signing costs $\Theta(l \cdot w)$; verification costs $\Theta(l \cdot w + b + h)$. The signature has $l + b + h$ hash values. Key generation can be cut to the first period with a tree traversal or a multi-tree layout, as in XMSS$^{MT}$.

Other schemes trade these costs differently:

| scheme | assumption | main feature |
|---|---|---|
| Bellare and Miner tree scheme (1999) | any signature scheme | signatures carry a certificate chain of length about $\log T$ |
| Bellare and Miner (1999) | factoring, random oracle | short keys; signing and verification grow with $T$ |
| Itkis and Reyzin (2001) | strong RSA, random oracle | signing and verification as fast as Guillou and Quisquater; the cost moves to the update |
| Malkin, Micciancio and Miner (2002) | any signature scheme | no fixed bound on the number of periods |
| XMSS with a forward-secure generator (2011) | hash functions | post-quantum; one message per one-time key |

## Properties

- **Fixed public key.** Only the secret key changes; verifiers need no new certificate per period.
- **One-way update.** The update must be hard to reverse; erasure of the old secret is part of the scheme, not an option.
- **No post-compromise security.** After a break-in, the attacker can sign for the current and all later periods. Revocation is still needed.
- **Periods are public.** Each signature names its period, and the verifier must also check that the period fits the claimed time of the document.
- **Bounded number of periods.** Most schemes fix $T$ at key generation; the composition of Malkin, Micciancio and Miner removes the bound.

## Variants and improvements

- **Generic constructions.** Bellare and Miner certify period keys with a binary tree of ordinary signatures; Krawczyk (CCS 2000) uses one ordinary key that certifies $T$ fresh keys at once; Malkin, Micciancio and Miner (Eurocrypt 2002) give sum and product compositions with an unbounded number of periods.
- **Number-theoretic schemes.** Bellare and Miner (factoring), Abdalla and Reyzin (Asiacrypt 2000, shorter keys), and Itkis and Reyzin (Crypto 2001, signing and verification as fast as Guillou and Quisquater).
- **Hash-based schemes.** [XMSS](/xmss/) in its 2011 form is forward secure: the one-time keys come from a forward-secure pseudorandom generator, and used seeds are erased. The key generation of RFC 8391 from one fixed seed is not forward secure.
- **Key-insulated and intrusion-resilient signatures.** A helper device stores a second secret that refreshes the key, so that the signer's key alone does not reveal other periods, past or future.
- **Forward-secure group, threshold and aggregate signatures.** The same idea combined with other properties, used for secure logs and sensor networks.

## When to use it

Use forward-secure signatures where old signatures must stay valid after a later key theft: audit logs and secure logging, timestamping, signing devices that may be captured, and proof-of-stake blockchains, where an attacker who steals old validator keys could otherwise rewrite history. For example, the Cardano Ouroboros Praos protocol uses a key-evolving signature built from the sum composition of Malkin, Micciancio and Miner. Do not confuse it with perfect forward secrecy in key exchange, which protects past session keys, not past signatures.

## Pitfalls

- **No real erasure.** Old keys that stay in swap files, backups, snapshots or logs remove all protection. Python cannot erase memory, so the code here only models it.
- **Backups of the evolving key.** A backup taken in period $t$ holds $s_t$; if it leaks, all later periods are lost. With stateful one-time keys, a restored backup also reuses keys.
- **Period not checked against time.** A thief can sign for a later period and backdate within it; verifiers must compare the period with a trusted time.
- **Fixed-seed derivation.** Deriving all period keys from one master seed that stays in the key destroys forward security.
- **Missed updates.** If the update is late, the key of the old period stays exposed longer.

## Implementations

The Python code is for study only. It is not constant time, and it must not protect real data. It is a simple tree-based construction in the spirit of the generic tree schemes and of forward-secure XMSS, with SHA-256 from hashlib, Winternitz keys with $w = 16$, and a seed chain $s_{t+1} = G(s_t)$; it is not the exact scheme of any paper and has no official test vectors. The tests show round trips in all eight periods, that a key stolen in period 4 signs for periods 4 and 7 but not for periods 0 to 3, and that a fixed master seed allows back-dated signatures.

## History

Ross Anderson proposed forward-secure signatures in talks in 1997 and 1998 (Bellare and Miner credit an invited lecture at ACM CCS 1997) and wrote them up in 2002. Mihir Bellare and Sara Miner gave the formal model, a generic tree-based scheme and an efficient factoring-based scheme at Crypto 1999. Abdalla and Reyzin (2000), Krawczyk (2000), Itkis and Reyzin (2001), and Malkin, Micciancio and Miner (2002) improved the costs and removed the bound on periods. Buchmann, Dahmen and Hülsing (2011) made XMSS a practical forward-secure scheme from hash functions only.

## References
