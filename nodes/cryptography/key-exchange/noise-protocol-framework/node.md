---
tag: E0N5YS
kind: algorithm
slug: noise-protocol-framework
name: Noise protocol framework
aliases:
- Noise framework
area: cryptography/key-exchange
level: advanced
summary: A framework of Diffie-Hellman handshakes written as patterns of tokens. Each party keeps a chaining key and a transcript hash, and ends with two cipher states for transport.
solves: [key-agreement-problem]
model: word-ram
complexity:
  vars: {m: the number of binary digits of the Diffie-Hellman field prime, l: the total length of the payloads in bytes}
  time: {worst: Θ(m^3 + l), average: Θ(m^3 + l), best: Θ(m^3 + l)}
  space: {extra: Θ(m + l)}
properties: {deterministic: false, randomized: true}
history:
  year: 2018
  people: [Trevor Perrin]
  note: Perrin developed Noise through many public revisions. Revision 34, dated 2018-07-11, is the current stable version of the specification.
prereqs: [diffie-hellman, authenticated-key-exchange, hkdf]
see_also: [x25519, chacha20-poly1305, perfect-forward-secrecy, key-compromise-impersonation, sigma-key-exchange, tls-handshake, x3dh, ike-protocol]
sources:
  - url: "https://noiseprotocol.org/noise.html"
    title: "Trevor Perrin, The Noise Protocol Framework, revision 34, 2018-07-11"
    locator: Section 4.3 (HKDF), Section 5 (CipherState, SymmetricState, HandshakeState), Section 6 (prologue), Section 7 (handshake patterns, with NN and XX); the sections on pre-shared keys and compound protocols (numbers to check)
  - paper: "Nadim Kobeissi, Georgio Nicolas and Karthikeyan Bhargavan, Noise Explorer: fully automated modeling and verification for arbitrary Noise protocols, IEEE European Symposium on Security and Privacy (EuroS&P) 2019"
    locator: the automatic ProVerif models and the security properties found for each pattern (pages to check)
  - paper: "Benjamin Dowling, Paul Rösler and Jörg Schwenk, Flexible authenticated and confidential channel establishment (fACCE): analyzing the Noise protocol framework, PKC 2020, LNCS 12110, Springer, 2020, pages 341 to 373, doi 10.1007/978-3-030-45374-9_12"
    locator: the fACCE model and the computational proofs for the Noise patterns
  - paper: "Jason A. Donenfeld, WireGuard: next generation kernel network tunnel, NDSS 2017"
    locator: the handshake, which is Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s (section to check)
  - url: "https://github.com/lightning/bolts/blob/master/08-transport.md"
    title: "Lightning Network BOLT 8, Encrypted and authenticated transport"
    locator: the handshake Noise_XK_secp256k1_ChaChaPoly_SHA256 in three acts
  - url: "https://www.whatsapp.com/security/WhatsApp-Security-Whitepaper.pdf"
    title: "WhatsApp, WhatsApp encryption overview, technical white paper"
    locator: the transport security section (Noise Pipes with Curve25519, AES-GCM and SHA-256)
  - url: "https://github.com/haskell-cryptography/cacophony/blob/master/vectors/cacophony.txt"
    title: "Cacophony Noise test vectors"
    locator: "the entries Noise_NN_25519_ChaChaPoly_SHA256 and Noise_XX_25519_ChaChaPoly_SHA256"
  - url: "https://www.rfc-editor.org/rfc/rfc7748"
    title: "A. Langley, M. Hamburg and S. Turner, RFC 7748, Elliptic curves for security, January 2016"
    locator: Section 5 (X25519), Section 5.2 and Section 6.1 (test vectors)
---

The Noise protocol framework is a way to describe and build [Diffie-Hellman](/diffie-hellman/) handshakes. A Noise protocol is a short list of message patterns, each a list of tokens such as `e` (send an ephemeral public key), `s` (send a static public key) and `ee`, `es`, `se`, `ss` (do a Diffie-Hellman between the named keys). Both parties run the same small state machine. Each token updates a chaining key $ck$, which collects all the Diffie-Hellman results, and a transcript hash $h$, which collects everything sent. As soon as there is a key, everything sent is encrypted with $h$ as associated data. At the end, both parties split $ck$ into two transport keys, one for each direction. The specification is by Trevor Perrin; revision 34 is dated 2018-07-11. WireGuard, WhatsApp and the Lightning Network use it.

**Notation.** $\mathrm{DH}(a, B)$ is X25519 of the private key $a$ and the public key $B$. $\mathrm{HASH}$ is SHA-256 and $\mathrm{HASHLEN} = 32$. $\mathrm{HKDF}(ck, ikm, n)$ gives $n$ outputs: $t = \mathrm{HMAC}(ck, ikm)$, $o_1 = \mathrm{HMAC}(t, \mathtt{01})$, $o_i = \mathrm{HMAC}(t, o_{i-1} \| i)$. $\mathrm{MixHash}(d)$ sets $h \leftarrow \mathrm{HASH}(h \| d)$. $\mathrm{MixKey}(d)$ sets $(ck, k) \leftarrow \mathrm{HKDF}(ck, d, 2)$ and the nonce $n \leftarrow 0$. $\mathrm{EncryptAndHash}(p)$ gives $c = \mathrm{AEAD}_k(n, h, p)$ (or $c = p$ while there is no $k$), then does $\mathrm{MixHash}(c)$. $\mathrm{DecryptAndHash}$ is the mirror. $s, e$ are one's own static and ephemeral key pairs and $rs, re$ are the peer's public keys.

## In plain words

Two programs want to set up a secret channel. Noise gives them a short script to follow, for example "I send a new public key; you send a new public key and we mix our two keys". Each step of the script either sends a key or mixes a shared secret into a running secret. Both sides also keep a running summary of every byte that has gone across. Once there is a secret, every later piece is locked with it and tied to the summary, so a change by an attacker shows up at once. At the end, the running secret gives one key for each direction. The same few rules build many different handshakes, with or without long-term keys on each side.

## The problem

Two parties want an [authenticated key exchange](/authenticated-key-exchange/) that fits their setting: no long-term keys, a key on one side, keys on both sides, keys known in advance or sent in the handshake, with [forward secrecy](/perfect-forward-secrecy/) and some hiding of identities. Ad hoc designs for each case are easy to get wrong. Noise gives one set of rules and a compact pattern language, so each handshake is a small, checkable object, and the security of each pattern can be studied once.

## The algorithm

This is the handshake of one party. The pattern NN is `-> e` then `<- e, ee`. The pattern XX is `-> e`, then `<- e, ee, s, es`, then `-> s, se`. The initiator writes the messages with `->` and reads those with `<-`; the responder does the opposite. In `es` the first letter is the initiator's key and the second the responder's, so the initiator computes $\mathrm{DH}(e, rs)$ and the responder computes $\mathrm{DH}(s, re)$.

```pseudo id=main
NOISE-HANDSHAKE(pattern, role, prologue, s)
L1  h ← protocol name padded with zeros to HASHLEN, or HASH(name) if longer; ck ← h; k ← empty
L2  MixHash(prologue); MixHash each pre-message public key of the pattern
L3  for each token of the next message pattern, writing it or reading it in order
L4      "e": write e.pub for a new pair e, or read re; MixHash of that key
L5      "s": write EncryptAndHash(s.pub), or read rs ← DecryptAndHash(next bytes)
L6      "ee", "es", "se", "ss": MixKey(DH(own key, peer key)) for the keys the token names
L7  write EncryptAndHash(payload), or read payload ← DecryptAndHash(rest); go to L3 for the next message
L8  after the last message: (c1, c2) ← HKDF(ck, empty, 2); the initiator sends with c1, the responder with c2
```

At line L5 the length to read is 32 bytes if there is no key yet and 48 bytes (key plus tag) if there is one; both sides know this because they have the same state. A failed tag check at line L5 or L7 ends the handshake. After line L8, the transport messages use the cipher states with their own nonces and no associated data, and $h$ is the handshake hash, which the application can use for channel binding.

**About the code.** The Python code implements Noise_NN_25519_ChaChaPoly_SHA256 and Noise_XX_25519_ChaChaPoly_SHA256: its own X25519 Montgomery ladder (RFC 7748), its own ChaCha20-Poly1305 (RFC 8439), SHA-256 and HMAC from `hashlib` and `hmac`, and the CipherState, SymmetricState and HandshakeState objects of the specification. The tests check it against the RFC 7748 vectors and the cacophony vectors for NN and XX, including the transport messages and the handshake hash. It is for study only. It is not constant time and must not protect real data. Use a maintained Noise library, such as snow (Rust) or noise-c, or the handshake code of WireGuard.

## Example

The cacophony vector for Noise_NN_25519_ChaChaPoly_SHA256, with the prologue "John Galt" and fixed ephemeral keys. Values show the first 8 bytes in hex.

| step | party | line | action | result |
|---|---|---|---|---|
| 1 | both | L1 | the name is exactly 32 bytes, so $h$ is the name | $h$ = 4e6f6973655f4e4e ("Noise_NN") |
| 2 | both | L2 | MixHash(prologue) | $h$ = ed35952131cddb48 |
| 3 | initiator | L4 | send e.pub, MixHash | e.pub = ca35def5ae56cec3 |
| 4 | initiator | L7 | no key yet, so the payload goes in clear | message 1 is 32 + 16 = 48 bytes; $h$ = 443165f72d404a81 |
| 5 | responder | L4, L6 | send its e.pub; ee gives MixKey(DH) | DH = 934eec08e1e6aad4 |
| 6 | responder | L7 | EncryptAndHash of a 15-byte payload | message 2 is 32 + 15 + 16 = 63 bytes |
| 7 | both | L8 | Split | c1.k = 19f88af6c8510409, c2.k = 800b5b76073c7f99 |
| 8 | both | | handshake hash | $h$ = 9223fec1b892ec9d |

Message 3 is the first transport message, from the initiator with c1 and nonce 0: an 11-byte payload gives 27 bytes. In NN nobody is authenticated: an active attacker can run the handshake with each side. XX adds static keys, so each side proves its static key with `es` or `se`.

## Correctness

If both parties run the same pattern with the same prologue and the messages arrive unchanged, then before and after each token the two parties have equal $h$, $ck$, $k$ and $n$. The `e` and `s` tokens hash the same bytes on both sides, and each DH token gives the same value on both sides because $\mathrm{DH}(a, bG) = \mathrm{DH}(b, aG)$. So every tag check passes, each party reads the payload that the other wrote, and line L8 gives the same two keys to both, used in opposite roles. The proof is below.

## Complexity

Each party does three DH operations in XX (one in NN), plus one X25519 key generation for its ephemeral key. With schoolbook arithmetic an X25519 operation takes $\Theta(m^3)$ bit operations for an $m$-bit prime ($m = 255$). The hashing and AEAD work is $\Theta(l)$ in the payload length. NN and XX take one and one and a half round trips. The state is a few 32-byte values.

## Properties

- **Transcript binding.** Every byte sent and the prologue go into $h$, and $h$ is the associated data of every encryption, so a change to any earlier message makes the next tag check fail.
- **Key separation.** Each DH result goes into $ck$ through HKDF; the transport keys depend on all DH results of the handshake.
- **Forward secrecy** when the transport keys depend on `ee`, as in NN and XX.
- **Authentication per pattern.** NN gives none. In XX the responder proves its static key with `es` in message 2, and the initiator proves its static key with `se` in message 3.
- **Identity hiding.** In XX both static keys travel encrypted. The responder's static key goes out before the responder knows who the initiator is, so an active attacker can learn it; the initiator's static key goes only to a responder that has proved its own.
- **Payload security grows.** Early payloads have weaker properties than late ones; the specification lists the properties of each payload for each pattern.

## Variants and improvements

- **Other patterns.** One-way patterns (N, K, X) for a single message, and interactive patterns such as NK, KK, IK and XK, where a letter says how each side's static key is known: N for none, K for known in advance, X for sent in the handshake, I for sent at once.
- **Pre-shared keys.** The modifiers psk0, psk1, psk2 and so on mix a symmetric key into the handshake at a given position. WireGuard uses Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s.
- **Fallback and Noise Pipes.** A client tries IK with a cached server key and falls back to XX if that fails. WhatsApp uses Noise Pipes for its client to server transport.
- **Other primitives.** The DH can be 448 (or secp256k1 in Lightning BOLT 8, which uses XK), the cipher AES-GCM, and the hash SHA-512 or BLAKE2.
- **Formal analysis.** Noise Explorer (EuroS&P 2019) makes symbolic models of any pattern and checks them with ProVerif. Dowling, Rösler and Schwenk's fACCE model (PKC 2020) gives computational proofs for the patterns.
- **Post-quantum variants.** KEM-based versions of the patterns have been proposed (for example PQNoise, 2022; details to check).

## When to use it

Use Noise when you control both ends, want a small handshake with no certificate parsing and no negotiation, and know which keys each side has: VPN tunnels, peer-to-peer links, client to server links of one application. Use [TLS](/tls-handshake/) when you need interoperation with other software or a public-key infrastructure. Choose the pattern from the keys you have, and check its properties in the specification or with Noise Explorer.

## Pitfalls

- **Payloads in the first message are in clear.** In NN and XX there is no key at line L7 of message 1, so the payload is sent without encryption, as the example shows.
- **Early payloads are weaker.** In XX the payload of message 2 is encrypted, but the responder does not know yet who the initiator is. Do not send secrets to a party that has not yet authenticated.
- **Negotiation outside the prologue.** If the parties agree on the protocol over the network, they must put that data in the prologue at line L2, or an attacker can downgrade the choice without detection.
- **Wrong roles at line L8.** The initiator sends with c1 and receives with c2; if both use c1 to send, the keys and nonces collide.
- **Nonce reuse.** Each cipher state must count its nonce up by one for each message and stop before $2^{64} - 1$. Transport messages that can be lost or reordered need an explicit nonce in the message, as WireGuard sends.
- **Reusing ephemeral keys.** A new $e$ at line L4 for each handshake is what gives forward secrecy; a fixed $e$, as in the test vectors, is only for testing.
- **The handshake hash before line L8.** Use $h$ for channel binding only after the handshake ends.

## Implementations

## History

Trevor Perrin developed Noise in public revisions over several years; revision 34, dated 2018-07-11, is the current stable version. Jason Donenfeld built WireGuard (NDSS 2017) on the IK pattern with a pre-shared key. WhatsApp describes its client to server transport as Noise Pipes, and the Lightning Network's BOLT 8 uses the XK pattern over secp256k1. Kobeissi, Nicolas and Bhargavan presented Noise Explorer at IEEE EuroS&P 2019, and Dowling, Rösler and Schwenk analysed the framework in the fACCE model at PKC 2020.

## References
