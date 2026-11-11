---
tag: 8PE1DX
kind: problem
slug: secure-messaging
name: Secure messaging
aliases:
- end-to-end encrypted messaging
area: cryptography/protocols
level: advanced
summary: Let users exchange messages through untrusted servers so that only the ends can read them, with forward secrecy, recovery after a compromise, and trust in the right keys.
prereqs: [perfect-forward-secrecy, authenticated-key-exchange]
see_also: [signal-protocol, double-ratchet, x3dh, key-ratchet, group-key-agreement-problem, tree-based-group-diffie-hellman, merkle-tree, anonymous-communication]
sources:
  - paper: "Nik Unger, Sergej Dechand, Joseph Bonneau, Sascha Fahl, Henning Perl, Ian Goldberg and Matthew Smith, SoK: secure messaging, IEEE Symposium on Security and Privacy 2015, pages 232 to 249"
    locator: the three problem areas (trust establishment, conversation security, transport privacy), the list of security, usability and adoption properties, and the evaluation of existing apps
  - paper: doi:10.1145/1029179.1029200
    title: Nikita Borisov, Ian Goldberg and Eric Brewer, Off-the-record communication, or, why not to use PGP, Workshop on Privacy in the Electronic Society (WPES) 2004, pages 77 to 84
    locator: perfect forward secrecy with short-lived Diffie-Hellman keys, repudiation with MACs instead of signatures, and the publication of old MAC keys
  - paper: "Katriel Cohn-Gordon, Cas Cremers and Luke Garratt, On post-compromise security, IEEE Computer Security Foundations Symposium (CSF) 2016"
    locator: the definition of post-compromise security and the conditions under which it can be reached
  - url: "https://www.rfc-editor.org/rfc/rfc9420"
    title: Richard Barnes, Benjamin Beurdouche, Raphael Robert, Jon Millican, Emad Omara and Katriel Cohn-Gordon, RFC 9420, The Messaging Layer Security (MLS) Protocol, July 2023
    locator: Section 7 (the ratchet tree and TreeKEM), Section 8 (the key schedule), Section 12 (proposals and commits)
  - paper: "Marcela S. Melara, Aaron Blankstein, Joseph Bonneau, Edward W. Felten and Michael J. Freedman, CONIKS: bringing key transparency to end users, USENIX Security Symposium 2015, pages 383 to 398"
    locator: the Merkle prefix tree of name to key bindings, signed tree roots per epoch, and the monitoring and auditing of the directory
  - paper: "Alma Whitten and J. D. Tygar, Why Johnny can't encrypt: a usability evaluation of PGP 5.0, USENIX Security Symposium 1999"
    locator: the user study in which most users failed to encrypt and sign mail correctly with PGP
  - paper: "Joël Alwen, Sandro Coretti and Yevgeniy Dodis, The Double Ratchet: security notions, proofs, and modularization for the Signal protocol, Eurocrypt 2019, LNCS 11476, pages 129 to 158"
    locator: the definition of secure messaging with immediate decryption, and continuous key agreement as the building block
---

Secure messaging is the problem of letting people send each other messages, through servers that they do not trust, so that only the sender and the receivers can read and change them. The servers store and forward the messages, often while the receiver is offline. A solution must keep messages secret over years of use, in which phones are lost, stolen or copied, so it needs [forward secrecy](/perfect-forward-secrecy/) for old messages and a way to make new messages secret again after a compromise. It must also tie each key to the right person, which is a problem of its own. This page states the problem and its parts. The [Signal protocol](/signal-protocol/) is the main solution for two parties, and MLS for groups.

## In plain words

You want to send letters that only your friend can read, but every letter passes through a post office that opens what it can. You and your friend each have a lock, and the post office hands out copies of the locks. So first you must be sure that the lock you got is your friend's and not the post office's.

Then, over months, a thief may copy your desk drawer of keys one night. A good system makes that copy almost useless: the keys for old letters were thrown away, and the keys for new letters change soon after, in a way the thief cannot follow. It also lets letters arrive late or out of order, and does not leave a signature that proves to others what you wrote.

## Definition

There are users, each with one or more devices, a set of servers, and an adversary. A *conversation* is a sequence of messages among two or more users. The adversary controls the network and the servers: it reads, delays, drops, reorders and injects messages. At chosen times it may also learn the long-term keys of a user, or the full state of a device (a compromise). A secure messaging scheme gives each device algorithms to set up a conversation, to send a message and to receive one, and it should reach these goals:

- **Confidentiality.** The adversary learns nothing about the content of a message, except its length, unless it holds the state of a device that is entitled to read it at the time.
- **Integrity and authentication.** A device accepts a message as from user $U$ in a conversation only if $U$ sent it in that conversation.
- **Forward secrecy.** A compromise at time $t$ does not expose messages sent and received before $t$.
- **Post-compromise security.** If the adversary compromises a device at time $t$ and then stays passive, messages sent after some later time $t'$ are secret again. $t'$ is reached after the device has used fresh randomness that the adversary did not see, for example one round trip in the Double Ratchet.
- **Asynchronicity and immediate decryption.** A sender can start a conversation and send while the receiver is offline. A message can be decrypted when it arrives, even if earlier messages are lost or late.
- **Deniability.** The transcript does not prove to a third party who sent a message, because the receiver could have made it too.
- **Trust establishment.** Each user gets the right long-term public key of each partner, or detects a wrong one.

Unger et al. (IEEE S&P 2015) split the field into three problems: trust establishment, conversation security (the goals above), and transport privacy (hiding who talks to whom, see [anonymous communication](/anonymous-communication/)).

## Variants

- **Two-party and group.** In a group, a message goes to many devices, members join and leave, and the scheme must keep removed members out (forward secrecy for the group) and heal after a compromise of one member. The key part is continuous group key agreement, solved by TreeKEM in MLS; see the [group key agreement problem](/group-key-agreement-problem/).
- **Synchronous and asynchronous.** In the synchronous setting both parties are online, as in OTR; in the asynchronous setting a server holds prekeys for offline receivers, as in [X3DH](/x3dh/).
- **Multi-device.** Each user has several devices that must all receive each message; Signal runs a session per pair of devices (Sesame), while some systems share keys among a user's devices.
- **Strength of the adversary.** Models differ in what a compromise reveals (long-term keys only, or also session state and randomness) and in whether the adversary may be active after the compromise.
- **Metadata privacy.** Stronger variants also hide who talks to whom and when, from the servers.

## Examples

**PGP and its limits.** OpenPGP (Zimmermann, 1991; RFC 4880) encrypts each mail to the receiver's long-term key and signs it with the sender's. It needs no online server, but every message is encrypted under the same long-term key, so a key stolen later opens all recorded mail: no forward secrecy and no post-compromise security. The signatures are non-repudiable, so they prove authorship to anyone. Key distribution relies on a web of trust or on key servers, and the user study of Whitten and Tygar (1999), "Why Johnny can't encrypt", found that most users could not use PGP correctly.

**OTR.** Off-the-Record messaging (Borisov, Goldberg and Brewer, WPES 2004) was designed as an answer to these limits for chat. It runs authenticated Diffie-Hellman exchanges and replaces the keys often, so a later theft does not expose old messages; it authenticates messages with MACs instead of signatures, and publishes old MAC keys after use, so anyone could have made an old message. OTR needs both parties online.

**A harness for FS and PCS.** The Python code is a study harness, not a protocol to use. It is not constant time; for real messaging use libsignal or an MLS library. It runs four toy protocols on 16 messages that alternate between Alice and Bob, copies Alice's full state just before message 6, and lets the attacker read every later record without sending. The attacker tries to open earlier records with the copy, and runs the copy forward on later records with its own random values where the real party drew fresh ones. A new session (for the protocol that has sessions) starts every four messages.

| Toy protocol | Earlier messages exposed | Later messages exposed | FS | PCS |
|---|---|---|---|---|
| static long-term key | 0 to 5 | 6 to 15 | no | no |
| fresh Diffie-Hellman per session (OTR-like) | 4, 5 (this session) | 6, 7 (to the end of this session) | per session | at the next session |
| hash ratchet only | none | 6 to 15 | yes | no |
| hash ratchet with a Diffie-Hellman ratchet | none | 6, 7 | yes | after one round trip |

The table shows that the two goals need different tools. Forward secrecy comes from deleting keys after a one-way step, which the hash ratchet does. Post-compromise security needs new randomness that the attacker never sees, mixed in through a key exchange, which a hash chain alone cannot give.

## Known algorithms

- **PGP and S/MIME.** Long-term keys, no forward secrecy, non-repudiable signatures.
- **OTR (2004).** Synchronous two-party chat with Diffie-Hellman key updates, forward secrecy and deniability.
- **SCIMP and sender keys.** Symmetric hash ratchets: forward secrecy, no post-compromise security.
- **The [Signal protocol](/signal-protocol/).** [X3DH](/x3dh/) or PQXDH for an asynchronous start, and the [Double Ratchet](/double-ratchet/) for per-message keys with forward secrecy and post-compromise security. Used by Signal, WhatsApp and others.
- **MLS.** The Messaging Layer Security protocol (RFC 9420, July 2023) handles groups of up to many thousands of members. Its core is TreeKEM, a binary tree of public keys over the members, an idea that goes back to [tree-based group Diffie-Hellman](/tree-based-group-diffie-hellman/): to update its key, a member sends new secrets along the path from its leaf to the root, encrypted to the sibling subtrees, so an update or a removal costs $O(\log n)$ public-key encryptions in a balanced tree instead of $O(n)$. Each commit moves the group to a new epoch with a new key schedule, which gives forward secrecy and post-compromise security for the group. MLS also authenticates members with credentials and signatures, and leaves the delivery service and the authentication service to the application.
- **Key transparency.** CONIKS (Melara et al., USENIX Security 2015) attacks the trust establishment part. The provider keeps the bindings of user names to public keys in a Merkle prefix tree, publishes a signed root of the tree each epoch, and links each root to the previous one. Each client checks, with a short proof, that its own key is in the tree as it should be (monitoring), and that it sees the same root as other clients (auditing). A provider that gives a false key to one user must then either show that key to its owner, or show different roots to different users, both of which can be detected. Later systems, such as the key transparency of WhatsApp, follow this design.

## Bounds

- **PCS needs fresh randomness and a passive window.** If the adversary has a device's full state and the device uses no new randomness, the adversary can compute everything the device computes, so no deterministic scheme heals. If the adversary stays active after the compromise, it can impersonate the device to its partners with the stolen state, and no scheme can tell the two apart; healing then depends on the real device also talking and being detected (Cohn-Gordon, Cremers and Garratt, CSF 2016).
- **Immediate decryption against forward secrecy.** To decrypt late messages, a receiver must keep their keys until they arrive, and those keys are exposed by a compromise in the meantime. Schemes bound the number and the age of stored keys.
- **Optimal security has a cost.** Schemes that heal at the first message from the other side, under any interleaving, need stronger primitives such as key-updatable public-key encryption, and cost more than the Double Ratchet (Jaeger and Stepanovs, and Poettering and Rösler, both Crypto 2018).
- **Groups.** In TreeKEM, an update costs $O(\log n)$ in the best case but $O(n)$ when the tree has many empty nodes, and lower bounds for continuous group key agreement with strong security in general trees are an active field.

## Reductions

- Two-party secure messaging with immediate decryption reduces to a continuous key agreement, a forward-secure authenticated encryption and a PRF-PRNG for the root chain (Alwen, Coretti and Dodis, Eurocrypt 2019). The Double Ratchet is one instance.
- The start of a conversation is an [authenticated key exchange](/authenticated-key-exchange/); asynchronous starts need prekeys, as in X3DH.
- Group messaging reduces to continuous group key agreement plus a symmetric key schedule per epoch, as in MLS.
- Trust establishment reduces to an authenticated directory: a key transparency log, a certificate authority, or the manual comparison of fingerprints.

## Applications

End-to-end encryption protects the chats and calls of Signal, WhatsApp, iMessage, Facebook Messenger, Google Messages, Wire and Matrix, and the Signal protocol or MLS underlies most of them. Email remains mostly without forward secrecy: OpenPGP and S/MIME are used where long-term archives and signatures are needed. MLS is deployed in some business chat products and is the basis of work on interoperable messaging between large providers.

## References
