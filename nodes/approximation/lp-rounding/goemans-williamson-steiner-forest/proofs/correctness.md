---
title: The Goemans-Williamson forest is feasible and costs at most 2 - 2/k times a feasible dual
proves: [correctness]
status: full
---

**Setting.** The graph $G = (V, E)$ has costs $c_e \ge 0$ and pairs $(s_i, t_i)$ with $s_i \ne t_i$; the $k$ terminals are the vertices in some pair. For $S \subseteq V$, $\delta(S)$ is the set of edges with exactly one end in $S$. The set $S$ is *separating* if it holds exactly one vertex of some pair. The dual LP is $\max \sum_S y_S$ subject to $\sum_{S : e \in \delta(S)} y_S \le c_e$ for each edge $e$ and $y \ge 0$, with $y_S$ defined for the separating sets. The *load* of $e$ is $\ell_e(y) = \sum_{S : e \in \delta(S)} y_S$. Number the passes of the loop of line L2 as $1, 2, \ldots, r$. In pass $j$, let $\mathcal{C}_j$ be the components at its start, $\mathcal{A}_j \subseteq \mathcal{C}_j$ the active ones, $a_j = |\mathcal{A}_j|$, $\varepsilon_j$ the value of line L4 and $e_j$ the edge of line L6. Let $F = \{e_1, \ldots, e_r\}$ and let $F'$ be the output of line L9.

**Lemma 1 (invariants).** At the start of each pass $j$, and after the last pass:

1. the components are the vertex sets of the components of the graph $(V, \{e_1, \ldots, e_{j-1}\})$, and this graph is a forest;
2. each set $S$ with $y_S > 0$ was an active component at the start of some earlier pass; in particular it is separating, and it is contained in one current component;
3. $y$ is feasible for the dual LP;
4. each of $e_1, \ldots, e_{j-1}$ is tight.

*Proof.* At the start, the components are the singletons, there are no edges, and $y = 0$, so all four parts hold. Assume they hold at the start of pass $j$.

Line L5 raises $y_C$ only for the active components $C \in \mathcal{A}_j$, which are separating; this keeps part 2, and every set raised so far is a subset of a component of $\mathcal{C}_j$, so it stays inside one component after a merge. For an edge $e = uv$ with both ends in one component $D \in \mathcal{C}_j$, no raised set of pass $j$ holds exactly one of $u, v$, because each raised set is a component of $\mathcal{C}_j$ and either equals $D$ or misses it. So the load of $e$ does not change. For an edge $e = uv$ with ends in two different components $D_u \ne D_v$, the load grows by $\varepsilon_j \rho_e$, where $\rho_e \in \{0, 1, 2\}$ is the number of active components among $D_u$ and $D_v$. Line L3 computes $\tau_e = (c_e - \ell_e(y)) / \rho_e$ for each such edge with $\rho_e > 0$, and line L4 takes $\varepsilon_j = \min_e \tau_e \ge 0$; the minimum is nonnegative by part 3. So after line L5 each edge has $\ell_e(y) \le c_e$, which keeps part 3, and the edge $e_j$ that attains the minimum is tight. The edges $e_1, \ldots, e_{j-1}$ have both ends in one component, so their loads do not change, and they stay tight. This gives part 4.

Line L6 adds $e_j$, whose ends are in two different components, and merges them. Adding an edge between two different components of a forest keeps it a forest and merges exactly those two components, which keeps part 1. $\square$

**Lemma 2 (termination and feasibility).** If each pair is connected in $G$, the loop ends after at most $n - 1$ passes, and $F$ and $F'$ connect each pair.

*Proof.* Suppose some component $C$ is active. It separates a pair $(s, t)$ connected in $G$, so the $s$-$t$ path in $G$ has an edge $e \in \delta(C)$, whose other end is in another component, and $\rho_e \ge 1$ because $C$ is active. So line L4 finds an edge. Each pass merges two components, so by part 1 of Lemma 1 there are at most $n - 1$ passes. When the loop ends, no component is active, so no component separates a pair: each pair lies in one component, and by part 1 it is connected by $F$. Line L8 removes an edge only if the rest still connects every pair, so $F'$ connects every pair. $\square$

**Lemma 3 (minimality).** For each $e \in F'$, the set $F' - e$ does not connect every pair.

*Proof.* Let $F''$ be the set held by the loop of line L7 when it reaches $e$. Then $F' \subseteq F''$, because the loop only removes edges. The loop kept $e$, so $F'' - e$ does not connect every pair. Since $F' - e \subseteq F'' - e$, and a superset of a set that connects every pair also connects every pair, $F' - e$ does not connect every pair either. $\square$

**Lemma 4 (cost through the dual).** $c(F') = \sum_{j=1}^{r} \varepsilon_j \sum_{C \in \mathcal{A}_j} |F' \cap \delta(C)|$.

*Proof.* Each edge of $F' \subseteq F$ is tight by part 4 of Lemma 1, so

$$c(F') = \sum_{e \in F'} \sum_{S : e \in \delta(S)} y_S = \sum_S y_S \, |F' \cap \delta(S)|.$$

The final $y_S$ is the sum of $\varepsilon_j$ over the passes $j$ with $S \in \mathcal{A}_j$. Putting this in and exchanging the sums gives the claim. $\square$

**Lemma 5 (the key bound).** For each pass $j$, $\sum_{C \in \mathcal{A}_j} |F' \cap \delta(C)| \le 2a_j - 2$.

*Proof.* Build a multigraph $H$ with one node for each component of $\mathcal{C}_j$ and one edge for each $e \in F'$ whose ends lie in two different components of $\mathcal{C}_j$, joining those two nodes. An edge of $F'$ with both ends in one component $D \in \mathcal{C}_j$ is in $\delta(C)$ for no $C \in \mathcal{C}_j$. So for each $C \in \mathcal{C}_j$, the degree of $C$ in $H$ is $\deg_H(C) = |F' \cap \delta(C)|$.

*$H$ is a forest.* By part 1 of Lemma 1, each component of $\mathcal{C}_j$ is spanned by a tree of edges among $e_1, \ldots, e_{j-1}$. Contracting each of these trees in the forest $(V, F)$ gives a forest, because contracting a connected subgraph of a forest gives a forest. The edges of $H$ are a subset of the edges of this contracted forest, so $H$ is a forest.

*No inactive node is a leaf.* Let $C \in \mathcal{C}_j \setminus \mathcal{A}_j$, so $C$ separates no pair, and suppose $\deg_H(C) = 1$, with the single edge $e \in F' \cap \delta(C)$. By Lemma 3 there is a pair $(s, t)$ such that the $s$-$t$ path $P$ in the forest $(V, F')$ uses $e$. Walk along $P$ from $s$ to $t$. Each edge of $P$ in $\delta(C)$ moves the walk from $C$ to $V \setminus C$ or back, and no other edge does. Since $C$ does not separate $(s, t)$, the walk starts and ends on the same side, so $P$ has an even number of edges in $\delta(C)$. It has at least one, the edge $e$, so it has at least two distinct ones, and both are in $F' \cap \delta(C)$. This contradicts $\deg_H(C) = 1$.

*Counting.* Let $H'$ be $H$ without its isolated nodes, with node set $N'$ and edge set $E'$, and let $A' = N' \cap \mathcal{A}_j$ and $I' = N' \setminus A'$. If $E'$ is empty, the sum in the lemma is $0 \le 2a_j - 2$, since $a_j \ge 1$ in each pass. Otherwise $H'$ is a nonempty forest, so $|E'| \le |N'| - 1$. Each node of $I'$ has degree at least 2 in $H'$, since it is not isolated and not a leaf. So

$$\sum_{C \in \mathcal{A}_j} \deg_H(C) = \sum_{C \in A'} \deg_{H'}(C) = 2|E'| - \sum_{C \in I'} \deg_{H'}(C) \le 2(|N'| - 1) - 2|I'| = 2|A'| - 2 \le 2a_j - 2. \qquad \square$$

**Theorem.** If each pair is connected in $G$, then $F'$ connects each pair, $y$ is feasible for the dual LP, and

$$c(F') \le \Big(2 - \frac{2}{k}\Big) \sum_S y_S \le \Big(2 - \frac{2}{k}\Big) \cdot \text{OPT}.$$

*Proof.* Feasibility of $F'$ is Lemma 2, and feasibility of $y$ is part 3 of Lemma 1. The active components of one pass are disjoint, and each holds a terminal of a pair that it separates, so $1 \le a_j \le k$, and $2a_j - 2 = a_j (2 - 2/a_j) \le a_j (2 - 2/k)$. By Lemmas 4 and 5, and with $\varepsilon_j \ge 0$,

$$c(F') \le \sum_j \varepsilon_j (2a_j - 2) \le \Big(2 - \frac{2}{k}\Big) \sum_j \varepsilon_j a_j = \Big(2 - \frac{2}{k}\Big) \sum_S y_S,$$

where the last step holds because pass $j$ adds $\varepsilon_j$ to each of the $a_j$ active sets, and these additions make up all of $y$. By weak duality, $\sum_S y_S$ is at most the LP optimum. The incidence vector of an optimal forest meets each separating cut, so it is feasible for the LP, and the LP optimum is at most OPT. $\blacksquare$

**Remark.** The proof uses line L7 only through Lemma 3, that each output edge is needed. So for Steiner forest each order of deletion that ends with a minimal subset of $F$ gives the same bound.
