---
title: Component growing labels each component and builds a spanning forest
proves: [correctness]
status: full
---

Let $G = (V, E)$ be an undirected graph with the lists $\mathrm{Adj}[v]$, where an edge $\{u, v\}$ with $u \neq v$ is in both lists. Parallel edges and loops are allowed. Write $C(s)$ for the set of vertices joined to $s$ by a path, and $L_k = \{ v : \mathrm{comp}[v] = k \}$.

**Lemma 1.** Consider a call GROW$(G, s, k)$ that starts with $\mathrm{comp}[s] = \mathrm{nil}$ and with no vertex labelled $k$. After each step of the loop of line L3 these invariants hold:

> **(I1)** Every $v \in L_k$ is in $C(s)$, and following parent pointers from $v$ reaches $s$ through vertices of $L_k$.
>
> **(I2)** For each $u \in L_k$, the entries $\mathrm{Adj}[u][0 \ldots \mathrm{next}[u] - 1]$ all lead to vertices of $L_k$.
>
> **(I3)** Each $u \in L_k \setminus F$ has $\mathrm{next}[u] = |\mathrm{Adj}[u]|$, and $F \subseteq L_k$.

*Proof.* After lines L1 and L2, $L_k = F = \{s\}$ and $\mathrm{next}[s] = 0$, so all three hold. Take a step with the vertex $u \in F$ of line L4.

If line L5 removes $u$, then $\mathrm{next}[u] = |\mathrm{Adj}[u]|$, so (I3) holds for $u$, and nothing else changes.

Otherwise line L6 reads $v = \mathrm{Adj}[u][\mathrm{next}[u]]$ and moves the pointer by one. If $\mathrm{comp}[v] = k$, the new entry leads into $L_k$ and (I2) holds. The label of $v$ cannot be a smaller value $k' < k$: by Lemma 2 applied to the earlier call, $L_{k'}$ is a full component, $u \notin L_{k'}$, and $v$ is a neighbour of $u$, so $v \notin L_{k'}$. If $\mathrm{comp}[v] = \mathrm{nil}$, line L8 puts $v$ into $L_k$ and into $F$ with $\mathrm{next}[v] = 0$ and $\mathrm{parent}[v] = u$. Then $v \in C(s)$ because $u \in C(s)$ and $\{u, v\}$ is an edge, and the parent chain of $v$ is $v$ followed by the chain of $u$, so (I1) holds. The entry just read leads to $v \in L_k$, so (I2) holds, and $v \in F$, so (I3) holds. $\square$

**Lemma 2.** The call stops, and then $L_k = C(s)$.

*Proof.* Each step either moves a pointer forward or removes a vertex from $F$. A pointer moves at most $|\mathrm{Adj}[u]|$ times, a vertex enters $F$ only once (when it gets its label), and so the loop runs at most $\sum_u |\mathrm{Adj}[u]| + |V|$ times.

When $F = \emptyset$, (I3) gives $\mathrm{next}[u] = |\mathrm{Adj}[u]|$ for each $u \in L_k$, and (I2) then says that every neighbour of every vertex of $L_k$ is in $L_k$. Let $w \in C(s)$ and let $s = x_0, x_1, \ldots, x_r = w$ be a path. Since $x_0 \in L_k$ and $L_k$ is closed under neighbours, induction on $i$ gives $x_i \in L_k$, so $w \in L_k$. Thus $C(s) \subseteq L_k$, and (I1) gives $L_k \subseteq C(s)$. $\square$

**Theorem.** COMPONENTS$(G)$ returns labels with $\mathrm{comp}[u] = \mathrm{comp}[v]$ if and only if $u$ and $v$ lie in the same component, $k$ equal to the number of components, and parent pointers that form a spanning forest of $G$ with one tree for each component.

*Proof.* By induction over the loop of line L10, before the iteration for $s$ the labelled vertices are the union of the components of the vertices $0, \ldots, s-1$, and each value $k' < k$ labels exactly one component. If $\mathrm{comp}[s] \neq \mathrm{nil}$, $s$ lies in one of these components and nothing changes. Otherwise $s$ lies in none of them, so no vertex of $C(s)$ has a label, and by Lemma 2 the call labels exactly $C(s)$ with the new value $k$. So at the end each component has its own label and $k$ is their number.

Each vertex $v \neq s$ of $C(s)$ gets exactly one parent, in line L8, and its parent got its label earlier. So the parent edges in $C(s)$ have no cycle, they number $|C(s)| - 1$, and by (I1) they join every vertex to $s$. They form a spanning tree of $C(s)$, and over all components a spanning forest. $\blacksquare$

The proof does not use the rule of line L4, so it holds for every rule, which is the point of the generic algorithm.
