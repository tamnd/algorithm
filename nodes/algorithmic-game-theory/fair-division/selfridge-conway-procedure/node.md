---
tag: 9GXB9K
kind: algorithm
slug: selfridge-conway-procedure
name: Selfridge-Conway procedure
aliases:
- Selfridge-Conway discrete procedure
area: algorithmic-game-theory/fair-division
level: core
summary: A finite protocol that gives an envy-free division of a cake among three agents with at most five cuts. Each agent gets at most two intervals.
solves: [cake-cutting-problem]
model: robertson-webb-query-model
complexity:
  vars: {n: the number of agents (here 3)}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [divide-and-choose, envy-freeness, robertson-webb-query-model]
see_also: [stromquist-moving-knife, brams-taylor-procedure, aziz-mackenzie-protocol, stromquist-impossibility-theorem, dubins-spanier-moving-knife, chore-division, proportional-division]
sources:
  - book: isbn:9780521556446
    title: Steven J. Brams and Alan D. Taylor, Fair Division, From Cake-Cutting to Dispute Resolution, Cambridge University Press, 1996
    locator: the Selfridge-Conway procedure and its history, pp. 116-120
  - book: isbn:9781568810768
    title: Jack Robertson and William Webb, Cake-Cutting Algorithms, Be Fair If You Can, A K Peters, 1998
    locator: the envy-free procedure for three players, pp. 13-14
  - paper: doi:10.2307/2974850
    title: Steven J. Brams and Alan D. Taylor, An envy-free cake division protocol, American Mathematical Monthly 102(1) (1995)
    locator: pp. 9-18 (the extension of the trimming idea to any number of agents)
  - book: isbn:9781107060432
    title: Felix Brandt, Vincent Conitzer, Ulle Endriss, Jerome Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016
    locator: Chapter 13, Ariel D. Procaccia, Cake Cutting Algorithms (pp. 311-330)
---

The Selfridge-Conway procedure is a finite protocol that divides a [cake](/cake-cutting-problem/) among three agents so that the division is [envy-free](/envy-freeness/): no agent values another agent's piece more than its own. It uses at most five cuts, and each agent gets at most two intervals. It differs from the three other envy-free protocols of this area as follows: the [Stromquist moving knife](/stromquist-moving-knife/) gives connected pieces to three agents but needs continuously moving knives, the [Brams-Taylor procedure](/brams-taylor-procedure/) works for any number of agents but has no bound on its steps, and the [Aziz-Mackenzie protocol](/aziz-mackenzie-protocol/) works for any number of agents with a bound that is a tower of exponentials. In the [Robertson-Webb query model](/robertson-webb-query-model/), the procedure makes at most 5 cut queries and 12 eval queries.

## In plain words

Three friends share a cake. The first friend cuts it into three pieces that look equal to her. The second friend looks at the pieces. If two pieces tie for best in her eyes, nothing changes. If one piece looks bigger than all others, she trims a thin slice from it until it ties with her second best piece. The slice is put aside for now.

The third friend chooses first, then the second friend, then the first friend. The second friend must take the trimmed piece if it is still there. So the first friend always gets an untrimmed piece.

Now the slice is shared. The friend who did not get the trimmed piece cuts the slice into three equal parts in her eyes. The friend with the trimmed piece chooses first, then the first friend, then the cutter of the slice.

## The problem

The cake is $[0, 1]$. Agents 1, 2 and 3 have nonnegative, additive and nonatomic valuations $V_1, V_2, V_3$ with $V_i([0, 1]) = 1$. The protocol must output pieces $X_1, X_2, X_3$, each a finite union of intervals, that are disjoint and cover the cake, with $V_i(X_i) \ge V_i(X_j)$ for all $i$ and $j$. Pieces need not be connected. An envy-free division is also [proportional](/proportional-division/), because $3 V_i(X_i) \ge V_i(X_1) + V_i(X_2) + V_i(X_3) = 1$. The protocol learns the valuations only by the queries $\mathrm{Eval}_i(a, b) = V_i([a, b])$ and $\mathrm{Cut}_i(a, t)$, the least $x \ge a$ with $V_i([a, x]) = t$.

## The algorithm

Agent 1 is the cutter, agent 2 the trimmer and agent 3 the first chooser. "Takes the piece it values most" means one eval query per piece that is left; ties go to the leftmost piece.

```pseudo id=main
SELFRIDGE-CONWAY(agents 1, 2, 3)
L1  c ← CUT_1(0, 1/3); d ← CUT_1(c, 1/3); the pieces are [0, c], [c, d], [d, 1]
L2  P ← the piece agent 2 values most; Q ← the piece agent 2 values second    ▷ three evals
L3  if V_2(P) > V_2(Q) then
L4      [a, b] ← P; x ← CUT_2(a, V_2(Q)); P ← [a, x]; L ← [x, b]               ▷ trim P, set L aside
L5  else L ← nothing                                                         ▷ no trim needed
L6  agent 3 takes the piece it values most
L7  if P is still there then agent 2 takes P else agent 2 takes its better piece of the two left
L8  agent 1 takes the last piece
L9  if L is nothing then return
L10 T ← the agent of {2, 3} that holds P; U ← the other one
L11 U cuts L into three parts that U values at V_U(L)/3 each                  ▷ one eval, two cuts
L12 T takes the part it values most, then agent 1 takes its better part, U takes the last
```

Stage one is lines L1 to L8 and divides the cake minus the trimmings $L$. Stage two is lines L10 to L12 and divides $L$. Agent 2 needs no query in line L7, because it knows its values from line L2.

## Example

Take six equal segments of $[0, 1]$ with piecewise-constant densities. Agent 1 is uniform. Agent 2 has densities proportional to $(3, 1, 1, 1, 2, 4)$, and agent 3 to $(1, 2, 3, 3, 2, 1)$.

| step | what happens | values |
|---|---|---|
| L1 | agent 1 cuts at $1/3$ and $2/3$ | $A = [0, 1/3]$, $B = [1/3, 2/3]$, $C = [2/3, 1]$ |
| L2 | agent 2 values $A, B, C$ | $1/3$, $1/6$, $1/2$, so $P = C$ and $Q = A$ |
| L4 | agent 2 trims $C$ to value $1/3$ | $P = [2/3, 11/12]$, $L = [11/12, 1]$ |
| L6 | agent 3 values $A, B, P$ | $1/4$, $1/2$, $5/24$, so it takes $B$ |
| L7 | $P$ is still there | agent 2 takes $P$ |
| L8 | the last piece | agent 1 takes $A$ |
| L10 | $T$ = agent 2, $U$ = agent 3 | |
| L11 | agent 3 values $L$ at $1/24$ and cuts at $17/18$ and $35/36$ | three parts of value $1/72$ to agent 3 |
| L12 | agent 2 takes $[11/12, 17/18]$, agent 1 takes $[17/18, 35/36]$ | agent 3 gets $[35/36, 1]$ |

The final values, with row $i$ giving $V_i$ of each agent's piece:

| | $X_1$ | $X_2$ | $X_3$ |
|---|---|---|---|
| $V_1$ | **13/36** | 5/18 | 13/36 |
| $V_2$ | 7/18 | **7/18** | 2/9 |
| $V_3$ | 19/72 | 2/9 | **37/72** |

Each row has its largest entry on the diagonal, so the division is envy-free. Agent 1 ties with agent 3, and agent 2 ties with agent 1. The run made 5 cut queries and 12 eval queries. With agent 2 as $(1, 1, 2, 2, 3, 3)$ and agent 3 as $(1, 1, 1, 2, 4, 3)$ instead, agent 3 takes the trimmed piece $[2/3, 8/9]$, agent 2 takes $[1/3, 2/3]$, and then agent 2 cuts the trimmings.

## Correctness

The proof checks each agent against each other agent, stage by stage, and adds the two stages by additivity.
- **Agents 2 and 3 in stage one.** Agent 3 chooses first. Agent 2 values the trimmed piece equal to its second best piece and at least as much as the third piece, so whichever piece it gets in line L7 is a best piece for it.
- **Agent 1 in stage one.** Agent 2 or agent 3 holds the trimmed piece, so agent 1 gets an untrimmed piece of value $1/3$, which is at least the value of any stage one piece to agent 1.
- **Stage two.** $T$ chooses first, so it envies nobody's part. $U$ made three equal parts, so it envies nobody's part. Agent 1 chooses before $U$. Against $T$, agent 1 uses a stronger fact: the trimmed piece and all of $L$ together are worth exactly $1/3$ to agent 1, because they make up one of agent 1's equal pieces. So $T$'s whole piece is worth at most $1/3$ to agent 1, which is what agent 1 already has from stage one.

The full proof, with the existence of each cut and the query count, is in `proofs/correctness.md`.

## Complexity

The number of agents is fixed at three, so the cost is a constant.
- At most 5 cut queries: two in line L1, one in line L4 and two in line L11. Without a trim, only 2.
- At most 12 eval queries: three each in lines L2 and L6, one in line L11, and three plus two in line L12.
- The time outside the queries is $\Theta(1)$, and the output has at most six intervals.

## Properties

- **Envy-free and proportional.** Envy-freeness implies proportionality for additive valuations.
- **Not connected.** Agents 2 and 3 can each get two intervals, and so can agent 1. With connected pieces, no finite protocol in the Robertson-Webb model can be envy-free for three agents, by [Stromquist's impossibility theorem](/stromquist-impossibility-theorem/).
- **Safe for an honest agent.** Each agent that answers by its own valuation gets an envy-free share, whatever the other agents do. The proof for agent $i$ uses only agent $i$'s own answers and the order of choices.
- **Not equitable and not Pareto optimal in general.** In the example, the agents get $13/36$, $7/18$ and $37/72$.

## Variants and improvements

- **More agents.** Brams and Taylor found the first finite envy-free protocol for every number of agents, with no bound on its steps. Aziz and Mackenzie gave a bounded protocol for four agents and then for any number of agents.
- **Connected pieces.** The [Stromquist moving knife](/stromquist-moving-knife/) gives each of three agents one interval, at the price of continuous knives.
- **Chores.** For a burden that each agent wants to minimize, the roles of choosing change; see [chore division](/chore-division/).
- **Proportional only.** If proportionality is enough, [divide and choose](/divide-and-choose/) style protocols such as the [Dubins-Spanier moving knife](/dubins-spanier-moving-knife/) need fewer queries per agent and give connected pieces.

## When to use it

Use the Selfridge-Conway procedure when exactly three agents must share a divisible good without envy, and each agent accepts a piece made of two intervals. It is short enough to run by hand. For connected pieces, use a moving-knife method; for more agents, the known envy-free protocols are much larger.

## Pitfalls

- **Letting agent 2 skip the trimmed piece.** If agent 3 leaves the trimmed piece and agent 2 may choose freely, agent 1 can be left with it. Agent 1 values it at less than $1/3$ and then envies.
- **The wrong cutter in stage two.** The agent without the trimmed piece cuts the trimmings, and the holder of the trimmed piece chooses first. If the holder cut, the other agent would choose before agent 1, and agent 1 could envy it, because agent 1's extra margin holds only against the holder of the trimmed piece.
- **Agent 1 choosing last in stage two.** Agent 1 must choose before $U$; agent 1 has no margin against $U$ from stage one.
- **Stopping after stage one.** Stage one alone leaves the trimmings unassigned. The partial division is envy-free, but it is not a division of the whole cake.
- **Trimming on a tie.** When agent 2's two best pieces tie, there is nothing to trim. A trim of zero value gives empty trimmings and the same result with one more query.

## Implementations

## History

John Selfridge found the procedure around 1960 and told it to Richard Guy, who passed it on. John Horton Conway found it independently later. Neither of them published it, and Brams and Taylor describe it in their 1996 book. It was the first finite envy-free procedure for three agents. Brams and Taylor extended the trimming idea to any number of agents in 1995, and Aziz and Mackenzie gave the first bounded protocol for any number of agents in 2016.

## References
