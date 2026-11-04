---
title: Smith's rule minimizes the weighted sum of completion times
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The input is a set $J$ of $n \ge 0$ jobs; job $j$ has a processing time $p_j > 0$ and a real weight $w_j$. For an order $\pi = (\pi_1, \ldots, \pi_n)$ of $J$, the completion time of $\pi_i$ is $C_{\pi_i}(\pi) = \sum_{l \le i} p_{\pi_l}$, and the cost is $K(\pi) = \sum_{i=1}^{n} w_{\pi_i} C_{\pi_i}(\pi)$. Write $\rho_j = w_j / p_j$. For jobs $a, b$, since $p_a p_b > 0$, the test $w_a p_b \ge w_b p_a$ of line L1 holds if and only if $\rho_a \ge \rho_b$. Call an order *sorted* when $\rho_{\pi_1} \ge \rho_{\pi_2} \ge \cdots \ge \rho_{\pi_n}$.

**Claim.** The algorithm stops, it returns a sorted order $\sigma$ together with $K(\sigma)$, and $K(\sigma) = \min_\pi K(\pi)$. Moreover, an order is optimal if and only if it is sorted.

**Step 1: termination and the output.** Line L1 is a sort with the key $\rho$, so it stops and gives a sorted order $\sigma$. The loop of line L3 runs $n$ times. By induction on $i$, after line L4 of iteration $i$ the value of $t$ is $\sum_{l \le i} p_{\sigma_l} = C_{\sigma_i}(\sigma)$, and after line L5 the value of $total$ is $\sum_{l \le i} w_{\sigma_l} C_{\sigma_l}(\sigma)$. For $i = n$ this is $K(\sigma)$.

**Step 2: the adjacent swap.** Let $\pi$ be an order, let $1 \le i < n$, and let $\pi'$ be $\pi$ with the jobs $a = \pi_i$ and $b = \pi_{i+1}$ exchanged. Let $s = \sum_{l < i} p_{\pi_l}$. Each job other than $a$ and $b$ has the same set of predecessors in both orders, so the same completion time. In $\pi$, $C_a = s + p_a$ and $C_b = s + p_a + p_b$. In $\pi'$, $C_b = s + p_b$ and $C_a = s + p_a + p_b$. So
$$ K(\pi') - K(\pi) = w_b(s + p_b) + w_a(s + p_a + p_b) - w_a(s + p_a) - w_b(s + p_a + p_b) = w_a p_b - w_b p_a. $$
Dividing by $p_a p_b > 0$, $K(\pi') - K(\pi)$ has the sign of $\rho_a - \rho_b$.

**Step 3: every optimal order is sorted.** A set of $n!$ orders is finite and not empty, so an optimal order $\pi^*$ exists. Suppose $\pi^*$ is not sorted. Then some $i$ has $\rho_{\pi^*_i} < \rho_{\pi^*_{i+1}}$, and by Step 2 the swap of positions $i$ and $i+1$ gives an order of strictly smaller cost. This contradicts the optimality of $\pi^*$. So each optimal order is sorted.

**Step 4: all sorted orders have the same cost.** Let $\pi$ and $\tau$ be sorted orders. Group the jobs into blocks of equal ratio. In a sorted order, the jobs of each block are consecutive, and the blocks appear in decreasing order of ratio, so $\pi$ and $\tau$ have the same blocks in the same positions and differ only in the order inside the blocks. Inside one block, sort the jobs of $\pi$ into their order in $\tau$ by adjacent swaps, as [bubble sort](/bubble-sort/) does; each swap exchanges two adjacent jobs of equal ratio, so by Step 2 it does not change the cost, and it keeps the order sorted. After finitely many swaps, $\pi$ becomes $\tau$. So $K(\pi) = K(\tau)$.

**Step 5: conclusion.** By Step 3, the optimal order $\pi^*$ is sorted. By Step 4, $K(\sigma) = K(\pi^*)$, so $\sigma$ is optimal. For the second part of the claim: an optimal order is sorted by Step 3, and a sorted order has the cost $K(\pi^*)$ by Step 4, so it is optimal. $\blacksquare$

**Cost.** Line L1 does $O(n \log n)$ comparisons with a comparison sort such as merge sort, and each comparison is two multiplications. The loop does $n$ iterations of $O(1)$ arithmetic operations. So the time is $O(n \log n)$ arithmetic operations.
