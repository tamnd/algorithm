---
tag: B9R0C1
kind: definition
slug: inverse-ackermann-function
name: Inverse Ackermann function
aliases:
- alpha(n)
area: foundations/asymptotic-analysis
level: advanced
summary: The inverse of the Ackermann function, which grows so slowly that it is at most 4 for any practical n and bounds union-find.
prereqs: [ackermann-function, asymptotic-notation]
see_also: [iterated-logarithm, disjoint-set-forest, union-by-rank, path-compression, union-find-amortized-bound, fredman-saks-lower-bound, cell-probe-model, minimum-spanning-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 19 (analysis of union by rank with path compression)
  - paper: doi:10.1145/321879.321884
    title: Robert E. Tarjan, Efficiency of a good but not linear set union algorithm, Journal of the ACM 22 (1975)
    locator: the bound with the two-argument inverse
  - paper: "Robert E. Tarjan, A class of algorithms which require nonlinear time to maintain disjoint sets, Journal of Computer and System Sciences 18 (1979)"
    locator: the pointer-machine lower bound
  - paper: "Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, STOC 1989"
    locator: lower bound for the union-find problem
  - paper: "Bernard Chazelle, A minimum spanning tree algorithm with inverse-Ackermann type complexity, Journal of the ACM 47 (2000)"
    locator: the main theorem
---

The inverse Ackermann function $\alpha(n)$ is the least $k$ such that the $k$-th row of the [Ackermann function](/ackermann-function/) reaches $n$. It grows more slowly than the [iterated logarithm](/iterated-logarithm/) $\lg^* n$, and it is at most 4 for each $n$ that a computer can store. It bounds the amortized cost of each operation of [union-find](/disjoint-set-forest/) with union by rank and path compression, which is $O(\alpha(n))$, and it appears in the best proven time bound for a deterministic [minimum spanning tree](/minimum-spanning-tree/) algorithm.

## Definition

**One argument (CLRS).** Let $A_k(j)$ be the function of CLRS, chapter 19, defined on the page of the [Ackermann function](/ackermann-function/): $A_0(j) = j + 1$ and $A_k(j) = A_{k-1}^{(j+1)}(j)$ for $k \ge 1$. For each integer $n \ge 0$

$$\alpha(n) = \min\{\, k \ge 0 : A_k(1) \ge n \,\}.$$

The minimum exists because $A_k(1)$ is increasing in $k$ and unbounded. Since $A_0(1) = 2$, $A_1(1) = 3$, $A_2(1) = 7$ and $A_3(1) = 2047$, we get

| $n$ | $\alpha(n)$ |
|---|---|
| 0 to 2 | 0 |
| 3 | 1 |
| 4 to 7 | 2 |
| 8 to 2047 | 3 |
| 2048 to $A_4(1)$ | 4 |

**Two arguments.** Tarjan stated the union-find bound with a two-argument inverse $\alpha(m, n)$. A common form, for example in the first edition of CLRS, is as follows. For $m \ge n \ge 1$, use the function with $A(1, j) = 2^j$ for $j \ge 1$, $A(i, 1) = A(i - 1, 2)$ for $i \ge 2$, and $A(i, j) = A(i - 1, A(i, j - 1))$ for $i, j \ge 2$. This function is not the Ackermann-Péter function. The two-argument inverse is

$$\alpha(m, n) = \min\{\, i \ge 1 : A(i, \lfloor m / n \rfloor) > \lg n \,\}.$$

Since $A(i, j)$ increases with $j$, $\alpha(m, n)$ does not increase when $m$ grows with $n$ fixed. So a larger ratio $m / n$ gives a value that is no larger. Authors differ in the exact constants of this definition. Always compare the definition before you compare two bounds.

## Examples and non-examples

**The bound 4.** The value $A_4(1) = A_3(A_3(1)) = A_3(2047)$. Now $A_3(2047) = A_2^{(2048)}(2047)$, and $A_2(j) > j$, so $A_3(2047) \ge A_2(2047) = 2^{2048} \cdot 2048 - 1 > 2^{2048}$. The number $2^{2048}$ has 617 decimal digits. So $\alpha(n) \le 4$ for every $n \le 2^{2048}$, which is far above the number of bits of any real memory. In fact $A_4(1)$ is much larger than $2^{2048}$, because $A_3(2047)$ applies $A_2$ 2048 times.

**The two-argument form for $m = n$.** Here $A(1, 1) = 2$, $A(2, 1) = A(1, 2) = 4$ and $A(3, 1) = A(2, 2) = A(1, A(2, 1)) = 16$. The condition $A(i, 1) > \lg n$ gives: $\alpha(n, n) = 1$ for $n < 4$, $\alpha(n, n) = 2$ for $4 \le n < 2^{4}$, and $\alpha(n, n) = 3$ for $2^{4} \le n < 2^{16}$. Since $A(4, 1) = A(3, 2)$ is a tower of 17 twos, $\alpha(n, n) \le 4$ whenever $\lg n$ is below that tower.

**Not constant.** $\alpha(n)$ is unbounded, so $\alpha(n) \ne O(1)$. An upper bound of $O(m \, \alpha(n))$ alone does not show that an algorithm is not linear. For union-find, the lower bounds below show that no linear bound is possible, so the factor is real.

## Related definitions

**Where it appears.**

- **Union-find.** A [disjoint-set forest](/disjoint-set-forest/) with [union by rank](/union-by-rank/) and [path compression](/path-compression/) runs a sequence of $m$ operations on $n$ elements in $O(m \, \alpha(m, n))$ time in the worst case. Tarjan proved this bound in 1975 with the two-argument inverse. CLRS proves the bound $O(m \, \alpha(n))$ with its one-argument inverse, which gives $O(\alpha(n))$ amortized time per operation. See [the amortized bound](/union-find-amortized-bound/).
- **Lower bound.** Tarjan (1975) showed that this analysis is tight for the algorithm, and Tarjan (1979) showed $\Omega(m \, \alpha(m, n))$ for a class of pointer-machine algorithms. Fredman and Saks (1989) showed that in the [cell-probe model](/cell-probe-model/), with words of $O(\log n)$ bits, any data structure for union-find needs $\Omega(m \, \alpha(m, n))$ total time for $m$ operations, so $\Omega(\alpha(n))$ amortized time per operation when $m = \Theta(n)$. So the bound $\Theta(m \, \alpha(m, n))$ is tight, see [the lower bound](/fredman-saks-lower-bound/).
- **Minimum spanning tree.** Chazelle (2000) gave a deterministic comparison-based algorithm for the [minimum spanning tree](/minimum-spanning-tree/) of a graph with $n$ vertices and $m$ edges in $O(m \, \alpha(m, n))$ time. It uses soft heaps. This is the best proven bound for a deterministic algorithm. Pettie and Ramachandran (2002) gave a deterministic algorithm that is provably optimal, but its exact running time is not known. It is at most $O(m \, \alpha(m, n))$.

**Neighbours.** The [iterated logarithm](/iterated-logarithm/) $\lg^* n$ is the inverse of a tower and grows faster than $\alpha(n)$. The earlier bound $O(m \lg^* n)$ of Hopcroft and Ullman (1973) for union-find is weaker than the bound with $\alpha$.

## References
