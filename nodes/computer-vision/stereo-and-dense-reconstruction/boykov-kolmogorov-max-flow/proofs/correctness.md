---
title: Correctness of the Boykov-Kolmogorov max-flow algorithm
proves: [correctness]
status: full
---

We prove that BK-MAX-FLOW, with integer capacities, stops after at most $|C|$ augmentations, where $|C|$ is the capacity of a minimum cut, and that it returns a maximum flow $f$ and a minimum cut whose source side is the final S tree. Write $r(u \to v)$ for the residual capacity of the stored edge from $u$ to $v$. A node is active when it is in the queue $A$, and passive when it is in a tree and not in $A$.

## Invariants

Between two lines of the main loop the following hold.

1. **Flow.** The stored capacities are the residual capacities of a feasible flow $f$ of value $\textit{flow}$.
2. **Tree edges.** If $\textit{parent}[q]$ is an edge $p \to q$ of an S node $q$, then $\textit{tree}[p] = S$ and $r(p \to q) > 0$. If it is an edge $q \to p$ of a T node $q$, then $\textit{tree}[p] = T$ and $r(q \to p) > 0$. Outside the adoption stage no node has the parent NONE, and the parent edges lead from each S node to $s$ and from each T node to $t$ without a cycle.
3. **Passive nodes.** If $p$ is a passive S node and $r(p \to q) > 0$, then $\textit{tree}[q] = S$. If $p$ is a passive T node and $r(q \to p) > 0$, then $\textit{tree}[q] = T$.

At the start only $s$ and $t$ are in trees and both are active, so all three hold.

**Growth (lines L12 to L18).** Line L15 gives a free node $q$ the tree of $p$ and the edge between them, which has positive residual capacity in the right direction by the test of line L14; $q$ becomes active, and its parent chain is the edge to $p$ followed by the chain of $p$. So invariant 2 holds. A node leaves $A$ at line L17 only after all its edges were scanned and every neighbor $q$ with a residual edge in the right direction was either put in the same tree or found in the other tree; the second case returns at line L16 before line L17, so at line L17 every such $q$ is in the same tree. Residual capacities do not change during growth, so invariant 3 holds for $p$.

**Augmentation (lines L6 to L10).** Line L16 returns an edge $a \to c$ with $\textit{tree}[a] = S$, $\textit{tree}[c] = T$ and $r(a \to c) > 0$. By invariant 2 the parent chains give a path from $s$ to $a$ and from $c$ to $t$ of edges with positive residual capacity, so line L6 builds an augmenting path $P$ and $\Delta > 0$. Pushing $\Delta$ along $P$ keeps capacity and conservation, so invariant 1 holds with the value increased by $\Delta$. Residual capacities change only on $P$ and on the reverse edges of $P$. An edge of $P$ that becomes saturated is a tree edge or the bridge. Lines L9 and L10 cut the saturated tree edges and make their children orphans, so the remaining tree edges still have positive residual capacity. For invariant 3: a reverse edge $v \to u$ of an edge $u \to v$ of $P$ gains capacity. If $u \to v$ is in the S part, then both ends are in S, and the new residual edge joins two S nodes, which invariant 3 allows. The same holds in the T part. For the bridge $a \to c$, the new residual edge is $c \to a$. It leaves the T node $c$ and enters the S node $a$, and invariant 3 says nothing about the edges out of a T node or into an S node.

**Adoption (lines L19 to L24).** An orphan $p$ is given a new parent $q$ at line L20 only if $q$ is in the same tree, the edge between them has positive residual capacity in the right direction, and the chain of $q$ reaches a terminal. That chain does not pass through $p$, because $p$ has the parent NONE, so no cycle forms and invariant 2 holds for $p$. If no such $q$ exists, $p$ becomes free at line L24. Before that, line L22 makes active each node $q$ of the same tree with a residual edge toward $p$ (for S) or from $p$ (for T). These are exactly the passive nodes for which invariant 3 would fail when $p$ leaves the tree. Line L23 makes the children of $p$ orphans, because their chain went through $p$. When the orphan set is empty, every node in a tree has a chain to a terminal again, and invariants 2 and 3 hold.

## The final state is a minimum cut

The loop stops at line L5 when growth finds no bridge and $A$ is empty. Then every node of the S tree is passive, so by invariant 3 every residual edge out of an S node goes to an S node. Let $S$ be the set of S nodes. It contains $s$, and it does not contain $t$, because $t$ is always in T. No residual edge leaves $S$. So every edge from $S$ to the rest carries flow equal to its capacity, and every edge into $S$ carries no flow, because a positive flow on $v \to u$ with $u \in S$ would give the residual edge $u \to v$. The value of $f$ is the net flow across the cut, so it equals the capacity of the cut $S$. By weak duality every flow is at most every cut, so $f$ is a maximum flow and $S$ is a minimum cut, which is the [max-flow min-cut theorem](/max-flow-min-cut-theorem/). The returned source side is $S$.

## Termination

With integer capacities each $\Delta$ is a positive integer, and the value of a flow is at most $|C|$, so there are at most $|C|$ augmentations. Between two augmentations, the work is finite and bounded as follows.

- **Growth.** No node leaves a tree during growth, so a free node joins a tree at most once and enters $A$ at most once. Each node in $A$ is scanned once and then removed at line L17, except the node at which a bridge is found, which stays at the front. So one growth stage scans each edge $O(1)$ times, in $O(n + m)$ time.
- **Adoption.** A node with a chain to a terminal keeps it for the rest of the adoption stage: a node gets the parent NONE only when its parent becomes free, and only an orphan becomes free. So a node is an orphan at most once in each adoption stage. Processing an orphan $p$ scans its edges twice and follows a chain of at most $n$ nodes for each candidate parent, in $O(n \deg p)$ time, and the sum over all nodes is $O(m n)$.

So the time between two augmentations is $O(m n)$, and the total time is $O(m n |C|)$. Boykov and Kolmogorov state the bound $O(m n^2 |C|)$; the count above is a little finer for this version, and neither bound is polynomial in the input size. $\square$
