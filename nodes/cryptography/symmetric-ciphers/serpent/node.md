---
tag: 9ATZRG
kind: algorithm
slug: serpent
name: Serpent
area: cryptography/symmetric-ciphers
level: advanced
summary: A 32-round substitution-permutation network on 128-bit blocks with keys up to 256 bits, built for bitslice software. An AES finalist, second to Rijndael in the informal vote of April 2000.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {b: the number of 16-byte blocks}
  time: {worst: Θ(b), average: Θ(b), best: Θ(b)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1998
  people: [Ross Anderson, Eli Biham, Lars Knudsen]
  note: A first version with the DES S-boxes appeared at FSE 1998. The AES submission of June 1998 has new S-boxes, and Serpent became an AES finalist in 1999.
prereqs: [substitution-permutation-network, s-box, block-cipher]
see_also: [advanced-encryption-standard, twofish, rc6, differential-cryptanalysis, linear-cryptanalysis, boomerang-attack, key-schedule]
sources:
  - url: "https://www.cl.cam.ac.uk/~rja14/Papers/serpent.pdf"
    title: Ross Anderson, Eli Biham and Lars Knudsen, Serpent, a proposal for the Advanced Encryption Standard, AES submission, 1998
    locator: Section 2 (the cipher and its bit order), Section 3 (the bitslice implementation and the linear transformation), Section 4 (the key schedule), Section 5 (security) and Appendix A.5 (the S-boxes)
  - paper: doi:10.1007/3-540-69710-1_15
    title: Eli Biham, Ross Anderson and Lars Knudsen, Serpent, a new block cipher proposal, Fast Software Encryption 1998, LNCS 1372, Springer, 1998
    locator: pp. 222-238, the first version (Serpent-0) with the DES S-boxes
  - url: "https://www.cs.technion.ac.il/~biham/Reports/Serpent/"
    title: NESSIE test vectors for Serpent, files Serpent-128-128, Serpent-192-128 and Serpent-256-128 verified test vectors
    locator: sets 1 to 4
  - url: "https://www.cl.cam.ac.uk/~rja14/serpent.html"
    title: Ross Anderson, the Serpent home page
    locator: the vote at the last AES conference (Rijndael 86, Serpent 59, Twofish 31, RC6 23, MARS 13)
  - paper: doi:10.1007/3-540-44987-6_21
    title: Eli Biham, Orr Dunkelman and Nathan Keller, The rectangle attack, rectangling the Serpent, EUROCRYPT 2001, LNCS 2045, Springer, 2001
    locator: pp. 340-357, the attack on 10-round Serpent
---

Serpent is a [block cipher](/block-cipher/) on 128-bit blocks with a key of up to 256 bits, built as a 32-round [substitution-permutation network](/substitution-permutation-network/). Anderson, Biham and Knudsen designed it for the AES competition, with a large safety margin and an implementation as 32 parallel copies of a 4-bit [S-box](/s-box/) computed with word-wide Boolean operations (the bitslice form). Serpent was an AES finalist and came second in the informal vote of April 2000; NIST chose Rijndael as [AES](/advanced-encryption-standard/). No attack on more than a small part of its 32 rounds is known.

**Notation.** A block is four 32-bit words $X_0, X_1, X_2, X_3$. As in the paper, all values are little-endian: $X_0$ is the least significant word, and bit 0 is the least significant bit of $X_0$. ROL is a left rotation of a 32-bit word, $\ll$ a left shift with zero fill, $\oplus$ XOR. $\hat K_0, \ldots, \hat K_{32}$ are the 33 round keys of 128 bits. $S_0, \ldots, S_7$ are the eight S-boxes, each a permutation of $\{0, \ldots, 15\}$, and $\varphi$ = 9E3779B9 is the fractional part of the golden ratio.

## In plain words

Serpent stacks the block as four words of 32 bits, one above the other. Each column then holds 4 bits, and there are 32 columns. In each round, Serpent first mixes in a round key. Then it replaces each 4-bit column with another 4-bit value from a small table. Because all 32 columns use the same table in the same round, a program can do this with a few AND, OR and XOR operations on the whole words at once. Then a fixed mix of rotations, shifts and XORs spreads each bit over many columns.

There are 32 rounds and eight tables, and each table is used in four rounds. The designers used about twice as many rounds as they thought necessary, to stay safe against attacks found later.

## The problem

Serpent computes a permutation $E_K$ of $\{0,1\}^{128}$ for each key $K$, and its inverse $D_K$. The AES submission fixes keys of 128, 192 or 256 bits, but any key of up to 256 bits works: a short key is padded to 256 bits with one "1" bit just above its most significant bit, then zeros. The security goal is that $E_K$ is a [pseudorandom permutation](/pseudorandom-permutation/). There is no proof; the designers bound the probability of differential and linear characteristics and leave a large margin.

## The algorithm

This is the bitslice description of Section 3 of the paper. The standard description adds an initial permutation IP before the rounds and its inverse FP after them, and applies the S-boxes to 4-bit groups of consecutive bits; the two descriptions compute the same function.

```pseudo id=main
SERPENT-ENCRYPT(K, x)
L1  K̂0, ..., K̂32 ← KEY-SCHEDULE(K)
L2  X ← x, as four 32-bit words X0, X1, X2, X3
L3  for i ← 0 to 31 do
L4      X ← X ⊕ K̂i
L5      X ← S(i mod 8)(X)                    ▷ one 4-bit S-box on each of the 32 bit columns
L6      if i < 31 then X ← LT(X)
L7      else X ← X ⊕ K̂32
L8  return X

LT(X0, X1, X2, X3)                           ▷ the linear transformation
L9  X0 ← ROL(X0, 13), X2 ← ROL(X2, 3)
L10 X1 ← X1 ⊕ X0 ⊕ X2, X3 ← X3 ⊕ X2 ⊕ (X0 ≪ 3)
L11 X1 ← ROL(X1, 1), X3 ← ROL(X3, 7)
L12 X0 ← X0 ⊕ X1 ⊕ X3, X2 ← X2 ⊕ X3 ⊕ (X1 ≪ 7)
L13 X0 ← ROL(X0, 5), X2 ← ROL(X2, 22)
L14 return (X0, X1, X2, X3)

KEY-SCHEDULE(K)
L15 pad K to 256 bits: a 1 bit just above its top bit, then zeros
L16 w(−8), ..., w(−1) ← the eight words of the padded key
L17 for i ← 0 to 131 do w(i) ← ROL(w(i−8) ⊕ w(i−5) ⊕ w(i−3) ⊕ w(i−1) ⊕ φ ⊕ i, 11)
L18 return K̂j ← S((3 − j) mod 8)(w(4j), w(4j+1), w(4j+2), w(4j+3)) for j = 0, ..., 32
```

In line L5, column $j$ is the 4-bit number whose bit $t$ is bit $j$ of $X_t$; the S-box output is written back to the same column. So round $i$ uses $S_{i \bmod 8}$, and the key schedule uses $S_3, S_2, S_1, S_0, S_7, \ldots$ for $\hat K_0, \hat K_1, \ldots$. Decryption runs the rounds backward with the inverse S-boxes and the inverse of LT, which applies the inverse of each line of L9 to L13 in reverse order.

The Python code for this page is for study only. It is not constant time as written (Python itself is not), although the bitslice form of Serpent has no table lookups and can be made constant time in C. Do not use it to protect real data. Use AES-GCM or ChaCha20-Poly1305 from a FIPS 140 validated module, or libsodium, instead.

## Example

Take set 3, vector 0 of the NESSIE file for 128-bit keys: the key and the plaintext are all zero. The padded key has a 1 in bit 128. The first round key is $\hat K_0$ = (6F579DD2, A7A3A3CE, F29990ED, 8ED77392) as $(X_0, X_1, X_2, X_3)$.

| step | $X_0$ | $X_1$ | $X_2$ | $X_3$ |
|---|---|---|---|---|
| round 1, after $S_0$ | A9E4805C | 742AC163 | 4A65629C | BAEDCCF1 |
| round 1, after LT | 64FDBE66 | 6E14817B | 35A514D4 | CD38F9B4 |
| round 2, after LT | DB826FD2 | 0C37720E | FA214410 | BABA82C9 |
| round 32, after $S_7$ | 270B29FE | D7A641F3 | F03808D0 | A34C4E76 |
| after $\oplus \hat K_{32}$ | 7AB12036 | D093A9E6 | 76B81896 | E9BA6682 |

NESSIE writes a block as its 16 bytes in memory order, least significant byte first. So the output words give the bytes 36 20 B1 7A, E6 A9 93 D0, 96 18 B8 76, 82 66 BA E9, that is the ciphertext 3620B17AE6A993D09618B8768266BAE9 of the file. The paper writes the same block as one 128-bit hex number, most significant digit first, so in the paper's notation the hex string is reversed byte by byte. The test file checks eleven NESSIE vectors with keys of 128, 192 and 256 bits, for example key 000102030405060708090A0B0C0D0E0F and plaintext 00112233445566778899AABBCCDDEEFF give 563E2CF8740A27C164804560391E9B27, and the "iterated 100 times" value of set 4.

## Correctness

SERPENT-DECRYPT inverts SERPENT-ENCRYPT for every key. Each step of a round is a bijection with a known inverse: XOR with a round key is its own inverse, each S-box is a permutation of 4-bit values and the bitslice form applies it to columns independently, and LT is a product of rotations and of XOR steps that add a function of the other words, each undone by the same XOR. The [proof](proofs/correctness.md) gives each step.

## Complexity

One block costs 32 rounds. A round costs one 128-bit key XOR, one bitsliced S-box layer and one LT. In the bitslice form, an S-box layer is a short Boolean circuit on four words, which computes all 32 S-boxes at once. LT costs 6 rotations, 2 shifts and 8 XORs. So a block costs a few hundred word operations, and $b$ blocks cost $\Theta(b)$. The key schedule makes 132 prekey words and 33 S-box layers, once for each key. The key state is 33 round keys of 128 bits.

The designers estimated that a differential or linear attack would need more than $2^{256}$ texts in the sense of characteristics averaged over keys (Section 5 of the paper). Published attacks reach only versions with far fewer rounds: for example, the rectangle attack of Biham, Dunkelman and Keller (2001) reaches 10 of the 32 rounds.

## Properties

- **Bitslice design.** The S-boxes and LT use only Boolean operations, rotations and shifts on 32-bit words. There are no table lookups, so a careful implementation is constant time.
- **Conservative margin.** 32 rounds. The designers wrote that 16-round Serpent would already be as secure as triple DES, and doubled the count because the AES might stay in use for 50 years (Section 2 of the paper).
- **Eight S-boxes, four uses each.** Round $i$ uses $S_{i \bmod 8}$. Each S-box has every differential probability at most $1/4$, every linear approximation probability in $1/2 \pm 1/4$, no one-bit input difference that gives a one-bit output difference, and output bits of degree 3 (Section 2.1 of the paper).
- **Key padding.** Any key of up to 256 bits maps to a distinct 256-bit key, so no two short keys are equivalent.
- **Slow in a single block on 32-bit software.** Serpent was slower than Rijndael in most software tests of the AES process, which counted against it.

## Variants and improvements

- **Serpent-0.** The FSE 1998 version, with the DES S-boxes. The AES submission (Serpent-1, usually just called Serpent) replaced them with stronger S-boxes and changed the key schedule slightly.
- **Cascades.** Disk encryption tools such as VeraCrypt offer Serpent alone or in a cascade with AES and [Twofish](/twofish/).

## When to use it

Serpent is unbroken and has a large security margin, but AES has hardware support and is the standard. Use Serpent when a format requires it, or when an extra margin matters more than speed and you can use a vetted implementation, for example from Botan, libgcrypt or the Linux kernel crypto API.

## Pitfalls

- **Bit and byte order.** The paper prints blocks as big hex numbers, but most test vector files, including NESSIE, list bytes in memory order. A wrong guess here is the most common cause of failed test vectors.
- **Key padding.** The 1 bit goes just above the most significant bit of the short key, not at bit 0 and not at the end of the byte string in big-endian order.
- **Key schedule S-box order.** $\hat K_j$ uses $S_{(3 - j) \bmod 8}$, which runs backwards, while round $i$ uses $S_{i \bmod 8}$.
- **The last round.** Round 31 replaces LT with a second key XOR with $\hat K_{32}$.
- **IP and FP.** Code that mixes the standard and bitslice descriptions must apply IP and FP exactly once, or not at all.

## Implementations

## History

Biham, Anderson and Knudsen presented a first version at Fast Software Encryption in March 1998, built on the DES S-boxes. For the AES submission in June 1998 they chose new S-boxes and changed the key schedule. NIST named Serpent one of the five finalists in August 1999. At the third AES conference in April 2000, an informal vote gave positive votes to Rijndael 86, Serpent 59, Twofish 31, RC6 23 and MARS 13, as reported on the Serpent home page. NIST announced Rijndael as the AES in October 2000. Serpent remains in many libraries and disk encryption tools.

## References
