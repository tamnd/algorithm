---
title: Lawler's dynamic program computes the chromatic number of every induced subgraph
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a finite simple graph. For $S \subseteq V$ write $G[S]$ for the induced subgraph and $\chi(S) = \chi(G[S])$, with $\chi(\emptyset) = 0$. Identify each subset with its bitmask, so that a proper subset $T \subsetneq S$ has a smaller bitmask than $S$.

**Termination.** Line L2 visits the $2^n - 1$ nonempty subsets once each. For each $S$, line L4 runs over the finite family of maximal independent sets of $G[S]$, and this family is not empty when $S \ne \emptyset$, since any single vertex of $S$ extends greedily to a maximal independent set. So the algorithm stops, and $X[S]$ is finite after the turn of $S$.

**Order of evaluation.** If $S \ne \emptyset$ and $I$ is a maximal independent set of $G[S]$, then $I \ne \emptyset$, so $S \setminus I$ is a proper subset of $S$. Its bitmask is smaller, so its turn in line L2 came earlier (or it is $\emptyset$, set in line L1). Hence line L5 reads only final values.

**Claim.** After the turn of $S$, $X[S] = \chi(S)$.

*Proof.* By strong induction on the bitmask of $S$. For $S = \emptyset$, line L1 sets $X[\emptyset] = 0 = \chi(\emptyset)$. Let $S \ne \emptyset$ and assume the claim for all smaller bitmasks, in particular for all proper subsets of $S$. After the loop of lines L4 and L5,

$$X[S] = 1 + \min \{\, \chi(S \setminus I) : I \text{ a maximal independent set of } G[S] \,\}.$$

*Upper bound on $\chi(S)$.* Fix a maximal independent set $I$ of $G[S]$ and a proper coloring of $G[S \setminus I]$ with $\chi(S \setminus I)$ colors. Give every vertex of $I$ one new color. No edge joins two vertices of $I$, since $I$ is independent, and an edge between $I$ and $S \setminus I$ has ends of different colors because the color of $I$ is new. So $G[S]$ has a proper coloring with $\chi(S \setminus I) + 1$ colors, and $\chi(S) \le X[S]$.

*Lower bound on $\chi(S)$.* Let $k = \chi(S) \ge 1$ and fix a proper coloring of $G[S]$ with classes $C_1, \ldots, C_k$; we may take $C_1 \ne \emptyset$. The class $C_1$ is independent in $G[S]$. Add vertices of $S$ to it one at a time, each time a vertex with no neighbor in the current set, until no such vertex is left. The result $I \supseteq C_1$ is a maximal independent set of $G[S]$. The sets $C_2 \setminus I, \ldots, C_k \setminus I$ are independent and cover $S \setminus I$, because $S \setminus I \subseteq S \setminus C_1 = C_2 \cup \cdots \cup C_k$. So $\chi(S \setminus I) \le k - 1$, and the term of $I$ in the minimum gives $X[S] \le 1 + (k - 1) = \chi(S)$.

The two bounds give $X[S] = \chi(S)$, which proves the claim. $\square$

**Output.** Line L6 returns $X[V] = \chi(G)$. For the coloring, the implementation stores at each $S$ the set $I$ that gave the minimum. Following these choices from $V$ gives sets $I_1, I_2, \ldots$ with $S_0 = V$, $S_j = S_{j-1} \setminus I_j$ and $X[S_j] = X[S_{j-1}] - 1$, so the chain reaches $\emptyset$ after exactly $X[V]$ steps. Each $I_j$ is independent and the $I_j$ partition $V$, so giving color $j$ to $I_j$ is a proper coloring with $\chi(G)$ colors. ∎
