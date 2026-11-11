---
tag: YVV26W
kind: algorithm
slug: threshold-signature
name: Threshold signature
aliases:
- t-of-n threshold signature
- threshold BLS
area: cryptography/signatures
level: advanced
summary: "Any t of n parties holding Shamir shares of one key sign under the one public key, and t - 1 cannot. Threshold BLS combines t partial signatures by Lagrange interpolation in the exponent."
model: word-ram
complexity:
  vars: {n: the number of binary digits of the group order, t: the threshold}
  time: {worst: Θ(t n^3), average: Θ(t n^3), best: Θ(t n^3)}
  space: {extra: Θ(t n)}
properties: {deterministic: true, randomized: false}
history:
  year: 2003
  people: [Alexandra Boldyreva, Victor Shoup, Chelsea Komlo, Ian Goldberg]
  note: Shoup gave practical threshold RSA in 2000 and Boldyreva threshold BLS in 2003. FROST for Schnorr appeared in 2020 and became RFC 9591 in 2024.
prereqs: [threshold-signing-problem, shamir-secret-sharing, bls-signature]
see_also: [lagrange-interpolation, verifiable-secret-sharing, musig, aggregate-signature, ecdsa, schnorr-signature, multisignature-problem, threshold-cryptography]
sources:
  - paper: "Victor Shoup, Practical threshold signatures, EUROCRYPT 2000, LNCS 1807, Springer, pages 207 to 220"
    locator: threshold RSA with a trusted dealer, partial signatures with proofs of correctness, and combination with the factor Delta = n! to avoid inverses
  - paper: "Alexandra Boldyreva, Threshold signatures, multisignatures and blind signatures based on the gap-Diffie-Hellman-group signature scheme, PKC 2003, LNCS 2567, Springer, pages 31 to 46"
    locator: threshold BLS, partial signatures checked by a pairing, and combination by Lagrange interpolation in the exponent
  - paper: "Chelsea Komlo and Ian Goldberg, FROST, flexible round-optimized Schnorr threshold signatures, SAC 2020, LNCS 12804, Springer"
    locator: two round threshold Schnorr signing with two nonces per party and a binding factor, and the preprocessing of the first round
  - url: "https://www.rfc-editor.org/rfc/rfc9591"
    title: "D. Connolly, C. Komlo, I. Goldberg and C. A. Wood, RFC 9591, The Flexible Round-Optimized Schnorr Threshold (FROST) Protocol for Two-Round Schnorr Signatures, June 2024"
    locator: the two round protocol, the ciphersuites, and the test vectors in its appendix
  - paper: "Rosario Gennaro and Steven Goldfeder, Fast multiparty threshold ECDSA with fast trustless setup, ACM CCS 2018"
    locator: t-of-n threshold ECDSA for any t with a dishonest majority, using a multiplicative to additive conversion based on Paillier encryption
  - paper: "Yehuda Lindell, Fast secure two-party ECDSA signing, CRYPTO 2017, LNCS 10402, Springer"
    locator: two party ECDSA in which one party holds a Paillier encryption of the other's key share
  - url: "https://doi.org/10.6028/NIST.IR.8214C"
    title: Luis T. A. N. Brandao and Rene Peralta, NIST IR 8214C, NIST First Call for Multi-Party Threshold Schemes, January 2026
    locator: the call for threshold schemes, with signing among the primitives in scope
  - paper: "Yvo Desmedt and Yair Frankel, Threshold cryptosystems, CRYPTO 1989, LNCS 435, Springer"
    locator: the first threshold schemes
---

A threshold signature scheme splits one signing key among $n$ parties so that any $t$ of them can sign under the one public key and any $t - 1$ cannot. Each party signs with its own share, and a combiner turns any $t$ partial signatures into one ordinary signature; the verifier sees a normal key and a normal signature. This page describes threshold BLS (Boldyreva, 2003), the simplest case, in detail, and then FROST for Schnorr, Shoup's threshold RSA and threshold ECDSA. The problem it solves, with its adversary models and key generation, is the [threshold signing problem](/threshold-signing-problem/).

**Notation.** $G$ is a group of prime order $r$ with generator $g$ and a bilinear pairing $e$, written multiplicatively. $x$ is the secret key and $y = g^x$ the public key. $f$ is a polynomial of degree $t - 1$ over $\mathbb{Z}_r$ with $f(0) = x$; party $i$ holds $x_i = f(i)$, and $y_i = g^{x_i}$ is its public verification key. $H$ hashes messages into $G$.

## In plain words

The key is hidden as the starting value of a secret curve that is described by $t$ numbers. Each party gets one point on the curve. Any $t$ points fix the curve, and so the key; fewer points fit every possible key equally well.

To sign, each party makes an ordinary BLS signature with its point instead of the key. Those partial signatures behave like points on a hidden curve too. A combiner takes any $t$ of them and works out the starting value by the same rule that would rebuild the key, but on the signatures. The result is exactly the signature the full key would make. The key itself is never rebuilt.

## The problem

Given $t \le n$, produce shares and a signing procedure such that any $t$ honest parties can sign any message under $y$, the output is a valid BLS signature, and an adversary that holds at most $t - 1$ shares and sees signatures on messages of its choice cannot sign any other message.

## The algorithm

Key generation by a trusted dealer, then signing and combination.

```pseudo id=main
DEAL(x, t, n)
L1  pick c_1, ..., c_{t−1} at random;  f(z) = x + c_1 z + … + c_{t−1} z^{t−1};  x_i ← f(i), y_i ← g^{x_i}

PARTIAL-SIGN(x_i, m), at party i
L2  σ_i ← H(m)^{x_i}

PARTIAL-VERIFY(y_i, m, σ_i)
L3  accept if σ_i ∈ G and e(σ_i, g) = e(H(m), y_i)

COMBINE({σ_i : i ∈ S}), with |S| = t
L4  λ_i ← Π_{j ∈ S, j ≠ i} j / (j − i) mod r
L5  σ ← Π_{i ∈ S} σ_i^{λ_i}

VERIFY(y, m, σ)
L6  accept if e(σ, g) = e(H(m), y)
```

Line L6 is plain [BLS](/bls-signature/) verification. The combiner needs no secret, so any party, or any outsider, can combine.

**Without a dealer.** In a distributed key generation in the style of Pedersen (1991), each party $j$ picks its own random polynomial $f_j$ of degree $t - 1$, sends $f_j(i)$ to each party $i$, and publishes the commitments $g^{c_{j,k}}$ of its coefficients, so each receiver can check its share as in [verifiable secret sharing](/verifiable-secret-sharing/). Party $i$ sets $x_i = \sum_j f_j(i)$, and $y = \prod_j g^{f_j(0)}$. Nobody ever knows $x = \sum_j f_j(0)$. A full protocol adds a complaint phase and, following Gennaro, Jarecki, Krawczyk and Rabin (1999), a commitment step that stops a corrupt party from biasing $y$. The code includes the version for honest parties only.

**Robustness.** Line L3 lets the combiner check every partial signature before it uses it. If a party sends a wrong one, the combiner drops it and takes another, so with at least $t$ honest parties the protocol always ends with a valid signature.

## Example

In the toy pairing group of the code ($r = 2147483659$, not secure), take $x = 1234567$, $t = 2$, $n = 3$ and the dealer's coefficient $c_1 = 1000$, so $f(z) = 1234567 + 1000 z$ and the shares are $x_1 = 1235567$, $x_2 = 1236567$, $x_3 = 1237567$. Parties 1 and 3 sign "hi":

| item | value (additive notation) |
|---|---|
| $\sigma_1 = x_1 H(\text{hi})$ | $(1450704056411498721, 251261093609784528)$ |
| $\sigma_3 = x_3 H(\text{hi})$ | $(432337061687768120, 543179746740589889)$ |
| $\lambda_1 = 3/2 \bmod r$ | $1073741831$ |
| $\lambda_3 = -1/2 \bmod r$ | $1073741829$ |
| $\sigma = \lambda_1 \sigma_1 + \lambda_3 \sigma_3$ | $(1544493870114847728, 559180719914778072)$ |

The result is the same point as the single-signer signature $x H(\text{hi})$ on the [BLS signature](/bls-signature/) page, because $\tfrac{3}{2} f(1) - \tfrac{1}{2} f(3) = f(0)$ for every line $f$. Parties 1 and 2, or 2 and 3, give the same $\sigma$. One partial signature alone, "interpolated" with itself, gives $x_1 H(\text{hi})$, which fails verification.

## Correctness

Each $\sigma_i = H(m)^{f(i)}$. The Lagrange coefficients of line L4 satisfy $\sum_{i \in S} \lambda_i f(i) = f(0)$ for every polynomial $f$ of degree at most $t - 1$, so

$$\prod_{i \in S} \sigma_i^{\lambda_i} = H(m)^{\sum_i \lambda_i f(i)} = H(m)^{f(0)} = H(m)^x,$$

the BLS signature, which passes line L6. Partial signatures pass line L3 by the BLS argument with $x_i$ in place of $x$. The full proof, with the statement that $t - 1$ shares reveal nothing about $x$, is below.

## Complexity

Let $n$ also stand for the number of binary digits of $r$ (the context separates it from the number of parties), and $t$ for the threshold.

- **Partial signing**: one hash to $G$ and one exponentiation.
- **Partial verification**: two pairings per share.
- **Combination**: $O(t^2)$ field operations for the coefficients and $t$ exponentiations, $\Theta(t n^3)$ word operations with schoolbook arithmetic.
- **Verification**: two pairings, independent of $t$ and $n$.
- **Space**: $\Theta(t n)$ for the shares being combined. Each party stores one share; the public data are $y$ and the $n$ keys $y_i$.

## Properties

- **Non-interactive signing.** Parties do not talk to each other; each sends one group element.
- **Unique output.** Every set of $t$ parties gives the same signature, because BLS signatures are unique. This makes threshold BLS a good source of distributed randomness.
- **Robust**, with share checks by pairing.
- **Secure** in the random oracle model under the CDH assumption in the pairing group (gap Diffie-Hellman in Boldyreva's terms), against a static adversary that corrupts up to $t - 1$ parties.
- **Private set of signers.** The signature does not show which $t$ parties signed.

## Variants and improvements

- **Threshold RSA** (Shoup, 2000). Shares of $d$ cannot be interpolated directly, because the combiner does not know $\varphi(N)$. Shoup scales by $\Delta = n!$ so that all coefficients are integers, and removes the extra exponent at the end with the extended Euclidean algorithm. Partial signatures carry zero knowledge proofs of correctness.
- **FROST** (Komlo and Goldberg, 2020; RFC 9591, 2024) for Schnorr signatures. Each party publishes two nonce commitments $(D_i, E_i)$, possibly in advance. For a signing set $S$ and message $m$, a binding factor $\rho_i = H(i, y, m, \{D_j, E_j\})$ gives the group nonce $R = \prod_{j \in S} D_j E_j^{\rho_j}$, and party $i$ returns $z_i = d_i + e_i \rho_i + \lambda_i x_i c$ with $c = H(R, y, m)$. The sum $z = \sum z_i$ gives an ordinary Schnorr signature $(R, z)$. As in [MuSig2](/musig/), the two nonces stop the concurrent attacks that break a one nonce design.
- **Threshold ECDSA.** The [ECDSA](/ecdsa/) equation $s = k^{-1}(h + r x)$ multiplies two shared secrets. Lindell (2017) gave fast two party signing with Paillier encryption; Gennaro and Goldfeder (2018) gave $t$-of-$n$ signing with a dishonest majority. Later protocols add identifiable abort and proactive refresh. These protocols are complex, and several deployed implementations have had serious bugs in their zero knowledge proofs.
- **NIST.** NIST IR 8214C (January 2026) is the first NIST call for multi-party threshold schemes, including threshold signing.

## When to use it

Use threshold BLS when a group must sign as one key, signing should be one round with no talk between the signers, and verifiers can do pairings: randomness beacons, distributed validators, and committee certificates. Use FROST when the output must be an ordinary Schnorr or EdDSA signature, for example on a blockchain that already checks such signatures. Use threshold ECDSA only when the verifier accepts nothing else, and use a reviewed implementation. When each signer should have its own key and the verifier may see the set, a [multisignature](/multisignature-problem/) is simpler.

## Pitfalls

- **Unchecked shares.** Without line L3, one bad partial signature spoils the result and nobody knows who sent it.
- **A dealer that keeps the key.** A trusted dealer must erase $x$; a DKG avoids the problem.
- **Naive DKG.** The plain joint Feldman DKG lets a corrupt party bias the key; use a protocol whose analysis covers this.
- **Duplicate or zero indices.** The evaluation points must be distinct and nonzero, or line L4 divides by zero or reveals $f(0)$.
- **Nonces in threshold Schnorr and ECDSA.** Reusing or biasing nonces leaks shares, as for single signers, and one nonce per party is open to concurrent attacks.
- **Mixing up thresholds.** Some papers write $t$ for the number of corrupt parties (so $t + 1$ sign); check the convention.

## Implementations

The Python code on this page implements threshold BLS as described by Boldyreva: a trusted dealer with Shamir sharing, partial signatures with pairing checks, and Lagrange combination at 0, over the toy symmetric pairing of the [BLS](/bls-signature/) page. It also has a joint Feldman DKG for honest parties only, without the complaint phase or the GJKR fix. The tests show that every set of $t$ shares gives the same valid signature and that $t - 1$ shares do not. There are no official test vectors for the toy group. FROST and threshold ECDSA are described but not implemented. The code is for study only and is not constant time.

## History

Desmedt (1987) and Desmedt and Frankel (1989) proposed threshold cryptography, building on Shamir's secret sharing (1979). Pedersen gave a distributed key generation without a trusted party in 1991, and Gennaro, Jarecki, Krawczyk and Rabin gave robust threshold DSS in 1996 and a secure DKG in 1999. Shoup's practical threshold RSA appeared in 2000, and Boldyreva's threshold BLS in 2003. Interest grew again with cryptocurrencies: Lindell's two party ECDSA (2017), Gennaro and Goldfeder's threshold ECDSA (2018), and FROST (2020), standardized as RFC 9591 in 2024. NIST published its first call for multi-party threshold schemes as NIST IR 8214C in January 2026.

## References
