---
tag: A93T41
kind: problem
slug: counting-connected-labeled-graphs
name: Counting connected labeled graphs
aliases:
- number of connected labeled graphs
- connected graph enumeration
area: combinatorics/counting-algorithms
level: core
summary: Count the connected simple graphs on [n] by subtracting the disconnected ones, with a recurrence on the size of the component of vertex 1, or by the logarithm of an exponential generating function.
prereqs: [counting-labeled-graphs, connected-graph, binomial-coefficient, exponential-generating-functions]
see_also: [counting-labeled-graphs-with-k-components, counting-labeled-bipartite-graphs, cayley-formula, connected-components, erdos-renyi-model, polynomial-multiplication, convolution-via-fft, union-bound]
sources:
  - book: isbn:9780123242457
    title: Frank Harary and Edgar M. Palmer, Graphical Enumeration, Academic Press, 1973
    locator: Chapter 1, Labeled enumeration (the count of connected labeled graphs, by the recurrence and by the logarithm of the exponential generating function)
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter II, Labelled structures and exponential generating functions (the set construction, the exp-log relation, and connected graphs)
  - url: https://oeis.org/A001187
    title: OEIS A001187, Number of connected labeled graphs with n nodes
    locator: the data, the recurrence and the exponential generating function log(sum 2^binomial(n,2) x^n/n!)
---

Counting connected labeled graphs asks for the number $c_n$ of connected simple graphs on the vertex set $[n] = \{1, \ldots, n\}$. There is no product formula. Instead, one counts all $2^{\binom{n}{2}}$ [labeled graphs](/counting-labeled-graphs/) and sorts them by the size $k$ of the component that holds vertex 1, which gives the recurrence $c_n = 2^{\binom{n}{2}} - \sum_{k=1}^{n-1} \binom{n-1}{k-1} c_k 2^{\binom{n-k}{2}}$. It runs in $O(n^2)$ arithmetic operations. In the language of [exponential generating functions](/exponential-generating-functions/), the generating function of connected graphs is the logarithm of that of all graphs.

## In plain words

You want to know how many ways there are to join numbered points with lines so that every point can reach every other point. Counting these directly is hard. Counting all drawings is easy: each pair is joined or not.

So count all drawings, and subtract the ones that fall apart. To count a drawing that falls apart, look at the piece that holds point number one. Say that piece has some number of points. Choose which other points are in it, join them so that the piece holds together, and draw anything at all on the points that are left. The piece itself is a smaller version of the same question, so you can fill a table from small sizes up to large ones.

## Definition

Notation: $[n] = \{1, \ldots, n\}$, $g_n = 2^{\binom{n}{2}}$ is the number of labeled graphs on $[n]$, and $C(n, k) = \binom{n}{k}$.

A labeled graph on $[n]$ is [connected](/connected-graph/) if each two vertices are joined by a path. By convention the graph on the empty vertex set is not connected, so $c_0 = 0$; OEIS A001187 sets $a(0) = 1$ instead.

**Problem.** Input: $n \ge 1$ (and optionally a prime $p$). Output: $c_n$, the number of connected labeled graphs on $[n]$ (or $c_n \bmod p$).

**Theorem (the recurrence).** For every $n \ge 1$,

$$g_n = \sum_{k=1}^{n} \binom{n-1}{k-1} c_k \, g_{n-k}, \qquad\text{so}\qquad c_n = g_n - \sum_{k=1}^{n-1} \binom{n-1}{k-1} c_k \, g_{n-k}.$$

*Proof.* Classify the $g_n$ graphs on $[n]$ by the vertex set $S$ of the [connected component](/connected-components/) that contains vertex 1. Let $k = |S|$, with $1 \le k \le n$. There are $\binom{n-1}{k-1}$ choices of $S$, because $1 \in S$ and the other $k - 1$ vertices come from $\{2, \ldots, n\}$. Given $S$, a graph whose component of 1 is exactly $S$ is the same as a pair: a connected graph on $S$ (there are $c_k$, since the count depends only on $|S|$), and any graph on $[n] \setminus S$ (there are $g_{n-k}$). The map is a bijection: a graph with component $S$ has no edge between $S$ and its complement, so it is the union of its parts on $S$ and on the complement. Conversely, the union of a connected graph on $S$ and any graph on the complement, with no edges between them, has $S$ as the component of 1. Sum over $k$ by the rule of sum, and solve for the term $k = n$, which is $c_n g_0 = c_n$. $\square$

**Exponential generating functions.** Let $G(x) = \sum_{n \ge 0} g_n x^n / n!$ and $C(x) = \sum_{n \ge 1} c_n x^n / n!$, as formal power series. Then $G(x) = e^{C(x)}$, and $C(x) = \log G(x)$, because a graph is a set of connected components on disjoint label sets. The recurrence is the coefficient form of $G'(x) = C'(x) G(x)$, the derivative of $G = e^{C}$: the coefficient of $x^{n-1}/(n-1)!$ on both sides gives the identity above.

## Variants

- **Modulo a prime.** Run the recurrence with all numbers reduced modulo $p$. The binomial coefficients come from a table of factorials and inverse factorials modulo $p$ when $p > n$, or from Pascal's rule otherwise.
- **By the number of edges.** Let $c_{n,m}$ be the number of connected graphs with $n$ vertices and $m$ edges. The same split, with $g_{n,m} = \binom{\binom{n}{2}}{m}$ in place of $g_n$, gives a recurrence over $n$ and $m$. Its first diagonal is $c_{n,n-1} = n^{n-2}$, the trees of [Cayley's formula](/cayley-formula/).
- **With $k$ components.** The same split gives the counts of graphs with exactly $k$ components; see [counting labeled graphs with k components](/counting-labeled-graphs-with-k-components/).
- **Other families.** The exp-log relation holds for every family closed under disjoint union and with membership decided per component: connected bipartite graphs from bipartite graphs (see [counting labeled bipartite graphs](/counting-labeled-bipartite-graphs/)), connected forests (trees) from forests, and connected regular graphs from regular graphs.
- **Unlabeled.** For graphs up to isomorphism, the relation between all graphs and connected graphs is the Euler transform instead of exp, and it starts from the [Pólya](/polya-enumeration-theorem/) counts.

## Examples

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $c_n$ (A001187) | 1 | 1 | 4 | 38 | 728 | 26704 | 1866256 | 251548592 | 66296291072 | 34496488594816 |
| $g_n$ | 1 | 2 | 8 | 64 | 1024 | 32768 | 2097152 | 268435456 | 68719476736 | 35184372088832 |

**The case $n = 4$.** With $c_1 = 1$, $c_2 = 1$, $c_3 = 4$ and $g_0, \ldots, g_3 = 1, 1, 2, 8$:

$$c_4 = 64 - \left(\tbinom{3}{0} c_1 g_3 + \tbinom{3}{1} c_2 g_2 + \tbinom{3}{2} c_3 g_1\right) = 64 - (8 + 6 + 12) = 38.$$

The three subtracted terms are the graphs where vertex 1 is alone (8 graphs on the other three vertices), where vertex 1 is in a component of size 2 (3 choices of the partner, times 2 graphs on the remaining two vertices), and where the component of 1 has size 3 (3 choices of the left-out vertex, times the 4 connected graphs on three vertices). The 38 connected graphs are 16 trees, 15 graphs with 4 edges (one of the $\binom{6}{4} = 15$ edge sets each, all connected), 6 with 5 edges and 1 complete graph: $16 + 15 + 6 + 1 = 38$.

Modulo $p = 10^9 + 7$, the recurrence gives $c_{10} \bmod p = 488353344$, which matches the exact value reduced modulo $p$.

## Known algorithms

- **The recurrence.** Fill $c_1, \ldots, c_n$ in order. Step $n$ needs $n - 1$ products, so the total is $\Theta(n^2)$ multiplications and additions. With exact integers of up to $\binom{n}{2}$ binary digits, each product costs $O(M(n^2))$ bit operations, where $M(b)$ is the cost of multiplying $b$-bit numbers, so the total is $O(n^2 M(n^2))$ bit operations. Modulo a word-size prime $p$, it is $\Theta(n^2)$ word operations.
- **The logarithm of a power series.** Modulo a prime $p$ with $p > n$ and a suitable root of unity, compute $C = \log G = \int G'/G$ with a power series inverse by Newton iteration and [FFT multiplication](/convolution-via-fft/). This takes $O(n \log n)$ operations modulo $p$ for all of $c_1, \ldots, c_n$.
- **Listing.** For small $n$, generate all $2^{\binom{n}{2}}$ graphs and test each with a [connected components](/connected-components/) search. This is the brute-force check of the recurrence, with $2^{\binom{n}{2}}$ tests.

## Bounds

For $n \ge 2$ the output $c_n$ has exactly $\binom{n}{2}$ binary digits, because $g_n / 2 \le c_n < g_n$ (the lower inequality follows from the bounds below for $n \ge 5$ and from the table for $n \le 4$). So writing it exactly needs $\Omega(n^2)$ time. Almost all labeled graphs are connected: for every $n \ge 2$,

$$n \, 2^{1-n} - \binom{n}{2} 2^{3-2n} \;\le\; 1 - \frac{c_n}{g_n} \;\le\; \sum_{k=1}^{\lfloor n/2 \rfloor} \binom{n}{k} 2^{-k(n-k)}.$$

*Proof.* Think of $1 - c_n / g_n$ as the probability that a uniformly random labeled graph, the [Erdős-Rényi graph](/erdos-renyi-model/) $G(n, 1/2)$, is disconnected. A disconnected graph has a component with at most $n/2$ vertices, and a fixed set $S$ of size $k$ has no edge to its complement with probability $2^{-k(n-k)}$. The [union bound](/union-bound/) over the sets $S$ with $1 \le |S| \le n/2$ gives the upper bound. For the lower bound, the graph is disconnected if some vertex is isolated (when $n \ge 2$). Vertex $i$ is isolated with probability $2^{-(n-1)}$, and two vertices $i \ne j$ are both isolated with probability $2^{-(2n-3)}$, since $2n - 3$ pairs are involved. The Bonferroni inequality $\Pr[\bigcup A_i] \ge \sum \Pr[A_i] - \sum_{i<j} \Pr[A_i \cap A_j]$ gives the lower bound. $\square$

Both bounds are $n 2^{1-n}(1 + o(1))$, so $1 - c_n / g_n \sim n \, 2^{1-n}$: a random graph is disconnected mostly because of an isolated vertex. For $n = 10$ the three numbers are about 0.01919, 0.01955 and 0.02030.

## Reductions

- **From labeled graphs.** The count reduces to the counts $g_n$ by the exp-log relation, and back: $g_n$ is a polynomial in $c_1, \ldots, c_n$ by the same recurrence.
- **To $k$ components.** The numbers of graphs with $k$ components are the coefficients of $C(x)^k / k!$, so they follow from $c_1, \ldots, c_n$ by power series multiplication.
- **Probability of connectivity.** The probability that $G(n, 1/2)$ is connected is $c_n / 2^{\binom{n}{2}}$. With a general edge probability $p$, weight each graph by $p^m (1-p)^{\binom{n}{2} - m}$ and use the edge-counting variant.

## Applications

- The probability that a random network is connected, and the reliability of a network whose links fail at random, for small numbers of nodes.
- The model case of the exp-log principle for labeled structures in [exponential generating functions](/exponential-generating-functions/).
- Tests for graph generators: a uniform generator of connected labeled graphs must hit each of the $c_n$ graphs with probability $1/c_n$.

## References
