---
tag: 8BYDFQ
kind: algorithm
slug: parallel-alpha-beta
name: Parallel alpha-beta search
area: games-and-search/game-tree-search
level: research
summary: Alpha-beta parallelized across processors by searching eldest children first, then the rest in parallel.
solves: [game-tree-evaluation]
model: word-ram
complexity:
  vars: {b: the branching factor, d: the depth in plies, P: the number of processors}
  time: {worst: O(b^d)}
  space: {extra: O(P b d)}
properties: {deterministic: false, recursive: true}
prereqs: [alpha-beta-pruning, knuth-moore-theorem, move-ordering]
see_also: [young-brothers-wait, transposition-table, principal-variation-search, iterative-deepening-search, work-stealing, speedup, amdahls-law, monte-carlo-tree-search]
sources:
  - paper: doi:10.1016/0004-3702(75)90019-3
    title: Donald E. Knuth and Ronald W. Moore, An analysis of alpha-beta pruning, Artificial Intelligence 6(4) (1975)
    locator: pp. 293 to 326 (the minimal tree and its nodes of types 1, 2 and 3, the PV, CUT and ALL nodes of later papers)
  - paper: "Gérard M. Baudet, The Design and Analysis of Algorithms for Asynchronous Multiprocessors, PhD thesis, Carnegie-Mellon University, report CMU-CS-78-116 (1978)"
    locator: the part on the parallel search of game trees
  - paper: doi:10.1016/0004-3702(82)90022-4
    title: Raphael A. Finkel and John P. Fishburn, Parallelism in alpha-beta search, Artificial Intelligence 19(1) (1982)
    locator: pp. 89 to 106 (the tree-splitting algorithm on a tree of processors, and its speedup on best-case and worst-case trees)
  - paper: doi:10.1145/356893.356895
    title: T. Anthony Marsland and Murray S. Campbell, Parallel search of strongly ordered game trees, ACM Computing Surveys 14(4) (1982)
    locator: pp. 533 to 551 (the survey of sequential and parallel alpha-beta, and the principal variation splitting method)
  - paper: doi:10.1109/tpami.1985.4767683
    title: T. Anthony Marsland and Fred Popowich, Parallel game-tree search, IEEE Transactions on Pattern Analysis and Machine Intelligence 7(4) (1985)
    locator: pp. 442 to 452 (experiments with principal variation splitting and its refinements)
  - paper: "Rainer Feldmann, Burkhard Monien, Peter Mysliwietz and Oliver Vornberger, Distributed game-tree search, ICCA Journal 12(2) (1989)"
    locator: pp. 65 to 73 (the distributed alpha-beta search of the Paderborn group, in which a node is split only after its first child is searched)
  - paper: doi:10.3233/ICG-1997-20102
    title: Robert M. Hyatt, The dynamic tree-splitting parallel search algorithm, ICCA Journal 20(1) (1997)
    locator: pp. 3 to 19 (DTS, which lets an idle processor choose a split point anywhere in the tree, as used in Cray Blitz)
  - paper: "Jean-Christophe Weill, The ABDADA distributed minimax-search algorithm, ICCA Journal 19(1) (1996)"
    locator: pp. 3 to 16 (the search in which all processors share a transposition table that marks the nodes being searched, so that other processors defer them)
---

Parallel alpha-beta search runs the [alpha-beta](/alpha-beta-pruning/) search of a game tree on several processors at once. The problem is that alpha-beta is sequential by nature: it saves work because the value of the first children narrows the window for the later ones, and a later child that is searched before the window is known costs more than in the sequential search. So every parallel version trades *search overhead*, the extra nodes, against idle processors. The main family, from principal variation splitting to the *Young Brothers Wait* rule, searches the first child of a node alone and only then gives the other children to other processors. The *lazy SMP* method of modern chess programs takes the other road: all threads search the same root and share a [transposition table](/transposition-table/), and the table spreads the work. The search is correct when every child result is combined as in sequential fail-soft alpha-beta; its speed depends on the tree, the move order and the machine.

## In plain words

A chess program wants to use many processor cores. The easy idea is to give each core one move at the root. But alpha-beta is fast because its first good move tells it to stop looking at bad moves early. If all moves start at once, no core knows yet what is good, and each one does much more work.

The usual fix is to wait a little. At each position, one core first looks at the most promising move alone. When that is done, the program knows a good score, and the other moves are shared out to the idle cores, each with that score as its bar to beat. If one of them finds a move so good that the position is decided, the others stop.

Many chess engines today use another fix: all cores search the same position and share one big memory of results.

## The problem

The input is a game tree, a depth $d$, an evaluation function, and $P$ processors. The output is the negamax value of the root in the tree cut at depth $d$, the same value that sequential alpha-beta returns. This is the [game tree evaluation](/game-tree-evaluation/) problem. The aim is a small time on $P$ processors. The measures are the *speedup* $T_1 / T_P$, where $T_1$ is the time of the best sequential search, and the *search overhead* $N_P / N_1$, the ratio of the nodes visited by all processors to the nodes of the sequential search.

## The algorithm

The pseudocode is the Young Brothers Wait form, with fail-soft negamax values for the side to move.

```pseudo id=main
PARALLEL-AB(n, d, α, β)
L1  if n is terminal or d = 0 then return EVALUATE(n)
L2  m ← −∞
L3  c1 ← the first child of n in the move order       ▷ the eldest brother
L4  m ← −PARALLEL-AB(c1, d − 1, −β, −α)               ▷ searched alone
L5  if m ≥ β then return m                            ▷ a cutoff: no brother is started
L6  for each other child c of n, in parallel do        ▷ the young brothers
L7      a ← max(m, α)                                  ▷ read when the work on c starts
L8      t ← −PARALLEL-AB(c, d − 1, −β, −a)
L9      m ← max(m, t)                                  ▷ in the order the results arrive
L10     if m ≥ β then cancel the other brothers and return m
L11 return m
```

Lines L3 to L5 are the wait. If the move order is good, the eldest brother is the best move, and at a node that will be cut off (a CUT node in the terms of [Knuth and Moore](/knuth-moore-theorem/)) the cutoff comes from it, so no work is wasted on its brothers. At a node where every move fails low (an ALL node), all brothers must be searched anyway, and they can run in parallel with no overhead. Line L7 reads the window when the work starts, not when it is offered, so a brother that starts late uses a better bound. Line L10 stops the brothers that are still running when a cutoff is found. Their work up to then is search overhead.

The tests run this pseudocode on a simulated machine: each node visit costs one time unit, idle processors take the newest ready task from a stack, and nodes with depth less than 2 are searched inside one task. The simulator is deterministic, so the counts can be repeated.

## Example

The tests use 100 lazy random game trees from the seeds 50000 to 50099 (Python's `random.Random`, seeded per node), with branching factor 4 and height 6. A move changes the score by $-9$ to $+9$, and the moves are ordered by their static score. Sequential alpha-beta to depth 6 visits 38,839 nodes in all. Time steps are counted on the simulated machine.

| processors $P$ | nodes visited | search overhead | time steps | speedup |
| --- | --- | --- | --- | --- |
| 1 | 38,839 | 1.000 | 38,839 | 1.00 |
| 2 | 42,250 | 1.088 | 23,288 | 1.67 |
| 4 | 44,381 | 1.143 | 13,972 | 2.78 |
| 8 | 44,951 | 1.157 | 10,370 | 3.75 |

The root value was the same as that of sequential alpha-beta in every case. With one processor, the simulated search is exactly sequential alpha-beta. With more processors the overhead grows slowly, but the speedup stays well below $P$, because the eldest brothers are searched alone, and on a tree of depth 6 that is a long sequential chain. Without the wait for the eldest brother, the same trees need 107,363 nodes on 4 processors, an overhead of 2.76; the [Young Brothers Wait](/young-brothers-wait/) page gives the full comparison. These numbers are for a small simulated instance. They say nothing about a real program on a real machine.

## Correctness

The [proof](proofs/correctness/) shows that each call returns a fail-soft answer for the value of its node, whatever the number of processors and whatever the order in which the results of the brothers arrive.

- **The window of a brother.** A brother reads $\max(m, \alpha)$ when it starts. This bound is at most the bound that the node has later, so the brother's fail-soft answer is valid for the node's final window too.
- **The maximum in any order.** A maximum does not depend on the order of its terms. A result that is only a bound is at most the bound of the brother, and a result that raises $m$ above every earlier bound is exact.
- **A cutoff.** If a result reaches $\beta$, it is a lower bound on the value of the node, so cancelling the others is safe.

The tests check the root value against sequential alpha-beta on 500 random trees with branching factors 2 to 4, heights 1 to 5, $P \in \{1, 2, 4, 8\}$, with and without the wait for the eldest, and with three thresholds for the split depth.

## Complexity

**Work.** The search visits $N_P$ nodes in all, at most the $b^d$ leaves and inner nodes of the full tree. It is usually more than the $N_1$ nodes of the sequential search with the same move order, but not always: when the order is bad, a brother that is searched early can give a better bound than the sequential search has at that point, and then $N_P$ can be less than $N_1$.

**Time.** In each time step a processor visits at most one node, so $T_P \ge N_P / P$, and the speedup is at most $P \cdot N_1 / N_P$. On a tree of depth $d$, the chain of eldest brothers from the root to a leaf is searched in order, which adds about $d$ steps at each level that cannot be shared. Finkel and Fishburn (1982) analyse their tree-splitting algorithm on best-case and worst-case trees.

**Space.** Each processor keeps one path of at most $d$ nodes, with a move list per node, so $O(P b d)$ in all, plus the shared tables and the queues of the scheduler.

**Overheads that the simulation does not model.** A real machine also pays for the time to hand work to another processor (communication), for the time a processor is idle (synchronization), and for the loss of locality in the caches. Programs keep the split depth high enough that a task is large compared with the cost of handing it out.

## Properties

- **Same value, not the same nodes.** The root value is the sequential value, but the visited nodes and their number depend on the timing. A real parallel search is not deterministic, and its node counts change from run to run.
- **Best move.** Two moves with the same value can come out in a different order, so the best move that a program reports can differ between runs.
- **The order matters more than in the sequential search.** A wrong eldest brother at a CUT node means that all brothers are searched in parallel with a bad bound.
- **Transposition tables.** A shared table makes the results of one processor visible to the others. It also makes the node counts and the move order depend on the timing.

## Variants and improvements

- **Principal variation splitting (PV split).** Marsland and Campbell (1982) split the work only at the nodes of the [principal variation](/principal-variation/): the first child is searched down the PV, and then the other children of each PV node are searched in parallel. Marsland and Popowich (1985) report experiments with it.
- **Tree splitting.** Finkel and Fishburn (1982) arrange the processors as a tree, and each processor splits its subtree among its children processors.
- **Young Brothers Wait (YBW).** The Paderborn group of Feldmann, Monien, Mysliwietz and Vornberger (1989) splits any node, but only after its first child is searched, as in the pseudocode above. See [Young Brothers Wait](/young-brothers-wait/).
- **Dynamic tree splitting (DTS).** Hyatt (1997) lets an idle processor look at the trees of the busy processors and choose a split point anywhere, which needs the search to be written without recursion. It was used in Cray Blitz.
- **ABDADA.** Weill (1996) lets all processors search the same tree with a shared transposition table, which marks the nodes that some processor is searching. Another processor that reaches such a node defers it and comes back to it later.
- **Lazy SMP.** All threads run the full sequential search from the same root and share only the transposition table; some programs start the threads at different depths or with a different move order. There is no explicit split. The threads speed each other up through the table entries they leave. Lazy SMP is engine practice: it is used in many strong open-source chess programs, but it has no founding paper that we know of, and its history is folklore.
- **Parallel aspiration search.** Baudet (1978) studied the parallel search of game trees on asynchronous multiprocessors. One method in this family gives each processor a different part of the window of the root.
- **Parallel MCTS.** [Monte Carlo tree search](/monte-carlo-tree-search/) is easier to run in parallel, by root, leaf or tree parallelism, because it has no window to wait for.

## When to use it

Use a parallel search when a game program has a fixed time per move and more than one core. For a few cores, lazy SMP is the simplest choice, and it fits a program that already has a shared transposition table. For many processors or a cluster, a splitting method with the Young Brothers Wait rule, such as the one of the Paderborn group or DTS, gives more control over the overhead. Do not expect a speedup close to $P$; the overhead grows with $P$, and the gain depends on the program and the machine.

## Pitfalls

- **Splitting before the eldest brother is known.** This is the error that the wait rule avoids. The naive search, with all children at once, can do several times the sequential work.
- **Stale windows.** A brother that started with a weak bound does not see a better bound found later, unless the program sends it. The simulation here does not send it, so its overhead is an upper estimate for this model.
- **Races on shared tables.** A transposition table entry can be read while another thread writes it. Programs check the entry with a key stored with the data, or use the XOR trick of storing the key XOR the data.
- **Non-determinism in tests.** A parallel program does not give the same node count twice. Test the value against a sequential search, not the node count.
- **Claims of speedup.** A speedup measured for one program, one machine and one set of positions is not a property of the algorithm. Report the instance, the machine and the method.

## Implementations

## History

Knuth and Moore (1975) gave the node types of the minimal alpha-beta tree that later parallel methods use to decide where to split. Baudet (1978) studied game-tree search on asynchronous multiprocessors. Finkel and Fishburn (1982) gave tree splitting, and Marsland and Campbell (1982) gave principal variation splitting, which Marsland and Popowich (1985) tested further. The Paderborn group of Feldmann, Monien, Mysliwietz and Vornberger (1989) published distributed game-tree search with the rule that a node is split only after its first child is searched, the Young Brothers Wait rule. Hyatt published dynamic tree splitting, used in Cray Blitz, in the ICCA Journal in 1997. Weill (1996) gave ABDADA. Lazy SMP spread among chess programs much later through program practice, and we know of no paper that introduced it.

## References
