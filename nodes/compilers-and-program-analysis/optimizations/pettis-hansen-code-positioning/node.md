---
tag: YB331X
kind: algorithm
slug: pettis-hansen-code-positioning
name: Pettis-Hansen code positioning
aliases:
- profile-guided code layout
area: compilers-and-program-analysis/optimizations
level: advanced
summary: Orders basic blocks and procedures by greedily merging chains along the heaviest edges of the profile, to improve instruction cache use.
model: word-ram
complexity:
  vars: {V: the number of basic blocks of the procedure, E: the number of CFG edges with a profile weight, C: the number of chains left after merging}
  time: {worst: O(E log E + C E)}
  space: {extra: Θ(V + E)}
properties: {deterministic: true, recursive: false, online: false, exact: false}
prereqs: [control-flow-graph, basic-block, call-graph, profile-guided-optimization, greedy-algorithm]
see_also: [ball-larus-path-profiling, hamiltonian-path-problem, hamiltonian-cycle-np-completeness, traveling-salesman-problem, locality-of-reference, function-inlining, trace-scheduling, superblock-scheduling]
sources:
  - paper: doi:10.1145/93542.93550
    title: Karl Pettis and Robert C. Hansen, Profile guided code positioning, Proceedings of the ACM SIGPLAN 1990 Conference on Programming Language Design and Implementation (PLDI), 16-27
    locator: procedure positioning by the closest-is-best merging of the call graph, basic block positioning by bottom-up chain merging along the heaviest edges, and procedure splitting into hot and cold parts
  - paper: doi:10.1016/0020-0190(79)90023-1
    title: Ján Plesník, The NP-completeness of the Hamiltonian cycle problem in planar digraphs with degree bound two, Information Processing Letters 8(4), 1979, 199-201
    locator: the main theorem, used here for the hardness of layout with two-way branches
  - paper: doi:10.1109/CGO.2017.7863743
    title: Guilherme Ottoni and Bertrand Maher, Optimizing function placement for large-scale data-center applications, Proceedings of the 2017 IEEE/ACM International Symposium on Code Generation and Optimization (CGO), 233-244
    locator: the comparison with Pettis-Hansen procedure ordering and the call-chain clustering heuristic for large binaries
  - paper: doi:10.1109/TC.2020.2982888
    title: Andy Newell and Sergey Pupyrev, Improved basic block reordering, IEEE Transactions on Computers 69(12), 2020, 1784-1794
    locator: the extended TSP model of block layout, which also rewards short forward and backward jumps, and its heuristics
---

Pettis-Hansen code positioning puts the [basic blocks](/basic-block/) of each procedure, and the procedures of a program, in an order chosen from a profile. Inside a procedure it builds chains of blocks: it takes the [control-flow graph](/control-flow-graph/) edges from the most frequent to the least frequent, and joins two chains when the edge goes from the end of one to the start of the other. The frequent edges then become fall-throughs, which need no taken jump and keep the hot code dense in the instruction cache. Across procedures it does the same on the [call graph](/call-graph/), so that a caller and a callee that call each other often end up close in memory. Choosing the best layout is NP-hard, and the greedy merge is a fast approximation of it.

## In plain words

A program is stored in memory as one long line of code. When the processor runs one block and the next block it needs is right after it, it just keeps going. When the next block is somewhere else, it has to jump, and the code it fetched around the first block is partly wasted. A profile says which moves from block to block happen most. The method starts with every block on its own and then, from the most common move downwards, glues the two pieces together when one ends where the other begins. The busiest routes become straight lines of code. The same gluing on the procedures puts procedures that call each other often next to each other.

## The problem

The input is a CFG with blocks $b_1, \ldots, b_V$, where $b_1$ is the entry, and a weight $w(a, b) \ge 0$ for each edge, the number of times the profile run took it. A *layout* is an order of the blocks with the entry first. An edge $a \to b$ is a *fall-through* in the layout when $b$ comes right after $a$. The *fall-through weight* of a layout is the total weight of its fall-through edges. The goal is a layout with large fall-through weight.

The model is simple on purpose. It ignores the cost of a taken jump that depends on its distance, the cache line boundaries, and the size of each block. In the [toy IR](/three-address-code/) every block ends in an explicit `jump`, `br` or `ret`, so any order of the blocks with the entry first has the same meaning. In machine code, a `jump` to the next block is deleted, and a `br` gets its condition flipped when its first target is the next block.

**Legality.** Any layout is legal: moving blocks changes only addresses, and the control flow is given by the terminators. The entry must stay first in the toy IR, because the first block is where a run starts. **Profit.** Each fall-through edge saves a taken jump on each of its traversals, and chains of hot blocks fill fewer cache lines.

**Hardness.** Finding a layout of the largest fall-through weight is NP-hard, even with two-way branches only and all weights 1. Decision form: given $k$, is there a layout with fall-through weight at least $k$?

*Reduction.* Plesník showed that the Hamiltonian cycle problem stays NP-complete on digraphs where every node has in-degree and out-degree at most 2. Given such a digraph $G$ on $n$ nodes, pick a node $v$ and split it: $v_{\mathrm{out}}$ keeps the arcs out of $v$ and becomes the entry, and $v_{\mathrm{in}}$ keeps the arcs into $v$ and gets no successors (it ends in `ret`). Give every arc weight 1 and ask for $k = n$. The new graph has $n + 1$ blocks, so a layout has $n$ consecutive pairs, and its fall-through weight is $n$ exactly when every consecutive pair is an arc. Such a layout is a Hamiltonian path that starts at $v_{\mathrm{out}}$. It must end at $v_{\mathrm{in}}$, the only node with no successor, and so it is a Hamiltonian cycle of $G$ through $v$. Conversely, a Hamiltonian cycle of $G$, cut open at $v$, gives such a layout. Out-degrees stay at most 2, so every block ends in a `jump`, a `br` or a `ret`. If some block cannot be reached from the entry, $G$ has no Hamiltonian cycle, and that case is easy to detect. The construction is linear, so the decision problem is NP-hard. It is in NP, since a layout is a certificate checked in linear time. In this model, layout is the maximum-weight [Hamiltonian path](/hamiltonian-path-problem/) problem with a fixed start, a close relative of the [traveling salesman problem](/traveling-salesman-problem/).

## The algorithm

A chain is a list of blocks. `head(c)` and `tail(c)` are its first and last blocks.

```pseudo id=main
PETTIS-HANSEN-BLOCKS(blocks, w)
L1  make one chain [b] for every block b
L2  for each edge a -> b with w(a, b) > 0, by decreasing weight do
L3      if a = b, or b is the entry, or a and b are in the same chain then skip the edge
L4      if a = tail(chain(a)) and b = head(chain(b)) then
L5          append chain(b) to chain(a)
L6  placed <- [the chain whose head is the entry]
L7  while some chain is not placed do
L8      c <- the unplaced chain with the largest total weight of edges from placed blocks into c
L9      append c to placed
L10 return the blocks of placed, chain by chain
```

Lines L1 to L5 are the bottom-up chain building of Pettis and Hansen. Lines L6 to L9 put the chains in a sequence. Pettis and Hansen order chains with a precedence relation that tries to make conditional branches jump forward. The rule in L8 is a simpler version of the same idea, used by the implementation here: the next chain is the one the placed code jumps into most. Ties go to the earlier chain in the original order.

**Procedure positioning ("closest is best").** The call graph is made undirected: the weight of $\{f, g\}$ is the number of calls between $f$ and $g$ in either direction. Each procedure starts as its own group. Repeat: take the heaviest edge between two different groups (the weight between groups is the sum of the edges between them), and join the two groups into one list. Of the four ways to join (each group forwards or reversed), take the one where the two procedures of the heaviest single edge between the groups end up closest. The final groups give the order of the procedures in memory.

## Example

**A case where the greedy loses.** Blocks E (entry), A, B, X, D, C with the profile E$\to$A 19, A$\to$B 10, A$\to$D 9, D$\to$C 9, C$\to$B 9 and B$\to$X 19. A branches to B or D, and the D side joins B again through C.

| step | edge | weight | action | chains |
|---|---|---|---|---|
| 1 | E$\to$A | 19 | join | [E A], [B], [X], [D], [C] |
| 2 | B$\to$X | 19 | join | [E A], [B X], [D], [C] |
| 3 | A$\to$B | 10 | join | [E A B X], [D], [C] |
| 4 | A$\to$D | 9 | skip, A is not a tail | |
| 5 | D$\to$C | 9 | join | [E A B X], [D C] |
| 6 | C$\to$B | 9 | skip, B is not a head | |

The layout is E A B X D C, with fall-through weight $19 + 10 + 19 + 9 = 57$. Trying all 120 orders that start with E gives the best layout E A D C B X, with weight $19 + 9 + 9 + 9 + 19 = 65$. The greedy took A$\to$B (10) and so lost both A$\to$D and C$\to$B (18 together).

**A loop.** Blocks B0 (entry) to B4 with B0$\to$B1 1, B1$\to$B2 100, B1$\to$B4 1, B2$\to$B1 90, B2$\to$B3 10 and B3$\to$B1 10. B1 is the loop test, B2 the body, B3 a rare path in the body and B4 the exit. The merges are B1$\to$B2 (100), then B2$\to$B3 (10), then B0$\to$B1 (1). B2$\to$B1 and B3$\to$B1 close the loop and are skipped, and B1$\to$B4 is skipped because B1 is no longer a tail. The layout B0 B1 B2 B3 B4 has fall-through weight 111, which is also the best of all 24 orders. The back edge B2$\to$B1 (90) stays a taken jump: no layout can make both B1$\to$B2 and B2$\to$B1 fall through.

**Procedures.** Procedures main, parse, lex, eval, print, gc with calls parse-lex 500, parse-gc 60, eval-gc 40, eval-print 30, main-print 2, main-parse 1 and main-eval 1. The merges, heaviest first:

1. parse-lex 500: [parse lex].
2. parse-gc 60: joining [parse lex] and [gc] as [lex parse gc] puts parse and gc next to each other.
3. eval-gc 40: [eval gc parse lex].
4. eval-print 30: [lex parse gc eval print].
5. main: the group weight is $2 + 1 + 1 = 4$, and the heaviest single edge is main-print, so main goes next to print.

The final order is main, print, eval, gc, parse, lex. The 500 calls between parse and lex and the 60 between parse and gc cross a distance of one procedure.

## Correctness

The output is a layout: each block is in exactly one chain at all times, because L5 moves a whole chain into another and the two chains differ by L3. The entry is never appended to another chain by L3, so it stays the head of its chain, and L6 puts that chain first. Every pair of consecutive blocks inside a chain was joined by L5 along an edge $a \to b$ of positive weight, so it is a fall-through. Legality holds for any order, as explained above, so the layout keeps the meaning of the procedure.

The layout is not optimal in general, and cannot be unless P = NP, by the reduction above. The example shows a loss of $65 - 57 = 8$ on a graph with six blocks.

## Complexity

Sorting the edges takes $O(E \log E)$. With head and tail markers per block and linked lists for the chains, each test in L4 and each join in L5 takes $O(1)$ time, and the "same chain" test in L3 is a find in a [disjoint-set forest](/disjoint-set-forest/). The union-find steps cost less than the sort, so L1 to L5 take $O(E \log E + V)$. The ordering loop L7 to L9 scans all edges for each of the $C$ chains, so it takes $O(C E)$. The procedure ordering recomputes the group weights after each of at most $P - 1$ joins of $P$ procedures, which takes $O(P \cdot E_{\mathrm{call}})$ for $E_{\mathrm{call}}$ call-graph edges.

## Properties

- Greedy and deterministic for a fixed tie rule.
- It only uses edge weights, so an edge profile is enough. A path profile adds nothing for this model.
- It is not optimal: it is a greedy algorithm for an NP-hard problem, and it has no constant-factor guarantee in this form.
- An edge into the entry is never a fall-through, and in each loop at least one edge of the cycle is not a fall-through.

## Variants and improvements

- **Procedure splitting.** Pettis and Hansen also move blocks that never ran in the profile into a separate cold part far away, so the hot part of each procedure is small.
- **Extended TSP.** Newell and Pupyrev score a layout also by the short jumps it makes, forward and backward, which fit better with real branch costs and cache lines, and give better heuristics for that score.
- **Call-chain clustering.** For very large binaries, Ottoni and Maher order procedures by merging each one into the cluster of its most frequent caller, with a limit on the cluster size, and report better results than closest-is-best.
- **Exact layout for small procedures.** For a few blocks, a search over all orders, as in the tests here, finds the optimum in this model.

## When to use it

Use it in the back end of a compiler or a post-link optimizer, after the profile is collected, when the hot code of a program is larger than the instruction cache or when taken branches are costly. Inlining should come first, since it changes the CFG. Without a profile, static branch predictions can stand in for the weights, but the gain is smaller.

## Pitfalls

- **A stale profile.** The weights describe the training run. If production inputs take other paths, the layout can be worse than the source order.
- **Ties.** Many edges have equal weights in small profiles. The result then depends on the tie rule, so the rule must be fixed for builds to be reproducible.
- **Moving the entry.** In a format where the first block is the entry, as in the toy IR, a chain that puts another block first changes the program. L3 keeps the entry at the head.
- **Fall-through is not the whole cost.** The model ignores block sizes, cache line boundaries and the distance of jumps. A layout that wins on fall-through weight can still fill more cache lines.
- **Greedy is not optimal.** The example above loses 8 of 65. Do not report the result as the best layout.

## Implementations

## History

Pettis and Hansen presented profile guided code positioning at PLDI 1990. The paper introduced the three parts that later tools kept: closest-is-best procedure ordering, bottom-up block chaining and procedure splitting. Later work changed the cost model and the merge rules for large data-center binaries, for example the call-chain clustering of Ottoni and Maher in 2017 and the extended TSP layout of Newell and Pupyrev in 2020.

## References
