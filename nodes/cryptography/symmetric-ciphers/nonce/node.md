---
tag: KJJQF7
kind: definition
slug: nonce
name: Nonce
aliases:
- number used once
area: cryptography/symmetric-ciphers
level: intro
summary: A public value that must never repeat under one key but may be predictable. CTR, GCM and ChaCha20-Poly1305 need nonces; a repeat leaks plaintext XORs and can allow forgery.
prereqs: [symmetric-encryption, birthday-paradox]
see_also: [initialization-vector, ctr-mode, gcm-mode, chacha20-poly1305, authenticated-encryption, nonce-reuse-attack, birthday-attack]
sources:
  - paper: "Phillip Rogaway, Nonce-based symmetric encryption, Fast Software Encryption (FSE 2004), LNCS 3017, pages 348 to 359"
    locator: the syntax of nonce-based encryption and the notion of indistinguishability from random bits for nonce-respecting adversaries
  - url: "https://doi.org/10.6028/NIST.SP.800-38D"
    title: Morris Dworkin, NIST Special Publication 800-38D, Recommendation for Block Cipher Modes of Operation, Galois/Counter Mode (GCM) and GMAC, 2007
    locator: Section 8 (uniqueness requirement on IVs and keys), Section 8.2 (deterministic and RBG-based IV constructions) and Section 8.3 (at most 2^32 invocations with RBG-based or non-96-bit IVs)
  - url: "https://www.rfc-editor.org/rfc/rfc8439"
    title: Yoav Nir and Adam Langley, RFC 8439, ChaCha20 and Poly1305 for IETF Protocols, 2018
    locator: Section 2.3 (the 96-bit nonce of ChaCha20) and Section 4 (security considerations on nonce uniqueness)
  - url: "https://doi.org/10.6028/NIST.SP.800-38A"
    title: Morris Dworkin, NIST Special Publication 800-38A, Recommendation for Block Cipher Modes of Operation, Methods and Techniques, 2001
    locator: Appendix B (unique counter blocks for CTR) and Section 5.3 (the OFB IV must be a nonce)
---

A nonce ("number used once") is a public input to encryption that must never take the same value twice under the same key. Unlike an [initialization vector](/initialization-vector/) for CBC, it does not need to be random or unpredictable: a simple message counter is a perfect nonce. Rogaway (FSE 2004) made this precise as nonce-based encryption, and it is the interface of [CTR](/ctr-mode/), [GCM](/gcm-mode/), [CCM](/ccm-mode/), [OCB](/ocb-mode/) and [ChaCha20-Poly1305](/chacha20-poly1305/). If a nonce repeats, these schemes fail badly: the keystream repeats, so the XOR of two plaintexts leaks, and in GCM and ChaCha20-Poly1305 the attacker can also forge.

## Definition

**Notation.** $K$ is the key, $N$ the nonce, $\mathcal{N} = \{0,1\}^\nu$ the nonce space ($\nu = 96$ for GCM and ChaCha20-Poly1305), $M$ the message and $q$ the number of encryptions under one key.

**Nonce-based encryption (Rogaway, FSE 2004).** A nonce-based scheme is a pair of deterministic functions $\mathcal{E}(K, N, M)$ and $\mathcal{D}(K, N, C)$ with $\mathcal{D}(K, N, \mathcal{E}(K, N, M)) = M$. The caller supplies $N$, and the nonce is sent with the ciphertext or known to the receiver from context.

**Nonce-respecting adversary.** An adversary is nonce-respecting if it never asks for two encryptions with the same nonce. Security (Rogaway calls it $\mathrm{IND\$\text{-}CPA}$) asks that for every nonce-respecting adversary, the oracle $\mathcal{E}(K, \cdot, \cdot)$ be hard to tell from an oracle that returns random strings of the right length. The adversary may choose the nonces, so they may be predictable, sequential or even chosen in advance: only repetition is forbidden.

**The nonce rule.** A user of a nonce-based scheme must ensure that $(K, N)$ pairs never repeat for encryption. There are three ways.

1. **A counter.** Keep a counter per key and increment it for each message. No repeat is possible while the state is kept safe. This is the deterministic construction of SP 800-38D, Section 8.2.1, where a fixed field names the device and an invocation field counts.
2. **Random values.** Draw $N$ uniformly from $\{0,1\}^\nu$. No state is needed, but a repeat happens by chance, as computed below. SP 800-38D, Section 8.2.2, allows this for GCM with limits.
3. **Derived values.** Use a unique value already present, such as a record sequence number. TLS 1.3 XORs the 64-bit record sequence number into a per-connection IV to form the 96-bit nonce.

### The birthday bound for random nonces

**Claim.** If $q$ nonces are drawn independently and uniformly from $\{0,1\}^\nu$, the probability that two are equal is at most $q(q-1)/2^{\nu+1}$.

**Proof.** There are $\binom{q}{2}$ pairs, and each pair is equal with probability $2^{-\nu}$. The union bound gives $\binom{q}{2} 2^{-\nu} = q(q-1)/2^{\nu+1}$. $\blacksquare$

The bound is close to the truth while it is small; the exact value is about $1 - e^{-q(q-1)/2^{\nu+1}}$ (see the [birthday paradox](/birthday-paradox/)).

| nonce bits $\nu$ | messages $q$ | bound $q(q-1)/2^{\nu+1}$ | about $1 - e^{-x}$ |
|---|---|---|---|
| 96 | $2^{32}$ | $1.16 \times 10^{-10} \approx 2^{-33}$ | $1.16 \times 10^{-10}$ |
| 96 | $2^{40}$ | $7.6 \times 10^{-6} \approx 2^{-17}$ | $7.6 \times 10^{-6}$ |
| 96 | $2^{48}$ | $0.5$ | $0.39$ |
| 64 | $2^{32}$ | $0.5$ | $0.39$ |
| 192 | $2^{64}$ | $2.7 \times 10^{-20} = 2^{-65}$ | $2.7 \times 10^{-20}$ |

This is where the NIST limit comes from. SP 800-38D, Section 8, requires the probability that one key is ever used with the same IV on two different inputs to be at most $2^{-32}$. Section 8.3 then says that, when IVs come from the random construction or have a length other than 96 bits, the total number of invocations of authenticated encryption under one key shall not exceed $2^{32}$. The first row of the table shows the margin: $2^{-33}$. The last row is the reason for 192-bit nonces in XChaCha20: random nonces are then safe for any realistic number of messages.

### What fails when a nonce repeats

- **CTR and every stream mode.** The same $(K, N)$ gives the same keystream $O$, so $C \oplus C' = P \oplus P'$, the two-time pad. The tests of the [CTR mode](/ctr-mode/) page recover the second message from the first this way.
- **GCM.** Two messages under the same nonce share both the keystream and the mask $E_K(J_0)$ of the tag. The XOR of the two tags is a known polynomial in the hash key $H$, whose roots include $H$; once $H$ is known, the attacker forges tags for any ciphertext under that nonce (Joux, 2006). See [GCM](/gcm-mode/).
- **ChaCha20-Poly1305.** The Poly1305 one-time key is derived from the nonce, so a repeat reuses it, and two tags give $r$ and $s$ and so forgeries. See [Poly1305](/poly1305/).
- **CCM, EAX and OCB.** Confidentiality fails in the same way for the CTR part of CCM and EAX. OCB with a repeated nonce repeats its offsets, so it acts like ECB at each position: equal blocks at equal positions give equal ciphertext blocks.

## Examples and non-examples

- **Example: a 64-bit message counter padded to 96 bits.** Never repeats while the counter state survives. Predictable, and that is fine.
- **Example: TLS 1.3 record nonces.** Per-connection IV XOR the record number; unique because each connection has its own keys.
- **Non-example: a counter that resets to zero on reboot, with a long-term key.** After the reboot the old nonces come back. Store the counter, or derive a new key per boot.
- **Non-example: a random 64-bit nonce.** By the table, a repeat is likely after about $2^{32}$ messages.
- **Non-example: a nonce as the IV of CBC.** CBC needs an unpredictable IV, and a counter is not one. Rogaway (FSE 2004) shows that CBC with a nonce as IV is insecure, and that $IV = E_K(N)$ repairs it. See [initialization vector](/initialization-vector/).
- **Different meaning: nonces in authentication protocols.** In a challenge-response protocol a nonce is a fresh challenge that proves an answer is new. There it often must be unpredictable as well, so that an attacker cannot collect answers in advance.

## Related definitions

- **[Initialization vector](/initialization-vector/).** Must be uniformly random and unpredictable for CBC and CFB. A random IV is a nonce with high probability, but a nonce need not be an IV of that kind.
- **Nonce-misuse resistance.** A scheme such as SIV (RFC 5297) or AES-GCM-SIV (RFC 8452) whose security degrades only to revealing equal messages when a nonce repeats. See [authenticated encryption](/authenticated-encryption/).
- **[Nonce reuse attack](/nonce-reuse-attack/).** The same failure for signatures: a repeated ECDSA or DSA nonce reveals the private key.
- **Salt and tweak.** Public values that change a key derivation or a permutation; they do not carry the never-repeat rule.

## References
