---
tag: 9XG8MF
kind: technique
slug: integral-cryptanalysis
name: Integral cryptanalysis
aliases:
- square attack
area: cryptography/symmetric-ciphers
level: research
summary: A chosen-plaintext attack on sets of texts that take every value in some cells. Their XOR sum stays zero through several rounds, and this reveals last-round key bits.
prereqs: [block-cipher, chosen-plaintext-attack, substitution-permutation-network, advanced-encryption-standard]
see_also: [differential-cryptanalysis, linear-cryptanalysis, boomerang-attack, s-box, gf2-polynomial-arithmetic, camellia, cryptanalysis]
sources:
  - paper: doi:10.1007/BFb0052343
    title: Joan Daemen, Lars Knudsen and Vincent Rijmen, The block cipher Square, Fast Software Encryption 1997, LNCS 1267, Springer, 1997
    locator: pp. 149-165, Section 6 (the dedicated attack, the Lambda-set, the 4-round attack and its extensions to 5 and 6 rounds) and Table 3 (the complexities)
  - url: "https://csrc.nist.gov/csrc/media/projects/cryptographic-standards-and-guidelines/documents/aes-development/rijndael-ammended.pdf"
    title: Joan Daemen and Vincent Rijmen, AES proposal, Rijndael, document version 2, 1999
    locator: Section 8.4 (the Square attack applied to Rijndael) and Figure 12 (its complexity)
  - paper: doi:10.1007/3-540-45661-9_9
    title: Lars Knudsen and David Wagner, Integral cryptanalysis, Fast Software Encryption 2002, LNCS 2365, Springer, 2002
    locator: pp. 112-127, the abstract and the framework of integrals as a dual of differential cryptanalysis
  - paper: doi:10.1007/978-3-662-46800-5_12
    title: Yosuke Todo, Structural evaluation by generalized integral property, Eurocrypt 2015, LNCS 9056, Springer, 2015
    locator: pp. 287-314, the abstract and the definition of the division property
  - paper: doi:10.1007/978-3-662-47989-6_20
    title: Yosuke Todo, Integral cryptanalysis on full MISTY1, Crypto 2015, LNCS 9215, Springer, 2015
    locator: pp. 413-432, the abstract (a 6-round integral characteristic and key recovery on the full MISTY1)
  - paper: doi:10.1007/3-540-44706-7_15
    title: Niels Ferguson, John Kelsey, Stefan Lucks, Bruce Schneier, Mike Stay, David Wagner and Doug Whiting, Improved cryptanalysis of Rijndael, Fast Software Encryption 2000, LNCS 1978, Springer, 2001
    locator: pp. 213-230, the partial sum technique for the Square attack on Rijndael
---

Integral cryptanalysis is a [chosen-plaintext attack](/chosen-plaintext-attack/) on [block ciphers](/block-cipher/) that work on words, such as bytes. The attacker encrypts a set of plaintexts that take every value in some words and are equal in the others. Through a few rounds, each word of the state either keeps this form or has a sum, by XOR over the set, of zero. One round more, the attacker guesses part of the last round key, undoes the last round and checks that the sum is zero. The method first appeared in 1997 as a dedicated attack in the paper by Joan Daemen, Lars Knudsen and Vincent Rijmen that introduced the cipher Square, so it is also called the Square attack. It applies to [AES](/advanced-encryption-standard/) reduced to 6 rounds.

**Notation.** The state has $w$ words of $m$ bits. A $\Lambda$-set is a set of $2^m$ states that take all $2^m$ values in one word, the active word, and are constant in the others. For a set of states, a word is A (all) if it takes every value exactly once, C if it is constant, B (balanced) if its XOR over the set is 0, and ? if nothing is known. $\bigoplus_{x \in \Lambda}$ is the XOR over the set.

## In plain words

Take sixteen messages that are the same except in one small part, where they go through every possible value once. Encrypt all of them. At first, the one changing part stays in its place, and every table in the cipher only renames its values, so it still goes through every value. The mixing steps spread it to the other parts, but each part still goes through every value.

After a few rounds, the parts are no longer so neat. But one property stays: if you combine all sixteen versions of any part with XOR, you get zero. The attacker guesses a part of the last key, undoes the last table, and checks this property. A wrong guess passes only by chance, so a few sets of messages leave only the right key.

## When it applies

- **The attacker can choose plaintexts**, in sets of $2^m$ or more that are all equal except in some words.
- **Word structure with bijective parts.** The method follows words through the rounds. It works best when the S-boxes and the linear maps act on whole words and are bijective, as in AES, Square and [Camellia](/camellia/). Knudsen and Wagner note that it applies to ciphers that are not open to [differential cryptanalysis](/differential-cryptanalysis/).
- **Few rounds.** The balanced property lasts only a few rounds. The key guess adds one round at the end, and other guesses can add a round at the start.

## The template

**The balanced property.** These rules hold for any $\Lambda$-set:

1. A bijective S-box maps an A word to an A word and a C word to a C word.
2. Key addition by XOR keeps A, C and B.
3. A permutation of the words moves the labels.
4. In a linear map over $\mathrm{GF}(2^m)$, an output word that depends on one A word, with a nonzero factor, and on C words only is A.
5. If every input of a linear map is A or B, every output word is B. The output is a sum of terms $c \cdot x$, and $\bigoplus_{x} c \cdot x = c \cdot \bigoplus_{x} x = 0$ for each term, since the XOR of all $2^m$ values is 0.

**The attack on the last round.** If the state before the last round is B in a word, and the last round is an S-box, a word permutation and a key addition, then each ciphertext word $C[i]$ equals $S(y) \oplus k_i$ for a B word $y$. For a guess $g$ of $k_i$, compute $\bigoplus S^{-1}(C[i] \oplus g)$ over the set. The right guess gives 0. A wrong guess gives 0 by chance, with probability about $2^{-m}$.

```pseudo id=main
INTEGRAL-LAST-ROUND(E)
L1  cands[i] ← all 2^m values, for each word i of the last round key
L2  while some cands[i] holds more than one value do
L3      choose a Λ-set P₁ .. P_(2^m) with one active word
L4      C_j ← E(P_j) for each j
L5      for each word i do
L6          remove from cands[i] each g with ⊕_j S⁻¹(C_j[i] ⊕ g) ≠ 0
L7  return cands
```

**Cost.** Each word is tested on its own, so one $\Lambda$-set costs $2^m$ encryptions and $w \cdot 2^m \cdot 2^m$ S-box lookups. A wrong guess survives one set with probability about $2^{-m}$, so a few sets leave only the right key.

**About the code.** The Python code of this page attacks mini-Square, a toy cipher made for this page, not taken from the literature. It has the round structure of AES at a smaller scale: a $4 \times 4$ array of 4-bit cells, the 4-bit S-box of the Heys tutorial, ShiftRows, MixColumns with the circulant matrix (2 3 1 1) over $\mathrm{GF}(2^4)$ with the polynomial $x^4 + x + 1$, and independent 64-bit round keys. The last round has no MixColumns, as in AES. The code is for study only and is not constant time. Do not use any of it to protect real data. Use AES from a validated library such as OpenSSL instead.

## Classic examples

### Three rounds of mini-Square

Take a $\Lambda$-set with cell 0 active. Cell $4c + r$ is row $r$ of column $c$, so the patterns below list column 0 first.

| after round | pattern of the 16 cells | XOR over the set |
|---|---|---|
| 0 (key addition) | A C C C, C C C C, C C C C, C C C C | 0 in every cell |
| 1 | A A A A, C C C C, C C C C, C C C C | 0 in every cell |
| 2 | all A | 0 in every cell |
| 3 | all B | 0 in every cell |
| 4 | ? | not 0 |

In round 1, ShiftRows does not move cell 0, and MixColumns spreads it to the whole column by rule 4, since each factor of the matrix is nonzero. In round 2, ShiftRows puts one A cell in each column, and MixColumns makes every cell A. In round 3, MixColumns adds four A cells for each output, so every cell is B by rule 5. The S-boxes of round 4 break the property. With one random key, the XOR of the sixteen states after four rounds, the last without MixColumns, was 9CE42D5EFFBDF303.

### Key recovery on four rounds

Rounds 1 to 3 are full rounds and round 4 has no MixColumns, so line L6 applies to each of the 16 cells of the last round key. With the last round key D698014EFB68FEFD, one $\Lambda$-set leaves one candidate in 5 cells, and up to 8 candidates in the worst cell. Over 200 random keys, a cell kept on average 1.37 wrong candidates after one set, a little more than the $15/16$ of a random sum, since the S-box has only 16 inputs. The attack needed 2 sets for 14 keys, 3 sets for 115 keys, 4 sets for 50 keys, 5 sets for 15 keys and 6 sets for 6 keys. So 48 chosen plaintexts are typical.

### Square and AES

In Square and Rijndael, the words are bytes and a $\Lambda$-set has 256 plaintexts. Table 3 of the Square paper and Figure 12 of the Rijndael proposal give the same costs:

| attack | chosen plaintexts | time | memory |
|---|---|---|---|
| 4 rounds | $2^9$ | $2^9$ | small |
| 5 rounds, extension at the end | $2^{11}$ | $2^{40}$ | small |
| 5 rounds, extension at the start | $2^{32}$ | $2^{40}$ | $2^{32}$ |
| 6 rounds, both extensions | $2^{32}$ | $2^{72}$ | $2^{32}$ |

The attack does not depend on the S-box, on the factors of MixColumns or on the key schedule. Because of it, the designers of Square raised the number of rounds to at least seven and chose eight as a safety margin.

### MISTY1

Todo built a 6-round integral characteristic of MISTY1 with the division property, and used it in 2015 to recover the key of the full MISTY1 with $2^{63.58}$ chosen plaintexts and $2^{121}$ time. It was the first attack on the full cipher. The attack is theoretical and does not affect the practical use of MISTY1.

## Variations

- **A general framework.** Knudsen and Wagner unified these ideas under the name integral cryptanalysis, with sums over larger sets and several active words, and applied them to MISTY. Their abstract calls integral cryptanalysis a dual to differential cryptanalysis.
- **Higher-order differentials.** The XOR of $f$ over a linear subspace of dimension $d$ is a derivative of order $d$. If the degree of $f$ over $\mathrm{GF}(2)$ is less than $d$, the sum is 0. This gives integral properties for ciphers without word structure.
- **The division property.** Todo generalized the A, C and B rules to the division property in 2015. It finds integral distinguishers for bit-oriented ciphers, ciphers with non-bijective parts and ciphers of low degree.
- **Partial sums.** Ferguson and his coauthors split the sum of line L6 into steps with shared parts. This saves time when the key guess covers several words, as in the attacks on AES with more rounds.

## Pitfalls

- **B is not A.** A balanced word has XOR sum 0, but it may not take every value. Rule 4 does not apply to B words, so the property does not pass through another S-box.
- **The last MixColumns.** If the last round has a linear map after the S-boxes, apply its inverse to the ciphertexts first. The map is linear, so the attack then finds an equivalent key, the inverse map of the round key. AES has no MixColumns in its last round, so it does not need this step.
- **False survivors.** Wrong guesses pass with probability about $2^{-m}$ for each set. Use enough sets, as in line L2.
- **Real ciphers.** Run such experiments only on toy ciphers or reduced rounds that you are allowed to attack.

## Exercises

1. Prove rule 5: the XOR of $c \cdot x$ over all $x \in \mathrm{GF}(2^m)$ is 0 for any $c$.
2. Show that if the matrix of MixColumns had a zero factor, rule 4 could fail, and find which cells of round 1 would then stay C.
3. Show that the sum of $S(x)$ over a B word need not be 0, by an example with the S-box of the toy cipher.
4. Extend the toy attack by a round at the start: choose plaintexts with one active column and guess one column of the first round key.
5. For a Boolean function of degree $t$ over $\mathrm{GF}(2)$, prove that the XOR of its values over any affine subspace of dimension $t + 1$ is 0.

## References
