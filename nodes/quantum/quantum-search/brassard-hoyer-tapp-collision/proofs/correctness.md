---
title: BHT-COLLISION returns a collision after k + O(sqrt(N/(r k))) expected queries
proves: [correctness]
status: full
---

We use the pseudocode of the page. $F : X \to Y$ is $r$-to-one with $r \ge 2$ and $|X| = N$, $K \subseteq X$ has $k$ elements, and $H(x) = 1$ if and only if $x \notin K$ and $F(x) = F(x_0)$ for some $x_0 \in K$. We assume $t = (r-1)k \le N/2$; this holds for $k = \sqrt[3]{N/r}$ as soon as $N \ge 8r$, since then $(r-1)k \le r (N/r)^{1/3} \le N/2$.

**Claim.** BHT-COLLISION returns a pair $x_0 \ne x_1$ with $F(x_0) = F(x_1)$. The expected number of queries is at most $k + 2\big(\frac{\pi}{4}\sqrt{N/((r-1)k)} + 1\big)$, which is $k + O(\sqrt{N/(rk)})$.

*Proof.* **Step 1: a collision in $K$.** If line L4 finds two pairs with the same value, their inputs are different elements of $K$, and line L5 returns a collision. The algorithm then made $k$ queries.

**Step 2: the solutions of $H$.** Assume the values $F(x)$, $x \in K$, are distinct. Since $F$ is $r$-to-one, each $x_0 \in K$ has exactly $r - 1$ other inputs with the value $F(x_0)$, and none of them is in $K$, because the values in $K$ are distinct. Two different $x_0, x_0' \in K$ have different values, so their sets of partners are disjoint. So the set $\{x : H(x) = 1\}$ is the disjoint union of these sets, and it has exactly $t = (r-1)k$ elements. Each solution $x_1$ has a unique $x_0 \in K$ with $F(x_0) = F(x_1)$, and $x_0 \ne x_1$ since $x_1 \notin K$.

**Step 3: one round of search.** Let $\sin\theta = \sqrt{t/N}$, with $0 < \theta \le \pi/4$ since $t \le N/2$, and let $j = \lfloor \pi/(4\theta) \rfloor$. By the analysis of [Grover search](/grover-search/), after $j$ iterations with the phase oracle of $H$, the measurement gives a solution with probability $p = \sin^2((2j+1)\theta)$. Since $\pi/(4\theta) - 1 < j \le \pi/(4\theta)$, the angle $(2j+1)\theta$ lies in $(\pi/2 - \theta, \pi/2 + \theta]$, so $p \ge \cos^2\theta = 1 - t/N \ge 1/2$. A phase query of $H$ uses one query of $F$ and a lookup in the sorted table, which makes no query. So one round makes $j$ queries in line L7 and one in line L9.

**Step 4: the output.** Line L9 checks $H(x_1) = 1$ with one query, so line L10 runs only when $x_1$ is a solution. By Step 2, the lookup finds the unique $x_0 \in K$ with $F(x_0) = F(x_1)$, and $x_0 \ne x_1$. So every returned pair is a collision.

**Step 5: the expected count.** The rounds are independent, and each succeeds with probability $p \ge 1/2$. So the number of rounds is geometric with mean $1/p \le 2$. The expected number of queries is $k + (j + 1)/p \le k + 2(j + 1)$. Since $\theta \ge \sin\theta = \sqrt{t/N}$, we have $j \le \pi/(4\theta) \le \frac{\pi}{4}\sqrt{N/t}$. With $t = (r-1)k \ge rk/2$ this gives $j \le \frac{\pi}{4}\sqrt{2N/(rk)}$, so the expected count is $k + O(\sqrt{N/(rk)})$. Steps 1 and 5 together prove the claim. $\blacksquare$

**The choice of $k$.** The function $g(k) = k + c\sqrt{N/(rk)}$ has $g'(k) = 1 - \frac{c}{2}\sqrt{N/r}\, k^{-3/2}$, which is zero at $k = (c/2)^{2/3}(N/r)^{1/3}$. At this point both terms are $\Theta((N/r)^{1/3})$. So $k = \Theta((N/r)^{1/3})$ gives $O((N/r)^{1/3})$ expected queries, and no other choice of $k$ does better than a constant factor.

**Space.** The table holds $k$ pairs and nothing else grows with $N$, apart from the $\lceil \lg N \rceil$ qubits of the search register and the work qubits for $F$ and for one lookup.
