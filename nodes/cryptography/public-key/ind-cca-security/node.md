---
tag: W29Z86
kind: definition
slug: ind-cca-security
name: IND-CCA security
aliases:
- IND-CCA2
- chosen-ciphertext security
- indistinguishability under chosen-ciphertext attack
area: cryptography/public-key
level: advanced
summary: IND-CPA where the adversary may also decrypt any ciphertext except the challenge. IND-CCA1 allows this only before the challenge, IND-CCA2 also after. IND-CCA2 is the standard goal.
prereqs: [ind-cpa-security, chosen-ciphertext-attack]
see_also: [non-malleability, cramer-shoup-cryptosystem, naor-yung-paradigm, fujisaki-okamoto-transform, rsa-oaep, hybrid-encryption, key-encapsulation-mechanism, authenticated-encryption]
sources:
  - paper: "Moni Naor and Moti Yung, Public-key cryptosystems provably secure against chosen ciphertext attacks, STOC 1990, pages 427 to 437"
    locator: the lunchtime attack (IND-CCA1) and the first scheme secure against it
  - paper: "Charles Rackoff and Daniel R. Simon, Non-interactive zero-knowledge proof of knowledge and chosen ciphertext attack, CRYPTO 1991, LNCS 576, pages 433 to 444"
    locator: the adaptive attack (IND-CCA2)
  - paper: "Mihir Bellare, Anand Desai, David Pointcheval and Phillip Rogaway, Relations among notions of security for public-key encryption schemes, CRYPTO 1998, LNCS 1462, pages 26 to 45"
    locator: the definitions of IND-CCA1 and IND-CCA2, the implications and separations, and the equivalence of IND-CCA2 and NM-CCA2
  - paper: "Danny Dolev, Cynthia Dwork and Moni Naor, Nonmalleable cryptography, SIAM Journal on Computing 30(2), pages 391 to 437, 2000"
    locator: the first scheme secure against adaptive chosen-ciphertext attacks
  - paper: "Ran Canetti, Hugo Krawczyk and Jesper Buus Nielsen, Relaxing chosen-ciphertext security, CRYPTO 2003, LNCS 2729, pages 565 to 582"
    locator: the definition of replayable CCA (RCCA) security
  - paper: "Ronald Cramer and Victor Shoup, A practical public key cryptosystem provably secure against adaptive chosen ciphertext attack, CRYPTO 1998, LNCS 1462, pages 13 to 25"
    locator: the first practical IND-CCA2 scheme in the standard model, and the variant secure against lunchtime attacks
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 12, the definition of CCA security for public-key encryption
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 12, chosen ciphertext secure public key encryption
---

IND-CCA security is [IND-CPA security](/ind-cpa-security/) against an adversary that may also ask for the decryption of ciphertexts of its choice. In IND-CCA1, the lunchtime notion of Naor and Yung (1990), the decryption oracle is available only before the challenge ciphertext; in IND-CCA2, the adaptive notion of Rackoff and Simon (1991), it is available before and after, for every ciphertext except the challenge. IND-CCA2 is what "IND-CCA" means without a qualifier, and it is the standard goal for public-key encryption and [KEMs](/key-encapsulation-mechanism/): it models the [chosen-ciphertext attacks](/chosen-ciphertext-attack/) of real servers, and it is equivalent to [non-malleability](/non-malleability/) under the same attack.

**Notation.** $\Pi = (\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$ is a public-key encryption scheme, $\lambda$ the security parameter, and $\bot$ the rejection symbol. $\mathcal{A}$ is an adversary that runs in time $t$ and makes $q_d$ decryption queries. $\mathrm{Adv} = |\Pr[b' = 1 \mid b = 1] - \Pr[b' = 1 \mid b = 0]|$. The definition is the same in the standard model and in the [random oracle model](/random-oracle-model/); in the second, $\mathcal{A}$ also makes $q_h$ hash queries.

## Definition

**The game.** For a bit $b$, the experiment $\mathrm{IND\text{-}CCA2}^b_\Pi(\mathcal{A})$ runs as follows.

1. $(pk, sk) \leftarrow \mathrm{Gen}(1^\lambda)$. $\mathcal{A}$ gets $pk$.
2. *Phase 1.* $\mathcal{A}$ may ask the oracle $\mathrm{Dec}(sk, \cdot)$ on any ciphertexts.
3. $\mathcal{A}$ outputs $m_0, m_1$ with $|m_0| = |m_1|$, and gets $c^* \leftarrow \mathrm{Enc}(pk, m_b)$.
4. *Phase 2.* $\mathcal{A}$ may ask the oracle on any ciphertext $c \ne c^*$.
5. $\mathcal{A}$ outputs a bit $b'$.

$$\mathrm{Adv}^{\mathrm{ind\text{-}cca2}}_\Pi(\mathcal{A}) = \bigl|\Pr[\mathrm{IND\text{-}CCA2}^1_\Pi(\mathcal{A}) = 1] - \Pr[\mathrm{IND\text{-}CCA2}^0_\Pi(\mathcal{A}) = 1]\bigr|.$$

$\Pi$ is **IND-CCA2 secure** if this advantage is negligible in $\lambda$ for every adversary that runs in time polynomial in $\lambda$. The total number of queries $q_d$ in both phases is part of the concrete bound.

**IND-CCA1** is the same game without phase 2: once $\mathcal{A}$ has $c^*$, it can no longer decrypt. This is the lunchtime attack: the adversary used the decryption box while its owner was away, and must then work on the target alone.

### Why the challenge is excluded

Without the rule $c \ne c^*$, $\mathcal{A}$ would ask for $\mathrm{Dec}(sk, c^*) = m_b$ and win with advantage 1, so no scheme would be secure. The rule excludes only the exact string $c^*$. Every other string is allowed, including strings that decrypt to $m_b$. So an IND-CCA2 scheme must make every change of $c^*$ either invalid or unrelated to $m_b$, and this is what rules out malleable schemes.

A consequence is that IND-CCA2 is fragile under trivial changes. If $\Pi'$ appends a bit to each ciphertext and $\mathrm{Dec}'$ ignores it, then $c^* \Vert 1$ is a different ciphertext with the same plaintext, and $\Pi'$ is not IND-CCA2, although it seems no less secure than $\Pi$. Replayable CCA, below, accepts such schemes.

### Implications

**Theorem 1 (Bellare, Desai, Pointcheval and Rogaway, 1998).** IND-CCA2 implies IND-CCA1, which implies IND-CPA. If any IND-CPA scheme exists, there are schemes that are IND-CPA but not IND-CCA1, and schemes that are IND-CCA1 but not IND-CCA2.

The implications hold because the adversaries of a weaker game are adversaries of the stronger game that make fewer queries. The separations modify a secure scheme so that a decryption query reveals the key, either at any time or only after a challenge.

**Theorem 2 (one challenge implies many).** Let the left-or-right IND-CCA2 game give $\mathcal{A}$ an oracle $\mathrm{LR}_b(m_0, m_1)$, at most $q$ times, and a decryption oracle that refuses every ciphertext returned by $\mathrm{LR}_b$. Then there is a one-challenge adversary $\mathcal{B}$ with

$$\mathrm{Adv}^{\mathrm{lor\text{-}cca2}}(\mathcal{A}) \le q \cdot \mathrm{Adv}^{\mathrm{ind\text{-}cca2}}(\mathcal{B}).$$

*Proof.* Use the hybrids $H_0, \ldots, H_q$ of the [IND-CPA proof](/ind-cpa-security/): $\mathcal{B}$ picks $i$, answers the calls $j \ne i$ with encryptions it makes itself, and embeds its challenge at call $i$. It answers a decryption query with its own oracle, except that for a ciphertext it made itself at call $j$ it returns $\bot$, as the game requires. The query $c^*$ never reaches its own oracle. The rest is as before. $\square$

**Theorem 3 (Bellare, Desai, Pointcheval and Rogaway, 1998).** IND-CCA2 is equivalent to NM-CCA2, non-malleability under adaptive chosen-ciphertext attack. Under weaker attacks non-malleability is strictly stronger than indistinguishability; see [non-malleability](/non-malleability/).

### Replayable CCA

Canetti, Krawczyk and Nielsen (2003) defined replayable CCA (RCCA) security. The game is the same, but in phase 2 the oracle answers "test" for every ciphertext that decrypts to $m_0$ or $m_1$, instead of refusing only $c^*$. An RCCA secure scheme may allow anyone to turn $c^*$ into a new ciphertext of the same message, but into nothing else. This is enough for most uses where the message itself is what matters, such as key exchange and secure channels with replay protection, and it admits rerandomizable schemes. IND-CCA2 implies RCCA, and the scheme $\Pi'$ above is RCCA secure.

## Examples and non-examples

| scheme | IND-CCA2? | assumption and model |
|---|---|---|
| [Cramer-Shoup](/cramer-shoup-cryptosystem/) | yes | DDH and a target collision resistant hash, standard model |
| [RSA-OAEP](/rsa-oaep/) | yes | RSA, random oracle model |
| [ECIES](/ecies/), DHIES | yes | gap Diffie-Hellman, random oracle model, or oracle Diffie-Hellman |
| [Fujisaki-Okamoto](/fujisaki-okamoto-transform/) schemes, including [ML-KEM](/crystals-kyber/) | yes | the underlying problem, random oracle model or quantum random oracle model |
| [Naor-Yung](/naor-yung-paradigm/) with simulation-sound proofs (Sahai 1999), DDN | yes | general assumptions, standard model |
| Cramer-Shoup without the hash ("lite") | IND-CCA1 only | DDH, standard model |
| [ElGamal](/elgamal-encryption/), [Paillier](/paillier-cryptosystem/), [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) | no | each has a public homomorphism |
| textbook [RSA](/rsa-cryptosystem/), [Rabin](/rabin-cryptosystem/), [Blum-Goldwasser](/blum-goldwasser-cryptosystem/) | no | one query recovers the message or the key |
| [RSA PKCS #1 v1.5](/rsa-pkcs1-v1-5-encryption/) | no | Bleichenbacher's validity oracle |

**No homomorphic scheme is IND-CCA2.** Suppose an efficient public operation maps any ciphertext of $m$ to a ciphertext of $f(m)$, for a known function $f$ with $f(m_0) \ne f(m_1)$. The adversary applies it to $c^*$, gets a ciphertext $c$ that differs from $c^*$, asks for its decryption, and checks whether the answer is $f(m_0)$ or $f(m_1)$. If the operation could return $c^*$ itself, rerandomize first. This is why [homomorphic encryption](/homomorphic-encryption/) aims at IND-CPA, or at weaker variants of CCA1.

## Related definitions

- **[IND-CPA security](/ind-cpa-security/).** The same game with no decryption oracle.
- **[Non-malleability](/non-malleability/).** The adversary must not be able to make a ciphertext of a related message. NM-CCA2 equals IND-CCA2.
- **IND-CCA for a [KEM](/key-encapsulation-mechanism/).** The challenge is an encapsulation with a real or a random key, and the oracle decapsulates every other ciphertext. With a one-time secure DEM it gives IND-CCA2 [hybrid encryption](/hybrid-encryption/).
- **Plaintext awareness.** An adversary that outputs a valid ciphertext must "know" its plaintext. Together with IND-CPA it implies IND-CCA2 in the random oracle model (Bellare, Desai, Pointcheval and Rogaway, 1998).
- **Replayable CCA and benign malleability.** Weaker notions that allow changes which keep the message, as described above.
- **Authenticated encryption.** The symmetric notion that gives chosen-ciphertext security for [symmetric encryption](/symmetric-encryption/); see [authenticated encryption](/authenticated-encryption/).

## References
