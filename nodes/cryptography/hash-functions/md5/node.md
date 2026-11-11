---
tag: E0VM6D
kind: algorithm
slug: md5
name: MD5
aliases:
- Message Digest 5
area: cryptography/hash-functions
level: core
summary: Rivest's 128-bit hash of 1991 (RFC 1321), four rounds of 16 steps. Broken for collisions since Wang and Yu (2005); chosen-prefix collisions forged certificates.
model: word-ram
complexity:
  vars: {n: the message length in bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1991
  people: [Ronald L. Rivest]
  note: Rivest designed MD5 in 1991 as a stronger MD4 and published it as RFC 1321 in April 1992. Wang and Yu published the first collisions in 2005.
prereqs: [md4, merkle-damgard-construction]
see_also: [sha-1, sha-2, chosen-prefix-collision, collision-finding, collision-resistance, preimage-resistance, hmac, length-extension-attack]
sources:
  - paper: doi:10.17487/RFC1321
    title: R. Rivest, RFC 1321, The MD5 Message-Digest Algorithm, April 1992
    locator: Section 3 (steps 1 to 5; Section 3.4 has the four rounds and the sine table), Appendix A.3 (reference code md5c.c with the 64 constants) and Appendix A.5 (test suite)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 9.4.2, Algorithm 9.51 (MD5) and Remark 9.52
  - paper: "Xiaoyun Wang and Hongbo Yu, How to break MD5 and other hash functions, Advances in Cryptology, EUROCRYPT 2005, LNCS 3494, Springer, 2005"
    locator: the two-block differential path and the first MD5 collisions
  - paper: "Marc Stevens, Arjen Lenstra and Benne de Weger, Chosen-prefix collisions for MD5 and colliding X.509 certificates for different identities, Advances in Cryptology, EUROCRYPT 2007, LNCS 4515, Springer, 2007"
    locator: the first chosen-prefix collision attack on MD5 and two colliding certificates with different names
  - paper: "Marc Stevens, Alexander Sotirov, Jacob Appelbaum, Arjen Lenstra, David Molnar, Dag Arne Osvik and Benne de Weger, Short chosen-prefix collisions for MD5 and the creation of a rogue CA certificate, Advances in Cryptology, CRYPTO 2009, LNCS 5677, Springer, 2009"
    locator: the rogue certification authority certificate, first shown in December 2008
  - paper: "Marc Stevens, Counter-cryptanalysis, Advances in Cryptology, CRYPTO 2013, LNCS 8042, Springer, 2013"
    locator: the detection of the chosen-prefix collision in the Flame malware certificate and its new variant of the attack
  - paper: "Yu Sasaki and Kazumaro Aoki, Finding preimages in full MD5 faster than exhaustive search, Advances in Cryptology, EUROCRYPT 2009, LNCS 5479, Springer, 2009"
    locator: a preimage attack on the full MD5 with complexity 2^123.4
  - paper: doi:10.17487/RFC6151
    title: S. Turner and L. Chen, RFC 6151, Updated Security Considerations for the MD5 Message-Digest and the HMAC-MD5 Algorithms, March 2011
    locator: Section 2 (security considerations for MD5 and for HMAC-MD5)
  - url: "https://www.mscs.dal.ca/~selinger/md5collision/"
    title: Peter Selinger, MD5 collision demo, 2006
    locator: the two 128-byte colliding messages of Wang et al. in hexadecimal, used in the tests
---

MD5 is a [cryptographic hash function](/cryptographic-hash-function/) that Ronald Rivest designed in 1991 to replace [MD4](/md4/). It maps a message of any length to a 128-bit digest. Like MD4, it is a [Merkle-Damgard](/merkle-damgard-construction/) hash over a compression function on four 32-bit registers, but with four rounds of 16 steps and a distinct constant in each step. MD5 was the most used hash of the 1990s. It is broken for [collision resistance](/collision-resistance/): Wang and Yu published collisions in 2005, and [chosen-prefix collisions](/chosen-prefix-collision/) (Stevens, Lenstra and de Weger 2007) were used to forge a certificate authority in 2008 and a Microsoft code-signing chain in the Flame malware in 2012. Preimages are still hard in practice: the best attack costs about $2^{123.4}$ (Sasaki and Aoki 2009).

**Notation.** Words have 32 bits. $+$ is addition modulo $2^{32}$, $\lll s$ is left rotation by $s$, and $\wedge$, $\vee$, $\oplus$, $\neg$ are the bitwise operations. $X[0 \ldots 15]$ are the little-endian words of a 512-bit block and $(A, B, C, D)$ is the chaining value. $n$ is the message length in bytes.

## In plain words

MD5 works like MD4. It pads the message to whole blocks of 64 bytes, with the message length at the end. It keeps four 32-bit numbers as its state, and it starts from four fixed numbers. Each block goes through 64 steps. A step takes one of the four numbers, adds a mix of the other three, one word of the block and a fixed constant, rotates the result, and adds the next number. Each of the 64 steps has its own constant and its own rotation. After the 64 steps, the old state is added back in. The final state is the digest. The design is fast and simple, but researchers found ways to build two different messages with the same digest.

## The problem

The input is a message $M$ of $8n$ bits. The output is a 128-bit digest. The design aimed at collision resistance at $2^{64}$ and [preimage resistance](/preimage-resistance/) at $2^{128}$. Collisions now take seconds on a laptop, so the first goal fails completely.

## The algorithm

The round functions are $F(x, y, z) = (x \wedge y) \vee (\neg x \wedge z)$, $G(x, y, z) = (x \wedge z) \vee (y \wedge \neg z)$, $H(x, y, z) = x \oplus y \oplus z$ and $I(x, y, z) = y \oplus (x \vee \neg z)$. Step $i$ ($0 \le i < 64$) uses the function of round $r = \lfloor i/16 \rfloor$, the constant $T[i] = \lfloor 2^{32} |\sin(i + 1)| \rfloor$ with the angle in radians, the shift $s_r[i \bmod 4]$ and the word $X[k_i]$, where $k_i = i$ in round 0, $(5i + 1) \bmod 16$ in round 1, $(3i + 5) \bmod 16$ in round 2 and $7i \bmod 16$ in round 3. The shifts are $s_0 = (7, 12, 17, 22)$, $s_1 = (5, 9, 14, 20)$, $s_2 = (4, 11, 16, 23)$ and $s_3 = (6, 10, 15, 21)$. The IV is the one of MD4.

```pseudo id=main
MD5(M)
L1  P ← M ‖ 1 ‖ 0^k ‖ [8n]_64            ▷ as MD4: |P| ≡ 0 mod 512, length little-endian
L2  (A, B, C, D) ← IV                     ▷ 67452301, EFCDAB89, 98BADCFE, 10325476
L3  for each 512-bit block Y of P, in order, do
L4      (A, B, C, D) ← COMPRESS((A, B, C, D), Y)
L12 return A ‖ B ‖ C ‖ D                  ▷ each word in little-endian byte order

COMPRESS((A, B, C, D), Y)
L5  X[0..15] ← the 16 little-endian words of Y
L6  (a, b, c, d) ← (A, B, C, D)
L7  for i ← 0 to 63 do
L8      t ← a + Φ_r(b, c, d) + X[k_i] + T[i]       ▷ r = ⌊i/16⌋, Φ_0..Φ_3 = F, G, H, I
L9      a ← b + (t ⋘ s_r[i mod 4])
L10     (a, b, c, d) ← (d, a, b, c)
L11 return (A + a, B + b, C + c, D + d)
```

Compared with MD4, line L9 adds $b$ after the rotation, so a change spreads to the next register at once. $G$ is no longer the majority function, and each step has its own constant $T[i]$. Rivest made these changes to resist the attacks of den Boer and Bosselaers on MD4.

## Example

Hash `abc`. The padded block is the one of MD4: $X[0] = \texttt{80636261}$, $X[14] = \texttt{00000018}$, and the other words are 0.

Step 0 uses $F$, $X[0]$, $T[0] = \texttt{D76AA478}$ and the shift 7. $F(B, C, D) = \texttt{98BADCFE}$, so $t = \texttt{67452301} + \texttt{98BADCFE} + \texttt{80636261} + \texttt{D76AA478} = \texttt{57CE06D8}$. The rotation gives $\texttt{E7036C2B}$, and adding $B = \texttt{EFCDAB89}$ gives the new $A = \texttt{D6D117B4}$. Step 16 is the first step of round 1; it reads $X[1]$, and step 17 reads $X[6]$. The registers after each round are:

| after | $A$ | $B$ | $C$ | $D$ |
|---|---|---|---|---|
| start (IV) | `67452301` | `EFCDAB89` | `98BADCFE` | `10325476` |
| round 0 | `DDA9B9A6` | `72AFF2E0` | `E396856B` | `A1051895` |
| round 1 | `790A77FB` | `726342D3` | `A62884AA` | `9F47E4F8` |
| round 2 | `7F2E507B` | `7BEB9700` | `8FAE6399` | `99D9679D` |
| round 3 | `310ADE8F` | `C08226B3` | `E484B9D8` | `624D8CB2` |
| feed-forward | `98500190` | `B04FD23C` | `7D3F96D6` | `727FE128` |

In little-endian bytes the digest is `900150983cd24fb0d6963f7d28e17f72`, the value for "abc" in RFC 1321, Appendix A.5. A script computed each entry with the code of this page.

**A collision.** The tests also hash the two 128-byte messages of Wang and Yu, as published by Selinger. They differ in 6 bytes (positions 19, 45, 59, 83, 109 and 123, counted from 0), and both have the MD5 digest `79054025255fb1a26e4bc422aef54eb4`. After the first block, the chaining values differ only in the top bits of each word (XOR differences `80000000`, `82000000`, `86000000`, `82000000`). After the second block they are equal, so any common suffix keeps the collision. The tests check the collision with the code of this page and with `hashlib.md5`.

## Correctness

The padding is the injective MD-strengthening padding of MD4, the loop of lines L3 and L4 computes the Merkle-Damgard iteration, and each step of lines L8 to L10 is a bijection of the state for a fixed block: from the new $a$ and the old $b$, line L9 can be undone by a subtraction and a right rotation, and line L8 by a subtraction. So COMPRESS is $E_Y(H) + H$ for a permutation $E_Y$, the [Davies-Meyer](/davies-meyer-construction/) form. The full proof is below. The test vectors of RFC 1321 check that the code computes the standard function.

## Complexity

COMPRESS does 64 steps. Each step does 4 additions, one rotation and a round function of 2 or 3 bitwise operations. A message of $n$ bytes has $\lfloor (n + 8)/64 \rfloor + 1$ blocks, so the time is $\Theta(n)$ and the extra space $\Theta(1)$. The 64 steps form one long chain of dependent operations, so MD5 cannot use the parallel units of a modern processor well. Speed is not a good reason to keep MD5: [BLAKE3](/blake3/), and SHA-256 on processors with SHA instructions, are about as fast or faster.

## Properties

- 128-bit digest, 512-bit block, little-endian words.
- [Length extension](/length-extension-attack/): from $\text{MD5}(M)$ and $|M|$ anyone can compute $\text{MD5}(M \| \text{pad} \| S)$ for any $S$.
- Collisions: practical since 2005. Identical-prefix collisions take seconds; chosen-prefix collisions are within reach of a small cluster.
- Preimages: the best attack costs about $2^{123.4}$ (Sasaki and Aoki 2009), so MD5 is not inverted in practice. Second preimages of a given random message are not practical either.
- HMAC-MD5 does not rest on collision resistance. RFC 6151 says it is not urgent to remove it from old protocols, but new protocols should not use it.

## Variants and improvements

- [SHA-1](/sha-1/) (1995) took the MD4 structure with a message expansion and 160-bit output. It is broken too.
- [SHA-2](/sha-2/) and [SHA-3](/sha-3/) are the current standards.
- [RIPEMD-160](/ripemd-160/) is a European design of the same family with two parallel lines.
- Collision detection (Stevens 2013) checks whether a message was made by a known MD5 or SHA-1 collision attack. It is a stopgap, not a fix.

## When to use it

Do not use MD5 where an attacker can choose or influence the input: not for signatures, certificates, commit hashes or file identities in a hostile setting. It is still used as a fast [checksum](/checksum/) against accidental corruption and as a non-security key, but a [CRC](/cyclic-redundancy-check/) or a non-cryptographic hash is enough there. For new security work, use SHA-256, SHA-512/256 or SHA3-256.

## Pitfalls

- "Nobody can make a file with my MD5" is a preimage claim, and it holds today. "Nobody can make two files with the same MD5" is a collision claim, and it is false. Systems that sign or whitelist a hash fall to collisions: the attacker prepares a harmless and a harmful file with one digest, gets the harmless one approved, and swaps.
- A collision with a common suffix stays a collision. This is why PDF, PostScript and executable formats that branch on a block of bytes can show two different contents.
- The constants come from $|\sin(i + 1)|$ for $i = 0, \ldots, 63$, not $\sin(i)$. Check $T[0] = \texttt{D76AA478}$ and $T[63] = \texttt{EB86D391}$.
- The code on this page is for study only. It is not constant time, and it must not protect real data. Use `hashlib.sha256` or the SHA-2 or SHA-3 functions of OpenSSL or libsodium.

## Implementations

## History

Rivest designed MD5 in 1991, after attacks on reduced versions of MD4, and published it as RFC 1321 in 1992. Den Boer and Bosselaers found pseudo-collisions of the compression function in 1993 (two different chaining values, one block). Dobbertin found a collision of the compression function with a chosen IV in 1996, and experts then advised against MD5 for new designs. In 2004, Wang, Feng, Lai and Yu announced collisions of MD5, and Wang and Yu published the method at EUROCRYPT 2005. Klima's tunnels (2006) cut the time to under a minute on a notebook. Stevens, Lenstra and de Weger gave chosen-prefix collisions in 2007. In December 2008, Stevens, Sotirov, Appelbaum, Lenstra, Molnar, Osvik and de Weger used a chosen-prefix collision, computed on about 200 PlayStation 3 consoles, to get a rogue CA certificate that browsers trusted. The Flame malware, found in 2012, used another chosen-prefix collision to fake a Microsoft signature (Stevens 2013). RFC 6151 (2011) updated the security considerations of MD5.

## References
