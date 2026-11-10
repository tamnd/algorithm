---
title: Algorithm L returns a uniform k-subset
proves: [correctness, termination]
status: full
---

**Statement.** Let $k \ge 1$, let the stream have $n \ge k$ items, and assume exact real arithmetic and independent uniform random reals in $(0, 1]$ and uniform integers in $\{1, \ldots, k\}$. Then ALGORITHM-L stops, and it returns the items of a $k$-subset of the positions $\{1, \ldots, n\}$ that is uniform: each $k$-subset has probability $1/\binom{n}{k}$. (For $n < k$ line L1 already holds all items, and for $k = 0$ the result is empty.)

**Setup: the key process.** Give the items independent uniform keys $u_1, u_2, \ldots$ in $(0, 1)$. For $t \ge k$, let $A_t$ be the set of the positions of the $k$ smallest keys among $u_1, \ldots, u_t$, and let $M_t$ be the largest key in $A_t$, that is, the $k$-th smallest of $u_1, \ldots, u_t$. Ties have probability 0 and we ignore them.

**Step 1: $A_n$ is a uniform $k$-subset.** The keys are independent and identically distributed, so each of the $n!$ orders of $u_1, \ldots, u_n$ is equally likely. A $k$-subset $S$ is $A_n$ exactly when the keys of $S$ come first in the order, which happens in $k!\,(n-k)!$ of the $n!$ orders. So $\Pr[A_n = S] = 1/\binom{n}{k}$.

**Step 2: how the key process moves.** We claim, by induction on $t \ge k$: given the whole past $(A_k, M_k, \ldots, A_t, M_t)$, the keys at the positions of $A_t$ consist of one key equal to $M_t$, at a position that is uniform over $A_t$, and $k - 1$ keys that are independent and uniform on $(0, M_t)$; and the keys $u_{t+1}, u_{t+2}, \ldots$ are still independent uniform on $(0, 1)$.

- *Base, $t = k$.* $A_k = \{1, \ldots, k\}$. The $k$ keys are independent uniform. Their maximum $M_k$ has $\Pr[M_k \le x] = x^k$. By symmetry the position of the maximum is uniform and independent of $M_k$, and given both, the other $k - 1$ keys are independent uniform on $(0, M_k)$.
- *Step.* Item $t+1$ enters $A_{t+1}$ if and only if $u_{t+1} < M_t$, which has probability $M_t$ given the past. If it does not enter, nothing changes, and the claim holds for $t + 1$. If it enters, the position with key $M_t$ leaves. It is uniform over $A_t$ by the hypothesis. The new set has $k - 1$ old keys that are independent uniform on $(0, M_t)$, and the key $u_{t+1}$, which given $u_{t+1} < M_t$ is uniform on $(0, M_t)$ and independent of them. So the $k$ keys of $A_{t+1}$ are independent uniform on $(0, M_t)$. Their maximum is $M_{t+1} = M_t \cdot V^{1/k}$ for a uniform $V$ independent of the past, since $\Pr[\max \le M_t x] = x^k$. By symmetry the position of the new maximum is uniform over $A_{t+1}$, and the other keys are independent uniform on $(0, M_{t+1})$.

So the process $(A_t, M_t)$ is a Markov chain with these moves: start from $A_k = \{1, \ldots, k\}$ and $M_k = U_0^{1/k}$; each next item enters independently with probability $M$; when an item enters, a uniform member of $A$ leaves and $M$ is multiplied by $V^{1/k}$ for a fresh uniform $V$.

**Step 3: the skip.** In the chain, the number $G$ of items that do not enter before the next item that enters satisfies $\Pr[G \ge g \mid M = w] = (1 - w)^g$ for $g = 0, 1, 2, \ldots$. Line L4 sets $G = \lfloor \ln U / \ln(1 - W) \rfloor$ for a uniform $U \in (0, 1]$. Since $\ln(1 - W) < 0$ for $0 < W < 1$,
$$\Pr[G \ge g] = \Pr\!\left[\frac{\ln U}{\ln(1 - W)} \ge g\right] = \Pr[\ln U \le g \ln(1 - W)] = \Pr[U \le (1 - W)^g] = (1 - W)^g.$$
So the skip has the same law as in the chain.

**Step 4: the algorithm is the chain.** Line L2 sets $W = U_0^{1/k}$, the law of $M_k$. Lines L4 and L5 move to the next item that enters, with the skip of step 3. Line L7 puts it in a uniform slot, so a uniform member of the reservoir leaves. Line L8 multiplies $W$ by $V^{1/k}$. Each of these uses fresh random numbers, so by induction on the number of entries, the sequence of reservoir sets of the algorithm has the same joint law as $(A_t)$ in the key process. In particular, the reservoir after the last item, $t = n$, has the law of $A_n$, which is uniform by step 1.

**Termination.** Each round of lines L4 and L5 increases the position $i$ by $G + 1 \ge 1$, so after at most $n - k + 1$ rounds $i > n$ and line L6 returns. $\blacksquare$

**Remark: the number of entries.** Let $R_t \in \{1, \ldots, t\}$ be the rank of $u_t$ among $u_1, \ldots, u_t$. The map from the order of $u_1, \ldots, u_n$ to the vector $(R_1, \ldots, R_n)$ is a bijection between $n!$ orders and $1 \cdot 2 \cdots n = n!$ vectors, so the $R_t$ are independent and $R_t$ is uniform on $\{1, \ldots, t\}$. Item $t > k$ enters exactly when $R_t \le k$. So the entries are independent events with probability $k/t$, and the expected number of entries is $k(H_n - H_k)$, as for [Algorithm R](/reservoir-sampling/).
