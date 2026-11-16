---
tag: 369D3Z
kind: technique
slug: iterative-compression
name: Iterative compression
area: complexity/parameterized-complexity
level: advanced
summary: "Add the vertices one at a time and keep a solution of size k. Each new vertex gives a solution of size k+1, and a compression step either shrinks it to size k or proves that none exists."
prereqs: [fixed-parameter-tractable, bounded-search-tree]
see_also: [odd-cycle-transversal, parameterized-feedback-vertex-set, directed-feedback-vertex-set, parameterized-vertex-cover, max-flow-min-cut-theorem, bounded-search-tree, kernelization, measure-and-conquer]
sources:
  - paper: doi:10.1016/j.orl.2003.10.009
    title: "Bruce Reed, Kaleigh Smith and Adrian Vetta, Finding odd cycle transversals, Operations Research Letters 32(4), 299-301 (2004)"
    locator: the first use of iterative compression, for odd cycle transversal
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 4, Iterative compression, pp. 77-98 (feedback vertex set, and Section 4.4 on odd cycle transversal)
  - paper: doi:10.1016/j.ipl.2014.05.001
    title: "Tomasz Kociumaka and Marcin Pilipczuk, Faster deterministic feedback vertex set, Information Processing Letters 114(10), 556-560 (2014)"
    locator: a finer analysis of the disjoint step for feedback vertex set, with time 3.619^k n^O(1)
---

Iterative compression is a technique for *vertex deletion* problems: delete at most $k$ vertices of a graph so that the rest has some property, such as no odd cycle or no cycle at all. The parameter is $k$. The idea is to solve an easier problem many times. Suppose you already have a solution $S$ with $k + 1$ vertices. The *compression* step must find a solution with at most $k$ vertices, or prove that none exists, and it can use $S$ as a guide: it guesses which vertices of $S$ stay in the new solution, and then looks for the rest outside $S$. To get the first $S$, the method adds the vertices of the graph one at a time and keeps a solution for the part seen so far. Reed, Smith and Vetta (2004) introduced the technique to show that [odd cycle transversal](/odd-cycle-transversal/) is [fixed-parameter tractable](/fixed-parameter-tractable/), and it later gave the first FPT algorithms for [directed feedback vertex set](/directed-feedback-vertex-set/) and other cut problems.

## In plain words

Suppose you must remove at most $k$ bad items from a pile, and you already know a way to do it with one item too many. That extra knowledge helps a lot. You guess which items of your known answer to keep in the new answer. The other items of the known answer must stay in the pile, and that fixes much of the structure.

To get a known answer at all, you build the pile one item at a time. When you add an item, you put it into the answer too, so the answer grows by one. Then you shrink it again by the step above.

If the shrink step ever fails, the part of the pile you have is already too hard, and so is the full pile.

## When it applies

- The problem asks for a set $X$ of at most $k$ vertices whose deletion leaves a graph in a class $\Pi$.
- The class $\Pi$ is *hereditary*: if $G$ is in $\Pi$, so is every induced subgraph. Then a solution for $G$ restricts to a solution for every induced subgraph, and a solution for $G - v$ plus the vertex $v$ is a solution for $G$.
- The *disjoint* version is easy: given $G$ and a solution $W$, find a solution of size at most $k'$ that is *disjoint* from $W$. Often the vertices of $W$, which may not be deleted, force so much that a cut, a matching or a small branching solves it.
- The parameter is $k$. The method gives time $f(k) \cdot n^{O(1)}$ if the disjoint version takes $g(k) \cdot n^{O(1)}$.

## The template

The template has one hole. DISJOINT$(H, W, k')$ returns a solution of $H$ with at most $k'$ vertices that is disjoint from $W$, or NONE. Here $W$ is itself a solution of $H$.

```pseudo id=main
ITERATIVE-COMPRESSION(G, k)           ▷ a solution with at most k vertices, or NONE
L1  let v_1, …, v_n be the vertices of G; S ← ∅
L2  for i ← 1 to n do
L3      G_i ← G[{v_1, …, v_i}]; S ← S ∪ {v_i}
L4      if |S| ≤ k then continue
L5      S ← COMPRESS(G_i, S, k)
L6      if S = NONE then return NONE
L7  return S

COMPRESS(H, S, k)                     ▷ |S| = k + 1, and S is a solution of H
L8  for each Z ⊆ S with |Z| ≤ k do
L9      X ← DISJOINT(H - Z, S \ Z, k - |Z|)
L10     if X ≠ NONE then return Z ∪ X
L11 return NONE
```

**Lemma (compression).** If $S$ is a solution of $H$ with $|S| = k + 1$, then COMPRESS returns a solution with at most $k$ vertices if one exists, and NONE otherwise.

*Proof.* A returned set $Z \cup X$ has at most $k$ vertices. It is a solution: $X$ is a solution of $H - Z$, so deleting $Z \cup X$ from $H$ leaves a graph in $\Pi$. Conversely, let $S'$ be a solution of $H$ with $|S'| \le k$. Then $Z = S' \cap S$ is one of the sets in L8, and $S' \setminus Z$ is a solution of $H - Z$ that is disjoint from $S \setminus Z$ and has at most $k - |Z|$ vertices. So DISJOINT does not return NONE for this $Z$. $\square$

**Theorem.** ITERATIVE-COMPRESSION is correct.

*Proof.* Invariant: after round $i$, $S$ is a solution of $G_i$ with $|S| \le k$. Round 1 makes it true. In round $i$, $S \cup \{v_i\}$ is a solution of $G_i$ because $\Pi$ is hereditary, and COMPRESS keeps the invariant by the lemma. If COMPRESS returns NONE, $G_i$ has no solution with $k$ vertices. Since $G_i$ is an induced subgraph of $G$ and $\Pi$ is hereditary, a solution of $G$ would restrict to one of $G_i$, so $G$ has none either. At the end $G_n = G$. $\square$

**Time.** There are $n$ rounds, and each calls DISJOINT at most $2^{k+1}$ times. If DISJOINT with budget $k'$ costs $g(k') \cdot n^{O(1)}$, the total is $\sum_{j} \binom{k+1}{j} g(k - j) \cdot n^{O(1)}$. For $g(k') = c^{k'}$ this is $(1 + c)^{k+1} n^{O(1)}$.

## Classic examples

### Vertex cover

This is a toy case, since [vertex cover](/parameterized-vertex-cover/) has simpler algorithms, but it shows the mechanics. In DISJOINT$(H, W, k')$, the vertices of $W$ may not be deleted. So $W$ must be an independent set in $H$, and every neighbor of $W$ must be deleted. Since $W$ is a vertex cover of $H$, every edge has an end in $W$, so the forced set $N(W)$ is already a cover. DISJOINT returns $N(W)$ if $W$ is independent and $|N(W)| \le k'$, and NONE otherwise, in polynomial time. Each guess costs $O(n + m)$, so the total time is $O(2^k \cdot n \cdot (n + m))$.

Take the cycle $1, 2, 3, 4, 5$ with $k = 2$ and the vertices in this order. In round 3, $S = \{1, 2, 3\}$ on the path $1, 2, 3$, and the guess $Z = \{2\}$ works: $W = \{1, 3\}$ is independent with no neighbor outside $Z$, so $S$ becomes $\{2\}$. Round 4 gives $S = \{2, 4\}$. In round 5, $S = \{2, 4, 5\}$ on the full cycle, and all 8 guesses fail:

| $Z$ | $W = S \setminus Z$ | why it fails |
|---|---|---|
| $\emptyset$, $\{2\}$ | $\{2, 4, 5\}$, $\{4, 5\}$ | $W$ has the edge $45$ |
| $\{4\}$, $\{5\}$ | $\{2, 5\}$, $\{2, 4\}$ | $N(W) \setminus Z = \{1, 3\}$, total 3 |
| $\{2, 4\}$, $\{2, 5\}$ | $\{5\}$, $\{4\}$ | $N(W) \setminus Z$ has 1 vertex, total 3 |
| $\{4, 5\}$ | $\{2\}$ | $N(W) \setminus Z = \{1, 3\}$, total 4 |
| $\{2, 4, 5\}$ | $\emptyset$ | $\lvert Z \rvert = 3 > k$ |

So the answer is NONE, which is right: a 5-cycle needs 3 vertices to cover its edges.

### Odd cycle transversal

For [odd cycle transversal](/odd-cycle-transversal/), $H - S$ is bipartite. The compression guesses, for each vertex of $S$, whether it is deleted, on the left side, or on the right side, so $3^{k+1}$ guesses. For a fixed guess, the problem is to delete at most $k - |Z|$ vertices outside $S$ so that the 2-coloring of $H - S$ agrees with the guessed sides. This is a minimum vertex cut between two sets in an auxiliary graph, solved by [max flow](/max-flow-min-cut-theorem/). The total time is $3^k \cdot n^{O(1)}$ (Reed, Smith and Vetta, 2004).

### Feedback vertex set

For [feedback vertex set](/parameterized-feedback-vertex-set/), $W$ is a forest that must stay. DISJOINT uses reduction rules (delete vertices of degree at most 1, bypass vertices of degree 2) and branches on a vertex outside $W$ with two neighbors in $W$: either delete it, or add it to $W$, which merges two trees of $W$. A simple measure gives $4^{k'}$ for the disjoint step and $5^k n^{O(1)}$ in total. Kociumaka and Pilipczuk (2014) refined the measure and got $3.619^k n^{O(1)}$.

## Variations

- *Edge deletion.* The same scheme works when the solution is a set of edges, for example edge bipartization, if the class is closed under edge deletion.
- *Directed graphs.* For directed feedback vertex set, the disjoint step is much harder and uses separators in directed graphs. This gave the first FPT algorithm for that problem (Chen, Liu, Lu, O'Sullivan and Razgon, 2008).
- *Compression without iteration.* If a solution with $f(k)$ vertices can be found in polynomial time, for example by an approximation algorithm, compression can start from it directly, at the price of more guesses.
- *Kernels.* Kratsch and Wahlström used a compression of an odd cycle transversal of size $k + 1$ into matroid data to get a randomized polynomial kernel. See [kernelization](/kernelization/).

## Pitfalls

- A class that is not hereditary. Then $S \cup \{v_i\}$ need not be a solution of $G_i$, and a NONE for $G_i$ does not imply NONE for $G$.
- Forgetting that $S \setminus Z$ must stay. DISJOINT must not delete any vertex of $W$; this is the constraint that makes it easy.
- Skipping some guesses. Every subset $Z$ of $S$ with at most $k$ vertices can be the right one, and $Z = \emptyset$ is a real case.
- Counting the time as $2^k \cdot g(k)$. The budget of DISJOINT is $k - |Z|$, so the sum over $Z$ gives $(1 + c)^{k+1}$, not $2^{k+1} c^k$.
- Restarting from scratch in each round. Only one new vertex enters, so the old solution plus that vertex is the right input for the next compression.

## Exercises

1. Run ITERATIVE-COMPRESSION for vertex cover on the cycle $1, 2, 3, 4, 5$ with $k = 3$, and give the final solution.
2. Show that if $\Pi$ is not hereditary, the theorem can fail. Give a class and a graph where it fails.
3. Prove that $\sum_{j=0}^{k+1} \binom{k+1}{j} c^{k+1-j} = (1 + c)^{k+1}$, and use it to bound the time of the odd cycle transversal algorithm when the disjoint step costs $2^{k'}$ per guess of sides.
4. Design DISJOINT for cluster vertex deletion: delete at most $k'$ vertices outside $W$ so that the rest is a disjoint union of cliques.
5. In the disjoint step for feedback vertex set, show that a vertex with two neighbors in the same tree of $W$ must be deleted, and that adding a vertex with at most one neighbor in each tree of $W$ keeps $W$ a forest.

## References
