---
tag: HRY17J
kind: concept
slug: threshold-cryptography
name: Threshold cryptography
aliases:
- threshold decryption
- threshold cryptosystem
area: cryptography/protocols
level: advanced
summary: Split a private key among n servers so that any t of them can decrypt or sign together, while t - 1 learn nothing and the whole key never sits in one place.
prereqs: [shamir-secret-sharing, elgamal-encryption]
see_also: [threshold-signature, threshold-signing-problem, verifiable-secret-sharing, lagrange-interpolation, secure-multiparty-computation, bls-signature, key-distribution-center, verifiable-random-function]
sources:
  - paper: "Yvo Desmedt, Society and group oriented cryptography: a new concept, Crypto 1987, LNCS 293, pages 120 to 127"
    locator: the proposal that a group, not a person, should hold a key, so that a message can be read or signed only by the right subset of the group
  - paper: doi:10.1007/0-387-34805-0_28
    title: Yvo Desmedt and Yair Frankel, Threshold cryptosystems, Crypto 1989, LNCS 435, pages 307 to 315
    locator: the threshold ElGamal decryption with Shamir shares of the key and Lagrange interpolation in the exponent
  - paper: doi:10.1007/3-540-45539-6_15
    title: Victor Shoup, Practical threshold signatures, Eurocrypt 2000, LNCS 1807, pages 207 to 220
    locator: threshold RSA with non-interactive signature shares, proofs of correctness for each share, and a security proof in the random oracle model
  - paper: "Torben Pryds Pedersen, A threshold cryptosystem without a trusted party, Eurocrypt 1991, LNCS 547, pages 522 to 526"
    locator: distributed key generation in which each party deals a Feldman-verified sharing and the key is the sum of the dealt secrets
  - paper: doi:10.1007/s00145-006-0347-3
    title: Rosario Gennaro, Stanisław Jarecki, Hugo Krawczyk and Tal Rabin, Secure distributed key generation for discrete-log based cryptosystems, Journal of Cryptology 20(1), 2007, pages 51 to 83; first at Eurocrypt 1999
    locator: the attack by which a rushing party biases the public key of Pedersen's DKG, and a fixed DKG with Pedersen commitments that gives a uniform key
  - url: "https://doi.org/10.6028/NIST.IR.8214C"
    title: Luís T. A. N. Brandão and René Peralta, NIST IR 8214C, NIST First Call for Multi-Party Threshold Schemes, final version 2026-01-20
    locator: the categories of schemes asked for (signing, public-key encryption, key generation and others), the submission phases; initial public draft 2023-01-25, second public draft 2025-03-27
  - paper: doi:10.1145/359168.359176
    title: Adi Shamir, How to share a secret, Communications of the ACM 22(11), 1979, pages 612 to 613
    locator: the polynomial sharing scheme on which the threshold key shares rest
---

Threshold cryptography splits the private key of a public-key scheme among $n$ servers, so that any $t$ of them can decrypt or sign together, while any $t - 1$ of them learn nothing about the key and cannot do the operation. Unlike [secret sharing](/secret-sharing/) alone, the key is never put back together: each server applies its share to the input and sends a partial result, and a combiner joins $t$ partial results into the output. The public key and the output look the same as in the ordinary scheme, so users and verifiers do not see that the key is shared. Desmedt proposed the idea in 1987, and Desmedt and Frankel gave the first threshold cryptosystem, threshold ElGamal, in 1989.

**Notation.** $p = 2q + 1$ is a safe prime and $g$ generates the subgroup of prime order $q$. $x$ is the secret key and $y = g^x$ the public key. $f$ is a random polynomial of degree $t - 1$ over $\mathbb{Z}_q$ with $f(0) = x$, server $i$ holds the share $x_i = f(i)$, and $y_i = g^{x_i}$ is its public verification key. For a set $S$ of servers, $\lambda_i^S = \prod_{j \in S, j \ne i} j / (j - i) \bmod q$ is the Lagrange coefficient of $i$ at zero.

## In plain words

A bank vault has one lock, but the key is cut into five pieces, given to five managers. Any three managers together can open the vault; two cannot, and two pieces give no hint about the key. The clever part is that the managers never put the key together on a table, where one thief could copy it. Each manager turns their own piece in the lock in turn, and after three turns the vault opens.

Threshold cryptography does the same with a decryption or signing key. A thief must break into three servers, not one, and one server that is down or dishonest does not stop the others. Customers see one ordinary public key and do not know that it is split.

## The idea

**Shares of the key.** A trusted dealer, or better a distributed protocol, picks $x$, chooses a random polynomial $f$ of degree $t - 1$ with $f(0) = x$, and gives server $i$ the share $x_i = f(i)$. This is [Shamir secret sharing](/shamir-secret-sharing/): any $t$ points fix $f$ and so $x$, by [Lagrange interpolation](/lagrange-interpolation/), $x = \sum_{i \in S} \lambda_i^S x_i$, while any $t - 1$ shares fit every value of $x$ equally well.

**Lagrange in the exponent.** Threshold [ElGamal](/elgamal-encryption/) decrypts a ciphertext $(c_1, c_2) = (g^r, m \cdot y^r)$ by computing $c_1^x$. Each server $i$ in a set $S$ of $t$ servers sends the partial decryption $d_i = c_1^{x_i}$. The combiner computes

$$\prod_{i \in S} d_i^{\lambda_i^S} = c_1^{\sum_{i \in S} \lambda_i^S x_i} = c_1^{x},$$

and then $m = c_2 / c_1^x$. The interpolation happens in the exponent, so no one learns $x$, and each $d_i$ is useful only for this one ciphertext.

**Robustness.** A dishonest server can send a wrong $d_i$, which silently gives a wrong plaintext. So each server also proves that $\log_g y_i = \log_{c_1} d_i$, with the Chaum-Pedersen proof of equal discrete logarithms, a [sigma protocol](/sigma-protocol/). The combiner discards shares with bad proofs and uses any $t$ good ones. With $n \ge 2t - 1$, the $n - t + 1$ honest servers are enough even when $t - 1$ servers cheat.

**No dealer: distributed key generation.** A dealer knows $x$, which defeats the purpose. In Pedersen's distributed key generation (DKG, 1991), each server $j$ deals its own random secret $s_j$ with a Shamir sharing and publishes Feldman commitments $g^{a_{j,k}}$ to the coefficients of its polynomial, so each receiver can check its share. A dealer whose shares fail the check is disqualified. The key is $x = \sum_j s_j$ over the qualified dealers, each server's share is the sum of the shares it received, and $y = \prod_j g^{s_j}$; nobody ever knows $x$. Gennaro, Jarecki, Krawczyk and Rabin (Eurocrypt 1999, J. Cryptology 2007) showed that a party who waits to see the others' commitments can make some dealers fail on purpose and so bias $y$; their DKG first commits with hiding Pedersen commitments and gives a uniform key. For many uses, such as threshold ElGamal and Schnorr signatures, the biased key of the simpler DKG is still known to be enough.

**Threshold signatures.** The same pattern gives a [threshold signature](/threshold-signature/): servers sign with shares, and the combined signature verifies under the ordinary public key. [BLS](/bls-signature/) signatures are the easiest case, because a signature is $H(m)^x$ and Lagrange in the exponent applies at once. Shoup (Eurocrypt 2000) gave practical threshold RSA: each server makes a signature share with a proof that it is correct, the shares are combined without interaction, and the scheme is proved secure in the random oracle model. Threshold Schnorr and threshold ECDSA need interactive protocols for the shared nonce; see the [threshold signing problem](/threshold-signing-problem/).

**Further properties.** Proactive schemes refresh the shares from time to time by adding sharings of zero, so a thief must break $t$ servers within one period. Chosen-ciphertext secure threshold encryption needs more care than threshold ElGamal, which is only secure against chosen-plaintext attacks, because a server that decrypts any ciphertext it is shown acts as a decryption oracle; Shoup and Gennaro gave such schemes in 1998. Threshold schemes are a special case of [secure multiparty computation](/secure-multiparty-computation/) for one function, and they are much faster than generic MPC.

## Examples

**Threshold ElGamal with $n = 5$ and $t = 3$.** The Python code works in the subgroup of order $q$ modulo the 128-bit safe prime $p = 2^{127} + 8799$, with $g = 4$. This group is a toy chosen for speed; real systems use groups of 256 bits or more, usually elliptic curves. A dealer shares $x$ among five servers. A ciphertext of $m = 123456789$ is decrypted by every one of the ten sets of three servers, and by every set of four and of five. None of the ten pairs of servers decrypts it: the combination of two partial results gives a wrong value, as it must, since two shares fit every key. A server with a wrong share fails the Chaum-Pedersen check, and the combiner takes the next server. The code also runs Pedersen's DKG with Feldman checks: the key from the DKG works with every set of three servers, and a dealer that sends one bad share is disqualified.

The code is for study only. It is not constant time and must not protect real data. Shamir sharing is a local copy, and the Chaum-Pedersen proof is run interactively with a random challenge, so the code needs no hash function. For real use, take a reviewed library of threshold protocols, and follow the documents of the NIST threshold call. Threshold ElGamal has no official test vectors, so the tests check the threshold property itself.

**Lagrange coefficients.** For $S = \{1, 2, 3\}$, $\lambda_1 = (2 \cdot 3)/((2-1)(3-1)) = 3$, $\lambda_2 = (1 \cdot 3)/((1-2)(3-2)) = -3$ and $\lambda_3 = (1 \cdot 2)/((1-3)(2-3)) = 1$, modulo $q$. Their sum is $1$, as it must be, because the constant polynomial $1$ interpolates to $1$.

## Where it is used

- **Key custody.** Wallets for cryptocurrencies and certificate authorities split signing keys among devices or data centers with threshold ECDSA, threshold Schnorr (FROST, RFC 9591) or threshold BLS, so that no single machine holds the key.
- **Randomness beacons and consensus.** Threshold BLS signatures make unbiased public random values, as in drand and in some [proof-of-stake](/proof-of-stake/) systems; the value is unique for each round, as with a [verifiable random function](/verifiable-random-function/).
- **Electronic voting.** Votes are encrypted under a threshold ElGamal key held by several trustees, and the tally is decrypted only when enough trustees agree, as in Helios and in several national pilots.
- **Replacing a trusted server.** A threshold of servers can play the role of a [key distribution center](/key-distribution-center/) or a key escrow agent, so that one corrupt server cannot act alone.
- **Standards.** NIST IR 8214C, "NIST First Call for Multi-Party Threshold Schemes" (initial public draft 2023-01-25, second public draft 2025-03-27, final 2026-01-20), asks for threshold schemes for signing, encryption, key generation and other primitives; the first previews of submissions are planned for the MPTS 2026 workshop.

## References
