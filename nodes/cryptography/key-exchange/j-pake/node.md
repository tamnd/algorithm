---
tag: KK5EW8
kind: algorithm
slug: j-pake
name: J-PAKE
aliases:
- Password Authenticated Key Exchange by Juggling
- EC-J-PAKE
area: cryptography/key-exchange
level: research
summary: A balanced PAKE in two rounds. Each side sends g^x1, g^x2 and then (g^(x1+x3+x4))^(x2 s), each value with a Schnorr proof. Hao and Ryan 2008, RFC 8236. Used in Thread.
solves: [password-authenticated-key-exchange]
model: word-ram
complexity:
  vars: {m: the number of binary digits of the prime p}
  time: {worst: O(m^3), average: O(m^3), best: O(m^3)}
  space: {extra: Θ(m)}
properties: {deterministic: false, randomized: true}
history:
  year: 2008
  people: [Feng Hao, Peter Ryan]
  note: Hao and Ryan presented J-PAKE at the Security Protocols Workshop 2008 and in a journal version in 2010. RFC 8236 (2017) describes it; Abdalla, Benhamouda and MacKenzie proved it secure in 2015.
prereqs: [password-authenticated-key-exchange, diffie-hellman, schnorr-identification-protocol]
see_also: [fiat-shamir-heuristic, zero-knowledge-proof, cpace, spake2, encrypted-key-exchange, key-confirmation, opaque]
sources:
  - paper: "Feng Hao and Peter Ryan, Password authenticated key exchange by juggling, Security Protocols Workshop (SPW) 2008, LNCS 6615, pages 159 to 171"
    locator: the two-round protocol, the zero-knowledge proofs, and the informal security analysis
  - paper: "Feng Hao and Peter Ryan, J-PAKE: authenticated key exchange without PKI, Transactions on Computational Science XI, LNCS 6480, 2010, pages 192 to 206"
    locator: the journal version, with the cost of 14 exponentiations per party
  - url: "https://www.rfc-editor.org/rfc/rfc8236"
    title: Feng Hao (editor), RFC 8236, J-PAKE, Password-Authenticated Key Exchange by Juggling, September 2017 (Informational)
    locator: Section 2 (the protocol over a finite field, round 1, round 2, key computation), Section 3 (the elliptic curve setting), Section 4 (three-pass variant), Section 5 (key confirmation), Section 6 (security considerations)
  - url: "https://www.rfc-editor.org/rfc/rfc8235"
    title: Feng Hao (editor), RFC 8235, Schnorr Non-interactive Zero-Knowledge Proof, September 2017
    locator: Section 2 (Schnorr NIZK over a finite field, the challenge c = H(g, V, X, UserID, OtherInfo)), Section 3 (elliptic curve), Section 4 (the hash with length prefixes)
  - paper: "Michel Abdalla, Fabrice Benhamouda and Philip MacKenzie, Security of the J-PAKE password-authenticated key exchange protocol, IEEE Symposium on Security and Privacy 2015"
    locator: the security proof of J-PAKE in the BPR model, in the random oracle model, with algebraic adversaries, under the decision square Diffie-Hellman assumption
---

J-PAKE (Password Authenticated Key Exchange by Juggling) is a balanced [password-authenticated key exchange](/password-authenticated-key-exchange/) of Feng Hao and Peter Ryan (2008). Each party sends two [Diffie-Hellman](/diffie-hellman/) shares in the first round and one value that combines its share with the password in the second round. Each value carries a [Schnorr](/schnorr-identification-protocol/) non-interactive [zero-knowledge proof](/zero-knowledge-proof/) that the sender knows its exponent. The design needs no hash to the group, no fixed points with unknown logarithms and no ideal cipher, only the Schnorr proofs. RFC 8236 (2017) describes it, and the Thread network protocol uses its elliptic curve form.

**Notation.** $p$ a prime, $q$ a prime that divides $p - 1$, and $g$ a generator of the subgroup of order $q$ in $\mathbb{Z}_p^*$. $s$ the password as a number in $[1, q)$. Alice holds $x_1, x_2$ and Bob holds $x_3, x_4$; $G_1 = g^{x_1}$, $G_2 = g^{x_2}$, $G_3 = g^{x_3}$, $G_4 = g^{x_4}$. $\mathrm{ZKP}\{x\}$ for a base $h$ is a Schnorr proof of knowledge of $x$ with $X = h^x$. All arithmetic is modulo $p$, and exponents are modulo $q$.

## In plain words

Two parties share a password and want a strong key. In the first round, each party picks two random secret numbers and sends two public values made from them, with a proof that it really knows the secrets.

In the second round, each party mixes its second secret with the password and with the public values of both sides, and sends the result, again with a proof.

From what it receives, each party can strip away the parts it knows and is left with a common secret. The common secret is the same on both sides only if the two passwords are equal. The proofs stop an attacker from sending values whose secrets it does not know, which would let it test passwords offline.

## The problem

[Password-authenticated key exchange](/password-authenticated-key-exchange/) in the balanced setting: two parties share a low-entropy password and no public keys, and want a [session key](/session-key/) such that an active attacker can test at most one password per run and a passive attacker learns nothing it can test offline.

## The algorithm

```pseudo id=main
J-PAKE(s; p, q, g)                ▷ RFC 8236, Section 2; Alice is shown, Bob does the same with x3, x4
                                   ▷ round 1
L1  x1 ← random in [0, q);  x2 ← random in [1, q)
L2  send G1 = g^x1, G2 = g^x2 with ZKP{x1} and ZKP{x2} for base g
                                   ▷ round 2, after receiving G3, G4 and Bob's proofs
L3  verify Bob's two proofs; abort if G4 = 1
L4  send A = (G1·G3·G4)^(x2·s) with ZKP{x2·s} for base G1·G3·G4
                                   ▷ key computation, after receiving B = (G1·G2·G3)^(x4·s)
L5  verify Bob's proof for base G1·G2·G3
L6  K ← (B / G4^(x2·s))^x2        ▷ = g^((x1 + x3)·x2·x4·s)
L7  key ← KDF(K)
                                   ▷ Schnorr NIZK (RFC 8235): prove x with X = h^x
L8  v ← random in [0, q);  V ← h^v
L9  c ← H(h, V, X, UserID, OtherInfo)
L10 r ← (v − x·c) mod q;  the proof is (V, r)
L11 verify: X and V lie in the subgroup, and V = h^r · X^c
```

In round 1 (lines L1 and L2) each party publishes two shares. The rule $x_2 \ne 0$ (and the check $G_4 \ne 1$ in line L3) makes sure that the second share is not trivial. In round 2 (line L4), Alice raises the product $G_1 G_3 G_4 = g^{x_1 + x_3 + x_4}$ to $x_2 s$. The base is a fresh random element that neither party controls alone, and the proof shows that Alice knows the exponent $x_2 s$ for that base. Bob's value is $B = g^{(x_1 + x_2 + x_3) x_4 s}$. In line L6, Alice divides out the term $g^{x_2 x_4 s}$, which she can compute from $G_4$, and raises the rest to $x_2$:

$$K = \left(g^{(x_1 + x_3) x_4 s}\right)^{x_2} = g^{(x_1 + x_3) x_2 x_4 s}.$$

Bob computes $(A / G_2^{x_4 s})^{x_4}$, the same value. The name "juggling" comes from this way of combining the four exponents.

Lines L8 to L11 are the Schnorr NIZK of RFC 8235: a [Schnorr identification](/schnorr-identification-protocol/) run made non-interactive with the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/). The hash covers the base, $V$, $X$ and the sender's identity, each item with a 4-byte length prefix; the identity stops an attacker from replaying a proof back to its sender. The page's code then derives the key with SHA-256 and runs a key confirmation in the spirit of RFC 8236, Section 5, but not in its exact byte format.

**About the code.** The Python code is for study only. It is not constant time, and it must not protect real data. It works in the subgroup of quadratic residues modulo the 1024-bit safe prime of RFC 5054, Appendix A, with $g = 4$ of prime order $q = (p - 1)/2$. No official test vector exists for finite-field J-PAKE, so the tests check agreement, rejection and the proofs.

## Example

A toy group, far too small for use: $p = 23$, $q = 11$, $g = 4$, and $s = 3$. Alice picks $x_1 = 2$, $x_2 = 5$, Bob picks $x_3 = 7$, $x_4 = 4$.

| step | Alice | Bob |
|---|---|---|
| L2 | $G_1 = 4^2 = 16$, $G_2 = 4^5 = 12$ | $G_3 = 4^7 = 8$, $G_4 = 4^4 = 3$ |
| L4 | $A = (16 \cdot 8 \cdot 3)^{15} = 16^{4} = 9$ | $B = (16 \cdot 12 \cdot 8)^{12} = 18$ |
| L6 | $(18 / 3^{15})^5 = (18 / 12)^5 = 13^5 = 4$ | $(9 / 12^{12})^4 = (9/12)^4 = 18^4 = 4$ |

Exponents are reduced modulo 11. Both get $K = 4 = g^{(2 + 7) \cdot 5 \cdot 4 \cdot 3} = g^{540 \bmod 11} = g^1$. If Bob uses $s' = 4$, Alice gets $K = 2$ and Bob gets $K = 13$, and the key confirmation fails.

## Correctness

**Claim.** With the same $s$, both parties compute $K = g^{(x_1 + x_3) x_2 x_4 s}$. Alice: $B / G_4^{x_2 s} = g^{(x_1 + x_2 + x_3) x_4 s - x_2 x_4 s} = g^{(x_1 + x_3) x_4 s}$, then the power $x_2$. Bob: $A / G_2^{x_4 s} = g^{(x_1 + x_3 + x_4) x_2 s - x_2 x_4 s} = g^{(x_1 + x_3) x_2 s}$, then the power $x_4$. With $s' \ne s$, the two values agree only if $x_1 + x_2 + x_3 + x_4 \equiv 0 \pmod q$, which has probability $1/q$. Honest Schnorr proofs always verify, since $h^r X^c = h^{v - xc} h^{xc} = h^v = V$. See the [full proof](/j-pake/proofs/correctness/).

**Security.** Hao and Ryan gave an informal argument. Abdalla, Benhamouda and MacKenzie (2015) proved J-PAKE secure in the BPR model (see [PAKE](/password-authenticated-key-exchange/)) in the [random oracle model](/random-oracle-model/), for algebraic adversaries, under the decision square Diffie-Hellman assumption, with the Schnorr proofs used as simulation-sound extractable proofs. The proof bounds an active attacker to about one password guess per online run. There is no UC proof.

## Complexity

Each party does 14 [modular exponentiations](/modular-exponentiation/): 4 in round 1 ($G_1$, $G_2$ and the two values $V$), 4 to verify the two proofs it receives (two each), 2 in round 2 ($A$ and its $V$), and 4 for the key (2 to verify the last proof, then $G_4^{x_2 s}$ and the power $x_2$). Checking that received values lie in the subgroup adds one exponentiation per value in the finite-field setting. Each exponentiation costs $O(m^3)$ word operations with schoolbook multiplication, so a run costs $O(m^3)$. There are two rounds and four messages (two per party), plus the key confirmation, which RFC 8236, Section 5, recommends. Each party keeps $O(1)$ numbers of $m$ binary digits. On elliptic curves (EC-J-PAKE) the counts are the same in scalar multiplications.

## Properties

- **Balanced**: both parties hold $s$.
- **No trusted setup** and no hash to the group: the only public parameters are $p$, $q$ and $g$.
- **Symmetric**: both parties run the same code, so the two rounds can be sent in parallel.
- **Forward secrecy**: $K$ depends on fresh exponents, so a later leak of $s$ does not reveal past keys to an eavesdropper.
- **Implicit authentication** without the key confirmation of RFC 8236, Section 5.
- **Not quantum-safe**.

## Variants and improvements

- **EC-J-PAKE** (RFC 8236, Section 3): the same protocol on an elliptic curve such as P-256, with point validation. Thread uses it in the cipher suite `TLS_ECJPAKE_WITH_AES_128_CCM_8` for commissioning devices.
- **Three-pass J-PAKE** (RFC 8236, Section 4): the two rounds sent as three messages, with the second round piggybacked.
- **Key confirmation** (RFC 8236, Section 5): an explicit MAC on both sides, for example with HMAC over the shares.
- **[CPace](/cpace/)** and **[SPAKE2](/spake2/)**: one round instead of two and fewer exponentiations, but a hash to the curve (CPace) or fixed points $M$ and $N$ (SPAKE2).

## When to use it

Use J-PAKE when two devices share a password or a pairing code, and the platform already uses it, such as Thread. For a new design, [CPace](/cpace/) is the CFRG recommendation for a balanced PAKE: it has one round, costs less and has a UC proof. Use an augmented PAKE such as [OPAQUE](/opaque/) for client-server logins.

## Pitfalls

- **No proof check.** Without line L3 or L5, an attacker can send values whose exponents it does not know and then test passwords offline. Verify every proof before line L4 and line L6.
- **No identity in the proof.** If line L9 omits the UserID, an attacker can reflect a party's own proof back to it. Include the sender's identity and reject a proof made with one's own identity.
- **$x_2 = 0$ or $G_4 = 1$.** Then the round 2 value does not depend on the password. Lines L1 and L3 exclude it.
- **No subgroup check.** Line L11 must check that $X$ and $V$ lie in the subgroup of order $q$; on a curve, that the point is on the curve.
- **A password reduced to 0.** The page requires $s \ne 0 \bmod q$; derive $s$ with a hash that gives $s \in [1, q)$.
- **Using K directly.** $K$ is a group element; derive the session key with a KDF (line L7).

## Implementations

The Python code gives `zkp_prove` and `zkp_verify` (lines L8 to L11), and a `Party` with `round1` (lines L1 and L2), `round2` (lines L3 and L4) and `finish` (lines L5 to L7), plus `confirm_tag` and `run`. The tests check the group, the binding of a proof to its base, value and identity, agreement, the failure of key confirmation with a wrong password, and the rejection of a round 1 message reflected back to its sender.

J-PAKE was used in Firefox Sync for device pairing until Mozilla replaced that pairing method with Firefox Accounts, and OpenSSL shipped an experimental implementation that it later removed. Mbed TLS and Bouncy Castle implement EC-J-PAKE or J-PAKE.

## History

Hao and Ryan presented J-PAKE at the Security Protocols Workshop in Cambridge in 2008 (proceedings 2011) and in the journal Transactions on Computational Science in 2010, as a PAKE whose security rests on zero-knowledge proofs rather than an ideal cipher or fixed parameters. Firefox Sync used it for pairing devices, and Thread adopted EC-J-PAKE for network commissioning. RFC 8236 and RFC 8235 were published as independent submissions in 2017. Abdalla, Benhamouda and MacKenzie gave the first security proof in 2015. In the CFRG PAKE selection of 2019 and 2020, J-PAKE was a candidate but was not selected.

## References
