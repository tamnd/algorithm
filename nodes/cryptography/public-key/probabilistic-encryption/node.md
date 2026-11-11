---
tag: 6YZSYC
kind: concept
slug: probabilistic-encryption
name: Probabilistic encryption
area: cryptography/public-key
level: advanced
summary: Encryption that uses fresh randomness, so one message has many ciphertexts. Goldwasser and Micali (1984) showed that public-key encryption needs it to hide all partial information.
prereqs: [ind-cpa-security]
see_also: [goldwasser-micali-cryptosystem, blum-goldwasser-cryptosystem, elgamal-encryption, semantic-security, hard-core-predicate, trapdoor-one-way-function, rsa-oaep, rsa-cryptosystem]
sources:
  - paper: doi:10.1016/0022-0000(84)90070-9
    title: Shafi Goldwasser and Silvio Micali, Probabilistic encryption, Journal of Computer and System Sciences 28(2), pages 270 to 299, 1984
    locator: the motivation (partial information leaked by deterministic schemes), the bitwise scheme and its security
  - paper: "Shafi Goldwasser and Silvio Micali, Probabilistic encryption and how to play mental poker keeping secret all partial information, STOC 1982, pages 365 to 377"
    locator: the conference version
  - paper: "Manuel Blum and Shafi Goldwasser, An efficient probabilistic public-key encryption scheme which hides all partial information, CRYPTO 1984, LNCS 196, pages 289 to 299"
    locator: the scheme with an expansion of a constant number of blocks
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 8, Remark 8.22 (randomized encryption), Section 8.7 (probabilistic public-key encryption), Note 8.53 (message expansion of Goldwasser-Micali)
  - paper: "Mihir Bellare, Alexandra Boldyreva and Adam O'Neill, Deterministic and efficiently searchable encryption, CRYPTO 2007, LNCS 4622, pages 535 to 552"
    locator: the security notion for deterministic public-key encryption of messages with high min-entropy
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 12, the remark that deterministic public-key encryption cannot be CPA secure, and the construction from trapdoor permutations
  - book: isbn:9780521830843
    title: Oded Goldreich, Foundations of Cryptography, Volume 2, Basic Applications, Cambridge University Press, 2004
    locator: Chapter 5, the constructions of public-key encryption from trapdoor permutations and hard-core predicates
---

Probabilistic encryption is encryption that draws fresh random values each time, so that one message has many possible ciphertexts and the same message encrypted twice looks different. Goldwasser and Micali introduced the idea in 1982, together with the first definition of what a ciphertext must hide, and showed that [public-key encryption](/public-key-encryption/) cannot meet that definition without it. Every scheme that is [IND-CPA secure](/ind-cpa-security/) is probabilistic, from [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) and [ElGamal](/elgamal-encryption/) to [RSA-OAEP](/rsa-oaep/) and ML-KEM. This page is about the concept; the [Goldwasser-Micali page](/goldwasser-micali-cryptosystem/) is about their scheme.

**Notation.** $\mathrm{Enc}(pk, m; r)$ is encryption with random value $r$. $\lambda$ is the security parameter and $\ell$ the length of a message. $\mathcal{A}$ is an adversary and $\mathrm{Adv}$ its advantage in the IND-CPA game. The statements here are in the standard model.

## In plain words

With a public key, anyone can lock any message. If the lock always gives the same result for the same message, an attacker who sees a locked message can guess the content, lock the guess with the public key, and compare. When the possible messages are few, such as "yes" or "no", or a salary from a short list, this finds the message at once.

Probabilistic encryption mixes fresh random values into every lock. The same message now gives a different result each time, so the attacker's own locked guess never matches. The price is that the locked message is longer than the original, because it must leave room for all the possible random values.

## The idea

**Deterministic public-key encryption leaks.** With a deterministic $\mathrm{Enc}$, an attacker who sees $c$ and suspects $m$ checks whether $\mathrm{Enc}(pk, m) = c$. This is a dictionary attack, and it wins the IND-CPA game with advantage 1. Deterministic schemes may also leak a function of every message. Textbook [RSA](/rsa-cryptosystem/) leaks the [Jacobi symbol](/jacobi-symbol/): for odd $e$, $\left(\frac{m^e}{n}\right) = \left(\frac{m}{n}\right)^e = \left(\frac{m}{n}\right)$, and anyone can compute it from $c$. Goldwasser and Micali asked for a scheme that hides *all* partial information, and showed that randomness is necessary for that.

**How much randomness.** Randomness must make each ciphertext unlikely.

*Claim.* For every message $m_0$, let $\gamma = \max_c \Pr_r[\mathrm{Enc}(pk, m_0; r) = c]$. Then there is an IND-CPA adversary with advantage at least $\gamma^2$.

*Proof.* The adversary outputs $m_0$ and any $m_1 \ne m_0$ of the same length, encrypts $m_0$ itself to get $c_0$, and outputs 0 if $c^* = c_0$ and 1 otherwise. If $b = 0$, then $c^*$ and $c_0$ are two independent encryptions of $m_0$, equal with probability $\sum_c \Pr[c]^2 \ge \gamma^2$. If $b = 1$, they are never equal, since $c^*$ decrypts to $m_1$. $\square$

So in an IND-CPA scheme $\gamma$ must be negligible: every message must have a superpolynomial number of likely ciphertexts. Since there are $2^\ell$ messages of length $\ell$ and their sets of ciphertexts are disjoint, a ciphertext must be at least $\ell + \log_2(1/\gamma) = \ell + \omega(\log \lambda)$ binary digits long. This is the *expansion* that every secure public-key scheme pays.

**Ways to add randomness.**

| method | example | expansion |
|---|---|---|
| encrypt each bit with a random element and a [hard-core predicate](/hard-core-predicate/) | [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) | each bit becomes an element of $\mathbb{Z}_n$, a factor $\log_2 n$ (HAC Note 8.53) |
| a random seed for a pseudorandom pad, sent through a [trapdoor permutation](/trapdoor-one-way-function/) | [Blum-Goldwasser](/blum-goldwasser-cryptosystem/) | one element of $\mathbb{Z}_n$ in total |
| a random exponent in a group | [ElGamal](/elgamal-encryption/) | a factor 2 |
| random padding before a trapdoor permutation | [RSA-OAEP](/rsa-oaep/), [PKCS #1 v1.5](/rsa-pkcs1-v1-5-encryption/) | a fixed number of bytes |
| a random key, then [hybrid encryption](/hybrid-encryption/) | ECIES, HPKE | one KEM ciphertext and a tag |

The general construction from any trapdoor permutation $f$ with hard-core predicate $B$ encrypts a bit $b$ as $(f(r), b \oplus B(r))$ for a random $r$. It is IND-CPA secure, and its proof is the model for the Goldwasser-Micali proof.

**Randomness must be fresh and secret.** If the random value repeats, or an attacker can predict it, the scheme loses its security, often completely: two ElGamal ciphertexts with the same $r$ reveal the ratio of their messages (HAC Note 8.23 (ii)).

## Examples

**A dictionary attack on textbook RSA.** Let $n = 3233 = 61 \cdot 53$ and $e = 17$, and suppose the message is 89 for "yes" or 78 for "no".

| message | $c = m^{17} \bmod 3233$ |
|---|---|
| 89 ("yes") | 99 |
| 78 ("no") | 3165 |

An attacker who sees $c = 99$ computes both encryptions with the public key and knows the answer. For the same key, $60^{17} \bmod 3233 = 1097$ and $63^{17} \bmod 3233 = 3216$: the Jacobi symbols modulo 3233 of 60 and 1097 are both $+1$, and those of 63 and 3216 are both $-1$, so the ciphertext shows one bit of every message.

**The same bit, two ciphertexts.** In [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) with $n = 77 = 7 \cdot 11$ and the non-square $y = 76$ of Jacobi symbol $+1$, the bit 1 is sent as $y r^2 \bmod 77$. With $r = 2$ it gives $76 \cdot 4 \bmod 77 = 73$; with $r = 3$ it gives $76 \cdot 9 \bmod 77 = 68$. The bit 0 with $r = 2$ gives $4$. All three values have Jacobi symbol $+1$, and without the factors of 77 nobody knows which of them are squares.

**ElGamal.** In the group of squares modulo 23 with $g = 4$ and the public key $h = 8$, the message 6 encrypts to $(12, 4)$ with $r = 5$ and to $(13, 8)$ with $r = 9$. The [ElGamal](/elgamal-encryption/) page has the full trace of the first ciphertext.

## Where it is used

- **Every IND-CPA and IND-CCA public-key scheme.** RSA is used only with random padding (OAEP), and Diffie-Hellman based encryption picks a fresh exponent each time. Post-quantum schemes such as [ML-KEM](/crystals-kyber/) add random noise.
- **Symmetric encryption.** Random or unique IVs and nonces play the same role in [CBC](/cbc-mode/), [CTR](/ctr-mode/) and [GCM](/gcm-mode/); the [semantic security](/semantic-security/) page shows why a stateless deterministic symmetric scheme fails too.
- **Rerandomization.** Schemes whose randomness can be refreshed by anyone, such as ElGamal, support mix networks and voting, where a ciphertext must be made unlinkable to its earlier form.
- **Deliberately deterministic schemes.** Searchable databases sometimes need equal plaintexts to give equal ciphertexts. Bellare, Boldyreva and O'Neill (2007) defined the best possible security for this case, for messages with high min-entropy; it cannot be IND-CPA.

**History.** Goldwasser and Micali presented probabilistic encryption at STOC 1982 (journal version 1984), with the quadratic residuosity scheme and the definitions of semantic security and polynomial indistinguishability. Their scheme expanded each bit to a full element of $\mathbb{Z}_n$. Blum and Goldwasser (1984) reduced the expansion to a constant number of elements with the Blum-Blum-Shub generator. ElGamal (1985) gave a randomized scheme based on discrete logarithms. Goldwasser and Micali received the Turing Award in 2012, partly for this work.

## References
