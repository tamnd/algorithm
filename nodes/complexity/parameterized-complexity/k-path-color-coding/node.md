---
tag: BTJ3GM
kind: algorithm
slug: k-path-color-coding
name: k-path algorithm by color coding
aliases:
- color-coding longest path
area: complexity/parameterized-complexity
level: advanced
summary: "Color the vertices at random with k colors and find a path with k different colors by dynamic programming over color sets. About e^k colorings find a k-path with constant probability."
solves: [parameterized-longest-path]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the number of vertices on the path}
  time: {worst: "O(5.44^k (n + m))"}
  space: {extra: O(2^k n + m)}
properties: {randomized: true, one_sided_error: true, success_per_coloring: "k!/k^k", fixed_parameter_tractable: true}
history:
  year: 1995
  people: [Noga Alon, Raphael Yuster, Uri Zwick]
  note: Alon, Yuster and Zwick introduced color coding in the Journal of the ACM in 1995, with simple paths and cycles of length k as the first application, and derandomized it with families of perfect hash functions.
prereqs: [color-coding, parameterized-longest-path]
see_also: [divide-and-color, representative-families, graph-motif, longest-path-problem, held-karp-algorithm, bitmask-dp, perfect-hashing, one-sided-error]
sources:
  - paper: doi:10.1145/210332.210337
    title: "Noga Alon, Raphael Yuster and Uri Zwick, Color-coding, Journal of the ACM 42(4), 844-856 (1995)"
    locator: the color-coding method and its use for simple paths and cycles of length k
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Section 5.2, Color coding (5.2.1, A color coding algorithm for Longest Path), and the derandomization in Chapter 5
  - paper: doi:10.1109/SFCS.1995.492475
    title: "Moni Naor, Leonard J. Schulman and Aravind Srinivasan, Splitters and near-optimal derandomization, 36th Annual Symposium on Foundations of Computer Science (FOCS 1995), 182-191"
    locator: the construction of (n, k)-perfect hash families of size e^k k^O(log k) log n
  - paper: doi:10.1016/j.ipl.2008.11.004
    title: "Ryan Williams, Finding paths of length k in O*(2^k) time, Information Processing Letters 109(6), 315-318 (2009)"
    locator: the randomized algebraic algorithm that replaces color coding
---

The color coding algorithm for k-path decides [p-Longest-Path](/parameterized-longest-path/): given a graph $G$ with $n$ vertices and $m$ edges and an integer $k$, does $G$ have a simple path with $k$ vertices? The parameter is $k$. The algorithm colors the vertices at random with $k$ colors and then looks only for a *colorful* path, one whose $k$ vertices have pairwise different colors. A colorful path is simple by force, so the search only needs to remember the *set* of colors used so far, not the vertices. Dynamic programming over (end vertex, color set) pairs finds a colorful path in $O(2^k m)$ time. A fixed $k$-path becomes colorful with probability $k!/k^k > e^{-k}$, so about $e^k$ random colorings find it with constant probability. The total time is $O((2e)^k (n + m))$ for a fixed error probability, which is [fixed-parameter tractable](/fixed-parameter-tractable/). The error is [one-sided](/one-sided-error/): a path that the algorithm returns is always a real path. The general method is on the page [color coding](/color-coding/).

## In plain words

You want to know if a road map has a route through a given number of towns that never visits a town twice. Checking every route is too slow. So paint each town with one of as many paints as there are towns on the route, picked at random.

Then look only for routes where each town has its own paint. Such a route can never come back to a town, because the paint would repeat. To build these routes step by step, you only have to remember where the route ends and which paints it has used. That list is short for a short route.

If a good route exists, a random paint job gives all its towns different paints with a fair chance. Repeat it a few thousand times, and you find the route almost surely. If no route exists, the method never claims one.

## The problem

The input is a graph $G = (V, E)$ with $n$ vertices and $m$ edges, given by adjacency lists, and an integer $k \ge 1$. A *k-path* is a sequence of $k$ distinct vertices $v_1, \ldots, v_k$ in which $v_i$ and $v_{i+1}$ are adjacent. The output is a $k$-path if one exists, and NONE otherwise. The graph can be undirected or directed; for a directed graph the lists hold the out-neighbors, and the same algorithm finds directed paths. Some authors count the length of a path in edges; a path of length $k - 1$ in edges has $k$ vertices.

A *coloring* is a map $c: V \to \{1, \ldots, k\}$. A path is *colorful* under $c$ if its vertices have pairwise different colors. A colorful path with $k$ vertices uses each of the $k$ colors exactly once.

## The algorithm

$D[v, S]$ is set when some colorful path ends at $v$ and uses exactly the colors in $S$. It stores the vertex before $v$ on one such path, or a mark for a path of one vertex. The sets $S$ are $k$-bit masks.

```pseudo id=main
COLORFUL-PATH(G, c, k)         ▷ a colorful path with k vertices, or NONE
L1  for each vertex v do D[v, {c(v)}] ← start
L2  for i ← 1 to k - 1 do
L3      for each entry D[u, S] with |S| = i and each neighbor v of u do
L4          if c(v) ∉ S and D[v, S ∪ {c(v)}] is not set then D[v, S ∪ {c(v)}] ← u
L5  if D[v, {1, …, k}] is set for some v then return the path traced back from (v, {1, …, k})
L6  return NONE

K-PATH(G, k, t)                ▷ t is the number of colorings to try
L7  repeat t times
L8      pick c(v) uniformly in {1, …, k} for each vertex v, independently
L9      P ← COLORFUL-PATH(G, c, k); if P ≠ NONE then return P
L10 return NONE
```

The trace back at L5 starts at $(v, S)$ with $S = \{1, \ldots, k\}$, steps to $(D[v, S], S \setminus \{c(v)\})$, and stops at an entry marked start. It visits $k$ vertices, and their colors are different, so it is a $k$-path.

For an error probability of at most $\delta$, take $t = \lceil \ln(1/\delta) \cdot k^k / k! \rceil$. Since $k^k / k! < e^k$, the rule $t = \lceil e^k \ln(1/\delta) \rceil$ is also safe, but it does more work than needed.

The table stores at most one predecessor per pair. The *counting* form replaces it with the number $N[v, S]$ of colorful paths that end at $v$ with the color set $S$: $N[v, \{c(v)\}] = 1$, and line L4 adds $N[u, S]$ to $N[v, S \cup \{c(v)\}]$. The sum of $N[v, \{1, \ldots, k\}]$ over all $v$ is the number of colorful $k$-paths as vertex sequences; in an undirected graph each path with $k \ge 2$ appears twice, once in each direction.

## Example

Let $G$ have the vertices $a, b, c, d, e, f$ and the edges $ab$, $bc$, $cd$, $de$, $be$ and $ef$: a path $a$ to $f$ with the chord $be$. Let $k = 4$. A brute-force search finds 9 simple paths with 4 vertices, or 18 as vertex sequences.

Take the coloring $a \mapsto 1$, $b \mapsto 2$, $c \mapsto 1$, $d \mapsto 2$, $e \mapsto 3$, $f \mapsto 4$. Line L1 sets six entries, one per vertex. The loop then sets these entries, layer by layer:

| size of $S$ | entries $(v, S)$ that are set |
|---|---|
| 2 | $(a, \{1,2\})$, $(b, \{1,2\})$, $(b, \{2,3\})$, $(c, \{1,2\})$, $(d, \{1,2\})$, $(d, \{2,3\})$, $(e, \{2,3\})$, $(e, \{3,4\})$, $(f, \{3,4\})$ |
| 3 | $(a, \{1,2,3\})$, $(b, \{2,3,4\})$, $(c, \{1,2,3\})$, $(d, \{2,3,4\})$, $(e, \{1,2,3\})$, $(f, \{2,3,4\})$ |
| 4 | $(a, \{1,2,3,4\})$, $(c, \{1,2,3,4\})$, $(f, \{1,2,3,4\})$ |

The table has $6 + 9 + 6 + 3 = 24$ entries. For example, $(e, \{1,2,3\})$ comes from $(b, \{1,2\})$ over the edge $be$, because $c(e) = 3$ is new. The edge $de$ reaches the same entry from $(d, \{1, 2\})$, and line L4 keeps the first predecessor. The entry $(f, \{1,2,3,4\})$ traces back through $(e, \{1,2,3\})$ and $(b, \{1,2\})$ to $(a, \{1\})$, so COLORFUL-PATH returns $a, b, e, f$. The counting form gives 6 colorful vertex sequences, which are the three paths $a b e f$, $c b e f$ and $c d e f$ in both directions. The other six paths repeat a color; for example $a b c d$ has the colors $1, 2, 1, 2$.

With the coloring $a \mapsto 1$, $b \mapsto 1$, $c \mapsto 2$, $d \mapsto 3$, $e \mapsto 2$, $f \mapsto 4$, the table has 20 entries and no entry with all four colors, so COLORFUL-PATH returns NONE, although $G$ has 4-paths.

Over all $4^6 = 4096$ colorings, exactly 1392 find a 4-path, a fraction of $0.340$. Each of the 9 paths alone is colorful with probability $4!/4^4 = 0.09375$, and the paths share vertices, so the fraction for the whole graph is higher than for one path. With $\delta = 0.01$, K-PATH tries at most $t = 50$ colorings.

## Correctness

The proof is in the proof file of this page. It has three steps.

1. *The table is exact.* By induction on $|S|$, an entry $D[v, S]$ is set exactly when $G$ has a colorful path that ends at $v$ and uses exactly the colors $S$. Line L4 extends a colorful path ending at $u$ by the edge $uv$ when $c(v)$ is new, and every colorful path with at least two vertices arises in this way from its prefix. So COLORFUL-PATH returns a path exactly when a colorful $k$-path exists, and the trace back yields one.
2. *One coloring.* Fix a $k$-path $P$. Its $k$ vertices get independent uniform colors, and $P$ is colorful exactly when the colors form a permutation of $\{1, \ldots, k\}$. There are $k!$ such outcomes out of $k^k$, so the probability is $k!/k^k$. From $e^k = \sum_{i \ge 0} k^i / i! > k^k / k!$ we get $k!/k^k > e^{-k}$.
3. *Many colorings.* The colorings are independent, so all $t$ miss $P$ with probability at most $(1 - k!/k^k)^t \le \exp(-t \cdot k!/k^k) \le \delta$ for the $t$ above. A returned path is always a $k$-path, so the error is one-sided: on a no-instance the answer is always NONE.

## Complexity

**One coloring.** Each pair $(u, S)$ with $c(u) \in S$ is set at most once and processed once at L3, where it scans the $\deg(u)$ neighbors of $u$. With $S$ held in one machine word, each test and union at L4 is $O(1)$. There are $2^{k-1}$ sets that contain a given color, so the work is at most $\sum_u 2^{k-1} \deg(u) = 2^k m$, plus $O(n)$ for line L1 and $O(k)$ for the trace back. So COLORFUL-PATH runs in $O(2^k m + n)$ time. If the sets are kept as lists of up to $k$ colors, each set operation costs $O(k)$ and the bound is $O(2^k k m + n)$, the form that some texts give.

**All colorings.** K-PATH runs COLORFUL-PATH $t = \lceil \ln(1/\delta) k^k / k! \rceil$ times, and each coloring costs $O(n)$. Since $k^k/k! < e^k$, the total time is $O(e^k \cdot 2^k (n + m) \log(1/\delta)) = O((2e)^k (n + m) \log(1/\delta))$, and $2e \approx 5.44$. The space is $O(2^k n + m)$ for one table and the graph.

The table shows the success probability of one coloring for one fixed path, the number $k^k/k!$ of colorings for one expected success, the cruder bound $e^k$, the number of colorings $t$ for $\delta = 0.01$, and the factor $2^k$ of one coloring.

| $k$ | $k!/k^k$ | $k^k/k!$ | $e^k$ | $t$ for $\delta = 0.01$ | $2^k$ |
|---|---|---|---|---|---|
| 4 | 0.09375 | 10.7 | 54.6 | 50 | 16 |
| 6 | 0.01543 | 64.8 | 403 | 299 | 64 |
| 8 | 0.00240 | 416 | 2981 | 1917 | 256 |
| 10 | 0.000363 | 2756 | 22026 | 12691 | 1024 |

By Stirling's formula $k^k / k! \approx e^k / \sqrt{2 \pi k}$, so the crude bound $e^k$ is off by a factor of about $\sqrt{2 \pi k}$.

## Properties

- **One-sided error.** On a no-instance the answer is always NONE. On a yes-instance the answer is NONE with probability at most $\delta$. This makes it a [Monte Carlo algorithm](/monte-carlo-algorithm/) in the class of algorithms with one-sided error.
- **Single-exponential in k.** The time is $2^{O(k)} (n + m)$, linear in the size of the graph for fixed $k$.
- **Exponential space in k.** The table has up to $2^{k-1} n$ entries. The [divide and color](/divide-and-color/) method and the algebraic methods use polynomial space.
- **Easy to extend.** The same table finds a colorful path of least weight (keep the least weight per entry), a colorful path between two given vertices, or a colorful cycle (check for an edge from the last vertex back to the first).

## Variants and improvements

- **Derandomization.** Replace the random colorings by an $(n, k)$-perfect hash family: a list of maps $V \to \{1, \ldots, k\}$ such that every set of $k$ vertices is colorful under at least one map. Naor, Schulman and Srinivasan (1995) built such families of size $e^k k^{O(\log k)} \log n$, which gives a deterministic algorithm in time $(2e)^k k^{O(\log k)} m \log n$. Alon, Yuster and Zwick used families built from [perfect hashing](/perfect-hashing/) with a larger size, still $2^{O(k)} \log n$.
- **More colors.** With $ck$ colors for a constant $c > 1$, a fixed path is colorful with a higher probability, but the table grows to $2^{ck}$ sets per vertex. The product of the two factors changes only a little: for $k = 8$ it is about $1.1 \cdot 10^5$ with 8 colors, $8.8 \cdot 10^4$ with 12 colors and $5.4 \cdot 10^5$ with 16 colors. See [color coding](/color-coding/) for the numbers.
- **Divide and color.** A random split of the vertices into two halves, applied recursively, gives randomized time $4^k k^{O(1)} m$ with polynomial space (Chen et al., 2009). See [divide and color](/divide-and-color/).
- **Algebraic methods.** Koutis (2008) and Williams (2009) test whether a polynomial over a field of characteristic 2 has a multilinear term, in randomized time $O^*(2^k)$, where $O^*$ hides factors polynomial in $n$. Björklund, Husfeldt, Kaski and Koivisto (2017) gave $O^*(1.66^k)$ for undirected graphs.
- **Deterministic and fast.** [Representative families](/representative-families/) give deterministic time $O(2.619^k n \log n)$ (Fomin, Lokshtanov, Panolan and Saurabh, 2016).
- **Approximate counting.** The counting form gives the number $X$ of colorful $k$-paths for one coloring. Since each $k$-path is colorful with probability $k!/k^k$, the value $X \cdot k^k / k!$ is an unbiased estimate of the number of $k$-paths. Exact counting of $k$-paths is #W[1]-hard (Flum and Grohe, 2004).

## When to use it

Use it to find paths, cycles or small trees with up to about 10 to 12 vertices in large sparse graphs, for example motifs in biological networks. The code is short, and the table for one coloring is a plain [bitmask DP](/bitmask-dp/) over color sets. For $k$ above about 15, the $(2e)^k$ factor is too large; use the algebraic $O^*(2^k)$ method if randomized answers are fine, or representative families for a deterministic answer. For a Hamiltonian path in a small graph, the [Held-Karp algorithm](/held-karp-algorithm/) is the same DP over vertex sets, with no coloring.

## Pitfalls

- **Tracking only the length.** A DP that stores only the end vertex and the number of vertices counts walks, not paths. The walk $a, b, a, b$ looks like a 4-path. The color set is what makes the path simple.
- **One coloring.** A single coloring misses the path with probability $1 - k!/k^k$, which is 0.906 already for $k = 4$. The answer NONE after one coloring means nothing.
- **Too few trials.** The number of trials must grow like $k^k/k!$, roughly $e^k$. A fixed number such as 100 is too small for $k = 8$, where one coloring succeeds with probability $0.0024$ per path.
- **Reading the error the wrong way.** A returned path is certain. A NONE is only probably right. Do not report NONE as a proof that no $k$-path exists.
- **A seed that repeats.** Each trial needs fresh random colors. Reseeding the generator with the same seed inside the loop tries the same coloring $t$ times.
- **Counting both directions.** In an undirected graph the counting form counts each path twice. Divide by 2 for $k \ge 2$.
- **Masks wider than a word.** For $k$ larger than the word size, set operations are no longer $O(1)$. This does not matter in practice, because $2^k$ entries per vertex are too many long before that.

## Implementations

## History

Monien (1985) gave the first FPT algorithm for $k$-path, in time $O(k! \cdot nm)$, using an early form of representative families. Bodlaender (1993) improved it to $O(2^k k! \cdot n)$. Alon, Yuster and Zwick (1995) introduced color coding and found $k$-paths in randomized time $2^{O(k)} m$, and deterministic time $2^{O(k)} m \log n$, So a path with $O(\log n)$ vertices can be found in polynomial time, which answered a question of Papadimitriou and Yannakakis. The base of the exponent then fell from $2e$ to 4 with divide and color (Chen, Kneis, Lu, Mölle, Richter, Rossmanith, Sze and Zhang; Kneis, Mölle, Richter and Rossmanith, 2006), to 2 with the algebraic method of Koutis (2008) and Williams (2009), and to 1.66 for undirected graphs (Björklund, Husfeldt, Kaski and Koivisto). Color coding stays the simplest method, and the one most used in practice.

## References
