---
tag: 3197Z9
kind: algorithm
slug: aziz-mackenzie-protocol
name: Aziz-Mackenzie protocol
aliases:
- bounded envy-free cake cutting
area: algorithmic-game-theory/fair-division
level: research
summary: "The first envy-free cake cutting protocol for n agents whose number of queries is bounded by a function of n, a tower of exponentials."
solves: [cake-cutting-problem]
model: robertson-webb-query-model
complexity:
  vars: {n: the number of agents}
  time: {worst: O(n^(n^(n^(n^(n^n)))))}
  space: {extra: O(n^(n^(n^(n^(n^n)))))}
properties: {deterministic: true, recursive: true, online: false}
prereqs: [envy-freeness, robertson-webb-query-model, brams-taylor-procedure]
see_also: [selfridge-conway-procedure, stromquist-moving-knife, stromquist-impossibility-theorem, cake-cutting-problem, proportional-division, edmonds-pruhs-lower-bound, chore-division]
sources:
  - paper: "Haris Aziz and Simon Mackenzie, A discrete and bounded envy-free cake cutting protocol for any number of agents, FOCS 2016, pp. 416-427, arXiv:1604.03655"
    locator: the abstract (the bound of a tower of six n, and the partial allocations with n^3 (n^2)^n queries)
  - paper: "Haris Aziz and Simon Mackenzie, A discrete and bounded envy-free cake cutting protocol for four agents, STOC 2016, arXiv:1508.05143"
    locator: the abstract (the first bounded envy-free protocol for four agents)
  - paper: doi:10.2307/2974850
    title: Steven J. Brams and Alan D. Taylor, An envy-free cake division protocol, American Mathematical Monthly 102(1) (1995)
    locator: pp. 9-18 (the finite but unbounded protocol that this one improves)
  - book: isbn:9781107060432
    title: Felix Brandt, Vincent Conitzer, Ulle Endriss, Jerome Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016
    locator: Chapter 13, Ariel D. Procaccia, Cake Cutting Algorithms (pp. 311-330)
---

The Aziz-Mackenzie protocol divides a [cake](/cake-cutting-problem/) among any number $n$ of agents so that no agent [envies](/envy-freeness/) another, with a number of queries in the [Robertson-Webb model](/robertson-webb-query-model/) that is bounded by a function of $n$ alone: at most $n^{n^{n^{n^{n^n}}}}$, a tower of six $n$. It differs from the other envy-free protocols in its bound. The [Brams-Taylor procedure](/brams-taylor-procedure/) also handles any $n$ and always stops, but its number of steps depends on the valuations and has no bound in $n$. The [Selfridge-Conway procedure](/selfridge-conway-procedure/) is bounded but handles only three agents, and the [Stromquist moving knife](/stromquist-moving-knife/) gives connected pieces to three agents but is not a finite protocol. The tower bound makes the protocol a result about what is possible, not a practical method.

## In plain words

Several friends share a cake so that no friend wants another friend's piece. An older method does this, but the number of its steps has no limit set by the number of friends.

This method sets such a limit. It gives out the cake in rounds, as the older method does. In each round, a friend can build a lead over another friend: it thinks its own piece beats the other's piece by more than all the cake that is left. Once a friend has such a lead over everyone else, it no longer cares how the rest is shared, so it can step aside. The others then share the rest by the same method. The rounds are arranged so that leads come after a fixed number of steps. The limit is enormous, but it depends only on how many friends there are.

## The problem

There are $n$ agents and a cake $[0, 1]$. Each agent $i$ has a nonnegative, additive and nonatomic valuation $V_i$ with $V_i([0, 1]) = 1$. The protocol asks Eval and Cut queries and outputs disjoint pieces $X_1, \dots, X_n$, each a finite union of intervals, that cover the cake, with $V_i(X_i) \ge V_i(X_j)$ for all $i$ and $j$. Its cost is the number of queries in the worst case over all valuations, and the goal is a bound that depends only on $n$.

During the protocol, $X_1, \dots, X_n$ are the pieces given out so far and $R$ is the leftover. Agent $i$ **dominates** agent $j$ if $V_i(X_i) - V_i(X_j) \ge V_i(R)$, which is the irrevocable advantage of Brams and Taylor.

## The algorithm

The pseudocode is a simplified outline. It shows how domination lets the protocol finish with fewer agents, not the exact order of the sub-protocols. The sub-protocols, and the counting that bounds them, are in the FOCS 2016 paper.

```pseudo id=main
AZIZ-MACKENZIE(agents N, leftover R)
L1  if |N| = 1 then give R to the agent in N; return
L2  repeat
L3      run the core protocol on R, with each agent of N in turn as cutter     ▷ an envy-free partial allocation
L4      add the parts given out to the pieces; R ← what is left
L5      run the sub-protocols that turn the core rounds into domination
L6  until some agent i in N dominates every other agent in N
L7  AZIZ-MACKENZIE(N minus {i}, R)                                       ▷ i no longer cares about R
```

The core protocol is a bounded sub-protocol that gives out part of the leftover with no envy. The other sub-protocols use the rounds where agents disagree about pieces to create domination. The key property is that each loop of lines L2 to L6 ends after a number of queries bounded by a function of $|N|$, which is the point where the Brams-Taylor procedure has no bound.

The code of this page is a toy, not the protocol of Aziz and Mackenzie, and it has none of their bounds. It works for three agents only. It keeps the recursion of lines L1 to L7, but with three agents a round is the first stage of the Selfridge-Conway procedure, and with two agents a round is divide and choose. These rounds cannot force domination, so the toy caps the number of rounds, and at the cap it divides the leftover with the second stage of the Selfridge-Conway procedure.

## Example

Suppose that after some rounds with four agents, agent 1 values the pieces given out so far and the leftover as follows.

| | $X_1$ | $X_2$ | $X_3$ | $X_4$ | $R$ |
|---|---|---|---|---|---|
| $V_1$ | 0.40 | 0.15 | 0.20 | 0.20 | 0.05 |

For each $j$, $V_1(X_1) - V_1(X_j)$ is at least $0.40 - 0.20 = 0.20 \ge 0.05 = V_1(R)$. So agent 1 dominates the three others. In whatever way agents 2, 3 and 4 later share $R$, each of their pieces stays worth at most $0.20 + 0.05 = 0.25 < 0.40$ to agent 1. The protocol removes agent 1 and continues with three agents on $R$. If $V_1(R)$ were $0.30$, agent 1 would not dominate agent 3, and giving all of $R$ to agent 3 would make agent 1 envious.

## Correctness

**Domination lasts.** Each core round divides a part $P$ of the leftover with no envy, so if $i$ dominates $j$, then $i$ values its part of $P$ at least as much as the part of $j$, and the leftover only shrinks. So $V_i(X_i) - V_i(X_j)$ does not decrease and $V_i(R)$ does not increase.

**No envy at the end, by induction on $|N|$.** Before line L7, the pieces given out have no envy. In line L7, agent $i$ dominates every other agent of $N$, so whatever part of $R$ an agent $j$ gets later, $V_i(X_j) + V_i(R) \le V_i(X_i)$, and $i$ does not envy $j$. The other agents share $R$ envy-free among themselves, by induction, and they do not envy $i$, because $X_i$ does not grow and their own pieces do not shrink. With one agent, line L1 gives it all of $R$ and creates no envy. So the final division is envy-free, and, since it covers the cake, [proportional](/proportional-division/).

**Bounded.** Aziz and Mackenzie prove that the loop in lines L2 to L6 ends after a number of queries bounded in terms of $|N|$, and that the bound for $n$ agents is at most $n^{n^{n^{n^{n^n}}}}$.

## Complexity

The number of Robertson-Webb queries is at most $n^{n^{n^{n^{n^n}}}}$ (Aziz and Mackenzie 2016). The best known lower bound for envy-free cake cutting is $\Omega(n^2)$ queries (Procaccia 2009), so the bounds are very far apart. Closing this gap is an open problem, as of the 2016 sources of this page. The extra space is the list of cuts and pieces, so it has the same bound. The arithmetic between queries is free in the model.

If the protocol is stopped early, it gives a partial allocation that is envy-free and proportional, in which each agent values its piece at least $1/n$ of the whole cake, within $n^3 (n^2)^n$ queries. A variant gives an envy-free partial allocation with connected pieces, each worth at least $1/(3n)$ of the cake to its owner, with the same number of queries.

## Properties

- **Envy-free and proportional**, for every $n$.
- **Bounded.** The number of queries depends only on $n$.
- **Pieces are not connected.** An agent can get many intervals. With connected pieces, no finite protocol exists for $n \ge 3$, by [Stromquist's impossibility theorem](/stromquist-impossibility-theorem/).
- **Deterministic and discrete.** It uses only Eval and Cut queries.
- **Recursive.** It removes one dominating agent at a time and recurses on fewer agents.

## Variants and improvements

- **Four agents.** Aziz and Mackenzie first gave a bounded envy-free protocol for four agents (STOC 2016), and then extended the ideas to any $n$.
- **Partial allocations.** The early-stopping versions above give envy-free partial allocations with much smaller bounds: exponential in $n \log n$ instead of a tower.
- **Chores.** Dehghani, Farhadi, Hajiaghayi and Yami (2018) gave a bounded envy-free protocol for [chore division](/chore-division/) with any number of agents.

## When to use it

Use it as the reference result that envy-free cake cutting has bounded query complexity. For actual divisions its bound is far too large. For three agents use Selfridge-Conway; for proportional division use a protocol with $O(n \log n)$ queries; and when some envy or some waste is allowed, use an approximate or partial method.

## Pitfalls

- **Bounded is not small.** For $n = 2$ the tower of six $n$ is already $2^{2^{65536}}$. The bound is a worst-case guarantee, not an estimate of a typical run.
- **Domination over everyone.** The recursion may remove agent $i$ only when it dominates every remaining agent; domination over some of them is not enough.
- **Free disposal.** The connected variant above throws part of the cake away. It is not a full envy-free division with connected pieces.

## Implementations

## History

Envy-free cake cutting for three agents was solved by Selfridge and Conway around 1960, and Brams and Taylor gave a finite protocol for any $n$ in 1995, without a bound in $n$. Whether a bounded protocol exists for $n \ge 4$ was a well-known open question. Haris Aziz and Simon Mackenzie answered it for four agents in a paper posted in 2015 and presented at STOC 2016, and for any number of agents at FOCS 2016.

## References
