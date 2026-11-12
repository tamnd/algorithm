---
title: RED spaces its marks uniformly and averages the queue with fixed weights
proves: [correctness]
status: full
---

We use the pseudocode of the page. All claims are about one queue.

**Lemma 1 (the gap law).** Assume that $avg$ stays at one value with $min_{th} \le avg < max_{th}$, so that $p_b$ is a constant in $(0, 1)$, and that the coins of line L7 are independent. Let $N = \lfloor 1/p_b \rfloor$. Start just after a mark, so $count = 0$, and let $X$ be the number of arrivals up to and including the next mark. Then $\Pr[X = n] = p_b$ for $1 \le n \le N$, and $\Pr[X = N + 1] = 1 - N p_b$. No other value has positive probability.

*Proof.* Line L8 adds 1 to $count$ at each unmarked arrival, and line L7 sets it to 0 at a mark. So the $n$-th arrival after a mark sees $count = n - 1$ if no mark came between. Let $a_n$ be the probability that the first $n - 1$ arrivals are not marked. Then $a_1 = 1$.

We show by induction on $n$ that $a_n = 1 - (n-1) p_b$ for $1 \le n \le N + 1$. This holds for $n = 1$. Assume it for some $n \le N$. Since $n p_b \le N p_b \le 1$, we have $1 - (n-1) p_b \ge p_b > 0$. So line L6 gives the probability $p_a = p_b / (1 - (n-1) p_b)$, which is at most 1. Hence

$$\Pr[X = n] = a_n \cdot \frac{p_b}{1 - (n-1) p_b} = p_b, \qquad a_{n+1} = a_n - \Pr[X = n] = 1 - n p_b.$$

This proves the claim for $n + 1$. At $n = N + 1$, the arrival sees $count = N$, and $N p_b > 1 - p_b$ because $(N + 1) p_b > 1$. So $1 - N p_b < p_b$, and line L6 gives a value of at least 1 (or a denominator of 0 or less when $N p_b = 1$), which the pseudocode treats as 1. So $\Pr[X = N + 1] = a_{N+1} = 1 - N p_b$, and no arrival after it can be the first mark. $\square$

When $1/p_b$ is an integer $N$, the last probability is 0, so $X$ is uniform on $\{1, \ldots, N\}$ and

$$E[X] = \frac{N + 1}{2} = \frac{1/p_b + 1}{2}.$$

By the renewal reward theorem, the long-run fraction of marked packets is $1/E[X] = 2 p_b / (1 + p_b)$.

*Comparison.* If each arrival is marked with the fixed probability $p_b$ (Method 1 of Floyd and Jacobson), then $\Pr[X = n] = (1 - p_b)^{n-1} p_b$, a geometric law with mean $1/p_b$. Then $\Pr[X > N] = (1 - p_b)^N$, which is about $e^{-1} \approx 0.37$ for small $p_b$. Lemma 1 gives $\Pr[X > N + 1] = 0$.

**Lemma 2 (the average).** Let arrivals $1, \ldots, k$ see the queue lengths $q_1, \ldots, q_k > 0$, and let $avg_0$ be the average before them. Then after them

$$avg_k = (1 - w_q)^k avg_0 + \sum_{j=1}^{k} w_q (1 - w_q)^{k-j} q_j.$$

*Proof.* By induction on $k$. For $k = 0$ the sum is empty. Line L1 gives $avg_{k+1} = (1 - w_q) avg_k + w_q q_{k+1}$. Put in the formula for $avg_k$: each old weight is multiplied by $1 - w_q$, and the new term has weight $w_q (1 - w_q)^0$. $\square$

The weights are $(1 - w_q)^k$ and $w_q (1 - w_q)^{k-j}$ for $j = 1, \ldots, k$. They are not negative, and their sum is $(1 - w_q)^k + w_q \cdot \frac{1 - (1 - w_q)^k}{w_q} = 1$. So $avg_k$ is a convex combination of $avg_0, q_1, \ldots, q_k$. Line L2 multiplies the average by a number in $[0, 1]$, which keeps it between 0 and its old value.

*The ramp.* Let $avg_0 = 0$ and $q_j = j$, and write $r = 1 - w_q$. We show $avg_k = k + 1 + (r^{k+1} - 1)/w_q$ by induction on $k$. For $k = 0$ the right side is $1 + (r - 1)/w_q = 1 - 1 = 0$. If it holds for $k$, then line L1 gives

$$avg_{k+1} = r\, avg_k + w_q (k + 1) = (k + 1)(r + w_q) + \frac{r^{k+2} - r}{w_q} = (k + 1) + \frac{r^{k+2} - r}{w_q},$$

and $(k + 2) + (r^{k+2} - 1)/w_q$ minus this is $1 + (r - 1)/w_q = 0$. For $k = 100$ and $w_q = 0.001$ the value is about $4.887$.

**Lemma 3 (no flow bias).** The decision for a packet is a function of $avg$, $count$ and a fresh uniform random number. None of these depends on the flow of the packet. So, given the state at its arrival, the probability that a packet is marked does not depend on its flow. $\square$
