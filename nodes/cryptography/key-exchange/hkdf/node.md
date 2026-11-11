---
tag: DCNWKP
kind: algorithm
slug: hkdf
name: HKDF
aliases:
- HMAC-based Key Derivation Function
- HMAC-based key derivation function
area: cryptography/key-exchange
level: advanced
summary: An extract-then-expand key derivation function built on HMAC (RFC 5869). It turns a shared secret into a uniform key, then stretches it into many keys bound to a context string.
solves: [key-agreement-problem]
model: word-ram
complexity:
  vars: {I: bytes of input keying material, L: bytes of output, c: bytes of the info string, h: bytes of the hash output}
  time: {worst: Θ(I + (1 + L/h)(h + c)), average: Θ(I + (1 + L/h)(h + c)), best: Θ(I + (1 + L/h)(h + c))}
  space: {extra: Θ(L + c)}
properties: {deterministic: true}
history:
  year: 2010
  people: [Hugo Krawczyk, Pasi Eronen]
  note: Krawczyk designed HKDF and gave its analysis at CRYPTO 2010. RFC 5869 (May 2010, Krawczyk and Eronen) specified it.
prereqs: [hmac, session-key]
see_also: [hmac, session-key, tls-handshake, x25519, hybrid-key-exchange, randomness-extractor, pseudorandom-function, double-ratchet]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc5869"
    title: Hugo Krawczyk and Pasi Eronen, RFC 5869, HMAC-based Extract-and-Expand Key Derivation Function (HKDF), May 2010
    locator: Section 2.2 (HKDF-Extract), Section 2.3 (HKDF-Expand), Section 3 (notes to implementers on salt, info and skipping extract) and Appendix A (test vectors)
  - paper: doi:10.1007/978-3-642-14623-7_34
    title: Hugo Krawczyk, Cryptographic extraction and key derivation, the HKDF scheme, CRYPTO 2010, LNCS 6223, pages 631 to 648
    locator: the extract-then-expand design, the definition of KDF security, and the analysis of HMAC as an extractor and as a PRF
  - url: "https://www.rfc-editor.org/rfc/rfc8446"
    title: Eric Rescorla, RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3, August 2018
    locator: Section 7.1 (the key schedule, HKDF-Expand-Label and Derive-Secret)
  - url: "https://www.rfc-editor.org/rfc/rfc8448"
    title: Martin Thomson, RFC 8448, Example Handshake Traces for TLS 1.3, January 2019
    locator: Section 3 (the early secret, the handshake secret and the handshake traffic keys of the simple 1-RTT handshake)
  - url: "https://csrc.nist.gov/pubs/sp/800/56/c/r2/final"
    title: Elaine Barker, Lily Chen and Richard Davis, NIST SP 800-56C Rev. 2, Recommendation for Key-Derivation Methods in Key-Establishment Schemes, August 2020
    locator: the two-step key derivation, randomness extraction followed by key expansion, with HMAC
---

HKDF is a key derivation function that turns a secret with some entropy, such as a [Diffie-Hellman](/diffie-hellman/) shared value, into one or more cryptographic keys of any length. It works in two steps: Extract compresses the input into a short uniform pseudorandom key with [HMAC](/hmac/) keyed by a salt, and Expand stretches that key into as many bytes as needed, bound to a context string called info. Hugo Krawczyk designed it in 2010 with a proof in standard models, and RFC 5869 specifies it. TLS 1.3, Signal, Noise, WireGuard, QUIC and many other protocols derive all their keys with it.

**Notation.** $\mathrm{HMAC}(K, M)$ is HMAC with a hash function of output length $h$ bytes ($h = 32$ for SHA-256). IKM is the input keying material, salt an optional non-secret random value, info a context string, and $L \le 255h$ the number of output bytes. PRK is the pseudorandom key and OKM the output keying material. $\|$ is concatenation and $\mathrm{byte}(i)$ is the single byte with value $i$.

## In plain words

A key exchange gives two people the same secret number, but that number is not a ready-made key: some of its bits are predictable, and they may need several keys of different sizes.

HKDF fixes both problems. First it mixes the secret through a keyed hash, which squeezes out the predictable part and leaves a short key that looks fully random. Then it feeds that key, a counter and a label into the same hash again and again, and joins the outputs until it has enough bytes.

Different labels, such as "client key" and "server key", give unrelated keys from the same secret, so one exchange can safely make many keys.

## The problem

After a key exchange the parties share a secret $Z$ that is hard to guess but not uniform: a DH value lies in a group, not among all bit strings, and an attacker may know some of its structure. They need several independent uniform keys, for each direction and purpose, that stay secure even if one of them leaks. A key derivation function must produce them from $Z$, with optional salt and a context, deterministically so that both parties get the same keys. This is the last step of solving the [key agreement problem](/key-agreement-problem/) in practice.

## The algorithm

```pseudo id=main
HKDF(salt, IKM, info, L)                           ▷ RFC 5869
L1  if salt is empty then salt ← h zero bytes
L2  PRK ← HMAC(salt, IKM)                          ▷ HKDF-Extract
L3  N ← ⌈L / h⌉                                     ▷ HKDF-Expand from here
L4  if N > 255 then error
L5  OKM ← empty; T ← empty
L6  for i ← 1 to N do
L7      T ← HMAC(PRK, T ‖ info ‖ byte(i)); OKM ← OKM ‖ T
L8  return the first L bytes of OKM
```

**About the code.** Lines L1 and L2 are HKDF-Extract and lines L3 to L8 are HKDF-Expand; the Python code has a function for each and a function that runs both. Note that the salt is the HMAC key in Extract and the IKM is the message, which is the reverse of what one might guess: this way the salt, not the secret, plays the role of the extractor's seed. The counter is one byte, which is why $L \le 255h$. The code also has HKDF-Expand-Label and Derive-Secret from the TLS 1.3 key schedule (RFC 8446, Section 7.1), whose info is a structure with the output length, the label "tls13 " followed by a name, and a context hash. It uses the HMAC of the Python standard library, checks the three SHA-256 vectors of RFC 5869 Appendix A and the start of the RFC 8448 key schedule, and is for study only, not constant time.

## Example

**RFC 5869, test case A.1** (SHA-256). IKM is 22 bytes of `0x0b`, the salt is `000102030405060708090a0b0c`, info is `f0f1f2f3f4f5f6f7f8f9`, and $L = 42$. Extract gives

$$\mathrm{PRK} = \texttt{077709362c2e32df0ddc3f0dc47bba6390b6c73bb50f9c3122ec844ad7c2b3e5}.$$

Expand needs $N = \lceil 42/32 \rceil = 2$ blocks: $T(1) = \mathrm{HMAC}(\mathrm{PRK}, \mathrm{info} \,\|\, \texttt{01})$ and $T(2) = \mathrm{HMAC}(\mathrm{PRK}, T(1) \,\|\, \mathrm{info} \,\|\, \texttt{02})$. The first 42 bytes of $T(1) \,\|\, T(2)$ are

$$\mathrm{OKM} = \texttt{3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c5db02d56ecc4c5bf34007208d5b887185865}.$$

**TLS 1.3 (RFC 8448, Section 3).** With no pre-shared key, the early secret is $\mathrm{HKDF\text{-}Extract}(0^{32}, 0^{32})$ = `33ad0a1c...f170f92a`. Derive-Secret with the label "derived" gives the salt `6f2615a1...6c3611ba` for the next Extract, whose IKM is the [X25519](/x25519/) shared secret `8bd4054f...0f89492d`; the result is the handshake secret `1dc826e9...043fbeac`. HKDF-Expand-Label then gives the server's 16-byte handshake key `3fce516009c21727d0f2e4e86ee403bc` and 12-byte IV `5d313eb2671276ee13000b30`.

## Correctness

HKDF is a deterministic function of (salt, IKM, info, $L$), so two parties with the same inputs get the same OKM; this is all that agreement needs. The loop computes the chain $T(0) = $ empty, $T(i) = \mathrm{HMAC}(\mathrm{PRK}, T(i - 1) \,\|\, \mathrm{info} \,\|\, \mathrm{byte}(i))$ of RFC 5869 Section 2.3, and since $N h \ge L$ the output has exactly $L$ bytes. Since $T(i)$ does not depend on $L$, the output for a smaller $L$ is a prefix of the output for a larger one. The full proof is below.

**Security, in brief.** Krawczyk (2010) proves that HKDF is a secure KDF if HMAC with a random salt is a good randomness extractor on the distribution of IKM (or, without salt, under stronger assumptions on the compression function) and HMAC keyed with PRK is a [pseudorandom function](/pseudorandom-function/). Expand is a PRF in counter-and-feedback mode, so outputs with different info strings, and the separate blocks of one output, are independent-looking keys.

## Complexity

Extract is one HMAC over $I$ bytes, $\Theta(I + h)$ time. Expand makes $N = \lceil L/h \rceil$ HMAC calls, each over $h + c + 1$ bytes, plus the constant cost of HMAC's two extra hash blocks; that is $\Theta((1 + L/h)(h + c))$. With SHA-256, deriving a 32-byte key costs four compression function calls for Extract with a short IKM and four for one Expand block. The extra space is the output and one block, $\Theta(L + c)$ with the info buffer.

## Properties

- **Deterministic.** Both parties get the same keys from the same inputs.
- **Prefix property.** The first $L'$ bytes of a longer output equal the output of length $L'$; protocols must therefore put the length or purpose in info when that matters (TLS does, in HkdfLabel).
- **Domain separation.** Different info strings give independent keys from one PRK.
- **Two clear roles.** Extract handles non-uniform input; Expand handles length and context. If IKM is already a uniform key, Extract may be skipped (RFC 5869, Section 3.3).
- **Not slow.** HKDF is fast on purpose, so it is not a password hash.

## Variants and improvements

- **HKDF-Expand-Label** (TLS 1.3) puts the length, a "tls13 " label and a transcript hash in info; Derive-Secret uses it with the hash of the handshake messages.
- **NIST SP 800-56C** allows the same two-step derivation with HMAC, and a one-step KDF that hashes $\mathrm{counter} \,\|\, Z \,\|\, \mathrm{OtherInfo}$.
- **Hash choices.** HKDF-SHA-256 and HKDF-SHA-384 in TLS and HPKE, and SHA-256 or SHA-512 in Signal's X3DH.
- **KMAC and the SHAKE functions** can replace both steps with one call to a variable-output function.
- **Password-based KDFs.** For low-entropy secrets, use [PBKDF2](/pbkdf2/), [scrypt](/scrypt/) or [Argon2](/argon2/), which are slow on purpose.

## When to use it

Use HKDF after every key exchange and whenever one secret must give several keys: derive client and server keys, encryption and MAC keys, and new chain keys in a [ratchet](/double-ratchet/). Put a random salt in Extract when one is available (a nonce from the handshake is fine), and put the protocol name, the roles and a transcript hash in info. In a [hybrid key exchange](/hybrid-key-exchange/), feed both shared secrets to one Extract. Do not use it for passwords.

## Pitfalls

- **Swapped arguments.** HMAC(IKM, salt) instead of HMAC(salt, IKM) gives a different, unstandard function; libraries differ in the order of their parameters.
- **Same info for different keys.** Two keys derived with the same PRK and info are the same key, or one is a prefix of the other.
- **Secret salt assumptions.** The salt need not be secret, but it must not be chosen by the attacker after seeing IKM, or the extractor guarantee is lost.
- **Too long an output.** $L > 255h$ is an error, not a wrap-around.
- **Low-entropy input.** HKDF cannot add entropy; a weak password stays weak.

## Implementations

## History

Key derivation in early protocols was ad hoc: TLS 1.0 and 1.1 used their own PRF that combined HMAC-MD5 and HMAC-SHA-1, TLS 1.2 used one built on HMAC-SHA-256, and IKE used another. Hugo Krawczyk, who co-designed HMAC in 1996, proposed the extract-then-expand approach and HKDF, and published its analysis at CRYPTO 2010. RFC 5869 by Krawczyk and Eronen appeared in May 2010. Signal's protocols adopted it, NIST SP 800-56C allowed two-step derivation of this kind, and TLS 1.3 (2018) rebuilt its whole key schedule on HKDF.

## References
