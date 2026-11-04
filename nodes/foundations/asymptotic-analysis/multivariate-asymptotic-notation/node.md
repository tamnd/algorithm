---
tag: 2PQEFE
kind: concept
slug: multivariate-asymptotic-notation
name: Multivariate asymptotic notation
aliases:
- big-O in several variables
area: foundations/asymptotic-analysis
level: core
summary: Extends O, Omega and Theta to running times that depend on several parameters such as V and E.
prereqs: [asymptotic-notation, input-size]
see_also: [time-complexity, breadth-first-search, dijkstra, kruskal, graph, sparse-graph, dense-graph]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 3 (asymptotic notation, with an exercise on two parameters) and Chapter 20 (Elementary Graph Algorithms, running times in V and E)
  - paper: "Rodney R. Howell, On Asymptotic Notation with Multiple Variables, Technical Report 2007-4, Department of Computing and Information Sciences, Kansas State University, 2008"
    locator: the analysis of which properties of one-variable O-notation survive with several variables
  - book: isbn:9780321295354
    title: Kleinberg and Tardos, Algorithm Design
    locator: Chapter 3, Graphs (running times in n and m)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Chapter 4, Graphs
---

Multivariate asymptotic notation extends $O$, $\Omega$ and $\Theta$ of [asymptotic notation](/asymptotic-notation/) to functions of two or more variables, such as the numbers $n$ of vertices and $m$ of edges of a [graph](/graph/). The statement $f(m, n) = O(g(m, n))$ says that $f$ is at most a constant times $g$ when the variables are large. The meaning of "large" is a choice, and the two common choices are not equivalent, so a precise statement says which one it uses and which values the variables can take together.

## In plain words

Many inputs have more than one size. A graph has vertices and edges. A matrix has rows and columns. The cost depends on all of these numbers, and it can grow fast in one and slowly in another. So a cost such as "the number of vertices plus the number of edges" cannot be reduced to one number without a loss of information.

The one-variable habits mostly work here: ignore constant factors, and keep the larger of two terms. But a new question appears. What does "for large inputs" mean when there are two numbers? It can mean that both numbers are large, or that at least one is large. The two readings disagree when one number stays small, for example a graph with many vertices and no edges. The safe habit is to say which reading you use, and which combinations of sizes can occur.

## The idea

### Definition

Let $D \subseteq \mathbb{N}^k$ be the set of the values that the variables can take together (the domain), and let $f, g : D \to [0, \infty)$. Write $\mathbf{n} = (n_1, \ldots, n_k)$. Two definitions of $O$ are in use.

- **All variables large.** $f \in O_{\mathrm{all}}(g)$ if there are $c > 0$ and $N$ such that $f(\mathbf{n}) \le c \, g(\mathbf{n})$ for each $\mathbf{n} \in D$ with $n_i \ge N$ for every $i$.
- **Some variable large.** $f \in O_{\mathrm{some}}(g)$ if there are $c > 0$ and $N$ such that $f(\mathbf{n}) \le c \, g(\mathbf{n})$ for each $\mathbf{n} \in D$ with $n_i \ge N$ for at least one $i$.

The second definition says the same as "the bound holds at all but finitely many points of $D$". *Proof.* The set of points of $\mathbb{N}^k$ with $n_i < N$ for every $i$ is the box $\{0, \ldots, N-1\}^k$, which is finite. Conversely, a finite set of exceptions lies in such a box when $N$ is larger than each coordinate of each exception. $\square$ For two parameters, Cormen, Leiserson, Rivest and Stein state the second definition in an exercise of Chapter 3, with the condition "$n \ge n_0$ or $m \ge m_0$".

The classes $\Omega$ and $\Theta$ follow in the same way: $\Omega$ reverses the inequality, and $\Theta = O \cap \Omega$. For $o$, "there is $c > 0$" becomes "for each $c > 0$". With $k = 1$ and $D = \mathbb{N}$ both definitions are the usual one.

**The second is stronger.** Each bound of the second kind is a bound of the first kind, with the same $c$ and $N$, because a point with every $n_i \ge N$ has at least one $n_i \ge N$. The converse is false. Let $D = \{1, 2, \ldots\}^2$, and let $T(m, n) = m^2$ if $n = 1$, and $T(m, n) = m$ otherwise. Then $T \in O_{\mathrm{all}}(m)$ with $N = 2$ and $c = 1$. But $T \notin O_{\mathrm{some}}(m)$: for each $c$ and $N$, the point $(m, 1)$ with $m > \max(c, N)$ has a large variable, and $T = m^2 > c\,m$ there. The first definition ignores what happens while one variable stays small, and the second does not.

On this page a bound means $O_{\mathrm{some}}$ unless the text says otherwise, as in the exercise of Cormen et al. In analysis, a limit as all variables tend to infinity matches the first reading.

### Rules that carry over

These rules hold for both definitions, with the one-variable proofs. Where two bounds are combined, take the larger $N$ and the product or the larger of the constants.

- **Transitive.** If $f = O(g)$ and $g = O(h)$, then $f = O(h)$: $f \le c_1 g \le c_1 c_2 h$ at the points where both bounds hold.
- **Constant factors and sums.** For $c > 0$, $c f = \Theta(f)$. Also $f + g = \Theta(\max(f, g))$, since $\max(f,g) \le f + g \le 2\max(f,g)$ at every point. In particular $m + n = \Theta(\max(m, n))$.
- **Products.** If $f_1 = O(g_1)$ and $f_2 = O(g_2)$, then $f_1 f_2 = O(g_1 g_2)$, with constant $c_1 c_2$, because all four functions are non-negative.
- **Restriction to a smaller domain.** A bound on $D$ holds on each subset of $D$. The converse is the source of most errors below.

### What does not carry over

- **A term can be dropped only if the domain makes it smaller.** For $m + n$ neither term dominates the other on all graphs, so both stay, or the bound is written as $\max(m, n)$. The domain "connected graphs" gives $n - 1 \le m$, so $n + m \le 2m + 1 \le 3m$ for $m \ge 1$, and there $\Theta(n + m) = \Theta(m)$. Without the condition this is false: a graph with $n$ vertices and no edges has $n + m = n$ and $m = 0$.
- **A factor that can be zero.** On the domain of all graphs, $n \notin O_{\mathrm{some}}(mn)$, because at the infinitely many points $(m, n) = (0, n)$ the right side is 0. It is true that $n \in O_{\mathrm{all}}(mn)$. A bound such as $O(mn)$ for an algorithm that also scans the vertices is safe only if it is written as $O(n + mn)$ or the domain excludes $m = 0$.
- **A substitution works in one direction.** If $f = O(g)$ in either sense, then each substitution $m = m(n)$ with $m(n) \to \infty$ and $(m(n), n) \in D$ gives a one-variable bound $f(m(n), n) = O(g(m(n), n))$. The converse is false: a bound along one curve says nothing elsewhere. Let $T(m, n) = 0$ if $m = n$, and $T(m, n) = 2^m$ otherwise. Along the curve $m = n$, $T = O(1)$, yet $T$ is bounded by no polynomial in $m$ and $n$.
- **The summation rule can fail.** In one variable, $f = O(g)$ with $g$ positive gives $\sum_{i=0}^{m} f(i) = O\left(\sum_{i=0}^{m} g(i)\right)$, because the finitely many early terms add only a constant. With a second variable the early terms can depend on it. Let $D = \mathbb{N}^2$ with points $(i, n)$, let $f(i, n) = 2^n$ if $i = 0$ and $f(i, n) = 1$ otherwise, and let $g = 1$. Then $f \in O_{\mathrm{all}}(g)$ with $N = 1$ and $c = 1$. The sums are $F(m, n) = \sum_{i=0}^{m} f(i, n) = 2^n + m$ and $G(m, n) = m + 1$. For each $c$ and $N$, the point $m = N$ with $n$ large has $F > c\,G$, so $F \notin O_{\mathrm{all}}(G)$. At $m = 1$ and $n = 20$, $F/G = 524\,288.5$. A loop analysis under the all-variables-large definition can therefore give a wrong bound. Here $f \notin O_{\mathrm{some}}(g)$, so the example says nothing against the second definition.
- **No definition keeps every rule.** Howell shows that the properties of one-variable $O$ that analyses of algorithms use cannot all hold at once for functions of several variables, and he studies which definitions keep which properties. In practice, state the domain and keep the bound in a form, such as a sum of products of the parameters, that is true at every point of the domain up to the constant.
- **Limits depend on the path.** The ratio $f/g$ can tend to different values along different paths to infinity. For $f = m$ and $g = m + n$, the ratio tends to 1 along $n = 1$ and to $\frac12$ along $m = n$. So the tests of [comparing growth by limits](/comparing-growth-by-limits/) apply along a path, not to the whole domain.

### Pitfalls

- **Dropping a parameter.** "BFS runs in $O(n)$ time" and "BFS runs in $O(m)$ time" are both false on the domain of all graphs. The correct bound is $O(n + m)$.
- **Comparing bounds with one family in mind.** On all graphs with $n \ge 2$, $m + n\lg n \le (n + m)\lg n$, so $O(m + n\log n) \subseteq O((n + m)\log n)$. On a sparse family ($m = \Theta(n)$) both are $\Theta(n\log n)$, so the two bounds are the same class there. On a dense family ($m = \Theta(n^2)$) they differ by a factor $\Theta(\log n)$. A claim that one bound is better must name the family.
- **Forgetting the domain.** $m \le n^2$ holds for simple graphs, not for multigraphs. A step that uses $\log m = O(\log n)$ needs the simple-graph domain, or a bound on the multiplicity of edges.

## Examples

**Breadth-first search.** On a graph with $n$ vertices and $m$ edges, given as an [adjacency list](/adjacency-list/), [breadth-first search](/breadth-first-search/) initializes $n$ marks and scans the list of each vertex that it reaches, once. The lists have $m$ entries in total for a directed graph and $2m$ for an undirected one. So the time is $O(n + m)$ on every input. When every vertex is reachable from the source, as in a connected undirected graph, the search scans every list and the time is $\Theta(n + m)$. If the source has no edges, the time is $\Theta(n)$ whatever $m$ is. On the complete bipartite graph with $n/2$ vertices on each side ($n$ even), which is connected, the lists hold $2 \cdot n^2/4 = n^2/2$ entries: $500\,000$ entries for $n = 1000$. So a bound $O(n)$ is false on this family, and $O(m)$ is false on graphs without edges.

**Sorting the edges.** [Kruskal's algorithm](/kruskal/) sorts the $m$ edges with $O(m\log m)$ comparisons. For a [simple graph](/simple-graph/) with $n \ge 2$ and $m \ge 1$ we have $m \le n(n-1)/2 < n^2$, so $\lg m < 2\lg n$ and $m\log m = O(m\log n)$. For a [connected graph](/connected-graph/) that is simple, with $n \ge 3$, we also have $m \ge n - 1 \ge \sqrt n$, so $\lg m \ge \frac12\lg n$ and $m\log n = O(m\log m)$. The step $n - 1 \ge \sqrt n$ holds at $n = 3$ ($2 \ge 1.732$), and $n - 1 - \sqrt n$ increases with $n$, since its derivative $1 - 1/(2\sqrt n)$ is positive. So on connected simple graphs $\Theta(m\log m) = \Theta(m\log n)$. On multigraphs the first step fails, since $m$ has no bound in terms of $n$.

**Shortest paths.** [Dijkstra's algorithm](/dijkstra/) with a [binary heap](/binary-heap/) runs in $O((n + m)\log n)$ time, and with a [Fibonacci heap](/fibonacci-heap/) in $O(m + n\log n)$. Without the hidden constants, the ratio of the first expression to the second is $2.73$ at $n = 10^6$ and $m = 2 \cdot 10^6$, and $19.9$ at $n = 10^6$ and $m = 10^{11}$. On a sparse family the ratio stays bounded, and on a dense family it grows like $\lg n$. Neither statement can be read with one variable alone.

**Matrix product.** The classical algorithm for an $a \times b$ matrix times a $b \times c$ matrix makes exactly $abc$ multiplications of entries and $a(b-1)c$ additions. The cost is $\Theta(abc)$ in three variables. No variable can be dropped: with $a = c = 1$ the product is an inner product of length $b$, and the cost is $\Theta(b)$.

**Dense and sparse graphs.** For a simple graph, $m \le n(n-1)/2$, so $O(n + m) \subseteq O(n^2)$ on this domain. A [sparse graph](/sparse-graph/) family has $m = O(n)$, so $O(n + m) = O(n)$ on it. A [dense graph](/dense-graph/) family has $m = \Theta(n^2)$, so $O(n + m) = O(n^2)$ on it. These are bounds on regions of the $(m, n)$ plane, and the region is part of the statement.

## Where it is used

Graph algorithms state their costs in $n$ and $m$. Cormen, Leiserson, Rivest and Stein write $V$ and $E$ inside the notation for $|V|$ and $|E|$, as in $O(V + E)$ for breadth-first search. Algorithms on strings use the text length and the pattern length, and algorithms on matrices use the two or three dimensions. A cost such as $O(m + n)$ stays in this form when $m$ and $n$ are independent, and the forms $O(m\log n)$ and $O(m + n\log n)$ let a reader compare algorithms on sparse and dense inputs. Each such statement should name the domain (simple, connected, directed) and, when it matters, the reading of "large".

## References
