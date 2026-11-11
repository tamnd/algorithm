---
tag: EJVHSG
kind: problem
slug: threshold-signing-problem
name: Threshold signing problem
aliases:
- distributed signing problem
area: cryptography/signatures
level: advanced
summary: "Split one signing key among n parties so that any t of them can sign under the one public key, while t - 1 corrupt parties can neither sign nor learn the key, with or without a trusted dealer."
prereqs: [digital-signature, shamir-secret-sharing]
see_also: [threshold-signature, multisignature-problem, verifiable-secret-sharing, threshold-cryptography, secure-multiparty-computation, malicious-adversary-model, musig, lagrange-interpolation]
sources:
  - paper: "Yvo Desmedt and Yair Frankel, Threshold cryptosystems, CRYPTO 1989, LNCS 435, Springer"
    locator: the first threshold schemes, in which t of n parties jointly use a key that none of them holds
  - paper: "Adi Shamir, How to share a secret, Communications of the ACM 22(11), 1979, doi:10.1145/359168.359176"
    locator: t-of-n sharing by a polynomial of degree t - 1, the basis of most threshold signing
  - paper: "Paul Feldman, A practical scheme for non-interactive verifiable secret sharing, FOCS 1987"
    locator: commitments g^{c_j} to the coefficients, which let each party check its share
  - paper: "Torben Pryds Pedersen, A threshold cryptosystem without a trusted party, EUROCRYPT 1991, LNCS 547, Springer"
    locator: distributed key generation in which every party deals a Feldman sharing and the key is the sum, so no dealer ever knows the key
  - paper: "Rosario Gennaro, Stanislaw Jarecki, Hugo Krawczyk and Tal Rabin, Secure distributed key generation for discrete-log based cryptosystems, EUROCRYPT 1999, LNCS 1592, Springer"
    locator: the attack by which a corrupt party biases the public key of Pedersen's protocol, and the fixed protocol that first commits with Pedersen VSS
  - paper: "Rosario Gennaro, Stanislaw Jarecki, Hugo Krawczyk and Tal Rabin, Robust threshold DSS signatures, EUROCRYPT 1996, LNCS 1070, Springer"
    locator: robustness, the need for an honest majority, and threshold signing for a standard scheme that is hard to share
  - url: "https://doi.org/10.6028/NIST.IR.8214C"
    title: Luis T. A. N. Brandao and Rene Peralta, NIST IR 8214C, NIST First Call for Multi-Party Threshold Schemes, January 2026
    locator: the categories of threshold schemes NIST asks for, including signing, and the security and adversary models a submission must state
---

The threshold signing problem asks how to split one signing key among $n$ parties so that any $t$ of them can produce a signature that verifies under the one public key, while any coalition of at most $t - 1$ corrupt parties can neither sign a new message nor learn the key. The verifier sees one ordinary public key and one ordinary signature; it does not learn which $t$ parties signed or that the key was shared at all. The problem has two halves: getting the shares to the parties, by a trusted dealer or by distributed key generation, and signing with the shares without ever putting the key back together. It differs from the [multisignature problem](/multisignature-problem/), where each signer has its own key and the verifier knows the set of keys.

**Notation.** $t$ is the threshold, $n \ge t$ the number of parties, $x$ the secret key and $y = g^x$ the public key in a group of prime order $q$. Party $i$ holds the share $x_i = f(i)$ of a polynomial $f$ of degree $t - 1$ with $f(0) = x$.

## In plain words

A company wants its signing key used only when enough officers agree, for example any three of five. It must not trust any one officer, or any one computer, with the whole key.

So the key is cut into five pieces in a special way. Any three pieces together are enough to sign, and two pieces show nothing about the key. When three officers agree, each one uses only its own piece, and they send small partial answers that combine into one normal signature. The key itself is never rebuilt in one place.

The cutting can be done by a trusted helper who then forgets the key, or by the officers together, so that no one ever sees the whole key.

## Definition

A $(t, n)$ threshold signature scheme for an ordinary signature scheme $(\mathrm{KeyGen}, \mathrm{Sign}, \mathrm{Verify})$ has:

- **Key generation.** Either a *trusted dealer* runs $\mathrm{KeyGen}$, shares $x$ with a [Shamir sharing](/shamir-secret-sharing/) and erases $x$, or the parties run a *distributed key generation* (DKG) protocol. The output is the public key $y$, a share $x_i$ for each party, and often public verification keys $y_i = g^{x_i}$.
- **Signing.** A protocol among any set $S$ of $|S| \ge t$ parties on a message $m$, with output $\sigma$.
- **Verification.** The unchanged $\mathrm{Verify}(y, m, \sigma)$ of the base scheme.

**Correctness.** If at least $t$ parties follow the protocol, $\mathrm{Verify}$ accepts.

**Unforgeability.** An adversary corrupts up to $t - 1$ parties, sees their state, controls their messages, and asks the honest parties to sign messages of its choice. It wins if it outputs a valid signature on a message that no honest party agreed to sign. The scheme is secure if every efficient adversary wins with negligible probability.

**The adversary model** must be stated with the scheme:

- **Static or adaptive** corruption: chosen before the protocol, or during it.
- **Semi-honest or malicious**: corrupt parties follow the protocol or deviate as they like; see the [malicious model](/malicious-adversary-model/).
- **Network**: synchronous with a broadcast channel, or asynchronous.
- **Concurrency**: one signing session at a time, or many at once, which allows attacks on the nonces.

## Variants

- **Trusted dealer versus DKG.** A dealer is simple, but it sees the key and is a single point of failure at setup. In Pedersen's DKG (1991), each party deals a [verifiable](/verifiable-secret-sharing/) Feldman sharing of its own random value, and the key is the sum of the values of the parties that were not disqualified. Gennaro, Jarecki, Krawczyk and Rabin (GJKR, 1999) showed that a corrupt party can bias the resulting key in that protocol, by deciding which honest dealings to complain about after it sees them, and gave a fix that commits first with Pedersen VSS. For many signature schemes the biased key is still safe, but the proofs must account for it.
- **Robustness.** A *robust* protocol outputs a signature even if up to $t - 1$ parties send wrong values. This needs $t$ honest parties among the $n$, so $n \ge 2t - 1$, and a way to check partial results. A weaker goal is *identifiable abort*: the protocol may fail, but it names a cheater, who can then be excluded.
- **Proactive security.** Shares are refreshed from time to time, so an adversary must corrupt $t$ parties within one period.
- **Accountability.** Plain threshold signatures hide which parties signed. Accountable variants reveal the set, at the cost of a larger signature or a separate log.
- **Weighted thresholds** give parties different numbers of shares.

## Examples

- **Threshold BLS** (Boldyreva, 2003). Each party sends $H(m)^{x_i}$. Anyone combines $t$ of them by [Lagrange interpolation](/lagrange-interpolation/) in the exponent into $H(m)^x$. One round, no interaction among the signers, and robust because each share can be checked by a pairing.
- **Threshold Schnorr.** The nonce must be shared too. FROST (Komlo and Goldberg, 2020) does this in two rounds with two nonces per party, like MuSig2.
- **Threshold ECDSA.** The signature $s = k^{-1}(h + rx)$ needs the inverse of a shared nonce times a shared key, a multiplication of secrets, which takes homomorphic encryption or oblivious transfer and several rounds.
- **Threshold RSA** (Shoup, 2000) shares the private exponent and combines partial signatures with a trick that avoids inverses modulo the unknown group order.

See [threshold signatures](/threshold-signature/) for these schemes in detail.

## Known algorithms

| scheme | base signature | key setup | rounds to sign | notes |
|---|---|---|---|---|
| Shoup (2000) | RSA | trusted dealer | 1 | robust, needs safe primes |
| Boldyreva (2003) | BLS | dealer or DKG | 1 | robust, needs pairings |
| GJKR (1996) | DSS | DKG | several | robust with an honest majority |
| Lindell (2017) | ECDSA, two parties | two-party DKG | a few messages | uses Paillier encryption |
| Gennaro and Goldfeder (2018) | ECDSA, any t | DKG | several | dishonest majority |
| FROST (2020), RFC 9591 (2024) | Schnorr | dealer or DKG | 2, or 1 with preprocessing | aborts on misbehavior, then identifies the cheater |

## Bounds

- **Share size.** Each share is at least as large as the secret if $t - 1$ shares must reveal nothing; Shamir sharing meets this bound.
- **Honest parties.** Robustness needs at least $t$ honest parties, hence $n \ge 2t - 1$ when $t - 1$ may be corrupt. Without it, a dishonest majority can always stop the protocol, so the best possible is abort with identification.
- **Rounds.** Threshold BLS needs one round. Schnorr-type schemes need a shared nonce, and their concurrent security with one nonce per party falls to the ROS attack, as for multisignatures; two rounds with two nonces avoid it.
- **Generic solution.** Any signature scheme can be computed by general [secure multiparty computation](/secure-multiparty-computation/) on shares of the key, so the problem is always solvable in principle; the research question is the cost.

## Reductions

- **From secret sharing.** Every scheme here starts from a $t$-of-$n$ sharing of the key, and the security proof simulates the $t - 1$ corrupt shares as random values.
- **To multisignatures.** With $t = n$ and joint key generation, a threshold scheme gives an $n$-of-$n$ multisignature for one fixed group. It does not give the ad hoc groups of a multisignature, and a multisignature with $t$ of $n$ keys listed is not a threshold scheme, because the verifier sees the keys.
- **Threshold decryption** shares a decryption key the same way; signing and decryption are both treated under [threshold cryptography](/threshold-cryptography/).

## Applications

- Certificate authorities and code signing, where no single machine should hold the root key.
- Custody of digital assets, where a wallet key is split among devices or institutions.
- Distributed randomness beacons, such as drand, which publish threshold BLS signatures on round numbers.
- Distributed validators in proof of stake, where one validator key is split among several machines.
- The NIST multi-party threshold call (NIST IR 8214C, 2026), which asks for threshold schemes for signing among other primitives.

## References
