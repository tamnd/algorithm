---
tag: TTAAD5
kind: concept
slug: hybrid-key-exchange
name: Hybrid key exchange
aliases:
- combined classical and post-quantum key exchange
- hybrid key agreement
- hybrid key establishment
area: cryptography/key-exchange
level: advanced
summary: A key exchange that runs a classical method (such as X25519) and a post-quantum KEM (such as ML-KEM) together and joins both secrets in a KDF, so the key is safe if either part holds.
prereqs: [x25519, key-encapsulation-mechanism, hkdf]
see_also: [x25519, crystals-kyber, key-encapsulation-mechanism, hkdf, harvest-now-decrypt-later, post-quantum-cryptography, frodokem, tls-handshake]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc9954"
    title: Douglas Stebila, Scott Fluhrer and Shay Gueron, RFC 9954, Hybrid Key Exchange in TLS 1.3, July 2026
    locator: Section 3.3 (shared secret calculation, the concatenation of the component secrets as input to the TLS 1.3 key schedule)
  - url: "https://www.rfc-editor.org/rfc/rfc10024"
    title: Kris Kwiatkowski, Panos Kampanakis, Bas Westerbaan and Douglas Stebila, RFC 10024, Post-Quantum Traditional (PQ/T) Hybrid Key Agreement Mechanisms for TLS 1.3, August 2026
    locator: Section 4.1 (client share), Section 4.2 (server share) and Section 4.3 (shared secret) for X25519MLKEM768, SecP256r1MLKEM768 and SecP384r1MLKEM1024
  - paper: doi:10.1007/978-3-319-76578-5_7
    title: Federico Giacon, Felix Heuer and Bertram Poettering, KEM combiners, PKC 2018, LNCS 10769, pages 190 to 218
    locator: the definition of a KEM combiner, why XOR of the keys fails for IND-CCA, and combiners that hash the keys together with the ciphertexts
  - paper: doi:10.1007/978-3-030-25510-7_12
    title: Nina Bindel, Jacqueline Brendel, Marc Fischlin, Brian Goncalves and Douglas Stebila, Hybrid key encapsulation mechanisms and authenticated key exchange, PQCrypto 2019, LNCS 11505, pages 206 to 226
    locator: the security of hybrid KEM combiners against quantum adversaries and the analysis of hybrid authenticated key exchange in TLS 1.3 style
  - url: "https://csrc.nist.gov/pubs/fips/203/final"
    title: NIST FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard, August 2024
    locator: the ML-KEM-768 parameter set and the sizes of its encapsulation key (1184 bytes), ciphertext (1088 bytes) and shared secret (32 bytes)
---

A hybrid key exchange is a key exchange that runs two or more component methods at once, typically a classical one such as [X25519](/x25519/) and a post-quantum [key encapsulation mechanism](/key-encapsulation-mechanism/) such as ML-KEM, and derives the session key from all of their shared secrets. The goal is that the key stays secret as long as at least one component is secure: X25519 protects against a flaw in the new lattice scheme, and ML-KEM protects against a future quantum computer that would break X25519. Since 2023 major browsers and servers have deployed it in TLS 1.3 to stop "harvest now, decrypt later" attacks, and RFC 10024 (2026) standardizes X25519MLKEM768.

**Notation.** $\mathrm{KEM} = (\mathrm{KeyGen}, \mathrm{Encaps}, \mathrm{Decaps})$ is the post-quantum KEM; $\mathrm{Encaps}(pk)$ returns a ciphertext $ct$ and a secret $ss_{pq}$. $x$ and $y$ are the X25519 secrets of the client and the server, and $ss_{ec}$ is their X25519 shared secret. $\mathrm{KDF}$ is a key derivation function such as [HKDF](/hkdf/), and the transcript is the list of messages sent.

## In plain words

Nobody knows for sure how strong the new post-quantum methods are, and the old methods will fall if a large quantum computer is built. So use both at once.

The two sides run an old exchange and a new one in the same messages. Each exchange gives them a secret. They put both secrets, and a record of the messages, into a key derivation function, and use its output as the key.

An attacker who breaks only one of the two methods still lacks one secret, so the output still looks random to her. She must break both. The price is bigger messages and a little more work.

## The idea

**One round trip, two secrets.** The client sends a KEM public key and an X25519 share; the server encapsulates to the KEM key and sends the ciphertext and its own X25519 share. This fits the one-round-trip shape of the TLS 1.3 key share, which is why a KEM, not a DH-style post-quantum method, is used.

```pseudo id=main
HYBRID-EXCHANGE()
L1  client: (pk, sk) ← KEM.KeyGen()
L2  client: send share_C = pk ‖ X25519(x, 9)
L3  server: (ct, ss_pq) ← KEM.Encaps(pk)
L4  server: send share_S = ct ‖ X25519(y, 9); ss_ec ← X25519(y, X_C)
L5  client: ss_pq ← KEM.Decaps(sk, ct); ss_ec ← X25519(x, Y_S)
L6  both: K ← KDF(ss_pq ‖ ss_ec, transcript)
```

**The combiner.** Line L6 is where hybrid designs succeed or fail. If the KDF is a good [pseudorandom function](/pseudorandom-function/) keyed by either input, or is modelled as a random oracle, then $K$ is pseudorandom whenever one of $ss_{pq}$ and $ss_{ec}$ is unknown to the attacker. Two simple combiners are wrong:

- **Truncation.** Keeping only the first 32 bytes of $ss_{ec} \,\|\, ss_{pq}$ keeps only $ss_{ec}$, so breaking X25519 alone gives the key.
- **XOR.** $ss_{pq} \oplus ss_{ec}$ keeps passive security, but Giacon, Heuer and Poettering (2018) show that XOR does not keep IND-CCA security in general: an attacker can change one ciphertext and keep one key fixed. Hashing the ciphertexts together with the keys fixes this.

TLS 1.3 feeds the concatenation into HKDF-Extract of its key schedule, and the later Derive-Secret steps hash in the transcript, which includes $pk$, $ct$ and both shares (RFC 9954, Section 3.3). For X25519MLKEM768 the ML-KEM secret comes first (RFC 10024, Section 4.3).

**What it protects and what it does not.** Hybrid key exchange gives confidentiality of the session against a future quantum attacker, as long as the KEM holds. It does not give post-quantum authentication: the signatures in the certificates are still classical, and an attacker with a quantum computer at the time of the handshake could forge them. That threat starts only when such a computer exists, while recorded traffic is at risk from today, which is why key exchange was moved first.

**Cost.** For X25519MLKEM768 the client share is $1184 + 32 = 1216$ bytes and the server share $1088 + 32 = 1120$ bytes, against 32 bytes each for X25519 alone (RFC 10024, Sections 4.1 and 4.2). The larger ClientHello can split into two network packets, which broke some middleboxes in early tests. The computing cost of ML-KEM is about the same as that of X25519.

## Examples

**Toy run.** The Python code of this page joins X25519 (the RFC 7748 function, checked against its Section 6.1 example) with a toy FrodoKEM-style LWE KEM of dimension 64, which stands in for ML-KEM-768. ML-KEM is not implemented here, and the toy KEM is neither secure (the dimension is far too small) nor IND-CCA (it has no [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/)). The combiner is HKDF-SHA-256 with a zero salt, IKM $= ss_{pq} \,\|\, ss_{ec}$, and info a label plus the SHA-256 hash of the transcript. Client and server derive the same 32-byte key. If an attacker learns $ss_{ec}$ but guesses $ss_{pq}$, or the reverse, her 100 guesses never give the key; a change of one byte in the transcript changes the key; and the truncation combiner above gives exactly $ss_{ec}$. The code is for study only and is not constant time, and both parties are local simulations.

**TLS 1.3 deployment.** Google Chrome and Cloudflare tested X25519Kyber768 in 2023, then moved to X25519MLKEM768 after FIPS 203 was published in August 2024. OpenSSL 3.5 and later, BoringSSL and rustls offer it, and by 2025 a large share of TLS connections from browsers used it.

**SSH.** OpenSSH 9.0 (2022) made the hybrid sntrup761x25519-sha512 its default, and later versions added mlkem768x25519-sha256; RFC 10042 (2026) specifies ML-KEM hybrids for SSH.

**Messaging.** Signal's PQXDH (2023) adds a Kyber encapsulation to the X3DH handshake and hashes all secrets together, and Apple's iMessage PQ3 (2024) does a similar thing.

## Where it is used

- **TLS 1.3 and QUIC**, through the named groups X25519MLKEM768, SecP256r1MLKEM768 and SecP384r1MLKEM1024.
- **SSH**, IKEv2 (with additional key exchanges) and WireGuard variants with a post-quantum pre-shared key.
- **Secure messaging**, in PQXDH and similar protocols, and in the [double ratchet](/double-ratchet/) when it adds post-quantum steps.
- **Migration policy.** Many government guides ask for hybrid exchange during the move to post-quantum methods; some, such as the NSA CNSA 2.0 suite, plan pure ML-KEM in the end.
- **Theory.** Combiners for KEMs, signatures and encryption are studied as a general topic, since they answer the question of how to use a new primitive without trusting it fully.

## References
