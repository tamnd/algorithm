---
tag: TM5HTG
kind: technique
slug: hybrid-encryption
name: Hybrid encryption
aliases:
- KEM-DEM
area: cryptography/public-key
level: core
summary: Encrypt the data with a symmetric cipher under a fresh key, and send that key with a public-key KEM. IND-CCA KEM plus one-time IND-CCA DEM gives IND-CCA encryption.
prereqs: [key-encapsulation-mechanism, ind-cca-security, authenticated-encryption]
see_also: [ecies, rsa-oaep, padding-oracle-attack, gcm-mode, tls-handshake, crystals-kyber, chosen-ciphertext-attack, fujisaki-okamoto-transform]
sources:
  - paper: "Ronald Cramer and Victor Shoup, Design and analysis of practical public-key encryption schemes secure against adaptive chosen ciphertext attack, SIAM Journal on Computing 33(1), pages 167 to 226, 2003"
    locator: Section 7, key encapsulation, data encapsulation and the hybrid theorem
  - url: "https://eprint.iacr.org/2001/112"
    title: Victor Shoup, A proposal for an ISO standard for public key encryption, version 2.1, IACR Cryptology ePrint Archive 2001/112, 2001
    locator: the hybrid construction from a KEM and a DEM
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 12, the section on hybrid encryption and the KEM/DEM paradigm
  - url: "https://www.rfc-editor.org/rfc/rfc9180"
    title: RFC 9180, Hybrid Public Key Encryption, 2022
    locator: Sections 4 and 5, the KEM, the key schedule and the AEAD
  - url: "https://www.rfc-editor.org/rfc/rfc4880"
    title: RFC 4880, OpenPGP Message Format, 2007
    locator: Section 5.1, Public-Key Encrypted Session Key Packets
  - url: "https://www.rfc-editor.org/rfc/rfc5246"
    title: RFC 5246, The Transport Layer Security (TLS) Protocol Version 1.2, 2008
    locator: Section 7.4.7.1, RSA-Encrypted Premaster Secret Message
  - url: "https://www.rfc-editor.org/rfc/rfc8446"
    title: RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3, 2018
    locator: Section 1.2, the removal of static RSA and Diffie-Hellman cipher suites
  - paper: "Kaoru Kurosawa and Yvo Desmedt, A new paradigm of hybrid encryption scheme, CRYPTO 2004, LNCS 3152, pages 426 to 442"
    locator: hybrid encryption that is IND-CCA with a KEM that is not IND-CCA
  - paper: "Masayuki Abe, Rosario Gennaro and Kaoru Kurosawa, Tag-KEM/DEM, a new framework for hybrid encryption, Journal of Cryptology 21(1), pages 97 to 130, 2008"
    locator: the Tag-KEM generalization
---

Hybrid encryption encrypts a message with a fast symmetric cipher under a fresh random key, and sends that key with a public-key scheme. In the modern form, a [key encapsulation mechanism](/key-encapsulation-mechanism/) (KEM) makes the key and its ciphertext, and a data encapsulation mechanism (DEM), usually [authenticated encryption](/authenticated-encryption/), encrypts the data. Cramer and Shoup proved that an [IND-CCA](/ind-cca-security/) KEM and a one-time IND-CCA DEM give an IND-CCA public-key encryption scheme, with a tight bound. Almost every system that encrypts data to a public key works this way: OpenPGP, S/MIME, [ECIES](/ecies/) and HPKE (RFC 9180).

**Notation.** $\lambda$ is the security parameter. $(c_0, K) \leftarrow \mathrm{Encaps}(pk)$ is the KEM, $c_1 \leftarrow \mathrm{Enc}_K(m)$ and $\mathrm{Dec}_K(c_1)$ the DEM. $\mathcal{A}$ is an adversary against the hybrid scheme that runs in time $t$ and makes $q_d$ decryption queries, and $\mathrm{Adv}$ is an advantage of the form $|\Pr[b' = 1 \mid b = 1] - \Pr[b' = 1 \mid b = 0]|$. The theorem below is in the standard model; the security of a given KEM may need the [random oracle model](/random-oracle-model/).

## In plain words

Public-key operations are slow and handle only short inputs. Symmetric ciphers are fast and handle data of any length, but both sides need the same key. Hybrid encryption uses each for what it does well.

The sender makes a fresh random key and uses it once, with a symmetric cipher, to encrypt the data. It then uses the receiver's public key to send that short key in a locked form. The receiver unlocks the key with its private key and decrypts the data. The modern form lets the public-key part make the random key itself, so the sender never needs to choose or pad it. If both parts resist active attackers, the whole does too.

## When it applies

- The message is long, or its length is not fixed in advance.
- The public-key scheme can only carry short values, or only random values (a KEM).
- The receiver is offline, so an interactive key exchange is not possible. With an online receiver, the same structure appears as an authenticated key exchange followed by a secure channel.
- Many recipients: encapsulate one data key to each recipient, and encrypt the data once.

## The template

```pseudo id=main
HYBRID-ENCRYPT(pk, m)
L1  (c0, K) ← KEM.Encaps(pk)            ▷ fresh key K and its encapsulation c0
L2  c1 ← DEM.Enc(K, m)                  ▷ authenticated encryption, key used once
L3  return (c0, c1)

HYBRID-DECRYPT(sk, (c0, c1))
L4  K ← KEM.Decaps(sk, c0)
L5  if K = ⊥ then return ⊥
L6  return DEM.Dec(K, c1)               ▷ ⊥ if the authentication check fails
```

The DEM key is used for one message only, so the DEM may use a fixed nonce, and it needs only one-time security. With a public-key encryption scheme in place of a KEM, line L1 becomes "choose $K$ uniform, $c_0 \leftarrow \mathrm{PKE.Enc}(pk, K)$". This is the older "key transport" form.

### The composition theorem

**Theorem (Cramer and Shoup, 2003).** For every IND-CCA adversary $\mathcal{A}$ against the hybrid scheme there are a KEM adversary $\mathcal{B}_1$ and a one-time DEM adversary $\mathcal{B}_2$, each running in about the time of $\mathcal{A}$, with

$$\mathrm{Adv}^{\mathrm{pke\text{-}cca}}(\mathcal{A}) \le 2\,\mathrm{Adv}^{\mathrm{kem\text{-}cca}}(\mathcal{B}_1) + \mathrm{Adv}^{\mathrm{dem\text{-}ot\text{-}cca}}(\mathcal{B}_2).$$

$\mathcal{B}_1$ makes at most $q_d$ decapsulation queries and $\mathcal{B}_2$ at most $q_d$ decryption queries. The reduction is tight.

*Proof sketch.* Let Game 0 be the IND-CCA game for the hybrid scheme with challenge $(c_0^*, c_1^*)$, where $(c_0^*, K^*) \leftarrow \mathrm{Encaps}(pk)$. In Game 1, replace $K^*$ by an independent uniform key $K'$, both in the challenge and in the answers to decryption queries $(c_0^*, c_1)$ with $c_1 \ne c_1^*$.

*Game 0 to Game 1.* Fix the challenge bit $b$. $\mathcal{B}_1$ gets $(pk, c_0^*, K_\beta)$ from the KEM game, makes $c_1^* = \mathrm{Enc}_{K_\beta}(m_b)$, answers a query $(c_0, c_1)$ with $c_0 \ne c_0^*$ by its own decapsulation oracle, and a query $(c_0^*, c_1)$ with $\mathrm{Dec}_{K_\beta}(c_1)$. If $K_\beta = K^*$ this is Game 0, and if $K_\beta$ is random it is Game 1. So the output distributions of $\mathcal{A}$ in the two games differ by at most $\mathrm{Adv}^{\mathrm{kem\text{-}cca}}(\mathcal{B}_1)$, once for $b = 0$ and once for $b = 1$. This gives the factor 2.

*Game 1.* The key $K'$ is independent of everything else and is used for one encryption, $c_1^* = \mathrm{Enc}_{K'}(m_b)$, and for decryption queries on other $c_1$. That is exactly the one-time IND-CCA game of the DEM, so $\mathcal{A}$'s advantage in Game 1 is at most $\mathrm{Adv}^{\mathrm{dem\text{-}ot\text{-}cca}}(\mathcal{B}_2)$. $\square$

Weaker parts give a weaker result: an IND-CPA KEM and a one-time IND-CPA DEM (for example AES-CTR with a fixed nonce) give an IND-CPA scheme, by the same proof without decryption queries.

## Classic examples

- **OpenPGP.** A message is encrypted with a symmetric cipher under a random session key, and a Public-Key Encrypted Session Key packet carries the key to each recipient, encrypted with [RSA PKCS #1 v1.5](/rsa-pkcs1-v1-5-encryption/) or [ElGamal](/elgamal-encryption/) (RFC 4880, Section 5.1). The data part was not authenticated by default for years, which made the EFAIL attacks of 2018 possible; RFC 9580 (2024) adds AEAD packets.
- **TLS RSA key transport.** In TLS 1.2 and earlier, the client encrypts a random premaster secret with the server's RSA key using PKCS #1 v1.5 (RFC 5246, Section 7.4.7.1), and the record layer then uses keys derived from it. This was the target of Bleichenbacher's attack and its revival as ROBOT in 2017. TLS 1.3 (RFC 8446) removed static RSA key transport: every handshake uses ephemeral Diffie-Hellman, which is a KEM used for key exchange.
- **HPKE (RFC 9180).** A standard KEM-DEM scheme: a KEM (DHKEM over P-256, X25519 or others), a key schedule built on [HKDF](/hkdf/), and an AEAD such as [AES-GCM](/gcm-mode/). It is used by Messaging Layer Security (RFC 9420) and by TLS Encrypted Client Hello.
- **[ECIES](/ecies/).** Elliptic curve Diffie-Hellman as the KEM, a KDF, and a stream cipher with a MAC as the DEM.
- **Post-quantum encryption.** [ML-KEM](/crystals-kyber/) or [FrodoKEM](/frodokem/) as the KEM with AES-GCM as the DEM; hybrid HPKE and TLS 1.3 key shares combine a classical and a post-quantum KEM.

## Variations

- **Key transport.** A public-key encryption scheme encrypts a symmetric key chosen by the sender, as in PKCS #1 based systems. It is a special case: a PKE gives a KEM by encrypting a random key.
- **Tag-KEM/DEM.** Abe, Gennaro and Kurosawa let the KEM see a tag, usually the DEM ciphertext, before it fixes the key. This allows secure schemes from a KEM that is not IND-CCA on its own.
- **Kurosawa-Desmedt.** A variant of [Cramer-Shoup](/cramer-shoup-cryptosystem/) whose KEM is not IND-CCA, but whose hybrid with an authenticated DEM is IND-CCA under DDH. It shows that the theorem gives sufficient, not necessary, conditions.
- **Authenticated modes.** HPKE has modes in which the sender also proves its identity with a static key or a pre-shared key. Plain hybrid encryption is anonymous: anyone can encrypt to the public key.
- **Multi-recipient.** One DEM ciphertext, one KEM ciphertext per recipient. Randomness reuse across recipients needs care.

## Pitfalls

- **A weak DEM breaks CCA security.** If the DEM is not authenticated, an attacker flips bits of $c_1$ and asks for decryption; the answer reveals the message. A stronger KEM does not help. Use an AEAD or encrypt-then-MAC.
- **A padding oracle in the KEM.** RSA PKCS #1 v1.5 key transport, with a server that reacts differently to bad padding, gives a [padding oracle attack](/padding-oracle-attack/) on the session key. Use RSA-KEM, [RSA-OAEP](/rsa-oaep/) or an elliptic curve KEM.
- **Distinguishable errors.** If decryption reports whether the KEM or the DEM failed, or takes different time for each, the attacker gets an oracle that the proof does not allow. Return one error, in constant time.
- **Reused encapsulation.** If $c_0$ and $K$ are reused for a second message, the DEM key is no longer one-time, and a fixed nonce then breaks confidentiality. Run Encaps again for every message.
- **Unbound context.** The DEM should authenticate the KEM ciphertext and any context (HPKE does this in its key schedule). Otherwise an attacker may combine parts of different ciphertexts, as in the $-U$ case of ECIES.
- **Length leakage.** The hybrid ciphertext reveals the message length, like any encryption scheme. Pad the message if the length matters.

## Exercises

1. Let the DEM be AES-CTR with a fixed nonce and no MAC, and the KEM be IND-CCA. Give an IND-CCA attack on the hybrid scheme with one decryption query. *Hint:* flip the first bit of $c_1^*$.
2. Prove that a public-key scheme that is IND-CCA gives an IND-CCA KEM by $\mathrm{Encaps}(pk) = (\mathrm{Enc}_{pk}(K), K)$ for uniform $K$. Where is the restriction $c \ne c^*$ used?
3. Show that if the DEM is one-time IND-CPA and the KEM is IND-CPA, the hybrid scheme is IND-CPA, with $\mathrm{Adv} \le 2\,\mathrm{Adv}^{\mathrm{kem\text{-}cpa}} + \mathrm{Adv}^{\mathrm{dem\text{-}ot}}$.

## References
