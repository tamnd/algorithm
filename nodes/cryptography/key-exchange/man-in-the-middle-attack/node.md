---
tag: 0ZCK64
kind: concept
slug: man-in-the-middle-attack
name: Man-in-the-middle attack
aliases:
- MITM attack
area: cryptography/key-exchange
level: intro
summary: An active attacker sits between two parties, runs a separate key exchange with each, and relays and changes their messages. Unauthenticated key exchange cannot stop it.
prereqs: [diffie-hellman]
see_also: [authenticated-key-exchange, diffie-hellman, station-to-station-protocol, sigma-key-exchange, unknown-key-share-attack, digital-signature, key-confirmation, password-authenticated-key-exchange]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 12, Section 12.9.1, Attack 1 (intruder-in-the-middle on unauthenticated Diffie-Hellman), and Section 12.2.3 (active attacks)
  - paper: doi:10.1109/TIT.1976.1055638
    title: Whitfield Diffie and Martin E. Hellman, New directions in cryptography, IEEE Transactions on Information Theory 22(6), pages 644 to 654, 1976
    locator: Section III (public key distribution needs an authentic public file)
  - paper: doi:10.1145/358027.358053
    title: Ronald L. Rivest and Adi Shamir, How to expose an eavesdropper, Communications of the ACM 27(4), pages 393 to 394, 1984
    locator: the interlock protocol, which sends each ciphertext in two halves
  - paper: doi:10.1007/11535218_19
    title: Serge Vaudenay, Secure communications over insecure channels based on short authenticated strings, CRYPTO 2005, LNCS 3621, pages 309 to 326
    locator: the SAS-based message cross-authentication protocol and its bound of about 2^-k for a k-bit authenticated string
  - url: "https://www.rfc-editor.org/rfc/rfc6189"
    title: Philip Zimmermann, Alan Johnston and Jon Callas, RFC 6189, ZRTP, Media Path Key Agreement for Unicast Secure RTP, April 2011
    locator: the hash commitment in the Commit message and the short authentication string that users compare by voice
  - book: isbn:9783662581452
    title: Colin Boyd, Anish Mathuria and Douglas Stebila, Protocols for Authentication and Key Establishment, second edition, Springer, 2020
    locator: Chapter 1 (adversary capabilities and typical attacks on key establishment)
---

A man-in-the-middle attack is an attack in which an active adversary sits on the path between two parties, takes part in the protocol with each of them on its own, and relays, reads or changes their messages, while each party believes it talks directly to the other. Against plain [Diffie-Hellman](/diffie-hellman/) it is complete: the attacker ends with one key shared with Alice and another shared with Bob, and decrypts and re-encrypts all traffic. No protocol can stop it unless the parties hold some authentic data in advance, such as a public key, a shared password or a channel that the attacker cannot change; this is the reason for [authenticated key exchange](/authenticated-key-exchange/).

**Notation.** Alice and Bob are the honest parties, and Mallory is the attacker. $g$ generates a group of prime order $q$. $a$, $b$, $m_1$ and $m_2$ are secret exponents; $A = g^a$, $B = g^b$, $M_1 = g^{m_1}$ and $M_2 = g^{m_2}$. $K_A$ and $K_B$ are the keys that Alice and Bob end with, and $\mathrm{KDF}$ is a key derivation function.

## In plain words

Alice and Bob send each other locks so that they can make a shared secret. Mallory sits between them on the line. She stops Alice's lock and sends Bob her own lock, and she stops Bob's lock and sends Alice another lock of her own.

Now Alice shares a secret with Mallory and thinks it is Bob, and Bob shares a different secret with Mallory and thinks it is Alice. Each message Alice sends, Mallory opens, reads, changes if she likes, locks again for Bob, and sends on. Nobody sees anything wrong.

The cure is to check who sent each lock: with a signature from a known key, a password both people know, or a short code they compare by voice.

## The idea

**The attack on Diffie-Hellman.** Mallory controls the network. The attack follows HAC, Section 12.9.1, Attack 1.

```pseudo id=main
MALLORY(label, msg)                          ▷ runs on every message on the wire
L1  if label = "A" then keep A; send M1 = g^{m1} to Bob instead
L2  if label = "B" then send M2 = g^{m2} to Alice instead
L3      K_A ← KDF(A^{m2})                    ▷ Alice computes KDF(M2^a), the same value
L4      K_B ← KDF(B^{m1})                    ▷ Bob computes KDF(M1^b), the same value
L5  if label = "data" then decrypt with K_A, read or change, encrypt with K_B, forward
```

Alice computes $K_A = \mathrm{KDF}(M_2^a) = \mathrm{KDF}(g^{a m_2})$, and Mallory computes the same value as $\mathrm{KDF}(A^{m_2})$. Bob and Mallory share $K_B = \mathrm{KDF}(g^{b m_1})$ in the same way. Both honest parties complete the protocol with no error, since each received a valid group element. Validation of the values (as in the [small subgroup attack](/small-subgroup-attack/)) does not help, because $M_1$ and $M_2$ are honest values.

**Why it cannot be stopped without prior trust.** Suppose Alice and Bob share no secret and hold no authentic public data about each other. Then everything Alice sees is a function of the messages she gets, and Mallory can produce those messages by running Bob's algorithm herself with her own coins. Alice's view of a run with Mallory has the same distribution as her view of a run with Bob, so no test that Alice can make tells them apart. The same holds for Bob. So every defence starts from something authentic: HAC (Definition 12.6 and Section 12.2.3) calls the needed property key authentication, and Diffie and Hellman (1976) already assumed an authentic public file of keys.

**Defences.**

- **Signatures over the transcript.** Each party signs the exchanged values (and its own and its peer's identity) with a key certified by an authority. Mallory cannot sign $(A, M_2)$ in Bob's name. This is the [station-to-station protocol](/station-to-station-protocol/), [SIGMA](/sigma-key-exchange/), and the TLS 1.3 CertificateVerify message. The signature must cover the identities too, or an [unknown key-share attack](/unknown-key-share-attack/) remains.
- **Static Diffie-Hellman keys.** Mixing in a certified long-term key gives implicit authentication: only the owner of that key can compute the session key ([MQV](/mqv/), [HMQV](/hmqv/), [Noise](/noise-protocol-framework/), [X3DH](/x3dh/)).
- **Passwords.** A [password-authenticated key exchange](/password-authenticated-key-exchange/) lets two parties who share only a short password run DH so that Mallory can test one password guess per active attempt.
- **Short authentication strings.** After the exchange, both users compare a short code derived from the key, by voice or on two screens. A man in the middle gives the two sides different keys, so their codes differ. The code is safe only if each side commits to its value before it sees the other's (ZRTP, RFC 6189, uses a hash commitment). Then Mallory, who must choose her values before she knows the result, matches a $k$-bit code with probability about $2^{-k}$ (Vaudenay, CRYPTO 2005). Without the commitment, she can try about $2^k$ values of $m_2$ offline until the two codes match.
- **The interlock protocol.** Rivest and Shamir (1984) send each encrypted message in two halves, the second only after the first half from the other side has arrived. Mallory must then send something to Bob before she can read Alice's message. This detects the attack only if the parties check the content of the messages, and later work broke it when used for authentication.
- **Key confirmation alone is not enough.** A MAC under the session key, as in [key confirmation](/key-confirmation/), shows only that the peer holds the same key. Mallory holds both keys, so she passes it.

## Examples

**Toy run.** The Python code of this page runs plain Diffie-Hellman in a toy safe-prime group with $p = 140737488356903$ on a simulated network that Mallory controls. Alice and Bob each end with a key and no error. Alice sends the encrypted text "pay 10 to Alice"; Mallory decrypts it, logs it, changes "Alice" to "Mallory", re-encrypts, and Bob decrypts "pay 10 to Mallory" with no error. When the two users compare a 20-bit code from their keys, the codes differ in each of 20 runs (Mallory in this code does not search for matching codes). When Bob signs the pair $(A', B)$ that he saw with a toy Schnorr key that Alice already trusts, Alice checks the signature on $(A, B')$, the pair she saw, and rejects. The code is for study only: the group is far too small, nothing is constant time, and every party is a local simulation.

**Wi-Fi with a shared password.** WPA2-Personal derives its keys from the passphrase, so an attacker without the passphrase cannot sit in the middle. An attacker who knows it, such as another guest on the same network, can set up an access point with the same name.

**TLS with a bad certificate check.** A client that does not check the server's certificate chain or host name runs authenticated TLS in name only. Interception proxies in companies and some malware install their own root certificate on the client and then act as a man in the middle on purpose.

**Non-example: eavesdropping.** An attacker who only records traffic is passive. Plain Diffie-Hellman resists her, because she sees $A$ and $B$ but must solve the [CDH problem](/computational-diffie-hellman/) to get the key.

## Where it is used

- **Threat models.** Every analysis of a key exchange protocol states whether the adversary is passive or a man in the middle. The models of Bellare and Rogaway and of Canetti and Krawczyk give the adversary full control of the network ([session key](/session-key/)).
- **TLS, SSH and IKE.** TLS uses certificates; SSH uses trust on first use, where the client stores the server's host key the first time and warns if it changes; IKEv2 uses certificates, pre-shared keys or EAP.
- **Messaging.** [Signal](/signal-protocol/) and similar apps show a safety number that two users can compare in person to rule out a man in the middle at the server.
- **Device pairing.** Bluetooth numeric comparison and passkey entry show a short code on both devices for the user to compare or type.
- **Attack tools.** ARP spoofing, rogue access points and DNS spoofing put an attacker on the path, after which a weak protocol falls to the attack above.

## References
