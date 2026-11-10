---
tag: QHSMWD
kind: algorithm
slug: balance-algorithm
name: Balance algorithm
aliases:
- MSVV algorithm
- Balance
- water-filling
area: online-and-streaming/competitive-analysis
level: advanced
summary: For online b-matching, sends each arrival to the neighbour with room and the smallest load; deterministic ratio 1 - (1 + 1/b)^(-b), which tends to 1 - 1/e. MSVV extends it to budgets.
solves: [online-bipartite-matching, online-adwords-problem]
model: word-ram
complexity:
  vars: {n: the number of online vertices, m: the number of edges, k: the number of offline vertices, b: the capacity of each offline vertex}
  time: {worst: O(m + k)}
  space: {extra: O(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2000
  people: [Bala Kalyanasundaram, Kirk R. Pruhs]
  note: Kalyanasundaram and Pruhs proved that Balance is 1 - (1 + 1/b)^(-b) competitive for online b-matching and that no deterministic algorithm does better; Mehta, Saberi, Vazirani and Vazirani (2007) extended it to budgets and bids.
prereqs: [online-bipartite-matching, b-matching, weak-duality]
see_also: [ranking-algorithm, greedy-online-matching, online-adwords-problem, online-primal-dual, fractional-matching, dual-linear-program]
sources:
  - paper: doi:10.1016/S0304-3975(99)00140-1
    title: "Bala Kalyanasundaram and Kirk R. Pruhs, An optimal deterministic algorithm for online b-matching, Theoretical Computer Science 233(1-2) (2000), 319-325"
    locator: the algorithm Balance, the bound 1 - 1/(1 + 1/b)^b, and the matching lower bound for deterministic algorithms
  - paper: doi:10.1145/1284320.1284321
    title: "Aranyak Mehta, Amin Saberi, Umesh Vazirani and Vijay Vazirani, AdWords and generalized online matching, Journal of the ACM 54(5) (2007), Article 22"
    locator: the analysis of Balance by factor-revealing LPs and the tradeoff function psi(f) = 1 - e^(f - 1) for budgets and bids
  - paper: doi:10.1561/0400000024
    title: "Niv Buchbinder and Joseph (Seffi) Naor, The design of competitive online algorithms via a primal-dual approach, Foundations and Trends in Theoretical Computer Science 3(2-3) (2009), 93-263"
    locator: Chapter 10 (the ad auctions problem), the primal-dual algorithm and its analysis
  - paper: doi:10.1561/0400000057
    title: "Aranyak Mehta, Online matching and ad allocation, Foundations and Trends in Theoretical Computer Science 8(4) (2013), 265-368"
    locator: the chapters on b-matching and Balance, and on budgeted allocation with small bids
---

Balance is a deterministic algorithm for online [b-matching](/b-matching/), the form of [online bipartite matching](/online-bipartite-matching/) in which each offline vertex can be matched to up to $b$ online vertices. It sends each arriving vertex to a neighbour that still has room and has the smallest load. Kalyanasundaram and Pruhs (2000) showed that it matches at least $1 - (1 + 1/b)^{-b}$ times the optimum, and that no deterministic algorithm does better. The ratio is $1/2$ for $b = 1$, $5/9$ for $b = 2$, and it tends to $1 - 1/e$ as $b$ grows, the same limit as the randomized [Ranking algorithm](/ranking-algorithm/), but with no randomness at all.

## In plain words

Each worker can take a fixed number of jobs. When a job arrives, give it to the worker on its list who has the fewest jobs so far and still has room.

Keeping the workers level is a hedge. Nobody knows which workers the future jobs will need. A worker with few jobs has the most room left for those jobs, and filling the emptiest worker never wastes the room of a worker who is close to full. When each worker can take many jobs, this simple rule does almost as well as the best random rule for single jobs, and no fixed rule can do better.

## The problem

The input is a bipartite graph $G = (U \cup V, E)$ with offline side $U$, $\lvert U \rvert = k$, and a capacity $b \ge 1$ for each offline vertex. The online vertices $v_1, \ldots, v_n$ arrive one at a time with their neighbour sets $N(v_t) \subseteq U$. Each $v_t$ must be assigned at once and for good to a neighbour with fewer than $b$ assigned vertices, or left unassigned. $\mathrm{ALG}(\sigma)$ is the number of assigned vertices and $\mathrm{OPT}(\sigma)$ is the size of a maximum $b$-matching. The ratio convention is $\mathrm{ALG}(\sigma) \ge c \cdot \mathrm{OPT}(\sigma)$ with $c \le 1$ and no additive term.

## The algorithm

```pseudo id=main
BALANCE(U, b, σ)                                     ▷ σ = v_1 .. v_n, revealed one at a time
L1  load(u) ← 0 for each u ∈ U, M ← ∅
L2  for t ← 1 to n do
L3      receive v_t and N(v_t)
L4      C ← {u ∈ N(v_t) : load(u) < b}                 ▷ neighbours with room
L5      if C ≠ ∅ then
L6          u ← a vertex of C with the smallest load; load(u) ← load(u) + 1
L7          M ← M ∪ {(u, v_t)}
L8  return M
```

Ties at line L6 may be broken in any way. The proof keeps a dual price $\alpha_u = A(\mathrm{load}(u))$ with $A(\ell) = (r^\ell - 1)/(r^b - 1)$ and $r = 1 + 1/b$, and gives each assigned online vertex the share $\beta_v = 1 - A(\ell)$, where $\ell$ is the load of its partner just before the assignment. The algorithm does not need these numbers; the implementation keeps them to check the proof.

## Example

Take $b = 2$, offline vertices $u_1, u_2, u_3$, and six arrivals in three rounds of two: first on $\{u_1, u_2, u_3\}$, then on $\{u_1, u_2\}$, then on $\{u_2\}$. Ties go to the vertex listed first. With $r = 3/2$, the prices are $A(0) = 0$, $A(1) = 0.4$ and $A(2) = 1$.

| $t$ | $N(v_t)$ | loads before ($u_1, u_2, u_3$) | assigned to | $\beta_{v_t}$ |
|---|---|---|---|---|
| 1 | $u_1, u_2, u_3$ | 0, 0, 0 | $u_1$ | 1 |
| 2 | $u_1, u_2, u_3$ | 1, 0, 0 | $u_2$ | 1 |
| 3 | $u_1, u_2$ | 1, 1, 0 | $u_1$ | 0.6 |
| 4 | $u_1, u_2$ | 2, 1, 0 | $u_2$ | 0.6 |
| 5 | $u_2$ | 2, 2, 0 | unassigned | 0 |
| 6 | $u_2$ | 2, 2, 0 | unassigned | 0 |

Balance assigns 4. The optimum assigns all 6: $v_1, v_2$ to $u_3$, $v_3, v_4$ to $u_1$, and $v_5, v_6$ to $u_2$. The final prices are $\alpha = (1, 1, 0)$, so the dual value is $2 \cdot 2 + 3.2 = 7.2 = 4 / (5/9)$, and each edge has $\alpha_u + \beta_v \ge 1$; for example $(u_3, v_1)$ has $0 + 1$. So $\mathrm{OPT} \le 7.2$ and $4 \ge (5/9) \cdot 6$.

**Near-tight instances.** Repeat the rounds with $n$ offline vertices: round $t$ brings $b$ arrivals adjacent to the vertices still in play, and after the round the adversary removes the one with the smallest load, which is the optimum partner of that round. For $n = 200$, Balance gets ratio $0.5$, $0.5575$, $0.58$ and $0.6$ for $b = 1, 2, 3, 5$, against the bounds $0.5$, $0.5556$, $0.5781$ and $0.5981$.

## Correctness

The [proof](proofs/correctness.md) is a primal-dual argument. Validity is clear: line L4 keeps only neighbours with room. For the ratio, each assignment at load $\ell$ raises the dual $b\sum_u \alpha_u + \sum_v \beta_v$ by $b(A(\ell+1) - A(\ell)) + 1 - A(\ell)$, which is exactly $1/(1 - r^{-b})$ for every $\ell$; this is why $A$ is a geometric sequence with ratio $1 + 1/b$. The dual is feasible: for an edge $(u, v)$, either $u$ was full when $v$ arrived, so $\alpha_u = 1$, or $v$ went to a vertex whose load $\ell^*$ was at most that of $u$, so $\alpha_u \ge A(\ell^*) = 1 - \beta_v$. By [weak duality](/weak-duality/), $\mathrm{OPT} \le \mathrm{ALG}/(1 - (1 + 1/b)^{-b})$.

## Complexity

- **Time.** Line L4 and the minimum at line L6 cost $O(\deg v_t)$ with the loads in an array, so the run costs $O(m + k)$.
- **Space.** $O(k)$ for the loads.
- **No randomness.** The rule is deterministic, which helps when decisions must be reproducible or audited.

## Properties

- **Ratio $1 - (1 + 1/b)^{-b}$.** For every input, $\mathrm{ALG} \ge (1 - (1 + 1/b)^{-b})\,\mathrm{OPT}$, also against the fractional optimum.
- **Optimal among deterministic algorithms.** Kalyanasundaram and Pruhs (2000) showed that no deterministic online algorithm for $b$-matching has a better ratio.
- **Limit $1 - 1/e$.** As $b \to \infty$ the ratio rises to $1 - 1/e$, which is also the best ratio of any randomized algorithm for large $b$, by the upper triangular instance with blocks.
- **Same as greedy for $b = 1$.** With $b = 1$ every neighbour with room has load 0, so Balance is a greedy rule with ratio $1/2$.
- **Fractional limit.** Splitting each arrival continuously over the least loaded neighbours (water-filling) gives the fractional algorithm with ratio exactly $1 - 1/e$.

## Variants and improvements

- **MSVV for budgets and bids.** In the [online adwords problem](/online-adwords-problem/), advertiser $i$ has budget $B_i$ and bids $b_{ij}$. Mehta, Saberi, Vazirani and Vazirani (2007) give query $j$ to the advertiser that maximizes $b_{ij}\,\psi(f_i)$, where $f_i$ is the fraction of the budget spent and $\psi(f) = 1 - e^{f-1}$. With equal bids it is Balance; with small bids its ratio tends to $1 - 1/e$. This is the algorithm that the alias "MSVV algorithm" refers to.
- **Primal-dual form.** Buchbinder, Jain and Naor (2007) keep a price $x_i$ per advertiser, give query $j$ to the advertiser that maximizes $b_{ij}(1 - x_i)$, and raise $x_i$ multiplicatively. Their ratio is $(1 - 1/c)(1 - R_{\max})$ with $c = (1 + R_{\max})^{1/R_{\max}}$, where $R_{\max}$ is the largest ratio of a bid to its budget ([online primal-dual](/online-primal-dual/)).
- **Randomized algorithms for small $b$.** For $b = 1$, Ranking gets $1 - 1/e$ against an oblivious adversary, far above the $1/2$ of Balance.

## When to use it

Use Balance when each offline vertex has a large capacity, such as an advertiser with many impressions or a server with many slots, and a deterministic rule is wanted. For capacity one, use Ranking, which needs randomness but gets $1 - 1/e$. With bids and budgets, use the MSVV rule or its primal-dual form.

## Pitfalls

- **Filling the fullest vertex.** "First fit" or "most loaded first" is greedy and has ratio only $1/2$ for every $b$. The gain of Balance comes from the choice of the least loaded neighbour.
- **Counting full vertices as candidates.** A vertex at load $b$ has no room; it must be removed at line L4, not merely ranked last.
- **Using the limit for small $b$.** The ratio $1 - 1/e$ is a limit. For $b = 2$ the guarantee is only $5/9 \approx 0.556$.
- **Plain Balance with bids.** With unequal bids, choosing by the spent fraction alone ignores the size of the bid, and choosing by the bid alone is the greedy rule, which is only $1/2$-competitive. The MSVV rule weights the bid by $\psi$ of the spent fraction.

## Implementations

## History

Kalyanasundaram and Pruhs studied online $b$-matching and proved in 2000 that Balance is $1 - 1/(1 + 1/b)^b$-competitive and that this is optimal for deterministic algorithms. Mehta, Saberi, Vazirani and Vazirani (FOCS 2005, JACM 2007) used the idea for the adwords problem: they analysed Balance with factor-revealing LPs and found the tradeoff function $\psi(f) = 1 - e^{f-1}$, which gives $1 - 1/e$ for small bids. Buchbinder, Jain and Naor (2007) recovered this ratio with the online primal-dual method, which is the style of the proof on this page.

## References
