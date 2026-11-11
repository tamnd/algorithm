---
tag: EE0J5J
kind: concept
slug: key-ratchet
name: Key ratchet
aliases:
- hash ratchet
- KDF chain
- symmetric-key ratchet
area: cryptography/key-exchange
level: advanced
summary: A key that only moves forward. A KDF chain gives a new key per message and forgets the old one (forward secrecy); a Diffie-Hellman ratchet adds fresh secrets so the keys heal after a leak.
prereqs: [perfect-forward-secrecy, hkdf, diffie-hellman]
see_also: [double-ratchet, x3dh, hash-chain, signal-protocol, secure-messaging, x25519, hmac, tree-based-group-diffie-hellman]
sources:
  - url: "https://signal.org/docs/specifications/doubleratchet/"
    title: Trevor Perrin and Moxie Marlinspike, The Double Ratchet Algorithm, revision 1, 2016-11-20
    locator: Section 2.1 (KDF chains), Section 2.2 (symmetric-key ratchet), Section 2.3 (Diffie-Hellman ratchet), Section 5.2 (recommended algorithms, HMAC with the constants 0x01 and 0x02 for the chain key and HKDF for the root key)
  - paper: "Mihir Bellare and Bennet Yee, Forward-security in private-key cryptography, CT-RSA 2003, LNCS 2612"
    locator: forward-secure pseudorandom generators and the key evolution that the KDF chain uses
  - paper: "Nikita Borisov, Ian Goldberg and Eric Brewer, Off-the-record communication, or, why not to use PGP, ACM Workshop on Privacy in the Electronic Society 2004"
    locator: the OTR protocol, which changes the Diffie-Hellman keys during a conversation, an early Diffie-Hellman ratchet
  - paper: "Katriel Cohn-Gordon, Cas Cremers and Luke Garratt, On post-compromise security, IEEE Computer Security Foundations Symposium (CSF) 2016"
    locator: the definition of post-compromise security and the result that it needs state that changes with fresh randomness, as in a Diffie-Hellman ratchet
  - url: "https://www.rfc-editor.org/rfc/rfc7748"
    title: Adam Langley, Mike Hamburg and Sean Turner, RFC 7748, Elliptic Curves for Security, January 2016
    locator: Section 5 (the X25519 function) and Section 5.2 (test vectors), used by the code
  - url: "https://www.rfc-editor.org/rfc/rfc5869"
    title: Hugo Krawczyk and Pasi Eronen, RFC 5869, HMAC-based Extract-and-Expand Key Derivation Function (HKDF), May 2010
    locator: Section 2 (Extract and Expand) and Appendix A.1 (Test Case 1), used by the code
---

A key ratchet is a rule that replaces a secret key by a new one in a way that cannot be undone, like a ratchet wheel that turns only one way. There are two kinds. A KDF chain (also called a symmetric-key or hash ratchet) derives each new key from the previous one with a one-way function and then deletes the old key, so a thief who steals the current key cannot compute past keys: this is [forward secrecy](/perfect-forward-secrecy/) for each message. A Diffie-Hellman ratchet mixes a fresh [Diffie-Hellman](/diffie-hellman/) output into the key at each turn of a conversation, so a thief who stole the state loses access once the parties have done one exchange with new random values: this is post-compromise security, or healing. The [double ratchet](/double-ratchet/) of Signal combines both.

**Notation.** A chain key $ck$ and a root key $rk$ are 32-byte strings. $\mathrm{HMAC}(k, m)$ is [HMAC](/hmac/) with SHA-256; $\mathrm{HKDF}(\text{salt}, \text{ikm}, \text{info}, L)$ is [HKDF](/hkdf/) with SHA-256 and $L$ output bytes. $\mathrm{DH}(a, B)$ is [X25519](/x25519/) of a private key $a$ and a public key $B$. $mk$ is a message key, used once.

## In plain words

Think of a diary with a lock, where the key changes every day. Each morning you make tomorrow's key from today's key with a machine that works in one direction only, and you throw today's key away. If a thief takes your key today, it opens today's page and the pages after it, but not the pages before. That is the first kind of ratchet.

The second kind fixes the future. Two people who write to each other also add a fresh shared secret each time they take a turn. A thief who copied the keys once cannot follow along after the next fresh secret, because it never saw it. So the keys heal.

Messaging apps use both: the first for every message, the second for every turn of the conversation.

## The idea

**KDF chain.** A KDF chain is a sequence of chain keys $ck_0, ck_1, \ldots$ with $(ck_{i+1}, mk_{i+1}) = \mathrm{KDF}(ck_i)$. Each step gives one message key and the next chain key, and the holder deletes $ck_i$ at once. If KDF is a pseudorandom function keyed by $ck$, then given $ck_{i+1}$ the earlier values $ck_0, \ldots, ck_i$ and $mk_1, \ldots, mk_i$ look random. The Double Ratchet specification, Section 5.2, recommends $mk = \mathrm{HMAC}(ck, \texttt{0x01})$ and $ck' = \mathrm{HMAC}(ck, \texttt{0x02})$: two independent PRF outputs, so a message key gives nothing about the next chain key.

**Diffie-Hellman ratchet.** Two parties share a root key $rk$. When a party starts a turn, it picks a fresh key pair $(a, A)$, sends $A$, and both sides update $(rk, ck) \leftarrow \mathrm{HKDF}(rk, \mathrm{DH}(a, B), \text{info}, 64)$, where $B$ is the last public key of the peer. The new $ck$ starts a KDF chain for the messages of this turn. When the peer replies, it picks its own fresh pair, and the update repeats. The root key is itself a chain, but each step adds a new DH output.

```pseudo id=main
KDF chain step(ck)                       ▷ Double Ratchet, Section 5.2
L1  mk ← HMAC-SHA256(ck, 0x01)
L2  ck' ← HMAC-SHA256(ck, 0x02)
L3  return (ck', mk); delete ck
DH ratchet, sender's turn(rk, B)
L4  a ← 32 random bytes               ▷ a fresh private key
L5  A ← X25519(a, 9)                   ▷ sent with the next message
L6  (rk, ck_send) ← HKDF(salt = rk, ikm = X25519(a, B), info, 64)
DH ratchet, receiver's turn(rk, b, A)
L7  B_peer ← A                          ▷ the new public key of the peer
L8  (rk, ck_recv) ← HKDF(salt = rk, ikm = X25519(b, B_peer), info, 64)
L9  return ck_recv                     ▷ equals the sender's ck_send
```

Lines L1 to L3 are the symmetric ratchet: the HMAC calls are one-way in $ck$, and line L3 deletes the input. Lines L4 to L6 are the sender's half of a DH ratchet step: the fresh private key of line L4 is what an earlier thief does not know. Lines L7 to L9 are the receiver's half: X25519 is symmetric, $\mathrm{DH}(a, B) = \mathrm{DH}(b, A)$, so both sides derive the same new root key and chain key.

**Forward secrecy and healing.** The KDF chain gives forward secrecy within a chain but no healing: a thief with $ck_i$ computes every later key of that chain, as a test of the code checks. The DH ratchet gives healing: after a party uses a fresh $a$ that the thief did not see, the new root key depends on $\mathrm{DH}(a, B)$, which the thief cannot compute from $A$ and $B$ under the Diffie-Hellman assumption. Cohn-Gordon, Cremers and Garratt (2016) define this goal as post-compromise security and show that a protocol needs state that is updated with fresh randomness to reach it; a fixed long-term key alone cannot give it.

**About the code.** The Python code is for study only. It is not constant time and must not protect real data. X25519 (RFC 7748) and HKDF (RFC 5869) are small local copies, checked against the RFC test vectors; HMAC and SHA-256 come from the standard library. The info string is the study value `KeyRatchetStudy`. There is no official test vector for a ratchet; the tests check agreement and the two security properties.

## Examples

**A chain from a zero key.** Start with $ck_0$ equal to 32 zero bytes. The code gives these first 8 bytes:

| Step $i$ | $mk_i$ | $ck_i$ |
|---|---|---|
| 1 | `3d7afb663124ecbf` | `4ee7be0c7872360c` |
| 2 | `e43cd1fae55cf944` | `4d86454c5efcc9ba` |
| 3 | `7718295d45e4164b` | `877299963d6463dd` |

Both sides of a chain with the same start get the same message keys. A thief who takes $ck_5$ and runs the chain 50 steps forward meets none of $mk_1, \ldots, mk_5$, but it does get $mk_6$, the next key of the honest party.

**Healing with a DH ratchet.** In a test, Eve copies Alice's full state once. Bob starts a turn: Eve, with Alice's old private key, derives Bob's new chain key, as Alice does. Then Alice starts a turn with a fresh private key that Eve does not see; Eve's guess of the new chain key is wrong. When Bob replies, his new chain key depends on the new root key, and Eve's copy of the state now gives a wrong key. One round trip with fresh randomness has locked Eve out.

**Hash chains for one-time passwords.** A [hash chain](/hash-chain/) $x, H(x), H(H(x)), \ldots$ used backward (Lamport 1981, later S/KEY) is the same one-way idea used for authentication instead of key derivation.

**Group ratchets.** In a ratchet tree, as in TreeKEM of MLS (RFC 9420), a member who updates its leaf replaces all keys on its path to the root, which heals the group key; this is a DH ratchet for groups, related to [TGDH](/tree-based-group-diffie-hellman/).

## Where it is used

- The [double ratchet](/double-ratchet/) in the [Signal protocol](/signal-protocol/), WhatsApp, Facebook Messenger secret conversations and other [secure messaging](/secure-messaging/) systems, started with [X3DH](/x3dh/) or PQXDH.
- Off-the-Record messaging (2004), which changes its Diffie-Hellman keys during a conversation.
- TLS 1.3 key update, a symmetric ratchet: each KeyUpdate message derives the next traffic secret from the current one with HKDF, which gives forward secrecy within a long connection but no healing.
- Messaging Layer Security (RFC 9420): a secret tree of KDF chains for messages and a ratchet tree for healing.
- Forward-secure storage and logging, where a key is evolved after each entry so that a later break-in cannot change or read old entries.

## References

The Double Ratchet specification of Perrin and Marlinspike defines KDF chains and the two ratchets. Bellare and Yee (2003) give the theory of forward-secure key evolution, and Cohn-Gordon, Cremers and Garratt (2016) define post-compromise security.
