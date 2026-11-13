---
tag: PYWCCV
kind: algorithm
slug: df-pn
name: Depth-first proof-number search
aliases:
- DFPN
- df-pn
area: games-and-search/game-tree-search
level: research
summary: A depth-first form of proof-number search that stays in a subtree while its proof and disproof numbers stay below thresholds, and keeps the numbers in a transposition table.
solves: [game-tree-evaluation]
model: word-ram
complexity:
  vars: {N: the number of interior nodes of the tree, b: the branching factor, d: the depth}
  time: {worst: O(N b d), best: O(b)}
  space: {extra: O(N b)}
properties: {deterministic: true, recursive: true}
prereqs: [proof-number-search, transposition-table, depth-first-search]
see_also: [alpha-beta-pruning, iterative-deepening-search, solved-game, endgame-solving, hex-game, zobrist-hashing, minimax, monte-carlo-tree-search]
sources:
  - paper: "\"Df-pn algorithm for searching AND/OR trees and its applications\""
    title: Ayumu Nagai, Df-pn algorithm for searching AND/OR trees and its applications, PhD thesis, Department of Information Science, University of Tokyo (2002)
    locator: the definition of df-pn with thresholds, and the proof that on trees it always expands a most-proving node, as proof-number search does (general locator)
  - paper: doi:10.1007/978-3-540-70829-2_6
    title: H. Jaap van den Herik and Mark H. M. Winands, Proof-Number Search and its variants, in Oppositional Concepts in Computational Intelligence, Studies in Computational Intelligence 155, Springer (2008)
    locator: Section 2.5 (df-pn, the thresholds of the child, min(thpn, pn2 + 1) and thdn - dn + dn(child) at an OR node, and the dual at an AND node)
  - paper: "\"Game-tree search using proof numbers: The first twenty years\""
    title: Akihiro Kishimoto, Mark H. M. Winands, Martin Müller and Jahn-Takeshi Saito, Game-tree search using proof numbers, The first twenty years, ICGA Journal 35(3) (2012)
    locator: pp. 131 to 156 (df-pn and its enhancements, the table, the 1 + epsilon trick, transpositions and cycles)
  - paper: "\"Improving depth-first PN-search: 1 + epsilon trick\""
    title: Jakub Pawlewicz and Łukasz Lew, Improving depth-first PN-search, 1 + epsilon trick, Computers and Games 2006, Lecture Notes in Computer Science 4630
    locator: pp. 160 to 171 (the threshold ceil(pn2 (1 + epsilon)) in place of pn2 + 1, to cut down re-expansions)
  - paper: doi:10.1016/j.ins.2004.04.012
    title: Akihiro Kishimoto and Martin Müller, A solution to the GHI problem for depth-first proof-number search, Information Sciences 175(4) (2005)
    locator: pp. 296 to 314 (the graph history interaction problem in df-pn and its solution)
  - paper: "\"About the completeness of depth-first proof-number search\""
    title: Akihiro Kishimoto and Martin Müller, About the completeness of depth-first proof-number search, Computers and Games 2008, Lecture Notes in Computer Science 5131
    locator: pp. 146 to 156 (df-pn is complete on finite directed acyclic graphs and incomplete on finite graphs with cycles)
  - paper: doi:10.1007/978-3-319-09165-5_12
    title: Jakub Pawlewicz and Ryan B. Hayward, Scalable parallel DFPN search, Computers and Games 2013, Lecture Notes in Computer Science 8427
    locator: pp. 138 to 150 (a parallel df-pn that solved all remaining 9 x 9 Hex openings and one 10 x 10 opening)
---

Depth-first proof-number search (df-pn) proves or disproves a yes-or-no goal on an AND/OR tree with the proof and disproof numbers of [proof-number search](/proof-number-search/), but it searches depth first. A call on a node gets two thresholds, one for each number, and stays in the subtree of that node until one of its numbers reaches its threshold; the thresholds are set so that this is exactly the moment when the most-proving node leaves the subtree. The numbers are kept in a [transposition table](/transposition-table/) instead of an explicit tree, so the memory can be bounded and positions reached by different move orders share one entry. Nagai introduced df-pn in his 2002 thesis and proved that on trees it always expands a most-proving node, as proof-number search does; it is the standard method for solving positions in shogi, Go and [Hex](/hex-game/).

## In plain words

Proof-number search always knows which open position to look at next, but after each step it walks back to the start of the game, and it keeps the whole search in memory.

Df-pn finds the same next position without walking back. When it goes into one line of play, it also writes down how bad that line may get before another line becomes the better choice. It keeps working in that line until the line gets that bad, and only then goes back up one level and chooses again.

The counts for each position go into a table. If the table fills up, the least useful counts can be thrown away and computed again later, so the search fits in a fixed amount of memory.

## The problem

The input is the same as for [proof-number search](/proof-number-search/): a root position, a move generator, and a terminal test that says whether the goal holds (proved) or fails (disproved) at a position where the search stops. At OR nodes the prover moves and one proved child is enough; at AND nodes the opponent moves and every child must be proved. The output is whether the root is proved. The positions may form a tree or, with transpositions, a directed acyclic graph.

## The algorithm

The table maps each position to a pair $(\mathrm{pn}, \mathrm{dn})$. A proved terminal position has $(0, \infty)$, a disproved one $(\infty, 0)$, and a position with no entry counts as $(1, 1)$. An expanded node gets its numbers from its children by the rules of proof-number search: at an OR node $\mathrm{pn} = \min_c \mathrm{pn}(c)$ and $\mathrm{dn} = \sum_c \mathrm{dn}(c)$, at an AND node the sum and the minimum change places.

```pseudo id=main
DFPN(root)
L1  MID(root, ∞, ∞)
L2  return pn(root) = 0                          ▷ read from the table

MID(n, thpn, thdn)
L3  if n is terminal then store (0, ∞) or (∞, 0) for n; return
L4  generate the children of n
L5  loop
L6      compute (pn(n), dn(n)) from the table entries of the children
L7      if pn(n) ≥ thpn or dn(n) ≥ thdn then store (pn(n), dn(n)) for n; return
L8      if n is an OR node then
L9          c ← a child with the smallest pn; p₂ ← the second smallest pn (∞ if n has one child)
L10         MID(c, min(thpn, p₂ + 1), thdn − dn(n) + dn(c))
L11     else
L12         c ← a child with the smallest dn; d₂ ← the second smallest dn (∞ if n has one child)
L13         MID(c, thpn − pn(n) + pn(c), min(thdn, d₂ + 1))
```

The thresholds of the child in line L10 say when the search must leave it. While $\mathrm{pn}(c) < p_2 + 1$, the child $c$ still has the smallest proof number, so the most-proving path still goes through it. While $\mathrm{dn}(c) < \mathrm{thdn} - \mathrm{dn}(n) + \mathrm{dn}(c_{\text{old}})$, the parent's disproof number, which changes by the same amount as $\mathrm{dn}(c)$, stays below the parent's own threshold. Line L13 is the dual at an AND node. The root call has no limits, so it ends only when the root is proved or disproved.

The *1 + ε trick* of Pawlewicz and Lew replaces $p_2 + 1$ in line L10 by $\max(p_2 + 1, \lceil p_2 (1 + \varepsilon) \rceil)$, and $d_2 + 1$ in line L13 in the same way. The child then stays longer in its subtree, which saves re-expansions at the cost of sometimes searching a node that is no longer most-proving.

## Example

The tree is the one of the [proof-number search](/proof-number-search/) example: the OR root A has the AND children B, C and D; B has a proved terminal child and an OR child X with two disproved terminal children; C has an OR child Y, with a disproved and a proved terminal child, and a proved terminal child; D has one disproved terminal child.

| call | thresholds (thpn, thdn) | what happens |
|---|---|---|
| MID(A) | $(\infty, \infty)$ | B, C, D are $(1,1)$, so A is $(1, 3)$; B is best, $p_2 = 1$; call B with $(\min(\infty, 2), \infty - 3 + 1) = (2, \infty)$ |
| MID(B) | $(2, \infty)$ | B is $(0 + 1, \min(\infty, 1)) = (1, 1)$; X has the smallest dn, $d_2 = \infty$; call X with $(2 - 1 + 1, \infty) = (2, \infty)$ |
| MID(X) | $(2, \infty)$ | X is $(\infty, 0)$, and $\infty \ge 2$: store and return |
| back in B | | B is $(\infty, 0)$: store and return |
| back in A | | A is $(\min(\infty, 1, 1), 0 + 1 + 1) = (1, 2)$; C is best, $p_2 = 1$; call C with $(2, \infty)$ |
| MID(C) | $(2, \infty)$ | C is $(1, 1)$; call Y with $(2, \infty)$ |
| MID(Y) | $(2, \infty)$ | Y is $(0, \infty)$, and $\infty \ge \infty$: store and return |
| back in C, A | | C is $(0, \infty)$, then A is $(0, \infty)$: proved |

Df-pn makes five calls and expands the same nodes in the same order as proof-number search, A, B, X, C, Y, without walking back to the root between them, and D is never searched.

With the table indexed by the board, df-pn proves that X does not lose tic-tac-toe with 708 calls of MID on 558 different positions, and disproves "X wins" with 1,758 calls on 1,341 positions; tic-tac-toe has 5,478 legal positions. In [Nim](/nim/) with heaps $3, 5, 7$, where equal positions arise by many move orders, it proves the first-player win with 195 calls. With $\varepsilon = 0.25$ the two tic-tac-toe searches take 744 and 1,912 calls: on problems this small the trick does not pay.

## Correctness

The [proof](proofs/correctness/) covers finite trees with a table that never loses an entry.

- **The stored numbers are the numbers of proof-number search.** In a tree the children of a node change only during calls inside that node's own call. So, outside the active calls, every stored pair is computed from the current pairs of the children, and the table holds the proof and disproof numbers of the explored tree. Their meaning is the one proved on the proof-number search page: $\mathrm{pn} = 0$ means proved.
- **A child is entered below its thresholds.** At line L10, $\mathrm{pn}(c) = \mathrm{pn}(n) < \mathrm{thpn}$ and $\mathrm{pn}(c) \le p_2 < p_2 + 1$, and $\mathrm{dn}(n) < \mathrm{thdn}$ gives $\mathrm{dn}(c) < \mathrm{thdn} - \mathrm{dn}(n) + \mathrm{dn}(c)$. So each call starts with numbers strictly below its thresholds, and by induction it expands at least one node that was never expanded.
- **Termination and the answer.** Each call expands a new node, and each expansion belongs to at most $d + 1$ active calls, so there are at most $(d + 1) N$ calls. The root call ends only with $\mathrm{pn} = \infty$ or $\mathrm{dn} = \infty$, so the root is disproved or proved.
- **Most-proving nodes** (Nagai). When df-pn enters a new frontier node, every node on the call stack is a child with the smallest proof number (OR) or disproof number (AND) of its parent, by the current numbers. So the path is a selection path of proof-number search, and the node is most-proving. Ties can be broken in a different way, so the two searches can expand different most-proving nodes, and with the 1 + ε trick the property is lost. The tests check this against a mirror proof-number tree at every expansion.
- **Graphs.** On a directed acyclic graph with an unbounded table, df-pn is complete (Kishimoto and Müller 2008), but sums count shared subtrees more than once. On graphs with cycles it is not complete, and the value of a position can depend on the path that reached it (the graph history interaction problem).

## Complexity

The costs are in the [word RAM](/word-ram/), with the move generator, the terminal test and each table access counted as $O(1)$ per position.

**Time.** On a tree with $N$ interior nodes there are at most $(d + 1) N$ calls of MID. Each turn of the loop of a call either returns or makes one child call, and costs $O(b)$ to read the children's entries, so the total is $O(N b d)$, the same bound as for proof-number search. In practice the cost of df-pn is dominated by *re-expansions*: a node can be entered many times, and each entry generates its children again.

**Space.** The recursion holds at most $d$ frames of $O(b)$ each. The table holds one entry per stored position, $O(N b)$ in the worst case with an unbounded table. With a table of fixed size and a replacement rule, the memory is bounded; the search stays correct when it ends, but it may re-search lost subtrees.

**How it compares.** Df-pn does the same expansions as proof-number search on trees but saves the walk from the root and the explicit tree, and with transpositions it shares the work for equal positions. Its run time can be larger because of re-expansions, which the 1 + ε trick and good table management reduce.

## Properties

- **Depth-first and best-first.** It moves like a depth-first search but expands nodes in a best-first order, the most-proving order of proof-number search.
- **Bounded memory.** The table can have a fixed size; the explicit tree of proof-number search is gone.
- **Transpositions for free.** Equal positions share a table entry, so a graph of positions is searched as a graph. Keys are usually [Zobrist hashes](/zobrist-hashing/).
- **Two-valued.** Like proof-number search, it decides a yes-or-no goal; draws need a second search.
- **Not an iterative deepening search.** The thresholds bound proof and disproof numbers, not depth, so a long forced line is followed to its end in one call.

## Variants and improvements

The survey of Kishimoto, Winands, Müller and Saito describes these and more.

- **1 + ε trick.** Larger thresholds for the best child, as above, to reduce the switching between siblings.
- **Initial numbers from knowledge.** Frontier nodes get numbers from move counts or evaluation functions instead of $(1, 1)$, often together with a threshold that grows with the depth.
- **Table management.** Keep the entries of large subtrees, and remove entries of small ones when the table is full.
- **Cycles.** Kishimoto and Müller give a solution of the graph history interaction problem for df-pn, which keeps proofs that depend on the path apart from those that do not.
- **Parallel df-pn.** The parallel df-pn of Pawlewicz and Hayward shares one table among several threads; it solved the remaining $9 \times 9$ openings of Hex and one $10 \times 10$ opening.

## When to use it

Use df-pn to solve positions with a binary goal when the search is too large for the memory of [proof-number search](/proof-number-search/): mate problems in shogi and chess, life-and-death in Go, and the solution of [Hex](/hex-game/) openings. It is the default proof-number method for long searches. For move choice in games far from solved, use [alpha-beta pruning](/alpha-beta-pruning/) or [Monte Carlo tree search](/monte-carlo-tree-search/); for small trees, plain proof-number search is simpler and has no re-expansions.

## Pitfalls

- **Infinity arithmetic.** The threshold $\mathrm{thdn} - \mathrm{dn}(n) + \mathrm{dn}(c)$ must stay $\infty$ when $\mathrm{thdn}$ is $\infty$. With a large integer in place of $\infty$, choose the arithmetic so that the result does not drop below "infinite".
- **Double counting on graphs.** On a DAG the sum at an AND or OR node counts a shared subtree once per path, so the numbers grow too fast, and the search can spend a long time in parts that look hopeless but are not.
- **Cycles.** A position that repeats can make a proof depend on the path, and a naive table then stores wrong results.
- **Thrashing.** When two siblings have close numbers, the search can switch between them on every call, and each switch re-generates subtrees. The 1 + ε trick is the usual cure.
- **Table loss.** With a small table, entries of solved subtrees can be overwritten, and the work is done again.
- **Deep recursion.** Forced lines can be very long; a recursive implementation needs a large stack.

## Implementations

## History

Nagai introduced df-pn in his 2002 thesis at the University of Tokyo and proved that on trees it always expands a most-proving node, like the proof-number search of Allis, van der Meulen and van den Herik. Kishimoto and Müller gave a solution of the graph history interaction problem for df-pn in 2005, and in 2008 showed that df-pn is complete on finite acyclic graphs and incomplete on graphs with cycles. Pawlewicz and Lew proposed the 1 + ε trick in 2006. Pawlewicz and Hayward used a parallel df-pn to solve all remaining $9 \times 9$ Hex openings and one $10 \times 10$ opening in 2013. The survey of Kishimoto, Winands, Müller and Saito in 2012 reviews these developments.

## References
