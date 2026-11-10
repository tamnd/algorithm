---
tag: G9E3P4
kind: problem
slug: linear-search-problem
name: Linear search problem
aliases:
- cow path problem
- lost cow problem
- searching on a line
- doubling search on a line
area: online-and-streaming/competitive-analysis
level: intro
summary: Find a target at an unknown position on an infinite line, starting from the origin; the doubling strategy walks at most 9 times the distance, and no deterministic strategy does better.
prereqs: [competitive-ratio, online-algorithm]
see_also: [exponential-search, unbounded-search, search-problem, ski-rental-problem, randomized-online-algorithm, yao-minimax-principle, online-graph-exploration-problem, online-traveling-salesman-problem]
sources:
  - paper: "Anatole Beck and Donald J. Newman, Yet more on the linear search problem, Israel Journal of Mathematics 8 (1970)"
    title: "Beck and Newman, Yet more on the linear search problem (1970)"
    locator: the doubling strategy and the optimal ratio 9 for deterministic strategies when the distribution of the target is unknown
  - paper: "Ricardo A. Baeza-Yates, Joseph C. Culberson and Gregory J. E. Rawlins, Searching in the plane, Information and Computation 106(2) (1993)"
    title: "Baeza-Yates, Culberson and Rawlins, Searching in the plane (1993)"
    locator: the competitive analysis of the cow path problem, the ratio 9, and the optimal ratio for m rays
  - paper: "Ming-Yang Kao, John H. Reif and Stephen R. Tate, Searching in an unknown environment: an optimal randomized algorithm for the cow-path problem, Information and Computation 131(1) (1996), 63-79"
    title: "Kao, Reif and Tate, Searching in an unknown environment (1996)"
    locator: the randomized strategy with turn points r^(i + epsilon), the ratio 1 + (1 + r)/ln r, and its optimality, about 4.591
  - paper: "Shmuel Gal, Search games, Academic Press, 1980"
    title: "Gal, Search games (1980)"
    locator: the linear search problem as a game between a searcher and a hider, and the randomized solution
---

The linear search problem asks how to find a target on an infinite line, when the searcher starts at the origin and does not know the side or the distance of the target. The searcher walks at unit speed and sees the target only when it reaches it. The cost is the total distance walked, compared with the distance $d$ of the target. The *doubling* strategy goes $1$ to the right, back, $2$ to the left, back, $4$ to the right, and so on. It walks less than $9d$ for every target at distance $d \ge 1$, and Beck and Newman (1970) proved that no deterministic strategy has a smaller ratio. A randomized strategy of Kao, Reif and Tate (1996) reaches about $4.591$ in expectation, which is optimal. The problem is a model for every situation where an online algorithm must guess a scale, and doubling is the standard answer.

Bellman posed the problem in 1963, and Beck studied it in 1964 for targets with a known distribution. The version with an unknown target, studied here, is also called the *cow path problem*.

## In plain words

A cow stands on a long straight fence and wants to find the one gate in it. The gate may be to the left or to the right, and it may be close or far. The cow can see the gate only when it is at the gate.

If the cow walks only to the right, it may never find a gate on the left. So it must turn. A good plan is to walk a little to one side, come back, walk twice as far to the other side, come back, and keep doubling. The cow then walks at most nine times the distance to the gate. If the cow flips coins to choose its first side and its exact turning points, it walks only about four and a half times the distance on average.

## Definition

**Notation.**

| Symbol | Meaning |
|---|---|
| $s \in \{-1, +1\}$ | the side of the target |
| $d \ge 1$ | the distance of the target from the origin |
| $x_0, x_1, x_2, \ldots$ | the turn points of a strategy: excursion $i$ goes to distance $x_i$ on one side and returns to the origin |
| $\mathrm{ALG}(s, d)$ | the distance walked until the target is reached |
| $c$ | the competitive ratio |

**Input.** Nothing at the start. The searcher learns the target only when it stands on it.

**Output.** A walk on the line from the origin that reaches every point. Every such walk is a sequence of excursions, and a strategy is the list of excursions with their sides and turn points.

**Cost.** $\mathrm{ALG}(s, d)$. If excursion $k$ is the first one that reaches the target, then $\mathrm{ALG}(s, d) = 2 \sum_{i < k} x_i + d$.

**Competitive ratio.** A strategy is $c$-competitive if $\mathrm{ALG}(s, d) \le c \cdot d$ for every $s$ and every $d \ge 1$. The lower limit $1$ is needed: without a minimum distance, no strategy has a finite ratio, because the first excursion would have to be shorter than every target. For a randomized strategy, the condition is $\mathbb{E}[\mathrm{ALG}(s, d)] \le c \cdot d$.

## Variants

- **Known distance.** If $d$ is known but not the side, walk $d$ to one side, back, and $d$ to the other side. The cost is at most $3d$, and this is optimal.
- **Known side.** Walk straight to the target. The ratio is $1$.
- **m rays.** The target is on one of $m$ rays from the origin, as in a star. Baeza-Yates, Culberson and Rawlins proved that the best deterministic ratio is $1 + 2 m^m / (m - 1)^{m - 1}$, with turn points that grow by the factor $m/(m - 1)$. For $m = 2$ this is $9$.
- **Randomized search.** Random first side and random turn points $r^{i + \varepsilon}$ give $1 + (1 + r)/\ln r$, which is about $4.591$ at the best $r$ (Kao, Reif and Tate 1996).
- **Turn costs and several searchers.** Each turn may cost extra time, or several searchers may share the work. These change the constants but not the doubling idea.
- **Search in the plane and in graphs.** Searching for a point, a line or a region in the plane, and the [online graph exploration problem](/online-graph-exploration-problem/), use the same ideas.
- **Search with a distribution.** If the position of the target has a known probability distribution, the aim is the expected cost, as in the original work of Bellman and Beck.

## Examples

**Doubling.** Let $x_i = 2^i$, with excursion $i$ to the right when $i$ is even and to the left when $i$ is odd. These targets give the following costs.

| $d$ | side | first excursion that reaches it | cost | ratio |
|---|---|---|---|---|
| $1$ | right | $0$ | $1$ | $1$ |
| $1$ | left | $1$ | $2 + 1 = 3$ | $3$ |
| $3$ | right | $2$ | $2(1 + 2) + 3 = 9$ | $3$ |
| $5$ | left | $3$ | $2(1 + 2 + 4) + 5 = 19$ | $19/5$ |
| $9$ | right | $4$ | $2(1 + 2 + 4 + 8) + 9 = 39$ | $13/3$ |
| $17$ | right | $6$ | $2 \cdot 63 + 17 = 143$ | $143/17$ |

The bad targets are just past a turn point. A target at $2^{k-2} + 1$ on the side of excursion $k$ is missed by excursion $k - 2$, so it is found by excursion $k$.

| $k$ | $d = 2^{k-2} + 1$ | cost $2(2^k - 1) + d$ | ratio |
|---|---|---|---|
| $4$ | $5$ | $35$ | $7$ |
| $6$ | $17$ | $143$ | $8.41$ |
| $8$ | $65$ | $575$ | $8.85$ |
| $10$ | $257$ | $2303$ | $8.96$ |
| $11$ | $513$ | $4607$ | $8.98$ |

Over all integer targets $1 \le d \le 1000$ on both sides, the largest ratio is $4607/513 \approx 8.9805$, at $d = 513$ on the left. As $d \to \infty$ just past the turns, the ratio tends to $9$ but never reaches it.

**Other growth factors.** With $x_i = r^i$, the ratio tends to $1 + 2r^2/(r - 1)$. This is $10$ at $r = 1.5$, $9$ at $r = 2$, about $9.33$ at $r = 2.5$, and $10$ at $r = 3$. The minimum over $r$ is at $r = 2$.

## Known algorithms

- **Doubling.** Turn points $2^i$ on alternate sides. Ratio less than $9$ for every target, and $9$ in the limit (Theorem 1). Optimal among deterministic strategies (Theorem 2).
- **Geometric strategies.** Turn points $r^i$. Ratio $1 + 2r^2/(r - 1)$ in the limit, which is minimal at $r = 2$.
- **Randomized doubling.** Choose the first side at random and $\varepsilon$ uniform in $[0, 1)$, and use turn points $r^{i + \varepsilon}$ with $r \approx 3.591$, the root of $\ln r = 1 + 1/r$. The expected ratio is $1 + r \approx 4.591$ (Theorem 3), and Kao, Reif and Tate proved that no randomized strategy does better.

## Bounds

| Setting | Lower bound | Upper bound |
|---|---|---|
| deterministic, line | $9$ (Beck and Newman 1970; Theorem 2) | $9$, doubling (Theorem 1) |
| randomized, line | about $4.591$ (Kao, Reif and Tate 1996) | about $4.591$ (Theorem 3) |
| deterministic, $m$ rays | $1 + 2m^m/(m - 1)^{m-1}$ (Baeza-Yates, Culberson and Rawlins 1993) | the same, geometric with factor $m/(m-1)$ |
| known distance, unknown side | $3$ | $3$ |

**Theorem 1 (doubling).** For every target at distance $d \ge 1$, doubling walks less than $9d$.

*Proof.* Let $k$ be the first excursion that reaches the target. If $k = 0$, the cost is $d$. If $k = 1$, the target is on the left with $d \le 2$, and the cost is $2 + d \le 3d$. If $k \ge 2$, excursion $k - 2$ went to the same side and did not reach the target, so $d > 2^{k-2}$. The cost is

$$2 \sum_{i < k} 2^i + d = 2(2^k - 1) + d < 2 \cdot 2^k + d < 8d + d = 9d. \qquad \square$$

**Theorem 2 (no deterministic strategy beats 9).** For every deterministic strategy and every $c < 9$, some target at distance $d \ge 1$ has $\mathrm{ALG} > c \cdot d$.

*Proof.* We may assume that the excursions alternate sides and that each one goes farther than the previous excursion on its side, because an excursion that sees nothing new can be removed, and two consecutive excursions on one side can be merged into the longer one, without making any target more expensive. The turn points on each side must grow without bound, or far targets are never found. Let $S_n = x_0 + \cdots + x_n$. Fix an index $i$ with $x_i \ge 1$, and put the target at distance $x_i + \eta$ on the side of excursion $i$. Excursions $0, \ldots, i$ do not reach it, and excursion $i + 1$ goes to the other side, so the cost is at least $2 S_{i+1} + x_i + \eta$. If the strategy is $c$-competitive, then $2 S_{i+1} + x_i + \eta \le c(x_i + \eta)$ for every $\eta > 0$, so

$$S_{i+1} \le a\, x_i = a (S_i - S_{i-1}), \qquad a = \frac{c - 1}{2} < 4.$$

Let $q_i = S_{i+1}/S_i > 1$. Dividing by $S_i$ gives $q_i \le a (1 - 1/q_{i-1})$, for all large $i$. If $a \le 1$, this gives $q_i < 1$ at once. Otherwise, since $q^2 - a q + a \ge a(1 - a/4) > 0$ for every $q$,

$$q_{i-1} - q_i \ge \frac{q_{i-1}^2 - a q_{i-1} + a}{q_{i-1}} \ge \frac{a (1 - a/4)}{q_{i-1}} \ge 1 - \frac{a}{4},$$

where the last step uses $q_{i-1} \le a$, which holds after one step because $a(1 - 1/q) < a$. So $q_i$ decreases by at least the fixed amount $1 - a/4 > 0$ at each step, and after finitely many steps $q_i \le 1$, a contradiction. $\square$

**Theorem 3 (randomized doubling).** With a random first side, $\varepsilon$ uniform in $[0, 1)$ and turn points $x_i = r^{i + \varepsilon}$ for $i \ge 0$, the expected cost for every target at distance $d \ge 1$ is at most $\big(1 + (1 + r)/\ln r\big) d$.

*Proof.* Extend the strategy with excursions $x_i = r^{i + \varepsilon}$ for all negative $i$ as well; their total length is finite, and since $x_{-1} < 1 \le d$ they only add cost. Let $m$ be the first index with $x_m \ge d$. With probability $1/2$, excursion $m$ goes to the side of the target and finds it; otherwise excursion $m + 1$ finds it. The excursions before index $j$ have total length $\sum_{i < j} x_i = x_j/(r - 1)$, so the cost is $d + 2 x_j/(r - 1)$, and

$$\mathbb{E}[\mathrm{ALG} \mid \varepsilon] = d + \frac{2}{r - 1} \cdot \frac{1 + r}{2}\, x_m.$$

Write $d = r^t$. Then $x_m / d = r^u$ with $u = \lceil t - \varepsilon \rceil + \varepsilon - t$, and $u$ is uniform in $[0, 1)$ when $\varepsilon$ is. So $\mathbb{E}[x_m] = d \int_0^1 r^u\,du = d (r - 1)/\ln r$, and

$$\mathbb{E}[\mathrm{ALG}] = \Big(1 + \frac{1 + r}{\ln r}\Big) d.$$

The excursions with $i < 0$ only increase this, so the strategy that starts at $i = 0$ costs at most the same. $\square$

The function $(1 + r)/\ln r$ is smallest where $\ln r = 1 + 1/r$, at $r^* \approx 3.5911$, and there $1 + (1 + r^*)/\ln r^* = 1 + r^* \approx 4.5911$. A numerical average over $\varepsilon$ and the first side gives about $4.591$ for targets at $d = 7.3$, $50$ and $123.4$.

## Reductions

- **To unbounded search.** Searching for an unknown integer $n$ with comparisons by trying $1, 2, 4, \ldots$ and then binary search is the same doubling idea; see [unbounded search](/unbounded-search/) and [exponential search](/exponential-search/).
- **To online algorithms with an unknown scale.** Many online problems use doubling to guess an unknown parameter, such as the optimal cost, and lose a constant factor from the same geometric sum. The guess plays the role of the turn point, and a wrong guess plays the role of a wasted excursion.
- **To interruptible computation.** Running a contract algorithm with time budgets $2^i$ turns it into an algorithm that can be stopped at any time, and the analysis is the same geometric sum.
- **Discrete version.** Searching for one target vertex on an infinite path, with the start in the middle, is this problem with integer distances. The [online graph exploration problem](/online-graph-exploration-problem/) asks instead to visit every vertex of an unknown graph.

## Applications

- **Search and rescue.** Searching along a coast, a road or a corridor for a lost person or object.
- **Robot navigation.** A robot that looks for a gap in a wall, or for the end of an obstacle, without a map.
- **Algorithm design.** Doubling strategies for unknown parameters, iterative deepening search, and the restarts of randomized algorithms.

## References
