---
tag: M2H1VD
kind: algorithm
slug: idea
name: IDEA
aliases:
- International Data Encryption Algorithm
area: cryptography/symmetric-ciphers
level: advanced
summary: A 64-bit block cipher with a 128-bit key by Lai and Massey (1991). It mixes XOR, addition modulo 2^16 and multiplication modulo 2^16 + 1 in 8.5 rounds. PGP 2 used it.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {b: the number of 8-byte blocks}
  time: {worst: Θ(b), average: Θ(b), best: Θ(b)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1991
  people: [Xuejia Lai, James L. Massey]
  note: Lai and Massey proposed PES in 1990 and the improved IPES in 1991, after differential cryptanalysis appeared. IPES became IDEA in 1992, and PGP 2 made it widely used.
prereqs: [block-cipher, modular-multiplication, key-schedule]
see_also: [data-encryption-standard, blowfish, advanced-encryption-standard, differential-cryptanalysis, birthday-attack, confusion-and-diffusion, feistel-network]
sources:
  - paper: doi:10.1007/3-540-46877-3_35
    title: Xuejia Lai and James L. Massey, A proposal for a new block encryption standard, Advances in Cryptology (EUROCRYPT 1990), LNCS 473, Springer, 1991
    locator: the cipher PES, the three group operations on 16-bit words and the MA structure that IDEA keeps
  - paper: doi:10.1007/3-540-46416-6_2
    title: Xuejia Lai, James L. Massey and Sean Murphy, Markov ciphers and differential cryptanalysis, Advances in Cryptology (EUROCRYPT 1991), LNCS 547, Springer, 1991
    locator: the differential attack on PES and the improved cipher IPES, which is IDEA
  - url: "https://cacr.uwaterloo.ca/hac/about/chap7.pdf"
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996, Chapter 7
    locator: Section 7.6, Algorithm 7.101 (IDEA encryption), Algorithm 7.102 (the key schedule), Note 7.103 with Table 7.11 (decryption subkeys), Example 7.106 with Tables 7.12 and 7.13 (test vectors)
  - paper: doi:10.1007/3-540-48329-2_20
    title: Joan Daemen, René Govaerts and Joos Vandewalle, Weak keys for IDEA, Advances in Cryptology (CRYPTO 1993), LNCS 773, Springer, 1994
    locator: the classes of weak keys found from the simple key schedule
---

IDEA is a [block cipher](/block-cipher/) on 64-bit blocks with a 128-bit key, by Xuejia Lai and James Massey. It has no S-boxes and is not a [Feistel network](/feistel-network/). It mixes three group operations on 16-bit words: XOR, addition modulo $2^{16}$, and multiplication modulo $2^{16} + 1$. No two of these operations obey a distributive law or an associative law with each other, so the cipher is far from linear in any one of them. IDEA has 8 rounds and a final half round. PGP 2 used it in the 1990s, but its 64-bit block makes it unfit for new designs.

**Notation.** A block is four 16-bit words $X_1, X_2, X_3, X_4$, read big-endian. $\oplus$ is XOR, $\boxplus$ is addition modulo $2^{16}$, and $\odot$ is multiplication modulo $2^{16} + 1$, where the word 0 stands for $2^{16}$. The key schedule gives 52 subkeys $K_1, \ldots, K_{52}$ of 16 bits, 6 for each round and 4 for the output step. $K$ is the key and $b$ is the number of blocks.

## In plain words

IDEA cuts a block into four small numbers. Each round mixes a key number into each of them, two by addition and two by a special multiplication. Then a small mixing step takes two combinations of the four numbers, scrambles them with two more key numbers, and adds the result back into all four. The two middle numbers then change places. After eight rounds, a last key step finishes the block.

The design idea is to mix kinds of arithmetic that do not fit together. Addition and multiplication of this kind and XOR each break the patterns of the others. This gives confusion without any lookup tables. Decryption uses the same steps with inverted keys.

## The problem

IDEA computes a permutation $E_K$ of $\{0,1\}^{64}$ for each 128-bit key $K$, and its inverse $D_K$. Messages longer than one block need a mode of operation such as [CBC](/cbc-mode/) or [CTR](/ctr-mode/). The security goal is that $E_K$ is a [pseudorandom permutation](/pseudorandom-permutation/). There is no proof of this.

## The algorithm

```pseudo id=main
IDEA-ENCRYPT(K, X)                          ▷ K = 52 subkeys, X = (X1, X2, X3, X4)
L1  for r ← 1 to 8 do
L2      (k1, ..., k6) ← K[6r − 5 .. 6r]
L3      a ← X1 ⊙ k1;  b ← X2 ⊞ k2;  c ← X3 ⊞ k3;  d ← X4 ⊙ k4
L4      t0 ← k5 ⊙ (a ⊕ c)
L5      t1 ← k6 ⊙ (t0 ⊞ (b ⊕ d))
L6      t2 ← t0 ⊞ t1
L7      X1 ← a ⊕ t1;  X4 ← d ⊕ t2;  X2 ← c ⊕ t1;  X3 ← b ⊕ t2
L8  return (X1 ⊙ K49, X3 ⊞ K50, X2 ⊞ K51, X4 ⊙ K52)

A ⊙ B
L9  return the product of A and B modulo 2^16 + 1, with 0 read as 2^16 and the result 2^16 written as 0

KEY-SCHEDULE(K)                             ▷ K is a 128-bit key
L10 while fewer than 52 subkeys are made do
L11     append the 8 words of K, from the most significant
L12     K ← K rotated left by 25 places
L13 return the first 52 subkeys
```

Lines L4 to L6 are the MA step (multiply and add). Line L7 adds $t_1$ and $t_2$ into all four words and also exchanges the middle words. Line L8 undoes that exchange for the output. Since $2^{16} + 1 = 65537$ is prime, the nonzero residues form a group of order $2^{16}$ under multiplication, and line L9 maps it one to one onto the 16-bit words. So $\odot$ with a fixed key word is a permutation.

Decryption runs IDEA-ENCRYPT with other subkeys (HAC, Note 7.103 and Table 7.11). Decryption round $r$ uses the inverses $k_1^{-1}$ and $k_4^{-1}$ for $\odot$ and the negatives $-k_2$, $-k_3$ for $\boxplus$ of encryption round $10 - r$, where round 9 means the output step, with $-k_2$ and $-k_3$ exchanged for $r = 2, \ldots, 8$. Its $k_5$ and $k_6$ are those of encryption round $9 - r$.

The Python code for this page is for study only. It is not constant time, because Python integers do not have a fixed run time, and the multiplication modulo $2^{16} + 1$ needs care to be constant time in other languages. Do not use it to protect real data. Use AES or ChaCha20 from a validated library such as OpenSSL instead.

## Example

Take Example 7.106 of the Handbook of Applied Cryptography: the key is the words 0001, 0002, ..., 0008 and the plaintext is 0000 0001 0002 0003. Line L11 first gives the 8 key words as $K_1, \ldots, K_8$, and after one rotation by 25 places, $K_9$ = 0400 and $K_{10}$ = 0600. The output step uses $K_{49}, \ldots, K_{52}$ = 0080, 00C0, 0100, 0140.

Round 1 has the subkeys 0001, ..., 0006. Line L3 gives $a$ = 0000 (the word 0 times 1 is $2^{16}$, written 0), $b$ = 0003, $c$ = 0005 and $d$ = 000C. Then $t_0$ = 0005 $\odot$ 0005 = 0019, $t_1$ = 0006 $\odot$ (0019 $\boxplus$ 000F) = 00F0 and $t_2$ = 0109.

| after | $X_1$ | $X_2$ | $X_3$ | $X_4$ |
|---|---|---|---|---|
| round 1 | 00F0 | 00F5 | 010A | 0105 |
| round 2 | 222F | 21B5 | F45E | E959 |
| round 4 | 57DF | AC58 | C65B | BA4D |
| round 8 | 0A24 | 0098 | EC6B | 4925 |
| line L8 | 11FB | ED2B | 0198 | 6DE5 |

The ciphertext 11FB ED2B 0198 6DE5 is the value in the handbook. The test file checks it in both directions, the subkeys of Table 7.12, the output of round 1, and the first decryption subkeys of Table 7.13.

## Correctness

Decryption inverts encryption for every key. Split a round into the key step of line L3 and the MA step with the exchange of lines L4 to L7. The MA step without the exchange is its own inverse: it XORs $t_1$ into $X_1$ and $X_3$ and $t_2$ into $X_2$ and $X_4$, so $X_1 \oplus X_3$ and $X_2 \oplus X_4$ do not change, and those are the only inputs of $t_0$, $t_1$ and $t_2$. The key step is inverted by the inverse and negative subkeys. The [proof](proofs/correctness.md) moves the exchanges through the key steps, which is why the decryption subkeys $-k_2$ and $-k_3$ change places in the middle rounds.

## Complexity

A block costs 8 rounds plus the output step: 34 multiplications modulo $2^{16} + 1$, 34 additions and 48 XORs. So $b$ blocks cost $\Theta(b)$ time, and the 52 subkeys take $\Theta(1)$ space. Encryption key setup costs only 6 rotations. Decryption key setup needs 18 inverses modulo 65537, each by the [extended Euclidean algorithm](/extended-euclidean-algorithm/) or by [modular exponentiation](/modular-exponentiation/).

The data limit is the block size. By the [birthday bound](/birthday-attack/), ciphertext blocks of CBC collide after about $2^{32}$ blocks under one key. Daemen, Govaerts and Vandewalle (1993) found classes of weak keys, caused by the simple linear key schedule. The handbook (Section 7.8) describes the largest: $2^{51}$ keys, for which membership can be tested with two encryptions and the key then found with little work. A random key is in this class with probability $2^{51}/2^{128} = 2^{-77}$. Note 7.107 of the handbook states that, apart from weak keys, no published attack on the full 8 rounds was better than exhaustive search at the time.

## Properties

- **No S-boxes.** All nonlinearity comes from mixing three incompatible group operations, so there are no tables to look up.
- **Multiplication.** $\odot$ is the operation that gives most of the nonlinearity. The word 0 stands for $2^{16}$, which is $-1$ modulo 65537.
- **MA structure.** Lines L4 to L6 spread each of the four input words to all four output words in one round.
- **Same structure for decryption.** Like a Feistel network, IDEA decrypts with the same rounds and other subkeys, but the key step needs inverses, not only the reversed order.
- **Avalanche.** With the key of the example, a one-bit change of the plaintext changes on average 32.04 of the 64 ciphertext bits over 2000 random trials. The ideal value is 32. See [avalanche effect](/avalanche-effect/).

## Variants and improvements

- **PES.** The first version of 1990. IDEA (first called IPES) changed the order of operations to resist [differential cryptanalysis](/differential-cryptanalysis/), which Lai, Massey and Murphy found effective against PES.
- **The Lai-Massey scheme.** The structure of lines L4 to L7, where a function of the difference of two halves is added to both, is now called the Lai-Massey scheme. Later ciphers such as FOX use it.
- **Modern ciphers.** For new systems, use [AES](/advanced-encryption-standard/), which has a 128-bit block.

## When to use it

Do not use IDEA in new designs. Its 64-bit block limits the safe data under one key, it has weak keys, and fast multiplication modulo $2^{16} + 1$ is hard to make constant time. Use IDEA only to read old data, for example messages from PGP 2. Use AES-GCM or ChaCha20-Poly1305 instead.

## Pitfalls

- **The word 0.** In $\odot$, the word 0 means $2^{16}$, not zero. Treating it as zero makes $\odot$ not invertible and fails the test vectors.
- **The exchange of the middle words.** Line L7 exchanges $X_2$ and $X_3$, and line L8 undoes it. An extra or a missing exchange gives a different cipher.
- **Decryption subkeys.** The negatives $-k_2$ and $-k_3$ change places in rounds 2 to 8 of decryption, but not in the first and last steps.
- **Multiplicative inverses.** The inverse of 0 (that is $2^{16} = -1$) is 0, and the inverse of 1 is 1. Code that computes inverses only for nonzero words fails on these keys.
- **Large data under one key.** With a 64-bit block, rekey long before $2^{32}$ blocks.

## Implementations

## History

Lai and Massey at ETH Zurich proposed PES in 1990. After Biham and Shamir published differential cryptanalysis, Lai, Massey and Murphy showed in 1991 how to measure the resistance of a cipher to it, and gave an improved version, IPES. It became IDEA in Lai's doctoral thesis of 1992. Ascom held patents on IDEA, which expired around 2011 and 2012. PGP 2.0 of 1992 replaced its first cipher with IDEA, which made it one of the most used ciphers of the 1990s. Later versions of PGP and OpenPGP moved to other ciphers.

## References
