---
title: GRASP for weighted set cover returns the best of K covers that are local minima, and with alpha 0 each cover costs at most H(d) times the optimum
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The input is a finite universe $U$, sets $S_1, \ldots, S_n \subseteq U$ whose union is $U$, costs $c_j > 0$, a parameter $\alpha \in [0, 1]$ and a number of iterations $K \ge 1$. A *cover* is a set $x$ of indices with $\bigcup_{j \in x} S_j = U$, and $c(x) = \sum_{j \in x} c_j$. Write $d = \max_j |S_j|$ and $H(d) = 1 + 1/2 + \cdots + 1/d$. LOCAL-SEARCH is the best-improvement descent with two moves: drop one chosen set, or replace one chosen set by one set that is not chosen. It only makes moves that give a cover of strictly lower cost.

**Lemma 1 (construction).** Lines L3 to L7 stop after at most $\min(n, |U|)$ passes of the loop, and they end with a cover.

*Proof.* At line L5, while some element $e$ is not covered, $e$ is in some $S_j$, since the union of the sets is $U$. So at least one ratio $r_j$ is defined, $r_{\min}$ exists, and the set with ratio $r_{\min}$ is in the RCL of line L6, because $r_{\min} \le r_{\min} + \alpha (r_{\max} - r_{\min})$ for $\alpha \ge 0$. So the RCL is not empty, and line L7 can pick from it. Every set in the RCL has at least one uncovered element, so each pass covers at least one new element, and a chosen set has no uncovered element after it is chosen, so it is never chosen again. So there are at most $|U|$ and at most $n$ passes. The loop stops only when no element is uncovered, so $x$ is a cover. $\square$

**Lemma 2 (local search).** LOCAL-SEARCH stops, and it returns a cover $z$ with $c(z) \le c(x)$ such that no drop and no swap gives a cover of lower cost.

*Proof.* Each move goes to a cover of strictly lower cost, so no cover repeats, and there are at most $2^n$ covers. The descent stops only when no move improves, which is the second claim. $\square$

**Lemma 3 (the best cover).** After iteration $i$, $b$ is one of the covers $z_1, \ldots, z_i$ returned by line L8, and $c(b) = \min_{k \le i} c(z_k)$.

*Proof.* Line L9 sets $b = z_1$ in iteration 1 and later replaces $b$ by $z_i$ exactly when $c(z_i) < c(b)$. $\square$

**Theorem 1 (correctness and termination).** GRASP stops after $K$ iterations and returns a cover $b$ that is a local minimum for drop and swap moves, with $c(b) = \min_k c(z_k)$.

*Proof.* Line L2 makes $K$ passes. Each pass stops by Lemmas 1 and 2, and the claims follow from Lemmas 2 and 3. $\square$

**Theorem 2 (the greedy bound, Chvátal).** If $\alpha = 0$, every cover built by lines L3 to L7 has $c(x) \le H(d) \cdot \mathrm{OPT}$, where $\mathrm{OPT}$ is the least cost of a cover. So GRASP with $\alpha = 0$ returns $b$ with $c(b) \le H(d) \cdot \mathrm{OPT}$.

*Proof.* With $\alpha = 0$, the RCL holds only sets of the least ratio, so each pass picks a set $j$ with $r_j = r_{\min}$. When set $j$ is picked and it covers $q$ new elements, give each of these elements the price $c_j / q = r_{\min}$. Each element gets a price once, and the prices of one pass add up to $c_j$, so $c(x)$ is the sum of all prices.

Take a set $T = S_t$ of an optimal cover, with $k = |T| \le d$ elements. List its elements in the order in which they are covered, $e_1, \ldots, e_k$, with ties in any order. Just before $e_i$ is covered, the elements $e_i, \ldots, e_k$ are uncovered, so $T$ has at least $k - i + 1$ uncovered elements, and $r_t \le c_t / (k - i + 1)$. The pass that covers $e_i$ picks a set of ratio $r_{\min} \le r_t$, so the price of $e_i$ is at most $c_t / (k - i + 1)$. Add over $i$: the prices of the elements of $T$ add up to at most $c_t H(k) \le c_t H(d)$.

Every element is in some set of the optimal cover, so the sum of all prices is at most the sum of $c_t H(d)$ over the sets of the optimal cover, which is $H(d) \cdot \mathrm{OPT}$. By Lemma 2 the local search does not raise the cost, so $c(b) \le c(z_1) \le c(x_1) \le H(d) \cdot \mathrm{OPT}$. $\blacksquare$

**Theorem 3 (independent iterations).** Suppose the random choices of line L7 come from an ideal source of random bits, and let $p$ be the probability that one iteration ends at an optimal cover. Then the probability that all $K$ iterations miss is $(1 - p)^K$.

*Proof.* Each iteration starts from the empty set and uses only its own random choices, so the $K$ iterations are independent and have the same distribution. Each misses with probability $1 - p$. $\square$

**What is not claimed.** The value of $p$ is not known in advance, and it can be 0: on the example of the page, with $\alpha = 0$ every iteration ends at cost 24 or 27, never at the optimum 23. For $\alpha > 0$, Theorem 2 does not hold, since line L7 can pick a set with a ratio above $r_{\min}$. A local minimum for drop and swap moves need not be optimal. GRASP has no guarantee of optimality for a fixed $K$.
