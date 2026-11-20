---
tag: PK1D3M
kind: algorithm
slug: stromquist-moving-knife
name: Stromquist moving knife
aliases:
- Stromquist procedure
area: algorithmic-game-theory/fair-division
level: advanced
summary: "An envy-free division among three agents into connected pieces with four moving knives, one held by a referee."
solves: [cake-cutting-problem]
model: real-ram
complexity:
  vars: {k: the number of segments of a piecewise-constant valuation}
  time: {worst: O(k log k)}
  space: {extra: O(k)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [envy-freeness, dubins-spanier-moving-knife, selfridge-conway-procedure]
see_also: [stromquist-impossibility-theorem, brams-taylor-procedure, aziz-mackenzie-protocol, su-rental-harmony-algorithm, robertson-webb-query-model, cake-cutting-problem]
sources:
  - paper: doi:10.2307/2320951
    title: Walter Stromquist, How to cut a cake fairly, American Mathematical Monthly 87(8) (1980)
    locator: pp. 640-644 (the moving-knife procedure for three players, and the existence of envy-free divisions into intervals)
  - book: isbn:9780521556446
    title: Steven J. Brams and Alan D. Taylor, Fair Division, From Cake-Cutting to Dispute Resolution, Cambridge University Press, 1996
    locator: the moving-knife procedures for three persons
  - paper: doi:10.37236/735
    title: Walter Stromquist, Envy-free cake divisions cannot be found by finite protocols, Electronic Journal of Combinatorics 15 (2008)
    locator: R11, Sections 1 and 3 (why the moving knife cannot be made finite)
  - paper: "Julius B. Barbanel and Steven J. Brams, Cake division with minimal cuts: envy-free procedures for 3 persons, 4 persons, and beyond, Mathematical Social Sciences 48 (2004), 251-269"
    locator: a simpler moving-knife procedure for three persons with two cuts
---

The Stromquist moving knife is a procedure that divides a [cake](/cake-cutting-problem/) among three agents into three intervals so that no agent [envies](/envy-freeness/) another. A referee moves a sword over the cake, each agent moves a knife that halves the rest of the cake in its own eyes, and the cake is cut at the sword and at the middle knife when an agent shouts. It differs from the other envy-free protocols for three or more agents: the [Selfridge-Conway procedure](/selfridge-conway-procedure/) is finite but can give two intervals to an agent, while this procedure gives connected pieces but needs four knives that move continuously. By [Stromquist's impossibility theorem](/stromquist-impossibility-theorem/), no finite protocol in the [Robertson-Webb query model](/robertson-webb-query-model/) can do what this procedure does. The [Brams-Taylor procedure](/brams-taylor-procedure/) and the [Aziz-Mackenzie protocol](/aziz-mackenzie-protocol/) handle any number of agents, with pieces that are not connected.

## In plain words

A referee slowly moves a sword from the left end of a long cake to the right, splitting off a left part. Each of three friends holds a knife over the rest of the cake, at the place where the two sides of the knife look equal to that friend. The middle knife marks a second cut.

So there are always three pieces: left, middle and right. As soon as some friend thinks the left part is at least as good as each other part, that friend shouts "cut". The cake is cut at the sword and at the middle knife. The friend who shouted takes the left part. Each other friend takes the part that holds its own knife. To that friend, this part is the better of the two right parts and is at least as good as the left part, or it would have shouted first.

## The problem

The cake is $[0, 1]$. Agents 1, 2 and 3 have nonnegative, additive and nonatomic valuations $V_i$ with $V_i([0, 1]) = 1$. The procedure must output three intervals that cover the cake and meet only at end points, one for each agent, with $V_i(X_i) \ge V_i(X_j)$ for all $i$ and $j$. Here we also assume that every interval of positive length has positive value to every agent, so that each knife position is unique and moves continuously. Without this assumption the halving point can jump, and the argument below fails.

## The algorithm

For a sword position $x$, agent $i$ holds its knife at $k_i(x)$, the point of $[x, 1]$ with $V_i([x, k_i]) = V_i([k_i, 1])$. The median knife is $y(x) = \mathrm{med}(k_1(x), k_2(x), k_3(x))$.

```pseudo id=main
STROMQUIST-KNIFE(agents 1, 2, 3)
L1  the referee puts the sword at x = 0
L2  move x continuously to the right, and at each moment:
L3      each agent i holds its knife at k_i(x)                    ▷ halves [x, 1] in its eyes
L4      y ← the median of k_1(x), k_2(x), k_3(x)
L5      agent i shouts if V_i([0, x]) ≥ V_i([x, y]) and V_i([0, x]) ≥ V_i([y, 1])
L6  stop at the first shout; s ← the agent that shouts            ▷ ties go to the smallest index
L7  cut at x and at y; give [0, x] to s
L8  of the two other agents, the one whose knife is further left gets [x, y]
L9  the other one gets [y, 1]
```

The procedure is a thought experiment with continuous motion. For valuations with positive piecewise-constant densities on $k$ equal segments, the implementation simulates it exactly: every knife position and the median are piecewise affine in $x$, with $O(k)$ break points, so the first shout is found by solving linear equations between break points.

## Example

Take four equal segments. Agent 1 is uniform, agent 2 has densities proportional to $(2, 2, 1, 1)$, and agent 3 to $(1, 1, 1, 3)$. The first shout comes at $x = 2/7$. There the knives are at $k_1 = 9/14$, $k_2 = 15/28$ and $k_3 = 67/84$, so the median is $y = 9/14$, the knife of agent 1.

Agent 2 values $[0, 2/7]$ at $8/21$, $[2/7, 9/14]$ at $8/21$ and $[9/14, 1]$ at $5/21$. So agent 2 shouts at the moment its left part ties with its best right part, and it gets $[0, 2/7]$. Agent 1's knife ($9/14$) is left of agent 3's knife ($67/84$), so agent 1 gets $[2/7, 9/14]$ and agent 3 gets $[9/14, 1]$. Row $i$ gives $V_i$ of each agent's piece:

| | $X_1 = [2/7, 9/14]$ | $X_2 = [0, 2/7]$ | $X_3 = [9/14, 1]$ |
|---|---|---|---|
| $V_1$ | **5/14** | 2/7 | 5/14 |
| $V_2$ | 8/21 | **8/21** | 5/21 |
| $V_3$ | 5/21 | 4/21 | **4/7** |

Each row has its largest entry on the diagonal, so the division is envy-free. Agent 1 holds the median knife, so it values the two right parts equally at $5/14$.

## Correctness

The knife positions and the median knife move continuously, because each $V_i$ is continuous and strictly increasing on $[0, 1]$. Let $h_i(x)$ be the value of the left part to agent $i$ minus the larger of the values of the two right parts. At $x = 0$, $h_i$ is at most $-1/2$; at $x = 1$, it is $1$. So there is a first moment $x^* > 0$ when some $h_i$ reaches 0, and at that moment no $h_i$ is positive, because each $h_i$ was negative just before.

The shouter has $h_s(x^*) \ge 0$, so it values the left part at least as much as each right part. The two other agents have $h_i(x^*) \le 0$, so each values its better right part at least as much as the left part. The agent whose knife is left of or at the median values $[x^*, y]$ at least half of $[x^*, 1]$, so $[x^*, y]$ is its better right part; the other agent is the mirror case. So every agent gets a piece it values most. The full proof, and the proof that the simulation is exact, are in `proofs/correctness.md`.

## Complexity

The procedure uses two cuts, the fewest possible for three connected pieces. It is not a finite protocol: the agents watch values change continuously, and no finite number of Robertson-Webb queries replaces this in general, by Stromquist's 2008 theorem.

The simulation for piecewise-constant valuations with $k$ segments costs $O(k \log k)$ arithmetic operations on rationals, in the [real-RAM](/real-ram/) sense. It builds the prefix sums of each valuation in $O(k)$, finds $O(k)$ break points ($k + 1$ segment ends, at most $k - 1$ points per knife where it crosses a segment end, and at most three knife crossings between two of these), sorts them, and does $O(\log k)$ work per break point to invert a valuation. The rationals can grow in size, so the bit cost is larger.

## Properties

- **Envy-free and connected.** Each agent gets one interval, and envy-freeness implies proportionality.
- **Two cuts.** The sword and the middle knife are the only cuts.
- **Each agent can protect itself.** An agent that keeps its knife at its own halving point and shouts at the right moment gets a piece it does not envy, as long as the other knives move continuously. The proof above uses, for one agent, only its own knife and the rule for the median.
- **Not Pareto optimal in general.** It finds one envy-free division, not a best one.
- **Ties.** If two agents would shout at the same moment, either one can take the left part; both pieces left are still fine for the other.

## Variants and improvements

- **A simpler procedure.** Barbanel and Brams gave a moving-knife procedure for three agents that also uses two cuts and is simpler to run.
- **More agents.** There is no natural extension to four or more agents with connected pieces. For $n$ agents, envy-free divisions into intervals still exist (Stromquist 1980), and [Su's algorithm](/su-rental-harmony-algorithm/) uses Sperner's lemma to find approximate ones.
- **Finite protocols.** If pieces need not be connected, the [Selfridge-Conway procedure](/selfridge-conway-procedure/) is finite for three agents.

## When to use it

Use the Stromquist moving knife when three agents must get one interval each with no envy, and the agents can watch a continuous process, or when the valuations are known well enough to simulate it, as for piecewise-constant densities. When only queries are available, use the Selfridge-Conway procedure and accept pieces of two intervals, or find an approximately envy-free division of intervals.

## Pitfalls

- **A knife that jumps.** If an agent values some interval at 0, its halving point is not unique and can jump. Then the median can jump, and the first moment of a shout may not have the equality that the proof needs. Use positive densities, or fix a continuous choice of the halving point.
- **The middle knife, not a fixed agent's knife.** The second cut is at the median of the three knives, and which agent holds it can change as the sword moves.
- **The wrong right piece.** Each non-shouter gets the piece that contains its own knife. Giving the middle part to a fixed agent breaks envy-freeness.
- **Treating it as finite.** A discrete search for the shout point with finitely many queries in the Robertson-Webb model can only find an approximate answer in general.

## Implementations

## History

Walter Stromquist published the procedure in 1980 in the American Mathematical Monthly, in the same paper that proves that envy-free divisions into intervals exist for any number of agents. In 2008 Stromquist proved that no finite protocol finds envy-free divisions into intervals for three or more agents.

## References
