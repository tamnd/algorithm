---
tag: M2GPXZ
kind: algorithm
slug: cache-oblivious-matrix-multiplication
name: Cache-oblivious matrix multiplication
aliases:
- recursive cache-oblivious matrix multiplication
- REC-MULT
- recursive matrix multiplication by halving the largest dimension
area: algebra/matrix-multiplication
level: advanced
summary: Halves the largest of the three dimensions until the pieces are tiny; without knowing M or B it makes O(n^2/B + n^3/(B sqrt(M))) cache misses, the optimal count for the classical product.
model: cache-oblivious-model
complexity:
  vars: {n: the order of the matrices, M: the cache size in words (a tall cache with M = Ω(B^2)), B: the line size in words}
  time: {worst: Θ(n^3), average: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(log n)}
  io:
    worst: "O(n^2/B + n^3/(B sqrt(M)))"
    average: "O(n^2/B + n^3/(B sqrt(M)))"
    best: "O(n^2/B + n^3/(B sqrt(M)))"
properties: {deterministic: true, recursive: true, in_place: false}
history:
  year: 1999
  people: [Matteo Frigo, Charles E. Leiserson, Harald Prokop, Sridhar Ramachandran]
  note: The FOCS 1999 paper that defined the cache-oblivious model gave this method as its first example.
prereqs: [divide-and-conquer-matrix-multiplication, cache-oblivious-model]
see_also: [blocked-matrix-multiplication, red-blue-pebble-game, funnelsort, van-emde-boas-layout, z-order-curve, strassen-algorithm, memory-hierarchy, parallel-matrix-multiplication]
sources:
  - paper: doi:10.1109/SFFCS.1999.814600
    title: Matteo Frigo, Charles E. Leiserson, Harald Prokop and Sridhar Ramachandran, Cache-oblivious algorithms, 40th Annual Symposium on Foundations of Computer Science (FOCS 1999)
    locator: Section 2, Matrix multiplication (the method REC-MULT and its cache complexity Θ(m + n + p + (mn + np + mp)/B + mnp/(B sqrt(M)))), and the section on LRU and regularity
  - paper: doi:10.1145/2071379.2071383
    title: Matteo Frigo, Charles E. Leiserson, Harald Prokop and Sridhar Ramachandran, Cache-oblivious algorithms, ACM Transactions on Algorithms 8(1), 2012
    locator: Article 4 (the journal version, with full proofs)
  - paper: "Harald Prokop, Cache-oblivious algorithms, Master's thesis, Massachusetts Institute of Technology, 1999"
    locator: the chapter on matrix multiplication and the tall-cache assumption
  - paper: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2), 1985"
    locator: pp. 202 to 208 (LRU with k lines against an optimal rule with h lines)
  - paper: "Kamen Yotov, Tom Roeder, Keshav Pingali, John Gunnels and Fred Gustavson, An experimental comparison of cache-oblivious and cache-conscious programs, Proceedings of the 19th ACM Symposium on Parallelism in Algorithms and Architectures (SPAA 2007)"
    locator: the measurements of recursive and tuned blocked matrix multiplication
  - paper: "Jia-Wei Hong and H. T. Kung, I/O complexity, the red-blue pebble game, Proceedings of the 13th Annual ACM Symposium on Theory of Computing (STOC 1981)"
    locator: pp. 326 to 333 (the lower bound Ω(n^3/sqrt(M)) words for the conventional product)
---

Cache-oblivious matrix multiplication computes $C = C + AB$ by cutting the largest of the three dimensions in half and recursing on the two halves, down to single entries. It never looks at the cache size $M$ or the line size $B$. Still, because the recursion passes through subproblems of every size, some level of it fits in the cache, whatever the cache is. In the [ideal-cache model](/cache-oblivious-model/) with a tall cache ($M = \Omega(B^2)$), it makes $O(n^2/B + n^3/(B\sqrt M))$ misses for $n \times n$ matrices, the same as a [blocked product](/blocked-matrix-multiplication/) tuned to $M$ and $B$, and optimal for the classical product by the bound of Hong and Kung. Frigo, Leiserson, Prokop and Ramachandran gave it in 1999. Because it is good for every $M$, it is good at every level of a cache hierarchy at once.

## In plain words

The blocked method cuts tables into tiles that fit in the cache, so it must know the cache size. This method does not. It cuts the job in two along its longest side: the rows of the answer, the shared inner side, or the columns of the answer. Each half is again cut along its longest side, and so on, until each piece is a single multiplication.

Somewhere along the way the pieces become just small enough to fit in the cache, whatever its size. From that point on, a piece is loaded once and finished. Bigger pieces are made of a few such pieces. So the method moves about as little data as a hand-tuned tiled method, and the same code is good for the small first-level cache, the larger second-level cache and main memory.

## The problem

The input is an $m \times n$ matrix $A$ and an $n \times p$ matrix $B$ over a ring or semiring $R$, and the output is $C = AB$. No commutativity and no subtraction are used; the operations are those of the [triple loop](/naive-matrix-multiplication/). For the bounds take $m = n = p$.

The cost model is the [cache-oblivious model](/cache-oblivious-model/): the [external memory model](/external-memory-model/) with an ideal cache of $M$ words in lines of $B$ words, fully associative with optimal replacement, where the algorithm does not know $M$ or $B$. Misses count I/Os. The matrices are stored in [row-major order](/row-major-order/). Time is counted in ring operations and is $\Theta(n^3)$, as for the triple loop.

## The algorithm

Write $A = (A_1 ; A_2)$ for a split into a top and a bottom half and $A = (A_1 \ A_2)$ for a split into a left and a right half. The procedure adds $AB$ into $C$.

```pseudo id=main
REC-MULT(A, B, C)                    ▷ C ← C + AB, A is m × n, B is n × p
L1  if max(m, n, p) ≤ base then C ← C + AB by the triple loop; return
L2  if m ≥ n and m ≥ p then split A = (A1 ; A2), C = (C1 ; C2); REC-MULT(A1, B, C1); REC-MULT(A2, B, C2)
L3  else if n ≥ p then split A = (A1 A2), B = (B1 ; B2); REC-MULT(A1, B1, C); REC-MULT(A2, B2, C)
L4  else split B = (B1 B2), C = (C1 C2); REC-MULT(A, B1, C1); REC-MULT(A, B2, C2)
```

To get $AB$, start with $C = 0$. The splits are views of the same arrays, with index ranges, not copies, so no temporary matrix is needed. Line L1 stops the recursion; in the analysis $\mathit{base} = 1$, and in practice a base of $16$ to $64$ with a tuned kernel saves the cost of the calls. Line L2 splits the rows of $A$ and $C$, line L3 splits the inner dimension, and line L4 splits the columns of $B$ and $C$. In each case the split dimension is a largest one, so it has at least $2$ entries. The halves have sizes $\lfloor x/2 \rfloor$ and $\lceil x/2 \rceil$, so no padding is needed for any shape.

On square matrices whose side is a power of two, three consecutive levels split $m$, $n$ and $p$ in turn, which gives the $8$ products of the [divide-and-conquer method](/divide-and-conquer-matrix-multiplication/). The difference is that the halving of the largest side also keeps rectangular pieces close to square.

## Example

Take $m = 8$, $n = 2$, $p = 4$. The shapes along the leftmost branch of the recursion are:

| level | shape $m \times n \times p$ | line | split |
|---|---|---|---|
| 0 | $8 \times 2 \times 4$ | L2 | rows, since $8$ is largest |
| 1 | $4 \times 2 \times 4$ | L2 | rows, since $m \ge n$ and $m \ge p$ (tie with $p$) |
| 2 | $2 \times 2 \times 4$ | L4 | columns, since $p = 4$ is largest |
| 3 | $2 \times 2 \times 2$ | L2 | rows |
| 4 | $1 \times 2 \times 2$ | L3 | inner, since $n \ge p$ |
| 5 | $1 \times 1 \times 2$ | L4 | columns |
| 6 | $1 \times 1 \times 1$ | L1 | one product $c_{ij} \mathrel{+}= a_{ik} b_{kj}$ |

The tree has $8 \cdot 2 \cdot 4 = 64$ leaves, one for each product, and depth $6 = \lg 8 + \lg 2 + \lg 4$. The thin input became cube-shaped after two levels.

The effect on misses was measured with the implementation, which simulates a fully associative LRU cache on the row-major addresses read, for $n = 64$ and lines of $B = 8$ words. The blocked method uses $b = 16$, which is tuned for $M = 768$ ($3b^2 = M$).

| cache $M$ (words) | recursive, $\mathit{base} = 1$ | blocked, $b = 16$ | loop order $i, k, j$ |
|---|---|---|---|
| 192 | 12 032 | 36 864 | 33 792 |
| 768 | 6 112 | 6 000 | 33 792 |
| 3072 | 3 068 | 3 072 | 33 792 |

These are observed counts for this simulation, not bounds. The recursive method is within 2% of the tuned blocked method at the cache size that method was tuned for, and is three times better when the cache is four times smaller, where the tiles no longer fit. It never needed to know $M$.

## Correctness

By strong induction on $mnp$. At line L1, the triple loop adds $AB$ into $C$. At line L2, $AB = (A_1 B ; A_2 B)$, and the two calls add $A_1 B$ into $C_1$ and $A_2 B$ into $C_2$. At line L3, $AB = A_1 B_1 + A_2 B_2$ by block multiplication, and the two calls add both terms into $C$. At line L4, $AB = (A B_1 \ A B_2)$. Each call has a smaller product $mnp$, because the split side is at least $2$ and is replaced by a half. No step swaps the factors of a product, so commutativity is not needed.

For each entry $c_{ij}$, the terms $a_{ik} b_{kj}$ arrive with $k$ increasing: only line L3 splits the range of $k$, and it does the lower half first. So in floating point the result equals that of the plain triple loop with the same inner order. The proofs section has the details, the depth bound and the miss bound.

## Complexity

- **Arithmetic.** $mnp$ multiplications and $mnp$ additions: $\Theta(n^3)$.
- **Recursion depth.** At most $\lceil \lg m \rceil + \lceil \lg n \rceil + \lceil \lg p \rceil$, so $3 \lceil \lg n \rceil$ for square matrices. Extra space is the stack, $\Theta(\log n)$ words.
- **Calls.** With $\mathit{base} = 1$ the tree has $mnp$ leaves and $mnp - 1$ inner nodes, so the overhead of calls is a constant factor. A larger base reduces it.
- **Misses, proved for powers of two.** Let $n$ be a power of two and $M \ge 36 B^2$. In the ideal cache, $Q(n) \le 9n^2/B$ if $B \le n$ and $9n^2 \le M$, and $Q(n) \le 54\, n^3/(B\sqrt M)$ otherwise. The proof stops the recursion at the first cube of side $s$ with $9s^2 \le M$; then $s > \sqrt M / 6 \ge B$, each such cube costs at most $9s^2/B$ misses, and there are $(n/s)^3$ of them. The proofs section writes it out.
- **Misses, general shapes.** Frigo et al. (1999) prove $\Theta(m + n + p + (mn + np + mp)/B + mnp/(B\sqrt M))$ for all $m$, $n$, $p$ under the tall-cache assumption. This is not reproduced here.
- **LRU.** By the lemma of Sleator and Tarjan, LRU with $M$ words makes at most twice the misses of the ideal cache with $M/2$ words. The bound above changes only by a constant factor when $M$ is halved, so it also holds, with a larger constant, for LRU.
- **Optimality.** Every schedule of the $n^3$ products moves $\Omega(n^3/\sqrt M)$ words (Hong and Kung, 1981), so it makes $\Omega(n^3/(B\sqrt M))$ misses, and reading the input costs $n^2/B$. So the method is optimal up to a constant factor for every $M$ and $B$ with a tall cache, and, by the argument of Frigo et al., at every level of a multilevel cache.

## Properties

- **Oblivious.** No parameter depends on the machine, except an optional base size.
- **Same arithmetic as the triple loop.** Same products and the same summation order for each entry, so the same rounding behaviour.
- **In place in $C$.** It accumulates into the output and needs no temporary matrices, unlike the 8-product method that adds two temporary results.
- **Any shape.** Halving the largest side handles thin and rectangular inputs with no padding.
- **Works over semirings.** Boolean and min-plus products recurse the same way.

## Variants and improvements

- **Recursive layouts.** Storing the matrices in a recursive order such as the [Z-order](/z-order-curve/) (Morton order) makes every subproblem a contiguous range of memory, so a subproblem touches fewer partly used lines. Converting the layout costs $O(n^2/B)$ extra misses.
- **Strassen.** [Strassen's algorithm](/strassen-algorithm/) is also a recursion on halves and is cache-oblivious in the same way. The pebbling bound of Ballard, Demmel, Holtz and Schwartz, $\Omega(n^{\log_2 7}/M^{\log_4 7 - 1})$ words, is met by the plain recursion.
- **Parallel version.** The two calls of lines L2 and L4 write disjoint parts of $C$, so they can run in parallel. The two calls of line L3 write the same $C$; running them in parallel needs a temporary matrix for one of them and an addition at the end. See [parallel matrix multiplication](/parallel-matrix-multiplication/).
- **Large base case.** A base of $16$ to $64$ handled by a register-blocked kernel is how the method is made fast in practice.

## When to use it

Use it when one portable code must run well on machines whose caches are not known, when there are several levels of cache, or for products over semirings and other rings where no BLAS exists. On a machine with a tuned BLAS, the library is faster: Yotov and others (2007) measured recursive codes, even with good base kernels, below tuned blocked codes, mostly because of the cost at the leaves and the lack of register-level control. The cache-oblivious recursion is a good outer structure around a fast kernel.

## Pitfalls

- **A base case of one entry.** The analysis uses $\mathit{base} = 1$, but a real implementation spends most of its time in calls. Stop at small blocks and use a tight loop.
- **Splitting by a fixed rule.** Always splitting $m$, then $n$, then $p$ is fine for cubes but handles thin matrices badly. Split the largest dimension.
- **Copying the halves.** Copying the submatrices at each level costs $\Theta(n^2)$ per level of work and memory traffic. Pass index ranges.
- **Tall cache.** The bound needs $M = \Omega(B^2)$. With very long lines in a small cache, row-major subproblems use only part of each line. A recursive layout helps.
- **Reading the bound as one for all algorithms.** Like the blocked method, it is optimal only among schedules of the classical $n^3$ products.

## Implementations

## History

Divide and conquer for matrix multiplication goes back at least to Strassen (1969). Its good locality was used in numerical libraries in the 1990s, including recursive layouts and recursive blocked algorithms by Gustavson and others. Frigo, Leiserson, Prokop and Ramachandran (FOCS 1999) defined the cache-oblivious model and proved that the recursion that halves the largest dimension is optimal in it for every $M$ and $B$ with a tall cache; Prokop's master's thesis of the same year has the details. The journal version appeared in ACM Transactions on Algorithms in 2012.

## References
