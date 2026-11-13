---
tag: EV9FYH
kind: problem
slug: nonogram-problem
name: Nonogram problem
aliases:
- Picross
- Paint by numbers
- Griddlers
area: games-and-search/puzzles
level: advanced
summary: Fill grid cells so that the blocks of filled cells in each row and column match the clues. NP-complete; one line is solved exactly in polynomial time, but line solving alone is incomplete.
prereqs: [constraint-satisfaction-problem, np-complete, nondeterministic-finite-automaton]
see_also: [sat, 2-sat, constraint-propagation, three-dimensional-matching, parsimonious-reduction, regular-expression, kakuro-problem, minesweeper-consistency]
sources:
  - paper: "Nobuhisa Ueda and Tadaaki Nagao, NP-completeness results for NONOGRAM via parsimonious reductions, Technical Report TR96-0008, Department of Computer Science, Tokyo Institute of Technology, May 1996"
    locator: the NP-completeness of Nonogram by a parsimonious reduction from three-dimensional matching
  - paper: doi:10.1016/j.patcog.2008.12.003
    title: K. Joost Batenburg and Walter A. Kosters, Solving Nonograms by combining relaxations, Pattern Recognition 42(8), 2009, 1672 to 1683
    locator: line solving, its incompleteness, and the combination with a 2-SAT relaxation
  - paper: doi:10.1007/978-3-540-78275-9_33
    title: K. Joost Batenburg and Walter A. Kosters, A reasoning framework for solving Nonograms, Combinatorial Image Analysis (IWCIA 2008), LNCS 4958
    locator: the hierarchy of reasoning rules for one line and for several lines
---

The Nonogram problem gives the number of rows and columns of a grid and, for each row and each column, a clue: the list of lengths of the blocks of consecutive filled cells in that line, in order. It asks for a set of filled cells that matches all the clues. Ueda and Nagao (1996) proved the problem [NP-complete](/np-complete/) by a [parsimonious reduction](/parsimonious-reduction/) from [three-dimensional matching](/three-dimensional-matching/). One line alone is easy: the cells that are forced in every filling of a line follow from a run of a [finite automaton](/nondeterministic-finite-automaton/) forward and backward over the line. Repeating this *line solving* over all rows and columns solves most published puzzles, but not all, so a complete solver adds search or a stronger relaxation.

## In plain words

The puzzle is a grid of white squares and a list of numbers beside each row and above each column. The numbers say how long the black stretches in that line are, in order, with at least one white square between two stretches. You must find which squares are black. When you are done, the black squares often draw a picture.

You can reason about one line at a time. A stretch of six in a line of ten must cover the two middle squares, wherever it sits. Each square you decide gives new facts for the crossing line, and so on.

Sometimes this line by line reasoning gets stuck, even when the puzzle has only one answer. Then you must guess and check. In general no fast method is known.

## Definition

A *line* of length $L$ is a word $x \in \{0, 1\}^L$, where 1 is a filled cell. Its *clue* $\operatorname{cl}(x) = (b_1, \ldots, b_k)$ is the list of lengths of the maximal blocks of 1s, from left to right, so $b_i \ge 1$, and $x$ matches $(b_1, \ldots, b_k)$ exactly when $x$ is in the language of the [regular expression](/regular-expression/)

$$0^* \, 1^{b_1} \, 0^+ \, 1^{b_2} \, 0^+ \cdots 0^+ \, 1^{b_k} \, 0^*.$$

An *instance* is $h, w$, row clues $R_1, \ldots, R_h$ and column clues $C_1, \ldots, C_w$. A *solution* is a matrix $X \in \{0, 1\}^{h \times w}$ with $\operatorname{cl}(\text{row } r) = R_r$ and $\operatorname{cl}(\text{column } c) = C_c$ for all $r, c$.

- **Decision.** Does the instance have a solution?
- **Search, uniqueness, counting.** Find one, decide whether it is unique (published puzzles have one), or count them.
- **Line solving.** Given one clue and a *partial line* in $\{0, 1, ?\}^L$, find the cells that have the same value in every matching completion, or report that there is none.

The instance size is $\Theta(h + w)$ numbers plus the clue lengths, at most $\Theta(hw)$ numbers in all. The state space is the $2^{hw}$ matrices. A matrix is checked in $O(hw)$ time, so the decision problem is in [NP](/np/). The hardness results are for the family of all board sizes.

## Variants

- **Color nonograms.** Each block has a color, and two adjacent blocks of different colors need no gap. Line solving extends with one automaton state per cell of each block.
- **Row and column counts only.** If a clue gives only the number of filled cells in each line, the problem is the reconstruction of a 0-1 matrix from its row and column sums, which is solvable in polynomial time by the Gale-Ryser condition and a greedy construction. The block structure is what makes nonograms hard.
- **Other grids.** Triangular and hexagonal boards, and boards with clues on three axes.
- **Simple puzzles.** Puzzles that line solving alone solves form the usual "fair" class of published puzzles.

## Examples

**The overlap rule.** In a line of length $L$, a single block of length $b$ with $2b > L$ covers the cells $L - b, \ldots, b - 1$ (0-indexed) in every placement: the leftmost placement covers $0, \ldots, b - 1$, the rightmost covers $L - b, \ldots, L - 1$, and every placement covers the cells common to these two, $2b - L$ of them. For $b = 6$ and $L = 10$ that is the two middle cells 4 and 5. The clue $(3, 1)$ in a line of 5 fixes the whole line to $11101$, because $3 + 1 + 1 = 5$ leaves no slack.

**Line solving can stall with a unique solution.** Take the $4 \times 4$ instance with row clues $(1), (1), (1, 1), (2)$ and column clues $(1), (1), (2), (2)$. Its only solution is

```
. . . #
. . . #
# . # .
. # # .
```

but each of the eight lines, on its own, still allows each of its cells to be filled or empty, so line solving fixes no cell at all. Over all $2^{16} = 65{,}536$ fillings of a $4 \times 4$ grid, 52,362 are the unique solution of their own clues, and line solving alone solves 51,234 of these; it fails on the other 1,128. On the $3 \times 3$ grid, all 384 uniquely determined fillings are solved by line solving.

**Two solutions.** The $2 \times 2$ instance with all four clues $(1)$ has the two diagonals as solutions, and line solving fixes nothing.

## Known algorithms

**Exact line solving.** Build the automaton for the regular expression of the clue: one state for each cell of each block (symbol 1), one looping state for each gap between blocks (symbol 0, at least one cell), and looping start and end states for the optional outer gaps. Run it forward and backward over the partial line, keeping the set of states that can be occupied at each cell.

```pseudo id=main
LINE-SOLVE(b[1 .. k], x[0 .. L-1])
L1  build the automaton for 0* 1^b1 0+ 1^b2 ... 0+ 1^bk 0*, one symbol per state
L2  F[0] ← start states whose symbol fits x[0]
L3  for i ← 1 to L - 1: F[i] ← successors of states in F[i-1] whose symbol fits x[i]
L4  B[L-1] ← accepting states whose symbol fits x[L-1]
L5  for i ← L - 2 down to 0: B[i] ← states that fit x[i] and have a successor in B[i+1]
L6  for i ← 0 to L - 1: V ← the symbols of the states in F[i] ∩ B[i]
L7      if V is empty then return INCONSISTENT
L8      x[i] ← the symbol if V has one element, else ?
L9  return x
```

*Correctness.* An accepting run of the automaton is a sequence of states $s_0, \ldots, s_{L-1}$ that starts in a start state, follows transitions, and ends in an accepting state. Each state reads one fixed symbol, so the symbols along a run spell a word of the language, and each word of the language has a run. A run is consistent when each symbol fits the known cells. By induction on $i$, $F[i]$ is the set of states $s$ such that some consistent run prefix ends in $s$ at cell $i$, and $B[i]$ is the set of states from which a consistent run suffix starts at cell $i$ and ends in an accepting state. So $s \in F[i] \cap B[i]$ exactly when some consistent accepting run passes $s$ at cell $i$. Cell $i$ can take the value $v$ in a matching completion exactly when such a state has symbol $v$. If no state qualifies at some cell, no completion exists. $\square$

The automaton has $m = b_1 + \cdots + b_k + k + 1$ states and each state has at most two successors, so the time is $O(Lm) = O(L^2)$ and the space is $O(Lm)$.

**Propagation and search.** Line solve every row and column, and after any change line solve the crossing lines again, until nothing changes. Each change fixes at least one more cell, so there are at most $hw$ rounds of change, and the fixpoint is reached in polynomial time. If a cell is still unknown, branch on it (filled, then empty) and propagate in each branch. This is complete, and it is [constraint propagation](/constraint-propagation/) with one global constraint per line, each filtered to generalized arc consistency by the automaton.

**Stronger relaxations.** Batenburg and Kosters combine line solving with a [2-SAT](/2-sat/) relaxation that captures implications between pairs of cells, and solve many puzzles that line solving leaves open without search. A [SAT](/sat/) encoding gives each cell a variable and encodes each line constraint through its automaton or through the start positions of its blocks.

## Bounds

- **NP-completeness.** Ueda and Nagao (1996) reduce three-dimensional matching to Nonogram. Their reduction is parsimonious, so the number of solutions is preserved, and counting nonogram solutions is as hard as counting three-dimensional matchings.
- **One line.** Exact line solving takes $O(L^2)$ time per line by the automaton, polynomial in the line length.
- **Incompleteness of line solving.** Line solving to a fixpoint runs in polynomial time but is not complete: the $4 \times 4$ example above has a unique solution and line solving fixes none of its cells. Unless $\mathrm{P} = \mathrm{NP}$, no polynomial time propagation is complete.
- **Fixed size.** For a fixed board the problem is finite with $2^{hw}$ candidate fillings.

## Reductions

- **From three-dimensional matching (Ueda and Nagao).** Gadgets of rows and columns encode the triples, and the clues force each element to be covered once.
- **To SAT and CSP.** One Boolean variable per cell, and a regular-language constraint per line, which has a compact CNF form through its automaton.
- **To 2-SAT, as a relaxation.** Implications between pairs of cells give a 2-SAT formula whose solutions include all nonogram solutions; unsatisfiable assignments of one cell can then be ruled out in polynomial time.
- **Discrete tomography.** A nonogram is the reconstruction of a binary image from block projections, a sibling of the polynomial reconstruction from plain row and column sums.

## Applications

- **Puzzle design.** Publishers want a unique solution that line solving finds without guessing. A generator draws a picture, computes its clues, and keeps it when a line solver solves it.
- **Benchmarks.** Nonograms are used to test propagation of regular-language constraints and SAT encodings.
- **Image reconstruction.** The problem is a case of discrete tomography, where an image is rebuilt from summaries of its rows and columns.

## References
