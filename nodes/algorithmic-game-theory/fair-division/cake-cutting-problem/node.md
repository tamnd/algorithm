---
tag: PKXVNC
kind: problem
slug: cake-cutting-problem
name: Cake cutting problem
aliases:
- fair cake cutting
area: algorithmic-game-theory/fair-division
level: intro
summary: Divide a divisible resource, modeled as the interval [0, 1], among n agents with different value measures, so that each agent finds its piece fair.
model: robertson-webb-query-model
complexity:
  vars: {n: the number of agents}
  time: {worst: Θ(n log n)}
see_also: [divide-and-choose, even-paz-algorithm, edmonds-pruhs-lower-bound, selfridge-conway-procedure, stromquist-impossibility-theorem, aziz-mackenzie-protocol, chore-division, indivisible-goods-allocation]
sources:
  - book: isbn:9780521556446
    title: Steven J. Brams and Alan D. Taylor, Fair Division, From Cake-Cutting to Dispute Resolution, Cambridge University Press, 1996
    locator: Chapters 1 and 2 (proportional procedures for two and for n agents), Chapters 6 and 7 (envy-free procedures)
  - book: isbn:9781568810768
    title: Jack Robertson and William Webb, Cake-Cutting Algorithms, Be Fair If You Can, A K Peters, 1998
    locator: Chapter 1, Fairly Dividing a Cake; Chapter 8, Impossibility Theorems; Chapter 10, Exact and Envy-Free Algorithms
  - book: isbn:9781107060432
    title: Felix Brandt, Vincent Conitzer, Ulle Endriss, Jerome Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016
    locator: Chapter 13, Ariel D. Procaccia, Cake Cutting Algorithms, pp. 311-330 (Section 13.3, classic algorithms, from p. 313; Section 13.4, complexity of cake cutting, from p. 316)
  - paper: "Hugo Steinhaus, The problem of fair division, Econometrica 16(1) (1948), 101-104"
    locator: the first statement of the problem for n people
---

The cake cutting problem asks how to divide one divisible resource among $n$ agents who value its parts differently, so that each agent thinks its piece is fair. The resource is modeled as the interval $[0, 1]$, and each agent has its own measure of value on it. The two main fairness goals are [proportional division](/proportional-division/), in which each agent gets at least $1/n$ by its own measure, and [envy-freeness](/envy-freeness/), in which no agent prefers the piece of another agent. Protocols are compared by the number of queries they ask in the [Robertson-Webb query model](/robertson-webb-query-model/). For proportional division the answer is known: $\Theta(n \log n)$ queries.

## In plain words

Some friends share a cake with many toppings. Each friend likes different toppings, so the same piece can look large to one friend and small to another. Each friend knows only what it likes. The problem is to find a rule that cuts the cake and gives the pieces out, so that each friend thinks it was treated fairly.

Fair can mean different things. A weak meaning is that each friend gets at least its share of the whole, as it sees it. A strong meaning is that no friend wants to swap its piece with the piece of another friend. The rule cannot look inside the heads of the friends. It can only ask them questions, so a good rule asks few questions.

## Definition

The cake is the interval $[0, 1]$. There are $n$ agents. Agent $i$ has a valuation $V_i$ that assigns a value to each finite union of intervals. It has these properties.

- **Nonnegative.** $V_i(X) \ge 0$ for every piece $X$.
- **Additive.** $V_i(X \cup Y) = V_i(X) + V_i(Y)$ when $X$ and $Y$ are disjoint.
- **Nonatomic.** $V_i([x, x]) = 0$ for every point $x$. So it does not matter which piece holds a cut point, and $V_i([a, t])$ changes continuously with $t$.
- **Normalized.** $V_i([0, 1]) = 1$.

Often $V_i$ is given by a density $v_i$, so that $V_i(X) = \int_X v_i$. An allocation is a list of pieces $X_1, \dots, X_n$, each a finite union of intervals, that are disjoint (up to the end points) and cover $[0, 1]$. Agent $i$ gets $X_i$. The allocation is

- **proportional** if $V_i(X_i) \ge 1/n$ for every $i$;
- **envy-free** if $V_i(X_i) \ge V_i(X_j)$ for every $i$ and $j$;
- **equitable** if $V_1(X_1) = V_2(X_2) = \dots = V_n(X_n)$.

A problem instance also says whether each $X_i$ must be one interval (connected pieces) or may be a finite union of intervals. A protocol does not know the valuations. It asks queries of the agents. In the Robertson-Webb model there are two kinds: $\mathrm{Eval}_i(x, y)$ returns $V_i([x, y])$, and $\mathrm{Cut}_i(x, t)$ returns a point $y$ with $V_i([x, y]) = t$. The cost of a protocol is the number of queries in the worst case. Arithmetic and the choice of the next query are free.

## Variants

- **Proportional division.** Each agent gets at least $1/n$. Finite protocols with connected pieces exist for every $n$.
- **Envy-free division.** No agent envies another. With $n$ agents, an envy-free allocation that covers the whole cake is also proportional, since $n V_i(X_i) \ge \sum_j V_i(X_j) = 1$. Envy-free allocations with connected pieces always exist, but no finite protocol finds them for $n \ge 3$ (see [Stromquist's impossibility theorem](/stromquist-impossibility-theorem/)).
- **Equitable and exact division.** Each agent gets the same value by its own measure, or each agent values each piece at exactly $1/n$. A [consensus halving](/consensus-halving/) is the exact case with two pieces. These divisions exist, but no finite protocol in the Robertson-Webb model finds an exact one.
- **Efficiency.** A [Pareto optimal](/pareto-optimality/) allocation leaves no other allocation that is at least as good for every agent and better for one.
- **Unequal entitlements.** Agent $i$ has a weight $w_i$ and should get at least $w_i$.
- **Chores.** The resource is bad, and each agent wants a piece of small cost. See [chore division](/chore-division/).
- **Indivisible goods.** The resource is a set of items that cannot be cut. Proportional and envy-free allocations need not exist then, so weaker goals are used. See [indivisible goods allocation](/indivisible-goods-allocation/).
- **Strategic agents.** A protocol is strategyproof if no agent gains by false answers. Most classic protocols only guarantee that an honest agent gets its fair share, whatever the others do.

## Examples

**Two agents.** Agent 1 values the cake uniformly. Agent 2 values only $[1/2, 1]$, with density 2 there. The allocation $X_1 = [0, 1/2]$ and $X_2 = [1/2, 1]$ gives agent 1 the value $1/2$ and agent 2 the value $1$. It is proportional and envy-free. The allocation $X_1 = [1/2, 1]$ and $X_2 = [0, 1/2]$ gives agent 2 the value 0, so it is neither.

**Proportional but not envy-free.** Split $[0, 1]$ into four equal segments, and let three agents have the densities $(1, 1, 1, 1)$, $(2, 1, 1, 0)$ and $(3, 1, 0, 0)$, scaled to total value 1. The [last diminisher](/last-diminisher/) gives agent 3 the piece $[0, 1/9]$, agent 2 the piece $[1/9, 11/36]$ and agent 1 the piece $[11/36, 1]$. The values are $25/36$, $1/3$ and $1/3$, so the allocation is proportional. But agent 3 values the piece of agent 2 at $17/36 > 1/3$, so agent 3 envies agent 2.

**The same piece, different values.** For agent 1 above, $[0, 1/4]$ is worth $1/4$; for agent 3 it is worth $3/4$. This difference is what makes fair division possible: when the agents disagree, each agent can get more than $1/n$ by its own measure.

## Known algorithms

| protocol | agents | goal | pieces | queries |
|---|---|---|---|---|
| [divide and choose](/divide-and-choose/) | 2 | envy-free | connected | 2 |
| [last diminisher](/last-diminisher/) | $n$ | proportional | connected | $O(n^2)$ |
| [Dubins-Spanier moving knife](/dubins-spanier-moving-knife/) | $n$ | proportional | connected | $O(n^2)$ |
| [Even-Paz](/even-paz-algorithm/) | $n$ | proportional | connected | $O(n \log n)$ |
| [Selfridge-Conway](/selfridge-conway-procedure/) | 3 | envy-free | unions | at most 5 cuts |
| [Brams-Taylor](/brams-taylor-procedure/) | $n$ | envy-free | unions | finite, not bounded |
| [Aziz-Mackenzie](/aziz-mackenzie-protocol/) | $n$ | envy-free | unions | bounded, a tower of six $n$ |

The [Stromquist moving knife](/stromquist-moving-knife/) gives an envy-free division with connected pieces for three agents, but it uses continuous knives, so it is not a finite protocol in the Robertson-Webb model. For two agents who share several goods by points, the [adjusted winner procedure](/adjusted-winner/) is envy-free, equitable and Pareto optimal.

## Bounds

- **Proportional, upper bound.** Even-Paz uses at most $2n \lceil \lg n \rceil - n$ queries, so $O(n \log n)$.
- **Proportional, lower bound.** Every deterministic proportional protocol needs $\Omega(n \log n)$ queries, even with pieces that are unions of intervals. This is the [Edmonds-Pruhs lower bound](/edmonds-pruhs-lower-bound/). Woeginger and Sgall had proved it before for connected pieces. So $\Theta(n \log n)$ is the deterministic query complexity of proportional cake cutting.
- **Proportional, randomized.** Even and Paz gave a randomized protocol with $O(n)$ expected cuts. Edmonds and Pruhs proved $\Omega(n \log n)$ for randomized protocols when the queries return approximate answers.
- **Envy-free, lower bound.** Procaccia (2009) proved that every envy-free protocol needs $\Omega(n^2)$ queries.
- **Envy-free, upper bound.** Aziz and Mackenzie (2016) gave the first bounded protocol for every $n$, with $O(n^{n^{n^{n^{n^n}}}})$ queries. The gap between the bounds is open.
- **Envy-free with connected pieces.** For $n \ge 3$ no finite protocol exists (Stromquist 2008).

## Reductions

- **Envy-free to proportional.** Any envy-free allocation of the whole cake is proportional, so a protocol for envy-freeness also gives a proportional division. For $n = 2$ the two goals are the same.
- **Proportional to search.** Each of the $n/2$ agents in the Edmonds-Pruhs proof must find a piece that is thin and rich for it. This turns the lower bound into a search problem with an adversary, as in the [comparison sort lower bound](/comparison-sort-lower-bound/).
- **Envy-free to fixed points.** The existence of envy-free allocations with connected pieces follows from [Sperner's lemma](/sperner-lemma/), by the method that Su also uses for [rental harmony](/rental-harmony/).
- **Exact division to necklace splitting.** The [necklace splitting theorem](/necklace-splitting-theorem/) is the discrete form of an exact division with few cuts.

## Applications

- Division of land, an inheritance or the assets in a divorce. The adjusted winner procedure was designed for such cases.
- Division of time, such as shifts or the use of a shared machine, when the agents prefer different times of the day.
- Division of rent and rooms in a shared house (rental harmony).
- Allocation of a shared resource among users in computer systems, where the fairness goals of cake cutting are compared with goals such as [proportional fairness](/proportional-fairness/).

## References
