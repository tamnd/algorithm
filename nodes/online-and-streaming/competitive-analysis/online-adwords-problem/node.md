---
tag: PHX39Y
kind: problem
slug: online-adwords-problem
name: Online adwords problem
aliases:
- online budgeted allocation
- adwords problem
- online budgeted matching
area: online-and-streaming/competitive-analysis
level: advanced
summary: Queries arrive online with a bid from each advertiser and must be given at once to one advertiser, who pays up to its budget; the goal is the total revenue. The best ratio for small bids is 1 - 1/e.
prereqs: [online-bipartite-matching, competitive-ratio, lp-duality]
see_also: [balance-algorithm, ranking-algorithm, online-primal-dual, b-matching, weak-duality, online-knapsack-problem]
sources:
  - paper: doi:10.1145/1284320.1284321
    title: "Aranyak Mehta, Amin Saberi, Umesh Vazirani and Vijay Vazirani, AdWords and generalized online matching, Journal of the ACM 54(5) (2007), Article 22"
    locator: the problem, the tradeoff function psi(f) = 1 - e^(f - 1), the bound 1 - 1/e for small bids, and the upper bound for deterministic algorithms
  - paper: doi:10.1007/978-3-540-75520-3_24
    title: "Niv Buchbinder, Kamal Jain and Joseph (Seffi) Naor, Online primal-dual algorithms for maximizing ad-auctions revenue, Algorithms ESA 2007, LNCS 4698, 253-264"
    locator: the primal-dual algorithm, the ratio (1 - 1/c)(1 - R_max), and its link to the tradeoff function
  - paper: doi:10.1561/0400000024
    title: "Niv Buchbinder and Joseph (Seffi) Naor, The design of competitive online algorithms via a primal-dual approach, Foundations and Trends in Theoretical Computer Science 3(2-3) (2009), 93-263"
    locator: Chapter 10, the ad auctions problem and its primal-dual analysis
  - paper: doi:10.1561/0400000057
    title: "Aranyak Mehta, Online matching and ad allocation, Foundations and Trends in Theoretical Computer Science 8(4) (2013), 265-368"
    locator: the chapters on the adwords problem, the greedy bound 1/2 and the small bids assumption
---

The online adwords problem is the budgeted form of [online bipartite matching](/online-bipartite-matching/). Advertisers with daily budgets are known in advance, search queries arrive one at a time, and each query comes with a bid from each interested advertiser. The query must be given at once to one advertiser, who pays its bid, but never more in total than its budget. Mehta, Saberi, Vazirani and Vazirani (2007) gave an algorithm with ratio $1 - 1/e$ when each bid is small compared with its budget, and showed that no deterministic algorithm does better; Buchbinder, Jain and Naor (2007) gave a primal-dual proof of the same bound.

## In plain words

A search engine sells ad space. Each advertiser has a daily budget. Each time a user searches, the advertisers who care about the search name a price, and the engine shows one ad and charges that price, as long as the advertiser has money left.

Showing the highest price is natural, but it can spend the budget of an advertiser who is the only buyer for later searches. Those later searches then earn nothing. A good rule weighs each price by how much of that advertiser's budget is still left, and gives the search to an advertiser with plenty of money left unless the price gap is large. With many small prices, this earns at least about two thirds of what the best plan in hindsight earns.

## Definition

**Input.** A set of advertisers $i = 1, \ldots, k$ with budgets $B_i > 0$, known at the start. Queries $j = 1, \ldots, n$ arrive one at a time. When query $j$ arrives, the bids $b_{ij} \ge 0$ for all $i$ are revealed. The sequence $\sigma$ is the list of queries with their bids.

**Online rule.** Before query $j + 1$ arrives, the algorithm gives query $j$ to one advertiser or to none, for good. If $S_i$ is the total of the bids of the queries given to $i$, the revenue is

$$\mathrm{ALG}(\sigma) = \sum_{i} \min(S_i, B_i).$$

**Offline optimum.** $\mathrm{OPT}(\sigma)$ is the largest revenue of any assignment, chosen with the whole input known. It is at most the value of the LP

$$\max \sum_{i, j} b_{ij} y_{ij} \ \text{ s.t. } \ \sum_j b_{ij} y_{ij} \le B_i \ (\text{each } i), \ \sum_i y_{ij} \le 1 \ (\text{each } j), \ y \ge 0,$$

whose [dual](/dual-linear-program/) is

$$\min \sum_i B_i x_i + \sum_j z_j \ \text{ s.t. } \ b_{ij} x_i + z_j \ge b_{ij} \ (\text{each } i, j), \ x, z \ge 0.$$

**Small bids.** Let $R_{\max} = \max_{i,j} b_{ij}/B_i$. The small bids assumption is $R_{\max} \to 0$: each bid is a tiny fraction of its budget.

**Notation and cost model.**

| Symbol | Meaning |
|---|---|
| $\sigma$ | the sequence of queries with their bids |
| $\mathrm{ALG}(\sigma)$, $\mathrm{OPT}(\sigma)$ | the revenue of the online algorithm and the best offline revenue |
| $c$ | the competitive ratio, with $c \le 1$; in Theorem 2, $c$ is also the constant $(1 + R_{\max})^{1/R_{\max}}$ |
| $k$, $n$ | the number of advertisers and of queries |
| $f_i$ | the fraction $S_i / B_i$ of the budget of $i$ spent so far |

This is a maximization problem, with the convention $\mathrm{ALG}(\sigma) \ge c \cdot \mathrm{OPT}(\sigma)$, $c \le 1$, and no additive term. A randomized algorithm is measured in expectation against an [oblivious adversary](/oblivious-adversary/).

## Variants

- **Online bipartite matching.** All bids and budgets equal to 1. Then Ranking gets $1 - 1/e$, and deterministic algorithms get only $1/2$.
- **$b$-matching.** All bids 1 and all budgets $b$. [Balance](/balance-algorithm/) gets $1 - (1 + 1/b)^{-b}$.
- **Vertex weights.** If $b_{ij} \in \{0, w_i\}$ and $B_i = w_i$, each advertiser takes one query, and the problem is vertex-weighted online matching. The perturbed Ranking of Aggarwal, Goel, Karande and Mehta (2011) gets $1 - 1/e$ there, although the bids are not small.
- **Stochastic arrivals.** If queries arrive in random order or are drawn i.i.d. from a known distribution, ratios close to 1 are possible for small bids, and the [online primal-dual](/online-primal-dual/) method with learned prices is used.
- **Display ads with free disposal.** An advertiser has a cap on the number of impressions, and an impression may later be replaced by a better one. This is the edge-weighted matching problem with free disposal.

## Examples

Take two advertisers $A$ and $B$ with budgets 100. The first 100 queries have bids 1 from $A$ and 0.99 from $B$. The next 100 queries have a bid 1 from $A$ only.

| Algorithm | first 100 queries | last 100 queries | revenue | ratio |
|---|---|---|---|---|
| offline optimum | all to $B$ | all to $A$ | $99 + 100 = 199$ | 1 |
| greedy (highest bid) | all to $A$ | none ($A$ is out of budget) | 100 | 0.503 |
| MSVV, $\psi(f) = 1 - e^{f-1}$ | 50 to $A$, 50 to $B$ | 50 to $A$ | 149.5 | 0.751 |
| primal-dual of Theorem 2 | 50 to $A$, 50 to $B$ | 51 to $A$, 50 paid | 149.5 | 0.751 |

The dual built by the primal-dual algorithm has value $238.8$, an upper bound on $\mathrm{OPT}$ certified by the run itself. If the bid of $B$ is $1 - \varepsilon$ instead of $0.99$, greedy still gets 100 and the optimum is $200 - 100\varepsilon$, so Theorem 1 is tight.

## Known algorithms

- **Greedy.** Give query $j$ to the advertiser with the largest $\min(b_{ij}, B_i - S_i)$. Ratio $1/2$ for every bid size (Theorem 1).
- **MSVV.** Give query $j$ to the advertiser that maximizes $b_{ij}\,\psi(f_i)$ with $\psi(f) = 1 - e^{f-1}$. Ratio $1 - 1/e$ as $R_{\max} \to 0$ (Mehta, Saberi, Vazirani and Vazirani 2007, by a factor-revealing LP). With unit bids it is [Balance](/balance-algorithm/).
- **Primal-dual (Buchbinder, Jain and Naor 2007).** Give query $j$ to the advertiser that maximizes $b_{ij}(1 - x_i)$, then raise $x_i$ multiplicatively. Ratio $(1 - 1/c)(1 - R_{\max})$ with $c = (1 + R_{\max})^{1/R_{\max}}$ (Theorem 2). It is the same as MSVV in the limit.
- **General bids.** Huang, Zhang and Zhang (2020) gave the first algorithm with a ratio above $1/2$ for arbitrary bids, about $0.5016$, by a randomized method.

## Bounds

Theorems 1 and 2 are proved here. The bound for MSVV by a factor-revealing LP is only cited.

**Theorem 1 (greedy is 1/2-competitive).** If each query goes to the advertiser with the largest $\min(b_{ij}, B_i - S_i)$ (or to none if all are 0), then $\mathrm{ALG} \ge \mathrm{OPT}/2$.

*Proof.* Let $O_i$ be the set of queries that a fixed optimum gives to $i$, so $\mathrm{OPT} = \sum_i \min(B_i, \sum_{j \in O_i} b_{ij})$. Let $g_j$ be the revenue of greedy on query $j$, let $r_i(j)$ be the budget of $i$ left just before query $j$, and let $A_i$ be the final revenue of greedy from $i$. Greedy picks the largest effective bid, so $g_j \ge \min(b_{ij}, r_i(j))$ for each $i$. Fix $i$.

- If $b_{ij} \le r_i(j)$ for all $j \in O_i$, then $\sum_{j \in O_i} b_{ij} \le \sum_{j \in O_i} g_j$.
- Otherwise some $j_0 \in O_i$ has $b_{ij_0} > r_i(j_0)$, so $g_{j_0} \ge r_i(j_0)$, and the optimum gets at most $B_i = (B_i - r_i(j_0)) + r_i(j_0) \le A_i + g_{j_0}$ from $i$.

In both cases the optimum gets at most $A_i + \sum_{j \in O_i} g_j$ from $i$. The sets $O_i$ are disjoint, so $\mathrm{OPT} \le \sum_i A_i + \sum_j g_j = 2\,\mathrm{ALG}$. $\square$

**Theorem 2 (Buchbinder, Jain and Naor).** Let $c = (1 + R_{\max})^{1/R_{\max}}$. Run this algorithm, with all $x_i = 0$ at the start: when query $j$ arrives, pick $i$ that maximizes $b_{ij}(1 - x_i)$. If this value is not positive, do nothing and set $z_j = 0$. Otherwise give $j$ to $i$, set $z_j = b_{ij}(1 - x_i)$, and set

$$x_i \leftarrow x_i \Big(1 + \frac{b_{ij}}{B_i}\Big) + \frac{b_{ij}}{(c - 1) B_i}.$$

Then $\mathrm{ALG} \ge (1 - 1/c)(1 - R_{\max})\,\mathrm{OPT}$. As $R_{\max} \to 0$, $c \to e$ and the ratio tends to $1 - 1/e$.

*Proof.* Let $P$ be the sum of the bids of the given queries, which counts a bid even when it overruns the budget, and let $D = \sum_i B_i x_i + \sum_j z_j$.

*Step 1: $D = \frac{c}{c-1} P$.* When $j$ goes to $i$, $D$ grows by $B_i \Delta x_i + z_j = b_{ij} x_i + \frac{b_{ij}}{c - 1} + b_{ij}(1 - x_i) = \frac{c}{c-1} b_{ij}$, and $P$ grows by $b_{ij}$.

*Step 2: the final $(x, z)$ is dual feasible.* The values $x_i$ never decrease. At the time of query $j$, $z_j \ge b_{ij}(1 - x_i)$ for every $i$, by the choice of the maximum (and $z_j = 0 \ge b_{ij}(1 - x_i)$ when the maximum is not positive). So with the final $x_i$, $z_j \ge b_{ij}(1 - x_i)$ still holds, that is $b_{ij} x_i + z_j \ge b_{ij}$. By [weak duality](/weak-duality/), $D \ge \mathrm{OPT}$.

*Step 3: overruns are small.* Let $S_i$ be the total of the bids given to $i$. By induction, $x_i \ge (c^{S_i/B_i} - 1)/(c - 1)$. It holds at the start, and the update gives

$$x_i + \frac{1}{c-1} \leftarrow \Big(x_i + \frac{1}{c-1}\Big)\Big(1 + \frac{b_{ij}}{B_i}\Big) \ge \frac{c^{S_i/B_i}}{c-1} \, c^{b_{ij}/B_i},$$

because $\ln(1 + t)/t$ is decreasing, so $\ln(1 + t) \ge t \ln(1 + R_{\max})/R_{\max} = t \ln c$ for $0 < t = b_{ij}/B_i \le R_{\max}$. So once $S_i \ge B_i$, $x_i \ge 1$ and $i$ gets no more queries. Before its last query $S_i < B_i$, so in the end $S_i < B_i + b_{ij} \le (1 + R_{\max}) B_i$. So $\min(S_i, B_i) \ge S_i/(1 + R_{\max}) \ge (1 - R_{\max}) S_i$, and $\mathrm{ALG} \ge (1 - R_{\max}) P$.

Together, $\mathrm{ALG} \ge (1 - R_{\max}) P = (1 - R_{\max})(1 - 1/c) D \ge (1 - R_{\max})(1 - 1/c)\,\mathrm{OPT}$. $\square$

**The tradeoff function.** In the limit of small bids, $x_i = (e^{f_i} - 1)/(e - 1)$ with $f_i = S_i/B_i$, so $1 - x_i = \frac{e}{e - 1}(1 - e^{f_i - 1}) = \frac{e}{e - 1}\,\psi(f_i)$. So the choice "maximize $b_{ij}(1 - x_i)$" becomes "maximize $b_{ij}\,\psi(f_i)$", which is the MSVV rule. The function $\psi$ discounts an advertiser that has spent a fraction $f$ of its budget, from $\psi(0) = 1 - 1/e$ down to $\psi(1) = 0$.

**Upper bounds.**

- No deterministic algorithm is better than $1 - 1/e$, even with small bids (Mehta, Saberi, Vazirani and Vazirani 2007). The instance is the upper triangular one of [online bipartite matching](/online-bipartite-matching/), with each online vertex split into many small queries.
- No randomized algorithm is better than $1 - 1/e$ either. Against an oblivious adversary the expected assignment of a randomized algorithm is a fractional assignment that is built online, and since $\min(S_i, B_i)$ is concave its revenue is at least the expected revenue. The upper triangular argument holds for fractional algorithms.
- With large bids, the problem contains online bipartite matching, so no deterministic algorithm beats $1/2$.

| Setting | Best ratio known | Upper bound |
|---|---|---|
| general bids, deterministic | $1/2$ (greedy) | $1/2$ |
| general bids, randomized | about $0.5016$ | $1 - 1/e$ |
| small bids ($R_{\max} \to 0$) | $1 - 1/e$ (MSVV, BJN) | $1 - 1/e$ |
| unit bids, unit budgets | $1 - 1/e$ (Ranking) | $1 - 1/e$ |

## Reductions

- **From online bipartite matching and $b$-matching.** Set all bids to 1 and all budgets to 1 or $b$.
- **To an online packing LP.** The LP above is a packing LP whose columns arrive online; the [online primal-dual](/online-primal-dual/) method handles it, and the analysis of Theorem 2 is the general packing analysis with one constraint per advertiser.
- **Compared with online knapsack.** With one advertiser the problem is easy: a bid that overruns the budget still pays the rest, so giving every query to the advertiser is optimal. In the [online knapsack problem](/online-knapsack-problem/) an item that does not fit must be rejected, and no bounded ratio is possible without extra assumptions.

## Applications

- **Sponsored search.** The model of Mehta, Saberi, Vazirani and Vazirani is the allocation of search ads to advertisers with daily budgets. The $\psi$ rule scales a bid by a factor that falls as the budget is spent, a form of budget pacing.
- **Display advertising.** Contracts for a number of impressions are planned with the same tradeoff between the value now and the budget left.
- **Online resource allocation.** Any setting in which requests arrive with values for capacity-limited agents, such as cloud credits or crowd workers, fits the same LP.

## References
