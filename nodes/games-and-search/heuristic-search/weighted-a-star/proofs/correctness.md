---
title: Weighted A* returns a path of cost at most w C*, with reopening for an admissible heuristic and without reopening for a consistent one
proves: [correctness]
status: full
---

We use the pseudocode of the page, with a weight $w \ge 1$. The graph is directed, each state has finitely many successors, and each action cost $c(n, n')$ is a nonnegative number. We write $g^*(n)$ for the cost of a cheapest path from $s_0$ to $n$, $h^*(n)$ for the cost of a cheapest path from $n$ to a goal, $d(u, v)$ for the cost of a cheapest path from $u$ to $v$, and $C^* = h^*(s_0)$, which we assume finite. The key of a state in OPEN is $f(n) = g[n] + w\,h(n)$. An admissible $h$ has $h(n) \le h^*(n)$, so $h(t) = 0$ at each goal $t$.

The lines L1 to L12 are the lines of A* with $h$ replaced by $w\,h$ in the key. The facts of the [A* proof](/a-star-search/) that do not use the key hold here word for word: Fact 1 ($g$ only goes down and never below $g^*$, and each node holds a real path of cost $g$), Fact 3 (each value of $g$ is the cost of a path that repeats no state), Theorem 1 (termination on a finite graph) and Lemma 2. Lemma 2 says: if $P = (p_0, \ldots, p_k)$ is a cheapest path from $s_0$ and $p_k$ is not in CLOSED with $g[p_k] = g^*(p_k)$, then at each visit of line L3 some $p_j$ is in OPEN with $g[p_j] = g^*(p_j)$. Its proof looks only at lines L7 to L11 and at the fact that a state in CLOSED with $g = g^*$ is never reopened. It does not use the order in which line L4 removes states.

**Theorem 1 (the bound with reopening).** Let $h$ be admissible. If the search returns at line L5, the path goes from $s_0$ to a goal and costs at most $w C^*$.

*Proof.* The path is a real path of cost $g[t]$ for the returned goal $t$, by Fact 1. Let $t^*$ be a goal with $g^*(t^*) = C^*$ and $P$ a cheapest path from $s_0$ to $t^*$. A goal is never put in CLOSED, since line L5 returns before line L6. So Lemma 2 applies to $P$ just before line L4 removes $t$, and it gives a state $p$ of $P$ in OPEN with $g[p] = g^*(p)$. Then
$$f(p) = g^*(p) + w\,h(p) \le w\,g^*(p) + w\,h^*(p) = w\,C^*,$$
where we used $w \ge 1$, $g^* \ge 0$, admissibility, and $g^*(p) + h^*(p) = C^*$ for a state on a cheapest path to a goal. Line L4 removed $t$, so $f(t) \le f(p)$, and $f(t) = g[t] + w\,h(t) = g[t]$ because $h(t) = 0$. So $g[t] \le w C^*$. $\square$

For the form without reopening, line L8 skips a cheaper path to a state in CLOSED. A state in CLOSED stays there, each state is expanded at most once, and a state with a value $g$ is in OPEN or in CLOSED but never in both. Lemma 2 is no longer true in this form, so we need a different argument and a stronger hypothesis.

**Lemma A (consistency along a path).** If $h$ is consistent, then $h(u) \le d(u, v) + h(v)$ for all states $u, v$, and $h$ is admissible.

*Proof.* Add the inequalities $h(x) \le c(x, y) + h(y)$ along a cheapest path from $u$ to $v$. For admissibility take $v$ a goal, where $h(v) = 0$. This is Lemma 4 of the A* proof. $\square$

**Lemma B (a good state in OPEN).** Let $h$ be consistent, use the form without reopening, and suppose that each state removed so far at line L4 had $g \le w\,g^*$ at its removal. Let $P = (p_0, \ldots, p_k)$ be a cheapest path from $s_0$ to a state $p_k$ that is not in CLOSED. Then the first state $p_j$ of $P$ that is not in CLOSED is in OPEN and has $g[p_j] \le w\,g^*(p_j)$.

*Proof.* If $j = 0$, then $p_0 = s_0$ has $g = 0 = g^*(s_0)$. If $j \ge 1$, then $p_{j-1}$ is in CLOSED, so it was removed and expanded, with $g[p_{j-1}] \le w\,g^*(p_{j-1})$ at that time. The expansion looked at the action to $p_j$, so afterwards
$$g[p_j] \le w\,g^*(p_{j-1}) + c(p_{j-1}, p_j) \le w\,\bigl(g^*(p_{j-1}) + c(p_{j-1}, p_j)\bigr) = w\,g^*(p_j),$$
since $w \ge 1$ and a part of a cheapest path is a cheapest path. Here we used that $p_j$ was not in CLOSED at that time, which holds because states never leave CLOSED in this form and $p_j$ is not in CLOSED now. Line L8 then either lowered $g[p_j]$ to at most $g[p_{j-1}] + c$ or found it already at most that value, and $g$ only goes down. Finally $p_j$ has a value $g$ and is not in CLOSED, so it is in OPEN. $\square$

**Theorem 2 (the bound without reopening).** Let $h$ be consistent, and use the form without reopening. Each time line L4 removes a state $s$, $g[s] \le w\,g^*(s)$. If the search returns a goal $t$, then $g[t] \le w\,C^*$.

*Proof.* By induction on the number of removals. Suppose the claim holds for all earlier removals, and line L4 now removes $s$. Take $P$ a cheapest path from $s_0$ to $s$. The state $s$ is in OPEN, so it is not in CLOSED, and Lemma B gives $p_j$ on $P$ in OPEN with $g[p_j] \le w\,g^*(p_j)$. If $p_j = s$ we are done. Otherwise line L4 chose $s$, so $f(s) \le f(p_j)$, and by Lemma A
$$g[s] + w\,h(s) \le g[p_j] + w\,h(p_j) \le w\,g^*(p_j) + w\,\bigl(d(p_j, s) + h(s)\bigr) = w\,g^*(s) + w\,h(s),$$
because $g^*(p_j) + d(p_j, s) = g^*(s)$ on a cheapest path. Subtract $w\,h(s)$.

For the second claim, let $t$ be the returned goal and $t^*$ a goal with $g^*(t^*) = C^*$. If $t^*$ was in CLOSED, it would have been removed, and a goal that is removed is returned at once, so $t^* = t$ and $g[t] \le w\,g^*(t^*) = w\,C^*$ by the first claim. Otherwise Lemma B, applied to a cheapest path to $t^*$ just before the removal of $t$, gives $p_j$ in OPEN with $g[p_j] \le w\,g^*(p_j)$, and
$$g[t] = f(t) \le f(p_j) \le w\,g^*(p_j) + w\,h^*(p_j) = w\,C^*,$$
using $h(t) = 0$ and the admissibility of $h$ from Lemma A. $\square$

**Theorem 3 (completeness).** If a goal can be reached and the graph is finite, both forms return a path, with the bounds of Theorems 1 and 2.

*Proof.* Both forms stop on a finite graph: the form with reopening by Theorem 1 of the A* proof, and the form without it because each state is expanded at most once. While no goal has been removed, some state of a cheapest path to a goal is in OPEN: by Lemma 2 of the A* proof in the form with reopening, and by Lemma B in the form without it. So OPEN is not empty at line L3, neither form reaches line L12, and each stops at line L5. $\square$

**Remark.** Without reopening and with an admissible $h$ that is not consistent, the bound can fail already for $w = 1$, where the method is A* without reopening. The page [graph search versus tree search](/graph-search-vs-tree-search/) gives such an example.
