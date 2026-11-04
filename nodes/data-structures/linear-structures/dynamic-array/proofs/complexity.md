---
title: Append and pop on a dynamic array cost O(1) amortized
proves: [amortized]
status: full
---

**Cost model.** APPEND costs 1 for line L2, plus $n$ if line L1 resizes. POP costs 1 for line L5, plus $n'$ if line L6 resizes, where $n' = n - 1$ is the count after line L4. RESIZE costs one unit per copy in line L10. GET and SET cost 1 and do not change $n$ or $cap$.

**Potential.** For a state with count $n$ and capacity $cap$, let

$$\Phi(n, cap) = \begin{cases} 2n - cap & \text{if } 2n \ge cap, \\ cap/2 - n & \text{if } 2n < cap. \end{cases}$$

Both branches are at least 0 where they apply, so $\Phi \ge 0$. At the start $\Phi(0, 1) = 1/2$. The amortized cost of an operation is its cost plus $\Phi_{\text{after}} - \Phi_{\text{before}}$.

**Claim.** Each APPEND has amortized cost at most 3, and each POP at most 2.

*APPEND without a resize ($n < cap$).* The cost is 1 and $n$ becomes $n + 1$.

- If $2n \ge cap$: $\Delta\Phi = 2(n + 1) - 2n = 2$, amortized cost 3.
- If $2(n + 1) < cap$: $\Delta\Phi = -1$, amortized cost 0.
- If $2n < cap \le 2n + 2$: $\Delta\Phi = (2n + 2 - cap) - (cap/2 - n) = 3n + 2 - \tfrac{3}{2} cap$. Since $cap > 2n$, this is less than $3n + 2 - 3n = 2$, so the amortized cost is less than 3.

*APPEND with a resize ($n = cap \ge 1$).* The cost is $1 + n$. Before, $\Phi = 2n - n = n$. After, the count is $n + 1$ and the capacity $2n$, and $2(n + 1) \ge 2n$, so $\Phi = 2(n + 1) - 2n = 2$. The amortized cost is $1 + n + 2 - n = 3$.

*POP without a resize.* The cost is 1 and $n$ becomes $n' = n - 1$, with the same $cap$.

- If $2n' \ge cap$: $\Delta\Phi = -2$, amortized cost $-1$.
- If $2n < cap$: $\Delta\Phi = (cap/2 - n + 1) - (cap/2 - n) = 1$, amortized cost 2.
- If $2n' < cap \le 2n$: $\Delta\Phi = (cap/2 - n + 1) - (2n - cap) = \tfrac{3}{2} cap - 3n + 1$. Since $cap \le 2n$, this is at most $3n - 3n + 1 = 1$, so the amortized cost is at most 2.

*POP with a resize ($n' \ge 1$ and $cap = 4n'$).* The cost is $1 + n'$. After, the capacity is $2n'$ and the count $n'$, so $\Phi = 2n' - 2n' = 0$. Before, the count was $n' + 1$.

- If $n' \ge 2$: $2(n' + 1) < 4n'$, so $\Phi_{\text{before}} = 2n' - (n' + 1) = n' - 1$, and the amortized cost is $1 + n' + 0 - (n' - 1) = 2$.
- If $n' = 1$: $cap = 4$ and the count was 2, so $2 \cdot 2 \ge 4$ and $\Phi_{\text{before}} = 0$. The amortized cost is $1 + 1 + 0 - 0 = 2$.

This proves the claim. $\square$

**Theorem.** Any sequence of $m$ operations on a new dynamic array, of which $a$ are appends, costs at most $3a + 2(m - a) + 1/2 \le 3m + 1/2$.

*Proof.* Let $c_k$ and $\hat c_k$ be the cost and the amortized cost of operation $k$, and $\Phi_k$ the potential after it. Then $\sum_{k=1}^{m} \hat c_k = \sum_{k=1}^{m} c_k + \Phi_m - \Phi_0$, because the sum of the differences telescopes. So $\sum c_k = \sum \hat c_k - \Phi_m + \Phi_0 \le \sum \hat c_k + 1/2$, because $\Phi_m \ge 0$ and $\Phi_0 = 1/2$. GET and SET have amortized cost 1, and the claim bounds the rest. $\blacksquare$
