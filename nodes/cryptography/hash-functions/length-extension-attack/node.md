---
tag: 8W23N6
kind: concept
slug: length-extension-attack
name: Length extension attack
aliases:
- length extension
area: cryptography/hash-functions
level: core
summary: With a Merkle-Damgard hash, anyone who knows H(k || m) and the length of k can compute H(k || m || pad || x) without k. It breaks the MAC H(k || m); HMAC and SHA-3 stop it.
prereqs: [merkle-damgard-construction, message-authentication-code]
see_also: [hmac, sha-2, sha-3, md5, sha-1, blake2, blake3, kmac]
sources:
  - paper: doi:10.6028/NIST.FIPS.180-4
    title: NIST FIPS 180-4, Secure Hash Standard (SHS), 2015
    locator: Section 5.1.1 (the padding of SHA-256), Section 6.2 (SHA-256), and Section 6.7 (SHA-512/256 by truncation)
  - url: "http://netifera.com/research/flickr_api_signature_forgery.pdf"
    title: Thai Duong and Juliano Rizzo, Flickr's API signature forgery vulnerability, September 2009
    locator: the forgery of Flickr API calls signed as MD5(secret || arguments)
  - paper: "Mihir Bellare, Ran Canetti and Hugo Krawczyk, Keying hash functions for message authentication, CRYPTO 1996, LNCS 1109, pages 1 to 15"
    locator: the secret prefix MAC and its extension weakness, and the NMAC and HMAC constructions
  - url: "https://www.rfc-editor.org/rfc/rfc2104"
    title: "H. Krawczyk, M. Bellare and R. Canetti, RFC 2104, HMAC: keyed-hashing for message authentication, 1997"
    locator: Section 2 (the HMAC definition)
  - paper: "Jean-Sebastien Coron, Yevgeniy Dodis, Cecile Malinaud and Prashant Puniya, Merkle-Damgard revisited: how to construct a hash function, CRYPTO 2005, LNCS 3621, pages 430 to 448"
    locator: plain Merkle-Damgard is not indifferentiable from a random oracle, and the fixes by prefix-free encoding, chop and a final distinct function
  - paper: doi:10.6028/NIST.FIPS.202
    title: NIST FIPS 202, SHA-3 Standard, 2015
    locator: Section 4 (the sponge construction, where the capacity part of the state is never output)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 9.5.2 (MACs from hash functions, the secret prefix and secret suffix methods)
---

A length extension attack uses the structure of a [Merkle-Damgard](/merkle-damgard-construction/) hash such as MD5, SHA-1 or SHA-256. Its digest is the full internal state after the last block. So anyone who knows $H(k \,\|\, m)$ and the length of $k \,\|\, m$ can set the state to that digest and hash more blocks. The result is the correct value of $H(k \,\|\, m \,\|\, \mathrm{pad} \,\|\, x)$ for any $x$ of the attacker's choice, where $\mathrm{pad}$ is the padding that the hash put after $m$. The attacker never learns $k$. This breaks the naive [MAC](/message-authentication-code/) $\mathrm{tag} = H(k \,\|\, m)$. Duong and Rizzo used it in 2009 to forge signed calls to the Flickr API. The fixes are [HMAC](/hmac/), or a hash whose output is not its whole state: [SHA-3](/sha-3/), SHA-512/256, [BLAKE2](/blake2/) and [BLAKE3](/blake3/).

## In plain words

A Merkle-Damgard hash reads a message in blocks and keeps a running state. The final digest is just that state.

So the digest is also a checkpoint. If you know the digest of some message and how long the message was, you can pick up from the checkpoint and keep hashing more blocks, without ever seeing the start of the message.

If a system signs messages by hashing a secret key followed by the message, an attacker can take a signed message, add text at the end, and compute a valid signature for the longer message.

## The idea

**The state is the digest.** A Merkle-Damgard hash pads the input $M$ to whole blocks $M_1, \ldots, M_L$, with a 1 bit, zeros and the bit length of $M$. It sets $h_0 = IV$ and $h_i = f(h_{i-1}, M_i)$ for a [compression function](/compression-function/) $f$, and outputs $h_L$. Hashing a longer input $M \,\|\, \mathrm{pad}(M) \,\|\, x$ runs through the same $h_L$, and then continues with the blocks of $x$ and a new padding, whose length field counts all the bytes before it. Nothing in $h_L$ marks it as final.

**The attack.** Suppose a server tags $m$ with $t = H(k \,\|\, m)$ for a secret $k$ of known length $\ell_k$. Given $(m, t)$, the attacker:

```pseudo id=main
EXTEND(t, ℓk, m, x)
L1  glue ← the padding of a message of ℓk + |m| bytes
L2  state ← t, split into the words of the hash state
L3  done ← ℓk + |m| + |glue|                   ▷ bytes already hashed, a multiple of the block size
L4  t' ← continue hashing x from state, with a final length field for done + |x| bytes
L5  return (m ‖ glue ‖ x, t')
```

The forged message $m' = m \,\|\, \mathrm{glue} \,\|\, x$ starts with $m$, so it passes any check that only looks at the start, and $t' = H(k \,\|\, m')$ exactly. If $\ell_k$ is unknown, the attacker tries each likely length. Each try costs one hash and one query to the server.

**A worked example.** The page's code has a pure Python SHA-256, checked against hashlib and against the FIPS 180-4 vectors for `abc`, the empty string and the 56-byte two-block message. A local simulated server holds a 16-byte key. Here the key is 16 bytes of `k` so that the example can be repeated.

- $m$ = `user=alice&amount=10` (20 bytes), $t$ = `5be8b0bd0bc75a39...2385226b`.
- The glue is 28 bytes: `80`, 25 zero bytes, and the 2-byte end `0120`, since $16 + 20 = 36$ bytes is 288 bits, and 288 is `0x120`. With the key, this fills one 64-byte block.
- $x$ = `&amount=1000000`. The forged message has 63 bytes, and its tag is $t'$ = `1a6cdb5824ca7e62...b8701205`.
- The server computes SHA-256 of the key and the 63 bytes, and gets $t'$. The forgery is accepted.

The tests repeat the forgery for 40 random keys of 1 to 69 bytes, with random messages and extensions, check that a wrong key length gives a wrong tag, and check that the same method fails on HMAC-SHA-256 and on SHA3-256. The code is for study only and not constant time. The attack runs only on a local simulated MAC. For real message authentication, use HMAC from the standard library (Python's `hmac`), a FIPS 140 validated module, or libsodium's `crypto_auth`.

## Examples

**Flickr, 2009.** The Flickr API signed requests as MD5 of a shared secret followed by the sorted names and values of the arguments. Duong and Rizzo showed that an attacker who saw one signed request could append arguments and compute a valid signature, and so call the API as the user. The fix was to change the signing method.

**Which hashes are vulnerable.** Every hash whose digest is its whole chaining state:

| Hash | Vulnerable | Why |
|---|---|---|
| MD4, MD5, SHA-1, RIPEMD-160 | yes | the digest is the full state |
| SHA-256, SHA-512 | yes | the digest is the full state |
| SHA-224 | partly | 32 state bits are dropped, so the attacker guesses them: $2^{32}$ tries |
| SHA-384 | no, in practice | 128 state bits are dropped, so $2^{128}$ guesses |
| SHA-512/256, SHA-512/224 | no | 256 or more state bits are dropped |
| SHA-3, SHAKE, KMAC | no | a sponge never outputs its capacity part, so the full state is unknown |
| BLAKE2, BLAKE3 | no | the last compression uses a finalization flag, so a digest is not a valid middle state |
| SHA-256 applied twice, $H(H(m))$ | no | the outer call hides the inner state |

**Variants of the naive MAC.**

- *Secret suffix*, $H(m \,\|\, k)$. Length extension does not apply, but a collision $H(m) = H(m')$ found offline, with no key, gives $H(m \,\|\, k) = H(m' \,\|\, k)$ when $m$ and $m'$ have the same length and fill whole blocks. So the security drops to collision resistance, which is broken for MD5 and SHA-1.
- *Envelope*, $H(k \,\|\, m \,\|\, k)$. Better, but with weaker proofs than HMAC and some key recovery attacks on MD5 versions.
- *HMAC*, $H((k \oplus \mathrm{opad}) \,\|\, H((k \oplus \mathrm{ipad}) \,\|\, m))$. The outer hash hides the inner state. Bellare, Canetti and Krawczyk (1996) prove it unforgeable when the compression function is a secure MAC and the keyed iterated hash is weakly collision resistant, and Bellare (2006) proves it a PRF when the compression function is a PRF. This is the standard fix.

## Where it is used

- **Breaking homemade MACs.** Web APIs and cookies signed as $H(\text{secret} \,\|\, \text{data})$ are the usual target. CTF challenges and audits look for it first.
- **Design rules.** The attack is a main reason why SHA-3 is a sponge, why BLAKE2 has a finalization flag, and why SHA-512/256 was added. Coron, Dodis, Malinaud and Puniya showed that plain Merkle-Damgard is not indifferentiable from a [random oracle](/random-oracle-model/), and that chopping the output, a prefix-free encoding or a distinct final function fixes it.
- **Not a break of collision resistance.** The attack does not find collisions or preimages. SHA-256 remains a secure hash. The fault is in using it as a MAC by plain prefixing. With SHA-3, the plain prefix MAC $H(k \,\|\, m)$ is not open to this attack, and [KMAC](/kmac/) (NIST SP 800-185) is a standard form of it.

## References
