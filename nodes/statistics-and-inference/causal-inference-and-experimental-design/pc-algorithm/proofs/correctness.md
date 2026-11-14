---
title: With a perfect independence oracle for a distribution that is Markov and faithful to a DAG G, the PC algorithm stops and returns the skeleton and the v-structures of G, and every edge that the Meek rules direct has the same direction in every DAG Markov equivalent to G
proves: [correctness, termination]
status: full
---

**Setting.** $G$ is a DAG on the finite set $V$ of $n$ nodes, and $P$ is a distribution on $V$. The causal Markov condition says that each $d$-separation $(a \perp b \mid S)_G$ implies $a \perp b \mid S$ in $P$. Faithfulness says the converse: each independence $a \perp b \mid S$ in $P$ implies $(a \perp b \mid S)_G$. Together, $a \perp b \mid S$ holds in $P$ exactly when $S$ d-separates $a$ and $b$ in $G$. The oracle answers the test of line L5 with the truth in $P$. Two DAGs are Markov equivalent when they have the same d-separations. By Verma and Pearl (1990), this holds exactly when they have the same skeleton and the same v-structures, that is, the same triples $a \to c \leftarrow b$ with $a$ and $b$ not adjacent. The class of $G$ is the set of DAGs Markov equivalent to $G$.

**Lemma 1 (local Markov property).** If $a$ and $b$ are not adjacent in $G$ and $b$ is not a descendant of $a$, then $\mathrm{pa}(a)$ d-separates $a$ and $b$.

*Proof.* Take a path from $a$ to $b$. If its first arrow is $p \to a$, then $p \in \mathrm{pa}(a)$ is a non-collider on the path, $p \ne b$, and $p$ is in the conditioning set, so the path is blocked. Otherwise the path starts $a \to c$. It cannot be directed all the way to $b$, since $b$ is not a descendant of $a$. So there is a first node $d$ where the direction turns, $\to d \leftarrow$, and $d$ is a descendant of $a$. If $d$ or one of its descendants were in $\mathrm{pa}(a)$, then $a$ would be its own ancestor, which is a cycle. So the collider $d$ blocks the path. $\square$

**Lemma 2 (skeleton).** Line L1 to line L6 stop, and at the end two nodes are adjacent exactly when they are adjacent in $G$. Every removed pair $\{a, b\}$ has $\mathrm{sepset}(a, b) = S$ with $(a \perp b \mid S)_G$.

*Proof.* An edge is removed only when the oracle reports $a \perp b \mid S$, and then $(a \perp b \mid S)_G$ by faithfulness. Adjacent nodes of $G$ are d-connected given every set, since the single edge is a path with no inner node. So no edge of $G$ is removed, and at all times $\mathrm{adj}(a)$ contains the neighbours of $a$ in $G$.

Let $a$ and $b$ be non-adjacent in $G$. As $G$ is acyclic, $b$ is not a descendant of $a$, or $a$ is not a descendant of $b$; by symmetry say the first. By Lemma 1, $\mathrm{pa}(a)$ separates them, and $\mathrm{pa}(a) \subseteq \mathrm{adj}(a) \setminus \{b\}$ at all times. Let $k_0 = |\mathrm{pa}(a)|$. Suppose the edge $a - b$ is still present at the start of level $k_0$. Then $|\mathrm{adj}(a)| - 1 \ge k_0$, so the loop of line L2 runs level $k_0$, and line L3 visits the ordered pair $(a, b)$ unless the edge has gone already. Line L4 then reaches $S = \mathrm{pa}(a)$ unless an earlier set removes the edge. Either way the edge is gone after level $k_0$.

So after level $q$, where $q$ is the largest degree in $G$, the graph is the skeleton of $G$. Then $|\mathrm{adj}(a)| - 1 < q + 1$ for every $a$, and the loop stops after at most $q + 1$ levels. Each level makes finitely many tests. $\square$

**Lemma 3 (v-structures).** Let $a$ and $b$ be non-adjacent with a common neighbour $c$ in the skeleton. Then $c \notin \mathrm{sepset}(a, b)$ exactly when $a \to c \leftarrow b$ in $G$.

*Proof.* Let $S = \mathrm{sepset}(a, b)$. By Lemma 2, $S$ d-separates $a$ and $b$ in $G$, so the path $a - c - b$ is blocked by $S$. If $c$ is a collider on it, the path is blocked only if $c \notin S$ (and no descendant of $c$ is in $S$). If $c$ is a non-collider, the path is blocked only if $c \in S$. $\square$

So after line L8 the graph has the skeleton of $G$, and the arrows are exactly the v-structures of $G$. Since the class of $G$ shares the skeleton and the v-structures, every arrow at this point has the same direction in every DAG of the class.

**Lemma 4 (soundness of the Meek rules).** Suppose every arrow of the current graph has the same direction in every DAG of the class, and every v-structure of $G$ is an arrow pair in it. Then each of R1, R2 and R3 adds an arrow with the same property.

*Proof.* Let $D$ be any DAG of the class. By the hypothesis, $D$ has every current arrow. The edge $b - c$ that the rule orients is undirected. The v-structures of $D$ are those of $G$, and their arrows are arrows of the current graph. So no v-structure of $D$ uses the edge between $b$ and $c$. We show $b \to c$ in $D$.

- R1: $a \to b - c$ with $a$ and $c$ not adjacent. If $c \to b$ in $D$, then $a \to b \leftarrow c$ is a v-structure of $D$ that uses the edge $b - c$. That is impossible, so $b \to c$.
- R2: $b \to a \to c$ and $b - c$. If $c \to b$ in $D$, then $b \to a \to c \to b$ is a cycle in $D$. So $b \to c$.
- R3: $b - a_1$, $b - a_2$, $a_1 \to c \leftarrow a_2$, $a_1$ and $a_2$ not adjacent, and $b - c$. Suppose $c \to b$ in $D$. If $b \to a_1$ in $D$, then $a_1 \to c \to b \to a_1$ is a cycle, so $a_1 \to b$ in $D$. In the same way $a_2 \to b$. Then $a_1 \to b \leftarrow a_2$ is a v-structure of $D$, so of $G$, so it is an arrow pair of the current graph. But $b - a_1$ is undirected, a contradiction. So $b \to c$. $\square$

**Theorem (termination and correctness).** With a perfect oracle under the causal Markov condition and faithfulness, the PC algorithm stops. Its output has the skeleton of $G$ and the v-structures of $G$ as arrows, and every arrow in it has the same direction in all DAGs of the class of $G$. No DAG of the class has a v-structure that is not an arrow pair of the output.

*Proof.* Lemma 2 gives termination of the first phase and the skeleton. Lemma 3 gives the v-structures. Each pass of the loop of line L9 either directs at least one of the finitely many undirected edges or stops, so the loop stops. Lemma 4 and induction over the arrows added show that every arrow has the same direction in the whole class. $\square$

**What is cited, not proved here.** The theorem shows that each directed edge of the output is directed in the CPDAG (the edges on which the whole class agrees). The converse, that each edge left undirected by R1 to R3 takes both directions in DAGs of the class, is the completeness theorem of Meek (1995). With it, the output is exactly the CPDAG. The tests check this converse by exhaustive enumeration for all 25 DAGs on three nodes and all 543 DAGs on four nodes, and on 25 random DAGs with five to seven nodes against an enumeration of their classes.

**What does not follow.** The theorem assumes a perfect oracle. With statistical tests on finite data, errors in early tests change the later conditioning sets and orientations. Consistency of PC with tests at a suitable level, also when the number of variables grows with the sample size, is a theorem of Kalisch and Bühlmann (2007) for Gaussian data, and is cited, not proved here.
