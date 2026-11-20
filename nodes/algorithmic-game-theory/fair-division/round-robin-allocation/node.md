---
tag: MZAAJ5
kind: algorithm
slug: round-robin-allocation
name: Round-robin allocation
aliases:
- round-robin picking sequence
area: algorithmic-game-theory/fair-division
level: intro
summary: Agents take turns picking their favourite remaining good. With additive valuations the result is EF1.
model: word-ram
complexity:
  vars: {n: the number of agents, m: the number of goods}
  time: {worst: O(n m log m)}
  space: {extra: O(n m)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [envy-freeness-up-to-one-good]
see_also: [envy-cycle-elimination, indivisible-goods-allocation, serial-dictatorship, maximin-share, pareto-optimality, dominant-strategy-incentive-compatibility, greedy-algorithm, approximate-mms-allocation]
sources:
  - paper: doi:10.1145/3355902
    title: "Ioannis Caragiannis, David Kurokawa, Herve Moulin, Ariel D. Procaccia, Nisarg Shah and Junxing Wang, The unreasonable fairness of maximum Nash welfare, ACM Transactions on Economics and Computation 7(3) (2019), article 12 (conference version EC 2016)"
    locator: Section 3, the draft mechanism (the EF1 argument by phases and the remark that the result need not be Pareto optimal)
---

Round-robin allocation divides indivisible goods among $n$ agents by letting them pick in turn: agent 1, agent 2, up to agent $n$, then agent 1 again, and so on, and each agent takes its favourite good among those still free. For [additive valuations](/indivisible-goods-allocation/) the result is [envy-free up to one good](/envy-freeness-up-to-one-good/) (EF1), and it is computed in $O(n m \log m)$ time. It is the draft used to pick players for sports teams. The result need not be [Pareto optimal](/pareto-optimality/), and it need not be EF1 when valuations are not additive; [envy-cycle elimination](/envy-cycle-elimination/) handles general monotone valuations.

## In plain words

Children pick teams in the schoolyard this way. The first child takes the player they like best. The second child takes their own favourite among the players left, and so on. When everybody has had a turn, the first child picks again. This goes on until nobody is left.

Nobody gets a lot more than anybody else. If you pick after me, then in every round I pick before you, so my pick is at least as good for me as yours. If you pick before me, the only head start you have over me is your very first pick. So if I envy you, the envy goes away when I ignore that first pick.

## The problem

There are $n$ agents and $m$ indivisible goods. Agent $i$ values good $g$ at $v_i(g) \ge 0$, and the value of a bundle is the sum of the values of its goods. The goal is an allocation $A = (A_1, \dots, A_n)$ of all goods that is EF1: for all agents $i, j$ with $A_j \ne \emptyset$, some $g \in A_j$ has $v_i(A_i) \ge v_i(A_j \setminus \{g\})$. The agents pick in a fixed order, here $1, 2, \dots, n$.

## The algorithm

```pseudo id=main
ROUND-ROBIN(v)                         ▷ n agents, m goods, additive values v_i(g) ≥ 0
L1  for each agent i: L_i ← the goods sorted by v_i decreasing, ties by index; A_i ← ∅
L2  R ← all goods; t ← 0
L3  while R ≠ ∅ do
L4      i ← (t mod n) + 1
L5      g ← the first good of L_i that is still in R
L6      A_i ← A_i ∪ {g}; R ← R \ {g}
L7      t ← t + 1
L8  return A
```

Line L1 fixes each agent's preference list once. Line L4 picks the agent whose turn it is. Line L5 walks along the list of agent $i$ from where it stopped last time; a good that is not in $R$ now will never come back, so each list is read once from left to right over the whole run. Lines L6 and L7 record the pick and move to the next turn. Another order of the agents is handled by renaming them.

## Example

Three agents value six goods $a, \dots, f$ as follows.

| | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ |
|---|---|---|---|---|---|---|
| agent 1 | 8 | 7 | 4 | 3 | 2 | 1 |
| agent 2 | 8 | 2 | 6 | 5 | 1 | 3 |
| agent 3 | 6 | 7 | 5 | 1 | 4 | 2 |

The preference lists of line L1 are $a, b, c, d, e, f$ for agent 1, $a, c, d, f, b, e$ for agent 2 and $b, a, c, e, f, d$ for agent 3.

| turn $t$ | agent | free goods before the pick | pick |
|---|---|---|---|
| 0 | 1 | $a, b, c, d, e, f$ | $a$ |
| 1 | 2 | $b, c, d, e, f$ | $c$ |
| 2 | 3 | $b, d, e, f$ | $b$ |
| 3 | 1 | $d, e, f$ | $d$ |
| 4 | 2 | $e, f$ | $f$ |
| 5 | 3 | $e$ | $e$ |

The output is $A_1 = \{a, d\}$, $A_2 = \{c, f\}$, $A_3 = \{b, e\}$, worth 11, 9 and 11 to their owners. Agent 2 values $A_1$ at 13 and envies agent 1, which picked before it; without $a$ the bundle is worth 5, so the envy is within EF1. Agent 1, which picks first, envies nobody. Each agent's [maximin share](/maximin-share/) is 8 here, so this output also meets every maximin share.

## Correctness

Fix two agents $i$ and $j$. Cut the sequence of turns into phases that start at the turns of $i$. In each phase, $i$ picks first, and $j$ picks at most once, later in the phase; the good of $j$ was free when $i$ picked, so $i$ values its own pick at least as much. If $j$ comes after $i$ in the order, every pick of $j$ lies in some phase, so $v_i(A_i) \ge v_i(A_j)$. If $j$ comes before $i$, only the first pick $g_1$ of $j$ lies before the first phase, so $v_i(A_i) \ge v_i(A_j \setminus \{g_1\})$. Hence the output is EF1. The loop runs $m$ times, because each turn removes one good from $R$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Line L1 sorts $n$ lists of length $m$ in $O(n m \log m)$ time. Over the whole run, the pointer of each agent in line L5 moves at most $m$ steps, so lines L3 to L7 take $O(n m)$ time in total. The time is $O(n m \log m)$ and the extra space is $O(n m)$ for the lists.

## Properties

- **EF1, with no envy toward later agents.** Agent $i$ does not envy any agent that picks after it, and its envy toward an earlier agent disappears after removing that agent's first pick.
- **Balanced bundle sizes.** The sizes differ by at most one.
- **Not Pareto optimal.** Two agents value goods $g_0, \dots, g_3$ at $(4, 3, 2, 1)$ and $(6, 3, 2, 1)$. Round-robin gives $\{g_0, g_2\}$ to agent 1 and $\{g_1, g_3\}$ to agent 2, worth 6 and 4. The allocation $\{g_1, g_2, g_3\}$ and $\{g_0\}$ is worth 6 and 6, which is better for agent 2 and no worse for agent 1. Equal bundle sizes block such trades of one good for several.
- **Not strategyproof.** Agent 1 values $a, b, c$ at $3, 2, 1$ and agent 2 at $1, 3, 2$. Picking sincerely, agent 1 takes $a$, agent 2 takes $b$ and agent 1 gets $c$, for a total of 4. If agent 1 takes $b$ first, agent 2 takes $c$ and agent 1 still gets $a$, for a total of 5. So round-robin is not [dominant-strategy incentive compatible](/dominant-strategy-incentive-compatibility/).
- **Deterministic, not online.** The output depends only on the order and the values, with ties broken by index.

## Variants and improvements

- **Picking sequences.** Any fixed sequence of agents, such as $1, 2, 2, 1$, gives a picking sequence rule; round-robin is the sequence $1, 2, \dots, n$ repeated. With at most one good per agent, it is [serial dictatorship](/serial-dictatorship/).
- **Chores.** With costs in place of values and each agent taking its least costly chore, the same argument gives EF1 for chores, where the envy disappears after removing one chore from the agent's own bundle.
- **Non-additive valuations.** For general monotone valuations, use [envy-cycle elimination](/envy-cycle-elimination/), which gives EF1.
- **Approximate maximin share.** Round-robin also appears as a last step of [approximate MMS algorithms](/approximate-mms-allocation/), which first remove large goods by fixed rules.

## When to use it

Use round-robin when valuations are additive and EF1 is enough, especially when the agents can pick in person, as in a draft, so that only the agents' own choices are needed. When efficiency matters too, use an EF1 and Pareto optimal method such as the [Barman-Krishnamurthy-Vaish algorithm](/ef1-and-pareto-optimal-algorithm/) or [maximum Nash welfare](/maximum-nash-welfare/).

## Pitfalls

- **Sorting in the loop.** Sorting the free goods of $R$ again at every turn in line L5 costs $O(m \log m)$ per turn and $O(m^2 \log m)$ in total. The lists of line L1 are sorted once.
- **Restarting the pointer in line L5.** Starting each agent's search at the head of $L_i$ in every turn makes the cost of line L5 grow with the number of goods already taken, up to $O(m^2)$ in total. The pointer only needs to move forward.
- **Using it for non-additive valuations.** Line L1 ranks single goods, and the EF1 proof compares single goods, which is valid only for additive valuations. With a coverage valuation, an agent can lose EF1: agent $B$ values a set of coloured goods by the colours it covers, with weights red 2, blue 2 and green 1, and goods $0, \dots, 4$ are red, blue, green, blue and blue; agent $A$ is additive with values $5, 1, 4, 2, 3$. Round-robin with $A$ first gives $A$ the goods $0, 2, 4$ and $B$ the goods $1, 3$, worth 2 to $B$, while $\{0, 2, 4\}$ minus any one good is still worth at least 3 to $B$.
- **Forgetting ties.** Line L1 must break ties by a fixed rule, here the good index, so that the output is reproducible; the EF1 proof holds for any tie rule.

## Implementations

## History

Round-robin picking is the draft mechanism of sports leagues. Caragiannis et al. (2019, Section 3) gave the phase argument that it is EF1 for additive valuations and noted that it is not Pareto optimal.

## References
