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
    locator: Chapter 3 (asymptotic notation) and Chapter 20 (Elementary Graph Algorithms, running times in V and E)
  - book: isbn:9780321295354
    title: Kleinberg and Tardos, Algorithm Design
    locator: Chapter 3 (Graphs, running time of breadth-first search in n and m)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Chapter 4 (Graphs)
  - paper: "Rodney R. Howell, On Asymptotic Notation with Multiple Variables, Kansas State University, technical report 2007-4, 2008"
    locator: the discussion of which rules of one-variable notation hold for several variables
---

Multivariate asymptotic notation extends $O$, $\Omega$ and $\Theta$ to functions of two or more variables, such as the numbers $n$ of vertices and $m$ of edges of a [graph](/graph/). The statement $f(m, n) = O(g(m, n))$ says that $f$ is at most a constant times $g$ when the variables are large. The meaning of "large" is a choice, and the choices are not equivalent, so a precise statement must say which one it uses.

## In plain words

Many inputs have more than one size. A graph has vertices and edges. A matrix has rows and columns. The cost depends on all of these numbers, and it can grow fast in one and slowly in another. So a cost such as "the number of vertices plus the number of edges" cannot be reduced to one number without a loss of information.

The one-variable rules work in the same way here: ignore constant factors, and a sum is dominated by its larger term. But a new question appears. What does "for large inputs" mean when there are two numbers? It can mean that both numbers must be large, or that at least one is large. These two readings give different answers on some costs. The safe habit is to say which reading you use, and which values the variables can take together.

## The idea

### Definition

Let $D \subseteq \mathbb{N}^k$ be the set of the values that the variables can take together (the domain), and let $f, g : D \to [0, \infty)$. Two definitions of $O$ are in use. Write $\mathbf{n} = (n_1, \ldots, n_k)$.

- **All variables large.** $f \in O_{\mathrm{all}}(g)$ if there are $c > 0$ and $N$ such that $f(\mathbf{n}) \le c \, g(\mathbf{n})$ for each $\mathbf{n} \in D$ with $n_i \ge N$ for every $i$.
- **All but finitely many points.** $f \in O_{\mathrm{fin}}(g)$ if there are $c > 0$ and a finite set $F \subseteq D$ such that $f(\mathbf{n}) \le c \, g(\mathbf{n})$ for each $\mathbf{n} \in D \setminus F$.

On $D \subseteq \mathbb{N}^k$ the second definition asks for the bound at every point where at least one $n_i \ge N$ for some $N$: the excluded set is a finite set, and every finite set lies in a box $\{n_i < N\}$. For $k = 2$ this is the reading "$n \ge n_0$ or $m \ge m_0$".

The classes $\Omega$ and $\Theta$ follow in the same way: $\Omega$ reverses the inequality, and $\Theta = O \cap \Omega$. For $o$, the constant $c$ is replaced by "for each $c > 0$". With $k = 1$ and $D = \mathbb{N}$, both definitions are the usual one of [asymptotic notation](/asymptotic-notation/).

Every bound of the second kind is a bound of the first kind. Proof: let $F$ be the finite exceptional set, and choose $N$ larger than every coordinate of every point of $F$. A point with $n_i \ge N$ for each $i$ is not in $F$, so the bound holds at it. The converse is false, as the next example shows.

**Example where they differ.** Let $D = \{1, 2, \ldots\}^2$, and let $T(m, n) = m^2$ if $n = 1$, and $T(m, n) = m$ otherwise. Then $T \in O_{\mathrm{all}}(m)$: take $N = 2$ and $c = 1$. But $T \notin O_{\mathrm{fin}}(m)$: the points $(m, 1)$ with $m > c$ are infinitely many, and at each of them $T = m^2 > c\,m$. The first definition ignores the behavior when one variable stays small, and the second does not.

Sources do not always say which definition they use. On this page, a bound is read as $O_{\mathrm{fin}}$ unless the text says otherwise. In analysis, limits as all variables tend to infinity correspond to the first reading.

### Rules

These three rules hold for both definitions, with the same proofs as for one variable, taking $N$ as the maximum of the thresholds that appear.

- **Transitive.** If $f = O(g)$ and $g = O(h)$, then $f = O(h)$: $f \le c_1 g \le c_1 c_2 h$ on the points where both bounds hold (take the larger $N$ for the first definition, or the union of the two finite sets for the second).
- **Constant factors and sums.** For $c > 0$, $c f = \Theta(f)$. Also $f + g = \Theta(\max(f, g))$, since $\max(f,g) \le f + g \le 2\max(f,g)$. In particular $m + n = \Theta(\max(m, n))$.
- **Products.** If $f_1 = O(g_1)$ and $f_2 = O(g_2)$, then $f_1 f_2 = O(g_1 g_2)$.

What does not carry over from one variable:

- **A term can be dropped only if the domain makes it smaller.** For $m + n$, neither term dominates the other, so both are kept, or the bound is written as $\max(m, n)$. For graphs, a domain such as "connected" gives $n - 1 \le m$, and then $n + m \le 2m + 1 \le 3m$ for $m \ge 1$, so $\Theta(n + m) = \Theta(m)$. Without the condition, $\Theta(n + m) \ne \Theta(m)$: a graph with $n$ vertices and no edges has $m = 0$.
- **A substitution works in one direction.** If $f = O(g)$ in either sense, then each substitution $m = m(n)$ with $m(n) \to \infty$ and $(m(n), n) \in D$ gives a one-variable bound $f(m(n), n) = O(g(m(n), n))$. The converse is false: a bound along the curve $m = n$ says nothing for other values. Let $T(m, n) = 0$ if $m = n$, and $T(m, n) = 2^m$ otherwise. Along the curve $m = n$ the bound $T = O(1)$ holds, yet $T$ is not bounded by any polynomial in $m$ and $n$.
- **The summation rule can fail.** In one variable, $f = O(g)$ gives $\sum_{i=0}^{m} f(i) = O\left(\sum_{i=0}^{m} g(i)\right)$. Let $D = \mathbb{N}^2$ with points $(i, n)$, and let $f(i, n) = 2^n$ if $i = 0$ and $f(i, n) = 1$ otherwise, with $g = 1$. Then $f \in O_{\mathrm{all}}(g)$ with $N = 1$ and $c = 1$, because only the points with $i = 0$ break the bound. The sums are $\sum_{i=0}^{m} f(i, n) = 2^n + m$ and $\sum_{i=0}^{m} g(i, n) = m + 1$. For $m = N$ and $n$ large, $2^n + m > c\,(m + 1)$ for each $c$, so the first sum is not in $O_{\mathrm{all}}$ of the second as a function of $(m, n)$. A loop analysis that uses the all-variables-large definition can therefore give a wrong bound. Howell studies this problem and the rules that survive in his report. The example does not apply to $O_{\mathrm{fin}}$, because $f \notin O_{\mathrm{fin}}(g)$: the points $(0, n)$ are infinitely many.
- **Limits are not simple.** The ratio $f/g$ can tend to different values along different paths to infinity, so the limit tests of [comparing growth by limits](/comparing-growth-by-limits/) apply along a path, not to the whole domain.

## Examples

- **Breadth-first search.** On a graph with $n$ vertices and $m$ edges, in an [adjacency list](/adjacency-list/), [breadth-first search](/breadth-first-search/) initializes $n$ marks and scans the list of each vertex that it reaches, once. The sum of all list lengths is $m$ for a directed graph and $2m$ for an undirected one. So the time is $O(n + m)$ on every input. When every vertex is reachable from the source, as in a connected undirected graph, the algorithm scans every list and the time is $\Theta(n + m)$. If the source has no edges, the time is $\Theta(n)$ whatever $m$ is. The bound $O(m)$ is false in general: with $m = 0$ the algorithm still initializes $n$ marks. For a connected graph, $n \le m + 1$, so $\Theta(n + m) = \Theta(m)$.
- **Sorting the edges.** [Kruskal's algorithm](/kruskal/) sorts the $m$ edges, which takes $O(m \log m)$ comparisons. For a simple graph with $n \ge 2$ and $m \ge 1$ we have $m \le n^2$, so $\lg m \le 2 \lg n$ and $m \log m = O(m \log n)$. For a connected simple graph with $n \ge 3$ we also have $m \ge n - 1 \ge \sqrt{n}$, so $\lg m \ge \tfrac12 \lg n$ and $m \log n = O(m \log m)$. So for connected simple graphs, $\Theta(m \log m) = \Theta(m \log n)$. The step $n - 1 \ge \sqrt{n}$ holds at $n = 3$ ($2 \ge 1.73$), and the difference $n - 1 - \sqrt{n}$ grows with $n$.
- **Shortest paths.** [Dijkstra's algorithm](/dijkstra/) with a [binary heap](/binary-heap/) runs in $O((n + m) \log n)$ time. For a connected graph this is $O(m \log n)$. With a [Fibonacci heap](/fibonacci-heap/) it runs in $O(m + n \log n)$, which is better when $m$ is much larger than $n$. The two bounds can be compared only as functions of both $m$ and $n$.
- **Matrix product.** The classical algorithm for an $a \times b$ matrix times a $b \times c$ matrix makes exactly $a b c$ multiplications of entries. The cost is $\Theta(abc)$ with three variables, and no variable can be dropped.
- **Dense and sparse graphs.** For a simple graph, $m \le n(n-1)/2$, so $O(n + m)$ is at most $O(n^2)$. A [sparse graph](/sparse-graph/) has $m = O(n)$, so $O(n + m) = O(n)$. A [dense graph](/dense-graph/) has $m = \Theta(n^2)$, so $O(n + m) = O(n^2)$. These are bounds on a restricted domain, a region of the $(m, n)$ plane, and the statement of that domain is needed for them.
- **Non-example.** "Breadth-first search takes $O(n)$ time" is false. The complete bipartite graph with $n/2$ vertices on each side (for even $n$) has $n^2/4$ edges and is connected. A search from any vertex scans all lists, with $n^2/2$ entries in total, so it takes $\Theta(n^2)$ time on this family.

## Where it is used

Graph algorithms use $n$ and $m$ (the texts of Cormen et al. write $V$ and $E$ inside the notation for $|V|$ and $|E|$). Algorithms on strings and matrices use the two or three dimensions. A cost like $O(m + n)$ is written without a further reduction when $m$ and $n$ are independent. The forms $O(m \log n)$ and $O(m + n \log n)$ make the comparison of algorithms possible for sparse and dense graphs. Any such statement should name the domain (simple, connected, directed) and the reading of "large".

## References
