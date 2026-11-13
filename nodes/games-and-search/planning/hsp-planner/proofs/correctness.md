---
title: HSP2 is sound, terminates and is complete for nonnegative integer costs, and its cost is bounded by the number of reachable states
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode HSP2 of the page, for a ground STRIPS task $(F, A, I, G)$ with $n = |F|$, $m = |A|$ and action costs $c(a)$ that are nonnegative integers. Write $s[a] = (s \setminus \mathit{del}(a)) \cup \mathit{add}(a)$. A state is a *key* once `best` has a finite value for it, and `best` is $\infty$ for every other state. Let $r$ be the number of states reachable from $I$. We use two facts from other pages: $h_{\mathrm{add}}(t) = \infty$ exactly when the delete relaxation from $t$ has no plan ([h-add](/h-add-heuristic/)), and every plan from $t$ is a relaxed plan from $t$ ([delete relaxation](/delete-relaxation/)).

**Lemma 1 (values only drop).** The value best(t) of a key changes only at line L11, and only to a strictly smaller value. The value best(I) stays 0, and parent(I) stays nil.

*Proof.* Line L11 runs only after the test of line L9 has shown that the new value is smaller. For $t = I$ the new value would be best(s) + c(a) $\ge 0$ = best(I), so the test fails. $\square$

**Lemma 2 (parent links).** If parent(t) = (s, a), then $a$ is applicable in $s$, $t = s[a]$, $s$ is a key, and from then on best(t) $\ge$ best(s) + c(a).

*Proof.* Line L11 sets parent(t) = (s, a) where $s$ is the state being expanded, so a key, with $\mathit{pre}(a) \subseteq s$ by line L7 and $t = s[a]$ by line L8. At that moment best(t) = best(s) + c(a). Until parent(t) is set again, best(t) stays the same, and best(s) can only drop by Lemma 1, so the inequality stays true. $\square$

**Lemma 3 (the links form a tree).** At every moment, following parent links from a key never repeats a state, and it ends at $I$.

*Proof.* Suppose a cycle $t_0, t_1, \ldots, t_j = t_0$ of parent links appears, where parent($t_{i+1}$) = ($t_i$, $a_{i+1}$). Consider the moment when the last of its links was set, say parent($t_1$) = ($t_0$, $a_1$), and let $b$ be the value of best($t_1$) just before. The other links of the cycle were set earlier, so by Lemma 2, at that moment best($t_{i+1}$) $\ge$ best($t_i$) + c($a_{i+1}$) $\ge$ best($t_i$) for $i = 1, \ldots, j - 1$, and so best($t_0$) $\ge$ best($t_1$) $= b$. The new value is best($t_0$) + c($a_1$) $\ge b$, which contradicts the strict drop of Lemma 1. So there is no cycle. The keys are finitely many, and the only key with the link nil is $I$, so following the links ends at $I$. $\square$

**Theorem 1 (soundness).** If HSP2 returns a sequence at line L6, it is a plan.

*Proof.* By Lemma 3 the parent links from $s$ lead back to $I$. Read in the order from $I$, by Lemma 2 each action is applicable in the state before it and leads to the state after it. So the sequence is applicable from $I$ and ends in $s$, and line L6 checked $G \subseteq s$. $\square$

**Lemma 4 (pruning keeps plans).** If $h(t) = \infty$, no plan leaves $t$. Every state on a plan from $I$ has $h < \infty$.

*Proof.* A plan from $t$ is a relaxed plan from $t$, so if $t$ had a plan, the relaxed task from $t$ would have one and $h_{\mathrm{add}}(t)$ would be finite. The part of a plan from $I$ after a state $u$ on it is a plan from $u$. $\square$

**Lemma 5 (values are costs of simple paths).** Each value that line L11 assigns to best(t) is the cost of a path from $I$ to $t$ in the state graph that visits no state twice.

*Proof.* Attach to each value a *witness*: for best(I) = 0 the empty path, and for a value best(s) + c(a) assigned to best(t) the witness of the current value of best(s) followed by $a$. By induction over time, every witness is a path from $I$ whose cost is the value. Each prefix of a witness that ends at a state $u$ is the witness of a value that was assigned to best(u) earlier in time. Suppose the witness of a new value $v$ of best(t) visits $t$ also before its end. The prefix up to that visit is the witness of an earlier value $v'$ of best(t), and $v' \le v$ because costs are nonnegative. But values of best(t) only drop, so $v < v'$, a contradiction. If the witness visits some other state $u$ twice, the prefixes up to the first and up to the second visit are the witnesses of two values $v_1$ and $v_2$ of best(u), where $v_1$ was assigned first, because the shorter prefix is also a prefix of the witness of $v_2$. Then $v_1 \le v_2$ because costs are nonnegative, and $v_2 < v_1$ because values only drop, again a contradiction. $\square$

**Theorem 2 (termination).** HSP2 stops after a finite number of iterations of line L4.

*Proof.* Every key is reachable from $I$, by Lemma 3 and Lemma 2, so there are at most $r$ keys. Each insertion of $t$ at line L12 follows a strict drop of best(t) at line L11. The values are nonnegative integers and the first one is finite, so $t$ is inserted finitely often. So the total number of insertions is finite, and each iteration of line L4 removes one entry. $\square$

**Theorem 3 (completeness).** If the task has a plan, HSP2 returns a plan.

*Proof.* Let $a_1, \ldots, a_k$ be a plan with states $s_0 = I, s_1, \ldots, s_k$ and $G \subseteq s_k$. By Lemma 4, $h(I) < \infty$, so HSP2 does not stop at line L2. Suppose it stops at line L13, so OPEN becomes empty and no goal state was removed without being skipped. We first show: every key $u$ is at some time removed at line L5 with the entry of its final value and not skipped. By Theorem 2 the value of best(u) changes finitely often. After its last change, line L12 inserted an entry for $u$ with that value (for $u = I$, line L3 did). This entry is removed at some time, since OPEN becomes empty, and then best(u) still equals its value, so it is not skipped. Then $u$ is expanded, and since no goal state is returned, $u$ does not contain $G$.

Now by induction each $s_i$ is a key. $s_0 = I$ is one. If $s_i$ is a key, it is expanded with its final value $b$. The action $a_{i+1}$ is applicable in $s_i$ and line L8 builds $s_{i+1}$. Either best($s_{i+1}$) $\le b + c(a_{i+1})$ already, so $s_{i+1}$ is a key, or line L9 succeeds, line L10 does not prune $s_{i+1}$ by Lemma 4, and line L11 makes it a key. So $s_k$ is a key, and by the claim above it is expanded, so it does not contain $G$. This contradicts $G \subseteq s_k$. $\square$

**Theorem 4 (cost).** For unit costs HSP2 makes at most $r$ evaluations of $h$ and at most $r^2$ expansions, and runs in time $O(r^2 m n + r m n \log(m n))$ and space $O(r n + m n)$. For integer costs at most $C$, replace $r^2$ by $r (C (r - 1) + 1)$.

*Proof.* A state is evaluated once and its value is stored, and only keys and states examined at line L10 are evaluated, all of them reachable, so at most $r$ evaluations happen. One evaluation is a run of H-ADD on a task of size $L = n + \sum_a (|\mathit{pre}(a)| + |\mathit{add}(a)|) = O(m n)$, in time $O(L \log L)$ with a binary heap, by the analysis on the [h-add](/h-add-heuristic/) page. By Lemma 5, each value of best(t) is the cost of a path that visits at most $r$ states, so it is at most $C (r - 1)$, and the values of best(t) strictly drop, so $t$ is inserted at most $C (r - 1) + 1$ times; for unit costs, $r$ times. Each expansion is a removal of an entry that is not skipped, so there are at most as many expansions as insertions, at most $r^2$ for unit costs. An expansion tests $m$ preconditions and builds up to $m$ successors in $O(n)$ time each, with a hash of $O(n)$ time per lookup, and does up to $m$ heap insertions in $O(\log r^2) = O(n)$ time each, since $r \le 2^n$. So an expansion costs $O(m n)$. The tables hold at most $r$ states of $O(n)$ bits, the heap holds at most $r^2$ entries that refer to stored states, and the precondition index of H-ADD has size $O(m n)$. $\square$

**Remark (the first HSP).** The hill climbing search `hsp1` is sound, because it applies only applicable actions and returns a plan only at a goal state, and it stops because the number of moves is bounded. It is not complete: on the Sussman anomaly it returns no plan for the seeds 0 to 4, with the limits of the page, although a plan of 6 actions exists. The test file checks this.
