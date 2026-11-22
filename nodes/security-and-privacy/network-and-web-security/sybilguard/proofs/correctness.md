---
title: Correctness of SybilGuard
proves: [correctness]
status: full
---

Let $G$ be an undirected graph in which every node has degree at least 1. A directed edge $(p, x)$ is an edge $\{p, x\}$ used from $p$ to $x$. Every node $x$ has a permutation $\pi_x$ of its edges (line L1). For a directed edge $(p, x)$, define its successor $\sigma(p, x) = (x, y)$, where $\{x, y\} = \pi_x(\{p, x\})$. A route of $s$ along its edge to $t$ is the sequence of directed edges $e_1 = (s, t)$ and $e_{k+1} = \sigma(e_k)$; it crosses $e_k$ at hop $k$, and its witness list is the heads of $e_1, \ldots, e_w$.

**Lemma 1 (the successor is a bijection).** $\sigma$ is a bijection of the set of directed edges.

*Proof.* The set is finite, so it suffices that $\sigma$ is onto. Take $(x, y)$. Since $\pi_x$ is a permutation of the edges of $x$, there is exactly one edge $\{p, x\}$ with $\pi_x(\{p, x\}) = \{x, y\}$, and then $\sigma(p, x) = (x, y)$. $\square$

**Theorem 1 (back-traceability).** If every node is honest, then for each hop $i \in \{1, \ldots, w\}$ every directed edge is crossed at hop $i$ by exactly one route, and after the $w$ rounds of lines L2 to L4, entry $i$ of $R[p, x]$ is the start of that route. A route that crosses some directed edge twice repeats its first edge before any other edge.

*Proof.* A route is fixed by its first edge $e_1$, and it crosses $\sigma^{i-1}(e_1)$ at hop $i$. By Lemma 1, $\sigma^{i-1}$ is a bijection, so for each directed edge $e$ there is exactly one first edge $e_1 = \sigma^{-(i-1)}(e)$, and $e_1$ is the first edge of exactly one route, the route of its tail along it.

For the tables, show by induction on the round $k$ that after round $k$, for every $(p, x)$, $R[p, x]$ has $\min(k, w)$ entries and entry $i$ is the start of the route that crosses $(p, x)$ at hop $i$. Before round 1 all tables are empty. In round $k$, line L4 sets $R[p, x]$ to $p$ followed by the first $w - 1$ entries of $R[q, p]$ from round $k - 1$, where $\sigma(q, p) = (p, x)$. Entry 1 is $p$, the start of the route of $p$ along $(p, x)$, which is the route that crosses $(p, x)$ at hop 1. For $i \ge 2$, entry $i$ is entry $i - 1$ of $R[q, p]$, which by induction is the start of the route that crosses $(q, p)$ at hop $i - 1$. That route crosses $\sigma(q, p) = (p, x)$ at hop $i$, and by the first claim it is the only one. The length is $1 + \min(k - 1, w - 1) = \min(k, w)$.

For loops, let $e_k = e_j$ with $j < k$ be the first repetition, with $k$ smallest. If $j > 1$, then $\sigma(e_{j-1}) = e_j = e_k = \sigma(e_{k-1})$, so $e_{j-1} = e_{k-1}$ by Lemma 1, a repetition that ends before hop $k$. This contradicts the choice of $k$, so $j = 1$. $\square$

**Model of the adversary.** Let $H$ be the honest nodes and $A$ the set of $g$ attack edges, each written as a directed edge $(s, h)$ with $s \notin H$ and $h \in H$. Honest nodes run lines L1 to L4 and keep tables $R[p, x]$ for $x \in H$. Over each $(s, h) \in A$ the adversary sends a list $L_{s, h}$ of its choice, and $h$ stores its first $w$ entries as $R[s, h]$. The adversary also chooses the permutations of Sybil nodes, the tables on edges between Sybil nodes, and the witness lists of Sybil suspects, with full knowledge of the graph. It cannot send on an edge with an honest tail, since it does not hold the edge keys of honest pairs. We consider the stable state: the adversary has sent the same list over each attack edge in the last $w$ rounds.

**Lemma 2 (where Sybil names come from).** In the stable state, every entry of an honest table is an honest identity or a member of $L_{s, h}[1..w]$ for some $(s, h) \in A$. So the honest tables name at most $g w$ distinct Sybil identities, and at most $w(w + 1) / 2$ entries are copied from each attack edge.

*Proof.* Consider entry $i$ of $R[p, x]$ after the last round, with $x \in H$. If $p \notin H$, then $(p, x) \in A$ and the entry is in $L_{p, x}[1..w]$. Otherwise $p$ is honest and ran line L4: entry 1 is the honest $p$, and entry $i \ge 2$ is entry $i - 1$ of $R[q, p]$ from the round before, with $\sigma(q, p) = (p, x)$ and $p \in H$. Follow this chain backward. After at most $i - 1$ steps it stops either at entry 1 of a table on an edge with an honest tail, which is that honest tail, or at a table on an attack edge, from a round within the last $w$ rounds, whose content is $L_{s, h}[1..w]$ by stability. This proves the first claim. There are $g$ attack edges and each list contributes at most $w$ names.

For the count of entries, fix $(s, h) \in A$. An entry copied from $R[s, h]$ through $t$ steps of line L4 lies on the edge $\sigma^t(s, h)$, since each step moves from an edge to its successor, and it sits at position $i = j + t$, where $j \le w$ is its position in $R[s, h]$. So $t \le w - 1$, and the edge $\sigma^t(s, h)$ holds at most $w - t$ such entries, at positions $t + 1$ to $w$. The total is at most $\sum_{t=0}^{w-1} (w - t) = w(w + 1) / 2$. $\square$

**Theorem 2 (Sybil bound).** In the stable state, let $V$ be an honest verifier and suppose that fewer than half of the $\deg(V)$ routes of $V$ contain a node outside $H$. Then $V$ accepts no Sybil identity outside the at most $g w$ names of Lemma 2, whatever witness lists the suspect sends. So $V$ accepts at most $g w$ Sybil identities.

*Proof.* Let $b < \deg(V) / 2$ be the number of routes of $V$ that reach the Sybil region. If $V$ accepts $S$, line L9 gives at least $\deg(V) / 2 > b$ accepting routes, so some accepting route $r$ lies inside $H$. For $r$, line L8 found a node $X$ on $r$, so $X \in H$, with the key of $S$ in a registry table of $X$. That table is an honest table, so if $S$ is a Sybil identity, it is one of the at most $g w$ names of Lemma 2. The witness lists sent by $S$ only choose which node $X$ line L7 picks; they cannot change honest tables. $\square$

**Remark (changing lists).** If the adversary changes $L_{s, h}$ between rounds, the chain argument of Lemma 2 still shows that every Sybil entry comes from a list sent over an attack edge within the last $w$ rounds, but entries from different rounds can then hold different names, up to $w(w + 1) / 2$ per attack edge. After $w$ rounds without changes the stable state, and the bound $g w$, hold again.

**Cost.** Line L1 takes $O(\deg(x))$ time per node, $O(n + m)$ in total. Each round of lines L3 and L4 builds one list of at most $w$ entries for each of the at most $2m$ directed edges, after finding the predecessor edge with the inverse permutation, so a round takes $O(w m)$ time and the $w$ rounds take $O(w^2 m)$. The tables hold $O(w m)$ entries. Verification walks $\deg(V)$ routes of $w$ hops and makes one lookup per node, $O(\deg(V) w)$ expected time with a hash set of the claimed nodes. $\blacksquare$
