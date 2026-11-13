---
title: Forward state-space search is sound and complete, breadth-first order gives a plan with the fewest actions, and the cost order gives a cheapest plan
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode FORWARD-SEARCH of the page, for a ground STRIPS task $(F, A, I, G)$ with $n = |F|$ and $m = |A|$. Write $s[a] = (s \setminus \mathit{del}(a)) \cup \mathit{add}(a)$ for the state after an applicable action. A state $t$ is *reachable* if some sequence of actions is applicable from $I$ and ends in $t$; let $d(t)$ be the least number of actions of such a sequence, and $R$ the set of reachable states, with $r = |R| \le 2^n$.

**Invariant (P).** At the start of each pass of the loop at line L3, for each key $t$ of `parent`, PLAN(parent, $t$) returns a sequence of actions that is applicable from $I$ and ends in $t$. Every state in $Q$ is a key of `parent`.

*Proof.* Before the loop the only key is $I$, PLAN returns the empty sequence, and $Q$ holds $I$. A pass adds a key $t$ only at line L10, with $\mathit{parent}[t] = (s, a)$, where $s$ is a key, $a$ is applicable in $s$ (line L7) and $t = s[a]$ (line L8). PLAN(parent, $t$) is PLAN(parent, $s$) followed by $a$. By the invariant for $s$, this sequence is applicable from $I$ and ends in $s$, and then $a$ is applicable and ends in $t$. Keys are never removed or changed, because line L9 sets `parent` only for a new key, so the sequences of the old keys stay the same. Line L11 puts in $Q$ only the key just added. $\square$

**Theorem 1 (soundness).** If FORWARD-SEARCH returns a sequence, it is a plan.

*Proof.* It returns at line L5 only for a state $s$ removed from $Q$ with $G \subseteq s$. By (P), $s$ is a key, and PLAN(parent, $s$) is applicable from $I$ and ends in $s$, which contains $G$. $\square$

**Theorem 2 (termination).** The loop makes at most $r$ passes.

*Proof.* By (P) every key is reachable, so there are at most $r$ keys. A state enters $Q$ only when it becomes a key (lines L9 to L11), and it becomes a key at most once, so at most $r$ states ever enter $Q$. Each pass removes one. $\square$

**Theorem 3 (completeness).** If a plan exists, FORWARD-SEARCH returns a plan. If it returns failure, no plan exists.

*Proof.* The two claims are the same, because by Theorem 2 the search returns either a plan or failure. Suppose it returns failure at line L12. Then each key was removed from $Q$ and expanded, since $Q$ is empty, and no removed state contains $G$. We show that every reachable state is a key. Let $t \in R$ and let $I = t_0, t_1, \ldots, t_k = t$ be the states along a sequence of applicable actions $a_1, \ldots, a_k$. The state $t_0 = I$ is a key. If $t_{i-1}$ is a key, it was expanded, and in its expansion the action $a_i$ passed the test of line L7 and gave $t_i$ at line L8. Then $t_i$ was already a key, or it became one at line L10. By induction $t$ is a key. So every reachable state was removed and does not contain $G$, and no plan exists. $\square$

**Theorem 4 (breadth-first order gives the fewest actions).** With the FIFO queue, a returned plan has exactly $\min \{ d(t) : t \in R, G \subseteq t \}$ actions.

*Proof.* Let $\ell(t)$ be the length of PLAN(parent, $t$) for a key $t$. By (P), $\ell(t) \ge d(t)$.

*Step 1 (order of the queue).* At each moment the values $\ell$ of the states in $Q$, from the front to the back, are nondecreasing, and the last is at most the first plus 1. At the start $Q = (I)$. When $s$ is removed from the front, every value left in $Q$ is between $\ell(s)$ and $\ell(s) + 1$, and the new keys go to the back with $\ell(s) + 1$, so both properties are kept. It follows that the states leave $Q$ in nondecreasing order of $\ell$, and that the value of the removed state grows by at most 1 from one pass to the next. Also, a state with value $k$ enters $Q$ only during the expansion of a state with value $k - 1$, so every state of value $k$ that ever enters $Q$ is in $Q$ before the first state of value $k$ is removed.

*Step 2 (claim).* For each $k \ge 0$: if the search removes a state of value $k$, then at the moment it removes the first such state, every reachable state $u$ with $d(u) \le k$ is a key and has $\ell(u) = d(u)$. We use induction on $k$. For $k = 0$ the only state with $d = 0$ is $I$, a key with $\ell(I) = 0$. Let $k \ge 0$, and let the search remove a state of value $k + 1$. By Step 1 it removed a state of value $k$ before, so by the induction hypothesis every $w$ with $d(w) = k$ was a key with $\ell(w) = k$ at that moment, and by Step 1 it was removed before the first state of value $k + 1$. Since the search did not stop, $w$ was expanded. Let $u$ be reachable with $d(u) = k + 1$, and let $w$ be the state before $u$ on a shortest path, so $d(w) = k$ and $u = w[a]$ for some action $a$. The expansion of $w$ generated $u$. Either $u$ became a key then, with $\ell(u) = k + 1$, or it was a key before, made by the expansion of a state removed no later than $w$, which has value at most $k$, so $\ell(u) \le k + 1$. With $\ell(u) \ge d(u) = k + 1$ this gives $\ell(u) = d(u)$.

*Step 3 (the plan).* Let $d^* = \min \{ d(t) : t \in R, G \subseteq t \}$ and let $t^*$ be a goal state with $d(t^*) = d^*$. Let the search stop at a removed goal state $s$; then $\ell(s) \ge d(s) \ge d^*$. Suppose $\ell(s) > d^*$. By Step 1 the removed values grow from 0 by at most 1 at a time, so a state of value $d^*$ was removed before $s$. By Step 2, $t^*$ was then a key of value $d^*$, and by Step 1 it was removed before $s$, which has a larger value. When it was removed, line L5 stopped the search, so the search did not reach $s$. This is a contradiction, so $\ell(s) = d^*$. $\square$

**Theorem 5 (cost order gives a cheapest plan).** Let every cost be nonnegative, let $Q$ be a priority queue on the path cost $g$, let a state be put back in $Q$ with its new cost whenever a cheaper path to it is found, and let a removed state with a cost larger than its best known cost be skipped. Then the returned plan has the least total cost.

*Proof.* This is uniform-cost search on the state graph, a finite graph with nonnegative edge costs, whose source is $I$ and whose targets are the states that contain $G$. It is [Dijkstra's algorithm](/dijkstra/) with the test for a target at removal. By the proof of [the correctness of Dijkstra's algorithm](/dijkstra-correctness/), each state leaves $Q$ for the first time with the cost of a cheapest path from $I$, and states leave $Q$ in nondecreasing order of that cost. The first target removed therefore has the least cost among all targets, and PLAN returns the path whose cost was recorded. $\square$

**Theorem 6 (cost).** FORWARD-SEARCH takes $O(r m n)$ time and $O(r n)$ space.

*Proof.* By Theorem 2 there are at most $r$ passes. In one pass, line L5 and each test of line L7 cost $O(n)$, line L8 costs $O(n)$, and the lookup of line L9 costs $O(n)$ to hash the state and expected $O(1)$ further work with a [hash table](/hash-table/), or $O(n \log r)$ with a balanced search tree. So a pass costs $O(m n)$, and PLAN costs $O(n)$ per action of the plan, at most $r$ actions. The table and the queue hold at most $r$ states of $O(n)$ bits. $\square$
