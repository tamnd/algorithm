---
tag: 9ZC0XC
kind: algorithm
slug: jain-vazirani-facility-location
name: Jain-Vazirani primal-dual facility location
aliases:
- primal-dual uncapacitated facility location
- Jain-Vazirani algorithm
area: approximation/lp-rounding
level: advanced
summary: Grow client duals until facilities are paid for, then keep a conflict-free set of them; a 3-approximation for metric facility location, and through Lagrangian relaxation a 6 for k-median.
solves: [facility-location-problem, k-median-problem]
model: real-ram
complexity:
  vars: {m: the number of facilities, n: the number of clients}
  time: {worst: O(m n log(m n))}
  space: {extra: O(m n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2001
  people: [Kamal Jain, Vijay V. Vazirani]
  note: Jain and Vazirani gave a combinatorial primal-dual 3-approximation for metric uncapacitated facility location, and used the stronger form of its guarantee with Lagrangian relaxation to get a 6-approximation for k-median.
prereqs: [facility-location-problem, primal-dual-schema, dual-linear-program, complementary-slackness, triangle-inequality]
see_also: [shmoys-tardos-aardal-facility-location, capacitated-facility-location, k-median-problem, lagrangian-relaxation, primal-dual-approximation, dual-fitting, goemans-williamson-steiner-forest, k-median-inapproximability]
sources:
  - paper: doi:10.1145/375827.375845
    title: Kamal Jain and Vijay V. Vazirani, Approximation algorithms for metric facility location and k-median problems using the primal-dual schema and Lagrangian relaxation, Journal of the ACM 48(2), 2001
    locator: Section 3 (facility location, factor 3) and Section 4 (k-median, factor 6)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 7.6 (uncapacitated facility location) and Section 7.7 (k-median by Lagrangean relaxation)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 24 (facility location) and Chapter 25 (k-median)
---

The Jain-Vazirani algorithm is a primal-dual 3-approximation for metric uncapacitated [facility location](/facility-location-problem/): open some facilities, each with an opening cost, and connect each client to an open one, so that the opening costs plus the connection costs are small. Each client raises a dual value $\alpha_j$, the amount it is willing to pay. Once $\alpha_j$ passes the distance to a facility, the excess goes toward that facility's opening cost. A facility opens for the moment when it is fully paid, and a client stops when it reaches an open facility. A second phase keeps only open facilities that no client pays for twice. The result costs at most $3 \sum_j \alpha_j \le 3 \cdot \text{OPT}$. In fact it gives the stronger bound $C + 3F \le 3 \sum_j \alpha_j$, and through [Lagrangian relaxation](/lagrangian-relaxation/) that bound gives a 6-approximation for [k-median](/k-median-problem/).

## In plain words

Each customer starts a clock and slowly raises the amount it will pay. When the amount covers the trip to a shop, the extra money starts to go toward building that shop. When a shop has collected its full price, it is ready, and every customer who can reach it with its money stops raising.

When all customers have stopped, some shops are ready, but a customer may have paid toward two of them. Keep the ready shops one by one, and skip a shop if some customer paid both it and a shop already kept. Then send each customer to its nearest kept shop.

A customer whose shop was skipped is not far from a kept shop, at most three times what it offered. So the total bill is at most three times the money offered, which is at most the best possible bill.

## The problem

There are facilities $i$ with opening costs $f_i \ge 0$ and clients $j$, with connection costs $c_{ij} \ge 0$ that satisfy the [triangle inequality](/triangle-inequality/) on facilities and clients together. A solution is a set $X$ of open facilities and an assignment of each client to some $i \in X$, with cost $F + C = \sum_{i \in X} f_i + \sum_j c_{\sigma(j) j}$. The LP relaxation and its dual are

$$\min \sum_i f_i y_i + \sum_{i, j} c_{ij} x_{ij} \ \text{ s.t. } \sum_i x_{ij} = 1, \ \ x_{ij} \le y_i, \ \ x, y \ge 0,$$

$$\max \sum_j \alpha_j \ \text{ s.t. } \sum_j \beta_{ij} \le f_i, \ \ \alpha_j - \beta_{ij} \le c_{ij}, \ \ \beta \ge 0.$$

In a dual solution, $\beta_{ij} = \max(0, \alpha_j - c_{ij})$ is the part of client $j$'s payment that goes to facility $i$. By [weak duality](/weak-duality/), each feasible dual has $\sum_j \alpha_j \le \text{LP} \le \text{OPT}$.

## The algorithm

```pseudo id=main
JAIN-VAZIRANI(f, c)
L1  α_j ← 0 for each client j; all clients are active; no facility is open
L2  while some client is active do
L3      raise α_j of all active clients at the same rate, up to the next event time t
L4      a facility with Σ_j max(0, α_j − c_ij) = f_i becomes temporarily open
L5      an active client with α_j ≥ c_ij for a temporarily open i is frozen; i is its witness
L6  X ← ∅
L7  for each temporarily open facility i, in order of opening, do
L8      if no client j has β_ij > 0 and β_kj > 0 for some k ∈ X then add i to X
L9  connect each client to its nearest facility in X
L10 return X and the assignment
```

The events of line L3 are of two kinds: a client reaches the distance $c_{ij}$ to a facility, or the payments to a closed facility reach $f_i$. Between events the payments grow linearly, so each event time is the root of a linear equation. Line L4 can open several facilities at one time, and lines L4 and L5 repeat at that time until nothing changes. Frozen clients keep their $\alpha_j$ for the rest of the run. Phase 2 (lines L6 to L8) picks a maximal set of temporarily open facilities in which no client pays two facilities. The simple version here uses the opening order. Jain and Vazirani state it as a maximal independent set in a conflict graph.

## Example

Facilities $A, B, C$ are at points $1, 4, 6$ on a line, with costs $f_A = 2$, $f_B = 2$, $f_C = 3$. Clients are at $0, 2, 5, 8$, and $c_{ij}$ is the distance.

| time $t$ | event |
|---|---|
| 1 | clients 0 and 2 reach $A$; client 5 reaches $B$ and $C$ |
| 2 | $A$ is paid $1 + 1 = 2$ and opens; clients 0 and 2 freeze with $\alpha = 2$; client 8 reaches $C$ |
| 3 | $B$ is paid $2$ by client 5, and $C$ is paid $2 + 1 = 3$ by clients 5 and 8; both open; clients 5 and 8 freeze with $\alpha = 3$ |

So $\alpha = (2, 2, 3, 3)$ and $\sum_j \alpha_j = 10$. The payments are as follows.

| client | $\beta_{Aj}$ | $\beta_{Bj}$ | $\beta_{Cj}$ | witness |
|---|---|---|---|---|
| 0 | 1 | 0 | 0 | $A$ |
| 2 | 1 | 0 | 0 | $A$ |
| 5 | 0 | 2 | 2 | $B$ |
| 8 | 0 | 0 | 1 | $C$ |

Phase 2 takes $A$, then $B$, which shares no paying client with $A$. It skips $C$, since client 5 pays both $B$ and $C$. Clients 0 and 2 go to $A$ at cost 1 each, and clients 5 and 8 go to $B$ at cost 1 and 4. So $F = 4$, $C = 7$ and the cost is 11. The optimum opens $A$ and $C$ for $5 + 5 = 10$, so here $\sum_j \alpha_j = \text{LP} = \text{OPT} = 10$.

Client 8 is the indirect case: its witness $C$ was skipped. The proof routes it through client 5, which paid both $C$ and $B$: $c_{B8} \le c_{C8} + c_{C5} + c_{B5} = 2 + 1 + 1 = 4 \le 3 \alpha_8 = 9$. The stronger bound holds as well: $C + 3F = 7 + 12 = 19 \le 3 \cdot 10$.

## Correctness

**Theorem (Jain and Vazirani 2001).** The algorithm returns a solution with $C + 3F \le 3 \sum_j \alpha_j$ for a feasible dual $\alpha$, so the cost is at most $3 \cdot \text{OPT}$.

The proof has four steps, given in full in the proof file below.

1. *Dual feasibility.* A closed facility opens the moment its payments reach $f_i$, and after it opens, every client that reaches it freezes. So $\sum_j \beta_{ij} \le f_i$ always.
2. *Facility cost.* Each facility in $X$ is paid exactly $f_i$, and no client pays two facilities of $X$. So $F = \sum_{j \text{ direct}} \beta_{\phi(j) j}$, where a client is *direct* if it pays some $\phi(j) \in X$.
3. *Direct clients.* A direct client has $c_{\phi(j) j} = \alpha_j - \beta_{\phi(j) j}$, so its connection cost plus three times its payment is at most $3 \alpha_j - 2c_{\phi(j)j} \le 3 \alpha_j$.
4. *Indirect clients.* Let $i$ be the witness of $j$. If $i \in X$, then $c_{ij} \le \alpha_j$. Otherwise $i$ was skipped because some client $j'$ pays both $i$ and some $i' \in X$. Then $c_{ij'}, c_{i'j'} < \alpha_{j'}$, and $\alpha_{j'} \le t_i \le \alpha_j$, where $t_i$ is the time when $i$ opened. By the triangle inequality, $c_{i'j} \le c_{ij} + c_{ij'} + c_{i'j'} \le 3 \alpha_j$.

Adding over the clients gives $C + 3F \le 3 \sum_j \alpha_j$, and weak duality gives $\sum_j \alpha_j \le \text{OPT}$.

**The lower bound used.** The dual value $\sum_j \alpha_j$, which is at most the LP value.

**Hardness.** No polynomial algorithm has ratio below about $1.463$ for metric facility location unless NP has slightly superpolynomial algorithms (Guha and Khuller 1999). So constant ratios are the right goal.

## Complexity

- **Time.** With $m$ facilities and $n$ clients, there are $mn$ pairs. Sort the pairs by $c_{ij}$ once, in $O(mn \log(mn))$ time, and keep the facility events in a priority queue. Each event changes the rate of payment of one facility or freezes clients, and each pair causes $O(1)$ events. So phase 1 takes $O(mn \log(mn))$ time, as Jain and Vazirani show. Phase 2 and the assignment take $O(mn)$ time with a mark for each client. The implementation below recomputes all event times at each event, which is slower but simpler.
- **Space.** The pairs, the payments and the queue take $O(mn)$ extra space.

## Properties

- **Lagrangian multiplier preserving.** The bound $C + 3F \le 3 \sum_j \alpha_j$ is stronger than $C + F \le 3 \sum_j \alpha_j$. It says the facility cost is counted three times with no loss, which is what the k-median reduction needs.
- **Combinatorial.** No LP is solved; the dual is grown directly, so the method is fast and exact.
- **Metric needed.** Step 4 uses the triangle inequality three times. With general costs, set cover is a special case, and no constant ratio is possible.
- **Deterministic.** Ties are broken by a fixed rule, and the output depends only on the input.

## Variants and improvements

- **k-median (sketch).** Give every facility the same cost $z$ and run the algorithm. With $z = 0$ all facilities open, and with a large $z$ only one opens, so a binary search finds $z_1 < z_2$, very close, with solutions of sizes $k_1 > k > k_2$. If some $z$ gives exactly $k$ facilities, the bound $C \le 3(\sum_j \alpha_j - kz)$ and $\sum_j \alpha_j - kz \le \text{OPT}_k$ give ratio 3 directly. Otherwise a convex combination of the two solutions is a fractional solution with $k$ facilities and cost at most $3 \cdot \text{OPT}_k$, up to a tiny error. Jain and Vazirani round it to $k$ facilities with a loss of factor 2, for ratio 6. This part is only sketched here.
- **Better ratios for facility location.** Dual fitting gives 1.861 and 1.61 (Jain, Mahdian, Markakis, Saberi and Vazirani 2003). With scaling, Mahdian, Ye and Zhang (2006) got 1.52. Byrka (2007) got 1.5 by combining LP rounding with these, and Li (2013) got 1.488.
- **Better ratios for k-median.** The LMP factor 2 of Jain, Mahdian and Saberi gives 4. Local search gives $3 + \varepsilon$ (Arya et al. 2004). The pseudo-approximation method of Li and Svensson (2013) gives $1 + \sqrt{3} + \varepsilon$, and later work went below that.
- **Other problems.** The same method works for facility location with outliers and penalties, and for the version where each facility can be opened several times at a cost per copy.

## When to use it

Use it for metric facility location when an LP solver is too slow or not at hand, and a guarantee is needed. It runs in near linear time in the number of pairs. If ratio matters most, the greedy dual fitting methods give 1.61 with similar speed. Use the Lagrangian form when the number of facilities is fixed, as in k-median, but expect the factor 2 rounding to make it worse in practice than local search.

## Pitfalls

- **Opening all temporarily open facilities.** A client can pay several of them, so their total cost can be far more than $\sum_j \alpha_j$. Phase 2 is needed.
- **Letting payments go up after opening.** A client that reaches an open facility must freeze at once. If it keeps raising its $\alpha_j$, the payments to that facility pass $f_i$, and the dual is no longer feasible.
- **A wrong witness.** The witness of a frozen client is the open facility it reached. The proof needs $t_i \le \alpha_j$ for that facility; a facility that opened later does not work.
- **Using the factor 3 for non-metric costs.** The proof routes through three edges. Without the triangle inequality, the indirect clients can be arbitrarily far from $X$.

## Implementations

## History

Shmoys, Tardos and Aardal (1997) gave the first constant ratio for metric facility location, 3.16, by LP rounding. Jain and Vazirani (1999 conference, 2001 journal) gave a primal-dual 3-approximation that solves no LP, and noted that its guarantee is Lagrangian multiplier preserving. They used this to get a 6-approximation for k-median, the first one based on the primal-dual schema; Charikar, Guha, Tardos and Shmoys had shortly before given a $6\frac{2}{3}$ by LP rounding. The idea of growing duals and taking a conflict-free subset came from the network design algorithms of Goemans and Williamson.

## References
