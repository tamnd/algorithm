---
tag: 67AG3K
kind: concept
slug: signature-malleability
name: Signature malleability
aliases:
- transaction malleability
- ECDSA malleability
- low-s rule
area: cryptography/signatures
level: advanced
summary: Anyone can turn a valid signature into a different valid signature on the same message, as with ECDSA (r, s) to (r, n - s). It breaks systems that use signatures as identifiers.
prereqs: [strong-unforgeability, elliptic-curve-cryptography]
see_also: [ecdsa, ed25519, schnorr-signature, existential-unforgeability, rsa-signature, rsa-pss, rabin-signature, signature-forgery]
sources:
  - url: "https://github.com/bitcoin/bips/blob/master/bip-0062.mediawiki"
    title: Pieter Wuille, BIP 62, Dealing with malleability, 2014 (withdrawn)
    locator: the list of sources of malleability in Bitcoin transactions, including the inverted s of ECDSA and non-DER encodings, and the low-s rule
  - url: "https://github.com/bitcoin/bips/blob/master/bip-0066.mediawiki"
    title: Pieter Wuille, BIP 66, Strict DER signatures, 2015
    locator: the consensus rule that signatures must be in strict DER encoding
  - url: "https://github.com/bitcoin/bips/blob/master/bip-0146.mediawiki"
    title: Johnson Lau and Pieter Wuille, BIP 146, Dealing with signature encoding malleability, 2016
    locator: the LOW_S rule (s at most n/2) and the NULLFAIL rule
  - url: "https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki"
    title: Eric Lombrozo, Johnson Lau and Pieter Wuille, BIP 141, Segregated Witness (Consensus layer), 2015
    locator: the transaction identifier that no longer covers the witness data, which removes third-party malleability of the txid
  - url: "https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki"
    title: Pieter Wuille, Jonas Nick and Tim Ruffing, BIP 340, Schnorr Signatures for secp256k1, 2020
    locator: the design section, x-only R with an even y and the check s < n, and the claim of strong unforgeability
  - url: "https://eips.ethereum.org/EIPS/eip-2"
    title: Vitalik Buterin, EIP-2, Homestead Hard-fork Changes, 2015
    locator: transaction signatures with s greater than n/2 of secp256k1 are invalid
  - url: "https://www.rfc-editor.org/rfc/rfc8032"
    title: Simon Josefsson and Ilari Liusvaara, RFC 8032, Edwards-Curve Digital Signature Algorithm (EdDSA), January 2017
    locator: Section 5.1.7 (verification rejects S that is not below L) and Section 8.4 (signature malleability)
  - paper: "Christian Decker and Roger Wattenhofer, Bitcoin transaction malleability and MtGox, ESORICS 2014, LNCS 8713, pages 313 to 326"
    locator: the measurement of malleated transactions in the Bitcoin network around the Mt. Gox halt of February 2014
  - paper: "Jacqueline Brendel, Cas Cremers, Dennis Jackson and Mang Zhao, The provable security of Ed25519, theory and practice, IEEE Symposium on Security and Privacy 2021"
    locator: Ed25519 with the check S < L is strongly unforgeable; without it, only existentially unforgeable
  - paper: "Konstantinos Chalkias, François Garillot and Valeria Nikolaenko, Taming the many EdDSAs, Security Standardisation Research (SSR) 2020, LNCS 12529"
    locator: the differences between Ed25519 libraries in their validation rules, including the check on S
  - paper: "David Pointcheval and Olivier Sanders, Short randomizable signatures, CT-RSA 2016, LNCS 9610, pages 111 to 126"
    locator: signatures that anyone can rerandomize on purpose, for anonymous credentials
  - url: "https://www.secg.org/sec2-v2.pdf"
    title: Certicom Research, SEC 2, Recommended Elliptic Curve Domain Parameters, version 2.0, January 2010
    locator: Section 2.4.1, the parameters of secp256k1 used by the code
---

A signature scheme is malleable if someone without the private key can take a valid signature $\sigma$ on a message $m$ and compute a different string $\sigma' \ne \sigma$ that is also a valid signature on $m$. This is not a forgery in the sense of [existential unforgeability](/existential-unforgeability/), because the message is not new; it is exactly what [strong unforgeability](/strong-unforgeability/) forbids. It matters when a system treats a signature, or a hash that covers it, as a unique identifier. The best known case is ECDSA, where $(r, s)$ and $(r, n - s)$ are both valid, and the best known damage is to Bitcoin transaction identifiers before 2017.

**Notation.** For ECDSA, $G$ is a base point of prime order $n$, $d$ the private key, $Q = dG$ the public key, $z$ the hash value of the message, $k$ the nonce, $R = kG$, $r = x(R) \bmod n$, and $s = k^{-1}(z + r d) \bmod n$. For Ed25519, $L$ is the order of the base point and a signature is $(R, S)$. For RSA, $N$ is the modulus.

## In plain words

A signature is a string of bytes that proves who approved a message. With some schemes, anyone can change those bytes in a simple way and still have a valid signature for the same message. Nothing false gets signed, so in one sense nothing is broken.

Trouble starts when a system uses the exact bytes of a signature as a name for something. If a payment is identified by a fingerprint of its bytes, and the signature is part of those bytes, then a stranger can change the name of the payment while it is on its way. Someone who looks only at the old name will think the payment never happened.

The fix is to allow only one form of each signature, or to keep signatures out of the name.

## The idea

**Third-party malleability.** The concern is a party without $sk$ who sees $(m, \sigma)$ and outputs $(m, \sigma')$ with $\sigma' \ne \sigma$ and $\mathrm{Verify}(pk, m, \sigma') = 1$. Such a party wins the SUF-CMA game but not the EUF-CMA game. The signer itself can always make many signatures on one message if signing is randomized; that is not malleability, because it needs the key.

**Where it comes from.**

- **Algebraic symmetry.** ECDSA verification computes $X = u_1 G + u_2 Q$ with $u_1 = z s^{-1}$ and $u_2 = r s^{-1}$, and checks $x(X) \bmod n = r$. Replacing $s$ by $n - s = -s \bmod n$ negates $u_1$ and $u_2$, so $X$ becomes $-X$, which has the same $x$-coordinate. Hence $(r, n - s)$ is valid whenever $(r, s)$ is. Anyone can compute it.
- **Reduction without a range check.** If a verifier reduces a value modulo the group order instead of rejecting large values, then adding the order gives a second string. For Ed25519, $(R, S + L)$ passes a verifier that does not check $S < L$; for RSA, $s + N$ passes a verifier that does not check $s < N$.
- **Encoding.** If the verifier accepts several byte encodings of the same numbers, for example BER instead of strict DER for the pair $(r, s)$, or extra leading zeros, each encoding is a different signature string. OpenSSL accepted such encodings for years, which made Bitcoin signatures malleable in this way too.

**Removing it.** Each source has a matching rule: accept only one of $s$ and $n - s$ (the low-s rule), check every range, and accept only one encoding. A scheme is then strongly unforgeable if it is otherwise secure. Schemes with unique signatures, such as RSA with a deterministic encoding and a range check, or BLS with a canonical point encoding, have one signature per message and need no extra rule. Fiat-Shamir schemes in the style of [Schnorr](/schnorr-signature/) can be made strongly unforgeable by fixing the encoding of the commitment and checking the range of the response, as BIP 340 and RFC 8032 do.

## Examples

**ECDSA on a toy curve.** Take the curve $y^2 = x^3 + 7$ over $\mathbb{F}_{97}$, whose points form a group of prime order $n = 79$, with $G = (1, 28)$. The private key is $d = 11$, so $Q = 11G = (65, 5)$. Sign the hash value $z = 30$ with $k = 23$:

| step | computation | value |
|---|---|---|
| $R = kG$ | $23 \cdot (1, 28)$ | $(61, 28)$ |
| $r$ | $61 \bmod 79$ | 61 |
| $s$ | $k^{-1}(z + r d) = 55 \cdot 701 \bmod 79$ | 3 |
| verify $(61, 3)$ | $w = 53$, $u_1 = 10$, $u_2 = 73$, $u_1 G + u_2 Q$ | $(61, 28)$, valid |
| twin $(61, 76)$ | $w = 26$, $u_1 = 69$, $u_2 = 6$, $u_1 G + u_2 Q$ | $(61, 69) = -R$, valid |

Both signatures verify, and the second one was made from the first without $d$. Since $n$ is odd, exactly one of $s$ and $n - s$ is at most $\lfloor n/2 \rfloor = 39$; here $s = 3$ is the low one, and a verifier with the low-s rule accepts only $(61, 3)$.

**ECDSA on secp256k1.** The code of this page does the same on secp256k1, with its own affine curve arithmetic and the constants of SEC 2. For three messages it signs with a key from a fixed seed, checks that $(r, n - s)$ also verifies, that a toy transaction identifier which hashes the signature changes, that normalizing to low $s$ gives a signature that a BIP 146 verifier accepts, and that this verifier rejects the twin. It also checks every nonce on the toy curve. No official vector exists for malleated signatures. The code is for study only and is not constant time.

**Ed25519.** RFC 8032, Section 5.1.7, decodes $S$ and rejects the signature if $S \ge L$. With this check, Brendel, Cremers, Jackson and Zhao (2021) proved Ed25519 strongly unforgeable in the random oracle model; without it, $(R, S + L)$ is a second valid signature, since only $S \bmod L$ enters the group equation. Chalkias, Garillot and Nikolaenko (2020) found that libraries differ in this and other checks.

**RSA and RSA-PSS.** For [RSA signatures](/rsa-signature/) with PKCS #1 v1.5 or a full-domain hash, $x \mapsto x^e \bmod N$ is a permutation, so with the check $0 \le s < N$ and a fixed length of $k$ bytes each message has exactly one signature: there is nothing to malleate. [RSA-PSS](/rsa-pss/) has one valid signature per salt, so a message has many signatures, but making a new one requires inverting RSA on a new encoded value, which a party without the key cannot do; the random oracle proof of PSS covers this case. [Rabin-Williams signatures](/rabin-signature/) need a rule that picks one of $s$ and $N - s$.

**Malleable on purpose.** Some schemes let anyone rerandomize a signature so that two showings of the same credential cannot be linked, for example the signatures of Pointcheval and Sanders (2016). Here malleability is a feature, and protocols built on them must not use signatures as identifiers.

## Where it is used

**Bitcoin transaction identifiers.** Before segregated witness, the identifier of a Bitcoin transaction (txid) was the double SHA-256 hash of the whole transaction, signatures included. A relay node could replace $s$ by $n - s$, or change the DER encoding, and the transaction stayed valid with a new txid. If the new form was mined first, wallets that tracked payments by the old txid saw it as never confirmed, and chains of unconfirmed transactions that spent its outputs became invalid. BIP 62 (2014) listed the sources and proposed rules; it was withdrawn, but parts of it were adopted separately. BIP 66 (2015) made strict DER a consensus rule; BIP 146 (2016) defined LOW_S, which Bitcoin Core enforces as a policy for relaying transactions. BIP 141 (segregated witness, active since August 2017) computes the txid without the witness data, which removed third-party malleability for its transactions and made payment channels such as the Lightning Network practical. BIP 340 Schnorr signatures have one valid encoding by design.

**The Mt. Gox claim.** In February 2014 the Mt. Gox exchange stopped withdrawals and said that transaction malleability had let attackers change the txid of a withdrawal, claim that it had failed, and be paid again. The exchange later reported about 850,000 bitcoins missing and went bankrupt. Decker and Wattenhofer (ESORICS 2014) measured malleated transactions in the network and concluded that malleability attacks could explain only a small part of such a loss, and that most of the malleated transactions they saw appeared after the announcement of the halt. Malleability was a real weakness of how the exchange tracked withdrawals, but it has not been shown to be the cause of the loss.

**Ethereum.** EIP-2 (Homestead, 2016) made transaction signatures with $s > n/2$ invalid. The `ecrecover` precompile still accepts both values, so a contract that marks signatures as used, to stop replays, must store the signed message or a nonce and not the signature bytes, or must apply the low-s rule itself.

**Protocols that need a fixed signature.** Constructions of CCA-secure encryption from one-time signatures, signcryption, and any database or log that uses the hash of a signed object as a key need strong unforgeability. Using a malleable scheme there turns a harmless change into a replay or a collision of identifiers.

## References
