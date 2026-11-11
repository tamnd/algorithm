---
tag: 1JEH0C
kind: algorithm
slug: tea
name: Tiny Encryption Algorithm
aliases:
- TEA
area: cryptography/symmetric-ciphers
level: intro
summary: A 64-bit block cipher with a 128-bit key and 64 Feistel rounds of shifts, XORs and additions (Wheeler and Needham, 1994). Each key has three equivalent keys, and it has related-key attacks.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of 64-bit blocks}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1994
  people: [David Wheeler, Roger Needham]
  note: Wheeler and Needham of the Cambridge Computer Laboratory presented TEA at Fast Software Encryption 1994 as a cipher short enough to remember. XTEA (1997) fixed its key schedule.
prereqs: [feistel-network, block-cipher]
see_also: [xtea, feistel-network, related-key-attack, key-schedule, rc5, speck, block-cipher]
sources:
  - paper: "David J. Wheeler and Roger M. Needham, TEA, a tiny encryption algorithm, Fast Software Encryption (FSE 1994), LNCS 1008, Springer, 1995, pages 363 to 366"
    locator: the C code of encode and decode with 32 cycles, the constant delta = 0x9E3779B9 from the golden ratio, and the notes on the number of cycles
  - paper: "John Kelsey, Bruce Schneier and David Wagner, Key-schedule cryptanalysis of IDEA, G-DES, GOST, SAFER, and Triple-DES, Advances in Cryptology (CRYPTO 1996), LNCS 1109"
    locator: the equivalent keys of TEA (each key is equivalent to three others, so the effective key length is 126 bits)
  - paper: "John Kelsey, Bruce Schneier and David Wagner, Related-key cryptanalysis of 3-WAY, Biham-DES, CAST, DES-X, NewDES, RC2, and TEA, Information and Communications Security (ICICS 1997), LNCS 1334"
    locator: the related-key differential attack on full TEA
  - paper: "Michael Steil, 17 Mistakes Microsoft Made in the Xbox Security System, 22nd Chaos Communication Congress (22C3), 2005"
    locator: the use of TEA as a hash function in the Xbox boot chain and the attack that uses its equivalent keys
  - url: "https://github.com/weidai11/cryptopp/blob/master/TestVectors/tea.txt"
    title: Crypto++ test vectors for TEA and XTEA (TestVectors/tea.txt), which cite http://www.cix.co.uk/~klockstone/teavect.htm as their source
    locator: the TEA entries (published reference values, not official test vectors)
---

The Tiny Encryption Algorithm (TEA) is a [block cipher](/block-cipher/) with 64-bit blocks and 128-bit keys, by David Wheeler and Roger Needham (1994). Its whole round function is one line of C: shifts, XORs and additions modulo $2^{32}$, applied in a [Feistel network](/feistel-network/) of 32 cycles (64 rounds). It has no S-box and no real key schedule: the four key words are used in the same way in every cycle. That simplicity makes it a good example, and also the cause of its main weaknesses: each key has three equivalent keys, and related-key attacks break it. [XTEA](/xtea/) is the repaired version.

## In plain words

TEA cuts a 64-bit block into two 32-bit halves. In each step, it mixes one half and adds the result to the other half. The mix shifts the half left by 4 places and adds a key word, shifts it right by 5 places and adds another key word, adds a growing counter, and XORs the three results. Then the halves change roles. After 64 such steps the block is the ciphertext. To decrypt, run the steps backward and subtract instead of add. The counter grows by a fixed number taken from the golden ratio, so no two steps are the same. The key words are used the same way in each step, so the top bit of two key words can cancel. Thus four keys give the same cipher.

## The problem

Encrypt a 64-bit block $v = (v_0, v_1)$ under a 128-bit key $k = (k_0, k_1, k_2, k_3)$, all 32-bit words, with a permutation of $\{0,1\}^{64}$ that depends on the key and has an inverse. TEA aims at a cipher that is small in code, needs no tables and no setup time, and is fast on 32-bit processors.

## The algorithm

Let $\delta = \texttt{0x9E3779B9} = \lfloor 2^{32}/\varphi \rfloor$, where $\varphi = (1 + \sqrt 5)/2$. All words are 32-bit, $+$ and $-$ are modulo $2^{32}$, and $\ll$, $\gg$ are logical shifts.

```pseudo id=main
TEA-ENCRYPT((v0, v1), (k0, k1, k2, k3))
L1  sum ← 0
L2  for i ← 1 to 32 do                             ▷ one cycle = two Feistel rounds
L3      sum ← sum + δ
L4      v0 ← v0 + (((v1 ≪ 4) + k0) ⊕ (v1 + sum) ⊕ ((v1 ≫ 5) + k1))
L5      v1 ← v1 + (((v0 ≪ 4) + k2) ⊕ (v0 + sum) ⊕ ((v0 ≫ 5) + k3))
L6  return (v0, v1)

TEA-DECRYPT((v0, v1), (k0, k1, k2, k3))
L7  sum ← 32·δ mod 2^32                            ▷ = 0xC6EF3720
L8  for i ← 1 to 32 do
L9      v1 ← v1 − (((v0 ≪ 4) + k2) ⊕ (v0 + sum) ⊕ ((v0 ≫ 5) + k3))
L10     v0 ← v0 − (((v1 ≪ 4) + k0) ⊕ (v1 + sum) ⊕ ((v1 ≫ 5) + k1))
L11     sum ← sum − δ
L12 return (v0, v1)
```

Lines L4 and L5 are two Feistel rounds, with addition modulo $2^{32}$ in place of XOR. Write $F(x, s, a, b) = ((x \ll 4) + a) \oplus (x + s) \oplus ((x \gg 5) + b)$. Round $2i - 1$ adds $F(v_1, \mathit{sum}_i, k_0, k_1)$ to $v_0$, and round $2i$ adds $F(v_0, \mathit{sum}_i, k_2, k_3)$ to $v_1$, where $\mathit{sum}_i = i\delta$. The shifts mix bits across positions, the additions give nonlinearity through their carries, and the XOR of addition and shift results mixes the two group operations. The term $v + \mathit{sum}$ makes each cycle different, which stops slide attacks that need identical rounds. Decryption runs the same rounds backward: line L9 undoes line L5 of cycle $i$, because $v_0$ at that point is the value it had when line L5 ran.

The code on this page is for study only. It is not constant time as Python runs it, TEA has related-key attacks, and the code must not protect real data. Use a vetted cipher from libsodium, OpenSSL or a FIPS 140 validated module.

## Example

Encrypt the zero block under the zero key. In cycle 1, $\mathit{sum} = \delta$. Line L4 gives $v_0 = 0 + ((0 + 0) \oplus (0 + \delta) \oplus (0 + 0)) = \texttt{9e3779b9}$. Line L5 gives $v_1 = \texttt{dbe8d32f}$.

| cycle $i$ | $\mathit{sum}$ | $v_0$ | $v_1$ |
|---|---|---|---|
| 1 | 9e3779b9 | 9e3779b9 | dbe8d32f |
| 2 | 3c6ef372 | 3e3d2c81 | 747811b6 |
| 3 | daa66d2b | 4979d18d | 266efa9a |
| 31 | 28b7bd67 | fa8572e9 | 804528e6 |
| 32 | c6ef3720 | 41ea3a0a | 94baa940 |

The ciphertext 41ea3a0a 94baa940 matches the published reference value. There are no official TEA test vectors; the values used here are from the Crypto++ file tea.txt, which names Klockstone's page as its source, with words read big-endian.

**Equivalent keys.** The key 01234567 89abcdef fedcba98 76543210 encrypts the zero block to f257f740 2d578cee. So do 81234567 09abcdef fedcba98 76543210 (top bits of $k_0, k_1$ flipped), 01234567 89abcdef 7edcba98 f6543210 (top bits of $k_2, k_3$ flipped), and the key with all four top bits flipped. The tests check this on random blocks and keys.

## Correctness

Each Feistel round is invertible: line L4 maps $(v_0, v_1)$ to $(v_0 + F(v_1, \ldots), v_1)$, and subtracting the same value, which depends only on $v_1$, the key and the cycle, gives $v_0$ back. Line L7 starts $\mathit{sum}$ at its value in cycle 32, and line L11 steps it down, so decryption cycle $j$ uses $\mathit{sum}_{33-j}$ and undoes encryption cycle $33 - j$. For the equivalent keys: adding $2^{31}$ modulo $2^{32}$ only flips the top bit, so flipping the top bits of both $k_0$ and $k_1$ flips the top bit of two of the three XORed terms of $F$, and the two flips cancel. The full proofs are in [proofs/correctness.md](proofs/correctness.md).

## Complexity

One block takes 32 cycles of a fixed number of 32-bit operations: about 6 shifts and additions and 2 XORs per round, so $\Theta(1)$ per block and $\Theta(n)$ for $n$ blocks. TEA needs no tables and no key setup, so its extra space is $\Theta(1)$, and the key is used directly. On 32-bit processors it is fast for its size, but each round does little mixing, which is why it needs 64 rounds.

## Properties

- **Block and key.** 64-bit blocks and a nominal 128-bit key. Because of the equivalent keys, there are at most $2^{126}$ distinct permutations.
- **Feistel network.** Encryption and decryption have the same structure with the round order reversed.
- **No S-boxes, no table lookups.** The nonlinearity comes from the carries of addition modulo $2^{32}$. With no table lookups there are no cache-timing leaks from tables; data-dependent timing can still come from the platform.
- **Weak key schedule.** Rounds use the fixed pairs $(k_0, k_1)$ and $(k_2, k_3)$. Only $\mathit{sum}$ changes from cycle to cycle.

## Variants and improvements

- **[XTEA](/xtea/)** (Needham and Wheeler, 1997) changes the order of the operations and selects the key word in each round from bits of $\mathit{sum}$, so the key words are used in an irregular order. This removes the equivalent keys and the 1997 related-key attack on TEA.
- **Block TEA and XXTEA** (1997 and 1998) work on blocks of any number of 32-bit words. They are covered on the [XTEA](/xtea/) page.
- **Fewer cycles.** The authors suggested that 16 cycles may suffice and that 32 is conservative. Reduced-round versions have been attacked by differential and impossible differential cryptanalysis.

## When to use it

Do not use TEA for new designs. Its equivalent keys break its use as a hash, and related-key attacks matter whenever keys are derived from each other. It also has only a 64-bit block, so a key must protect far fewer than $2^{32}$ blocks because of the [birthday bound](/birthday-attack/). TEA is useful for study: it shows the Feistel structure, the role of round constants and the cost of a weak key schedule in about ten lines. For small devices today, use a modern [lightweight](/lightweight-cryptography/) design such as [Ascon](/ascon/).

## Pitfalls

- **Equivalent keys in a hash.** A Davies-Meyer hash $H_i = E_{m_i}(H_{i-1}) \oplus H_{i-1}$ built from TEA has free collisions: flip the top bits of $m_i$'s words 0 and 1 and the hash does not change. The Xbox boot chain used TEA in this way, and the equivalent keys let attackers change the hashed code without changing the hash (see Steil, 2005).
- **Byte order.** The paper defines TEA on 32-bit words, not on bytes. Libraries differ in how they read bytes into words, so check a vector before you combine two implementations.
- **Signed shifts.** In C, $v \gg 5$ on a signed int is an arithmetic shift on most platforms. TEA needs a logical shift, so the words must be unsigned.
- **The number of cycles.** Some code uses 16 cycles or a different $\delta$ and still calls it TEA. The result is not interoperable and not the analysed cipher.
- **A 64-bit block.** With $2^{32}$ blocks under one key in CBC or CTR mode, block collisions leak plaintext.

## Implementations

## History

David Wheeler and Roger Needham of the Cambridge Computer Laboratory presented TEA at Fast Software Encryption in Leuven in December 1994. The goal was a cipher that one could carry in one's head and write in a few lines in any language, with no tables. Kelsey, Schneier and Wagner noted in 1996 that each TEA key has three equivalent keys, and in 1997 gave a related-key attack on the full cipher. Wheeler and Needham replied in 1997 with the "Tea extensions" report, which defined XTEA and Block TEA, and in 1998 with XXTEA. Microsoft used TEA as a hash in the boot chain of the original Xbox, and the equivalent keys were part of the hardware hacks of that system.

## References
