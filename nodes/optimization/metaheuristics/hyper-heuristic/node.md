---
tag: TCERB7
kind: technique
slug: hyper-heuristic
name: Hyper-heuristic
aliases:
- heuristic selection
area: optimization/metaheuristics
level: research
summary: Search over heuristics or heuristic combinations rather than over direct solutions.
prereqs: [metaheuristic, local-search, neighborhood-structure]
see_also: [metaheuristic, late-acceptance-hill-climbing, variable-neighborhood-search, stochastic-local-search, no-free-lunch-theorem, two-opt, iterated-local-search, intensification-and-diversification]
sources:
  - paper: doi:10.1057/jors.2013.71
    title: Edmund K. Burke, Michel Gendreau, Matthew Hyde, Graham Kendall, Gabriela Ochoa, Ender Özcan and Rong Qu, Hyper-heuristics, a survey of the state of the art, Journal of the Operational Research Society 64(12), 2013
    locator: pp. 1695 to 1724 (definition, the classification into selection and generation methods, online and offline learning, early history)
  - book: isbn:9783319910857
    title: Michel Gendreau and Jean-Yves Potvin (editors), Handbook of Metaheuristics, third edition, Springer, 2019
    locator: Chapter 14, A Classification of Hyper-Heuristic Approaches, Revisited, by Edmund K. Burke, Matthew R. Hyde, Graham Kendall, Gabriela Ochoa, Ender Özcan and John R. Woodward, from p. 453
  - paper: "Peter Cowling, Graham Kendall and Eric Soubeiga, A hyperheuristic approach to scheduling a sales summit, in E. Burke and W. Erben (editors), Practice and Theory of Automated Timetabling III, Lecture Notes in Computer Science 2079, Springer, 2001"
    locator: pp. 176 to 190 (selection of low-level heuristics by a choice function, behind a domain barrier)
---

A hyper-heuristic is a method that searches in a space of heuristics instead of a space of solutions. A *selection* hyper-heuristic is given a set of simple low-level heuristics, such as different move operators, and at each step it chooses which one to apply, learning from how well each has worked. A *generation* hyper-heuristic builds new heuristics from parts, for example by genetic programming. The aim is a method that can be reused on new problems with little change: the hyper-heuristic sees only objective values and the names of the heuristics, not the problem itself. Burke, Kendall and coworkers developed the field from about 2000, and Cowling, Kendall and Soubeiga used the term for combinatorial optimization in 2001. A hyper-heuristic has the same lack of guarantees as the heuristics it controls.

## In plain words

Suppose you have a toolbox of small tricks for improving a timetable or a route: swap two items, move one item, reverse a part. Some tricks work well on some problems and badly on others, and the best trick may change during the search.

A hyper-heuristic is a manager that does not know the problem. It only picks a trick, sees whether the result got better or worse, and keeps a score for each trick. It uses good tricks more often, but still tries the others now and then. A second rule decides whether to keep each new result.

## When it applies

Use a hyper-heuristic when:

- there are several reasonable low-level heuristics and it is not clear which is best, or the best one changes between instances or during a run;
- the same code must handle many problems or many kinds of instances, and tuning a method for each is too expensive;
- the low-level heuristics are cheap to apply and their effect is measured by the objective alone.

It is less useful when one well-tuned method for one problem is known to work, since the extra layer then costs time and adds parameters.

## The template

```pseudo id=main
SELECTION-HYPER-HEURISTIC(x0, f, H, K)
L1  x ← x0;  b ← x0;  score_h ← 0 for every h in H
L2  for k ← 1 to K do
L3      h ← SELECT(H, score)            ▷ uniform, greedy, choice function or learned
L4      y ← h(x)
L5      update score_h from f(x), f(y) and the time used
L6      if ACCEPT(x, y) then x ← y     ▷ improving only, all moves, late acceptance
L7      if f(x) < f(b) then b ← x
L8  return b
```

The *domain barrier* separates the two layers. Below it are the solutions, the objective $f$ and the low-level heuristics $H$, all specific to the problem. Above it are SELECT, the scores and ACCEPT, which see only the values of $f$, the index of each heuristic and perhaps the time used. So the upper layer can be reused on a new problem by giving it a new set $H$.

Burke and coworkers classify hyper-heuristics in two ways. By the nature of the search space: *selection* of existing heuristics, as in the template, or *generation* of new heuristics from components. By the source of feedback: *online* learning during the run, as the scores above, *offline* learning on training instances before the run, or no learning, as uniform random selection. The low-level heuristics can be *constructive*, adding one part to a partial solution, or *perturbative*, changing a complete solution.

## Classic examples

- **Choice function.** Cowling, Kendall and Soubeiga score each low-level heuristic by its recent improvement per unit of time, by how well it performs right after the heuristic used before it, and by the time since it was last used, and choose the heuristic of highest score.
- **Reinforcement learning selection.** Keep a utility for each heuristic, raise it after an improvement and lower it after a failure, and choose by the utilities, with some random choices.
- **Acceptance rules.** The move acceptance of line L6 is often a rule from a single-solution method: only improving moves, improving or equal moves, [simulated annealing](/simulated-annealing/) or [late acceptance](/late-acceptance-hill-climbing/).
- **Generation by genetic programming.** Evolve an expression, such as a priority rule for packing items into bins or for dispatching jobs, on training instances, then use the best rule as a constructive heuristic on new instances.

**A measured example.** On one 40-city instance (integer coordinates in $[0, 1000]$ from Python `random.Random(7)`), four perturbative heuristics were used: a random [2-opt](/two-opt/) move, a random swap of two cities, a random move of one city and a random double-bridge move. The start was the tour $0, 1, \ldots, 39$, the acceptance rule kept moves that do not make the tour longer, and each run had 20000 steps; 10 runs used seeds 0 to 9. With uniform random selection, the four heuristics gave on average 41, 22, 31 and 6 improving moves per run, so their usefulness differed a great deal. An adaptive rule, which kept $s_h \leftarrow 0.9 \, s_h + 0.1 \cdot [\text{the move improved}]$ and chose the highest score with probability 0.9 and a uniform heuristic otherwise, moved the calls toward 2-opt and the single-city move (on average 6850 and 6599 calls, against 4290 and 2259 for the other two), but its mean best tour length was 5395, against 5336 for uniform selection. Learning which heuristic to use is not by itself a gain; on this instance it was not.

## Variations

- **Selection rules.** Uniform random, greedy (try all heuristics and take the best result), choice functions, reinforcement learning, and multi-armed bandit rules.
- **Acceptance rules.** Deterministic rules (improving only, all moves) or rules with memory or randomness (late acceptance, simulated annealing, great deluge).
- **Sequences of heuristics.** Choose a sequence, not a single heuristic, as in [variable neighborhood search](/variable-neighborhood-search/), which can be seen as a fixed rule for changing between neighborhoods.
- **Automated design.** Offline methods that configure or assemble a whole metaheuristic from parts, using training instances.
- **Cross-domain benchmarks.** Test frameworks give the same hyper-heuristic several problem domains, each with its own low-level heuristics behind the domain barrier.

## Pitfalls

- **Claiming generality from a few problems.** By the [no free lunch theorem](/no-free-lunch-theorem/), no method is better than another on average over all problems. A hyper-heuristic is general only over the problems and heuristics it was tested on.
- **Weak low-level heuristics.** The upper layer cannot create quality that the low-level heuristics lack. Most of the work is still in designing good moves.
- **Too much exploitation.** A rule that always picks the current best heuristic stops trying the others and misses a change in which one works best. Keep some random choices.
- **Counting time unfairly.** Heuristics differ in cost. Compare them per unit of time, not per call.
- **Learning noise.** In the example above, the adaptive rule spent many calls on what it learned, and it still did no better. Report measured gains with instances, seeds and the number of runs.

## Exercises

1. Show that a selection hyper-heuristic with uniform random selection over perturbative heuristics $h_1, \ldots, h_k$, each picking a random neighbor in its own neighborhood $N_i$, and an acceptance rule that accepts only improving moves, is a stochastic local search in the union neighborhood $N_1 \cup \cdots \cup N_k$.
2. Suppose that at the current solution, heuristic $h_i$ gives an improvement with probability $p_i$, independently at each call. Show that uniform random selection gives an improvement with probability $(p_1 + \cdots + p_k)/k$ per step, and that the best fixed choice gives $\max_i p_i$. When does learning which heuristic to use pay most?
3. List what a selection hyper-heuristic must be given to work on 0-1 knapsack and on the TSP, and check that the upper layer of the template needs no other knowledge of either problem.

## References
