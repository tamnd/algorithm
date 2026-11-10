---
tag: DW570S
kind: algorithm
slug: meyerson-algorithm
name: Meyerson's algorithm
aliases:
- randomized online facility location
- Meyerson's online facility location algorithm
- Meyerson algorithm
area: online-and-streaming/competitive-analysis
level: research
summary: Opens a facility at each arriving point with probability proportional to its distance from the nearest open facility.
solves: [online-facility-location-problem]
model: word-ram
complexity:
  vars: {n: the number of demand points, k: the number of open facilities}
  time: {worst: O(n k)}
  space: {extra: O(n)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 2001
  people: [Adam Meyerson]
  note: Meyerson gave the algorithm in 2001 and proved that it is O(log n)-competitive in adversarial order and O(1)-competitive when the points arrive in random order.
prereqs: [online-facility-location-problem, facility-location-problem, randomized-online-algorithm, linearity-of-expectation]
see_also: [online-greedy-steiner-tree, k-median-problem, k-means, streaming-k-median, jain-vazirani-facility-location, oblivious-adversary]
sources:
  - paper: "Adam Meyerson, Online facility location, Proceedings of the 42nd IEEE Symposium on Foundations of Computer Science (FOCS 2001)"
    title: "Meyerson, Online facility location (2001)"
    locator: the randomized algorithm, the O(log n) bound in adversarial order, the constant bound in random order, and the version with nonuniform facility costs
  - paper: doi:10.1007/s00453-007-9049-y
    title: "Dimitris Fotakis, On the competitive ratio for online facility location, Algorithmica 50(1) (2008), 1-57"
    locator: the lower bound Omega(log n / log log n) for randomized algorithms against an oblivious adversary, and the matching deterministic algorithm
  - url: https://arxiv.org/abs/2207.08783
    title: "Haim Kaplan, David Naori and Danny Raz, Almost tight bounds for online facility location in the random-order model"
    locator: the improved random order analysis of Meyerson's algorithm and the lower bound for random order
  - paper: "Moses Charikar, Liadan O'Callaghan and Rina Panigrahy, Better streaming algorithms for clustering problems, STOC 2003"
    title: "Charikar, O'Callaghan and Panigrahy, Better streaming algorithms for clustering problems (2003)"
    locator: the use of online facility location as a step of streaming k-median
---

Meyerson's algorithm is a randomized online algorithm for [facility location](/online-facility-location-problem/). Demand points arrive one at a time, and each must be served at once, either by a new facility at the point, at cost $f$, or by an open facility, at the cost of the distance. The algorithm opens a facility at the new point with probability $\delta/f$, where $\delta$ is the distance to the nearest open facility, and otherwise connects the point to that facility. Meyerson proved in 2001 that its expected cost is $O(\log n)$ times the optimum when an oblivious adversary chooses the order of $n$ points, and $O(1)$ times the optimum when the points arrive in random order. The rule is a single line, and it is the basis of many streaming clustering algorithms.

## In plain words

A company opens shops for customers who appear one by one. A new shop costs a fixed amount. A customer who is not given a new shop walks to the nearest shop, and the walk costs money too.

For each new customer, the company flips a biased coin. If the nearest shop is far, the coin is likely to say "open a shop here". If a shop is near, the coin rarely says so. A customer who stands on top of a shop never gets a new one. In this way the money spent on new shops roughly matches the money that walks would cost. The company never knows where later customers will be, but on average it pays only a small factor more than the best plan.

## The problem

**Notation.** $M$ is a metric space with distance $d$. The request sequence is $\sigma = p_1, \ldots, p_n$, a sequence of $n$ demand points of $M$, which may repeat. Opening a facility costs $f > 0$ at any point. $F$ is the set of open facilities. $\mathrm{ALG}(\sigma)$ is the total cost of the algorithm and $\mathrm{OPT}(\sigma)$ the cost of the best offline solution, which may open facilities at any points of $M$.

When $p_t$ arrives, the algorithm must either open a facility at $p_t$ or assign $p_t$ to an open facility, and the decision is final. Facilities never close. The cost is $f \cdot \lvert F \rvert + \sum_t d(p_t, \text{its facility})$. A randomized algorithm is $c$-competitive against an [oblivious adversary](/oblivious-adversary/) if $\mathbb{E}[\mathrm{ALG}(\sigma)] \le c \cdot \mathrm{OPT}(\sigma)$ for every $\sigma$ that is fixed in advance. In the random order model, $\sigma$ is a set of points chosen by the adversary, and the order is uniformly random. The [online facility location problem](/online-facility-location-problem/) page gives the model in full.

## The algorithm

```pseudo id=main
MEYERSON(σ, d, f)
L1  F ← ∅
L2  for each point p of σ, in the order of arrival do
L3      δ ← min over q ∈ F of d(p, q), with δ = ∞ if F = ∅
L4      with probability min(δ / f, 1) do
L5          open a facility at p and pay f
L6      otherwise
L7          assign p to the nearest q ∈ F and pay δ
L8  return F
```

The first point always opens a facility. A point at distance at least $f$ from all facilities also opens one. A point on top of a facility never opens one. For nonuniform facility costs, Meyerson rounds the costs to powers of $2$ and uses a similar coin for each cost class.

## Example

Points $a, b, c, d$ lie at $0, 1, 3, 10$ on a line, $f = 4$, and they arrive in this order.

| point | open facilities before | $\delta$ | probability of opening | expected cost of the step |
|---|---|---|---|---|
| $a$ | none | $\infty$ | $1$ | $4$ |
| $b$ | $\{a\}$ | $1$ | $1/4$ | $\tfrac14 \cdot 4 + \tfrac34 \cdot 1 = 7/4$ |
| $c$ | $\{a, b\}$, probability $1/4$ | $2$ | $1/2$ | $\tfrac12 \cdot 4 + \tfrac12 \cdot 2 = 3$ |
| $c$ | $\{a\}$, probability $3/4$ | $3$ | $3/4$ | $\tfrac34 \cdot 4 + \tfrac14 \cdot 3 = 15/4$ |
| $d$ | any | at least $7$ | $1$ | $4$ |

The expected cost is $4 + 7/4 + (\tfrac14 \cdot 3 + \tfrac34 \cdot \tfrac{15}{4}) + 4 = 213/16 = 13.3125$. The optimum opens facilities at $b$ and $d$ and pays $8 + 1 + 2 = 11$. The ratio is about $1.21$. The average of the expected cost over all $24$ orders of the four points is also $213/16$.

## Correctness

The output is always feasible: every point is either a facility or assigned to one. The cost bound has two parts. Given the past, a point at distance $\delta$ from $F$ has expected cost $\min(\delta/f, 1) \cdot f + (1 - \min(\delta/f, 1))\,\delta \le 2 \min(\delta, f)$. Now fix a cluster $C$ of the optimal solution, with facility $c$, and split its points into rings by their distance to $c$: an inner ring within the average distance $\rho_0$, and rings $2^{i-1}\rho_0 < d(p, c) \le 2^i \rho_0$. There are at most $1 + \lceil \log_2 \lvert C \rvert \rceil$ rings. In each ring, the points up to the first one that opens a facility cost at most $2f$ in expectation, by a stopping argument: each of them opens with probability $\min(\delta, f)/f$. After that, every point of the ring is near an open facility and pays at most a constant times its own distance to $c$. Summing gives

$$\mathbb{E}[\mathrm{ALG}] \le \max\big(2 + 2 \lceil \log_2 n \rceil,\ 8\big) \cdot \mathrm{OPT}$$

for every order of the points, so the bound holds in adversarial order. The correctness proof gives each step in full.

## Complexity

Each point scans the open facilities, so step $t$ takes $O(\lvert F \rvert)$ time and the whole run $O(n k)$ time, where $k \le n$ is the final number of facilities. With a nearest neighbor structure for the facilities, the time per point drops to the time of one query. The algorithm stores the facilities in $O(k)$ space and the assignment of each point in $O(n)$ space. It uses one random number per point.

## Properties

- **Adversarial order.** $O(\log n)$-competitive against an oblivious adversary, with the explicit bound above and additive constant $0$.
- **Random order.** $O(1)$-competitive when the order is uniformly random. Meyerson proved a constant of $8$, and Kaplan, Naori and Raz (2022) improved the analysis to $4$.
- **Not optimal in adversarial order.** Fotakis (2008) proved that every randomized algorithm has ratio $\Omega(\log n / \log\log n)$ against an oblivious adversary, already on a line, and gave a deterministic algorithm that matches it. So the gap between Meyerson's bound and the best possible is at most a factor $\log\log n$.
- **Does not know $n$.** The rule does not need $n$, the metric, or the future, only the distances to open facilities.
- **Randomization matters.** The deterministic rule "open a facility when $\delta \ge f$" is not competitive: points at distance just below $f$ from one facility, all near each other, make it pay about $f$ each, while the optimum opens one facility among them.

## Variants and improvements

- **Deterministic algorithms.** Fotakis gave a deterministic $O(\log n / \log\log n)$-competitive algorithm. Anagnostopoulos, Bent, Upfal and Van Hentenryck (2004) gave a simpler deterministic algorithm with ratio $O(\log n)$.
- **Nonuniform facility costs.** Meyerson's paper treats facility costs that depend on the location, with an $O(\log n)$ bound.
- **Streaming clustering.** Running the rule with a facility cost that doubles when too many facilities are open gives a small set of weighted centers, which streaming algorithms for [k-median](/k-median-problem/) and [k-means](/k-means/) then cluster again. Charikar, O'Callaghan and Panigrahy, and later Shindler, Wong and Meyerson, use this idea; see [streaming k-median](/streaming-k-median/).
- **Online k-means.** Liberty, Sriharsha and Sviridenko built an online k-means algorithm on the same coin.

## When to use it

Use Meyerson's rule when points arrive in a stream and you need a set of centers at once, with no second pass: placing servers or caches for clients that appear over time, building a coreset or a summary of a data stream, or seeding a clustering algorithm. It needs only one distance search per point. If the whole input is available, use an offline [facility location](/facility-location-problem/) algorithm such as [Jain and Vazirani](/jain-vazirani-facility-location/), which has a constant factor.

## Pitfalls

- **The adversary must be oblivious.** An adaptive adversary that sees which points opened facilities can place the next point to hurt the algorithm. The bounds hold for a sequence fixed in advance.
- **Only an expected bound.** One run can cost much more than the mean. Repeat runs, or use a deterministic algorithm, when a guarantee for every run is needed.
- **Facility cost scale.** The probability is $\delta / f$ with the true cost $f$. A wrong value of $f$ changes the trade-off between opening and connecting, and the bounds no longer apply.
- **Repeated points.** A point on top of an open facility costs $0$, but it still counts in $n$. The bound above uses the number of requests with repetitions.
- **Random number range.** The test "open if $u \cdot f < \delta$" with $u$ uniform in $[0, 1)$ opens with probability $\min(\delta/f, 1)$. A test with $\le$ opens points with $\delta = 0$ when $u = 0$.

## Implementations

## History

Meyerson introduced the online facility location problem and this algorithm at FOCS 2001. He showed the $O(\log n)$ bound for adversarial order, the constant bound for random order, and the extension to nonuniform costs. Fotakis (ICALP 2003, Algorithmica 2008) settled the adversarial case at $\Theta(\log n / \log\log n)$. Charikar, O'Callaghan and Panigrahy used the rule in 2003 for streaming k-median, and it became a standard step of streaming and online clustering algorithms.

## References
