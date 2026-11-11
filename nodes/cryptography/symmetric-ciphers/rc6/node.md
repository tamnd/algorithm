---
tag: FKPS33
kind: algorithm
slug: rc6
name: RC6
area: cryptography/symmetric-ciphers
level: advanced
summary: An AES finalist by Rivest, Robshaw, Sidney and Yin (1998), built on RC5. It uses four 32-bit words, 20 rounds, and rotation amounts computed by the multiplication x(2x + 1).
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of blocks, r: the number of rounds}
  time: {worst: Θ(r·n), average: Θ(r·n), best: Θ(r·n)}
  space: {extra: Θ(r)}
properties: {deterministic: true}
history:
  year: 1998
  people: [Ronald L. Rivest, Matthew J. B. Robshaw, Ray Sidney, Yiqun Lisa Yin]
  note: Rivest and three colleagues from RSA Laboratories submitted RC6 to the AES competition in 1998. It was one of the five finalists, and NIST chose Rijndael in 2000.
prereqs: [rc5, block-cipher, bitwise-operations]
see_also: [advanced-encryption-standard, serpent, twofish, rc5, differential-cryptanalysis, linear-cryptanalysis, key-schedule]
sources:
  - url: "https://people.csail.mit.edu/rivest/pubs/RRSY98.pdf"
    title: Ronald L. Rivest, Matthew J. B. Robshaw, Ray Sidney and Yiqun Lisa Yin, The RC6 block cipher, version 1.1, August 20, 1998
    locator: Section 2 (details of RC6, the key schedule, encryption and decryption), the design rationale with the function f(x) = x(2x + 1), Section 6 (security), and the appendix with test vectors for RC6-32/20/b
  - paper: doi:10.6028/jres.106.023
    title: James Nechvatal and others, Report on the development of the Advanced Encryption Standard (AES), Journal of Research of the National Institute of Standards and Technology 106(3), 2001
    locator: the evaluation of the five finalists, including RC6, and the reasons for the choice of Rijndael
---

RC6 is a [block cipher](/block-cipher/) on 128-bit blocks with keys of 128, 192 or 256 bits, by Ronald Rivest, Matt Robshaw, Ray Sidney and Yiqun Lisa Yin. It was one of the five finalists of the AES competition. It keeps the half-round of [RC5](/rc5/), a rotation by an amount that depends on the data, but works on four 32-bit words and computes each rotation amount from all bits of a word with the multiplication $x(2x + 1)$. RC6-$w$/$r$/$b$ names an instance with word size $w$, $r$ rounds and a key of $b$ bytes; the AES version is RC6-32/20/$b$.

**Notation.** $A, B, C, D$ are $w$-bit words, read little-endian from bytes, so the first byte of a block is the low byte of $A$. $+$, $-$ and $\times$ are modulo $2^w$, $\oplus$ is XOR, and $X \lll Y$ is rotation to the left by $Y \bmod w$ places. $\lg w = \log_2 w$, which is 5 for $w = 32$. $S[0 \ldots 2r+3]$ is the expanded key table, and $n$ is the number of blocks.

## In plain words

RC6 cuts a block into four words and works on them in pairs. In each round, it takes the second and fourth words and puts each through a small mixing function: multiply the word by one more than twice itself, and turn the result. The top few bits of each result decide how far to turn the first and third words, after an XOR with the other result. Then it adds a secret word to each, and all four words move one place along.

RC5 used only the low bits of a word to decide the amount of turning, which helped attackers. RC6 uses the multiplication so that every bit of the word affects the amount. This gives more mixing in each round, so RC6 needs fewer rounds for the same safety.

## The problem

RC6-32/20/$b$ computes a permutation $E_K$ of $\{0,1\}^{128}$ for each key $K$ of $b$ bytes, and its inverse $D_K$. The AES call asked for keys of 16, 24 and 32 bytes, and RC6 accepts any length up to 255 bytes. Messages longer than one block need a mode of operation such as [CBC](/cbc-mode/) or [CTR](/ctr-mode/). The security goal is that $E_K$ is a [pseudorandom permutation](/pseudorandom-permutation/). There is no proof of this.

## The algorithm

```pseudo id=main
RC6-ENCRYPT(S, A, B, C, D)                  ▷ S[0 .. 2r + 3]
L1  B ← B + S[0]
L2  D ← D + S[1]
L3  for i ← 1 to r do
L4      t ← (B × (2B + 1)) ⋘ lg w
L5      u ← (D × (2D + 1)) ⋘ lg w
L6      A ← ((A ⊕ t) ⋘ u) + S[2i]
L7      C ← ((C ⊕ u) ⋘ t) + S[2i + 1]
L8      (A, B, C, D) ← (B, C, D, A)
L9  A ← A + S[2r + 2]
L10 C ← C + S[2r + 3]
L11 return (A, B, C, D)

RC6-EXPAND-KEY(K, r)                        ▷ L[0 .. c − 1] are the key bytes as little-endian words
L12 for i ← 0 to 2r + 3 do S[i] ← P_w + i · Q_w
L13 A ← B ← i ← j ← 0
L14 repeat 3 · max(c, 2r + 4) times
L15     A ← S[i] ← (S[i] + A + B) ⋘ 3;  B ← L[j] ← (L[j] + A + B) ⋘ (A + B)
L16     i ← (i + 1) mod (2r + 4);  j ← (j + 1) mod c
L17 return S
```

The key schedule is the one of RC5 with $2r + 4$ table words in place of $2r + 2$, and with the same constants $P_{32}$ = B7E15163 and $Q_{32}$ = 9E3779B9. Lines L6 and L7 are two RC5 half-rounds that run side by side, and each takes its rotation amount from the other pair. Line L8 rotates the four words, so each word plays each role in turn.

Decryption undoes the steps in reverse order: $C \leftarrow C - S[2r+3]$ and $A \leftarrow A - S[2r+2]$; then for $i = r$ down to 1, $(A, B, C, D) \leftarrow (D, A, B, C)$, compute $u$ from $D$ and $t$ from $B$, and set $C \leftarrow ((C - S[2i+1]) \ggg t) \oplus u$ and $A \leftarrow ((A - S[2i]) \ggg u) \oplus t$; finally $D \leftarrow D - S[1]$ and $B \leftarrow B - S[0]$.

The Python code for this page is for study only. It is not constant time, because the rotation amounts depend on the data. Do not use it to protect real data. Use AES from a validated library such as OpenSSL instead.

## Example

Take the second test vector of the RC6 paper for a 128-bit key: the key is the bytes 0123456789ABCDEF0112233445566778 and the plaintext is the bytes 02132435465768798A9BACBDCEDFE0F1. Read little-endian, the plaintext gives $A$ = 35241302, $B$ = 79685746, $C$ = BDAC9B8A and $D$ = F1E0DFCE. The key schedule gives $S[0]$ = 05479D38 and $S[1]$ = E4A3E582.

| step | $A$ | $B$ | $C$ | $D$ |
|---|---|---|---|---|
| plaintext | 35241302 | 79685746 | BDAC9B8A | F1E0DFCE |
| lines L1 and L2 | 35241302 | 7EAFF47E | BDAC9B8A | D684C550 |
| round 1 | 7EAFF47E | A17A48D4 | D684C550 | FDBC336A |
| round 2 | A17A48D4 | FD35085F | FDBC336A | 8D81F7B9 |
| round 20 | 3E3439E9 | 23C61547 | F105F04E | 183FA47E |
| lines L9 and L10 | 2F194E52 | 23C61547 | 36F6511F | 183FA47E |

In round 1, line L4 gives $t$ = 471A10DD and line L5 gives $u$ = 75A6EA0F, so $A$ is rotated by $u \bmod 32 = 15$ places and $C$ by $t \bmod 32 = 29$ places. After line L8, the old $B$ is the new $A$. Read as bytes, the result is 524E192F4715C6231F51F6367EA43F18, the ciphertext in the paper. The test file checks the six vectors of the paper, two for each key length, in both directions.

## Correctness

Decryption inverts encryption for every table $S$. In lines L4 and L5, $t$ and $u$ depend only on $B$ and $D$, and lines L6 and L7 do not change $B$ or $D$. So, after undoing the rotation of line L8, decryption can compute the same $t$ and $u$, and then undo lines L6 and L7 with a subtraction, a rotation to the right and an XOR. The function $x \mapsto x(2x + 1)$ need not be inverted. The [proof](proofs/correctness.md) gives each step.

## Complexity

A block costs $r$ rounds, and each round costs 2 multiplications, 2 rotations by $\lg w$, 2 data-dependent rotations, 2 XORs and about 6 additions, so $n$ blocks cost $\Theta(r \cdot n)$ time. The table $S$ has $2r + 4$ words, 44 for the AES version, which is $\Theta(r)$ space. Key setup costs $3 \max(c, 2r + 4)$ iterations, 132 for $r = 20$ and a key of up to 44 words.

The designers' security estimates are in Section 6 of the paper. They conjecture that the best attack on RC6-32/20 is exhaustive search for the key, or for the table $S$ when the key is very long. For a reduced version with 8 rounds, they estimate that a differential attack needs about $2^{56}$ chosen plaintext pairs and a linear attack about $2^{47}$ known plaintexts. For 18 rounds, the best differential characteristic they found has probability about $2^{-238}$, which needs more pairs than there are plaintexts.

## Properties

- **Rotation amounts from all bits.** The function $f(x) = x(2x + 1) \bmod 2^w$ is one to one, and its high bits depend on all bits of $x$. Line L4 rotates them into the low $\lg w$ bits, which set the rotation amount. This fixes the weakness of RC5, where only the low bits of a word set the amount.
- **Fixed rotation by $\lg w$.** The designers state that this fixed rotation, by 5 places for $w = 32$, plays a simple but important role in making both differential and linear cryptanalysis harder.
- **Whitening.** Lines L1, L2, L9 and L10 hide the inputs of the first round and the outputs of the last round, so the plaintext and the ciphertext do not give them directly.
- **Avalanche.** With the key of the example, a one-bit change of the plaintext changes on average 63.94 of the 128 ciphertext bits over 1000 random trials. The ideal value is 64.
- **No proof.** As with the other AES finalists, there is no proof of security.

## Variants and improvements

- **Parameters.** As with RC5, one description covers RC6-$w$/$r$/$b$ for other word sizes and numbers of rounds. Only RC6-32/20 was analyzed in depth for the AES.
- **[RC5](/rc5/).** RC6 is RC5 with four words, the function $f$ and whitening of all four words.
- **Other AES finalists.** [AES](/advanced-encryption-standard/) (Rijndael), [Serpent](/serpent/) and [Twofish](/twofish/) are the others in this collection.

## When to use it

Use AES instead. RC6 is a sound design, but it has less analysis and support than AES, and its data-dependent rotations and multiplications are hard to make constant time on small processors. RC6 is a good example of how a design can fix a known weakness of its predecessor.

## Pitfalls

- **Multiplication modulo $2^w$.** Line L4 needs the low $w$ bits of the product. In a language with arbitrary integers, mask the result.
- **The rotation of line L8.** The new $A$ is the old $B$, not the old $D$. A rotation in the wrong direction gives a different cipher.
- **The rotation amount.** Line L6 rotates by $u$, which comes from $D$, and line L7 rotates by $t$, which comes from $B$. Exchanging them still gives a permutation, so only the test vectors find the error.
- **Byte order.** Words are little-endian, as in RC5.
- **Timing.** Data-dependent rotations and multiplications can take a variable time on some processors.

## Implementations

## History

Rivest designed RC5 in 1994. When NIST asked for AES candidates, Rivest and Robshaw, Sidney and Yin of RSA Laboratories built RC6 on it. They changed to four 32-bit words, because a 128-bit block with two words would need 64-bit operations, and added the multiplication that the processors of the time did fast. They submitted RC6 in 1998. In 1999 NIST chose it as one of the five finalists, with MARS, Rijndael, Serpent and Twofish, and in 2000 NIST chose Rijndael as the AES.

## References
