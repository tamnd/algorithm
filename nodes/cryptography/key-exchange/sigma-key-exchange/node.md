---
tag: 7AWQRY
kind: algorithm
slug: sigma-key-exchange
name: SIGMA key exchange
aliases:
area: cryptography/key-exchange
level: research
summary: Krawczyk's SIGn-and-MAc family of authenticated Diffie-Hellman protocols. Each party signs both DH values and MACs its own identity; SIGMA is the basis of IKEv2 and the TLS 1.3 handshake.
solves: [key-agreement-problem]
model: word-ram
complexity:
  vars: {m: the number of binary digits of the prime p}
  time: {worst: Θ(m^3), average: Θ(m^3), best: Θ(m^3)}
  space: {extra: Θ(m)}
properties: {deterministic: false, randomized: true}
history:
  year: 2003
  people: [Hugo Krawczyk]
  note: Krawczyk described SIGMA at CRYPTO 2003, after its design had shaped the signature modes of IKE; Canetti and Krawczyk had proved the core protocol secure at CRYPTO 2002.
prereqs: [station-to-station-protocol, unknown-key-share-attack, hmac]
see_also: [authenticated-key-exchange, ike-protocol, tls-handshake, key-confirmation, perfect-forward-secrecy, digital-signature, sigma-protocol, hmqv]
sources:
  - paper: "Hugo Krawczyk, SIGMA: the SIGn-and-MAc approach to authenticated Diffie-Hellman and its use in the IKE protocols, CRYPTO 2003, LNCS 2729, Springer, 2003, pages 400 to 425"
    locator: Section 3 (basic SIGMA), Section 5 (SIGMA-I and SIGMA-R with identity protection) and Section 2 (STS, ISO 9798-3 and the identity misbinding attacks)
  - paper: "Ran Canetti and Hugo Krawczyk, Security analysis of IKE's signature-based key-exchange protocol, CRYPTO 2002, LNCS 2442, Springer, 2002, pages 143 to 161"
    locator: the proof that the SIGMA core protocol is SK-secure in the Canetti-Krawczyk model under DDH; full version IACR ePrint 2002/120
  - paper: "Ran Canetti and Hugo Krawczyk, Analysis of key-exchange protocols and their use for building secure channels, EUROCRYPT 2001, LNCS 2045, Springer, 2001, pages 453 to 474"
    locator: the Canetti-Krawczyk model and the definition of SK-security
  - url: "https://www.rfc-editor.org/rfc/rfc7296"
    title: "C. Kaufman, P. Hoffman, Y. Nir, P. Eronen and T. Kivinen, RFC 7296, Internet Key Exchange Protocol Version 2 (IKEv2), 2014"
    locator: Section 1.2 (IKE_AUTH) and Section 2.15 (the AUTH payload, signed octets with prf(SK_pi, IDi'))
---

SIGMA ("SIGn-and-MAc") is a family of authenticated [Diffie-Hellman](/diffie-hellman/) key exchange protocols that Hugo Krawczyk described in 2003. Each party signs the two ephemeral Diffie-Hellman values and also sends a MAC of its *own identity* under a key derived from the shared secret. The signature proves that the party took part in this exchange; the MAC binds the party's identity to the key. Together they give a protocol that is provably secure in the Canetti-Krawczyk model, with [forward secrecy](/perfect-forward-secrecy/), and that resists the identity misbinding ([unknown key-share](/unknown-key-share-attack/)) attacks that break [STS](/station-to-station-protocol/)-style "sign only" protocols. SIGMA-I and SIGMA-R add identity protection. SIGMA is the basis of the signature authentication in [IKEv2](/ike-protocol/), and the [TLS 1.3 handshake](/tls-handshake/) follows the same design.

**Notation.** $G = \langle g \rangle$ has prime order $q$. $s$ is a session identifier, $X = g^x$ and $Y = g^y$ the ephemeral values, $\mathrm{SIG}_P$ the signature of party $P$, and $\mathrm{MAC}_{K_m}$ an [HMAC](/hmac/) under the key $K_m$. From $g^{xy}$ the parties derive three keys: $K_e$ for encryption, $K_m$ for the MAC, and the session key $K_s$, which the protocol itself never uses.

## In plain words

SIGMA is a careful fix of an older idea. Two parties swap fresh Diffie-Hellman numbers and each signs both numbers, so a person in the middle cannot swap them. That alone has a hole: a dishonest user can take Alice's last message, put his own name and his own signature on it, and pass it on. The key is still shared with Alice, but Bob now thinks it belongs to the dishonest user.

SIGMA closes the hole with one more item. Each party also sends a short check value over its own name, made with a key that only the two real parties can compute. The dishonest user can sign anything with his own key, but he cannot make the check value for his name, so Bob rejects.

The SIGMA-I form also hides the names inside encryption, so an eavesdropper cannot see who is talking.

## The problem

Two parties with long-term signature keys, certified in a public key infrastructure, run a key exchange over a network controlled by an active adversary. Some of the other users may be dishonest and hold valid certificates. The parties want a fresh session key with mutual authentication and forward secrecy, and they may want to hide their identities from eavesdroppers. In the Canetti-Krawczyk model this is SK-security: matching sessions get the same key, and the key of an uncorrupted session is indistinguishable from random (see [authenticated key exchange](/authenticated-key-exchange/)).

## The algorithm

The pseudocode is SIGMA-I. The signed and MACed data carry a direction tag ("1" for the responder, "0" for the initiator) and $s$, as in the protocol that Canetti and Krawczyk analysed.

```pseudo id=main
SIGMA-I(A, B)                                         ▷ A initiates; B responds
L1  A: x ← uniform in [1, q − 1]; X ← g^x; send (s, X)
L2  B: if X ∉ G then fail
L3  B: y ← uniform in [1, q − 1]; Y ← g^y; (K_e, K_m, K_s) ← KDF(X^y, s)
L4  B: send (s, Y, E_Ke(B, SIG_B("1", s, X, Y), MAC_Km("1", s, B)))
L5  A: if Y ∉ G then fail; (K_e, K_m, K_s) ← KDF(Y^x, s); erase x
L6  A: decrypt to (B, σ, τ); fail unless VERIFY(pk_B, ("1", s, X, Y), σ) and τ = MAC_Km("1", s, B)
L7  A: send (s, E_Ke(A, SIG_A("0", s, Y, X), MAC_Km("0", s, A))); accept K_s with peer B
L8  B: decrypt to (A, σ, τ); fail unless VERIFY(pk_A, ("0", s, Y, X), σ) and τ = MAC_Km("0", s, A)
L9  B: erase y; accept K_s with peer A
```

The signature at lines L4 and L7 covers only the two ephemeral values (and $s$); it does not name the peer. The MAC at the same lines covers only the sender's *own* name. This split is the point of the design. The signature gives freshness and proof of participation, and it does not reveal whom the signer is talking to. The MAC proves knowledge of $K_m$, which only the parties to $g^{xy}$ have, and binds the sender's name to it. Line L6 and line L8 check both, under the public key of the identity found inside the message.

In SIGMA-I the responder's identity in $m_2$ is protected against passive attackers (it is encrypted under $K_e$), and the initiator's identity in $m_3$ is protected against active attackers, because $\hat A$ sends it only after it has authenticated $\hat B$ at line L6.

**About the code.** The Python code of this page uses Schnorr signatures in a 256-bit toy group, HMAC-SHA-256, HMAC-based key derivation, and a toy stream cipher for $E$. Two flags switch off the encryption (basic SIGMA) and the MAC (the insecure "sign only" protocol) for the tests. It is for study only and not constant time. Use IKEv2 through strongSwan or libreswan, or TLS 1.3 through OpenSSL, BoringSSL or rustls, or a FIPS 140 validated module.

## Example

The test "sign only falls to identity misbinding" runs the protocol without the MACs and without encryption. Eve is a registered user with her own key pair.

| step | what happens |
|---|---|
| L1 to L6 | Alice and Bob run normally; both hold $K_s$, Alice with peer Bob |
| L7 | Alice sends $(s, \text{"A"}, \mathrm{SIG}_A(\text{"0"}, s, Y, X))$ |
| attack | Eve replaces it by $(s, \text{"E"}, \mathrm{SIG}_E(\text{"0"}, s, Y, X))$, a valid signature under *her own* key |
| L8, L9 | Bob checks $\mathrm{SIG}_E$ under Eve's public key: it verifies. Bob accepts $K_s$ with peer Eve |

Alice and Bob share $K_s$, but Bob credits Eve with Alice's messages. Eve does not know $K_s$. With the MAC switched on, Eve must also send $\mathrm{MAC}_{K_m}(\text{"0"}, s, \text{"E"})$. She does not know $K_m$; Alice's tag is over "A", so Bob rejects at line L8. The test tries the empty tag, Alice's tag and a zero tag.

## Correctness

If both parties are honest and the messages arrive unchanged, both compute $g^{xy}$ ($X^y = Y^x$) and so the same $(K_e, K_m, K_s)$. Decryption under the same $K_e$ returns the sender's identity, signature and tag. The signature is on the same string that the receiver rebuilds from $s$, $X$ and $Y$, and the tag is the MAC under the same $K_m$ of the same identity, so both checks pass, and both parties accept $K_s$, each naming the other. The proof is below.

Security is the theorem of Canetti and Krawczyk (2002): the core protocol (basic SIGMA) is SK-secure in the Canetti-Krawczyk model, with forward secrecy, if the DDH assumption holds in $G$, the signature scheme is unforgeable, the MAC is secure and the key derivation is a pseudorandom function. Krawczyk (2003) argues that the identity-protecting variants keep this security.

## Complexity

Each party computes one ephemeral value, one Diffie-Hellman value, one subgroup check, one signature and one verification, so a constant number of exponentiations, $\Theta(m^3)$ bit operations with schoolbook arithmetic. The MACs, key derivation and encryption cost $O(1)$ hash calls for messages of $O(m)$ bits. SIGMA-I has three messages; SIGMA-R has four. The extra space is $\Theta(m)$.

## Properties

- **SK-secure in the CK model** with full forward secrecy (Canetti and Krawczyk 2002).
- **Resistant to identity misbinding.** The MAC over the own identity binds the name to the key, without the CA needing to check proof of possession.
- **Identity protection.** SIGMA-I protects the initiator against active attackers and the responder against passive ones; SIGMA-R does the opposite.
- **Deniability of the peer's name.** The signature does not contain the peer's identity, so a signed transcript does not prove *whom* the signer talked to.
- **Key separation.** The session key $K_s$ is not used inside the protocol.

## Variants and improvements

- **Basic SIGMA.** Three messages with no encryption: $m_2 = (s, Y, \hat B, \mathrm{SIG}_B(\dots), \mathrm{MAC}_{K_m}(\dots, \hat B))$ and $m_3 = (s, \hat A, \mathrm{SIG}_A(\dots), \mathrm{MAC}_{K_m}(\dots, \hat A))$.
- **SIGMA-R.** Four messages: $X$, then $Y$, then the initiator's encrypted identity, signature and MAC, then the responder's. The responder's identity is protected against active attackers; this is the form behind IKEv2, where the IKE_SA_INIT exchange carries $X$ and $Y$ and the IKE_AUTH exchange carries the encrypted identities.
- **MAC inside the signature.** One may sign the MAC value instead of sending both; Krawczyk discusses this and other placements.
- **TLS 1.3.** The server sends CertificateVerify, a signature over the transcript hash, then Finished, a MAC over the transcript under a key from the handshake secret; the transcript includes the certificate and so the identity. This is SIGMA with the whole transcript in place of the separate items.

## When to use it

Use SIGMA, through IKEv2 or TLS 1.3, when parties have certified signature keys and need mutual authentication with forward secrecy and identity protection. Use [HMQV](/hmqv/) or a [Noise](/noise-protocol-framework/) pattern when the parties have static Diffie-Hellman keys instead of signature keys and want fewer messages or less computation.

## Pitfalls

- **Dropping the MAC.** Without the MAC at lines L4 and L7, the protocol is "sign only" and a registered user mounts the misbinding attack shown in the example. Signing only the ephemeral values is safe *only* together with the MAC of line L4 and line L7.
- **MAC over the peer's identity instead of the own one.** The MAC must cover the sender's own name, the one that the receiver uses at line L6 or L8 to pick the public key.
- **Using the session key inside the protocol.** $K_e$ and $K_m$ must be separate from $K_s$. Using $K_s$ to encrypt or MAC handshake messages breaks the indistinguishability of $K_s$.
- **No group checks.** Lines L2 and L5 reject elements outside $G$, as in [Diffie-Hellman](/diffie-hellman/).
- **Unauthenticated encryption.** The toy stream cipher gives confidentiality only; the signature and the MAC inside give integrity. Real implementations use an authenticated cipher, as IKEv2 does.

## Implementations

## History

The identity misbinding attacks on signature-based Diffie-Hellman go back to the analysis of STS by Diffie, van Oorschot and Wiener (1992) and the unknown key-share attacks of Blake-Wilson and Menezes (1999). Krawczyk designed SKEME (1996) and contributed the SIGMA approach to the signature modes of IKEv1 (1998) and later IKEv2 (2005). Canetti and Krawczyk proved the core protocol secure at CRYPTO 2002, and Krawczyk explained the design and its variants at CRYPTO 2003. The TLS 1.3 handshake (2018) uses the same sign-and-MAC structure over the full transcript.

## References
