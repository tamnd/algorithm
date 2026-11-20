---
tag: EWY1RW
kind: algorithm
slug: divide-and-choose
name: Divide and choose
aliases:
- I cut you choose
area: algorithmic-game-theory/fair-division
level: intro
summary: One agent cuts the cake into two pieces it values equally, and the other takes the piece it prefers. The result is envy-free.
solves: [cake-cutting-problem]
model: robertson-webb-query-model
complexity:
  vars: {n: the number of agents}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [cake-cutting-problem, proportional-division, envy-freeness]
see_also: [last-diminisher, even-paz-algorithm, selfridge-conway-procedure, adjusted-winner, robertson-webb-query-model, cut-and-choose]
sources:
  - book: isbn:9780521556446
    title: Steven J. Brams and Alan D. Taylor, Fair Division, From Cake-Cutting to Dispute Resolution, Cambridge University Press, 1996
    locator: Chapter 1, Proportionality for n = 2 (divide-and-choose, its properties, and moving-knife versions for two people)
  - book: isbn:9781568810768
    title: Jack Robertson and William Webb, Cake-Cutting Algorithms, Be Fair If You Can, A K Peters, 1998
    locator: Chapter 1, Fairly Dividing a Cake
  - book: isbn:9781107060432
    title: Felix Brandt, Vincent Conitzer, Ulle Endriss, Jerome Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016
    locator: Chapter 13, Ariel D. Procaccia, Cake Cutting Algorithms, Section 13.3 (classic cake cutting algorithms)
  - paper: "Hugo Steinhaus, The problem of fair division, Econometrica 16(1) (1948), 101-104"
    locator: the two-person method that the paper extends to n people
---

Divide and choose is the protocol that splits a [cake](/cake-cutting-problem/) between two agents: one agent cuts the cake into two pieces that it values equally, and the other agent takes the piece it prefers. Each agent gets at least half of the cake by its own measure, so the division is [proportional](/proportional-division/), and neither agent prefers the other piece, so it is [envy-free](/envy-freeness/). In the [Robertson-Webb query model](/robertson-webb-query-model/) it uses one cut query and one eval query. The cryptographic [cut-and-choose](/cut-and-choose/) technique (one party makes many copies of an object and the other opens all but one to check them) takes its name from this protocol, but it is a method of verification, not a method of division.

## In plain words

Two children share a cake with chocolate on one side and fruit on the other. They like the parts in different ways. The first child cuts the cake into two pieces. The first child does not know which piece it will get, so it cuts where both pieces look equally good to it. The second child then takes the piece that it likes more.

The first child gets exactly half by its own view, whichever piece is left. The second child gets at least half by its own view, because it chose the better of two pieces. Neither child wants to swap. Each child can make sure of this result by itself: the cutter by cutting honestly, the chooser by choosing honestly. Neither child needs to trust the other.

## The problem

The cake is the interval $[0, 1]$. Agent $i \in \{1, 2\}$ has a valuation $V_i$: a nonnegative, additive and nonatomic measure on $[0, 1]$ with $V_i([0, 1]) = 1$. Nonatomic means that a single point has value 0, so it does not matter which piece holds a cut point. The output is a partition of $[0, 1]$ into pieces $X_1$ and $X_2$, here two intervals.

The goal is a [proportional division](/proportional-division/), $V_i(X_i) \ge 1/2$ for $i = 1, 2$, and [envy-freeness](/envy-freeness/), $V_i(X_i) \ge V_i(X_j)$. With two agents and $X_1 \cup X_2 = [0, 1]$, the two goals are the same: $V_i(X_i) + V_i(X_j) = 1$, so $V_i(X_i) \ge V_i(X_j)$ holds exactly when $V_i(X_i) \ge 1/2$.

The protocol does not see $V_1$ and $V_2$. It asks queries: $\mathrm{Cut}_i(a, t)$ returns a point $x \ge a$ with $V_i([a, x]) = t$, and $\mathrm{Eval}_i(a, b)$ returns $V_i([a, b])$.

## The algorithm

Agent 1 is the cutter and agent 2 is the chooser.

```pseudo id=main
DIVIDE-AND-CHOOSE()                          ▷ agent 1 cuts, agent 2 chooses
L1  x ← CUT_1(0, 1/2)                         ▷ now V_1([0, x]) = 1/2
L2  if EVAL_2(0, x) ≥ 1/2 then
L3      return X_1 = [x, 1], X_2 = [0, x]     ▷ the chooser takes the left piece
L4  else return X_1 = [0, x], X_2 = [x, 1]    ▷ the chooser takes the right piece
```

Line L1 is the cut. Line L2 asks the chooser for the value of the left piece. Because $V_2([0, x]) + V_2([x, 1]) = 1$, the test $V_2([0, x]) \ge 1/2$ is the same as $V_2([0, x]) \ge V_2([x, 1])$, so the chooser takes the piece it values more. On a tie it takes the left piece; any fixed rule for ties gives the same guarantees.

## Example

Split the cake into four equal segments $[0, 1/4], [1/4, 1/2], [1/2, 3/4], [3/4, 1]$. The cutter has densities $(3, 1, 0, 0)$ on them, so it values the four segments at $3/4, 1/4, 0, 0$. The chooser has the uniform density $(1, 1, 1, 1)$.

| step | query | answer |
|---|---|---|
| L1 | $\mathrm{Cut}_1(0, 1/2)$ | $x = 1/6$, because $3 \cdot 1/6 = 1/2$ |
| L2 | $\mathrm{Eval}_2(0, 1/6)$ | $1/6$, less than $1/2$ |
| L4 | | $X_1 = [0, 1/6]$, $X_2 = [1/6, 1]$ |

The cutter gets $V_1([0, 1/6]) = 1/2$. The chooser gets $V_2([1/6, 1]) = 5/6$. Both pieces meet the guarantee, but the chooser does much better than half. This is typical: the cutter gets exactly $1/2$ when it cuts honestly, and the chooser gets $\max(V_2([0, x]), V_2([x, 1])) \ge 1/2$.

## Correctness

**Claim.** If agent 1 cuts as in line L1 and agent 2 chooses as in line L2, then $V_1(X_1) = 1/2$ and $V_2(X_2) \ge 1/2$. So the division is proportional and envy-free.

Line L1 gives $V_1([0, x]) = 1/2$, and additivity gives $V_1([x, 1]) = 1 - 1/2 = 1/2$, so agent 1 gets $1/2$ in both branches. In line L3, $V_2(X_2) = V_2([0, x]) \ge 1/2$. In line L4, $V_2([0, x]) < 1/2$, so $V_2(X_2) = V_2([x, 1]) = 1 - V_2([0, x]) > 1/2$. Envy-freeness follows from the equivalence of the two goals for two agents. The cut query always has an answer: $t \mapsto V_1([0, t])$ is continuous (the measure is nonatomic) and goes from 0 to 1, so it takes the value $1/2$. The full proof is in proofs/correctness.md.

## Complexity

The protocol makes exactly one cut query (line L1) and one eval query (line L2), so it uses $\Theta(1)$ queries in the Robertson-Webb model in every case. Each agent answers one question. If the valuations are piecewise constant on $k$ segments, as in the implementation, each query takes $O(k)$ arithmetic operations on rationals.

## Properties

- **Each agent is safe alone.** The cutter gets $1/2$ if it cuts at its own half point, whatever the chooser does. The chooser gets at least $1/2$ if it takes the piece it prefers, whatever the cut is. So the guarantee needs no assumption about the other agent.
- **Connected pieces.** Each agent gets one interval, with one cut.
- **Not equitable.** In the example the cutter gets $1/2$ and the chooser gets $5/6$. The chooser has the advantage, because the cutter commits first.
- **Not Pareto optimal.** Let the cutter be uniform and let the chooser have density $(0, 2, 2, 0)$. The cutter cuts at $1/2$, and the chooser values both halves at $1/2$, so each agent gets $1/2$. The division $X_2 = [1/4, 3/4]$ and $X_1 = [0, 1/4] \cup [3/4, 1]$ gives the cutter $1/2$ and the chooser $1$. See [Pareto optimality](/pareto-optimality/).
- **Not strategyproof for the cutter.** A cutter that knows the chooser's measure can gain by a cut that is not at its half point. In the example, a cut at $x = 0.49$ makes the uniform chooser take $[0.49, 1]$, and the cutter gets $V_1([0, 0.49]) = 3/4 + 0.24 = 0.99$. Honest cutting is still the safe choice when the cutter does not know the chooser's measure.

## Variants and improvements

- **More agents, proportional.** The [last diminisher](/last-diminisher/) and the [Dubins-Spanier moving knife](/dubins-spanier-moving-knife/) use $\Theta(n^2)$ queries for $n$ agents. The [Even-Paz algorithm](/even-paz-algorithm/) uses $O(n \log n)$ queries, which is optimal by the [Edmonds-Pruhs lower bound](/edmonds-pruhs-lower-bound/).
- **More agents, envy-free.** For three agents, the [Selfridge-Conway procedure](/selfridge-conway-procedure/) gives an envy-free division with at most five cuts. For any number of agents there are the [Brams-Taylor procedure](/brams-taylor-procedure/) and the bounded [Aziz-Mackenzie protocol](/aziz-mackenzie-protocol/).
- **Moving knives for two agents.** Austin's moving-knife procedure gives each of two agents a piece that both value at exactly $1/2$. It needs continuous moves, so it is not a finite protocol in the Robertson-Webb model.
- **Goods and points.** For two agents who split several divisible goods by points, the [adjusted winner procedure](/adjusted-winner/) is envy-free, equitable and Pareto optimal.

## When to use it

Use divide and choose for two agents when you want a simple rule that each agent can check by itself. It needs only one cut and one comparison. If the agents also want equal satisfaction or an efficient result, use the adjusted winner procedure on a list of goods, or an exact two-person moving knife if continuous moves are possible. For more than two agents, use one of the $n$-agent protocols above; divide and choose alone does not extend.

## Pitfalls

- **Cutting at the wrong value.** Line L1 must cut at value $1/2$ for the cutter. A cut at the midpoint $x = 1/2$ of the interval gives the cutter $V_1([x, 1])$, which can be 0 (in the example, $V_1([1/2, 1]) = 0$).
- **Comparing with the wrong total.** The test of line L2 compares $V_2([0, x])$ with $1/2$ only because $V_2([0, 1]) = 1$. With unnormalized valuations, compare $V_2([0, x])$ with $V_2([x, 1])$ instead.
- **Two cut points.** A cut query can have many answers when the density is 0 on a stretch. Any answer gives the cutter $1/2$; the implementation returns the least one. Do not assume the answer is unique.
- **Envy-free for two is not envy-free for more.** Running divide and choose repeatedly on pieces among three agents does not give envy-freeness; that needs a procedure such as Selfridge-Conway.

## Implementations

## History

The method is old, and it appears in many stories of two people who share land or an inheritance. Steinhaus (1948) took the two-person method as known and asked how to extend it to $n$ people, which led to the [last diminisher](/last-diminisher/) of Banach and Knaster. Brams and Taylor (1996) study it and its moving-knife versions in their first chapter.

## References
