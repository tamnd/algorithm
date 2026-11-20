---
title: McAfee's trade reduction mechanism is truthful, individually rational, weakly budget balanced and loses at most one trade
proves: [correctness]
status: full
---

We use the pseudocode of the page. Buyers report bids and sellers report asks. Line L1 ranks the buyers as $b_1 \ge b_2 \ge \cdots$ and the sellers as $s_1 \le s_2 \le \cdots$, with ties broken by index. Line L2 sets $k$ to the largest $t$ with $b_t \ge s_t$. Because the $b_t$ do not increase and the $s_t$ do not decrease, the set $\{t : b_t \ge s_t\}$ is a prefix $\{1, \ldots, k\}$ of the ranks. We write $p_0 = (b_{k+1} + s_{k+1})/2$ when both traders of rank $k + 1$ exist.

**Claim 1 (the efficient trades).** With truthful reports, the largest gain from trade over all sets of trading pairs is $\mathrm{OPT} = \sum_{t=1}^{k} (b_t - s_t)$.

*Proof.* A set of $q$ trading pairs uses $q$ buyers and $q$ sellers. Its gain is at most the sum of the $q$ largest bids minus the sum of the $q$ smallest asks, which is $g(q) = \sum_{t=1}^{q} (b_t - s_t)$. The terms $b_t - s_t$ do not increase in $t$, they are at least 0 for $t \le k$ and below 0 for $t > k$. So $g$ is largest at $q = k$. $\square$

**Claim 2 (feasibility, budget balance and the trade loss).** The output has as many buyers as sellers. Every trading buyer pays at most its bid and every trading seller receives at least its ask. The buyer price is at least the seller price, so the auctioneer never adds money. The gain from trade of the output is at least $\mathrm{OPT} - (b_k - s_k) \ge (1 - 1/k)\,\mathrm{OPT}$ when $k \ge 1$.

*Proof.* If $k = 0$, line L3 returns no trade. Line L6 returns the top $k$ of each side at the price $p_0$, and it runs only if $s_k \le p_0 \le b_k$. So each trading buyer has $b_t \ge b_k \ge p_0$ and each trading seller has $s_t \le s_k \le p_0$. Line L7 returns the top $k - 1$ of each side. Each buyer pays $b_k \le b_t$ and each seller receives $s_k \ge s_t$, and $b_k \ge s_k$ by the definition of $k$, so the auctioneer keeps $(k - 1)(b_k - s_k) \ge 0$. Line L6 trades all $k$ pairs of Claim 1. Line L7 trades all of them but the pair of rank $k$, whose gain $b_k - s_k$ is the smallest of the $k$ nonnegative terms. So it is at most $\mathrm{OPT}/k$. $\square$

**Claim 3 (a threshold for each buyer).** Fix a buyer $i$ and the reports of all other traders. There is a number $\theta$ that depends only on these reports, such that buyer $i$ trades if its bid $b > \theta$, does not trade if $b < \theta$, and pays exactly $\theta$ whenever it trades.

*Proof.* Let $c_1 \ge c_2 \ge \cdots$ be the bids of the other buyers, ranked as in line L1, and put $c_0 = +\infty$. Let $s_1 \le s_2 \le \cdots$ be the asks. Let $h$ be the largest $t$ with $c_t \ge s_t$, the number of efficient trades without $i$. If there is no seller, nobody trades, and $\theta = +\infty$ works. So assume $s_1$ exists.

Let $b'_1 \ge b'_2 \ge \cdots$ be the ranked bids with $b$ added. The value $b'_t$ is the $t$-th largest of a list that contains the list $c$ and is one longer, so $c_t \le b'_t \le c_{t-1}$. Then $b'_h \ge c_h \ge s_h$ and $b'_{h+2} \le c_{h+1} < s_{h+2}$, hence $k \in \{h, h + 1\}$. If buyer $i$ has a rank $r$, the values below it shift down: $b'_t = c_{t-1}$ for $t > r$. If buyer $i$ trades, it has rank $r \le k$ in line L6 and $r \le k - 1$ in line L7.

*Case I: $s_{h+1}$ exists and $c_h \ge s_{h+1}$.* Here $b'_{h+1} \ge \min(b, c_h)$, so $k = h + 1$ when $b \ge s_{h+1}$. If $b < s_{h+1}$, then $b < c_h$ and $b'_{h+1} \le \max(c_{h+1}, b) < s_{h+1}$, so $k = h$ and buyer $i$ has a rank above $h$; it does not trade. Now let $b \ge s_{h+1}$, so $k = h + 1$. Since $b \ge s_{h+1} > c_{h+1}$, buyer $i$ has a rank $r \le h + 1$, and $b'_{h+2} = c_{h+1}$. So $p_0 = q := (c_{h+1} + s_{h+2})/2$ does not depend on $b$, and $b'_{h+1} = \min(b, c_h)$.

- *(a)* If $q$ exists and $s_{h+1} \le q \le c_h$, set $\theta = q$. For $b \ge q$, line L5 holds and buyer $i$ trades at $q$ in line L6. For $s_{h+1} \le b < q$, we get $b'_{h+1} = b < q$, so line L7 runs, and buyer $i$ has rank $h + 1 = k$ and does not trade.
- *(b)* Otherwise set $\theta = c_h$. Line L5 fails for every $b \ge s_{h+1}$: either $q$ does not exist, or $q < s_{h+1}$, or $q > c_h \ge b'_{h+1}$. So line L7 runs with $k = h + 1$. Buyer $i$ trades if and only if its rank is at most $h$, which holds for $b > c_h$ and fails for $b < c_h$. Then $b'_{h+1} = c_h$, so it pays $c_h$.

*Case II: $s_{h+1}$ does not exist, or $c_h < s_{h+1}$.* Then $h \ge 1$, because $c_0 = +\infty \ge s_1$. We have $k = h$ for every $b$: if $s_{h+1}$ does not exist there are only $h$ sellers, and otherwise $b'_{h+1} = \max(c_{h+1}, \min(b, c_h)) < s_{h+1}$. If buyer $i$ has rank at most $h$, then $b'_{h+1} = c_h$, so $p_0 = q := (c_h + s_{h+1})/2$, which does not depend on $b$. Note $q > c_h \ge s_h$.

- *(a)* If $s_{h+1}$ exists and $c_{h-1} \ge q$, set $\theta = q$. For $b \ge q$, buyer $i$ ranks above $c_h < q$, so its rank is at most $h$, and $b'_h = \min(b, c_{h-1}) \ge q \ge s_h$. Line L5 holds and $i$ trades at $q$. For $b < q$, either buyer $i$ has a rank above $h$, or it has rank $h$ with $b'_h = b < q$, so line L7 runs and the trader of rank $h$ does not trade. In both cases $i$ does not trade.
- *(b)* Otherwise set $\theta = c_{h-1}$. If $s_{h+1}$ does not exist, line L7 runs. If it exists, $b'_h \le c_{h-1} < q$ when $i$ has rank at most $h$, so again line L7 runs. Buyer $i$ trades if and only if its rank is at most $h - 1$, which holds for $b > c_{h-1}$ and fails for $b < c_{h-1}$, and then it pays $b'_h = c_{h-1}$.

In every case the price paid by buyer $i$ is $\theta$, and the outcome at $b = \theta$ only depends on the tie rule. $\square$

**Claim 4 (truthful reporting is a dominant strategy, and it is individually rational).** For every buyer $i$ with value $v$, every bid $b$ and all reports of the others, the utility of bidding $v$ is at least the utility of bidding $b$ and at least 0. The same holds for every seller.

*Proof.* Take $\theta$ from Claim 3. If $v > \theta$, the bid $v$ trades and gives $v - \theta > 0$, and every other bid gives $v - \theta$ or 0. If $v < \theta$, the bid $v$ gives 0, and any bid that trades gives $v - \theta < 0$. If $v = \theta$, every bid gives 0. For sellers, replace each bid $b$ by $-b$ and each ask $s$ by $-s$ and exchange the two sides. This maps the ranking, the index $k$, the price $p_0$, the test of line L5 and the prices of line L7 to the same objects of the other side, so the mechanism is symmetric, and Claim 3 holds for sellers with the inequalities reversed. $\square$

Claims 2 and 4 together are the theorem of McAfee (1992): the mechanism is dominant-strategy incentive compatible, ex post individually rational and weakly budget balanced, and with truthful reports it loses at most the least valuable of the $k$ efficient trades.
