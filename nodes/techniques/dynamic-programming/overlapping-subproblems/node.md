---
tag: 98D1TQ
kind: concept
slug: overlapping-subproblems
name: Overlapping subproblems
area: techniques/dynamic-programming
level: intro
summary: A naive recursion revisits the same subproblems many times, which DP avoids.
prereqs: [recursion, recursion-tree-method]
see_also: [optimal-substructure, independent-subproblems, memoization, tabulation, subproblem-graph, divide-and-conquer-paradigm, fibonacci-numbers, rod-cutting-problem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.1 (the running time of CUT-ROD) and Section 14.3, Elements of dynamic programming (the subsection on overlapping subproblems and RECURSIVE-MATRIX-CHAIN)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Section 0.2 (the exponential Fibonacci algorithm) and Chapter 6
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 6.1 (the recursive algorithm for weighted interval scheduling and its exponential running time)
---

A recursive algorithm has overlapping subproblems when it solves the same subproblem many times, so that the number of calls is much larger than the number of distinct subproblems. It is the second property that dynamic programming needs, after [optimal substructure](/optimal-substructure/): when it holds, [memoization](/memoization/) or [tabulation](/tabulation/) solves each distinct subproblem once and can turn an exponential [recursion](/recursion/) into a polynomial one. When it fails, as in [merge sort](/merge-sort/), a plain [divide and conquer](/divide-and-conquer-paradigm/) recursion already does no repeated work.

## In plain words

Write a function that calls itself on smaller inputs. Draw each call as a box, with lines to the calls it makes. For some functions, the same small input shows up in many boxes, far apart in the drawing. Each time, the function does the same work again from the start, and gets the same answer.

That repeated work is what "overlapping subproblems" means. The fix is to remember each answer the first time you compute it. Then each different input is solved once. If the number of different inputs is small, the total work becomes small, even when the drawing of calls is huge.

## The idea

### The definition

Let $f$ be defined by a recurrence: for an input $x$ that is not a base case, $f(x)$ is computed from $f(y_1), \ldots, f(y_k)$ for subproblems $y_i$ that are smaller than $x$. The naive recursive algorithm makes one call for each node of the *recursion tree*: the root is $x$, and the children of a node $y$ are the subproblems of $y$.

Let $N(x)$ be the number of nodes of the recursion tree, and let $D(x)$ be the number of *distinct* subproblems in it. The subproblems overlap when $N(x)$ is much larger than $D(x)$, that is, when some subproblem appears at many nodes. The distinct subproblems, with an edge from each to the subproblems it uses, form the [subproblem graph](/subproblem-graph/). The recursion tree is that graph unrolled into a tree, with one copy of a vertex for each path that reaches it from the root.

The definition is a matter of degree, not a yes or no test. What matters in practice:

- If $D(x)$ is polynomial in the input size and $N(x)$ is exponential, then solving each distinct subproblem once is an exponential gain.
- If $N(x) = D(x)$, every subproblem appears once and remembering answers gains nothing.

### Why the count can explode

A subproblem that is reached by many different paths from the root appears at many nodes of the tree. In a recurrence where $f(n)$ uses both $f(n-1)$ and $f(n-2)$, the subproblem $f(n-j)$ for $0 \le j < n$ is reached by as many paths as there are ways to write $j$ as an ordered sum of 1s and 2s, which is a [Fibonacci number](/fibonacci-numbers/). So it is called that many times.

### Overlap and independence

Two different properties use similar words. Subproblems *overlap* when the same subproblem is a subproblem of several different problems: $f(n-2)$ is used by $f(n)$ and by $f(n-1)$. Subproblems are [independent](/independent-subproblems/) when the subproblems used by one problem do not share a resource, so their solutions can be chosen apart. A DP needs both: independence among the siblings of one choice, and overlap across the whole recursion. CLRS Section 14.3 discusses the two together.

## Examples

### Fibonacci numbers

The naive recursion $F(n) = F(n-1) + F(n-2)$ with $F(0) = 0$ and $F(1) = 1$ makes $C(n)$ calls, where $C(0) = C(1) = 1$ and $C(n) = C(n-1) + C(n-2) + 1$.

**Claim.** $C(n) = 2F(n+1) - 1$ for each $n \ge 0$.

**Proof.** By induction on $n$. For $n = 0$ and $n = 1$, $2F(1) - 1 = 2F(2) - 1 = 1$. For $n \ge 2$, $C(n) = (2F(n) - 1) + (2F(n-1) - 1) + 1 = 2(F(n) + F(n-1)) - 1 = 2F(n+1) - 1$. ∎

There are only $n + 1$ distinct subproblems, $F(0), \ldots, F(n)$.

| $n$ | $F(n)$ | calls $C(n)$ | distinct subproblems |
| --- | --- | --- | --- |
| 10 | 55 | 177 | 11 |
| 20 | 6765 | 21891 | 21 |
| 30 | 832040 | 2692537 | 31 |
| 40 | 102334155 | 331160281 | 41 |

Since $F(n+1) \sim \varphi^{n+1}/\sqrt5$ with $\varphi = (1 + \sqrt5)/2 \approx 1.618$, the number of calls grows as $\Theta(\varphi^n)$, while the distinct subproblems grow as $n$.

### Rod cutting

The recursion CUT-ROD of CLRS Section 14.1 computes $r_n = \max_{1 \le i \le n}(p_i + r_{n-i})$ by calling itself on each of $0, 1, \ldots, n-1$. The number of calls $T(n)$ satisfies $T(0) = 1$ and $T(n) = 1 + \sum_{j=0}^{n-1} T(j)$. Subtracting the equation for $n - 1$ from the one for $n$ gives $T(n) - T(n-1) = T(n-1)$ for $n \ge 2$, and $T(1) = 2$. So $T(n) = 2^n$. The distinct subproblems are the $n + 1$ lengths $0, \ldots, n$. Here the recursion tree has one leaf for each of the $2^{n-1}$ ways to cut the rod, so the naive method tries each cutting.

### Matrix-chain multiplication

The recursion RECURSIVE-MATRIX-CHAIN of CLRS Section 14.3 computes $m[i, j]$ for the product $A_i \cdots A_j$ by calling itself on $m[i, k]$ and $m[k+1, j]$ for each split $k$. For a chain of $n$ matrices, the number of calls $C(n)$ is $C(1) = 1$ and $C(n) = 1 + \sum_{k=1}^{n-1}\bigl(C(k) + C(n-k)\bigr) = 1 + 2\sum_{k=1}^{n-1} C(k)$. Subtracting the equation for $n - 1$ gives $C(n) - C(n-1) = 2C(n-1)$ for $n \ge 3$, and $C(2) = 3$. So $C(n) = 3^{n-1}$. CLRS proves the weaker bound $\Omega(2^n)$. The distinct subproblems are the $n(n+1)/2$ ranges $[i, j]$. For $n = 15$, that is 4782969 calls for 120 subproblems.

### Non-example: merge sort

[Merge sort](/merge-sort/) on a range $[lo, hi)$ calls itself on the two halves. The ranges of any two calls are either disjoint or strictly nested, because the two halves of a range are disjoint and shorter than the range. So no range appears twice, each subproblem appears exactly once, $N = D$, and a table of answers would only cost space. The same holds for [binary search](/binary-search/), whose recursion is a single path.

### Non-example that is still slow

Overlap is not enough for a fast DP. The recursion for the [traveling salesman problem](/traveling-salesman-problem/) over pairs (set of visited cities, last city) has heavy overlap, and memoization reduces $(n-1)!$ tours to $O(n^2 2^n)$ time in the [Held-Karp algorithm](/held-karp-algorithm/). This is a large gain, but the number of distinct subproblems is still exponential.

## Where it is used

- **Deciding to use DP.** When a correct recursion is too slow, count its distinct subproblems. If the count is polynomial and the recursion tree is exponential, memoize or tabulate.
- **Memoization.** [Memoization](/memoization/) keeps the recursion and adds a table, so each distinct subproblem is solved once.
- **Tabulation.** [Tabulation](/tabulation/) drops the recursion and fills the table in an order where each subproblem comes after the ones it uses.
- **Running-time analysis.** With the overlap removed, the running time is the size of the [subproblem graph](/subproblem-graph/), not the size of the recursion tree.
- **Outside optimization.** Counting problems such as [counting lattice paths](/counting-lattice-paths/) or [binomial coefficients](/binomial-coefficient/) by [Pascal's rule](/pascal-triangle-dp/) have the same overlap, and parsers such as [packrat parsing](/packrat-parsing/) remove it by the same table.

## References
