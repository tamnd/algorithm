---
tag: F2V5M9
kind: algorithm
slug: skipjack
name: Skipjack
area: cryptography/symmetric-ciphers
level: advanced
summary: The NSA block cipher of the Clipper chip, made public in 1998. It has a 64-bit block, an 80-bit key and 32 steps of two rules built on a small byte Feistel permutation G.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of 8-byte blocks}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1998
  people: [National Security Agency]
  note: The NSA designed Skipjack for the Clipper chip and the Escrowed Encryption Standard of 1994 and kept it secret. NIST published the specification in 1998.
prereqs: [block-cipher, feistel-network]
see_also: [data-encryption-standard, advanced-encryption-standard, differential-cryptanalysis, exhaustive-key-search, key-schedule, s-box, tea]
sources:
  - url: "https://csrc.nist.gov/csrc/media/projects/cryptographic-algorithm-validation-program/documents/skipjack/skipjack.pdf"
    title: SKIPJACK and KEA Algorithm Specifications, Version 2.0, 29 May 1998
    locator: Section II.B.4 (the rules A and B and their order), Section II.B.7 (the F-table) and Annex III.A (the codebook test vector with all 32 intermediate steps)
  - paper: doi:10.1007/3-540-48910-X_2
    title: Eli Biham, Alex Biryukov and Adi Shamir, Cryptanalysis of Skipjack reduced to 31 rounds using impossible differentials, Eurocrypt 1999, LNCS 1592, Springer, 1999
    locator: pp. 12-23
  - paper: doi:10.1007/s00145-005-0129-3
    title: Eli Biham, Alex Biryukov and Adi Shamir, Cryptanalysis of Skipjack reduced to 31 rounds using impossible differentials, Journal of Cryptology 18(4), 2005
    locator: the journal version of the attack on 31 of the 32 rounds
---

Skipjack is a [block cipher](/block-cipher/) on 64-bit blocks with an 80-bit key, designed by the NSA. It was the cipher in the Clipper chip and the Fortezza card, and it was secret until NIST published the specification in 1998. The block is four 16-bit words. Each of 32 steps applies one of two rules, A or B, and each rule puts one word through G, a small four-round [Feistel network](/feistel-network/) on two bytes. The key schedule is simple: step $k$ takes four bytes of the key in turn.

**Notation.** $w_1, w_2, w_3, w_4$ are 16-bit words, read big-endian from the block. The key, or cryptovariable, is ten bytes $cv_0, \ldots, cv_9$. $\oplus$ is XOR, and in lines L3 and L5 the step number $k + 1$ is a 16-bit word. $F$ is a fixed permutation of the bytes, given as a table in the specification. $g_1 \| g_2$ is the 16-bit word with high byte $g_1$ and low byte $g_2$. $n$ is the number of blocks.

## In plain words

Skipjack cuts a block into four parts. In each of 32 steps, the first part goes through a small scrambler that uses four bytes of the key. The result takes the place of one part and is also mixed with another part. Then the parts move one place along, and the step number is mixed in as well.

There are two kinds of step. They differ only in which part gets the mix and which part moves to the front. The cipher does eight steps of the first kind, eight of the second kind, and then the same again. The scrambler itself is four rounds of byte lookups in a fixed table of 256 entries.

## The problem

Skipjack computes a permutation $E_K$ of $\{0,1\}^{64}$ for each key $K$ of 80 bits, and its inverse $D_K$. Messages longer than one block need a mode of operation, such as [CBC](/cbc-mode/). The goal was that $E_K$ behaves like a [pseudorandom permutation](/pseudorandom-permutation/) for a user who does not know the key. Today the goal fails for size alone: a search over $2^{80}$ keys is near the limit of large computing efforts, and a 64-bit block repeats after about $2^{32}$ blocks under the [birthday bound](/birthday-attack/).

## The algorithm

```pseudo id=main
SKIPJACK-ENCRYPT(cv, w₁, w₂, w₃, w₄)
L1  for k ← 0 to 31 do                         ▷ step k + 1
L2      if k < 8 or 16 ≤ k < 24 then             ▷ rule A
L3          (w₁, w₂, w₃, w₄) ← (G_k(w₁) ⊕ w₄ ⊕ (k + 1), G_k(w₁), w₂, w₃)
L4      else                                    ▷ rule B
L5          (w₁, w₂, w₃, w₄) ← (w₄, G_k(w₁), w₁ ⊕ w₂ ⊕ (k + 1), w₃)
L6  return (w₁, w₂, w₃, w₄)

G_k(g₁ ‖ g₂)
L7  g₃ ← F[g₂ ⊕ cv_(4k mod 10)] ⊕ g₁
L8  g₄ ← F[g₃ ⊕ cv_((4k + 1) mod 10)] ⊕ g₂
L9  g₅ ← F[g₄ ⊕ cv_((4k + 2) mod 10)] ⊕ g₃
L10 g₆ ← F[g₅ ⊕ cv_((4k + 3) mod 10)] ⊕ g₄
L11 return g₅ ‖ g₆
```

In line L3 and line L5, all values on the right side are the old values. Rule A is a step of an unbalanced Feistel network: the new $w_1$ is $w_4$ masked by a function of $w_1$, and $w_1$ itself survives in changed form as $G_k(w_1)$. Rule B uses the old $w_1$ twice: once as the input of $G_k$ and once to mask $w_2$. The key schedule is lines L7 to L10: step $k + 1$ takes the four key bytes after the ones of step $k$, with wrap-around, so the key repeats every five steps.

Decryption runs the steps from $k = 31$ down to 0. With $x = G_k^{-1}(w_2)$, the inverse of rule A is $(w_1, w_2, w_3, w_4) \leftarrow (x, w_3, w_4, w_1 \oplus w_2 \oplus (k + 1))$, and the inverse of rule B is $(w_1, w_2, w_3, w_4) \leftarrow (x, x \oplus w_3 \oplus (k + 1), w_4, w_1)$. $G_k^{-1}$ runs lines L7 to L10 backwards, with the key bytes in reverse order.

The Python code for this page is for study only. It is not constant time, because the table $F$ is indexed by bytes that depend on the key. Do not use it to protect real data. Use AES from a validated library such as OpenSSL instead.

## Example

Take the test vector of Annex III.A of the specification. The key is 00998877665544332211, so $cv_0$ = 00, $cv_1$ = 99, $cv_2$ = 88 and $cv_3$ = 77. The plaintext is 33221100DDCCBBAA, so $w_1$ = 3322, $w_2$ = 1100, $w_3$ = DDCC and $w_4$ = BBAA.

In step 1, $G_0(3322)$ starts with $g_1$ = 33 and $g_2$ = 22. Lines L7 to L10 give $g_3$ = 31, $g_4$ = 72, $g_5$ = 0B and $g_6$ = AF, so $G_0(3322)$ = 0BAF. Rule A then gives the new $w_1$ = 0BAF ⊕ BBAA ⊕ 0001 = B004 and the new $w_2$ = 0BAF.

| after step | rule | $w_1$ | $w_2$ | $w_3$ | $w_4$ |
|---|---|---|---|---|---|
| 0 (plaintext) | | 3322 | 1100 | DDCC | BBAA |
| 1 | A | B004 | 0BAF | 1100 | DDCC |
| 2 | A | E688 | 3B46 | 0BAF | 1100 |
| 8 | A | D79B | 5599 | BE50 | DD90 |
| 9 | B | DD90 | 1E0B | 820B | BE50 |
| 16 | B | D7F8 | 8990 | 5397 | 9883 |
| 24 | A | 65A7 | DEAA | 1115 | 45C0 |
| 32 | B | 2587 | CAE2 | 7A12 | D300 |

In step 9, rule B moves $w_4$ = DD90 to the front and sets $w_3$ = D79B ⊕ 5599 ⊕ 0009 = 820B. The last row, read as bytes, is the ciphertext 2587CAE27A12D300 of the specification. The annex lists the state after every one of the 32 steps, and the test file checks all of them.

## Correctness

Each step is a bijection on the four words, so encryption is a bijection, and decryption undoes the steps in reverse order. $G_k$ is a Feistel network on bytes, so it is invertible whatever $F$ and the key are. Given the output of rule A or rule B, the second word is $G_k(w_1)$, which gives back $w_1$; then each other old word is either copied or found by an XOR with known values. The [proof](proofs/correctness.md) gives the details.

## Complexity

A block costs 32 steps. Each step costs one $G_k$, which is 4 table lookups and 8 byte XORs, and one or two word XORs. So $n$ blocks cost $\Theta(n)$ time. The cipher needs the 256-byte table $F$ and the 10 key bytes, with no expanded key, which is $\Theta(1)$ extra space.

Biham, Biryukov and Shamir found a differential that holds with probability zero over 24 of the 32 rounds, and used it to break Skipjack reduced to 31 rounds faster than exhaustive search (Eurocrypt 1999, pp. 12-23). No attack on all 32 rounds that is faster than a search of $2^{80}$ keys appears in these sources.

## Properties

- **Two rules.** Rule A mixes $G_k(w_1)$ into $w_4$ and moves the result to the front. Rule B mixes the old $w_1$ into $w_2$ and moves the result to the third place. The change from one rule to the other after each 8 steps sends differences along different paths.
- **No real key schedule.** Step $k + 1$ uses key bytes $4k$ to $4k + 3$ modulo 10. This is fast and needs no memory, but the same bytes come back every five steps.
- **A step counter.** XOR with the step number makes the steps different from each other, even where the key bytes repeat.
- **Avalanche.** With the key of the example, a one-bit change of the plaintext changes on average 31.92 of the 64 ciphertext bits over 2000 random trials. The ideal value is 32.
- **Small sizes.** The 80-bit key and the 64-bit block are both too small for new systems.

## Variants and improvements

- **Reduced rounds.** The attacks of Biham, Biryukov and Shamir work on 31 rounds and on other reduced versions. The 24-round impossible differential comes from the way the rules A and B fit together, and not from the table $F$.
- **Other old 64-bit ciphers.** [DES](/data-encryption-standard/) and [Triple DES](/triple-des/) are the standard ciphers of the same era. [TEA](/tea/) is another cipher with a very simple key schedule.

## When to use it

Do not use Skipjack in new systems. Its key is 80 bits and its block is 64 bits, so key search and birthday attacks are both too close to practical limits. Use [AES](/advanced-encryption-standard/). Skipjack is worth study as a design from a closed government process that later became public, and as the cipher that led to the impossible differential technique.

## Pitfalls

- **Old values.** In line L5, rule B uses the old $w_1$ both in $G_k$ and in the XOR with $w_2$. An implementation that updates $w_1$ first gets a different cipher.
- **The counter.** The counter starts at 1, not at 0, and it is a 16-bit word XORed into the full word.
- **Key bytes.** $G_k$ takes the key bytes in order $cv_{4k}, \ldots, cv_{4k+3}$ modulo 10, starting from the low byte $g_2$. Check the first step against the annex.
- **Byte order.** Words are big-endian, and $g_1$ is the high byte of the input of $G_k$.
- **Timing.** Table lookups at secret indices can leak through the cache.

## Implementations

## History

In 1993 the United States government announced the Clipper chip, a device for voice encryption that gave a copy of each key to escrow agents. Its cipher was Skipjack, and it was secret: the Escrowed Encryption Standard, FIPS 185 of 1994, did not include it. The NSA also used Skipjack in the Fortezza card. In 1998 the NSA declassified Skipjack, and NIST published the specification of Skipjack and of the key exchange KEA. Biham, Biryukov and Shamir published their attack on 31 rounds the next year.

## References
