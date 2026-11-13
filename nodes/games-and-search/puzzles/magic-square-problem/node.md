---
tag: DGVTGW
kind: problem
slug: magic-square-problem
name: Magic square problem
aliases:
- Magic squares
area: games-and-search/puzzles
level: intro
summary: Place 1 to n squared in an n by n grid so that all rows, columns and both diagonals have the same sum. Squares exist for every n of 3 or more and are built in O(n^2) time.
prereqs: []
see_also: [latin-square-completion, counting-latin-squares, burnside-lemma, n-queens-problem, constraint-satisfaction-problem, generic-backtracking-algorithm, brute-force-search, simulated-annealing]
sources:
  - paper: "Simon de La Loubère, Du Royaume de Siam, Paris, 1691; English translation, A New Historical Relation of the Kingdom of Siam, London, 1693"
    locator: the account of magic squares, with the method for odd orders
  - url: https://oeis.org/A006052
    title: OEIS A006052, number of magic squares of order n composed of the numbers from 1 to n^2, counted up to rotations and reflections
    locator: the values 1, 0, 1, 880, 275305224 and 17753889197660635632, with the comments on Frénicle (1693), Schroeppel (1973) and Mino (2024)
  - paper: doi:10.1142/S0129183198000443
    title: Klaus Pinn and Christian Wieczerkowski, Number of magic squares from parallel tempering Monte Carlo, International Journal of Modern Physics C 9(4), 1998, 541 to 546
    locator: the Monte Carlo estimate of the number of order 6 squares
---

The magic square problem asks for an arrangement of the numbers $1, 2, \ldots, n^2$ in an $n \times n$ grid such that every row, every column and both main diagonals have the same sum, the *magic constant* $n(n^2 + 1)/2$. Such a square exists for $n = 1$ and every $n \ge 3$, and none exists for $n = 2$. Three classical methods build one in $O(n^2)$ time: the Siamese method for odd $n$, the complement method for $n$ divisible by 4, and Conway's LUX method for $n = 4m + 2$. Counting all squares is much harder: there are 880 of order 4 and 275,305,224 of order 5, up to rotation and reflection.

## In plain words

Write the numbers 1 to 9 in a 3 by 3 grid so that each row, each column and each of the two corner to corner lines adds up to 15. There is one way to do it, if you count turned and mirrored copies as the same.

The same task works for any size from 3 up. For each size there is a simple rule that writes the numbers one after another and always gives a correct square.

Finding one square is easy. Finding all of them is hard, because their number grows very fast: 880 for size 4, and more than 275 million for size 5.

## Definition

A *normal magic square of order $n$* is an $n \times n$ matrix $A$ whose entries are $1, \ldots, n^2$, each once, such that

$$\sum_{j} A_{ij} = \sum_{i} A_{ij} = \sum_{i} A_{ii} = \sum_{i} A_{i, n-1-i} = M_n \quad \text{for all } i, j.$$

Summing all $n$ rows gives $n M_n = 1 + 2 + \cdots + n^2 = n^2(n^2 + 1)/2$, so $M_n = n(n^2 + 1)/2$: 15 for $n = 3$, 34 for $n = 4$, 65 for $n = 5$.

- **Construction.** Given $n$, output a magic square of order $n$.
- **Counting.** The number of magic squares of order $n$, usually up to the 8 rotations and reflections of the square.
- **Completion.** Given some entries, fill the rest. This is a [constraint satisfaction problem](/constraint-satisfaction-problem/) with an all-different constraint on the entries and $2n + 2$ sum constraints.

*No square of order 2.* The rows $a + b = c + d$ and the column $a + c = b + d$ give $b = c$.

## Variants

- **Semi-magic squares.** Only the rows and columns must sum to $M_n$.
- **Associative squares.** Every pair of cells symmetric about the center sums to $n^2 + 1$. The Siamese squares are associative.
- **Pandiagonal squares.** The broken diagonals, which wrap around the edges, also sum to $M_n$. There is none of order 3.
- **Other entries.** Any distinct integers, or primes, with equal line sums. Multiplying every entry by $a$ and adding $b$ keeps a square magic.
- **Magic cubes** and higher dimensions, with lines in every axis direction.

## Examples

**Order 3, the Lo Shu.** The Siamese method gives the square on the left. All 8 magic squares of order 3 are its rotations and reflections, and Frénicle's standard form, with the smallest corner at the top left and its right neighbor smaller than the cell below it, is on the right.

```
8 1 6        2 7 6
3 5 7        9 5 1
4 9 2        4 3 8
```

*Proof that there is only one up to symmetry.* The four lines through the center add up to $4 \cdot 15 = 60$ and count the center four times and every other cell once, so $45 + 3c = 60$ and $c = 5$. The partner of each cell across the center is then $10$ minus that cell. If 1 were in a corner, the row and the column through it would each need two other cells with sum 14. The only such pairs are $5 + 9$ and $6 + 8$, and 5 is in the center and 9 in the opposite corner, so only $6 + 8$ is left for two lines. So 1 is in the middle of a side, 9 is across from it, and the side through 1 holds 6 and 8 in its corners. The partner rule and the line sums then fix every other cell. The 4 places of 1 and the 2 orders of 6 and 8 are the 8 symmetries.

**Order 4, the complement method.** Write 1 to 16 in order and replace $v$ by $17 - v$ on the two main diagonals:

```
16  2  3 13
 5 11 10  8
 9  7  6 12
 4 14 15  1
```

**Order 6, the LUX method.** From the Siamese square of order 3, rows lettered L L L, L U L, U L U:

```
32 29  4  1 24 21
30 31  2  3 22 23
12  9 17 20 28 25
10 11 18 19 26 27
13 16 36 33  5  8
14 15 34 35  6  7
```

## Known algorithms

**Construction for every order.**

```pseudo id=main
MAGIC-SQUARE(n)
L1  if n is odd then start in the middle of the top row, and put each next number one step up and right with wraparound, or one step down if that cell is full
L2  else if n mod 4 = 0 then
L3      write 1 to n^2 row by row
L4      replace v by n^2 + 1 - v in each cell that lies on a diagonal of its 4 by 4 block
L5  else n = 4m + 2:
L6      build the Siamese square S of order 2m + 1; letter its rows m + 1 times L, once U, m - 1 times X; swap the letters of the center cell and the cell below it
L7      replace each cell v of S by a 2 by 2 block holding 4(v - 1) + 1 to 4(v - 1) + 4 in the order of its letter: L is 4 1 / 2 3, U is 1 4 / 2 3, X is 1 4 / 3 2
L8  return the square
```

Each method writes every cell once, so the time is $O(n^2)$, the size of the output.

*Siamese method, correctness.* Let $c_0 = (n - 1)/2$ and write $v - 1 = qn + r$ with $0 \le q, r < n$. Within a run of $n$ numbers the moves go up and right, and the step after the run goes down, so $v$ lands in row $i \equiv 2q - r$ and column $j \equiv c_0 + r - q \pmod n$. The map $(q, r) \mapsto (i, j)$ has determinant 1, so it is a bijection, and the cell checked at the end of each run is the full cell where that run started. In row $i$, $r \equiv 2q - i$, and since 2 is invertible modulo odd $n$, $q$ and $r$ each take all $n$ values once; columns are the same with $r \equiv q + j - c_0$. So each line sums to $n \cdot n(n - 1)/2 + n(n - 1)/2 + n = M_n$. On the anti-diagonal $q = c_0$ is fixed and $r$ takes all values, which gives $M_n$ again. On the main diagonal $q \equiv 2i - c_0$ takes all values and $r \equiv 3i + 1$; if 3 does not divide $n$ these are all residues, and if $n = 3t$ they are the residues $1, 4, \ldots, 3t - 2$ three times each, whose sum is also $n(n - 1)/2$.

*Complement method, correctness.* Call a cell *marked* when its row and its column are both, or both not, $\equiv 0$ or $3 \pmod 4$. The map $c \mapsto n - 1 - c$ sends residues $0, 1, 2, 3$ to $3, 2, 1, 0$, so the marked cells are symmetric about the center, and a mirrored pair holds $v$ and $n^2 + 1 - v$; so complementing swaps values within pairs and every number still appears once. In row $r$, columns $c$ and $n - 1 - c$ have the same mark, and the marked columns are half of the row, so $n/4$ of the $n/2$ column pairs are complemented. Every pair of row $r$ holds $P = 2rn + n + 1$ before the change and $2(n^2 + 1) - P$ after it, so the row sums to $\frac{n}{4} P + \frac{n}{4}(2(n^2 + 1) - P) = M_n$. Columns are the same. Both main diagonals are fully marked; on the main diagonal the new values sum to $n(n^2 + 1) - \sum_i (i(n + 1) + 1) = M_n$, and the anti-diagonal is the same by the same count.

*LUX method, correctness.* With $k = 2m + 1$, a block holding $v$ adds $8(v - 1)$ plus a pattern sum to each of its two rows, two columns and its diagonal. Every pattern has row sums 5 and 5. Column sums are 6, 4 for L, 3, 7 for U and 4, 6 for X; every column of $S$ has $m + 1$ letters L, one U and $m - 1$ letters X, even the middle one after the swap, so both columns of the block column get $6(m + 1) + 3 + 4(m - 1) = 4(m + 1) + 7 + 6(m - 1) = 5k$. On the main diagonal the patterns add 7, 4 and 3, and the blocks there are $m$ L, two U and $m - 1$ X, again $5k$; on the anti-diagonal they add 3, 6 and 7 over $m$ L, two U and $m - 1$ X, again $5k$. Since $S$ is magic, every line sums to $8(M_k - k) + 5k = 4k^3 + k = M_{2k}$. Without the swap, the main diagonal would get $10m + 8$ instead of $5k = 10m + 5$.

**Counting.** Brute force tries all $(n^2)!$ arrangements, which is feasible for $n = 3$ only. A [backtracking](/generic-backtracking-algorithm/) search that fills a row, a column and the diagonals first and forces the last cell of each line by its sum counts the 880 squares of order 4; it keeps only squares in Frénicle's form, so it counts each class of 8 once, and it chooses only 8 of the 16 cells, since the line sums force the others. For orders 5 and 6, exact counts took much larger searches, and Monte Carlo methods estimate the count for larger orders (Pinn and Wieczerkowski 1998).

**Completion and search.** A partial square is completed by backtracking with propagation on the line sums, or by [simulated annealing](/simulated-annealing/) on the total deviation of the line sums from $M_n$.

## Bounds

- **Existence.** For $n = 1$ and all $n \ge 3$, by the three methods; never for $n = 2$.
- **Construction.** $\Theta(n^2)$ time, the size of the output.
- **Counts up to symmetry** (OEIS A006052):

| $n$ | Squares | Source |
| --- | --- | --- |
| 3 | 1 | classical |
| 4 | 880 | Frénicle (1693) |
| 5 | 275,305,224 | Schroeppel (1973) |
| 6 | 17,753,889,197,660,635,632 | Mino (2024) |

Each square has 8 distinct images under the symmetries of the square, so there are 8 and 7040 squares of orders 3 and 4 in total. No formula for the count is known.

## Reductions

- **To a CSP.** Completion is a CSP with $n^2$ variables of domain $\{1, \ldots, n^2\}$, one all-different constraint and $2n + 2$ linear constraints, so it has an integer programming and a [SAT](/sat/) encoding.
- **From Latin squares.** If $A$ and $B$ are Latin squares of order $n$ on $\{0, \ldots, n - 1\}$ that are orthogonal, that is, every pair $(A_{ij}, B_{ij})$ occurs once, and both have each symbol once on each main diagonal, then $nA + B + 1$ is a magic square. See [Latin square completion](/latin-square-completion/).
- **Symmetry.** Counting up to symmetry divides by 8 here; for general symmetry groups, [Burnside's lemma](/burnside-lemma/) counts orbits.

## Applications

- **Recreational mathematics and history.** The Lo Shu of order 3 comes from ancient Chinese tradition, and magic squares appear in art, such as the order 4 square in Dürer's engraving Melencolia I.
- **Test problems.** Completion and counting of magic squares are used as test problems for constraint solvers and for exhaustive enumeration.

## References
