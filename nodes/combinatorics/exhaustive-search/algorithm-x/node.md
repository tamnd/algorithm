---
tag: 0R5E65
kind: algorithm
slug: algorithm-x
name: Algorithm X
aliases:
- DLX search
- Knuth's Algorithm X
area: combinatorics/exhaustive-search
level: advanced
summary: Knuth's backtracking search for exact covers, choosing the element with the fewest candidate sets at each step.
solves: [exact-cover]
uses: [dancing-links]
model: word-ram
complexity:
  vars: {n: the number of items, s: the total size of all options, T: the number of nodes of the search tree}
  time: {worst: O(T (n + s)), best: O(n + s)}
  space: {extra: O(n + s)}
properties: {deterministic: true, recursive: true}
history:
  year: 2000
  people: [Donald E. Knuth]
  note: Knuth named the method Algorithm X and its dancing-links program DLX in his paper Dancing links of 2000.
prereqs: [exact-cover, generic-backtracking-algorithm, dancing-links]
see_also: [dancing-links, exact-cover, n-queens-problem, sudoku, polyomino-tiling-problem, generic-backtracking-algorithm, variable-ordering-heuristics, exact-cover-by-3-sets]
sources:
  - paper: "Donald E. Knuth, Dancing links, in Millennial Perspectives in Computer Science, Palgrave, 2000, 187 to 214, arXiv:cs/0011047"
    locator: Sections 1 to 3 (Algorithm X, the rule of the shortest column, and the DLX program), and the pentomino examples
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms, Part 2
    locator: Section 7.2.2.1, Dancing links (Algorithm X, exact covering with primary and secondary items, and Algorithm C for colors)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 4, Backtracking algorithms (exact cover by backtracking)
---

Algorithm X is Knuth's [backtracking](/generic-backtracking-algorithm/) search for all solutions of an [exact cover](/exact-cover/) problem. At each step it picks an item that is not yet covered and has the fewest options left, tries each of those options in turn, removes every option that conflicts with the choice, and recurses. Knuth implements the removals with [dancing links](/dancing-links/), so that each removal is undone in constant time when the search backs up; the program is called DLX. It solves tiling puzzles, [Sudoku](/sudoku/), the [n-queens problem](/n-queens-problem/) and many other combinatorial searches after one translation to exact cover.

## In plain words

You have a list of things that must each be covered once, and a list of pieces, where each piece covers some of the things. You must choose pieces so that each thing is covered exactly once, with no overlap.

Look for the thing that is hardest to cover: the one that the fewest remaining pieces can cover. One of those pieces must be in the answer, so try each of them in turn. When you pick a piece, throw away every other piece that overlaps it, because none of them can be used any more. Then solve the smaller puzzle that is left in the same way.

If some thing can no longer be covered by any piece, the current choices are wrong, so undo the last choice and try the next piece. Starting with the hardest thing makes such dead ends appear early.

## The problem

The input is a finite set of *primary items*, a finite set of *secondary items*, and a list of *options*. Each option is a set of items with at least one primary item. A solution is a set of options that are pairwise disjoint and that together contain each primary item exactly once; each secondary item is contained at most once. With no secondary items this is the [exact cover problem](/exact-cover/). The task is to list all solutions.

We write $n$ for the number of items, $m$ for the number of options, and $s$ for the total size of the options, that is, the number of ones in the 0/1 matrix with a row for each option and a column for each item.

## The algorithm

The state of the search is a set of *active* items and *active* options. At the start, every primary item and every option is active. COVER$(i)$ makes item $i$ inactive and makes every active option that contains $i$ inactive, but leaves the list of options of $i$ itself as it was. UNCOVER$(i)$ undoes COVER$(i)$. The [dancing links](/dancing-links/) page gives these two operations; any representation with the same effect works.

```pseudo id=main
ALGORITHM-X()                               ▷ the chosen options so far are in a list S
L1  if no primary item is active then
L2      OUTPUT(S)
L3      return
L4  i ← an active primary item with the fewest active options     ▷ the first one on a tie
L5  COVER(i)
L6  for each active option o that contains i, in order do
L7      append o to S
L8      for each item j ≠ i of o do COVER(j)
L9      ALGORITHM-X()
L10     for each item j ≠ i of o, in reverse order, do UNCOVER(j)
L11     remove o from S
L12 UNCOVER(i)
```

Line L4 is the *minimum remaining values* rule, the rule that Knuth calls the choice of the shortest column. If the chosen item has no active option, the loop of line L6 does nothing and the call returns: this is a dead end. Line L8 removes every option that shares an item with $o$. Line L10 undoes line L8 in the reverse order, which the dancing-links operations need. Since every solution covers $i$ exactly once, every solution below this node uses exactly one of the options tried at line L6, so the search loses nothing by branching on $i$ alone.

## Example

Knuth's example in *Dancing links* has the items $A, \ldots, G$, all primary, and six options:

| option | items |
|---|---|
| 1 | C E F |
| 2 | A D G |
| 3 | B C F |
| 4 | A D |
| 5 | B G |
| 6 | D E G |

The item counts are $A{:}\,2$, $B{:}\,2$, $C{:}\,2$, $D{:}\,3$, $E{:}\,2$, $F{:}\,2$, $G{:}\,3$, so line L4 picks $A$, the first item with the least count. COVER$(A)$ removes options 2 and 4 from the columns of $D$ and $G$.

1. **Try option 2 (A D G).** COVER$(D)$ removes option 6, and COVER$(G)$ removes option 5. Now $B$ has only option 3, so line L4 picks $B$. Try option 3 (B C F): COVER$(C)$ removes option 1. Item $E$ now has no option left, so this branch is a dead end. Back up to the level of $A$.
2. **Try option 4 (A D).** COVER$(D)$ removes option 6. The counts are $B{:}\,2$, $C{:}\,2$, $E{:}\,1$, $F{:}\,2$, $G{:}\,1$, so line L4 picks $E$. Its only option is 1 (C E F). Choosing it removes option 3, so $B$ and $G$ both have only option 5. Choosing option 5 covers $B$ and $G$, and no primary item is left.

The output is the solution $\{1, 4, 5\}$, that is, $\{C, E, F\}$, $\{A, D\}$ and $\{B, G\}$. It is the only one. The search tree has 6 nodes: the root, the two choices for $A$, one choice below the first of them, and two levels below the second.

On larger problems the rule of line L4 matters a great deal. The 12 pentominoes as an exact cover of the $6 \times 10$ rectangle have 72 items and 2,056 options; Algorithm X finds all 9,356 solutions, which are the 2,339 distinct tilings of Haselgrove up to the 4 symmetries of the rectangle.

## Correctness

Call the state of the search *faithful* to a list $S$ of pairwise disjoint options when the active primary items are exactly the primary items that no option of $S$ contains, and the active options are exactly the options that are disjoint from every option of $S$. The start state is faithful to the empty list. The claim is: if ALGORITHM-X is called in a state faithful to $S$, it outputs each list $S \cup T$, where $T$ is a solution of the *residual* problem (the active primary items, the inactive and active secondary items, and the active options), exactly once, and it returns with the state unchanged. The proof is by induction on the number of active primary items, with the lemma that COVER and UNCOVER keep the state faithful and undo each other. The full proof is below.

## Complexity

The search tree has $T$ nodes, one per call. At a node, line L4 scans the active items in $O(n)$ time. For each child, lines L8 and L10 cover and uncover the items of one option. Each option leaves the lists at most once in these covers, and its removal costs its size, so lines L8 and L10 cost $O(s)$ per child. Each node is a child of at most one node, so the total time is

$$O\big(T \cdot (n + s)\big),$$

and in practice much less, because a cover touches only the options that are still active. The extra space is $O(n + s)$ for the structure and $O(n)$ for the list $S$ and the recursion.

$T$ itself depends on the instance and can be exponential: exact cover is NP-complete, and with the [proposition on enumeration problems](/enumeration-problem/), no algorithm lists all exact covers in time polynomial in the input and the output unless $\mathrm{P} = \mathrm{NP}$. The best case is a problem with no solution and an item with no option: then the time is $O(n + s)$ for the build and one scan.

The time per solution is not bounded by a polynomial either: the search can visit many dead ends between two solutions. To estimate $T$ before a long run, Knuth's random-path estimate of [backtracking](/generic-backtracking-algorithm/) applies to the tree of Algorithm X.

## Properties

- **Complete and non-redundant.** It lists each solution exactly once.
- **Depth-first.** The depth of the recursion is at most the number of primary items, because each level covers at least one primary item.
- **Order.** The order of the output depends on the order of the items and of the options.
- **Fixed branching rule.** Branching on an item, not on an option, means each node has only as many children as the chosen item has options.

## Variants and improvements

- **Secondary items.** Items that may be covered at most once. The [n-queens problem](/n-queens-problem/) uses them for the diagonals.
- **Colors (Algorithm C).** In Section 7.2.2.1 of *The Art of Computer Programming*, a secondary item can carry a color, and options that give it the same color may share it. Word puzzles and many layout problems need this.
- **Multiplicities (Algorithm M).** An item must be covered between $u$ and $v$ times instead of exactly once.
- **Counting and estimation.** Replace OUTPUT by a counter, or walk random paths to estimate $T$ and the number of solutions.
- **Other branching rules.** Line L4 may use another rule, for example a weighted count, but the minimum count is the standard one. With a random choice among the items of least count, repeated short runs give restarts.
- **Symmetry.** For a puzzle whose board has symmetries, restrict the options of one piece to remove symmetric copies of each solution, as Knuth does for the pentominoes.

## When to use it

Use Algorithm X when a problem can be stated as "choose pieces that cover each requirement exactly once": tilings, packings, Sudoku and its variants, schedules in which each slot is used once, and designs. The translation is short, and the search is fast for many such problems. For problems with long chains of logical implications, a SAT solver with clause learning can be much faster. For optimization rather than listing, add a bound and use [branch and bound](/depth-first-branch-and-bound/).

## Pitfalls

- **Options with no primary item.** Such an option is never chosen, because the search only branches on primary items. State the problem so that each option has a primary item.
- **Undo in the wrong order.** With dancing links, the uncovers of line L10 must run in exactly the reverse order of the covers of line L8, and line L12 must undo line L5 last.
- **Forgetting to restrict to active options.** Line L6 must use the options that are active after COVER$(i)$, which are the options of $i$ that are still in its list.
- **Symmetric copies.** A puzzle with symmetries has each solution several times. Count the copies, or break the symmetry in the input.
- **Deep recursion in Python.** The depth is the number of primary items. For a few hundred items use an explicit stack.

## Implementations

## History

Knuth published Algorithm X and its program DLX in the paper *Dancing links* in 2000, where he gave many tiling examples, including the pentominoes. The paper credits the link trick to Hitotsumatsu and Noshita (1979). The rule of choosing the item with the fewest options is the classical "most constrained variable first" rule of backtracking. In Volume 4B of *The Art of Computer Programming* (2022), Section 7.2.2.1 presents Algorithm X with secondary items and extends it to colors and multiplicities.

## References
