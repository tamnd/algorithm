---
tag: YSM480
kind: concept
slug: key-confirmation
name: Key confirmation
area: cryptography/key-exchange
level: advanced
summary: Key confirmation lets one party check that its peer holds the same new key, usually with a MAC under a key derived from the shared secret over the transcript, as in the TLS 1.3 Finished message.
prereqs: [authenticated-key-exchange, hmac]
see_also: [session-key, tls-handshake, hkdf, entity-authentication, man-in-the-middle-attack, perfect-forward-secrecy, station-to-station-protocol, sigma-key-exchange]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 12.2.1, Definition 12.6 (implicit key authentication), Definition 12.7 (key confirmation) and Definition 12.8 (explicit key authentication)
  - url: "https://doi.org/10.6028/NIST.SP.800-56Ar3"
    title: "E. Barker, L. Chen, A. Roginsky, A. Vassilev and R. Davis, NIST SP 800-56A Rev. 3, Recommendation for Pair-Wise Key-Establishment Schemes Using Discrete Logarithm Cryptography, April 2018"
    locator: Section 5.9 (5.9.1 unilateral, 5.9.2 bilateral, 5.9.3 MAC choice and MacTagBits of at least 64)
  - url: "https://www.rfc-editor.org/rfc/rfc8446"
    title: "E. Rescorla, RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3, 2018"
    locator: Section 4.4.4 (Finished) and Section 7.1 (HKDF-Expand-Label)
  - url: "https://www.rfc-editor.org/rfc/rfc8448"
    title: "M. Thomson, RFC 8448, Example Handshake Traces for TLS 1.3, 2019"
    locator: Section 3 (simple 1-RTT handshake), the server Finished computation used as the test vector
  - paper: "Marc Fischlin, Felix Günther, Benedikt Schmidt and Bogdan Warinschi, Key confirmation in key exchange: a formal treatment and implications for TLS 1.3, IEEE Symposium on Security and Privacy 2016"
    locator: the game-based definitions of key confirmation and their use for TLS 1.3 (page numbers to check)
---

Key confirmation is the property that a party in a key exchange is assured that its peer actually holds the same new [session key](/session-key/). The peer proves this by computing a value that needs the key, most often a MAC under a key derived from the shared secret, over the transcript of the exchange. Key confirmation turns implicit key authentication ("only B *could* know the key") into explicit key authentication ("B *does* know the key"). The Finished messages of [TLS 1.3](/tls-handshake/) and the MacTag of NIST SP 800-56A are the two standard forms.

**Notation.** $Z$ is the shared secret of the key exchange, KDF the key derivation function, $\mathrm{MAC}_k(m)$ an [HMAC](/hmac/) under key $k$, $\mathrm{ID}_P$ and $\mathrm{ID}_R$ the identities of the provider and the recipient of the confirmation, and $T_n(s)$ the first $n$ bits of $s$.

## In plain words

Two people set up a secret key over the network. Each of them computed the key on their own, from the messages they got. How does Alice know that Bob got the same key? An error, or an attacker who changed a message on the way, can make the two keys differ, and then nothing works, or worse, something works in a way that nobody planned.

Key confirmation is a short final message. Bob uses the new key to make a check value over everything that was said in the exchange, and sends it. Alice computes the same value with her key and her own record of the exchange. If they match, Alice knows that Bob has the key and that he saw the same messages she saw.

Key confirmation does not tell Alice who Bob is. That part must come from somewhere else.

## The idea

### Definitions

The Handbook of Applied Cryptography gives three related definitions:

- **Implicit key authentication** (Definition 12.6): one party is assured that no party other than a specifically identified second party (and maybe trusted third parties) may gain access to a particular secret key.
- **Key confirmation** (Definition 12.7): one party is assured that a second (possibly unidentified) party actually has possession of a particular secret key.
- **Explicit key authentication** (Definition 12.8): both implicit key authentication and key confirmation hold.

The words "possibly unidentified" matter. A MAC under the new key proves possession of the key, not identity. Together with implicit key authentication (the key can only be known by $B$), it proves that $B$ is present.

### The SP 800-56A MacTag

NIST SP 800-56A Rev. 3 (Section 5.9) fixes the form for its discrete logarithm schemes. The derived keying material is split into two parts of agreed lengths,

$$\mathrm{MacKey} \,\|\, \mathrm{KeyData} = \mathrm{KDF}(Z, \dots),$$

and the provider $P$ sends to the recipient $R$

$$\mathrm{MacTag}_P = T_{\mathrm{MacTagBits}}\big(\mathrm{MAC}(\mathrm{MacKey},\ \texttt{message\_string} \,\|\, \mathrm{ID}_P \,\|\, \mathrm{ID}_R \,\|\, \mathrm{EphemData}_P \,\|\, \mathrm{EphemData}_R \,\|\, \mathrm{Text}_P)\big).$$

The six-byte message_string is "KC_1_U" or "KC_1_V" for unilateral confirmation from party U or V, and "KC_2_U" or "KC_2_V" for bilateral confirmation. The ephemeral data are the ephemeral public keys or nonces of the two parties. The recipient recomputes the tag and compares. Section 5.9.3 lists the approved MACs (HMAC with SHA-2 or SHA-3, KMAC, AES-CMAC) and sets MacTagBits to at least 64. Both parties destroy MacKey once confirmation is done; if the tag does not verify, they destroy all of the derived keying material and stop. MacKey is separate from KeyData, so the key that is used later never touches a value that was sent in the clear.

### The TLS 1.3 Finished message

TLS 1.3 (RFC 8446, Section 4.4.4) ends each side of the handshake with a Finished message:

$$\text{finished\_key} = \text{HKDF-Expand-Label}(\text{BaseKey}, \texttt{"finished"}, \texttt{""}, L),$$
$$\text{verify\_data} = \mathrm{HMAC}(\text{finished\_key},\ \text{Transcript-Hash}(\text{all handshake messages so far})).$$

BaseKey is the handshake traffic secret of the sender, and $L$ is the hash length. Because the MAC covers the hash of the whole transcript, the Finished message confirms the key *and* that both sides saw the same messages. An attacker who changes any message, for example to remove strong cipher suites from the ClientHello, makes the transcripts differ and the Finished check fail, even if the attacker cannot change the shared secret.

### What key confirmation gives and what it does not

- **It detects disagreement early.** A changed message, a wrong key derivation or a bug shows up during the handshake and not as garbage later.
- **It binds the transcript.** A MAC over the transcript catches changes that a signature over only part of the messages misses (the downgrade example below).
- **It completes protocols that are only implicitly authenticated.** In a two-message protocol such as [HMQV](/hmqv/), the initiator never proves that it took part. A third message with a MAC gives explicit authentication and lifts the protocol from weak to full [forward secrecy](/perfect-forward-secrecy/).
- **It proves possession of a static key.** SP 800-56A notes that when the scheme uses the static key of the provider, a correct MacTag shows that the provider holds the matching private key.
- **It is not entity authentication.** Over an unauthenticated exchange, a [man in the middle](/man-in-the-middle-attack/) runs one exchange with each side and confirms each key.
- **It is not needed for key secrecy.** In the Canetti-Krawczyk model, protocols such as HMQV are secure without it. Key confirmation adds a separate guarantee about the peer's state.

A design rule follows from this: the confirmation MAC must use a key that is separate from the session key (MacKey in SP 800-56A, finished_key in TLS), so that the MAC does not give an adversary a known function of the session key. In the [station-to-station protocol](/station-to-station-protocol/), the signatures are encrypted under the new key to give key confirmation; [SIGMA](/sigma-key-exchange/) replaces this with a separate MAC key.

## Examples

**The RFC 8448 trace.** In the TLS 1.3 example trace (RFC 8448, Section 3), the server handshake traffic secret is b67b7d69...d391ad38. HKDF-Expand-Label with label "tls13 finished" gives finished_key 008d3b66...cdc19fc8. The HMAC of finished_key over SHA-256 of ClientHello, ServerHello, EncryptedExtensions, Certificate and CertificateVerify (907 bytes) is verify_data 9b9b141d...b78f0718. The tests recompute all three values from the bytes of the trace. A single bit flipped in any of the five messages gives a different verify_data.

**A downgrade that only the Finished message catches.** In the toy handshake of the code, the client offers the suites (strong, weak), and the server signs only its ephemeral value $Y$ and the client nonce. An attacker deletes "strong" from the offer. The server picks "weak", its signature still verifies, and both sides still compute the same $Z$. But the client's transcript has (strong, weak) and the server's has (weak), so the Finished values differ and both sides abort.

**Confirmation without authentication.** Alice and Bob run the same handshake with no signatures. Mallory answers Alice with her own $Y$ and calls Bob with her own $X$. Alice's Finished check passes against Mallory, and Bob's passes against Mallory. Each key is confirmed, but with the wrong party.

**The code.** The Python code on this page implements HKDF, HKDF-Expand-Label, the TLS 1.3 Finished computation and the SP 800-56A MacTag with all four message strings, and checks them against RFC 5869 and RFC 8448. It compares tags with hmac.compare_digest. Otherwise it is for study only: it is not constant time, the toy handshake uses a 256-bit prime order group and a simple encoding, and it must not protect real data. Use TLS 1.3 through OpenSSL, BoringSSL or rustls, or a FIPS 140 validated module.

## Where it is used

- [TLS 1.3](/tls-handshake/) Finished messages in both directions; TLS 1.2 also has Finished messages, computed with its PRF.
- NIST SP 800-56A (discrete logarithm schemes) and SP 800-56B (RSA schemes) as an option for approved key establishment.
- [IKEv2](/ike-protocol/): the AUTH payload is a signature or a MAC over the exchange that includes a key from SKEYSEED, which gives key confirmation.
- The [station-to-station protocol](/station-to-station-protocol/) and [SIGMA](/sigma-key-exchange/) through encrypted signatures or a MAC over the identity.
- The [Noise framework](/noise-protocol-framework/) gets it implicitly: each handshake payload is encrypted with a key that depends on the chaining key, and a successful decryption confirms the key.

## References
