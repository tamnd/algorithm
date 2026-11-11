---
tag: 6RCPBE
kind: algorithm
slug: tiger-hash
name: Tiger
aliases:
- Tiger hash
- Tiger2
area: cryptography/hash-functions
level: advanced
summary: A 192-bit Merkle-Damgard hash by Anderson and Biham (1996) for 64-bit machines, with three 64-bit registers, four 8-to-64-bit S-boxes and 24 rounds. Tiger2 changes only the pad byte.
model: word-ram
complexity:
  vars: {n: the message length in bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1996
  people: [Ross Anderson, Eli Biham]
  note: Presented at Fast Software Encryption 1996 in Cambridge as a fast hash for the new 64-bit processors; Tiger2, with the MD4 pad byte, came later from the same designers.
prereqs: [merkle-damgard-construction, s-box]
see_also: [md4, sha-1, sha-2, ripemd-160, compression-function, merkle-tree, collision-resistance, length-extension-attack]
sources:
  - paper: "Ross Anderson and Eli Biham, Tiger, a fast new hash function, Fast Software Encryption, FSE 1996, LNCS 1039, Springer, 1996"
    locator: the description of the compression function (the registers, the S-boxes, the round, the pass and the key schedule), the padding, the generation of the S-boxes and the design rationale
  - url: "https://www.cs.technion.ac.il/~biham/Reports/Tiger/"
    title: Ross Anderson and Eli Biham, Tiger, a fast new cryptographic hash function (designed in 1995)
    locator: the test results page (testresults.html) with the vectors used in the tests, the reference code with gen-sboxes.c, and the note on Tiger2 and its padding
  - paper: "Florian Mendel and Vincent Rijmen, Cryptanalysis of the Tiger hash function, Advances in Cryptology, ASIACRYPT 2007, LNCS 4833, Springer, 2007"
    locator: the pseudo-near-collision for the full 24-round Tiger and the attacks on reduced versions
  - paper: "John Kelsey and Stefan Lucks, Collisions and near-collisions for reduced-round Tiger, Fast Software Encryption, FSE 2006, LNCS 4047, Springer, 2006"
    locator: the collision attack on Tiger reduced to 16 rounds
  - paper: "Florian Mendel, Bart Preneel, Vincent Rijmen, Hirotaka Yoshida and Dai Watanabe, Update on Tiger, Progress in Cryptology, INDOCRYPT 2006, LNCS 4329, Springer, 2006"
    locator: the collision attack on Tiger reduced to 19 rounds
---

Tiger is a hash function with a 192-bit digest, designed by Ross Anderson and Eli Biham in 1995 and presented at FSE 1996. It was made for the 64-bit processors that were new at the time, such as the DEC Alpha: all its arithmetic is on 64-bit words. It uses the [Merkle-Damgard construction](/merkle-damgard-construction/) with 512-bit blocks and the padding layout of [MD4](/md4/). The state is three 64-bit registers $a$, $b$, $c$. The compression function has 24 rounds in three passes of eight, with a key schedule that mixes the 8 message words between passes. Each round does eight lookups in four [S-boxes](/s-box/) that map one byte to a 64-bit word. Tiger pads with the byte $\texttt{01}$ and Tiger2 with $\texttt{80}$; nothing else differs. Truncations to 160 and 128 bits are called Tiger/160 and Tiger/128.

**Notation.** Words are 64 bits and little-endian. $+$, $-$ and $\times$ are modulo $2^{64}$, $\oplus$ is XOR and $\neg$ is bitwise NOT. $c_i$ is byte $i$ of $c$, with $c_0$ the least significant. $t_1, t_2, t_3, t_4$ are the four S-boxes of 256 words each. $IV = (\texttt{0123456789ABCDEF}, \texttt{FEDCBA9876543210}, \texttt{F096A5B4C3B2E187})$. $n$ is the message length in bytes.

## In plain words

Tiger reads the message in 64-byte blocks, which it sees as eight 64-bit words. It keeps three 64-bit registers. For each block, it runs 24 rounds. In a round, one message word is XORed into a register. The eight bytes of that register are then used to look up eight words in four big tables. The four bytes at even positions give words that are subtracted from a second register. The four bytes at odd positions give words that are added to the third register, which is then multiplied by a small odd number. The registers change roles from round to round. After every eight rounds, the message words are stirred among themselves. At the end, the old registers are combined with the new ones.

## The problem

The input is a message $M$ of $n$ bytes, with $8n < 2^{64}$. The output is a 192-bit digest. It should be collision resistant up to about $2^{96}$ work and preimage resistant up to about $2^{192}$. The design goal in 1995 was a hash that is fast on 64-bit machines and still usable on 32-bit ones, with a larger digest than SHA-1 and a margin against the attacks that had broken MD4 and reduced versions of MD5.

## The algorithm

One round with registers $(a, b, c)$, message word $x$ and multiplier $\mathit{mul}$ is lines L9 to L12. A pass applies 8 rounds with the roles of the registers turning: $(a, b, c), (b, c, a), (c, a, b), (a, b, c), \ldots$ for the words $x_0, \ldots, x_7$. The three passes use $(a, b, c)$ with multiplier 5, $(c, a, b)$ with 7 and $(b, c, a)$ with 9. The key schedule between passes is

$$\begin{aligned}
x_0 &\mathrel{-}= x_7 \oplus \texttt{A5A5A5A5A5A5A5A5}; & x_1 &\mathrel{\oplus}= x_0; & x_2 &\mathrel{+}= x_1; & x_3 &\mathrel{-}= x_2 \oplus (\neg x_1 \ll 19); \\
x_4 &\mathrel{\oplus}= x_3; & x_5 &\mathrel{+}= x_4; & x_6 &\mathrel{-}= x_5 \oplus (\neg x_4 \gg 23); & x_7 &\mathrel{\oplus}= x_6; \\
x_0 &\mathrel{+}= x_7; & x_1 &\mathrel{-}= x_0 \oplus (\neg x_7 \ll 19); & x_2 &\mathrel{\oplus}= x_1; & x_3 &\mathrel{+}= x_2; \\
x_4 &\mathrel{-}= x_3 \oplus (\neg x_2 \gg 23); & x_5 &\mathrel{\oplus}= x_4; & x_6 &\mathrel{+}= x_5; & x_7 &\mathrel{-}= x_6 \oplus \texttt{0123456789ABCDEF}.
\end{aligned}$$

```pseudo id=main
TIGER(M, pad)                               ▷ pad = 01 for Tiger, 80 for Tiger2
L1  P ← M ‖ pad ‖ 00…00 ‖ [8n]₆₄            ▷ zeros until |P| ≡ 56 mod 64; length little-endian
L2  (a, b, c) ← IV
L3  for each 64-byte block Y of P, in order, do
L4      (a, b, c) ← COMPRESS((a, b, c), Y)
L14 return a ‖ b ‖ c                        ▷ each word in little-endian byte order

COMPRESS((a₀, b₀, c₀), Y)
L5  x[0..7] ← the 8 little-endian words of Y;  (a, b, c) ← (a₀, b₀, c₀)
L6  for each pass p = 0, 1, 2 with mul = 5, 7, 9 do
L7      if p > 0 then KEY-SCHEDULE(x)
L8      for i ← 0 to 7 do                   ▷ with the registers renamed as described
L9          c ← c ⊕ x[i]
L10         a ← a − (t₁[c₀] ⊕ t₂[c₂] ⊕ t₃[c₄] ⊕ t₄[c₆])
L11         b ← b + (t₄[c₁] ⊕ t₃[c₃] ⊕ t₂[c₅] ⊕ t₁[c₇])
L12         b ← b × mul
L13 return (a ⊕ a₀, b − b₀, c + c₀)
```

The S-boxes are not printed constants in the code: the designers generated them from the string "Tiger - A Fast New Hash Function, by Ross Anderson and Eli Biham", which is exactly one block. Each table starts with every word equal to its index byte repeated 8 times. Then the procedure makes five sweeps. In a sweep it visits each entry $i$ and each of the four tables in turn. For each visit it takes the next of the three registers, and every third visit it first runs COMPRESS on the string again, from the previous registers and with the tables as they are at that moment. Byte $k$ of the register chooses the entry whose byte $k$ is swapped with byte $k$ of entry $i$. The code follows this procedure, and the tests compare words of the result with the printed tables, such as $t_1[0] = \texttt{02AAB17CF7E90C5E}$.

## Example

**Tiger("abc").** The padded message is one block: $\texttt{61 62 63 01}$, 52 zero bytes, then the bit length 24 as 8 bytes little-endian. So $x_0 = \texttt{0000000001636261}$, $x_7 = \texttt{0000000000000018}$, and the other words are 0. The first round has $(a, b, c) = IV$ and multiplier 5:

- L9: $c = \texttt{F096A5B4C3B2E187} \oplus \texttt{0000000001636261} = \texttt{F096A5B4C2D183E6}$, with bytes $c_0, \ldots, c_7 = \texttt{E6, 83, D1, C2, B4, A5, 96, F0}$.
- L10: the even bytes give $a = \texttt{0123456789ABCDEF} - (t_1[\texttt{E6}] \oplus t_2[\texttt{D1}] \oplus t_3[\texttt{B4}] \oplus t_4[\texttt{96}]) = \texttt{88E9A28DC801D385}$.
- L11 and L12: the odd bytes give $b = (\texttt{FEDCBA9876543210} + (t_4[\texttt{83}] \oplus t_3[\texttt{C2}] \oplus t_2[\texttt{A5}] \oplus t_1[\texttt{F0}])) \times 5 = \texttt{94B4EC821716D181}$.

After 24 rounds and the feed-forward of line L13, the registers are $a = \texttt{F258C1E88414AB2A}$, $b = \texttt{527AB541FFC5B8BF}$ and $c = \texttt{935F7B951C132951}$, which are the three words that the Tiger page prints for "abc". Written little-endian, the digest is $\texttt{2aab1484e8c158f2bfb8c5ff41b57a525129131c957b5f93}$.

**The Tiger page vectors.** The designers' test results print the three words of each result as numbers. The tests check all nine, among them:

| Message | $a$, $b$, $c$ |
|---|---|
| "" | `24F0130C63AC9332 16166E76B1BB925F F373DE2D49584E7A` |
| "abc" | `F258C1E88414AB2A 527AB541FFC5B8BF 935F7B951C132951` |
| "Tiger" | `9F00F599072300DD 276ABB38C8EB6DEC 37790C116F9D2BDF` |

So Tiger("") as bytes is $\texttt{3293ac630c13f0245f92bbb1766e16167a4e58492dde73f3}$. **Tiger2** has no official test vectors that we could find. This code gives Tiger2("") $= \texttt{4441be75f6018773c206c22745374b924aa8313fef919f41}$ and Tiger2("abc") $= \texttt{f68d7bc5af4b43a06e048d7829560d4a9415658bb0b1f3bf}$; these are computed values, not standard ones. The tests check only that Tiger2 differs from Tiger in the pad byte and nowhere else.

## Correctness

The padding is injective for either pad byte and gives whole blocks, and the loop of lines L3 and L4 is the Merkle-Damgard iteration, so the [Merkle-Damgard theorem](/merkle-damgard-theorem/) reduces collisions of Tiger to collisions of COMPRESS. For a fixed block, each round is a bijection of the three registers (the multipliers 5, 7 and 9 are odd, so multiplication is invertible modulo $2^{64}$), and the key schedule is a bijection of the message words. So the 24 rounds compute a permutation $E_Y$ of the chaining value, and line L13 combines it with the input by $\oplus$, $-$ and $+$, one operation per word: a Davies-Meyer form with mixed operations. The proof file gives the details. That the code is Tiger is checked by the vectors.

## Complexity

Each block takes 24 rounds, each with 8 table lookups, 7 XORs, an addition, a subtraction and a multiplication, plus two runs of the key schedule: $\Theta(1)$ per block. A message of $n$ bytes has $\lfloor (n + 8)/64 \rfloor + 1$ blocks, so the time is $\Theta(n)$. The extra space is the three registers and eight words, $\Theta(1)$, plus the 8 KB of S-boxes, which are fixed. The tables are the price of the design: they fit in the first-level cache of the processors that Tiger was made for, but they make the speed depend on the cache.

## Properties

- **Generic security.** 192 bits give at most 96 bits against collisions and 192 against preimages.
- **Cryptanalysis.** Kelsey and Lucks (FSE 2006) found collisions for Tiger reduced to 16 of the 24 rounds. Mendel, Preneel, Rijmen, Yoshida and Watanabe (INDOCRYPT 2006) reached 19 rounds. Mendel and Rijmen (ASIACRYPT 2007) gave a pseudo-near-collision for the full 24 rounds, in which the attacker chooses the chaining value and the outputs differ in a few bits. No collision of the full hash is known.
- **Length extension.** Tiger is a plain Merkle-Damgard hash, so $H(M)$ and $|M|$ give $H(M \| \mathrm{pad} \| S)$. Use [HMAC](/hmac/) for a MAC.
- **Cache timing.** The S-box lookups use secret-dependent indices when the input is secret, so table-based Tiger leaks through the cache.

## Variants and improvements

- **Tiger2.** The same function with the pad byte $\texttt{80}$, as in MD4, MD5 and SHA-1. Only the first padding byte changes.
- **Tiger/160 and Tiger/128.** The first 160 or 128 bits of the digest, for use in place of SHA-1 or MD5.
- **Tiger Tree Hash (TTH).** A [Merkle tree](/merkle-tree/) of Tiger hashes over 1024-byte leaves, with a leaf prefix $\texttt{00}$ and an inner prefix $\texttt{01}$, used in the Gnutella and Direct Connect file-sharing networks to verify parts of large files.

## When to use it

Use Tiger only to read or verify existing data: Tiger Tree Hashes in file-sharing networks and old archives or checksums. For new work, use [SHA-2](/sha-2/), [SHA-3](/sha-3/) or [BLAKE2](/blake2/). Tiger has had less analysis than these, the full-round pseudo-near-collision has eroded its margin, and 96-bit collision security is low by today's standards.

## Pitfalls

- **Tiger is not Tiger2.** The pad byte changes every digest. A library named "tiger" may implement either; check "" against `3293ac63` (Tiger) or `4441be75` (Tiger2 as computed here).
- **Byte order of the vectors.** The designers print each of the three words as a big number, so "" appears as `24F0130C63AC9332 …`. The digest bytes are each word little-endian, `3293ac630c13f024 …`. Some libraries print one form and some the other.
- **S-box generation.** The tables are derived, not random. A port that copies them by hand should check a few words, as the tests do.
- **For study only.** The code on this page is slow and not constant time. Tiger is not in `hashlib`; use a vetted library if a format needs it.

## Implementations

## History

Anderson and Biham designed Tiger in 1995 and presented it at the third Fast Software Encryption workshop in Cambridge in February 1996, the same volume that has RIPEMD-160. The aim was a hash that is fast on 64-bit processors such as the DEC Alpha, at a time when MD4 was broken and MD5 had been attacked. Tiger was not patented and saw use in file-sharing networks through the Tiger Tree Hash. Later the designers published Tiger2, which uses the usual MD4 padding byte. The attacks of 2006 and 2007 by Kelsey and Lucks and by Mendel, Rijmen and colleagues reached reduced versions and then the full compression function with a pseudo-near-collision.

## References
