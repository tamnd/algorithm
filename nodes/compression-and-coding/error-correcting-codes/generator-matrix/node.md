---
tag: ZSJ6JS
kind: definition
slug: generator-matrix
name: Generator matrix
aliases:
- generator matrix of a linear code
area: compression-and-coding/error-correcting-codes
level: core
summary: A k x n matrix of rank k whose rows form a basis of a linear code. The encoder maps a message m to the codeword c = m G.
prereqs: [linear-code, linear-independence]
see_also: [parity-check-matrix, systematic-code, dual-code, reduced-row-echelon-form, gaussian-elimination-modular, reed-muller-code, product-codes, rank]
sources:
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 1 (the generator matrix of a linear code and encoding)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 3, Section 3.1 (the generator matrix, encoding as u G, and the systematic form)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Chapter 2 (linear codes, generator matrices and encoding)
  - book: isbn:9780521782807
    title: W. Cary Huffman and Vera Pless, Fundamentals of Error-Correcting Codes, Cambridge University Press, 2003
    locator: Chapter 1 (generator and parity check matrices, equivalence of codes)
---

A generator matrix of a [linear code](/linear-code/) $C$ is a $k \times n$ matrix $G$ whose rows form a basis of $C$. It encodes a message $m$ of $k$ symbols as the codeword $c = m G$, so the code is the row space of $G$. One code has many generator matrices, one for each choice of basis, and each one gives a different map from messages to codewords.

## Definition

**Notation.** $C$ is an $[n, k, d]_q$ linear code over the finite field $\mathrm{GF}(q)$, with rate $R = k/n$. Vectors are rows. $\mathrm{GF}(q)^k$ is the set of messages.

A **generator matrix** of $C$ is a $k \times n$ matrix $G$ over $\mathrm{GF}(q)$ with

1. each row of $G$ in $C$, and
2. $\mathrm{rank}(G) = k$, so the rows are [linearly independent](/linear-independence/).

Then the rows are a basis of $C$, and

$$C = \{\, m G : m \in \mathrm{GF}(q)^k \,\}.$$

The **encoder** of $G$ is the map $m \mapsto m G$. It is linear and one to one, because $m G = m' G$ gives $(m - m') G = 0$, and independent rows force $m = m'$. So it is a bijection from $\mathrm{GF}(q)^k$ onto $C$. It costs $k n$ multiplications and additions in $\mathrm{GF}(q)$, or $k (n - k)$ for a [systematic](/systematic-code/) $G = [I_k \mid P]$, where the first $k$ symbols are the message itself.

**All generator matrices of one code.** If $G$ and $G'$ generate the same code, then each row of $G'$ is a combination of the rows of $G$, so $G' = A G$ for a $k \times k$ matrix $A$, and $A$ is invertible because both have rank $k$. Conversely, $A G$ generates $C$ for each invertible $A$. So the generator matrices of $C$ are exactly the matrices $A G$ with $A \in \mathrm{GL}(k, q)$, and there are

$$|\mathrm{GL}(k, q)| = (q^k - 1)(q^k - q)(q^k - q^2) \cdots (q^k - q^{k-1})$$

of them. For $k = 4$ and $q = 2$ this is $15 \cdot 14 \cdot 12 \cdot 8 = 20160$.

**What changes the code.** Row operations (swap two rows, scale a row by a nonzero element, add a multiple of one row to another) multiply $G$ on the left by an invertible matrix, so they keep the code and change only the encoder. A permutation of the columns changes the code to an equivalent code, with the same weights. The [reduced row echelon form](/reduced-row-echelon-form/) of $G$ is the same for all generator matrices of $C$, so it is a canonical generator matrix. [Gaussian elimination over GF(q)](/gaussian-elimination-modular/) finds it in $O(k^2 n)$ field operations.

**Link to the parity-check matrix.** A $(n - k) \times n$ matrix $H$ of rank $n - k$ is a [parity-check matrix](/parity-check-matrix/) of $C$ exactly when $G H^T = 0$. The rows of $H$ then generate the [dual code](/dual-code/) $C^\perp$, so a generator matrix of $C^\perp$ is a parity-check matrix of $C$ and the reverse.

**Recovering the message.** The receiver who has a codeword $c$ needs the $m$ with $m G = c$. If $G = [I_k \mid P]$, then $m$ is the first $k$ symbols of $c$. Otherwise pick $k$ independent columns of $G$, with index set $S$; then $m = c_S (G_S)^{-1}$, where $c_S$ and $G_S$ keep only the columns in $S$.

## Examples and non-examples

**Examples.**

- **Hamming code.** The binary $[7, 4, 3]$ [Hamming code](/hamming-code/) has the systematic generator matrix

$$G = \begin{pmatrix} 1&0&0&0&1&1&0 \\ 0&1&0&0&0&1&1 \\ 0&0&1&0&1&1&1 \\ 0&0&0&1&1&0&1 \end{pmatrix}.$$

The message $m = 1011$ is the sum of rows 1, 3 and 4: $1000110 + 0010111 + 0001101 = 1011100$. The first four symbols are the message.

- **The same code, another encoder.** The rows $1100101$, $0110100$, $1111111$, $0001101$ span the same 16 codewords; row reduction of this matrix gives the matrix $G$ above. With this matrix the message $1011$ becomes $1100101 + 1111111 + 0001101 = 0010111$. That is a different codeword (the third row of $G$), so a sender and a receiver must agree on the matrix, not only on the code.
- **Repetition and parity codes.** $G = (1\ 1\ \cdots\ 1)$ generates the $[n, 1, n]$ [repetition code](/repetition-code/). $G = [I_{n-1} \mid \mathbf{1}^T]$, where $\mathbf{1}$ is the all ones row, generates the $[n, n - 1, 2]$ even weight code.
- **Reed-Solomon codes.** For distinct points $\alpha_1, \ldots, \alpha_n$ of $\mathrm{GF}(q)$, the $k \times n$ Vandermonde matrix with entry $\alpha_j^{\,i}$ in row $i = 0, \ldots, k - 1$ and column $j$ is a generator matrix of a [Reed-Solomon code](/reed-solomon-code/). Row $i$ is the evaluation of $x^i$.
- **First order Reed-Muller code.** The all ones row together with the $r$ rows of the binary expansions of $0, 1, \ldots, 2^r - 1$ form a generator matrix of the $[2^r, r + 1, 2^{r-1}]$ [Reed-Muller code](/reed-muller-code/) of order 1.
- **Product codes.** If $G_1$ and $G_2$ generate $C_1$ and $C_2$, the Kronecker product $G_1 \otimes G_2$ generates the [product code](/product-codes/), with parameters $[n_1 n_2, k_1 k_2, d_1 d_2]$.

**Non-examples.**

- **Dependent rows.** Over $\mathrm{GF}(2)$, the rows $110$, $011$, $101$ add to $000$, so the matrix has rank 2. It spans the even weight code of length 3, which has 4 codewords, not 8, and the map $m \mapsto m G$ sends two messages to each codeword. It is not a generator matrix. Over $\mathrm{GF}(3)$ the same integer matrix has determinant 2, which is not 0, so there it is a generator matrix of all of $\mathrm{GF}(3)^3$. Rank depends on the field.
- **Rows that do not span.** The single row $1100$ is a codeword of $\{0000, 1100, 0011, 1111\}$, but it generates only a subcode. A generator matrix needs $k$ rows.
- **A list of all codewords.** The $q^k \times n$ matrix of all codewords spans $C$, but its rows are dependent. A generator matrix stores $k n$ symbols instead of $q^k n$.

## Related definitions

- [Linear code](/linear-code/): the row space of $G$.
- [Parity-check matrix](/parity-check-matrix/): the matrix $H$ with $G H^T = 0$ and $C = \{\, c : H c^T = 0 \,\}$.
- [Systematic code](/systematic-code/): the generator matrix $[I_k \mid P]$, found by row reduction and, if needed, a column permutation.
- [Dual code](/dual-code/): the code that $H$ generates.
- [Reduced row echelon form](/reduced-row-echelon-form/) and [rank](/rank/): the linear algebra that tests whether a matrix is a generator matrix and puts it in a canonical form.

## References
