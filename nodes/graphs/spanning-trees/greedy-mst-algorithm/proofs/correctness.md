---
title: The greedy MST algorithm returns a minimum spanning forest for every order of the blue and red rules
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a finite undirected graph with a real weight $w(e)$ on each edge. Parallel edges and self-loops are allowed, weights may tie, and $G$ need not be connected. A *spanning forest* is a forest $F \subseteq E$ with the same components as $G$; it has $n - c$ edges, where $c$ is the number of components. A *minimum spanning forest* (MSF) is a spanning forest of least total weight. In a connected graph it is a minimum spanning tree.

During the run each edge is uncolored, blue or red. We write $B$ for the set of blue edges and $R$ for the set of red edges.

## The invariant

**Invariant I.** Some minimum spanning forest $T$ has $B \subseteq T$ and $T \cap R = \emptyset$.

**Lemma 1 (start).** Invariant I holds after line L1.

*Proof.* $B = R = \emptyset$, and $G$ has a spanning forest, so it has a minimum one. $\square$

**Lemma 2 (blue rule).** Assume Invariant I holds with the forest $T$. Let $(S, V \setminus S)$ be a cut that no blue edge crosses, and let $e = (u, v)$ be a lightest uncolored edge that crosses it, with $u \in S$. Then Invariant I holds after $e$ is colored blue.

*Proof.* If $e \in T$, the forest $T$ still works. Otherwise $T \cup \{e\}$ has exactly one cycle, the fundamental cycle of $e$: the edge $e$ and the path $P$ in $T$ from $u$ to $v$. (The path exists: $u$ and $v$ are in one component of $G$, and $T$ spans it.) The path starts in $S$ and ends outside $S$, so it has an edge $f$ that crosses the cut. Then:

- $f$ is not blue, because no blue edge crosses the cut;
- $f$ is not red, because $f \in T$ and $T \cap R = \emptyset$;
- so $f$ is uncolored, and since $e$ is a lightest uncolored crossing edge, $w(e) \le w(f)$.

Let $T' = T - f + e$. Removing $f$ splits one tree of $T$ into two, with $u$ and $v$ on different sides, since $f$ lies on their only path; adding $e$ joins them again. So $T'$ is a spanning forest, and $w(T') = w(T) - w(f) + w(e) \le w(T)$, so $T'$ is an MSF. It contains $B \cup \{e\}$, since $f \notin B$. It avoids $R$, since $e$ was uncolored and $T$ avoids $R$. $\square$

**Lemma 3 (red rule).** Assume Invariant I holds with the forest $T$. Let $C$ be a simple cycle with no red edge, and let $e = (u, v)$ be a heaviest uncolored edge of $C$. Then Invariant I holds after $e$ is colored red.

*Proof.* If $e \notin T$, the forest $T$ still works. Otherwise $e \in T$, so $e$ is not a self-loop and $C \setminus \{e\}$ is a path from $u$ to $v$. Removing $e$ splits the tree of $T$ that holds it into two trees; let $S$ be the vertex set of the one that holds $u$, so $v \notin S$. The path $C \setminus \{e\}$ starts in $S$ and ends outside it, so it has an edge $f$ with exactly one end in $S$. Then:

- $f \notin T$, because the only edge of $T$ with exactly one end in $S$ is $e$, and $f \ne e$;
- $f$ is not blue, because $B \subseteq T$;
- $f$ is not red, because $C$ has no red edge;
- so $f$ is uncolored, and since $e$ is a heaviest uncolored edge of $C$, $w(f) \le w(e)$.

Let $T' = T - e + f$. The edge $f$ joins the two trees again, so $T'$ is a spanning forest with $w(T') \le w(T)$, hence an MSF. It contains $B$, since $e \notin B$ ($e$ was uncolored). It avoids $R \cup \{e\}$, since $f$ is uncolored. $\square$

## The scheme never gets stuck

**Lemma 4 (applicability).** Before each step, the blue edges form a forest. If an edge $e = (u, v)$ is uncolored, then a rule applies in the way lines L3 to L8 describe.

*Proof.* By Invariant I, $B \subseteq T$ and $T$ is a forest, so $B$ is a forest.

- If $u$ and $v$ are in different blue trees, let $S$ be a union of blue trees that holds $u$ and not $v$ (for example the blue tree of $u$). No blue edge has exactly one end in $S$, and the uncolored edge $e$ crosses the cut. So the blue rule applies to this cut.
- If $u$ and $v$ are in one blue tree, let $P$ be the blue path from $u$ to $v$ (empty if $e$ is a self-loop). Then $P \cup \{e\}$ is a simple cycle: $e \notin P$ since $e$ is uncolored, and $P$ is a simple path. It has no red edge and contains the uncolored edge $e$, so the red rule applies. If line L7 uses any other path of non-red edges from $u$ to $v$ that avoids $e$, the same holds for the cycle it gives; the implementation finds such a path by breadth-first search, which gives a simple path. $\square$

## Termination and the result

**Theorem.** For each sequence of choices, GREEDY-MST stops after exactly $m$ steps, and the set $B$ it returns is a minimum spanning forest of $G$.

*Proof.* Each step colors exactly one uncolored edge (Lemma 4 shows that a step exists while an edge is uncolored), and no color changes. So the loop runs exactly $m$ times. By Lemmas 1, 2 and 3 and induction on the steps, Invariant I holds at the end, with some MSF $T$. Then every edge is blue or red, $B \subseteq T$ and $T \cap R = \emptyset$, so $T \subseteq E \setminus R = B$. Hence $B = T$, an MSF. $\blacksquare$

**Remark (ties).** Lemmas 2 and 3 use only $w(e) \le w(f)$ and $w(f) \le w(e)$. So any lightest or heaviest uncolored edge may be chosen when weights tie, and different choices may give different minimum spanning forests, all of the least weight.
