---
tag: Q2MXRM
kind: definition
slug: golay-code
name: Golay code
aliases:
- binary Golay code
- extended Golay code
- ternary Golay code
- "[23, 12, 7] Golay code"
- "[24, 12, 8] Golay code"
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "The perfect binary [23, 12, 7] cyclic code, its self-dual extension [24, 12, 8], and the perfect ternary [11, 6, 5] code. Each corrects every error pattern up to its radius."
history:
  year: 1949
  people: [Marcel J. E. Golay]
  note: Golay gave both perfect codes as generator matrices in a one-page note in 1949. Pless (1968) and Delsarte and Goethals (1975) proved that the codes are unique.
prereqs: [cyclic-code, minimum-distance, hamming-bound]
see_also: [hamming-code, macwilliams-identity, syndrome-decoding, griesmer-bound, delsarte-lp-bound, reed-muller-code, bch-code]
sources:
  - paper: doi:10.1109/JRPROC.1949.233620
    title: M. J. E. Golay, Notes on digital coding, Proceedings of the IRE 37(6), 1949
    locator: p. 657 (the binary code of length 23 and the ternary code of length 11, given by their generator matrices)
  - paper: doi:10.1016/0012-365x(75)90047-3
    title: P. Delsarte and J.-M. Goethals, Unrestricted codes with the Golay parameters are unique, Discrete Mathematics 12(3), 1975
    locator: pp. 211 to 224 (every binary or ternary code, linear or not, with the Golay parameters is equivalent to the Golay code)
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 20 (the Golay codes, their uniqueness, the Steiner systems S(5, 8, 24) and S(4, 7, 23), and the Mathieu groups)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Section 4.6 (the (24, 12) Golay code, the matrix B, and the decoding algorithm that the implementation follows)
  - book: isbn:9780521782807
    title: W. Cary Huffman and Vera Pless, Fundamentals of Error-Correcting Codes, Cambridge University Press, 2003
    locator: Sections 1.9 and 10.1 (the Golay codes, their weight distributions and their automorphism groups)
  - paper: doi:10.1109/tit.1986.1057187
    title: J. H. Conway and N. J. A. Sloane, Lexicographic codes, error-correcting codes from game theory, IEEE Transactions on Information Theory 32(3), 1986
    locator: The greedy lexicode of length 24 and distance 8 is the extended Golay code
---

The Golay codes are three linear codes with exceptional parameters. The binary Golay code is a [cyclic code](/cyclic-code/) with parameters $[23, 12, 7]$. It is *perfect*: the balls of radius 3 around its 4096 codewords fill the space $\mathrm{GF}(2)^{23}$ with no gaps and no overlaps. The extended binary Golay code $[24, 12, 8]$ adds a parity bit and is self-dual. The ternary Golay code $[11, 6, 5]_3$ is perfect with radius 2. With the [Hamming codes](/hamming-code/) and the trivial codes, the Golay codes give all the parameters of perfect codes over alphabets of prime power size.

## Definition

**Binary Golay code.** Let

$$g(x) = x^{11} + x^{10} + x^{6} + x^{5} + x^{4} + x^{2} + 1 \in \mathrm{GF}(2)[x].$$

Over GF(2), $x^{23} + 1 = (x + 1)\, g(x)\, \tilde g(x)$, where $\tilde g(x) = x^{11} g(1/x) = x^{11} + x^{9} + x^{7} + x^{6} + x^{5} + x + 1$ is the reciprocal of $g$. The binary Golay code $G_{23}$ is the cyclic code of length 23 with generator polynomial $g(x)$:

$$G_{23} = \{\, m(x) g(x) \bmod (x^{23} + 1) : \deg m < 12 \,\}.$$

It has dimension $23 - 11 = 12$ and [minimum distance](/minimum-distance/) 7. The code from $\tilde g$ is equivalent: it is $G_{23}$ with the coordinates in reverse order.

**Extended binary Golay code.** $G_{24}$ is $G_{23}$ with an overall parity bit added to each word, so every word has even weight. It is a $[24, 12, 8]$ code. A convenient generator matrix is $[\,I_{12} \mid B\,]$, where the first 11 rows of the $12 \times 12$ matrix $B$ are the 11 left cyclic shifts of $11011100010$, each followed by a 1, and the last row is eleven 1s followed by a 0. This $B$ is symmetric and $B^2 = I$, so $[\,B \mid I_{12}\,]$ is also a generator matrix and a parity check matrix.

**Ternary Golay code.** $G_{11}$ is the cyclic code of length 11 over GF(3) with generator polynomial $x^5 + x^4 - x^3 + x^2 - 1$, which divides $x^{11} - 1$. It is an $[11, 6, 5]_3$ code. Adding the parity symbol $-\sum_i c_i$ gives the extended ternary Golay code $G_{12}$, a $[12, 6, 6]_3$ code.

### Perfection

A code is perfect when it meets the [Hamming bound](/hamming-bound/) with equality. For the two short Golay codes:

$$2^{12}\left[\binom{23}{0} + \binom{23}{1} + \binom{23}{2} + \binom{23}{3}\right] = 2^{12}(1 + 23 + 253 + 1771) = 2^{12} \cdot 2^{11} = 2^{23},$$

$$3^{6}\left[1 + 2\binom{11}{1} + 4\binom{11}{2}\right] = 3^{6}(1 + 22 + 220) = 3^{6} \cdot 3^{5} = 3^{11}.$$

So each word of $\mathrm{GF}(2)^{23}$ is at distance at most 3 from exactly one codeword of $G_{23}$, and each word of $\mathrm{GF}(3)^{11}$ is at distance at most 2 from exactly one codeword of $G_{11}$. The extended codes are not perfect, because a word at distance 4 from a codeword of $G_{24}$ can be at distance 4 from several codewords.

### Weight distributions

The tests compute these counts from the 4096 and 729 codewords. $A_i$ is the number of codewords of weight $i$, and weights with $A_i = 0$ are left out.

| code | weights $i$ : $A_i$ |
|---|---|
| $G_{23}$, $[23, 12, 7]$ | 0 : 1, 7 : 253, 8 : 506, 11 : 1288, 12 : 1288, 15 : 506, 16 : 253, 23 : 1 |
| $G_{24}$, $[24, 12, 8]$ | 0 : 1, 8 : 759, 12 : 2576, 16 : 759, 24 : 1 |
| $G_{11}$, $[11, 6, 5]_3$ | 0 : 1, 5 : 132, 6 : 132, 8 : 330, 9 : 110, 11 : 24 |
| $G_{12}$, $[12, 6, 6]_3$ | 0 : 1, 6 : 264, 9 : 440, 12 : 24 |

All weights of $G_{24}$ are multiples of 4, so the code is *doubly even*. $G_{24}$ and $G_{12}$ are self-dual, $C = C^\perp$, so the [MacWilliams identity](/macwilliams-identity/) maps each of their weight enumerators to itself.

### Uniqueness

Any binary code of length 24, with $2^{12}$ words and minimum distance 8, that contains the zero word is equivalent to $G_{24}$. The same holds for length 23, $2^{12}$ words and distance 7, and for the ternary parameters. Pless proved this for linear codes in 1968, and Delsarte and Goethals proved it for all codes, linear or not, in 1975. So the phrase "the Golay code" names one code up to a permutation of coordinates (and, for the ternary code, a change of signs).

Tietäväinen, and independently Zinoviev and Leontiev, proved in 1973 that a nontrivial perfect code over an alphabet of prime power size has the parameters of a Hamming code or of a Golay code. With uniqueness, this means that $G_{23}$ and $G_{11}$ are the only perfect codes that correct more than one error over such alphabets.

### Decoding

Because $G_{23}$ is perfect, a table with $2^{11} = 2048$ entries maps each syndrome $r(x) \bmod g(x)$ to the unique error pattern of weight at most 3 with that syndrome. Every received word decodes, and the decoder is a complete [syndrome decoder](/syndrome-decoding/).

For $G_{24}$ there is a short arithmetic decoder that uses $B$ only. Let $b_i$ be row $i$ of $B$, $u_i$ the unit vector, and $r = (r_1 \mid r_2)$ the received word.

1. Compute $s = r_1 + r_2 B$.
2. If $\mathrm{wt}(s) \le 3$, the error is $(s \mid 0)$.
3. If $\mathrm{wt}(s + b_i) \le 2$ for some $i$, the error is $(s + b_i \mid u_i)$.
4. Compute $sB$. If $\mathrm{wt}(sB) \le 3$, the error is $(0 \mid sB)$.
5. If $\mathrm{wt}(sB + b_i) \le 2$ for some $i$, the error is $(u_i \mid sB + b_i)$.
6. Otherwise at least 4 errors occurred. Report a failure.

The steps work because $B^2 = I$: the vector $sB$ is the syndrome for the parity check matrix $[\,B \mid I\,]$, so steps 4 and 5 are steps 2 and 3 seen from the other half. An error of weight at most 3 has at most one bit in one of the two halves, so one of the four cases finds it. The tests run this decoder on all 2325 error patterns of weight at most 3, and check that it reports a failure on all 10626 patterns of weight 4.

## Examples and non-examples

**Encoding and decoding $G_{23}$.** The implementation puts the 12 message bits at positions 11 to 22 and the remainder $x^{11} m(x) \bmod g(x)$ at positions 0 to 10. For the message with $m_0 \dots m_{11} = 000111001101$ the codeword, positions 0 to 22, is

$$c = 01000110011\;000111001101,$$

of weight 11. Flip positions 0, 5 and 17 to get $r = 11000010011\;000111101101$. The remainder of $r(x)$ modulo $g(x)$ is $10110111011$, read from $x^0$ up. The table entry for this syndrome is the error $x^0 + x^5 + x^{17}$, and $r$ plus this error is $c$. If a fourth bit is flipped, the decoder still returns a codeword, but it is a different codeword at distance 3 from $r$. A perfect code has no words that it can only detect as wrong.

**The weight 8 words of $G_{24}$.** Each set of 5 coordinates lies in the support of exactly one codeword of weight 8. This gives $\binom{24}{5} / \binom{8}{5} = 42504 / 56 = 759$ such words, and their supports form the Steiner system $S(5, 8, 24)$. In the same way the 253 words of weight 7 in $G_{23}$ form $S(4, 7, 23)$. The automorphism group of $G_{24}$ is the Mathieu group $M_{24}$, of order 244823040, and that of $G_{23}$ is $M_{23}$.

**A greedy construction.** List all binary words of length 24 in lexicographic order. Keep each word whose distance to all kept words is at least 8. The result has 4096 words and is the extended Golay code (Conway and Sloane, 1986). With length 23 and distance 7 the same rule gives $G_{23}$.

**The quadratic residue view.** The squares modulo 23 are $Q = \{1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18\}$. Since 2 is in $Q$, the polynomial $\prod_{i \in Q}(x - \alpha^i)$, for a primitive 23rd root of unity $\alpha$, has coefficients in GF(2), and it is $g(x)$ or $\tilde g(x)$ for a suitable $\alpha$. So $G_{23}$ is the binary quadratic residue code of length 23. In the same way $G_{11}$ is the ternary quadratic residue code of length 11.

**Non-example: parameters that pass the Hamming bound.** The numbers $n = 90$, $M = 2^{78}$, $t = 2$ satisfy the Hamming bound with equality, because $1 + 90 + \binom{90}{2} = 4096 = 2^{12}$. Golay noticed this in 1949, but there is no binary code with these parameters, linear or not. Equality in the bound does not by itself give a code.

**Non-example: the binary codes against the Griesmer bound.** For $k = 12$ and $d = 7$ the [Griesmer bound](/griesmer-bound/) gives $n \ge 7 + 4 + 2 + 1 + 8 \cdot 1 = 22$, and for $d = 8$ it gives $n \ge 8 + 4 + 2 + 1 + 8 \cdot 1 = 23$. $G_{23}$ and $G_{24}$ are each one longer. Both are optimal, because a $[22, 12, 7]$ code would break the Hamming bound ($2^{12} \cdot 1794 > 2^{22}$), and so would a $[23, 12, 8]$ code after one coordinate is removed. So the Griesmer bound is not tight here. The ternary code $G_{11}$ does meet it: $5 + 2 + 1 + 1 + 1 + 1 = 11$.

**Non-example: a cyclic $[23, 12]$ code with a different generator.** The only degree 11 divisors of $x^{23} + 1$ are $g$ and $\tilde g$. Any other polynomial of degree 11 does not divide $x^{23} + 1$, so it does not generate a cyclic code of length 23. The product $(x + 1) g(x)$ generates the $[23, 11, 8]$ even weight subcode of $G_{23}$, which is not perfect.

## Related definitions

- [Hamming code](/hamming-code/): the other family of perfect codes, with radius 1.
- [Hamming bound](/hamming-bound/): the sphere packing bound that a perfect code meets with equality.
- [Cyclic code](/cyclic-code/): the family that contains $G_{23}$ and $G_{11}$. Both are also quadratic residue codes.
- [Reed-Muller code](/reed-muller-code/): $G_{24}$, the $[8, 4, 4]$ code $\mathrm{RM}(1, 3)$ and the $[32, 16, 8]$ code $\mathrm{RM}(2, 5)$ are doubly even self-dual codes.
- [MacWilliams identity](/macwilliams-identity/): it shows that the weight enumerator of a self-dual code is invariant.
- [Delsarte LP bound](/delsarte-lp-bound/): the linear program for $n = 24$, $d = 8$ has optimum 4096, and its solution is the weight distribution of $G_{24}$.
- The Leech lattice, which gives the densest sphere packing in 24 dimensions, is built from $G_{24}$.

## References
