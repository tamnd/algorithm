---
title: The first-price auction sells to the highest eligible bid at that bid, and the bid a(n-1)v/(a(n-1)+1) is a symmetric equilibrium for values with CDF v^a
proves: [correctness]
status: full
---

We use the pseudocode of the page, with bids $b_1, \ldots, b_n$ and a reserve $r$.

**Claim 1 (the outcome).** FIRST-PRICE returns the smallest index $w$ among the bids $b_i \ge r$ of largest value, and the price $b_w$. If no bid is at least $r$, it returns no winner.

*Proof.* Invariant of the loop of line L2: before the iteration for $i$, $w$ is the smallest index among the bids $b_j \ge r$ with $j < i$ of largest value, or NIL if there is none. It holds for $i = 1$ with $w = \mathrm{NIL}$. In iteration $i$, line L3 makes $i$ the leader exactly when $b_i \ge r$ and $b_i$ is strictly larger than every earlier eligible bid. A bid equal to the leader's bid does not replace it, so the smallest index is kept. At the end the invariant covers all bids, and lines L4 and L5 return the claimed result. $\square$

**Claim 2 (equilibrium).** Let the $n \ge 2$ values be independent with CDF $F(v) = v^a$ on $[0, 1]$, for a real $a > 0$, and let $k = a(n-1)$. With $r = 0$, the strategy $\beta(v) = \frac{k}{k+1} v$ for every bidder is a Bayes-Nash equilibrium. For uniform values ($a = 1$) it is $\beta(v) = \frac{n-1}{n} v$.

*Proof.* Fix bidder $i$ with value $v$, and let the others use $\beta$. The bid $\beta(v_j)$ of each other bidder has no atom, and $\beta$ is strictly increasing with range $[0, \beta(1)]$.

- A bid $b > \beta(1)$ wins with probability 1 and gives $v - b < v - \beta(1)$, so it is worse than the bid $\beta(1)$.
- A bid $b \in [0, \beta(1)]$ equals $\beta(t)$ for one $t \in [0, 1]$. Ties have probability 0. It wins when every other value is below $t$, which has probability $F(t)^{n-1} = t^k$. So its expected utility is

$$u(v, t) = (v - \beta(t))\, t^k = v t^k - \tfrac{k}{k+1} t^{k+1}.$$

The derivative in $t$ is $k v t^{k-1} - k t^k = k t^{k-1}(v - t)$. It is positive for $0 < t < v$ and negative for $t > v$. So $u(v, \cdot)$ has its maximum over $[0, 1]$ at $t = v$, and the bid $\beta(v)$ is a best response, with utility $u(v, v) = \frac{v^{k+1}}{k+1} \ge 0$. This holds for every $v$, so $\beta$ is a symmetric equilibrium. $\square$

The bid equals $\mathbb{E}[Y \mid Y < v]$, where $Y$ is the largest of the other $n - 1$ values: $Y$ has CDF $t^k$, and $\int_0^v t \, d(t^k) / v^k = \frac{k}{k+1} v$. The general form of this fact and its uniqueness are on the page on the [equilibrium of the symmetric first-price auction](/first-price-auction-equilibrium/).

**Claim 3 (revenue with uniform values).** In the equilibrium of Claim 2 with $a = 1$, the expected revenue is $\frac{n-1}{n+1}$.

*Proof.* The highest bid comes from the highest value $Y_{(1)}$, whose CDF is $t^n$ and whose mean is $\frac{n}{n+1}$. The price is $\beta(Y_{(1)}) = \frac{n-1}{n} Y_{(1)}$, with mean $\frac{n-1}{n} \cdot \frac{n}{n+1} = \frac{n-1}{n+1}$. $\square$

This is the mean of the second-highest value, the revenue of the Vickrey auction, as the revenue equivalence theorem says.

**Cost.** The loop runs $n$ times with at most two comparisons each. The time is $\Theta(n)$ and the extra space is $O(1)$.
