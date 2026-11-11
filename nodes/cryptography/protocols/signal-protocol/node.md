---
tag: EQ8HBA
kind: algorithm
slug: signal-protocol
name: Signal protocol
aliases:
- Signal messaging protocol
- TextSecure protocol
area: cryptography/protocols
level: advanced
summary: End-to-end encrypted messaging that joins the X3DH or PQXDH handshake with the Double Ratchet, for forward secrecy, post-compromise security and deniability between offline peers.
solves: [secure-messaging]
model: word-ram
complexity:
  vars: {n: the number of messages in a session, s: the number of message keys stored for messages that have not arrived}
  time: {worst: O(n), average: O(n), best: O(n)}
  space: {extra: O(s)}
properties: {deterministic: false, randomized: true}
history:
  year: 2016
  people: [Trevor Perrin, Moxie Marlinspike]
  note: The ratchet, first called Axolotl, went into TextSecure in 2014; the X3DH and Double Ratchet specifications were published in 2016, and Sesame in 2017.
prereqs: [x3dh, double-ratchet]
see_also: [secure-messaging, perfect-forward-secrecy, key-ratchet, ed25519, tls-handshake, noise-protocol-framework, hybrid-key-exchange, anonymous-communication]
sources:
  - url: "https://signal.org/docs/specifications/x3dh/"
    title: Moxie Marlinspike and Trevor Perrin, The X3DH Key Agreement Protocol, revision 1, 2016
    locator: Section 2 (prekey bundles and the KDF), Section 3 (the protocol), Section 4 (security considerations, including deniability and the role of the server)
  - url: "https://signal.org/docs/specifications/doubleratchet/"
    title: Trevor Perrin and Moxie Marlinspike, The Double Ratchet Algorithm, revision 1, 2016
    locator: Section 3 (the algorithm with skipped message keys), Section 5.2 (recommended cryptographic algorithms)
  - url: "https://signal.org/docs/specifications/sesame/"
    title: Moxie Marlinspike and Trevor Perrin, The Sesame Algorithm, Session Management for Asynchronous Message Encryption, revision 2, 2017
    locator: Section 2 (users, devices and sessions) and Section 3 (the algorithm)
  - url: "https://signal.org/docs/specifications/pqxdh/"
    title: Ehren Kret and Rolfe Schmidt, The PQXDH Key Agreement Protocol, 2023
    locator: the X3DH variant with an added post-quantum KEM key in the prekey bundle
  - paper: doi:10.1007/s00145-020-09360-1
    title: Katriel Cohn-Gordon, Cas Cremers, Benjamin Dowling, Luke Garratt and Douglas Stebila, A formal security analysis of the Signal messaging protocol, Journal of Cryptology 33(4), 2020, pages 1914 to 1983
    locator: the multi-stage model with ratchet stages, and the proof of secrecy with forward secrecy and post-compromise security; the first version was at IEEE EuroS&P 2017
  - paper: "Katriel Cohn-Gordon, Cas Cremers and Luke Garratt, On post-compromise security, IEEE Computer Security Foundations Symposium (CSF) 2016"
    locator: the definition of post-compromise security and the argument that a ratchet with fresh Diffie-Hellman values achieves it
  - paper: "Joël Alwen, Sandro Coretti and Yevgeniy Dodis, The Double Ratchet: security notions, proofs, and modularization for the Signal protocol, Eurocrypt 2019, LNCS 11476, pages 129 to 158"
    locator: the security notions for secure messaging with immediate decryption of out-of-order messages
  - url: "https://signal.org/blog/sealed-sender/"
    title: Signal, Technology preview, sealed sender for Signal, October 2018
    locator: the sender certificate inside the encrypted envelope and the delivery tokens
---

The Signal protocol is the end-to-end encryption of the Signal messenger, also used by WhatsApp, Google Messages and others. It joins two parts. The [X3DH](/x3dh/) handshake (or PQXDH, its post-quantum version) gives two users a shared secret even when the receiver is offline, using keys that the receiver left on a server. The [Double Ratchet](/double-ratchet/) then derives a new key for every message, and mixes in a new Diffie-Hellman value each time the direction of the talk changes. The result has forward secrecy, heals after a compromise, accepts messages in any order, and leaves no signature that proves who wrote a message. This page is about the composition; the two parts have their own pages.

**Notation.** Alice starts a session with Bob. $IK$ is an identity key, $SPK_B$ Bob's signed prekey, $OPK_B$ a one-time prekey and $EK_A$ Alice's ephemeral key, all X25519 key pairs. $\mathrm{DH}(a, B)$ is X25519. $SK$ is the X3DH output and $AD = IK_A \| IK_B$ the associated data. In the ratchet, $DH_s$ is a party's current ratchet key pair, $DH_r$ the other party's current ratchet public key, $RK$ the root key, $CK_s$ and $CK_r$ the sending and receiving chain keys, $N_s$, $N_r$ and $PN$ the message counters, and MAX_SKIP the most message keys that one receive may store.

## In plain words

Bob leaves a box of padlocks at the post office before he goes to sleep. Alice takes one padlock, mixes it with her own keys and with Bob's lasting key, and gets a secret that only Bob can also work out. She sends her first letter at once.

Then every letter has its own key, made from the last key by a one-way step and thrown away after use. Each answer carries a new padlock, and both mix a new secret into the chain. A thief who copies Alice's phone can read only until the next mixing, and old letters stay closed because their keys are gone. Late letters still open, because the receiver keeps the keys of missing letters for a time. No letter is signed, so Bob cannot prove to a judge that Alice wrote it.

## The problem

Two users want to exchange messages through a server they do not trust with the content. Either of them may be offline when the other writes, and each may have several devices. The messages must stay secret and authentic; old messages must stay secret if a device is stolen later ([forward secrecy](/perfect-forward-secrecy/)); new messages must become secret again after an attacker who copied a device stops watching (post-compromise security); messages may arrive late, twice or in any order; and the transcript should not prove to a third party who said what (deniability). This is the [secure messaging](/secure-messaging/) problem for two parties.

## The algorithm

```pseudo id=main
Setup and handshake (X3DH)                                          ▷ X3DH Sections 2 and 3
L1  B: publish IK_B, SPK_B, Sig(IK_B, SPK_B) and a set of one-time prekeys OPK_B on the server
L2  A: fetch Bob's bundle with one OPK_B, which the server then deletes; verify the signature on SPK_B, else abort
L3  A: EK_A ← random; SK ← KDF(DH(IK_A, SPK_B) ∥ DH(EK_A, IK_B) ∥ DH(EK_A, SPK_B) ∥ DH(EK_A, OPK_B)); AD ← IK_A ∥ IK_B; erase EK_A
L4  A: DH_s ← random; RK, CK_s ← KDF_RK(SK, DH(DH_s, SPK_B)); send IK_A, EK_A and the OPK id with the first message (line L7)
L5  B: delete OPK_B, or abort if it is unknown; compute SK from the same four values with his private keys
L6  B: DH_s ← SPK_B; RK ← SK; receive the first message (lines L8 to L11); on failure erase SK
Each message (Double Ratchet)                                        ▷ Double Ratchet Section 3
L7  send m: CK_s, mk ← KDF_CK(CK_s); header ← (DH_s.public, PN, N_s); N_s ← N_s + 1; c ← AEAD(mk, m, AD ∥ header)
L8  receive (header, c): if a skipped key is stored for (header.dh, header.n), decrypt with it, delete it and stop
L9  if header.dh ≠ DH_r: store the keys of the rest of the current receiving chain up to header.pn, then do line L10
L10 DH ratchet: PN ← N_s; N_s, N_r ← 0; DH_r ← header.dh; RK, CK_r ← KDF_RK(RK, DH(DH_s, DH_r)); DH_s ← random; RK, CK_s ← KDF_RK(RK, DH(DH_s, DH_r))
L11 store the keys up to header.n (at most MAX_SKIP); CK_r, mk ← KDF_CK(CK_r); N_r ← N_r + 1; decrypt c, else restore the state from before line L9 and reject
```

**The handshake.** X3DH lets Alice start while Bob is offline (lines L1 to L5). The first value $\mathrm{DH}(IK_A, SPK_B)$ authenticates Alice and the second $\mathrm{DH}(EK_A, IK_B)$ authenticates Bob, in the way of an implicitly authenticated key exchange; the third and fourth give forward secrecy. The one-time prekey also stops a replay of the first message: once Bob has deleted it in line L5, the same first message is rejected. If the server has run out of one-time prekeys, X3DH runs with three values, and the first message can be replayed to Bob until he replaces his signed prekey.

**The composition.** The X3DH output $SK$ becomes the first root key, and Bob's signed prekey becomes his first ratchet key (lines L4 and L6). So Alice can send at once, and Bob's first DH ratchet step already mixes Alice's fresh ratchet key with $SPK_B$. $AD$ is bound into every message, so a message is accepted only in a session between these two identity keys.

**The ratchets.** The symmetric ratchet (line L7, and KDF_CK in line L11) gives each message its own key and moves the chain forward with a one-way function, which gives forward secrecy within a chain. The DH ratchet (line L10) runs when a message with a new ratchet key arrives: the receiver mixes $\mathrm{DH}$ of its old key and the new key into the root key, picks a fresh key pair, and mixes $\mathrm{DH}$ again. This gives post-compromise security: one round trip after the attacker stops watching, the new root key depends on a Diffie-Hellman value that it cannot compute. Skipped message keys (lines L8, L9 and L11) let a message open after later ones.

**Sesame and sealed sender.** Real users have several devices, and each pair of devices runs its own session. Sesame (Marlinspike and Perrin, 2017) is the session management layer: each device keeps a record of sessions per user and device, sends each message to every device of the receiver and of the sender, decides which session is active when both sides start one at the same time, and drops sessions of devices that are removed. Sealed sender (2018) hides the sender's identity from the server: the sender's certificate goes inside the encrypted envelope, and the server checks a delivery token instead of the sender's login. The server still sees the receiver, the time and the sender's network address.

**About the code.** The Python code is for study only. It is not constant time and must not protect real data; use libsignal. It composes a minimal X3DH and a minimal Double Ratchet for one device per user, so there is no Sesame, sealed sender, header encryption or PQXDH. The signed prekey is signed with a separate Ed25519 key, not with the X25519 identity key through XEdDSA as in Signal. Keys are raw 32-byte strings without the type byte of the Signal encoding, and messages use a study AEAD (encrypt-then-MAC with an HMAC-SHA256 key stream), not the AES-256-CBC with HMAC-SHA256 of the specification. The Signal specifications have no test vectors; the local X25519 and Ed25519 are checked with RFC 7748 and RFC 8032.

## Example

A run of the code. $A_i$ and $B_i$ are the ratchet keys of Alice and Bob, and $B_0 = SPK_B$.

| Step | Line | Event | Result |
|---|---|---|---|
| 1 | L1 | Bob publishes $IK_B$, $SPK_B$, the signature and five one-time prekeys | the server holds the bundle |
| 2 | L2 to L4 | Alice takes $OPK_0$, computes $SK$ and sends "hi bob" with header $(A_1, 0, 0)$ | her chain key is KDF_RK$(SK, \mathrm{DH}(A_1, B_0))$ |
| 3 | L5, L6, L10 | Bob deletes $OPK_0$, computes $SK$ and ratchets on $A_1$ | he reads "hi bob"; a copy of step 2 is now rejected |
| 4 | L7 | Bob sends "late" and "on time" with headers $(B_1, 0, 0)$ and $(B_1, 0, 1)$ | |
| 5 | L9 to L11 | Alice receives "on time" first | she ratchets on $B_1$ and stores the key of $(B_1, 0)$ |
| 6 | L8 | "late" arrives after one more round trip | it opens with the stored key; a second copy fails |
| 7 | | an attacker copies Alice's state, which holds her current private ratchet key $A$ | |
| 8 | L7, L10 | Alice sends $a_1$; Bob ratchets to a fresh $B$ and replies $b_1$ under $\mathrm{DH}(A, B)$ | the attacker reads $a_1$ and $b_1$ |
| 9 | L10 | Alice ratchets to a fresh $A'$ and sends $a_2$; Bob replies $b_2$ | the attacker can read neither: healed |
| 10 | | an attacker copies Bob's state later | the messages recorded in step 6 and before stay closed |

## Correctness

**Claim.** If both parties follow the protocol and the server delivers the right bundle, every message that arrives unchanged decrypts to what was sent, exactly once, in any order, as long as one receive skips at most MAX_SKIP messages. X3DH gives both parties the same $SK$, because each of the four Diffie-Hellman values is the same from both ends. After that the two ratchet states move in step: each DH ratchet step on one side computes the value that the sender used, and each chain step is a deterministic function. A late message finds its key in the table of skipped keys, which the receiver filled when it moved past that message.

**Forward secrecy and healing.** A message key is derived by a one-way step and deleted after use, so a state stolen later does not give it. After a compromise, the first DH ratchet step with a ratchet key that the attacker never saw gives a root key that depends on a Diffie-Hellman value the attacker cannot compute. The proof page states and proves both claims, with random oracles for the KDFs.

**Security.** Cohn-Gordon, Cremers, Dowling, Garratt and Stebila (EuroS&P 2017, J. Cryptology 2020) model Signal as a multi-stage key exchange in which each ratchet step is a stage. They prove that every message key is secret, with forward secrecy and post-compromise security, under the Diffie-Hellman assumptions and with the KDFs as random oracles. The model leaves out Sesame, sealed sender and the authentication of identity keys, which users check by comparing safety numbers.

## Complexity

Each message costs one KDF_CK step to send and one to receive. A DH ratchet step adds two X25519 operations and two KDF_RK steps, at most once per message. A receive that skips $k$ messages costs $k$ more KDF_CK steps, and each skipped key is made once and used once. So a session with $n$ messages costs $O(n)$ time in total, with constant cost for each curve operation on the fixed curve. A party stores its ratchet state, which has constant size, and the $s$ skipped keys of messages that have not arrived, which MAX_SKIP and a time limit bound in practice. The handshake costs four X25519 operations on each side and one signature check for Alice.

## Properties

- **Asynchronous start.** Alice needs only Bob's bundle from the server, not Bob himself.
- **Forward secrecy.** Message keys are deleted after use; the one-time prekey and the ephemeral key are deleted after the handshake.
- **Post-compromise security.** A passive attacker with a copied state loses access after one round trip of fresh ratchet keys.
- **Deniability.** No message is signed by its author. Bob can make a first message "from Alice" with Alice's public identity key alone, because he can compute each of the four Diffie-Hellman values from his own private keys. So a transcript does not prove to a third party that Alice took part.
- **Immediate decryption.** A message decrypts when it arrives, even if earlier messages are lost or late.
- **Trust in the key server.** A server that replaces both the signing key and the prekeys of Bob can run a man-in-the-middle attack. Users detect it only by comparing safety numbers, the fingerprints of the identity keys.

## Variants and improvements

- **PQXDH.** Since 2023, Signal adds a post-quantum KEM key (ML-KEM, first as Kyber-1024) to the prekey bundle, and mixes the KEM secret into $SK$. This protects the handshake against an attacker who records it now and has a quantum computer later; the ratchet itself still uses X25519.
- **Header encryption.** The Double Ratchet specification encrypts the headers with header keys from the root chain, so the server does not see the ratchet keys and counters.
- **Groups.** Signal groups use pairwise sessions for control messages and sender keys, a symmetric chain per sender that the sender distributes over the pairwise sessions. Sender keys have forward secrecy but no post-compromise security. MLS (RFC 9420) is a group protocol with both.
- **Other apps.** WhatsApp, the Facebook Messenger secret conversations and Google Messages use the Signal protocol with their own session management.

## When to use it

Use the Signal protocol, through libsignal, for end-to-end encrypted chat between users whose devices are often offline. For groups of many members, consider MLS. For a connection between a client and a server that are online at the same time, use the [TLS handshake](/tls-handshake/) or a Noise pattern instead: they are simpler and need no prekey server.

## Pitfalls

- **Unverified identity keys.** Without a comparison of safety numbers, the key server can replace a user's keys and read all messages. Show a warning when a contact's identity key changes.
- **One-time prekeys run out.** Without them, the first message can be replayed and loses some forward secrecy. Upload new ones in time and rotate the signed prekey.
- **Keeping skipped keys too long.** Skipped message keys are a store of keys for messages not yet read; a thief gets them. Bound their number with MAX_SKIP and delete them after a time.
- **State rollback.** A device restored from a backup reuses old chain keys and counters, which can repeat message keys. Never restore ratchet state from a backup; start new sessions.
- **Not rolling back on failure.** A forged message with a new ratchet key must not change the state; the code saves the state before line L9 and restores it when decryption fails.
- **Metadata.** The protocol hides content, not who talks to whom and when; sealed sender hides only part of it from the server.

## Implementations

## History

Open Whisper Systems, founded by Moxie Marlinspike, released TextSecure for Android in 2010. In 2013 and 2014 Trevor Perrin and Marlinspike designed the Axolotl ratchet, which combines the per-message key updates of SCIMP, the Silent Circle instant messaging protocol, with the Diffie-Hellman ratchet of Off-the-Record messaging, and TextSecure version 2 used it from 2014. WhatsApp added the protocol for all its users in 2016. The X3DH and Double Ratchet specifications were published in November 2016, the formal analysis by Cohn-Gordon et al. appeared at EuroS&P 2017, and Sesame followed in 2017. Sealed sender came in 2018, and PQXDH in 2023.

## References
