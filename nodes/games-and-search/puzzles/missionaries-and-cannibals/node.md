---
tag: YW0KDJ
kind: problem
slug: missionaries-and-cannibals
name: Missionaries and cannibals problem
aliases:
- River crossing puzzle
area: games-and-search/puzzles
level: intro
summary: "Ferry n missionaries and n cannibals across a river in a small boat so that cannibals never outnumber missionaries on a bank; the classic case of 3 and 3 with a boat for 2 needs 11 crossings."
prereqs: [breadth-first-search, state-space]
see_also: [water-jug-problem, tower-of-hanoi, state-space-search, implicit-graph, invariant, strips, a-star-search, bidirectional-search]
sources:
  - paper: "Saul Amarel, On representations of problems of reasoning about actions, in Donald Michie (editor), Machine Intelligence 3, Edinburgh University Press, 1968"
    locator: "pp. 131-171"
  - paper: doi:10.2307/3619658
    title: "Ian Pressman and David Singmaster, The jealous husbands and the missionaries and cannibals, The Mathematical Gazette 73(464), 1989"
    locator: "pp. 73-81"
  - paper: doi:10.1080/0025570X.1966.11975705
    title: "Robert Fraley, Kenneth L. Cooke and Peter Detrick, Graphical solution of difficult crossing puzzles, Mathematics Magazine 39(3), 1966"
    locator: "pp. 151-157"
---

The missionaries and cannibals problem asks how $n$ missionaries and $n$ cannibals can cross a river in a boat that holds at most $k$ people, so that on neither bank the cannibals outnumber the missionaries who are there. The classic case $n = 3$, $k = 2$ needs 11 crossings. With a boat for 2 or 3 the puzzle is solvable exactly when $n \le 2k - 1$, and with a boat for 4 every $n$ is solvable. Saul Amarel used it in 1968 to show how the choice of a [state space](/state-space/) can make a search problem easy.

## In plain words

Three missionaries and three cannibals stand on one bank of a river with a boat that carries two. Everyone must reach the other bank. If at any moment the cannibals on a bank outnumber the missionaries there, the missionaries are eaten, so that is not allowed. A bank with no missionaries is always safe. Somebody has to row the boat back each time, and that is what makes the puzzle hard: every trip across loses a passenger on the return. The trick is to send cannibals over first, then swap one missionary and one cannibal at the middle stage. Eleven trips are enough, and no plan uses fewer. With four people of each kind and the same boat no plan works at all, but a boat for four people solves any number of travellers.

## Definition

**Instance.** Integers $n \ge 1$ (missionaries, and as many cannibals) and $k \ge 1$ (boat capacity).

**States.** A state $(m, c, s)$ gives the missionaries $m$ and cannibals $c$ on the start bank and the side $s$ of the boat. The far bank holds $n - m$ and $n - c$. The start is $(n, n, \text{start})$ and the goal is $(0, 0, \text{far})$.

**Safety.** A bank is safe if it has no missionaries or at least as many missionaries as cannibals. A state is safe if both banks are safe.

**Crossings.** A crossing takes $i$ missionaries and $j$ cannibals from the side of the boat to the other side, with $1 \le i + j \le k$, and must end in a safe state. The boat cannot cross empty.

**Problem.** Find a shortest sequence of crossings from the start to the goal, or show that none exists.

Every safe state with $0 < m < n$ has $m = c$: the start bank needs $m \ge c$ and the far bank needs $n - m \ge n - c$. So the safe states fall into three groups, called $L$ ($m = n$), $R$ ($m = 0$) and $D$ ($0 < m = c < n$).

## Variants

- **Jealous husbands.** Three couples cross with a boat for two, and no woman may be with another man unless her husband is present. The puzzle goes back to the medieval collection attributed to Alcuin; Pressman and Singmaster trace how it became the missionaries and cannibals version in the late 19th century.
- **Boat rule.** Some versions also forbid the cannibals to outnumber the missionaries in the boat. For $n \le 8$ and $2 \le k \le 5$ the shortest crossing counts stay the same.
- **Other river puzzles.** The wolf, the goat and the cabbage, from the same medieval collection, is a smaller puzzle with the same structure: a few items, forbidden pairs on a bank, and a boat that must be rowed back.
- **Larger groups.** Changing $n$ and $k$ gives the table below, and the general analysis of such puzzles by drawing their state graph is due to Fraley, Cooke and Detrick.

## Examples

**The classic case.** Write the state as the missionaries and cannibals on the start bank, and B for the boat on the start bank. One shortest solution is:

| crossing | carried | start bank | far bank |
|---|---|---|---|
| 0 | | 3 M, 3 C, B | |
| 1 | 2 C over | 3 M, 1 C | 2 C, B |
| 2 | 1 C back | 3 M, 2 C, B | 1 C |
| 3 | 2 C over | 3 M | 3 C, B |
| 4 | 1 C back | 3 M, 1 C, B | 2 C |
| 5 | 2 M over | 1 M, 1 C | 2 M, 2 C, B |
| 6 | 1 M and 1 C back | 2 M, 2 C, B | 1 M, 1 C |
| 7 | 2 M over | 2 C | 3 M, 1 C, B |
| 8 | 1 C back | 3 C, B | 3 M |
| 9 | 2 C over | 1 C | 3 M, 2 C, B |
| 10 | 1 C back | 2 C, B | 3 M, 1 C |
| 11 | 2 C over | | 3 M, 3 C, B |

There are exactly 4 shortest solutions. Crossings 1 and 2 can also be "1 M and 1 C over, 1 M back", and crossings 10 and 11 can also be "1 M back, 1 M and 1 C over"; the two choices are independent. Of the 32 triples $(m, c, s)$, 20 are safe and 16 are reachable from the start.

**Fewest crossings** for $n$ pairs and a boat for $k$ ("no" means that no solution exists):

| $k$ \ $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | no | no | no | no | no | no | no | no | no | no |
| 2 | 1 | 5 | 11 | no | no | no | no | no | no | no |
| 3 | 1 | 3 | 5 | 9 | 11 | no | no | no | no | no |
| 4 | 1 | 1 | 3 | 5 | 7 | 9 | 11 | 13 | 15 | 17 |
| 5 | 1 | 1 | 3 | 3 | 5 | 7 | 7 | 9 | 11 | 13 |
| 6 | 1 | 1 | 1 | 3 | 3 | 5 | 5 | 7 | 7 | 9 |

With a boat for 1 there is no solution: the single passenger who arrives first on the far bank is the only one who can row back.

## Known algorithms

- **Breadth-first search.** There are $2(n + 1)^2$ triples and at most $(k + 1)(k + 2)/2 - 1$ loads per state, so a [breadth-first search](/breadth-first-search/) on the [implicit graph](/implicit-graph/) costs $O(n^2 k^2)$ time and $O(n^2)$ space and returns a shortest plan or proves that none exists. Every crossing can be undone, so the graph is undirected and a [bidirectional search](/bidirectional-search/) also works.
- **Heuristic search.** With $p$ people on the start bank and the boat there, a round trip moves at most $k - 1$ people net and the last crossing at most $k$, so at least $2\lceil (p - k)/(k - 1) \rceil + 1$ crossings remain when $p > k \ge 2$. This is an admissible heuristic for [A* search](/a-star-search/), though for the small classic graph plain search is enough.
- **Hand analysis on the state graph.** Fraley, Cooke and Detrick solve crossing puzzles by drawing the state graph. For this puzzle the safe pairs $(m, c)$ form the column $m = n$, the diagonal $m = c$ and the column $m = 0$, so a solution goes from the first column to the last one through the diagonal, and the 11 crossings of the classic case can be read off the drawing.

## Bounds

**Theorem.** For $k \in \{2, 3\}$, a solution exists if and only if $n \le 2k - 1$. For $k \ge 4$ a solution exists for every $n$, with $2n - 3$ crossings when $n \ge 3$.

*Proof of the limit.* Let $k \in \{2, 3\}$ and $n > k$. Consider a crossing from a state in $D$, at $(m, m)$.

- If the boat leaves the start bank with $i$ missionaries and $j$ cannibals, the new pair $(m - i, m - j)$ is in $D$ only if $i = j$, and since $2i \le k \le 3$ this means $i = j = 1$. It is in $R$ only if $i = m$, so $m \le k$. It is never in $L$.
- If the boat leaves the far bank, the new pair $(m + i, m + j)$ is in $D$ only if $i = j = 1$, and in $L$ only if $i = n - m$. It is never in $R$.

A crossing from $L$ with the boat on the start bank stays in $L$, reaches $D$ at $m = n - i \ge n - k$, or reaches $R$ only if all $n$ missionaries cross, which needs $n \le k$. A crossing from $L$ with the boat on the far bank brings people back to the start bank, so it stays in $L$.

Follow a solution up to its first state in $R$; one exists, because the goal is in $R$. By induction along this part, every state in $D$ with the boat on the far bank has $m \ge n - k$, and every state in $D$ with the boat on the start bank has $m \ge n - k + 1$: the first kind arises from $L$ (with $m \ge n - k$) or from the second kind by one step down, and the second kind arises only from the first kind by one step up. Since $n > k$, the first state in $R$ is entered from a state in $D$ with the boat on the start bank and $m \le k$. So $n - k + 1 \le k$, that is $n \le 2k - 1$. The table gives solutions for all $n \le 2k - 1$. $\square$

*Construction for $k \ge 4$.* Keep both banks balanced. Send 2 missionaries and 2 cannibals over and bring 1 of each back. Each round trip of 2 crossings moves one pair, both banks always have as many missionaries as cannibals, and when 2 pairs remain they cross together. From $n \ge 3$ pairs this takes $2(n - 2) + 1 = 2n - 3$ crossings; for $n \le 2$ one crossing suffices. For $k = 4$ the table shows that $2n - 3$ is the fewest for $3 \le n \le 10$.

**Size.** The state graph has at most $2(n + 1)^2$ vertices, and the safe ones number $O(n)$ because of the grouping into $L$, $D$ and $R$, so every instance is solved in time polynomial in $n$ and $k$.

## Reductions

- **Graph search.** The puzzle is a reachability question in an undirected graph with $O(n)$ safe states, so any shortest path method on a [state space](/state-space/) applies, as for the [water jug problem](/water-jug-problem/) and the [Tower of Hanoi](/tower-of-hanoi/).
- **Planning.** The puzzle is a small [STRIPS](/strips/) instance with the counts on each bank as fluents, and a common first exercise in planning languages.

## Applications

- Teaching [state-space search](/state-space-search/): the state space is small enough to draw, and it shows forbidden states, undirected moves and a non-obvious shortest path.
- Problem representation: Amarel shows a sequence of ever better formulations, from a description in words to a small graph in which the solution can be seen at once, and uses it to argue that finding a good representation is the central step in problem solving.
- Testing search programs, where a known optimum of 11 and a known impossible case ($n = 4$, $k = 2$) give quick checks.

## References
