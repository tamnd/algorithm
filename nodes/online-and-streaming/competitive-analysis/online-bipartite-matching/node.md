---
tag: AH9VYY
kind: problem
slug: online-bipartite-matching
name: Online bipartite matching
aliases:
- online matching
- one-sided online bipartite matching
area: online-and-streaming/competitive-analysis
level: advanced
summary: One side of a bipartite graph is known; the other side arrives one vertex at a time and each arrival must be matched at once and for good. Greedy gets 1/2 and no randomized algorithm beats 1 - 1/e.
prereqs: [online-algorithm, competitive-ratio, bipartite-matching]
see_also: [greedy-online-matching, ranking-algorithm, balance-algorithm, online-adwords-problem, maximal-matching, yao-minimax-principle, b-matching, online-primal-dual]
sources:
  - paper: doi:10.1145/100216.100262
    title: "Richard M. Karp, Umesh V. Vazirani and Vijay V. Vazirani, An optimal algorithm for on-line bipartite matching, Proceedings of the 22nd Annual ACM Symposium on Theory of Computing (STOC 1990), 352-358"
    locator: the model, the bound 1/2 for deterministic algorithms, the analysis of RANDOM, the upper triangular instance and the bound 1 - 1/e for randomized algorithms
  - paper: doi:10.1561/0400000057
    title: "Aranyak Mehta, Online matching and ad allocation, Foundations and Trends in Theoretical Computer Science 8(4) (2013), 265-368"
    locator: Chapters 2 and 3 (the problem, the greedy bound, the upper triangular lower bound and RANKING), and the later chapters on vertex weights, budgets and stochastic arrivals
  - paper: doi:10.1145/1360443.1360462
    title: "Benjamin Birnbaum and Claire Mathieu, On-line bipartite matching made simple, ACM SIGACT News 39(1) (2008), 80-87"
    locator: the short proof of the bound 1 - 1/e for RANKING and the statement of the upper bound
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 6 (randomized online algorithms and the adversary models) and Chapter 8 (Yao's principle)
---

Online bipartite matching is the problem of building a matching in a bipartite graph whose one side is known in advance and whose other side arrives one vertex at a time, with its edges. Each arrival must be matched to a free neighbour or left unmatched at once, and the choice can never change. The goal is a large matching, measured against the maximum matching of the whole graph. Any greedy rule gets at least half of the optimum, no deterministic rule does better, and Karp, Vazirani and Vazirani (1990) showed that the randomized [Ranking algorithm](/ranking-algorithm/) gets $1 - 1/e \approx 0.632$, which is the best possible for any randomized algorithm.

## In plain words

A shop has a fixed list of workers. Jobs come in one at a time, and each job says which workers can do it. The shop must give the job to one free worker who can do it, or turn the job away, before the next job comes in. A worker who has a job keeps it. At the end, count the jobs that were given out, and compare this count with the best count that the shop could have got if it had seen all the jobs at the start.

Giving each job to any free worker who fits is never worse than half of the best. A clever order of jobs can push any fixed rule down to half. A rule that uses a random ranking of the workers does better, at almost two thirds, and no rule can do better than that on all job orders.

## Definition

**Input.** A bipartite graph $G = (U \cup V, E)$. The offline side $U$ is known at the start. The online vertices $v_1, v_2, \ldots, v_n$ of $V$ arrive one at a time. When $v_t$ arrives, its set of neighbours $N(v_t) \subseteq U$ is revealed. The request sequence $\sigma$ is the order of arrivals with their neighbour sets.

**Online rule.** Before $v_{t+1}$ arrives, the algorithm must match $v_t$ to a vertex of $N(v_t)$ that is still free, or leave $v_t$ unmatched. Both choices are irrevocable: a matched pair stays matched, and an unmatched $v_t$ stays unmatched.

**Goal.** Maximize the size $\mathrm{ALG}(\sigma)$ of the final [matching](/bipartite-matching/). $\mathrm{OPT}(\sigma)$ is the size of a [maximum matching](/maximum-matching/) of $G$, computed offline.

**Notation and cost model.**

| Symbol | Meaning |
|---|---|
| $\sigma$ | the arrival sequence of the online vertices with their neighbour sets |
| $\mathrm{ALG}(\sigma)$, $\mathrm{OPT}(\sigma)$ | the size of the online matching and of a maximum matching |
| $c$ | the competitive ratio, with $c \le 1$ |
| $n$ | the number of online vertices; on the hard instances also $\lvert U \rvert = n$ |

This is a maximization problem, and the page uses the convention $\mathrm{ALG}(\sigma) \ge c \cdot \mathrm{OPT}(\sigma)$ with $c \le 1$, with no additive term. A randomized algorithm is $c$-competitive if $\mathbb{E}[\mathrm{ALG}(\sigma)] \ge c \cdot \mathrm{OPT}(\sigma)$ for every $\sigma$, against an [oblivious adversary](/oblivious-adversary/) that fixes $\sigma$ before the coins are tossed. All bounds below are of this strict form, and the lower bound constructions repeat a gadget, so an additive constant does not change them.

## Variants

- **Vertex weights.** Each offline vertex $u$ has a weight $w_u$, and the goal is the total weight of the matched offline vertices. Aggarwal, Goel, Karande and Mehta (2011) gave a perturbed form of Ranking with ratio $1 - 1/e$.
- **$b$-matching.** Each offline vertex can take up to $b$ online vertices ([b-matching](/b-matching/)). The deterministic [Balance algorithm](/balance-algorithm/) gets $1 - 1/(1 + 1/b)^b$, which tends to $1 - 1/e$ as $b$ grows.
- **Budgets and bids.** In the [online adwords problem](/online-adwords-problem/), an edge has a bid and an offline vertex has a budget. With small bids the best ratio is again $1 - 1/e$.
- **Edge weights.** With edge weights and no way to drop a matched edge, no online algorithm has a constant ratio. With free disposal (an offline vertex may drop its edge for a heavier one), constant ratios exist.
- **Random order and stochastic arrivals.** If the online vertices arrive in a uniform random order, or are drawn i.i.d. from a known distribution, ratios above $1 - 1/e$ are possible. Ranking in random order gets at least $0.696$ (Mahdian and Yan 2011).
- **Adaptive adversary.** If the adversary sees the random choices before it builds the next vertex, no algorithm, random or not, beats $1/2$ (see Bounds). See [adaptive adversary](/adaptive-adversary/).
- **Fractional version.** The algorithm may split each online vertex over its neighbours, with total at most 1 per vertex. The deterministic water-filling rule gets $1 - 1/e$, and the upper triangular bound below holds for it too. See [fractional matching](/fractional-matching/).

## Examples

**A bad order for a fixed greedy rule.** Let $U = \{u_1, u_2, u_3\}$ and take the rule "match to the free neighbour with the smallest index". The adversary knows the rule, so it builds the sequence after it predicts each choice.

| $t$ | $N(v_t)$ | free neighbours | greedy picks | optimum pairs |
|---|---|---|---|---|
| 1 | $u_1, u_2, u_3$ | $u_1, u_2, u_3$ | $u_1$ | $u_3$ |
| 2 | $u_1, u_2$ | $u_2$ | $u_2$ | $u_2$ |
| 3 | $u_1$ | none | unmatched | $u_1$ |

So $\mathrm{ALG} = 2$ and $\mathrm{OPT} = 3$. The neighbour sets are nested, and the vertex removed from the set at each step is the optimum partner of the vertex that just arrived. This is the upper triangular instance with the permutation $(u_3, u_2, u_1)$.

**The same instance against Ranking.** On the upper triangular instance with $n$ offline vertices, every rule that matches whenever it can has the same expected size when the permutation is uniform. For Ranking, the exact expected size, by enumeration of all rank orders, is $1$, $3/2$, $13/6$, $67/24$, $137/40$, $2921/720$ and $23633/5040 \approx 4.689$ for $n = 1, \ldots, 7$. The ratio at $n = 7$ is $0.670$. A dynamic program over the state $(t, X_t)$ of the proof below gives the best expected size over all deterministic algorithms: $6.585$ for $n = 10$ and $63.476$ for $n = 100$, a ratio of $0.635$, which is close to $1 - 1/e \approx 0.632$.

**RANDOM is only 1/2.** The rule RANDOM matches each arrival to a uniform random free neighbour. Take $2k$ offline vertices $u_1, \ldots, u_{2k}$. First the vertices $v_1, \ldots, v_k$ arrive, and $v_i$ is adjacent to $u_i$ and to all of $u_{k+1}, \ldots, u_{2k}$. Then $v_{k+1}, \ldots, v_{2k}$ arrive, and $v_i$ is adjacent only to $u_i$. The optimum is $2k$, a perfect matching. The exact expected size of RANDOM is $3/2$, $25/9$ and $763/192$ for $k = 1, 2, 3$, and the ratio falls to $0.584$ at $k = 10$. Karp, Vazirani and Vazirani showed that on a family of this kind RANDOM gets only $n/2 + O(\log n)$. On the same instances Ranking gets ratio $0.75$, $0.729$ and $0.718$ for $k = 1, 2, 3$.

## Known algorithms

- **Greedy.** Match each arrival to any free neighbour. Every such rule is $1/2$-competitive, and this is tight for each deterministic rule. See [greedy online matching](/greedy-online-matching/).
- **RANDOM.** A uniform random free neighbour for each arrival. Its ratio is $1/2$, the same as greedy in the worst case.
- **Ranking.** Pick one uniform random order of $U$ at the start, then match each arrival to its free neighbour that comes first in the order. Ratio $1 - 1/e$, optimal among randomized algorithms. See [Ranking algorithm](/ranking-algorithm/).
- **Balance and water-filling.** For $b$-matching, or for the fractional version, assign to the neighbour with the smallest load. See [Balance algorithm](/balance-algorithm/).
- **Primal-dual.** The [online primal-dual method](/online-primal-dual/) gives the same ratios with a dual certificate, and extends to budgets and weights.

## Bounds

Below, a *greedy* rule is any rule that matches $v_t$ whenever $v_t$ has a free neighbour. Theorems 1, 2 and 3 are proved here. The bound $1 - 1/e$ for Ranking is proved on the [Ranking algorithm](/ranking-algorithm/) page.

**Theorem 1 (greedy is 1/2-competitive).** For every greedy rule and every $\sigma$, $\mathrm{ALG}(\sigma) \ge \mathrm{OPT}(\sigma)/2$.

*Proof.* Let $M$ be the online matching and $M^*$ a maximum matching. Take an edge $(u, v) \in M^*$. If $v$ is unmatched in $M$, then when $v$ arrived it had no free neighbour, because the rule is greedy. So $u$ was matched at that time, and it stays matched. So each edge of $M^*$ has an endpoint that is matched in $M$, that is, $M$ is a [maximal matching](/maximal-matching/) of $G$. The edges of $M^*$ are disjoint, so they need $\lvert M^* \rvert$ distinct matched vertices, and each edge of $M$ gives only two. So $\lvert M^* \rvert \le 2 \lvert M \rvert$. $\square$

**Theorem 2 (no deterministic rule beats 1/2).** For each deterministic online algorithm and each $k \ge 1$ there is a $\sigma$ with $\mathrm{OPT}(\sigma) = 2k$ and $\mathrm{ALG}(\sigma) \le k$.

*Proof.* Take one gadget with $U = \{u_1, u_2\}$. The vertex $v_1$ is adjacent to $u_1$ and $u_2$. The adversary simulates the algorithm. If it matches $v_1$ to $u_i$, then $v_2$ is adjacent only to $u_i$. If it leaves $v_1$ unmatched, $v_2$ is adjacent only to $u_1$. In both cases the algorithm matches at most one vertex, while $v_1 u_{3-i}$ and $v_2 u_i$ (or $v_1 u_2$ and $v_2 u_1$) is a matching of size 2. Repeat the gadget on $k$ disjoint pairs. $\square$

The same argument works for a randomized algorithm against an adaptive online adversary, which sees the choice for $v_1$ before it builds $v_2$. So randomization helps only against an oblivious adversary.

**Theorem 3 (no randomized algorithm beats 1 - 1/e).** For each randomized online algorithm $R$ and each $n$, there is an instance with $\mathrm{OPT} = n$ and $\mathbb{E}[\mathrm{ALG}] \le (n + 1)(1 - 1/e) + 2$. So no ratio $c > 1 - 1/e$ is possible.

*Proof.* Let $U = \{u_1, \ldots, u_n\}$, and let $\pi$ be a permutation of $U$. In the *upper triangular instance* $I_\pi$, the vertex $v_t$ is adjacent to $N_t = \{\pi(t), \pi(t+1), \ldots, \pi(n)\}$. The edges $v_t \pi(t)$ form a perfect matching, so $\mathrm{OPT} = n$.

By [Yao's principle](/yao-minimax-principle/) it is enough to show the bound for each deterministic algorithm $A$ when $\pi$ is uniform: $R$ is a distribution over deterministic algorithms, so $\mathbb{E}_\pi \mathbb{E}_R[R(I_\pi)] \le \max_A \mathbb{E}_\pi[A(I_\pi)]$, and some fixed $\pi$ is at most this average.

Fix $A$. When $v_t$ arrives, $A$ has seen $N_1 \supset N_2 \supset \cdots \supset N_t$, so it knows $\pi(1), \ldots, \pi(t-1)$ and nothing about the order of $\pi$ inside $N_t$. Given this history, $\pi(t)$ is uniform in $N_t$ and independent of the choice of $A$ at step $t$. Let $s_t = n - t + 1 = \lvert N_t \rvert$, let $X_t$ be the number of vertices of $N_t$ that are matched before $v_t$ arrives, let $\delta_t \in \{0, 1\}$ say whether $A$ matches $v_t$, and let $Y_t = X_t / s_t$. A matched $v_t$ takes a vertex of $N_t$, so after step $t$ the set $N_t$ holds $X_t + \delta_t$ matched vertices. Then $N_{t+1} = N_t \setminus \{\pi(t)\}$ loses a uniform vertex of $N_t$, so

$$\mathbb{E}[X_{t+1} \mid \text{history}, \delta_t] = (X_t + \delta_t) \frac{s_t - 1}{s_t}, \qquad \mathbb{E}[Y_{t+1} \mid \text{history}, \delta_t] = Y_t + \frac{\delta_t}{s_t}.$$

Since $Y_1 = 0$ and $Y_n = X_n / 1 \le 1$, taking expectations and summing gives

$$\sum_{t=1}^{n-1} \frac{p_t}{n - t + 1} \le 1, \qquad p_t = \Pr[\delta_t = 1] \in [0, 1].$$

Now $\mathbb{E}[\mathrm{ALG}] = \sum_{t=1}^{n} p_t \le 1 + \sum_{t=1}^{n-1} p_t$. Maximize $\sum p_t$ under the constraint. It is a fractional knapsack with unit values and weights $1/n, 1/(n-1), \ldots$, so the best choice fills $p_1 = p_2 = \cdots = p_k = 1$ for the largest $k$ with $H_n - H_{n-k} \le 1$, and puts less than 1 on one more step, where $H_j$ is the [harmonic number](/harmonic-series/). Since $H_n - H_{n-k} = \sum_{j=n-k+1}^{n} 1/j \ge \ln\frac{n+1}{n-k+1}$, the condition gives $n - k + 1 \ge (n+1)/e$, so $k \le (n+1)(1 - 1/e)$. So $\mathbb{E}[\mathrm{ALG}] \le 1 + k + 1 \le (n+1)(1 - 1/e) + 2$, and the ratio is at most $1 - 1/e + (3 - 1/e)/n$. $\square$

**Tight results.**

| Algorithm class | Best ratio | Upper bound proof | Lower bound proof |
|---|---|---|---|
| deterministic | $1/2$ | Theorem 2 | Theorem 1 (any greedy) |
| randomized, oblivious adversary | $1 - 1/e$ | Theorem 3 | Ranking (KVV 1990) |
| randomized, adaptive online adversary | $1/2$ | Theorem 2 | Theorem 1 |
| fractional, deterministic | $1 - 1/e$ | Theorem 3 (the same proof) | water-filling |

## Reductions

- **To offline matching.** $\mathrm{OPT}$ is a maximum bipartite matching, computed by [Hopcroft-Karp](/hopcroft-karp/) or [Kuhn's algorithm](/kuhn-algorithm/) once the whole graph is known.
- **Special case of adwords and b-matching.** With all bids and budgets equal to 1, the [online adwords problem](/online-adwords-problem/) is online bipartite matching. With $b = 1$, online $b$-matching is the same problem.
- **Packing LP.** The fractional version is an online packing LP with one row per offline vertex and one column per edge. The [online primal-dual method](/online-primal-dual/) analyses it and its rounding.

## Applications

- **Display and search ads.** Ad slots (online) are assigned to advertisers (offline) as page views arrive; see the [online adwords problem](/online-adwords-problem/).
- **Assignment of requests to servers or workers.** Jobs, rides or tasks arrive and must be sent at once to one compatible resource with a free slot.
- **A test case for online methods.** The problem is a standard first example for randomized online algorithms, Yao's principle and the randomized primal-dual analysis.

## References
