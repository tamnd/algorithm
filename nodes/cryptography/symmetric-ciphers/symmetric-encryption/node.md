---
tag: 9EBD8W
kind: problem
slug: symmetric-encryption
name: Symmetric-key encryption
aliases:
- secret-key encryption
- private-key encryption
area: cryptography/symmetric-ciphers
level: intro
summary: Two parties share one secret key. Encrypt messages so that anyone without the key learns nothing useful, and so that the key holder can decrypt them.
prereqs: []
see_also: [block-cipher, chosen-plaintext-attack, semantic-security, pseudorandom-function, one-time-pad, perfect-secrecy, ctr-mode, authenticated-encryption]
sources:
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 2 (perfect secrecy) and Chapter 3 (private-key encryption, CPA security and the construction from a pseudorandom function)
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 2 (ciphers and semantic security) and Chapter 5 (chosen plaintext attack)
  - paper: "Mihir Bellare, Anand Desai, Eron Jokipii and Phillip Rogaway, A concrete security treatment of symmetric encryption, Proceedings of the 38th IEEE Symposium on Foundations of Computer Science (FOCS), 1997"
    locator: the definitions of left-or-right and real-or-random security and the analysis of CTR and CBC modes
  - paper: doi:10.1002/j.1538-7305.1949.tb00928.x
    title: Claude E. Shannon, Communication theory of secrecy systems, Bell System Technical Journal 28(4), 1949
    locator: the definition of a secrecy system and perfect secrecy
---

Symmetric-key encryption is the problem of hiding messages between two parties who share one secret key: the same key encrypts and decrypts. A solution is an encryption scheme $(\mathsf{Gen}, \mathsf{Enc}, \mathsf{Dec})$ that is correct and meets a security goal; the default goal today is indistinguishability under a [chosen-plaintext attack](/chosen-plaintext-attack/) (IND-CPA). Most schemes in use are built from a [block cipher](/block-cipher/) such as AES in a mode of operation, or from a [stream cipher](/stream-cipher/).

## In plain words

Alice and Bob agree on a secret key in advance. Alice runs the key and her message through an encryption method and sends the result over an open channel. Bob runs the key and the result through the decryption method and gets the message back. An eavesdropper sees the result but not the key.

What does "secure" mean here? It is not enough that the eavesdropper cannot recover the whole message. The modern goal is stronger: the eavesdropper cannot even tell which of two messages of its own choice was sent, even when it can ask for encryptions of other messages. A method that always turns the same message into the same output fails this test, because the eavesdropper can compare outputs. So good methods use fresh randomness, or a counter, each time they encrypt.

## Definition

**Notation.** $\lambda$ is the security parameter, $k$ a key, $n$ the block length in bits where a block cipher is used, $\mathcal{A}$ an adversary, $q$ the number of its encryption queries and $t$ its running time.

**Syntax.** A symmetric encryption scheme over a message space $\mathcal{M}$ is a triple of algorithms that run in time polynomial in $\lambda$:

- $\mathsf{Gen}(1^\lambda)$ is randomized and outputs a key $k$. Often $k$ is a uniform string in $\{0,1\}^\lambda$.
- $\mathsf{Enc}_k(m)$ takes $m \in \mathcal{M}$ and outputs a ciphertext $c$. It may be randomized.
- $\mathsf{Dec}_k(c)$ is deterministic and outputs a message or the symbol $\bot$ for "invalid".

**Correctness.** For every $\lambda$, every key $k$ that $\mathsf{Gen}(1^\lambda)$ can output, and every $m \in \mathcal{M}$: $\Pr[\mathsf{Dec}_k(\mathsf{Enc}_k(m)) = m] = 1$, over the coins of $\mathsf{Enc}$.

**Security (IND-CPA).** In the game $\mathrm{IND\text{-}CPA}^b_\Pi(\mathcal{A})$ for $b \in \{0,1\}$, the challenger draws $k \leftarrow \mathsf{Gen}(1^\lambda)$. The adversary gets an oracle $\mathsf{Enc}_k(\cdot)$. At one point it outputs two messages $m_0, m_1$ of the same length and gets $c^* \leftarrow \mathsf{Enc}_k(m_b)$. It may make more oracle queries, then outputs a bit $b'$. Its advantage is

$$\mathrm{Adv}^{\mathrm{ind\text{-}cpa}}_\Pi(\mathcal{A}) = \bigl|\Pr[b' = 1 \mid b = 1] - \Pr[b' = 1 \mid b = 0]\bigr|.$$

$\Pi$ is IND-CPA secure if this advantage is negligible in $\lambda$ for each probabilistic polynomial-time $\mathcal{A}$. In the concrete view, one bounds the advantage as a function of $t$, $q$ and the total length of the queries. The page [chosen-plaintext attack](/chosen-plaintext-attack/) gives the game in full, and [semantic security](/semantic-security/) shows that IND-CPA is the same as "the ciphertext reveals nothing about the message beyond its length". All claims on this page are in the standard model.

## Variants

- **Perfect secrecy.** The adversary has unbounded time and sees one ciphertext. Shannon's [perfect secrecy](/perfect-secrecy/) asks that the ciphertext be independent of the message. The [one-time pad](/one-time-pad/) achieves it, but the key must be as long as all messages together.
- **One-time (EAV) security.** The game above with no oracle: the adversary sees one ciphertext only. A pseudorandom pad, $c = G(k) \oplus m$ for a [pseudorandom generator](/pseudorandom-generator/) $G$, meets it.
- **IND-CPA.** The default goal, defined above.
- **IND-CCA.** The adversary also gets a decryption oracle, which it may not call on $c^*$. See [IND-CCA security](/ind-cca-security/) and [chosen-ciphertext attack](/chosen-ciphertext-attack/).
- **Authenticated encryption.** IND-CPA plus integrity of ciphertexts (INT-CTXT). Together they imply IND-CCA. See [authenticated encryption](/authenticated-encryption/).
- **Stateful schemes.** $\mathsf{Enc}$ keeps a counter between calls. A stateful scheme can be IND-CPA and deterministic, because the counter never repeats.

## Examples

**The one-time pad, used twice.** With $\mathsf{Enc}_k(m) = k \oplus m$ and two messages under one key, $c_1 \oplus c_2 = m_1 \oplus m_2$. The adversary asks for the encryption of $m_0$, then sends the challenge $(m_0, m_1)$ and outputs $b' = 0$ if $c^*$ equals the answer. Its advantage is 1. The same attack breaks each deterministic stateless scheme; see [semantic security](/semantic-security/).

**A block cipher used directly (ECB).** $\mathsf{Enc}_k(m) = E_k(m)$ on one block is deterministic, so it fails IND-CPA in the same way. See [ECB mode](/ecb-mode/).

**Randomized counter encryption.** Let $F_k : \{0,1\}^n \to \{0,1\}^n$ be a [pseudorandom function](/pseudorandom-function/). For an $n$-bit message, $\mathsf{Enc}_k(m)$ draws a uniform $r \in \{0,1\}^n$ and outputs $(r, F_k(r) \oplus m)$; $\mathsf{Dec}_k(r, s) = F_k(r) \oplus s$. Correctness is immediate. For security, first replace $F_k$ by a truly random function $f$. Then $f(r^*)$ for the challenge value $r^*$ is uniform and independent of everything else, unless $r^*$ equals one of the at most $q$ values $r$ of the oracle answers. That event has probability at most $q/2^n$, and outside it $c^*$ carries no information on $b$. A distinguisher $\mathcal{B}$ for $F$ runs $\mathcal{A}$ and outputs 1 when $\mathcal{A}$ wins. So, with $\mathrm{Adv} = 2\Pr[b' = b] - 1$,

$$\mathrm{Adv}^{\mathrm{ind\text{-}cpa}}(\mathcal{A}) \le 2\,\mathrm{Adv}^{\mathrm{prf}}_F(\mathcal{B}) + \frac{2q}{2^n},$$

where $\mathcal{B}$ makes $q + 1$ queries and runs in about the time of $\mathcal{A}$. The reduction is tight up to the factor 2. With $n = 128$ and $q = 2^{32}$ queries, the second term is $2^{-95}$. CTR mode is the multi-block form of this scheme; see [CTR mode](/ctr-mode/).

## Known algorithms

- **AES in a mode of operation.** The [Advanced Encryption Standard](/advanced-encryption-standard/) with [CTR mode](/ctr-mode/), [CBC mode](/cbc-mode/) or [GCM](/gcm-mode/) is the common choice. GCM adds integrity.
- **ChaCha20.** A stream cipher, used with Poly1305 for integrity. See [ChaCha20](/chacha20/).
- **Legacy ciphers.** [DES](/data-encryption-standard/) is broken by key search. [Triple DES](/triple-des/) is disallowed for new encryption by NIST after 2023.

## Bounds

- **Key length for perfect secrecy.** A perfectly secret scheme needs at least as many keys as messages (Shannon 1949). See [Shannon's perfect secrecy theorem](/shannon-perfect-secrecy-theorem/).
- **Key search.** Each scheme with $k$-bit keys falls to [exhaustive key search](/exhaustive-key-search/) in at most $2^k$ trial decryptions, given a few known plaintexts. So the key must be long enough that $2^k$ operations are out of reach.
- **Randomness or state.** A stateless deterministic scheme is never IND-CPA secure, by the attack in Examples.
- **Birthday bounds.** Modes built on an $n$-bit block cipher lose security after about $2^{n/2}$ blocks under one key. For $n = 64$ this is the Sweet32 attack on [Triple DES](/triple-des/).

## Reductions

- A [pseudorandom function](/pseudorandom-function/) gives an IND-CPA scheme, by the construction above.
- A [pseudorandom permutation](/pseudorandom-permutation/), which is what a [block cipher](/block-cipher/) aims to be, is also a PRF up to the term $q(q-1)/2^{n+1}$ of the [PRP/PRF switching lemma](/prp-prf-switching-lemma/).
- A [pseudorandom generator](/pseudorandom-generator/) gives a PRF by the GGM tree construction, and a [one-way function](/one-way-function/) gives a pseudorandom generator. So IND-CPA encryption exists if one-way functions exist. The converse also holds: secure private-key encryption implies one-way functions (Katz and Lindell, Chapter 8).

## Applications

- The record layer of TLS 1.3 encrypts with AES-GCM or ChaCha20-Poly1305 under keys from a key exchange.
- Disk and file encryption, for example AES in [XTS mode](/xts-mode/).
- Hybrid encryption: a public-key method sends a fresh symmetric key, and the symmetric scheme encrypts the data.
- [Message authentication codes](/message-authentication-code/) are the integrity partner of encryption and use the same primitives.

## References
