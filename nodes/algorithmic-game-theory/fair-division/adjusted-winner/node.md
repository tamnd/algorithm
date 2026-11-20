---
tag: 8XAEP1
kind: algorithm
slug: adjusted-winner
name: Adjusted winner procedure
aliases:
- Brams-Taylor adjusted winner
area: algorithmic-game-theory/fair-division
level: core
summary: Two agents spread 100 points over divisible goods. Each good goes to the higher bidder, then goods move by point ratio until both have equal points.
model: real-ram
complexity:
  vars: {m: the number of goods}
  time: {worst: Θ(m log m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [envy-freeness, pareto-optimality]
see_also: [divide-and-choose, proportional-division, indivisible-goods-allocation, fractional-knapsack, maximum-nash-welfare, envy-freeness-up-to-one-good, cake-cutting-problem]
sources:
  - book: isbn:9780521556446
    title: Steven J. Brams and Alan D. Taylor, Fair Division, From Cake-Cutting to Dispute Resolution, Cambridge University Press, 1996
    locator: Chapter 4, Envy-freeness and equitability for n = 2 (the point-allocation procedures and adjusted winner), and Chapter 5, Applications of the point-allocation procedures
---

The adjusted winner procedure divides a set of divisible goods between two agents. Each agent spreads 100 points over the goods to show how much it values them. Each good first goes to the agent that gives it more points. Then the agent with more points, the winner, gives goods to the other agent, in the order of the ratio of their points, until both agents have the same number of points; at most one good is split. The result is [envy-free](/envy-freeness/), equitable (both agents get the same number of points) and [Pareto optimal](/pareto-optimality/), if the agents report their true points. Brams and Taylor designed it for disputes such as divorce settlements.

## In plain words

Two people must share some things, such as a house, a car and savings. Each person gets 100 points and puts them on the things, more points on the things that matter more to that person. First each thing goes to the person who put more points on it.

Usually one person now has more points. That person must give something back. It gives first the thing where its own points are closest to the points of the other person, because that costs it the least for the most help to the other. It gives things until the points are equal, and it may give only a part of the last thing. In the end both have the same points, neither prefers the share of the other, and no other division is better for both.

## The problem

There are $m$ divisible goods and two agents, $A$ and $B$. Agent $A$ gives good $g$ the points $p_A(g) \ge 0$, with $\sum_g p_A(g) = 100$, and likewise $p_B$. Valuations are additive and linear in shares: if $A$ gets the share $s_g \in [0, 1]$ of each good $g$ and $B$ gets $1 - s_g$, then
$$U_A = \sum_g p_A(g)\, s_g, \qquad U_B = \sum_g p_B(g)\, (1 - s_g).$$
The goal is a share vector $s$ that is equitable ($U_A = U_B$), envy-free ($U_A \ge 100 - U_A$ and $U_B \ge 100 - U_B$, since the share of the other agent is worth the rest of the 100 points), and Pareto optimal (no other $s'$ gives both agents at least as much and one agent more), with as few split goods as possible.

## The algorithm

```pseudo id=main
ADJUSTED-WINNER(p_A, p_B)                   ▷ points on m goods, each list sums to 100
L1  for each good g: give g to A if p_A(g) ≥ p_B(g), else to B
L2  T_A, T_B ← the points of A and of B for their own goods
L3  if T_A = T_B then return the shares
L4  W ← the agent with more points; L ← the other agent
L5  G ← the goods of W with p_W(g) > 0, sorted by p_W(g)/p_L(g) increasing (p_L(g) = 0 counts as ∞)
L6  for each good g of G, in order do
L7      if T_W − p_W(g) ≥ T_L + p_L(g) then move all of g to L
L8      else move the share α = (T_W − T_L)/(p_W(g) + p_L(g)) of g to L    ▷ now T_W = T_L; stop
L9  return the shares
```

Line L1 gives ties to $A$; any fixed rule works. Each good of $W$ has $p_W(g) \ge p_L(g)$, so every ratio in line L5 is at least 1. Moving a good with a small ratio costs $W$ few points for each point that $L$ gains. Line L7 moves a whole good when $W$ still has at least as many points after the move, and updates $T_W$ and $T_L$. Line L8 solves $T_W - \alpha p_W(g) = T_L + \alpha p_L(g)$ for $\alpha$.

## Example

Two agents split a house, a pension, a car and a boat.

| good | $p_A$ | $p_B$ | after L1 | ratio $p_A/p_B$ |
|---|---|---|---|---|
| house | 50 | 40 | A | 1.25 |
| pension | 20 | 30 | B | |
| car | 15 | 10 | A | 1.5 |
| boat | 15 | 20 | B | |

After line L1, $T_A = 50 + 15 = 65$ and $T_B = 30 + 20 = 50$, so $W = A$. The goods of $A$ in the order of line L5 are the house (1.25) and the car (1.5). For the house, $65 - 50 = 15 < 50 + 40 = 90$, so line L8 moves the share
$$\alpha = \frac{65 - 50}{50 + 40} = \frac{1}{6}$$
of the house to $B$. Agent $A$ keeps $5/6$ of the house and the car, with $50 \cdot 5/6 + 15 = 170/3 \approx 56.67$ points. Agent $B$ gets $1/6$ of the house, the pension and the boat, with $40/6 + 30 + 20 = 170/3$ points. Both get more than 50, so neither envies the other.

If instead $p_A = (40, 30, 20, 10)$ and $p_B = (10, 20, 30, 40)$, line L1 gives the first two goods to $A$ and the last two to $B$, with 70 points each, and line L3 returns at once.

## Correctness

**Equitable.** Each whole move of line L7 keeps $T_W \ge T_L$, and line L8 makes them equal. If every good of $G$ moved whole, $W$ would hold only goods with $p_W(g) = 0$, so $T_W = 0 \le T_L$, and the last move would have been a move of line L8. So the loop ends with $T_W = T_L$.

**Pareto optimal.** Let $r \ge 1$ be the ratio of the last good that moved (or $r = 1$ if none moved). At the end, $W$ holds a share only of goods with ratio $p_W/p_L \ge r$, and $L$ holds a share only of goods with ratio at most $r$. Such a division maximizes $U_W + r\, U_L$ over all share vectors, because each good goes to the agent with the larger weighted points. A division that is better for one agent and not worse for the other would give a larger value of $U_W + r\, U_L$, since $r > 0$. So none exists.

**Envy-free.** Let $T$ be the common number of points. If $T < 50$, each agent values the share of the other at $100 - T > T$, so swapping the shares makes both agents better off, which contradicts Pareto optimality. So $T \ge 50$, and each agent values its share at least as much as the other share. The full proof is in proofs/correctness.md.

## Complexity

Lines L1 and L2 take $O(m)$ time. The sort of line L5 takes $O(m \log m)$, and the loop of lines L6 to L8 takes $O(m)$. So the time is $\Theta(m \log m)$ in the worst case, and $O(m)$ if the goods are already sorted by ratio. Extra space is $O(m)$.

## Properties

- **Equitable, envy-free and Pareto optimal** for the reported points, as proved above. For two agents, all equitable Pareto optimal divisions give the same number of points, so no other rule with these two goals gives either agent more.
- **At most one split good.** Only line L8 splits a good, and it runs once.
- **At least 50 points each.** Both agents get the same $T \ge 50$, often more.
- **Not strategyproof.** An agent that knows the points of the other can gain by false points, for example by putting points just below the bids of the other on goods that it will lose anyway. Then its reported points on the goods that it wins are lower, and the step that makes the points equal gives it more of these goods. An agent that reports its true points is still sure of at least 50 true points, whatever the other reports, because the result is envy-free for the reported points.
- **Divisible goods.** The guarantees need the split of one good. With indivisible goods, a split can be replaced by joint ownership, a sale or a lottery, or by the weaker goals of [indivisible goods allocation](/indivisible-goods-allocation/).

## Variants and improvements

- **More agents.** The procedure works for two agents only. With three or more agents, envy-free, equitable and Pareto optimal divisions of goods with linear values need not exist together, and other rules are used, such as the competitive equilibrium from equal incomes or [maximum Nash welfare](/maximum-nash-welfare/).
- **Proportional allocation of points.** Brams and Taylor also describe a simpler point rule that gives each good to the two agents in proportion to their points. It is equitable but in general not Pareto optimal.
- **Divide and choose.** For one heterogeneous good, such as a cake, [divide and choose](/divide-and-choose/) is the classic two-agent rule. It is envy-free but not equitable.
- **A link to knapsack.** The order of line L5 is the order of a greedy rule for the [fractional knapsack](/fractional-knapsack/) problem: the winner gives up the goods with the lowest value per point gained by the other, and only the last item is split.

## When to use it

Use adjusted winner for two parties who must share several divisible goods or issues and can state their values in points, as in a divorce, a business breakup or a negotiation on several issues. It suits cases where the parties want equal satisfaction and no waste. It needs honest points to keep its guarantees, so it fits best when parties cannot learn much about the points of the other, or when a mediator checks the reports.

## Pitfalls

- **Points that do not sum to 100.** The test for envy uses the totals. If one agent spreads 120 points, its share must be compared with the rest of its own total.
- **The wrong order.** Moving goods in an order other than increasing $p_W/p_L$ still gives equal points, but the result need not be Pareto optimal: both agents could get more by moving a different good.
- **Moving goods with $p_W = 0$.** They give $L$ points at no cost to $W$, but $W$ holds such a good only if $p_L = 0$ too (by line L1), so they do not matter. Code that leaves them out of line L5 avoids a division by zero in the order.
- **Floating point.** The share $\alpha$ and the test of line L7 should use exact rationals; with floats the totals may differ by a rounding error, and the test for equality fails.

## Implementations

## History

Steven Brams and Alan Taylor introduced adjusted winner in their 1996 book Fair Division, where Chapter 4 proves its properties and Chapter 5 applies it to disputes. They wrote about it for a general readership in The Win-Win Solution (1999). The procedure brings the goals of the [cake cutting problem](/cake-cutting-problem/) (envy-freeness, equitability and efficiency) to the division of several goods by points.

## References
