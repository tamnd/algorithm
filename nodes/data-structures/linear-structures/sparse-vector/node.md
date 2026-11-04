---
tag: E8QPZ3
kind: data-structure
slug: sparse-vector
name: Sparse vector
area: data-structures/linear-structures
level: core
summary: Vector stored as a symbol table of its nonzero entries, making dot products cost proportional to the nonzero count.
prereqs: [hash-table, dictionary, array]
see_also: [dot-product, sparse-matrix, compressed-sparse-row, sparse-matrix-vector-multiplication, pagerank, sequential-search-symbol-table, bit-set]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.5 (Searching Applications), Sparse vectors and the class SparseVector
  - url: https://algs4.cs.princeton.edu/35applications/
    title: Robert Sedgewick and Kevin Wayne, Algorithms, 4th edition, booksite page of Section 3.5 and SparseVector.java
    locator: the part Sparse vectors and matrices
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM (2003)
    locator: Chapter 3 (Sparse Matrices), Section 3.4 (Storage Schemes)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.6 (Arrays and orthogonal lists), the representation of sparse matrices
---

A sparse vector stores a vector $v \in \mathbb{R}^d$ by its nonzero entries only, as a symbol table that maps each index $i$ with $v_i \ne 0$ to $v_i$. With a [hash table](/hash-table/) as the symbol table, reading or writing one entry takes $O(1)$ expected time, the [dot product](/dot-product/) of two sparse vectors takes time proportional to the smaller number of nonzeros, and the space is proportional to the number of nonzeros instead of to $d$. It is the row type of a [sparse matrix](/sparse-matrix/), and it makes a [matrix-vector product](/sparse-matrix-vector-multiplication/) cost time proportional to the nonzeros of the matrix, as in [PageRank](/pagerank/).

## In plain words

Most of the numbers in some long lists are zero. A list of the links from one web page to a billion others has a handful of ones and nearly a billion zeros. Writing all the zeros wastes memory, and adding up products with zeros wastes time.

A sparse vector writes down only the places that are not zero, each with its number, like a short list of "at place 4 the value is 2". To read a place that is not on the list, it answers zero. To multiply two such vectors entry by entry and add up the results, it only looks at the places on the shorter list, because every other product is zero.

## The abstract type

A sparse vector is a vector of a fixed dimension $d$ with these operations:

- `new(d)`: the zero vector of dimension $d$;
- `get(v, i)` and `put(v, i, x)` for $0 \le i < d$: read or write the entry $v_i$;
- `nnz(v)`: the number of nonzero entries;
- `dot(u, w)`: $\sum_i u_i w_i$, for two vectors of the same dimension; also `dot(u, a)` with a dense [array](/array/) $a$;
- `plus(u, w)`, `scale(v, \alpha)` and `norm(v)` $= \sqrt{\mathrm{dot}(v, v)}$.

These are the operations of the class SparseVector of Sedgewick and Wayne.

## Representation

The fields are the dimension $d$ and a symbol table $T$ from integer indices to numbers. Here $T$ is a hash table, so it supports CONTAINS, GET, PUT, DELETE, a size and iteration over its pairs.

**Invariant.**

- (I1) Each key $i$ of $T$ satisfies $0 \le i < d$.
- (I2) Each value stored in $T$ is nonzero.
- (I3) For each $i$ with $0 \le i < d$, the entry $v_i$ is $T[i]$ when $i$ is a key of $T$, and 0 otherwise.

Part (I2) makes $\mathrm{nnz}(v)$ equal to the size of $T$, so the costs below depend on the true number of nonzeros.

## Operations

```pseudo id=main
PUT(v, i, x)                               ▷ 0 ≤ i < v.d
L1  if x = 0 then DELETE(v.T, i)           ▷ keep no zero in T
L2  else T-PUT(v.T, i, x)

GET(v, i)                                  ▷ 0 ≤ i < v.d
L3  if CONTAINS(v.T, i) then return T-GET(v.T, i) else return 0

DOT(u, w)                                  ▷ u.d = w.d
L4  if |u.T| > |w.T| then exchange u and w ▷ loop over the smaller table
L5  s ← 0
L6  for each pair (i, x) in u.T do
L7      s ← s + x · GET(w, i)
L8  return s
```

PUT writes a nonzero value into the table and deletes the index for a zero, so a write of zero frees the entry. GET answers 0 for an index that is not in the table. DOT walks the pairs of the vector with fewer nonzeros and looks up each index in the other. Every term $u_i w_i$ that it skips has $u_i = 0$, so it adds nothing. Each table operation takes $O(1)$ expected time, so PUT and GET take $O(1)$ expected time and DOT takes $O(1 + \min(\mathrm{nnz}(u), \mathrm{nnz}(w)))$ expected time.

```pseudo id=plus
PLUS(u, w)                                 ▷ u.d = w.d, returns a new vector
A1  r ← a copy of u
A2  for each pair (i, x) in w.T do
A3      PUT(r, i, GET(r, i) + x)
A4  return r
DOT-DENSE(u, a)                            ▷ a is an array of length u.d
A5  s ← 0
A6  for each pair (i, x) in u.T do s ← s + x · a[i]
A7  return s
```

PLUS copies $u$ and adds each nonzero of $w$. When $u_i + w_i = 0$, line A3 calls PUT with 0, which removes the index and keeps (I2). The cost is $O(\mathrm{nnz}(u) + \mathrm{nnz}(w))$ expected. DOT-DENSE costs $O(1 + \mathrm{nnz}(u))$, independent of $d$. SCALE by $\alpha \ne 0$ multiplies each stored value; scaling by 0 empties the table.

## Example

Take $d = 10$, $u$ with $u_1 = 0.5$, $u_4 = 2$, $u_7 = -1$, and $w$ with $w_0 = 3$, $w_4 = 1.5$, $w_7 = 2$, $w_9 = 1$. All other entries are 0.

| operation | table after it, or result | work |
|---|---|---|
| $u$ | $\{1: 0.5,\ 4: 2,\ 7: -1\}$ | |
| $w$ | $\{0: 3,\ 4: 1.5,\ 7: 2,\ 9: 1\}$ | |
| GET$(u, 5)$ | 0 | one failed lookup |
| DOT$(u, w)$ | $0.5 \cdot 0 + 2 \cdot 1.5 + (-1) \cdot 2 = 1$ | 3 lookups in $w$, since $u$ has fewer nonzeros |
| PLUS$(u, w)$ | $\{0: 3,\ 1: 0.5,\ 4: 3.5,\ 7: 1,\ 9: 1\}$ | 4 updates |
| PLUS$(u, z)$ with $z = \{7: 1\}$ | $\{1: 0.5,\ 4: 2\}$ | $-1 + 1 = 0$, so index 7 is deleted |
| PUT$(u, 4, 0)$ | $\{1: 0.5,\ 7: -1\}$ | index 4 is deleted |
| NORM$(u)$ before the last PUT | $\sqrt{0.25 + 4 + 1} = \sqrt{5.25} \approx 2.2913$ | 3 terms |

A dense array would store 10 numbers for each vector and make 10 products for the dot product. The sparse form stores 3 and 4 pairs and makes 3 lookups.

## Correctness

Each operation keeps (I1) to (I3) and returns the value of the mathematical operation. PUT with $x = 0$ removes $i$, so $v_i$ reads as 0 by (I3); with $x \ne 0$ it stores $x$, which keeps (I2). GET returns $T[i]$ or 0, which is $v_i$ by (I3). DOT sums $u_i w_i$ over the keys of the smaller table; the missing terms have a zero factor. PLUS starts from $u$ and adds each nonzero of $w$ through PUT, which removes the sums that are 0. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $k = \mathrm{nnz}(v)$, and $k_u, k_w$ for two vectors. The table is a hash table with $O(1)$ expected time per operation, as for a [hash table](/hash-table/) under its hashing assumption (for example, a random hash function from a universal family), and iteration over its pairs takes $O(1 + k)$ time.

| operation | expected time | worst case with a hash table |
|---|---|---|
| new | $O(1)$ | $O(1)$ |
| get, put | $O(1)$ | $O(k)$ |
| nnz | $O(1)$ | $O(1)$ |
| dot of two sparse vectors | $O(1 + \min(k_u, k_w))$ | $O(1 + k_u k_w)$ |
| dot with a dense array | $O(1 + k)$ | $O(1 + k)$ |
| plus | $O(1 + k_u + k_w)$ | $O(1 + (k_u + k_w)^2)$ |
| scale, norm | $O(1 + k)$ | $O(1 + k)$ |
| space | $\Theta(1 + k)$ | |

The derivations are short. DOT runs line L7 $\min(k_u, k_w)$ times, each with one expected $O(1)$ lookup. PLUS copies $k_u$ pairs and runs line A3 $k_w$ times. NORM is one DOT of $v$ with itself, $O(1 + k)$ since both tables are the same. A dense vector needs $\Theta(d)$ space and $\Theta(d)$ time for each of these whole-vector operations, so the sparse form wins when $k$ is much smaller than $d$. A matrix stored as $n$ sparse rows multiplies a dense vector in $O(n + N)$ expected time, where $N$ is the number of nonzeros of the matrix, by one DOT-DENSE per row.

## Variants

- **An ordered symbol table.** SparseVector of Sedgewick and Wayne uses their ordered symbol table, a red-black tree. Then get and put take $O(\log k)$ time in the worst case, the dot product loops over the smaller vector and makes $O(\min(k_u, k_w) \log \max(k_u, k_w))$ compares, and the entries come out in index order.
- **Sorted index arrays.** Store the indices in increasing order in one array and the values in a parallel array. Get is a binary search, $O(\log k)$; dot and plus are a merge of the two index lists, $\Theta(k_u + k_w)$ in the worst case and with good cache behaviour; but put of a new index moves $O(k)$ entries. This is the row format of [compressed sparse row](/compressed-sparse-row/) matrices, and it is the usual form when the vector is built once and then read many times.
- **Coordinate list.** An unsorted list of pairs $(i, v_i)$, as in a [sequential search symbol table](/sequential-search-symbol-table/), is the simplest form; get costs $O(k)$.
- **Sparse matrices.** A [sparse matrix](/sparse-matrix/) is an array of sparse rows, or a symbol table of sparse rows. Knuth, Section 2.2.6, links the nonzeros of each row and of each column in two circular lists, so that both rows and columns can be walked.
- **Bit vectors.** When the only values are 0 and 1 and $d$ is small, a [bit vector](/bit-set/) stores the vector in $d$ bits and computes a dot product with an AND and a population count per word.

## When to use it

Use a sparse vector when the number of nonzeros $k$ is much smaller than the dimension $d$, say less than a few percent, and the vector changes by single entries. Examples are document vectors in text search (one entry per word of a large vocabulary), the rows of the link matrix of the web, and feature vectors in machine learning. When $k$ is close to $d$, a dense array is smaller (a hash table entry takes several words) and much faster. When the vector is built once and then used many times, sorted index arrays are better than a hash table.

## Pitfalls

- **Storing zeros.** If line L1 is left out and PUT stores $x = 0$, the table grows with useless entries, $\mathrm{nnz}$ becomes wrong, and the costs grow with the number of writes instead of the number of nonzeros. Delete the index when the new value is 0.
- **Cancellation in plus.** If line A3 adds without the zero test of PUT, a sum such as $-1 + 1$ leaves an entry with value 0. Route every write through PUT.
- **Floating-point zeros.** With floats, $0.1 + 0.2 - 0.3$ is about $5.55 \cdot 10^{-17}$, not 0, so an entry that should vanish stays. Either accept such entries, or drop values with an absolute value below a tolerance chosen for the application, and state which.
- **Looping over the larger vector.** Line L4 is not needed for correctness, but without it DOT$(u, w)$ costs $O(k_u)$ even when $w$ has one nonzero. Iterate over the smaller table.
- **Mismatched dimensions.** Adding a vector of dimension 10 to one of dimension 20 gives no error in a hash table, but the result breaks (I1) for one of them. Check that the dimensions are equal.
- **An index out of range.** PUT with $i \ge d$ stores a key outside the vector and breaks (I1). Check $0 \le i < d$.

## Implementations

## History

Sparse matrices were stored by their nonzero entries from the early days of numerical computing; Knuth, Section 2.2.6, describes the orthogonal linked lists for this. Saad, Chapter 3, surveys the storage schemes used in modern solvers, such as the coordinate and the compressed sparse row formats. Sedgewick and Wayne, Section 3.5, present the sparse vector as an application of symbol tables, with the class SparseVector.

## References
