---
title: With a perfect oracle for the d-separations among the observed nodes of a DAG with latent nodes and no selection, FCI stops, keeps every edge of the MAG, and every mark that the collider steps and the rules R1 to R3 set is shared by all MAGs of the class
proves: [correctness, termination]
status: partial
---

**What is proved and what is cited.** This file proves termination, that no edge of the true MAG is removed, that every removed pair has a true separating set, that the collider steps put arrowheads only where all MAGs of the class have them, and that R1, R2 and R3 are sound. Four results are cited and not proved here: the properties of the MAG of a DAG (Richardson and Spirtes 2002), that the Possible-D-SEP phase removes every edge that is not in the MAG (Spirtes, Meek and Richardson 1995; Spirtes, Glymour and Scheines 2000), the soundness of R4 and R8 to R10, and the completeness of R1 to R4 with R8 to R10 when there is no selection (Zhang 2008). The tests check the full claim, including completeness, on every MAG with three or four nodes.

**Setting.** $G$ is a DAG on $V \cup L$, where $V$ is the finite set of observed nodes and $L$ the latent nodes. There is no selection. The oracle answers $\mathrm{CI}(a, b, S)$ for $a, b \in V$ and $S \subseteq V \setminus \{a, b\}$ with the truth of $(a \perp b \mid S)_G$, the d-separation in $G$. This is what a perfect test gives under the causal Markov condition and faithfulness.

The MAG $M$ of $G$ over $V$ has an edge between $a$ and $b$ exactly when no $S \subseteq V \setminus \{a, b\}$ d-separates them in $G$. The edge is $a \to b$ if $a$ is an ancestor of $b$ in $G$, $a \leftarrow b$ if $b$ is an ancestor of $a$, and $a \leftrightarrow b$ otherwise. We cite from Richardson and Spirtes (2002) that $M$ is ancestral (no directed cycle, and no $a \leftrightarrow b$ with $a$ an ancestor of $b$) and that m-separation in $M$ equals d-separation in $G$ for sets of observed nodes. Two MAGs are Markov equivalent when they have the same m-separations. The class of $M$ is the set of MAGs Markov equivalent to $M$. A MAG here has only the edges $\to$ and $\leftrightarrow$, since there is no selection.

**Lemma 1 (meaning of a mark).** In a MAG without undirected edges, the edge between $a$ and $c$ has a tail at $c$ exactly when $c$ is an ancestor of $a$ in the MAG, and an arrowhead at $c$ exactly when $c$ is not an ancestor of $a$.

*Proof.* If the edge is $c \to a$, then $c$ is an ancestor of $a$. If it is $a \to c$, then $c$ is not an ancestor of $a$, or there would be a directed cycle. If it is $a \leftrightarrow c$, then $c$ is not an ancestor of $a$ by the ancestral property. These are the only edges. $\square$

**Lemma 2 (termination and the skeleton phase).** Lines L1 to L6 stop. No edge of $M$ is removed, and every removed pair $\{a, b\}$ has $\mathrm{sepset}(a, b) = S$ with $(a \perp b \mid S)_G$.

*Proof.* Lines L1 and L4 to L6 make finitely many tests: each level of line L1 tests subsets of a finite set, the level grows by one each round, and it stops when it passes the largest degree; lines L4 to L6 test the subsets of finite sets once. An edge is removed only when the oracle reports a separation, and that separation is then true and recorded. If $a$ and $b$ are adjacent in $M$, then by definition no subset of $V \setminus \{a, b\}$ separates them, so the oracle never reports one, and the edge stays. $\square$

So the final skeleton contains the skeleton of $M$. The converse, that every pair not adjacent in $M$ is removed, is the cited Possible-D-SEP theorem: some separating set of the pair lies inside $\mathrm{PDS}(a) \setminus \{b\}$ or $\mathrm{PDS}(b) \setminus \{a\}$, computed on the graph after line L3, and lines L4 to L6 test all subsets of both. The rest of this file assumes that the final skeleton is the skeleton of $M$.

**Lemma 3 (unshielded triples).** Let $M'$ be a MAG in the class of $M$, and let $a$ and $b$ be non-adjacent with a common neighbour $c$. Let $S$ be any set that m-separates $a$ and $b$ in $M'$. Then $c$ is a collider on $a, c, b$ in $M'$ exactly when $c \notin S$. So all MAGs of the class have the same skeleton and the same unshielded colliders.

*Proof.* The path $a, c, b$ has only the inner node $c$. If $c$ is a collider and $c \in S$, the path is open, since a collider in $S$ is in $S$ and so in its ancestor set. If $c$ is not a collider and $c \notin S$, the path is also open. Either case contradicts the separation. So $c$ is a collider exactly when $c \notin S$. For the second claim, two nodes are adjacent in a MAG exactly when no set m-separates them: an edge is an open path given every set, and maximality gives the converse. So equivalent MAGs have the same skeleton. Any separating set $S$ of a non-adjacent pair is a separating set in every MAG of the class, so the first claim gives the same colliders in all of them. $\square$

**Lemma 4 (collider steps).** After line L8, the arrowheads are exactly the arrowheads at the middle nodes of the unshielded colliders of $M$, and every MAG of the class has them.

*Proof.* Line L8 puts arrowheads at $c$ on both edges of an unshielded triple $a, c, b$ exactly when $c \notin \mathrm{sepset}(a, b)$. By Lemma 2 the recorded set m-separates $a$ and $b$ in $M$, so by Lemma 3 this holds exactly when $c$ is a collider in $M$, and then in every MAG of the class. $\square$

The rules keep this invariant: every arrowhead and every tail of the current graph is in every MAG of the class. Call such a graph sound. A circle at an end does not claim anything. We now show that R1 to R3 map a sound graph to a sound graph. In each case $M'$ is any MAG of the class; by soundness, it has every non-circle mark of the current graph.

**Lemma 5 (R1).** If $a \mathrel{*\!\!\to} b \mathrel{\circ\!\!-\!\!*} c$ and $a$, $c$ are not adjacent, then every MAG of the class has $b \to c$.

*Proof.* The triple $a, b, c$ is unshielded. It is not a collider in $M$: if it were, line L8 would have put an arrowhead at $b$ on the edge from $c$, and later rules never turn a mark into a circle, but the mark is a circle. By Lemma 3, $b$ is not a collider in $M'$ either. $M'$ has the arrowhead at $b$ from $a$, so the edge between $b$ and $c$ has a tail at $b$. A MAG without undirected edges then has $b \to c$. $\square$

**Lemma 6 (R2).** If $a \to b \mathrel{*\!\!\to} c$ or $a \mathrel{*\!\!\to} b \to c$, and $a$ and $c$ are adjacent, then every MAG of the class has an arrowhead at $c$ on the edge between $a$ and $c$.

*Proof.* By Lemma 1 it is enough to show that $c$ is not an ancestor of $a$ in $M'$. In the first case, $a$ is an ancestor of $b$. If $c$ were an ancestor of $a$, it would be an ancestor of $b$, but the arrowhead at $c$ on the edge from $b$ says it is not. In the second case, $b$ is an ancestor of $c$. If $c$ were an ancestor of $a$, then $b$ would be an ancestor of $a$, but the arrowhead at $b$ on the edge from $a$ says it is not. $\square$

**Lemma 7 (R3).** If $a \mathrel{*\!\!\to} b \mathrel{\leftarrow\!\!*} c$, $a \mathrel{*\!\!-\!\!\circ} d \mathrel{\circ\!\!-\!\!*} c$, $a$ and $c$ are not adjacent, and $d$ is adjacent to $b$, then every MAG of the class has an arrowhead at $b$ on the edge between $d$ and $b$.

*Proof.* The triple $a, d, c$ is unshielded with circles at $d$, so as in Lemma 5 it is not a collider in $M'$. So one of its two edges has a tail at $d$, say $d \to a$; the case $d \to c$ is the same. Suppose $b$ were an ancestor of $d$. Then $b$ would be an ancestor of $a$, but the arrowhead at $b$ on the edge from $a$ says it is not. So $b$ is not an ancestor of $d$, and Lemma 1 gives the arrowhead. $\square$

**Lemma 8 (termination of the rules).** If every rule application keeps the graph sound, the loop of lines L9 to L12 stops after at most $2|E|$ applications, where $|E|$ is the number of edges.

*Proof.* Each rule in the implementation fires only on a circle and replaces it by an arrowhead or a tail. No step creates a circle. In a sound graph, a mark that is set already has the value of every MAG of the class, so a later rule that sets it again gives the same value. So each application lowers the number of circles by at least one, and there are $2|E|$ ends. $\square$

**Theorem.** With the oracle above, FCI stops. Its skeleton contains the skeleton of $M$, and every removed pair has a true separating set. If the final skeleton is that of $M$ (cited), then after line L8 and after every application of R1, R2 or R3 the graph is sound: every arrowhead and tail is in every MAG of the class.

*Proof.* Lemma 2 gives termination of lines L1 to L8 and the claims about the skeleton. Lemma 4 gives soundness after line L8. Lemmas 5 to 7 show that R1 to R3 keep soundness. With the cited soundness of R4 and R8 to R10, Lemma 8 gives termination of the rules. $\square$

**Cited results.** Zhang (2008) proved that R4 and R8 to R10 are sound and that R1 to R4 with R8 to R10, applied until none applies to the correct skeleton with the correct unshielded colliders, leave a circle exactly at the ends where two MAGs of the class differ, when there is no selection. Together with the theorem above, this makes the output the PAG of the class. The test file checks this full claim against the PAG of every class of MAGs on three and four nodes (56 and 2492 MAGs), on all 543 DAGs on four nodes, on 300 random DAGs with latent nodes, and checks soundness on larger graphs.
