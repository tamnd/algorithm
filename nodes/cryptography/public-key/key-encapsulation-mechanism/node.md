---
tag: ASVB4X
kind: abstract-type
slug: key-encapsulation-mechanism
name: Key encapsulation mechanism
aliases:
- KEM
area: cryptography/public-key
level: intro
summary: The public-key interface that makes a fresh random key and a ciphertext that carries it. Only the private key holder can recover the key. Hybrid encryption builds on it.
prereqs: [public-key-encryption]
see_also: [hybrid-encryption, ind-cca-security, fujisaki-okamoto-transform, crystals-kyber, ecies, rsa-cryptosystem, diffie-hellman, tls-handshake]
sources:
  - url: "https://eprint.iacr.org/2001/112"
    title: Victor Shoup, A proposal for an ISO standard for public key encryption, version 2.1, IACR Cryptology ePrint Archive 2001/112, 2001
    locator: the sections that define key encapsulation mechanisms, data encapsulation mechanisms and their security
  - paper: "Ronald Cramer and Victor Shoup, Design and analysis of practical public-key encryption schemes secure against adaptive chosen ciphertext attack, SIAM Journal on Computing 33(1), pages 167 to 226, 2003"
    locator: Section 7, key encapsulation and the hybrid construction
  - url: "https://www.iso.org/standard/37971.html"
    title: ISO/IEC 18033-2:2006, Information technology, Security techniques, Encryption algorithms, Part 2, Asymmetric ciphers
    locator: the KEM interface and the mechanisms RSA-KEM, ECIES-KEM, PSEC-KEM and ACE-KEM
  - url: "https://www.rfc-editor.org/rfc/rfc5990"
    title: RFC 5990, Use of the RSA-KEM Key Transport Algorithm in the Cryptographic Message Syntax (CMS), 2010
    locator: Section 1 and Appendix A, the RSA-KEM algorithm
  - url: "https://www.rfc-editor.org/rfc/rfc9180"
    title: RFC 9180, Hybrid Public Key Encryption, 2022
    locator: Section 4 (the KEM interface GenerateKeyPair, Encap, Decap) and Section 4.1 (DHKEM)
  - url: "https://doi.org/10.6028/NIST.FIPS.203"
    title: NIST FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard, 2024
    locator: Section 7, ML-KEM.KeyGen, ML-KEM.Encaps and ML-KEM.Decaps
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 12, the sections on hybrid encryption and the KEM/DEM paradigm
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 11 and Chapter 12, the sections on key encapsulation
---

A key encapsulation mechanism (KEM) is the public-key interface that does not encrypt a chosen message. Instead it makes a fresh random key $K$ together with a ciphertext $c$ that carries it, and only the holder of the private key can recover $K$ from $c$. The key then drives a symmetric cipher, as in [hybrid encryption](/hybrid-encryption/). Shoup named and defined KEMs in his 2001 ISO proposal, and almost every deployed public-key encryption today is a KEM: [RSA-KEM](/rsa-cryptosystem/), DHKEM in HPKE, [ECIES](/ecies/) and [ML-KEM](/crystals-kyber/).

**Notation.** $\lambda$ is the security parameter, $pk$ and $sk$ the public and private keys, $c$ the encapsulation (the KEM ciphertext), and $K \in \mathcal{K}$ the shared key, often a string of $\lambda$ or $2\lambda$ binary digits. $\mathcal{A}$ is an adversary that runs in time $t$ and makes $q_d$ decapsulation queries, and $\mathrm{Adv}$ is its advantage. $\bot$ is the rejection symbol.

## In plain words

A sender wants to share a secret key with a receiver over an open channel. The receiver has published a public key. The sender runs one operation on that public key. It gives the sender a fresh random key and a short message to send. The receiver runs one operation on that message with its private key and gets the same random key back.

An eavesdropper sees the public key and the message, and it cannot tell the key apart from a random one. The sender does not choose the key: it comes out of the operation. This is why a KEM is simpler to build than encryption of a chosen message. After the exchange, both sides use the key with a fast symmetric cipher to protect the data itself.

## Operations

A KEM is a triple of algorithms.

| operation | input | output | randomized |
|---|---|---|---|
| $\mathrm{KeyGen}()$ | the security parameter $\lambda$ | a key pair $(pk, sk)$ | yes |
| $\mathrm{Encaps}(pk)$ | a public key | a pair $(c, K)$ with $K \in \mathcal{K}$ | yes |
| $\mathrm{Decaps}(sk, c)$ | a private key and a ciphertext | a key $K \in \mathcal{K}$, or $\bot$ | no |

RFC 9180 calls the operations GenerateKeyPair, Encap and Decap, and adds DeriveKeyPair (keys from a seed) and the serialization of public keys. FIPS 203 calls them ML-KEM.KeyGen, ML-KEM.Encaps and ML-KEM.Decaps. A KEM has no "encrypt this message" operation. The data goes into a separate symmetric scheme, the data encapsulation mechanism (DEM).

## Laws

**Correctness.** For every $(pk, sk)$ from KeyGen, if $(c, K) \leftarrow \mathrm{Encaps}(pk)$ then $\mathrm{Decaps}(sk, c) = K$. Lattice KEMs such as ML-KEM satisfy this only with probability $1 - \delta$, where the failure probability $\delta$ is tiny and is part of the security analysis.

**IND-CPA security.** The challenger runs $(pk, sk) \leftarrow \mathrm{KeyGen}()$ and $(c^*, K_0) \leftarrow \mathrm{Encaps}(pk)$, draws $K_1$ uniform in $\mathcal{K}$ and a uniform bit $b$, and gives $(pk, c^*, K_b)$ to $\mathcal{A}$. The adversary outputs $b'$, and

$$\mathrm{Adv}^{\mathrm{kem\text{-}cpa}}(\mathcal{A}) = \bigl|\Pr[b' = 1 \mid b = 1] - \Pr[b' = 1 \mid b = 0]\bigr|.$$

The KEM is IND-CPA secure if this is negligible in $\lambda$ for every $\mathcal{A}$ that runs in polynomial time. Unlike [IND-CPA security](/ind-cpa-security/) for encryption, the adversary chooses no messages: the key is the message, and it must look uniform.

**IND-CCA security.** As above, and $\mathcal{A}$ may also ask a decapsulation oracle $\mathrm{Decaps}(sk, \cdot)$ on any $c \ne c^*$, at most $q_d$ times, before and after it sees $c^*$. This is the notion that [hybrid encryption](/hybrid-encryption/) needs, and it is the KEM form of [IND-CCA security](/ind-cca-security/). The exclusion of $c^*$ is the same as in the encryption game.

**Rejection.** Decaps may reject a bad ciphertext in two ways. Explicit rejection returns $\bot$. Implicit rejection returns a pseudorandom key such as $H(z, c)$ for a secret seed $z$, so the attacker learns nothing from the shape of the answer. ML-KEM uses implicit rejection; see the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/).

**Relations with public-key encryption.**

- *PKE to KEM.* If $(\mathrm{Enc}, \mathrm{Dec})$ is a public-key encryption scheme, then $\mathrm{Encaps}(pk)$: pick $K$ uniform, return $(\mathrm{Enc}_{pk}(K), K)$ is a KEM. It is IND-CPA or IND-CCA secure if the scheme is.
- *KEM to PKE.* A KEM together with a DEM gives public-key encryption of messages of any length. If the KEM is IND-CCA secure and the DEM is one-time IND-CCA secure, the result is IND-CCA secure. See [hybrid encryption](/hybrid-encryption/) for the theorem.
- *KEM from trapdoor functions and Diffie-Hellman.* Encapsulation can be simpler than encryption: RSA-KEM encrypts a random $r$ with raw RSA and sets $K = H(r)$, and DHKEM sends $g^r$ and sets $K = H(g^{xr})$. Neither needs padding, because the encapsulated value is random by construction.

**Key exchange.** A KEM gives a one-round key exchange: one side sends $pk$, the other answers with $c$. TLS 1.3 uses the key share of each side this way, and the hybrid groups of TLS 1.3 with ML-KEM treat both the elliptic curve [Diffie-Hellman](/diffie-hellman/) share and ML-KEM as KEMs. The exchange has no authentication of its own.

## Implementations

| KEM | hardness | security model | standard |
|---|---|---|---|
| RSA-KEM | RSA problem | random oracle model | ISO/IEC 18033-2, RFC 5990 |
| ECIES-KEM and DHKEM | gap or oracle Diffie-Hellman | random oracle model | ISO/IEC 18033-2, SEC 1, RFC 9180 |
| Cramer-Shoup KEM (ACE-KEM) | DDH | standard model | ISO/IEC 18033-2 |
| ML-KEM | module learning with errors | (quantum) random oracle model | FIPS 203 |
| FrodoKEM | learning with errors | (quantum) random oracle model | ISO proposal |

Pages: [ECIES](/ecies/) shows a full elliptic curve KEM with a DEM, [Cramer-Shoup](/cramer-shoup-cryptosystem/) the standard model scheme, [ML-KEM](/crystals-kyber/) and [FrodoKEM](/frodokem/) the post-quantum KEMs, and [the Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) the generic way to get an IND-CCA KEM from a weak encryption scheme. Hashed [ElGamal](/elgamal-encryption/) is the simplest DH-based KEM: $c = g^r$ and $K = H(h^r)$.

**Pitfalls in implementations.**

- An RSA-KEM must encrypt a uniform $r$ in $\{0, \ldots, n-1\}$ with no padding and hash it. Putting a key in PKCS #1 v1.5 padding instead gives the [padding oracle attack](/padding-oracle-attack/) of Bleichenbacher.
- A DH-based KEM must check that $c$ is a valid group element, or [small subgroup attacks](/small-subgroup-attack/) recover the private key. X25519-based DHKEM avoids most of these checks by design.
- Decaps must take the same time for valid and invalid ciphertexts. With implicit rejection, the comparison and the choice between the real and the pseudorandom key must be constant time.
- Bind the KEM ciphertext into the key derivation (DHKEM hashes $c$ and $pk$ with the shared value). Otherwise two ciphertexts can give the same key, as the ECIES page shows for the point $-U$.

## References
