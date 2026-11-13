---
title: The operations of a partial-order plan are correct, every linearization of a solution plan is a valid plan, and every valid plan is a linearization of some solution plan
proves: [correctness]
status: full
---

We use the definitions and the pseudocode of the page. Write $i \prec^+ j$ when a chain of stored ordering pairs leads from $i$ to $j$; this is the transitive closure of the stored pairs. Every link $i \xrightarrow{p} j$ is stored with the pair $i \prec j$ (line L11). A linearization respects every stored pair, hence every pair of $\prec^+$.

**Lemma 1 (PRECEDES).** PRECEDES$(P, i, j)$ returns true if and only if $i \prec^+ j$.

*Proof.* The search pushes each step at most once, so it ends. Every pushed step $k$ satisfies $i \prec^+ k$, since it was found as a successor of $i$ or of an earlier pushed step; so a true answer at line L5 is correct. Conversely, let $i = k_0 \prec k_1 \prec \cdots \prec k_r = j$ be a chain. If the search returned false, take the least $t \ge 1$ such that $k_t$ is never pushed and is not $j$, or $t = r$. Then $k_{t-1}$ was pushed, or is $i$, and was later popped, since the loop at line L3 empties the stack; at that pop, line L4 met $k_t$. If $k_t = j$, line L5 returned true. Otherwise line L6 pushed $k_t$, against the choice of $t$. $\square$

**Lemma 2 (consistency).** $P$ has a linearization if and only if its ordering graph has no cycle. If $P$ has no cycle and ADD-ORDERING$(P, i, j)$ adds a pair, the new graph has no cycle.

*Proof.* The first claim is the existence theorem for [topological orders](/topological-sort/): a cycle cannot be ordered, and a finite acyclic graph has a vertex with no incoming edge, which can be placed first, after which induction applies. For the second, a cycle in the new graph must use the new pair $i \prec j$, so the rest of it is a chain from $j$ to $i$ in the old graph, or $i = j$. Line L8 rules out both, by Lemma 1. $\square$

**Lemma 3 (the threat test).** Let $P$ have no cycle, and let $i \xrightarrow{p} j$ be a link and $k \notin \{i, j\}$ a step. Some linearization puts $k$ after $i$ and before $j$ if and only if neither $k \prec^+ i$ nor $j \prec^+ k$. So line L14 reports exactly the threats.

*Proof.* If $k \prec^+ i$, every linearization puts $k$ before $i$; if $j \prec^+ k$, every linearization puts $k$ after $j$. Conversely, suppose neither holds. Add the pairs $i \prec k$ and $k \prec j$. A cycle in the new graph uses a new pair. If it uses $i \prec k$ but not $k \prec j$, the rest is a chain from $k$ to $i$ in the old graph, which is excluded. If it uses $k \prec j$ but not $i \prec k$, the rest is a chain from $j$ to $k$, excluded. If it uses both, it also contains a chain from $j$ to $i$ in the old graph, and with the stored pair $i \prec j$ of the link this is a cycle in the old graph, excluded. So the new graph has no cycle, by Lemma 2 it has a linearization, and that linearization respects the old pairs and puts $k$ between $i$ and $j$. By Lemma 1, line L14 tests exactly this condition. $\square$

**Theorem 1 (the solution law).** Let $P$ be a solution: it has no cycle, no open condition and no threat. Then the action sequence of every linearization of $P$ is a plan: every action applies in turn, and the goal holds at the end.

*Proof.* Let the linearization be $(u_0, u_1, \ldots, u_{m+1})$, with $u_0 = $ START and $u_{m+1} = $ FINISH, and let $x_t$ be the state after the actions of $u_1, \ldots, u_t$, so $x_0 = I$. We show that for every $t$ with $0 \le t \le m$, $\mathit{pre}(u_{t+1}) \subseteq x_t$. Since $\mathit{pre}(\text{FINISH}) = G$, this gives both claims.

Take $p \in \mathit{pre}(u_{t+1})$. It is not an open condition, so there is a link $u_r \xrightarrow{p} u_{t+1}$, with $r \le t$ because the link stores $u_r \prec u_{t+1}$. Step $u_r$ adds $p$: for $r = 0$ this means $p \in I = x_0$, and for $r \ge 1$ the next state after $u_r$ contains $\mathit{add}(u_r)$, so $p \in x_r$. For $r < v \le t$, the step $u_v$ lies after $u_r$ and before $u_{t+1}$ in a linearization. If $p \in \mathit{del}(u_v)$, then $(u_v, u_r \xrightarrow{p} u_{t+1})$ would be a threat, and $P$ has none. So no step from $u_{r+1}$ to $u_t$ deletes $p$, and $p \in x_t$. $\square$

**Theorem 2 (the converse).** Let $\sigma = (a_1, \ldots, a_m)$ be a plan. Build $P$ with steps $s_1, \ldots, s_m$ for the actions of $\sigma$, put START at position $0$ and FINISH at $m + 1$, and:

1. for every step $s_t$, with FINISH at $t = m + 1$, and every $p \in \mathit{pre}(s_t)$, link $p$ from the last earlier position $q < t$ whose step adds $p$, or from START if there is none;
2. for every link $s_q \xrightarrow{p} s_t$ and every step $s_v \notin \{s_q, s_t\}$ with $p \in \mathit{del}(s_v)$, store $s_v \prec s_q$ if $v < q$ and $s_t \prec s_v$ otherwise.

Then $P$ is a solution, and $\sigma$ is the action sequence of one of its linearizations.

*Proof.* Every stored pair goes from a smaller position to a larger one, so the order of positions is a linearization, and $P$ has no cycle. In step 1, START is a correct producer if no earlier step adds $p$: since $\sigma$ is a plan, $p$ holds before position $t$, and a fact that no step added holds only if it was in $I$. Every precondition has a link, so none is open. Take a link $s_q \xrightarrow{p} s_t$ and a step $s_v$ that deletes $p$. Position $v$ is not strictly between $q$ and $t$: if it were, then $p$ would fail after $s_v$, and no step between $v$ and $t$ adds $p$, since $q$ was the last adder, so $p$ would not hold before $s_t$, against $\sigma$ being a plan. So $v < q$ or $v > t$, and the stored pair of step 2 forces $s_v \prec^+ s_q$ or $s_t \prec^+ s_v$. By Lemma 3, $s_v$ is not a threat. $\square$

Theorem 1 says that a solution stands only for valid plans. Theorem 2 says that every valid plan is represented by some solution, so the data structure loses nothing by leaving orders out.
