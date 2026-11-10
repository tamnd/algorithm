---
tag: NV7H45
kind: algorithm
slug: ranking-algorithm
name: Ranking algorithm
aliases:
- RANKING
- Karp-Vazirani-Vazirani algorithm
- KVV algorithm
area: online-and-streaming/competitive-analysis
level: research
summary: Draws one random order of the offline vertices and matches each arrival to its free neighbour that comes first in it; ratio 1 - 1/e against an oblivious adversary, the best possible.
solves: [online-bipartite-matching]
model: word-ram
complexity:
  vars: {n: the number of online vertices, m: the number of edges, k: the number of offline vertices}
  time: {worst: O(m + k)}
  space: {extra: O(k)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1990
  people: [Richard M. Karp, Umesh V. Vazirani, Vijay V. Vazirani]
  note: Karp, Vazirani and Vazirani introduced Ranking and the bound 1 - 1/e with a matching upper bound; a gap in their analysis was later repaired by Goel and Mehta (2008), and short proofs were given by Birnbaum and Mathieu (2008) and by Devanur, Jain and Kleinberg (2013).
prereqs: [online-bipartite-matching, greedy-online-matching, randomized-online-algorithm, oblivious-adversary]
see_also: [balance-algorithm, online-adwords-problem, online-primal-dual, yao-minimax-principle, weak-duality, maximum-matching]
sources:
  - paper: doi:10.1145/100216.100262
    title: "Richard M. Karp, Umesh V. Vazirani and Vijay V. Vazirani, An optimal algorithm for on-line bipartite matching, Proceedings of the 22nd Annual ACM Symposium on Theory of Computing (STOC 1990), 352-358"
    locator: the algorithm RANKING, the bound 1 - 1/e, and the upper triangular upper bound
  - paper: doi:10.1137/1.9781611973105.7
    title: "Nikhil R. Devanur, Kamal Jain and Robert D. Kleinberg, Randomized primal-dual analysis of RANKING for online bipartite matching, Proceedings of the 24th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 2013), 101-107"
    locator: the continuous ranks y_u, the split g(y) = e^(y-1), and the proof that the dual is feasible in expectation
  - paper: doi:10.1145/1360443.1360462
    title: "Benjamin Birnbaum and Claire Mathieu, On-line bipartite matching made simple, ACM SIGACT News 39(1) (2008), 80-87"
    locator: the short combinatorial proof of the bound 1 - 1/e and the lemma on free sets when one offline vertex is removed
  - paper: "Gagan Goel and Aranyak Mehta, Online budgeted matching in random input models with applications to Adwords, Proceedings of the 19th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 2008), 982-991"
    title: Goel and Mehta 2008
    locator: the corrected proof of the KVV lemma for RANKING
  - paper: doi:10.1561/0400000057
    title: "Aranyak Mehta, Online matching and ad allocation, Foundations and Trends in Theoretical Computer Science 8(4) (2013), 265-368"
    locator: Chapter 3, RANKING and its analyses, and the chapter on vertex weights
---

Ranking is a randomized algorithm for [online bipartite matching](/online-bipartite-matching/). Before the first arrival it draws one uniform random order of the offline vertices, and it then matches each arriving vertex to its free neighbour that comes first in that order. Karp, Vazirani and Vazirani (1990) showed that the expected size of the matching is at least $1 - 1/e \approx 0.632$ times the maximum, against an [oblivious adversary](/oblivious-adversary/), and that no randomized algorithm does better. The bound beats the $1/2$ of every deterministic rule, and it comes from one correlated random choice, not from a fresh coin at each step.

## In plain words

Before any job comes in, shuffle the list of workers once and keep this order. When a job arrives, give it to the free worker who can do it and who is highest in the shuffled order. If no such worker is free, turn the job away.

A fixed order lets a sly sender of jobs predict each choice and steer jobs onto the wrong workers. A coin tossed for each job is not enough: the sender can still make the good choices rare. One shared random order spreads the risk well: on every input, the expected number of served jobs is almost two thirds of the best possible, and no rule can promise more on all inputs.

## The problem

The input is a bipartite graph $G = (U \cup V, E)$ with offline side $U$, $\lvert U \rvert = k$, known at the start, and online vertices $v_1, \ldots, v_n$ that arrive one at a time with their neighbour sets $N(v_t) \subseteq U$. Each $v_t$ must be matched to a free neighbour or left unmatched, at once and for good. $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the sizes of the online matching and of a [maximum matching](/maximum-matching/). The goal is $\mathbb{E}[\mathrm{ALG}(\sigma)] \ge c \cdot \mathrm{OPT}(\sigma)$ for every $\sigma$ with $c \le 1$ as large as possible, where $\sigma$ is fixed before the random choices (oblivious adversary).

## The algorithm

```pseudo id=main
RANKING(U, σ, rng)                                 ▷ σ = v_1 .. v_n, revealed one at a time
L1  draw a uniform random permutation π of U       ▷ rank(u) = position of u in π
L2  F ← U, M ← ∅
L3  for t ← 1 to n do
L4      receive v_t and N(v_t)
L5      C ← N(v_t) ∩ F
L6      if C ≠ ∅ then
L7          u ← the vertex of C with the smallest rank
L8          M ← M ∪ {(u, v_t)}, F ← F \ {u}
L9  return M
```

For the analysis it is easier to let each $u$ draw a real $y_u$ uniform in $[0, 1]$, and to rank by $y$. The sorted order is a uniform permutation, so this is the same algorithm. Lines L2 to L9 are [greedy online matching](/greedy-online-matching/) with a fixed tie-break order; all the randomness is in line L1.

## Example

Take the upper triangular instance with $n = 3$: $N(v_1) = \{u_1, u_2, u_3\}$, $N(v_2) = \{u_2, u_3\}$, $N(v_3) = \{u_3\}$. The maximum matching $v_1 u_1, v_2 u_2, v_3 u_3$ has size 3. Ranking gets the following for each of the 6 orders.

| order $\pi$ | $v_1$ | $v_2$ | $v_3$ | size |
|---|---|---|---|---|
| $u_1, u_2, u_3$ | $u_1$ | $u_2$ | $u_3$ | 3 |
| $u_1, u_3, u_2$ | $u_1$ | $u_3$ | unmatched | 2 |
| $u_2, u_1, u_3$ | $u_2$ | $u_3$ | unmatched | 2 |
| $u_2, u_3, u_1$ | $u_2$ | $u_3$ | unmatched | 2 |
| $u_3, u_1, u_2$ | $u_3$ | $u_2$ | unmatched | 2 |
| $u_3, u_2, u_1$ | $u_3$ | $u_2$ | unmatched | 2 |

The expected size is $13/6 \approx 2.167$, a ratio of $0.722 \ge 1 - 1/e$. Only the order that puts $u_1$ first and $u_2$ second avoids the loss. On the same family the exact expectation is $67/24$, $137/40$, $2921/720$ and $23633/5040 \approx 4.689$ for $n = 4, \ldots, 7$, and the ratio decreases toward $1 - 1/e$ as $n$ grows: the upper triangular instance is the one that makes the bound tight.

**The dual split.** In the proof, a matched pair $(u, v)$ with value $y_u$ gives $\alpha_u = e^{y_u - 1}/(1 - 1/e)$ to the offline vertex and $\beta_v = (1 - e^{y_u - 1})/(1 - 1/e)$ to the online vertex. A vertex with a small $y$ is matched early and often, so it keeps a small share; one with a large $y$ is matched only when nothing better is free, so it keeps a large share.

## Correctness

The [proof](proofs/correctness.md) follows Devanur, Jain and Kleinberg. Validity is the same as for greedy. For the ratio, the gain $1/(1 - 1/e)$ of each matched pair is split into $\alpha_u + \beta_v$ as above. For an edge $(u, v)$, fix all $y$ values other than $y_u$ and run Ranking without $u$; let $y^c$ be the value of the partner of $v$ in that run, or 1. Adding $u$ changes the free sets by at most one vertex at each step, and only by making them larger. From this, $u$ is matched whenever $y_u < y^c$, and $v$ is always matched to a vertex with value at most $y^c$. So $\mathbb{E}[\alpha_u + \beta_v] \ge \int_0^{y^c} e^{y-1} dy + 1 - e^{y^c - 1}$, divided by $1 - 1/e$, which is exactly 1 for every $y^c$. Summing over the edges of a maximum matching gives $\mathbb{E}[\mathrm{ALG}] \ge (1 - 1/e)\,\mathrm{OPT}$.

## Complexity

- **Time.** Line L1 costs $O(k)$ with the Fisher-Yates shuffle. With $F$ as an array over $U$, line L5 and line L7 cost $O(\deg v_t)$, so the whole run is $O(m + k)$, where $m = \sum_t \deg v_t$.
- **Space.** $O(k)$ for the ranks and the free flags.
- **Randomness.** One permutation of $U$, that is $\log_2 k!$ random bits, all drawn before the first arrival. The rest is deterministic.

## Properties

- **Competitive ratio $1 - 1/e$.** $\mathbb{E}[\mathrm{ALG}(\sigma)] \ge (1 - 1/e)\,\mathrm{OPT}(\sigma)$ for every $\sigma$, with no additive term, against an oblivious adversary.
- **Optimal.** By the upper triangular instance and [Yao's principle](/yao-minimax-principle/), no randomized online algorithm has a ratio above $1 - 1/e + O(1/n)$ ([online bipartite matching](/online-bipartite-matching/), Theorem 3).
- **Greedy for every order.** Each outcome of line L1 gives a greedy run, so $\mathrm{ALG} \ge \mathrm{OPT}/2$ always holds, not only in expectation.
- **Not better against an adaptive adversary.** An adversary that sees the matches as they happen holds Ranking to $1/2$, as it does every algorithm.
- **One correlated choice matters.** RANDOM, which draws a fresh uniform free neighbour at each step, has ratio only $1/2 + o(1)$. On the RANDOM bad family with $k = 3$ (6 offline vertices), Ranking has exact expectation $517/120 \approx 4.31$ against $763/192 \approx 3.97$ for RANDOM.
## Variants and improvements

- **Vertex weights.** Aggarwal, Goel, Karande and Mehta (2011) rank by $w_u (1 - e^{y_u - 1})$, a perturbed weight, and keep the ratio $1 - 1/e$ for the total weight of the matched offline vertices.
- **Budgets and $b$-matching.** When an offline vertex can take $b$ arrivals, the deterministic [Balance algorithm](/balance-algorithm/) gets $1 - (1 + 1/b)^{-b}$, which tends to the same $1 - 1/e$. With small bids, the [online adwords problem](/online-adwords-problem/) has the same limit.
- **Random arrival order.** If the online vertices arrive in a uniform random order, Ranking gets at least $0.696$ (Mahdian and Yan 2011) and at most $0.727$ (Karande, Mehta and Tripathi 2011).
- **Primal-dual view.** The proof is an instance of the [online primal-dual method](/online-primal-dual/), with a dual that is feasible only in expectation.

## When to use it

Use Ranking when offline vertices take one arrival each, when the order of arrivals may be adversarial but cannot react to the coins, and when the worst-case ratio matters. It costs one shuffle more than greedy. When capacities are large, use Balance, which needs no randomness and approaches the same ratio. When arrivals are random or drawn from a known distribution, algorithms built for those models do better than $1 - 1/e$.

## Pitfalls

- **Redrawing the order.** The order must be drawn once, before the first arrival. A new random choice at each step is RANDOM, which is $1/2 + o(1)$.
- **Ranking the online side.** The random order is over the offline vertices, the side that is known in advance.
- **Claiming the bound against an adaptive adversary.** An adversary that sees the matches can hold every algorithm to $1/2$.
- **Trusting the original proof.** A key lemma in the 1990 paper had a gap. Use one of the corrected proofs: Goel and Mehta (2008), Birnbaum and Mathieu (2008), or Devanur, Jain and Kleinberg (2013).
- **Expecting the bound on small instances to be tight.** On small graphs the exact ratio is well above $1 - 1/e$; the bound is reached only as $n$ grows on the upper triangular family.

## Implementations

## History

Karp, Vazirani and Vazirani introduced Ranking at STOC 1990, proved the ratio $1 - 1/e$, and showed with the upper triangular instance that it is optimal. A gap in the proof of one of their lemmas was found later (the error is credited to Krohn and Varadarajan), and Goel and Mehta (2008) gave a corrected proof as part of their work on budgeted matching. Birnbaum and Mathieu (2008) gave a short combinatorial proof, and Devanur, Jain and Kleinberg (2013) recast it as a randomized primal-dual argument, which is the proof on this page. The method has since been used for vertex weights, budgets and many other variants of online matching.

## References
