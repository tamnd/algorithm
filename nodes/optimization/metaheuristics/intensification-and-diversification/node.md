---
tag: DWK8BM
kind: concept
slug: intensification-and-diversification
name: Intensification and diversification
aliases:
- intensification
- diversification
area: optimization/metaheuristics
level: advanced
summary: Searching promising areas in depth versus spreading the search to unexplored areas.
prereqs: [metaheuristic, local-search, local-optimum]
see_also: [tabu-search, tabu-list, grasp, late-acceptance-hill-climbing, scatter-search, path-relinking, simulated-annealing, premature-convergence]
sources:
  - paper: doi:10.1287/ijoc.2.1.4
    title: Fred Glover, Tabu Search, Part II, ORSA Journal on Computing 2(1), 1990
    locator: pp. 4 to 32 (long-term memory, intensification and diversification strategies)
  - book: isbn:9780792381877
    title: Fred Glover and Manuel Laguna, Tabu Search, Kluwer Academic Publishers, 1997
    locator: the chapters on long-term memory, frequency-based memory, intensification and diversification
  - paper: doi:10.1145/937503.937505
    title: Christian Blum and Andrea Roli, Metaheuristics in combinatorial optimization, overview and conceptual comparison, ACM Computing Surveys 35(3), 2003
    locator: pp. 268 to 308 (intensification and diversification as the two forces of every metaheuristic, and the components that drive each)
  - book: isbn:9783319910857
    title: Michel Gendreau and Jean-Yves Potvin (editors), Handbook of Metaheuristics, third edition, Springer, 2019
    locator: Chapter 2, Tabu Search, from p. 37 (intensification and diversification in tabu search)
---

Intensification and diversification are the two aims that a [metaheuristic](/metaheuristic/) must balance. *Intensification* searches the region around good solutions found so far more closely, in the hope that better ones are near. *Diversification* moves the search to regions it has not seen, so that it does not spend all its time near one [local optimum](/local-optimum/). Glover introduced the terms in [tabu search](/tabu-search/), where long-term memory drives both, and Blum and Roli later used them to compare all metaheuristics. Too much intensification makes a search stall near one solution; too much makes it a random sampler. There is no general rule for the right balance; it depends on the problem and is set by parameters.

## In plain words

You look for the deepest point in a range of hills, in fog. When you find a deep hollow, you can search all around it carefully, because a deeper spot is often close by. That is intensification. Or you can walk away to a part of the range you have not seen yet, because the deepest point may be there. That is diversification.

Doing only the first, you search one valley for ever. Doing only the second, you never look closely anywhere. A good search does both, and decides when to switch.

## The idea

In tabu search, Glover tied the two aims to kinds of memory.

- **Recency memory**, the [tabu list](/tabu-list/), works in the short term: it stops the search from undoing recent moves, so it leaves the current local optimum.
- **Frequency memory** counts how often each attribute, such as an edge of a tour or a bit set to 1, has appeared in the current solution or in good solutions. *Intensification* favors attributes that often appear in good solutions, for example by fixing them or by restarting from elite solutions. *Diversification* penalizes attributes that appear often, so the search tries new ones.

Blum and Roli give the general view: every component of a metaheuristic pushes the search toward one aim or the other. Moves guided by the objective intensify; random moves and moves guided by memory away from visited regions diversify. Most methods have a parameter that sets the balance, and many change it during the run.

| method | toward intensification | toward diversification |
|---|---|---|
| [simulated annealing](/simulated-annealing/) | low temperature | high temperature |
| [tabu search](/tabu-search/) | short tenure, restarts from elite solutions | long tenure, frequency penalties |
| [iterated local search](/iterated-local-search/) | small kicks, accept only better | large kicks, accept always |
| [GRASP](/grasp/) | small $\alpha$, [path relinking](/path-relinking/) | large $\alpha$ |
| [variable neighborhood search](/variable-neighborhood-search/) | small shaking index $k$ | large $k$ |
| [late acceptance hill climbing](/late-acceptance-hill-climbing/) | short history length $L$ | long $L$ |
| [guided local search](/guided-local-search/) | the descent on the augmented objective | penalties on features of local optima |
| [scatter search](/scatter-search/) | the $b_1$ best members | the $b_2$ most diverse members |
| [genetic algorithm](/genetic-algorithm/) | strong selection | [mutation](/mutation/), large populations |

## Examples

The pages of this section show the balance in measured or exact numbers. Each is for one instance.

- **GRASP, exact.** On the set cover example of the GRASP page, the probability that one iteration ends at the optimum is 0 for $\alpha = 0$, $0.30$ for $\alpha = 1/4$, $0.465$ for $\alpha = 1/2$, $0.48$ for $\alpha = 3/4$ and $0.42$ for $\alpha = 1$. Pure greed (no diversification) never succeeds; pure randomness does worse than a middle value.
- **Tabu search, measured.** On 200 random knapsack instances of 12 items (Python `random.Random(2026)`, from the empty knapsack, 100 iterations each), the optimum was reached in 73 instances by hill climbing alone, and by tabu search in 75, 130, 157 and 146 instances with tenure 0, 1, 3 and 5. A tenure of 0 gives no diversification; the largest tenure tried was past the best value on this set.
- **Late acceptance, measured.** On the 10-city instance of the late acceptance page (optimum 231), 30 runs of 2000 iterations for each history length $L$, with seeds 0 to 29, reached the optimum 21 times for $L = 1$, 25 times for $L = 10$ and 30 times for $L = 50$, and accepted on average 0, 29 and 158 worse moves per run. A longer history accepts more worse moves, which diversifies.
- **Scatter search, measured.** On the knapsack example of the scatter search page, with seeds 0 to 99, a reference set of 2 best and 2 diverse solutions found the optimum in 36 runs, and a set of the 4 best solutions in 33; all 33 were runs in which the optimum was already in the first reference set.

## Where it is used

The two terms are part of the design vocabulary of every metaheuristic. They are used to explain why a method works, to set parameters, and to build adaptive methods that change the balance during a run, such as reactive tabu search, which lengthens the tenure when solutions repeat, and reactive GRASP, which shifts the probability of each value of $\alpha$ toward the values that gave good results. In population methods the same tension appears as the risk of [premature convergence](/premature-convergence/), when the population loses its diversity too early.

## References
