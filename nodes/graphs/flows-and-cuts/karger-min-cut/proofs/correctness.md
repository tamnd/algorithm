---
title: Karger's algorithm returns a cut, and a minimum one with probability at least 2/(n(n-1)) per run
proves: [correctness, success-probability]
status: full
---

Let $G = (V, E)$ be an undirected multigraph with $n \ge 2$ vertices, and let $\lambda$ be the size of a minimum cut, that is, the least number of edges with exactly one end in $S$ over all $S$ with $\emptyset \ne S \subsetneq V$. We use the pseudocode of the page. During a run, the classes of the union-find structure are the *super-vertices*. An edge is a *loop* if both its ends are in the same class.

**Lemma 1 (each run returns a cut).** CONTRACT returns $(S, k)$ with $0 \in S$, $S \ne V$, and $k$ equal to the number of edges with exactly one end in $S$. So $k \ge \lambda$.

*Proof.* Line L9 merges two classes only when they differ, so `comps` is always the number of classes, and it never drops below 2: the loop of line L8 stops as soon as it reaches 2, and each step lowers it by at most 1. So at line L10 there are at least two classes, and the class $S$ of vertex 0 is not all of $V$. Line L11 counts the crossing edges exactly. $\square$

**Lemma 2 (degrees).** At any moment, each super-vertex $X$ is incident to at least $\lambda$ non-loop edges, so if $i$ super-vertices remain, there are at least $i \lambda / 2$ non-loop edges.

*Proof.* The non-loop edges at $X$ are exactly the edges of $G$ with one end in $X$ and the other end outside $X$. When at least two super-vertices remain, $\emptyset \ne X \subsetneq V$, so this number is a cut size and at least $\lambda$. Summing over the $i$ super-vertices counts each non-loop edge twice. $\square$

**Lemma 3 (the shuffle is random contraction).** Condition on the edges that the loop has read so far. The next edge that line L9 contracts is uniformly distributed over the non-loop edges at that moment.

*Proof.* Given the prefix of $\pi$ read so far, the remaining edges are in a uniformly random order, because $\pi$ is a uniform permutation. The edges read so far are all loops now: each one was either contracted or was already a loop. So the non-loop edges at this moment are exactly the remaining edges whose ends lie in different classes. Classes change only at a contraction, so the next contraction is the first edge in the random order of the remaining edges that belongs to this set. By symmetry of the uniform order, each edge of the set is equally likely to come first. $\square$

**Lemma 4 (disconnected graphs).** If $\lambda = 0$, every run returns $k = 0$.

*Proof.* If the loop of line L8 reads all edges, each class is a connected component, since every edge was contracted or was a loop. There are then at least two classes, and no edge joins $S$, the component of 0, to the rest, so $k = 0$. If the loop stops at two classes, each class is a connected set of vertices, so it lies inside one component. There are at least two components, and each component is a union of classes, so each of the two classes is a whole component, and again $k = 0$. $\square$

**Theorem.** Assume $\lambda \ge 1$. Let $S^{*}$ with $0 \in S^{*}$ be a fixed minimum cut, and let $F$ be its $\lambda$ crossing edges. One run of CONTRACT returns $S = S^{*}$ with probability at least $2 / (n(n-1))$.

*Proof.* As $\lambda \ge 1$, the graph is connected, so the loop always ends with exactly two classes. If no edge of $F$ is ever contracted, every class stays inside $S^{*}$ or inside $V \setminus S^{*}$, so at the end the two classes are $S^{*}$ and $V \setminus S^{*}$, and $S = S^{*}$. A contraction of an edge of $F$ puts a vertex of $S^{*}$ and a vertex outside it in one class, which never splits again, so the run cannot return $S^{*}$. Hence the run returns $S^{*}$ exactly when no edge of $F$ is contracted.

There are $n - 2$ contractions. Before the $j$-th one, $i = n - j + 1$ super-vertices remain, with $3 \le i \le n$. Let $\mathcal{E}_j$ be the event that none of the first $j$ contractions takes an edge of $F$. Given $\mathcal{E}_{j-1}$, all $\lambda$ edges of $F$ are non-loop edges, and by Lemma 2 there are at least $i \lambda / 2$ non-loop edges. By Lemma 3 the next contraction picks a uniform non-loop edge, so

$$\Pr[\mathcal{E}_j \mid \mathcal{E}_{j-1}] \ge 1 - \frac{\lambda}{i \lambda / 2} = 1 - \frac{2}{i}.$$

Multiplying over $j = 1, \ldots, n - 2$, that is, over $i = n, n - 1, \ldots, 3$,

$$\Pr[S = S^{*}] = \Pr[\mathcal{E}_{n-2}] \ge \prod_{i=3}^{n} \frac{i - 2}{i} = \frac{(n-2)!\, / \, 0!}{n! \, / \, 2!} = \frac{2}{n(n-1)}.$$

The product telescopes: the numerators are $1, 2, \ldots, n - 2$ and the denominators are $3, 4, \ldots, n$. $\square$

**Corollary 1 (amplification).** KARGER-MIN-CUT with $T$ runs returns $\lambda$ with probability at least $1 - (1 - 2/(n(n-1)))^T \ge 1 - e^{-2T/(n(n-1))}$, and it never returns a value below $\lambda$.

*Proof.* By Lemma 1 each run gives $k \ge \lambda$, and line L4 keeps the least $k$, so the output is at least $\lambda$, and it is $\lambda$ if some run returns a minimum cut. If $\lambda = 0$, every run returns $k = 0$ by Lemma 4. Otherwise the runs use independent permutations, so all of them miss the fixed cut $S^{*}$ with probability at most $(1 - p)^T$ with $p \ge 2/(n(n-1))$, and $1 - p \le e^{-p}$. $\square$

**Corollary 2 (number of minimum cuts).** A connected multigraph with $n \ge 2$ vertices has at most $\binom{n}{2}$ minimum cuts.

*Proof.* For distinct minimum cuts $S_1^{*}, S_2^{*}, \ldots$ (each written with vertex 0 on its side), the events "one run returns $S_r^{*}$" are disjoint, and each has probability at least $1/\binom{n}{2}$ by the theorem. Their probabilities sum to at most 1. $\blacksquare$
