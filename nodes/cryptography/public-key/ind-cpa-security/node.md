---
tag: TJKQPG
kind: definition
slug: ind-cpa-security
name: IND-CPA security
aliases:
- indistinguishability under chosen-plaintext attack
area: cryptography/public-key
level: advanced
summary: A public-key scheme is IND-CPA secure if no efficient adversary that holds the public key can tell which of two chosen messages a challenge ciphertext encrypts.
prereqs: [public-key-encryption, semantic-security, hybrid-argument]
see_also: [ind-cca-security, probabilistic-encryption, non-malleability, elgamal-encryption, goldwasser-micali-cryptosystem, chosen-plaintext-attack, key-encapsulation-mechanism, computational-indistinguishability]
sources:
  - paper: doi:10.1016/0022-0000(84)90070-9
    title: Shafi Goldwasser and Silvio Micali, Probabilistic encryption, Journal of Computer and System Sciences 28(2), pages 270 to 299, 1984
    locator: the definitions of polynomial security and semantic security for public-key encryption
  - paper: "Silvio Micali, Charles Rackoff and Bob Sloan, The notion of security for probabilistic cryptosystems, SIAM Journal on Computing 17(2), pages 412 to 426, 1988"
    locator: the equivalence of the indistinguishability and semantic notions
  - paper: "Mihir Bellare, Anand Desai, Eron Jokipii and Phillip Rogaway, A concrete security treatment of symmetric encryption, FOCS 1997, pages 394 to 403"
    locator: the left-or-right and real-or-random notions and their relations
  - paper: "Mihir Bellare, Alexandra Boldyreva and Silvio Micali, Public-key encryption in a multi-user setting, security proofs and improvements, EUROCRYPT 2000, LNCS 1807, pages 259 to 274"
    locator: the hybrid bound for many users and many challenges, and the tight bound for ElGamal
  - paper: "Mihir Bellare, Anand Desai, David Pointcheval and Phillip Rogaway, Relations among notions of security for public-key encryption schemes, CRYPTO 1998, LNCS 1462, pages 26 to 45"
    locator: the definition of IND-CPA in the find-then-guess form and its place among the other notions
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 12, the security definitions for public-key encryption, the equivalence of one and many challenges
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 11, the definition of semantic security for public-key encryption
  - book: isbn:9780521830843
    title: Oded Goldreich, Foundations of Cryptography, Volume 2, Basic Applications, Cambridge University Press, 2004
    locator: Chapter 5, Section 5.2, definitions of security for encryption schemes
---

IND-CPA security, indistinguishability under chosen-plaintext attack, is the basic secrecy notion for [public-key encryption](/public-key-encryption/). An adversary that holds the public key picks two messages of the same length, gets an encryption of one of them, and must guess which one; the scheme is IND-CPA secure if no efficient adversary does much better than a coin flip. It is equivalent to [semantic security](/semantic-security/), it forces encryption to be [randomized](/probabilistic-encryption/), and it is the floor on which [IND-CCA security](/ind-cca-security/) builds. It does not protect against an attacker who can change ciphertexts and see them decrypted.

**Notation.** $\Pi = (\mathrm{Gen}, \mathrm{Enc}, \mathrm{Dec})$ is a public-key encryption scheme and $\lambda$ the security parameter. $\mathcal{A}$ is an adversary that runs in time $t$ and makes $q$ challenge queries (one in the basic game). $\mathrm{Adv}$ is an advantage of the form $|\Pr[b' = 1 \mid b = 1] - \Pr[b' = 1 \mid b = 0]|$, which equals $|2\Pr[b' = b] - 1|$ when $b$ is uniform. $|m|$ is the length of a message $m$. The definition makes no use of random oracles; a given scheme may be proved IND-CPA in the standard model or in the [random oracle model](/random-oracle-model/).

## Definition

**The game.** For a bit $b$, the experiment $\mathrm{IND\text{-}CPA}^b_\Pi(\mathcal{A})$ runs as follows.

1. $(pk, sk) \leftarrow \mathrm{Gen}(1^\lambda)$. The adversary gets $pk$.
2. $\mathcal{A}(pk)$ outputs two messages $m_0, m_1$ with $|m_0| = |m_1|$, and a state.
3. The challenger computes $c^* \leftarrow \mathrm{Enc}(pk, m_b)$ with fresh randomness and gives $c^*$ to $\mathcal{A}$.
4. $\mathcal{A}$ outputs a bit $b'$.

$$\mathrm{Adv}^{\mathrm{ind\text{-}cpa}}_\Pi(\mathcal{A}) = \bigl|\Pr[\mathrm{IND\text{-}CPA}^1_\Pi(\mathcal{A}) = 1] - \Pr[\mathrm{IND\text{-}CPA}^0_\Pi(\mathcal{A}) = 1]\bigr|.$$

$\Pi$ is **IND-CPA secure** if this advantage is a negligible function of $\lambda$ for every adversary that runs in time polynomial in $\lambda$. In concrete terms, $\Pi$ is $(t, \varepsilon)$-IND-CPA secure if every $\mathcal{A}$ that runs in time $t$ has advantage at most $\varepsilon$.

The game has no encryption oracle: the adversary holds $pk$ and encrypts what it wants by itself. This is the difference from the symmetric game on the [chosen-plaintext attack](/chosen-plaintext-attack/) page. The restriction $|m_0| = |m_1|$ is needed, because no scheme for messages of any length can hide the length.

**Left-or-right (LOR).** The adversary gets $pk$ and an oracle $\mathrm{LR}_b(m_0, m_1) = \mathrm{Enc}(pk, m_b)$, which it may call $q$ times on pairs of equal length, with the same hidden $b$ for all calls. $\mathrm{Adv}^{\mathrm{lor}}$ is defined as above.

**Real-or-random (ROR).** The oracle takes one message $m$ and returns $\mathrm{Enc}(pk, m)$ if $b = 1$, and $\mathrm{Enc}(pk, m')$ for a fresh uniform $m'$ with $|m'| = |m|$ if $b = 0$.

### One challenge implies many

**Theorem 1.** For every LOR adversary $\mathcal{A}$ that makes $q$ oracle calls, there is an IND-CPA adversary $\mathcal{B}$ with one challenge, running in the time of $\mathcal{A}$ plus $q$ encryptions, such that

$$\mathrm{Adv}^{\mathrm{lor}}_\Pi(\mathcal{A}) \le q \cdot \mathrm{Adv}^{\mathrm{ind\text{-}cpa}}_\Pi(\mathcal{B}).$$

*Proof.* This is a [hybrid argument](/hybrid-argument/). For $i = 0, \ldots, q$, let $H_i$ be the game in which the first $i$ oracle calls return an encryption of the right message $m_1$ and the others an encryption of the left message $m_0$. Let $P_i$ be the probability that $\mathcal{A}$ outputs 1 in $H_i$. Then $H_0$ is the LOR game with $b = 0$ and $H_q$ the game with $b = 1$, so $\mathrm{Adv}^{\mathrm{lor}}(\mathcal{A}) = |P_q - P_0|$.

$\mathcal{B}$ gets $pk$, picks $i$ uniform in $\{1, \ldots, q\}$ and runs $\mathcal{A}(pk)$. It answers call $j < i$ with $\mathrm{Enc}(pk, m_1^{(j)})$ and call $j > i$ with $\mathrm{Enc}(pk, m_0^{(j)})$, computed with the public key. On call $i$ it outputs the pair $(m_0^{(i)}, m_1^{(i)})$ as its own challenge and passes $c^*$ to $\mathcal{A}$. It outputs what $\mathcal{A}$ outputs. If the challenge bit is 1, $\mathcal{A}$ runs in $H_i$; if it is 0, in $H_{i-1}$. So

$$\Pr[\mathcal{B} = 1 \mid 1] - \Pr[\mathcal{B} = 1 \mid 0] = \frac{1}{q} \sum_{i=1}^{q} (P_i - P_{i-1}) = \frac{P_q - P_0}{q}. \qquad \square$$

The reduction loses a factor $q$. This loss is the price of generality: for [ElGamal](/elgamal-encryption/), the random self-reducibility of [DDH](/decisional-diffie-hellman/) gives a tight bound for many challenges and many users (Bellare, Boldyreva and Micali, 2000). The proof needs the public key, so that $\mathcal{B}$ can make the other encryptions; for symmetric schemes the same argument uses the encryption oracle.

### Left-or-right and real-or-random

**Theorem 2.** For every ROR adversary $\mathcal{A}$ there is a LOR adversary $\mathcal{B}$ with $\mathrm{Adv}^{\mathrm{ror}}(\mathcal{A}) \le \mathrm{Adv}^{\mathrm{lor}}(\mathcal{B})$. For every LOR adversary $\mathcal{A}$ there are ROR adversaries $\mathcal{B}_0, \mathcal{B}_1$ with $\mathrm{Adv}^{\mathrm{lor}}(\mathcal{A}) \le \mathrm{Adv}^{\mathrm{ror}}(\mathcal{B}_0) + \mathrm{Adv}^{\mathrm{ror}}(\mathcal{B}_1)$. All run in about the same time and make the same number of calls.

*Proof.* For the first claim, $\mathcal{B}$ answers each call $m$ of $\mathcal{A}$ by calling $\mathrm{LR}(m', m)$ with a fresh uniform $m'$ of length $|m|$. For the second, let $W_0$, $W_1$ and $W_{\mathrm{r}}$ be the games in which every call $(m_0, m_1)$ returns an encryption of $m_0$, of $m_1$, or of a fresh random message. $\mathcal{B}_c$ answers each call by asking its ROR oracle on $m_c$; it runs $\mathcal{A}$ in $W_c$ or in $W_{\mathrm{r}}$. The triangle inequality gives $|\Pr_{W_1} - \Pr_{W_0}| \le |\Pr_{W_1} - \Pr_{W_{\mathrm{r}}}| + |\Pr_{W_{\mathrm{r}}} - \Pr_{W_0}|$. $\square$

So LOR, ROR and the one-challenge game define the same notion up to a factor of at most $2q$.

### Deterministic encryption is not IND-CPA

**Theorem 3.** If $\mathrm{Enc}$ is deterministic and the message space has two distinct messages of the same length, then there is an IND-CPA adversary with advantage 1 that runs in the time of one encryption.

*Proof.* $\mathcal{A}$ outputs $m_0 \ne m_1$, receives $c^*$, computes $c_0 = \mathrm{Enc}(pk, m_0)$ itself, and outputs 0 if $c^* = c_0$ and 1 otherwise. If $b = 0$, then $c^* = c_0$. If $b = 1$, then $c^* = \mathrm{Enc}(pk, m_1) \ne c_0$, because decryption maps the two ciphertexts to different messages. $\square$

Unlike the symmetric case, the adversary needs no oracle. So textbook [RSA](/rsa-cryptosystem/) is not IND-CPA secure, and every IND-CPA scheme is [probabilistic](/probabilistic-encryption/).

### Relation to semantic security

IND-CPA security is equivalent to semantic security under chosen-plaintext attack (Goldwasser and Micali, 1984; Micali, Rackoff and Sloan, 1988). The proofs, for the symmetric case, are on the [semantic security](/semantic-security/) page and carry over to public-key schemes with the public key in place of the encryption oracle.

## Examples and non-examples

| scheme | IND-CPA? | assumption and model |
|---|---|---|
| [ElGamal](/elgamal-encryption/) in a prime order subgroup | yes | DDH, standard model, tight |
| ElGamal in all of $\mathbb{Z}_p^*$ | no | the Legendre symbol leaks one bit of the message |
| [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) | yes | quadratic residuosity, standard model |
| [Blum-Goldwasser](/blum-goldwasser-cryptosystem/) | yes | factoring Blum integers, standard model |
| [Paillier](/paillier-cryptosystem/) | yes | decisional composite residuosity, standard model |
| hashed ElGamal, $(g^r, m \oplus H(h^r))$ | yes | CDH, random oracle model |
| [Regev](/regev-encryption/) and the K-PKE inside [ML-KEM](/crystals-kyber/) | yes | (module) [learning with errors](/learning-with-errors/), standard model |
| textbook [RSA](/rsa-cryptosystem/), $m^e \bmod n$ | no | deterministic (Theorem 3) |
| [RSA-OAEP](/rsa-oaep/) | yes, and IND-CCA | RSA, random oracle model |

Two further non-examples show what the notion leaves out.

- **Malleable but IND-CPA.** ElGamal is IND-CPA, yet $(c_1, 2c_2)$ encrypts $2m$. IND-CPA says nothing about ciphertexts the adversary changes; see [non-malleability](/non-malleability/) and [chosen-ciphertext attacks](/chosen-ciphertext-attack/).
- **Key-dependent messages.** The game picks messages independent of $sk$. A scheme can be IND-CPA and still insecure when it encrypts its own private key; circular security is a separate notion.

## Related definitions

- **[Semantic security](/semantic-security/).** The simulation-based form; equivalent to IND-CPA.
- **[IND-CCA security](/ind-cca-security/).** IND-CPA plus a decryption oracle before (IND-CCA1) or before and after (IND-CCA2) the challenge.
- **[Non-malleability](/non-malleability/).** NM-CPA implies IND-CPA, and the converse fails.
- **IND-CPA for a [KEM](/key-encapsulation-mechanism/).** The challenge is a real or a random key with the encapsulation, and no messages are chosen.
- **Multi-user security.** $n$ public keys, each with challenges under one shared bit. A hybrid argument gives a loss of $nq$ in general; Bellare, Boldyreva and Micali (2000) defined it and gave tight bounds for some schemes.
- **Key privacy (IK-CPA).** The ciphertext also hides which public key was used (Bellare, Boldyreva, Desai and Pointcheval, 2001).
- **[Computational indistinguishability](/computational-indistinguishability/).** IND-CPA says that the ensembles $\{(pk, \mathrm{Enc}(pk, m_0))\}$ and $\{(pk, \mathrm{Enc}(pk, m_1))\}$ are computationally indistinguishable for every efficiently chosen pair of messages.

## References
