---
tag: 02765M
kind: algorithm
slug: hmac
name: HMAC
aliases:
- hash-based message authentication code
- Keyed-hash MAC
area: cryptography/hash-functions
level: core
summary: "A MAC from a hash function: HMAC(K, m) = H((K' xor opad) || H((K' xor ipad) || m)). It is a PRF if the compression function is a PRF (Bellare 2006). RFC 2104, FIPS 198-1."
solves: [message-authentication]
model: word-ram
complexity:
  vars: {n: the message length in bytes, b: the block size of the hash in bytes}
  time: {worst: Θ(n/b + 1), average: Θ(n/b + 1), best: Θ(n/b + 1)}
  space: {extra: Θ(b)}
properties: {deterministic: true}
history:
  year: 1996
  people: [Mihir Bellare, Ran Canetti, Hugo Krawczyk]
  note: Bellare, Canetti and Krawczyk defined NMAC and HMAC at CRYPTO 1996. RFC 2104 (1997) and FIPS 198 (2002, revised as FIPS 198-1 in 2008) standardized HMAC.
prereqs: [message-authentication-code, cryptographic-hash-function, merkle-damgard-construction, pseudorandom-function]
see_also: [nmac, kmac, cmac, poly1305, hkdf, pbkdf2, length-extension-attack, timing-attack]
sources:
  - paper: "Mihir Bellare, Ran Canetti and Hugo Krawczyk, Keying hash functions for message authentication, CRYPTO 1996, LNCS 1109, pages 1 to 15"
    locator: the definitions of NMAC and HMAC, and the security of NMAC from a MAC-secure compression function and a weakly collision resistant iterated hash
  - paper: "Mihir Bellare, New proofs for NMAC and HMAC: security without collision-resistance, CRYPTO 2006, LNCS 4117, pages 602 to 619"
    locator: NMAC is a PRF if the compression function is a PRF; HMAC is a PRF under an added related-key PRF assumption on the compression function
  - url: "https://www.rfc-editor.org/rfc/rfc2104"
    title: Hugo Krawczyk, Mihir Bellare and Ran Canetti, RFC 2104, HMAC, Keyed-Hashing for Message Authentication, February 1997
    locator: Section 2 (definition, ipad and opad, key handling), Section 3 (keys), Section 4 (precomputation of the two key states), Section 5 (truncated output), Section 6 (security)
  - url: "https://csrc.nist.gov/pubs/fips/198-1/final"
    title: NIST FIPS 198-1, The Keyed-Hash Message Authentication Code (HMAC), July 2008
    locator: Section 4 (the HMAC specification, steps 1 to 9)
  - url: "https://www.rfc-editor.org/rfc/rfc4231"
    title: Magnus Nystrom, RFC 4231, Identifiers and Test Vectors for HMAC-SHA-224, HMAC-SHA-256, HMAC-SHA-384 and HMAC-SHA-512, December 2005
    locator: Section 4.2 to 4.8, Test Cases 1 to 7
  - url: "https://www.rfc-editor.org/rfc/rfc2202"
    title: Pau-Chen Cheng and Robert Glenn, RFC 2202, Test Cases for HMAC-MD5 and HMAC-SHA-1, September 1997
    locator: Section 2 (HMAC-MD5) and Section 3 (HMAC-SHA-1), test cases 1 to 7
  - url: "https://www.rfc-editor.org/rfc/rfc6151"
    title: Sean Turner and Lily Chen, RFC 6151, Updated Security Considerations for the MD5 Message-Digest and the HMAC-MD5 Algorithms, March 2011
    locator: Section 2.3 (HMAC-MD5)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, 2020
    locator: Chapter 6, Section 6.3 (HMAC and NMAC)
---

HMAC is a [message authentication code](/message-authentication-code/) built from a [cryptographic hash function](/cryptographic-hash-function/) $H$ and a secret key $K$. It hashes twice: $\mathrm{HMAC}(K, m) = H\bigl((K' \oplus \mathrm{opad}) \,\|\, H((K' \oplus \mathrm{ipad}) \,\|\, m)\bigr)$, where $K'$ is the key brought to the block size of $H$. Bellare, Canetti and Krawczyk defined it in 1996; RFC 2104 and FIPS 198-1 standardize it. For a [Merkle-Damgård](/merkle-damgard-construction/) hash, HMAC is the two-key cascade [NMAC](/nmac/) with both keys derived from $K$, and it is a [pseudorandom function](/pseudorandom-function/) when the [compression function](/compression-function/) is one (Bellare 2006). It is the most used MAC on the Internet: TLS, IPsec, SSH, JWT, and the key derivation functions [HKDF](/hkdf/) and [PBKDF2](/pbkdf2/) all use it.

**Notation.** $H$ a hash function with block size $B$ bytes and output $L$ bytes ($B = 64$, $L = 32$ for SHA-256; $B = 128$, $L = 64$ for SHA-512). $K$ the key, $K'$ the key after the key handling, $m$ the message, $\mathrm{ipad}$ the byte `36` repeated $B$ times, $\mathrm{opad}$ the byte `5c` repeated $B$ times, $\|$ concatenation, $\oplus$ bitwise XOR. $f$ the compression function of $H$ with chaining length $c$ bits, IV its initial value. $A$ an adversary, $q$ its number of queries, $t$ its time, $\mathrm{Adv}^{\mathrm{prf}}$ its advantage in the PRF game.

## In plain words

A hash function gives a short fingerprint of a message, but anyone can compute it. A MAC needs a secret: only the people who hold the key can make a valid tag. The obvious idea, hash the key followed by the message, is broken for the common hash functions, because from the hash of a message an attacker can compute the hash of a longer message without the key.

HMAC fixes this with two hash calls. The first call hashes a masked copy of the key together with the message. The second call hashes another masked copy of the key together with the result of the first call. The attacker never sees the inner result, and the outer call makes a fresh, keyed fingerprint of it. So extending the message gives the attacker nothing useful.

## The problem

[Message authentication](/message-authentication/): sender and receiver share a key $K$. The sender attaches a tag $T = \mathrm{MAC}(K, m)$. The receiver recomputes the tag and compares. The goal is EUF-CMA security: an adversary who gets tags for messages of its choice cannot produce a valid tag for a new message. HMAC aims for more: it should be a PRF, that is, its outputs on new messages should look uniformly random. A PRF with $L$-byte output is a secure MAC, with an extra loss of $2^{-8L}$ (see [message authentication code](/message-authentication-code/)).

## The algorithm

```pseudo id=main
HMAC(H, K, m)                       ▷ H has block size B bytes, RFC 2104 Section 2
L1  if |K| > B then K ← H(K)        ▷ a long key is hashed first
L2  K' ← K ‖ 0x00^(B − |K|)         ▷ pad with zero bytes to B bytes
L3  h ← H((K' ⊕ ipad) ‖ m)          ▷ inner hash, ipad = 0x36 repeated B times
L4  return H((K' ⊕ opad) ‖ h)       ▷ outer hash, opad = 0x5c repeated B times

VERIFY(H, K, m, T)                  ▷ T may be a truncated tag of |T| bytes
L5  T' ← the first |T| bytes of HMAC(H, K, m)
L6  d ← OR over all i of (T'[i] ⊕ T[i])
L7  return d = 0                    ▷ no early exit at the first different byte
```

Lines L1 and L2 are the key handling of RFC 2104, Section 2, and of FIPS 198-1, Section 4, steps 1 to 3. RFC 2104 recommends keys of at least $L$ bytes; shorter keys are allowed but weaker, and keys longer than $L$ add little, because the inner chaining value has only $L$ bytes. The two pads differ in many bits (`36` ⊕ `5c` = `6a`, four bits in each byte), so the inner and outer keys are different. Lines L5 to L7 accept a truncated tag: RFC 2104, Section 5, allows the output to be cut to its leftmost $t$ bytes and recommends $t$ of at least half the output and at least 80 bits.

**Precomputation.** The first block of each call is a fixed function of the key. RFC 2104, Section 4, stores the two chaining values $k_{\mathrm{in}} = f(\mathrm{IV}, K' \oplus \mathrm{ipad})$ and $k_{\mathrm{out}} = f(\mathrm{IV}, K' \oplus \mathrm{opad})$ once per key, and each tag then starts from them. This saves two compression calls per message.

**About the code.** The Python code is for study only. It is not constant time, and it must not protect real data. Use `hmac.new` and `hmac.compare_digest` of the Python standard library, libsodium, or a FIPS 140 validated module. The page is about HMAC and not about the hash, so the code takes $H$ from `hashlib` and implements only the HMAC layer.

## Example

RFC 4231, Section 4.3, Test Case 2, with $H$ = SHA-256 ($B = 64$). The key is `Jefe` (4 bytes) and the message is `what do ya want for nothing?` (28 bytes).

| step | value |
|---|---|
| L2: $K'$ | `4a656665` followed by 60 zero bytes |
| $K' \oplus \mathrm{ipad}$, first 8 bytes | `7c53505336363636` |
| $K' \oplus \mathrm{opad}$, first 8 bytes | `16393a395c5c5c5c` |
| L3: inner hash $h$ of 92 bytes | `a2e485863d27f9d864ac8d802432a1ed477d8c4c6f349d16d4e7e917c629cad7` |
| L4: outer hash of 96 bytes | `5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843` |

The tag in the last row is the HMAC-SHA-256 value of RFC 4231. The inner input has 92 bytes, so with the SHA-256 padding it fills two 64-byte blocks; the outer input has 96 bytes and also fills two blocks. The tag costs four compression calls, or two with the precomputed key states. Test Case 5 of the same RFC truncates the tag to 128 bits: HMAC-SHA-256 then gives `a3b6167473100ee06e0c796c2955552b`.

**Why not $H(K \| m)$.** For SHA-256, the value $H(K \| m)$ is the chaining state after the padded input. An attacker who knows it and the length of $K \| m$ can continue the iteration and get $H(K \| m \| \mathrm{pad} \| s)$ for any suffix $s$, a valid tag for a new message. This is the [length extension attack](/length-extension-attack/). In HMAC the inner value $h$ is hidden, and the only output passes through the outer keyed call.

## Correctness

**Claim 1 (verification).** VERIFY$(H, K, m, T)$ returns true if and only if $T$ is a prefix of $\mathrm{HMAC}(H, K, m)$ of length at least 1. Line L6 computes the OR of the byte differences, which is 0 exactly when all bytes are equal.

**Claim 2 (HMAC is NMAC with derived keys).** Let $H$ be a Merkle-Damgård hash with compression function $f$, and let $F_k(x)$ be the iteration of $f$ from the chaining value $k$ over $x$ followed by the padding for a total length of $B + |x|$ bytes. Set $k_2 = f(\mathrm{IV}, K' \oplus \mathrm{ipad})$ and $k_1 = f(\mathrm{IV}, K' \oplus \mathrm{opad})$. Then $\mathrm{HMAC}(K, m) = F_{k_1}(F_{k_2}(m)) = \mathrm{NMAC}_{k_1, k_2}(m)$. The proof is below. It holds for MD5, SHA-1 and SHA-2, and it does not hold for SHA-3, which is a sponge.

**Claim 3 (key equivalence).** Two keys with the same $K'$ give the same function. So a key of at most $B$ bytes and the same key with zero bytes appended give the same tags, and a key longer than $B$ bytes and its hash give the same tags. This is a property of the key handling, not an attack on HMAC as a PRF with a uniform key, but protocols must not assume that different key strings give independent functions.

**Security.** The model is the standard model, with assumptions on the compression function $f$.

- Bellare, Canetti and Krawczyk (1996) proved NMAC unforgeable if $f$ is a secure MAC and the keyed iterated hash is weakly collision resistant (collision resistant against an adversary who does not know the key).
- Bellare (2006) removed the collision resistance assumption: NMAC is a PRF if $f$ is a PRF when keyed through its chaining input. HMAC is a PRF if, in addition, $f$ keyed through its message input is a PRF against the related-key attack given by the two derived keys $K' \oplus \mathrm{ipad}$ and $K' \oplus \mathrm{opad}$. The reduction is not tight: the bound has a term that grows with $q^2$ and with the message length in blocks. Gaži, Pietrzak and Rybár (CRYPTO 2014) later gave a tighter analysis of NMAC and HMAC.
- These results matter for MD5 and SHA-1: collisions in a hash do not by themselves break HMAC, because the proof does not use collision resistance. RFC 6151, Section 2.3, says that the known attacks on HMAC-MD5 do not seem to give a practical attack on its use as a MAC, and still advises against HMAC-MD5 for new protocols.
- **A generic limit.** Any iterated MAC with a $c$-bit chaining value admits a forgery after about $2^{c/2}$ queries, by an internal collision that is then extended (Preneel and van Oorschot, CRYPTO 1995). For HMAC-SHA-256, $c = 256$.

## Complexity

For a message of $n$ bytes and a hash with block size $B$ and output $L$ bytes, the inner hash processes $B + n$ bytes and the outer hash $B + L$ bytes. For SHA-256 this is $\lceil (n + 9)/64 \rceil + 1$ compression calls for the inner hash and 2 for the outer hash. With the precomputed key states it is $\lceil (n + 9)/64 \rceil + 1$ calls in total, so for long messages HMAC costs the same as one hash of the message. Extra space is $\Theta(B)$ for the padded key, or two chaining values when the states are precomputed. A streaming implementation needs no buffer for the message.

## Properties

- **Deterministic.** The same key and message always give the same tag. HMAC needs no nonce.
- **Black-box use of $H$.** HMAC calls $H$ as a whole, so the code of the hash is reused without change. This was a design goal in 1996.
- **Not vulnerable to length extension**, unlike $H(K \| m)$.
- **Works with any hash.** HMAC-SHA-3 and HMAC-BLAKE2 are well defined, and the standard library compares equal to this code for them. For a sponge such as SHA-3, [KMAC](/kmac/) or a keyed $H(K \| m)$ is enough and cheaper, because a sponge has no length extension.
- **A PRF, not only a MAC**, under the assumptions above. This is why HMAC is used for key derivation.

## Variants and improvements

- **NMAC.** Two independent keys enter the chaining values directly. It is the theoretical form; HMAC derives both keys from one key so that it needs no change to the hash code. See [NMAC](/nmac/).
- **Truncated HMAC.** HMAC-SHA-256-128 and the 96-bit tags of IPsec (HMAC-SHA-1-96). The forgery probability of one guess rises to $2^{-t}$ for $t$ tag bits, but the PRF bound of the full output does not get worse.
- **HMAC as a KDF and a PRF.** [HKDF](/hkdf/) (RFC 5869) uses HMAC for extract and expand, [PBKDF2](/pbkdf2/) iterates it with a password as the key, the TLS 1.2 PRF and HMAC_DRBG of NIST SP 800-90A use it. Each of these uses the PRF property, not only unforgeability.
- **[KMAC](/kmac/).** The SHA-3 based MAC of NIST SP 800-185, one sponge call with no nesting.
- **[CMAC](/cmac/) and [Poly1305](/poly1305/).** MACs from a block cipher and from a universal hash, with different assumptions and costs.

## When to use it

Use HMAC with SHA-256 or SHA-512 as the default MAC for data at rest and in protocols, and as the PRF inside key derivation. Use a key of at least $L$ bytes from a good random source. For new designs that already use SHA-3, KMAC is the direct choice. For short inputs where speed matters, such as keys of a hash table, a PRF like [SipHash](/siphash/) is much faster.

## Pitfalls

- **Comparing tags with `==`.** A compare that stops at the first different byte leaks, through its [timing](/timing-attack/), how many leading bytes of a guess are right. Then an attacker finds a tag one byte at a time. Use `hmac.compare_digest` or a loop as in lines L6 and L7.
- **Building $H(K \| m)$ or $H(m \| K)$ by hand.** The first falls to length extension; the second depends on the collision resistance of $H$ for its security.
- **Truncating too much.** Each guess at a $t$-bit tag succeeds with probability $2^{-t}$. Keep $t \ge 80$ (RFC 2104) and count the number of tries the attacker can make.
- **Keys from passwords.** HMAC with a password as the key is not slow, so it does not resist guessing. Use [PBKDF2](/pbkdf2/) or a [memory-hard function](/memory-hard-function/) for passwords.
- **Key equivalence.** Keys `key` and `key\x00` give the same tags. Do not use the key string as an identity.
- **Reusing one key for two purposes**, for example as a MAC key and an encryption key. Derive separate keys with HKDF.

## Implementations

The Python code gives `normalize_key` (lines L1 and L2), `hmac_digest` (lines L3 and L4), `hmac_truncated`, `tags_equal` and `hmac_verify`, with the line markers of the pseudocode. The file has the same name as the standard module `hmac`, so the tests load both modules by path. The tests check all of RFC 4231, Test Cases 1 to 7, for SHA-224, SHA-256, SHA-384 and SHA-512, all of RFC 2202 for MD5 and SHA-1 with the 96-bit truncations, and the standard library `hmac` module on random keys of 0 to 200 bytes for six hashes. They also check that a wrong key and every single changed bit of a tag are rejected, the key equivalences of Claim 3, and that one changed message bit changes about half of the 256 output bits.

## History

Before 1996, protocols used ad hoc keyed hashes such as $H(K \| m)$, $H(m \| K)$ and the envelope $H(K \| m \| K)$, and Preneel and van Oorschot showed generic attacks on several of them (1995). Bellare, Canetti and Krawczyk proposed NMAC and HMAC at CRYPTO 1996 with a proof of security, and RFC 2104 (February 1997) made HMAC an Internet standard, with test vectors for MD5 and SHA-1 in RFC 2202. NIST published FIPS 198 in 2002 and FIPS 198-1 in July 2008. After the collision attacks on MD5 and SHA-1 (2004 and 2005), Bellare's 2006 proof explained why HMAC stayed secure: it needs a PRF, not collision resistance.

## References
