---
tag: ECDFJQ
kind: definition
slug: stream-cipher
name: Stream cipher
aliases:
- keystream generator
area: cryptography/symmetric-ciphers
level: intro
summary: A symmetric cipher that XORs the message with a keystream made from a key (and a nonce). It is secure if the keystream is pseudorandom, and fails if a key and nonce pair repeats.
prereqs: [one-time-pad, pseudorandom-generator]
see_also: [chacha20, rc4, trivium, lfsr, ctr-mode, pseudorandom-function, semantic-security, authenticated-encryption]
sources:
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 3 (pseudorandom generators, the encryption scheme from a pseudorandom generator and its proof of security, stream ciphers and their synchronized and unsynchronized modes)
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 3 (stream ciphers, pseudorandom generators, the two-time pad and malleability)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 6 (stream ciphers), Section 6.1 (synchronous and self-synchronizing stream ciphers)
  - paper: "Steve Babbage, Christophe De Canniere, Anne Canteaut, Carlos Cid, Henri Gilbert, Thomas Johansson, Matthew Parker, Bart Preneel, Vincent Rijmen and Matthew Robshaw, The eSTREAM portfolio, ECRYPT, April 2008, revised September 2008"
    locator: the profile 1 (software) and profile 2 (hardware) portfolios, and the removal of F-FCSR-H v2 in the revision
---

A stream cipher is a [symmetric encryption](/symmetric-encryption/) scheme that makes a long pseudorandom keystream from a short key, and usually a [nonce](/nonce/), and XORs the keystream with the message. It imitates the [one-time pad](/one-time-pad/) with a short key, so it is secure only in the computational sense: the keystream must look random to each efficient adversary. If one key and nonce pair is used twice, the cipher fails at once.

## Definition

We write $\lambda$ for the security parameter, $K$ for the key, $N$ for the nonce, $A$ for an adversary, $t$ for its running time, $q$ for its number of queries and $\mathrm{Adv}$ for its advantage.

**Synchronous stream cipher.** A *keystream generator* is a deterministic, efficiently computable function
$$G : \mathcal{K} \times \mathcal{N} \to \{0,1\}^{L},$$
where $\mathcal{K} = \{0,1\}^{\lambda}$ is the key space, $\mathcal{N}$ the nonce space (it may have one element) and $L$ the maximum message length. The stream cipher built on $G$ encrypts a message $M$ with $|M| \le L$ as
$$\mathrm{Enc}(K, N, M) = M \oplus G(K, N)[0 \ldots |M|-1], \qquad \mathrm{Dec}(K, N, C) = C \oplus G(K, N)[0 \ldots |C|-1].$$
The keystream does not depend on the message or the ciphertext. Sender and receiver must stay in step: a lost or inserted ciphertext bit shifts all later keystream bits.

**Self-synchronizing stream cipher.** Each keystream symbol depends on the key and on the previous $s$ ciphertext symbols: $z_i = f(K, c_{i-1}, \ldots, c_{i-s})$ and $c_i = m_i \oplus z_i$. After a lost, inserted or changed symbol, the receiver is in step again after $s$ correct symbols. The CFB mode of a [block cipher](/block-cipher/) is the standard example.

**Security as a PRG.** Without a nonce, $G(K)$ for a uniform $K$ should be a [pseudorandom generator](/pseudorandom-generator/) output:
$$\mathrm{Adv}^{\mathrm{prg}}_G(A) = \bigl|\Pr[A(G(K)) = 1] - \Pr[A(U_L) = 1]\bigr|$$
is small for each $A$ that runs in time $t$, where $U_L$ is uniform on $\{0,1\}^L$. Then one message per key is secure: for each $A$ in the indistinguishability game with one challenge (the one-time version of [IND-CPA](/semantic-security/), with no encryption queries), there is $B$ with about the same running time such that $\mathrm{Adv}(A) \le 2\,\mathrm{Adv}^{\mathrm{prg}}_G(B)$. *Proof.* $B$ gets a string $y$, runs $A$ to get $M_0, M_1$, picks a uniform bit $b$, gives $M_b \oplus y$ to $A$, and outputs 1 when $A$ guesses $b$. If $y = G(K)$, $B$ simulates the real game. If $y$ is uniform, $M_b \oplus y$ is a one-time pad, so $A$ guesses $b$ with probability exactly $1/2$. So $|\Pr[A \text{ wins}] - 1/2| \le \mathrm{Adv}^{\mathrm{prg}}_G(B)$, and the advantage $2|\Pr[A \text{ wins}] - 1/2|$ is at most $2\,\mathrm{Adv}^{\mathrm{prg}}_G(B)$. $\square$

**Security as a PRF on the nonce.** With a nonce, $N \mapsto G(K, N)$ should be a [pseudorandom function](/pseudorandom-function/) with outputs of $L$ bits. Then the cipher is IND-CPA secure against adversaries that never repeat a nonce: the advantage is at most $2\,\mathrm{Adv}^{\mathrm{prf}}_G(B)$ for $B$ with about the same time and $q + 1$ queries. The proof replaces $G(K, \cdot)$ by a random function; the nonces differ, so each message gets a fresh one-time pad. This is the model of [ChaCha20](/chacha20/), [Salsa20](/salsa20/), [Trivium](/trivium/) and [CTR mode](/ctr-mode/). The proofs are in the standard model, and the reductions are tight up to the factor 2.

## Examples and non-examples

**The two-time pad (a broken use).** Take the keystream bytes 3a 91 5c 07 and encrypt both "SEND" (53 45 4e 44) and "STOP" (53 54 4f 50) with it. The ciphertexts are 69 d4 12 43 and 69 c5 13 57. Their XOR is 00 11 01 14, which is the XOR of the two plaintexts: the key has gone. Natural language has so much redundancy that crib dragging (trying likely words at each position) recovers both texts, and a known first message gives the second at once. The same holds for each cipher on this page when a key and nonce pair repeats; the tests of the [RC4](/rc4/) and [ChaCha20](/chacha20/) pages show it in code.

**Malleability (a property, not a bug in one cipher).** Flipping bit $j$ of $c_i$ flips bit $j$ of $m_i$ and nothing else. The message "PAY 100" has the byte 31 for the digit 1. XOR the matching ciphertext byte with $31 \oplus 39 = 08$ and the receiver decrypts "PAY 900". A stream cipher gives confidentiality only. For integrity use [authenticated encryption](/authenticated-encryption/), such as [ChaCha20-Poly1305](/chacha20-poly1305/).

**Examples.**
- [RC4](/rc4/): a synchronous cipher with a key and no nonce. It is broken.
- [ChaCha20](/chacha20/) and [Salsa20](/salsa20/): synchronous ciphers built from a PRF on (nonce, counter).
- [Trivium](/trivium/) and [Grain](/grain/): bit-oriented hardware ciphers built from shift registers, in the eSTREAM profile 2.
- [A5/1](/a5-1/), [SNOW 3G](/snow-3g/) and [ZUC](/zuc/): the ciphers of GSM, UMTS and LTE, with the frame or bearer number as the nonce.
- [CTR mode](/ctr-mode/) and [OFB mode](/ofb-mode/) turn a block cipher into a synchronous stream cipher; [CFB mode](/cfb-mode/) gives a self-synchronizing one.

**Non-examples.**
- The [one-time pad](/one-time-pad/) has a truly random key as long as the message. It has [perfect secrecy](/perfect-secrecy/), and a stream cipher does not, because its key is shorter than the message.
- A bare [LFSR](/lfsr/) or a statistical generator such as a [linear congruential generator](/linear-congruential-generator/) is not a stream cipher in this sense. Its output passes many statistical tests, but it is linear or nearly so, and a short piece of output reveals the rest.
- ECB mode of a block cipher encrypts each block separately with no keystream. It is a mode of a block cipher, and it is not even IND-CPA secure.

**The eSTREAM portfolio.** The ECRYPT eSTREAM project (2004 to 2008) chose a portfolio in April 2008. Profile 1 (software): HC-128, Rabbit, Salsa20/12 and SOSEMANUK. Profile 2 (hardware): F-FCSR-H v2, Grain v1, MICKEY v2 and Trivium. The September 2008 revision removed F-FCSR-H v2 after a published attack on it.

## Related definitions

- **[Pseudorandom generator](/pseudorandom-generator/).** A stream cipher without a nonce is a PRG with a long output. The PRG must be secure against efficient adversaries, not only pass statistical tests.
- **[Pseudorandom function](/pseudorandom-function/).** A nonce-based stream cipher is a PRF from nonces to keystreams. A [block cipher](/block-cipher/) in CTR mode is one such PRF, up to the PRP to PRF switching bound.
- **[Nonce](/nonce/) and [initialization vector](/initialization-vector/).** The nonce must be unique for a key; it need not be secret or random.
- **[Semantic security](/semantic-security/).** The target notion. A stream cipher alone meets it only for nonce-respecting use.
- **[Authenticated encryption](/authenticated-encryption/).** A stream cipher with a MAC, or a design such as [Ascon](/ascon/) or Grain-128AEAD, adds integrity.
- **[Linear feedback shift register](/lfsr/).** The classic building block of hardware stream ciphers, always combined with a nonlinear part.

## References
