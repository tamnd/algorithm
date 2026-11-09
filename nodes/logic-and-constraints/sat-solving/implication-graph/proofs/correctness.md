---
title: The implication graph is acyclic with the trail as a topological order, and the backward scan finds exactly the unique implication points
proves: [correctness]
status: full
---

We use the operations of the page. The nodes are the literals on the trail, plus the conflict node $\kappa$ while it exists. For a node $v$, $\mathrm{pos}(v)$ is its index on the trail, $\mathrm{lev}(v)$ is its decision level, and $\delta_i$ is the decision of level $i$. We set $\mathrm{pos}(\kappa) = \infty$.

## The shape of the graph

**Lemma 1.** After each operation: (a) every edge $w \to v$ between literal nodes has $\mathrm{pos}(w) < \mathrm{pos}(v)$ and $\mathrm{lev}(w) \le \mathrm{lev}(v)$; (b) the levels are non-decreasing along the trail, and $\delta_i$ is the first node of level $i$; (c) the graph is acyclic, and the trail followed by $\kappa$ is a topological order.

*Proof.* DECIDE appends a node with no in-edges and the new largest level. IMPLY appends a node whose predecessors are the negations of false literals, so they are nodes already on the trail, with smaller positions and levels at most the current level, which is the level of the new node. CONFLICT adds edges into $\kappa$ only. BACKJUMP removes a suffix of the trail, all nodes of the removed levels, and their edges, so (a) and (b) still hold for the rest. Part (c) follows from (a): every edge goes forward on the trail or into $\kappa$. $\square$

**Lemma 2.** Suppose IMPLY is called only on a clause that has become unit at the current level, that is, at least one of its other literals became false at the current level, or the clause is a learned clause that is asserted right after a backjump to the second highest level of its literals. Then for every level $i \ge 1$, every node of level $i$ is reachable from $\delta_i$ by a path of level-$i$ nodes.

*Proof.* Take a node $v \ne \delta_i$ of level $i \ge 1$. In both cases of the hypothesis, $v$ has a predecessor of level $i$: in the first case the literal that became false at level $i$, and in the second case a literal of the second highest level, which is $i$. That predecessor has a smaller position, by Lemma 1(a). By induction on the position, it is reachable from $\delta_i$ through level-$i$ nodes, and so is $v$. $\square$

The CDCL loop meets this hypothesis, because it decides only after propagation is complete, so every clause it uses as a reason at level $i$ was not unit at the end of level $i - 1$.

## Unique implication points

Let $\kappa$ exist, and let $d \ge 1$ be the largest level of its predecessors. A node $u$ of level $d$ is a *unique implication point* (UIP) if every path from $\delta_d$ to $\kappa$ passes through $u$. Paths from $\delta_d$ never leave level $d$: along an edge the level does not decrease (Lemma 1(a)), and no node of a level above $d$ has a path to $\kappa$ when the conflict comes from propagation at level $d$. In what follows we use only the nodes of level $d$ and $\kappa$. Let $t_1 = \delta_d, t_2, \ldots, t_r$ be the nodes of level $d$ in trail order.

UIPS keeps a set $S$ of marked nodes and the count $c$ of marked nodes that the scan has not reached yet. Line L8 marks the level-$d$ predecessors of $\kappa$. The loop of line L9 visits $t_r, t_{r-1}, \ldots, t_1$. When it visits a marked node $v$, line L11 records $v$ if $c = 1$, line L12 decrements $c$, and line L13 marks the unmarked level-$d$ predecessors of $v$.

**Lemma 3.** When the scan is about to visit $t_i$, a node $t_j$ is marked if and only if $t_j$ has an edge to $\kappa$ or to a marked node $t_l$ with $l > i$. Every node $t_l$ with $l > i$ that has a path to $\kappa$ is marked.

*Proof.* The first claim is what lines L8 and L13 do, since a node is visited only once and the predecessors of $t_l$ have positions less than $l$. For the second, use induction on $l$ from $r$ down. A node $t_l$ with a path to $\kappa$ has a successor $s$ on that path, which is $\kappa$ or a node $t_{l'}$ with $l' > l$ and a path to $\kappa$. In the first case line L8 marked $t_l$. In the second case $t_{l'}$ is marked by induction, and line L13 marked $t_l$ when the scan visited $t_{l'}$, which is before it reaches $t_i$ because $l' > l > i$. $\square$

So at the visit of $t_i$, the count $c$ is the number of marked nodes among $t_1, \ldots, t_i$.

**Theorem.** Assume the hypothesis of Lemma 2. A node $u = t_i$ is recorded by UIPS if and only if $u$ is a UIP. So UIPS returns all UIPs of level $d$, in decreasing trail order, and the first one is the UIP closest to $\kappa$. The decision $\delta_d$ is always the last one.

*Proof.* Some predecessor of $\kappa$ has level $d$, and by Lemma 2 it is reachable from $\delta_d$, so a path from $\delta_d$ to $\kappa$ exists.

(If.) Let $u = t_i$ be marked with $c = 1$ at its visit, so $u$ is the only marked node among $t_1, \ldots, t_i$. Take a path $\delta_d = p_0, p_1, \ldots, p_s = \kappa$. Let $p_a$ be the last node of the path with position at most $\mathrm{pos}(u)$. It exists because $p_0 = t_1$. Its successor $p_{a+1}$ is $\kappa$ or a node after $u$ with a path to $\kappa$, which is marked by Lemma 3. So $p_a$ is marked by Lemma 3, and it is among $t_1, \ldots, t_i$. Hence $p_a = u$, and the path passes through $u$.

(Only if.) Let $u = t_i$ be a UIP. A path from $\delta_d$ to $\kappa$ passes through $u$, so $u$ has a path to $\kappa$, and its successor on it is $\kappa$ or a later node with a path to $\kappa$. By Lemma 3, $u$ is marked at its visit. Suppose some other node $w = t_j$ with $j < i$ is marked at that time. By Lemma 3, $w$ has an edge to $\kappa$ or to a marked node $t_l$ with $l > i$, and from $t_l$ there is a path to $\kappa$ through nodes of positions greater than $l$. By Lemma 2, $w$ is reachable from $\delta_d$ through nodes of positions at most $j$, by Lemma 1(a). Joining the two parts gives a path from $\delta_d$ to $\kappa$ whose nodes have positions at most $j < i$ or greater than $i$, so it avoids $u$. This contradicts that $u$ is a UIP. So $c = 1$ at the visit of $u$, and $u$ is recorded.

When the scan reaches $\delta_d = t_1$, it is marked, because it has a path to $\kappa$, and it is the only node left, so $c = 1$ and it is recorded. $\blacksquare$

## The first UIP clause

FIRST-UIP-CLAUSE runs the same scan and stops at the first recorded node $u$. Let $A$ be the set of nodes visited while marked before $u$, together with $\kappa$. The clause is $\{\neg u\}$ together with $\neg w$ for each node $w$ of a level from 1 to $d - 1$ with an edge into $A$. All these literals are false, because their negations are nodes. The only literal of level $d$ is $\neg u$: every level-$d$ predecessor of a node of $A$ was marked, and at the stop, $u$ is the only marked node not in $A$. So the clause has exactly one literal of level $d$, and the backjump level returned is the largest level among the other literals. That the clause is implied by the formula is proved on the [clause learning](/clause-learning/) and [CDCL](/cdcl/) pages, where the same set of literals is built by resolution. $\blacksquare$
