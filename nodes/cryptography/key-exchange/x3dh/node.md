---
tag: F1F34V
kind: algorithm
slug: x3dh
name: Extended Triple Diffie-Hellman
aliases:
- X3DH
- Extended Triple Diffie-Hellman key agreement
area: cryptography/key-exchange
level: advanced
summary: Asynchronous key agreement of Signal. Alice combines three or four X25519 values from identity keys, a signed prekey and one-time prekeys that Bob left on a server. Marlinspike and Perrin, 2016.
solves: [key-agreement-problem]
model: word-ram
complexity:
  vars: {m: the length of the first message in bytes}
  time: {worst: O(m), average: O(m), best: O(m)}
  space: {extra: O(m)}
properties: {deterministic: false, randomized: true}
history:
  year: 2016
  people: [Moxie Marlinspike, Trevor Perrin]
  note: The triple Diffie-Hellman handshake was used in TextSecure from 2013; Marlinspike and Perrin published the X3DH specification, revision 1, on 2016-11-04.
prereqs: [authenticated-key-exchange, x25519, hkdf]
see_also: [double-ratchet, signal-protocol, key-ratchet, ed25519, mqv, hmqv, noise-protocol-framework, station-to-station-protocol]
sources:
  - url: "https://signal.org/docs/specifications/x3dh/"
    title: Moxie Marlinspike and Trevor Perrin, The X3DH Key Agreement Protocol, revision 1, 2016-11-04
    locator: Section 2 (parameters, Encode, KDF with the 32 0xFF bytes and the zero salt, keys), Section 3 (publishing keys, sending and receiving the initial message), Section 4 (security considerations, including replay, deniability, key compromise and identity binding)
  - url: "https://signal.org/docs/specifications/xeddsa/"
    title: Trevor Perrin, The XEdDSA and VXEdDSA Signature Schemes, revision 1, 2016-10-20
    locator: calculate_key_pair, xeddsa_sign and xeddsa_verify, used to sign the signed prekey with the X25519 identity key
  - paper: "Katriel Cohn-Gordon, Cas Cremers, Benjamin Dowling, Luke Garratt and Douglas Stebila, A formal security analysis of the Signal messaging protocol, IEEE European Symposium on Security and Privacy (EuroS&P) 2017; full version in Journal of Cryptology, 2020"
    locator: the analysis of X3DH as the first stage of a multi-stage key exchange, with and without one-time prekeys
  - paper: "Kristin Lauter and Anton Mityagin, Security analysis of KEA authenticated key exchange protocol, PKC 2006"
    locator: KEA+, an earlier implicitly authenticated protocol that hashes the two mixed Diffie-Hellman values of long-term and ephemeral keys
  - url: "https://www.rfc-editor.org/rfc/rfc7748"
    title: Adam Langley, Mike Hamburg and Sean Turner, RFC 7748, Elliptic Curves for Security, January 2016
    locator: Section 5 (X25519) and Section 5.2 (test vectors), used by the code
  - url: "https://www.rfc-editor.org/rfc/rfc5869"
    title: Hugo Krawczyk and Pasi Eronen, RFC 5869, HMAC-based Extract-and-Expand Key Derivation Function (HKDF), May 2010
    locator: Section 2 and Appendix A.1 (Test Case 1), used by the code
  - url: "https://www.rfc-editor.org/rfc/rfc8032"
    title: Simon Josefsson and Ilari Liusvaara, RFC 8032, Edwards-Curve Digital Signature Algorithm (EdDSA), January 2017
    locator: Section 7.1, TEST 1, used to check the Edwards curve code under XEdDSA
---

Extended Triple Diffie-Hellman (X3DH) is the key agreement that starts a Signal conversation. Bob may be offline: he has earlier put an identity key, a signed medium-term prekey and a set of one-time prekeys on a server. Alice fetches this prekey bundle, checks the signature, makes an ephemeral key, and computes three or four [X25519](/x25519/) values between her keys and Bob's. A KDF of these values gives a shared key $SK$, and Alice sends her first message at once. Bob later recomputes the same values and $SK$. The mix of long-term and ephemeral keys gives mutual authentication without signatures on the messages, forward secrecy, and deniability. $SK$ then starts the [Double Ratchet](/double-ratchet/).

**Notation.** $IK_A$ and $IK_B$ are the long-term identity key pairs of Alice and Bob. $SPK_B$ is Bob's signed prekey, which he replaces from time to time, and $OPK_B$ one of his one-time prekeys. $EK_A$ is Alice's ephemeral key pair. $\mathrm{DH}(X, Y)$ is X25519 of the private key of one pair and the public key of the other; it has the same value whichever side computes it. $\mathrm{Encode}(PK)$ is the byte 0x05 followed by the 32-byte public key. $\mathrm{KDF}(KM) = \mathrm{HKDF}(\text{salt} = 32 \text{ zero bytes}, \text{ikm} = F \,\|\, KM, \text{info}, 32)$ with $F$ equal to 32 bytes 0xFF, which separates these inputs from XEdDSA. $\mathrm{Sig}$ is an XEdDSA signature made with the X25519 identity key.

## In plain words

Bob wants people to be able to start a private conversation with him while his phone is off. So he leaves some public keys with a server: his permanent key, a key he changes every week or so and signs with the permanent key, and a stack of single-use keys.

Alice takes Bob's keys from the server, checks the signature, and makes a single-use key of her own. She combines her permanent key and her new key with Bob's keys in three or four pairs. Each pair gives a shared secret that only the two holders of the matching private keys can compute. Together they give one key, which Alice uses at once to encrypt a first message.

Bob later does the same combination with his private keys and gets the same key. He deletes the single-use key that Alice used.

## The problem

Alice wants to establish a shared secret key with Bob and send him encrypted data while Bob is offline, through an untrusted server. The key must be known only to the holders of $IK_A$ and $IK_B$ (mutual authentication), must stay secret if the identity keys leak later (forward secrecy), and the exchange should not give either party a signature that proves to a third party that the two talked (deniability). This is an asynchronous form of [authenticated key exchange](/authenticated-key-exchange/), and a case of the [key agreement problem](/key-agreement-problem/).

## The algorithm

```pseudo id=main
Bob publishes                                   ▷ Section 3.2 of the specification
L1  sig ← Sig(IK_B, Encode(SPK_B.public))
L2  put on the server: IK_B.public, SPK_B.public, sig, and one-time prekeys OPK_B with ids
Alice sends                                     ▷ Section 3.3
L3  get a bundle; if the check of sig with IK_B.public on Encode(SPK_B.public) fails: abort
L4  EK_A ← a fresh X25519 key pair
L5  DH1 ← DH(IK_A, SPK_B)
L6  DH2 ← DH(EK_A, IK_B)
L7  DH3 ← DH(EK_A, SPK_B)
L8  if the bundle has OPK_B: DH4 ← DH(EK_A, OPK_B)
L9  SK ← KDF(DH1 ∥ DH2 ∥ DH3 [∥ DH4]);  delete EK_A.private and the DH values
L10 AD ← Encode(IK_A.public) ∥ Encode(IK_B.public);  send IK_A.public, EK_A.public, the OPK_B id and AEAD(SK, first plaintext, AD)
Bob receives                                    ▷ Section 3.4
L11 DH1 ← DH(SPK_B, IK_A);  DH2 ← DH(IK_B, EK_A);  DH3 ← DH(SPK_B, EK_A)
L12 if an OPK_B id is given: DH4 ← DH(OPK_B, EK_A), and delete OPK_B.private (abort if the id is unknown)
L13 SK ← KDF(DH1 ∥ DH2 ∥ DH3 [∥ DH4])
L14 AD ← Encode(IK_A.public) ∥ Encode(IK_B.public)
L15 if the AEAD decryption of the first ciphertext with SK and AD fails: abort and delete SK
L16 return SK
```

**Publishing.** Bob's identity key is an X25519 key, so he signs his prekey with XEdDSA, which turns an X25519 private key into an Edwards signing key (line L1). The server gives each one-time prekey to at most one sender and Bob uploads new ones when the stock is low. If the stock is empty, the bundle has no one-time prekey (line L2).

**The four values.** $DH1$ (line L5) binds Alice's identity to Bob's signed prekey, and $DH2$ (line L6) binds Alice's ephemeral key to Bob's identity: together they give mutual authentication, since a party who knows neither $IK_A$ nor $IK_B$ cannot compute both. $DH3$ (line L7) and $DH4$ (line L8) use the ephemeral key with the prekeys and give forward secrecy: once $EK_A$, $SPK_B$ and $OPK_B$ are deleted, $SK$ cannot be recomputed even with both identity keys.

**Receiving.** Bob computes the same values in lines L11 and L12, with each DH taken from the other side. He deletes the one-time prekey at once (line L12), so a replay of the same first message fails. The first ciphertext acts as key confirmation: if it does not decrypt under $SK$ and $AD$ (line L15), Bob aborts.

**About the code.** The Python code is for study only. It is not constant time and must not protect real data; use libsignal or another maintained implementation. X25519 (RFC 7748), HKDF (RFC 5869), the Edwards curve arithmetic and XEdDSA are local copies; the tests check X25519 and HKDF against the RFC test vectors and the Edwards code against RFC 8032 TEST 1. The info string is the study value `X3DHStudy`. The AEAD for the first message is a study scheme (encrypt-then-MAC with an HMAC-SHA256 key stream), not a standard AEAD; Signal uses the Double Ratchet's encryption here. The X3DH specification has no official test vectors.

## Example

The code uses X25519, whose values are 32-byte strings. To show the structure with small numbers, use the multiplicative group modulo $p = 23$ with generator $g = 4$ of order $11$, and write $\mathrm{DH}(x, g^y) = g^{xy}$.

| Key | Private | Public |
|---|---|---|
| $IK_A$ | 3 | $4^3 = 18$ |
| $EK_A$ | 5 | $4^5 = 12$ |
| $IK_B$ | 2 | $4^2 = 16$ |
| $SPK_B$ | 9 | $4^9 = 13$ |
| $OPK_B$ | 6 | $4^6 = 2$ |

| Value | Alice computes | Bob computes | Result |
|---|---|---|---|
| $DH1$ | $13^3$ | $18^9$ | 12 |
| $DH2$ | $16^5$ | $12^2$ | 6 |
| $DH3$ | $13^5$ | $12^9$ | 4 |
| $DH4$ | $2^5$ | $12^6$ | 9 |

Both get $KM = 12 \,\|\, 6 \,\|\, 4 \,\|\, 9$ and so the same $SK = \mathrm{KDF}(KM)$. In the code's tests, Alice and Bob get the same 32-byte $SK$ with and without a one-time prekey, $AD$ has length 66, and Bob's one-time prekey is gone after line L12.

## Correctness

**Claim.** If Bob's bundle is genuine and Alice's message arrives unchanged, Alice's check in line L3 passes, both compute the same four DH values and the same $SK$, and Bob accepts in line L15. Each DH value is X25519 of one private key and one public key, and X25519 is commutative, so $\mathrm{DH}(X, Y)$ computed by the owner of $X$ equals the value computed by the owner of $Y$. Both sides use the same order of values, the same KDF and the same $AD$. The full proof is on the proof page.

**Security.** Cohn-Gordon, Cremers, Dowling, Garratt and Stebila (2017, 2020) prove that X3DH, as the first stage of the Signal protocol, gives a secret session key under the gap Diffie-Hellman assumption with the KDF as a random oracle, in a model where the attacker can reveal long-term and ephemeral keys in combinations that do not trivially reveal the key. Without a one-time prekey, the key is secret only until Bob's signed prekey is compromised.

## Complexity

Alice computes up to five X25519 scalar multiplications (the public key of $EK_A$ and $DH1$ to $DH4$), one XEdDSA verification, one HKDF and one AEAD encryption; Bob computes three or four X25519 values, one HKDF and one decryption. For the fixed 255-bit curve each step is $O(1)$, so the cost is $O(m)$ for an $m$-byte first message. Bob stores one signed prekey and a constant stock of one-time prekeys on the server; the protocol needs one message from Alice and no round trip.

## Properties

- **Asynchronous.** Bob need not be online; Alice sends encrypted data in the first message.
- **Mutual implicit authentication.** Only holders of the private keys of $IK_A$ and $IK_B$ can compute $DH1$ and $DH2$, so only they get $SK$. No signature is made on the session.
- **Forward secrecy.** After the ephemeral and prekey private keys are deleted, a later leak of the identity keys does not reveal $SK$. With no one-time prekey, forward secrecy holds only after Bob deletes the old signed prekey.
- **Deniability.** The transcript contains no signature over the session, and either party could have made it with its own keys, so it is not a proof to a third party that the two talked.
- **No identity binding.** The protocol does not show that $IK_B$ belongs to Bob; users must compare identity key fingerprints (safety numbers) out of band.
- **Replay.** Without a one-time prekey, a replayed first message gives Bob the same $SK$ again.

## Variants and improvements

- **Triple Diffie-Hellman (3DH).** The version used in TextSecure from 2013 combines $\mathrm{DH}(IK_A, EK_B)$, $\mathrm{DH}(EK_A, IK_B)$ and $\mathrm{DH}(EK_A, EK_B)$ in an interactive exchange; X3DH replaces Bob's ephemeral key by prekeys so that Bob can be offline. OPAQUE uses the same three-value mix for its key exchange.
- **Without one-time prekeys.** When the server has none left, the protocol runs with $DH1$ to $DH3$ only; this is weaker against replay and against a later leak of $SPK_B$.
- **Other curves and key forms.** The specification allows X25519 or X448 with SHA-256 or SHA-512. Some implementations keep the identity key as an [Ed25519](/ed25519/) key and convert it for Diffie-Hellman, instead of signing with XEdDSA.
- **PQXDH.** In 2023 Signal added a post-quantum key encapsulation (CRYSTALS-Kyber, later ML-KEM) to X3DH: Bob also publishes signed KEM prekeys, and the KEM shared secret enters the KDF, so a later quantum attacker cannot recover $SK$ from a recorded transcript.
- **Related protocols.** KEA+ (Lauter and Mityagin 2006), [MQV](/mqv/) and [HMQV](/hmqv/) also get implicit authentication by mixing long-term and ephemeral Diffie-Hellman values; the [Noise framework](/noise-protocol-framework/) describes similar patterns such as XK and IK.

## When to use it

Use X3DH, or PQXDH where available, to start an end-to-end encrypted conversation in which the responder is often offline and a server holds its prekeys, followed by the Double Ratchet. For an interactive handshake where both parties are online, a protocol such as Noise or TLS 1.3 is simpler. Use a maintained library, and give users a way to verify identity keys.

## Pitfalls

- **Not checking the prekey signature.** If line L3 is skipped, a malicious server can put its own $SPK_B$ and $OPK_B$ in the bundle. It then knows $DH1$, $DH3$ and $DH4$, and if it later steals $IK_B$ it also gets $DH2$ and so $SK$: forward secrecy is lost. Abort when the check of line L3 fails.
- **Keeping one-time prekeys.** If line L12 does not delete $OPK_B$, a replayed first message is accepted and a later leak of $OPK_B$ reveals $SK$. Delete it in line L12, before line L13.
- **Keeping the ephemeral key.** Line L9 must delete $EK_A$'s private key and the DH values after use, or a later leak of Alice's device reveals $SK$.
- **Different AD on the two sides.** Line L10 and line L14 must put Alice's identity key first and Bob's second, with the same encoding; otherwise line L15 always fails, or, if $AD$ is left out, the session is not bound to the identities.
- **A different KDF input.** The prefix $F$, the zero salt and the order $DH1, DH2, DH3, DH4$ must be the same in lines L9 and L13.
- **Trusting the server for identity.** The server can give Alice a bundle with its own $IK_B$. Without a fingerprint check, nothing in lines L3 to L10 detects this.
- **Reused prekeys.** If the server gives one $OPK_B$ to two senders, line L12 aborts for the second; Bob should then not reuse that id, and the server should mark it as used.

## Implementations

The Python code implements Sections 2 and 3 of the specification with X25519 and SHA-256: `Bob.__init__` signs the prekey (line L1), `Bob.bundle` (line L2), `alice_send` (lines L3 to L10) and `Bob.receive` (lines L11 to L16). The tests check X25519, HKDF and the Edwards code against RFC 7748, RFC 5869 and RFC 8032; XEdDSA signatures verify and tampered ones fail; both sides get the same $SK$ with and without a one-time prekey; a swapped signed prekey is rejected; a false identity makes Bob abort; and a replay is accepted without a one-time prekey but rejected with one. libsignal (Rust) is the reference implementation.

## History

Perrin designed the triple Diffie-Hellman handshake for TextSecure in 2013, to replace a signed handshake with one that gives deniability. Prekeys, so that a conversation can start while the responder is offline, were added soon after. Marlinspike and Perrin published the X3DH specification, revision 1, on 2016-11-04, with the XEdDSA specification. Cohn-Gordon and others published a formal analysis in 2017. In 2023 Signal published PQXDH, which extends X3DH with a post-quantum key encapsulation.

## References
