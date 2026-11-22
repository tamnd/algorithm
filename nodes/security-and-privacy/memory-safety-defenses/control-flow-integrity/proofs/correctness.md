---
title: Label-based CFI accepts exactly the targets in the component of the site, and no labeling with one label per target does better
proves: [correctness, invariant, termination]
status: full
---

**The model.** The allowed graph gives, for each indirect branch site $s$ of a set $S$, a finite set $T(s)$ of allowed targets. Let $G$ be the bipartite graph with a node for each site and each target that appears in some $T(s)$, and an edge $\{s, t\}$ for each $t \in T(s)$. For a site $s$, let $T^*(s)$ be the set of targets in the connected component of $s$ in $G$. A run of the program is a sequence of transfers $(s, x)$, where $x$ is the target that the branch at $s$ computes at run time, from data that an attacker may control.

**Assumptions.** These are the model forms of the assumptions of Abadi et al. (A1) Non-writable code: after lines L1 to L5 run, nothing in the run changes the label of a target or the expected label of a site. (A2) Complete mediation: every indirect transfer of the run goes through CHECK at lines L6 and L7. (A3) Unique labels: a place that is not a target of $G$ carries no label, so it never matches; in machine code this is the requirement that the bit pattern of a label appears nowhere else in the code, and that data cannot run.

**Invariant of lines L1 to L3 (U).** After each union of line L2, two nodes have the same union-find root if and only if they are connected in the subgraph of $G$ formed by the edges added so far.

*Proof of (U), by induction on the number of edges added.* Before any edge, each node is its own root and is connected only to itself. Adding the edge $\{s, t\}$ joins the classes of $s$ and $t$ into one, which is exactly what the edge does to the connected components: two nodes are connected after the edge if and only if they were connected before, or one was connected to $s$ and the other to $t$. Path halving and union by size change the shape of the trees but not the sets they hold. $\square$

**Lemma (labels).** After lines L3 to L5, a target $t$ and a site $s$ have the same label if and only if $t \in T^*(s)$.

*Proof.* When the loop of line L2 ends, every edge of $G$ has been added, so by (U) two nodes have the same root if and only if they are in the same component of $G$. Line L3 gives one fresh integer to each root, the same one each time the root comes up, so two nodes have the same label if and only if they have the same root. Lines L4 and L5 store these labels for targets and sites. $\square$

**Theorem (correctness of CHECK).** Under (A1), (A2) and (A3), a transfer $(s, x)$ passes line L6 if and only if $x \in T^*(s)$. So every transfer of the run that reaches line L7 goes to a target in $T^*(s)$.

*Proof.* By (A1) the labels at the time of the transfer are those of the lemma. If $x$ is a target of $G$, it passes line L6 exactly when its label equals the label of $s$, which by the lemma is exactly when $x \in T^*(s)$. If $x$ is not a target of $G$, it carries no label by (A3), so it fails line L6, and indeed $x \notin T^*(s)$. If $s$ is not a site of the graph, line L6 fails for every $x$. By (A2) no transfer skips the check. $\square$

**Corollary 1 (no false alarm).** $T(s) \subseteq T^*(s)$, since each $t \in T(s)$ is joined to $s$ by an edge. So a run that follows the allowed graph never faults.

**Corollary 2 (precision when sets do not overlap partly).** If for every two sites $s$ and $s'$ the sets $T(s)$ and $T(s')$ are equal or disjoint, then $T^*(s) = T(s)$ for every site $s$.

*Proof.* If $T(s)$ is empty, $s$ is alone in its component, and $T^*(s) = \emptyset$. Otherwise, take a path in $G$ from $s$ to any node of its component. It alternates sites and targets: $s = s_0, t_1, s_1, t_2, s_2, \ldots$. Each target $t_i$ lies in both $T(s_{i-1})$ and $T(s_i)$, so these sets are not disjoint, hence equal. By induction along the path, every site on it has the set $T(s)$, and every target on it is in $T(s)$. So the targets of the component are exactly $T(s)$. $\square$

**Theorem (optimality).** Let $\lambda$ be any labeling that gives one label to each target and one expected label to each site, accepts a transfer $(s, x)$ exactly when $\lambda(x) = \lambda(s)$, and accepts every allowed edge. Then $\lambda$ accepts every edge $(s, x)$ with $x \in T^*(s)$. So no labeling of this form is more precise than the one of lines L1 to L5.

*Proof.* For every edge $\{s, t\}$ of $G$, $\lambda$ accepts $(s, t)$, so $\lambda(s) = \lambda(t)$. So $\lambda$ is constant along every path of $G$, hence on every component. For $x \in T^*(s)$, $x$ and $s$ are in one component, so $\lambda(x) = \lambda(s)$, and $(s, x)$ is accepted. $\square$

The optimality theorem is the formal reason that one label per target loses precision when allowed sets overlap without being equal: the effective set of a site grows to its whole component. Avoiding the loss needs more than one label per target, a different check, or a duplicate of the target code.

**What the theorems do not say.** They are statements about the transfers the graph covers, and only under (A1) to (A3). They do not say that $T(s)$ itself is small; that depends on the analysis that built the graph. They do not say which element of $T^*(s)$ a transfer goes to, so an attacker who controls the target data can still choose among them; [control-flow bending](/control-flow-bending/) shows how much that leaves. For returns, $T(s)$ is the set of all call sites of the function, so a [shadow stack](/shadow-stack/) is needed to require the matching one.

**Termination and cost.** Lines L1 to L5 run a fixed number of loops over the $V$ nodes and $E$ edges of $G$; with path halving and union by size, the union-find operations cost $O(\alpha(V))$ amortized each, so the build takes $O((V + E)\,\alpha(V))$ steps. Line L6 does two lookups, $O(1)$ expected time with hash tables. Every loop is over a finite set, so the build ends, and each check ends after a fixed number of steps. $\blacksquare$
