---
tag: Y0FP71
kind: problem
slug: message-authentication
name: Message authentication
aliases:
- message integrity
- data authentication
area: cryptography/symmetric-ciphers
level: core
summary: Let a receiver check that a message comes from the claimed sender and was not changed. A MAC solves it with a shared key, a signature with a public key. Neither stops replay.
prereqs: []
see_also: [message-authentication-code, digital-signature, hmac, authenticated-encryption, cyclic-redundancy-check, challenge-response-authentication, non-repudiation, universal-hashing]
sources:
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 4 (message authentication codes, the goals of integrity and authenticity, and replay attacks)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 9, Section 9.6 (data integrity and message authentication) and Section 9.7 (data integrity using MACs and encryption)
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 6 (message integrity)
  - paper: "Edgar N. Gilbert, F. Jessie MacWilliams and Neil J. A. Sloane, Codes which detect deception, Bell System Technical Journal 53(3), 1974, pages 405 to 424"
    locator: the first study of authentication codes with unconditional security
  - paper: "Mark N. Wegman and J. Lawrence Carter, New hash functions and their use in authentication and set equality, Journal of Computer and System Sciences 22(3), 1981, pages 265 to 279"
    locator: authentication with a universal hash family and a one-time pad on the tag
---

Message authentication is the problem of letting a receiver check two things about a message: that it was not changed on the way (integrity), and that it comes from the party it claims to come from (data origin authenticity). The adversary controls the channel: it can read, drop, change, insert and repeat messages. With a shared secret key the solution is a [message authentication code](/message-authentication-code/) (MAC); with a public key it is a [digital signature](/digital-signature/). Encryption alone does not solve the problem, and a checksum such as a CRC does not either. A MAC also does not stop an old valid message from being sent again: that needs a sequence number, a timestamp or a challenge.

## In plain words

Alice sends Bob a message over a network that an attacker controls. Bob wants to be sure that Alice wrote it and that nobody changed it. Alice and Bob share a secret key. Alice computes a short value, the tag, from the key and the message, and sends it with the message. Bob computes the tag again with his copy of the key and compares. Without the key, the attacker cannot make a correct tag for any new message, even after it has seen many messages with their tags.

The tag proves only that someone with the key made this exact message at some time. If the attacker sends an old message with its old tag again, the tag is still correct. So a protocol must also number its messages or check that they are fresh.

## Definition

**Notation.** $\mathcal{K}$ is the key space, $\mathcal{M}$ the message space, $\mathcal{T}$ the tag space with tags of $t$ bits, and $\mathcal{A}$ the adversary.

**Symmetric setting.** A solution is a MAC $\Pi = (\mathsf{Gen}, \mathsf{Mac}, \mathsf{Vrfy})$: $\mathsf{Gen}$ outputs a key $K$; $\mathsf{Mac}_K(M)$ outputs a tag $T$; $\mathsf{Vrfy}_K(M, T)$ outputs accept or reject. Correctness: $\mathsf{Vrfy}_K(M, \mathsf{Mac}_K(M))$ accepts for every $K$ and $M$.

**Security goal.** Existential unforgeability under chosen message attack (EUF-CMA): $\mathcal{A}$ may ask for tags of messages of its choice and may ask whether pairs verify; it wins if it outputs a pair $(M^*, T^*)$ that verifies, where $M^*$ was never asked to the tagging oracle. The scheme is secure if every efficient $\mathcal{A}$ wins with small probability. The [message authentication code](/message-authentication-code/) page gives the exact game, the strong variant and the proofs.

**What is not required.** Confidentiality: the message may be public. Freshness: a replay of $(M, T)$ is not a forgery, because $M$ was tagged before.

**Asymmetric setting.** The signer holds a private key and everyone holds the public key. The goal is the same unforgeability, but anyone can verify. See [digital signature](/digital-signature/) and [existential unforgeability](/existential-unforgeability/).

## Variants

- **MAC versus signature.** A MAC is fast (one block cipher call or one hash compression per block) and its tags are short, but every verifier can also create tags, so a MAC cannot convince a third party who made a message. A signature can, which gives [non-repudiation](/non-repudiation/), at a cost of public key operations.
- **Unconditional (information-theoretic) authentication.** Authentication codes, studied first by Gilbert, MacWilliams and Sloane (1974), resist unbounded adversaries but need fresh key for each message. Wegman and Carter (1981) built them from [universal hashing](/universal-hashing/) and a one-time pad on the tag.
- **One-time versus many-time.** A one-time MAC, such as [Poly1305](/poly1305/) with a fresh key, is secure for one message per key. A many-time MAC, such as [HMAC](/hmac/) or [CMAC](/cmac/), is secure for many.
- **Authentication with secrecy.** [Authenticated encryption](/authenticated-encryption/) gives both at once, and its integrity covers the ciphertext.
- **Replay and order protection.** A protocol layer on top of a MAC: include a sequence number in the tagged data and reject numbers already seen (TLS, IPsec with its anti-replay window), or a timestamp within a window, or a fresh [challenge](/challenge-response-authentication/).

## Examples

Key `000102030405060708090a0b0c0d0e0f`, HMAC-SHA-256 truncated to 128 bits, and CRC-32 for comparison (values checked by script).

| message | HMAC tag (first 16 bytes) | CRC-32 |
|---|---|---|
| `pay 10 EUR to bob, ref 0001` | `13c2d14f81282e52fdaeac801dde3347` | `7430765a` |
| `pay 90 EUR to bob, ref 0001` | `51041ae3150b3db87ab83111be55ba51` | `7489357c` |

**A checksum is not a MAC.** Anyone can compute a CRC, so an attacker who changes `10` to `90` simply recomputes it. Hiding the initial value of the CRC does not help, because CRC is affine over $\mathrm{GF}(2)$: for messages $a$ and $b$ of equal length, $\mathrm{CRC}(a) \oplus \mathrm{CRC}(b) = \mathrm{CRC}(a \oplus b) \oplus \mathrm{CRC}(0^{|a|})$, and the right side does not depend on the initial value. In the example both sides equal `00b94326`, so the change of the checksum is known from the change of the message alone. (A CRC with a secret random polynomial and an encrypted result is a different thing: Krawczyk showed in 1994 that it is a secure universal hash MAC.) See [cyclic redundancy check](/cyclic-redundancy-check/).

**A replay is not detected by the MAC.** If Bob accepts the first row once, he will accept it again when the attacker resends it, and pay twice. The fix is in the data: the reference `0001` must be a sequence number that Bob refuses to see twice.

**Encryption is not authentication.** With a stream mode such as [CTR](/ctr-mode/), flipping ciphertext bits flips the same plaintext bits, so `10` becomes `90` by XOR of the ciphertext with `10 xor 90`, with no key.

## Known algorithms

- **[HMAC](/hmac/)** with SHA-2 or SHA-3. The default MAC in protocols.
- **[CBC-MAC](/cbc-mac/)** (secure only for messages of one fixed length) and **[CMAC](/cmac/)** (secure for any length), from a block cipher.
- **[Poly1305](/poly1305/)** and GHASH in **[GCM](/gcm-mode/)**: universal hash functions with a one-time mask, in the Wegman and Carter style.
- **[KMAC](/kmac/)** from Keccak, and **[SipHash](/siphash/)**, a short-input PRF for hash tables.
- **Signatures:** [Ed25519](/ed25519/), [ECDSA](/ecdsa/), [RSA-PSS](/rsa-pss/) for the asymmetric setting.

## Bounds

**Claim (guessing).** For any MAC with $t$-bit tags and deterministic verification, an adversary that submits $q_v$ pairs for verification, each with a fresh message and a uniformly random tag, forges with probability at least $1 - (1 - 2^{-t})^{q_v} \ge q_v 2^{-t} (1 - q_v 2^{-t}/2)$.

**Proof.** For a fixed key and a fresh message $M$, exactly one tag value $\mathsf{Mac}_K(M)$ is accepted if the MAC is deterministic, and at least one in general. A uniformly random guess hits an accepted tag with probability at least $2^{-t}$, independently for each attempt given the key, so all $q_v$ attempts fail with probability at most $(1 - 2^{-t})^{q_v}$. The second form follows from $(1 - x)^q \le 1 - qx + \binom{q}{2}x^2$ for $0 \le x \le 1$. $\blacksquare$

So tags of 32 bits give no protection against an attacker that can try millions of times, and 64 to 128 bits are normal. In the same way, a key of $k$ bits is found by trying all $2^k$ keys against one known pair, so $k \ge 128$ is normal.

**Unconditional schemes need key material per message.** A Wegman and Carter MAC with a one-time pad on a $t$-bit tag uses $t$ fresh key bits per message, and it is secure against unbounded adversaries. A computationally secure MAC reuses one short key for many messages.

## Reductions

- **A PRF is a MAC.** If $F$ is a [pseudorandom function](/pseudorandom-function/) with $t$-bit outputs, $\mathsf{Mac}_K(M) = F_K(M)$ is EUF-CMA secure with advantage at most $\mathrm{Adv}^{\mathrm{prf}}_F + 2^{-t}$. Proof on the [message authentication code](/message-authentication-code/) page.
- **Universal hash plus PRF.** $T = h_{K_1}(M) \oplus F_{K_2}(N)$ for a nonce $N$ (Wegman and Carter) or $T = h_{K_1}(M) + s$ with a one-time $s$ (Poly1305).
- **A MAC from a signature.** A signature scheme with the signing key shared is a MAC, but slower than needed.
- **Authenticated encryption from encryption and a MAC.** Encrypt-then-MAC with independent keys, see [authenticated encryption](/authenticated-encryption/).

## Applications

TLS and IPsec records (through AEAD), SSH packets, API request signing with HMAC (for example AWS Signature Version 4), session cookies and tokens such as JWT with HS256, message integrity in Kerberos tickets, firmware and software update signatures, and banking messages, where the CBC-MAC of ISO/IEC 9797-1 was long the standard.

## References
