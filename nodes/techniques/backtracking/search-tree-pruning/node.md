---
tag: BZQ8BR
kind: concept
slug: search-tree-pruning
name: Search tree pruning
aliases:
- Pruning of the search tree
- cutting dead branches
- feasibility pruning
- pruning
- search-tree pruning
area: techniques/backtracking
level: intro
summary: Cutting off a subtree of the search as soon as it is proved to contain no valid solution.
prereqs: [state-space-tree, partial-solution]
see_also: [generic-backtracking-algorithm, fathoming-rule, bounding-function, dominance-pruning, alpha-beta-pruning, forward-checking, n-queens-problem]
sources:
  - paper: doi:10.1145/321296.321300
    title: Solomon W. Golomb and Leonard D. Baumert, Backtrack programming, Journal of the ACM 12(4), 1965
    locator: pp. 516 to 524
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2
    locator: Section 7.2.2, Backtrack programming
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 7 (bounding functions in backtracking) and Chapter 8 (branch-and-bound)
  - paper: doi:10.1145/322003.322010
    title: Toshihide Ibaraki, The power of dominance relations in branch-and-bound algorithms, Journal of the ACM 24(2), 1977
    locator: pp. 264 to 279
---

Search tree pruning is the step of a tree search that drops a node of the [state space tree](/state-space-tree/), together with its whole subtree, as soon as a test proves that the subtree contains no solution that the search still needs. It is what separates [backtracking](/generic-backtracking-algorithm/) and branch and bound from [brute-force search](/brute-force-search/): both walk the same tree, but a pruned search visits only a part of it. A pruning test must be *sound*, which means that it never cuts a subtree that holds a needed solution, and it should be cheap compared with the subtree that it saves.

## In plain words

A search tries many combinations of choices, and the choices form a tree. Often you can see early that a group of combinations is useless. If the first two queens on a chess board already attack each other, no way to place the other queens can help. So you skip every combination that starts with these two queens, all at once.

That skip is pruning. It needs a rule that tells you, from the first few choices only, that nothing good can follow. The rule must never be wrong in the bad direction: it may keep a useless group, but it must never throw away a group that holds an answer.

## The idea

Let $\mathcal{T}$ be the state space tree, and for a node $u$ let $\mathcal{L}(u)$ be the set of complete candidates (leaves) below $u$. Let $S$ be the set of solutions that the search must find. A pruning test is a predicate $\mathrm{cut}(u)$, computed from the [partial solution](/partial-solution/) at $u$ and from what the search knows so far. It is **sound** when

$$\mathrm{cut}(u) \implies \mathcal{L}(u) \cap S_{\text{needed}} = \emptyset,$$

where $S_{\text{needed}}$ depends on the task. A search that skips the subtree of each node where a sound test is true still finds every needed solution. Each subtree that holds a needed solution has no cut node on the path from the root to that solution, so the search reaches it.

The kinds of pruning differ in what "needed" means and in what the test uses.

1. **Feasibility pruning.** The task is to find all solutions, so $S_{\text{needed}} = S$. The test uses only the partial solution: "no extension can satisfy the constraints". This is the test $\neg P_k$ of [backtracking](/generic-backtracking-algorithm/) and the consistency check of a [constraint satisfaction problem](/constraint-satisfaction-problem/). Stronger tests look ahead, as [forward checking](/forward-checking/) and [arc consistency](/arc-consistency/) do.
2. **Bound pruning.** The task is to find one optimal solution of a minimization problem. The test is $\mathrm{lb}(u) \ge U$, where the [bounding function](/bounding-function/) value $\mathrm{lb}(u)$ is at most the cost of each candidate below $u$ and $U$ is the cost of the [incumbent solution](/incumbent-solution/). It is sound because no candidate below $u$ costs less than $U$, and one solution of cost $U$ is already known. This is the [fathoming rule](/fathoming-rule/) of branch and bound. Its strength changes during the run, as $U$ decreases.
3. **Symmetry pruning.** See [symmetry breaking](/symmetry-breaking/). The task is to find the solutions up to a symmetry group $G$ of the problem. A test may cut $u$ when each solution below $u$ is the image under $G$ of a solution in a subtree that is kept. The solutions below $u$ are then still found, as images.
4. **Dominance pruning.** A test may cut $u$ when another node $v$ is known to have, for each completion of $u$, a completion at least as good. See [dominance pruning](/dominance-pruning/).
5. **Game-tree pruning.** [Alpha-beta pruning](/alpha-beta-pruning/) cuts the subtrees of a [game tree](/game-tree/) that cannot change the minimax value of the root. It is bound pruning with two bounds, one for each player.

**Cost.** Let $t_c$ be the cost of the test and $s(u)$ the cost of searching the subtree of $u$ without it. Pruning at $u$ saves $s(u) - t_c$ when the test cuts and costs $t_c$ when it does not. A test that is strong but expensive can make the search slower. The best test depends on how often it cuts high in the tree, where $s(u)$ is large.

**What pruning cannot do.** A sound test does not make an alive node a good node: a partial solution can pass each test and still have no solution below it. In the worst case a pruned search can still visit exponentially many nodes. Pruning changes the size of the visited tree, not the worst-case complexity class of an [NP-hard](/np-hard/) problem.

## Examples

### Eight queens

Place 8 queens on a chess board, one in each row, so that no two attack each other.

| test | nodes visited | solutions found |
|---|---|---|
| none, all $8^k$ prefixes | 19173961 | 92 (tested at the leaves only) |
| "the new queen attacks no earlier queen" | 2057 | 92 |
| the same, and the first queen in columns 1 to 4 | 1029 | 46, which give 92 by reflection |

The feasibility test cuts the tree from about $1.9 \times 10^{7}$ nodes to 2057. The third row adds symmetry pruning. The reflection $x \mapsto 9 - x$ of the columns maps solutions to solutions and maps a first queen in columns 1 to 4 to one in columns 5 to 8. Since 8 is even, no solution is its own reflection, so the 46 solutions found give the other 46 by reflection.

### Subset sum

Take the items $3, 5, 6, 7$ and the target 15, with $x_i \in \{0, 1\}$ decided for item $i$ at depth $i$. The full tree has 31 nodes.

- Test A: "the chosen sum is at most 15". Sound because the items are non-negative. The search visits 28 nodes.
- Tests A and B, where B is "the chosen sum plus the sum of the items not yet decided is at least 15". Sound because the largest reachable sum is the chosen sum plus all the remaining items. The search visits 11 nodes, and the only leaf it reaches is the solution $\{3, 5, 7\}$.

Test B is a bound test in disguise: it compares an upper bound on the reachable sum with the target.

### An unsound cut

For 0-1 knapsack, the rule "skip an item whose value per unit of weight is below the average ratio of the items" is not a sound test. Take capacity 10 and two items: (value 10, weight 1) with ratio 10, and (value 45, weight 9) with ratio 5. The average ratio is 7.5, so the rule skips the second item and the search returns 10. The optimum takes both items, with weight 10 and value 55. A rule that only feels plausible is a heuristic, not a pruning test.

### Knapsack with a bound

For the 0-1 knapsack instance with capacity 16, values $40, 30, 50, 10$ and weights $2, 5, 10, 5$, the full tree has 31 nodes and the capacity test alone keeps 26 of them. The bound test of [depth-first branch and bound](/depth-first-branch-and-bound/) cuts most of the rest; that page gives the trace.

## Where it is used

Feasibility pruning is the core of the [generic backtracking algorithm](/generic-backtracking-algorithm/), [chronological backtracking](/chronological-backtracking/) and [DPLL](/dpll/), and of puzzle solvers for the [n-queens problem](/n-queens-problem/), [sudoku](/sudoku/) and [exact cover](/exact-cover/). Bound pruning is the core of branch and bound, through the [fathoming rule](/fathoming-rule/), in [depth-first](/depth-first-branch-and-bound/) and [best-first](/best-first-branch-and-bound/) branch and bound and in [knapsack branch and bound](/knapsack-branch-and-bound/). [Dominance pruning](/dominance-pruning/) and symmetry pruning, such as [orbital branching](/orbital-branching/) in integer programming, are added on top. In game search, the same idea is [alpha-beta pruning](/alpha-beta-pruning/).

## References
