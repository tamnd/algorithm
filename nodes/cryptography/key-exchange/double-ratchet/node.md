---
tag: EJKDEP
kind: algorithm
slug: double-ratchet
name: Double Ratchet algorithm
aliases:
- Signal Double Ratchet
- Axolotl ratchet
area: cryptography/key-exchange
level: advanced
summary: Gives each message of a conversation its own key. A KDF chain per message gives forward secrecy; a Diffie-Hellman ratchet per turn heals after a leak. Perrin and Marlinspike, Signal, 2016.
solves: [key-agreement-problem]
model: word-ram
complexity:
  vars: {m: the length of a message in bytes, s: "the number of skipped messages (at most MAX_SKIP per call)"}
  time: {worst: O(m + s), average: O(m), best: O(m)}
  space: {extra: Θ(m + s)}
properties: {deterministic: false, randomized: true}
history:
  year: 2013
  people: [Trevor Perrin, Moxie Marlinspike]
  note: Perrin and Marlinspike designed the ratchet for TextSecure in 2013, first called the Axolotl ratchet, and published the specification, revision 1, on 2016-11-20.
prereqs: [key-ratchet, x25519, hkdf]
see_also: [x3dh, signal-protocol, secure-messaging, perfect-forward-secrecy, authenticated-encryption, cbc-mode, hmac, noise-protocol-framework]
sources:
  - url: "https://signal.org/docs/specifications/doubleratchet/"
    title: Trevor Perrin and Moxie Marlinspike, The Double Ratchet Algorithm, revision 1, 2016-11-20
    locator: Section 2 (KDF chains, the symmetric-key ratchet and the Diffie-Hellman ratchet), Section 3 (state variables, RatchetInitAlice, RatchetInitBob, RatchetEncrypt, RatchetDecrypt, TrySkippedMessageKeys, SkipMessageKeys, DHRatchet and MAX_SKIP), Section 4 (header encryption), Section 5.2 (recommended cryptographic algorithms), Section 6 (security considerations)
  - paper: "Katriel Cohn-Gordon, Cas Cremers, Benjamin Dowling, Luke Garratt and Douglas Stebila, A formal security analysis of the Signal messaging protocol, IEEE European Symposium on Security and Privacy (EuroS&P) 2017; full version in Journal of Cryptology, 2020"
    locator: a multi-stage key exchange model for X3DH with the Double Ratchet, and proofs of secrecy of message keys with forward secrecy and post-compromise security
  - paper: "Joël Alwen, Sandro Coretti and Yevgeniy Dodis, The double ratchet: security notions, proofs, and modularization for the Signal protocol, EUROCRYPT 2019"
    locator: the secure messaging definition with immediate decryption, and a modular construction from continuous key agreement, forward-secure AEAD and a PRF-PRNG
  - paper: "Katriel Cohn-Gordon, Cas Cremers and Luke Garratt, On post-compromise security, IEEE Computer Security Foundations Symposium (CSF) 2016"
    locator: the definition of post-compromise security, which the Diffie-Hellman ratchet gives
  - url: "https://www.rfc-editor.org/rfc/rfc7748"
    title: Adam Langley, Mike Hamburg and Sean Turner, RFC 7748, Elliptic Curves for Security, January 2016
    locator: Section 5 (X25519) and Section 5.2 (test vectors), used by the code
  - url: "https://www.rfc-editor.org/rfc/rfc5869"
    title: Hugo Krawczyk and Pasi Eronen, RFC 5869, HMAC-based Extract-and-Expand Key Derivation Function (HKDF), May 2010
    locator: Section 2 and Appendix A.1 (Test Case 1), used by the code
---

The Double Ratchet algorithm lets two parties who share a secret key exchange encrypted messages in which every message has its own key. It combines two [key ratchets](/key-ratchet/). A symmetric ratchet, a KDF chain, derives a new message key for each message and deletes the old chain key, so a thief who steals the current state cannot read earlier messages. A Diffie-Hellman ratchet mixes a fresh [X25519](/x25519/) output into a root key each time the conversation changes direction, so a thief who copied the state is locked out after one round trip. The algorithm also handles messages that arrive out of order or are lost. Trevor Perrin and Moxie Marlinspike designed it for Signal; the session key usually comes from [X3DH](/x3dh/).

**Notation.** $SK$ is the 32-byte shared secret from the initial key agreement. $DH_s$ is a party's current ratchet key pair and $DH_r$ the peer's current ratchet public key. $RK$ is the root key, $CK_s$ and $CK_r$ the sending and receiving chain keys, and $mk$ a message key. $N_s$ and $N_r$ count the messages sent and received in the current chains, and $PN$ is the length of the previous sending chain. A header is $(dh, pn, n)$: the sender's ratchet public key, its $PN$ and the message number. $AD$ is associated data from the initial key agreement. $\mathrm{KDF\_RK}(rk, x) = \mathrm{HKDF}(\text{salt} = rk, \text{ikm} = x, \text{info}, 64)$ split into two 32-byte halves, and $\mathrm{KDF\_CK}(ck) = (\mathrm{HMAC}(ck, \texttt{0x02}), \mathrm{HMAC}(ck, \texttt{0x01}))$, the next chain key and the message key.

## In plain words

Alice and Bob start with one shared secret. Each time Alice sends a message, she turns a one-way wheel that gives a new key for that message and forgets the old position. Bob turns the same wheel on his side and gets the same key. A thief who looks at the wheel today cannot turn it backward to read old messages.

Each time the conversation changes direction, the sender also picks a new random key pair and puts the public half in the message header. Both sides combine it with the other side's latest public key into a fresh shared secret, and use that to start new wheels. A thief who copied everything once does not know the new random key, so soon it can read nothing.

Each message carries its number, so the receiver can keep keys for late messages and use them when those messages arrive.

## The problem

Two parties hold a shared key $SK$ and want an asynchronous conversation in which (1) each message key is deleted after use, so a later compromise reveals no earlier message (forward secrecy); (2) after a compromise of one party's state, security returns once the parties exchange messages with fresh randomness the attacker did not see (post-compromise security); (3) messages can be lost, delayed or reordered without blocking later ones. This is a stateful form of the [key agreement problem](/key-agreement-problem/), continued for the life of a conversation.

## The algorithm

```pseudo id=main
RatchetInitAlice(SK, bob_public)                ▷ Section 3.3 of the specification
L1  DHs ← GENERATE_DH();  DHr ← bob_public
L2  RK, CKs ← KDF_RK(SK, DH(DHs, DHr));  CKr ← none;  Ns, Nr, PN ← 0;  MKSKIPPED ← {}
RatchetInitBob(SK, bob_key_pair)
L3  DHs ← bob_key_pair;  DHr ← none;  RK ← SK;  CKs, CKr ← none;  Ns, Nr, PN ← 0
RatchetEncrypt(plaintext, AD)                   ▷ Section 3.4
L4  CKs, mk ← KDF_CK(CKs)
L5  header ← (DHs.public, PN, Ns)
L6  Ns ← Ns + 1
L7  return header, ENCRYPT(mk, plaintext, CONCAT(AD, header))
RatchetDecrypt(header, ciphertext, AD)          ▷ Section 3.5
L8  if TrySkippedMessageKeys(header, ciphertext, AD) gives a plaintext: return it
L9  if header.dh ≠ DHr:
L10   SkipMessageKeys(header.pn)
L11   DHRatchet(header)
L12 SkipMessageKeys(header.n)
L13 CKr, mk ← KDF_CK(CKr)
L14 Nr ← Nr + 1
L15 return DECRYPT(mk, ciphertext, CONCAT(AD, header))
L16 if any step of L9 to L15 fails: restore the state from before L9 and report the error
TrySkippedMessageKeys(header, ciphertext, AD)
L17 if (header.dh, header.n) is in MKSKIPPED: decrypt with that key
L18   delete the entry and return the plaintext
SkipMessageKeys(until)
L19 if Nr + MAX_SKIP < until: report an error
L20 if CKr ≠ none: while Nr < until:
L21     CKr, mk ← KDF_CK(CKr)
L22     MKSKIPPED[(DHr, Nr)] ← mk;  Nr ← Nr + 1
DHRatchet(header)
L23 PN ← Ns;  Ns ← 0;  Nr ← 0
L24 DHr ← header.dh
L25 RK, CKr ← KDF_RK(RK, DH(DHs, DHr))         ▷ the peer's new sending chain
L26 DHs ← GENERATE_DH()
L27 RK, CKs ← KDF_RK(RK, DH(DHs, DHr))         ▷ my new sending chain
```

**Setup.** Alice knows Bob's ratchet public key, in Signal his signed prekey from X3DH. Lines L1 and L2 give her a first sending chain at once, so she can send before Bob replies. Bob (line L3) has no chain until Alice's first message arrives.

**Sending.** Lines L4 to L7 turn the sending chain one step. The header carries the current ratchet public key, so the receiver can tell when the sender has made a DH ratchet step, and the message number $N_s$, so the receiver knows which key to use. The header is authenticated as part of the associated data, but it is not encrypted.

**Receiving.** Line L8 first looks for a stored key of a skipped message. If the header carries a new ratchet public key (line L9), the receiver first stores the keys of the remaining messages of the old receiving chain, whose length the sender gave as $pn$ (line L10), then makes a DH ratchet step (line L11). Line L12 stores the keys of any messages of the current chain that were skipped, and lines L13 to L15 decrypt. If decryption fails, line L16 discards all state changes, so a forged message cannot advance the ratchet or delete keys.

**DH ratchet step.** Lines L23 to L27 run when the peer has a new ratchet key. Line L25 derives the peer's new sending chain, which is the receiver's new receiving chain, from $\mathrm{DH}(DH_s, DH_r)$. Line L26 picks a fresh key pair, and line L27 derives the receiver's own next sending chain. Each step of the root chain adds a DH output that depends on one fresh private key.

**MAX_SKIP.** Line L19 limits how many message keys one header can force the receiver to compute and store, which stops a malicious sender from making the receiver use much time or memory. The specification leaves the value to the application.

**About the code.** The Python code is for study only. It is not constant time and must not protect real data; use libsignal or another maintained implementation. X25519 (RFC 7748) and HKDF (RFC 5869) are local copies, checked against the RFC test vectors. KDF_RK and KDF_CK follow Section 5.2 of the specification. ENCRYPT differs: the specification recommends AES-256 in [CBC mode](/cbc-mode/) with HMAC-SHA256, and the code uses an encrypt-then-MAC scheme whose key stream is HMAC-SHA256 in counter mode, with the same 80-byte HKDF split into an encryption key, a MAC key and an IV. It is a study AEAD, not a standard one. Header encryption (Section 4) is not implemented. The specification has no official test vectors.

## Example

**In order, both directions.** Alice's first chain $C_1$ comes from $RK_1 = \mathrm{KDF\_RK}(SK, \mathrm{DH}(A_1, B_0))$, where $B_0$ is Bob's initial ratchet key. The code runs this exchange:

| Message | Header $(dh, pn, n)$ | Sender's state change | Receiver's state change |
|---|---|---|---|
| a0 | $(A_1, 0, 0)$ | $C_1$ step 1 | new $dh$: DH ratchet, $C_1$ as receiving chain, new $B_1$, sending chain $C_2$ |
| a1 | $(A_1, 0, 1)$ | $C_1$ step 2 | $C_1$ step 2 |
| a2 | $(A_1, 0, 2)$ | $C_1$ step 3 | $C_1$ step 3 |
| b0 | $(B_1, 0, 0)$ | $C_2$ step 1 | new $dh$: DH ratchet, $PN = 3$, $C_2$ receiving, new $A_2$, sending chain $C_3$ |
| b1 | $(B_1, 0, 1)$ | $C_2$ step 2 | $C_2$ step 2 |
| again | $(A_2, 3, 0)$ | $C_3$ step 1 | new $dh$: DH ratchet |

The last header has $pn = 3$, $n = 0$, as a test checks: Alice sent 3 messages in her previous chain.

**Out of order across a ratchet step.** Alice sends m0 to m3 in one chain. Bob receives m2 first: line L12 stores the keys of m0 and m1. Bob replies, and Alice answers with a new ratchet key and header $pn = 4$. When Bob receives that message, line L10 stores the key of m3, the last message of the old chain, then line L11 ratchets. Later m0, m3 and m1 arrive and are decrypted with stored keys (line L17), and each key is deleted after use (line L18); at the end MKSKIPPED is empty.

**Replay.** A second copy of a message that was already decrypted fails: its key was deleted, and the chain has moved on, so line L15 uses the wrong key and line L16 rolls the state back.

## Correctness

**Claim.** If every message is delivered at most once, unchanged, in any order, and no more than MAX_SKIP messages of one chain are skipped, every message decrypts to its plaintext. Both parties compute the same sequence of root keys $RK_1, RK_2, \ldots$ in the same order, because X25519 is symmetric: Alice's sending chain of epoch $k$ and Bob's receiving chain of epoch $k$ come from the same $\mathrm{KDF\_RK}$ call on the same inputs. Within a chain, message $n$ uses the message key of step $n + 1$, which the receiver gets either at once (line L13) or from MKSKIPPED, where line L22 stored it under the index $n$. The full proof is on the proof page.

**Security.** Cohn-Gordon, Cremers, Dowling, Garratt and Stebila (2017, 2020) prove, in a multi-stage key exchange model, that X3DH followed by the Double Ratchet gives secret message keys with forward secrecy and post-compromise security, under the gap Diffie-Hellman assumption with the KDFs modelled as random oracles. Alwen, Coretti and Dodis (2019) define secure messaging with immediate decryption, which requires that every message can be decrypted on arrival, and build the Double Ratchet from three primitives, with proofs in the standard model for some instantiations.

## Complexity

Sending costs one KDF_CK step (two HMAC calls) and one encryption, $O(m)$ for an $m$-byte message. A DH ratchet step costs one key generation and two X25519 computations, each $O(1)$ for the fixed 255-bit curve. Receiving a message after $s$ skipped ones costs $s$ extra HMAC steps and stores $s$ keys, with $s \le$ MAX_SKIP for each call of line L19. The state is a constant number of 32-byte keys plus MKSKIPPED, so $\Theta(s)$ beyond the message. The specification advises deleting skipped keys after some time or some number of messages, so that MKSKIPPED stays bounded.

## Properties

- **Forward secrecy for each message.** Message keys are deleted after use, and chain keys move only forward.
- **Post-compromise security.** After an attacker copies one party's state, keys become secret again once that party sends with a fresh ratchet key that the attacker did not see, and the peer replies.
- **Immediate decryption.** A message can be decrypted when it arrives, even if earlier messages are missing.
- **Asynchronous.** Alice can send before Bob is online; no round trip is needed for each message.
- **Headers in clear.** Without header encryption, the ratchet public keys and the counters are visible, which shows the conversation's turn structure.
- **No authentication of its own.** Identity comes from the initial key agreement, such as X3DH, through $SK$ and $AD$.

## Variants and improvements

- **Header encryption** (Section 4 of the specification): KDF_RK also outputs header keys, the header is encrypted under the current header key, and the receiver tries the current and next header keys to tell whether a DH ratchet step occurred.
- **Deferred key generation** (Section 6): a party may generate its new ratchet key pair when it next sends, not when it receives, to save time; this delays healing a little.
- **OTR and SCIMP.** Off-the-Record messaging (2004) uses a Diffie-Hellman ratchet without a KDF chain per message; the Silent Circle protocol SCIMP uses a hash ratchet without a Diffie-Hellman ratchet. The Double Ratchet combines the two.
- **Post-quantum ratchets.** Proposals add a key encapsulation mechanism to the DH ratchet so that healing holds against a quantum attacker; in 2025 Signal announced a post-quantum ratchet run beside the Double Ratchet.
- **Group messaging.** Sender keys (one KDF chain per sender, sent to each member over pairwise Double Ratchet channels) and Messaging Layer Security (RFC 9420) extend the ideas to groups.

## When to use it

Use the Double Ratchet for an end-to-end encrypted conversation between two devices that may be offline, after an authenticated key agreement such as [X3DH](/x3dh/) or PQXDH, through a maintained library. For a short interactive session, such as a TLS connection, a single handshake with [forward secrecy](/perfect-forward-secrecy/) and a key update is simpler. For large groups, use MLS.

## Pitfalls

- **Advancing state on a bad message.** If the receiver keeps the result of lines L9 to L14 when decryption fails, a forged header can push the chain forward and delete keys, so real messages cannot be read. Line L16 must restore the state from before line L9.
- **Deleting a skipped key before the tag check.** Line L18 deletes the key only after line L17 decrypts successfully; otherwise a forged message with a valid header destroys the key of the real one.
- **No MAX_SKIP.** Without line L19, a header with $n = 2^{31}$ makes the receiver compute two billion HMAC steps. Check $N_r + \text{MAX\_SKIP} < \text{until}$ before line L20.
- **Skipping the old chain before the ratchet step.** If line L11 runs before line L10, the keys of the late messages of the old chain are lost, because line L25 replaces $CK_r$. Store them first with $pn$, as in line L10.
- **Reusing a message key.** Encrypting two messages under one $mk$ breaks the encryption; line L4 must run for every message.
- **Keeping keys.** Message keys and old chain keys must be erased, or forward secrecy is lost; old skipped keys should expire.
- **Weak associated data.** $AD$ must contain the identities from the key agreement, else the session is not bound to the parties.

## Implementations

The Python code implements Section 3 of the specification: `ratchet_init_alice` (lines L1 and L2), `ratchet_init_bob` (line L3), `ratchet_encrypt` (lines L4 to L7), `ratchet_decrypt` (lines L8 to L16), `try_skipped_message_keys` (lines L17 and L18), `skip_message_keys` (lines L19 to L22) and `dh_ratchet` (lines L23 to L27). The tests check X25519 against RFC 7748, HKDF against RFC 5869, messages in both directions, out-of-order delivery across a ratchet step, lost messages, the rejection of a replay, MAX_SKIP with roll back, a tampered ciphertext with roll back, forward secrecy of the chain, and healing after Eve copies Alice's state. libsignal (Rust) is the reference implementation.

## History

Off-the-Record messaging (2004) introduced frequent Diffie-Hellman key changes in instant messaging. In 2013 Perrin and Marlinspike combined such a ratchet with a per-message hash ratchet in TextSecure, under the name Axolotl, renamed the Double Ratchet in 2016. The specification, revision 1, appeared on 2016-11-20, with X3DH. WhatsApp adopted the Signal protocol in 2016. Formal analyses followed in 2017 and 2019.

## References
