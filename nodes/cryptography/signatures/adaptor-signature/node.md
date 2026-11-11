---
tag: ZMDYYY
kind: algorithm
slug: adaptor-signature
name: Adaptor signature
aliases:
- scriptless scripts signature
- Schnorr adaptor signature
area: cryptography/signatures
level: research
summary: "A pre-signature tied to a statement T = tG: anyone can check it, the witness t turns it into a valid signature, and the published signature reveals t. Used for atomic swaps and payment channels."
model: word-ram
complexity:
  vars: {n: the number of binary digits of the group order}
  time: {worst: Θ(n^3), average: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true}
history:
  year: 2017
  people: [Andrew Poelstra, Lukas Aumayr, Oguzhan Ersoy, Andreas Erwig, Sebastian Faust, Kristina Hostakova, Matteo Maffei, Pedro Moreno-Sanchez, Siavash Riahi]
  note: Poelstra described adaptor signatures as part of scriptless scripts in 2017. Aumayr et al. gave the formal definitions and proofs at Asiacrypt 2021.
prereqs: [schnorr-signature, discrete-logarithm-problem]
see_also: [musig, ecdsa, multisignature-problem, threshold-signature, nonce-reuse-attack, zero-knowledge-proof, commitment-scheme, signature-malleability]
sources:
  - paper: "Andrew Poelstra, Scriptless scripts, presentation at the MIT Bitcoin Expo, March 2017"
    locator: the idea of a Schnorr signature that is offset by a secret t, so that publishing the signature reveals t, and its use for atomic swaps without scripts
  - paper: "Lukas Aumayr, Oguzhan Ersoy, Andreas Erwig, Sebastian Faust, Kristina Hostakova, Matteo Maffei, Pedro Moreno-Sanchez and Siavash Riahi, Generalized channels from limited blockchain scripts and adaptor signatures, ASIACRYPT 2021, LNCS 13091, Springer"
    locator: the definition of adaptor signatures for a hard relation, pre-signature correctness, pre-signature adaptability, unforgeability (aEUF-CMA) and witness extractability, with Schnorr and ECDSA constructions
  - paper: "Giulio Malavolta, Pedro Moreno-Sanchez, Clara Schneidewind, Aniket Kate and Matteo Maffei, Anonymous multi-hop locks for blockchain scalability and interoperability, NDSS 2019"
    locator: payment channel networks whose hops are locked by adaptor signatures instead of hash locks, which removes the link between the hops
  - url: "https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki"
    title: Pieter Wuille, Jonas Nick and Tim Ruffing, BIP 340, Schnorr signatures for secp256k1
    locator: the verification algorithm and the even-y rule for R and P that the adapted signature must satisfy
---

An adaptor signature is a signature that is "locked" by a hard problem. The signer, who knows the secret key $d$ but not the witness $t$, produces a *pre-signature* for a message $m$ and a statement $T = tG$. Anyone can check that the pre-signature is well formed, but it is not a valid signature. Whoever knows $t$ can *adapt* it into a valid signature, and as soon as that signature is published, anyone who holds the pre-signature can *extract* $t$. This ties two events together without any script on a blockchain: publishing a signature reveals a secret, and the secret unlocks another signature. The idea, by Poelstra (2017), is the basis of "scriptless scripts", atomic swaps and payment channel hops.

**Notation.** $G$ is the base point of secp256k1, of prime order $n$, written additively. The signer has the secret $d$ and the public key $P = dG$, with $P$ of even y as in BIP 340. $T = tG$ is the statement and $t$ the witness. $H$ is the BIP 340 challenge hash, and $x(R)$ the x coordinate of $R$.

## In plain words

Bob writes a check to Alice but leaves one number blank, and only Alice knows the number. Everyone can see that the check is real and that it is complete except for that number. When Alice fills in the number and cashes the check, the number becomes public, and Bob can read it off the cashed check.

So Bob can make a second promise that depends on the same number. If Alice cashes the first check, Bob learns what he needs to cash a check from Alice. Either both payments happen, or neither does. No third party and no special rules are needed; ordinary signatures do the work.

## The problem

Given a hard relation, here $\{(T, t) : T = tG\}$, build algorithms $\mathrm{PreSign}(d, m, T)$, $\mathrm{PreVerify}(P, m, T, \hat\sigma)$, $\mathrm{Adapt}(\hat\sigma, t)$ and $\mathrm{Extract}(\sigma, \hat\sigma, T)$ such that an adapted pre-signature verifies as an ordinary signature, and the ordinary signature together with the pre-signature reveals $t$.

## The algorithm

The pre-signature $(\hat{R}, s')$ is a Schnorr signature whose nonce is shifted by $T$. The final nonce is $R = \hat{R} + T$. BIP 340 treats $x(R)$ as the point with an even y, so $\epsilon = 1$ if $R$ has an even y and $\epsilon = -1$ otherwise.

```pseudo id=main
PRE-SIGN(d, m, T)
L1  pick k at random;  R̂ ← kG;  R ← R̂ + T;  ε ← +1 if R has an even y, else −1
L2  e ← H(x(R) ‖ x(P) ‖ m)
L3  s' ← εk + e d mod n;  return (R̂, s')

PRE-VERIFY(P, m, T, (R̂, s'))
L4  R ← R̂ + T;  ε and e as in L1 and L2
L5  accept if s' G = ε R̂ + e P

ADAPT((R̂, s'), t)
L6  s ← s' + ε t mod n;  return σ = (x(R), s)

EXTRACT(σ = (x(R), s), (R̂, s'), T)
L7  t ← ε (s − s') mod n;  check tG = T;  return t
```

**Why it works.** After line L6, $sG = \epsilon kG + e d G + \epsilon tG = \epsilon(\hat{R} + T) + eP = \epsilon R + eP$. The point $\epsilon R$ is the even-y point with x coordinate $x(R)$, so $(x(R), s)$ is a valid BIP 340 signature with challenge $e$. Line L7 inverts line L6.

**Atomic swap.** Alice holds $t$ and publishes $T$. Alice pre-signs her payment to Bob on chain A, and Bob pre-signs his payment to Alice on chain B, both under $T$, and each checks the other's pre-signature. To take Bob's payment, Alice must adapt it with $t$ and publish the signature on chain B. Bob extracts $t$ from that signature and adapts Alice's pre-signature on chain A. If Alice never claims, Bob never pays; time locks (not shown) return the funds after a deadline. In practice each payment goes to a [MuSig](/musig/) 2-of-2 key, and the pre-signatures are partial signatures of that key.

**Payment channels.** In a route of payment channels, each hop is locked to a statement $T_j$, and claiming the last hop reveals the witness that unlocks the hop before it. With adaptor signatures, as in anonymous multi-hop locks (Malavolta et al., 2019), each hop uses a different statement, so observers cannot link the hops, unlike the one hash value shared along a route of hash time locked contracts.

## Example

With the BIP 340 key of $d = 3$ (its public key has an even y), the witness $t = 5$, the message "swap" and a nonce from `random.Random(1)`:

| item | value |
|---|---|
| $x(\hat{R})$ | D7DA18E28D6463EA9B7E93402AEC0E122B76A669E04AD12F5F4B913F772751EF |
| $x(R) = x(\hat{R} + 5G)$ | 057FD52B6F5FB97E1438A884478866BD01ACAB097D261C0FB5E9E5476BE8BA33 |
| parity of $R$ | odd, so $\epsilon = -1$ |
| $s'$ | 58A50B755E1E8AFF913CF290888F244A887B3AA9020C327901717D626814BEFC |
| $s = s' - 5$ | 58A50B755E1E8AFF913CF290888F244A887B3AA9020C327901717D626814BEF7 |

The pair $(x(R), s)$ passes BIP 340 verification, and $-(s - s') = 5$ gives back the witness. The pair $(x(R), s')$ does not verify.

## Correctness

Lines L1 to L3 give $s'G = \epsilon \hat{R} + eP$, so pre-verification accepts honest pre-signatures. Adaptation gives $sG = \epsilon R + eP$ as shown above, which is BIP 340 verification. Extraction returns $\epsilon(s - s') = \epsilon \cdot \epsilon t = t$. The full proof is below.

## Complexity

Each algorithm costs a constant number of scalar multiplications and one hash: two for pre-signing, three for pre-verification, none for adaptation, and one for the check in extraction. With $n$ binary digits in the group order and schoolbook arithmetic this is $\Theta(n^3)$ time and $\Theta(n)$ space. The pre-signature is one point and one scalar, 65 bytes with a compressed point.

## Properties

Aumayr et al. (2021) define the security notions for a hard relation:

- **Pre-signature correctness.** Honest pre-signatures pass pre-verification, adapt into valid signatures, and the witness can be extracted from the result.
- **Unforgeability (aEUF-CMA).** Even with a pre-signature on $m$ for a statement $T$ of its choice, an adversary that does not know $t$ cannot produce a valid signature on $m$.
- **Pre-signature adaptability.** Every pre-signature that passes pre-verification adapts into a valid signature with the right witness. This protects the receiver against a malicious signer.
- **Witness extractability.** If a valid signature on $m$ appears after a pre-signature on $m$ for $T$, then extraction yields a witness for $T$, even when the signer is malicious.

The Schnorr construction meets these notions in the random oracle model under the discrete logarithm assumption. The result is a standard signature, so an adapted signature is indistinguishable from any other Schnorr signature on chain.

## Variants and improvements

- **ECDSA adaptor signatures** exist, but they need a zero knowledge proof that $\hat{R}$ and a second point share the same discrete logarithm, because the ECDSA equation inverts the nonce; see [ECDSA](/ecdsa/).
- **Two-party adaptors** with MuSig or MuSig2, where the statement is added to the aggregate nonce, are the usual form in Bitcoin protocols.
- **Discreet log contracts** and oracle based contracts use adaptor signatures whose statements are the expected signatures of an oracle on each possible outcome.
- **Other relations.** The witness may come from a hash preimage or a lattice problem in research schemes, though the efficient constructions use discrete logarithms.

## When to use it

Use adaptor signatures to make one signature reveal a secret that unlocks another, without scripts and without a trusted party: atomic swaps across chains, hops in payment channel networks (point time locked contracts), and contracts settled by an oracle. They need interaction before the event and a hard relation that both sides agree on.

## Pitfalls

- **Skipping pre-verification.** A receiver who does not check the pre-signature may be unable to adapt it later; that is a loss of funds in a swap.
- **Nonce reuse.** A pre-signature and a normal signature, or two pre-signatures, with the same $k$ leak $d$, as for any Schnorr signature; see [nonce reuse attacks](/nonce-reuse-attack/). Some deterministic nonce schemes must include $T$ in the nonce derivation for this reason.
- **Parity.** Forgetting the even-y rule for $R$ gives signatures that fail BIP 340 half of the time.
- **Revealing too much.** Publishing the pre-signature itself lets anyone who later sees the signature extract $t$; keep pre-signatures between the parties.
- **Time locks.** The cryptography does not force either party to act; the protocol needs refunds after deadlines, set so the second party has time to claim.

## Implementations

The Python code on this page implements Schnorr adaptor signatures on secp256k1 whose adapted output passes plain BIP 340 verification, with pre-verification, adaptation, extraction, and an atomic swap test. It follows the common construction with the BIP 340 parity rule handled by $\epsilon$, not the byte format of a specific library, and there are no official test vectors for adaptor signatures. The code is for study only and is not constant time.

## History

Poelstra introduced adaptor signatures and scriptless scripts in 2017, in work on Mimblewimble and Bitcoin. Malavolta et al. used them for anonymous multi-hop locks in payment channel networks in 2019. Aumayr, Ersoy, Erwig, Faust, Hostakova, Maffei, Moreno-Sanchez and Riahi gave the first formal definitions and security proofs for Schnorr and ECDSA adaptor signatures at Asiacrypt 2021, and later work strengthened the definitions. Bitcoin's activation of Schnorr signatures with Taproot in November 2021 made the Schnorr form usable on Bitcoin.

## References
