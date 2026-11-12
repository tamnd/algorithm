---
tag: 883YSK
kind: problem
slug: key-transport-problem
name: Key transport problem
area: cryptography/key-exchange
level: intro
summary: One party chooses a secret key and sends it to another party over an open channel, so that only the intended receiver can recover it.
prereqs: [key-agreement-problem, public-key-encryption]
see_also: [key-agreement-problem, key-distribution-problem, session-key, key-encapsulation-mechanism, rsa-oaep, hybrid-encryption, kerberos, shamir-three-pass-protocol]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 12, Definition 12.3 (key transport), Section 12.3 (key transport based on symmetric encryption) and Section 12.5 (key transport based on public-key encryption, Table 12.3)
  - paper: doi:10.6028/NIST.SP.800-56Br2
    title: Elaine Barker, Lily Chen, Allen Roginsky, Apostol Vassilev, Richard Davis and Scott Simon, NIST SP 800-56B Rev. 2, Recommendation for Pair-Wise Key Establishment Using Integer Factorization Cryptography, March 2019
    locator: the definitions of key agreement and key transport, and the KTS-OAEP key-transport scheme
  - paper: doi:10.1007/BFb0055716
    title: "Daniel Bleichenbacher, Chosen ciphertext attacks against protocols based on the RSA encryption standard PKCS #1, CRYPTO 1998, LNCS 1462, pages 1 to 12"
    locator: "the attack on the PKCS #1 v1.5 padding in SSL 3.0 key transport"
  - url: "https://www.rfc-editor.org/rfc/rfc5246"
    title: Tim Dierks and Eric Rescorla, RFC 5246, The Transport Layer Security (TLS) Protocol Version 1.2, August 2008
    locator: Section 7.4.7.1 (RSA-encrypted premaster secret message)
  - url: "https://www.rfc-editor.org/rfc/rfc8446"
    title: Eric Rescorla, RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3, August 2018
    locator: Section 1.2 (static RSA cipher suites removed, so that all public-key key exchange gives forward secrecy)
  - book: isbn:9783662581452
    title: Colin Boyd, Anish Mathuria and Douglas Stebila, Protocols for Authentication and Key Establishment, second edition, Springer, 2020
    locator: Chapter 1 (key transport and key agreement) and the chapters on server-based and public-key key transport
---

The key transport problem asks one party to choose a secret key and deliver it to another party over a channel that an adversary can read, so that only the intended receiver learns the key. The sender alone fixes the key; this separates it from [key agreement](/key-agreement-problem/), where both parties contribute. The usual tools are [public-key encryption](/public-key-encryption/) (for example [RSA-OAEP](/rsa-oaep/)), a [key encapsulation mechanism](/key-encapsulation-mechanism/), or a trusted server that shares a long-term key with each party, as in [Kerberos](/kerberos/).

**Notation.** $A$ is the sender and $B$ the receiver. $K$ is the transported key, a string of $n$ binary digits. $(pk_B, sk_B)$ is a key pair of $B$ for public-key encryption, with encryption $\mathrm{Enc}$ and decryption $\mathrm{Dec}$. $K_{AS}$ and $K_{BS}$ are long-term symmetric keys that $A$ and $B$ share with a server $S$. $\mathcal{A}$ is an adversary.

## In plain words

One person picks a secret key and must get it to a second person. The only path between them is open, so anyone can read what goes along it.

The answer is to lock the key before it is sent. If the second person has published an open lock (a public key), the first person locks the key with it, and only the second person can open it. If there is no public key, a trusted helper who already shares a secret with each person can carry the key for them.

Only the sender chooses the key. If the receiver's secret is stolen later, an attacker who kept the old messages can open them all.

## Definition

**Input.** The sender $A$ holds a fresh key $K$, uniform in $\{0,1\}^n$. Before the run, $A$ holds some authentic data about $B$: a public key $pk_B$ (public-key key transport), or a key shared with a server (server-based key transport).

**Output.** $B$ outputs $K' = K$, except with negligible probability.

**Secrecy.** Given all messages of the run, an efficient adversary cannot tell $K$ from a uniform random string with a non-negligible advantage. HAC (Definition 12.3) states the problem in words: one party creates or otherwise obtains a secret value and securely transfers it to the other. NIST SP 800-56B Rev. 2 uses the same split: in key transport the key is chosen by the sender; in key agreement it is a function of contributions from both.

**Authentication goals.** One-pass encryption to $pk_B$ gives implicit key authentication to $A$: only $B$ can decrypt. It gives $B$ no assurance about who sent the key (HAC, Section 12.5). Signatures, a reply from $B$, or a trusted server add these assurances; see [authenticated key exchange](/authenticated-key-exchange/) and [key confirmation](/key-confirmation/).

## Variants

- **Public-key key transport.** $A$ sends $\mathrm{Enc}_{pk_B}(K)$. Signed variants (HAC, Section 12.5.2) add $A$'s signature, and X.509 two-pass and three-pass protocols add mutual entity authentication.
- **KEM-based.** $A$ runs $(c, K) \leftarrow \mathrm{Encaps}(pk_B)$ and sends $c$; $B$ runs $K = \mathrm{Decaps}(sk_B, c)$. The key is fixed by $A$'s random coins and $pk_B$ ([KEM](/key-encapsulation-mechanism/)).
- **Server-based.** A trusted server $S$ makes $K$ and sends it to $A$ and $B$, encrypted under $K_{AS}$ and $K_{BS}$: [Needham-Schroeder](/needham-schroeder-protocol/), [Otway-Rees](/otway-rees-protocol/), [Kerberos](/kerberos/), [wide-mouthed frog](/wide-mouthed-frog-protocol/). This is the [key distribution problem](/key-distribution-problem/) with a center.
- **Symmetric without a server.** $A$ sends $E_{K_{AB}}(K)$ under a long-term key $K_{AB}$ that the two already share (HAC, Section 12.3.1). Key wrapping, such as the AES key wrap of RFC 3394, is the same idea for stored keys.
- **No prior keys at all.** [Shamir's three-pass protocol](/shamir-three-pass-protocol/) moves a key with commutative locks and no prior shared data. It resists only passive adversaries.

## Examples

**TLS 1.2 RSA key exchange.** The client picks a 48-byte premaster secret (2 bytes of protocol version and 46 random bytes), encrypts it under the server's RSA public key with PKCS #1 v1.5 padding, and sends the result (RFC 5246, Section 7.4.7.1). The server decrypts it. Both then derive the session keys from the premaster secret and the two hello nonces. The server contributes only a public nonce, so the secret part of the key is the client's choice alone.

**Kerberos.** The key distribution center picks a session key for a client and a service, encrypts one copy under the client's long-term key, and puts the other copy in a ticket encrypted under the service's long-term key. Neither the client nor the service has any influence on the key.

**Non-example: Diffie-Hellman.** In [Diffie-Hellman](/diffie-hellman/) the key $g^{ab}$ depends on the secret values of both parties, so it is key agreement.

## Known algorithms

- [RSA-OAEP](/rsa-oaep/) encryption of a random key, which is the KTS-OAEP scheme of SP 800-56B Rev. 2. The older [PKCS #1 v1.5 encryption](/rsa-pkcs1-v1-5-encryption/) is still common but has padding-oracle attacks.
- [ECIES](/ecies/), [ElGamal](/elgamal-encryption/) and [hybrid encryption](/hybrid-encryption/) in general, and KEMs such as RSA-KEM, DHKEM and [ML-KEM](/crystals-kyber/).
- Server-based protocols: [Needham-Schroeder](/needham-schroeder-protocol/), [Otway-Rees](/otway-rees-protocol/), [Yahalom](/yahalom-protocol/), [Denning-Sacco](/denning-sacco-protocol/), [Kerberos](/kerberos/).
- [Shamir's three-pass protocol](/shamir-three-pass-protocol/) for the case with no prior keys.

## Bounds

**One message is enough.** If $A$ already holds an authentic $pk_B$, a single ciphertext transports $K$. Key agreement with fresh randomness from both parties needs at least one message in each direction, unless one side uses a static key.

**No forward secrecy with a static receiver key.** Suppose $B$ uses the same $sk_B$ for many runs, and an adversary records the ciphertext $c = \mathrm{Enc}_{pk_B}(K)$. If $sk_B$ leaks at any later time, the adversary computes $\mathrm{Dec}_{sk_B}(c) = K$. Correctness of the scheme forces this: $\mathrm{Dec}_{sk_B}$ must return $K$ on every honest ciphertext, so whoever holds $sk_B$ recovers every key ever sent to $B$. Forward secrecy needs a fresh receiver key for each session, which is what ephemeral Diffie-Hellman and ephemeral KEM keys give. This is why TLS 1.3 removed static RSA key transport (RFC 8446, Section 1.2).

**Security notion needed.** Against a passive adversary, IND-CPA security of the encryption is enough. When the receiver acts on decryption results that an attacker can observe, IND-CCA security is needed: Bleichenbacher (CRYPTO 1998) recovered SSL premaster secrets with about a million queries to a server that reported whether the PKCS #1 v1.5 padding was valid ([padding oracle attack](/padding-oracle-attack/)).

## Reductions

- **From public-key encryption.** Any IND-CPA public-key encryption scheme gives one-message key transport secure against eavesdroppers: send $\mathrm{Enc}_{pk_B}(K)$. A KEM is exactly key transport in which the scheme picks $K$.
- **To key agreement.** Two key transports, one in each direction, give key agreement: $A$ sends $K_1$ to $B$, $B$ sends $K_2$ to $A$, and both use $\mathrm{KDF}(K_1, K_2)$. Each party now contributes. Many authenticated protocols combine transported keys in this way.
- **Key agreement to key transport.** A two-message key agreement gives public-key encryption (the first message is the public key), and so key transport. Diffie-Hellman gives ElGamal in this way.

## Applications

- E-mail and file encryption: S/MIME and the Cryptographic Message Syntax (RFC 5652) encrypt a content key to each recipient's public key; OpenPGP does the same with a session key.
- TLS up to version 1.2 with RSA key exchange, now removed in TLS 1.3.
- Kerberos and other enterprise single sign-on systems, with server-based key transport.
- Key management systems and hardware security modules, which wrap keys under key-encryption keys before they store or move them.

## References
