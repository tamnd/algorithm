---
title: Move-to-front is 2-competitive, no online rule beats 2 - 2/(n+1), and the expected cost is below 2 OPT - 1
proves: [time.worst, competitive-ratio, lower-bound, time.expected]
status: full
---

The model is the list update model of the page. A list holds $n$ distinct items. To access the item at position $i$ costs $i$. Right after an access, the accessed item may move closer to the front for free, one *free exchange* per position. Any swap of two neighbours at another time is a *paid exchange* of cost 1.

**Time of one request.** By the correctness proof, the loop of lines L2 and L3 runs $p - 1$ times when the item is at position $p$, and every other line runs at most once. Each line takes $O(1)$ time on the word RAM. So a request takes $\Theta(p)$ time, which is $\Theta(n)$ for $p = n$ and $\Theta(1)$ for $p = 1$. In the list update model the cost is exactly $p$.

## Part 1. The bound of Sleator and Tarjan

**Statement.** Let $A$ be any algorithm that serves a sequence $\sigma$ of $m$ requests from the same start list as MTF. Let $C_A$ be the sum of the access costs of $A$, $X_A$ the number of its paid exchanges and $F_A$ the number of its free exchanges. Then $C_{\mathrm{MTF}}(\sigma) \le 2C_A + X_A - F_A - m$.

**Setup.** Run MTF and $A$ side by side. Split the run into events: for each request, the access of both algorithms together with the move of MTF; then each free exchange of $A$ after that access; and each paid exchange of $A$, at the time that $A$ makes it. Let $\Phi$ be the number of unordered pairs $\{y, z\}$ of items that are in a different order in the list of MTF and in the list of $A$. Then $\Phi \ge 0$ always, and $\Phi = 0$ at the start because the lists are equal. For an event, let its amortized cost be the cost that MTF pays in it plus the change of $\Phi$. Summing over all events, the changes of $\Phi$ add up to $\Phi_{\mathrm{end}} - 0 \ge 0$, so

$$C_{\mathrm{MTF}}(\sigma) \le \text{sum of the amortized costs of all events.}$$

**Step 1: an access.** Let the request be $x$, at position $k$ in the list of MTF and at position $i$ in the list of $A$. Let $B$ be the set of the $k - 1$ items before $x$ in the list of MTF. Let $v$ be the number of items of $B$ that are after $x$ in the list of $A$. The other $k - 1 - v$ items of $B$ are before $x$ in the list of $A$, and there are only $i - 1$ such items, so $k - 1 - v \le i - 1$. MTF moves $x$ to the front. This changes the relative order of $x$ and $y$ for each $y \in B$ and of no other pair. For the $v$ items $y$ of $B$ after $x$ in $A$, the pair $\{x, y\}$ was an inversion and is not one now. For the $k - 1 - v$ other items of $B$, the pair was not an inversion and is one now. MTF pays $k$. So the amortized cost is

$$k + (k - 1 - v) - v = 2(k - 1 - v) + 1 \le 2(i - 1) + 1 = 2i - 1.$$

**Step 2: a free exchange of $A$.** It moves the accessed item $x$ one place forward in the list of $A$, past the item $y$ just before it. In the list of MTF, $x$ is first, since MTF moved it there in the same access. So before the exchange the pair $\{x, y\}$ is an inversion, and after it the pair is not. No other pair changes. MTF pays 0. The amortized cost is $-1$.

**Step 3: a paid exchange of $A$.** It swaps two neighbours in the list of $A$. Only the order of these two items changes, so $\Phi$ changes by $+1$ or $-1$. MTF pays 0. The amortized cost is at most $1$.

**Conclusion.** Summing Step 1 over the $m$ requests gives at most $\sum_t (2i_t - 1) = 2C_A - m$. Step 2 adds $-F_A$ and Step 3 adds at most $X_A$. Therefore $C_{\mathrm{MTF}}(\sigma) \le 2C_A + X_A - F_A - m$. Since $F_A \ge 0$, this also gives $C_{\mathrm{MTF}}(\sigma) \le 2(C_A + X_A) - m$, which is less than twice the total cost of $A$. $\blacksquare$

## Part 2. A lower bound for every deterministic online algorithm

**Statement.** Call an online algorithm $\alpha$-competitive if there is a number $b$, which may depend on $n$ but not on $\sigma$, with $\mathrm{cost}_{\mathrm{ON}}(\sigma) \le \alpha \cdot \mathrm{OPT}(\sigma) + b$ for every $\sigma$. If a deterministic online algorithm ON is $\alpha$-competitive on lists of $n$ items, then $\alpha \ge 2n/(n + 1)$.

*Proof.* Fix $m \ge 1$. Because ON is deterministic, we can simulate it and build $\sigma$ one request at a time: each request is the item that is last in the list of ON at that moment. Each access costs ON exactly $n$, so $\mathrm{cost}_{\mathrm{ON}}(\sigma) \ge mn$.

For each of the $n!$ orders $\pi$ of the items, consider the offline algorithm that first sorts the start list into the order $\pi$ by swaps of neighbours (bubble sort uses at most $n(n-1)/2$ swaps) and then never changes the list. Its cost is at most $n(n-1)/2 + \sum_{t=1}^{m} \mathrm{pos}_\pi(x_t)$. For a fixed item, its position in a uniformly random order $\pi$ is uniform on $\{1, \ldots, n\}$ and has mean $(n + 1)/2$. By linearity of expectation, the mean of $\sum_t \mathrm{pos}_\pi(x_t)$ over all $\pi$ is $m(n + 1)/2$, so some $\pi$ has a sum at most this mean. Hence $\mathrm{OPT}(\sigma) \le m(n + 1)/2 + n(n - 1)/2$.

Then $mn \le \alpha\,(m(n + 1)/2 + n(n - 1)/2) + b$ for every $m$. Divide by $m$ and let $m \to \infty$: $n \le \alpha (n + 1)/2$, so $\alpha \ge 2n/(n + 1) = 2 - 2/(n + 1)$. $\blacksquare$

## Part 3. Expected cost under independent requests

**Statement.** Let the requests be independent, and let each be item $j$ with probability $p_j > 0$, where $\sum_j p_j = 1$. Number the items so that $p_1 \ge p_2 \ge \cdots \ge p_n$. Let $E_t$ be the expected cost of the $t$-th request of MTF. Then $E_t \to E_{\mathrm{MTF}} = 1 + 2\sum_{j<k} p_j p_k/(p_j + p_k)$ as $t \to \infty$, and $E_{\mathrm{MTF}} \le 2E_{\mathrm{OPT}} - 1$, where $E_{\mathrm{OPT}} = \sum_k k\, p_k$ is the least expected cost of a fixed order.

*Step 1: the order of two items.* Fix two items $y \ne z$ and let $q = p_y + p_z$. By the correctness of MTF-ACCESS, just before request $t$, the item $y$ is before $z$ exactly when the last of the requests $1, \ldots, t - 1$ that is for $y$ or $z$ is for $y$, or when no such request exists and $y$ is before $z$ in the start list. The last such request is request $s$ with probability $q(1 - q)^{t - 1 - s}$, and given that request $s$ is for $y$ or $z$, it is for $y$ with probability $p_y/q$, by independence. So

$$\Pr[y \text{ before } z] = \sum_{s=1}^{t-1} (1 - q)^{t-1-s}\, p_y + \delta\,(1 - q)^{t - 1} = \frac{p_y}{q}\left(1 - (1 - q)^{t-1}\right) + \delta\,(1 - q)^{t-1},$$

with $\delta \in \{0, 1\}$. Since $0 < q \le 1$, this tends to $p_y/(p_y + p_z)$.

*Step 2: the cost.* The cost of a request for $z$ is 1 plus the number of items before $z$. Request $t$ is independent of the list before it, so by linearity

$$E_t = \sum_z p_z \Big(1 + \sum_{y \ne z} \Pr[y \text{ before } z]\Big) \to 1 + \sum_z \sum_{y \ne z} \frac{p_z\, p_y}{p_y + p_z} = 1 + 2 \sum_{j < k} \frac{p_j\, p_k}{p_j + p_k}.$$

*Step 3: the comparison.* For $j < k$, $p_j \ge p_k$, so $p_j/(p_j + p_k) \le 1$ and $p_j p_k/(p_j + p_k) \le p_k$. Hence

$$E_{\mathrm{MTF}} \le 1 + 2\sum_{j<k} p_k = 1 + 2 \sum_k (k - 1)\, p_k = 1 + 2(E_{\mathrm{OPT}} - 1) = 2E_{\mathrm{OPT}} - 1.$$

*Step 4: the best fixed order.* A fixed order that puts item $j$ at position $r_j$ has expected cost $\sum_j r_j p_j$. If some items $a, b$ have $r_a < r_b$ and $p_a < p_b$, swapping their positions changes the cost by $(r_b - r_a)(p_a - p_b) < 0$. So a least-cost order has the $p$ values in non-increasing order, and its cost is $\sum_k k\,p_k = E_{\mathrm{OPT}}$; ties between equal $p$ values do not change the cost. $\blacksquare$
