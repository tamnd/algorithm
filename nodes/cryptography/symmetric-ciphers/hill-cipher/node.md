---
tag: G0FB2K
kind: algorithm
slug: hill-cipher
name: Hill cipher
area: cryptography/symmetric-ciphers
level: intro
summary: Encrypt blocks of n letters as c = Kp mod 26 for a key matrix K whose determinant is coprime to 26. There are 157,248 keys for n = 2. Being linear, it falls to n known plaintext blocks.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the block size, L: the number of letters of the message}
  time: {worst: Θ(n·L), average: Θ(n·L), best: Θ(n·L)}
  space: {extra: Θ(n)}
properties: {deterministic: true}
prereqs: [affine-cipher, determinant, matrix-inversion]
see_also: [known-plaintext-attack, chinese-remainder-theorem, gaussian-elimination, modular-inverse, substitution-cipher, playfair-cipher, confusion-and-diffusion]
sources:
  - paper: "Lester S. Hill, Cryptography in an algebraic alphabet, The American Mathematical Monthly 36(6), 1929, pages 306 to 312"
    locator: the encryption of blocks of letters by a linear transformation with an invertible matrix over the integers modulo 26
  - book: isbn:9781138197015
    title: Douglas R. Stinson and Maura B. Paterson, Cryptography, Theory and Practice, fourth edition, CRC Press, 2018
    locator: Section 2.1.5 (the Hill cipher, invertible matrices modulo 26) and Section 2.2.4 (cryptanalysis of the Hill cipher by known plaintext)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Section 1.3 (historical ciphers and their cryptanalysis) and its exercises
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 7, Section 7.3 (classical ciphers, including the Hill cipher, and its weakness to known plaintext)
---

The Hill cipher encrypts a block of $n$ letters at once, as a vector $p \in \mathbb{Z}_{26}^n$, by multiplying it with a secret $n \times n$ key matrix: $c = K p \bmod 26$. Lester Hill published it in 1929. It was the first practical cipher built on linear algebra, and it mixes the letters of a block, so a change of one plaintext letter changes the whole cipher block. A matrix works as a key exactly when its [determinant](/determinant/) is coprime to 26. For $n = 2$ there are exactly 157,248 such matrices. The cipher hides single letter counts, but it is linear: $n$ known plaintext blocks whose matrix is invertible modulo 26 give the key at once.

## In plain words

Turn the letters into numbers, A as 0 up to Z as 25. Cut the message into groups of, say, two letters. The key is a small table of numbers. Each output letter is a weighted sum of the letters in the group, wrapped around at 26. So every cipher letter depends on every letter of its group, and the same plaintext letter turns into different cipher letters in different groups.

To undo it, the receiver needs a second table that cancels the first, and such a table exists only for some keys. The weakness: everything is sums and products. If an attacker knows a few groups of plaintext and the cipher groups that they became, they can solve for the key like a school system of equations.

## The problem

Identify A to Z with $\mathbb{Z}_{26}$. A key is a matrix $K \in \mathbb{Z}_{26}^{n \times n}$ that is invertible modulo 26, that is, an element of the group $GL(n, \mathbb{Z}_{26})$. The message is padded with X to a multiple of $n$ letters and cut into column vectors $p^{(1)}, p^{(2)}, \ldots$. Then

$$c^{(b)} = K p^{(b)} \bmod 26, \qquad p^{(b)} = K^{-1} c^{(b)} \bmod 26.$$

This is an instance of [symmetric encryption](/symmetric-encryption/). The code takes only the letters of the message, in upper case. Stinson and Paterson write blocks as row vectors and compute $pK$; that is the same cipher with the transposed key.

**Which matrices are keys.** $K$ has an inverse modulo 26 if and only if $\gcd(\det K, 26) = 1$. If the determinant shares the factor 2 or 13 with 26, then two different plaintext blocks have the same cipher block, so no decryption exists. The section on correctness below proves both directions.

## The algorithm

```pseudo id=main
HILL-ENCRYPT(P, K)                         ▷ K is n × n with gcd(det K, 26) = 1
L1  pad P with X to a multiple of n letters
L2  for each block of n letters do
L3      p ← the block as a column vector over Z26
L4      c ← K p mod 26
L5  return the cipher blocks, joined
```

Decryption runs HILL-ENCRYPT with $K^{-1} = (\det K)^{-1} \operatorname{adj}(K) \bmod 26$, where $(\det K)^{-1}$ is the [modular inverse](/modular-inverse/) of the determinant and $\operatorname{adj}(K)$ is the adjugate, the transpose of the matrix of cofactors. For $n = 2$:

$$\begin{pmatrix} a & b \\ c & d \end{pmatrix}^{-1} = (ad - bc)^{-1} \begin{pmatrix} d & -b \\ -c & a \end{pmatrix} \bmod 26.$$

**The known plaintext attack.** Let the attacker know $m \ge n$ plaintext blocks and their cipher blocks. Put them as the columns of the $n \times m$ matrices $P$ and $C$, so $KP = C$.

```pseudo id=kpa
HILL-KPA(P, C)
L6  if m = n and gcd(det P, 26) = 1 then return C P⁻¹ mod 26
L7  for q in {2, 13} do
L8      solve K_q P = C over the field Z_q by Gaussian elimination
L9      if the columns of P do not span (Z_q)^n then return "not unique"
L10 return the K with K ≡ K_2 (mod 2) and K ≡ K_13 (mod 13)
```

Line L6 is the textbook attack: $n$ blocks with an invertible plaintext matrix. When that matrix is not invertible, more blocks can still fix the key. Because $26 = 2 \cdot 13$, the [Chinese remainder theorem](/chinese-remainder-theorem/) splits the problem into one over the field $\mathbb{Z}_2$ and one over $\mathbb{Z}_{13}$, where [Gaussian elimination](/gaussian-elimination/) works. The key is unique exactly when the plaintext blocks span both $(\mathbb{Z}_2)^n$ and $(\mathbb{Z}_{13})^n$. The code implements lines L7 to L10, which include the case of line L6.

The code is for study only. It is not constant time, and the cipher gives no protection. To protect real data, use AES-GCM or ChaCha20-Poly1305 from libsodium, from a FIPS 140 validated module, or from the standard library of your language.

## Example

**Encryption.** Take the key of Stinson and Paterson's example, written for column vectors:

$$K = \begin{pmatrix} 11 & 3 \\ 8 & 7 \end{pmatrix}, \qquad \det K = 77 - 24 = 53 \equiv 1 \pmod{26}.$$

JULY is $(9, 20)$ and $(11, 24)$. Then $K (9, 20)^T = (99 + 60, 72 + 140) = (159, 212) \equiv (3, 4)$, which is DE, and $K (11, 24)^T = (121 + 72, 88 + 168) = (193, 256) \equiv (11, 22)$, which is LW. So JULY becomes DELW. Because $\det K \equiv 1$, the inverse is just the adjugate: $K^{-1} = \begin{pmatrix} 7 & 23 \\ 18 & 11 \end{pmatrix}$.

A 3 × 3 example: the key with rows (6, 24, 1), (13, 16, 10), (20, 17, 15) has determinant 441 ≡ 25, which is coprime to 26. It maps ACT to POH and CAT to FIN, so the same three letters in another order give unrelated cipher letters.

**The known plaintext attack.** Suppose the attacker knows that HELP became LGKL under the key $K$ above. Then

$$P = \begin{pmatrix} 7 & 11 \\ 4 & 15 \end{pmatrix}, \quad C = \begin{pmatrix} 11 & 10 \\ 6 & 11 \end{pmatrix}, \quad \det P = 105 - 44 = 61 \equiv 9,$$

and $\gcd(9, 26) = 1$, so $P^{-1} = 9^{-1} \begin{pmatrix} 15 & -11 \\ -4 & 7 \end{pmatrix} = 3 \begin{pmatrix} 15 & 15 \\ 22 & 7 \end{pmatrix} \equiv \begin{pmatrix} 19 & 19 \\ 14 & 21 \end{pmatrix}$ (as $9 \cdot 3 = 27 \equiv 1$). Then $C P^{-1} \equiv \begin{pmatrix} 11 & 3 \\ 8 & 7 \end{pmatrix} = K$.

**When the plaintext matrix is not invertible.** WEST encrypts to UWVR. Its plaintext matrix has columns $(22, 4)$ and $(18, 19)$, with determinant $418 - 72 = 346 \equiv 8$, which is even. Modulo 2 both columns are multiples of $(0, 1)$, so they do not span $(\mathbb{Z}_2)^2$. Then the first column of $K$ modulo 2 is free, and exactly two valid keys map WEST to UWVR. Adding the block EN does not help, since $(4, 13) \equiv (0, 1) \pmod 2$ again. Adding WARD gives the block $(22, 0) \equiv (0, 0)$ and then $(17, 3) \equiv (1, 1) \pmod 2$, which is independent of $(0, 1)$, so WESTWARD fixes $K$.

For random 2 × 2 keys and random plaintext blocks, the attack fixed the key in 44 of 115 trials with two blocks, 85 of 128 with three and 97 of 129 with four. The first number fits the share of invertible matrices, $157{,}248 / 26^4 \approx 0.344$; most failures come from the factor 2.

## Correctness

**Keys are exactly the matrices with a unit determinant.** If $\gcd(\det K, 26) = 1$, then $K \cdot (\det K)^{-1} \operatorname{adj}(K) = (\det K)^{-1} \det(K) I = I$ modulo 26, since $K \operatorname{adj}(K) = \det(K) I$ holds over any commutative ring. If $KK' \equiv I$, then $\det K \det K' \equiv 1$, so $\det K$ is a unit. And if $\det K$ is not a unit, a prime $q \in \{2, 13\}$ divides it, so $K$ is singular over the field $\mathbb{Z}_q$, some $v \not\equiv 0 \pmod q$ has $Kv \equiv 0 \pmod q$, and the vector $(26/q) v$ is a nonzero block that encrypts to the same block as $0$.

**Decryption inverts encryption.** $K^{-1}(Kp) = p$ modulo 26 for each block, and padding only adds letters at the end.

**The attack.** If $K P = C$ and the columns of $P$ span $(\mathbb{Z}_q)^n$, then any $K'$ with $K'P = C$ satisfies $(K - K')P \equiv 0 \pmod q$, so each row of $K - K'$ is orthogonal to a spanning set and is zero modulo $q$. Doing this for $q = 2$ and $q = 13$ gives $K' \equiv K \pmod{26}$. If the columns do not span $(\mathbb{Z}_q)^n$, a nonzero $u$ is orthogonal to all of them, and adding $(26/q)\, a u^T$ to $K$ gives a second matrix that fits; for $n \ge 2$ some $a$ keeps it invertible, so a second key fits. The full proofs are in the proof file below.

## Complexity

Each block costs $n^2$ multiplications, and there are $\lceil L/n \rceil$ blocks, so encryption takes $\Theta(nL)$ time in each case and $\Theta(n)$ extra space. Computing $K^{-1}$ once costs $O(n^3)$ arithmetic operations with Gaussian elimination, or more with the adjugate as in the code ($n^2$ minors, fine for the small $n$ of a hand cipher). The known plaintext attack with $m$ blocks costs $O(m n^2)$ operations over each of the two fields.

| claim | value |
|---|---|
| encryption, decryption | $\Theta(nL)$ |
| keys for $n = 2$ | $157{,}248$ |
| keys for $n = 3$ | $1{,}634{,}038{,}189{,}056 \approx 2^{40.6}$ |
| known plaintext attack | $n$ blocks with an invertible plaintext matrix |

**Counting the keys.** By the Chinese remainder theorem, $\mathbb{Z}_{26}^{n \times n} \cong \mathbb{Z}_2^{n \times n} \times \mathbb{Z}_{13}^{n \times n}$, and $K$ is invertible modulo 26 exactly when it is invertible modulo 2 and modulo 13. Over a field with $q$ elements there are $\prod_{i=0}^{n-1} (q^n - q^i)$ invertible matrices: the first column is any nonzero vector, the second any vector outside the span of the first, and so on. For $n = 2$:

$$|GL(2, \mathbb{Z}_{26})| = (4 - 1)(4 - 2) \cdot (169 - 1)(169 - 13) = 6 \cdot 168 \cdot 156 = 157{,}248,$$

and a count over all $26^4 = 456{,}976$ matrices in the test gives the same number.

## Properties

- **Linear.** $E(p + p') = E(p) + E(p')$ for blocks. This is the root of the weakness.
- **Diffusion inside a block.** Each cipher letter depends on all $n$ letters of its block. Hill's cipher is an early example of the [diffusion](/confusion-and-diffusion/) that Shannon later named.
- **Deterministic blocks.** Equal plaintext blocks give equal cipher blocks, so the digram counts (for $n = 2$) leak, and a ciphertext-only attack by block frequencies works on long texts.
- **Zero is fixed.** The block AA...A always encrypts to AA...A.

## Variants and improvements

- **Affine Hill cipher.** $c = Kp + b$. Still affine, so $n + 1$ known blocks give $K$ and $b$.
- **Other moduli.** With a prime alphabet size, such as 29 symbols, $\mathbb{Z}_{29}$ is a field and more matrices are keys.
- **Involutory keys.** Hill suggested matrices with $K = K^{-1}$, so that one device both encrypts and decrypts.
- **Combining with a nonlinear step.** Modern block ciphers alternate linear mixing layers, such as the MixColumns matrix of the [AES](/advanced-encryption-standard/), with nonlinear substitutions. The linear layer alone is the Hill idea.

## When to use it

Use it to teach matrices modulo $n$, invertibility over a ring that is not a field, and why linearity is fatal for a cipher. Never use it to protect data.

## Pitfalls

- **Testing $\det K \ne 0$ instead of $\gcd(\det K, 26) = 1$.** An even determinant or a multiple of 13 makes the key useless, even though the matrix is invertible over the rationals.
- **Inverting $\det K$ over the rationals.** Use the inverse modulo 26 of the determinant, not $1/\det K$.
- **Plain Gaussian elimination modulo 26.** $\mathbb{Z}_{26}$ is not a field, so a pivot may have no inverse. Work modulo 2 and 13 separately, or pick pivots that are units.
- **Row vectors against column vectors.** Books differ. $pK$ with row vectors is the cipher with key $K^T$ in the column form.
- **Assuming that $n$ known blocks always suffice.** About two thirds of the 2 × 2 plaintext matrices are not invertible modulo 26, as the WEST example shows.

## Implementations

## History

Lester S. Hill, a mathematician at Hunter College in New York, published the cipher in 1929 in "Cryptography in an algebraic alphabet" in The American Mathematical Monthly, and a second paper on linear transformations for cryptography followed in the same journal in 1931. He and Louis Weisner patented a mechanical device for a fixed 6 × 6 involutory key. The cipher saw little practical use, but it was the first to treat encryption as linear algebra over a finite ring.

## References
