---
tag: NB7K96
kind: algorithm
slug: rc5
name: RC5
area: cryptography/symmetric-ciphers
level: advanced
summary: A block cipher by Rivest (1994) with a variable word size, number of rounds and key length. Its only nonlinear step is a rotation by an amount that depends on the data.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of blocks, r: the number of rounds}
  time: {worst: Θ(r·n), average: Θ(r·n), best: Θ(r·n)}
  space: {extra: Θ(r)}
properties: {deterministic: true}
history:
  year: 1994
  people: [Ronald L. Rivest]
  note: Rivest presented RC5 at the Fast Software Encryption workshop in Leuven in December 1994. RFC 2040 of 1996 describes it with its modes.
prereqs: [block-cipher, bitwise-operations, key-schedule]
see_also: [rc6, feistel-network, blowfish, data-encryption-standard, differential-cryptanalysis, linear-cryptanalysis, exhaustive-key-search, rc4]
sources:
  - paper: doi:10.1007/3-540-60590-8_7
    title: Ronald L. Rivest, The RC5 encryption algorithm, Fast Software Encryption (FSE 1994), LNCS 1008, Springer, 1995
    locator: the parameters w, r and b, the encryption and decryption algorithms, the key expansion with the constants P_w and Q_w, and the discussion of data-dependent rotations
  - url: "https://people.csail.mit.edu/rivest/Rivest-rc5rev.pdf"
    title: Ronald L. Rivest, The RC5 encryption algorithm, revised version of the FSE 1994 paper
    locator: the same description, with the notation RC5-w/r/b and the nominal choice RC5-32/12/16
  - url: "https://www.rfc-editor.org/rfc/rfc2040"
    title: Robert W. Baldwin and Ronald L. Rivest, The RC5, RC5-CBC, RC5-CBC-Pad, and RC5-CTS algorithms, RFC 2040, October 1996
    locator: Sections 4 to 6 (key expansion, encryption and decryption) and Section 9 (test vectors in CBC mode)
  - url: "https://cacr.uwaterloo.ca/hac/about/chap7.pdf"
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996, Chapter 7
    locator: Section 7.7.2 (Algorithms 7.115 and 7.116, Note 7.117, Table 7.14 and Example 7.118, a test vector of RC5-32/12/16) and the notes on RC5 in Section 7.8
---

RC5 is a [block cipher](/block-cipher/) by Ronald Rivest with three parameters: the word size $w$ (16, 32 or 64 bits, so the block has $2w$ bits), the number of rounds $r$, and the key length $b$ in bytes. It has no S-boxes. Each half-round uses only XOR, addition modulo $2^w$, and a rotation whose amount comes from the data itself. The notation RC5-$w$/$r$/$b$ names an instance, and RC5-32/12/16 (a 64-bit block, 12 rounds, a 128-bit key) was the nominal choice. RC5 led to [RC6](/rc6/), an AES finalist.

**Notation.** $A$ and $B$ are $w$-bit words, read little-endian from bytes. $+$ and $-$ are modulo $2^w$, $\oplus$ is XOR, and $X \lll Y$ is the rotation of $X$ to the left by $Y \bmod w$ places, which uses only the low $\log_2 w$ bits of $Y$. $S[0 \ldots 2r+1]$ is the expanded key table, $u = w/8$ is the number of bytes in a word, and $n$ is the number of blocks.

## In plain words

RC5 cuts a block into two words. It first adds a secret word to each. Then, in each half round, it combines one word with the other by XOR, turns its bits around by a number of places that the other word decides, and adds a secret word. The two words take turns.

The idea is that the amount of turning is not fixed. It depends on the data, so an attacker cannot know in advance where each bit goes. This makes the cipher short and fast in software with very few operations. The secret words come from a key setup that stirs the key into a table built from two fixed constants.

## The problem

RC5-$w$/$r$/$b$ computes a permutation $E_K$ of $\{0,1\}^{2w}$ for each key $K$ of $b$ bytes, with $0 \le b \le 255$, and its inverse $D_K$. Messages longer than one block need a mode of operation; RFC 2040 defines CBC, CBC with padding, and ciphertext stealing. The security goal is that $E_K$ is a [pseudorandom permutation](/pseudorandom-permutation/), for a large enough $r$. There is no proof of this.

## The algorithm

```pseudo id=main
RC5-ENCRYPT(S, A, B)                        ▷ S[0 .. 2r + 1], A and B are w-bit words
L1  A ← A + S[0]
L2  B ← B + S[1]
L3  for i ← 1 to r do
L4      A ← ((A ⊕ B) ⋘ B) + S[2i]
L5      B ← ((B ⊕ A) ⋘ A) + S[2i + 1]
L6  return (A, B)

RC5-EXPAND-KEY(K, r)                        ▷ K has b bytes, c = max(1, ⌈b/u⌉)
L7  L[0 .. c − 1] ← the bytes of K, as little-endian words
L8  t ← 2r + 2
L9  for i ← 0 to t − 1 do S[i] ← P_w + i · Q_w
L10 A ← B ← i ← j ← 0
L11 repeat 3 · max(t, c) times
L12     A ← S[i] ← (S[i] + A + B) ⋘ 3
L13     B ← L[j] ← (L[j] + A + B) ⋘ (A + B)
L14     i ← (i + 1) mod t;  j ← (j + 1) mod c
L15 return S
```

The constants are $P_w = \mathrm{Odd}((e - 2) \cdot 2^w)$ and $Q_w = \mathrm{Odd}((\phi - 1) \cdot 2^w)$, where $e$ is the base of natural logarithms, $\phi$ is the golden ratio, and $\mathrm{Odd}(x)$ is the odd integer nearest to $x$. For $w = 32$, $P_{32}$ = B7E15163 and $Q_{32}$ = 9E3779B9. Rivest calls each iteration of the loop of line L3 a round; it holds two half-rounds.

Decryption undoes the steps in reverse order: for $i = r$ down to 1, $B \leftarrow ((B - S[2i+1]) \ggg A) \oplus A$ and $A \leftarrow ((A - S[2i]) \ggg B) \oplus B$; then $B \leftarrow B - S[1]$ and $A \leftarrow A - S[0]$.

The Python code for this page is for study only. It is not constant time, because the rotation amounts depend on the data, and some processors take longer for some amounts. Do not use it to protect real data. Use AES or ChaCha20 from a validated library such as OpenSSL instead.

## Example

Take Example 7.118 of the Handbook of Applied Cryptography, RC5-32/12/16: the key is the bytes 5269F149D41BA0152497574D7F153125 and the plaintext is the bytes 65C178B284D197CC. Read little-endian, the plaintext gives $A$ = B278C165 and $B$ = CC97D184. The key expansion gives $S[0]$ = 1320D0D9, $S[1]$ = EBC1BABC, $S[2]$ = 678E2B82 and $S[3]$ = 7EDDCD4F.

| step | $A$ | $B$ |
|---|---|---|
| plaintext | B278C165 | CC97D184 |
| lines L1 and L2 | C599923E | B8598C40 |
| round 1 | E54E4A00 | DBF5938F |
| round 2 | CA99BB63 | 2CE89959 |
| round 12 | 15E444EB | 249831DA |

In round 1, the rotation in line L4 is by $B \bmod 32 = 0$, since $B$ ends in the byte 40, and the rotation in line L5 is by $A \bmod 32 = 0$ for the same reason. So round 1 here only XORs and adds. Read as bytes, the result is EB44E415DA319824, the ciphertext of the handbook. The test file also checks the 25 vectors of RFC 2040, Section 9, which cover 0 to 16 rounds and keys of 1 to 16 bytes.

## Correctness

Decryption inverts encryption for every table $S$ and every $r$. Line L4 changes only $A$, and its rotation amount is $B$, which line L4 does not change. So, given the new $A$ and $B$, subtract $S[2i]$, rotate right by $B$, and XOR with $B$ to get the old $A$. Line L5 is the same with the roles of $A$ and $B$ exchanged. Lines L1 and L2 are additions, undone by subtractions. The [proof](proofs/correctness.md) gives each step.

## Complexity

A block costs $2r + 2$ additions, $2r$ XORs and $2r$ rotations, so $n$ blocks cost $\Theta(r \cdot n)$ time. The table $S$ has $2r + 2$ words, which is $\Theta(r)$ space. Key expansion costs $3 \max(2r + 2, c)$ iterations, each with two additions and two rotations, where $c$ is the number of key words.

For the nominal RC5-32/12/16, a block is 26 additions, 24 XORs and 24 rotations, and key setup is 78 iterations. RC5 has a 64-bit block for $w = 32$, so the [birthday bound](/birthday-attack/) limits the data under one key to far less than $2^{32}$ blocks.

## Properties

- **Data-dependent rotations.** The rotation is the only nonlinear step. It mixes the two words in a way that differs from block to block.
- **Weak rotations.** A rotation amount has only $\log_2 w$ bits, 5 for $w = 32$, and the other bits of the word do not affect it. The example shows that an amount can be 0. Differential and linear attacks exploit pairs whose rotation amounts stay fixed over several rounds.
- **Parameters.** One description covers many instances, from RC5-16 with a 32-bit block to RC5-64 with a 128-bit block.
- **Avalanche.** For RC5-32/12/16 with the key of the example, a one-bit change of the plaintext changes on average 31.85 of the 64 ciphertext bits over 2000 random trials. The ideal value is 32. See [avalanche effect](/avalanche-effect/).
- **No proof.** There is no proof of security. Confidence depends on the number of rounds.

## Variants and improvements

- **Number of rounds.** The handbook gives 12 rounds for RC5-32 and 16 for RC5-64. Its notes (Section 7.8) report that the [differential cryptanalysis](/differential-cryptanalysis/) of Kaliski and Yin needs $2^{45}$ chosen-plaintext pairs for 9 rounds and $2^{62}$ for 12 rounds of RC5-32, and that their [linear cryptanalysis](/linear-cryptanalysis/) needs $2^{37}$, $2^{47}$ and $2^{57}$ known plaintexts for 4, 5 and 6 rounds. Knudsen and Meier improved the differential attacks by a factor of up to 512 and found weak keys for them. So 12 rounds leave a small margin.
- **[RC6](/rc6/).** Rivest, Robshaw, Sidney and Yin built RC6 on RC5 for the AES competition. It uses four words, a multiplication to compute rotation amounts from all bits of a word, and fixed rotations.
- **Modes.** RFC 2040 defines RC5-CBC, RC5-CBC-Pad and RC5-CTS (ciphertext stealing).

## When to use it

Do not use RC5 in new designs. It has a 64-bit block in its common form, its data-dependent rotations are hard to make constant time on some processors, and its security margin with 12 rounds is small. Use AES-GCM or ChaCha20-Poly1305 instead. RC5 is still a good example for the study of data-dependent rotations and of parameterized ciphers.

## Pitfalls

- **Rotation by the low bits.** $X \lll Y$ uses $Y \bmod w$. A shift by the full $Y$, or a shift by $w$ in a language where that is undefined, gives wrong results.
- **Byte order.** Words are little-endian. A big-endian load gives a cipher that decrypts what it encrypts but fails the test vectors.
- **Short keys.** A key of 0 bytes still gives $c = 1$ word of zeros. A key whose length is not a multiple of $u$ fills the last word with zero bytes at the top.
- **The key expansion loop.** Line L13 uses the new $A$ from line L12, and both lines update their table in place. Swapping the order of the updates gives a different key table.
- **Few rounds.** The parameter $r$ can be as small as 0, which is only a key addition. RFC 2040 includes such vectors for testing, not for use.

## Implementations

## History

Rivest designed RC5 in 1994 and presented it at the Fast Software Encryption workshop in Leuven in December of that year. The name stands for Rivest Cipher 5. RSA Data Security held a patent on it. Baldwin and Rivest published RFC 2040 in 1996, with modes of operation and test vectors. RSA Laboratories posed key-search challenges for RC5-32/12 with short keys, and the distributed.net project found the 56-bit and 64-bit keys by [exhaustive search](/exhaustive-key-search/). In 1998 Rivest and coauthors submitted RC6, a successor to RC5, to the AES competition.

## References
