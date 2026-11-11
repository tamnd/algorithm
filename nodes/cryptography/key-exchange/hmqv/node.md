---
tag: 294GKW
kind: algorithm
slug: hmqv
name: HMQV
aliases:
- Hashed MQV
area: cryptography/key-exchange
level: research
summary: MQV with d = H(X, B) and e = H(Y, A), so that each half-length value binds the ephemeral key to the peer's identity. It has a security proof in the random oracle model.
solves: [key-agreement-problem]
model: word-ram
complexity:
  vars: {m: the number of binary digits of the prime p}
  time: {worst: Θ(m^3), average: Θ(m^3), best: Θ(m^3)}
  space: {extra: Θ(m)}
properties: {deterministic: false, randomized: true}
history:
  year: 2005
  people: [Hugo Krawczyk]
  note: Krawczyk presented HMQV at CRYPTO 2005 with a proof in the Canetti-Krawczyk model; Menezes questioned parts of the proof in 2007.
prereqs: [mqv]
see_also: [authenticated-key-exchange, key-compromise-impersonation, perfect-forward-secrecy, unknown-key-share-attack, random-oracle-model, computational-diffie-hellman, schnorr-signature, sigma-key-exchange]
sources:
  - paper: "Hugo Krawczyk, HMQV: a high-performance secure Diffie-Hellman protocol, CRYPTO 2005, LNCS 3621, Springer, 2005, pages 546 to 566"
    locator: the protocol, the XCR and DCR signatures, the proof in the Canetti-Krawczyk model, and the generic attack showing that two-message protocols have only weak PFS; full version IACR ePrint 2005/176
  - paper: "Alfred Menezes, Another look at HMQV, Journal of Mathematical Cryptology 1(1), 2007, pages 47 to 64, doi:10.1515/JMC.2007.004"
    locator: the flaws in the proof, and the attacks on HMQV without validation of public keys
  - paper: "Laurie Law, Alfred Menezes, Minghua Qu, Jerry Solinas and Scott Vanstone, An efficient protocol for authenticated key agreement, Designs, Codes and Cryptography 28(2), 2003, pages 119 to 134"
    locator: MQV, the protocol that HMQV changes
  - paper: "Ran Canetti and Hugo Krawczyk, Analysis of key-exchange protocols and their use for building secure channels, EUROCRYPT 2001, LNCS 2045, Springer, 2001, pages 453 to 474"
    locator: the security model (CK) used in the proof
---

HMQV (hashed MQV) is Krawczyk's change to the [MQV](/mqv/) key agreement. The messages and the computation are as in MQV: $\hat A$ computes $\sigma = (Y B^e)^{x + d a}$ and $\hat B$ computes $\sigma = (X A^d)^{y + e b}$. But the half-length values are hashes, $d = \bar H(X, \hat B)$ and $e = \bar H(Y, \hat A)$, in place of bits of $X$ and $Y$, and the key is $K = H(\sigma)$. This small change binds each ephemeral value to the identity of the intended peer, stops the unknown key-share attacks on MQV, and allows a proof in the [random oracle model](/random-oracle-model/). The cost is the same as MQV.

**Notation.** As on the [MQV](/mqv/) page: $G = \langle g \rangle$ has prime order $q$, $\hat A$ has $(a, A)$ and $(x, X)$, $\hat B$ has $(b, B)$ and $(y, Y)$. $\bar H$ is a hash function with outputs of $l = \lceil \lceil \log_2 q \rceil / 2 \rceil$ bits, and $H$ is a hash function for the key.

## In plain words

HMQV works like MQV: each person mixes a long-term key and a fresh key into one secret number, and the two people combine their numbers so that only they get the same result.

MQV takes the short multiplier for the long-term key from the bits of the fresh public key. HMQV takes it from a hash of the fresh public key together with the name of the other person. So a value that one person makes for a talk with Bob is useless in a talk with anybody else.

This one change lets Krawczyk prove the protocol secure under clear assumptions, at no extra cost.

## The problem

The same as for [MQV](/mqv/): an [authenticated key exchange](/authenticated-key-exchange/) with two messages, static Diffie-Hellman keys and no signatures, now with a proof of security in a standard model of key exchange, resistance to [key compromise impersonation](/key-compromise-impersonation/), and the best [forward secrecy](/perfect-forward-secrecy/) that a two-message protocol can have.

## The algorithm

$\hat A$ sends $X$ and $\hat B$ sends $Y$, in any order. The pseudocode is $\hat A$'s side; $\hat B$'s side swaps the roles.

```pseudo id=main
HMQV-KEY(Â, B̂, a, x, B, Y)                       ▷ own name, peer name, own secrets, peer values
L1  X ← g^x                                       ▷ sent to the peer
L2  if B ∉ G or Y ∉ G then fail                   ▷ validation (see Pitfalls)
L3  d ← H̄(X, B̂); e ← H̄(Y, Â)                    ▷ l-bit hashes
L4  s_A ← (x + d · a) mod q
L5  σ ← (Y · B^e)^(s_A)
L6  return K = H(σ)                               ▷ then erase x and s_A
```

Line L3 is the only change from MQV. Krawczyk explains the design with a "dual" signature. The value $(Y B^e)^{x + d a}$ is a signature of $\hat A$ and $\hat B$ together on the pair of messages $(X, Y)$: only someone who knows $a$ and $x$, or $b$ and $y$, can compute it. He calls it the dual exponential challenge-response (DCR) signature, and proves that it cannot be forged when $\bar H$ is a random oracle and the computational Diffie-Hellman problem is hard. Because $d$ hashes $\hat B$'s name, the value $X A^d$ is only good for a session with $\hat B$.

**About the code.** The Python code of this page uses a 256-bit safe prime with $q$ of 255 bits, so $l = 128$; $\bar H$ is SHA-256 truncated to 128 bits. It is for study only. It is not constant time, and it must not protect real data. Use a vetted library, for example a [Noise](/noise-protocol-framework/) or TLS 1.3 implementation; Few libraries offer HMQV, and there are no official test vectors. The tests check agreement against the direct formula $g^{(x + d a)(y + e b)}$.

## Example

Take $p = 2039$, $q = 1019$, $g = 4$, and let $\bar H$ be the first 5 bits of SHA-256 over the length-prefixed value and name (as in the code), with names "alice" and "bob".

| value | Alice | Bob |
|---|---|---|
| static | $a = 57$, $A = 1556$ | $b = 311$, $B = 1502$ |
| ephemeral | $x = 100$, $X = 1153$ | $y = 200$, $Y = 2020$ |
| L3 | $d = \bar H(1153, \text{bob}) = 9$, $e = \bar H(2020, \text{alice}) = 15$ | same $d$ and $e$ |
| L4 | $s_A = 100 + 9 \cdot 57 \bmod 1019 = 613$ | $s_B = 200 + 15 \cdot 311 \bmod 1019 = 789$ |
| L5 | $Y B^{15} \bmod 2039 = 1332$, $\sigma = 1332^{613} \bmod 2039 = 200$ | $X A^{9} \bmod 2039 = 776$, $\sigma = 776^{789} \bmod 2039 = 200$ |

Both get $\sigma = 200 = 4^{613 \cdot 789 \bmod 1019}$. With MQV the same keys gave $d = 33$, $e = 36$ and $\sigma = 1795$.

## Correctness

$X A^d = g^{x + d a} = g^{s_A}$ and $Y B^e = g^{s_B}$. Both parties compute $d$ from $(X, \hat B)$ and $e$ from $(Y, \hat A)$, so they use the same values, and both get $g^{s_A s_B}$. The proof is below.

The security claims of Krawczyk's paper, under the assumptions as he states them, are these. HMQV is secure in the Canetti-Krawczyk model in the random oracle model under the computational Diffie-Hellman assumption, with weak perfect forward secrecy. Resistance to key compromise impersonation, and security when ephemeral secrets leak, need the gap Diffie-Hellman assumption and the knowledge of exponent assumption KEA1 as well. Menezes (2007) found errors in the proof and attacks on versions without public-key validation; the argument has since been revised, so read the claims with the current full version.

## Complexity

As MQV: one exponentiation for $X$ (can be precomputed), one half-length and one full exponentiation at line L5 (about 1.2 full ones with simultaneous exponentiation), plus validation at line L2. That is $\Theta(m^3)$ bit operations with schoolbook arithmetic and $\Theta(m)$ space. The two hashes at line L3 cost almost nothing.

## Properties

- **Implicit mutual authentication** with two messages and no signatures.
- **No unknown key share.** $d$ and $e$ bind the identities, so the [Kaliski attack](/unknown-key-share-attack/) on MQV fails even though $K = H(\sigma)$ holds no names. The tests show this.
- **Key compromise impersonation resistance**, under the stronger assumptions above.
- **Weak PFS only.** Krawczyk showed a generic attack: in any two-message protocol with implicit authentication, an attacker who plays $\hat A$ with its own $x'$ and later learns $a$ can compute $\hat B$'s key of that session. The tests run this attack. Sessions in which the attacker was passive stay secret after the static keys leak.

## Variants and improvements

- **One-pass HMQV.** $\hat B$ uses $y = b$ and $e = 0$, for one-way messages; it has no forward secrecy for the receiver.
- **HMQV-C.** Adds [key confirmation](/key-confirmation/) MACs in a third message, which gives full PFS.
- **FHMQV and others.** Later protocols by other authors change the hashes to get proofs in stronger models (such as eCK) or under weaker assumptions.
- **Signed and KEM-based protocols.** [SIGMA](/sigma-key-exchange/) and the [Noise](/noise-protocol-framework/) patterns are the usual choices in deployed systems.

## When to use it

HMQV is a good fit when both parties have static Diffie-Hellman keys and the cost of signatures matters, and when a third message for confirmation is acceptable. Its main uses are in research and in specialised systems; standard protocols (TLS 1.3, IKEv2, Noise) do not use it.

## Pitfalls

- **Skipped validation at line L2.** Krawczyk's paper argued that some checks could be omitted. Menezes (2007) showed attacks when the static or ephemeral public keys are not validated in some groups. Check that $B$ and $Y$ lie in $G$, as the code does.
- **Ephemeral leakage.** If $x$ and $s_A$ are not erased after line L6, a leaked $s_A$ gives the session key, and $s_A$ with $x$ gives $a = (s_A - x) / d \bmod q$.
- **Wrong hash inputs at line L3.** $d$ must hash $X$ with the peer's name $\hat B$, and $e$ must hash $Y$ with $\hat A$. With the names left out the protocol is MQV again, with its unknown key-share attack.
- **Full PFS assumed.** Without a confirmation step, an active attacker who later gets $a$ can read sessions it took part in as $\hat A$.

## Implementations

## History

Krawczyk presented HMQV at CRYPTO 2005, with a long full version on IACR ePrint (2005/176). The paper also defined the XCR and DCR signatures and showed that no two-message implicitly authenticated protocol can have full PFS. Menezes' "Another look at HMQV" (2007) pointed out errors in the proof and attacks when validation is left out, which started a debate on the role of proofs; this was part of the "another look" papers of Koblitz and Menezes. Many later protocols, such as FHMQV and the eCK-secure protocols, build on its design.

## References
