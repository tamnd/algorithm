---
tag: B9R0C1
kind: definition
slug: inverse-ackermann-function
name: Inverse Ackermann function
aliases:
- alpha(n)
area: foundations/asymptotic-analysis
level: advanced
summary: The least k with A_k(1) at least n, for a fast variant A_k of the Ackermann function. It grows more slowly than lg* n, is at most 4 for n up to 2^2048, and bounds union-find.
prereqs: [ackermann-function, iterated-logarithm, asymptotic-notation]
see_also: [disjoint-set-forest, union-by-rank, path-compression, union-find-amortized-bound, union-find-lower-bound, fredman-saks-lower-bound, minimum-spanning-tree, soft-heap]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.3 (the bounds for each heuristic alone) and Section 19.4, Analysis of union by rank with path compression (the functions A_k(j) and alpha(n))
  - paper: doi:10.1145/321879.321884
    title: Robert E. Tarjan, Efficiency of a good but not linear set union algorithm, Journal of the ACM 22(2), 1975, pages 215 to 225
    locator: the main theorem, upper and lower bounds of order m alpha(m, n) for union by rank with path compression
  - paper: doi:10.1016/0022-0000(79)90042-4
    title: Robert E. Tarjan, A class of algorithms which require nonlinear time to maintain disjoint sets, Journal of Computer and System Sciences 18(2), 1979, pages 110 to 127
    locator: the lower bound for separable pointer algorithms
  - paper: doi:10.1145/73007.73040
    title: Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, STOC 1989, pages 345 to 354
    locator: the lower bound for the union-find problem
  - paper: doi:10.1137/0202024
    title: John E. Hopcroft and Jeffrey D. Ullman, Set merging algorithms, SIAM Journal on Computing 2(4), 1973, pages 294 to 303
    locator: the O(m lg* n) bound
  - paper: doi:10.1145/355541.355562
    title: Bernard Chazelle, A minimum spanning tree algorithm with inverse-Ackermann type complexity, Journal of the ACM 47(6), 2000, pages 1028 to 1047
    locator: the main theorem
  - paper: doi:10.1145/505241.505243
    title: Seth Pettie and Vijaya Ramachandran, An optimal minimum spanning tree algorithm, Journal of the ACM 49(1), 2002, pages 16 to 34
    locator: the main theorem
---

The inverse Ackermann function $\alpha(n)$ is the least $k$ such that $A_k(1) \ge n$, where $A_k$ is a fast-growing variant of the [Ackermann function](/ackermann-function/). It is unbounded, but it grows more slowly than the [iterated logarithm](/iterated-logarithm/) $\lg^* n$, and $\alpha(n) \le 4$ for every $n \le 2^{2048}$. It is the amortized cost of one operation of a [disjoint-set forest](/disjoint-set-forest/) with [union by rank](/union-by-rank/) and [path compression](/path-compression/), and lower bounds show that this cost cannot be improved.

## Definition

**The functions $A_k$.** For integers $k \ge 0$ and $j \ge 1$, CLRS (Section 19.4) defines

$$A_k(j) = \begin{cases} j + 1 & \text{if } k = 0, \\ A_{k-1}^{(j+1)}(j) & \text{if } k \ge 1, \end{cases}$$

where $f^{(i)}$ is $f$ applied $i$ times and $f^{(0)}(x) = x$. So $A_k$ applies $A_{k-1}$ to $j$, $j + 1$ times in a row. This is not the two-argument Ackermann-Péter function $A(m, n)$.

**Three facts.** For all $k \ge 0$ and $j \ge 1$:

1. $A_k(j) > j$.
2. $A_k(j + 1) > A_k(j)$.
3. $A_{k+1}(j) > A_k(j)$.

*Proof.* Facts 1 and 2 hold for $k = 0$. Assume that they hold for $f = A_k$. Since $f$ is increasing, each iterate $f^{(i)}$ is increasing. Since $f(x) > x$, we have $f^{(i+1)}(x) = f(f^{(i)}(x)) > f^{(i)}(x)$, so the iterates of one point increase. Then $A_{k+1}(j) = f^{(j+1)}(j) > f^{(0)}(j) = j$, which is fact 1 for $k + 1$. Next, $A_{k+1}(j + 1) = f^{(j+2)}(j + 1) > f^{(j+1)}(j + 1) > f^{(j+1)}(j) = A_{k+1}(j)$, which is fact 2. Last, $j + 1 \ge 2$ gives $A_{k+1}(j) = f^{(j+1)}(j) \ge f^{(2)}(j) > f(j) = A_k(j)$, which is fact 3. $\square$

**The inverse.** For each integer $n \ge 0$,

$$\alpha(n) = \min\{\, k \ge 0 : A_k(1) \ge n \,\}.$$

The minimum exists. By fact 3 and because the values are integers, $A_k(1) \ge A_0(1) + k = k + 2$, so $k = n$ is in the set.

**The first values.** $A_0(1) = 2$. Since $A_1(j)$ adds 1 to $j$, $j + 1$ times, $A_1(j) = 2j + 1$ and $A_1(1) = 3$. By induction on $i$, $A_1^{(i)}(j) = 2^i (j + 1) - 1$: the case $i = 0$ is $j$, and $2(2^i(j+1) - 1) + 1 = 2^{i+1}(j+1) - 1$. So $A_2(j) = A_1^{(j+1)}(j) = 2^{j+1}(j+1) - 1$ and $A_2(1) = 7$. Then $A_3(1) = A_2(A_2(1)) = A_2(7) = 2^8 \cdot 8 - 1 = 2047$. This gives the table of CLRS:

| $n$ | $\alpha(n)$ |
|---|---|
| 0 to 2 | 0 |
| 3 | 1 |
| 4 to 7 | 2 |
| 8 to 2047 | 3 |
| 2048 to $A_4(1)$ | 4 |

**Two arguments.** Tarjan (1975) stated the union-find bound with a function $\alpha(m, n)$ of the number $m$ of operations and the number $n$ of elements. A common form, used in the first edition of CLRS (Cormen, Leiserson and Rivest, 1990), is as follows. Let $A(1, j) = 2^j$ for $j \ge 1$, $A(i, 1) = A(i - 1, 2)$ for $i \ge 2$, and $A(i, j) = A(i - 1, A(i, j - 1))$ for $i, j \ge 2$. For $m \ge n \ge 1$,

$$\alpha(m, n) = \min\{\, i \ge 1 : A(i, \lfloor m / n \rfloor) > \lg n \,\}.$$

Each $A(i, \cdot)$ is increasing, so $\alpha(m, n)$ does not increase when $m$ grows and $n$ stays fixed: more operations per element give a smaller value. Tarjan's paper uses other constants inside the definition. Read the definition before you compare two bounds.

**The inverse of the diagonal.** Some texts use the [Ackermann function](/ackermann-function/) $A(m, n)$ of Ackermann and Péter, and define $\alpha_d(n) = \min\{\, k \ge 0 : A(k, k) \ge n \,\}$. The diagonal values are $A(0, 0) = 1$, $A(1, 1) = 3$, $A(2, 2) = 7$, $A(3, 3) = 61$, and $A(4, 4) = 2^{2^{\cdot^{\cdot^{2}}}} - 3$ with seven twos. So $\alpha_d(n) = 4$ for $62 \le n \le A(4, 4)$.

## Examples and non-examples

**The bound 4.** $A_4(1) = A_3(A_3(1)) = A_3(2047)$. By fact 3, $A_3(2047) > A_2(2047) = 2^{2048} \cdot 2048 - 1 > 2^{2048}$. The number $2^{2048}$ has 617 decimal digits. So $\alpha(n) \le 4$ for each $n \le 2^{2048}$, which is far beyond the number of bits of any memory. The true value of $A_4(1)$ is much larger again, because $A_3(2047)$ applies $A_2$ 2048 times.

**The two-argument form.** For $m = n$, $\lfloor m / n \rfloor = 1$, and $A(1, 1) = 2$, $A(2, 1) = A(1, 2) = 4$, $A(3, 1) = A(2, 2) = A(1, A(2, 1)) = 16$. The test $A(i, 1) > \lg n$ gives $\alpha(n, n) = 1$ for $n < 4$, $\alpha(n, n) = 2$ for $4 \le n < 2^4$, and $\alpha(n, n) = 3$ for $2^4 \le n < 2^{16}$. Next, $A(2, j) = 2^{A(2, j-1)}$, so $A(2, j)$ is a tower of $j + 1$ twos, and $A(4, 1) = A(3, 2) = A(2, 16)$ is a tower of 17 twos. So $\alpha(n, n) = 4$ for $2^{16} \le n$ as long as $\lg n$ is below this tower. More operations lower the value. For $n = 2^{20}$:

| $m$ | $\lfloor m/n \rfloor$ | $\alpha(m, n)$ |
|---|---|---|
| $n$ | 1 | 4 |
| $2n$ | 2 | 3 |
| $4n$ | 4 | 2 |
| $5n$ | 5 | 1 |

The last row holds because $A(1, 5) = 32 > 20 = \lg n$. In general $\alpha(m, n) = 1$ exactly when $2^{\lfloor m/n \rfloor} > \lg n$.

**Three definitions at one point.** For $n = 100$: $\alpha(100) = 3$, because $7 < 100 \le 2047$. $\alpha(100, 100) = 3$, because $A(2, 1) = 4 \le \lg 100 \approx 6.64 < 16 = A(3, 1)$. $\alpha_d(100) = 4$, because $A(3, 3) = 61 < 100$. And $\lg^* 100 = 4$. The variants differ by small constants. They are all unbounded and all grow at the same very slow rate in the sense of the bounds of union-find.

**Slower than $\lg^* n$.** For every $n \ge 0$, $\alpha(n) \le \lg^* n$, and $\alpha(n) = o(\lg^* n)$. Here $\lg^* x = k$ exactly when $T(k-1) < x \le T(k)$, for the tower $T(0) = 1$, $T(k+1) = 2^{T(k)}$ (see the [iterated logarithm](/iterated-logarithm/)).

*Proof.* For $n \le A_4(1)$ compare the table above with the tower: $\lg^* n \ge 1$ for $n \ge 2$, $\lg^* n \ge 2$ for $n \ge 3$, $\lg^* n \ge 3$ for $n \ge 5$, and $\lg^* n \ge 4$ for $n \ge 17$. In each row of the table, $\alpha(n)$ is at most these values. For larger $n$ we need a lemma: $A_3(j) \ge T(j + 1)$ for $j \ge 1$. Indeed $A_2(x) = 2^{x+1}(x+1) - 1 \ge 2^x$, and both functions are increasing, so $A_3(j) = A_2^{(j+1)}(j) \ge g^{(j+1)}(j) \ge g^{(j+1)}(1) = T(j+1)$ with $g(x) = 2^x$. Now let $k \ge 4$. By fact 3, $A_k(1) = A_{k-1}(A_{k-1}(1)) \ge A_3(A_{k-1}(1)) \ge T(A_{k-1}(1) + 1)$, so $\lg^* A_k(1) \ge A_{k-1}(1) + 1$. Let $\alpha(n) = k \ge 5$. Then $n > A_{k-1}(1)$, so $\lg^* n \ge A_{k-2}(1) + 1$. Fact 3 also gives $A_{j+1}(1) = A_j(A_j(1)) \ge A_1(A_j(1)) = 2A_j(1) + 1$ for $j \ge 1$, so $A_j(1) \ge 2^{j+1} - 1$. Hence $\lg^* n \ge 2^{k-1} \ge k = \alpha(n)$, and $\alpha(n)/\lg^* n \le k/2^{k-1}$. Since $\alpha(n) \to \infty$, this ratio tends to 0. $\square$

At practical sizes both functions are tiny. For $n = 2^{64}$, $\alpha(n) = 4$ and $\lg^* n = 5$. The difference between them is a matter of proofs, not of running times.

**Non-example: a constant.** $\alpha(n)$ is unbounded, because each $A_k(1)$ is finite. So $\alpha(n) \ne O(1)$, and a bound $O(m \, \alpha(n))$ is not a linear bound. For union-find this is not a weakness of the analysis: the lower bounds below show that no linear bound is possible.

### Pitfalls

- **Comparing bounds with different definitions.** $\alpha(n)$, $\alpha(n, n)$ and $\alpha_d(n)$ are different functions, as the case $n = 100$ shows. A bound with one of them is not a statement about the others, unless you prove a relation.
- **Calling $\alpha$ a constant.** In practice $\alpha(n) \le 4$. In a theorem, $O(m \, \alpha(n))$ and $O(m)$ are different claims, and only the first is true for union-find.
- **Amortized, not per operation.** The bound $O(\alpha(n))$ is amortized over a sequence. With union by rank, a tree of rank $r$ can have height $r$, and a single FIND on its deepest node takes $\Theta(\log n)$ time.
- **One heuristic alone.** The bound needs both heuristics. Union by rank alone gives $\Theta(\log n)$ worst-case time per FIND. Path compression alone gives $\Theta(n + f \cdot (1 + \log_{2 + f/n} n))$ for $n$ MAKE-SET and $f$ FIND operations, as CLRS states in Section 19.3.
- **The wrong argument order.** In $\alpha(m, n)$, $m$ is the number of operations and $n$ the number of elements, with $m \ge n$. Swapping them changes the value.

## Related definitions

**Union-find.** A disjoint-set forest with union by rank and path compression runs a sequence of $m$ operations, $n$ of them MAKE-SET, in $O(m \, \alpha(n))$ time in the worst case (CLRS, Section 19.4). So the amortized cost of one operation is $O(\alpha(n))$. Tarjan (1975) proved the bound $O(m \, \alpha(m, n))$ with his two-argument inverse, and he showed that the algorithm takes $\Omega(m \, \alpha(m, n))$ time on some sequences, so his analysis is tight for this algorithm. See [the amortized bound](/union-find-amortized-bound/).

**Lower bounds for every algorithm.** Tarjan (1979) proved $\Omega(m \, \alpha(m, n))$ for each separable algorithm on a pointer machine. Fredman and Saks (1989) proved the same order of bound in the [cell-probe model](/cell-probe-model/) with words of $O(\log n)$ bits, which covers every data structure on a random-access machine. So the amortized cost $\Theta(\alpha(m, n))$ per operation is optimal. See [the union-find lower bound](/union-find-lower-bound/) and [the Fredman-Saks bound](/fredman-saks-lower-bound/).

**Minimum spanning trees.** Chazelle (2000) gave a deterministic comparison-based algorithm for the [minimum spanning tree](/minimum-spanning-tree/) of a graph with $n$ vertices and $m$ edges that runs in $O(m \, \alpha(m, n))$ time. It uses the [soft heap](/soft-heap/). Pettie and Ramachandran (2002) gave a deterministic algorithm whose time is within a constant factor of the optimal decision-tree complexity of the problem. That complexity is not known in closed form. It is $O(m \, \alpha(m, n))$ by Chazelle's result, and no deterministic linear-time algorithm is known.

**The iterated logarithm.** The [iterated logarithm](/iterated-logarithm/) $\lg^* n$ inverts the tower function, and it grows faster than $\alpha(n)$, as shown above. Hopcroft and Ullman (1973) proved the bound $O(m \lg^* n)$ for union-find with both heuristics. Tarjan's bound with $\alpha$ is stronger.

## References
