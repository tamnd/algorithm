---
tag: DJ7Z05
kind: technique
slug: cut-and-count
name: Cut and count
area: complexity/parameterized-complexity
level: research
summary: "Count pairs of a candidate set and a consistent cut modulo 2: disconnected candidates cancel. With the isolation lemma, connectivity problems get 3^t or 4^t Monte Carlo algorithms in the treewidth t."
prereqs: [tree-decomposition, treewidth, monte-carlo-algorithm]
see_also: [parameterized-steiner-tree, treewidth, parameterized-feedback-vertex-set, one-sided-error, strong-exponential-time-hypothesis, hamiltonian-cycle-problem, courcelle-theorem, monte-carlo-algorithm]
sources:
  - paper: doi:10.1145/3506707
    title: "Marek Cygan, Jesper Nederlof, Marcin Pilipczuk, Michal Pilipczuk, Johan M. M. van Rooij and Jakub Onufry Wojtaszczyk, Solving connectivity problems parameterized by treewidth in single exponential time, ACM Transactions on Algorithms 18(2), article 17 (2022)"
    locator: Section 1 (Theorems 1.1 to 1.6), Lemma 2.5 (isolation), Section 3 (Steiner tree, Lemmas 3.3 and 3.4, Algorithm 1); conference version FOCS 2011
  - paper: doi:10.1007/BF02579206
    title: "Ketan Mulmuley, Umesh V. Vazirani and Vijay V. Vazirani, Matching is as easy as matrix inversion, Combinatorica 7(1), 105-113 (1987)"
    locator: the isolation lemma
  - paper: doi:10.1016/j.ic.2014.12.008
    title: "Hans L. Bodlaender, Marek Cygan, Stefan Kratsch and Jesper Nederlof, Deterministic single exponential time algorithms for connectivity problems parameterized by treewidth, Information and Computation 243, 86-111 (2015)"
    locator: the rank-based approach, a deterministic alternative
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 11, Improving dynamic programming on tree decompositions (cut and count)
---

Cut and count is a method for problems with a connectivity condition, such as Steiner tree, connected vertex cover or Hamiltonian cycle, on graphs of small [treewidth](/treewidth/). The parameter is the width $t$ of a given tree decomposition. Usual dynamic programming must remember how the vertices of a bag are connected, which costs $t^{O(t)}$ states. Cut and count instead counts pairs of a candidate set and a *consistent cut* of it modulo 2. Each connected candidate is counted once, and each disconnected one an even number of times. A random weight function with the isolation lemma makes some count odd. Cygan, Nederlof, Pilipczuk, Pilipczuk, van Rooij and Wojtaszczyk introduced the method in 2011. It gives Monte Carlo algorithms with one-sided error in time $3^t n^{O(1)}$ for Steiner tree and $4^t n^{O(1)}$ for Hamiltonian cycle.

## In plain words

Suppose you want a connected set of vertices with some property. Checking connectedness in a table that moves through the graph piece by piece is costly, because the table must remember which vertices are joined.

Cut and count avoids this. It counts candidate sets together with a way to color each chosen vertex left or right, so that no edge joins a left vertex to a right vertex. A connected set has exactly one such coloring once one fixed vertex is always left. A set with several pieces has an even number of colorings, since each other piece can flip. So if you count only odd or even, sets with several pieces disappear. Each step of the table only checks single edges, which is cheap.

Two connected sets can also cancel each other. Random weights fix this: with good chance, some weight value has exactly one connected set.

## When it applies

- The solutions are the connected sets in a larger family that is easy to count, for example vertex sets of size $k$ that contain the terminals, or edge sets with the right degrees.
- The larger family can be counted by dynamic programming over a tree decomposition, with a fixed number of states per bag vertex.
- A one-sided Monte Carlo answer is acceptable: a NO answer may be wrong with small probability, and a YES answer is always right.
- The connectivity condition is global, such as "connected" or "one cycle". Problems where the number of components must be counted exactly, such as cycle packing, do not fit (see Pitfalls).

## The template

**Definitions.** Let $U$ be the universe, for example $V(G)$. Let $\mathcal R \subseteq 2^U$ be the *relaxed* solutions, and $\mathcal S \subseteq \mathcal R$ the solutions, which are the sets $X \in \mathcal R$ with $G[X]$ connected. Fix a vertex $v_1$ that every solution contains, for example a terminal. A *consistent cut* of $X$ is a pair $(X_L, X_R)$ with $X_L \cup X_R = X$, $X_L \cap X_R = \emptyset$, $v_1 \in X_L$, and no edge of $G$ between $X_L$ and $X_R$. Let $\mathcal C$ be the set of pairs $(X, (X_L, X_R))$ with $X \in \mathcal R$ and $(X_L, X_R)$ a consistent cut of $X$.

**Lemma 1 (Lemma 3.3).** A set $X$ with $v_1 \in X$ has exactly $2^{\mathrm{cc}(G[X]) - 1}$ consistent cuts, where $\mathrm{cc}$ is the number of components. So $|\mathcal C| \equiv |\mathcal S| \pmod 2$.

*Proof.* No component of $G[X]$ can be split, because it would have an edge between the two sides. So each component lies on one side. The component of $v_1$ is on the left, and each of the other $\mathrm{cc} - 1$ components has two choices. The count is odd exactly when $\mathrm{cc} = 1$. $\square$

**Lemma 2 (isolation, Mulmuley, Vazirani and Vazirani).** Let $\mathcal F$ be a nonempty family of subsets of $U$, and let each $u \in U$ get a weight $w(u)$ chosen uniformly and independently from $\{1, \ldots, N\}$. Then the probability that exactly one set in $\mathcal F$ has the least weight is at least $1 - |U| / N$.

The method has two holes. WEIGHTS chooses $w$ with $N = 2|U|$. COUNT$(w, W)$ returns, modulo 2, the number of pairs in $\mathcal C$ whose set $X$ has weight $W$. It is a dynamic program over the tree decomposition.

```pseudo id=main
CUT-AND-COUNT(G, T, k)
L1  w ← WEIGHTS(U), each value uniform in {1, ..., 2|U|}
L2  for W ← 0 to 2|U|² do
L3      if COUNT(w, W) = 1 then return YES
L4  return NO
```

**Correctness.** If there is no solution, every pair in $\mathcal C$ has a disconnected $X$, so by Lemma 1 every count is even and the answer is NO. If there is a solution, Lemma 2 with $\mathcal F = \mathcal S$ says that with probability at least $1/2$ the least weight $W^\ast$ of a solution is reached by one solution only. Then $|\mathcal C_{W^\ast}| \equiv |\mathcal S_{W^\ast}| = 1 \pmod 2$, and L3 returns YES. Repeating the algorithm $r$ times lowers the error to $2^{-r}$.

**The count for Steiner tree.** The node version asks for $X$ with $|X| = k$, $T \subseteq X$ and $G[X]$ connected. In the dynamic program, each vertex of a bag has one of three states: $0$ (not in $X$), $1_L$ (in $X_L$) or $1_R$ (in $X_R$). When an edge is introduced, its two ends may not have the states $1_L$ and $1_R$. A terminal may not have state $0$, and $v_1$ must have state $1_L$. A table entry is indexed by the states of the bag, the size of $X$ so far and its weight so far. So there are $3^{t+1}$ state vectors, and with fast join operations the time is $3^t n^{O(1)}$.

```pseudo id=dp
COUNT-STATE(bag state f, edge uv introduced)
L1  if f(u) ∈ {1_L, 1_R} and f(v) ∈ {1_L, 1_R} and f(u) ≠ f(v) then return 0
L2  return the count for f
```

## Classic examples

**A grid.** A scratch script took the $3 \times 3$ grid with vertices $(i, j)$, terminals $(0, 0)$, $(0, 2)$, $(2, 1)$, and $v_1 = (0, 0)$. It counted the pairs in $\mathcal C$ by brute force and, separately, by a frontier dynamic program in row-major order with states $0$, $1_L$, $1_R$ on the last 3 cells. Both gave the same counts.

| $k$ | connected sets $X$ | pairs in $\mathcal C$ | parity |
|---|---|---|---|
| 4 | 0 | 22 | even |
| 5 | 1 | 41 | odd |
| 6 | 7 | 35 | odd |
| 7 | 13 | 17 | odd |

Lemma 1 held for every candidate set. At most 21 of the $3^3 = 27$ frontier states occurred. For $k = 6$ and $k = 7$ the number of solutions is odd, so the plain parity is already correct, but that is luck. With the weights $w(0,0) = 5$, $w(0,1) = 3$, $w(0,2) = 9$, $w(1,0) = 4$, $w(1,1) = 16$, $w(1,2) = 15$, $w(2,0) = 16$, $w(2,1) = 13$, $w(2,2) = 7$, the only odd count for $k = 5$ is at weight 46, the weight of the unique solution $\{(0,0), (0,1), (0,2), (1,1), (2,1)\}$. For $k = 7$ the odd counts are at weights 56, 66, 69, 77 and 78. The least solution weight 56 has one solution; weight 69 has three. In 1000 random weight functions with values in $\{1, \ldots, 18\}$ (seed 1), the algorithm answered YES for $k = 7$ every time.

**Results of the paper.** Given a tree decomposition of width $t$, the method gives Monte Carlo algorithms with these running times, each times $n^{O(1)}$:

| time | problems |
|---|---|
| $3^t$ | Steiner tree, feedback vertex set, connected vertex cover |
| $4^t$ | connected dominating set, connected feedback vertex set, connected odd cycle transversal, Hamiltonian cycle and path, longest path and cycle, minimum cycle cover, exact $k$-leaf spanning tree, maximum full degree spanning tree, graph metric TSP |
| $6^t$ | the directed versions of these problems |

Before, the known algorithms for these problems had running time $t^{O(t)} n^{O(1)}$.

**Parameterized by the solution size.** With a tree decomposition from the solution structure, the method gives feedback vertex set in $3^k n^{O(1)}$, connected vertex cover in $2^k n^{O(1)}$ and connected feedback vertex set in $3^k n^{O(1)}$, all randomized. See [parameterized feedback vertex set](/parameterized-feedback-vertex-set/).

## Variations

- **Edge versions.** For Hamiltonian cycle the candidates are edge sets where every vertex has degree 2, and the cut is a coloring of the vertices that each chosen edge respects. The states record degrees as well as sides, and the bound is $4^t$.
- **Deterministic algorithms.** The rank-based approach of Bodlaender, Cygan, Kratsch and Nederlof keeps only a small representative set of partial solutions, chosen by Gaussian elimination over GF(2). It gives deterministic single exponential algorithms for many of the same problems.
## Pitfalls

- **Cancellation without weights.** On the 4-cycle with vertices $a, b, c, d$, terminals $\{a, c\}$ and $k = 3$, the solutions $\{a, b, c\}$ and $\{a, c, d\}$ each have one consistent cut, so the total is 2, which is even. A scratch script tried all $8^4 = 4096$ weight functions with values in $\{1, \ldots, 8\}$; 3584 of them, or $0.875$, gave an odd count at some weight. Lemma 2 promises at least $1 - 4/8 = 0.5$.
- **The fixed vertex.** If $v_1$ were not forced to the left side, every set would have an even number of cuts, and every count would be even. For $k = 2$ in the 4-cycle, the set $\{a, c\}$ is disconnected and has 2 consistent cuts, which cancel as they should.
- **Not every connectivity problem.** For cycle packing and maximum cycle cover the paper shows that no $2^{o(p \log p)} n^{O(1)}$ algorithm exists for path decompositions of width $p$ unless the exponential time hypothesis fails. The number of cycles there must be counted exactly, and parity does not do that.
- **Tight bases.** Under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) the paper shows that Steiner tree has no $(3 - \varepsilon)^p n^{O(1)}$ algorithm with a path decomposition of width $p$. Matching lower bounds hold for the other $3^t$ problems, so the bases are optimal.
- **Space and size of the numbers.** Weights up to $2|U|$ make the weight index range up to $2|U|^2$. This is only a polynomial factor.

## Exercises

1. Prove Lemma 2 for a family $\mathcal F$: for each $u$, bound the probability that $u$ is in some least set and not in another least set.
2. Write the introduce, forget and join rules of the dynamic program for the node Steiner tree, with states $0$, $1_L$, $1_R$, size and weight.
3. Explain why the join of two tables costs $3^t$ per pair of size and weight indices if the states are combined pointwise.
4. Adapt the method to connected vertex cover: what is $\mathcal R$, and which vertex should be $v_1$ if no vertex is known to be in every solution?
5. For the 4-cycle example, list a weight function for which both solutions have the same weight, and check that no weight has an odd count.

## References
