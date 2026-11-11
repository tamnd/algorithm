---
tag: H2EQ3A
kind: technique
slug: substitution-permutation-network
name: Substitution-permutation network
aliases:
- SPN
area: cryptography/symmetric-ciphers
level: core
summary: A block cipher built from rounds that XOR a round key, apply small S-boxes to the whole state and then a linear mixing layer. AES is one. The inverse needs the inverse S-box and layer.
prereqs: [s-box, block-cipher]
see_also: [advanced-encryption-standard, feistel-network, confusion-and-diffusion, key-schedule, differential-cryptanalysis, linear-cryptanalysis, serpent, present]
sources:
  - paper: doi:10.1080/0161-110291890885
    title: Howard M. Heys, A tutorial on linear and differential cryptanalysis, Cryptologia 26(3), 2002
    locator: Section 2, the basic substitution-permutation network (16-bit block, four 4-bit S-boxes, the bit permutation, five round keys)
  - book: isbn:9781584885085
    title: Douglas R. Stinson, Cryptography, Theory and Practice, third edition, Chapman and Hall/CRC, 2005
    locator: Chapter 3, Section 3.2 (substitution-permutation networks, the example with K = 3A94D63F and x = 26B7)
  - book: isbn:9783540425809
    title: Joan Daemen and Vincent Rijmen, The Design of Rijndael, Springer, 2002
    locator: Chapter 3 (the round structure of Rijndael) and Chapter 9 (the wide trail strategy)
  - paper: doi:10.1002/j.1538-7305.1949.tb00928.x
    title: Claude E. Shannon, Communication theory of secrecy systems, Bell System Technical Journal 28(4), 1949
    locator: the mixing transformations and product ciphers that alternate substitution and transposition
---

A substitution-permutation network (SPN) is a way to build a [block cipher](/block-cipher/) from rounds that each XOR a round key into the whole state, apply small invertible [S-boxes](/s-box/) in parallel, and then apply a linear layer that moves or mixes the bits between S-boxes. The S-boxes give confusion and the linear layer gives diffusion, in the sense of [Shannon](/confusion-and-diffusion/). Unlike a [Feistel network](/feistel-network/), each round changes the whole state, and decryption needs the inverse S-boxes and the inverse linear layer. [AES](/advanced-encryption-standard/), [Serpent](/serpent/) and [PRESENT](/present/) are SPNs, and the 16-bit SPN of Heys's tutorial is the standard toy example.

## In plain words

The state is a row of small groups of bits. In one round, you first mix in a round key with exclusive or. Then each group goes through a small lookup table, which replaces it by another value in a scrambled way. Then the bits are moved between groups, so that each group of the next round gets bits from many groups of this round.

After a few rounds, each output bit depends on every input bit and every key bit, in a tangled way.

To undo a round, you must run each step backward: move the bits back, look up each group in the reverse table, and remove the key. So, unlike a Feistel cipher, decryption needs the reverse tables, and it is a separate procedure.

## When it applies

Use an SPN when you can afford invertible S-boxes and an invertible linear layer, and you want full diffusion in few rounds. Each round acts on all bits, so an SPN needs fewer rounds than a Feistel cipher of the same strength. The price is that the decryption circuit differs from the encryption circuit. The design also gives clean proofs of resistance to [differential](/differential-cryptanalysis/) and [linear cryptanalysis](/linear-cryptanalysis/), by counting active S-boxes.

The notation on this page: the state has $n$ bits, split into $m$ words of $b$ bits; $S$ is a bijective S-box on $b$ bits; $P$ is an invertible linear map on $n$ bits; and $K_1, \ldots, K_{r+1}$ are the round keys of an $r$-round cipher.

## The template

SPN follows the layout of Heys and of AES. Rounds 1 to $r - 1$ are full rounds. Round $r$ omits the linear layer, and a last round key follows it.

```pseudo id=main
SPN(S, P, K1, ..., K(r+1), x)
L1  w ← x
L2  for i ← 1 to r − 1 do
L3      u ← w ⊕ Ki                         ▷ key mixing
L4      v ← S applied to each b-bit word of u
L5      w ← P(v)                           ▷ the linear layer
L6  u ← w ⊕ Kr
L7  v ← S applied to each b-bit word of u
L8  return v ⊕ K(r+1)
```

The cost is $r$ layers of $m$ S-box lookups, $r - 1$ applications of $P$ and $r + 1$ XORs of $n$ bits. The Python code for this page runs the 16-bit Heys cipher. It is for study only, is not constant time, and must not be used to protect real data. For real data, use AES from a FIPS 140 validated module or from libsodium.

**Lemma (an SPN is a block cipher).** If $S$ is a bijection and $P$ is invertible, then for every choice of round keys, SPN is a bijection of $\{0,1\}^n$, and its inverse is

$$x = K_1 \oplus S^{-1}\Bigl(P^{-1}\bigl(K_2 \oplus S^{-1}(P^{-1}(\cdots K_r \oplus S^{-1}(y \oplus K_{r+1}) \cdots))\bigr)\Bigr),$$

where $S^{-1}$ acts on each word.

*Proof.* Each step of lines L3 to L8 is a bijection of $\{0,1\}^n$: XOR with a fixed key is its own inverse, the layer of $m$ copies of $S$ is a bijection with inverse the layer of $m$ copies of $S^{-1}$, and $P$ is invertible. A composition of bijections is a bijection, and its inverse applies the inverses of the steps in reverse order. Writing these out from line L8 back to line L3 gives the formula. $\square$

So decryption is again an SPN-like network, but with $S^{-1}$ in place of $S$, $P^{-1}$ in place of $P$, the keys in reverse order and the order of the S-box and linear layers swapped. In AES, the decryption round keys of the "equivalent inverse cipher" are also passed through the inverse of MixColumns. This is the main structural difference from a Feistel network, whose inverse reuses the same round function with no inverse at all.

## Classic examples

**The Heys toy SPN.** $n = 16$, four 4-bit S-boxes, all equal to $S$ = E, 4, D, 1, 2, F, B, 8, 3, A, 6, C, 5, 9, 0, 7 (in hex, for inputs 0 to F), $r = 4$ rounds and five independent 16-bit round keys. The linear layer $P$ sends bit $i$ of the state to bit $4((i-1) \bmod 4) + \lfloor (i-1)/4 \rfloor + 1$, for bits numbered 1 to 16 from the left. This is the transpose of a $4 \times 4$ bit matrix: output bit $j$ of S-box $a$ goes to input bit $a$ of S-box $j$. The transpose is its own inverse.

**A worked trace.** Stinson uses the same S-box and permutation with the round keys taken from a 32-bit key $K$ = 3A94D63F: $K_i$ is the 16 bits of $K$ that start at bit $4i - 3$. So $K_1, \ldots, K_5$ = 3A94, A94D, 94D6, 4D63, D63F. For $x$ = 26B7:

| round | $u = w \oplus K_i$ | $v = S(u)$ | $w = P(v)$ |
|---|---|---|---|
| 1 | 1C23 | 45D1 | 2E07 |
| 2 | 874A | 3826 | 41B8 |
| 3 | D56E | 9FB0 | E46E |
| 4 | A90D | 6AE9 | |

The output is 6AE9 $\oplus$ D63F = BCD6, as in Stinson's example. Decryption of BCD6 with the inverse S-box returns 26B7.

**Diffusion.** On the Heys cipher with random keys, flipping one random plaintext bit changes on average 2.44 of the 16 output bits after 1 round, 5.94 after 2 rounds, 7.67 after 3 rounds, 7.94 after 4 rounds and 7.98 after 5 rounds. The ideal value is 8.

**AES.** The state is a $4 \times 4$ array of bytes, and $S$ is the AES S-box on 8 bits. The linear layer is ShiftRows followed by MixColumns, which is not a bit permutation but a linear map over GF($2^8$) with branch number 5. AES-128 has 10 rounds, and the last round omits MixColumns. See [AES](/advanced-encryption-standard/).

**Serpent and PRESENT.** [Serpent](/serpent/) has 32 rounds of 32 parallel 4-bit S-boxes and a linear transformation on 128 bits. [PRESENT](/present/) has 31 rounds of 16 parallel 4-bit S-boxes and a bit permutation on 64 bits, for small hardware.

## Variations

- **Bit permutation or linear mixing.** A bit permutation, as in Heys and PRESENT, is free in hardware but spreads each S-box output to only a few S-boxes. A linear map with a high branch number, such as the MixColumns of AES, spreads more and allows the bounds of the wide trail strategy.
- **Key-alternating ciphers.** An SPN in which the round key is only XORed, and the round function is otherwise fixed, is key-alternating. AES is one. With one round and a public permutation it is the [Even-Mansour cipher](/key-whitening/).
- **The last round.** Omitting the linear layer in the last round, as in Heys and AES, does not change security, because the attacker can apply or remove a known linear map. It makes the inverse cipher look like the cipher.
- **Partial SPN.** Only some words go through S-boxes in each round, as in LowMC or in the partial rounds of Poseidon. This saves nonlinear operations but needs more rounds.

## Pitfalls

- **A linear layer after the last key.** A final $P$ with no key after it adds nothing, since anyone can invert it. Put the last round key after the last nonlinear layer.
- **Weak S-boxes.** If $S$ is affine, the whole SPN is affine in $x$ for each key and falls to a few queries. The quality of $S$ is measured by its differential uniformity and nonlinearity; see [S-box](/s-box/).
- **Too few rounds.** The Heys cipher with 4 rounds is broken by the differential and linear attacks of the tutorial, with a few thousand chosen or known plaintexts.
- **Decryption tables.** An implementation needs $S^{-1}$ and $P^{-1}$, and a mistake in one of them shows only in decryption tests. Test both directions against official vectors.
- **Table lookups and timing.** A software SPN with table lookups indexed by key-dependent data leaks the index through the cache. See [AES](/advanced-encryption-standard/) and [timing attack](/timing-attack/).

## Exercises

1. Write out the decryption of BCD6 in the worked trace step by step, with $S^{-1}$ = E, 3, 4, 8, 1, C, A, F, 7, D, 9, 6, B, 2, 0, 5.
2. Show that the Heys permutation $P$ is an involution, and that this lets the decryption code apply $P$ in place of $P^{-1}$.
3. Show that if $S$ is an affine map over GF(2) on $b$ bits, then for each key the SPN satisfies $E(x) \oplus E(x') \oplus E(x'') = E(x \oplus x' \oplus x'')$, and give a distinguisher with 4 queries.
4. In the Heys cipher, a difference in one input bit of one S-box gives a nonzero difference in at least one output bit. Show that each round then has at least one active S-box, and explain why a bit permutation cannot give more than this lower bound of 1 per round.
5. Count the S-box lookups of AES-128, AES-192 and AES-256 per block, including the key expansion.

## References
