---
title: Johnson's two-list rule minimizes the makespan of the two-machine flow shop
proves: [correctness]
status: full
---

We use the notation of the page: job $j$ needs $a_j \ge 0$ on machine 1 and then $b_j \ge 0$ on machine 2, and $\pi$ is the order of lines L1 to L5.

**Step 1: one order is enough.** Take any schedule. If machine 1 and machine 2 run the jobs in different orders, then some two jobs $i$ and $j$ are adjacent on machine 1, with $i$ first, while machine 2 runs $j$ before $i$. (If every pair adjacent on machine 1 were in the same order on machine 2, the two orders would be equal.) Let $s$ be the start of $i$ on machine 1. Run $j$ in $[s, s + a_j]$ and $i$ in $[s + a_j, s + a_i + a_j]$ on machine 1 instead. Machine 1 stays busy in the same interval. Job $j$ now leaves machine 1 earlier than before. Job $i$ now leaves machine 1 at $s + a_i + a_j$, which is when $j$ left before; machine 2 started $j$ no earlier than that, and $i$ after $j$, so $i$ also starts on machine 2 after it leaves machine 1. Nothing on machine 2 moves, so the makespan does not change. The swap reduces the number of pairs that the two machines run in different orders by one. After finitely many swaps both machines use the order of machine 2. So there is an optimal permutation schedule, and we only compare orders.

**Step 2: the makespan of an order.** For an order $\sigma$, with every operation as early as possible, let $C_1(k) = \sum_{l \le k} a_{\sigma(l)}$ and $C_2(k) = \max(C_1(k), C_2(k-1)) + b_{\sigma(k)}$ with $C_2(0) = 0$, as in lines L8 and L9. Unrolling the recursion gives
$$C_2(n) = \max_{1 \le k \le n} T_k(\sigma), \qquad T_k(\sigma) = \sum_{l \le k} a_{\sigma(l)} + \sum_{l \ge k} b_{\sigma(l)}.$$
Indeed, by induction $C_2(k) = \max_{l \le k} \big(C_1(l) + \sum_{l \le q \le k} b_{\sigma(q)}\big)$: the case $k = 1$ is $a_{\sigma(1)} + b_{\sigma(1)}$, and the step adds $b_{\sigma(k)}$ to the maximum of $C_1(k)$ and the formula for $k - 1$.

**Step 3: an adjacent swap.** Let $\sigma$ have $i$ at position $k$ and $j$ at position $k + 1$, and let $\sigma'$ be $\sigma$ with the two swapped. For $q \ne k, k + 1$, the term $T_q$ is the same in both orders, since it depends only on the set of jobs before position $q$, the set after it, and the job at $q$. Let $A$ be the machine 1 time of the jobs before position $k$ and $B$ the machine 2 time of the jobs after position $k + 1$. Then
$$\max(T_k(\sigma), T_{k+1}(\sigma)) = A + B + \max(a_i + b_i + b_j,\ a_i + a_j + b_j) = A + B + a_i + a_j + b_i + b_j - \min(a_j, b_i),$$
and in the same way $\max(T_k(\sigma'), T_{k+1}(\sigma')) = A + B + a_i + a_j + b_i + b_j - \min(a_i, b_j)$. So if
$$\min(a_i, b_j) \le \min(a_j, b_i), \tag{J}$$
then $C_{\max}(\sigma) \le C_{\max}(\sigma')$: putting $i$ right before $j$ is no worse than putting $j$ right before $i$.

**Step 4: the order of line L5 satisfies (J) for every pair.** Let $i$ come before $j$ in $\pi$, at any distance.

- Both in $F$. Line L3 gives $a_i \le a_j$, and $i \in F$ gives $a_i \le b_i$. So $\min(a_i, b_j) \le a_i \le \min(a_j, b_i)$.
- Both in $G$. Line L4 gives $b_i \ge b_j$, and $j \in G$ gives $b_j < a_j$. So $\min(a_i, b_j) \le b_j \le \min(a_j, b_i)$.
- $i \in F$ and $j \in G$. Then $a_i \le b_i$ and $b_j < a_j$. If $\min(a_j, b_i) = a_j$, then $\min(a_i, b_j) \le b_j < a_j$. If $\min(a_j, b_i) = b_i$, then $\min(a_i, b_j) \le a_i \le b_i$.

Line L5 never puts a job of $G$ before a job of $F$, so these cases are all.

**Step 5: optimality.** Let $\sigma$ be an optimal order. If $\sigma \ne \pi$, some two adjacent jobs of $\sigma$, $j$ then $i$, appear in the other order in $\pi$; otherwise $\sigma$ would follow $\pi$ along the whole sequence. By Step 4, (J) holds for $i$ before $j$, and by Step 3, swapping them does not raise the makespan. The swap removes one pair that $\sigma$ and $\pi$ order differently and adds none. After at most $\binom{n}{2}$ swaps we reach $\pi$, so $C_{\max}(\pi) \le C_{\max}(\sigma)$, and $\pi$ is optimal. By Step 1 it is optimal over all schedules, not only over permutation schedules. $\blacksquare$

**Why Step 4 checks all pairs.** The relation (J) is not transitive when there are ties, so it is not enough to know that each adjacent pair of $\pi$ satisfies it. Step 5 swaps pairs that can be far apart in $\pi$, which is why Step 4 proves (J) for every pair in the order of $\pi$.

**Ties.** Nothing above uses how ties in lines L3 and L4 are broken, and a job with $a_j = b_j$ satisfies the conditions used for both $F$ and $G$, so it may go in either list.
