---
tag: GMRG0G
kind: concept
slug: digital-signature
name: Digital signature
aliases:
- Digital signature problem
- digital signatures
- message authentication with public verifiability
- public-key signature
area: cryptography/signatures
level: intro
summary: A digital signature lets the holder of a private key sign a message so that anyone with the public key can check who signed it and that it was not changed. Proposed by Diffie and Hellman in 1976.
prereqs: [public-key-cryptography, cryptographic-hash-function]
see_also: [signature-scheme, existential-unforgeability, message-authentication-code, rsa-signature, ecdsa, ed25519, hash-based-signatures, non-repudiation]
sources:
  - paper: "Whitfield Diffie and Martin E. Hellman, New directions in cryptography, IEEE Transactions on Information Theory IT-22(6), pages 644 to 654, November 1976"
    locator: Section 2 and Section 3, the proposal of public-key cryptosystems and of digital signatures that anyone can verify
  - paper: "Ronald L. Rivest, Adi Shamir and Leonard Adleman, A method for obtaining digital signatures and public-key cryptosystems, Communications of the ACM 21(2), pages 120 to 126, 1978"
    locator: the first concrete signature scheme, signing by applying the private RSA permutation
  - paper: "Leslie Lamport, Constructing digital signatures from a one way function, Technical Report CSL-98, SRI International, October 1979"
    locator: the one-time signature from any one-way function
  - paper: "Shafi Goldwasser, Silvio Micali and Ronald L. Rivest, A digital signature scheme secure against adaptive chosen-message attacks, SIAM Journal on Computing 17(2), pages 281 to 308, 1988"
    locator: the classification of attacks and forgeries, and the first scheme proved secure against adaptive chosen-message attacks
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, 2020
    locator: Chapter 13, Digital Signature Schemes
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 11, Digital Signatures
---

A digital signature is a short string that the holder of a private key computes from a message, and that anyone who has the matching public key can check. A valid signature shows that the message comes from the key holder and that nobody changed it after signing. Because the checking key is public, any third party can repeat the check, which is the base of [non-repudiation](/non-repudiation/). Diffie and Hellman proposed digital signatures in 1976 as one of the two goals of [public-key cryptography](/public-key-cryptography/); the [RSA](/rsa-signature/) paper of 1978 gave the first concrete scheme.

**Notation.** $\lambda$ is the security parameter. A [signature scheme](/signature-scheme/) is a triple $(\mathrm{KeyGen}, \mathrm{Sign}, \mathrm{Verify})$: $\mathrm{KeyGen}(1^\lambda)$ outputs a key pair $(pk, sk)$, $\mathrm{Sign}(sk, m)$ outputs a signature $\sigma$, and $\mathrm{Verify}(pk, m, \sigma)$ outputs 1 (accept) or 0 (reject). $A$ is an adversary, $t$ its running time and $q_s$ its number of signing queries. $H$ is a [cryptographic hash function](/cryptographic-hash-function/). For RSA, $N = pq$ is the modulus and $e$, $d$ the public and private exponents.

## In plain words

A handwritten signature ties a person to a paper. A digital signature does the same for a file, but it uses two keys. The signer keeps one key secret and uses it to make a signature for the file. Everyone else gets the other key, the public key, and uses it to check the signature.

Only the person with the secret key can make a signature that passes the check. If someone changes even one character of the file, the old signature fails. So a passing check tells you two things: who signed, and that the file is the one they signed. Because anyone can run the check, the signer cannot later claim that the receiver made the signature up. This is the main difference from a shared-secret code, which both sides can compute.

## The idea

**What a signature gives.**

- **Authenticity.** A valid signature under $pk$ shows that the holder of $sk$ signed the message. This needs [existential unforgeability](/existential-unforgeability/): an adversary that sees signatures on messages of its choice still cannot produce a valid signature on any new message.
- **Integrity.** A change to the message makes the signature invalid, except with negligible probability. Integrity is part of the same unforgeability notion, because a valid signature on a changed message is a forgery.
- **Public verifiability and non-repudiation.** The verification key is public, so a judge, an auditor or a later reader can check a signature without any secret. The signer cannot deny a valid signature unless its key was stolen; see [non-repudiation](/non-repudiation/) for the limits.

**Signature or MAC.** A [message authentication code](/message-authentication-code/) also gives authenticity and integrity, but the sender and the receiver share the same key. Each of them can compute every tag, so a tag does not prove to a third party which of them made it, and only a key holder can check it. A signature separates the key that signs from the key that verifies. The cost is speed and size: an HMAC tag takes microseconds, while an RSA-2048 signature takes a modular exponentiation with a 2048-bit exponent.

**How schemes are built.** Almost every deployed scheme follows the [hash-and-sign paradigm](/hash-and-sign-paradigm/): it signs $H(m)$ and not $m$, so that it can sign long messages and so that the algebra of the underlying problem cannot be used to forge. There are four main families.

- **Trapdoor permutations.** The signer inverts a [trapdoor one-way function](/trapdoor-one-way-function/) on an encoding of $H(m)$: [RSA signatures](/rsa-signature/) with PKCS #1 v1.5 padding, [RSA-FDH](/rsa-fdh/), [RSA-PSS](/rsa-pss/), and [Rabin signatures](/rabin-signature/) with square roots modulo $N$.
- **Discrete logarithm schemes.** The signer proves knowledge of $x$ with $y = g^x$ through a random nonce $k$: [ElGamal](/elgamal-signature/), [DSA](/dsa/), [Schnorr](/schnorr-signature/), [ECDSA](/ecdsa/) and [Ed25519](/ed25519/).
- **Pairing schemes.** [BLS signatures](/bls-signature/) are short and can be aggregated.
- **Hash-based schemes.** Built from a hash function alone: the [Lamport one-time signature](/lamport-signature/), [Winternitz](/winternitz-one-time-signature/), [XMSS](/xmss/) and [SPHINCS+](/sphincs-plus/); see [hash-based signatures](/hash-based-signatures/). They are believed to resist quantum computers.

**History.** Diffie and Hellman (1976) defined the goal: a signature that anyone can verify but only one party can produce. They did not give a scheme. Rivest, Shamir and Adleman (1978) gave the first one: sign by applying the private RSA permutation. Rabin (1979) gave a scheme as hard to break as factoring, and Lamport (1979) a one-time signature from any one-way function. Goldwasser, Micali and Rivest (1988) gave the first exact definition of security, existential unforgeability under adaptive chosen-message attack, and the first scheme proved to meet it. Naor and Yung (1989) and Rompel (1990) showed that signatures exist if [one-way functions](/one-way-function/) exist.

**A map of this folder.**

- Definitions and models: [signature scheme](/signature-scheme/), [existential unforgeability](/existential-unforgeability/) (EUF-CMA), [strong unforgeability](/strong-unforgeability/) (SUF-CMA), [chosen-message attack](/chosen-message-attack/), [key-only attack](/key-only-attack/), [signature forgery](/signature-forgery/), [non-repudiation](/non-repudiation/) and [signature malleability](/signature-malleability/).
- Design: [hash-and-sign](/hash-and-sign-paradigm/), the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/), the [forking lemma](/forking-lemma/) and [deterministic nonce generation](/deterministic-nonce-generation/).
- RSA and factoring: [RSA signature](/rsa-signature/), [RSA-FDH](/rsa-fdh/), [RSA-PSS](/rsa-pss/) and [Rabin signature](/rabin-signature/).
- Discrete logarithms: [ElGamal signature](/elgamal-signature/), [DSA](/dsa/), [Schnorr signature](/schnorr-signature/), [ECDSA](/ecdsa/), [Ed25519](/ed25519/) and the [nonce reuse attack](/nonce-reuse-attack/).
- Many signers and short signatures: [BLS](/bls-signature/), [aggregate](/aggregate-signature/), [batch verification](/batch-verification/), [MuSig](/musig/), [threshold](/threshold-signature/) and [adaptor](/adaptor-signature/) signatures.
- Hash-based: [Lamport](/lamport-signature/), [Winternitz](/winternitz-one-time-signature/), [Merkle](/merkle-signature-scheme/), [LMS](/leighton-micali-signature/), [XMSS](/xmss/) and [SPHINCS+](/sphincs-plus/).
- Special properties: [blind](/blind-signature/), [group](/group-signature/), [ring](/ring-signature/), [proxy](/proxy-signature/), [undeniable](/undeniable-signature/), [designated verifier](/designated-verifier-signature/) and [forward-secure](/forward-secure-signature/) signatures, and [signcryption](/signcryption/).

## Examples

- **RSA with PKCS #1 v1.5.** The key is $(N, e)$ with a 2048-bit $N$. The signer pads the SHA-256 hash of the message to 256 bytes and computes $s = m^d \bmod N$. The verifier computes $s^e \bmod N$ and compares it with the padded hash. The signature has 256 bytes. See [RSA signature](/rsa-signature/).
- **Ed25519.** A public key of 32 bytes, a signature of 64 bytes, and no random number at signing time, because the nonce is a hash of the key and the message. See [Ed25519](/ed25519/).
- **A non-example: textbook RSA.** Signing $m$ directly as $m^d \bmod N$ is not secure: from signatures on $m_1$ and $m_2$ anyone gets the signature $s_1 s_2 \bmod N$ on $m_1 m_2 \bmod N$. See [chosen-message attack](/chosen-message-attack/).
- **A non-example: a MAC.** HMAC gives integrity and authenticity between two parties who share a key, but no public verification and no non-repudiation.

## Where it is used

- **Certificates.** A certificate authority signs a certificate that binds a name to a public key, and browsers check chains of such signatures. The MD5 and SHA-1 collision attacks on certificates show why the hash inside the signature matters ([chosen-prefix collision](/chosen-prefix-collision/)).
- **TLS.** In the [TLS handshake](/tls-handshake/) the server signs the handshake transcript with the key in its certificate, which authenticates the [Diffie-Hellman](/diffie-hellman/) key exchange.
- **Code signing and software updates.** Operating systems, app stores and package managers check a signature before they install code.
- **Blockchains.** A Bitcoin transaction is valid only with a signature by the owner of the coins: ECDSA on the curve secp256k1, and Schnorr signatures since the Taproot upgrade. Here [malleability](/signature-malleability/) has had real effects.
- **Distributed agreement.** Byzantine fault tolerant protocols such as [PBFT](/pbft/) and the [Dolev-Strong algorithm](/dolev-strong-algorithm/) rely on [signed messages](/signed-messages-model/), and a [quorum certificate](/quorum-certificate/) is a set of signatures.
- **Documents and law.** Electronic signature laws such as the EU eIDAS regulation give legal effect to signed documents; see [non-repudiation](/non-repudiation/).

## References
