---
tag: WQC6R5
kind: problem
slug: crossword-filling-problem
name: Crossword filling problem
aliases:
- Crossword construction
- Crossword puzzle
area: games-and-search/puzzles
level: advanced
summary: Write a dictionary word into every slot of a crossword grid so that crossing slots agree on their shared letter. NP-complete (Garey and Johnson problem GP14).
prereqs: [constraint-satisfaction-problem, np-complete, exact-cover-by-3-sets]
see_also: [sat, wildcard-matching-in-trie, minimum-remaining-values, forward-checking, dynamic-backtracking, dual-graph-transformation, treewidth, kakuro-problem]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, 1979
    locator: Appendix A8, problem GP14, Crossword Puzzle Construction (NP-complete by a transformation from X3C, credited to Lewis and Papadimitriou)
  - paper: "Matthew L. Ginsberg, Michael Frank, Michael P. Halpin and Mark C. Torrance, Search lessons learned from crossword puzzles, Proceedings of the Eighth National Conference on Artificial Intelligence (AAAI-90), 1990, 210 to 215"
    locator: filling an empty grid from a large dictionary by search with the most constrained slot first
  - paper: arxiv:2109.11203
    title: Laurent Gourvès, Ararat Harutyunyan, Michael Lampis and Nikolaos Melissinos, Filling crosswords is very hard, 2021
    locator: the abstract and the introduction (hardness on grids of small treewidth, the m to the treewidth algorithm when words may repeat, and the approximation of the most words placed)
  - paper: arxiv:1401.4597
    title: "Matthew L. Ginsberg, Dr.Fill: crosswords and an implemented solver for singly weighted CSPs, Journal of Artificial Intelligence Research 42, 2011"
    locator: solving crosswords from their clues as a weighted CSP
---

The crossword filling problem gives a grid of white and black cells and a dictionary of words, and asks for letters in the white cells so that every *slot*, a maximal run of two or more white cells across or down, spells a word of the dictionary. Some letters may be given in advance, and often a word may fill at most one slot. Garey and Johnson list the problem as GP14, Crossword Puzzle Construction, and record it as [NP-complete](/np-complete/) by a reduction from [exact cover by 3-sets](/exact-cover-by-3-sets/). Solvers treat it as a [CSP](/constraint-satisfaction-problem/) with one variable per slot and fill the slot with the fewest fitting words first.

## In plain words

A crossword grid has white squares and black squares. Each white line of two or more squares, left to right or top to bottom, must hold a word from a word list.

Where an across line and a down line meet, they share a square, so the two words must have the same letter there. That is what makes the task hard: a good word in one place can block every word in a line that crosses it.

A computer fills the grid one line at a time. It picks the line with the fewest words that still fit the letters already written, tries those words one by one, and goes back when some line has no word left.

## Definition

Let the grid be $h \times w$ with a set $B$ of black cells. A *slot* is a maximal sequence of at least two consecutive white cells in one row or one column. An *instance* is the grid, a finite dictionary $D \subseteq \Sigma^*$, and letters for some white cells. A *filling* gives every white cell in a slot a letter of $\Sigma$ such that

1. every given letter is kept;
2. for every slot $s$, the letters on $s$, read left to right or top to bottom, form a word of $D$;
3. in the *distinct* variant, no word fills two slots.

A filling is checked in $O(hw)$ time plus a dictionary lookup per slot, so the problem is in [NP](/np/).

- **Decision.** Is there a filling?
- **Optimization.** Fill as many slots as possible with words, where each white cell holds one letter.

In GP14 of Garey and Johnson the grid is an $n \times n$ matrix of 0 and 1 entries and the dictionary $W$ is part of the input.

## Variants

- **Word reuse.** Allowed or not. The reduction below needs reuse in the down slots; the distinct variant is NP-complete as well (Gourvès et al.).
- **Given letters and themes.** Constructors fix some long theme entries and fill the rest.
- **Solving from clues.** A published crossword is solved from its clues, not from a dictionary. Each slot then has a ranked list of candidate answers, and the task is a weighted CSP; Ginsberg's Dr.Fill solves it in this form.
- **Word squares.** The grid has no black cells. A *symmetric* word square has the same words across and down.

## Examples

**A word square.** Take the open $3 \times 3$ grid and the dictionary

```
BAT ARE TEN TAN ATE NET EAR ERA RAT TAR BEE ONE TOE OAT
```

With distinct words there are exactly two fillings, one the transpose of the other:

```
T A R        T E N
E R A        A R E
N E T        R A T
```

The first has TAR, ERA, NET across and TEN, ARE, RAT down. If a word may fill two slots, there are 16 fillings, among them the symmetric square BAT, ARE, TEN, which uses each word twice.

**Black cells.** The grid below has six slots, three of length 2 and three of length 3. With the 3-letter words above and AT, TO, BE, NO, AN, ON, its two fillings are

```
A N #        A T #
T E N        N E T
# T O        # N O
```

A given T in the first column of the middle row leaves only the first.

## Known algorithms

**Slot backtracking with the fewest-candidates rule.** One variable per slot, whose domain is the dictionary words of its length. At each node, compute for every open slot the words that fit the letters already written, return at once if some slot has none, and branch on the slot with the fewest, by the [minimum remaining values](/minimum-remaining-values/) rule. A [trie](/trie/) or an index by length, position and letter lists the fitting words quickly, which is [wildcard matching](/wildcard-matching-in-trie/) on the slot's pattern.

```pseudo id=main
CROSSWORD-FILL(grid, D)
L1  if every slot is filled then output the grid; return
L2  for each open slot s, let F(s) be the words of D that fit the letters on s and are not used yet
L3  if F(s) is empty for some open slot then return
L4  pick the open slot s with the fewest words in F(s)
L5  for each word x in F(s) do
L6      write x into s and mark x used
L7      CROSSWORD-FILL(grid, D)
L8      mark x unused and erase the letters of s that no other filled slot holds
```

*Correctness.* Every filling is found once: in a filling, the slot chosen at line L4 holds some word that fits the letters written so far, and line L5 tries it. Line L3 cuts only states with no completion, since letters are only added along a branch and a word that does not fit now never fits later. The worst case is exponential in the number of slots.

**CSP methods.** Ginsberg et al. (1990) studied this search on large dictionaries, with the most constrained slot first. Ginsberg later reported large gains on crosswords with [dynamic backtracking](/dynamic-backtracking/), which keeps the work done on slots that are not to blame for a dead end. [Forward checking](/forward-checking/) is line L2 and line L3. In the [dual graph](/dual-graph-transformation/), slots are nodes and crossing slots are joined; when it is a tree, the instance is a [tree-structured CSP](/tree-structured-csp/) and is solved in polynomial time by arc consistency along the tree.

**Small treewidth.** When words may repeat, a dynamic program over a tree decomposition of the grid takes $m^{O(\mathrm{tw})}$ time for a dictionary of $m$ words and [treewidth](/treewidth/) $\mathrm{tw}$ (Gourvès et al.).

## Bounds

- **NP-completeness.** Garey and Johnson, GP14, credited to Lewis and Papadimitriou without a published proof; the reduction below is one standard proof.
- **Fine-grained.** With word reuse, under the exponential time hypothesis no algorithm does much better than the $m^{\mathrm{tw}}$ bound in terms of the number of across slots. The problem is [fixed-parameter tractable](/fixed-parameter-tractable/) in the number of slots $n$, but a $2^{o(n^2)}$ algorithm would contradict the randomized exponential time hypothesis (Gourvès et al.).
- **Distinct words.** NP-hard even on grids whose crossing structure is close to a tree (Gourvès et al.).
- **Approximation.** Placing the most words has a simple $1/2$-approximation, and a better ratio in polynomial time would contradict the [unique games conjecture](/unique-games-conjecture/) (Gourvès et al.).
- **Brute force.** $\prod_s |D_{|s|}|$ assignments of words to slots, each checked in $O(hw)$ time.

## Reductions

**From exact cover by 3-sets.** Given a ground set $\{1, \ldots, 3q\}$ and triples $T_1, \ldots, T_m$, use the alphabet $\{a, b\}$ and an open grid of $q$ rows and $3q$ columns.

- For each triple $T_j$, add the length-$3q$ word with $a$ at the positions in $T_j$ and $b$ elsewhere.
- For each $i \le q$, add the length-$q$ word with one $a$ at position $i$.

Each row is an across slot of length $3q$, so it holds a triple word with three $a$; each column is a down slot of length $q$, so it holds exactly one $a$. Hence the $q$ rows hold triples that are pairwise disjoint and cover all $3q$ columns, an exact cover. Conversely, the $q$ triples of an exact cover, one per row, put exactly one $a$ in each column. The down words repeat, so this is the variant with reuse. The tests run this reduction on small instances and compare the answer with a direct search for an exact cover.

**To SAT and CSP.** One Boolean variable per slot and word with an exactly-one constraint per slot, and a clause that forbids two words that disagree at a crossing; the distinct rule adds an at-most-one constraint per word. This is a [SAT](/sat/) encoding of the CSP model.

## Applications

- **Puzzle construction.** Constructors fill a grid around theme entries with a program of this kind, then write the clues.
- **Search research.** Crosswords are a standard test bed for CSP search, from Ginsberg et al. (1990) to clue-driven solvers such as Dr.Fill.

## References
