---
tag: YNGHPQ
kind: concept
slug: crypto-agility
name: Cryptographic agility
aliases:
- algorithm agility
area: cryptography/post-quantum
level: intro
summary: "Designing protocols and systems so that algorithms can be added, preferred or removed by policy, with identifiers, negotiation that resists downgrade, and an inventory."
prereqs: [post-quantum-cryptography, tls-handshake]
see_also: [hybrid-key-exchange, harvest-now-decrypt-later, nist-pqc-standardization, nist-security-levels, key-encapsulation-mechanism, crystals-kyber, crystals-dilithium, sphincs-plus]
sources:
  - url: "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.39-upd1.pdf"
    title: "Elaine Barker, Lily Chen, David Cooper, Dustin Moody, Andrew Regenscheid, Murugiah Souppaya, Bill Newhouse, Russ Housley, Sean Turner, William Barker and Karen Kent, NIST CSWP 39-upd1, Considerations for Achieving Crypto Agility: Strategies and Practices, June 29, 2026"
    locator: Section 3 (crypto agility for security protocols), Section 5 (the strategic plan with governance, inventory, risk assessment and migration) and Section 6 (agility-aware design); the first final version is CSWP 39 of December 2025, now marked withdrawn
  - url: "https://www.rfc-editor.org/rfc/rfc7696"
    title: "Russ Housley, RFC 7696 (BCP 201), Guidelines for Cryptographic Algorithm Agility and Selecting Mandatory-to-Implement Algorithms, November 2015"
    locator: Section 2.1 (algorithm identifiers), Section 2.2 (mandatory-to-implement algorithms), Section 2.4 (balancing security strength) and Section 3 (downgrade and the cost of agility)
  - url: "https://www.rfc-editor.org/rfc/rfc8446"
    title: "Eric Rescorla, RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3, 2018"
    locator: Section 4.1.1 (negotiation of groups and signature algorithms), Section 4.1.3 (the downgrade sentinel in ServerHello.random), Section 4.4.3 (CertificateVerify signs the transcript hash) and Section 4.4.4 (Finished)
  - paper: doi:10.1109/SP.2015.39
    title: "Benjamin Beurdouche, Karthikeyan Bhargavan, Antoine Delignat-Lavaud, Cedric Fournet, Markulf Kohlweiss, Alfredo Pironti, Pierre-Yves Strub and Jean Karim Zinzindohoue, A messy state of the union: taming the composite state machines of TLS, IEEE Symposium on Security and Privacy 2015"
    locator: the section on FREAK (the server accepts export RSA in a non-export cipher suite and the client accepts a 512-bit RSA key)
  - paper: doi:10.1145/2810103.2813707
    title: "David Adrian, Karthikeyan Bhargavan, Zakir Durumeric, Pierrick Gaudry, Matthew Green, J. Alex Halderman, Nadia Heninger, Drew Springall, Emmanuel Thome, Luke Valenta, Benjamin VanderSloot, Eric Wustrow, Santiago Zanella-Beguelin and Paul Zimmermann, Imperfect forward secrecy: how Diffie-Hellman fails in practice, ACM CCS 2015"
    locator: Section 3 (Logjam, the downgrade to 512-bit export Diffie-Hellman and the precomputation for common primes)
  - url: "https://cyclonedx.org/docs/1.6/json/"
    title: "OWASP CycloneDX, Bill of Materials specification version 1.6 (cryptographic bill of materials), 2024"
    locator: the cryptoProperties object (algorithm, certificate, protocol and related crypto material assets)
---

Cryptographic agility is the property of a protocol, product or organization that lets it replace one cryptographic algorithm with another, by configuration or policy, without a redesign and without breaking interoperation. It rests on three things: an identifier for each algorithm on the wire and in stored data, a negotiation that picks a common algorithm and resists downgrade, and an inventory that tells the owner where each algorithm is in use. The move to post-quantum cryptography, which replaces every RSA and elliptic curve key exchange and signature, is the largest test of agility so far. NIST describes the practice in CSWP 39, updated in June 2026.

## In plain words

Old systems often had one algorithm built in everywhere, so changing it meant rewriting and redeploying everything. An agile system names its algorithms, like plugs with labels, so a new one can be added and an old one switched off by changing a setting.

Agility has a risk. If two sides agree on an algorithm in public, an attacker can try to make them agree on the weakest one. Good protocols stop this by checking, at the end of the handshake, that both sides saw the same offer.

Agility also needs a list. An organization cannot replace an algorithm if it does not know where it uses it.

## The idea

**Identifiers.** Every algorithm, with its parameters, gets a registered name or number: TLS cipher suites and named groups, SSH key exchange names, X.509 and CMS object identifiers, JOSE and COSE algorithm names. RFC 7696 (Section 2.1) asks protocols to carry such identifiers instead of fixing one algorithm. A new algorithm is then a new entry, for example the TLS group X25519MLKEM768 (code point 0x11EC), and old software that does not know the entry ignores it.

**Negotiation.** The client lists what it supports, in preference order. The server picks the first entry in its own preference that the client offered and that its policy allows. In TLS 1.3 the client sends the groups in `supported_groups` and its key shares in `key_share`, and the signature algorithms in `signature_algorithms` (RFC 8446, Section 4.1.1). Policy decides which entries are allowed, so a deprecation is a configuration change.

**Downgrade attacks.** Negotiation in the clear invites an active attacker to remove the strong entries from the offer, so that the server picks a weak one that the attacker can break. Two attacks of 2015 showed this in TLS 1.2:

- **FREAK** (Beurdouche et al.): many clients accepted a 512-bit export RSA key in a normal RSA key exchange, because of a state machine bug. An attacker who asked the server for export RSA could factor the 512-bit key in hours and then read and change the session.
- **Logjam** (Adrian et al.): an attacker changed the offer to export Diffie-Hellman with 512-bit primes. The server's signature in TLS 1.2 did not cover the client's offer, so the client did not notice. Precomputation on the few primes in common use let the attacker find the discrete logarithm in about a minute and forge the Finished messages.

**The defence: authenticate the whole transcript.** Both sides hash the full handshake, including the offer exactly as sent, and check the hash at the end. A MAC under the session key (the TLS 1.2 Finished message) is not enough: if the downgraded algorithm is weak enough to break during the handshake, the attacker knows the session key and can fix the MAC. That is the Logjam case. TLS 1.3 makes the server sign the transcript hash with its long-term key (CertificateVerify, RFC 8446, Section 4.4.3), which the attacker cannot forge, and puts a sentinel value in ServerHello.random when a TLS 1.3 server negotiates an older version (Section 4.1.3). The general rules: authenticate the transcript with the long-term key, and remove broken algorithms from the code and not only from the default preferences, because a downgrade can only reach what is still enabled.

**Inventory.** An organization lists where it uses each algorithm: protocols, libraries, certificates, keys, stored data, hardware. A cryptographic bill of materials (CBOM), for example in the CycloneDX 1.6 format, records this per product. CSWP 39 (Section 5) puts the inventory at the start of a strategic plan: governance, inventory, a risk assessment that ranks the assets, then migration or compensating controls.

**Hybrids during the transition.** When a new algorithm is not yet trusted as much as the old one, protocols combine both, so that the result is secure if either holds. See [hybrid key exchange](/hybrid-key-exchange/). Hybrids are themselves registered as new identifiers, which is agility at work.

**The cost of agility.** RFC 7696 (Section 3) warns that every extra option is more code, more tests and more ways to fail, and that negotiation itself is a target. A protocol with one fixed, strong algorithm and a version number (WireGuard is the usual example) can be easier to get right, and changes by a new version instead of a new option.

## Examples

**The code with this page** builds a small registry of TLS groups (the IANA code points of X25519MLKEM768, SecP256r1MLKEM768, x25519, secp256r1 and ffdhe2048, plus an invented weak group 0xff01 that models export Diffie-Hellman). An attacker removes entries from the client's offer, and the handshake uses one of three protections:

| protection | downgrade to x25519 | downgrade to the breakable weak group |
|---|---|---|
| none | not detected | not detected |
| MAC over the transcript under the session key | detected | not detected (the attacker knows the key) |
| server signature over the transcript | detected | detected |

When the weak group is set to disallowed in the registry, the same attack finds no common group and the handshake fails, which is the safe result. The signature is modelled by an HMAC under a long-term key; the code is for study only, not constant time. Use a maintained TLS library that implements RFC 8446.

**The move to post-quantum TLS.** Chrome and Cloudflare first deployed X25519Kyber768 under a temporary code point (0x6399) based on a draft of Kyber. When FIPS 203 changed the algorithm, they moved to X25519MLKEM768 under a new code point, 0x11EC, and later removed the draft one. Because both were identifiers in an existing negotiation, the change needed no new protocol version. One problem appeared: the larger key share (1216 bytes) pushed the ClientHello over one TCP packet, and some servers and middleboxes that assumed a one-packet ClientHello failed. Agility in the protocol is not agility in every implementation.

**SHA-1 in certificates.** Browsers announced the end of SHA-1 certificates years ahead, but the removal still took until 2017, because certificates, hardware and old clients all had SHA-1 built in. The SHAttered collision of February 2017 came only weeks after the last browsers stopped trusting SHA-1 certificates.

**Where agility is hard.** Algorithms fixed in hardware (smart cards, HSMs, firmware boot ROMs), in long-lived stored formats, or in standards with no identifier field cannot change by configuration. CSWP 39 (Section 4) discusses gateways placed in front of such legacy systems.

## Where it is used

- **Post-quantum migration.** Moving key exchange to ML-KEM and signatures to ML-DSA, SLH-DSA or FN-DSA, in the order that [harvest now, decrypt later](/harvest-now-decrypt-later/) suggests.
- **Protocol design.** RFC 7696 (BCP 201) is the IETF guidance: algorithm identifiers, a small set of mandatory-to-implement algorithms, and a plan to change them.
- **Policy and compliance.** NIST IR 8547 deprecates RSA and elliptic curve algorithms after 2030 and disallows them after 2035; a system with agility follows such a schedule by configuration.
- **Libraries and platforms.** Cryptographic providers in OpenSSL 3, Java and the operating systems let applications ask for an algorithm by name and let administrators change the default set.

## References
