---
tag: BWP8XH
kind: algorithm
slug: bls-signature
name: BLS signature
aliases:
- Boneh-Lynn-Shacham signature
- BLS12-381 signature
area: cryptography/signatures
level: advanced
summary: "A pairing-based signature: sigma = H(m)^x, checked by e(sigma, g) = e(H(m), pk). One group element, unique, and many signatures aggregate into one. Used in Ethereum consensus."
model: word-ram
complexity:
  vars: {n: the number of binary digits of the group order}
  time: {worst: Θ(n^3), average: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: true, randomized: false}
history:
  year: 2001
  people: [Dan Boneh, Ben Lynn, Hovav Shacham]
  note: Presented at Asiacrypt 2001 and published in the Journal of Cryptology in 2004. Aggregation followed in 2003, threshold BLS in 2003, the curve BLS12-381 in 2017, and an IETF draft from 2019.
prereqs: [bilinear-pairing, computational-diffie-hellman, digital-signature]
see_also: [aggregate-signature, multisignature-problem, threshold-signature, batch-verification, miller-algorithm, random-oracle-model, proof-of-stake, schnorr-signature]
sources:
  - paper: "Dan Boneh, Ben Lynn and Hovav Shacham, Short signatures from the Weil pairing, ASIACRYPT 2001, LNCS 2248, Springer, pages 514 to 532"
    locator: the first version of the scheme, with the signature H(m)^x and the check by a pairing
  - paper: doi:10.1007/s00145-004-0314-9
    title: Dan Boneh, Ben Lynn and Hovav Shacham, Short signatures from the Weil pairing, Journal of Cryptology 17(4), 2004, pages 297 to 319
    locator: the scheme on gap co-Diffie-Hellman groups, the proof of security in the random oracle model with its loss, and the choice of curves
  - url: "https://datatracker.ietf.org/doc/draft-irtf-cfrg-bls-signature/"
    title: Boneh, Bradley, Gorbunov, Wahby, Wee, Wood and Zhang, BLS Signatures, Internet-Draft draft-irtf-cfrg-bls-signature-07, 2026 (a draft, not an RFC)
    locator: the core operations, the three schemes (basic, message augmentation, proof of possession) against rogue keys, and the ciphersuites on BLS12-381
  - url: "https://www.rfc-editor.org/rfc/rfc9380"
    title: Armando Faz-Hernandez, Sam Scott, Nick Sullivan, Riad S. Wahby and Christopher A. Wood, RFC 9380, Hashing to Elliptic Curves, 2023
    locator: the hash_to_curve functions and the suites for BLS12-381 G1 and G2 that the BLS draft uses
  - paper: "Dan Boneh, Craig Gentry, Ben Lynn and Hovav Shacham, Aggregate and verifiably encrypted signatures from bilinear maps, EUROCRYPT 2003, LNCS 2656, Springer, pages 416 to 432"
    locator: aggregation of BLS signatures on distinct messages
  - paper: "Thomas Ristenpart and Scott Yilek, The power of proofs-of-possession, securing multiparty signatures against rogue-key attacks, EUROCRYPT 2007, LNCS 4515, Springer, pages 228 to 245"
    locator: the proof of possession that stops rogue key attacks on BLS multisignatures
  - paper: "Dan Boneh, Manu Drijvers and Gregory Neven, Compact multi-signatures for smaller blockchains, ASIACRYPT 2018, LNCS 11273, Springer, pages 435 to 464"
    locator: the BLS multisignature with key coefficients that resists rogue keys in the plain public key model
  - url: "https://electriccoin.co/blog/new-snark-curve/"
    title: Sean Bowe, BLS12-381, New zk-SNARK Elliptic Curve Construction, Electric Coin Company blog, March 2017
    locator: the parameters of the curve BLS12-381
---

The BLS signature of Boneh, Lynn and Shacham (2001) signs a message by hashing it to a point of a group and raising that point to the secret key: $\sigma = H(m)^x$. Anyone checks it with a [bilinear pairing](/bilinear-pairing/) $e$: $e(\sigma, g) = e(H(m), pk)$ with $pk = g^x$. The signature is one group element, 48 bytes on BLS12-381, and for each message and key exactly one signature is valid. Because the check is a product of pairings, signatures of many signers multiply into one [aggregate signature](/aggregate-signature/), which is why Ethereum's proof of stake consensus uses BLS. It is EUF-CMA in the [random oracle model](/random-oracle-model/) if the [computational Diffie-Hellman](/computational-diffie-hellman/) problem is hard in the group, with a reduction that loses a factor of about the number of signing queries.

**Notation.** $G$ is a group of prime order $r$ with generator $g$, written multiplicatively as in the BLS paper. $e : G \times G \to G_T$ is a bilinear, non-degenerate, efficiently computable map: $e(g^a, g^b) = e(g, g)^{ab}$ and $e(g, g) \ne 1$. Real curves give an asymmetric pairing $e : G_1 \times G_2 \to G_T$; the steps are the same with the key and the signature in different groups. $H : \{0,1\}^* \to G$ is a hash to the group, $x \in [1, r-1]$ the secret key and $pk = g^x$.

## In plain words

The message is turned into a point of a special group by a hash. The signer multiplies that point by the secret number. That is the whole signature.

To check it without the secret, the verifier uses a pairing, a function that takes two points and lets numbers inside them move from one side to the other. The pairing of the signature with the public base point equals the pairing of the hashed message with the public key, because both hide the same product: message point times secret.

Many signatures can be added into one point, and the pairing checks them all together. A dishonest signer can fake a key that cancels other keys, so systems add one of three simple fixes.

## The problem

BLS solves the [digital signature](/digital-signature/) problem with very short signatures and with structure: signatures on many messages by many signers combine into one ([aggregate signature](/aggregate-signature/)), $t$ of $n$ shares combine into a signature under one key ([threshold signature](/threshold-signature/)), and a signature is unique, which makes it a verifiable random function in some uses.

## The algorithm

```pseudo id=main
KEYGEN()
L1  x ← uniform in [1, r − 1];  pk ← g^x;  return (x, pk)

SIGN(x, m)
L2  h ← H(m) ∈ G
L3  σ ← h^x;  return σ

VERIFY(pk, m, σ)
L4  if σ ∉ G or pk ∉ G or pk = 1 then return false
L5  h ← H(m)
L6  return e(σ, g) = e(h, pk)
```

**Why the check works.** $e(\sigma, g) = e(h^x, g) = e(h, g)^x = e(h, g^x) = e(h, pk)$ by bilinearity. The pairing lets the verifier test that $(g, pk, h, \sigma)$ is a Diffie-Hellman tuple, which is the decisional problem; the security rests on the computational problem of finding $h^x$ from $g, g^x, h$. Groups where the decisional problem is easy and the computational one is hard are called gap groups.

**BLS12-381.** Bowe (2017) designed the pairing friendly curve BLS12-381 for Zcash: a Barreto-Lynn-Scott curve of embedding degree 12 over a prime of 381 binary digits, with a prime subgroup order of 255 binary digits. Points of $G_1$ take 48 bytes compressed and points of $G_2$ 96 bytes. Current estimates put its security at about 117 to 120 binary digits after the improved number field sieve attacks on the target group. The IETF draft defines two variants: minimal signature size ($\sigma \in G_1$, $pk \in G_2$) and minimal public key size ($pk \in G_1$, $\sigma \in G_2$), which Ethereum uses.

**Hashing to the curve.** $H$ must behave as a random oracle into the group. The draft uses hash_to_curve from RFC 9380 (simplified SWU map to an isogenous curve, then clearing the cofactor), which takes constant time. The older try-and-increment method, which hashes with a counter until it hits an $x$ on the curve, leaks the message through timing.

**The IETF draft.** The draft draft-irtf-cfrg-bls-signature-07 (a draft, not an RFC) specifies KeyGen from a seed by HKDF, SkToPk, CoreSign, CoreVerify, Aggregate and CoreAggregateVerify, with KeyValidate that rejects the identity and points outside the subgroup, and three schemes against rogue keys.

### The rogue key attack and the three fixes

Several signers on the same message $m$ can multiply their signatures, $\sigma = \prod \sigma_i$, and a verifier can check $e(\sigma, g) = e(H(m), \prod pk_i)$. This is unsafe if keys are not checked: an attacker who sees an honest key $pk_1$ picks $\beta$ and announces the rogue key $pk^* = g^{\beta} / pk_1$. It knows no secret for $pk^*$, but the product of the keys is $g^{\beta}$, so $\sigma = H(m)^{\beta}$ verifies as a signature by both signers. The [multisignature problem](/multisignature-problem/) page treats this in general. The draft offers three schemes:

1. **Basic**: aggregate only signatures on distinct messages. AggregateVerify rejects a list with a repeated message. With distinct messages, BGLS (2003) proved aggregation secure without any key checks.
2. **Message augmentation**: each signer signs $pk_i \| m$. The messages now differ even when $m$ is the same, so the basic argument applies.
3. **Proof of possession (PoP)**: each signer publishes, once, a signature on its own public key under a separate hash domain. A rogue key has no known secret, so it has no proof. With proven keys, signatures on the same message aggregate with the fast check above (Ristenpart and Yilek, 2007). Ethereum's beacon chain uses this scheme.

A fourth fix, from Boneh, Drijvers and Neven (2018), weights each key by a hash of all the keys, $apk = \prod pk_i^{a_i}$, which works in the plain public key model without proofs.

## Example

The code uses a toy symmetric pairing: the curve $y^2 = x^3 + x$ over $\mathbb{F}_p$ with $p = 2305843081154396467$ (62 binary digits, $p \equiv 3 \bmod 4$), whose group of $p + 1$ points has a subgroup of prime order $r = 2147483659$. The distortion map $(x, y) \mapsto (-x, iy)$ with $i^2 = -1$ makes the reduced Tate pairing, computed by [Miller's algorithm](/miller-algorithm/), a symmetric map $G \times G \to \mathbb{F}_{p^2}^*$. This is not secure: discrete logs in both groups are easy at this size, and the hash is try-and-increment, not RFC 9380.

| step | value (in additive notation, $\sigma = x \cdot H(m)$) |
|---|---|
| generator $g$ | $(1801878418981150303, 1439449883564762898)$ |
| secret key $x$ | 1234567 |
| $pk = x \cdot g$ | $(1170081544000785331, 1102162133682722333)$ |
| $H(\text{"hi"})$ | $(983479099763344621, 2300073070106625736)$ |
| $\sigma = x \cdot H(\text{"hi"})$ | $(1544493870114847728, 559180719914778072)$ |
| $e(\sigma, g)$ | $1033196796202530200 + 1335882332243953737\,i$ |
| $e(H(\text{"hi"}), pk)$ | $1033196796202530200 + 1335882332243953737\,i$ |

The two pairing values are equal, so the signature verifies. The tests also check bilinearity, run the rogue key attack against the naive same-message check, and show that a proof of possession and message augmentation both stop it.

## Correctness

By bilinearity, $e(h^x, g) = e(h, g)^x = e(h, g^x)$, so an honest $\sigma = h^x$ passes line L6, and line L4 passes because $h \in G$ and $pk = g^x \ne 1$. The proof below also shows uniqueness: since $e(\cdot, g)$ is injective on $G$ when $e$ is non-degenerate, no other $\sigma' \in G$ passes for the same $pk$ and $m$.

## Complexity

Let $n$ be the number of binary digits of $r$ ($n = 255$ for BLS12-381).

- **Signing**: one hash to the curve and one scalar multiplication, $\Theta(n)$ group operations.
- **Verification**: two pairings, or one product of two Miller loops and one final exponentiation. A pairing on BLS12-381 costs several times one scalar multiplication, so BLS verification is much slower than Ed25519 or ECDSA verification.
- **Aggregation**: $N$ signatures on distinct messages need $N + 1$ pairings to verify; on the same message with proven keys, two pairings and $N - 1$ group multiplications of keys.
- **Sizes**: 48 bytes for a $G_1$ element and 96 bytes for a $G_2$ element on BLS12-381.
- **Time**: with schoolbook arithmetic each operation is $\Theta(n^3)$ word operations for fixed embedding degree, and space is $\Theta(n)$.

## Properties

- **EUF-CMA in the random oracle model under CDH.** If an adversary forges with probability $\varepsilon$ after $q_H$ hash queries and $q_S$ signing queries, the reduction of the BLS paper, with Coron's technique, solves (co-)CDH with probability about $\varepsilon / (e (q_S + 1))$, where $e \approx 2.718$, in about the same time. The reduction embeds the CDH challenge in a random fraction of the hash answers and knows the signatures of the others. The loss of about $q_S$ is necessary for this kind of reduction for unique signatures (Coron, 2002).
- **Unique and deterministic.** For each key and message exactly one valid signature exists. So BLS is [strongly unforgeable](/strong-unforgeability/) and can serve as a verifiable random function when combined with a hash.
- **Aggregation.** Signatures on distinct messages by distinct keys aggregate by multiplication. See [aggregate signatures](/aggregate-signature/).
- **Threshold friendly.** Signing is linear in $x$, so Shamir shares of $x$ give signature shares that combine by Lagrange interpolation in the exponent, in one round and without interaction (Boldyreva 2003). See [threshold signatures](/threshold-signature/).
- **Not quantum safe**, like every scheme based on discrete logs and pairings.

## Variants and improvements

- **BGLS aggregate signatures** (2003) and **sequential aggregates** (Lysyanskaya, Micali, Reyzin and Shacham, 2004).
- **Multisignatures**: same-message aggregation with PoP, or with the BDN coefficients.
- **Threshold BLS** (Boldyreva, 2003) and distributed key generation for it, used in randomness beacons.
- **Batch verification** of many BLS signatures with random weights; see [batch verification](/batch-verification/).
- **Signatures in $G_1$ or $G_2$**, the two variants of the IETF draft.

## When to use it

Use BLS when signatures must aggregate or be produced by a threshold of parties, and when verification time matters less than size: proof of stake consensus (Ethereum, and others), randomness beacons (drand), and certificates of many signers. For one signer and one verifier, [Ed25519](/ed25519/) or [Schnorr](/schnorr-signature/) are faster to verify and simpler. Use an audited library such as blst, with the ciphersuites of the IETF draft.

## Pitfalls

- **Rogue keys.** Same-message aggregation without PoP, message augmentation or key coefficients is broken, as the code shows.
- **No subgroup check.** Points outside the prime order subgroup (BLS12-381 has large cofactors) let attackers forge or split verifiers. KeyValidate and signature decoding must check subgroup membership.
- **The identity key.** A public key equal to the identity accepts the identity as a signature for every message; KeyValidate rejects it.
- **Hashing to the curve by try-and-increment** leaks timing and does not give a uniform point; use RFC 9380.
- **Splitting zero.** In aggregates, an attacker can give two signatures that are wrong but multiply to a right aggregate; aggregation proves only that the set was signed, not each member.
- **Mixing the variants.** A key for one ciphersuite must not be reused under another domain separation tag.

## Implementations

The Python code on this page implements BLS over a toy symmetric pairing with its own curve arithmetic, Miller loop and final exponentiation, the naive same-message aggregation with the rogue key attack, proofs of possession, and message augmentation. It is a toy: the groups are tiny, the pairing is symmetric unlike BLS12-381, the hash is try-and-increment rather than RFC 9380, and there are no official test vectors for it. It is for study only, not constant time, and must not be used to protect real data. Use blst or another audited library.

## History

Pairings entered cryptography as attacks (Menezes, Okamoto and Vanstone, 1993) and then as tools (Joux's three party key exchange in 2000, and the identity based encryption of Boneh and Franklin in 2001). Boneh, Lynn and Shacham presented short signatures from the Weil pairing at Asiacrypt 2001, with the journal version in 2004. Boneh, Gentry, Lynn and Shacham added aggregation in 2003, and Boldyreva gave threshold and multisignatures in the same year.

Bowe defined BLS12-381 in 2017. The IETF CFRG draft started in 2019, with RFC 9380 for hashing to curves in 2023. Ethereum's beacon chain launched with BLS signatures and proofs of possession in December 2020.

## References
