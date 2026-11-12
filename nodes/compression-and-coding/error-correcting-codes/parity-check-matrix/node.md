---
tag: TTGQBS
kind: definition
slug: parity-check-matrix
name: Parity-check matrix
aliases:
- check matrix
- parity check matrix of a linear code
area: compression-and-coding/error-correcting-codes
level: core
summary: An (n - k) x n matrix H of full rank with C = the set of c with H c^T = 0. The least number of dependent columns of H is the minimum distance.
prereqs: [linear-code, generator-matrix, nullspace]
see_also: [syndrome, dual-code, systematic-code, hamming-code, tanner-graph, ldpc-code, singleton-bound, syndrome-decoding-problem]
sources:
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 1 (the parity check matrix, the form [A | I] from a systematic generator matrix, and the minimum distance from the columns of H)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 3, Section 3.1 (the parity-check matrix and G H^T = 0) and Section 3.3 (the minimum distance and the columns of H)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Chapter 2 (parity-check matrices and the minimum distance)
  - book: isbn:9780521782807
    title: W. Cary Huffman and Vera Pless, Fundamentals of Error-Correcting Codes, Cambridge University Press, 2003
    locator: Chapter 1 (generator and parity check matrices)
---

A parity-check matrix of a [linear code](/linear-code/) $C$ is a full rank $(n - k) \times n$ matrix $H$ such that a word $c$ is a codeword exactly when $H c^T = 0$. Each row of $H$ is one linear check, a weighted sum of positions that must be zero. The minimum distance of $C$ is the least number of columns of $H$ that are linearly dependent, so $H$ is the matrix used to design codes, to decode them by [syndrome](/syndrome/), and to draw their [Tanner graph](/tanner-graph/).

## Definition

**Notation.** $C$ is an $[n, k, d]_q$ linear code over $\mathrm{GF}(q)$ with a $k \times n$ [generator matrix](/generator-matrix/) $G$, so $c = m G$. Vectors are rows, and $c^T$ is the column form of $c$.

A **parity-check matrix** of $C$ is an $(n - k) \times n$ matrix $H$ over $\mathrm{GF}(q)$ of rank $n - k$ with

$$C = \{\, c \in \mathrm{GF}(q)^n : H c^T = 0 \,\}.$$

So $C$ is the [null space](/nullspace/) of $H$. A matrix $H$ of rank $n - k$ is a parity-check matrix of $C$ if and only if $G H^T = 0$. *Proof.* If $C$ is the null space of $H$, each row $g_i$ of $G$ has $H g_i^T = 0$, which is $G H^T = 0$. Conversely, $G H^T = 0$ puts all of $C$ in the null space of $H$. By the [rank-nullity theorem](/rank-nullity-theorem/) the null space has dimension $n - (n - k) = k = \dim C$, so the two are equal. $\blacksquare$

The rows of $H$ span the [dual code](/dual-code/) $C^\perp$, so $H$ is a generator matrix of $C^\perp$. As with $G$, the parity-check matrices of $C$ are exactly the matrices $A H$ with $A$ an invertible $(n - k) \times (n - k)$ matrix.

**From a systematic generator matrix.** If $G = [I_k \mid P]$ with $P$ of size $k \times (n - k)$, then

$$H = [\, -P^T \mid I_{n-k} \,]$$

is a parity-check matrix. The identity block gives rank $n - k$, and $G H^T = I_k (-P) + P\, I_{n-k} = 0$. Over $\mathrm{GF}(2)$, $-1 = 1$, so $H = [P^T \mid I_{n-k}]$. Over other fields the minus sign matters. If $G$ is not in this form, row reduce it and permute columns as on the [systematic code](/systematic-code/) page, or compute a basis of the null space of $G$ directly.

**The minimum distance from the columns.** Write $h_1, \ldots, h_n$ for the columns of $H$. For any word $c$,

$$H c^T = c_1 h_1 + c_2 h_2 + \cdots + c_n h_n .$$

**Theorem.** Let $C \ne \{0\}$. The minimum distance $d$ of $C$ is the least number $w$ such that some $w$ columns of $H$ are linearly dependent. Equivalently, every $d - 1$ columns are independent and some $d$ columns are dependent.

*Proof.* Let $c$ be a nonzero codeword of weight $w$ with support $S$. Then $\sum_{j \in S} c_j h_j = H c^T = 0$ with all $c_j \ne 0$ for $j \in S$, so the $w$ columns in $S$ are dependent. Hence the least number of dependent columns is at most $d$. Conversely, let the columns in a set $S$ with $|S| = w$ be dependent: $\sum_{j \in S} a_j h_j = 0$ with some $a_j \ne 0$. The word $c$ with $c_j = a_j$ on $S$ and $0$ elsewhere is nonzero, has $H c^T = 0$, and has weight at most $w$. So $d \le w$, and the two minima are equal. $\blacksquare$

Two consequences:

- $d \ge 2$ if and only if $H$ has no zero column, and $d \ge 3$ if and only if, in addition, no column is a scalar multiple of another. This is how the [Hamming code](/hamming-code/) is built: take as columns one nonzero vector from each line through the origin.
- Any $n - k + 1$ columns of $H$ live in a space of dimension $n - k$, so they are dependent, and $d \le n - k + 1$. This is the [Singleton bound](/singleton-bound/) for linear codes.

## Examples and non-examples

**Examples.**

- **Hamming code.** For the generator matrix $G = [I_4 \mid P]$ with $P$ rows $110, 011, 111, 101$,

$$H = [\, P^T \mid I_3 \,] = \begin{pmatrix} 1&0&1&1&1&0&0 \\ 1&1&1&0&0&1&0 \\ 0&1&1&1&0&0&1 \end{pmatrix}.$$

The codeword $c = 1011100$ gives $H c^T = (0, 0, 0)^T$. The columns are the seven nonzero vectors of length 3, all different, so no two are dependent and $d \ge 3$. Columns 1, 2 and 4 are $110$, $011$, $101$, and they add to $000$. So $d = 3$, and $1101000$ is a codeword of weight 3.

- **The minus sign over GF(3).** The tetracode has $G = \begin{pmatrix} 1&0&1&1 \\ 0&1&1&2 \end{pmatrix}$, so $P = \begin{pmatrix} 1&1 \\ 1&2 \end{pmatrix}$ and $-P^T = \begin{pmatrix} 2&2 \\ 2&1 \end{pmatrix}$ modulo 3. Then $H = \begin{pmatrix} 2&2&1&0 \\ 2&1&0&1 \end{pmatrix}$, and both rows of $G$ pass the checks. The matrix $[P^T \mid I_2] = \begin{pmatrix} 1&1&1&0 \\ 1&2&0&1 \end{pmatrix}$, without the sign, gives $1 + 0 + 1 + 0 = 2 \ne 0$ on the first row $1011$ of $G$, so it is not a parity-check matrix of this code. No two columns of $H$ are proportional, and the code has $d = 3$.
- **A repeated column.** $H = \begin{pmatrix} 1&1&0&1 \\ 0&0&1&1 \end{pmatrix}$ has two equal columns, 1 and 2, so the word $1100$ is a codeword and $d = 2$.
- **A zero column.** If column $j$ of $H$ is zero, the unit vector $e_j$ is a codeword of weight 1, and $d = 1$. Position $j$ is never checked.
- **The even weight code.** $H = (1\ 1\ \cdots\ 1)$, one check, is the parity-check matrix of the $[n, n - 1, 2]$ code. Each pair of columns is dependent.

**Non-examples.**

- **Extra rows.** The [LDPC codes](/ldpc-code/) of many standards are given by a check matrix with more rows than $n - k$, or with dependent rows. Such a matrix defines the code as its null space, but it is not a parity-check matrix in the strict sense of rank $n - k$, and its row count is not $n - k$. The extra checks help the iterative decoder.
- **A matrix with $G H^T = 0$ of lower rank.** $H = 0$ satisfies $G H^T = 0$ for each code, but its null space is all of $\mathrm{GF}(q)^n$. The rank condition is necessary.
- **The transpose.** A parity-check matrix multiplies the received word as a column, $H r^T$. Some books write vectors as columns and use $H r$; mixing the two conventions gives the wrong shape, or, for a square case, the wrong code.

## Related definitions

- [Generator matrix](/generator-matrix/): $G$ with $G H^T = 0$.
- [Syndrome](/syndrome/): $s = H r^T$ for a received word $r$. It is zero exactly on codewords.
- [Dual code](/dual-code/): the row space of $H$.
- [Systematic code](/systematic-code/): the form $G = [I_k \mid P]$ and $H = [-P^T \mid I_{n-k}]$.
- [Tanner graph](/tanner-graph/): the bipartite graph of $H$, with a node for each position and a node for each row.
- [Syndrome decoding problem](/syndrome-decoding-problem/): the cryptographic problem of finding a low weight $e$ with $H e^T = s$ for a random $H$.

## References
