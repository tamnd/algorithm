---
title: BCNF decomposition stops and returns a lossless decomposition into BCNF
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $R$ is a finite set of attributes, $F$ a set of functional dependencies over $R$, and $X^+$ the closure of $X$ under $F$. A relation $r$ over $R$ is *legal* when it satisfies $F$. For $S \subseteq R$ and a legal $r$, $\pi_S(r)$ satisfies each dependency $V \to W$ with $V \cup W \subseteq S$ that $F$ implies, because two tuples of $\pi_S(r)$ come from two tuples of $r$ with the same values on $S$.

**Claim.** BCNF-DECOMPOSE$(R, F)$ stops. Its output $R_1, \ldots, R_k$ satisfies (a) $R_1 \cup \cdots \cup R_k = R$, (b) each $R_i$ is in BCNF under $\pi_{R_i}(F)$, and (c) $r = \pi_{R_1}(r) \bowtie \cdots \bowtie \pi_{R_k}(r)$ for each legal $r$.

**Lemma 1 (one split).** Let $S$ be popped at line L3, and let line L4 find $X \subset S$ with $(X^+ \cap S) \ne X$ and $S \not\subseteq X^+$. Let $Y = (X^+ \cap S) - X$, $S_1 = X \cup Y$ and $S_2 = S - Y$. Then $S_1$ and $S_2$ are nonempty proper subsets of $S$, $S_1 \cup S_2 = S$ and $S_1 \cap S_2 = X$.

*Proof.* $Y \ne \emptyset$ because $X^+ \cap S$ contains $X$ and is not equal to $X$. $S_1 = X^+ \cap S$, and $S_1 \ne S$ because $S \not\subseteq X^+$. $S_1 \supseteq Y \ne \emptyset$. $S_2 \ne S$ because $Y \subseteq S$ and $Y \ne \emptyset$. If $S_2 = \emptyset$, then $S \subseteq Y \subseteq X^+$, a contradiction. $S_1 \cup S_2 = X \cup Y \cup (S - Y) = S$ since $X \cup Y \subseteq S$. Since $X \cap Y = \emptyset$, $S_1 \cap S_2 = (X \cup Y) - Y = X$. $\square$

**Lemma 2 (Heath).** Let $s$ be a relation over $S$ that satisfies $X \to Y$, with $X \cap Y = \emptyset$ and $X \cup Y \subseteq S$. Then $s = \pi_{XY}(s) \bowtie \pi_{S - Y}(s)$.

*Proof.* Each $t \in s$ is in the join, since $t[XY] \in \pi_{XY}(s)$ and $t[S - Y] \in \pi_{S-Y}(s)$ agree on $X$. Conversely, let $t$ be in the join. Then there are $u, v \in s$ with $u[XY] = t[XY]$ and $v[S - Y] = t[S - Y]$. Both $u$ and $v$ agree with $t$ on $X$, which is in both sets, so $u[X] = v[X]$. By $X \to Y$, $u[Y] = v[Y] = t[Y]$. So $v$ agrees with $t$ on $(S - Y) \cup Y = S$, and $t = v \in s$. $\square$

**Termination.** By Lemma 1, each part pushed at line L8 is a proper nonempty subset of the part popped. So each part on a path from the root has at least one attribute fewer than its parent, and a path has at most $|R|$ parts. Each pop either ends a path (line L6) or replaces one part by two smaller ones. The parts form a binary tree of depth less than $|R|$, which has fewer than $2^{|R|}$ nodes, so the loop of line L2 runs fewer than $2^{|R|}$ times and stops.

**Invariant of line L2.** Call the parts in todo and done the *frontier*. Before each test of line L2: (I1) the union of the frontier is $R$, and (I2) for each legal $r$, $r$ is the join of $\pi_P(r)$ over the parts $P$ of the frontier, and (I3) each part in done is in BCNF under its projection of $F$.

- *Initialization.* The frontier is $\{R\}$, and $r = \pi_R(r)$.
- *Maintenance.* If line L4 finds no $X$, then $S$ moves to done. The frontier is the same, so (I1) and (I2) hold. For (I3): suppose $S$ is not in BCNF under $\pi_S(F)$. Then there are $X \subseteq S$ and $A \in S - X$ with $F \models X \to A$ and $S \not\subseteq X^+$. So $A \in (X^+ \cap S) - X$, and $X \ne S$ because $A \notin X$. Line L4 tries every proper subset of $S$, so it would have found $X$. Hence $S$ is in BCNF. If line L4 finds $X$, the frontier changes from $\ldots, S, \ldots$ to $\ldots, S_1, S_2, \ldots$ with $S_1 \cup S_2 = S$ by Lemma 1, so (I1) holds. For (I2): $\pi_S(r)$ satisfies $X \to Y$ because $F \models X \to Y$ (each $A \in Y$ is in $X^+$) and $X \cup Y \subseteq S$. By Lemma 2, $\pi_S(r) = \pi_{S_1}(\pi_S(r)) \bowtie \pi_{S_2}(\pi_S(r)) = \pi_{S_1}(r) \bowtie \pi_{S_2}(r)$. The natural join is associative and commutative, so replacing the factor $\pi_S(r)$ by this join keeps the value of the whole join. (I3) does not change.
- *End.* When the loop stops, todo is empty, and the frontier is done. (I1), (I2) and (I3) give (a), (c) and (b). $\blacksquare$

**Remark on the cost.** The proof of (I3) uses the fact that line L4 tries every proper subset of $S$. A test that tries fewer sets, such as the dependencies of $F$ alone, keeps (I1) and (I2) but can break (I3); the page gives an example.
