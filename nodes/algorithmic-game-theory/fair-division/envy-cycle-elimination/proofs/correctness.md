---
title: Envy-cycle elimination ends and returns an EF1 allocation for monotone valuations
proves: [correctness]
status: full
---

**Setting.** There are $n \ge 1$ agents and goods $g_1, \dots, g_m$. Each valuation $v_i$ is defined on all sets of goods, has $v_i(\emptyset) = 0$, and is monotone: $S \subseteq T$ implies $v_i(S) \le v_i(T)$. We refer to the lines L1 to L10 of the page. A *partial allocation* is a list of disjoint bundles $(A_1, \dots, A_n)$. It is EF1 if for all agents $i \ne j$ with $A_j \ne \emptyset$ some $g \in A_j$ has $v_i(A_i) \ge v_i(A_j \setminus \{g\})$. The envy graph $G(A)$ has an edge $i \to j$ when $v_i(A_j) > v_i(A_i)$, and $|G(A)|$ is its number of edges.

**Lemma 1 (a cycle exists in line L5).** If every agent has an incoming edge in $G(A)$, then $G(A)$ has a cycle $c_0, \dots, c_{k-1}$ with $k \ge 2$ in which $c_{t+1}$ envies $c_t$ for every $t$, indices taken mod $k$.

*Proof.* Start at any agent $x_0$ and let $x_{s+1}$ be an agent with an edge $x_{s+1} \to x_s$. Among the $n + 1$ agents $x_0, \dots, x_n$ two are equal, say $x_a = x_b$ with $a < b$ and $b - a$ least. Then $x_a, x_{a+1}, \dots, x_{b-1}$ is a cycle of the required kind. It has $k = b - a \ge 2$ agents, because there are no loops: $v_i(A_i) > v_i(A_i)$ is false. $\square$

**Lemma 2 (a rotation keeps EF1 and raises the values on the cycle).** Let $A$ be EF1 and let $A'$ be the result of line L6. Then $v_{c}(A'_{c}) > v_{c}(A_{c})$ for every agent $c$ on the cycle, $A'_i = A_i$ for every other agent, the bundles of $A'$ are those of $A$ in another order, and $A'$ is EF1.

*Proof.* Agent $c_{t+1}$ gets $A_{c_t}$, which it values more than $A_{c_{t+1}}$ because it envies $c_t$. Agents off the cycle keep their bundles. The bundles of the cycle agents are permuted among them, so the set of bundles does not change.

Now take agents $i \ne j$ with $A'_j \ne \emptyset$, and let $B = A'_j$. If $B = A_\ell$ for some $\ell \ne i$, then EF1 of $A$ gives a good $g \in B$ with $v_i(B \setminus \{g\}) \le v_i(A_i) \le v_i(A'_i)$. Otherwise $B = A_i$, which happens only when $i$ is on the cycle; then $v_i(B \setminus \{g\}) \le v_i(A_i) < v_i(A'_i)$ for any $g \in B$, by monotonicity. $\square$

**Lemma 3 (giving the good to an unenvied agent keeps EF1).** Let $A$ be EF1, let $i$ have no incoming edge in $G(A)$, and let $A'$ be $A$ with $A'_i = A_i \cup \{g\}$ for a good $g$ outside all bundles. Then $A'$ is EF1.

*Proof.* For an agent $k \ne i$ and the bundle $A'_i$, remove $g$: $v_k(A'_i \setminus \{g\}) = v_k(A_i) \le v_k(A_k) = v_k(A'_k)$, since $k$ does not envy $i$. For an agent $k \ne i$ and a bundle $A'_j = A_j$ with $j \ne i, k$, nothing changed. For agent $i$ and a bundle $A'_j = A_j$, EF1 of $A$ gives $g' \in A_j$ with $v_i(A_j \setminus \{g'\}) \le v_i(A_i) \le v_i(A'_i)$, by monotonicity. $\square$

**Lemma 4 (edge count).** A rotation of line L6 over a cycle of $k$ agents gives $|G(A')| \le |G(A)| - k$. The step of line L9 gives $|G(A')| \le |G(A)| + n - 1$.

*Proof.* Rotation: by Lemma 2 the set of bundles is the same. For an agent $x$ off the cycle, its own bundle and the set of the other bundles are the same, so its out-degree is the same. For an agent $c = c_{t+1}$ on the cycle, its new own bundle is $A_{c_t}$. A bundle that $c$ envies in $A'$ is worth more to $c$ than $A_{c_t}$, hence more than $A_c$, so $c$ also envied its owner in $A$; and the bundle $A_{c_t}$, which $c$ envied in $A$, is now its own. So the out-degree of $c$ drops by at least 1, and the $k$ agents of the cycle lose at least $k$ edges.

Line L9: only $A_i$ changes. An edge $x \to y$ with $x, y \ne i$ is unchanged. An edge out of $i$ in $G(A')$ means $v_i(A_y) > v_i(A_i \cup \{g\}) \ge v_i(A_i)$, so it was in $G(A)$. New edges can only point into $i$, and there are at most $n - 1$ of them. $\square$

**Theorem.** The algorithm ends after at most $m(n - 1)/2$ rotations, and it returns an EF1 allocation of all goods.

*Proof.* The edge count starts at 0 in line L1 and is never negative. By Lemma 4 the $m$ steps of line L9 add at most $m(n - 1)$ edges in total, and each rotation removes at least $k \ge 2$ edges (Lemma 1). So the total number of rotations is at most $m(n - 1)/2$, every loop of line L4 ends, and line L8 then finds an agent with no incoming edge.

The empty allocation of line L1 is EF1. By Lemma 2 each rotation keeps EF1, and by Lemma 3 each step of line L9 keeps EF1, since its receiver has no incoming edge. The good $g$ of line L2 is outside all bundles, because each good is given once. After the last good, every good lies in exactly one bundle, and the allocation is EF1. $\blacksquare$
