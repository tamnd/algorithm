---
tag: VJGVJA
kind: algorithm
slug: last-diminisher
name: Last diminisher
aliases:
- Banach-Knaster procedure
area: algorithmic-game-theory/fair-division
level: intro
summary: A proportional cake cutting protocol for n agents. A piece passes from agent to agent, each may trim it to value 1/n, and the last agent to trim it takes it.
solves: [cake-cutting-problem]
model: robertson-webb-query-model
complexity:
  vars: {n: the number of agents}
  time: {best: Θ(n^2), worst: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [proportional-division, robertson-webb-query-model]
see_also: [divide-and-choose, dubins-spanier-moving-knife, even-paz-algorithm, edmonds-pruhs-lower-bound, envy-freeness, cake-cutting-problem]
sources:
  - paper: "Hugo Steinhaus, The problem of fair division, Econometrica 16(1) (1948), 101-104"
    locator: the method for n people that Steinhaus credits to Banach and Knaster
  - book: isbn:9780521556446
    title: Steven J. Brams and Alan D. Taylor, Fair Division, From Cake-Cutting to Dispute Resolution, Cambridge University Press, 1996
    locator: Chapter 2, Proportionality for n > 2, the divisible case (from p. 30)
  - book: isbn:9781568810768
    title: Jack Robertson and William Webb, Cake-Cutting Algorithms, Be Fair If You Can, A K Peters, 1998
    locator: Chapter 1, Fairly Dividing a Cake
  - book: isbn:9781107060432
    title: Felix Brandt, Vincent Conitzer, Ulle Endriss, Jerome Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016
    locator: Chapter 13, Ariel D. Procaccia, Cake Cutting Algorithms, Section 13.3, classic algorithms (from p. 313)
---

The last diminisher is a protocol that gives each of $n$ agents a connected piece of a [cake](/cake-cutting-problem/) worth at least $1/n$ to that agent, so it finds a [proportional division](/proportional-division/). In each round, one agent marks a piece worth $1/n$ to it, and the piece passes to the other remaining agents in turn. An agent that values the piece at more than $1/n$ trims it to $1/n$ by its own measure. The last agent to trim the piece takes it and leaves, and the others continue with the rest of the cake. In the [Robertson-Webb query model](/robertson-webb-query-model/) it uses at most $n^2 - 1$ queries.

## In plain words

A group of friends shares a cake. The first friend cuts a slice from the left end that it thinks is a fair share. The slice then goes around the group. Each friend looks at the slice. If the slice looks too large, the friend makes it smaller, so that it looks exactly fair to that friend. If the slice looks fair or small, the friend lets it pass.

When every friend has seen the slice, the last friend who made it smaller takes it. If nobody made it smaller, the friend who cut it takes it. That friend leaves the group with a fair share. The others think the slice was not too large, so they think enough cake is left for them. They repeat the method on the rest, until one friend remains and takes what is left.

## The problem

The cake is $[0, 1]$. Agent $i \in \{1, \dots, n\}$ has a nonnegative, additive and nonatomic valuation $V_i$ with $V_i([0, 1]) = 1$. The protocol must output disjoint intervals $X_1, \dots, X_n$ that cover $[0, 1]$, with $V_i(X_i) \ge 1/n$ for every $i$. It learns the valuations only by queries: $\mathrm{Cut}_i(a, t)$ returns a point $x \ge a$ with $V_i([a, x]) = t$, and $\mathrm{Eval}_i(a, b)$ returns $V_i([a, b])$.

## The algorithm

The remaining cake is always $[a, 1]$, and $R$ is the list of agents that do not have a piece yet, in a fixed order.

```pseudo id=main
LAST-DIMINISHER(n)
L1  a ← 0; R ← (1, 2, …, n)
L2  while |R| > 1 do
L3      h ← the first agent of R; x ← CUT_h(a, 1/n)        ▷ h marks [a, x]
L4      for each agent j of R after h, in order do
L5          if EVAL_j(a, x) > 1/n then                      ▷ j thinks [a, x] is too large
L6              x ← CUT_j(a, 1/n); h ← j                    ▷ j trims it and becomes the holder
L7      give [a, x] to h; remove h from R; a ← x
L8  give [a, 1] to the last agent of R
```

Each trim moves $x$ to the left, because the agent that trims values $[a, x]$ at more than $1/n$ and its new mark has value exactly $1/n$. So the piece of a round is never larger than the first mark, and the holder always values $[a, x]$ at exactly $1/n$.

## Example

Split $[0, 1]$ into four equal segments, and let the densities on them be $(1, 1, 1, 1)$ for agent 1, $(2, 1, 1, 0)$ for agent 2 and $(3, 1, 0, 0)$ for agent 3, Each segment has width $1/4$ and each list sums to 4, so each agent values the whole cake at 1. For example, agent 2 values the first segment at $2/4 = 1/2$. Here $n = 3$ and $1/n = 1/3$.

| round | step | query | answer | holder |
|---|---|---|---|---|
| 1 | L3 | $\mathrm{Cut}_1(0, 1/3)$ | $x = 1/3$ | 1 |
| 1 | L5 | $\mathrm{Eval}_2(0, 1/3)$ | $7/12 > 1/3$ | |
| 1 | L6 | $\mathrm{Cut}_2(0, 1/3)$ | $x = 1/6$ | 2 |
| 1 | L5 | $\mathrm{Eval}_3(0, 1/6)$ | $1/2 > 1/3$ | |
| 1 | L6 | $\mathrm{Cut}_3(0, 1/3)$ | $x = 1/9$ | 3 |
| 2 | L3 | $\mathrm{Cut}_1(1/9, 1/3)$ | $x = 4/9$ | 1 |
| 2 | L5 | $\mathrm{Eval}_2(1/9, 4/9)$ | $17/36 > 1/3$ | |
| 2 | L6 | $\mathrm{Cut}_2(1/9, 1/3)$ | $x = 11/36$ | 2 |

Agent 3 gets $[0, 1/9]$, agent 2 gets $[1/9, 11/36]$, and agent 1 gets $[11/36, 1]$. The values for their owners are $1/3$, $1/3$ and $25/36$. The run makes 8 queries, which is $n^2 - 1$: every agent trims in every round. The result is proportional but not [envy-free](/envy-freeness/): agent 3 values the piece of agent 2 at $17/36$, and agent 2 values the piece of agent 1 at $4/9$.

## Correctness

**Invariant.** At the start of each round, every agent $i$ in $R$ has $V_i([a, 1]) \ge |R|/n$.

At the start, $a = 0$ and $|R| = n$, so the invariant holds. In a round, the final holder $h$ values $[a, x]$ at exactly $1/n$, because $x$ is its own cut. Every other agent $j$ in $R$ values $[a, x]$ at most $1/n$. For an agent after the last trim, line L5 said so. For an agent before the last trim, it valued an earlier, larger piece at most $1/n$, or trimmed it to $1/n$, and the final piece is a subset of that piece. So $V_j([x, 1]) = V_j([a, 1]) - V_j([a, x]) \ge |R|/n - 1/n$, which is the invariant for the next round with $|R| - 1$ agents.

Every agent that gets a piece in line L7 gets exactly $1/n$. The last agent gets $[a, 1]$, worth at least $1/n$ by the invariant with $|R| = 1$. So the division is proportional. The cut queries have answers because each agent in $R$ values $[a, 1]$ at least $1/n$. The full proof is in proofs/correctness.md.

## Complexity

A round with $r = |R|$ agents makes $r - 1$ eval queries (one per agent after the first) and between 1 and $r$ cut queries. Rounds run for $r = n, n - 1, \dots, 2$. So the protocol makes exactly $\sum_{r=2}^{n} (r - 1) = n(n - 1)/2$ eval queries, between $n - 1$ and $\sum_{r=2}^{n} r = n(n + 1)/2 - 1$ cut queries, and at most $n^2 - 1$ queries in total. Even with no trims it makes $n(n - 1)/2 + n - 1$ queries, so its cost is $\Theta(n^2)$ in every case.

The bound $n^2 - 1$ is reached: if agent $i$ puts more weight to the left than every agent before it in the order (for example, density $2^{i(n - j)}$ on segment $j$ of $n$ equal segments), every agent trims in every round. Extra space is $O(n)$ for the list $R$.

## Properties

- **Connected pieces.** Each agent gets one interval, and the cake is cut at $n - 1$ points in the end.
- **Safe for an honest agent.** The guarantee of $1/n$ for agent $i$ uses only the answers of agent $i$. Whatever the other agents answer, an agent that cuts and trims by its true valuation gets at least $1/n$.
- **Envy only toward later pieces.** An agent $j$ that gets a piece in round $k$ was waiting in every round before $k$, so it values each earlier piece at most $1/n$, and it gets exactly $1/n$ itself. So no agent envies a piece that was given out before its own. It may envy a later piece, as the example shows.
- **Not equitable and not Pareto optimal** in general. In the example the last agent gets $25/36$ and the others $1/3$.
- **Uses eval and cut queries.** Unlike the [Dubins-Spanier moving knife](/dubins-spanier-moving-knife/), it asks waiting agents to evaluate the current piece, and only some of them cut.

## Variants and improvements

- **Dubins-Spanier moving knife.** A knife moves from $a$ to the right, and the first agent to call stop takes the piece. With cut queries, every remaining agent marks its $1/n$ point and the least mark wins. It gives the same kind of allocation with exactly $n(n + 1)/2 - 1$ cut queries and no evals.
- **Even-Paz.** The [Even-Paz algorithm](/even-paz-algorithm/) splits the agents into two halves at a median mark and recurses. It uses $O(n \log n)$ queries, which is optimal by the [Edmonds-Pruhs lower bound](/edmonds-pruhs-lower-bound/).
- **Other classic proportional methods.** Brams and Taylor describe the lone divider and the lone chooser methods next to the last diminisher. They give the same guarantee of $1/n$ by other steps.
- **Two agents.** For $n = 2$ the protocol is a form of [divide and choose](/divide-and-choose/): agent 1 marks its half $[0, x]$, and agent 2 either lets agent 1 take it or trims it to its own half point and takes the trimmed piece.

## When to use it

Use the last diminisher when you want a simple proportional protocol with connected pieces that people can run by hand, one piece at a time. It is easy to explain and each agent can check its own guarantee. For many agents, the Even-Paz algorithm needs far fewer queries. If envy matters, use an envy-free procedure such as [Selfridge-Conway](/selfridge-conway-procedure/) for three agents.

## Pitfalls

- **Giving the piece to the first trimmer.** The piece goes to the last agent that trims it, after all agents of $R$ have seen it. If it goes to an agent before the others have seen it, a later agent may value it at more than $1/n$, and then that agent can be left with less than its share of the rest.
- **Trimming from the wrong end.** The trim must keep the left end $a$ and move the right end $x$. If it moves $a$, the remaining cake is no longer one interval.
- **Ties.** With the strict test of line L5, an agent that values the piece at exactly $1/n$ lets it pass. A test with $\ge$ also keeps the guarantees, but it adds cut queries and changes who gets the piece.
- **Not envy-free.** A proportional result can still leave agents with envy. Do not report it as envy-free for $n \ge 3$.

## Implementations

## History

Steinhaus (1948) described the problem of fair division for $n$ people and gave this method, which he credited to his colleagues Stefan Banach and Bronislaw Knaster. It is the first protocol for proportional division for every $n$. Brams and Taylor (1996) treat it as a classic method for $n > 2$, and the counts of queries in the Robertson-Webb model were studied later, with the $O(n \log n)$ method of Even and Paz (1984) and the matching lower bound of Edmonds and Pruhs (2006).

## References
