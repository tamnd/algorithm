---
tag: PTGD3C
kind: technique
slug: four-russians-method
name: Four Russians method
aliases:
- Arlazarov-Dinic-Kronrod-Faradzev method
- Method of Four Russians
- four Russians
- method of four Russians
area: techniques/bit-tricks
level: advanced
summary: Precomputes lookup tables of row combinations to speed up Boolean products by a log factor.
prereqs: [boolean-matrix-multiplication, table-lookup, bit-set]
see_also: [boolean-matrix-multiplication, transitive-closure, edit-distance, table-lookup, bit-parallelism, fischer-heun-rmq, word-ram, valiant-algorithm]
sources:
  - url: "https://www.mathnet.ru/eng/dan35675"
    title: V. L. Arlazarov, E. A. Dinic, M. A. Kronrod and I. A. Faradzhev, On economical construction of the transitive closure of an oriented graph, Doklady Akademii Nauk SSSR 194(3), 1970; English translation in Soviet Mathematics Doklady 11, 1970, pp. 1209 to 1210
    locator: pp. 487 to 488
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms, Addison-Wesley, 1974
    locator: Chapter 6, Matrix Multiplication and Related Operations (the Four Russians algorithm for Boolean matrix multiplication)
  - paper: doi:10.1016/0022-0000(80)90002-1
    title: William J. Masek and Michael S. Paterson, A faster algorithm computing string edit distances, Journal of Computer and System Sciences 20(1), 1980
    locator: pp. 18 to 31
  - paper: doi:10.1145/1644001.1644010
    title: Martin Albrecht, Gregory Bard and William Hart, Algorithm 898, Efficient multiplication of dense matrices over GF(2), ACM Transactions on Mathematical Software 37(1), 2010
    locator: pp. 1 to 14
---

The Four Russians method speeds up a computation by a logarithmic factor: it cuts the input into blocks of about $\lg n$ bits, precomputes the answer for every possible block in a table, and then replaces the work on each block by one lookup. Arlazarov, Dinic, Kronrod and Faradzhev used it in 1970 to compute the [transitive closure](/transitive-closure/) of a directed graph, and the classic form multiplies two $n \times n$ Boolean matrices with $O(n^3 / \log n)$ bit operations, against $n^3$ for the direct method. Masek and Paterson used the same idea in 1980 to compute [edit distance](/edit-distance/) in $O(n^2 / \log n)$ time. The name refers to the four authors of the 1970 paper.

## In plain words

Suppose you must do the same small job many times, and the job depends only on a few bits, say eight. There are only 256 possible inputs. So do the job once for each of the 256 inputs, write the answers in a table, and from then on look the answer up instead of doing the job.

The trick pays when the table is small enough to build quickly and the job is asked for many more times than the table has entries. Choosing blocks of about $\log n$ bits gives tables of about $n$ entries, so building them costs little, while each lookup saves the work of $\log n$ separate steps.

## When it applies

- The work splits into many small subproblems, and each subproblem is a function of a short input, a block of $t$ bits or of $t$ small values.
- The number of distinct block inputs, $2^t$ or $c^t$, is small compared with the number of times blocks are processed, so the table cost is paid back.
- The answer for a block fits in a few words, or in a bitset that the [word RAM](/word-ram/) handles with $O(n / w)$ operations.
- The combination of the block answers is cheap: an OR, an XOR, a sum or a table-driven merge.

## The template

For Boolean matrix multiplication $C = AB$, with $A$, $B$ and $C$ $n \times n$ matrices over $(\{0, 1\}, \lor, \land)$, and each row stored as a [bitset](/bit-set/) with bit $k$ for column $k$:

```
choose t ≈ lg n
for g = 0, t, 2t, …, (n − 1)                        ▷ a group of t columns of A, rows of B
    T[0] ← 0
    for x = 1 to 2^t − 1                            ▷ all subsets of the t rows g, …, g + t − 1 of B
        k ← index of the lowest 1-bit of x
        T[x] ← T[x AND (x − 1)] OR B[g + k]          ▷ one row OR
    for i = 0 to n − 1
        C[i] ← C[i] OR T[(A[i] >> g) AND (2^t − 1)]  ▷ one lookup and one row OR
```

**Correctness.** Row $i$ of $C$ is the OR of the rows $B[k]$ for the $k$ with $A[i][k] = 1$. The table entry $T[x]$ is the OR of the rows $B[g + k]$ for the bits $k$ of $x$, by induction on $x$, because $x \mathbin{\&} (x - 1)$ is $x$ without its lowest bit. Group $g$ adds to $C[i]$ exactly the rows $B[k]$ with $g \le k < g + t$ and $A[i][k] = 1$, and the groups cover all $k$.

**Cost.** There are $\lceil n / t \rceil$ groups. Each group does $2^t - 1$ row ORs to build its table and $n$ row ORs to use it, and a row OR costs $\lceil n / w \rceil$ word operations. The total is $\lceil n / t \rceil (2^t + n) \lceil n / w \rceil$. With $t = \lfloor \lg n \rfloor$, $2^t \le n$, so this is $O(n^2 / \log n)$ row operations: $O(n^3 / \log n)$ bit operations, or $O(n^3 / (w \log n))$ word operations with bitsets. The table needs $2^t \le n$ rows, $O(n^2 / w)$ words, reused for each group.

The general pattern is the same: fix a block size $t$, tabulate the block function over all $2^t$ inputs, and run the main loop with one lookup for each block.

## Classic examples

- **Boolean matrix multiplication.** The template above, $O(n^3 / \log n)$ bit operations. See [Boolean matrix multiplication](/boolean-matrix-multiplication/). Aho, Hopcroft and Ullman present it in Chapter 6 of their 1974 book.
- **Transitive closure.** The original use: the closure of a directed graph on $n$ vertices from $O(n^3 / \log n)$ bit operations. See [transitive closure](/transitive-closure/).
- **Edit distance.** Masek and Paterson cut the dynamic programming table into blocks of $t \times t$ cells with $t = \Theta(\log n)$. For a constant alphabet, the output of a block, as a vector of differences in $\{-1, 0, 1\}$ along its bottom and right sides, is a function of the two substrings and the differences along its top and left sides. Tabulate all such blocks, then run the DP over the $(n/t)^2$ blocks with one lookup each, $O(n^2 / \log n)$ time. See [edit distance](/edit-distance/).
- **Multiplication over GF(2).** The same table with XOR in place of OR gives the product over GF(2), as in the M4RM routine of Albrecht, Bard and Hart. The table can also be built in Gray code order, with one row XOR for each entry.
- **Range minimum queries.** The $O(n)$-space, $O(1)$-time RMQ structures split the array into blocks of $\Theta(\log n)$ items and answer queries inside a block from tables indexed by the shape of the block, of which there are $O(4^{t})$ for blocks of size $t$. See [Fischer-Heun RMQ](/fischer-heun-rmq/).

## Variations

- **Choice of block size.** The table size $2^t$ must not dominate. $t = \lg n$ balances the build cost against the main loop; $t = \frac{1}{2} \lg n$ keeps the table at $\sqrt n$ entries and loses only a factor of 2 in the speedup.
- **Several tables at once.** An implementation can build the tables of several consecutive groups and combine their lookups in one pass over the rows of $A$, which reads each row once for several groups.
- **Bit-parallel combination.** With bitsets the speedups multiply: $\log n$ from the tables and $w$ from the words. Compare [bit parallelism](/bit-parallelism/), which uses only the second factor.
- **Shared tables.** When the block function does not depend on the input, as in the edit distance method, the table is built once for all inputs of the same size.
- **Table lookup in general.** The method is [table lookup](/table-lookup/) with the block size chosen as a function of $n$, so that the table is built in time $o$ of the main work.

## Pitfalls

- **Tables that do not fit.** For $t = \lg n$ with $n = 10^5$, a table has $2^{16}$ or more entries of $n$ bits each, far more than the cache. Pick $t$ for the memory hierarchy, often 8.
- **Counting the table cost twice or not at all.** The build cost is $2^t$ row operations for each group, not for the whole run. Forgetting it and taking $t$ large makes the method slower than the direct one.
- **Bit and word models.** The bound $O(n^3 / \log n)$ counts bit operations. On the word RAM with $w \ge \lg n$, bitsets alone give $O(n^3 / w)$, which is already better; the tables then add another factor of $\log n$.
- **Not a better exponent.** The method saves a logarithmic factor. Algebraic methods such as the [Strassen algorithm](/strassen-algorithm/) lower the exponent below 3 and win for large $n$, while the Four Russians method is combinatorial and has small constants.
- **Edge groups.** When $t$ does not divide $n$, the last group has fewer columns; its table index must use the right mask, or rows past the end are read.

## Exercises

1. Compute $C = AB$ over the Boolean semiring with the template for $n = 4$, $t = 2$, $A = [1010_2, 0101_2, 0011_2, 1000_2]$ and $B = [0001_2, 0010_2, 0100_2, 1001_2]$ (row $k$ is the word $A[k]$, column $k$ is bit $k$). Write both tables.
2. Show that the table of the template can be built in Gray code order so that each entry costs one row XOR from the previous entry, and give the code over GF(2).
3. Show that the cost $\lceil n / t \rceil (2^t + n)$ row operations is $\Theta(n^2 / \log n)$ for $t = \lfloor c \lg n \rfloor$ with a constant $0 < c \le 1$, and that it is $\Omega(n^3 / \log n)$ for $t = \lfloor 2 \lg n \rfloor$.
4. Use the Boolean product to compute the transitive closure of a directed graph with $O(n^3 / \log n)$ bit operations, by repeated squaring or by a single pass in topological order of the strongly connected components.
5. Show that, for strings over an alphabet of size $\sigma$, the number of distinct $t \times t$ edit distance blocks, as functions of their inputs, is at most $\sigma^{2t} 3^{2t}$, and choose $t$ so that tabulating them takes $O(n)$ time.

## References
