---
tag: 6KA5ES
kind: technique
slug: color-coding
name: Color coding
aliases:
- chromatic coding
area: complexity/parameterized-complexity
level: advanced
summary: "Color the vertices at random with k colors and search only for a solution whose k vertices get different colors. Repeat about e^k times; perfect hash families remove the randomness."
prereqs: [fixed-parameter-tractable, monte-carlo-algorithm]
see_also: [k-path-color-coding, divide-and-color, parameterized-longest-path, graph-motif, representative-families, perfect-hashing, k-wise-independence, inclusion-exclusion-principle]
sources:
  - paper: doi:10.1145/210332.210337
    title: "Noga Alon, Raphael Yuster and Uri Zwick, Color-coding, Journal of the ACM 42(4), 844-856 (1995)"
    locator: the color-coding method, its use for paths, cycles and subgraphs of bounded treewidth, and its derandomization
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 5, Randomized methods in parameterized algorithms (Section 5.2, Color coding; Section 5.4, A divide and color algorithm for Longest Path; the derandomization of these methods)
  - paper: doi:10.1109/SFCS.1995.492475
    title: "Moni Naor, Leonard J. Schulman and Aravind Srinivasan, Splitters and near-optimal derandomization, 36th Annual Symposium on Foundations of Computer Science (FOCS 1995), 182-191"
    locator: (n, k)-perfect hash families of size e^k k^O(log k) log n
---

Color coding is a randomized method for finding a small pattern with $k$ vertices, such as a path, a cycle or a tree, in a large graph with $n$ vertices. It colors the vertices at random with $k$ colors and then looks only for a *colorful* copy of the pattern, one whose $k$ vertices have pairwise different colors. Two things make this work. First, a colorful search does not need to remember which vertices it has used, only which colors, and there are $2^k$ color sets instead of about $n^k$ vertex sets. So dynamic programming over color sets finds a colorful copy in time $2^{O(k)} \cdot \mathrm{poly}(n)$. Second, a fixed copy becomes colorful with probability $k!/k^k > e^{-k}$, so about $e^k$ independent colorings find it with constant probability. Together this gives [fixed-parameter tractable](/fixed-parameter-tractable/) algorithms with one-sided error, and families of perfect hash functions make them deterministic. Alon, Yuster and Zwick introduced the method in 1995. The algorithm for paths is on the page [k-path by color coding](/k-path-color-coding/).

## In plain words

You look for a small group in a big network, for example a chain of a few people who know each other. The hard part is to keep the chain from using a person twice. Remembering the people already used costs too much.

So give each person a random badge, with one badge color per place in the chain. Then look only for chains in which all badges differ. Such a chain can never use a person twice, and you only need to remember which badge colors you have used, which is a short list.

Random badges can give two people of the chain the same color, and then you miss it. But a good set of badges comes up with a fair chance, so you repeat many times. If you never find a chain, very likely none exists. A chain that you find is always right.

## When it applies

- The solution is a set of $k$ vertices (or edges) with some structure, and the parameter is $k$.
- If the $k$ vertices are known to be distinct, the structure is easy to find. The difficulty is only to avoid using a vertex twice. Paths, cycles, trees, and patterns of bounded [treewidth](/treewidth/) are the main cases.
- A search that keeps the set of used *colors* instead of the set of used *vertices* fits in $2^{O(k)} \cdot \mathrm{poly}(n)$ time.
- One-sided error is acceptable, or a deterministic run time with an extra factor $k^{O(\log k)} \log n$ is acceptable.

It does not apply to patterns that are hard even when they are colorful. A colorful $k$-clique is no easier to find than a $k$-clique, and $k$-clique is W[1]-hard (see [parameterized clique](/parameterized-clique/)).

## The template

The template has three holes. $K$ is the number of colors, usually $k$. FIND-COLORFUL$(I, c)$ decides, in time $T(k, n)$, whether the instance $I$ has a solution whose vertices get pairwise different colors under $c$, and returns one if so. $t$ is the number of trials.

```pseudo id=main
COLOR-CODE(I, k, K, t)                 ▷ a solution with k vertices, or NONE
L1  repeat t times
L2      for each vertex v do c(v) ← a uniform random color in {1, …, K}
L3      X ← FIND-COLORFUL(I, c)
L4      if X ≠ NONE then return X
L5  return NONE
```

**Lemma (random coloring).** Let $X$ be a fixed set of $k$ vertices, and let $c$ give each vertex a uniform color from $\{1, \ldots, K\}$, independently, with $K \ge k$. Then $X$ is colorful with probability

$$p(k, K) = \frac{K (K - 1) \cdots (K - k + 1)}{K^k}.$$

For $K = k$ this is $k!/k^k$, and $k!/k^k > e^{-k}$.

*Proof.* The colors of the $k$ vertices of $X$ form a uniform element of $\{1, \ldots, K\}^k$. They are pairwise different for $K (K - 1) \cdots (K - k + 1)$ of the $K^k$ elements. For the bound, $e^k = \sum_{i \ge 0} k^i/i!$ has the term $k^k/k!$ and other positive terms, so $e^k > k^k / k!$. $\square$

**Lemma (repetition).** If FIND-COLORFUL is correct, COLOR-CODE never returns a wrong solution, and if a solution $X$ exists, COLOR-CODE misses every solution with probability at most $(1 - p)^t \le e^{-pt}$, where $p = p(k, K)$. With $t = \lceil \ln(1/\delta)/p \rceil$ this is at most $\delta$.

*Proof.* Every returned value comes from FIND-COLORFUL, which is correct. If a solution $X$ exists, each trial makes $X$ colorful with probability $p$, independently of the other trials, and then FIND-COLORFUL returns some solution. All $t$ trials fail with probability at most $(1 - p)^t$, and $1 - p \le e^{-p}$. $\square$

So the time is $O(t \cdot (n + T(k, n)))$, which is $O(e^k \cdot T(k, n) \log(1/\delta))$ for $K = k$, plus the time to draw the colorings.

**Derandomization.** An $(n, k)$-*perfect hash family* is a list of functions $V \to \{1, \ldots, k\}$ such that every set of $k$ vertices is colorful under at least one of them. If L1 and L2 run over such a family instead of random colorings, the algorithm becomes deterministic and exact. Naor, Schulman and Srinivasan (1995) built families of size $e^k k^{O(\log k)} \log n$ in time linear in their size, so the deterministic time is $e^k k^{O(\log k)} \log n \cdot T(k, n)$.

**The trade-off for K.** More colors make a solution colorful more often, but the colorful search then works with sets of up to $K$ colors. For a search that costs $2^K$ per coloring, the work for one expected success is $2^K / p(k, K)$:

| $k$ | $K$ | $p(k, K)$ | $1/p$ | $2^K$ | $2^K/p$ |
|---|---|---|---|---|---|
| 5 | 5 | 0.0384 | 26.0 | 32 | 833 |
| 5 | 10 | 0.3024 | 3.3 | 1024 | 3386 |
| 8 | 8 | 0.0024 | 416 | 256 | $1.07 \cdot 10^5$ |
| 8 | 12 | 0.0464 | 21.5 | 4096 | $8.8 \cdot 10^4$ |
| 8 | 16 | 0.1208 | 8.3 | 65536 | $5.4 \cdot 10^5$ |

So $K = k$ is close to the best choice. More colors help when the search costs much less than $2^K$, for example when only colors of a few vertices matter.

## Classic examples

### k-path

A path with $k$ vertices. FIND-COLORFUL is a dynamic program over pairs $(v, S)$: is there a colorful path that ends at $v$ and uses exactly the color set $S$? A path ending at $v$ with set $S$ extends along an edge $vw$ to $(w, S \cup \{c(w)\})$ when $c(w) \notin S$. This takes $O(2^k m)$ time per coloring, and the total is $O((2e)^k (n + m))$ for a fixed error. See [k-path by color coding](/k-path-color-coding/) for the algorithm, a worked trace, a proof and code, and [parameterized longest path](/parameterized-longest-path/) for the problem.

### k-cycle

A cycle with exactly $k$ vertices. Fix a start vertex $s$, run the path table only from $s$, and check whether some colorful path from $s$ with all $k$ colors ends at a neighbor of $s$. Doing this for every $s$ costs $O(2^k n m)$ per coloring. A long cycle with *at least* $k$ vertices needs a different argument, because the cycle may be much longer than $k$.

### Trees and patterns of bounded treewidth

A tree $T$ with $k$ vertices. Root $T$ at a vertex $r$. For each subtree $T_x$, each vertex $v$ of $G$ and each color set $S$ with $|S| = |T_x|$, the table says whether $T_x$ has a colorful copy with $x$ mapped to $v$ and with colors exactly $S$. A node $x$ with a child $y$ combines a copy of $T_x$ without the subtree of $y$, with colors $S_1$, and a copy of $T_y$ at a neighbor of $v$, with colors $S_2$, where $S_1$ and $S_2$ are disjoint. The disjoint colors make the two parts vertex-disjoint. Summed over all pairs of disjoint sets this is $3^k$ per edge, so the time per coloring is $O(3^k k m)$. Alon, Yuster and Zwick extend this to every pattern of treewidth $w$, in time $2^{O(k)} n^{w + 1}$ per coloring, using a [tree decomposition](/tree-decomposition/) of the pattern.

### Graph motif with a colorful motif

In [graph motif](/graph-motif/) the coloring is part of the input: find a connected set of vertices whose colors match a given multiset. When the multiset has $k$ different colors, the instance asks for a connected colorful set, and the colorful dynamic program solves it with no random step, in time $O^*(3^k)$ by the same splitting of color sets as for trees, where $O^*$ hides factors polynomial in $n$.

## Variations

- **Divide and color.** Instead of $k$ colors, use 2 colors at random and recurse on each half. This gives $4^k$ instead of $(2e)^k$ for paths and needs only polynomial space. See [divide and color](/divide-and-color/).
- **Counting.** The colorful table can count colorful copies. A fixed copy is colorful with probability $p$, so the number of colorful copies divided by $p$ is an unbiased estimate of the number of copies. Averaging over many colorings gives an approximate count, which is used to count small motifs in biological networks. Exact counting of $k$-paths is #W[1]-hard (Flum and Grohe, 2004).
- **Edge colorings and random separation.** For patterns given by edges, color the edges instead of the vertices. A related method of Cai, Chan and Chan colors each vertex with one of 2 colors and asks that the solution gets one color and its neighbors the other.
- **Many colors.** Some algorithms color with a number of colors that is a function of $k$ much larger than $k$ and ask only that a few chosen pairs of vertices get different colors. Alon, Lokshtanov and Saurabh (2009) used this idea for subexponential algorithms on dense problems, such as feedback arc set in tournaments.
- **Polynomial space.** A walk with $k$ vertices is colorful exactly when it uses all $k$ colors. So, by the [inclusion-exclusion principle](/inclusion-exclusion-principle/), the number of colorful walks is $\sum_{X} (-1)^{k - |X|} w(X)$, where $X$ runs over the $2^k$ sets of colors and $w(X)$ counts the walks with $k$ vertices whose colors all lie in $X$. Each $w(X)$ takes polynomial time by counting walks, so FIND-COLORFUL for paths runs in $O^*(2^k)$ time and polynomial space. The algebraic methods of Koutis and Williams replace colors by variables of a polynomial and find $k$-paths in randomized time $O^*(2^k)$.
- **Deterministic with representative families.** [Representative families](/representative-families/) keep, for each partial solution, a small family that is enough to extend it. This gives deterministic algorithms that are faster than derandomized color coding.

## Pitfalls

- **Patterns that are hard when colorful.** Color coding removes only the difficulty of keeping vertices distinct. A colorful $k$-clique is as hard as a $k$-clique, so the method gives nothing there.
- **Too few trials.** A fixed pattern is colorful with probability only $k!/k^k$, which is 0.0024 for $k = 8$. With a fixed small number of trials, the error is not bounded.
- **Two-sided error by mistake.** The method must only return solutions that FIND-COLORFUL has built and checked. A heuristic step that can report a false solution breaks the one-sided error.
- **Dependent colorings.** The bound $(1 - p)^t$ needs independent trials. Reusing the same seed, or deriving colorings from a hash with few bits of randomness, can make the trials dependent. Perfect hash families give a guarantee without independence.
- **A table indexed by size.** Keeping only the number of colors used, not the set, loses the guarantee that the vertices are distinct.
- **The wrong count of colors.** With $K < k$ colors, no pattern with $k$ vertices is colorful, and the algorithm always says NONE.

## Exercises

1. Show that a fixed set of $k$ vertices is colorful under a uniform coloring with $K$ colors with probability $K (K - 1) \cdots (K - k + 1)/K^k$, and that for $K = k^2$ this is at least $1/e$ when $k \ge 2$.
2. Give the color coding algorithm for a cycle with exactly $k$ vertices in a directed graph, and bound its time per coloring.
3. Let $T$ be a star with $k$ vertices. Show that a copy of $T$ can be found in polynomial time without color coding. Which property of the star makes this easy?
4. Use color coding with $3k$ colors to decide in time $2^{O(k)} n^{O(1)}$ whether a graph has $k$ vertex-disjoint triangles.
5. Prove that a list of $(n, k)$-perfect hash functions must have at least $\log_k n$ functions when $k \ge 2$.

## References
