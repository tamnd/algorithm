---
tag: ZN5HGJ
kind: problem
slug: matrix-chain-multiplication
name: Matrix-chain multiplication
aliases:
- matrix-chain ordering
- optimal parenthesisation of a matrix product
area: techniques/dynamic-programming
level: core
summary: Choose the parenthesisation of a product of matrices that minimises scalar multiplications.
prereqs: [parenthesization, naive-matrix-multiplication, optimal-substructure]
see_also: [parenthesization, interval-dp, optimal-polygon-triangulation, polygon-triangulation-dp, optimal-binary-search-tree, knuth-optimization, catalan-numbers, traceback]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.2 (matrix-chain multiplication) and Section 14.3 (elements of dynamic programming)
  - paper: doi:10.1137/0211028
    title: T. C. Hu and M. T. Shing, Computation of matrix chain products, Part I, SIAM Journal on Computing 11(2), 1982
    locator: pp. 362 to 373
  - paper: doi:10.1137/0213017
    title: T. C. Hu and M. T. Shing, Computation of matrix chain products, Part II, SIAM Journal on Computing 13(2), 1984
    locator: pp. 228 to 251
  - paper: doi:10.1109/TC.1973.5009182
    title: S. S. Godbole, On efficient computation of matrix chain products, IEEE Transactions on Computers C-22(9), 1973
    locator: pp. 864 to 866
  - paper: doi:10.1145/359545.359556
    title: Francis Y. Chin, An O(n) algorithm for determining a near-optimal computation order of matrix chain products, Communications of the ACM 21(7), 1978
    locator: pp. 544 to 549
  - paper: doi:10.1137/18m1195401
    title: Oded Schwartz and Elad Weiss, Revisiting "Computation of matrix chain products", SIAM Journal on Computing 48(5), 2019
    locator: pp. 1481 to 1486
  - paper: doi:10.1137/S0097539790190077
    title: Prakash Ramanan, A new lower bound technique and its application, tight lower bound for a polygon triangulation problem, SIAM Journal on Computing 23(4), 1994
    locator: pp. 834 to 851
---

Matrix-chain multiplication is the problem of choosing the order in which to multiply a chain of matrices $A_1 A_2 \cdots A_n$ so that the total number of scalar multiplications is as small as possible. The order is a [parenthesization](/parenthesization/) of the product; all orders give the same matrix, but their costs can differ by orders of magnitude. The textbook solution is an [interval dynamic program](/interval-dp/) in $\Theta(n^3)$ time and $\Theta(n^2)$ space, and Hu and Shing solved the problem in $O(n \log n)$ time by a reduction to [optimal polygon triangulation](/optimal-polygon-triangulation/). It is the standard first example of dynamic programming in CLRS.

## In plain words

You must multiply a list of matrices, in the given order. You may choose which neighbours to multiply first. The answer does not change, but the amount of arithmetic does: multiplying a tall thin matrix by a wide one makes a huge result, and that result makes every later step expensive.

The question is which order is cheapest. Trying every order takes far too long, because the number of orders grows almost four times with each extra matrix. The way out is to notice that the cheapest plan for the whole list ends with one last multiplication, which joins the result of a left part and the result of a right part. Each part must itself be done in its cheapest way. So you compute the cheapest cost of every stretch of neighbouring matrices, short stretches first, and build the answer from them.

## Definition

**Input.** An integer $n \ge 1$ and positive integers $p_0, p_1, \ldots, p_n$. Matrix $A_i$ has $p_{i-1}$ rows and $p_i$ columns, so each adjacent pair $A_i A_{i+1}$ is compatible.

**Cost model.** Multiplying a $p \times q$ matrix by a $q \times r$ matrix with the [standard algorithm](/naive-matrix-multiplication/) takes $pqr$ scalar multiplications. The cost of a full parenthesization $\pi$ of $A_1 \cdots A_n$ is the sum of the costs of its $n - 1$ matrix multiplications. In the tree of $\pi$, the node that joins $A_i \cdots A_k$ and $A_{k+1} \cdots A_j$ multiplies a $p_{i-1} \times p_k$ matrix by a $p_k \times p_j$ matrix, so
$$\mathrm{cost}(\pi) = \sum_{\text{nodes } (i,k,j) \text{ of } \pi} p_{i-1}\, p_k\, p_j .$$

**Output.** A parenthesization $\pi^*$ with $\mathrm{cost}(\pi^*) = \min_\pi \mathrm{cost}(\pi)$, where $\pi$ ranges over the $C_{n-1}$ full parenthesizations ([Catalan number](/catalan-numbers/)). The problem does not compute the product itself; it only chooses the order.

**The recurrence.** Let $m[i, j]$ be the least cost of computing $A_i \cdots A_j$, for $1 \le i \le j \le n$. Then
$$m[i, j] = \begin{cases} 0 & \text{if } i = j, \\ \min_{i \le k < j} \bigl( m[i, k] + m[k+1, j] + p_{i-1} p_k p_j \bigr) & \text{if } i < j. \end{cases}$$

*Proof.* For $i = j$ there is nothing to multiply. For $i < j$, every parenthesization of $A_i \cdots A_j$ has a last multiplication that splits at some $k$ with $i \le k < j$. Its cost is $c_L + c_R + p_{i-1} p_k p_j$, where $c_L$ and $c_R$ are the costs of the parenthesizations of the two parts. Since $c_L \ge m[i, k]$ and $c_R \ge m[k+1, j]$, every parenthesization costs at least the right side, so $m[i, j]$ is at least the minimum. Conversely, for each $k$ we can combine an optimal parenthesization of each part, which costs exactly $m[i, k] + m[k+1, j] + p_{i-1} p_k p_j$, so $m[i, j]$ is at most each term of the minimum. ∎

This is the [optimal substructure](/optimal-substructure/) of the problem, and the argument in the first half is a [cut-and-paste argument](/cut-and-paste-argument/): the parts of an optimal parenthesization are optimal for their ranges. The two parts are independent because the shape of the left part does not change the dimensions that the right part sees.

## Variants

- **Optimization (the standard form).** Find the least cost and a parenthesization that achieves it. Record the best split $s[i, j]$ for each range, then recover the order by [traceback](/traceback/) from $s[1, n]$.
- **Value only.** Return $m[1, n]$ only. The same table is needed; no traceback.
- **Decision.** Given $B$, decide whether some parenthesization costs at most $B$.
- **Other cost models.** Replace $pqr$ by the cost of another multiplication routine, for example a model of [Strassen's algorithm](/strassen-algorithm/) or of cache misses. The interval recurrence still works when the cost of a node depends only on $(i, k, j)$. The $O(n \log n)$ algorithms below use the product form $p_{i-1} p_k p_j$ and do not carry over.
- **Generalized chains.** Chains with transposes, inverses or structured matrices (triangular, symmetric) have node costs that depend on the kind of the operands. Each range then needs one table entry for each kind of result.
- **Maximum cost.** The same recurrence with max instead of min gives the most expensive order. It is a teaching variant; for the six matrices below it is 58000.

## Examples

**Three matrices.** For $A_1$ of size $10 \times 100$, $A_2$ of size $100 \times 5$ and $A_3$ of size $5 \times 50$, the order $((A_1 A_2) A_3)$ costs $5000 + 2500 = 7500$ and $(A_1 (A_2 A_3))$ costs $25000 + 50000 = 75000$.

**Six matrices (CLRS Section 14.2).** Take $p = (30, 35, 15, 5, 10, 20, 25)$. The table $m[i, j]$, with row $i$ and column $j$:

| $m[i,j]$ | $j=1$ | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $i=1$ | 0 | 15750 | 7875 | 9375 | 11875 | 15125 |
| 2 | | 0 | 2625 | 4375 | 7125 | 10500 |
| 3 | | | 0 | 750 | 2500 | 5375 |
| 4 | | | | 0 | 1000 | 3500 |
| 5 | | | | | 0 | 5000 |
| 6 | | | | | | 0 |

The least cost is $m[1, 6] = 15125$. The best split of the whole chain is $s[1, 6] = 3$: $m[1,3] + m[4,6] + p_0 p_3 p_6 = 7875 + 3500 + 30 \cdot 5 \cdot 25 = 15125$. Then $s[1, 3] = 1$ and $s[4, 6] = 5$, which give the order $((A_1 (A_2 A_3))((A_4 A_5) A_6))$. For comparison, the left-to-right order $(((((A_1 A_2) A_3) A_4) A_5) A_6)$ costs 40500, and the worst of the 42 orders costs 58000.

**Monotone splits fail.** The [Knuth optimization](/knuth-optimization/) needs $s[i, j-1] \le s[i, j] \le s[i+1, j]$. Matrix chains do not have this property. For $p = (8, 9, 4, 10, 2)$, the unique best split of $A_1 A_2 A_3$ is $k = 2$ (cost 608 against 1080), but the unique best split of $A_1 \cdots A_4$ is $k = 1$ (cost 296 against 432 and 768). So $s[1, 3] > s[1, 4]$, and restricting the search to the Knuth window would miss the optimum.

## Known algorithms

| algorithm | time | space | notes |
|---|---|---|---|
| try all parenthesizations | $\Theta(n \cdot C_{n-1})$, that is $4^n$ up to a polynomial factor | $O(n)$ | only for tiny $n$ |
| [interval DP](/interval-dp/) (Godbole 1973; CLRS Section 14.2) | $\Theta(n^3)$ | $\Theta(n^2)$ | bottom-up by range length, or top-down with [memoization](/memoization/) |
| Chin 1978 | $O(n)$ | $O(n)$ | approximate: the order costs less than 25 percent more than the optimum |
| Hu and Shing 1982, 1984 | $O(n \log n)$ | $O(n)$ | exact, through optimal triangulation of a convex polygon |

The interval DP fills $m[i, j]$ in increasing order of $j - i$, so every entry it reads is already final. The [tabulation](/tabulation/) evaluates the term of the minimum for each triple $i \le k < j$. There are $\sum_{l=2}^{n} (n - l + 1)(l - 1) = \binom{n+1}{3} = (n^3 - n)/6$ such triples, so the time is $\Theta(n^3)$ for every input, not only in the worst case.

The Hu and Shing algorithm is long and intricate. In 2019 Schwartz and Weiss showed that the proof of one lemma in Part II was wrong, and published a corrected proof due to Shing; the $O(n \log n)$ bound stands.

## Bounds

- **Upper bound.** $O(n \log n)$ time on a RAM with unit-cost arithmetic on the dimensions (Hu and Shing).
- **Lower bound.** Reading the $n + 1$ dimensions takes $\Omega(n)$ time. Ramanan (1994) proved a tight $\Omega(n \log n)$ lower bound in the linear decision tree model for a closely related problem: the minimum-cost triangulation of a convex polygon with weighted vertices.
- **The DP bound is tight for the DP.** Any algorithm that evaluates every term of the recurrence does $\Theta(n^3)$ work. Faster algorithms must use the product structure of the costs.

## Reductions

- **To optimal polygon triangulation.** Draw a convex polygon with vertices $v_0, v_1, \ldots, v_n$ and give $v_i$ the weight $p_i$. Side $v_{i-1} v_i$ stands for $A_i$ and side $v_0 v_n$ stands for the result. A triangulation of this polygon with $n + 1$ sides corresponds one to one to a parenthesization ([Catalan triangulation theorem](/catalan-triangulation-theorem/)): the triangle $v_{i-1} v_k v_j$ is the multiplication that joins $A_i \cdots A_k$ and $A_{k+1} \cdots A_j$. Give the triangle with vertices $v_a, v_b, v_c$ the weight $p_a p_b p_c$. Then the weight of a triangulation equals the cost of the parenthesization, and the problem is [optimal polygon triangulation](/optimal-polygon-triangulation/) with product weights. Hu and Shing work in this form. The reduction takes $O(n)$ time.
- **From the problem to interval DP.** The same recurrence shape, "best split of a range plus a cost that depends on the range and the split", also solves the [optimal binary search tree](/optimal-binary-search-tree/) problem and parsing with the [CYK algorithm](/cyk-algorithm/). For the optimal binary search tree the extra cost satisfies the conditions of the Knuth optimization, which matrix chains do not (see Examples).

## Applications

- **Linear algebra code.** Libraries and compilers for array languages reorder chains such as $A B C x$ before evaluation. A matrix times a vector is a chain whose last dimension is 1, and the right-to-left order can be cheaper by a factor of the matrix size.
- **Automatic differentiation.** The Jacobian of a composition is a chain of Jacobian matrices. Forward mode and reverse mode are the two extreme orders; choosing the cheapest order is a matrix-chain problem.
- **Database query plans.** Choosing the order of joins over a fixed sequence of tables has the same split-point structure. See [join ordering](/join-ordering/).
- **Teaching.** CLRS uses it to introduce the four steps of dynamic programming: characterize an optimal solution, write the recurrence, compute the values bottom up, and construct a solution from stored choices.

## References
