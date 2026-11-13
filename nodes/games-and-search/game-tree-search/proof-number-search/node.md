---
tag: 8X9ESA
kind: algorithm
slug: proof-number-search
name: Proof-number search
aliases:
- PN search
- PNS
area: games-and-search/game-tree-search
level: research
summary: Best-first search on AND/OR trees that keeps proof and disproof numbers and always expands a most-proving node, to prove or disprove a goal such as a forced win.
solves: [game-tree-evaluation]
model: word-ram
complexity:
  vars: {N: the number of interior nodes of the tree, b: the branching factor, d: the depth}
  time: {worst: O(N b d), best: O(b)}
  space: {extra: O(N b)}
properties: {deterministic: true, recursive: false, best_first: true}
prereqs: [game-tree, minimax, best-first-search]
see_also: [df-pn, alpha-beta-pruning, transposition-table, solved-game, endgame-solving, monte-carlo-tree-search, hex-game, contingent-planning]
sources:
  - paper: doi:10.1016/0004-3702(94)90004-3
    title: L. Victor Allis, Maarten van der Meulen and H. Jaap van den Herik, Proof-number search, Artificial Intelligence 66(1) (1994)
    locator: pp. 91 to 124 (the algorithm, proof and disproof numbers, the most-proving node and its theorem, the link to conspiracy numbers, and experiments against alpha-beta)
  - paper: "\"Game-tree search using proof numbers: The first twenty years\""
    title: Akihiro Kishimoto, Mark H. M. Winands, Martin Müller and Jahn-Takeshi Saito, Game-tree search using proof numbers, The first twenty years, ICGA Journal 35(3) (2012)
    locator: pp. 131 to 156 (a survey of PNS, PN2, df-pn and their variants, with the problems of transpositions and cycles)
  - paper: doi:10.1007/978-3-540-70829-2_6
    title: H. Jaap van den Herik and Mark H. M. Winands, Proof-Number Search and its variants, in Oppositional Concepts in Computational Intelligence, Studies in Computational Intelligence 155, Springer (2008)
    locator: Section 2 (PNS, the rules for the numbers, the most-proving node, and the memory problem; Section 2.5 for df-pn); general locator for the page numbers
---

Proof-number search (PNS) is a best-first search that proves or disproves a yes-or-no goal, such as "the player to move can force a win", on an AND/OR tree. Each node keeps a *proof number*, the least number of unexplored leaves that must be proved to prove it, and a *disproof number*, the least number that must be disproved to disprove it. Each step walks from the root to a *most-proving node*, a leaf whose proof lowers the root's proof number by one and whose disproof lowers its disproof number by one, expands it, and updates the numbers on the way back. Allis, van der Meulen and van den Herik introduced it in 1994; it needs no evaluation function, and it goes first where the opponent has few replies, which makes it strong for solving positions with forced lines.

## In plain words

You want to prove that you can win a game from some position, not just find a good move. A proof must show one good answer for each of your turns, and an answer for every reply the opponent has.

Proof-number search counts how much work is left. For each position it counts how many open positions you still must solve to prove a win there, and how many to prove that you cannot win. Where the opponent has only one or two replies, the count is small, so a proof there is close.

At each step the search goes to the open position that helps both counts most, looks one move further there, and updates the counts. It stops when one count reaches zero: then the win is proved, or it is shown to be impossible.

## The problem

The input is a finite AND/OR tree given by a root position, a move generator and a terminal test. At an *OR node* the prover (the player who wants the goal) moves; at an *AND node* the opponent moves; the types alternate. The terminal test says, for a position with no further search, whether the goal holds there (*proved*) or fails (*disproved*). A position with no legal move is terminal. A node is proved when it is a proved terminal, when it is an OR node with a proved child, or when it is an AND node whose children are all proved; it is disproved in the dual cases. The output is whether the root is proved. This is [game tree evaluation](/game-tree-evaluation/) with values in $\{\text{true}, \text{false}\}$. For a game with draws, the goal "win" and the goal "at least a draw" are two separate searches.

## The algorithm

PNS keeps the explored part of the tree in memory. A node is *expanded* when its children have been generated; an unexpanded node that is not terminal is a *frontier node*. The numbers satisfy these rules:

| node | proof number $\mathrm{pn}$ | disproof number $\mathrm{dn}$ |
|---|---|---|
| proved terminal | $0$ | $\infty$ |
| disproved terminal | $\infty$ | $0$ |
| frontier | $1$ | $1$ |
| expanded OR node | $\min_c \mathrm{pn}(c)$ | $\sum_c \mathrm{dn}(c)$ |
| expanded AND node | $\sum_c \mathrm{pn}(c)$ | $\min_c \mathrm{dn}(c)$ |

```pseudo id=main
PNS(root)
L1  EVALUATE(root)
L2  while pn(root) ≠ 0 and dn(root) ≠ 0 do
L3      m ← root
L4      while m is expanded do                ▷ select a most-proving node
L5          if m is an OR node then m ← the first child c with pn(c) = pn(m)
L6          else m ← the first child c with dn(c) = dn(m)
L7      for each move from m do create the child c and EVALUATE(c)
L8      SET-NUMBERS(m)
L9      n ← parent(m)                         ▷ update the ancestors
L10     while n ≠ nil do
L11         old ← (pn(n), dn(n))
L12         SET-NUMBERS(n)
L13         if (pn(n), dn(n)) = old then break  ▷ no ancestor can change
L14         n ← parent(n)
L15 return pn(root) = 0                        ▷ true: proved; false: disproved

EVALUATE(c)
L16 if c is a proved terminal then (pn(c), dn(c)) ← (0, ∞)
L17 else if c is a disproved terminal then (pn(c), dn(c)) ← (∞, 0)
L18 else (pn(c), dn(c)) ← (1, 1)

SET-NUMBERS(n)
L19 if n is an OR node then (pn(n), dn(n)) ← (min over children of pn, sum over children of dn)
L20 else (pn(n), dn(n)) ← (sum over children of pn, min over children of dn)
```

The loop of lines L4 to L6 follows the smallest proof number at OR nodes, where one child must be proved, and the smallest disproof number at AND nodes, where one child must be disproved. A program usually adds a budget of expansions or of memory to line L2, and returns "unknown" when it runs out.

## Example

The root A is an OR node with three AND children, B, C and D. B has a proved terminal child and an OR child X, whose two children are disproved terminals. C has an OR child Y, with a disproved and a proved terminal child, and a proved terminal child. D has one disproved terminal child. In the nested-list form of the tests, A is `[[T, [F, F]], [[F, T], T], [F]]`.

| step | selected node | after the expansion | root (pn, dn) after the step |
|---|---|---|---|
| 1 | A | B, C, D are frontier nodes, each $(1, 1)$ | $(\min(1,1,1), 1+1+1) = (1, 3)$ |
| 2 | B (first child with pn 1) | B: $(0 + 1, \min(\infty, 1)) = (1, 1)$ | $(1, 3)$ |
| 3 | X (the child of B with dn 1) | X: $(\min(\infty,\infty), 0 + 0) = (\infty, 0)$, so B: $(\infty, 0)$ | $(\min(\infty,1,1), 0+1+1) = (1, 2)$ |
| 4 | C | C: $(1 + 0, \min(1, \infty)) = (1, 1)$ | $(1, 2)$ |
| 5 | Y | Y: $(\min(\infty, 0), 0 + \infty) = (0, \infty)$, so C: $(0, \infty)$ | $(0, \infty)$: proved |

The search stops after five expansions with A proved through C. D is never expanded: once C is proved, nothing in D can change the answer. Steps 2 and 3 show the best-first character: B looked as good as C, its weak point X was found and disproved at once, and the search moved to C without finishing anything else in B.

On tic-tac-toe with X as the prover, PNS proves "X does not lose" from the empty board with 474 expansions, and disproves "X wins" with 3,323 expansions; the full game tree has 549,946 nodes ([minimax](/minimax/)). In [Nim](/nim/) with heaps $1, 2, 3$, with a position written as the sorted heap sizes and the moves to the same position merged into one child, it disproves "the player to move wins" with 39 expansions (90 when every move is a child of its own), as [Bouton's theorem](/boutons-theorem/) predicts from $1 \oplus 2 \oplus 3 = 0$.

## Correctness

The [proof](proofs/correctness/) works on the explored tree, where each frontier node is unknown.

- **Meaning of the numbers.** $\mathrm{pn}(n)$ is the least number of frontier nodes below $n$ that must be proved, with all others disproved, to prove $n$, and $\infty$ if no such set exists; $\mathrm{dn}(n)$ is the dual. This follows by induction from the rules: an OR node needs one child, so it takes the minimum; an AND node needs all children, whose subtrees are disjoint, so it takes the sum. So $\mathrm{pn}(n) = 0$ exactly when the explored tree already proves $n$, whatever the frontier nodes turn out to be, and then $\mathrm{dn}(n) = \infty$.
- **The rules hold after every step.** Expanding $m$ changes only $m$ and its ancestors, and lines L9 to L14 recompute them from the bottom up. If a node keeps its numbers, the inputs of every higher ancestor are unchanged, so the early stop in line L13 is safe.
- **Termination.** While the root numbers are both nonzero, they are finite, and the walk of lines L4 to L6 keeps both numbers finite and nonzero, so it ends at a frontier node. Each step expands a new node of a finite tree, so the loop stops. Then $\mathrm{pn}(\text{root}) = 0$ or $\mathrm{dn}(\text{root}) = 0$, and the answer is right by the meaning of the numbers.
- **Most-proving node** (Allis et al.). The selected node lies in a smallest proof set and in a smallest disproof set of the root. So proving it lowers $\mathrm{pn}(\text{root})$ by exactly 1, and disproving it lowers $\mathrm{dn}(\text{root})$ by exactly 1. The tests check this at every step on random trees.

## Complexity

The costs are in the [word RAM](/word-ram/), with each call of the move generator and of the terminal test counted as $O(1)$ per position.

**Time.** Each step expands a node that was never expanded, so a tree with $N$ interior nodes needs at most $N$ steps. A step walks down at most $d$ levels and back up at most $d$ levels, and scans at most $b$ children per level, so it costs $O(b d)$. The total is $O(N b d)$. The best case is one expansion, $O(b)$, when the root has a proved child (OR) or a disproved child (AND) among its terminal children. In the worst case PNS expands the whole tree, like [minimax](/minimax/), and pays the extra factor $d$ for walking from the root each time.

**Space.** PNS stores every generated node with its two numbers, $O(N b)$ in the worst case. This is the main limit in practice: a search of a few million expansions fills the memory, which is why [df-pn](/df-pn/) and PN² were developed.

**How it compares.** On trees with uniform branching and no forced lines, PNS has no advantage over [alpha-beta pruning](/alpha-beta-pruning/). Its strength is non-uniform trees: a forced line, where the opponent has one reply at each step, has a small proof number and is followed first, at any depth.

## Properties

- **Best-first.** The choice of the next node depends on the whole explored tree, not on a fixed depth or move order.
- **No evaluation function.** The only game knowledge is the move generator and the terminal test; the shape of the tree guides the search. Domain knowledge can still enter through the initial numbers of frontier nodes.
- **Two-valued.** It answers a yes-or-no question. A three-valued game such as tic-tac-toe needs two runs, and a numeric value needs a series of goals of the form "value at least $v$".
- **A proof comes with the answer.** When the root is proved, the explored tree contains a proof tree (a winning strategy): one proved child at each OR node and all children at each AND node. The tests check that it is valid.
- **Uses the mobility of the opponent.** An AND node with $k$ frontier children has proof number $k$, so positions where the opponent has few moves look cheap to prove.
- **Tree, not graph.** The basic algorithm treats a position reached by two move orders as two nodes. On graphs with transpositions the sums count shared subtrees twice, and on graphs with cycles the value of a position can depend on the path (the graph history interaction problem).

## Variants and improvements

The survey of Kishimoto, Winands, Müller and Saito describes these and more.

- **[Df-pn](/df-pn/).** A depth-first version with thresholds on the two numbers and a [transposition table](/transposition-table/), which, with a table that keeps every entry, expands the same most-proving nodes as PNS on trees; with a table of fixed size and a replacement rule it runs in bounded memory, at the cost of re-searching subtrees whose entries were lost.
- **PN².** A second, smaller PNS at each frontier node to compute better initial numbers, with the second-level trees thrown away; it trades time for memory.
- **Initial numbers from knowledge.** Set $\mathrm{pn}$ and $\mathrm{dn}$ of a frontier node from the number of legal moves or from an evaluation, in place of $1$ and $1$.
- **Transpositions and cycles.** Store positions in a table and handle shared subtrees and repetition, at the cost of more careful number updates.
- **Monte Carlo proof-number search.** Initialize the numbers of frontier nodes from random play-outs.

## When to use it

Use PNS to *solve* a position, that is, to prove a win or a loss, when the answer is binary and the tree is narrow along forcing lines: mate problems in chess and shogi, life-and-death problems in Go, and endgames of connection games such as [Hex](/hex-game/). It fits when memory holds the explored tree; for long searches, use [df-pn](/df-pn/). To choose a good move in a game that is far from solved, use [alpha-beta pruning](/alpha-beta-pruning/) with an evaluation function, or [Monte Carlo tree search](/monte-carlo-tree-search/).

## Pitfalls

- **Infinity arithmetic.** Use a value of $\infty$ that stays $\infty$ under addition. With a large integer in place of $\infty$, sums of several "infinite" numbers can overflow or compare wrongly.
- **Draws.** A draw is neither proved nor disproved for the goal "win". Decide which side draws count for before the search, and run a second search for the other goal.
- **Ties in the selection.** Any child with the extreme number is a correct choice, but the tie rule changes the order of expansions and the run time.
- **Memory.** The tree grows by up to $b$ nodes per step. Without a budget the search can fill the memory before it ends.
- **Terminal positions without moves.** A position where the player to move has no legal move must be terminal; an expanded node with no children would give $\min$ of an empty set.
- **Transpositions.** Merging equal positions into one node without changing the update rules gives wrong numbers along the second path, and with cycles it can give wrong answers.

## Implementations

## History

Allis, van der Meulen and van den Herik published proof-number search in 1994, building on McAllester's conspiracy numbers for minimax search, and proved that the node it selects is most-proving. A depth-first form with bounded memory, [df-pn](/df-pn/), followed, and the survey of Kishimoto, Winands, Müller and Saito in 2012 reviews twenty years of variants, including PN² and the handling of transpositions and cycles. Van den Herik and Winands give an overview of PNS and its variants in a 2008 book chapter.

## References
