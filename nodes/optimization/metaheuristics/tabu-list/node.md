---
tag: XZC2AW
kind: concept
slug: tabu-list
name: Tabu list
aliases:
- tabu memory
- short-term memory
- recency-based memory
area: optimization/metaheuristics
level: core
summary: A short memory of recent moves that tabu search forbids reversing for a set number of steps.
prereqs: [tabu-search, neighborhood-structure, local-optimum]
see_also: [tabu-search, aspiration-criterion, intensification-and-diversification, guided-local-search, two-opt, knapsack-problem, quadratic-assignment-problem]
sources:
  - paper: doi:10.1287/ijoc.1.3.190
    title: Fred Glover, Tabu Search, Part I, ORSA Journal on Computing 1(3), 1989
    locator: pp. 190 to 206 (tabu restrictions, attributes of moves, tabu list size)
  - book: isbn:9780792381877
    title: Fred Glover and Manuel Laguna, Tabu Search, Kluwer Academic Publishers, 1997
    locator: the chapters on short-term memory (recency-based memory, tabu tenure, data structures)
  - book: isbn:9783319910857
    title: Michel Gendreau and Jean-Yves Potvin (editors), Handbook of Metaheuristics, third edition, Springer, 2019
    locator: Chapter 2, Tabu Search, by Michel Gendreau and Jean-Yves Potvin, from p. 37 (tabu lists, tabu tenure)
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Section 2.2, 'Simple' SLS Methods, from p. 71 (tabu attributes and tabu tenure)
  - paper: "Éric Taillard, Robust taboo search for the quadratic assignment problem, Parallel Computing 17, 1991"
    locator: the whole paper (tabu attributes for QAP swaps, a random tenure)
  - paper: "Roberto Battiti and Giampietro Tecchiolli, The reactive tabu search, ORSA Journal on Computing 6(2), 1994"
    locator: the whole paper (a tenure that adapts when solutions repeat)
---

A tabu list is the short-term memory of [tabu search](/tabu-search/). It holds facts about the last few moves, and a move that would bring one of these facts back is *tabu*: the search may not make it, unless an [aspiration criterion](/aspiration-criterion/) allows it. The number of iterations that an entry stays in the list is the *tabu tenure*. The list exists to stop the search from going straight back into the [local optimum](/local-optimum/) it has just left.

## In plain words

When you walk out of a hollow, the easiest next step is often the step back into it. A tabu list is a note of your last few steps, with the rule "do not undo these yet". After a few more steps the oldest note drops off and that step is allowed again.

The note does not have to hold whole places. Often it holds just one fact about a step, such as "I took item 3 out of the bag", and the rule is then "do not put item 3 back for a while". This is cheap to store and to check. It also forbids more than it needs to, because it bans all steps that put item 3 back, not only the one step that undoes the last move.

## The idea

**What the list stores.** Each move has one or more *attributes*. The list stores attributes, and a move is tabu if it has an attribute in the list. There are three common choices.

- **Whole solutions.** The list holds the last $t$ solutions visited. A move is tabu if it leads to one of them. This forbids exactly the revisits and nothing more, but each test compares solutions, so it is used with hashing.
- **Reverse moves.** The list holds the moves made, and the reverse of each one is tabu.
- **Attributes of moves.** The list holds a feature of each move, such as the index of a flipped bit or an edge that a tour lost. This is the most common choice. It is cheap, and it can forbid solutions that were never visited, which is why aspiration criteria exist.

**Tenure.** The tenure $t$ is the number of iterations for which an attribute stays tabu. A fixed $t$ is the simplest rule. Taillard drew $t$ at random from an interval at each iteration. Battiti and Tecchiolli's reactive tabu search makes $t$ larger when solutions repeat and smaller when they do not. A short tenure lets the search cycle. A long tenure forbids so much that good moves are blocked, and in a small neighborhood it can leave no admissible move at all.

**Data structures.** A list of the last $t$ attributes, oldest first, gives a membership test in time $O(t)$. The usual implementation stores, for each attribute $a$, the last iteration $u(a)$ at which $a$ is still tabu. After a move with attribute $a$ at iteration $k$, set $u(a) \leftarrow k + t$. At iteration $k'$ a move with attribute $a$ is tabu if $k' \le u(a)$. The test costs $O(1)$, and the tenure can differ from move to move.

**What it guarantees.** Take bit strings with single-bit flips, let the attribute of a flip be the index of the bit, and let the tabu list hold the attributes of the last $t$ moves, with aspiration by objective. Then the search never comes back to a solution in $t + 1$ moves or fewer. Proof: suppose $x_j = x_k$ with $j < k \le j + t + 1$. The moves $j + 1, \ldots, k$ flip each bit an even number of times. So the bit $i$ flipped at move $k$ was also flipped at some earlier move $p$ with $j < p < k$, and $k - p \le t$. So bit $i$ was in the list at move $k$, and move $k$ was tabu. It was also not aspirated, because it led to $x_k = x_j$, and a visited solution is never better than the best solution seen. This is a contradiction. If no move between the two visits is aspirated, the same argument applied to the first $t + 1$ moves after $x_j$ shows that they flip $t + 1$ different bits, each of which must be flipped back, so a return takes at least $2(t + 1)$ moves. On 3000 random knapsack instances with 2 to 8 items (seed 1 of Python `random.Random`, 40 iterations each), the shortest return we saw for each tenure $t$ from 0 to 7 was exactly $2(t + 1)$. The bound says nothing about longer cycles: a tabu list of attributes does not prevent them.

## Examples

**Knapsack flips.** In the example of the [tabu search](/tabu-search/) page, a move adds or removes one item, and the attribute is the item index. With tenure 3, after the moves "add 2", "add 0", "add 1", "add 4", the list is 0, 1, 4: item 2 has dropped off. The full knapsack 111010 then has four moves, all removals, and the moves on items 0, 1 and 4 are tabu, so the search must remove item 2. With tenure 4 the list is 2, 0, 1, 4, every move is tabu, no aspiration applies, and the search has to stop.

| tenure | what happens on the example |
|---|---|
| 0 | the search moves between 111000 and 111010 for ever |
| 1 or 2 | the search leaves the local optimum but ends with value 32 |
| 3 | the search reaches the optimum, value 33, at step 10 |
| 4 or more | after step 4 every move is tabu, and the search stops |

**Tours.** In a [2-opt](/two-opt/) search on the [traveling salesman problem](/traveling-salesman-problem/), a move removes two edges and adds two others. A common attribute is the removed edges: adding one of them back is tabu for $t$ iterations. Another choice makes the added edges tabu to remove.

**Assignment.** In the [quadratic assignment problem](/quadratic-assignment-problem/), a move swaps the locations of two facilities. Taillard's robust tabu search makes it tabu to put a facility back on a location it left during the last $t$ iterations, with $t$ drawn at random from an interval.

**A non-example.** A list of the last $t$ objective values, used to accept or reject a move, is not a tabu list. [Late acceptance hill climbing](/late-acceptance-hill-climbing/) keeps such a list, and it forbids no moves; it only changes the test for accepting one.

## Where it is used

Every [tabu search](/tabu-search/) has a tabu list, and the choice of attributes and tenure is the main design decision. Long-term memories, such as counts of how often each attribute was used, extend the same idea from recency to frequency and drive [intensification and diversification](/intensification-and-diversification/). [Guided local search](/guided-local-search/) uses a related memory: it does not forbid features of solutions, it adds a penalty to them.

## References
