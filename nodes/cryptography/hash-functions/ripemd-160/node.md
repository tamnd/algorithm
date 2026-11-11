---
tag: QEE7BH
kind: algorithm
slug: ripemd-160
name: RIPEMD-160
aliases:
- HASH160
area: cryptography/hash-functions
level: advanced
summary: A 160-bit Merkle-Damgard hash from 1996 whose compression function runs two different MD4-like lines of 5 rounds in parallel and adds them together. Bitcoin uses it in HASH160.
model: word-ram
complexity:
  vars: {n: the message length in bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1996
  people: [Hans Dobbertin, Antoon Bosselaers, Bart Preneel]
  note: Designed as a strengthened RIPEMD after Dobbertin's attacks on reduced RIPEMD in 1995, published at FSE 1996, and later standardized in ISO/IEC 10118-3.
prereqs: [merkle-damgard-construction, md4]
see_also: [md5, sha-1, sha-2, compression-function, collision-resistance, length-extension-attack, hmac, digital-signature]
sources:
  - paper: "Hans Dobbertin, Antoon Bosselaers and Bart Preneel, RIPEMD-160, a strengthened version of RIPEMD, Fast Software Encryption, FSE 1996, LNCS 1039, Springer, 1996"
    locator: the design of the two parallel lines, the Boolean functions, the word orders, the rotations, the constants and the combination of the lines
  - url: "https://homes.esat.kuleuven.be/~bosselae/ripemd160.html"
    title: Antoon Bosselaers, The hash function RIPEMD-160
    locator: the section on test vectors, and the corrected specification (rmd160.txt) with the pseudocode and the tables
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 9.4.2 (iv), Algorithm 9.55, Table 9.6 (test vector), Tables 9.8 and 9.9 (round functions, word orders and rotations) and the chapter notes in Section 9.8 on RIPEMD
  - paper: "ISO/IEC 10118-3, Information technology, Security techniques, Hash-functions, Part 3, Dedicated hash-functions"
    locator: the dedicated hash function RIPEMD-160
  - url: "https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki"
    title: Pieter Wuille and Greg Maxwell, BIP 173, Base32 address format for native v0-16 witness outputs
    locator: the section Examples, the P2WPKH witness program of the generator public key, which is its HASH160
---

RIPEMD-160 is a hash function with a 160-bit digest, designed in 1996 by Hans Dobbertin, Antoon Bosselaers and Bart Preneel as a strengthened version of the 128-bit RIPEMD of 1992. It uses the [Merkle-Damgard construction](/merkle-damgard-construction/) with the padding of [MD4](/md4/), 512-bit blocks and little-endian words. Its compression function is unusual: it runs two lines of 80 steps on the same block in parallel, each with its own word order, rotations, constants and order of the five Boolean functions, and then adds the two results and the chaining value together. An attacker must control both lines at once. No collision of the full function is known, but 160 bits give only 80-bit generic collision resistance. Its main use today is HASH160 in Bitcoin, which is RIPEMD-160 of SHA-256.

**Notation.** Words are 32 bits, and $+$ is addition modulo $2^{32}$. $x \lll s$ rotates $x$ left by $s$ bits. $\oplus$, $\wedge$, $\vee$ and $\neg$ act bit by bit. $X[0..15]$ are the 16 words of a block, read little-endian. The chaining value $H = (h_0, \ldots, h_4)$ starts at $IV = (\texttt{67452301}, \texttt{EFCDAB89}, \texttt{98BADCFE}, \texttt{10325476}, \texttt{C3D2E1F0})$, the IV of [SHA-1](/sha-1/). $n$ is the message length in bytes.

## In plain words

Take MD4, give it a fifth register, and make it longer: 5 rounds of 16 steps instead of 3. Now build two different copies of it. The left copy reads the message words in one order, the right copy in another. They use different rotation amounts and different constants, and they use the five Boolean functions in opposite orders. Run both copies on the same block, starting from the same chaining value. At the end, mix the two results and the old chaining value together by adding them, with a shift of positions. A collision attack must make the differences cancel in two very different computations at the same time, which is much harder than in one.

## The problem

The input is a message $M$ of $n$ bytes, with $8n < 2^{64}$. The output is a 160-bit digest. It should be collision resistant up to about $2^{80}$ work, the birthday bound, and preimage resistant up to about $2^{160}$. The design goal in 1996 was a drop-in replacement for MD4, MD5 and RIPEMD with a larger digest and a large margin against the attacks of Dobbertin on MD4 and reduced RIPEMD.

## The algorithm

The five Boolean functions are, for $j = 0, \ldots, 79$ and round $\lfloor j/16 \rfloor$:

| Round | $f_j(x, y, z)$ | $K_j$ (left) | $K'_j$ (right) |
|---|---|---|---|
| 0 | $x \oplus y \oplus z$ | $\texttt{00000000}$ | $\texttt{50A28BE6} = \lfloor 2^{30} \sqrt[3]{2} \rfloor$ |
| 1 | $(x \wedge y) \vee (\neg x \wedge z)$ | $\texttt{5A827999} = \lfloor 2^{30} \sqrt{2} \rfloor$ | $\texttt{5C4DD124} = \lfloor 2^{30} \sqrt[3]{3} \rfloor$ |
| 2 | $(x \vee \neg y) \oplus z$ | $\texttt{6ED9EBA1} = \lfloor 2^{30} \sqrt{3} \rfloor$ | $\texttt{6D703EF3} = \lfloor 2^{30} \sqrt[3]{5} \rfloor$ |
| 3 | $(x \wedge z) \vee (y \wedge \neg z)$ | $\texttt{8F1BBCDC} = \lfloor 2^{30} \sqrt{5} \rfloor$ | $\texttt{7A6D76E9} = \lfloor 2^{30} \sqrt[3]{7} \rfloor$ |
| 4 | $x \oplus (y \vee \neg z)$ | $\texttt{A953FD4E} = \lfloor 2^{30} \sqrt{7} \rfloor$ | $\texttt{00000000}$ |

The left line uses $f_j$ in step $j$, and the right line uses $f_{79 - j}$, so the functions come in the opposite order. The word orders come from two permutations of $\{0, \ldots, 15\}$: $\rho = (7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8)$ and $\pi(i) = 9i + 5 \bmod 16$. In round $k$, step $i$ of the left line reads $X[\rho^k(i)]$ and step $i$ of the right line reads $X[\rho^k(\pi(i))]$. The rotation amounts $s_j$ and $s'_j$ are in Bosselaers' tables and in HAC Table 9.9.

```pseudo id=main
RIPEMD-160(M)
L1  P ← M ‖ 80 ‖ 00…00 ‖ [8n]₆₄            ▷ MD4 padding, length little-endian; 64 divides |P|
L2  H ← IV
L3  for each 64-byte block Y of P, in order, do
L4      H ← COMPRESS(H, Y)
L12 return h₀ ‖ h₁ ‖ h₂ ‖ h₃ ‖ h₄            ▷ each word in little-endian byte order

COMPRESS(H, Y)
L5  X[0..15] ← the 16 little-endian words of Y
L6  (A, B, C, D, E) ← H;  (A', B', C', D', E') ← H     ▷ the left line and the right line
L7  for j ← 0 to 79 do
L8      T ← ((A + f_j(B, C, D) + X[r_j] + K_j) ⋘ s_j) + E
L9      T' ← ((A' + f_{79−j}(B', C', D') + X[r'_j] + K'_j) ⋘ s'_j) + E'
L10     (A, B, C, D, E) ← (E, T, B, C ⋘ 10, D);  the same for the right line with T'
L11 return (h₁ + C + D', h₂ + D + E', h₃ + E + A', h₄ + A + B', h₀ + B + C')
```

Each step is an MD4 step with a fifth register: the new $B$ is the sum rotated, plus $E$, and $C$ is rotated by 10 as it moves to $D$. The code runs the left line and then the right line, which gives the same result, since the two lines do not share registers.

## Example

**RIPEMD-160("abc").** The padded message is one block: $\texttt{61 62 63 80}$, 52 zero bytes, then the bit length 24 as 8 bytes little-endian. So $X[0] = \texttt{80636261}$, $X[14] = \texttt{00000018}$ and the other words are 0. The first step of the left line uses $f_0 = B \oplus C \oplus D$, $X[0]$, $K_0 = 0$ and $s_0 = 11$:

$$T = ((\texttt{67452301} + (\texttt{EFCDAB89} \oplus \texttt{98BADCFE} \oplus \texttt{10325476}) + \texttt{80636261}) \lll 11) + \texttt{C3D2E1F0} = \texttt{3115FC67}.$$

After 80 steps the two lines hold these registers:

| Line | $A$ | $B$ | $C$ | $D$ | $E$ |
|---|---|---|---|---|---|
| left | $\texttt{641129CA}$ | $\texttt{D563BFDC}$ | $\texttt{0B2CDC01}$ | $\texttt{6E413468}$ | $\texttt{FC433DA8}$ |
| right | $\texttt{81D4727D}$ | $\texttt{5FCCBADE}$ | $\texttt{BF627814}$ | $\texttt{FC0E2B04}$ | $\texttt{739C4C7A}$ |

Line L11 gives, for example, $h_0' = h_1 + C + D' = \texttt{EFCDAB89} + \texttt{0B2CDC01} + \texttt{FC0E2B04} = \texttt{F708B28E}$, and the new chaining value is $(\texttt{F708B28E}, \texttt{7A985DE0}, \texttt{8E4A049B}, \texttt{87B0C698}, \texttt{FC0B5AF1})$. Written little-endian, this is the digest $\texttt{8eb208f7e05d987a9b044a8e98c6b087f15a0bfc}$.

**The Bosselaers vectors.** The tests check all eight short vectors from Bosselaers' page, among them:

| Message | RIPEMD-160 |
|---|---|
| "" | `9c1185a5c5e9fc54612808977ee8f548b2258d31` |
| "a" | `0bdc9d2d256b3ee9daae347be6f4dc835a467ffe` |
| "abc" | `8eb208f7e05d987a9b044a8e98c6b087f15a0bfc` |
| "message digest" | `5d0689ef49d2fae572b881b123a85ffa21595f36` |
| "abcdefghijklmnopqrstuvwxyz" | `f71c27109c692c1b56bbdceb5b9d2865b3708dbc` |
| 8 times "1234567890" | `9b752e45573d4b39f4dbd3323cab82bf63326bfb` |

**Bitcoin HASH160.** For the compressed public key $\texttt{0279BE66}\ldots\texttt{16F81798}$ of the secp256k1 generator, SHA-256 gives $\texttt{0f715baf}\ldots\texttt{4b9b0554}$, and RIPEMD-160 of that gives $\texttt{751e76e8199196d454941c45d1b3a323f1433bd6}$, the witness program in the examples of BIP 173. The tests check it.

## Correctness

The padding is injective and gives whole blocks, as for MD4, and the loop of lines L3 and L4 is the Merkle-Damgard iteration, so the [Merkle-Damgard theorem](/merkle-damgard-theorem/) reduces collisions of RIPEMD-160 to collisions of COMPRESS. Each step of each line is a bijection of the five registers for a fixed block, so each line computes a permutation of the chaining value. The final combination is not a feed-forward of one permutation, unlike the [Davies-Meyer](/davies-meyer-construction/) form of MD4, MD5 and SHA-1: each output word mixes one word of $H$ and one word of each line. The proof file gives the details. That the code is the standard function is checked by the Bosselaers vectors and by `hashlib`, where OpenSSL provides RIPEMD-160.

## Complexity

Each block takes $2 \times 80 = 160$ steps of a fixed number of word operations, so $\Theta(1)$ per block. A message of $n$ bytes has $\lfloor (n + 8)/64 \rfloor + 1$ blocks, so the time is $\Theta(n)$ and the extra space is 10 registers and 16 words, $\Theta(1)$. RIPEMD-160 does about twice the work of SHA-1 per block and is slower than SHA-256 on processors with SHA instructions. The two lines are independent, so they can run in parallel on two execution units or in SIMD lanes.

## Properties

- **Generic security.** A 160-bit digest gives at most 80 bits against collisions, below the 112 bits that current guidance asks for, and 160 bits against preimages.
- **Cryptanalysis.** No collision or preimage of the full 80-step function is known. Published attacks reach reduced versions with fewer steps, and semi-free-start collisions, where the attacker picks the chaining value, reach further.
- **Length extension.** Like every plain Merkle-Damgard hash, RIPEMD-160 allows [length extension](/length-extension-attack/): $H(M)$ and $|M|$ give $H(M \| \mathrm{pad} \| S)$. Use [HMAC](/hmac/) for a MAC.
- **Standards.** ISO/IEC 10118-3 includes RIPEMD-160. NIST does not approve it, so FIPS-validated modules do not offer it, and OpenSSL 3.0 at first offered it only in its legacy provider.

## Variants and improvements

- **RIPEMD** (1992), the original from the RIPE project of the European RACE program: 128 bits and two lines of 3 rounds. Dobbertin attacked two-round versions in 1995, and Wang and others found collisions for the full function in 2004.
- **RIPEMD-128** (1996): the same design with 4 rounds and 128 bits, as a drop-in replacement for RIPEMD.
- **RIPEMD-256 and RIPEMD-320**: double-length variants that keep the two lines separate and swap one register between them after each round. They give a longer digest but not more security than RIPEMD-128 and RIPEMD-160.
- **HASH160** in Bitcoin: $\mathrm{RIPEMD160}(\mathrm{SHA256}(x))$, used for P2PKH and P2WPKH addresses and for P2SH script hashes.

## When to use it

Use RIPEMD-160 only where a format requires it: Bitcoin and other cryptocurrency addresses, older OpenPGP keys and some old signature formats. For a new design, use [SHA-2](/sha-2/), [SHA-3](/sha-3/) or [BLAKE2](/blake2/), which have longer digests and more analysis. In Bitcoin, HASH160 is safe in practice for addresses of one key, because finding a second key with a given hash is a preimage problem; for multisignature addresses the 80-bit collision bound matters, which is one reason for 256-bit P2WSH and P2TR outputs.

## Pitfalls

- **Missing from hashlib.** `hashlib.new("ripemd160")` fails on systems where OpenSSL 3 has no legacy provider. Do not rely on it being present; the tests on this page skip the comparison in that case.
- **Byte order.** Words are little-endian as in MD4 and MD5, not big-endian as in SHA-1, although the IV is the same as SHA-1's.
- **HASH160 order.** Bitcoin's HASH160 is RIPEMD-160 of the SHA-256 digest, not SHA-256 of RIPEMD-160, and it hashes the raw 33-byte or 65-byte key, not its hex string.
- **80 bits.** A collision of a 160-bit hash costs about $2^{80}$ evaluations, within reach of a large organization. Do not use RIPEMD-160 where an attacker who can choose both inputs gains from a collision.
- **For study only.** The code on this page is slow and not constant time. Use a vetted library.

## Implementations

## History

RIPEMD was designed in 1992 by Bert den Boer and others in the RIPE project (RACE Integrity Primitives Evaluation) of the European Union, as a strengthened MD4 with two parallel lines of three rounds. In 1995 Hans Dobbertin found collisions for RIPEMD with the first or the last round left out, and he also attacked MD4 and the compression function of MD5. With the 128-bit digest also seen as too short, Dobbertin, Bosselaers and Preneel designed RIPEMD-160 and RIPEMD-128 and published them at FSE 1996. RIPEMD-160 entered ISO/IEC 10118-3. Bitcoin, released in 2009, uses RIPEMD-160 of SHA-256 for its addresses, which made RIPEMD-160 one of the most widely computed hash functions.

## References
