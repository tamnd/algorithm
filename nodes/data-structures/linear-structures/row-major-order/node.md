---
tag: K2G7GN
kind: concept
slug: row-major-order
name: Row-major and column-major order
aliases:
- Row-major order
area: data-structures/linear-structures
level: intro
summary: Two ways of storing a two dimensional array in linear memory, either row by row or column by column.
prereqs: [random-access-machine]
see_also: [array, locality-of-reference, memory-hierarchy, blocked-matrix-multiplication, cache-oblivious-matrix-multiplication, z-order-curve, sparse-matrix, compressed-sparse-row]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.1.2 (Matrices)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.6 (Arrays and orthogonal lists), the sequential allocation of a matrix in lexicographic order of the indices
  - url: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
    title: ISO/IEC 9899:2011 committee draft N1570 (the C11 standard)
    locator: Section 6.5.2.1 (Array subscripting), paragraph 3
  - url: https://numpy.org/doc/stable/reference/arrays.ndarray.html
    title: NumPy reference, The N-dimensional array (ndarray)
    locator: Section Internal memory layout of an ndarray (strides, C order and Fortran order)
---

Row-major order and column-major order are the two standard ways to store a multidimensional [array](/array/) in the one-dimensional memory of a [random-access machine](/random-access-machine/). In row-major order the rows are stored one after the other, so the last index changes fastest; in column-major order the columns are stored one after the other, so the first index changes fastest. Both give the address of any entry in $O(1)$ time by a linear formula, and the choice decides which loops over the array read memory in sequence and so make good use of the cache. C, C++ and NumPy use row-major order by default; Fortran, MATLAB, R and Julia use column-major order.

## In plain words

Memory is one long row of numbered boxes, but a table has rows and columns. To put a table in memory you must choose an order. One choice is to copy the first row, then the second row after it, and so on. The other choice is to copy the first column, then the second column, and so on.

With either choice, a short calculation turns a row number and a column number into the number of the box, so any entry can be found at once. The choice matters for speed. A computer reads memory in small blocks of neighbouring boxes. If a program walks the table in the same order as it is stored, each block it reads is used fully. If it walks the other way, it can read a new block for every single entry.

## The idea

Let $A$ be an $m \times n$ matrix with 0-based indices $0 \le i < m$ and $0 \le j < n$, stored in a block of $mn$ consecutive cells that starts at address $a$, each entry taking $s$ bytes.

**Row-major order** puts the entry $A[i][j]$ at

$$\text{addr}_R(i, j) = a + s\,(i\,n + j).$$

**Column-major order** puts it at

$$\text{addr}_C(i, j) = a + s\,(i + j\,m).$$

The map $(i, j) \mapsto i n + j$ is a bijection from $\{0, \dots, m-1\} \times \{0, \dots, n-1\}$ onto $\{0, \dots, mn - 1\}$. Proof: for $0 \le j < n$ the value $q = i n + j$ satisfies $0 \le q \le (m-1)n + n - 1 = mn - 1$; and by the division algorithm each $q$ in that range has exactly one pair $i = \lfloor q / n \rfloor$, $j = q \bmod n$ with $q = i n + j$ and $0 \le j < n$. The same argument with the roles of $i$ and $j$ exchanged shows that $(i, j) \mapsto i + j m$ is a bijection. So each scheme uses exactly $mn$ cells, with no gap and no overlap.

The step from one entry to the next along a dimension is its *stride*. In row-major order, moving one column to the right adds $s$ bytes and moving one row down adds $s\,n$ bytes; in column-major order the strides are $s\,m$ and $s$. Storing $A$ in column-major order puts every entry at the same place as storing the transpose $A^{\mathsf T}$ in row-major order, because $\text{addr}_C(i, j) = a + s\,(j\,m + i)$ is the row-major address of entry $(j, i)$ of the $n \times m$ matrix $A^{\mathsf T}$.

**More dimensions.** For an array of shape $n_1 \times n_2 \times \dots \times n_d$ and an index $(i_1, \dots, i_d)$ with $0 \le i_k < n_k$, the row-major offset (in entries) is

$$\sum_{k=1}^{d} i_k \prod_{l=k+1}^{d} n_l = (\cdots((i_1 n_2 + i_2) n_3 + i_3) \cdots ) n_d + i_d,$$

which is the order of the index tuples by the lexicographic order, and the column-major offset is $\sum_{k=1}^{d} i_k \prod_{l=1}^{k-1} n_l$. The nested form on the right computes the offset with $d - 1$ multiplications and $d - 1$ additions. A compiler for a fixed shape folds the products into constant strides.

**Locality.** Memory moves between the levels of the [memory hierarchy](/memory-hierarchy/) in blocks of $B$ consecutive entries. In the [external-memory model](/external-memory-model/), reading all $mn$ entries of a row-major matrix in row order touches each block once, so it costs at most $\lceil mn / B \rceil + 1$ block transfers (the $+1$ covers a start that is not at a block boundary). Reading it in column order, with $n \ge B$ and a cache of $C \le m - 1$ blocks under least-recently-used replacement, misses on every access: two entries of the same column are at least $n \ge B$ cells apart, so they lie in different blocks, and between two accesses to the same block the walk touches the $m - 1$ other rows of the column, which are $m - 1 \ge C$ distinct other blocks, so the block has been evicted. That is $mn$ transfers, a factor of about $B$ more. This is the [locality of reference](/locality-of-reference/) effect behind the advice to put the loop over the last index innermost in C and the loop over the first index innermost in Fortran.

## Examples

**A small matrix.** The $2 \times 3$ matrix with rows $(1, 2, 3)$ and $(4, 5, 6)$ is stored as $1, 2, 3, 4, 5, 6$ in row-major order and as $1, 4, 2, 5, 3, 6$ in column-major order. With 8-byte entries, its row-major strides are 24 bytes for a row and 8 bytes for a column.

**An address.** Take a $3 \times 4$ matrix of 8-byte entries that starts at address 1000. The entry $A[1][2]$ is at $1000 + 8 \cdot (1 \cdot 4 + 2) = 1048$ in row-major order and at $1000 + 8 \cdot (1 + 2 \cdot 3) = 1056$ in column-major order.

**Three dimensions.** For shape $2 \times 3 \times 4$ and index $(1, 0, 2)$, the row-major offset is $(1 \cdot 3 + 0) \cdot 4 + 2 = 14$, and the column-major offset is $1 + 2 \cdot (0 + 3 \cdot 2) = 13$. Going back, offset 14 gives $i_3 = 14 \bmod 4 = 2$, then $\lfloor 14 / 4 \rfloor = 3$ gives $i_2 = 3 \bmod 3 = 0$ and $i_1 = \lfloor 3 / 3 \rfloor = 1$.

**Loop order.** A $1024 \times 1024$ row-major matrix of 8-byte numbers, read row by row with 64-byte cache lines ($B = 8$), needs $1024 \cdot 1024 / 8 = 131072$ line loads when the matrix starts at a line boundary. Read column by column with a cache of fewer than 1023 lines, it needs a load for each of the $1048576$ entries.

**Non-example: an array of row pointers.** A Java `int[][]`, or a C array of pointers to separately allocated rows, is not stored in row-major order. Each row is a contiguous block, but the rows can be anywhere in memory, and reaching $A[i][j]$ needs one extra memory read, of the [pointer](/pointer/) to row $i$. Such a table (an Iliffe vector) allows rows of different lengths, but the formula $a + s(in + j)$ does not apply to it.

## Where it is used

- **Languages and libraries.** The C standard (Section 6.5.2.1, paragraph 3) states that arrays are stored in row-major order, with the last subscript changing fastest. Fortran stores arrays in column-major order, and so do the libraries built in it, such as BLAS and LAPACK; NumPy supports both and calls them C order and Fortran order.
- **Matrix algorithms.** [Blocked matrix multiplication](/blocked-matrix-multiplication/) and [cache-oblivious matrix multiplication](/cache-oblivious-matrix-multiplication/) reorder the work so that each block of the matrix is used many times while it is in the cache, whatever the order of storage.
- **Other layouts.** The [Z-order curve](/z-order-curve/) interleaves the bits of $i$ and $j$, which keeps entries that are near in both directions near in memory. [Sparse matrices](/sparse-matrix/) store only the nonzero entries, for example in [compressed sparse row](/compressed-sparse-row/) form, which is the row-major idea applied to the list of nonzeros.
- **Images and tensors.** Images are stored row by row (scan lines), and tensor libraries describe any layout, including transposed views, by a shape and a vector of strides.

## References
