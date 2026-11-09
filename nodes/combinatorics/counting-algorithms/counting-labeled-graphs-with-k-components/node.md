---
tag: ZXBH7H
kind: problem
slug: counting-labeled-graphs-with-k-components
name: Counting labeled graphs with k components
aliases:
- labeled graphs by number of components
- graphs with exactly k connected components
area: combinatorics/counting-algorithms
level: core
summary: Problem of counting labeled graphs on n vertices with exactly k connected components, using a recurrence over the component of a fixed vertex.
prereqs: [counting-connected-labeled-graphs, connected-components, exponential-generating-functions, binomial-coefficient]
see_also: [counting-labeled-graphs, stirling-numbers-second-kind, set-partitions, bell-numbers, cayley-formula, spanning-forest, disjoint-set, erdos-renyi-model]
sources:
  - book: isbn:9780123242457
    title: Frank Harary and Edgar M. Palmer, Graphical Enumeration, Academic Press, 1973
    locator: Chapter 1, Labeled enumeration (connected graphs and the counting of graphs by components)
  - book: isbn:9780521789875
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 2, Cambridge University Press, 1999
    locator: Section 5.1, The exponential formula
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter II, Labelled structures and exponential generating functions (the set construction with a fixed number of components)
  - url: https://oeis.org/A143543
    title: OEIS A143543, Triangle read by rows, number of labeled graphs on n nodes with k connected components
    locator: the data and the exponential generating function
---

Counting labeled graphs with $k$ components asks for the number $G(n, k)$ of simple graphs on the vertex set $[n] = \{1, \ldots, n\}$ that have exactly $k$ [connected components](/connected-components/). The case $k = 1$ is the count $c_n$ of [connected labeled graphs](/counting-connected-labeled-graphs/). Sorting the graphs by the component that holds vertex 1 gives the recurrence $G(n, k) = \sum_{j} \binom{n-1}{j-1} c_j \, G(n - j, k - 1)$, and in the language of [exponential generating functions](/exponential-generating-functions/), the column $k$ has the generating function $C(x)^k / k!$. The numbers form a triangle whose rows sum to $2^{\binom{n}{2}}$, the count of all [labeled graphs](/counting-labeled-graphs/).

## In plain words

Join numbered points with lines in any way you like. The drawing falls into pieces: two points are in the same piece when you can walk from one to the other along lines. The question is how many drawings have exactly a given number of pieces.

Look at the piece that holds point number one. Choose the other points of that piece, join them so that the piece holds together, and then draw the rest of the points so that they make one piece fewer. The count of drawings that hold together comes from a separate table, and the rest is a smaller version of the same question. So you can fill a table from small drawings up to large ones. Adding up a row of the table gives back the count of all drawings.

## Definition

Notation: $[n] = \{1, \ldots, n\}$, $g_n = 2^{\binom{n}{2}}$ is the number of labeled graphs on $[n]$, and $c_n$ is the number of connected labeled graphs on $[n]$, with $c_0 = 0$.

A labeled graph on $[n]$ has exactly $k$ components if its vertex set splits into $k$ nonempty classes such that two vertices are in the same class exactly when a path joins them. Set $G(0, 0) = 1$, $G(n, 0) = 0$ for $n \ge 1$, and $G(n, k) = 0$ for $k > n$.

**Problem.** Input: integers $n \ge 1$ and $1 \le k \le n$ (and optionally a prime $p$). Output: $G(n, k)$ (or $G(n, k) \bmod p$).

**Theorem (the recurrence).** For $n \ge 1$ and $k \ge 1$,

$$G(n, k) = \sum_{j=1}^{n-k+1} \binom{n-1}{j-1} \, c_j \, G(n - j, k - 1).$$

*Proof.* Classify the graphs on $[n]$ with $k$ components by the vertex set $S$ of the component that contains vertex 1, with $|S| = j$. There are $\binom{n-1}{j-1}$ choices of $S$. A graph whose component of 1 is exactly $S$ and which has $k$ components in total is the same as a pair: a connected graph on $S$ ($c_j$ choices), and a graph on $[n] \setminus S$ with exactly $k - 1$ components ($G(n - j, k - 1)$ choices, since the count depends only on the size of the vertex set). The pair determines the graph, because there are no edges between $S$ and its complement, and each graph gives one pair. The other $k - 1$ components need at least $k - 1$ vertices, so $j \le n - k + 1$. Sum over $j$. $\square$

**Exponential generating functions.** Let $C(x) = \sum_{n \ge 1} c_n x^n / n!$, as a formal power series. Then for each $k \ge 0$,

$$\sum_{n \ge 0} G(n, k) \frac{x^n}{n!} = \frac{C(x)^k}{k!}, \qquad \sum_{n, k \ge 0} G(n, k) \, y^k \frac{x^n}{n!} = e^{y C(x)}.$$

*Proof.* The coefficient of $x^n / n!$ in $C(x)^k$ is $\sum \binom{n}{n_1, \ldots, n_k} c_{n_1} \cdots c_{n_k}$ over $n_1 + \cdots + n_k = n$ with all $n_i \ge 1$. This counts the sequences $(B_1, \ldots, B_k)$ of disjoint nonempty sets that cover $[n]$, with a connected graph on each $B_i$. Each graph with $k$ components gives exactly $k!$ such sequences, one for each order of its components, because the components are distinct sets. Divide by $k!$. Summing over $k$ with weight $y^k$ gives the exponential. $\square$

At $y = 1$ the bivariate series is $e^{C(x)} = \sum_n g_n x^n / n!$, which is the relation $\sum_k G(n, k) = 2^{\binom{n}{2}}$.

## Variants

- **The exponential formula in general.** The recurrence and the generating function hold for every family of labeled structures that is a set of connected parts, with $c_j$ replaced by the number of connected structures of size $j$. With $c_j = 1$ for all $j$, the recurrence becomes the recurrence of the [Stirling numbers of the second kind](/stirling-numbers-second-kind/), which count the [set partitions](/set-partitions/) of $[n]$ into $k$ blocks. In general $G(n, k)$ is the partial Bell polynomial $B_{n,k}(c_1, c_2, \ldots)$: the sum, over the set partitions of $[n]$ into $k$ blocks, of the product of $c_{|B|}$ over the blocks $B$.
- **Forests with $k$ trees.** With $c_j = j^{j-2}$ from [Cayley's formula](/cayley-formula/), the same recurrence counts the labeled forests on $[n]$ with $k$ trees (OEIS A105599). The rows for $n = 1, \ldots, 6$ are $1$; $1, 1$; $3, 3, 1$; $16, 15, 6, 1$; $125, 110, 45, 10, 1$; $1296, 1080, 435, 105, 15, 1$.
- **By the number of edges.** Replace $c_j$ by the polynomial $c_j(y) = \sum_m c_{j,m} y^m$ that counts connected graphs by edges. The recurrence then counts graphs by vertices, edges and components at the same time, which gives the distribution of the number of components in the [Erdős-Rényi model](/erdos-renyi-model/) $G(n, p)$ for any $p$.
- **By the sizes of the components.** The number of graphs whose components have sizes $n_1, \ldots, n_k$ (as a multiset with $m_s$ parts equal to $s$) is $\frac{n!}{\prod_i n_i! \prod_s m_s!} \prod_i c_{n_i}$.
- **Unlabeled.** Up to isomorphism, the components form a multiset, and the counts come from the Euler transform of the counts of connected unlabeled graphs instead of from $C^k / k!$.

## Examples

The triangle $G(n, k)$ for $n = 1, \ldots, 8$ (OEIS A143543). Each row sums to $2^{\binom{n}{2}}$.

| $n$ | $k=1$ | $k=2$ | $k=3$ | $k=4$ | $k=5$ | $k=6$ | $k=7$ | $k=8$ |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | | | | | | | |
| 2 | 1 | 1 | | | | | | |
| 3 | 4 | 3 | 1 | | | | | |
| 4 | 38 | 19 | 6 | 1 | | | | |
| 5 | 728 | 230 | 55 | 10 | 1 | | | |
| 6 | 26704 | 5098 | 825 | 125 | 15 | 1 | | |
| 7 | 1866256 | 207536 | 20818 | 2275 | 245 | 21 | 1 | |
| 8 | 251548592 | 15891372 | 925036 | 64673 | 5320 | 434 | 28 | 1 |

**The case $n = 4$, $k = 2$.** With $c_1, c_2, c_3 = 1, 1, 4$ and $G(3, 1), G(2, 1), G(1, 1) = 4, 1, 1$:

$$G(4, 2) = \tbinom{3}{0} \cdot 1 \cdot 4 + \tbinom{3}{1} \cdot 1 \cdot 1 + \tbinom{3}{2} \cdot 4 \cdot 1 = 4 + 3 + 12 = 19.$$

By component sizes: sizes $\{1, 3\}$ give 4 choices of the single vertex times 4 connected graphs on the other three, so 16 graphs, and sizes $\{2, 2\}$ give the 3 ways to split $[4]$ into two pairs, each with one edge. The total is $16 + 3 = 19$. The row $38 + 19 + 6 + 1 = 64 = 2^6$.

**The diagonals.** $G(n, n) = 1$ (the empty graph), $G(n, n - 1) = \binom{n}{2}$ (one edge), and $G(n, n - 2) = 4 \binom{n}{3} + 3 \binom{n}{4}$: either one connected graph on 3 vertices with the rest isolated, or two disjoint edges. For $n = 6$ this is $80 + 45 = 125$.

## Known algorithms

- **The recurrence.** First compute $c_1, \ldots, c_n$ by the recurrence on [counting connected labeled graphs](/counting-connected-labeled-graphs/). Then fill the columns $G(\cdot, 1), \ldots, G(\cdot, k)$ in order. Each column needs $O(n^2)$ products, so $G(n, k)$ costs $O(k n^2)$ arithmetic operations, and the whole triangle up to $n$ costs $O(n^3)$. Modulo a word-size prime these are word operations. With exact integers the numbers have up to $\binom{n}{2}$ binary digits, which multiplies the cost by the cost of one big-integer product.
- **Powers of a power series.** Compute $C(x) \bmod x^{n+1}$, then $C(x)^k$ by repeated squaring with truncation, and divide by $k!$. This is $O(\log k)$ series products. Modulo a prime $p > n$ that supports [FFT multiplication](/convolution-via-fft/), each product costs $O(n \log n)$, so $G(n, k) \bmod p$ costs $O(n \log n \log k)$ after $C$ is known.
- **Listing.** For small $n$, enumerate all $2^{\binom{n}{2}}$ graphs and count the components of each with a [disjoint-set](/disjoint-set/) structure. This gives the whole row at once and is the brute-force check of the recurrence.

## Bounds

The row sums to $2^{\binom{n}{2}}$, so $G(n, k) < 2^{\binom{n}{2}}$ for every $k$ when $n \ge 2$, and the exact output can need $\Theta(n^2)$ binary digits. For $k \ge 2$, the graphs with $k$ components are among the disconnected graphs, so $G(n, k) \le g_n - c_n$, and the bounds on that page show that the fraction of graphs with $k \ge 2$ components tends to 0.

A lower bound: for $1 \le k \le n - 1$,

$$G(n, k) \ge \binom{n}{k-1} \, c_{n-k+1}.$$

*Proof.* Choose $k - 1$ vertices to be isolated and put any connected graph on the other $n - k + 1 \ge 2$ vertices. The result has $k$ components. Different choices give different graphs, because the isolated vertices are exactly the components of size 1, and the connected part has at least 2 vertices. $\square$

## Reductions

- **From connected counts.** $G(n, k)$ is a polynomial in $c_1, \ldots, c_{n-k+1}$ (the partial Bell polynomial), so the problem reduces to counting connected labeled graphs.
- **To connected counts.** The column $k = 1$ is $c_n$, and $c_n = g_n - \sum_{k \ge 2} G(n, k)$.
- **To probabilities.** The probability that $G(n, 1/2)$ has exactly $k$ components is $G(n, k) / 2^{\binom{n}{2}}$.

## Applications

- The distribution of the number of components of a random graph on few vertices, and the reliability of a small network whose links fail at random.
- Tests for connectivity code and [disjoint-set](/disjoint-set/) structures: the number of components over all graphs on $[n]$ must have the distribution of the row $G(n, \cdot)$.
- A model case of the exponential formula, which also gives the Stirling numbers, the [Bell numbers](/bell-numbers/) and the counts of forests from the counts of their connected parts.

## References
