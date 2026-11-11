---
tag: 07Z3SA
kind: algorithm
slug: xtea
name: XTEA
aliases:
- Extended TEA
area: cryptography/symmetric-ciphers
level: intro
summary: The 1997 repair of TEA by Needham and Wheeler. It keeps the 64-bit block, 128-bit key and 64 Feistel rounds, but picks key words from the round sum, which removes the equivalent keys.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of 64-bit blocks}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1997
  people: [Roger Needham, David Wheeler]
  note: Needham and Wheeler published XTEA and Block TEA in the report Tea extensions (1997), after the equivalent keys and related-key attacks on TEA. XXTEA followed in 1998.
prereqs: [tea, feistel-network]
see_also: [tea, feistel-network, key-schedule, related-key-attack, speck, block-cipher]
sources:
  - paper: "Roger M. Needham and David J. Wheeler, Tea extensions, technical report, Computer Laboratory, University of Cambridge, October 1997"
    locator: the C code of XTEA (tean with a positive round count) and of Block TEA, and the reasons for the changes from TEA
  - paper: "David J. Wheeler and Roger M. Needham, Correction to xtea, technical report, Computer Laboratory, University of Cambridge, October 1998"
    locator: the C code of XXTEA (Corrected Block TEA) and the number of cycles 6 + 52/n
  - paper: "Elias Yarrkov, Cryptanalysis of XXTEA, IACR Cryptology ePrint Archive, Report 2010/254"
    locator: the chosen-plaintext attack on full XXTEA with wide blocks
  - paper: "Dukjae Moon, Kyungdeok Hwang, Wonil Lee, Sangjin Lee and Jongin Lim, Impossible differential cryptanalysis of reduced round XTEA and TEA, Fast Software Encryption (FSE 2002), LNCS 2365"
    locator: the impossible differential attack on 14 rounds of XTEA
  - paper: "Jiqiang Lu, Related-key rectangle attack on 36 rounds of the XTEA block cipher, International Journal of Information Security 8(1), 2009"
    locator: the related-key rectangle attack on rounds 1 to 36 of XTEA
  - url: "https://github.com/weidai11/cryptopp/blob/master/TestVectors/tea.txt"
    title: Crypto++ test vectors for TEA and XTEA (TestVectors/tea.txt), which cite http://www.cix.co.uk/~klockstone/teavect.htm as their source
    locator: the XTEA entries (published reference values, not official test vectors; the field Rounds counts cycles)
---

XTEA (extended TEA) is a [block cipher](/block-cipher/) with 64-bit blocks and 128-bit keys, published by Roger Needham and David Wheeler in 1997 to fix the weak key schedule of [TEA](/tea/). Like TEA it is a [Feistel network](/feistel-network/) of 32 cycles (64 rounds) built from shifts, XORs and additions modulo $2^{32}$, and it fits in a few lines of code with no tables. The change is in how the key enters: each round adds one key word, chosen by two bits of a running sum, so the key words appear in an irregular order. This removes the equivalent keys of TEA. Reduced-round versions have been attacked, and no attack on the full 64 rounds is known that is faster than exhaustive search, but the 64-bit block limits its use today.

## In plain words

XTEA cuts a 64-bit block into two 32-bit halves. In each step it scrambles one half with shifts and an addition, and combines the result with a key word and a counter. Then it adds the result to the other half, and the halves change roles. The counter grows by a fixed number from the golden ratio. Two bits of the counter choose which of the four key words the step uses, so the key words come in an order that looks irregular. In TEA, each step used the same two key words in the same places, and that let two different keys act the same. After 64 steps the block is the ciphertext. Decryption runs the steps backward and subtracts.

## The problem

Encrypt a 64-bit block $v = (v_0, v_1)$ under a key $k = (k_0, k_1, k_2, k_3)$ of four 32-bit words, with a keyed permutation that has the small size and speed of TEA but not its equivalent keys and related-key weakness.

## The algorithm

Let $\delta = \texttt{0x9E3779B9}$, as in TEA. Words are 32-bit, $+$ and $-$ are modulo $2^{32}$, $\ll$ and $\gg$ are logical shifts, and $r$ is the number of cycles (the standard value is 32).

```pseudo id=main
XTEA-ENCRYPT((v0, v1), k[0..3], r)
L1  sum ← 0
L2  for i ← 1 to r do
L3      v0 ← v0 + ((((v1 ≪ 4) ⊕ (v1 ≫ 5)) + v1) ⊕ (sum + k[sum AND 3]))
L4      sum ← sum + δ
L5      v1 ← v1 + ((((v0 ≪ 4) ⊕ (v0 ≫ 5)) + v0) ⊕ (sum + k[(sum ≫ 11) AND 3]))
L6  return (v0, v1)

XTEA-DECRYPT((v0, v1), k[0..3], r)
L7  sum ← r·δ mod 2^32
L8  for i ← 1 to r do
L9      v1 ← v1 − ((((v0 ≪ 4) ⊕ (v0 ≫ 5)) + v0) ⊕ (sum + k[(sum ≫ 11) AND 3]))
L10     sum ← sum − δ
L11     v0 ← v0 − ((((v1 ≪ 4) ⊕ (v1 ≫ 5)) + v1) ⊕ (sum + k[sum AND 3]))
L12 return (v0, v1)
```

Lines L3 and L5 are two Feistel rounds. The data part $((x \ll 4) \oplus (x \gg 5)) + x$ mixes each bit with bits 4 places up and 5 places down, and the addition of $x$ adds carries. The key part $\mathit{sum} + k_j$ is XORed in, so the round function is $G(x) \oplus (\mathit{sum} + k_j)$. Line L3 picks the key word from the two low bits of $\mathit{sum}$ before line L4 updates it, and line L5 picks it from bits 11 and 12 after the update. The two lines therefore use different, irregular sequences of key words. Each key word enters a round only through $\mathit{sum} + k_j$, a single term, so a change in $k_j$ cannot cancel inside one round as in TEA.

The code on this page is for study only. It is not constant time as Python runs it, and with its 64-bit block it must not protect real data. Use a vetted cipher from libsodium, OpenSSL or a FIPS 140 validated module.

## Example

The key words used in the first eight cycles do not depend on the key, only on $\mathit{sum}$:

| cycle $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| line L3 uses $k[\cdot]$ | 0 | 1 | 2 | 3 | 0 | 1 | 2 | 3 |
| line L5 uses $k[\cdot]$ | 3 | 2 | 1 | 0 | 0 | 3 | 2 | 1 |

For the zero block under the zero key: after one cycle the block is 00000000 9e3779b9 (line L3 adds $0 \oplus (0 + 0) = 0$, line L5 adds $0 \oplus (\delta + 0) = \delta$), after two cycles 1b8ae3af 8dcb1ca7, and after 32 cycles dee9d4d8 f7131ed9.

There are no official XTEA test vectors. The tests use published reference values from the Crypto++ file tea.txt, which names Klockstone's page as its source. Words are big-endian, and the field "Rounds" in that file counts cycles. With 32 cycles, the key 27f917b1 c1da8993 60e2acaa a6eb923d and the block af20a390 547571aa give d26428af 0a202283. The values for 1 and 2 cycles also match.

## Correctness

Each half-cycle adds to one half a value that depends only on the other half, $\mathit{sum}$ and the key, so it is undone by subtracting the same value. Line L7 sets $\mathit{sum}$ to its final value $r\delta$. Decryption cycle $j$ starts with $\mathit{sum} = (r - j + 1)\delta$, the value that encryption cycle $r - j + 1$ has at line L5, so line L9 undoes that line L5. Then line L10 restores the value of line L3 of the same cycle, and line L11 undoes it. By induction over the cycles, decryption inverts encryption, so each key gives a permutation. The argument is the one for [TEA](/tea/), with the order of the update to $\mathit{sum}$ taken into account. The proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

One cycle is a fixed number of 32-bit shifts, XORs, additions and one indexed load of a key word, so a block costs $\Theta(r)$, which is $\Theta(1)$ for $r = 32$, and $n$ blocks cost $\Theta(n)$. There are no tables and no key setup, so the extra space is $\Theta(1)$. XTEA is a little slower than TEA per round because of the key word selection.

## Properties

- **Block and key.** A 64-bit block and a 128-bit key, with 64 Feistel rounds.
- **No TEA equivalent keys.** Flipping the top bits of $k_0$ and $k_1$ is an equivalence for TEA but changes the XTEA ciphertext. The tests check this on 100 random keys.
- **Irregular key use.** The key word of each round comes from bits of $\mathit{sum} = i\delta$, a fixed but irregular sequence, which also makes rounds differ and resists slide attacks.
- **Small and table-free.** It needs no S-boxes, so there are no table-lookup timing leaks; branch-free code is easy.

## Variants and improvements

- **Block TEA** (1997, in the same report) encrypts a block of any number $n \ge 2$ of 32-bit words. Each round updates each word from its two neighbours, the key and $\mathit{sum}$. Weaknesses were found soon after.
- **XXTEA** (Corrected Block TEA, 1998) changes the round function of Block TEA and uses $6 + \lfloor 52/n \rfloor$ cycles for $n$ words. Yarrkov (2010) gave a chosen-plaintext attack on full XXTEA. It works best for wide blocks, where the number of cycles is small, and it uses about $2^{59}$ queries. Do not use XXTEA.
- **Reduced rounds.** Impossible differential cryptanalysis breaks 14 rounds of XTEA (Moon et al., 2002), and a related-key rectangle attack breaks 36 rounds (Lu, 2009). Later work on meet-in-the-middle and related-key attacks has gone further, but no attack on all 64 rounds in the single-key setting is known that beats exhaustive search.

## When to use it

XTEA is suited to study, and it is still found in old embedded code where a table-free cipher of a few lines was needed. For new designs do not use it: its 64-bit block reaches the [birthday bound](/birthday-attack/) after about $2^{32}$ blocks, and it has no official test vectors, no standard and no modern analysis of the kind given to AES or [Ascon](/ascon/). For constrained devices use a [lightweight](/lightweight-cryptography/) standard such as Ascon, or AES where hardware supports it.

## Pitfalls

- **Rounds against cycles.** Some code counts Feistel rounds and some counts cycles. The standard XTEA has 32 cycles, which are 64 rounds. Reference files differ too: Crypto++ calls cycles "Rounds".
- **Byte order.** The design is on 32-bit words. Implementations read bytes into words in big-endian or little-endian order, so two correct implementations may disagree on the same bytes.
- **The order of the sum update.** Line L4 sits between the two half-cycles. If it moves, the key selection of line L5 changes and the cipher is no longer XTEA.
- **Confusing XTEA and XXTEA.** XXTEA is a different, wide-block cipher and has a practical-scale attack. A library function called "xxtea" is not XTEA.
- **Signed shifts.** In C, the words must be unsigned so that $\gg$ is a logical shift.

## Implementations

## History

TEA (1994) had a fixed use of the key words, and in 1996 and 1997 Kelsey, Schneier and Wagner showed its equivalent keys and a related-key attack. In October 1997, Needham and Wheeler answered with a technical report of the Cambridge Computer Laboratory, "Tea extensions". It defined XTEA, with the new key selection, and Block TEA for longer blocks. A further report in October 1998, "Correction to xtea", defined XXTEA after weaknesses were found in Block TEA. In 2010 Elias Yarrkov published a chosen-plaintext attack on full XXTEA. XTEA itself has stayed unbroken in its full form, and its analysis has moved to reduced-round and related-key attacks.

## References
