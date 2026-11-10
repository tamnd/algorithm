---
tag: C8XWBD
kind: theorem
slug: k-median-inapproximability
name: k-median inapproximability
aliases:
- 1+2/e k-median hardness
- Jain-Mahdian-Saberi k-median hardness
area: approximation/hardness-of-approximation
level: research
summary: Metric k-median has no polynomial algorithm with ratio below 1 + 2/e (Jain, Mahdian and Saberi 2002). The proof turns the max coverage gap into a metric with distances 1, 2 and 3.
prereqs: [k-median-problem, max-coverage-inapproximability, metric-space, gap-problem]
see_also: [set-cover-inapproximability, facility-location-problem, k-center-inapproximability, max-coverage, parameterized-inapproximability, gap-eth, triangle-inequality]
sources:
  - paper: doi:10.1145/509907.510012
    title: Kamal Jain, Mohammad Mahdian and Amin Saberi, A new greedy approach for facility location problems, STOC 2002
    locator: the hardness section, 1 + 2/e for k-median unless NP ⊆ DTIME(n^O(log log n))
  - paper: "S. Guha and S. Khuller, Greedy strikes back: improved facility location algorithms, Journal of Algorithms 31(1), 1999"
    locator: the bound 1.463 for metric facility location from set cover
  - paper: doi:10.1145/285055.285059
    title: Uriel Feige, A threshold of ln n for approximating set cover, Journal of the ACM 45(4), 1998
    locator: Section 5 (the gap for maximum k-coverage)
  - paper: doi:10.1137/S0097539702416402
    title: V. Arya, N. Garg, R. Khandekar, A. Meyerson, K. Munagala and V. Pandit, Local search heuristics for k-median and facility location problems, SIAM Journal on Computing 33(3), 2004
    locator: local search with p swaps, ratio 3 + 2/p
  - paper: "J. Byrka, T. Pensyl, B. Rybicki, A. Srinivasan and K. Trinh, An improved approximation for k-median, and positive correlation in budgeted optimization, Proceedings of the 26th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2015"
    locator: ratio 2.675 + ε
  - paper: "V. Cohen-Addad, A. Gupta, A. Kumar, E. Lee and J. Li, Tight FPT approximations for k-median and k-means, Proceedings of the 46th International Colloquium on Automata, Languages and Programming (ICALP), 2019"
    locator: ratio 1 + 2/e + ε in time f(k, ε) poly(n), and the matching lower bound under Gap-ETH
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Sections 7.7 and 9.2 (k-median by primal-dual and local search)
---

The $k$-median inapproximability theorem says that metric $k$-median has no polynomial algorithm with ratio $1 + \frac{2}{e} - \varepsilon \approx 1.736 - \varepsilon$. The proof is a short gap reduction from [maximum coverage](/max-coverage-inapproximability/): sets become facilities, elements become clients, and a client is at distance 1 from the sets that hold it and 3 from the others. Then the cost of $k$ facilities is $n$ plus twice the number of uncovered elements, so the gap $1$ against $1 - \frac1e$ for coverage becomes a gap $1$ against $1 + \frac2e$ for cost. The bound is due to Jain, Mahdian and Saberi (2002), after the same method by Guha and Khuller (1999) for facility location. The best polynomial algorithms reach about 2.6, so the gap is open.

## Statement

An instance of [$k$-median](/k-median-problem/) has a finite metric space, a set $F$ of facilities, a set $C$ of clients and an integer $k$. A solution opens a set $X \subseteq F$ of $k$ facilities, and its cost is $\sum_{c \in C} d(c, X)$ with $d(c, X) = \min_{x \in X} d(c, x)$. For this minimization problem, a ratio $\rho \ge 1$ means $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance.

The theorem uses the gap form of Feige's maximum coverage theorem (cited): for each $\varepsilon > 0$ it is NP-hard to tell instances where some $k$ sets cover all $n$ elements from instances where every $k$ sets cover at most $(1 - \frac1e + \varepsilon) n$ elements.

**Theorem.** For each $\varepsilon > 0$, it is NP-hard to tell metric $k$-median instances with $\mathrm{OPT} \le |C|$ from instances with $\mathrm{OPT} \ge (1 + \frac2e - 2\varepsilon) |C|$. So a polynomial algorithm with ratio $1 + \frac{2}{e} - \varepsilon$ for metric $k$-median gives P = NP.

Jain, Mahdian and Saberi state the bound under the assumption NP $\not\subseteq$ DTIME$(n^{O(\log \log n)})$, because they reduce from set cover with Feige's form of its threshold. The proof below uses the gap form of maximum coverage, which needs only P $\ne$ NP.

## In plain words

Some customers each need a shop. Each possible shop serves a fixed group of customers well: they travel one step. Every other customer travels three steps. You may open a fixed number of shops, and you want the total travel to be small.

If the shops can serve every customer well, the total is one step per customer. If the best choice of shops leaves a part of the customers unserved, each of them adds two more steps. A known hard result says that even the best choice may leave more than a third of the customers, about 37 percent, out, and that you cannot tell this case from the perfect case fast. Then the total is about $1.74$ steps per customer against one step, and a fast method cannot get closer than this.

## Proof

*The construction.* Take a maximum coverage instance with elements $U = \{1, \ldots, n\}$, sets $S_1, \ldots, S_M$ and budget $k$. Make a facility $f_j$ for each set and a client $c_e$ for each element, and set

$$d(f_j, c_e) = \begin{cases} 1 & e \in S_j, \\ 3 & e \notin S_j, \end{cases} \qquad d(f_j, f_{j'}) = 2, \qquad d(c_e, c_{e'}) = 2$$

for distinct points. The instance has $M + n$ points and $(M + n)^2$ distances, so it is built in polynomial time.

*The metric.* All distances between distinct points lie in $\{1, 2, 3\}$. A triangle inequality $d(p, q) \le d(p, x) + d(x, q)$ with distinct $p, q, x$ can fail only if $d(p, q) = 3$ and $d(p, x) + d(x, q) = 2$, so both are 1. A distance 3 is between a facility and a client, say $p = f_j$ and $q = c_e$. A distance 1 is also between a facility and a client, so $x$ would have to be a client, for $d(f_j, x) = 1$, and a facility, for $d(x, c_e) = 1$. That is impossible, so $d$ is a metric.

*The cost.* Open a set $X$ of $k$ facilities, given by $k$ sets. A client $c_e$ has $d(c_e, X) = 1$ if some chosen set holds $e$ and $d(c_e, X) = 3$ otherwise. If the chosen sets cover $\mathrm{cov}(X)$ elements, the cost is

$$\mathrm{cov}(X) + 3 (n - \mathrm{cov}(X)) = n + 2 (n - \mathrm{cov}(X)).$$

So $\mathrm{OPT}_{k\text{-med}} = n + 2 (n - \mathrm{OPT}_{\mathrm{cov}})$, where $\mathrm{OPT}_{\mathrm{cov}}$ is the maximum coverage with $k$ sets.

*The gap.* On a yes-instance of maximum coverage, $\mathrm{OPT}_{\mathrm{cov}} = n$ and $\mathrm{OPT}_{k\text{-med}} = n = |C|$. On a no-instance, $\mathrm{OPT}_{\mathrm{cov}} \le (1 - \frac1e + \varepsilon) n$, so

$$\mathrm{OPT}_{k\text{-med}} \ge n + 2 \left(\tfrac1e - \varepsilon\right) n = \left(1 + \tfrac2e - 2\varepsilon\right) n.$$

An algorithm with ratio $\rho = 1 + \frac2e - 3\varepsilon$ returns at most $\rho n$ on yes-instances, which is less than the no-instance bound, so comparing its cost with $\rho n$ decides the coverage gap. Since $\varepsilon$ is arbitrary, this proves the theorem. $\blacksquare$

The proof is complete given the gap form of maximum coverage. That gap form is cited from Feige (1998); the [maximum coverage](/max-coverage-inapproximability/) page proves only the ratio form, which is not enough here, because the $k$-median cost needs the yes case to cover all elements.

### Example

Let $U = \{0, \ldots, 5\}$, with sets $\{0, 1, 2\}$, $\{3, 4, 5\}$, $\{0, 3\}$, $\{1, 4\}$, $\{2, 5\}$. With $k = 2$, the first two sets cover all of $U$, so $\mathrm{OPT}_{k\text{-med}} = 6$. With $k = 1$, the best set covers 3 elements, so $\mathrm{OPT}_{k\text{-med}} = 6 + 2 \cdot 3 = 12$. The code for this page checks the metric and the identity $\mathrm{OPT}_{k\text{-med}} = n + 2(n - \mathrm{OPT}_{\mathrm{cov}})$ by brute force on random set systems.

## Consequences

- **Facility location.** With opening costs in place of the budget $k$, the same instance shape gives the bound $\gamma \approx 1.463$ for metric facility location, the root of $\gamma = 1 + 2 e^{-\gamma}$ (Guha and Khuller 1999). There the number of open facilities is free, and the best trade-off between opening cost and coverage gives $\gamma$ instead of $1 + \frac2e$.
- **$k$-means.** If the cost is the sum of squared distances, the same instance gives $1$ against $1 + \frac{8}{e}$, because uncovered clients pay $9$ in place of $1$. So $k$-means in general metrics has no ratio below $1 + \frac8e$ unless P = NP.
- **FPT algorithms.** Cohen-Addad, Gupta, Kumar, Lee and Li (2019) give ratio $1 + \frac2e + \varepsilon$ in time $f(k, \varepsilon) \cdot n^{O(1)}$, and show, under [Gap-ETH](/gap-eth/), that no algorithm with time $f(k) \cdot n^{o(k)}$ does better. So $1 + \frac2e$ is the exact threshold when the parameter is $k$; see [parameterized inapproximability](/parameterized-inapproximability/).
- **Without candidate facilities.** If every client may also be a facility, the construction above fails: opening a client $c_e$ gives it cost 0 and every other client cost 2. Other bounds hold for that version.

## Tightness

The constant $1 + \frac2e$ is not known to be tight for polynomial algorithms. Local search with $p$ swaps reaches $3 + \frac2p$ (Arya et al. 2004), and LP-based algorithms reach $2.675 + \varepsilon$ (Byrka, Pensyl, Rybicki, Srinivasan and Trinh 2015), with small later improvements. The reduction itself is tight: the instances have $\mathrm{OPT}$ equal to $n + 2(n - \mathrm{OPT}_{\mathrm{cov}})$ exactly, and greedy coverage gives cost at most $(1 + \frac2e) n$ on yes-instances. So no gap larger than $1 + \frac2e$ can come from instances with distances 1 and 3 only. The FPT result above shows that $1 + \frac2e$ is tight for algorithms with time $f(k) \cdot n^{O(1)}$.

## History

Guha and Khuller (1999) introduced the reduction from set cover to metric facility location with distances 1 and 3 and proved the bound 1.463. Jain, Mahdian and Saberi (2002) applied the same idea with a budget of $k$ facilities and obtained $1 + \frac2e$ for $k$-median. Cohen-Addad et al. (2019) showed that the bound is exact for FPT algorithms under Gap-ETH.

## References
