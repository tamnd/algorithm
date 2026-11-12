---
title: The critical path method computes the least project duration, the latest times and the floats
proves: [correctness]
status: full
---

Let $G$ be the precedence graph, a directed acyclic graph on the activities $1, \ldots, n$, with durations $p_j \ge 0$. A schedule $S$ is *feasible* if $S_j \ge 0$ for all $j$ and $S_j \ge S_i + p_i$ for every arc $(i, j)$. Its duration is $\max_j (S_j + p_j)$. A *chain* is a path $j_1 \to j_2 \to \cdots \to j_r$ in $G$, and its length is $\sum_q p_{j_q}$. Let $h_j$ be the largest length of a chain that ends at a predecessor of $j$ and is followed by the arc into $j$, that is, the longest chain ending just before $j$ ($h_j = 0$ if $j$ has no predecessor). Let $t_j$ be the largest length of a chain that starts at a successor of $j$ ($t_j = 0$ if $j$ has no successor).

Line L1 returns an order $\sigma$ in which every arc goes forward. Kahn's algorithm returns such an order whenever $G$ is acyclic, and fails exactly when $G$ has a cycle.

**Lemma 1.** After line L2, $ES_j = h_j$ for every $j$.

*Proof.* By induction along $\sigma$. When line L2 handles $j$, every predecessor $i$ was handled before, so $ES_i = h_i$. A longest chain ending just before $j$ ends at some predecessor $i$ and consists of a longest chain ending just before $i$ followed by $i$, so $h_j = \max_{(i, j)} (h_i + p_i)$, which is what line L2 computes. With no predecessor both sides are $0$. $\square$

**Lemma 2.** The schedule $S = ES$ is feasible, and every feasible schedule has $S_j \ge ES_j$ for all $j$.

*Proof.* For an arc $(i, j)$, line L2 gives $ES_j \ge ES_i + p_i$, and $ES_j \ge 0$. For the second claim, induct along $\sigma$: $S_j \ge S_i + p_i \ge ES_i + p_i$ for every arc $(i, j)$, and $S_j \ge 0$, so $S_j \ge ES_j$. $\square$

**Theorem 1.** The value $T$ of line L3 is the least duration of a feasible schedule, and it equals the length of a longest chain of $G$.

*Proof.* By Lemma 2, every feasible schedule has duration $\max_j (S_j + p_j) \ge \max_j (ES_j + p_j) = T$, and $S = ES$ reaches $T$. By Lemma 1, $ES_j + p_j = h_j + p_j$ is the length of a longest chain that ends at $j$, so $T$ is the length of a longest chain. $\square$

**Lemma 3.** After line L4, $LF_i = T - t_i$ for every $i$. Every feasible schedule of duration at most $T$ has $S_i + p_i \le LF_i$, and the schedule $S_j = LS_j = LF_j - p_j$ is feasible with duration $T$.

*Proof.* The first claim is Lemma 1 on the reversed graph, along the reversed order: line L4 computes $LF_i = \min_{(i, j)} (LF_j - p_j)$, and $t_i = \max_{(i, j)} (p_j + t_j)$, with $LF_i = T$ and $t_i = 0$ when $i$ has no successor. For the bound, induct along the reversed order: an activity with no successor must finish by $T = LF_i$; otherwise $S_i + p_i \le S_j \le LF_j - p_j$ for each arc $(i, j)$, so $S_i + p_i \le LF_i$. For feasibility of $LS$: for each arc $(i, j)$, $LS_j = LF_j - p_j \ge LF_i = LS_i + p_i$, by line L4. Also $LS_j = T - t_j - p_j \ge 0$, since $p_j + t_j$ is the length of a chain and so at most $T$. Every activity finishes by $LF_j \le T$. $\square$

**Theorem 2 (total float).** $TF_j = T - (h_j + p_j + t_j)$, the project duration minus the length of a longest chain through $j$. So $TF_j \ge 0$, and $TF_j = 0$ exactly when $j$ lies on a longest chain of $G$. Activity $j$ can start at any time in $[ES_j, LS_j]$ in some feasible schedule of duration $T$, and at no other time.

*Proof.* By Lemmas 1 and 3, $TF_j = LF_j - p_j - ES_j = T - t_j - p_j - h_j$. A chain through $j$ has length at most $T$ by Theorem 1, so $TF_j \ge 0$, with equality exactly when a chain through $j$ has length $T$. By Lemmas 2 and 3, every feasible schedule of duration at most $T$ has $ES_j \le S_j \le LS_j$. Conversely, take $s$ in $[ES_j, LS_j]$. Let $D$ be the set of activities that can be reached from $j$, with $j$ in $D$, and for $k$ in $D$ let $d_k$ be the largest length of a chain from $j$ to a predecessor of $k$ ($d_j = 0$). Set $S_k = ES_k$ for $k$ not in $D$ and $S_k = \max(ES_k, s + d_k)$ for $k$ in $D$. Then $S_j = s$. For an arc $(a, b)$: if $b$ is not in $D$, then $a$ is not in $D$ either, and $S_b = ES_b \ge ES_a + p_a$. If $b$ is in $D$ and $a$ is not, then $S_b \ge ES_b \ge ES_a + p_a = S_a + p_a$. If both are in $D$, then $d_b \ge d_a + p_a$, so $S_b \ge \max(ES_a + p_a, s + d_a + p_a) = S_a + p_a$. So $S$ is feasible. For $k$ in $D$, the schedule $LS$ is feasible, so $LS_k \ge LS_j + d_k \ge s + d_k$, and also $LS_k \ge ES_k$. So $S_k \le LS_k$ for every $k$, every activity ends by $LF_k \le T$, and the duration is $T$. $\square$

**Theorem 3 (free float).** If activity $j$ starts at $ES_j + \delta$ with $0 \le \delta \le FF_j$ and every other activity at its earliest start, the schedule is feasible and has duration $T$. For $\delta > FF_j$, keeping every other activity at its earliest start is infeasible or makes the duration larger than $T$.

*Proof.* Only the constraints that involve $j$ change. The arcs into $j$ still hold, since $j$ starts later. For each arc $(j, k)$, line L6 gives $ES_j + \delta + p_j \le ES_j + FF_j + p_j \le ES_k$. If $j$ has no successor, line L6 uses $T$, so $j$ ends by $T$. For $\delta > FF_j$, either some successor $k$ has $ES_j + \delta + p_j > ES_k$, which breaks the arc $(j, k)$, or $j$ has no successor and ends after $T$. $\square$

**Theorem 4 (the path of line L7).** Line L7 finds an activity to start from, never gets stuck, and returns a chain of length $T$.

*Proof.* Take a longest chain of $G$. Its first activity has $h = 0$, since a positive $h$ would extend the chain to a longer one, so its $ES = 0$, and it lies on a longest chain, so $TF = 0$ by Theorem 2. Now let $j$ be the current activity, with $TF_j = 0$, and $ES_j + p_j < T$. Then $t_j = T - h_j - p_j > 0$, so $j$ has a successor $k$ with $p_k + t_k = t_j$. Then $h_k \ge h_j + p_j$, and $h_k + p_k + t_k \le T = h_j + p_j + t_j$ gives $h_k \le h_j + p_j$. So $ES_k = h_k = ES_j + p_j$, and $h_k + p_k + t_k = T$, so $TF_k = 0$. Line L7 can move to such a $k$. Every step goes along an arc, so the walk ends, and it ends only when $ES_j + p_j = T$. The activities visited form a chain whose consecutive activities are back to back from time $0$ to time $T$, so its length is $T$. $\blacksquare$
