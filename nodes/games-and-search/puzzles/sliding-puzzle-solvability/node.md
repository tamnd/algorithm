---
tag: 9Q436M
kind: theorem
slug: sliding-puzzle-solvability
name: Sliding puzzle solvability criterion
aliases:
- Parity criterion for the 15 puzzle
area: games-and-search/puzzles
level: intro
summary: "On a w by h board with w, h >= 2, one arrangement of the sliding puzzle reaches another exactly when the inversion parity, plus the blank's row when w is even, is the same."
prereqs: [permutation-parity, inversion]
see_also: [sliding-tile-puzzle, permutation-sign, permutation-cycles, symmetric-group, invariant, implicit-graph, breadth-first-search, biconnected-graph]
sources:
  - paper: "Wm. Woolsey Johnson and William E. Story, Notes on the 15 puzzle, American Journal of Mathematics 2(4), 1879"
    locator: "pp. 397-404; Johnson proves that the parity is invariant, Story proves that it is the only obstruction"
  - paper: doi:10.2307/2589612
    title: "Aaron F. Archer, A modern treatment of the 15 puzzle, American Mathematical Monthly 106(9), 1999"
    locator: "pp. 795-797 for a proof with permutation cycles, pp. 798-799 for Wilson's theorem"
  - paper: "Richard M. Wilson, Graph puzzles, homotopy, and the alternating group, Journal of Combinatorial Theory, Series B 16(1), 1974"
    locator: "pp. 86-96, the main theorem on 2-connected graphs"
---

The sliding puzzle solvability criterion is the theorem that tells, for two arrangements of the tiles of a [sliding tile puzzle](/sliding-tile-puzzle/) on a board of at least 2 rows and 2 columns, whether a sequence of moves turns one into the other. The test is a [parity](/permutation-parity/): count the [inversions](/inversion/) of the tiles in reading order, add the row of the blank when the board has an even number of columns, and compare the parities of the two sums. The arrangements are mutually reachable exactly when the parities are equal, so exactly half of all arrangements can be solved. Johnson and Story proved the theorem in 1879 for the 15 puzzle; Wilson extended it in 1974 to the same puzzle on any graph.

## Statement

The board has $h \ge 2$ rows and $w \ge 2$ columns, so it has $N = wh$ cells. An arrangement puts the $N - 1$ tiles $1, \dots, N - 1$ and one blank on the cells, one item to a cell. A move slides a tile into the blank from a cell that shares a side with it, so the tile and the blank change places. Number the rows $0, \dots, h - 1$ from the top. For an arrangement $c$:

| Symbol | Meaning |
|---|---|
| $\pi(c)$ | the sequence of the $N - 1$ tiles in reading order (row by row, left to right in each row), with the blank left out |
| $\operatorname{inv}(c)$ | the number of inversions of $\pi(c)$: the pairs of tiles in which the larger number comes first |
| $r(c)$ | the row of the blank |
| $I(c)$ | $\operatorname{inv}(c) \bmod 2$ if $w$ is odd, and $(\operatorname{inv}(c) + r(c)) \bmod 2$ if $w$ is even |

**Theorem.** Let $w, h \ge 2$ and let $c$ and $c'$ be arrangements on the $w \times h$ board. A sequence of moves turns $c$ into $c'$ if and only if $I(c) = I(c')$. Each of the two values of $I$ is taken by exactly $N!/2$ arrangements, so the graph of arrangements and moves has exactly two [connected components](/connected-components/), of $N!/2$ arrangements each.

The standard goal has the tiles in order and the blank in the bottom right corner, so $\operatorname{inv} = 0$ and $r = h - 1$. Counting the row of the blank from the bottom instead, with the bottom row as row 1, the theorem gives the usual rule:

- $w$ odd: $c$ is solvable if and only if $\operatorname{inv}(c)$ is even.
- $w$ even: $c$ is solvable if and only if $\operatorname{inv}(c)$ plus the row of the blank counted from the bottom is odd.

## In plain words

If you slide tiles into the gap long enough, you might expect to reach every arrangement. You cannot. Each arrangement carries a hidden yes or no mark, and no move changes it. The mark comes from the number of pairs of tiles that are in the wrong order when you read the board line by line. On a board with an odd number of columns, a sideways slide does not change that count, and an up or down slide changes it by an even amount. On a board with an even number of columns, an up or down slide changes the count by an odd amount, but it also moves the gap to the next row, and the two changes cancel. The theorem says that this mark is the only obstacle. Two arrangements with the same mark always reach each other, so exactly half of all arrangements can be solved.

## Proof

The proof has three parts: $I$ does not change under a move, every even permutation of the tiles can be made with the blank kept at one fixed cell, and the two parts together give the theorem. A permutation is even when it is a product of an even number of transpositions; it is a standard fact that the parity of $\operatorname{inv}$ changes when two entries of a sequence change places, so two orders of the same tiles have inversion counts of the same parity exactly when the permutation between them is even (see [permutation parity](/permutation-parity/)).

### Part 1: no move changes $I$

A horizontal move exchanges the blank with a tile in the same row. The reading order of the tiles, with the blank left out, does not change, and the blank stays in its row. So $\operatorname{inv}$, $r$ and $I$ do not change.

A vertical move takes the tile at reading position $p + w$ to reading position $p$, where the blank was (or the reverse). The tiles at the positions $p + 1, \dots, p + w - 1$ stay where they are, and the moving tile passes over all $w - 1$ of them in $\pi$. Moving one entry of a sequence past one adjacent entry changes the number of inversions by exactly 1, so the move changes $\operatorname{inv}$ by $w - 1$ steps of $\pm 1$, and $\operatorname{inv} \bmod 2$ changes by $(w - 1) \bmod 2$. The row of the blank changes by 1. If $w$ is odd, $w - 1$ is even, so $\operatorname{inv} \bmod 2$ does not change, and $I = \operatorname{inv} \bmod 2$ does not change. If $w$ is even, $\operatorname{inv} \bmod 2$ and $r \bmod 2$ both change, so their sum $I$ does not change.

So $I(c) = I(c')$ when $c$ reaches $c'$. This proves the "only if" direction.

### Part 2: the group of moves that return the blank

Let $z$ be the bottom right cell and let $X$ be the set of the other $N - 1$ cells. Each sequence of moves that starts and ends with the blank on $z$ permutes the tiles on $X$; let $G$ be the set of these permutations of $X$. $G$ is a group: two such sequences can be done one after the other, and a sequence done backwards undoes it. A permutation of $X$ is even when it is a product of an even number of transpositions of cells. We show that $G$ contains every even permutation of $X$.

**Lemma 1 (3-cycles).** Every even permutation of a finite set is a product of 3-cycles.

*Proof.* Write the permutation as a product of an even number of transpositions and group them in pairs. A pair with equal factors is the identity. A pair with one common point is a 3-cycle: $(a\,b)(a\,c) = (a\,c\,b)$. A pair with no common point is a product of two 3-cycles: $(a\,b)(c\,d) = (a\,c\,b)(a\,c\,d)$. (Products act from right to left.) $\square$

**Lemma 2 (growing the alternating set).** Let $H$ be a group of permutations of a set $X = \{x_1, \dots, x_m\}$ with $m \ge 3$. Assume that $H$ contains a 3-cycle on $\{x_1, x_2, x_3\}$, and that for each $k$ with $4 \le k \le m$ it contains a 3-cycle $(x_a\,x_b\,x_k)$ with $a, b < k$. Then $H$ contains every even permutation of $X$.

*Proof.* Let $X_k = \{x_1, \dots, x_k\}$. We show by induction on $k$ that $H$ contains every 3-cycle on $X_k$; Lemma 1 then gives the claim for $k = m$. For $k = 3$, the 3-cycle in $H$ and its inverse are the only two 3-cycles on $X_3$. For $k \ge 4$, a 3-cycle on $X_k$ that does not move $x_k$ is in $H$ by the induction hypothesis. A 3-cycle that moves $x_k$ has the form $(x_p\,x_q\,x_k)$ with $p \ne q$ and $p, q < k$. Let $t = (x_a\,x_b\,x_k)$ be the given 3-cycle. If $g$ is a permutation that fixes $x_k$, then $g t g^{-1} = (g(x_a)\,g(x_b)\,x_k)$. If $k - 1 \ge 4$, choose a permutation $g$ of $X_{k-1}$ with $g(x_a) = x_p$ and $g(x_b) = x_q$; if it is odd, compose it with the transposition of two points of $X_{k-1}$ other than $x_p$ and $x_q$, which exist because $k - 1 \ge 4$. Then $g$ is even, so $g \in H$ by the induction hypothesis and Lemma 1, and $g t g^{-1} = (x_p\,x_q\,x_k) \in H$. If $k = 4$, the even permutations of $X_3$ are the identity, $\rho = (x_1\,x_2\,x_3)$ and $\rho^2$. Conjugating $t = (x_a\,x_b\,x_4)$ by them gives the 3-cycles $(x_p\,x_q\,x_4)$ for the three pairs $(p, q)$ obtained by rotating $(a, b)$, and conjugating $t^{-1} = (x_b\,x_a\,x_4)$ gives the three pairs obtained by rotating $(b, a)$. These are all six ordered pairs of distinct indices from $\{1, 2, 3\}$. $\square$

**Lemma 3 (3-cycles from the board).** Let $B$ be a $2 \times 2$ block of cells, let $u \in B$, and assume that there is a path of cells $z = v_0, v_1, \dots, v_\ell = u$, each sharing a side with the next, that meets $B$ only in $u$. Then $G$ contains both 3-cycles on the three cells of $B \setminus \{u\}$.

*Proof.* Move the blank along the path from $z$ to $u$. Each tile on the path moves one cell back along it, and no tile of $B \setminus \{u\}$ moves. Then move the blank once around the 4-cycle of cells of $B$, back to $u$; this moves each of the three tiles of $B \setminus \{u\}$ one cell along the cycle, which is a 3-cycle on $B \setminus \{u\}$, and it moves no other tile. Then move the blank back along the path to $z$; this undoes the shifts of the first step and does not touch $B \setminus \{u\}$. The net effect is the 3-cycle. Going around $B$ the other way gives its inverse. $\square$

Now list the cells of $X$ in an order that meets the conditions of Lemma 2. Write $(i, j)$ for the cell in row $i$ and column $j$, so $z = (h - 1, w - 1)$.

1. The first three cells are $(h - 2, w - 2)$, $(h - 2, w - 1)$ and $(h - 1, w - 2)$. Lemma 3 with the block of these cells and $z$, and with $u = z$ and the path of length 0, gives a 3-cycle on them.
2. For $j = w - 3, w - 4, \dots, 0$, add $p = (h - 2, j)$ and then $q = (h - 1, j)$. Let $B$ be the block in rows $h - 2$ and $h - 1$ and columns $j$ and $j + 1$, and let $a = (h - 2, j + 1)$ and $b = (h - 1, j + 1)$, which are already listed. The path from $z$ to the left along the bottom row ends at $b$ and meets $B$ only in $b$; the path from $z$ up one cell and then to the left along row $h - 2$ ends at $a$ and meets $B$ only in $a$. By Lemma 3, $G$ contains $t_1 = (p\,q\,a)$ and $t_2 = (p\,q\,b)$. A direct computation gives $t_1 t_2^{-1} = (b\,a\,p)$, which is the 3-cycle that Lemma 2 needs for $p$, and $t_1 = (p\,q\,a)$ is the 3-cycle it needs for $q$.
3. For $i = h - 3, h - 4, \dots, 0$, add the cells of row $i$ from right to left. The first two cells, $p = (i, w - 1)$ and $q = (i, w - 2)$, are handled as in step 2 with $a = (i + 1, w - 1)$ and $b = (i + 1, w - 2)$: the path from $z$ up column $w - 1$ ends at $a$, and the path from $z$ one cell to the left and then up column $w - 2$ ends at $b$, and each meets the block in rows $i, i + 1$ and columns $w - 2, w - 1$ only at its end. For a later cell $x = (i, j)$ with $j \le w - 3$, take the block $B$ in rows $i, i + 1$ and columns $j, j + 1$ and $u = (i + 1, j)$. The path from $z$ to the left along the bottom row to $(h - 1, j)$ and then up column $j$ to $u$ meets $B$ only in $u$, because $i + 1 \le h - 2$. Lemma 3 gives a 3-cycle on $x$, $(i, j + 1)$ and $(i + 1, j + 1)$, and the last two are already listed.

Every cell of $X$ is listed once, so Lemma 2 applies with $H = G$, and $G$ contains every even permutation of $X$.

### Part 3: the theorem

Let $I(c) = I(c')$. The cells form a connected grid, so moves take the blank of $c$ to $z$, which gives an arrangement $d$, and moves take the blank of $c'$ to $z$, which gives $d'$. By Part 1, $I(d) = I(c) = I(c') = I(d')$. The blank is on $z$ in both, so $r(d) = r(d')$ and therefore $\operatorname{inv}(d) \equiv \operatorname{inv}(d') \pmod 2$. The permutation of $X$ that turns the tiles of $d$ into those of $d'$ is therefore even, so by Part 2 a sequence of moves turns $d$ into $d'$. Moves can be undone, so $c$ reaches $d$, $d$ reaches $d'$, and $d'$ reaches $c'$. This proves the "if" direction.

For the count, exchanging the tiles 1 and 2 changes $\operatorname{inv}$ by an odd amount and does not move the blank, so it changes $I$. It is a bijection of the set of arrangements onto itself that maps each class of $I$ onto the other, so both classes have $N!/2$ arrangements. Each class is connected by the "if" direction, and no move joins the two classes by Part 1. $\blacksquare$

## Consequences

**Examples.** On the $4 \times 4$ board, the arrangement with 14 and 15 exchanged and the blank in the bottom right corner has one inversion, and the blank is in row 1 from the bottom. The sum 2 is even, so no sequence of moves solves it. The arrangement with the blank first and the tiles $1, \dots, 15$ after it in reading order has no inversions and the blank in row 4 from the bottom, so it is also in the other class: on a board of even width, the goal "blank in the top left corner" and the goal "blank in the bottom right corner" are not reachable from each other. On the $3 \times 3$ board the same two goals are reachable from each other, because the width is odd and both have no inversions. The $3 \times 3$ arrangement with rows 8 6 7, 2 5 4 and 3, blank, 1 has 24 inversions, so it is solvable; it is one of the two arrangements at the largest distance, 31 moves, from the standard goal.

**Counts.** The number of arrangements that reach the standard goal is $N!/2$:

| Board | Arrangements | Reachable from the goal |
|---|---|---|
| $2 \times 2$ | 24 | 12 |
| $2 \times 3$ | 720 | 360 |
| $2 \times 4$ | 40,320 | 20,160 |
| $3 \times 3$ | 362,880 | 181,440 |
| $4 \times 4$ | 20,922,789,888,000 | 10,461,394,944,000 |
| $5 \times 5$ | $25!$ | $25!/2 \approx 7.76 \times 10^{24}$ |

**A linear-time test.** The parity of $\operatorname{inv}$ equals the parity of $(N - 1)$ minus the number of [cycles](/permutation-cycles/) of the permutation, so one pass that follows the cycles decides solvability in $O(N)$ time, where counting the inversions pair by pair takes $O(N^2)$ time. Deciding whether an instance is solvable is therefore easy, while finding a shortest solution is NP-hard (see [sliding tile puzzle](/sliding-tile-puzzle/)).

**Search.** A search for a solution from an unsolvable arrangement explores the whole component, which is $N!/2$ states, before it stops. A solver must run the parity test first. The same parity also limits the state space that a [breadth-first search](/breadth-first-search/) or a [pattern database](/pattern-database/) has to cover: only one class is relevant.

**Any goal.** The theorem compares two arbitrary arrangements, so it also covers goals with the blank in another cell or the tiles in another order.

## Tightness

**Both dimensions at least 2.** On a board with one row or one column, tiles cannot pass each other, so the order of the tiles never changes and an arrangement reaches only the $N$ arrangements that differ from it in the position of the blank. The parity condition is then far from sufficient.

**Other graphs.** The same puzzle can be played on any connected graph, with one tile or the blank on each vertex and a move along an edge. Wilson's theorem describes every [2-connected](/biconnected-graph/) graph on $n \ge 3$ vertices. If the graph is a cycle, the tiles can only rotate, and there are $(n - 2)!$ classes. If the graph is [bipartite](/bipartite-graph/) and not a cycle, the reachable permutations with the blank fixed are exactly the even ones, and there are 2 classes; the grid with $w, h \ge 2$ is such a graph, except for the $2 \times 2$ grid, which is a 4-cycle and has $(4 - 2)! = 2$ classes. If the graph is not bipartite and not a cycle, every permutation is reachable and there is 1 class, with one exception: the graph $\theta_0$ on 7 vertices, two vertices of degree 3 joined by paths of 2, 3 and 3 edges. On $\theta_0$ the reachable permutations of the 6 tiles form a group of order 120, isomorphic to the symmetric group on 5 points, so there are $720/120 = 6$ classes. The theta graphs with paths of 1, 3 and 4 edges and of 1, 2 and 5 edges are also on 7 vertices and not bipartite, and they give all $6! = 720$ permutations, as the theorem says.

## History

In two notes printed together in the American Journal of Mathematics in 1879, Johnson proved that the parity is invariant, so that half of the arrangements cannot be solved, and Story proved that every arrangement with the right parity can be solved. Wilson (1974) put the result into a theorem on all 2-connected graphs and found the exceptional graph $\theta_0$. Archer (1999) gave a short modern proof of the rectangular case with permutation cycles.

## References
