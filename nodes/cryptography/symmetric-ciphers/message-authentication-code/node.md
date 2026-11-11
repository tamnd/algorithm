---
tag: K22DFM
kind: definition
slug: message-authentication-code
name: Message authentication code
aliases:
- MAC
area: cryptography/symmetric-ciphers
level: core
summary: A keyed scheme whose tags nobody without the key can forge for a new message, even after a chosen message attack. A PRF with t-bit output is one, with an extra loss of 2^-t.
prereqs: [message-authentication, pseudorandom-function]
see_also: [hmac, cbc-mac, cmac, poly1305, existential-unforgeability, strong-unforgeability, timing-attack, universal-hashing]
sources:
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 4, Sections 4.2 and 4.3 (the definition of a secure and a strongly secure MAC, and the fixed-length MAC from a pseudorandom function)
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 6, Sections 6.1 to 6.3 (MAC security, verification queries and PRFs as MACs) and Chapter 7 (Carter and Wegman MACs)
  - paper: "Mihir Bellare, Joe Kilian and Phillip Rogaway, The security of the cipher block chaining message authentication code, Journal of Computer and System Sciences 61(3), 2000, pages 362 to 399"
    locator: Section 2 (the concrete security definition of a MAC with a tagging oracle) and the result that a PRF is a secure MAC
  - paper: "Mihir Bellare, Oded Goldreich and Anton Mityagin, The power of verification queries in message authentication and authenticated encryption, Cryptology ePrint Archive, Report 2004/309"
    locator: the result that verification queries do not help against strong unforgeability, and the example where they help against the weak notion
  - paper: "Mark N. Wegman and J. Lawrence Carter, New hash functions and their use in authentication and set equality, Journal of Computer and System Sciences 22(3), 1981, pages 265 to 279"
    locator: Section 3 (authentication with a strongly universal hash family and a one-time pad on the tag)
---

A message authentication code (MAC) is a triple of algorithms $(\mathsf{Gen}, \mathsf{Mac}, \mathsf{Vrfy})$ with a shared secret key. The sender computes a short tag $T = \mathsf{Mac}_K(M)$ and sends it with $M$; the receiver accepts if $\mathsf{Vrfy}_K(M, T)$ says so. The scheme is secure if no efficient adversary, after it has seen tags of messages of its choice, can produce a valid tag for any new message. This is existential unforgeability under chosen message attack (EUF-CMA). [HMAC](/hmac/), [CMAC](/cmac/) and the tags of [GCM](/gcm-mode/) and [Poly1305](/poly1305/) are MACs. A MAC is the symmetric solution of [message authentication](/message-authentication/).

## Definition

**Notation.** $K$ is the key, $M$ a message, $T$ a tag of $t$ bits, $\mathcal{A}$ the adversary, $q$ the number of tagging queries and $q_v$ the number of verification queries.

**Syntax.** A MAC is a triple of efficient algorithms.

1. $\mathsf{Gen}$ outputs a key $K$, usually uniform in $\{0,1\}^k$.
2. $\mathsf{Mac}_K(M)$ outputs a tag $T \in \{0,1\}^t$. It may be randomized or use a nonce, but most MACs in use are deterministic.
3. $\mathsf{Vrfy}_K(M, T)$ outputs accept or reject.

**Correctness.** $\mathsf{Vrfy}_K(M, \mathsf{Mac}_K(M))$ accepts for every key and message. For a deterministic MAC the canonical verification computes $T' = \mathsf{Mac}_K(M)$ and accepts if and only if $T' = T$.

**The EUF-CMA game.** The key $K$ is drawn by $\mathsf{Gen}$. The adversary $\mathcal{A}$ gets a tagging oracle $M \mapsto \mathsf{Mac}_K(M)$ and a verification oracle $(M, T) \mapsto \mathsf{Vrfy}_K(M, T)$. Let $Q$ be the set of messages that $\mathcal{A}$ sent to the tagging oracle. $\mathcal{A}$ wins if some verification query, or its final output, is a pair $(M^*, T^*)$ that is accepted with $M^* \notin Q$. Its advantage $\mathrm{Adv}^{\mathrm{euf\text{-}cma}}_{\Pi}(\mathcal{A})$ is the probability that it wins. The MAC is secure if this advantage is negligible for every efficient $\mathcal{A}$; in concrete terms, it is $(\tau, q, q_v, \varepsilon)$-secure if every $\mathcal{A}$ that runs in time $\tau$ with $q$ and $q_v$ queries has advantage at most $\varepsilon$.

**The SUF-CMA game.** The same, except that $\mathcal{A}$ wins with any accepted pair $(M^*, T^*)$ that the tagging oracle never returned. So a second valid tag for a message in $Q$ is also a forgery. Strong unforgeability (SUF-CMA) is what [authenticated encryption](/authenticated-encryption/) needs for ciphertext integrity. A deterministic MAC with canonical verification has exactly one valid tag per message, so for it the two notions are the same.

**What the game does not cover.** A replay of a pair from the tagging oracle is not a forgery. Confidentiality is not asked for: a secure MAC may put the whole message in the tag.

### A pseudorandom function is a secure MAC

Let $F: \{0,1\}^k \times \mathcal{M} \to \{0,1\}^t$ be a [pseudorandom function](/pseudorandom-function/) and define $\mathsf{Mac}_K(M) = F_K(M)$ with canonical verification.

**Theorem.** For every adversary $\mathcal{A}$ that makes $q$ tagging queries and outputs one candidate forgery (no verification queries), there is a PRF adversary $\mathcal{B}$ that makes $q + 1$ queries and runs in about the time of $\mathcal{A}$, with
$$\mathrm{Adv}^{\mathrm{euf\text{-}cma}}_{\Pi}(\mathcal{A}) \le \mathrm{Adv}^{\mathrm{prf}}_F(\mathcal{B}) + 2^{-t}.$$

**Proof.** $\mathcal{B}$ has an oracle $\mathcal{O}$, which is either $F_K$ for a random $K$ or a uniformly random function $f: \mathcal{M} \to \{0,1\}^t$. $\mathcal{B}$ runs $\mathcal{A}$ and answers each tagging query $M$ with $\mathcal{O}(M)$, and it records the set $Q$. When $\mathcal{A}$ outputs $(M^*, T^*)$, $\mathcal{B}$ outputs 0 if $M^* \in Q$. Otherwise it queries $\mathcal{O}(M^*)$ and outputs 1 if the answer equals $T^*$, and 0 if not.

If $\mathcal{O} = F_K$, then $\mathcal{A}$ sees exactly the EUF-CMA game, and $\mathcal{B}$ outputs 1 exactly when $\mathcal{A}$ wins. So $\Pr[\mathcal{B}^{F_K} = 1] = \mathrm{Adv}^{\mathrm{euf\text{-}cma}}_{\Pi}(\mathcal{A})$.

If $\mathcal{O} = f$, then the view of $\mathcal{A}$ depends only on the values $f(M)$ for $M \in Q$. If $M^* \notin Q$, the value $f(M^*)$ is uniform in $\{0,1\}^t$ and independent of that view, so it is independent of $T^*$, and it equals $T^*$ with probability exactly $2^{-t}$. So $\Pr[\mathcal{B}^{f} = 1] \le 2^{-t}$.

By the definition of PRF advantage, $\mathrm{Adv}^{\mathrm{prf}}_F(\mathcal{B}) = \Pr[\mathcal{B}^{F_K} = 1] - \Pr[\mathcal{B}^{f} = 1] \ge \mathrm{Adv}^{\mathrm{euf\text{-}cma}}_{\Pi}(\mathcal{A}) - 2^{-t}$, which is the claim. $\blacksquare$

**With verification queries.** Let $\mathcal{B}$ answer a verification query $(M, T)$ by comparing $\mathcal{O}(M)$ with $T$. With $\mathcal{O} = f$, change the game so that every verification query on a message not in $Q$ at that time is rejected. The two games are the same until the first such query with $f(M) = T$. In the changed game the view never depends on $f(M)$ for a message outside $Q$, so each such query, and the final output, has $f(M) = T$ with probability exactly $2^{-t}$. A union bound over the $q_v$ queries and the final output gives $\mathrm{Adv}^{\mathrm{euf\text{-}cma}}_{\Pi}(\mathcal{A}) \le \mathrm{Adv}^{\mathrm{prf}}_F(\mathcal{B}) + (q_v + 1) 2^{-t}$, with $q + q_v + 1$ queries for $\mathcal{B}$.

**Tightness.** The reduction is tight: $\mathcal{B}$ has the running time of $\mathcal{A}$ plus the bookkeeping, one more query, and the full advantage of $\mathcal{A}$ minus a term that no MAC with $t$-bit tags can avoid, as the guessing bound on the [message authentication](/message-authentication/) page shows. So a PRF with 128-bit output, such as AES restricted to one block, gives a MAC for one-block messages with security that is limited only by the PRF and by $2^{-128}$ per try. For longer messages the PRF must have a variable input length: [CMAC](/cmac/) and [HMAC](/hmac/) are such PRFs, and plain [CBC-MAC](/cbc-mac/) is a PRF only for messages of one fixed length.

### Wegman and Carter: a universal hash with a one-time pad

A family of hash functions $\{h\}$ from $\mathcal{M}$ to $\{0,1\}^t$ is $\varepsilon$-almost-XOR-universal ($\varepsilon$-AXU) if for all $M \ne M'$ and every $\Delta$, $\Pr_h[h(M) \oplus h(M') = \Delta] \le \varepsilon$. Wegman and Carter (1981) authenticated a message with $T = h(M) \oplus P$, where $h$ is secret and $P$ is a fresh one-time pad for each message.

**Claim.** After seeing one pair $(M, T)$, an adversary of unbounded power outputs a valid $(M', T')$ with $M' \ne M$ with probability at most $\varepsilon$.

**Proof.** Since $P$ is uniform and independent of $h$, the observed tag $T$ is uniform and independent of $h$, so it tells nothing about $h$. The forgery is valid when $h(M') \oplus P = T'$, that is, when $h(M') \oplus h(M) = T' \oplus T$, because $P = T \oplus h(M)$. The values $M'$, $T'$ and $T$ are fixed by the adversary's view, which is independent of $h$, so by the AXU property this happens with probability at most $\varepsilon$. $\blacksquare$

Practical schemes replace the pad by a PRF of a nonce: $T = h_{K_1}(M) \oplus F_{K_2}(N)$. GHASH in [GCM](/gcm-mode/) is this with an XOR, and [Poly1305](/poly1305/) uses addition modulo $2^{128}$ instead, with an almost-$\Delta$-universal hash. The universal hash is fast, but the security falls apart if a pad or a nonce is used twice.

### Comparing tags

The receiver must compare $T'$ and $T$ in constant time. A comparison that stops at the first byte that differs has a running time that grows with the length of the correct prefix. An attacker who can measure that time finds the tag one byte at a time, with at most 256 tries per byte, so with about $256 \cdot t/8$ tries instead of $2^t$. Compare all bytes and fold the differences with OR, as `hmac.compare_digest` in Python and `crypto_verify_16` in libsodium do. See [timing attack](/timing-attack/).

## Examples and non-examples

- **Example: [HMAC](/hmac/) with SHA-256.** A PRF for any length under an assumption on the compression function, so a secure deterministic MAC. It is the default in protocols.
- **Example: [CMAC](/cmac/) with AES.** A PRF for any length if AES is a PRP, with a birthday-type loss of about $\sigma^2/2^{128}$ for $\sigma$ blocks in total.
- **Example: $F_K(M)$ with AES for 16-byte messages.** The theorem above applies directly.
- **Non-example: [CBC-MAC](/cbc-mac/) for messages of any length.** From the tags $t_1$ of $m_1$ and $t_2$ of $m_2$ (one block each), the message $m_1 \,\|\, (m_2 \oplus t_1)$ has tag $t_2$. It is secure only for one fixed length.
- **Non-example: $H(K \,\|\, M)$ with SHA-256.** Merkle and Damgard hashing allows a length extension: from the tag of $M$ one computes the tag of $M \,\|\, \mathrm{pad} \,\|\, X$ without $K$. See [length extension attack](/length-extension-attack/).
- **Non-example: Poly1305 with one key for two messages.** It is a one-time MAC: two tags under one key reveal the key, as the [Poly1305](/poly1305/) page shows.
- **Non-example: a 32-bit tag against $2^{20}$ online tries.** The guessing bound gives a forgery with probability about $2^{-12}$, which is too high for most uses, although the MAC itself is unbroken.

| tag bits $t$ | verification tries $q_v$ | forgery bound $q_v 2^{-t}$ |
|---|---|---|
| 32 | $2^{20}$ | $2^{-12}$ |
| 64 | $2^{40}$ | $2^{-24}$ |
| 96 | $2^{40}$ | $2^{-56}$ |
| 128 | $2^{64}$ | $2^{-64}$ |

## Related definitions

- **[Existential unforgeability](/existential-unforgeability/) and [strong unforgeability](/strong-unforgeability/)** are the same games for digital signatures, where the adversary also has the public key.
- **[Pseudorandom function](/pseudorandom-function/).** A stronger notion: every PRF with long enough output is a MAC, but a MAC need not be a PRF, because its tags may be far from random.
- **Weak unforgeability.** Bellare, Goldreich and Mityagin (2004) show that for strong unforgeability, verification queries add at most a factor $q_v$ to the advantage, but that for the weak notion there are MACs that are secure without verification queries and broken with them. So state the game with the verification oracle, as above.
- **One-time MAC.** Secure for a single message per key, such as a Wegman and Carter MAC with a one-time pad or Poly1305 with a fresh key.
- **[Authenticated encryption](/authenticated-encryption/).** Confidentiality and integrity of ciphertexts together; a MAC on the ciphertext with an independent key is one way to build it.

## References
