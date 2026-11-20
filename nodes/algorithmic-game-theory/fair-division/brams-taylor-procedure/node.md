---
tag: MN3VTM
kind: algorithm
slug: brams-taylor-procedure
name: Brams-Taylor procedure
aliases:
- Brams-Taylor envy-free protocol
area: algorithmic-game-theory/fair-division
level: advanced
summary: "The first finite envy-free cake cutting protocol for any number of agents, but its number of steps has no bound in n alone."
solves: [cake-cutting-problem]
model: robertson-webb-query-model
complexity:
  vars: {n: the number of agents}
  time: {worst: ∞}
  space: {extra: ∞}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [envy-freeness, robertson-webb-query-model, selfridge-conway-procedure]
see_also: [aziz-mackenzie-protocol, stromquist-moving-knife, stromquist-impossibility-theorem, cake-cutting-problem, proportional-division, chore-division, edmonds-pruhs-lower-bound, su-rental-harmony-algorithm]
sources:
  - paper: doi:10.2307/2974850
    title: Steven J. Brams and Alan D. Taylor, An envy-free cake division protocol, American Mathematical Monthly 102(1) (1995)
    locator: pp. 9-18 (the protocol for n agents, and irrevocable advantage)
  - book: isbn:9780521556446
    title: Steven J. Brams and Alan D. Taylor, Fair Division, From Cake-Cutting to Dispute Resolution, Cambridge University Press, 1996
    locator: the envy-free procedure for n persons
  - paper: "Haris Aziz and Simon Mackenzie, A discrete and bounded envy-free cake cutting protocol for any number of agents, FOCS 2016, pp. 416-427"
    locator: the introduction (the Brams-Taylor protocol is finite but unbounded)
  - book: isbn:9781107060432
    title: Felix Brandt, Vincent Conitzer, Ulle Endriss, Jerome Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016
    locator: Chapter 13, Ariel D. Procaccia, Cake Cutting Algorithms (pp. 311-330)
---

The Brams-Taylor procedure is a finite protocol that divides a [cake](/cake-cutting-problem/) among any number $n$ of agents so that no agent [envies](/envy-freeness/) another. It was the first such protocol for $n \ge 4$. It divides the cake part by part, and keeps dividing the leftover until each agent has an *irrevocable advantage* over each other agent, so that the last leftover can go to anyone. Its difference from the other envy-free protocols is its cost: it always stops, but the number of steps depends on the valuations and has no bound in terms of $n$ alone. The [Selfridge-Conway procedure](/selfridge-conway-procedure/) handles only three agents, with at most five cuts; the [Stromquist moving knife](/stromquist-moving-knife/) gives connected pieces to three agents with continuous knives; and the [Aziz-Mackenzie protocol](/aziz-mackenzie-protocol/) handles $n$ agents with a bound that depends only on $n$.

## In plain words

Several friends share a cake. The method gives out most of the cake fairly in one round, but a few crumbs are left over. It gives out most of the crumbs fairly in the next round, and so on.

The key idea is a lead that cannot be lost. Suppose one friend thinks its own piece is better than a second friend's piece by more than all the crumbs that are left. Then that friend will never envy the second friend, even if the second friend gets every crumb later. The method keeps going until every friend has such a lead over every other friend. Then it hands the last crumbs to anyone and stops.

The method always ends, but how many rounds it needs depends on how the friends value the cake, and it can be very large.

## The problem

There are $n$ agents and a cake $[0, 1]$. Each agent $i$ has a nonnegative, additive and nonatomic valuation $V_i$ with $V_i([0, 1]) = 1$. The protocol asks queries in the [Robertson-Webb model](/robertson-webb-query-model/) and must output disjoint pieces $X_1, \dots, X_n$, each a finite union of intervals, that cover the cake, with $V_i(X_i) \ge V_i(X_j)$ for all $i$ and $j$.

Let $X_1, \dots, X_n$ be the pieces given out so far and $R$ the leftover. Agent $i$ has an **irrevocable advantage** over agent $j$ if
$$V_i(X_i) - V_i(X_j) \ge V_i(R).$$
Then $i$ does not envy $j$, even if $j$ later gets all of $R$.

## The algorithm

The page gives the structure of the protocol. The details of the sub-protocols are in the paper of Brams and Taylor and in their book.

```pseudo id=main
BRAMS-TAYLOR(agents 1, …, n)
L1  R ← [0, 1]; X_i ← ∅ for every agent i
L2  for each ordered pair (i, j) of different agents:
L3      while i has no irrevocable advantage over j with respect to R:
L4          divide a part P of R among all n agents with no envy,     ▷ a trimming round
L5              so that i gets more of P than j does, in the eyes of i
L6          add each agent's part of P to its piece X
L7          R ← R minus P
L8  give R to any agent
L9  return X_1, …, X_n
```

A trimming round generalizes the first stage of the Selfridge-Conway procedure. One agent cuts the leftover into pieces that are equal to it, the other agents trim pieces to create ties, and the agents choose in an order that makes the division of the untrimmed parts envy-free. The trimmings form the new leftover. To make a lead of agent $i$ over a chosen agent $j$, Brams and Taylor use the fact that, if $i$ and $j$ value some part of the leftover differently, the cake can be cut so that $i$ gets a part it values more than the part of $j$.

The code of this page is a toy, not the protocol for $n$ agents. It works for three agents only. It keeps the loop over ordered pairs, but each round is the first stage of the Selfridge-Conway procedure with $i$ as the cutter, which gives $i$ an irrevocable advantage over whichever agent takes the trimmed piece, not over a chosen $j$. So the toy caps the number of rounds, and at the cap it divides the leftover with the second stage of the Selfridge-Conway procedure.

## Example

The first stage of the Selfridge-Conway procedure shows how a round makes an irrevocable advantage. Three agents, Alice, Bob and Charlie, have these values for four parts of the cake: $A'$ and $Y$, which together form a piece $A$, and two pieces $B$ and $C$.

| | $A'$ | $Y$ | $B$ | $C$ |
|---|---|---|---|---|
| Alice | 1/4 | 1/12 | 1/3 | 1/3 |
| Bob | 3/10 | 1/5 | 3/10 | 1/5 |
| Charlie | 2/5 | 0 | 3/10 | 3/10 |

Alice cut the cake into $A$, $B$ and $C$, each worth $1/3$ to her. Bob liked $A$ best, at $1/2$, and trimmed it to $A'$, worth $3/10$ to him, the same as his second best piece $B$. The trimming $Y$ is the leftover. Charlie chooses first and takes $A'$. Bob takes $B$, and Alice takes $C$. No one envies another on $A'$, $B$ and $C$.

Alice values her piece $C$ at $1/3$ and the piece $A'$ of Charlie at $1/4$. The difference is $1/12$, which is her value for $Y$. So Alice has an irrevocable advantage over Charlie: even if Charlie gets all of $Y$, his piece is $A$, which is worth $1/3$ to her. Alice has no such advantage over Bob, whose piece $B$ she values at $1/3$. The rest of the protocol must still deal with $Y$ and the other pairs.

## Correctness

**Advantages last.** Suppose $i$ has an irrevocable advantage over $j$ with respect to $R$. A round divides a part $P$ of $R$ with no envy, so $i$ values its own part of $P$ at least as much as the part of $j$. After the round, $V_i(X_i) - V_i(X_j)$ does not decrease, and the new leftover $R \setminus P$ has value at most $V_i(R)$ to $i$. So the advantage remains.

**No envy at the end.** Each round divides its part with no envy, so after the loop there is no envy on the pieces given out. When the loop ends, every agent has an irrevocable advantage over every other agent. Line L8 gives $R$ to some agent $k$. For each $i \ne k$, $V_i(X_i) \ge V_i(X_k) + V_i(R)$, which is the value of the new piece of $k$ to $i$. No other piece changes. So the final division is envy-free, and, as it covers the whole cake, also [proportional](/proportional-division/).

**Finite.** Brams and Taylor prove that each while loop ends after finitely many rounds, for every choice of the valuations. This is the part that depends on the valuations, so it gives no bound in terms of $n$.

## Complexity

The number of queries is finite for every input, but there is no function $f$ such that the protocol uses at most $f(n)$ queries for all valuations. The number of rounds in line L3 depends on the valuations, through how much agent $i$ gains over agent $j$ in each round compared with the value of the leftover. The extra space is the list of pieces, which grows with the number of cuts, so it has no bound in $n$ either. This unboundedness is a theorem about this protocol, stated by Brams and Taylor and by Aziz and Mackenzie; it says nothing about other protocols.

## Properties

- **Envy-free and proportional**, for any number of agents.
- **Finite but unbounded.** It ends on every input, after a number of steps that is not bounded by a function of $n$.
- **Pieces are not connected.** Each agent can get many intervals. By [Stromquist's impossibility theorem](/stromquist-impossibility-theorem/), no finite protocol can guarantee connected envy-free pieces for $n \ge 3$.
- **Discrete.** It uses only cuts and evaluations, with no moving knives.

## Variants and improvements

- **Bounded protocols.** Aziz and Mackenzie gave a bounded envy-free protocol for four agents in 2016, and then the [Aziz-Mackenzie protocol](/aziz-mackenzie-protocol/) for any $n$, with a bound that is a tower of exponentials in $n$.
- **Three agents.** For $n = 3$, the Selfridge-Conway procedure is a bounded special case of the same ideas: one trimming round, then a division of the leftover in which the agent with the irrevocable advantage chooses last.
- **Chores.** A bounded envy-free protocol for [chores](/chore-division/) with any number of agents was given later by Dehghani, Farhadi, Hajiaghayi and Yami (2018).

## When to use it

Use the Brams-Taylor procedure as a proof that envy-free divisions can be found by a finite protocol for any $n$, or for teaching the idea of irrevocable advantage. For computing, it is impractical: no bound in $n$ holds. For three agents use Selfridge-Conway. For more agents, a protocol with a bound, or an approximately envy-free method, is the better choice.

## Pitfalls

- **Finite is not bounded.** Each run stops, but for a fixed $n$ there are valuations that make it run longer than any given number of steps.
- **Advantage over whom.** An irrevocable advantage of $i$ over $j$ says nothing about $i$ and a third agent $k$. The protocol needs it for every ordered pair.
- **Giving out the leftover too early.** Giving $R$ to an agent $k$ before every other agent has an advantage over $k$ can create envy.

## Implementations

## History

Steven Brams and Alan Taylor published the protocol in the American Mathematical Monthly in January 1995, and described it again in their 1996 book. Envy-free cake cutting for $n \ge 4$ agents had been an open problem since the Selfridge-Conway procedure for three agents around 1960. The question of a bounded protocol stayed open until Aziz and Mackenzie solved it in 2016.

## References
