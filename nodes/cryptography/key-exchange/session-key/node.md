---
tag: 6FTZV2
kind: concept
slug: session-key
name: Session key
aliases:
- ephemeral session key
area: cryptography/key-exchange
level: intro
summary: A short-lived symmetric key that protects one communication session. It comes from key establishment and a KDF, and is discarded at the end of the session.
prereqs: [pseudorandom-function]
see_also: [key-agreement-problem, key-transport-problem, key-distribution-problem, hkdf, perfect-forward-secrecy, key-confirmation, authenticated-key-exchange, tls-handshake]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 12, Section 12.2.1 (Definitions 12.2 to 12.5, and the motivation for session keys) and Section 12.2.3 (Definition 12.16, perfect forward secrecy)
  - paper: doi:10.1007/3-540-48329-2_21
    title: Mihir Bellare and Phillip Rogaway, Entity authentication and key distribution, CRYPTO 1993, LNCS 773, pages 232 to 249
    locator: the model with session oracles, Reveal and Test queries, and the definition of a secure authenticated key exchange
  - paper: doi:10.1007/3-540-44987-6_28
    title: Ran Canetti and Hugo Krawczyk, Analysis of key-exchange protocols and their use for building secure channels, EUROCRYPT 2001, LNCS 2045, pages 453 to 474
    locator: the definition of SK-security, session-state reveal and session expiration, and the result that SK-secure key exchange gives secure channels
  - url: "https://www.rfc-editor.org/rfc/rfc8446"
    title: Eric Rescorla, RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3, August 2018
    locator: Section 7.1 (Key Schedule), Section 7.2 (Updating Traffic Secrets), Section 7.3 (Traffic Key Calculation)
  - url: "https://www.rfc-editor.org/rfc/rfc8448"
    title: Martin Thomson, RFC 8448, Example Handshake Traces for TLS 1.3, January 2019
    locator: Section 3 (Simple 1-RTT Handshake)
  - paper: doi:10.6028/NIST.SP.800-56Cr2
    title: Elaine Barker, Lily Chen and Richard Davis, NIST SP 800-56C Rev. 2, Recommendation for Key-Derivation Methods in Key-Establishment Schemes, August 2020
    locator: Section 4 (one-step key derivation) and Section 5 (two-step key derivation, extraction then expansion)
  - book: isbn:9783662581452
    title: Colin Boyd, Anish Mathuria and Douglas Stebila, Protocols for Authentication and Key Establishment, second edition, Springer, 2020
    locator: Chapter 1 (session keys, goals of key establishment) and Chapter 2 (computational security models)
---

A session key is a short-lived symmetric key that two or more parties use to protect the messages of one session, for example one TLS connection, and then erase. The parties get it from a key establishment protocol: [key agreement](/key-agreement-problem/), [key transport](/key-transport-problem/) or a [key distribution](/key-distribution-problem/) center. A key derivation function such as [HKDF](/hkdf/) turns the established secret into several independent keys, one for each direction and each purpose. Long-term keys only authenticate the parties or carry the session key, so a lost session key exposes one session and not the others.

**Notation.** $Z$ is the shared secret that key establishment gives (for example a Diffie-Hellman value). $\mathrm{KDF}$ is a key derivation function, $\ell$ a label that names the purpose of a key, and $T$ the transcript of the session. $K$ is a session key. $\mathcal{A}$ is an adversary, and $\mathrm{Adv}$ its advantage in a named game.

## In plain words

Two computers that want to talk in secret need a shared key. They could use the same key for years, but then one leak exposes everything they ever said, and an attacker gets a large amount of traffic under one key to study. So they make a fresh key for each conversation and destroy it at the end.

The fresh key comes from a short exchange at the start of the conversation. The exchange gives a shared secret, and a key derivation step turns it into several keys: one to encrypt what the first side sends, one for the other side, and others for other jobs. Each key has one job only.

A good design makes sure that an attacker who learns the key of one conversation learns nothing about the keys of other conversations.

## The idea

**Why short-lived keys.** Menezes, van Oorschot and Vanstone (HAC, Section 12.2.1) give four reasons: limit the ciphertext under one key that is available for cryptanalysis; limit the exposure, in time and in data, when a key is compromised; avoid the storage of many long-term keys, because a key is made only when it is needed; and make sessions and applications independent of each other. Modern designs add a fifth reason: if the session key comes from ephemeral values that are then erased, a later theft of long-term keys does not expose past sessions. This is [forward secrecy](/perfect-forward-secrecy/) (HAC, Definition 12.16).

**A key hierarchy.** Long-term keys sit at the top: signature keys, certificates, pre-shared keys, or keys shared with a [key distribution center](/key-distribution-center/). They are used only in the handshake. The handshake gives a secret $Z$. Session keys sit below it and do the bulk encryption and authentication. A session key must never be used as a long-term key, and a long-term key must never encrypt bulk data.

**From a shared secret to keys.** A Diffie-Hellman value $Z$ is a group element. It is hard to compute for an outsider, but it is not a uniform string: for example, in a prime-order subgroup of $\mathbb{Z}_p^*$ it is a quadratic residue, so its bits are not independent. So $Z$ is never used as a key directly. A KDF first extracts a uniform pseudorandom key from $Z$ and then expands it into as many keys as needed:

$$K_\ell = \mathrm{KDF}(Z, \ell, T) \quad \text{for each label } \ell.$$

NIST SP 800-56C Rev. 2 gives one-step KDFs (Section 4) and two-step KDFs (Section 5, extraction then expansion); HKDF is a two-step KDF. Putting the transcript $T$ into the derivation binds the keys to the session, so two sessions with different messages get unrelated keys.

**Key separation.** Each key has one purpose: one direction, one algorithm, one role. Different labels $\ell$ give keys that are computationally independent if the KDF is a [pseudorandom function](/pseudorandom-function/). This stops attacks that reflect a message back to its sender, and attacks that move a value from one algorithm into another.

**Security of session keys.** Bellare and Rogaway (CRYPTO 1993) gave the first formal model. The adversary controls the network and talks to many session instances. It may learn the session keys of some sessions by a Reveal query and the long-term keys of some parties by a Corrupt query. At one fresh session (not revealed, and with an uncorrupted partner) it makes a Test query and gets either the real session key or a uniform random key. The protocol is secure if partners that accept get the same key and

$$\mathrm{Adv}(\mathcal{A}) = \bigl|\Pr[\mathcal{A} \text{ guesses which key it got}] - \tfrac{1}{2}\bigr|$$

is negligible. So a session key must look random even to an adversary who knows the keys of all other sessions. Canetti and Krawczyk (EUROCRYPT 2001) added queries that reveal the internal state of a session and an expiration event that models forward secrecy. They called the result SK-security, and proved that the key of an SK-secure protocol, used with standard symmetric encryption and a MAC, gives a secure channel.

**Lifetime.** A session key ends with its session, or earlier: TLS 1.3 can replace the traffic keys during a connection (RFC 8446, Section 7.2), and the [double ratchet](/double-ratchet/) of Signal derives a new key for each message. Erasing old keys is part of the design: forward secrecy holds only if the old keys and ephemeral secrets are actually gone.

## Examples

**TLS 1.3, RFC 8448 Section 3.** The client and the server run X25519 and both get the 32-byte shared secret

$$Z = \texttt{8bd4054fb55b9d63fdfbacf9f04b9f0d35e6d63f537563efd46272900f89492d}.$$

The key schedule of RFC 8446, Section 7.1, extracts the handshake secret from $Z$ and then derives one secret for each direction from it, with the labels `c hs traffic` and `s hs traffic` and the hash of the first two handshake messages:

| value | first 16 bytes |
|---|---|
| handshake secret | `1dc826e93606aa6fdc0aadc12f741b01` |
| client handshake traffic secret | `b3eddb126e067f35a780b3abf45e2d8f` |
| server handshake traffic secret | `b67b7d690cc16c4e75e54213cb2d37b4` |

From the server traffic secret, the labels `key` and `iv` give the server's AES-128-GCM write key `3fce516009c21727d0f2e4e86ee403bc` and its 12-byte IV `5d313eb2671276ee13000b30` (Section 7.3). The client gets its own key and IV from its own secret. The two directions never share a key, and the application data later uses keys from another pair of secrets.

**Kerberos.** A [key distribution center](/key-distribution-center/) makes a fresh session key for a client and a service and gives a copy to each of them, encrypted under the long-term key it shares with that party; the copy for the service travels inside a ticket that the client forwards (see [Kerberos](/kerberos/)). Here the session key comes from key transport, and the KDC chooses it alone.

**SSH.** RFC 4253, Section 7.2, derives six values from the shared secret $K$, the exchange hash $H$ and the session identifier, with the single letters `A` to `F` as labels: an IV, an encryption key and an integrity key for each direction.

**Non-example: one key for everything.** A device that uses the raw Diffie-Hellman value as one AES key in both directions breaks two rules. The value is not uniform, and the same key in both directions lets an attacker send a message back to its sender, who accepts it as a message from the peer.

**Non-example: a long-term pre-shared key used directly.** If two sites encrypt all traffic with a fixed key typed into both devices, there is no session key. A leak of that key exposes every past and future message.

## Where it is used

- **TLS 1.3 and QUIC.** The key schedule derives handshake keys, application keys, resumption secrets and exporter secrets from the (EC)DHE secret, each with its own label ([TLS handshake](/tls-handshake/)).
- **IPsec IKEv2.** RFC 7296, Section 2.14, derives SKEYSEED from the Diffie-Hellman value and then the keys SK_d, SK_ai, SK_ar, SK_ei, SK_er, SK_pi and SK_pr, one per purpose and direction.
- **SSH**, as in the example above.
- **Signal and other [secure messaging](/secure-messaging/).** [X3DH](/x3dh/) gives the first shared secret, and the [double ratchet](/double-ratchet/) derives a new message key for each message.
- **Kerberos and other KDC systems**, where the center makes the session key ([key distribution problem](/key-distribution-problem/)).
- **Wi-Fi (WPA2 and WPA3).** The four-way handshake derives a pairwise transient key for one association from a longer-term pairwise master key.

## References
