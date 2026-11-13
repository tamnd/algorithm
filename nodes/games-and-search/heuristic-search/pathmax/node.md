---
tag: ZEM5KS
kind: concept
slug: pathmax
name: PATHMAX
aliases:
- path max correction
area: games-and-search/heuristic-search
level: research
summary: A rule that raises h of a child to h of its parent minus the action cost. Then f never drops from a parent to a child, but A* can still need to reopen states.
prereqs: [consistent-heuristic, a-star-search]
see_also: [admissible-heuristic, iterative-deepening-a-star, pattern-database, learning-real-time-a-star, graph-search-vs-tree-search, a-star-optimality]
sources:
  - paper: doi:10.1016/0004-3702(84)90003-1
    title: László Mérő, A heuristic search algorithm with modifiable estimate, Artificial Intelligence 23(1) (1984)
    locator: pp. 13 to 27 (algorithm B', which changes the estimates during the search with two propagation rules between a node and its successors)
  - paper: doi:10.1016/j.artint.2011.02.001
    title: Ariel Felner, Uzi Zahavi, Robert Holte, Jonathan Schaeffer, Nathan Sturtevant and Zhifu Zhang, Inconsistent heuristics in theory and practice, Artificial Intelligence 175(9-10) (2011)
    locator: Section 5.1 (pathmax rules 1 and 2), Section 5.2 (pathmax does not make f monotonic), Section 5.3 (bidirectional pathmax, rule 3, and its use in IDA*) and Section 5.4 (the limits of rule 2)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 3 (the monotone restriction and the correction of f along a path for heuristics that are not monotone)
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications
    locator: Chapter 2 (search with heuristics that are not consistent, and the reopening of nodes)
---

Pathmax is a rule that makes an [admissible](/admissible-heuristic/) heuristic look more consistent along the paths that a search walks. When a search generates a child $c$ of a state $p$ by an action of cost $c(p, c)$, it replaces $h(c)$ by $\max(h(c),\ h(p) - c(p, c))$. The new value is still a lower bound on the true cost, and it makes $f = g + h$ of the child at least $f$ of the parent. The rule is often written as $f(c) \leftarrow \max(f(c), f(p))$. Mérő introduced it in 1984 as one of two rules of his algorithm B'. It does not turn an inconsistent heuristic into a [consistent](/consistent-heuristic/) one: Felner et al. (2011) showed that [A*](/a-star-search/) with pathmax can still find a cheaper path to a closed state and must then reopen it.

## In plain words

A guess of the distance left must never be too large. Suppose that at one place your guess says "at least 10 more", and you take a step of length 3. Then at the next place at least 7 must be left, whatever the guess there says, because otherwise the first place would be closer than 10. So if the new guess says 2, you can raise it to 7 and still never guess too much.

This keeps your total, the distance walked plus the guess, from going down as you walk. But it only fixes the guesses on the roads you have walked. A road you have not walked yet can still lead to a place by a shorter way, and then you must go back and look again.

## The idea

### The rules

Let $h$ be admissible, $h \le h^*$, where $h^*(n)$ is the cost of a cheapest path from $n$ to a goal. For a parent $p$ and a child $c_i$:

- **Rule 1 (pathmax).** $h(c_i) \leftarrow \max\bigl(h(c_i),\ h(p) - c(p, c_i)\bigr)$.
- **Rule 2.** If $p$ is not a goal, $h(p) \leftarrow \max\bigl(h(p),\ \min_i (h(c_i) + c(p, c_i))\bigr)$, over all successors $c_i$ of $p$.
- **Rule 3 (the reverse of rule 1).** If the graph has an action from $c$ back to $p$, $h(p) \leftarrow \max\bigl(h(p),\ h(c) - c(c, p)\bigr)$.

Rules 1 and 2 are those of Mérő, in the form of Felner et al., who note that the printed form of rule 2 in the original paper has an error. Rule 3 is from Felner et al.; with rule 1 it gives *bidirectional pathmax* (BPMX) for undirected graphs, which can push a large value from a child up to its parent and from there to the other children.

**Fact 1 (the rules keep admissibility).** After any number of applications of the rules, $h \le h^*$ still holds.

*Proof.* It is enough to check one application, with $h \le h^*$ before it. For rule 1, one path from $p$ to a goal starts with the action to $c_i$, so $h^*(p) \le c(p, c_i) + h^*(c_i)$, and so $h(p) - c(p, c_i) \le h^*(p) - c(p, c_i) \le h^*(c_i)$. Rule 3 is the same with the action from $c$ to $p$. For rule 2, a cheapest path from a non-goal $p$ starts with some action to a successor $c_j$, so $h^*(p) = \min_i (c(p, c_i) + h^*(c_i)) \ge \min_i (c(p, c_i) + h(c_i))$. $\square$

**Fact 2 (f does not drop from parent to child).** If A* applies rule 1 each time it generates a child, with $g(c) = g(p) + c(p, c)$, then $f(c) \ge f(p)$ for the values that A* stores.

*Proof.* $f(c) = g(p) + c(p, c) + h(c) \ge g(p) + c(p, c) + h(p) - c(p, c) = f(p)$. $\square$

**Fact 3 (A* removes states in nondecreasing order of f).** With rule 1, the values $f$ of the states that A* removes from OPEN do not go down, also when it reopens states.

*Proof.* When A* removes $p$, every entry of OPEN has $f \ge f(p)$. The entries that the expansion of $p$ adds have $f \ge f(p)$ by Fact 2. So after the expansion all entries still have $f \ge f(p)$, and the next state removed has $f \ge f(p)$. $\square$

### What pathmax does not do

With a consistent heuristic, A* never reopens a state, because each state leaves OPEN with its least cost $g^*$. It is tempting to think that Fact 3 gives the same result, but it does not. Fact 3 is about the order of the removals. Consistency also bounds $h$ on the paths that the search has not walked yet, and pathmax knows nothing about them. A state $b$ can still leave OPEN with $g(b) > g^*(b)$ when the cheapest path to $b$ goes through a state whose $f$ is larger than $f(b)$ at that time. Felner et al. (Section 5.2) give such an example and note that Nilsson and Zhou and Hansen made the same point.

So the A* that uses pathmax must keep the reopening of closed states to stay optimal. Pathmax can still pay off: a larger $h$ can only remove states from the set with $f < C^*$, and in [IDA*](/iterative-deepening-a-star/) rule 3 prunes subtrees that rule 1 cannot. Felner et al. (Section 5.3) observe that rule 1 alone gives IDA* no extra pruning, because a child that inherits $f$ from its parent never exceeds a threshold that the parent did not exceed.

## Examples

The directed graph has the actions S→A 1, S→B 3, A→B 1, B→C 1 and C→G 1, and the goal is G. The heuristic is $h(S) = 0$, $h(A) = 3$ and $h(B) = h(C) = h(G) = 0$. The true costs to G are $h^* = 4, 3, 2, 1, 0$, so $h$ is admissible, but it is not consistent at A→B. A* breaks ties in $f$ toward larger $g$.

| run | expansions in order, with the f of each | reopenings | cost |
| --- | --- | --- | --- |
| A* with reopening | S 0, B 3, C 4, A 4, B 2, C 3 | 2 | 4 |
| A* with reopening and pathmax | S 0, B 3, C 4, A 4, B 4, C 4 | 2 | 4 |
| A* without reopening | S 0, B 3, C 4, A 4 | 0 | 5 |
| A* without reopening, with pathmax | S 0, B 3, C 4, A 4 | 0 | 5 |

Without pathmax, the values of $f$ go down from 4 to 2 when B is reopened by the path S-A-B with $g = 2$ and $h = 0$. With pathmax, B gets $h = \max(0, 3 - 1) = 2$ from A, so its $f$ is 4, and then C gets $h = \max(0, 2 - 1) = 1$ and $f = 4$. The sequence of $f$ is nondecreasing, as Fact 3 says. Still, B and C are expanded twice, because the first time B left OPEN it had $g = 3$ by S→B, and A, which lies on the cheaper path, had the larger $f = 4$. A* that does not reopen states returns the path S-B-C-G of cost 5 with or without pathmax.

Rule 2 on the same graph: after A* expands C with its only successor G, rule 2 gives $h(C) \leftarrow \max(0, 0 + 1) = 1$, which is exact. After it expands S, rule 2 gives $h(S) \leftarrow \max(0, \min(3 + 1, 0 + 3)) = 3$, which is a better bound than 0 but still below $h^*(S) = 4$.

## Where it is used

- **A* with inconsistent heuristics.** Many programs that use a random choice of [pattern databases](/pattern-database/), compressed pattern databases or dual lookups apply rule 1 when they generate a child. It costs one subtraction and one comparison per child.
- **IDA* with BPMX.** On undirected spaces such as the sliding-tile puzzles and Rubik's cube, rules 1 and 3 let a child with a large $h$ cut off its parent and its siblings. Felner et al. (Section 7) report experiments in these domains in which IDA* with randomly chosen pattern database lookups and BPMX, which is inconsistent, often generates far fewer nodes than with the same number of fixed lookups, which is consistent.
- **Algorithms with a bounded number of reexpansions.** Mérő's algorithm B', and Martelli's algorithm B before it, combine the order of A* with rules that change the estimates or the choice of the next state, to bound the work when $h$ is inconsistent.
- **Heuristic learning.** Real-time searches such as [LRTA*](/learning-real-time-a-star/) raise $h$ of a state to the least $c + h$ over its successors, which is rule 2 applied as the agent moves.

## References
