---
tag: YB3MDA
kind: algorithm
slug: aggregate-signature
name: Aggregate signature
aliases:
- signature aggregation
- BGLS aggregate signature
area: cryptography/signatures
level: research
summary: "Combine N signatures by N signers on N messages into one short signature. BGLS multiplies BLS signatures and checks one product of pairings; messages must be distinct or keys proven."
model: word-ram
complexity:
  vars: {n: the number of binary digits of the group order}
  time: {worst: Θ(n^3), average: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: true, randomized: false}
history:
  year: 2003
  people: [Dan Boneh, Craig Gentry, Ben Lynn, Hovav Shacham]
  note: BGLS aggregate signatures appeared at Eurocrypt 2003. Lysyanskaya, Micali, Reyzin and Shacham gave sequential aggregates in 2004. Ethereum's beacon chain aggregates BLS signatures since 2020.
prereqs: [bls-signature, bilinear-pairing]
see_also: [multisignature-problem, musig, threshold-signature, batch-verification, proof-of-stake, quorum-certificate, schnorr-signature]
sources:
  - paper: "Dan Boneh, Craig Gentry, Ben Lynn and Hovav Shacham, Aggregate and verifiably encrypted signatures from bilinear maps, EUROCRYPT 2003, LNCS 2656, Springer, pages 416 to 432"
    locator: the definition of aggregate signatures, the security game with chosen keys, the BLS based scheme, and the rule that the messages must be distinct
  - paper: "Anna Lysyanskaya, Silvio Micali, Leonid Reyzin and Hovav Shacham, Sequential aggregate signatures from trapdoor permutations, EUROCRYPT 2004, LNCS 3027, Springer, pages 74 to 90"
    locator: sequential aggregation, where each signer adds its signature to the aggregate it receives, from certified trapdoor permutations such as RSA
  - paper: "Mihir Bellare, Chanathip Namprempre and Gregory Neven, Unrestricted aggregate signatures, ICALP 2007, LNCS 4596, Springer, pages 411 to 422"
    locator: the proof that prefixing the public key to each message removes the distinct message rule
  - url: "https://datatracker.ietf.org/doc/draft-irtf-cfrg-bls-signature/"
    title: Boneh, Bradley, Gorbunov, Wahby, Wee, Wood and Zhang, BLS Signatures, Internet-Draft draft-irtf-cfrg-bls-signature-07, 2026 (a draft, not an RFC)
    locator: Aggregate, AggregateVerify and FastAggregateVerify, and the basic, message augmentation and proof of possession schemes
  - url: "https://github.com/ethereum/consensus-specs"
    title: Ethereum consensus specifications
    locator: the phase 0 beacon chain, the use of BLS12-381 with the proof of possession ciphersuite, and the aggregation of attestations
  - paper: "Dan Boneh, Manu Drijvers and Gregory Neven, Compact multi-signatures for smaller blockchains, ASIACRYPT 2018, LNCS 11273, Springer"
    locator: the key coefficients that make same-message aggregation safe in the plain public key model
  - paper: "Konstantinos Chalkias, Francois Garillot, Yashvanth Kondi and Valeria Nikolaenko, Non-interactive half-aggregation of EdDSA and variants of Schnorr signatures, CT-RSA 2021, LNCS 12704, Springer"
    locator: half aggregation of Schnorr signatures, which halves the total size without interaction
---

An aggregate signature scheme lets anyone compress $N$ signatures, made by $N$ signers on $N$ messages, into one signature of the size of a single one. The verifier gets the list of public keys and messages and the aggregate, and accepts only if every signer signed its message. Boneh, Gentry, Lynn and Shacham (BGLS, 2003) built the first scheme from [BLS signatures](/bls-signature/): the aggregate is the product of the signatures, and verification checks one equation with $N + 1$ pairings. Aggregation needs no interaction and no help from the signers. Blockchains use it to shrink blocks and certificates of many validators.

**Notation.** $G$ is a group of prime order $r$ with generator $g$ and a [bilinear pairing](/bilinear-pairing/) $e$, written multiplicatively. Signer $i$ has the secret key $x_i$ and the public key $pk_i = g^{x_i}$, and signs $m_i$ with the BLS signature $\sigma_i = H(m_i)^{x_i}$. $N$ is the number of signatures.

## In plain words

Each signer makes an ordinary BLS signature, a single point. Anyone, even someone who knows no secrets, multiplies all the points together into one point. The verifier pairs that one point with the base point and compares it with the product of the pairings of each hashed message with its signer's key. The two sides match only if every signature was right, or if the errors were planned to cancel.

The messages must all differ, or the keys must come with proofs that their owners know the secrets. Otherwise one cheater can choose a key that cancels the honest keys and sign for everybody.

## The problem

The goal is a scheme with an extra algorithm $\mathrm{Agg}$ that turns signatures $\sigma_1, \dots, \sigma_N$ into one aggregate $\sigma$, and $\mathrm{AggVerify}((pk_1, m_1), \dots, (pk_N, m_N), \sigma)$. Security in the chosen key model of BGLS: the adversary gets one honest key $pk_1$ and a signing oracle for it, may choose all the other keys as it likes, even without knowing their secrets, and wins if it outputs an aggregate that verifies on a list containing $(pk_1, m_1)$ for an $m_1$ it never asked to be signed. This is harder than ordinary [unforgeability](/existential-unforgeability/) because of the free choice of the other keys, which is the [multisignature problem](/multisignature-problem/) in general form.

## The algorithm

Key generation and signing are those of BLS.

```pseudo id=main
AGGREGATE(σ_1, ..., σ_N)
L1  σ ← σ_1 · σ_2 · … · σ_N;  return σ

AGGREGATE-VERIFY((pk_1, m_1), ..., (pk_N, m_N), σ)
L2  if m_1, ..., m_N are not all distinct then return false
L3  if σ ∉ G or some pk_i ∉ G then return false
L4  return e(σ, g) = Π_i e(H(m_i), pk_i)
```

**Why the distinct message rule.** Without line L2, take an honest key $pk_1$ and let the adversary announce $pk_2 = g^{\beta} / pk_1$, a key for which it knows no secret. For the same message $m$ on both, the right side of line L4 is $e(H(m), pk_1 \cdot pk_2) = e(H(m), g^\beta)$, so $\sigma = H(m)^\beta$, which the adversary computes alone, passes. With distinct messages, the hashes $H(m_i)$ are independent random points, and the BGLS proof shows that no such cancellation helps: a forger yields a CDH solver in the random oracle model.

**Removing the rule.** The distinct message rule is awkward when many signers sign the same thing, as in consensus. Three ways around it:

- **Message augmentation**: sign $pk_i \| m_i$ instead of $m_i$. The augmented messages always differ, and Bellare, Namprempre and Neven (2007) proved this secure with no restriction.
- **Proof of possession**: each key comes with a BLS signature on the key itself, checked once at registration. Then same-message aggregates can use FastAggregateVerify: $e(\sigma, g) = e(H(m), \prod_i pk_i)$, two pairings for any $N$.
- **Key coefficients**: weight each key by a hash of the whole key set (Boneh, Drijvers and Neven, 2018).

**Sequential aggregation.** Lysyanskaya, Micali, Reyzin and Shacham (LMRS, 2004) gave aggregates from trapdoor permutations such as RSA, where pairings are not needed but signers must sign in order: signer $i$ receives the aggregate $\sigma_{i-1}$, combines it with its message, and applies its trapdoor to produce $\sigma_i$. The verifier undoes the steps in reverse. This fits certificate chains and routing announcements, where the order is natural.

## Example

In the toy pairing group of the code (order $r = 2147483659$, not secure), two signers with $x_1 = 1111$ and $x_2 = 2222$ sign "alice pays bob" and "bob pays carol":

| item | value (additive notation) |
|---|---|
| $\sigma_1$ | $(71233457349279603, 1983420150349517799)$ |
| $\sigma_2$ | $(1180538197199823725, 768394226348273844)$ |
| $\sigma = \sigma_1 + \sigma_2$ | $(509617178391753419, 2219222789890113514)$ |
| $e(\sigma, g)$ | $1821205284372946678 + 238617430465922216\,i$ |

The product $e(H(m_1), pk_1) \cdot e(H(m_2), pk_2)$ gives the same element of $\mathbb{F}_{p^2}$, so the aggregate verifies. Changing a message, swapping the keys or removing one signature makes it fail.

The rogue key attack in the tests: the attacker sees $pk_1$, picks $\beta$ and registers $pk^* = \beta g - pk_1$ with no proof of possession. For one message $m$ it outputs $\beta H(m)$, which the verifier without line L2 accepts as an aggregate of both. With line L2, or with distinct messages, it fails.

## Correctness

If $\sigma_i = H(m_i)^{x_i}$ for each $i$, then

$$e\Big(\prod_i \sigma_i, g\Big) = \prod_i e(H(m_i)^{x_i}, g) = \prod_i e(H(m_i), g^{x_i}) = \prod_i e(H(m_i), pk_i)$$

by bilinearity in the first argument and then in the second. Line L2 passes when the messages are distinct, and line L3 passes because all the values are group elements. The full proof is below.

## Complexity

Let $n$ be the number of binary digits of $r$.

- **Aggregation**: $N - 1$ group multiplications, by anyone.
- **Verification**: $N$ hashes to the group and $N + 1$ pairings, or $N + 1$ Miller loops and one shared final exponentiation. With proofs of possession and one message, two pairings and $N - 1$ multiplications of keys.
- **Size**: one group element (48 or 96 bytes on BLS12-381) instead of $N$, but the verifier still needs the $N$ keys and messages.
- **Time**: each operation is $\Theta(n^3)$ word operations with schoolbook arithmetic; space $\Theta(n)$ for the aggregate.

## Properties

- **Secure in the chosen key model**, in the random oracle model under the co-CDH assumption on the pairing groups, with distinct messages (BGLS 2003), or with message augmentation (Bellare, Namprempre and Neven 2007), or with proofs of possession for same-message aggregates.
- **Non-interactive and public**: anyone can aggregate, at any time, and aggregates can be aggregated again.
- **Not a proof of each member.** Two wrong signatures with errors that cancel give a right aggregate (the "splitting zero" problem). An aggregate shows that the set as a whole was signed. Protocols that later need individual signatures must check them separately.
- **No removal.** One cannot take a signature out of an aggregate without knowing it.

## Variants and improvements

- **Multisignatures** are the special case of one message, with a compact aggregate key; see [MuSig](/musig/) for Schnorr and BLS with proofs of possession.
- **Sequential aggregates** (LMRS 2004) from RSA-type permutations, and later from other assumptions.
- **Half aggregation of Schnorr and EdDSA** (Chalkias, Garillot, Kondi and Nikolaenko, 2021) keeps all the $R_i$ but sums the $s_i$, which halves the size without interaction. Full non-interactive aggregation of Schnorr signatures is not known.
- **Lattice and hash based aggregates** are research topics for post-quantum use.

## When to use it

Use BLS aggregation when many signatures by many keys must be stored or sent together and verifiers can afford pairings: block attestations in proof of stake chains, certificates of a [quorum](/quorum-certificate/) in Byzantine fault tolerant replication, and logs. In Ethereum's consensus, each validator registers its key with a proof of possession in its deposit, and attestations on the same data are aggregated by aggregator nodes into one signature per committee.

## Pitfalls

- **Same messages without proofs or augmentation**: the rogue key attack.
- **Skipping the subgroup checks** of line L3 on keys and on the aggregate.
- **Splitting zero**: do not treat a valid aggregate as proof that each individual signature is valid.
- **Duplicates**: an implementation must define whether a repeated $(pk, m)$ pair is allowed, and must check the rule in the same way everywhere.
- **Cost**: verification is not cheaper than $N$ separate BLS verifications for distinct messages, only smaller. The savings are in space and bandwidth.

## Implementations

The Python code on this page implements BGLS aggregation and verification over the toy symmetric pairing of the [BLS](/bls-signature/) page, the rogue key attack with equal messages and no proof of possession, and the splitting zero case. There are no official test vectors for this toy. It is for study only, not constant time, and must not be used to protect real data.

## History

Boneh, Gentry, Lynn and Shacham defined aggregate signatures and gave the BLS based scheme at Eurocrypt 2003, together with verifiably encrypted signatures. Lysyanskaya, Micali, Reyzin and Shacham gave sequential aggregates in 2004. Bellare, Namprempre and Neven removed the distinct message rule in 2007, and Ristenpart and Yilek analyzed proofs of possession in the same year. Ethereum's beacon chain, launched in December 2020, made BLS aggregation a core part of a large deployed system.

## References
