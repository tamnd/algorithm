---
tag: FXRB76
kind: concept
slug: s-box
name: S-box
aliases:
- substitution box
area: cryptography/symmetric-ciphers
level: core
summary: A small nonlinear lookup table, the source of confusion in a block cipher. Its quality is measured by the DDT and the LAT. The AES S-box has differential uniformity 4 and nonlinearity 112.
prereqs: [confusion-and-diffusion]
see_also: [advanced-encryption-standard, data-encryption-standard, substitution-permutation-network, differential-cryptanalysis, linear-cryptanalysis, walsh-hadamard-transform, boolean-function, gf2-polynomial-arithmetic]
sources:
  - paper: doi:10.6028/NIST.FIPS.197-upd1
    title: NIST, FIPS 197, Advanced Encryption Standard (AES), November 2001, updated May 2023
    locator: Section 4 (the field GF(2^8) and its multiplicative inverse) and Section 5.1.1 (SubBytes, the affine map and the S-box table)
  - book: isbn:9783540425809
    title: Joan Daemen and Vincent Rijmen, The Design of Rijndael, Springer, 2002
    locator: Chapter 3 (the specification of SubBytes) and Chapter 5 (the design rationale of the S-box)
  - paper: "Kaisa Nyberg, Differentially uniform mappings for cryptography, Advances in Cryptology, EUROCRYPT 1993, LNCS 765, Springer, 1994"
    locator: the definition of differential uniformity and the properties of the inversion mapping in GF(2^m)
  - paper: "Don Coppersmith, The Data Encryption Standard (DES) and its strength against attacks, IBM Journal of Research and Development 38(3), 1994"
    locator: the design criteria S-1 to S-8 of the DES S-boxes
  - paper: doi:10.1080/0161-110291890885
    title: Howard M. Heys, A tutorial on linear and differential cryptanalysis, Cryptologia 26(3), 2002
    locator: the 4-bit S-box of the toy cipher, its linear approximation table and its difference distribution table
---

An S-box (substitution box) is a small fixed function $S : \{0,1\}^m \to \{0,1\}^p$, stored as a lookup table, that is the nonlinear part of a [block cipher](/block-cipher/). It provides the [confusion](/confusion-and-diffusion/) of the cipher: without it, every round would be affine over GF(2), and the cipher would fall to a few queries. Its resistance to [differential](/differential-cryptanalysis/) and [linear cryptanalysis](/linear-cryptanalysis/) is measured by two tables, the difference distribution table (DDT) and the linear approximation table (LAT). The AES S-box, the inverse in GF($2^8$) followed by an affine map, reaches differential uniformity 4 and nonlinearity 112.

## In plain words

An S-box is a small table. You look up a short group of bits, such as 4 or 8, and the table gives you another group of bits. The table is fixed and public, but it is scrambled in a careful way.

Why does a cipher need it? Steps such as exclusive or with the key, rotations and bit moves are all "linear": the effect of two changes is the sum of their effects. A cipher made only of such steps can be solved like a system of equations. The S-box breaks this.

A good S-box has two qualities. A given change at its input leads to many different output changes, each with low chance. And no simple sum of input bits predicts a sum of output bits much better than a coin flip.

## The idea

**Notation.** $S : \{0,1\}^m \to \{0,1\}^m$ is a bijective S-box (DES uses $m = 6$ inputs and 4 outputs). For $a, x \in \{0,1\}^m$, $a \cdot x$ is the inner product over GF(2). The analysis is in the standard model, and the counts are exact.

**The difference distribution table.** For an input difference $a$ and an output difference $b$,

$$\mathrm{DDT}[a][b] = \#\{x \in \{0,1\}^m : S(x \oplus a) \oplus S(x) = b\}.$$

Each entry is even, because $x$ and $x \oplus a$ give the same difference, and each row sums to $2^m$. The *differential uniformity* is $\delta(S) = \max_{a \ne 0, b} \mathrm{DDT}[a][b]$. A difference $a \to b$ holds with probability $\mathrm{DDT}[a][b]/2^m$, so differential cryptanalysis needs $\delta(S)$ small. The least possible value is 2 (such maps are called APN). For bijections on 4 bits the least value is 4, and for bijections on 8 bits no value below 4 is known.

**The linear approximation table.** With the convention of Heys,

$$\mathrm{LAT}[a][b] = \#\{x : a \cdot x = b \cdot S(x)\} - 2^{m-1},$$

so the linear relation $a \cdot x = b \cdot S(x)$ holds with probability $\frac{1}{2} + \mathrm{LAT}[a][b]/2^m$. The *Walsh transform* of the component $b \cdot S$ is $W_b(a) = \sum_x (-1)^{a \cdot x \oplus b \cdot S(x)} = 2\,\mathrm{LAT}[a][b]$. The *nonlinearity* is the least Hamming distance from a nonzero component $b \cdot S$ to an affine function:

$$\mathrm{NL}(S) = 2^{m-1} - \max_{a,\ b \ne 0} |\mathrm{LAT}[a][b]| = 2^{m-1} - \tfrac{1}{2}\max_{a,\ b \ne 0} |W_b(a)|.$$

Linear cryptanalysis needs $\mathrm{NL}(S)$ large. The LAT can be computed in $\Theta(m 4^m)$ steps by the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/), and the DDT in $\Theta(4^m)$.

**An upper bound on nonlinearity.** By Parseval's identity, $\sum_a W_b(a)^2 = 2^{2m}$ for each $b$: expand the square, and the sum over $a$ of $(-1)^{a \cdot (x \oplus x')}$ is $2^m$ if $x = x'$ and 0 otherwise. There are $2^m$ terms, so some $|W_b(a)| \ge 2^{m/2}$, and $\mathrm{NL}(S) \le 2^{m-1} - 2^{m/2 - 1}$. For $m = 8$ this gives 120.

**Affine maps do not change the tables.** Let $S' = L \circ S \oplus c$ with $L$ linear and invertible. Then $S'(x \oplus a) \oplus S'(x) = L(S(x \oplus a) \oplus S(x))$, so $\mathrm{DDT}_{S'}[a][L(b)] = \mathrm{DDT}_S[a][b]$, and $\delta(S') = \delta(S)$. In the same way, $b \cdot S'(x) = (L^{\mathsf T} b) \cdot S(x) \oplus b \cdot c$, so each row of the LAT of $S'$ is a row of the LAT of $S$, up to sign, and $\mathrm{NL}(S') = \mathrm{NL}(S)$.

**Theorem (the inverse in GF($2^m$) is 4-uniform).** Let $I(x) = x^{-1}$ in GF($2^m$), with $I(0) = 0$. Then $\delta(I) \le 4$, with equality when $m$ is even.

*Proof.* Fix $a \ne 0$ and $b$, and count the $x$ with $I(x + a) + I(x) = b$ (addition in the field is XOR). For $x \in \{0, a\}$, the left side is $a^{-1}$, so both values are solutions if $b = a^{-1}$ and neither is otherwise. For $x \notin \{0, a\}$, the equation is $\frac{1}{x+a} + \frac{1}{x} = \frac{a}{x(x+a)} = b$. Since $a \ne 0$, this needs $b \ne 0$, and then it is $b x^2 + a b x + a = 0$, a nonzero polynomial of degree 2 with at most 2 roots. So there are at most $2 + 2 = 4$ solutions. If $b = a^{-1}$, then with $t = x/a$ the quadratic becomes $t^2 + t + 1 = 0$. Its roots lie in GF(4), and GF(4) is a subfield of GF($2^m$) exactly when $m$ is even. Then $t \notin \{0, 1\}$, so $x = at \notin \{0, a\}$, and the count is 4. $\square$

## Examples

**The AES S-box.** FIPS 197 defines $S(x) = A(x^{-1}) \oplus \mathtt{0x63}$, where $x^{-1}$ is the inverse in GF($2^8$) modulo $x^8 + x^4 + x^3 + x + 1$ (with $0 \mapsto 0$, computed for example as $x^{254}$ by [polynomial arithmetic over GF(2)](/gf2-polynomial-arithmetic/)) and $A$ is the linear map

$$b'_i = b_i \oplus b_{(i+4) \bmod 8} \oplus b_{(i+5) \bmod 8} \oplus b_{(i+6) \bmod 8} \oplus b_{(i+7) \bmod 8}.$$

For the input 0x53, the inverse is 0xCA, and the affine map gives 0xED, so $S(\mathtt{0x53}) = \mathtt{0xED}$, as in FIPS 197. Also $S(\mathtt{0x00}) = \mathtt{0x63}$ and $S(\mathtt{0x01}) = \mathtt{0x7C}$. The 256 values built in this way agree with the S-box table of FIPS 197.

- **Differential uniformity 4.** By the theorem and the affine invariance, $\delta(S) = 4$. Each of the 255 nonzero rows of the DDT has exactly one entry 4, 126 entries 2 and 129 entries 0. So a one-round difference holds with probability at most $4/256 = 2^{-6}$.
- **Nonlinearity 112.** The largest $|\mathrm{LAT}|$ entry with $b \ne 0$ is 16, so $\mathrm{NL}(S) = 128 - 16 = 112$, and each linear relation has bias at most $16/256 = 2^{-4}$. Nyberg showed that the inversion mapping has nonlinearity at least $2^{m-1} - 2^{m/2}$ for even $m$, which is 112 for $m = 8$. The Parseval bound above is 120.
- **No fixed points.** The constant 0x63 was chosen so that $S(x) \ne x$ and $S(x) \ne x \oplus \mathtt{0xFF}$ for all $x$. Both counts are 0.
- **Strict avalanche.** When one input bit flips, each output bit flips with a probability between 0.453 and 0.5625, over the 64 pairs of an input bit and an output bit.

**The Heys S-box.** The 4-bit S-box of the Heys tutorial maps 0, 1, ..., F to E, 4, D, 1, 2, F, B, 8, 3, A, 6, C, 5, 9, 0, 7. Its DDT has $\mathrm{DDT}[\mathtt{B}][\mathtt{2}] = 8$, so $\delta = 8$ and the difference B to 2 holds with probability $1/2$. Other large entries are $\mathrm{DDT}[\mathtt{4}][\mathtt{6}] = 6$ and $\mathrm{DDT}[\mathtt{2}][\mathtt{5}] = 6$. Over the 15 nonzero rows, the 240 entries are 153 zeros, 62 twos, 18 fours, 6 sixes and one 8. Its LAT has entries of absolute value 6, for example $\mathrm{LAT}[\mathtt{1}][\mathtt{7}] = 6$ and $\mathrm{LAT}[\mathtt{2}][\mathtt{E}] = -6$, so $\mathrm{NL} = 8 - 6 = 2$ and some linear relation holds with probability $14/16$ or $2/16$. The tutorial builds its attacks from entries such as $\mathrm{LAT}[\mathtt{B}][\mathtt{4}] = 4$ and $\mathrm{LAT}[\mathtt{4}][\mathtt{5}] = -4$. This S-box is a good teaching example because it is weak: the best 4-bit S-boxes have $\delta = 4$ and $\mathrm{NL} = 4$.

**The DES S-boxes.** DES has eight S-boxes from 6 to 4 bits. Each row (fixed outer bits) is a permutation of 0 to 15. Coppersmith published the design criteria in 1994, after differential cryptanalysis became public. Among them: two inputs that differ in one bit give outputs that differ in at least two bits; two inputs that differ in the two middle bits do the same; two inputs that differ in the first two bits and agree in the last two never give equal outputs; and for each nonzero input difference, at most 8 of the 32 input pairs give the same output difference. All eight S-boxes meet these criteria, and each has a largest DDT entry of 16 out of 64. The largest $|\mathrm{LAT}|$ entry is 20 of 64, in S-box 5; Matsui's linear attack is built on this entry.

**A non-example.** The identity map on 4 bits has $\delta = 16$ and $\mathrm{NL} = 0$: it is linear, and gives no confusion.

The code for this page computes these tables. It is for study only: a table lookup at a secret index is not constant time, and the code must not be used to protect real data. Use AES from a FIPS 140 validated module or from libsodium.

## Where it is used

- **SPN ciphers.** [AES](/advanced-encryption-standard/), [Serpent](/serpent/) and [PRESENT](/present/) apply one layer of S-boxes in each round of a [substitution-permutation network](/substitution-permutation-network/).
- **Feistel ciphers.** The round function of [DES](/data-encryption-standard/), [Blowfish](/blowfish/) and [Camellia](/camellia/) uses S-boxes. In Blowfish they depend on the key.
- **Bounds on attacks.** In the wide trail strategy of AES, the probability of a differential trail is at most $\delta/2^m$ for each active S-box. With at least 25 active S-boxes in 4 rounds, a 4-round trail of AES has probability at most $(2^{-6})^{25} = 2^{-150}$.
- **Side channels.** A table lookup at a secret index leaks through the cache. Bitsliced and hardware implementations compute the S-box with logic gates instead, and AES-NI computes it inside the processor.
- **Design of new S-boxes.** Lightweight ciphers choose 4-bit S-boxes from the classes with $\delta = 4$ and $\mathrm{NL} = 4$, and with low gate counts.

## References
