---
tag: CWKBQ3
kind: definition
slug: reed-muller-code
name: Reed-Muller code
aliases:
- RM code
- binary Reed-Muller code
- generalized Reed-Muller code
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "RM(r, m) is the code of value tables of Boolean polynomials of degree at most r in m variables: length 2^m, distance 2^(m - r), dual RM(m - r - 1, m)."
history:
  year: 1954
  people: [David E. Muller, Irving S. Reed]
  note: Muller described the codes in 1954 in a paper on switching circuits. Reed, in the same year, gave the polynomial view and the majority-logic decoder. Kudekar et al. (2017) and Abbe and Sandon (2023) proved that the codes achieve capacity.
prereqs: [linear-code, minimum-distance, hadamard-code]
see_also: [majority-logic-decoding, polar-code, hadamard-code, hamming-code, golay-code, low-degree-test, hqc, binary-erasure-channel]
sources:
  - paper: doi:10.1109/TIT.1954.1057465
    title: I. S. Reed, A class of multiple-error-correcting codes and the decoding scheme, Transactions of the IRE Professional Group on Information Theory 4(4), 1954
    locator: pp. 38 to 49 (the codes as Boolean polynomials and the majority vote decoder)
  - paper: doi:10.1109/IREPGELC.1954.6499441
    title: D. E. Muller, Application of Boolean algebra to switching circuit design and to error detection, Transactions of the IRE Professional Group on Electronic Computers EC-3(3), 1954
    locator: pp. 6 to 12 (the codes, found from Boolean functions)
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapters 13 to 15 (Reed-Muller codes, the (u | u + v) construction, the dual, the minimum weight words as flats, first order codes)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Section 4.3 (Reed-Muller codes and their majority-logic decoding)
  - paper: doi:10.1109/TIT.2017.2673829
    title: S. Kudekar, S. Kumar, M. Mondelli, H. D. Pfister, E. Şaşoğlu and R. L. Urbanke, Reed-Muller codes achieve capacity on erasure channels, IEEE Transactions on Information Theory 63(7), 2017
    locator: pp. 4298 to 4316 (main theorem, for the binary erasure channel)
  - paper: doi:10.1109/FOCS57990.2023.00020
    title: E. Abbe and C. Sandon, A proof that Reed-Muller codes achieve Shannon capacity on symmetric channels, IEEE FOCS 2023
    locator: Main theorem (vanishing block error probability on every binary memoryless symmetric channel)
---

A Reed-Muller code $\mathrm{RM}(r, m)$ is the set of value tables of all Boolean polynomials of degree at most $r$ in $m$ variables. The table lists the value at each of the $2^m$ points of $\mathrm{GF}(2)^m$, so the code has length $2^m$. It is a [linear code](/linear-code/) with dimension $\sum_{i \le r} \binom{m}{i}$ and [minimum distance](/minimum-distance/) $2^{m - r}$. The family contains the repetition codes, the even weight codes, the extended [Hamming codes](/hamming-code/) and the augmented [Hadamard codes](/hadamard-code/). It has a short recursive construction, a dual in the same family, and a majority vote decoder from 1954. In 2017 and 2023 it was proved to achieve capacity, first on the erasure channel and then on all binary symmetric memoryless channels.

## Definition

Let $m \ge 1$ and $0 \le r \le m$. A Boolean polynomial in $x_1, \dots, x_m$ is a sum of monomials $x_S = \prod_{i \in S} x_i$ for subsets $S \subseteq \{1, \dots, m\}$, with $x_\emptyset = 1$. Because $x_i^2 = x_i$ on GF(2), no exponent above 1 is needed, and each function $\mathrm{GF}(2)^m \to \mathrm{GF}(2)$ is exactly one such polynomial, its algebraic normal form. Its degree is the largest $|S|$ with a nonzero coefficient. Fix an order $P_1, \dots, P_{2^m}$ of the points of $\mathrm{GF}(2)^m$. Then

$$\mathrm{RM}(r, m) = \{\, (f(P_1), \dots, f(P_{2^m})) : f \text{ a Boolean polynomial of degree} \le r \,\}.$$

**Parameters.** $\mathrm{RM}(r, m)$ is a binary linear code with

$$n = 2^m, \qquad k = \sum_{i=0}^{r} \binom{m}{i}, \qquad d = 2^{m - r}.$$

The value tables of the monomials $x_S$ with $|S| \le r$ form a generator matrix. They are independent because the algebraic normal form is unique.

The table gives the parameters for $m = 5$ and $m = 7$. It was made by the implementation; the tests check $k$ and $d$ on every codeword for $m \le 5$, $r \le 2$ and for all $r$ when $m \le 4$.

| $r$ | $\mathrm{RM}(r, 5)$ | rate | $\mathrm{RM}(r, 7)$ | rate |
|---|---|---|---|---|
| 0 | $[32, 1, 32]$ | 0.0312 | $[128, 1, 128]$ | 0.0078 |
| 1 | $[32, 6, 16]$ | 0.1875 | $[128, 8, 64]$ | 0.0625 |
| 2 | $[32, 16, 8]$ | 0.5000 | $[128, 29, 32]$ | 0.2266 |
| 3 | $[32, 26, 4]$ | 0.8125 | $[128, 64, 16]$ | 0.5000 |
| 4 | $[32, 31, 2]$ | 0.9688 | $[128, 99, 8]$ | 0.7734 |
| 5 | $[32, 32, 1]$ | 1.0000 | $[128, 120, 4]$ | 0.9375 |
| 6 | | | $[128, 127, 2]$ | 0.9922 |
| 7 | | | $[128, 128, 1]$ | 1.0000 |

### The (u | u + v) construction

Split the points by the value of $x_m$. A polynomial of degree at most $r$ is $f = g + x_m h$, where $g$ has degree at most $r$ and $h$ has degree at most $r - 1$, both in $x_1, \dots, x_{m-1}$. On the half with $x_m = 0$ the table of $f$ is $u = g$, and on the half with $x_m = 1$ it is $u + v$ with $v = h$. So

$$\mathrm{RM}(r, m) = \{\, (u \mid u + v) : u \in \mathrm{RM}(r, m - 1), \; v \in \mathrm{RM}(r - 1, m - 1) \,\},$$

with $\mathrm{RM}(0, m)$ the repetition code, $\mathrm{RM}(m, m) = \mathrm{GF}(2)^{2^m}$ and $\mathrm{RM}(-1, m) = \{0\}$. This is the Plotkin $(u \mid u + v)$ construction. It gives the distance by induction: a word $(u \mid u + v)$ with $v \ne 0$ has weight at least $\mathrm{wt}(v) \ge 2^{m - r}$, because $\mathrm{wt}(u) + \mathrm{wt}(u + v) \ge \mathrm{wt}(v)$. A word with $v = 0$ has weight $2\,\mathrm{wt}(u) \ge 2 \cdot 2^{m - 1 - r}$. The monomial $x_1 x_2 \cdots x_r$ has weight exactly $2^{m - r}$, so the bound is reached.

### Duality

$$\mathrm{RM}(r, m)^\perp = \mathrm{RM}(m - r - 1, m) \quad (0 \le r < m).$$

The dimensions add up to $\sum_{i \le r} \binom{m}{i} + \sum_{i \le m - r - 1} \binom{m}{i} = 2^m$. For a monomial $x_S$ with $|S| \le r$ and $x_T$ with $|T| \le m - r - 1$, the product $x_{S \cup T}$ has degree at most $m - 1$. A polynomial of degree less than $m$ has even weight, since the coefficient of $x_1 \cdots x_m$ is the sum of the table over all points. So the inner product is 0, and the two codes are orthogonal with complementary dimensions. In particular $\mathrm{RM}(r, 2r + 1)$ is self-dual.

### Minimum weight words

The words of weight $2^{m - r}$ are the indicator vectors of the affine subspaces of dimension $m - r$ in $\mathrm{GF}(2)^m$. Their number is

$$A_{2^{m-r}} = 2^r \prod_{i=0}^{m-r-1} \frac{2^{m-i} - 1}{2^{m-r-i} - 1}.$$

For $\mathrm{RM}(1, 4)$ this is 30 and for $\mathrm{RM}(2, 5)$ it is 620. The tests check the formula against the full weight distributions.

### Decoding

**Reed's algorithm.** Reed decoded $\mathrm{RM}(r, m)$ by majority votes. For each monomial $x_S$ of top degree $r$, its coefficient equals the sum of the codeword over each of the $2^{m - r}$ cosets of the subspace spanned by the coordinates in $S$. These $2^{m-r}$ sums use disjoint sets of positions, so $t$ errors spoil at most $t$ of them, and a majority vote gives the right coefficient while $t < 2^{m - r - 1}$. Subtract the top degree part and repeat with degree $r - 1$. The decoder corrects every pattern of up to $2^{m - r - 1} - 1$ errors, half the distance. See [majority-logic decoding](/majority-logic-decoding/) for the full algorithm and its proof.

**First order codes.** $\mathrm{RM}(1, m)$ has maximum likelihood decoding in $O(n \log n)$ by the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/). HQC uses a repeated $\mathrm{RM}(1, 7)$ decoded this way as the inner code of its concatenated code ([HQC](/hqc/)).

**Recursive decoders.** The $(u \mid u + v)$ form gives recursive soft decision decoders, and list versions of them, which split each step into a decoder for $v$ and a decoder for $u$. This is the same recursion as the successive cancellation decoder of [polar codes](/polar-code/).

### Capacity

For fixed $r$ the rate goes to 0, and for fixed rate the relative distance $2^{-r}$ goes to 0. So RM codes are not asymptotically good. Still, with $r$ chosen so that the rate tends to a constant $R$, they achieve capacity. Kudekar, Kumar, Mondelli, Pfister, Şaşoğlu and Urbanke (2017) proved this for the [binary erasure channel](/binary-erasure-channel/) under maximum a posteriori decoding, with the doubly transitive symmetry of the code and a sharp threshold argument. Abbe and Sandon (2023) proved vanishing block error probability at every rate below capacity on every binary memoryless symmetric channel. Neither proof gives a polynomial time decoder that reaches capacity.

### Generalized Reed-Muller codes

Over GF($q$) the generalized code $\mathrm{RM}_q(r, m)$ is the set of value tables of polynomials of total degree at most $r$ in $m$ variables over GF($q$), at all $q^m$ points. For $r < q$ the Schwartz-Zippel lemma gives relative distance at least $1 - r/q$. For $m = 1$ these are the [Reed-Solomon codes](/reed-solomon-code/) of length $q$. The [low-degree test](/low-degree-test/) checks with few queries whether a table is close to such a codeword, which is a step in the proof of the PCP theorem.

## Examples and non-examples

**$\mathrm{RM}(1, 3)$.** With points $p = 0, \dots, 7$ and $x_{i}$ equal to bit $i - 1$ of $p$, the rows of the generator matrix are

$$1 = 11111111, \quad x_1 = 01010101, \quad x_2 = 00110011, \quad x_3 = 00001111.$$

The message $1 + x_1 + x_2$ gives the codeword $10011001$. This $[8, 4, 4]$ code is the extended Hamming code, and it is self-dual since $r = 1 = (m - 1)/2$.

**Special cases.** $\mathrm{RM}(0, m)$ is the repetition code $[2^m, 1, 2^m]$. $\mathrm{RM}(m - 1, m)$ is the even weight code $[2^m, 2^m - 1, 2]$. $\mathrm{RM}(m - 2, m)$ is the extended Hamming code $[2^m, 2^m - m - 1, 4]$, and its dual $\mathrm{RM}(1, m)$ is the augmented Hadamard code $[2^m, m + 1, 2^{m-1}]$.

**$\mathrm{RM}(2, 5)$.** This self-dual $[32, 16, 8]$ code has the weight distribution

| weight | 0 | 8 | 12 | 16 | 20 | 24 | 32 |
|---|---|---|---|---|---|---|---|
| words | 1 | 620 | 13888 | 36518 | 13888 | 620 | 1 |

All weights are multiples of 4. The tests compute this from all $2^{16}$ codewords.

**Non-example: a cyclic code.** In the natural order of the points, $\mathrm{RM}(r, m)$ is not cyclic. For $\mathrm{RM}(1, 3)$ the cyclic shift of $x_3 = 00001111$ is $10000111$, and its support $\{0, 5, 6, 7\}$ is not an affine plane, so it is not a codeword. But if the position of the zero point is removed and the other points are listed as powers $1, \alpha, \alpha^2, \dots$ of a primitive element of GF($2^m$), the punctured code $\mathrm{RM}^*(r, m)$ is cyclic. For $r = m - 2$ it is the cyclic Hamming code.

**Non-example: the best code for its distance.** RM codes are not always the best codes of their length and distance. At length 64 and distance 16, $\mathrm{RM}(2, 6)$ is $[64, 22, 16]$, while the extended [BCH code](/bch-code/) $[64, 24, 16]$ has two more information bits.

## Related definitions

- [Hadamard code](/hadamard-code/): the first order code $\mathrm{RM}(1, m)$.
- [Hamming code](/hamming-code/): its extension is $\mathrm{RM}(m - 2, m)$.
- [Polar code](/polar-code/): built from the same kernel $\begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}^{\otimes m}$. A polar code keeps the rows of the most reliable synthetic channels, while an RM code keeps the rows of largest weight.
- [Majority-logic decoding](/majority-logic-decoding/): Reed's decoder and its one step and multi step forms for other codes.
- [Reed-Solomon code](/reed-solomon-code/): the case $m = 1$ of the generalized codes.
- [Golay code](/golay-code/): another doubly even self-dual code, of length 24.

## References
