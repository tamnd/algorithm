---
tag: KNDK1C
kind: definition
slug: simplex-code
name: Simplex code
aliases:
- maximal-length code
- dual Hamming code
area: compression-and-coding/error-correcting-codes
level: advanced
summary: The dual of the Hamming code, a [2^r - 1, r, 2^(r - 1)] linear code in which every nonzero codeword has weight 2^(r - 1). It meets the Griesmer and Plotkin bounds.
prereqs: [hamming-code, dual-code]
see_also: [griesmer-bound, plotkin-bound, reed-muller-code, hadamard-code, linear-feedback-shift-register, walsh-hadamard-transform, macwilliams-identity, generator-matrix]
sources:
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 1 (the dual of the Hamming code, the simplex code) and Chapter 14 (first order Reed-Muller codes and pseudo-noise sequences)
  - book: isbn:9780521782807
    title: W. Cary Huffman and Vera Pless, Fundamentals of Error-Correcting Codes, Cambridge University Press, 2003
    locator: Chapter 1 (Hamming codes and their duals, the simplex codes) and Chapter 2 (the Griesmer bound)
  - paper: "J. H. Griesmer, A bound for error-correcting codes, IBM Journal of Research and Development 4(5), 1960, pages 532 to 542"
    title: A bound for error-correcting codes
    locator: The bound n >= sum of ceil(d/2^i) for binary linear codes, met with equality by the simplex codes
  - paper: "M. Plotkin, Binary codes with specified minimum distance, IRE Transactions on Information Theory 6(4), 1960, pages 445 to 450"
    title: Binary codes with specified minimum distance
    locator: The bound on the number of codewords when 2d > n
  - paper: "A. Bonisoli, Every equidistant linear code is a sequence of dual Hamming codes, Ars Combinatoria 18, 1984, pages 181 to 186"
    title: Every equidistant linear code is a sequence of dual Hamming codes
    locator: The main theorem, the classification of linear codes with one nonzero weight
---

A simplex code is the [dual code](/dual-code/) of a [Hamming code](/hamming-code/): a binary [linear code](/linear-code/) of length $2^r - 1$ and dimension $r$ whose generator matrix has every nonzero column of length $r$ once. Every nonzero codeword has the same weight $2^{r - 1}$, so any two codewords are at the same distance, and the $2^r$ codewords are the vertices of a regular simplex. The code meets the [Griesmer bound](/griesmer-bound/) and the [Plotkin bound](/plotkin-bound/), and its nonzero codewords are the cyclic shifts of one period of a maximal-length shift register sequence.

## Definition

**Notation.** $\mathrm{GF}(q)$ is the finite field with $q$ elements. An $[n, k, d]_q$ code has length $n$, dimension $k$ and minimum distance $d$; the subscript is left out for $q = 2$. Vectors are rows, $c = m G$ for a generator matrix $G$, and $H c^T = 0$ for a parity-check matrix $H$. The rate is $R = k/n$, and $\mathrm{wt}$ is the Hamming weight.

**Binary simplex code.** Let $r \ge 2$ and $n = 2^r - 1$. Let $G$ be an $r \times n$ binary matrix whose columns $g_1, \ldots, g_n$ are the nonzero vectors of $\mathrm{GF}(2)^r$, each once. The simplex code of order $r$ is

$$\mathcal{S}_r = \{\, m G : m \in \mathrm{GF}(2)^r \,\}.$$

$G$ is a parity-check matrix of the Hamming code $\mathcal{H}_r$, so $\mathcal{S}_r = \mathcal{H}_r^\perp$. The rows of $G$ are independent (the unit vectors are among the columns), so $k = r$.

**Constant weight.** For a message $m \ne 0$, position $j$ of $c = m G$ is the inner product $m \cdot g_j$. The map $x \mapsto m \cdot x$ is a nonzero linear form on $\mathrm{GF}(2)^r$, so it is 1 on exactly half of the $2^r$ vectors, $2^{r - 1}$ of them, and the zero vector is not among these. The columns are all the nonzero vectors, so

$$\mathrm{wt}(m G) = 2^{r - 1} \quad \text{for every } m \ne 0.$$

So $\mathcal{S}_r$ is a $[2^r - 1,\ r,\ 2^{r - 1}]$ code with weight distribution $A_0 = 1$, $A_{2^{r-1}} = 2^r - 1$. Since the code is linear, $d(x, y) = \mathrm{wt}(x - y) = 2^{r - 1}$ for all distinct codewords: the code is *equidistant*. Map each bit $b$ to the real number $(-1)^b$; the $2^r$ codewords become points at equal Euclidean distance from each other, the vertices of a regular simplex, which gives the code its name.

**Optimal by two bounds.**

- *Griesmer.* A binary linear $[n, k, d]$ code has $n \ge \sum_{i = 0}^{k - 1} \lceil d / 2^i \rceil$. For $k = r$ and $d = 2^{r - 1}$ the sum is $2^{r - 1} + 2^{r - 2} + \cdots + 1 = 2^r - 1 = n$, so the bound holds with equality.
- *Plotkin.* A binary code with $2d > n$ has at most $2 \lfloor d / (2d - n) \rfloor$ codewords. Here $2d - n = 1$, so the bound is $2 \cdot 2^{r - 1} = 2^r$, the number of codewords of $\mathcal{S}_r$.

**$q$-ary simplex code.** Over $\mathrm{GF}(q)$, take as the columns of $G$ one nonzero vector from each one dimensional subspace of $\mathrm{GF}(q)^r$, that is, the parity-check matrix of the $q$-ary Hamming code. The code is a $[(q^r - 1)/(q - 1),\ r,\ q^{r - 1}]_q$ code, and every nonzero codeword has weight $q^{r - 1}$: a nonzero linear form vanishes on $q^{r - 1} - 1$ nonzero vectors, which lie on $(q^{r - 1} - 1)/(q - 1)$ of the chosen lines, so the weight is $(q^r - 1)/(q - 1) - (q^{r - 1} - 1)/(q - 1) = q^{r - 1}$.

## Examples and non-examples

**Examples.**

- **$r = 3$.** With the columns $1, \ldots, 7$ in binary,

  $$G = \begin{pmatrix} 0&0&0&1&1&1&1 \\ 0&1&1&0&0&1&1 \\ 1&0&1&0&1&0&1 \end{pmatrix}.$$

  The message $m = 101$ gives the sum of rows 1 and 3, $c = 1011010$, of weight 4. All 7 nonzero codewords have weight 4, so $\mathcal{S}_3$ is a $[7, 3, 4]$ code, the dual of the $[7, 4, 3]$ Hamming code.
- **Weight distributions.** $\mathcal{S}_2$: three words of weight 2 ($\{011, 101, 110\}$, the even weight code of length 3). $\mathcal{S}_3$: seven of weight 4. $\mathcal{S}_4$: fifteen of weight 8. $\mathcal{S}_5$: thirty-one of weight 16. The implementation checks these for $r$ up to 5.
- **Maximal-length sequences.** A [linear feedback shift register](/linear-feedback-shift-register/) with the primitive feedback polynomial $x^3 + x + 1$, that is $s_{i + 3} = s_{i + 1} + s_i$, started from $001$, outputs the period $0010111$. Its 7 cyclic shifts and the zero word are closed under addition and form a code equivalent to $\mathcal{S}_3$: the 7 windows of 3 consecutive bits are the 7 nonzero vectors of $\mathrm{GF}(2)^3$. This is why the simplex code is also called the maximal-length code. The same sequences are the m-sequences used in spread spectrum and, combined with nonlinear parts, in [LFSR](/lfsr/) based stream ciphers.
- **First order Reed-Muller code.** Put a 0 in front of each codeword of $\mathcal{S}_r$ and add the complements: the result is the [Reed-Muller code](/reed-muller-code/) $\mathrm{RM}(1, r)$, a $[2^r,\ r + 1,\ 2^{r - 1}]$ code. For $r = 3$ it is the $[8, 4, 4]$ extended Hamming code, with weights 0 (once), 4 (14 times) and 8 (once). For $r = 5$ it is the $[32, 6, 16]$ code that the Mariner probes to Mars used around 1970. Its fast decoder uses the [Walsh-Hadamard transform](/walsh-hadamard-transform/).
- **Ternary.** For $q = 3$ and $r = 2$, the simplex code is the $[4, 2, 3]_3$ tetracode: all 8 nonzero codewords have weight 3. It is equal to its dual, the ternary Hamming code with $r = 2$. For $r = 3$ it is a $[13, 3, 9]_3$ code with 26 codewords of weight 9.

**Non-examples.**

- **Not every constant weight code is a simplex code.** Repeat each column of $G$ twice: the $[14, 3, 8]$ code also has one nonzero weight. Bonisoli proved in 1984 that every linear code with one nonzero weight is, up to equivalence and zero columns, a simplex code with each column repeated the same number of times. So the simplex code is the shortest one.
- **Constant weight code in the other sense.** A "constant weight code" in combinatorics is any set of words of one weight, usually not linear and not containing 0. The simplex code contains 0, so it is a linear code with one *nonzero* weight.
- **The Hadamard code.** The rows of the Sylvester Hadamard matrix of order $2^r$, written with 0 for $+1$ and 1 for $-1$, are the words $(m \cdot x)_{x \in \mathrm{GF}(2)^r}$, so they are the codewords of $\mathcal{S}_r$ with a 0 in front for $x = 0$. A [Hadamard code](/hadamard-code/) is built from these rows, in some texts with their complements too. It is not the simplex code: its length is $2^r$, not $2^r - 1$, and without the complements one position is always 0.
- **Large rate.** The rate $r / (2^r - 1)$ goes to 0, so the simplex code is never used for high rate data; it trades rate for a large distance, $d \approx n / 2$.

## Related definitions

- [Hamming code](/hamming-code/) and [dual code](/dual-code/): $\mathcal{S}_r = \mathcal{H}_r^\perp$, and $G$ of one is $H$ of the other.
- [Griesmer bound](/griesmer-bound/) and [Plotkin bound](/plotkin-bound/): the simplex code meets both with equality.
- [MacWilliams identity](/macwilliams-identity/): the weight distribution $1 + (2^r - 1) z^{2^{r-1}}$ of $\mathcal{S}_r$ gives the weight distribution of the Hamming code.
- [Reed-Muller code](/reed-muller-code/): $\mathrm{RM}(1, r)$ is the extended simplex code plus the all ones vector.
- [Hadamard code](/hadamard-code/): a code of length $2^r$ from the rows of a Hadamard matrix, which contains $\mathcal{S}_r$ with a 0 in front.
- [Linear feedback shift register](/linear-feedback-shift-register/): its maximal-length output sequences are the codewords.
- [Generator matrix](/generator-matrix/): the matrix of all nonzero columns that defines the code.

## References
