---
tag: QXQVE0
kind: problem
slug: online-facility-location-problem
name: Online facility location problem
aliases:
- online k-median variant
- online facility location
- OFL
area: online-and-streaming/competitive-analysis
level: advanced
summary: Clients arrive online and must be served at once by opened facilities, with opening and connection costs, and facilities never close.
prereqs: [facility-location-problem, competitive-ratio, online-algorithm, metric-space]
see_also: [meyerson-algorithm, k-median-problem, streaming-k-median, online-steiner-tree-problem, ski-rental-problem, online-primal-dual, frt-tree-embedding, capacitated-facility-location]
sources:
  - paper: "Adam Meyerson, Online facility location, Proceedings of the 42nd IEEE Symposium on Foundations of Computer Science (FOCS 2001)"
    title: "Meyerson, Online facility location (2001)"
    locator: the online model, the randomized algorithm, O(log n) in adversarial order, and O(1) in random order
  - paper: doi:10.1007/s00453-007-9049-y
    title: "Dimitris Fotakis, On the competitive ratio for online facility location, Algorithmica 50(1) (2008), 1-57"
    locator: the lower bound Omega(log n / log log n) for randomized algorithms against an oblivious adversary, and the deterministic O(log n / log log n) algorithm
  - paper: "Aris Anagnostopoulos, Russell Bent, Eli Upfal and Pascal Van Hentenryck, A simple and deterministic competitive algorithm for online facility location, Information and Computation 194(2) (2004)"
    title: "Anagnostopoulos, Bent, Upfal and Van Hentenryck, A simple and deterministic competitive algorithm for online facility location (2004)"
    locator: a deterministic O(log n) algorithm based on a hierarchical partition of the space
  - url: https://arxiv.org/abs/2207.08783
    title: "Haim Kaplan, David Naori and Danny Raz, Almost tight bounds for online facility location in the random-order model"
    locator: the random order analysis of Meyerson's algorithm and the lower bound for random order
---

The online facility location problem is the online version of [uncapacitated facility location](/facility-location-problem/). Demand points arrive one at a time in a metric space. When a point arrives, the algorithm must serve it at once, either by opening a new facility, at cost $f$, or by connecting it to a facility that is already open, at the cost of the distance. Facilities never close, and connections never change. Meyerson defined the problem in 2001 and gave a randomized algorithm that is $O(\log n)$-competitive for $n$ demands, and $O(1)$-competitive if the demands arrive in random order. Fotakis proved in 2008 that the best ratio in adversarial order is $\Theta(\log n / \log\log n)$, for deterministic and randomized algorithms.

## In plain words

A chain of shops serves customers who appear one at a time, at places that no one knows in advance. For each customer, the chain must decide at once: build a new shop at the customer, which costs a fixed amount, or send the customer to an existing shop, which costs the travel distance. Shops stay forever.

A planner who knows all customers in advance can put shops in the middle of the crowds. The online chain does not know where the crowds will form. If it builds too early, it wastes money on lonely customers. If it builds too late, many customers travel far. The best online strategies lose a factor that grows very slowly with the number of customers. If customers arrive in random order, a factor that does not grow at all is possible.

## Definition

**Notation.**

| Symbol | Meaning |
|---|---|
| $(M, d)$ | the metric space, known to the algorithm only through distances between points seen so far |
| $f$ | the facility cost, the same at every point (the uniform case) |
| $\sigma = p_1, \ldots, p_n$ | the request sequence: $n$ demand points of $M$, which may repeat |
| $F_t$ | the facilities open after step $t$, with $F_{t-1} \subseteq F_t$ |
| $a(p_t)$ | the facility that serves $p_t$, chosen at step $t$ |
| $\mathrm{ALG}(\sigma)$, $\mathrm{OPT}(\sigma)$ | the cost of the online solution, and the cost of the best offline solution |

**Input.** The facility cost $f$ and the demand points $p_1, \ldots, p_n$, revealed one at a time.

**Output.** At step $t$, a facility set $F_t \supseteq F_{t-1}$ and a facility $a(p_t) \in F_t$. Both decisions are final.

**Cost.** $\mathrm{ALG}(\sigma) = f \cdot \lvert F_n \rvert + \sum_{t=1}^{n} d(p_t, a(p_t))$. The offline optimum minimizes $f \cdot \lvert F \rvert + \sum_t d(p_t, F)$ over all finite sets $F$ of points of $M$.

**Competitive ratio.** A deterministic algorithm is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma)$ for every $\sigma$, where $c$ may depend on $n$. A randomized algorithm is $c$-competitive if $\mathbb{E}[\mathrm{ALG}(\sigma)] \le c \cdot \mathrm{OPT}(\sigma)$ for every $\sigma$ fixed in advance, against an [oblivious adversary](/oblivious-adversary/). In the *random order* model, the adversary chooses the multiset of points, and the order is uniformly random.

In the nonuniform case, the cost $f_x$ of a facility depends on its location $x$, and the algorithm may open facilities at points other than the demands.

## Variants

- **Nonuniform facility costs.** Each location has its own cost. Meyerson's algorithm extends to this case with an $O(\log n)$ ratio, and Fotakis's bounds hold as well.
- **Random order.** The adversary chooses the points but not the order. Meyerson's algorithm is then $O(1)$-competitive.
- **Incremental facility location.** The algorithm may merge facilities and reassign clients, so that only the current solution matters. Fotakis gave constant-competitive algorithms in this model, which is close to [streaming k-median](/streaming-k-median/).
- **Online k-median.** The number of facilities is fixed at $k$, and the cost is only the connection cost. Without recourse, no online algorithm is competitive, because the first $k$ points must all be facilities. Incremental algorithms and streaming algorithms solve relaxed versions; see [k-median](/k-median-problem/).
- **Capacities and leasing.** Facilities may serve a bounded number of clients, as in [capacitated facility location](/capacitated-facility-location/), or may be leased for a limited time, which combines the problem with [ski rental](/ski-rental-problem/).

## Examples

**A threshold rule fails.** Consider the deterministic rule "open a facility at $p$ when its distance to the nearest facility is at least $f$". The first point $p_1 = 0$ on a line opens a facility. Then $n - 1$ points arrive, all at $x = f - \varepsilon$. Each has distance $f - \varepsilon < f$ to the facility at $0$, so each pays $f - \varepsilon$:

$$\mathrm{ALG} = f + (n - 1)(f - \varepsilon), \qquad \mathrm{OPT} \le 2f,$$

with the second facility at $x$. The ratio tends to $n/2$ as $\varepsilon \to 0$. An algorithm must open facilities before the connection cost of a crowd reaches $f$ for each point, but it cannot tell a crowd from one lonely point. Randomization or a more careful deterministic rule is needed.

**Meyerson's rule on four points.** Points at $0, 1, 3, 10$ on a line arrive in this order with $f = 4$. Meyerson's algorithm opens a facility at a point with probability $\delta/f$, where $\delta$ is its distance to the nearest facility. Its expected cost is $213/16 \approx 13.31$, while the optimum opens facilities at $1$ and $10$ and pays $11$. The [Meyerson algorithm](/meyerson-algorithm/) page gives the step by step table.

**Why the order matters.** If the $n - 1$ points of the first example arrive in random order with the first point, Meyerson's algorithm opens a facility in the crowd after about one point in expectation, because each point at distance $f - \varepsilon$ opens with probability close to $1$. In adversarial order, the adversary can instead send points that slowly approach a crowd center, as in the lower bound below, so that early facilities are always in the wrong place.

## Known algorithms

- **Meyerson's algorithm (2001).** Randomized. Open at $p$ with probability $\min(\delta/f, 1)$, else connect. Expected ratio $O(\log n)$ in adversarial order and $O(1)$ in random order. See [Meyerson's algorithm](/meyerson-algorithm/), which proves $\mathbb{E}[\mathrm{ALG}] \le \max(2 + 2\lceil \log_2 n \rceil, 8) \cdot \mathrm{OPT}$.
- **Fotakis's deterministic algorithm (2003, 2008).** Deterministic and $O(\log n / \log\log n)$-competitive, which is optimal up to a constant factor, also against randomized algorithms.
- **Anagnostopoulos, Bent, Upfal and Van Hentenryck (2004).** A simple deterministic $O(\log n)$ algorithm that works with a hierarchical partition of the space.
- **Primal-dual algorithms.** [Online primal-dual](/online-primal-dual/) methods raise a dual variable for each demand until it pays for a connection or for a share of a new facility. They give deterministic $O(\log n)$ bounds, also for nonuniform costs.

## Bounds

| Setting | Lower bound | Upper bound |
|---|---|---|
| deterministic, adversarial order | $\Omega(\log n / \log\log n)$ (Fotakis 2008) | $O(\log n / \log\log n)$ (Fotakis 2008) |
| randomized, oblivious adversary | $\Omega(\log n / \log\log n)$, already on a line (Fotakis 2008) | $O(\log n)$ (Meyerson 2001); $O(\log n / \log\log n)$ (Fotakis 2008, deterministic) |
| randomized, random order | $2$ (Kaplan, Naori and Raz) | $8$ (Meyerson 2001); $4$ (Kaplan, Naori and Raz) |
| deterministic threshold rule "open when $\delta \ge f$" | about $n/2$ (example above) | |

Here $n$ is the number of demand points, counted with repetition. The ratios are strict, with additive constant $0$. The lower bound of Fotakis uses demands that arrive in phases on a hierarchy of smaller and smaller intervals, each phase closer to the final crowd center, so that every facility opened in an early phase is far from the later demands.

## Reductions

- **From offline facility location.** An online algorithm that runs in polynomial time is also an offline approximation algorithm, so its ratio is at least the offline hardness bound of about $1.46$ (Guha and Khuller), unless $\mathrm{NP} \subseteq \mathrm{DTIME}(n^{O(\log \log n)})$. The online lower bound is much larger, and it holds even for online algorithms with unbounded time.
- **To streaming clustering.** Running an online facility location algorithm with a facility cost that grows as the number of facilities grows gives a small set of weighted centers, which a [k-median](/k-median-problem/) or [k-means](/k-means/) algorithm then clusters again. This is the basis of many [streaming k-median](/streaming-k-median/) algorithms.
- **Relation to online Steiner tree.** Both problems connect each new point to the nearest open point. In the [online Steiner tree problem](/online-steiner-tree-problem/) every point must join one tree, while here a point may start a new facility instead, at the price $f$.
- **Rent or buy.** Each demand chooses between renting a connection and buying a facility, as in [ski rental](/ski-rental-problem/). Meyerson's rule is a randomized rent or buy rule in a metric space.

## Applications

- **Network design.** Servers, caches or relay stations placed as clients join a network, when moving a server later is too expensive.
- **Streaming and online clustering.** One pass summaries of large data sets for k-median and k-means, as in the algorithms of Charikar, O'Callaghan and Panigrahy and of Shindler, Wong and Meyerson.
- **Logistics.** Depots or pickup points opened as demand appears in new regions.

## References
