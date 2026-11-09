---
tag: F6JEQ4
kind: concept
slug: aspiration-criterion
name: Aspiration criterion
aliases:
- aspiration level
- aspiration by objective
area: optimization/metaheuristics
level: advanced
summary: A rule in tabu search that overrides tabu status when a move yields a solution better than any found so far.
prereqs: [tabu-search, tabu-list]
see_also: [tabu-search, tabu-list, intensification-and-diversification, hill-climbing, knapsack-problem]
sources:
  - paper: doi:10.1287/ijoc.1.3.190
    title: Fred Glover, Tabu Search, Part I, ORSA Journal on Computing 1(3), 1989
    locator: pp. 190 to 206 (aspiration criteria and aspiration levels)
  - book: isbn:9780792381877
    title: Fred Glover and Manuel Laguna, Tabu Search, Kluwer Academic Publishers, 1997
    locator: the chapters on short-term memory (aspiration by default, by objective, by search direction and by influence)
  - book: isbn:9783319910857
    title: Michel Gendreau and Jean-Yves Potvin (editors), Handbook of Metaheuristics, third edition, Springer, 2019
    locator: Chapter 2, Tabu Search, by Michel Gendreau and Jean-Yves Potvin, from p. 37 (aspiration criteria)
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Section 2.2, 'Simple' SLS Methods, from p. 71 (the aspiration criterion of tabu search)
---

An aspiration criterion is a rule in [tabu search](/tabu-search/) that allows a move although it is tabu. The [tabu list](/tabu-list/) usually stores attributes of moves, not whole solutions, so it can forbid a move to a solution that the search has never seen, and that solution can be very good. The aspiration criterion repairs this. The most common one, *aspiration by objective*, allows a tabu move when it leads to a solution better than the best one found so far. Glover set out aspiration criteria in Part I of his paper "Tabu Search" (1989).

## In plain words

A tabu list is a blunt rule: "do not put item 3 back in the bag for a while". Most of the time this keeps the search from going back where it was. But sometimes putting item 3 back gives a bag better than any bag seen so far. Such a bag cannot be one we have seen, so there is no risk of going back, and refusing it would be silly.

An aspiration criterion is the exception to the rule. The usual one says: a forbidden step is allowed if it gives the best result so far. Other versions allow a forbidden step when every step is forbidden, or when it is the best step in some part of the search.

## The idea

At each iteration tabu search scans the moves of the current solution $x$. A move to $y$ is *admissible* if it is not tabu, or if it is tabu and satisfies the aspiration criterion. The search makes the best admissible move. Let $b$ be the best solution seen so far.

**Aspiration by objective.** A tabu move to $y$ is admissible if $f(y) < f(b)$. Two facts follow at once.

- *It never allows a revisit.* Each visited solution $z$ has $f(z) \ge f(b)$, since $b$ is the best of them. So a move that aspiration allows always leads to a solution not seen before. This is why aspiration by objective does not undo the work of the tabu list.
- *It keeps the descent of hill climbing.* While the current solution is the best so far and has an improving neighbor, every improving neighbor beats $f(b)$, so none of them is blocked. Tabu search then makes the same moves as best-improvement [hill climbing](/hill-climbing/), and it never ends with a worse solution than that descent. The proof is on the [tabu search](/tabu-search/) page.

The strict inequality matters. With $f(y) \le f(b)$, a tabu move back to $b$ itself would be allowed, and the search could cycle.

**Aspiration by default.** If every move is tabu and none is aspirated, make the move that is "least tabu", for example the one whose attribute leaves the list soonest. Without this rule the search has to stop.

**Aspiration by objective in a region.** Keep a best value for each region of the search space, such as each value of one key variable, and allow a tabu move that improves the best value of its region. This is a weaker test than the global one, so it allows more moves.

**Aspiration by search direction and by influence.** Glover and Laguna describe further rules: allow a tabu move that continues an improving direction, or a move of high influence, one that changes the structure of the solution a lot. These rules are used less often.

## Examples

**The knapsack example.** On the [tabu search](/tabu-search/) page, a 0-1 knapsack with six items is solved with flip moves, the item index as attribute and tenure 3. At step 10 the best value seen is 32 and the current knapsack is 010101 with value 24. Adding item 0 is tabu, because item 0 was removed at step 7. But it gives value 33, more than 32. Aspiration by objective allows the move, and 33 is the optimum. Without aspiration the search makes a different move at step 10 and does not reach 33 in that step.

**When every move is tabu.** On the same example with tenure 4, the full knapsack 111010 has four moves, all removals, and items 0, 1, 2 and 4 are all in the list. No removal gives a value above 32, so aspiration by objective allows none of them. Aspiration by default would remove item 2, whose attribute is the oldest in the list. Without it the search stops.

**Not an aspiration criterion.** The acceptance test of [simulated annealing](/simulated-annealing/), which sometimes accepts a worse neighbor, is not an aspiration criterion. It decides whether to accept a move, and there is no tabu status to override.

## Where it is used

Most implementations of [tabu search](/tabu-search/) use aspiration by objective, often together with aspiration by default. The choice interacts with the [tabu list](/tabu-list/): attributes that forbid many solutions need an aspiration rule more than lists of whole solutions do. Aspiration by region and by influence appear in tabu searches with long-term memory, where they help [intensification and diversification](/intensification-and-diversification/).

## References
