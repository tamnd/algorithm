---
title: The all-pay auction picks the highest bid and charges every bid, and its equilibria with uniform and with known values
proves: [correctness]
status: full
---

We use the pseudocode of the page, with bids $b_1, \ldots, b_n$ and $n \ge 1$.

**Claim 1 (the outcome).** ALL-PAY returns the smallest index $w$ with $b_w = \max_i b_i$ and the payments $p_i = b_i$ for all $i$.

*Proof.* Invariant of the loop of line L2: before the iteration for $i$, $w$ is the smallest index among $1, \ldots, i-1$ with the largest bid. Line L1 makes it true for $i = 2$. Line L3 changes $w$ only on a strictly larger bid, so it keeps the smallest index among equal largest bids. At the end the invariant covers all bids. Line L4 sets each payment to the bid. $\square$

**Claim 2 (symmetric equilibrium with uniform values).** Let the $n \ge 2$ values be independent and uniform on $[0, 1]$. Then $\beta(v) = \frac{n-1}{n} v^n$ for every bidder is a Bayes-Nash equilibrium, and the expected revenue is $\frac{n-1}{n+1}$.

*Proof.* Fix bidder $i$ with value $v$, and let the others use $\beta$, which is strictly increasing and continuous, with range $[0, \beta(1)]$, and has no atoms. A bid $b > \beta(1)$ wins for sure and costs more than $\beta(1)$, which also wins for sure, so it is worse. A bid $b \in [0, \beta(1)]$ is $\beta(t)$ for one $t \in [0, 1]$, wins when all other values are below $t$ (ties have probability 0), and is paid in every case. So

$$u(v, t) = v\, t^{n-1} - \tfrac{n-1}{n} t^n, \qquad \frac{\partial u}{\partial t} = (n-1) t^{n-2} (v - t).$$

The derivative is positive for $t < v$ and negative for $t > v$, so $t = v$ is the best choice, with $u(v, v) = v^n / n \ge 0$. Hence $\beta$ is a best response to itself.

Each bidder pays $\beta(v_i)$, and $\mathbb{E}[v_i^n] = \frac{1}{n+1}$. By [linearity of expectation](/linearity-of-expectation/), the expected revenue is $n \cdot \frac{n-1}{n} \cdot \frac{1}{n+1} = \frac{n-1}{n+1}$. $\square$

The same bid follows from revenue equivalence: in the Vickrey auction a bidder of value $v$ pays the highest other value when it is below $v$, which has expectation $\int_0^v t \, d(t^{n-1}) = \frac{n-1}{n} v^n$. In the all-pay auction a bidder pays its bid for sure, so the bid must equal this expected payment.

**Claim 3 (two bidders with known values).** Let two bidders have values $v_1 \ge v_2 > 0$ known to both. Let bidder 1 bid uniformly on $[0, v_2]$, and let bidder 2 bid 0 with probability $1 - v_2/v_1$ and otherwise uniformly on $[0, v_2]$, so that its bid has the CDF $G_2(b) = 1 - v_2/v_1 + b/v_1$ on $[0, v_2]$. This is a mixed Nash equilibrium, with expected payoffs $v_1 - v_2$ and $0$.

*Proof.* Bidder 1's bid has no atom, so ties have probability 0 except when both bid 0, which has probability 0 because bidder 1 bids 0 with probability 0. Against bidder 2, a bid $b \in [0, v_2]$ of bidder 1 wins with probability $G_2(b)$ and gives $v_1 G_2(b) - b = v_1 - v_2$, the same for each $b$. A bid $b > v_2$ wins for sure and gives $v_1 - b < v_1 - v_2$. So every bid in the support is a best response. Against bidder 1, a bid $b \in [0, v_2]$ of bidder 2 wins with probability $b / v_2$ and gives $v_2 \cdot b/v_2 - b = 0$, and a bid above $v_2$ gives $v_2 - b < 0$. So every bid in the support of bidder 2 is a best response as well. $\square$

**Cost.** The loop runs $n - 1$ times with one comparison each, and line L4 copies $n$ bids. The time is $\Theta(n)$ and the extra space is $O(n)$ for the payments.
