---
tag: RTDGDA
kind: algorithm
slug: dubins-spanier-moving-knife
name: Dubins-Spanier moving knife
aliases:
- Dubins-Spanier procedure
area: algorithmic-game-theory/fair-division
level: intro
summary: A proportional cake cutting protocol. A knife moves from left to right, and the first agent to value the piece behind it at 1/n calls stop and takes it.
solves: [cake-cutting-problem]
model: robertson-webb-query-model
complexity:
  vars: {n: the number of agents}
  time: {worst: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [proportional-division, robertson-webb-query-model]
see_also: [last-diminisher, even-paz-algorithm, divide-and-choose, stromquist-moving-knife, edmonds-pruhs-lower-bound, envy-freeness]
sources:
  - paper: "Lester E. Dubins and Edwin H. Spanier, How to cut a cake fairly, American Mathematical Monthly 68(1) (1961), 1-17"
    locator: the moving-knife method for n people, and the existence results for fair divisions
  - book: isbn:9780521556446
    title: Steven J. Brams and Alan D. Taylor, Fair Division, From Cake-Cutting to Dispute Resolution, Cambridge University Press, 1996
    locator: Chapter 2, Proportionality for n > 2, the divisible case (from p. 30)
  - book: isbn:9781107060432
    title: Felix Brandt, Vincent Conitzer, Ulle Endriss, Jerome Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016
    locator: Chapter 13, Ariel D. Procaccia, Cake Cutting Algorithms, Section 13.3, classic algorithms (from p. 313)
---

The Dubins-Spanier moving knife is a protocol that gives each of $n$ agents a connected piece of a [cake](/cake-cutting-problem/) worth at least $1/n$ to that agent, so it finds a [proportional division](/proportional-division/). A referee moves a knife slowly from the left end of the cake. The first agent that values the piece to the left of the knife at $1/n$ calls stop, takes that piece and leaves. The knife then starts again from the cut, and the last agent takes what is left. In the [Robertson-Webb query model](/robertson-webb-query-model/), each stop of the knife is found with one cut query per remaining agent, for $n(n+1)/2 - 1$ cut queries in total.

## In plain words

A group of friends shares a long cake. One person holds a knife over the left end and moves it slowly to the right. Each friend watches. As soon as the piece behind the knife looks like a fair share to some friend, that friend calls "stop". The cake is cut there, and the friend takes the piece and leaves.

The other friends did not call stop, so the piece looked small to them. They think enough cake is left for them. The knife starts again at the cut, and the method repeats. When only one friend is left, that friend takes the rest. Each friend can make sure of a fair share alone: it only has to call stop at the right time.

## The problem

The cake is $[0, 1]$. Agent $i \in \{1, \dots, n\}$ has a nonnegative, additive and nonatomic valuation $V_i$ with $V_i([0, 1]) = 1$. The protocol must output disjoint intervals $X_1, \dots, X_n$ that cover $[0, 1]$, with $V_i(X_i) \ge 1/n$ for every $i$. It learns the valuations only by queries. Here it needs only the cut query: $\mathrm{Cut}_i(a, t)$ returns the least point $x \ge a$ with $V_i([a, x]) = t$.

## The algorithm

A continuous knife is not a finite protocol, but this one is easy to simulate. When the knife starts at $a$, agent $i$ would call stop at its mark $m_i = \mathrm{Cut}_i(a, 1/n)$. The knife therefore stops at the least mark. So the protocol asks every remaining agent for its mark and takes the least one.

```pseudo id=main
DUBINS-SPANIER(n)
L1  a ← 0; R ← {1, 2, …, n}
L2  while |R| > 1 do
L3      for each agent i of R do m_i ← CUT_i(a, 1/n)    ▷ where agent i would call stop
L4      h ← the agent of R with the least m_i            ▷ ties go to the smallest index
L5      give [a, m_h] to h; remove h from R; a ← m_h
L6  give [a, 1] to the last agent of R
```

The rule for ties does not change the guarantees. A real knife must also break ties, for example by a fixed order of the agents.

## Example

Split $[0, 1]$ into four equal segments, and let the densities on them be $(1, 1, 1, 1)$ for agent 1, $(0, 1, 1, 2)$ for agent 2, $(2, 2, 0, 0)$ for agent 3 and $(1, 0, 0, 3)$ for agent 4. Each list sums to 4, so each agent values the whole cake at 1. Here $n = 4$ and $1/n = 1/4$.

| round | $a$ | marks of the remaining agents | least mark | piece |
|---|---|---|---|---|
| 1 | 0 | $m_1 = 1/4$, $m_2 = 1/2$, $m_3 = 1/8$, $m_4 = 1/4$ | agent 3 | $[0, 1/8]$ |
| 2 | $1/8$ | $m_1 = 3/8$, $m_2 = 1/2$, $m_4 = 19/24$ | agent 1 | $[1/8, 3/8]$ |
| 3 | $3/8$ | $m_2 = 5/8$, $m_4 = 5/6$ | agent 2 | $[3/8, 5/8]$ |
| | $5/8$ | | agent 4 | $[5/8, 1]$ |

Agents 3, 1 and 2 get exactly $1/4$, and agent 4 gets $3/4$. The run makes $4 + 3 + 2 = 9$ cut queries and no eval queries. The result is proportional but not [envy-free](/envy-freeness/): agent 2 values the piece of agent 4 at $1/8 + 1/2 = 5/8$, and agent 3 values the piece of agent 1 at $1/2$.

## Correctness

**Invariant.** At the start of each round, every agent $i$ in $R$ has $V_i([a, 1]) \ge |R|/n$.

It holds at the start with $a = 0$ and $|R| = n$. In a round, the receiver $h$ has the least mark, so every other agent $j$ of $R$ has $m_h \le m_j$ and $V_j([a, m_h]) \le V_j([a, m_j]) = 1/n$. Hence $V_j([m_h, 1]) \ge |R|/n - 1/n$, which is the invariant for the next round. Each receiver in line L5 gets exactly $1/n$, and the last agent gets at least $1/n$ by the invariant with $|R| = 1$. The cut queries have answers because each agent in $R$ values $[a, 1]$ at least $1/n$. The full proof is in proofs/correctness.md.

## Complexity

The round with $r$ remaining agents makes $r$ cut queries, for $r = n, n - 1, \dots, 2$. So the protocol makes exactly $\sum_{r=2}^{n} r = n(n+1)/2 - 1$ cut queries and no eval queries, which is $\Theta(n^2)$ on every input. Finding the least mark takes $O(r)$ comparisons, which the query model does not count. Extra space is $O(n)$ for the marks.

## Properties

- **Connected pieces.** Each agent gets one interval, and the cake is cut at $n - 1$ points.
- **Safe for an honest agent.** An agent that calls stop at its true $1/n$ point, and not before, gets at least $1/n$, whatever the others do. If it calls stop too early it gets less than $1/n$; if it waits too long, another agent may take a piece that it values at more than $1/n$.
- **Envy only toward later pieces.** An agent that gets a piece in a round valued every earlier piece at most $1/n$, and gets exactly $1/n$. So it does not envy the agents that left before it. It may envy agents that leave later, as in the example.
- **Cut queries only.** The protocol never asks an eval query. This makes it simple to run with marks on paper: each agent draws one mark per round.
- **Same output as the last diminisher in many cases.** On the three-agent example of the [last diminisher](/last-diminisher/) page, both protocols give the same pieces. They can differ when the last diminisher order makes a different agent the last to trim.

## Variants and improvements

- **Last diminisher.** The [last diminisher](/last-diminisher/) of Banach and Knaster passes the piece from agent to agent and lets each one trim it. It mixes eval and cut queries and uses at most $n^2 - 1$ queries.
- **Even-Paz.** The [Even-Paz algorithm](/even-paz-algorithm/) also asks each agent for one mark per step, but it cuts at the median mark and recurses on two halves of the agents. It needs $O(n \log n)$ queries, which is optimal by the [Edmonds-Pruhs lower bound](/edmonds-pruhs-lower-bound/).
- **Envy-free moving knives.** The [Stromquist moving knife](/stromquist-moving-knife/) uses four knives at once to give three agents an envy-free division with connected pieces. Unlike the Dubins-Spanier knife, it cannot be simulated with finitely many queries.
- **Two agents.** For $n = 2$, the first stop gives one agent a piece worth $1/2$, and the other agent, which did not stop, values that piece at most $1/2$. This is a moving-knife form of [divide and choose](/divide-and-choose/).

## When to use it

Use the Dubins-Spanier procedure when you want a proportional division with connected pieces and a simple rule: each agent gives one mark per round, and the least mark wins. It suits a small group and a physical cake or a time line, where marks are easy to draw. For many agents, use the Even-Paz algorithm, which needs $O(n \log n)$ marks instead of $\Theta(n^2)$.

## Pitfalls

- **Keeping old marks.** A mark is a $1/n$ point from the current left end $a$. After a round, $a$ moves, so every remaining agent must make a new mark. An old mark is worth less than $1/n$ from the new $a$.
- **The largest mark.** The piece goes to the least mark. If it went to the largest mark, the other agents could value it at more than $1/n$, and the invariant would break.
- **Cut queries that are not the least point.** If the valuation is 0 on a stretch, a cut query has many answers. Any answer keeps the guarantee, but the tie rule and the output can change. The implementation returns the least point.
- **Not envy-free.** For $n \ge 3$ the result can leave agents with envy.

## Implementations

## History

Dubins and Spanier (1961) described the moving knife in "How to cut a cake fairly", in the American Mathematical Monthly. The same paper proves the existence of divisions with stronger properties, such as divisions in which each agent values each piece at exactly $1/n$. The protocol gives the same guarantee as the earlier last diminisher of Banach and Knaster, which Steinhaus published in 1948. In the Robertson-Webb model, its $\Theta(n^2)$ cut queries were later improved to $O(n \log n)$ by Even and Paz (1984).

## References
