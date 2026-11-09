---
tag: AVNAXF
kind: algorithm
slug: iterated-local-search
name: Iterated local search
aliases:
- ILS
- large-step Markov chain
- chained local optimization
area: optimization/metaheuristics
level: advanced
summary: Repeat local search from perturbed copies of the current best solution.
model: word-ram
complexity:
  vars: {K: the number of iterations, H: the time of one run of the local search, P: the time of one perturbation, s: the size of one solution}
  time: {worst: O(K (H + P) + H)}
  space: {extra: O(s)}
properties: {deterministic: false, recursive: false}
prereqs: [local-search, hill-climbing, local-optimum, neighborhood-structure]
see_also: [random-restart-hill-climbing, variable-neighborhood-search, two-opt, lin-kernighan, traveling-salesman-problem, large-neighborhood-search, fitness-landscape, simulated-annealing]
sources:
  - paper: doi:10.1007/0-306-48056-5_11
    title: Helena R. Lourenço, Olivier C. Martin and Thomas Stützle, Iterated Local Search, in Fred Glover and Gary A. Kochenberger (editors), Handbook of Metaheuristics, Kluwer, 2003
    locator: the whole chapter (the framework, perturbation, acceptance, the double bridge for the TSP); preprint arXiv:math/0102188
  - book: isbn:9783319910857
    title: Michel Gendreau and Jean-Yves Potvin (editors), Handbook of Metaheuristics, third edition, Springer, 2019
    locator: Chapter 5, Iterated Local Search, Framework and Applications, by Helena R. Lourenço, Olivier C. Martin and Thomas Stützle, from p. 129
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Section 2.3, Hybrid SLS Methods, from p. 85 (iterated local search), and Section 8.3, Iterated Local Search Algorithms for the TSP, from p. 384
  - paper: "Olivier Martin, Steve W. Otto and Edward W. Felten, Large-step Markov chains for the traveling salesman problem, Complex Systems 5(3), 1991"
    locator: pp. 299 to 326 (the double-bridge kick followed by local search, with an acceptance test)
---

Iterated local search (ILS) runs a [local search](/local-search/) to a [local optimum](/local-optimum/), then repeats three steps: change the local optimum a little (a *perturbation*, or *kick*), run the local search again from the changed solution, and decide which of the two local optima to keep (the *acceptance* rule). It is a random walk over local optima instead of over all solutions. Unlike [random restarts](/random-restart-hill-climbing/), it starts each new descent near a good solution, so it keeps most of what the earlier work found. For the [traveling salesman problem](/traveling-salesman-problem/), with the *double-bridge* kick and [2-opt](/two-opt/), 3-opt or [Lin-Kernighan](/lin-kernighan/) as the local search, it is one of the most effective simple methods. It has no general guarantee of reaching a global optimum.

## In plain words

A walker goes downhill and stops in a hollow. Instead of being flown to a random place in the field, the walker takes a few big random steps from the hollow, then walks downhill again. If the new hollow is lower, the walker stays there; if not, the walker goes back to the old one and tries other big steps.

The big steps must be large enough that the downhill walk does not slide straight back into the same hollow, and small enough that the walker stays in the good part of the field. Good hollows are often near other good hollows, so this search near the best one found tends to pay off.

## The problem

The input is a set $S$ of solutions, an objective $f : S \to \mathbb{R}$ to minimize, a local search procedure LOCAL-SEARCH that maps any solution to a local minimum of a [neighborhood](/neighborhood-structure/) $N$, a random perturbation PERTURB, an acceptance rule, a start $x_0$ and a number of iterations $K$. The output is the best local minimum visited. The aim is a global minimum, which the method cannot prove it has found.

## The algorithm

```pseudo id=main
ITERATED-LOCAL-SEARCH(x0, f, LOCAL-SEARCH, PERTURB, ACCEPT, K)
L1  x ← LOCAL-SEARCH(x0), b ← x
L2  for k ← 1 to K do
L3      y ← PERTURB(x)                         ▷ the kick
L4      z ← LOCAL-SEARCH(y)                    ▷ a new local minimum
L5      if ACCEPT(x, z) then x ← z             ▷ better: f(z) < f(x); always: accept
L6      if f(x) < f(b) then b ← x
L7  return b
```

Line L1 finds a first local minimum. Line L3 kicks it to a solution outside its basin, line L4 descends to a new local minimum, and line L5 decides where the next kick starts. The rule *better* accepts only a strictly better local minimum, so the search stays at the best one found and kicks it again and again. The rule *always* accepts every new local minimum, which gives a random walk over local optima. Many rules lie between, such as accepting a worse local minimum with a small probability, as in [simulated annealing](/simulated-annealing/). Line L6 keeps the best one.

For tours the classic kick is the **double bridge**: cut the tour into four segments $A, B, C, D$ and reconnect them as $A, D, C, B$, with no segment reversed. This changes four edges, and it is hard for 2-opt and 3-opt to undo, since those moves change two or three edges and the double bridge cannot be built from such moves that each keep the tour in one piece.

## Example

Take nine cities in the plane, numbered 0 to 8, at $(17,2)$, $(11,19)$, $(19,9)$, $(2,16)$, $(11,12)$, $(13,0)$, $(1,3)$, $(14,20)$ and $(7,11)$, with distances rounded to the nearest integer. The local search is best-improvement 2-opt, the kick is a uniform random double bridge, and the acceptance rule is *better*. Start from the tour $0, 1, \ldots, 8$ of length 128. Line L1 descends to the 2-opt local minimum 0 2 4 8 7 1 3 6 5 of length 72. With the random generator `random.Random(3)` of the Python code:

| $k$ | kicked tour $y$ | $f(y)$ | local minimum $z$ | $f(z)$ | accepted | $f(b)$ |
|---|---|---|---|---|---|---|
| 1 | 0 2 4 8 6 5 1 3 7 | 101 | 0 2 7 1 3 4 8 6 5 | 71 | yes | 71 |
| 2 | 0 2 7 5 4 8 6 1 3 | 114 | 0 2 7 1 3 4 8 6 5 | 71 | no | 71 |
| 3 | 0 2 7 1 3 5 8 6 4 | 98 | 0 2 7 1 3 4 8 6 5 | 71 | no | 71 |
| 4 | 0 4 8 6 5 7 1 3 2 | 95 | 0 5 6 8 3 1 7 4 2 | 70 | yes | 70 |
| 5 | 0 5 6 2 1 7 4 8 3 | 92 | 0 5 6 3 8 4 1 7 2 | 69 | yes | 69 |
| 6 | 0 5 1 7 2 8 4 6 3 | 101 | 0 5 6 3 8 4 1 7 2 | 69 | no | 69 |

In iterations 2 and 3 the kick is undone: 2-opt returns to the same local minimum, and the rule *better* rejects it. In iterations 4 and 5 the search moves to better local minima. The result has length 69. By enumeration of all $8!$ tours that start at city 0, this instance has exactly four 2-opt local minima, counting a tour and its reverse as one, of lengths 69, 70, 71 and 72, and 69 is the optimum. The run visited all four.

## Correctness

ILS has no optimality guarantee, so "correct" means the following. If the local search stops on every input, ILS stops after $K + 1$ runs of it. Every current solution and the result are local minima of $N$, and the result is the best of the current solutions. With the rule *better* the current value never increases.

A probability bound holds under an assumption: if, whatever happened before, each iteration ends at a global minimum with probability at least $q > 0$, then all $K$ iterations miss with probability at most $(1 - q)^K \le e^{-qK}$. For the double bridge followed by 2-opt, no such $q$ is known in general, so this is a conditional statement. The [full proof](proofs/correctness.md) also shows when the double bridge changes exactly four edges.

## Complexity

The time is $O(K (H + P) + H)$, where $H$ bounds one run of the local search and $P$ one perturbation; the extra $H$ is line L1. A double bridge on an array costs $O(n)$. In the worst case $H$ itself can be exponential, as for any [hill climbing](/hill-climbing/) (see [PLS](/pls/)). In practice the descent after a small kick is much shorter than a descent from a random start, because the kicked solution is close to a local minimum; this is the main source of speed of ILS over restarts. Fast TSP codes also use *don't-look bits*, so that the descent after a kick scans only the cities near the changed edges. The extra space is a constant number of solutions, $O(s)$.

## Properties

- **A walk over local optima.** Each step goes from one local minimum to another, so the method searches the much smaller set of local minima.
- **Three design choices.** The local search, the perturbation and the acceptance rule. The local search does most of the work; the kick sets how far the walk jumps; the acceptance rule sets the balance between [intensification and diversification](/intensification-and-diversification/).
- **The strength of the kick matters.** Too weak, and the local search undoes it, as in iterations 2 and 3 of the example. Too strong, and ILS becomes a random restart.
- **Randomized.** Different seeds give different runs.
- **No general guarantee.** With the rule *better*, the walk can be stuck at a local minimum from which no kick and descent leads to a better one.

## Variants and improvements

- **Random restarts as a special case.** If PERTURB ignores its input and returns a random solution, and the rule is *always*, ILS is [random-restart hill climbing](/random-restart-hill-climbing/).
- **Large-step Markov chains.** Martin, Otto and Felten (1991) accepted a worse local minimum with a probability as in simulated annealing.
- **Iterated Lin-Kernighan.** With [Lin-Kernighan](/lin-kernighan/) as the local search and double-bridge kicks, ILS is among the best heuristics for large TSP instances.
- **Adaptive kicks.** Change the strength of the perturbation during the run: larger when the search returns to the same local minimum, as in [variable neighborhood search](/variable-neighborhood-search/), whose shaking step is a kick of growing size.
- **Destroy and repair.** [Large neighborhood search](/large-neighborhood-search/) uses a kick that removes part of a solution and an exact or greedy repair as the descent.
- **Restart on stagnation.** Add a random restart when no improvement occurs for many iterations.

## When to use it

Use ILS when you already have a good local search for the problem and want a simple way to go beyond its first local optimum. It needs only a kick that the local search does not undo at once, and a rule for acceptance. Prefer it over random restarts when good local optima are near each other, which is common for the TSP, scheduling and assignment problems, and when a descent from a random start is expensive. On the 10-city instance of the [late acceptance](/late-acceptance-hill-climbing/) page (optimum 231), 2-opt has only two local minima as cycles, and ILS with 10 iterations from the tour $0, 1, \ldots, 9$ reached the optimum with each of the 30 seeds 0 to 29; this small case shows only that the code works, not that the method is better than another.

## Pitfalls

- **A kick that the local search undoes.** A random 2-opt move as the kick of a 2-opt local search is undone at once. Use a move that the local search cannot reverse in one step, such as the double bridge for 2-opt and 3-opt.
- **A kick that is too large.** If the kick moves to an almost random solution, each descent is as long as from a random start, and the method loses its advantage.
- **Accepting equal local minima by mistake.** The rule *better* uses a strict test; with $\le$ the walk drifts among equal local minima. That can be useful, but it should be a choice.
- **Returning the current solution.** With an acceptance rule that allows worse solutions, the current solution can be worse than the best. Return $b$.

## Implementations

## History

Martin, Otto and Felten (1991) introduced large-step Markov chains for the TSP: a double-bridge kick followed by 3-opt or Lin-Kernighan, with an acceptance test. Lourenço, Martin and Stützle described iterated local search as a general framework in the 2003 Handbook of Metaheuristics, and their chapter in the 2019 edition reviews its applications. Hoos and Stützle cover the method and its use for the TSP in their book.

## References
