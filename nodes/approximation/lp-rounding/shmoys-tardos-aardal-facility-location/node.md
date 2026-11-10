---
tag: C5BW1S
kind: algorithm
slug: shmoys-tardos-aardal-facility-location
name: Shmoys-Tardos-Aardal facility location
aliases:
- filtering and rounding for facility location
- STA facility location rounding
area: approximation/lp-rounding
level: advanced
summary: Filter the facility location LP so each client uses only near facilities, then open one cheap facility per cluster; the best filter level gives cost at most 3/(1 - 1/e^3), about 3.16, times the LP.
solves: [facility-location-problem]
model: real-ram
complexity:
  vars: {m: the number of facilities, n: the number of clients, L: the time to solve the LP with m n + m variables}
  time: {worst: O(L + m^2 n^3)}
  space: {extra: O(m n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1997
  people: [David B. Shmoys, Éva Tardos, Karen Aardal]
  note: Shmoys, Tardos and Aardal gave the first constant factor approximation for metric uncapacitated facility location, 3.16, by filtering the LP solution in the style of Lin and Vitter and rounding it cluster by cluster.
prereqs: [facility-location-problem, lp-relaxation, filtering-technique, triangle-inequality]
see_also: [jain-vazirani-facility-location, capacitated-facility-location, filtering-technique, randomized-rounding, k-median-problem, integrality-gap, linear-programming-rounding, dependent-rounding]
sources:
  - paper: doi:10.1145/258533.258600
    title: David B. Shmoys, Éva Tardos and Karen Aardal, Approximation algorithms for facility location problems, Proceedings of the 29th ACM Symposium on Theory of Computing, 1997
    locator: the filtering lemma and the 3.16 bound
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 4.5 (deterministic rounding with ratio 4) and Section 5.8 (randomized rounding)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 24, notes (the history of the LP rounding results)
---

The Shmoys-Tardos-Aardal algorithm rounds the LP relaxation of metric uncapacitated [facility location](/facility-location-problem/): open some facilities, each with a cost, and connect each client to an open one, so that the total cost is small. It first *filters* the LP solution. For a level $\alpha \in (0, 1)$, each client keeps only the nearest facilities that hold an $\alpha$ fraction of its LP assignment, at distance at most $g_j(\alpha)$. Then it *clusters*: the client with the smallest $g_j$ becomes a center, the cheapest facility near it opens, and every client whose near set meets the center's near set connects to it. For one level, the cost is at most $F_{\text{LP}} / \alpha + 3 C_{\text{LP}} / (1 - \alpha)$, which is $4 \cdot \text{LP}$ at $\alpha = 1/4$. The best level gives at most $3 / (1 - e^{-3}) \approx 3.16$ times the LP value.

## In plain words

First solve an easier problem where a shop can be half built and a customer can be split among several shops. Then each customer looks only at its nearest shops, enough to cover a fixed part of its split. These shops are "near" to it.

Take the customer whose near shops are closest of all, and build the cheapest of its near shops. Every customer that shares a near shop with it goes there too. The trip is short: to the shared shop, back to the first customer, and on to the new shop, and each leg is no longer than the customer's own near distance. Repeat with the customers that are left.

The shops built are paid for by the half-built shops of different groups, and the trips are paid for by the split answer.

## The problem

There are $m$ facilities with costs $f_i \ge 0$ and $n$ clients, with costs $c_{ij} \ge 0$ that satisfy the [triangle inequality](/triangle-inequality/) on facilities and clients together. The LP is

$$\min \underbrace{\sum_i f_i y_i}_{F_{\text{LP}}} + \underbrace{\sum_{i, j} c_{ij} x_{ij}}_{C_{\text{LP}}} \ \text{ s.t. } \sum_i x_{ij} = 1, \ \ x_{ij} \le y_i, \ \ x, y \ge 0.$$

Its value $\text{LP} = F_{\text{LP}} + C_{\text{LP}}$ is at most OPT, since each solution gives a point with 0-1 values. Write $C_j = \sum_i c_{ij} x_{ij}$ for the LP connection cost of client $j$. The $\alpha$-point of client $j$ is

$$g_j(\alpha) = \min \Big\{ g : \sum_{i : c_{ij} \le g} x_{ij} \ge \alpha \Big\},$$

the radius of the smallest ball around $j$ that holds an $\alpha$ fraction of its LP assignment. Its near set is $N_j = \{ i : x_{ij} > 0, \ c_{ij} \le g_j(\alpha) \}$, so $\sum_{i \in N_j} x_{ij} \ge \alpha$.

## The algorithm

```pseudo id=main
SHMOYS-TARDOS-AARDAL(f, c)
L1  solve the LP for an optimal (x, y)
L2  for each level α in (0, 1] at which some g_j changes do
L3      g_j ← g_j(α) and N_j ← { i : x_ij > 0, c_ij ≤ g_j } for each client j
L4      U ← all clients
L5      while U ≠ ∅: let j be the client of U with the least g_j
L6          open the facility i of N_j with the least f_i
L7          connect each k ∈ U with N_k ∩ N_j ≠ ∅ to i, and remove it from U
L8      keep the cheapest of the solutions found so far
L9  return the kept solution
```

The values $g_j(\alpha)$ change only at the cumulative sums of $x_{ij}$ over the facilities sorted by $c_{ij}$, so line L2 tries at most $mn$ levels. Between two of these levels, all $g_j$ and $N_j$ stay the same, and so does the solution. So trying these levels is the same as trying every $\alpha \in (0, 1]$. A single fixed level, such as $\alpha = 1/4$, also works and gives ratio 4. Line L7 removes the center $j$ itself, so each pass of the loop removes at least one client.

## Example

There are three facilities, each of cost 2, and three clients. Each client is at distance 1 from two facilities and 3 from the third.

| | client 1 | client 2 | client 3 |
|---|---|---|---|
| facility 1 | 1 | 3 | 1 |
| facility 2 | 1 | 1 | 3 |
| facility 3 | 3 | 1 | 1 |

The LP optimum has $y_i = 1/2$ for each facility and sends half of each client to each of its two facilities at distance 1. So $F_{\text{LP}} = 3$, $C_{\text{LP}} = 3$ and $\text{LP} = 6$. The optimum is 7: one facility costs $2 + 1 + 1 + 3$, and two facilities cost $4 + 1 + 1 + 1$. The cumulative sums are $1/2$ and $1$, so line L2 tries $\alpha = 1/2$ and $\alpha = 1$.

At $\alpha = 1/2$, each $g_j = 1$, with near sets $N_1 = \{1, 2\}$, $N_2 = \{2, 3\}$ and $N_3 = \{1, 3\}$. All $g_j$ are equal, so client 1 is the center by index. Facility 1 is the cheapest in $N_1$, by index, and it opens. Both other clients meet $N_1$: $N_2 \cap N_1 = \{2\}$ and $N_3 \cap N_1 = \{1\}$. So all clients go to facility 1, at costs 1, 3 and 1, and the total is $2 + 5 = 7 = \text{OPT}$.

Client 2 pays $3 = 3 g_2$, so the bound of the connection step is tight here. Its route in the proof goes from facility 1 to client 1 to facility 2 to client 2, with three legs of length 1. The level $\alpha = 1$ gives the same solution.

## Correctness

**Theorem (Shmoys, Tardos and Aardal 1997).** For each level $\alpha \in (0, 1)$, lines L3 to L7 give a solution of cost at most $F_{\text{LP}} / \alpha + 3 \sum_j g_j(\alpha) \le F_{\text{LP}} / \alpha + 3 C_{\text{LP}} / (1 - \alpha)$. The best level costs at most $\frac{3}{1 - e^{-3}} \, \text{LP} < 3.16 \, \text{OPT}$.

The proof, in full in the proof file below, has four parts.

1. *Facility cost.* The near sets of the centers are disjoint, since every client whose near set meets a center's is removed. The opened facility is the cheapest in $N_j$, and $\sum_{i \in N_j} y_i \ge \sum_{i \in N_j} x_{ij} \ge \alpha$. So its cost is at most $\frac{1}{\alpha} \sum_{i \in N_j} f_i y_i$, and the sum over the centers is at most $F_{\text{LP}} / \alpha$.
2. *Connection cost.* A client $k$ joins center $j$ through some $h \in N_k \cap N_j$, with $g_j \le g_k$. So $c_{ik} \le c_{hk} + c_{hj} + c_{ij} \le g_k + 2 g_j \le 3 g_k$.
3. *Markov.* The LP sends more than $1 - \alpha$ of client $j$ to facilities at distance at least $g_j(\alpha)$, so $C_j > (1 - \alpha) \, g_j(\alpha)$.
4. *Averaging.* Since $g_j$ is the quantile function of the distances of $j$ under $x$, $\int_0^1 g_j(\alpha) \, d\alpha = C_j$. With $\alpha$ uniform on $(\beta, 1)$, the expected bound is $\frac{\ln(1/\beta)}{1 - \beta} F_{\text{LP}} + \frac{3}{1 - \beta} C_{\text{LP}}$. At $\beta = e^{-3}$ both factors equal $3 / (1 - e^{-3})$. Some level does at least as well as the average, and line L2 tries every distinct level.

**The lower bound used.** The LP value $F_{\text{LP}} + C_{\text{LP}}$.

**Integrality gap.** The example above has gap $7/6$. The gap of this LP is at least about $1.463$, matching the hardness result of Guha and Khuller (1999), and at most $1.488$, by the rounding of Li (2013).

## Complexity

- **Time.** One LP with $mn + m$ variables, in time $L$. For each of the at most $mn$ levels, computing all $g_j$ and $N_j$ takes $O(mn)$ time after sorting each client's facilities once. The clustering has at most $n$ centers, and each scans the remaining clients and compares near sets in $O(m)$ time each, so $O(n^2 m)$ per level. The total is $O(L + m^2 n^3)$ in the worst case. With a single fixed level, the rounding costs only $O(n^2 m)$.
- **Space.** The LP solution and the near sets take $O(mn)$ extra space.

## Properties

- **Bicriteria form.** Before clustering, filtering alone gives a fractional solution in which each client uses only facilities within $g_j(\alpha) \le C_j / (1 - \alpha)$, at facility cost at most $F_{\text{LP}} / \alpha$. This is the [filtering technique](/filtering-technique/) of Lin and Vitter.
- **Metric needed.** The connection bound uses the triangle inequality on a path of three edges.
- **Deterministic.** The algorithm tries all levels and keeps the best one, so it needs no random choices.
- **Uses an optimal LP solution.** Any feasible $(x, y)$ works in the proof, with $F_{\text{LP}}$ and $C_{\text{LP}}$ its own costs.

## Variants and improvements

- **Ratio 4 by one level.** At $\alpha = 1/4$ the bound is $4 F_{\text{LP}} + 4 C_{\text{LP}} = 4 \, \text{LP}$; this is the version in Williamson and Shmoys (Section 4.5).
- **Randomized rounding of the centers.** Chudak and Shmoys (2003) open each facility of a center's set at random in proportion to $y_i$, and open the other facilities independently. This gives $1 + 2/e \approx 1.736$.
- **Better ratios.** Byrka (2007) combined this rounding with the greedy algorithm of Jain, Mahdian and Saberi for 1.5, and Li (2013) got 1.488. No ratio below about $1.463$ is possible unless NP has slightly superpolynomial algorithms.
- **Primal-dual.** The [Jain-Vazirani](/jain-vazirani-facility-location/) algorithm gets 3 without solving the LP, and its proof uses the same three-edge path.
- **k-median.** Charikar, Guha, Tardos and Shmoys (2002) extended LP rounding to k-median with ratio $6 \frac{2}{3}$.

## When to use it

Use it when an LP solver is at hand and a simple deterministic rounding with a proof is wanted. The clustering idea of a center, its near set and all clients that touch it is the base of most later LP rounding for facility location, k-median and their variants. When speed matters more than a small ratio, the primal-dual or greedy algorithms avoid the LP.

## Pitfalls

- **Opening any facility near the center.** The cost bound needs the cheapest facility of $N_j$, not the nearest one. The nearest one can cost more than $\frac{1}{\alpha} \sum_{i \in N_j} f_i y_i$.
- **Choosing a center that is not the least $g_j$.** The bound $c_{ik} \le 3 g_k$ needs $g_j \le g_k$ for the center $j$. Taking clients in another order breaks it.
- **Keeping clients whose near sets overlap a center's.** If two centers have overlapping near sets, their facilities may be charged to the same $y_i$, and the facility bound fails.
- **Using $\alpha$ too close to 0 or 1.** At small $\alpha$ the facility cost $F_{\text{LP}} / \alpha$ grows, and at $\alpha$ near 1 the radius bound $C_j / (1 - \alpha)$ grows.

## Implementations

## History

Hochbaum (1982) gave an $O(\log n)$ ratio for facility location by reduction to set cover, and it is the best possible when the costs are not metric. Lin and Vitter (1992) introduced filtering and got constant factors with some violation of the constraints. Shmoys, Tardos and Aardal (1997) used filtering with clustering to give the first constant factor, 3.16, for the metric problem. It was followed by Guha and Khuller (1999) with 2.408 and by Chudak and Shmoys with $1 + 2/e$. Jain and Vazirani (2001) then gave a primal-dual 3, and a series of results led to Li's 1.488 (2013).

## References
