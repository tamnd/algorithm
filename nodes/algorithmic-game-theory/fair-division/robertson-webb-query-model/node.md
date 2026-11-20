---
tag: S2HRZZ
kind: model
slug: robertson-webb-query-model
name: Robertson-Webb query model
aliases:
- cut and eval queries
area: algorithmic-game-theory/fair-division
level: core
summary: A model in which a cake cutting protocol learns valuations only by eval queries for the value of a piece and cut queries for a piece of given value.
prereqs: [cake-cutting-problem, query-model]
see_also: [even-paz-algorithm, edmonds-pruhs-lower-bound, last-diminisher, dubins-spanier-moving-knife, comparison-model, decision-tree-model, adversary-argument, stromquist-impossibility-theorem]
sources:
  - book: isbn:9781568810768
    title: Jack Robertson and William Webb, Cake-Cutting Algorithms, Be Fair If You Can, A K Peters, 1998
    locator: the cut and evaluate steps that the protocols of the book use; Chapter 10, Exact and Envy-Free Algorithms
  - paper: doi:10.1016/j.disopt.2006.07.003
    title: Gerhard J. Woeginger and Jiri Sgall, On the complexity of cake cutting, Discrete Optimization 4(2) (2007)
    locator: pp. 213-220 (the formal statement of the model and the lower bound of Omega(n log n) for connected pieces)
  - paper: doi:10.1145/2000807.2000819
    title: Jeff Edmonds and Kirk Pruhs, Cake cutting really is not a piece of cake, ACM Transactions on Algorithms 7(4) (2011)
    locator: Article 51; Section 2, Theorem 4 (the deterministic lower bound), and Section 3 (randomized protocols with approximate queries)
  - book: isbn:9781107060432
    title: Felix Brandt, Vincent Conitzer, Ulle Endriss, Jerome Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016
    locator: Chapter 13, Ariel D. Procaccia, Cake Cutting Algorithms, Section 13.4, complexity of cake cutting (from p. 316)
---

The Robertson-Webb query model is the standard [query model](/query-model/) for [cake cutting](/cake-cutting-problem/). A protocol does not see the valuations of the agents. It learns about them only by two kinds of questions: an eval query asks an agent for the value of an interval, and a cut query asks an agent for the point where an interval reaches a given value. The cost of a protocol is the number of queries; all other work is free. The model makes statements such as "proportional division needs $\Theta(n \log n)$ queries" precise, in the same way that the [comparison model](/comparison-model/) does for sorting.

## The machine

The cake is $[0, 1]$. There are $n$ agents. Agent $i$ has a valuation $V_i$ that is nonnegative, additive and nonatomic, with $V_i([0, 1]) = 1$. The valuations are hidden. The protocol can ask two kinds of queries, each addressed to one agent.

- $\mathrm{Eval}_i(x, y)$, for $0 \le x \le y \le 1$, returns $V_i([x, y])$.
- $\mathrm{Cut}_i(x, \alpha)$, for $0 \le x \le 1$ and $0 \le \alpha \le V_i([x, 1])$, returns a point $y \ge x$ with $V_i([x, y]) = \alpha$.

Because $V_i$ is nonatomic, $t \mapsto V_i([x, t])$ is continuous and nondecreasing, so a cut query always has an answer. The answer can be any point of an interval when the valuation is 0 on a stretch; a common rule returns the least such point. The answers are exact real numbers.

A deterministic protocol is a rule that chooses the next query from the answers so far, or stops. When it stops, it outputs an allocation $X_1, \dots, X_n$, each a finite union of intervals, as a function of the answers. The points that it uses can be answers of cut queries, the points 0 and 1, or any points that it computes from earlier answers. A randomized protocol may also use random bits.

The agents are assumed to answer by a fixed valuation. A protocol "guarantees $1/n$" when every agent that answers by its true valuation gets at least $1/n$, whatever valuations the other agents use for their answers. The classic proportional protocols have this property.

## What it counts

The cost of a run is the number of queries, eval and cut together, summed over all agents. The cost of a protocol is the largest cost over all valuations, for a given $n$. Some results count the two kinds apart, for example $O(n)$ cuts and $O(n^2)$ evals.

The model does not count arithmetic, the size of the numbers, or the time of the agents to answer. A protocol that sorts $n$ cut points makes no queries for the sort. If the valuations are piecewise constant with $k$ pieces, each query can be answered in $O(k)$ time, and the running time of a protocol is at most its query count times $O(k)$, plus its own work.

Moving-knife procedures, in which a knife moves continuously and agents call stop, are not finite protocols in this model. Some of them can be simulated: the [Dubins-Spanier moving knife](/dubins-spanier-moving-knife/) becomes one cut query per waiting agent per round. Others, such as the [Stromquist moving knife](/stromquist-moving-knife/) for envy-free connected pieces, cannot be simulated with any finite number of queries.

## Relation to other models

- **Query model.** It is a query model over an input that is a list of measures instead of a bit string. An eval query is like reading one value of a function, and a cut query is like a search for a value, which a protocol could only approximate with many eval queries.
- **Decision trees.** A deterministic protocol is a [decision tree](/decision-tree-model/) whose nodes are queries and whose branches are the possible answers. Lower bounds are proved, as for decision trees, by an [adversary argument](/adversary-argument/) that answers each query so as to keep the protocol from finishing early.
- **Comparison model.** The [Edmonds-Pruhs lower bound](/edmonds-pruhs-lower-bound/) of $\Omega(n \log n)$ for proportional division plays the same role in this model as the bound of $\Omega(n \log n)$ comparisons does for sorting, and its proof also counts how many answers the protocol must learn.
- **Approximate queries.** In a weaker form, the answers are correct only up to a small error. Edmonds and Pruhs prove their randomized lower bound in this form.
- **Direct revelation.** Each agent reports its whole valuation, for example as a density with $k$ pieces. Then the protocol has full information, and the count of queries is replaced by the size of the input.

## Known results in the model

| goal | agents | upper bound | lower bound |
|---|---|---|---|
| proportional, deterministic | $n$ | $O(n \log n)$ ([Even-Paz](/even-paz-algorithm/)) | $\Omega(n \log n)$ (Edmonds-Pruhs) |
| proportional, connected pieces | $n$ | $O(n \log n)$ (Even-Paz) | $\Omega(n \log n)$ (Woeginger-Sgall) |
| proportional, randomized | $n$ | $O(n)$ expected cuts (Even-Paz) | $\Omega(n \log n)$ with approximate queries |
| envy-free | 2 | 2 ([divide and choose](/divide-and-choose/)) | |
| envy-free | 3 | at most 5 cuts ([Selfridge-Conway](/selfridge-conway-procedure/)) | |
| envy-free | $n$ | $O(n^{n^{n^{n^{n^n}}}})$ ([Aziz-Mackenzie](/aziz-mackenzie-protocol/)) | $\Omega(n^2)$ (Procaccia) |
| envy-free, connected pieces | $n \ge 3$ | no finite protocol | ([Stromquist](/stromquist-impossibility-theorem/)) |

The [last diminisher](/last-diminisher/) uses at most $n^2 - 1$ queries, and the Dubins-Spanier procedure uses $n(n + 1)/2 - 1$ cut queries. Even-Paz uses at most $2n \lceil \lg n \rceil - n$ queries.

Two preprints from 2026 refine the picture for proportional division. Arndt, Moseley, Im and Pruhs (arXiv 2606.07238, June 2026) give a deterministic protocol with $O(n)$ cut queries and $O(n^2)$ eval queries, so the $\Omega(n \log n)$ bound does not hold for cuts alone. Arndt, Pruhs and Tran (arXiv 2605.21829, May 2026) give an $\Omega(n \log n)$ lower bound for randomized protocols that give connected pieces.

## References
