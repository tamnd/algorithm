---
title: Beam-stack search publishes cheaper and cheaper paths, stops on a finite graph, and ends with an optimal path
proves: [correctness]
status: full
---

We use the pseudocode of the page and the tie rule of the implementation. Each action costs 1, the set of states reachable from $s_0$ is finite with $n$ states, $h$ is consistent with $h(t) = 0$ at each goal $t$, and $s_0$ is not a goal (the code handles that case first). We write $g^*(u)$ for the least number of actions from $s_0$ to $u$, $f(u, i) = i + h(u)$ for a state $u$ in layer $i$, and $D = \min_t g^*(t)$ over the goals $t$, if a goal is reachable. Consistency here says $h(u) \le 1 + h(v)$ for each action from $u$ to $v$, so along a path the values $i + h$ never fall, and $h(u)$ is at most the number of actions on any path from $u$ to a goal.

The item for layer $i$ is the $i$-th item of STACK from the bottom. We say that item $i$ *lives* from the time line L4 pushes it until line L11 pops it.

**Fact 1 (the stored layers).** At each visit of line L3, the stored layers $L_0, \ldots, L_{r}$ are disjoint, $L_0 = [s_0]$, each state of $L_i$ has a parent in $L_{i-1}$ and a path of exactly $i$ actions from $s_0$, and STACK has $r$ or $r + 1$ items. While item $i$ lives, the layers $L_0, \ldots, L_{i-1}$ and the items $1, \ldots, i - 1$ do not change.

*Proof.* Line L5 drops each successor that is in a stored layer, so a new layer is disjoint from the others, and each of its states has its parent in the layer before. Only the top item changes, at lines L9 and L13, and only the top layers are deleted, at line L14: after line L13 changes the item of layer $j$, line L14 deletes the layers $L_j$ and up, which belonged to the old range. While item $i$ is on the stack, it or an item above it is the top, so items $1, \ldots, i - 1$ and the layers $L_0, \ldots, L_{i-1}$ stay. $\square$

**Lemma 2 (slices).** Fix a time when line L5 builds the candidates for layer $i$ from the top item $[a, b)$ with $a < b$. Then the layer that line L10 stores, if any, is exactly the set of candidates with $f$ in $[a, b')$ and $f < U$, where $[a, b')$ is the item after line L9. Moreover $b' > a$.

*Proof.* If line L8 does not cut, $b' = b$ and all candidates are kept, and line L6 admitted exactly those with $a \le f < b$ and $f < U$. If it cuts at the value $c$ of the $(k+1)$-th best candidate, it keeps those with $f < c$ and sets $b' = c$. Since $c$ is the $f$ of a candidate, $c < b$, and the kept set is the candidates with $f$ in $[a, c)$. If that set is empty, the tie rule keeps the candidates with the least value $\ell$ and sets $b'$ to the next larger value among the candidates, or keeps $b' = b$ if there is none. No candidate has $f$ in $[a, \ell)$ or in $(\ell, b')$, so the kept set is again the candidates with $f$ in $[a, b')$. In each case $b' > a$: either the kept set is nonempty, so some $f \ge a$ is below $b'$, or no cut happened and $b' = b > a$. $\square$

**Lemma 3 (ranges).** Each item on STACK has $f_{\min} < f_{\max}$. While item $i$ lives, its successive ranges are $[a_0, b_0), [a_1, b_1), \ldots, [a_r, b_r)$ with $a_0 = 0$ and $a_{q+1} = b_q$, where $b_q$ is the value after line L9, and line L11 pops it only when $b_r \ge U$. So each value $x$ with $0 \le x < U$, for the value of $U$ at the pop, lies in exactly one of the ranges.

*Proof.* By induction over time. Line L4 pushes $[0, U)$, and $U > 0$ because $s_0$ is not a goal. Line L13 replaces $[a, b)$ by $[b, U)$ only after line L11 has popped every top item with $f_{\max} \ge U$, so $b < U$. Line L9 keeps $f_{\max} > f_{\min}$ by Lemma 2, which applies because the item had $f_{\min} < f_{\max}$ before. The ranges follow each other because line L13 starts the new range at the old $f_{\max}$. Line L11 pops only when $f_{\max} \ge U$. $\square$

**Theorem 4 (valid and improving paths).** Each path that line L7 publishes is a path of $i$ actions from $s_0$ to a goal, and its cost $i$ is below each earlier published cost.

*Proof.* The goal $m$ is a successor of a state of $L_{i-1}$, which has a path of $i - 1$ actions by Fact 1, and the path follows the parents. Line L6 admitted $m$ only with $f(m, i) = i + 0 < U$, so $i < U$, and $U$ was the cost of the last published path. $\square$

**Theorem 5 (termination).** The search stops after finitely many visits of line L3.

*Proof.* Let $\sigma$ be the sequence of the $f_{\min}$ values of the items on STACK, from the bottom. Each visit of line L3 either returns, or appends a layer at line L10, after which the next visit pushes an item with $f_{\min} = 0$ and $\sigma$ grows by one entry, or reaches line L13. In the last case lines L11 and L13 cut $\sigma$ to a prefix and raise its last entry from $a$ to $b > a$. In both cases $\sigma$ grows strictly in lexicographic order, where a proper prefix comes first. Line L9 changes only $f_{\max}$, so $\sigma$ is the same at the next visit when no layer is appended.

The sequence $\sigma$ has at most $n$ entries, because the stored layers are disjoint and nonempty by Fact 1 and STACK has at most one more item than there are layers beyond $L_0$. Each entry is 0 or a former $f_{\max}$ below $U$, which is the $f$ of a candidate, a value $i + h(u)$ with $i < n$ and $u$ reachable, or a former $U$, the cost of a published path. So the entries come from a finite set, there are finitely many sequences $\sigma$, and the search stops. $\square$

**Lemma 6 (the optimal path is followed).** Let a goal be reachable, let $P = (p_0, \ldots, p_D)$ be a path with $D = g^*(p_D)$ actions to a goal $p_D$, and suppose that $U > D$ at some time when item $j + 1$ lives, $p_j \in L_j$ and $j < D$. Then before item $j + 1$ is popped, either $U$ becomes at most $D$, or line L10 stores a layer $L_{j+1}$ with $p_{j+1} \in L_{j+1}$.

*Proof.* Suppose that $U > D$ until item $j + 1$ is popped. By Fact 1 the layers $L_0, \ldots, L_j$ stay fixed while item $j + 1$ lives, so $p_j$ stays in $L_j$. Each state $p_q$ of $P$ has $g^*(p_q) = q$, since a shorter path to $p_q$ would give a path to $p_D$ with fewer than $D$ actions. So $p_{j+1}$, which has no path of $j$ or fewer actions, is in none of $L_0, \ldots, L_j$ by Fact 1. Consistency gives $h(p_q) \le D - q$, so
$$x = f(p_{j+1}, j+1) = j + 1 + h(p_{j+1}) \le D < U.$$
By Lemma 3, $x$ lies in one of the ranges $[a_q, b_q)$ of item $j + 1$. Consider the time when line L5 builds the candidates from that range. The state $p_j$ is expanded, because $j + h(p_j) \le D < U$. Its successor $p_{j+1}$ is in no stored layer, has $f = x$ in the range and below $U$, and so is a candidate, at least through another parent in $L_j$. If some candidate is a goal, then line L7 sets $U = j + 1 \le D$. Otherwise, by Lemma 2, line L10 stores exactly the candidates with $f$ in $[a_q, b_q)$ below $U$, and $p_{j+1}$ is one of them. $\square$

**Theorem 7 (optimality).** If a goal is reachable, the search ends with $U = D$, and the last published path is optimal. If no goal is reachable, it publishes nothing and returns failure.

*Proof.* If no goal is reachable, line L7 never fires. Otherwise suppose that the search ends with $U > D$, so that $U > D$ the whole time, since $U$ only goes down. Item 1 is pushed at the first visit of line L3 with $p_0 = s_0 \in L_0$, and it is popped before the end, since STACK is empty at line L12. By Lemma 6 with $j = 0$, a layer $L_1 \ni p_1$ is stored while item 1 lives, and at the next visit item 2 is pushed with this $L_1$. Item 2 is popped before item 1, so by Lemma 6 with $j = 1$, a layer $L_2 \ni p_2$ is stored while item 2 lives, and so on. At $j = D - 1$, the candidates for layer $D$ built from the right range contain the goal $p_D$, so line L7 sets $U = D$, a contradiction. So the search ends with $U \le D$. Theorem 4 says that the last published path has $U$ actions and reaches a goal, so $U \ge D$. $\square$

**Remark.** The proof uses consistency twice: to skip the states with $i + h \ge U$, and to bound $f$ along the optimal path. With an admissible but inconsistent $h$, the first skip can cut an optimal path. The proof does not use the width $k$: it bounds the memory and the order of the slices, not the result.
