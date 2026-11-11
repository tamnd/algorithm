---
tag: T94CVM
kind: algorithm
slug: poly1305
name: Poly1305
area: cryptography/symmetric-ciphers
level: advanced
summary: A one-time MAC that evaluates the message as a polynomial at a secret clamped point r modulo 2^130 - 5 and adds a secret s. Each try forges with probability at most 8⌈L/16⌉/2^106.
solves: [message-authentication]
model: word-ram
complexity:
  vars: {m: the number of 16-byte message blocks}
  time: {worst: Θ(m), average: Θ(m), best: Θ(m)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2005
  people: [Daniel J. Bernstein]
  note: Bernstein published Poly1305-AES at FSE 2005. NaCl paired Poly1305 with XSalsa20, and RFC 7539 (2015) and RFC 8439 (2018) paired it with ChaCha20 for IETF protocols.
prereqs: [message-authentication-code, universal-hash-family, polynomial-evaluation]
see_also: [chacha20-poly1305, gcm-mode, chacha20, message-authentication-code, universal-hashing, nonce, cmac, hmac]
sources:
  - url: "https://cr.yp.to/mac/poly1305-20050329.pdf"
    title: Daniel J. Bernstein, The Poly1305-AES message-authentication code, Fast Software Encryption (FSE 2005), LNCS 3557, pages 32 to 49
    locator: Section 2 (specification and the restrictions on r), Section 3 (the security guarantee with the bound (1 - C/2^128)^(-(C+1)/2) 8D⌈L/16⌉/2^106, and Theorems 3.1 to 3.3)
  - url: "https://www.rfc-editor.org/rfc/rfc8439"
    title: Yoav Nir and Adam Langley, RFC 8439, ChaCha20 and Poly1305 for IETF Protocols, 2018
    locator: Section 2.5 (Poly1305 and the clamp), Section 2.5.1 (pseudocode), Section 2.5.2 (example and test vector), Section 2.6 (one-time key from ChaCha20) and Appendix A.3 (Test Vectors 1 to 11)
  - paper: "Mark N. Wegman and J. Lawrence Carter, New hash functions and their use in authentication and set equality, Journal of Computer and System Sciences 22(3), 1981, pages 265 to 279"
    locator: the universal hash with a one-time mask that Poly1305 instantiates
  - paper: "Victor Shoup, On fast and provably secure message authentication based on universal hashing, CRYPTO 1996, LNCS 1109, pages 313 to 328"
    locator: Theorem 5.4 as cited by Bernstein (the security of a universal hash plus a PRP of a nonce)
---

Poly1305 is a message authentication code designed by Daniel J. Bernstein (FSE 2005). It takes a 32-byte one-time key $(r, s)$ and a message, and returns a 16-byte tag. The message is cut into 16-byte blocks, each block becomes a number $c_i$ of up to 129 bits, and the tag is $\bigl(\bigl(\sum_i c_i r^{q+1-i}\bigr) \bmod (2^{130} - 5) + s\bigr) \bmod 2^{128}$. The polynomial part is a universal hash and $s$ is a one-time mask, in the style of Wegman and Carter. A key must be used for one message only: two messages under the same key reveal $r$ and $s$, and then the attacker can tag anything. [ChaCha20-Poly1305](/chacha20-poly1305/) makes a fresh key for every message from the nonce.

**Notation.** $p = 2^{130} - 5$ (a prime), $r$ the clamped first half of the key, $s$ the second half, both read as little-endian integers; $M$ the message of $\ell$ bytes, $q = \lceil \ell / 16 \rceil$ its number of blocks, $c_1, \ldots, c_q$ the block numbers, $a$ the accumulator, $L$ the maximum message length in bytes and $D$ the number of forgery attempts.

## In plain words

Read each 16-byte piece of the message as a number, and put a 1 just above its top byte, so that pieces of different lengths and trailing zero bytes give different numbers. Start with zero. For each piece, add the piece and multiply by the secret number $r$, all modulo the prime $2^{130} - 5$. At the end add the second secret number $s$ and keep the low 128 bits. That is the tag.

Without $s$, the tag is a polynomial in $r$ whose coefficients are the message pieces. Someone who wants to change the message must hit the same value with a different polynomial, which happens only for a few values of $r$ out of $2^{106}$. The value $s$ hides the polynomial value, but only once: two tags under the same $s$ give the difference of two polynomial values with no mask, and from that $r$ follows.

## The problem

[Message authentication](/message-authentication/) with a one-time key: after the attacker sees one message with its tag, it must not be able to produce a valid tag for any other message. Many-time security follows if each message gets a fresh pseudorandom key, as in Poly1305-AES, where $s = \mathrm{AES}_k(n)$ for a nonce $n$, or in ChaCha20-Poly1305.

## The algorithm

```pseudo id=main
POLY1305(key, M)                         ▷ key has 32 bytes, RFC 8439 Section 2.5.1
L1  r ← LE(key[0 .. 15]) AND 0x0ffffffc0ffffffc0ffffffc0fffffff     ▷ clamp
L2  s ← LE(key[16 .. 31])
L3  a ← 0;  p ← 2^130 − 5
L4  for each 16-byte chunk B of M, the last one possibly shorter, do
L5      c ← LE(B ‖ 0x01)                  ▷ c = LE(B) + 2^(8·|B|)
L6      a ← (a + c) · r mod p
L7  a ← (a + s) mod 2^128
L8  return the 16 bytes of a, little-endian

VERIFY(key, M, T)
L9  return POLY1305(key, M) = T, compared in constant time
```

The clamp in line L1 clears the top 4 bits of bytes 3, 7, 11 and 15 of $r$ and the low 2 bits of bytes 4, 8 and 12. It leaves 106 free bits, so $r$ takes $2^{106}$ values, and it makes the products fit in fewer machine words in fast implementations. Line L5 appends the byte `01`, which adds $2^{128}$ for a full chunk and $2^{8k}$ for a final chunk of $k$ bytes. The loop is Horner's rule, so after all chunks $a = \sum_{i=1}^{q} c_i r^{q+1-i} \bmod p$. Line L7 adds $s$ to the fully reduced value and drops all bits above 128.

**About the code.** The Python code is for study only and is not constant time: Python big integers take time that depends on their values. Real implementations use limbs of 26 or 64 bits with carries and a final constant-time reduction; RFC 8439, Appendix A.3, Test Vectors 5 to 11 check exactly those edge cases. Use `crypto_onetimeauth` or the AEAD of libsodium, or a FIPS 140 validated module.

## Example

RFC 8439, Section 2.5.2. The key is `85d6be7857556d337f4452fe42d506a8` `0103808afb0db2fd4abff6af4149f51b`. After the clamp, $r$ = `806d5400e52447c036d555408bed685` and $s$ = `1bf54941aff6bf4afdb20dfb8a800301` (as numbers). The message is the 34 bytes `Cryptographic Forum Research Group`.

| chunk | $c$ (with the `01` byte) | $a$ after L6 |
|---|---|---|
| `Cryptographic Fo` | `016f4620636968706172676f7470797243` | `2c88c77849d64ae9147ddeb88e69c83fc` |
| `rum Research Gro` | `016f7247206863726165736552206d7572` | `2d8adaf23b0337fa7cccfb4ea344b30de` |
| `up` | `017075` | `28d31b7caff946c77c8844335369d03a7` |

Then $a + s$ = `2a927010caf8b2bc2c6365130c11d06a8`; its low 128 bits in little-endian order give the tag `a8061dc1305136c6c22b8baf0c0127a9`.

**What key reuse gives away.** Suppose the same key also tags the two 16-byte messages $m_1$ = `Cryptographic Fo` and $m_2$ = `rum Research Gro` on their own. The tags are $t_1$ = `fd861c7184f98f45dc6d5b4dc6c081e4` and $t_2$ = `5a3a3f79bc3fef987ecdb135508869be`. Write $a_i = c_i r \bmod p$. Then $t_i \equiv a_i + s \pmod{2^{128}}$, so $a_1 - a_2 = (t_1 - t_2) + j \cdot 2^{128}$ for some integer $j$ with $|j| \le 4$, and $r \equiv (a_1 - a_2)(c_1 - c_2)^{-1} \pmod p$. Of the nine candidates, only the one with $j = 2$ passes the clamp, and it is the real $r$ = `806d5400e52447c036d555408bed685`. Then $s = (t_1 - c_1 r \bmod p) \bmod 2^{128}$ gives the real $s$, and the attacker can tag any message. The tests run this attack. For messages that differ in only a few bytes several candidates can pass the clamp; the attacker then sends one forgery per candidate, at most nine.

## Correctness

**Claim.** (1) VERIFY accepts every tag that POLY1305 computes. (2) After the loop, $a = \sum_{i=1}^{q} c_i r^{q+1-i} \bmod p$ (Horner's rule). (3) The map from a message to its polynomial is injective, even modulo $p$ and up to an added constant: if $M \ne M'$, then $\sum c'_i x^{q'+1-i} - \sum c_i x^{q+1-i} - u$ is a nonzero polynomial modulo $p$ for every integer $u$ (Bernstein, Theorem 3.2). (4) For distinct messages of at most $L$ bytes and any 16-byte difference $g$, at most $8\lceil L/16 \rceil$ values of $r$ satisfy $H_r(M) = H_r(M') + g$ (Bernstein, Theorem 3.3). The key step for (3) and (4) is that every $c_i$ lies in $[1, 2^{129}]$ thanks to the `01` byte, so differences of coefficients are smaller than $p$ in absolute value. The full proof is below.

**Security, as Bernstein states it.** For Poly1305-AES with tag $H_r(m) + \mathrm{AES}_k(n)$: assume the attacker sees at most $C$ authenticated messages, attempts at most $D$ forgeries, all messages have at most $L$ bytes, and the attacker has probability at most $\delta$ of distinguishing $\mathrm{AES}_k$ from a uniform random permutation after $C + D$ queries. Then, with probability at least
$$1 - \delta - \frac{(1 - C/2^{128})^{-(C+1)/2} \cdot 8D\lceil L/16 \rceil}{2^{106}},$$
all of the attacker's forgeries are rejected. If $C \le 2^{64}$, the attacker's chance of success is at most $\delta + 14D\lceil L/16 \rceil/2^{106}$. (Section 3 of the FSE 2005 paper; the step from the differential bound to this guarantee is Theorem 5.4 of Shoup, CRYPTO 1996.)

**One-time use.** With a uniform key used for one message, $s$ is a perfect one-time mask modulo $2^{128}$, so the seen tag says nothing about $r$, and a forgery $(M', T')$ is accepted only if $H_r(M') = H_r(M) + (T' - T)$. By claim (4) each attempt succeeds with probability at most $8\lceil L/16 \rceil / 2^{106}$, and $D$ attempts with at most $8D\lceil L/16 \rceil / 2^{106}$. For messages of 1 GiB ($L = 2^{30}$), one attempt succeeds with probability at most $2^{-77}$. The bound is unconditional: it needs no assumption about any cipher. It degrades linearly with the message length, so it is not tight for short messages compared with the $2^{-128}$ of an ideal MAC.

## Complexity

One addition and one multiplication modulo $p$ per 16-byte chunk: $\Theta(m)$ operations on 130-bit numbers, each a constant number of word operations on a machine with 64-bit words. Extra space is $\Theta(1)$: $r$, $s$ and the accumulator. Fast implementations precompute $r^2, r^3, r^4$ and process several chunks in parallel, because the polynomial can be split by powers of $r$; vector code reaches about one cycle per byte or less.

## Properties

- **Deterministic** for a given key, and a one-time MAC: secure for one message per key.
- **A universal hash plus a mask.** $H_r$ is $\varepsilon$-almost-$\Delta$-universal with $\varepsilon = 8\lceil L/16 \rceil/2^{106}$ for the difference modulo $2^{128}$, and $s$ is added modulo $2^{128}$.
- **Information-theoretic security** for one message with a uniform key; computational security when $s$ (or both $r$ and $s$) comes from a PRF of a nonce.
- **Linear in the message.** For a fixed key, the tag is affine in the block numbers modulo $p$ before the final addition. This is why reuse is fatal.
- **Parallel and incremental.** Blocks can be processed in any grouping with powers of $r$.
- **No block cipher inside.** It uses only integer arithmetic, so it is fast in software without AES instructions.

## Variants and improvements

- **Poly1305-AES.** The original: $r$ is a long-term secret, and $s = \mathrm{AES}_k(n)$ for a unique 16-byte nonce $n$. The bound above is for this form.
- **Poly1305 with XSalsa20 in NaCl** (`crypto_secretbox`) and **with ChaCha20 in RFC 8439**: both $r$ and $s$ come from the first 32 bytes of the stream cipher output for the nonce, so the key is fresh per message. See [ChaCha20-Poly1305](/chacha20-poly1305/).
- **GHASH in [GCM](/gcm-mode/).** The same polynomial idea in $\mathrm{GF}(2^{128})$ instead of modulo a prime, with the same failure under nonce reuse.
- **Other primes.** Bernstein chose $2^{130} - 5$ because it is just above $2^{129}$, the size of a chunk with its extra bit, and because reduction by $2^{130} \equiv 5$ is a multiply by 5.

## When to use it

Use Poly1305 inside an AEAD such as [ChaCha20-Poly1305](/chacha20-poly1305/) or XSalsa20-Poly1305, where the construction derives a fresh key for each message. It is a good choice on CPUs without AES or carry-less multiply instructions, where it is faster than GHASH and constant time without tables. Do not use raw Poly1305 with a long-term key; for a general-purpose MAC use [HMAC](/hmac/) or [CMAC](/cmac/).

## Pitfalls

- **Reusing the one-time key.** Two tags reveal $r$ and $s$, as in the example, and longer messages give a polynomial equation whose roots include $r$. A nonce repeat in ChaCha20-Poly1305 has the same effect.
- **Skipping the clamp.** The tag is then different from every standard implementation, and the bound changes.
- **Incomplete final reduction.** An implementation that keeps $a$ only partially reduced must reduce it fully modulo $p$ before adding $s$. Test Vectors 5 to 11 of Appendix A.3 exist because real implementations got this wrong.
- **The weak key $r = 0$.** Then the tag is $s$ for every message (Appendix A.3, Test Vector 2). With $r$ from a PRF this has probability $2^{-106}$.
- **Comparing tags with an early exit.** Use a constant-time comparison such as `crypto_verify_16`.
- **Confusing the layers.** Poly1305 authenticates bytes; the AEAD around it must encode the lengths of the associated data and the ciphertext, as RFC 8439, Section 2.8, does, or two different inputs can collide.

## Implementations

The Python code gives `clamp`, `poly1305_mac` with the line markers of the pseudocode, and `poly1305_verify`, which compares every byte. The tests check RFC 8439, Section 2.5.2, all eleven Test Vectors of Appendix A.3, the clamp mask, rejection of single changed bits in the message and the tag, the weak key $r = 0$, and the key reuse attack, which recovers $(r, s)$ from two tags and forges a tag for a new message.

## History

Wegman and Carter (1981) introduced authentication by a universal hash with a one-time mask, and polynomial evaluation hashes were analyzed in the 1990s, for example by den Boer, Bierbrauer and others, and by Shoup (1996). Bernstein designed Poly1305-AES for speed with a prime that allows fast floating-point and integer arithmetic, and published it at FSE 2005, together with fast implementations for many CPUs and a proof that $2^{130} - 5$ is prime. NaCl (2008 onwards) used Poly1305 with XSalsa20 in `crypto_secretbox`. Langley and others brought ChaCha20-Poly1305 to TLS in 2013, and the IETF standardized it in RFC 7539 (2015), replaced by RFC 8439 (2018).

## References
