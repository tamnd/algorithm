---
tag: K1XTPB
kind: technique
slug: randomized-contractions
name: Randomized contractions
aliases:
- randomized contraction algorithm
area: complexity/parameterized-complexity
level: research
summary: "An FPT method for cut problems with cut size k: recurse on a small separation, or, in a highly connected graph, use splitter sets to find and contract edges that the solution does not cut."
prereqs: [fixed-parameter-tractable, color-coding, important-separators]
see_also: [important-separators, color-coding, karger-min-cut, parameterized-multiway-cut, parameterized-multicut, unique-games-conjecture, multiway-cut-problem, min-cut-problem]
sources:
  - paper: doi:10.1137/15M1032077
    title: "Rajesh Chitnis, Marek Cygan, MohammadTaghi Hajiaghayi, Marcin Pilipczuk and Michal Pilipczuk, Designing FPT algorithms for cut problems using randomized contractions, SIAM Journal on Computing 45(4), 1171-1229 (2016)"
    locator: Section 1 (Lemma 1.1, Theorems 1.2 to 1.5 and the discussion of related work) and Section 2 (good separations, Lemma 2.2, recursive understanding, high connectivity phase, Lemmas 2.3 and 2.4); conference version FOCS 2012
  - paper: doi:10.1109/FOCS.2011.53
    title: Ken-ichi Kawarabayashi and Mikkel Thorup, The minimum k-way cut of bounded size is fixed-parameter tractable, FOCS 2011, 160-169
    locator: the recursive scheme on separations of small order that randomized contractions makes faster
  - paper: doi:10.1137/140988553
    title: "Marek Cygan, Daniel Lokshtanov, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Minimum bisection is fixed-parameter tractable, SIAM Journal on Computing 48(2), 417-450 (2019)"
    locator: the decomposition into highly connected parts that replaces the recursion
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 5, Randomized methods in parameterized algorithms (color coding and its derandomization); Chapter 8, Finding cuts and separators (important separators, for comparison)
---

Randomized contractions is a method for [fixed-parameter tractable](/fixed-parameter-tractable/) algorithms for cut problems in undirected graphs, with the size $k$ of the cut as the parameter. Chitnis, Cygan, Hajiaghayi, Pilipczuk and Pilipczuk introduced it in 2012. It is a win/win scheme. Either the graph has a *good separation*, a cut of at most $k$ edges with many vertices on both sides, and then one side is solved recursively and shrunk. Or no such cut exists, and then the graph is so well connected that the solution can be found by a guess from a family of sets of size $2^{O(\min(a, b) \log(a + b))} \log n$, where $a$ and $b$ depend on $k$ only. The name comes from [Karger's algorithm](/karger-min-cut/), which contracts random edges; the published algorithms are deterministic.

## In plain words

You must cut a few edges of a network, at most $k$, so that some condition holds. Two cases can happen.

In the first case a few edges split the network into two large connected parts. Then you solve one part for every way in which the rest can touch it. Only a few of its edges are ever useful, and you merge the others. The part gets smaller, and you start again.

In the second case the network has no weak point. Then the solution cuts off only small pieces, plus one huge piece. You guess a set of edges that contains all edges inside the small pieces and around the cut, and no edge of the cut itself. A random guess works with a chance that depends only on $k$. If you merge the ends of each guessed edge, the solution becomes easy to read off.

## When it applies

- The solution is a set $X$ of at most $k$ edges of an undirected graph. The method also works for vertex deletion, with more care, and with positive real weights on the edges.
- The problem has a *border* version with a set $T_b$ of $O(k)$ border terminals and a *behaviour* on them, for example which border terminals stay connected. The number of behaviours depends on $k$ only. For each behaviour, a minimum solution can be described.
- Edges that no minimum solution needs can be made undeletable, and an undeletable edge can be contracted or replaced by an equivalent structure.
- In a highly connected graph, the parts of the graph that the solution leaves together can be identified once a set $S$ that contains the edges around the solution is known. This step is specific to each problem.

The method does not work for directed graphs, and it does not handle multicut with an unbounded number of pairs. The authors note that [important separators](/important-separators/) with shadow removal handle those cases.

## The template

**Definitions.** For disjoint vertex sets $V_1, V_2$ with $V_1 \cup V_2 = V(G)$, a $(q, k)$-*good edge separation* is a pair with $|V_1| > q$, $|V_2| > q$, at most $k$ edges between $V_1$ and $V_2$, and both $G[V_1]$ and $G[V_2]$ connected. A graph with no $(q, k)$-good edge separation is $(q, k)$-*unbreakable*.

**Lemma 1 (splitters, Lemma 1.1 of the paper).** For a set $U$ of size $n$ and integers $a, b$, a family $\mathcal F$ of at most $2^{O(\min(a, b) \log(a + b))} \log n$ subsets of $U$ can be built in time $2^{O(\min(a, b) \log(a + b))} n \log n$. For any disjoint $A, B \subseteq U$ with $|A| \le a$ and $|B| \le b$, some $S \in \mathcal F$ has $A \subseteq S$ and $B \cap S = \emptyset$. It follows from the splitters of Naor, Schulman and Srinivasan, as in the derandomization of [color coding](/color-coding/).

**Lemma 2 (Lemma 2.2).** A $(q, k)$-good edge separation can be found, or shown not to exist, in $O(2^{O(\min(q, k) \log(q + k))} n^3 \log n)$ time. The proof uses Lemma 1 with $a = 2q$ and $b = k$ on the edge set, contracts the edges of the set $S$, and runs minimum cut computations between large contracted vertices.

**Lemma 3 (Lemma 2.3).** Let $G$ be connected with no $(q, 2k)$-good edge separation, and let $F$ be a set of at most $k$ edges. Then $G - F$ has components $C_0, C_1, \ldots, C_\ell$ with $\ell \le k$, and all of them except at most one have at most $q$ vertices. Also, any two vertex-disjoint connected subgraphs with more than $q$ vertices each are joined by at least $2k + 1$ edge-disjoint paths.

The template has three holes. BRUTE$(G, T)$ solves a small instance by trying all edge sets of size at most $k$. REDUCE$(G, D)$ makes the edges of $D$ undeletable, for example by contracting them. DECIDE$(G, T, S, \psi)$ is the problem-specific step that finds a minimum solution with behaviour $\psi$ that is disjoint from $S$, under the assumption that $S$ interrogates it (defined below). The number $q$ is chosen so that the total size of all the solutions returned for all behaviours is at most $q - 1$.

```pseudo id=main
SOLVE(G, T, k)
L1  if |V(G)| ≤ q(k + 1) then return BRUTE(G, T)
L2  (V1, V2) ← a (q, 2k)-good edge separation of G, or none
L3  if (V1, V2) ≠ none then
L4      if |V1 ∩ T| > 2k then swap V1 and V2
L5      T1 ← (V1 ∩ T) ∪ (vertices of V1 with a neighbor in V2)
L6      Z ← union of the edges of all solutions in SOLVE(G[V1], T1, k)
L7      G ← REDUCE(G, E(G[V1]) \ Z)
L8      return SOLVE(G, T, k)
L9  for each S in the family of Lemma 1 on E(G), with a = (3q - 1)k and b = k do
L10     for each behaviour ψ on T do
L11         keep the best of DECIDE(G, T, S, ψ) for ψ
L12 return the best solution kept for each behaviour ψ
```

**The recursive step (L2 to L8).** Since $|T| \le 4k$, one side holds at most $2k$ border terminals, and the cut adds at most $2k$ more, so $|T_1| \le 4k$ and the recursive call is a valid border instance. For every solution of the whole instance and every behaviour, the part inside $G[V_1]$ can be replaced by a solution of $G[V_1]$ with the same behaviour on $T_1$. So some minimum solution uses only edges of $Z$ inside $G[V_1]$, and the other edges of $G[V_1]$ can be made undeletable. Since $|V_1| > q$ and $|Z| \le q - 1$, at least one edge is contracted, so the graph shrinks; afterwards at most $q$ vertices of $V_1$ remain.

**The high connectivity step (L9 to L11).** Assume $X$ is a minimum solution and $G - X$ has components $C_0, \ldots, C_\ell$ as in Lemma 3. Since $|V(G)| > q(k + 1)$, the component $C_0$ is the big one. Take a spanning tree of each small component; together they have at most $(q - 1)k$ edges. For each endpoint $u$ of an edge of $X$ in $C_0$, take a subtree of $C_0$ with $q + 1$ vertices that contains $u$; there are at most $2k$ such endpoints, so these trees have at most $2qk$ edges. A set $S$ of edges *interrogates* $X$ if $S$ contains all these tree edges and no edge of $X$. Lemma 1 with $a = (3q - 1)k$ and $b = k$ gives a family that contains such an $S$.

The components of the graph $(V(G), S)$ are called *stains*, and a stain is *big* if it has more than $q$ vertices. Let $S^{\mathrm{big}}$ be the union of the big stains.

**Lemma 4 (Lemma 2.4).** If $S$ interrogates $X$, then for each component $D$ of $G - S^{\mathrm{big}}$ exactly one of the following holds: no edge of $X$ touches $D$ and $D \subseteq C_0$; or $D$ contains no vertex of $C_0$, and the small stains in $D$ are exactly the components $C_i$ with $i \ge 1$ that lie in $D$.

So DECIDE only has to choose, for each component $D$, one of two options. In the first, nothing in $D$ is cut. In the second, $D$ is cut exactly along its small stains. How to choose depends on the problem.

**Running time.** The recursion runs at most $n$ times, and each round costs the time of Lemma 2 with $2k$ in place of $k$. The high connectivity step tries $2^{O(k \log q)} \log n$ sets $S$ when $k \le q$. For unique label cover over an alphabet of size $s$, the paper takes $q = k s^{4k} + 1$, so $\log q = O(k \log s)$, and the total time is $O(2^{O(k^2 \log s)} n^4 \log n)$.

**The randomized view.** Put each edge into $S$ independently with probability $p = a / (a + b)$. For fixed sets $A$ and $B$ with $|A| = a$ and $|B| = b$, the chance that $A \subseteq S$ and $B \cap S = \emptyset$ is $p^a (1 - p)^b$, which is $2^{-O(\min(a, b) \log(a + b))}$. Lemma 1 replaces this random choice by a deterministic family.

## Classic examples

**A small run.** A scratch script built the graph with vertices $0, \ldots, 7$: a $K_5$ on $0, \ldots, 4$, a triangle on $5, 6, 7$, and the two edges $45$ and $36$, so $n = 8$ and $m = 15$. Take $q = 3$ and $k = 2$.

- By brute force over all bipartitions, the graph has no $(3, 4)$-good edge separation. Lemma 3 holds: for every set $F$ of at most 2 edges, $G - F$ has at most 2 components, and at most one has more than 3 vertices.
- The least edge cut between $0$ and $7$ has 2 edges, with two solutions, $\{67, 57\}$ and $X = \{45, 36\}$. Take $X$. The small component is the triangle. The set $A$ has 8 edges: the spanning tree $56$, $67$ of the triangle and the stars $30, 31, 32$ and $40, 41, 42$ around the endpoints 3 and 4. The set $B$ is $X$.
- With $p = 8/10$, the chance that a random $S$ interrogates $X$ is $0.8^8 \cdot 0.2^2 \approx 0.00671$. In 200000 trials with seed 5, the observed rate was $0.006775$.
- The first interrogating sample had 11 edges. Its stains are $\{0, 1, 2, 3, 4\}$, which is big, and $\{5, 6, 7\}$. The only component of $G - S^{\mathrm{big}}$ is $\{5, 6, 7\}$, and it is cut along its stain, as Lemma 4 says.

**Unique label cover.** Each edge $uv$ carries a permutation of an alphabet $\Sigma$ of size $s$, and at most $k$ edges (or vertices) may violate their constraint. The method gives the first FPT algorithm, in $O(2^{O(k^2 \log s)} n^4 \log n)$ time. In the high connectivity step, a label on one vertex of a big stain fixes the labels of the whole stain, and of all big stains through the $2k + 1$ edge-disjoint paths of Lemma 3. So DECIDE tries only $s$ labelings. With $k$ alone as the parameter, the problem is W[1]-hard. See the [unique games conjecture](/unique-games-conjecture/) for why this problem matters.

**Steiner cut.** Given terminals $T$ and integers $s$ and $k$, delete at most $k$ edges so that at least $s$ components contain a terminal. This contains $k$-way cut and [multiway cut](/parameterized-multiway-cut/). The method gives $O(2^{O(k^2 \log k)} n^4 \log n)$ time, which improves the double exponential bound of Kawarabayashi and Thorup.

**Node multiway cut-uncut.** Given terminals $T$ with an equivalence relation on them, delete at most $k$ non-terminals so that two terminals are connected exactly when they are equivalent. The method gives $O(2^{O(k^2 \log k)} n^4 \log n)$ time.

## Variations

- **Weights.** The algorithms extend to positive real edge weights, with $k$ the number of deleted edges. Important separators need unit or small integer weights, because their counting argument uses the cost of the cut.
- **Node deletion.** Two kinds of separations are needed, and Lemma 4 has a weaker form, but the scheme is the same.
- **A static decomposition.** Cygan, Lokshtanov, Pilipczuk, Pilipczuk and Saurabh replaced the recursion by a tree decomposition whose adhesions have bounded size and whose bags are highly connected in the same sense. This gave the first FPT algorithm for minimum bisection.
- **The randomized form.** Contract random edges directly instead of using the family of Lemma 1. This is simpler, and it gives a Monte Carlo algorithm.

## Pitfalls

- The method is not Karger's contraction algorithm. Karger contracts random edges to find a global minimum cut. Here the contracted set $S$ must contain specific edges and avoid the at most $k$ solution edges, and the chance of this depends on $k$ and $q$, not on $n$.
- The border version matters. A recursive call on $G[V_1]$ must return a solution for every behaviour on the border terminals, not one solution. Otherwise the edges that are made undeletable could be needed.
- Separations of order $2k$, not $k$, are used. With order $k$, Lemma 3 would not give $2k + 1$ edge-disjoint paths between big parts, and the majority argument for unique label cover would fail.
- The dependence on $k$ is $2^{O(k^2 \log k)}$, so the method usually gives a first FPT result or a single exponential bound, not the fastest algorithm.

## Exercises

1. Show that $p^a (1 - p)^b$ is largest at $p = a / (a + b)$, and that for $a \le b$ its value is at least $(a + b)^{-a} e^{-a}$. Conclude that $2^{O(a \log(a + b))}$ random sets suffice for constant success probability.
2. Prove the first part of Lemma 3: if $G - F$ had two components with more than $q$ vertices each, find a $(q, 2k)$-good edge separation.
3. In the example above, list all sets of 2 edges $F$ for which $G - F$ is disconnected, and check that each one cuts off a single vertex or the triangle.
4. Explain why the recursive step needs $|T| \le 4k$ and how the choice of the side with at most $2k$ border terminals keeps this bound.
5. For edge multiway cut, describe DECIDE: which components $D$ of $G - S^{\mathrm{big}}$ must be cut along their stains, and which can be left whole?

## References
