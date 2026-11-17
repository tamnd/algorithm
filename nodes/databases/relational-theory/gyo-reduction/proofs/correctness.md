---
title: The GYO reduction ends with at most one edge if and only if the hypergraph has a join tree
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $H$ has the edges $e_1, \ldots, e_m$. A run applies lines L4 and L6 in some order, chosen freely among the rules that apply, until line L7 stops the loop. $A$ is the set of the remaining edges, $c_i$ is the current copy of $e_i$, and $D$ is the set of vertices that line L4 has deleted so far. A *join tree* of a list of sets $(f_i)_{i \in I}$ is a tree on $I$ in which, for each vertex $x$, the set $S_x = \{ i \in I : x \in f_i \}$ induces a connected subtree.

**Termination.** Let $\Phi = \sum_{i \in A} |c_i| + |A|$. At the start $\Phi = \sum_i |e_i| + m$. Line L4 lowers $\Phi$ by exactly 1, and line L6 lowers it by $|c_i| + 1 \ge 1$. $\Phi \ge 0$, so there are at most $\sum_i |e_i| + m$ steps, and the loop stops.

**Lemma 1 (invariant).** At each point of the run, (a) $c_i = e_i \setminus D$ for each $i \in A$, and (b) no vertex of $D$ is in $c_i$ for any $i \in A$.

*Proof.* Part (b) follows from part (a), so we show (a). At the start $D = \emptyset$ and $c_i = e_i$. Line L6 only makes $A$ smaller, so it keeps (a). Line L4 deletes a vertex $x$ from the copy $c_i$, and $c_i$ is the only copy that holds $x$. It then adds $x$ to $D$. The new copy $c_i \setminus \{x\}$ is equal to $e_i \setminus (D \cup \{x\})$. For $k \in A$ with $k \ne i$, the copy $c_k = e_k \setminus D$ does not change and does not hold $x$, so it is equal to $e_k \setminus (D \cup \{x\})$. $\square$

**Lemma 2 (soundness).** If the run ends with $|A| \le 1$, the pairs $\{i, \mathit{parent}[i]\}$ form a join tree of $e_1, \ldots, e_m$.

*Proof.* If $m = 0$ there is nothing to prove. Otherwise line L6 runs $m - |A|$ times. Let $i_1, \ldots, i_{m-1}$ be the deleted edges in the order of deletion and $r$ the last edge, so $|A| = 1$ at the end; $|A| = 0$ is not possible, because line L6 needs a second edge $j \in A$. Let $A_t$ be the set $A$ just before the deletion of $i_t$, so $A_t = \{ i_t, i_{t+1}, \ldots, i_{m-1}, r \}$, and let $A_m = \{r\}$. The parent $j_t = \mathit{parent}[i_t]$ is in $A_t \setminus \{i_t\} = A_{t+1}$. Let $T_t$ be the graph on $A_t$ with the edges $\{i_s, j_s\}$ for $s \ge t$.

We show by induction on $t$, from $t = m$ down to $t = 1$, that $T_t$ is a join tree of $(e_i)_{i \in A_t}$. For $t = m$, $T_m$ is the single node $r$. For the step from $t + 1$ to $t$: $T_t$ is $T_{t+1}$ with the new leaf $i_t$ joined to $j_t \in A_{t+1}$, so it is a tree. Take a vertex $x$, and let $S_x$ be the set of edges of $A_t$ whose original edge holds $x$.

- If $x \notin e_{i_t}$, then $S_x \subseteq A_{t+1}$ is connected in $T_{t+1}$ by the induction hypothesis, and so in $T_t$.
- If $x \in e_{i_t}$ and no edge of $A_{t+1}$ holds $x$, then $S_x = \{i_t\}$ is connected.
- If $x \in e_{i_t}$ and $x \in e_k$ for some $k \in A_{t+1}$, then $x \notin D$ at the time of the deletion of $i_t$. Indeed, before that time both $i_t$ and $k$ are in $A$. While $x \notin D$, Lemma 1 (a) gives $x \in c_{i_t}$ and $x \in c_k$, so two copies hold $x$ and line L4 can not delete $x$. So $x$ stays out of $D$, and $x \in e_{i_t} \setminus D = c_{i_t}$. Line L6 runs only when $c_{i_t} \subseteq c_{j_t}$, so $x \in c_{j_t} \subseteq e_{j_t}$, and $j_t \in S_x \cap A_{t+1}$. By the induction hypothesis $S_x \cap A_{t+1}$ is connected in $T_{t+1}$, and $i_t$ is joined to $j_t$, so $S_x$ is connected in $T_t$.

For $t = 1$, $A_1 = \{1, \ldots, m\}$, and $T_1$ is the tree of the parent links. $\square$

**Lemma 3 (a rule applies).** Let $(c_i)_{i \in A}$ have a join tree $T$, with $|A| \ge 2$. Then line L4 or line L6 applies.

*Proof.* $T$ has at least two nodes, so it has a leaf $\ell$ with a neighbor $p$. Let $x \in c_\ell$ be in $c_k$ for some $k \ne \ell$. The path from $\ell$ to $k$ in $T$ starts with the edge $\{\ell, p\}$, and $S_x$ is connected and holds $\ell$ and $k$, so $p \in S_x$ and $x \in c_p$. So each vertex of $c_\ell$ is either in no other copy, and then line L4 applies to it, or it is in $c_p$. If no vertex of $c_\ell$ is of the first kind, $c_\ell \subseteq c_p$ and line L6 applies to $(\ell, p)$. $\square$

**Lemma 4 (the rules keep a join tree).** If $(c_i)_{i \in A}$ has a join tree before a step, it has one after the step.

*Proof.* After line L4 deletes $x$ from $c_i$, the same tree $T$ works: the sets $S_y$ for $y \ne x$ do not change, and $S_x$ becomes empty. After line L6 deletes $i$ with $c_i \subseteq c_j$, let $n_j$ be the neighbor of $i$ on the path from $i$ to $j$ in $T$ (so $n_j = j$ when $j$ is a neighbor of $i$). Build $T'$ from $T$: delete the node $i$ and join each neighbor of $i$ other than $n_j$ to $j$. $T - i$ has one component for each neighbor of $i$, the component of $n_j$ holds $j$, and $T'$ joins each other component to $j$ by one edge. So $T'$ is a tree on $A \setminus \{i\}$.

Take a vertex $y$ and two nodes $u, w \in S_y \setminus \{i\}$. The path from $u$ to $w$ in $T$ lies inside $S_y$. If it does not pass through $i$, it is also a path in $T'$. If $y \notin c_i$, then $i \notin S_y$ and this is always the case. If $y \in c_i$, then $y \in c_j$, so $S_y$ holds $i$ and $j$ and the whole path from $i$ to $j$ in $T$, which includes $n_j$. In $T'$, each neighbor of $i$ in $S_y$ other than $n_j$ is joined to $j$, and $n_j$ is joined to $j$ by the part of the path from $i$ to $j$ that does not use $i$. So all neighbors of $i$ in $S_y$ are connected to $j$ inside $S_y \setminus \{i\}$ in $T'$. A path from $u$ to $w$ through $i$ enters and leaves $i$ through two such neighbors, so $u$ and $w$ are connected inside $S_y \setminus \{i\}$ in $T'$. $\square$

**Theorem.** For every order of the rules, the run ends with $|A| \le 1$ if and only if $e_1, \ldots, e_m$ has a join tree, and then the parent links form a join tree.

*Proof.* If the run ends with $|A| \le 1$, Lemma 2 gives the join tree. Conversely, let $H$ have a join tree. By Lemma 4 and induction on the steps, the current copies have a join tree at each point of the run. The run ends at line L7, where no rule applies, so by Lemma 3, $|A| \le 1$ there. $\blacksquare$
