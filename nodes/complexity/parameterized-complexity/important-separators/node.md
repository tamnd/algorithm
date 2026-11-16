---
tag: 5RQ4TK
kind: technique
slug: important-separators
name: Important separators
aliases:
- important separator technique
area: complexity/parameterized-complexity
level: research
summary: "A cut of size at most k is important if no cut of at most the same size lies farther from X. There are at most 4^k of them, so FPT cut algorithms can branch over all of them."
prereqs: [max-flow-min-cut-theorem, fixed-parameter-tractable, bounded-search-tree]
see_also: [parameterized-multiway-cut, parameterized-multicut, directed-feedback-vertex-set, randomized-contractions, menger-theorem, submodular-function, iterative-compression, min-cut-problem]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 8, Finding cuts and separators (important cuts, the 4^k bound, edge multiway cut, directed graphs and directed feedback vertex set)
  - paper: doi:10.1016/j.tcs.2005.10.007
    title: "Daniel Marx, Parameterized graph separation problems, Theoretical Computer Science 351(3), 394-406 (2006)"
    locator: the introduction of important separators and the FPT algorithm for multiway cut parameterized by the cut size
  - url: https://fptschool.mimuw.edu.pl/slides/lec7.pdf
    title: Daniel Marx, Important separators and parameterized algorithms, lecture slides, School on Parameterized Algorithms and Complexity, Bedlewo, 2014
    locator: slides 8 to 26 (R_max, the 4^k bound and its proof, the tight example, the pushing lemma, the bound on the sum of 4^(-|S|), anti-isolation)
  - paper: doi:10.1007/s00453-007-9130-6
    title: "Jianer Chen, Yang Liu and Songjian Lu, An improved parameterized algorithm for the minimum node multiway cut problem, Algorithmica 55(1), 1-13 (2009)"
    locator: the 4^k bound on important separators and the O*(4^k) algorithm for node multiway cut
  - paper: doi:10.1137/110855247
    title: "Daniel Marx and Igor Razgon, Fixed-parameter tractability of multicut parameterized by the size of the cutset, SIAM Journal on Computing 43(2), 355-388 (2014)"
    locator: random sampling of important separators and shadow removal
---

Important separators are a tool for [fixed-parameter tractable](/fixed-parameter-tractable/) algorithms on cut problems, where the parameter $k$ is the size of the cut. In a graph $G$ with vertex sets $X$ and $Y$, an $(X, Y)$-cut is *important* if no other cut of at most the same size lies farther from $X$. Marx introduced them in 2006, and Chen, Liu and Lu proved that there are at most $4^k$ important cuts of size at most $k$. The technique has two steps: a *pushing lemma* shows that some solution contains an important cut, and the algorithm then branches over all important cuts, which gives a search tree with at most $4^k$ leaves.

## In plain words

You want to cut a few edges so that one part of a network cannot reach another part. There are often very many small cuts, too many to try each one. But many of them are worse than others. If two cuts have the same size, and one cut leaves more of the network on your side, that cut is never a worse choice for many problems: everything the near cut separates, the far cut separates too, and it also keeps more vertices together with your side.

So you only keep the cuts that cannot be pushed farther away without becoming larger. These are the important cuts. Their number depends only on the size of the cut, not on the size of the network: for cuts of at most $k$ edges there are at most $4^k$. A search can try all of them in turn.

## When it applies

- The solution is a set of at most $k$ edges or vertices, and its job is to destroy paths between given vertex sets.
- Some part of a solution is an $(X, Y)$-cut for sets $X$ and $Y$ that the algorithm can find.
- A *pushing lemma* holds: that part can be replaced by a cut of at most the same size that lies farther from $X$, and the result is still a solution. Then some solution contains an important cut.
- The graph can be undirected or directed, and the cut can consist of edges or of vertices. The $4^k$ bound holds in all four cases. For vertex cuts, the vertices of $X$ and $Y$ cannot be deleted.

The technique does not apply directly when the edges have arbitrary weights, because the bound counts edges. For those problems, see [randomized contractions](/randomized-contractions/).

## The template

**Definitions.** Let $G$ be an undirected graph and let $X, Y \subseteq V(G)$ be disjoint. For a set $R$ of vertices, $\delta(R)$ is the set of edges with exactly one endpoint in $R$. A set $S$ of edges is an *$(X, Y)$-cut* if $G - S$ has no path from $X$ to $Y$. It is a *minimal* cut if no proper subset of $S$ is a cut. Every minimal cut has the form $S = \delta(R)$, where $R$ is the set of vertices that $X$ reaches in $G - S$. So $X \subseteq R$ and $R \cap Y = \emptyset$, and we write $R(S)$ for this set.

A minimal $(X, Y)$-cut $S$ is *important* if there is no $(X, Y)$-cut $S'$ with $|S'| \le |S|$ and $R(S) \subsetneq R(S')$.

The method has a general template and an enumeration procedure. The template has three holes. SOLVED$(I)$ tests in polynomial time if the instance $I$ needs no more deletions. PICK$(I)$ returns a pair $(X, Y)$ such that a pushing lemma holds: if $I$ has a solution of size at most $k$, then it has one that contains an important $(X, Y)$-cut. APPLY$(I, S)$ deletes the edges of $S$ from $I$.

```pseudo id=main
SEPARATE(I, k)
L1  if SOLVED(I) then return YES
L2  if k = 0 then return NO
L3  (X, Y) ← PICK(I)
L4  for each important (X, Y)-cut S with |S| ≤ k do
L5      if SEPARATE(APPLY(I, S), k - |S|) = YES then return YES
L6  return NO
```

Line L4 uses the enumeration procedure below. It returns a set of candidate cuts that contains all important cuts of size at most $k$. A final filter removes candidates that are not important; it is optional for correctness of SEPARATE, because extra candidates are still cuts.

```pseudo id=enum
CANDIDATES(G, X, Y, k)
L1  λ ← size of a minimum (X, Y)-cut in G
L2  if λ > k then return ∅
L3  if λ = 0 then return {∅}
L4  R ← R_max(G, X, Y)
L5  choose an edge uv in δ(R) with u ∈ R
L6  A ← { S ∪ {uv} : S ∈ CANDIDATES(G - uv, R, Y, k - 1) }
L7  if v ∈ Y then B ← ∅ else B ← CANDIDATES(G, R ∪ {v}, Y, k)
L8  return A ∪ B
```

**Lemma 1 (submodularity).** For all sets $A, B$ of vertices, $|\delta(A)| + |\delta(B)| \ge |\delta(A \cap B)| + |\delta(A \cup B)|$.

*Proof.* Count the contribution of each edge $e = pq$ to both sides. If both endpoints lie in the same region of the Venn diagram of $A$ and $B$, $e$ adds 0 to both sides. If $p \in A \setminus B$ and $q \in B \setminus A$, then $e$ is in $\delta(A)$ and $\delta(B)$ but in neither $\delta(A \cap B)$ nor $\delta(A \cup B)$, so it adds 2 to the left and 0 to the right. In every other case one checks that $e$ adds the same amount to both sides, for example $p \in A \cap B$ and $q$ outside $A \cup B$ adds 2 to each side. $\square$

**Lemma 2 (the farthest minimum cut).** Let $\lambda$ be the size of a minimum $(X, Y)$-cut. Among the sets $R$ with $X \subseteq R$, $R \cap Y = \emptyset$ and $|\delta(R)| = \lambda$ there is a unique largest one, $R_{\max}$. It is the set of vertices from which $Y$ cannot be reached in the residual graph of a maximum flow, so it costs $O(\lambda (n + m))$ time with $\lambda$ augmenting paths.

*Proof.* Let $R_1$ and $R_2$ be two such sets. Both $R_1 \cap R_2$ and $R_1 \cup R_2$ contain $X$ and avoid $Y$, so each has $|\delta| \ge \lambda$. By Lemma 1, $|\delta(R_1 \cup R_2)| \le 2\lambda - |\delta(R_1 \cap R_2)| \le \lambda$. So the union of all such sets is again such a set, and it is the largest. The flow statement is the standard description of the minimum cuts by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/). $\square$

**Lemma 3 (pushing to $R_{\max}$).** If $S$ is an important $(X, Y)$-cut, then $R_{\max} \subseteq R(S)$. So the important $(X, Y)$-cuts and the important $(R_{\max}, Y)$-cuts are the same sets.

*Proof.* Let $R = R(S)$. The set $R_{\max} \cap R$ contains $X$ and avoids $Y$, so $|\delta(R_{\max} \cap R)| \ge \lambda$. Lemma 1 gives $|\delta(R_{\max} \cup R)| \le \lambda + |\delta(R)| - \lambda = |S|$. If $R_{\max} \not\subseteq R$, then $R \subsetneq R_{\max} \cup R$, and $\delta(R_{\max} \cup R)$ is a cut no larger than $S$ whose reached set contains $R_{\max} \cup R$. That contradicts the importance of $S$. $\square$

**Theorem (Chen, Liu and Lu; Marx).** There are at most $4^k$ important $(X, Y)$-cuts of size at most $k$, and CANDIDATES finds a set that contains all of them in time $O(4^k \cdot k \cdot (n + m))$.

*Proof.* Let $S$ be an important cut of size at most $k$. By Lemma 3, $R_{\max} \subseteq R(S)$. Take the edge $uv$ of line L5.

- If $uv \in S$, then $S \setminus \{uv\}$ is an important $(R_{\max}, Y)$-cut of $G - uv$ of size at most $k - 1$. It is a cut, and it is minimal, because a smaller cut $S''$ in $G - uv$ would make $S'' \cup \{uv\}$ a smaller cut in $G$. It is important: a cut $S'$ of $G - uv$ with $|S'| \le |S| - 1$ and a larger reached set gives the cut $S' \cup \{uv\}$ of $G$ with $|S' \cup \{uv\}| \le |S|$ and a larger reached set.
- If $uv \notin S$, then $v \in R(S)$, because $u \in R(S)$. So $v \notin Y$ and $S$ is an important $(R_{\max} \cup \{v\}, Y)$-cut.

So, by induction, every important cut appears in A or B. Now count the leaves of the recursion with the measure $\mu = 2k - \lambda$. In the call on line L6, $k$ drops by 1 and $\lambda$ drops by at most 1, so $\mu$ drops by at least 1. In the call on line L7, $k$ stays the same and the new minimum cut is larger than $\lambda$, because a cut of size $\lambda$ with $R_{\max} \cup \{v\}$ on its side would contradict Lemma 2; so $\mu$ drops by at least 1. A call with $\lambda \le k$ has $\mu \ge k \ge 0$, and a call with $\lambda > k$ stops. So the recursion tree is binary with depth at most $2k$ and has at most $2^{2k} = 4^k$ leaves. Each leaf returns at most one cut. Each node runs one flow computation in $O(k (n + m))$ time. $\square$

**Lemma 4 (a sharper count).** If $\mathcal{S}$ is the set of all important $(X, Y)$-cuts, then $\sum_{S \in \mathcal{S}} 4^{-|S|} \le 2^{-\lambda} \le 1$.

*Proof.* Use the same recursion with no bound on $k$, and induct on the number of edges plus the number of vertices outside $X$. If $\lambda = 0$, the only cut is $\emptyset$ and the sum is $1 = 2^0$. Otherwise the cuts from line L6 have the form $S \cup \{uv\}$ with $S$ from a graph whose minimum cut is at least $\lambda - 1$, so they add at most $\tfrac{1}{4} \cdot 2^{-(\lambda - 1)} = 2^{-\lambda}/2$. The cuts from line L7 come from an instance with minimum cut at least $\lambda + 1$, so they add at most $2^{-(\lambda + 1)} = 2^{-\lambda}/2$. $\square$

**The search tree of SEPARATE.** Each important cut used in line L4 is nonempty, because the pair $(X, Y)$ still has a path. Let $L(k)$ be the largest number of leaves for budget $k$. By Lemma 4, $L(k) \le \sum_S L(k - |S|) \le \sum_S 4^{k - |S|} \le 4^k$. So SEPARATE has at most $4^k$ leaves, and its depth is at most $k$.

## Classic examples

### A small graph with many important cuts

Take $X = \{x\}$, $Y = \{y\}$ and $g$ copies of a gadget: an edge $x u_i$, and two paths $u_i p_i y$ and $u_i q_i y$. Each gadget is cut either by the single edge $x u_i$ or by two edges. The two edges $u_i p_i, u_i q_i$ are never important, because $p_i y, q_i y$ has the same size and lies farther from $x$. A scratch script enumerated the important cuts by brute force over all vertex sets $R$, and also ran CANDIDATES.

For $g = 2$, the minimum cut has $\lambda = 2$ and $R_{\max} = \{x\}$. The important cuts of size at most 4 are:

| size | cut | $R(S)$ |
|---|---|---|
| 2 | $x u_1, x u_2$ | $\{x\}$ |
| 3 | $p_1 y, q_1 y, x u_2$ | $\{x, u_1, p_1, q_1\}$ |
| 3 | $p_2 y, q_2 y, x u_1$ | $\{x, u_2, p_2, q_2\}$ |
| 4 | $p_1 y, q_1 y, p_2 y, q_2 y$ | all but $y$ |

So there are 1, 3 and 4 important cuts of size at most 2, 3 and 4. The sum of $4^{-|S|}$ is $1/16 + 2/64 + 1/256 = 0.0977$, below $2^{-\lambda} = 0.25$, as Lemma 4 says. For $g = 3$ the counts for $k = 3, 4, 5, 6$ are 1, 4, 7 and 8. With $g = k/2$ gadgets there are $2^{k/2}$ important cuts of size at most $k$, so the number really is exponential in $k$.

### The 4^k bound is nearly tight

Let $Y$ be the leaves of a complete binary tree, and let $X$ be one extra vertex joined to the root. Every subtree that contains the root and whose boundary has $k$ edges gives an important cut of size $k$. The number of such subtrees is the Catalan number $C_{k-1} = \frac{1}{k}\binom{2k-2}{k-1}$, which is $4^k$ divided by a polynomial in $k$. The script checked the tree of depth 3, with 16 vertices and 8 leaves: it found 1, 1, 2 and 5 important cuts of sizes 1, 2, 3 and 4, which are $C_0, C_1, C_2, C_3$.

### Edge multiway cut

Given terminals $T$, a *multiway cut* is a set of at most $k$ edges whose deletion leaves each terminal in its own component. **Pushing lemma:** for every $t \in T$, some minimum solution contains an important $(t, T \setminus \{t\})$-cut.

*Proof.* Let $S$ be a solution and $R$ the vertices that $t$ reaches in $G - S$. Then $\delta(R) \subseteq S$ is a $(t, T \setminus \{t\})$-cut. If it is not important, take an important cut $\delta(R')$ with $R \subsetneq R'$ and $|\delta(R')| \le |\delta(R)|$, and set $S' = (S \setminus \delta(R)) \cup \delta(R')$, so $|S'| \le |S|$. In $G - S'$, $t$ reaches no other terminal. If two other terminals $u, v$ were joined by a path in $G - S'$, the path uses an edge of $\delta(R)$, so it enters $R \subseteq R'$; but $u$ and $v$ lie outside $R'$, so the path also crosses $\delta(R')$, which is deleted. $\square$

So PICK chooses a terminal $t$ that still reaches another terminal, with $X = \{t\}$ and $Y = T \setminus \{t\}$. The tree has at most $4^k$ leaves, and the total time is $O(4^k k^3 (n + m))$. On a $3 \times 3$ grid with terminals at three corners, the script found that the least edge multiway cut has 4 edges, with 7 optimal solutions. From the corner $(0, 0)$ there are three important cuts of size at most 4, of sizes 2, 3 and 4. SEPARATE with $k = 4$ succeeds on its first leaf, and with $k = 3$ it fails after 2 leaves. See [parameterized multiway cut](/parameterized-multiway-cut/).

### Few edges near a vertex

At most $k \cdot 4^k$ edges at a vertex $t$ belong to some inclusion-minimal $(s, t)$-cut of size at most $k$. Each such edge $vt$ lies in an important $(s, t)$-cut: push the cut $\delta(R)$ with $v \in R$ to an important cut $\delta(R')$ with $R \subseteq R'$, and then $v \in R'$, so $vt$ is still cut. There are at most $4^k$ important cuts, each with at most $k$ edges.

### Anti-isolation

Let $s, t_1, \ldots, t_n$ be vertices and $S_1, \ldots, S_n$ be cuts of size at most $k$ such that $S_i$ separates $t_j$ from $s$ exactly when $j \ne i$. Then $n \le (k + 1) 4^{k + 1}$. Add a new vertex $t$ joined to every $t_i$; then each edge $t t_i$ lies in a minimal $(s, t)$-cut of size at most $k + 1$, and the previous example bounds their number.

### Directed feedback vertex set

The compression step of the algorithm of Chen, Liu, Lu, O'Sullivan and Razgon reduces to a cut problem in a directed graph, and it branches over important separators in that graph. See [directed feedback vertex set](/directed-feedback-vertex-set/).

## Variations

- **Vertex separators.** An $(X, Y)$-separator is a set of vertices outside $X \cup Y$ whose deletion destroys all $X$-$Y$ paths. Important separators are defined in the same way, and there are at most $4^k$ of size at most $k$. Node multiway cut uses this version.
- **Directed graphs.** With $\delta^+(R)$, the arcs that leave $R$, the same proofs work, because the out-cut function is also submodular. The bound $4^k$ holds.
- **Random sampling of important separators.** Marx and Razgon choose each important separator at random with a suitable probability and delete the union. With probability depending only on $k$, this removes all vertices that a solution would cut away from the terminals, its *shadow*, without touching the solution. This *shadow removal* step proved that [multicut](/parameterized-multicut/) is FPT in the cut size, and that directed multiway cut is FPT (Chitnis, Hajiaghayi and Marx).
- **Enumeration with output-linear cost.** A refined procedure lists exactly the important cuts of size at most $k$ in time $O(|\mathcal{S}_k| \cdot k^2 (n + m))$, where $\mathcal{S}_k$ is the set of those cuts.

## Pitfalls

- **Minimal is not enough.** A minimal cut may be pushed farther with no extra cost. The definition compares the reached sets $R(S)$, not the cuts themselves.
- **The converse of the first branch is false.** An important cut of $G - uv$ plus $uv$ need not be important in $G$. In the graph with vertices $s, a, b, c, t$ and edges $sa, sc, ab, ac, at, bt, ct$, with $X = \{s\}$ and $Y = \{t\}$ and $k = 3$, CANDIDATES returned the three cuts $\{sa, sc\}$, $\{at, bt, ct\}$ and $\{sa, ac, ct\}$. The third is not important: its reached set is $\{s, c\}$, and $\{at, bt, ct\}$ has the same size and reaches $\{s, a, b, c\}$. Filter the output when the exact set is needed.
- **The pushing lemma must be proved for the problem.** For multiway cut it holds for every terminal, but in many problems it holds only for a carefully chosen pair $(X, Y)$, and a wrong choice gives a wrong algorithm.
- **Branching over cuts of a fixed size.** Branching only over important cuts of size exactly $k$, or only over minimum cuts, loses solutions. All sizes from $\lambda$ to $k$ are needed.
- **Weights.** The bound counts edges. With integer weights one can replace an edge of weight $w$ by $w$ parallel edges, but then the parameter is the total weight, not the number of edges.

## Exercises

1. Prove Lemma 1 by listing all ten types of edges by the positions of their endpoints.
2. Show that $\delta(R)$ is an important $(X, Y)$-cut if and only if it is a minimal cut and $R$ is the set $R_{\max}$ for the pair $(R, Y)$.
3. Count the important $(x, y)$-cuts of the gadget graph with $g$ gadgets for every size, and check the counts 1, 4, 7, 8 for $g = 3$.
4. Prove the pushing lemma for node multiway cut, where the solution deletes vertices other than terminals.
5. Give an edge that lies in a minimal $(s, t)$-cut of size at most $k$ but in no important $(s, t)$-cut of size at most $k$. Why does this not contradict the "few edges near a vertex" bound?

## References
