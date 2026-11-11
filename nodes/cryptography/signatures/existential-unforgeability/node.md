---
tag: AK19SW
kind: definition
slug: existential-unforgeability
name: Existential unforgeability
aliases:
- EUF-CMA
- unforgeability under chosen-message attack
- existential unforgeability under adaptive chosen-message attack
area: cryptography/signatures
level: core
summary: "EUF-CMA: no efficient adversary with a signing oracle can output a valid signature on any message it did not query. The standard security notion for signatures (Goldwasser, Micali and Rivest 1988)."
prereqs: [signature-scheme]
see_also: [strong-unforgeability, chosen-message-attack, key-only-attack, signature-forgery, random-oracle-model, one-way-function, forking-lemma, message-authentication-code]
sources:
  - paper: "Shafi Goldwasser, Silvio Micali and Ronald L. Rivest, A digital signature scheme secure against adaptive chosen-message attacks, SIAM Journal on Computing 17(2), pages 281 to 308, 1988"
    locator: the classification of attacks (key-only, known-message, generic, directed and adaptive chosen-message) and of breaks (total break, universal, selective and existential forgery), and the first scheme secure against adaptive chosen-message attack
  - paper: "Moni Naor and Moti Yung, Universal one-way hash functions and their cryptographic applications, STOC 1989, pages 33 to 43"
    locator: secure signatures from universal one-way hash functions, and so from one-way permutations
  - paper: "John Rompel, One-way functions are necessary and sufficient for secure signatures, STOC 1990, pages 387 to 394"
    locator: universal one-way hash functions, and so secure signatures, from any one-way function
  - paper: "Russell Impagliazzo and Michael Luby, One-way functions are essential for complexity based cryptography, FOCS 1989, pages 230 to 235"
    locator: secure signature schemes imply one-way functions
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, 2020
    locator: Chapter 13, the experiment Sig-forge and the definition of a secure signature scheme
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 11, Section 11.2.4, types of attacks on signature schemes
---

Existential unforgeability under adaptive chosen-message attack (EUF-CMA) is the standard security notion for a [signature scheme](/signature-scheme/). It says that an efficient adversary who gets the public key and signatures on messages of its own choice, chosen one after another, cannot produce a valid signature on any message it did not ask to have signed. It is the strongest attack combined with the weakest goal in the classification of Goldwasser, Micali and Rivest (1988), so a scheme that meets it resists every attack in that classification. Signature schemes with this property exist if and only if [one-way functions](/one-way-function/) exist.

**Notation.** $\Pi = (\mathrm{KeyGen}, \mathrm{Sign}, \mathrm{Verify})$ is a signature scheme and $\lambda$ the security parameter. $A$ is an adversary with running time $t$ that makes $q_s$ queries to a signing oracle and, in the [random oracle model](/random-oracle-model/), $q_h$ queries to the hash oracle $H$. $Q$ is the set of messages that $A$ submitted to the signing oracle. $\mathrm{Adv}^{\mathrm{euf\text{-}cma}}_{\Pi}(A)$ is the probability that $A$ wins the game below, and $\varepsilon$ is a bound on it. The definition is made in the standard model; a scheme that uses a hash function proved in the random oracle model is said to be EUF-CMA in the ROM.

## Definition

**The game $\mathrm{Exp}^{\mathrm{euf\text{-}cma}}_{\Pi, A}(\lambda)$.**

1. The challenger runs $(pk, sk) \leftarrow \mathrm{KeyGen}(1^\lambda)$ and sets $Q \leftarrow \emptyset$.
2. The challenger runs $A(pk)$. Whenever $A$ submits a message $m \in \mathcal{M}_{pk}$, the challenger computes $\sigma \leftarrow \mathrm{Sign}(sk, m)$, adds $m$ to $Q$ and returns $\sigma$ to $A$. $A$ chooses each query after it sees the answers to the earlier ones. For a stateful scheme the challenger updates the state after each query.
3. $A$ outputs a pair $(m^*, \sigma^*)$.
4. The game outputs 1 if $\mathrm{Verify}(pk, m^*, \sigma^*) = 1$ and $m^* \notin Q$, and 0 otherwise.

The advantage of $A$ is $\mathrm{Adv}^{\mathrm{euf\text{-}cma}}_{\Pi}(A) = \Pr[\mathrm{Exp}^{\mathrm{euf\text{-}cma}}_{\Pi, A}(\lambda) = 1]$, over the coins of KeyGen, Sign and $A$.

**Asymptotic form.** $\Pi$ is EUF-CMA secure if for every probabilistic polynomial-time $A$ the advantage is a negligible function of $\lambda$.

**Concrete form.** $\Pi$ is $(t, q_s, \varepsilon)$-EUF-CMA secure if every $A$ that runs in time at most $t$ and makes at most $q_s$ signing queries has advantage at most $\varepsilon$. In the random oracle model the bound is $(t, q_s, q_h, \varepsilon)$, and $A$ also has access to $H$. A security proof turns $A$ into an algorithm $B$ for a hard problem with time $t'$ and success $\varepsilon'$; it is tight if $\varepsilon' \approx \varepsilon$ and $t' \approx t$, and it loses a factor $L$ if $\varepsilon' \approx \varepsilon / L$. For example, [RSA-FDH](/rsa-fdh/) loses a factor about $q_s$, and [RSA-PSS](/rsa-pss/) is tight.

**The forgery condition.** The new pair must have a new message: $m^* \notin Q$. A new signature on an old message does not count. The notion that also counts it is [strong unforgeability](/strong-unforgeability/) (SUF-CMA), where the condition is $(m^*, \sigma^*) \notin \{(m_i, \sigma_i)\}$.

**The hierarchy of attacks (GMR 1988).** The attacks differ in what $A$ gets before it forges. From weakest to strongest:

1. **Key-only attack.** $A$ gets only $pk$. See [key-only attack](/key-only-attack/).
2. **Known-message attack.** $A$ gets $pk$ and signatures on messages that it does not choose, for example messages drawn from a distribution.
3. **Generic chosen-message attack.** $A$ chooses the messages before it sees $pk$; the list is the same for every key.
4. **Directed chosen-message attack.** $A$ chooses the list after it sees $pk$, but all at once, before it gets any signature.
5. **Adaptive chosen-message attack.** $A$ chooses each message after it sees $pk$ and the earlier signatures. This is the game above. See [chosen-message attack](/chosen-message-attack/).

Attacks 3 and 4 are the non-adaptive chosen-message attacks; later work often names them together as naCMA.

**The hierarchy of breaks (GMR 1988).** The goals differ in what $A$ must achieve. From strongest to weakest:

1. **Total break.** $A$ computes $sk$, or an equivalent trapdoor.
2. **Universal forgery.** $A$ gets an efficient algorithm that signs every message, without necessarily knowing $sk$.
3. **Selective forgery.** $A$ forges a signature on a message that it fixed before the attack.
4. **Existential forgery.** $A$ forges a signature on at least one message, which it may not control. This is the goal in the game above.

A scheme is secure in the strongest sense when no attack in the first list reaches even the weakest goal in the second list. Each pair (attack, break) gives a notion, for example UF-KOA (universal forgery under key-only attack) or EUF-KMA. EUF-CMA implies all of them, because an adversary for any weaker pair is also an adversary in the EUF-CMA game.

**Existence.** Naor and Yung (1989) built EUF-CMA signatures from universal one-way hash functions, and so from any one-way permutation. Rompel (1990) built universal one-way hash functions from any one-way function. So EUF-CMA signatures exist if one-way functions exist. Conversely, Impagliazzo and Luby (1989) showed that secure signatures imply one-way functions. These constructions are in the standard model and are not efficient; deployed schemes rely on specific assumptions.

## Examples and non-examples

- **Textbook RSA is not EUF-CMA.** Take the toy key $N = 3233 = 61 \cdot 53$, $e = 17$, $d = 2753$, and $\mathrm{Sign}(m) = m^d \bmod N$. The adversary queries $m_1 = 2$ and $m_2 = 3$ and gets $\sigma_1 = 1027$ and $\sigma_2 = 1857$. It outputs $m^* = 6$ and $\sigma^* = 1027 \cdot 1857 \bmod 3233 = 2902$. Then $2902^{17} \bmod 3233 = 6$ and $6 \notin Q$, so it wins with probability 1 and two queries. With no query at all it can also output $\sigma^* = 1234$ and $m^* = 1234^{17} \bmod 3233 = 2183$: an existential forgery under a key-only attack.
- **Hashed RSA.** [RSA-FDH](/rsa-fdh/) and [RSA-PSS](/rsa-pss/) are EUF-CMA in the random oracle model under the [RSA assumption](/rsa-problem/). The multiplicative relation of the toy example disappears because the forger would need $H(m^*) = H(m_1) H(m_2) \bmod N$.
- **Schnorr and EdDSA.** [Schnorr signatures](/schnorr-signature/) are EUF-CMA in the ROM under the discrete logarithm assumption, through the [forking lemma](/forking-lemma/), with a loss of about $q_h$. [Ed25519](/ed25519/) is analysed in the same way.
- **One-time schemes.** [Lamport](/lamport-signature/) signatures are EUF-CMA if $q_s \le 1$, under the one-wayness of the hash. With two signatures on suitable messages the adversary learns both preimages at some positions and forges, so the scheme is not EUF-CMA for $q_s = 2$.
- **Standard-model schemes.** The GMR scheme (factoring), and later Cramer and Shoup (strong RSA) and Waters (CDH in pairing groups), meet the notion without random oracles.
- **DSA and ECDSA.** There is no proof of EUF-CMA for [DSA](/dsa/) or [ECDSA](/ecdsa/) from the discrete logarithm assumption alone; known proofs use idealized models of the group or of the conversion function.

## Related definitions

- **[Strong unforgeability](/strong-unforgeability/).** Also forbids new signatures on queried messages. EUF-CMA plus unique signatures implies it.
- **[Chosen-message attack](/chosen-message-attack/) and [key-only attack](/key-only-attack/).** The attack models of the hierarchy, with worked attacks.
- **[Signature forgery](/signature-forgery/).** Real forgeries against deployed systems.
- **MAC unforgeability.** The same game for a [message authentication code](/message-authentication-code/), with a tag oracle and no public key; in the MAC game the adversary may also need a verification oracle.
- **Multi-user security.** The adversary gets many public keys and wins by forging under any of them. A generic reduction loses a factor of the number of users.
- **[Random oracle model](/random-oracle-model/).** The hash is an oracle that both the scheme and the adversary query; $q_h$ counts these queries.

## References
