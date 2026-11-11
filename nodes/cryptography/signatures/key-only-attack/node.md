---
tag: XJ1ZFG
kind: definition
slug: key-only-attack
name: Key-only attack
aliases:
- no-message attack
- KOA
- EUF-NMA
area: cryptography/signatures
level: intro
summary: The weakest attack on a signature scheme. The adversary knows only the public key, sees no signature, and must output a valid pair (message, signature).
prereqs: [signature-scheme]
see_also: [chosen-message-attack, existential-unforgeability, signature-forgery, rsa-signature, elgamal-signature, schnorr-signature, forking-lemma, hash-and-sign-paradigm]
sources:
  - paper: "Shafi Goldwasser, Silvio Micali and Ronald L. Rivest, A digital signature scheme secure against adaptive chosen-message attacks, SIAM Journal on Computing 17(2), pages 281 to 308, 1988"
    locator: Section 3, the classes of attacks (key-only attacks and the message attacks) and the kinds of break (total break, universal, selective and existential forgery)
  - paper: "Taher ElGamal, A public key cryptosystem and a signature scheme based on discrete logarithms, IEEE Transactions on Information Theory 31(4), pages 469 to 472, 1985"
    locator: the remark that, without a hash, signatures can be made for messages that the forger cannot choose
  - paper: "David Pointcheval and Jacques Stern, Security arguments for digital signatures and blind signatures, Journal of Cryptology 13(3), pages 361 to 396, 2000"
    locator: the no-message attack, the forking lemma for it, and the simulation of signatures that extends the result to adaptive chosen-message attacks
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 11.2.4 (types of attacks on signature schemes, key-only attacks), Note 11.66(iii) (existential forgery of ElGamal without a hash)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, 2020
    locator: Chapter 13, the attack on plain RSA signatures that uses no signature
---

A key-only attack is the weakest attack model for a [signature scheme](/signature-scheme/). The adversary gets the public key and nothing else: no signature on any message, chosen or not. It wins if it outputs a message and a signature that verify. Goldwasser, Micali and Rivest (1988) put it at the bottom of their list of attacks; Pointcheval and Stern call it the no-message attack.

**Notation.** $\Pi = (\mathrm{KeyGen}, \mathrm{Sign}, \mathrm{Verify})$ is a signature scheme and $\lambda$ the security parameter. $A$ is an adversary that runs in time $t$. For RSA, $(N, e)$ is the public key and $d$ the private exponent. For ElGamal, $p$ is a prime, $g$ a generator of $\mathbb{Z}_p^*$, and $y = g^x \bmod p$ the public key.

## Definition

**The game $\mathrm{Exp}^{\mathrm{euf\text{-}koa}}_{\Pi, A}(\lambda)$.**

1. The challenger runs $(pk, sk) \leftarrow \mathrm{KeyGen}(1^\lambda)$.
2. The challenger runs $A(pk)$. $A$ has no oracle.
3. $A$ outputs a pair $(m^*, \sigma^*)$.
4. The game outputs 1 if $\mathrm{Verify}(pk, m^*, \sigma^*) = 1$, and 0 otherwise.

$\Pi$ is existentially unforgeable under a key-only attack (EUF-KOA, also written EUF-NMA or UF-NMA) if $\Pr[\mathrm{Exp}^{\mathrm{euf\text{-}koa}}_{\Pi, A}(\lambda) = 1]$ is negligible in $\lambda$ for every probabilistic polynomial-time $A$. There is no freshness condition, because $A$ has seen no signature: every valid output is a forgery.

**Goals.** The same attack model can be paired with a weaker goal. In a *selective* forgery the message is fixed before $A$ sees $pk$, or is chosen at random by the challenger, and $A$ must sign that message; in a *universal* forgery $A$ must be able to sign any given message; a *total break* recovers $sk$ or an equivalent algorithm. Existential forgery, the goal above, is the easiest to reach, so security against it is the strongest of these four.

**Relation to the other attacks.** A key-only adversary is a chosen-message adversary that makes no query. So for every $A$,

$$\Pr[\mathrm{Exp}^{\mathrm{euf\text{-}koa}}_{\Pi, A}(\lambda) = 1] \le \Pr[\mathrm{Exp}^{\mathrm{euf\text{-}cma}}_{\Pi, A}(\lambda) = 1],$$

and [EUF-CMA](/existential-unforgeability/) security implies EUF-KOA security. The converse is false. The known-message attack sits between the two: the adversary gets signatures on messages that it did not choose.

## Examples and non-examples

- **Textbook RSA is broken.** The signature of an integer $m$ is $s = m^d \bmod N$, and the verifier accepts if $s^e \equiv m \pmod N$. The adversary picks any $s$ and outputs $(m, s)$ with $m = s^e \bmod N$. With the toy key $N = 3233 = 61 \cdot 53$ and $e = 17$, the choice $s = 2$ gives $m = 2^{17} \bmod 3233 = 1752$, and indeed $1752^{2753} \bmod 3233 = 2$ with the private exponent $d = 2753$. The adversary does not control $m$, so this is an existential forgery and nothing more. See [RSA signature](/rsa-signature/).
- **ElGamal on raw integers is broken.** If the verifier checks $y^r r^s \equiv g^m \pmod p$ on the message $m$ itself, pick $u$ and $v$ with $\gcd(v, p - 1) = 1$ and set $r = g^u y^v \bmod p$, $s = -r v^{-1} \bmod (p - 1)$ and $m = s u \bmod (p - 1)$. Then $r + v s \equiv 0 \pmod{p - 1}$, so $y^r r^s = y^{r + v s} g^{u s} \equiv g^{u s} = g^m$. With the group of HAC Example 11.65 ($p = 2357$, $g = 2$, $y = 1185$) and $u = 3$, $v = 5$, this gives $r = 311$, $s = 409$ and $m = 1227$, and both sides equal 299. See [ElGamal signature](/elgamal-signature/).
- **The hash stops both attacks.** In a [hash-and-sign](/hash-and-sign-paradigm/) scheme the verifier checks the equation against $H(m)$, not $m$. The adversary can still pick $s$ and compute $s^e \bmod N$, but then it needs a message $m$ with $H(m) = s^e \bmod N$, which is a preimage. In the random oracle model, [RSA-FDH](/rsa-fdh/) is EUF-KOA secure if the RSA function is hard to invert.
- **Schnorr signatures, proved in two steps.** Pointcheval and Stern first prove that a key-only forger of a [Schnorr signature](/schnorr-signature/) in the random oracle model gives a discrete logarithm, with the [forking lemma](/forking-lemma/). Then they answer the signing queries of a chosen-message adversary without the key, by choosing the challenge and the response first and programming the oracle. This lifts the key-only result to EUF-CMA.
- **Key-only security is not enough.** Take an EUF-KOA scheme $\Pi$ and let $\Pi'$ sign the message $0^\lambda$ by returning $sk$ in addition to the signature. A key-only adversary never sees a signature, so $\Pi'$ is exactly as secure as $\Pi$ against it. A chosen-message adversary asks for the signature of $0^\lambda$ and gets $sk$: a total break. One-time schemes such as the [Lamport signature](/lamport-signature/) are a natural case: they resist key-only attacks and a single signature, but signatures on two messages often let anyone sign a third.

**The code.** The implementation folder has the two forgeries and the verifiers they beat. The tests check the values above and 200 random RSA forgeries and more than 50 random ElGamal forgeries against the local verifiers, and they check that a hashed RSA verifier rejects the forged pair. No official vector exists for these attacks. The code is for study only, is not constant time, and runs only on toy keys against local simulated verifiers.

## Related definitions

- **[Chosen-message attack](/chosen-message-attack/).** The adversary gets signatures on messages of its choice. It is the standard model, and security in it implies security against a key-only attack.
- **Known-message attack.** The adversary gets signatures on messages that it did not choose, for example on random messages.
- **[Existential unforgeability](/existential-unforgeability/).** The standard goal, usually paired with the adaptive chosen-message attack as EUF-CMA.
- **[Signature forgery](/signature-forgery/).** The general idea of making a signature without the key, and the real attacks that have done it.

## References
