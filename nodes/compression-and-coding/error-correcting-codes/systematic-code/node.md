---
tag: 9C8353
kind: definition
slug: systematic-code
name: Systematic code
aliases:
- systematic encoding
- systematic linear code
area: compression-and-coding/error-correcting-codes
level: core
summary: A code whose codewords hold the message unchanged in a fixed set of k positions. For a linear code, G = [I_k | P] after a column permutation.
prereqs: [generator-matrix, parity-check-matrix, gaussian-elimination]
see_also: [linear-code, reduced-row-echelon-form, singleton-bound, information-set-decoding, cyclic-code, cyclic-redundancy-check, reed-solomon-code, turbo-code]
sources:
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 3, Section 3.1 (linear systematic block codes, the generator matrix [P | I_k] with the message in the last k positions, and its parity-check matrix)
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 1 (the standard form of the generator matrix, information sets and equivalent codes) and Chapter 11 (MDS codes)
  - book: isbn:9780521782807
    title: W. Cary Huffman and Vera Pless, Fundamentals of Error-Correcting Codes, Cambridge University Press, 2003
    locator: Chapter 1 (standard form, information sets and permutation equivalence)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Chapter 2 (systematic generator matrices)
---

A systematic code is a block code whose codewords carry the message unchanged in a fixed set of $k$ positions, with the check symbols in the other $n - k$ positions. For a [linear code](/linear-code/) this means a [generator matrix](/generator-matrix/) of the form $G = [I_k \mid P]$, after a permutation of the columns. Every linear code is equivalent to a systematic one, because row reduction always finds $k$ independent columns, but a given code need not be systematic on its first $k$ positions.

## Definition

**Notation.** $C$ is an $[n, k, d]_q$ linear code over $\mathrm{GF}(q)$ with generator matrix $G$, so $c = m G$, and parity-check matrix $H$, so $H c^T = 0$. Vectors are rows. For a set $S$ of positions, $c_S$ is $c$ restricted to $S$, and $G_S$ is $G$ restricted to the columns in $S$.

An **information set** of $C$ is a set $S$ of $k$ positions such that the map $c \mapsto c_S$ is a bijection from $C$ onto $\mathrm{GF}(q)^k$. For a linear code, $c_S = m\, G_S$, so $S$ is an information set if and only if the $k$ columns of $G_S$ are linearly independent. The other $n - k$ positions are *check* (or redundancy) positions.

An encoder is **systematic** on $S$ when the message appears in the codeword at the positions $S$: $c_S = m$. A code is **systematic on its first $k$ positions** when $\{1, \ldots, k\}$ is an information set; then its generator matrix in [reduced row echelon form](/reduced-row-echelon-form/) is

$$G = [\, I_k \mid P \,], \qquad c = (m,\ m P),$$

and $H = [\, -P^T \mid I_{n-k} \,]$ is a [parity-check matrix](/parity-check-matrix/) (over $\mathrm{GF}(2)$, $H = [P^T \mid I_{n-k}]$). Some books, Lin and Costello among them, put the message last and write $G = [P \mid I_k]$. The two forms differ by a cyclic shift of the positions.

**Every linear code has an information set.** $G$ has rank $k$, so some $k$ of its columns are independent. [Gauss-Jordan elimination](/gaussian-elimination/) finds them: it reduces $G$ to reduced row echelon form, and the pivot columns $S$ form an information set, with $G_S = I_k$ in the reduced matrix. Move the columns of $S$ to the front. The result is $[I_k \mid P]$ for a permutation equivalent code, with the same $n$, $k$, $d$ and weight distribution. This costs $O(k^2 n)$ operations in $\mathrm{GF}(q)$. If the first $k$ columns of $G$ are independent, the pivots are $1, \ldots, k$ and no permutation is needed.

**Which sets are information sets.** A set $S$ of $k$ positions fails to be an information set exactly when some nonzero codeword is zero on all of $S$, that is, has its support inside the other $n - k$ positions. Hence:

- If $d > n - k$, every $k$ set is an information set. By the [Singleton bound](/singleton-bound/) $d \le n - k + 1$, so this is the case $d = n - k + 1$ of MDS codes, such as [Reed-Solomon codes](/reed-solomon-code/). A Reed-Solomon codeword is fixed by any $k$ of its symbols.
- Each codeword of weight $w \le n - k$ spoils every $k$ set inside the complement of its support.

## Examples and non-examples

**Examples.**

- **Hamming code.** The binary $[7, 4, 3]$ [Hamming code](/hamming-code/) with $P$ rows $110, 011, 111, 101$ has $G = [I_4 \mid P]$. The message $1011$ becomes $1011\,100$: the message, then the three checks $m P = 100$. Of the $\binom{7}{4} = 35$ sets of four positions, 28 are information sets. The other 7 are the complements of the supports of the 7 codewords of weight 3.
- **Row reduction finds the form.** The rows $1100101$, $0110100$, $1111111$, $0001101$ generate the same Hamming code without the form $[I_4 \mid P]$. Gauss-Jordan elimination over $\mathrm{GF}(2)$ gives pivots in columns 1 to 4 and returns the matrix $G$ of the first example, with no permutation.
- **Reed-Solomon codes.** A $[7, 3, 5]_8$ Reed-Solomon code is MDS, so all 35 sets of three positions are information sets. The standards use systematic encoders, so a receiver that sees no error reads the data directly.
- **Systematic encoding by division.** For a [cyclic code](/cyclic-code/) with generator polynomial $g(x)$ of degree $n - k$, the codeword $x^{n-k} m(x) - (x^{n-k} m(x) \bmod g(x))$ has the message in its top $k$ coefficients. A [cyclic redundancy check](/cyclic-redundancy-check/) appends a remainder in exactly this way.
- **The tetracode.** $G = \begin{pmatrix} 1&0&1&1 \\ 0&1&1&2 \end{pmatrix}$ is systematic over $\mathrm{GF}(3)$. Its $d = 3 = n - k + 1$, so each of the 6 pairs of positions is an information set.

**Non-examples.**

- **Not systematic on the first positions.** $C = \{0000, 1100, 0011, 1111\}$ is a $[4, 2, 2]$ code. On positions 1 and 2 its codewords show only $00$ and $11$, so $\{1, 2\}$ is not an information set, and no generator matrix of $C$ starts with $I_2$. The information sets are $\{1, 3\}$, $\{1, 4\}$, $\{2, 3\}$ and $\{2, 4\}$. Row reduction picks $\{1, 3\}$, and after the permutation $(1, 3, 2, 4)$ the code has the generator matrix $\begin{pmatrix} 1&0&1&0 \\ 0&1&0&1 \end{pmatrix}$. This is an equivalent code, not the same code.
- **A non-systematic encoder for a systematic code.** The matrix with rows $1100101$, $0110100$, $1111111$, $0001101$ maps $1011$ to $0010111$, which does not start with $1011$. The code is systematic; the encoder is not.
- **Non-systematic codes in practice.** Feed-forward convolutional codes are usually used in a non-systematic form, which gives a larger free distance for the same memory. A [turbo code](/turbo-code/) uses recursive systematic encoders instead, because the decoder needs the systematic symbols.

## Related definitions

- [Generator matrix](/generator-matrix/) and [parity-check matrix](/parity-check-matrix/): the pair $[I_k \mid P]$ and $[-P^T \mid I_{n-k}]$.
- [Linear code](/linear-code/): permutation equivalence keeps the parameters, so results proved for systematic codes hold for all linear codes.
- [Singleton bound](/singleton-bound/): the bound $d \le n - k + 1$, which is also the bound for which all $k$ sets are information sets.
- [Information set decoding](/information-set-decoding/): guess an information set with no errors, then re-encode. This is the best known generic attack on code-based cryptosystems.

## References
