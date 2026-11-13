---
tag: YQFNF0
kind: theorem
slug: gods-number
name: God's number
aliases:
- God's number for the Rubik's Cube
area: games-and-search/puzzles
level: advanced
summary: "The largest number of moves that a Rubik's Cube position needs: 20 face turns in the half turn metric (2010) and 26 quarter turns in the quarter turn metric (2014), both by computer."
prereqs: [rubiks-cube-problem, subgroup, breadth-first-search]
see_also: [rubiks-cube-problem, kociemba-algorithm, counting-argument, finite-group, symmetry-reduction, set-cover, bidirectional-search, pattern-database]
sources:
  - paper: doi:10.1137/140973499
    title: "Tomas Rokicki, Herbert Kociemba, Morley Davidson and John Dethridge, The diameter of the Rubik's Cube group is twenty, SIAM Review 56(4), 2014"
    locator: "pp. 645-670, the proof that every position can be solved in 20 face turns"
  - url: "https://www.cube20.org/"
    locator: "the main page: the table of bounds since 1981, the 2,217,093,120 cosets, the reduction to 55,882,296 sets, and the 35 CPU-years"
  - url: "https://www.cube20.org/qtm/"
    locator: "the main page: the 2014 proof of 26 in the quarter turn metric and the table of bounds in that metric"
  - paper: "Tomas Rokicki, Twenty-five moves suffice for Rubik's Cube, arXiv:0803.3435, 2008"
    locator: "pp. 3-6: Kociemba's algorithm, Reid's bounds of 12 and 18 moves for the two phases, Table 1 with the distances inside the subgroup H, and Algorithm 2, the set solver with one bit per position"
  - paper: "Michael Reid, Superflip requires 20 face turns, cube-lovers e-mail, January 18, 1995"
    locator: "cited as reference 7 of Rokicki 2008; the message itself was not checked"
  - paper: doi:10.1007/978-3-642-23719-5_58
    title: "Erik D. Demaine, Martin L. Demaine, Sarah Eisenstat, Anna Lubiw and Andrew Winslow, Algorithms for solving Rubik's Cubes, ESA 2011, LNCS 6942"
    locator: "pp. 689-700, the diameter Θ(n^2 / log n) of the n by n by n cube"
---

God's number is the largest number of moves that any position of the [Rubik's Cube](/rubiks-cube-problem/) needs: the diameter of the graph whose vertices are the positions and whose edges are single moves. It is 20 when every turn of a face counts as one move, and 26 when only quarter turns count. Both values were found by computer searches that used about 35 and 29 CPU-years, in 2010 and 2014, and this page cites them; it does not repeat them. The name comes from the idea of an all-knowing solver that always uses a shortest solution.

## Statement

The cube group $G$ is the set of positions that face turns reach from the solved cube $e$, with

$$|G| = \frac{8!\, 3^7\, 12!\, 2^{11}}{2} = 43{,}252{,}003{,}274{,}489{,}856{,}000.$$

A metric is a set of generators. The half turn metric (HTM) has the 18 moves $S$: each of the 6 faces turned by a quarter turn either way or by a half turn. The quarter turn metric (QTM) has the 12 quarter turns $Q$. For a set $T$ of generators the distance $d_T(g)$ is the least $k$ with $g = t_1 t_2 \cdots t_k$, $t_i \in T$.

**Theorem.** $\max_{g \in G} d_S(g) = 20$ and $\max_{g \in G} d_Q(g) = 26$.

Both sets of generators are closed under inverses, so $d_T(g) = d_T(g^{-1})$, and the maxima are the diameters of the [Cayley graphs](/finite-group/) of $G$ for $S$ and for $Q$.

## In plain words

Mix up a Rubik's Cube in any way you like. Some ways need more moves to undo than others. God's number is the count for the worst mix of all: every position can be solved in that many moves, and some position needs all of them. If a turn by a half turn counts as one move, the number is 20. If only quarter turns count, it is 26. Nobody found these numbers by hand. A simple count shows that some position needs at least 18 moves, and a hard position found in 1995 needs 20. To show that 20 always suffice, a team split the positions into about two billion large blocks, solved every block with a fast solver, and used symmetry to skip most blocks. The full run used Google computers for a few weeks.

## Proof

The proof has a lower bound by counting, a lower bound by one position, and an upper bound by an exhaustive computation. This page describes the computation and does not repeat it.

### Lower bound by counting

Every position at distance $k$ is the result of some sequence of $k$ moves that is *canonical*: no two neighbouring moves turn the same face (they would merge into one move or none), and two neighbouring turns of opposite faces, which commute, come in a fixed order. With the order U before D, R before L and F before B, HTM has 18 choices for the first move, 15 after a turn of U, R or F (any other face), and 12 after a turn of D, L or B (any face but that one and its opposite). The counts $c_k$ of canonical sequences of length $k$ are

| $k$ | 0 | 1 | 2 | 3 | 4 | 17 | 18 |
|---|---|---|---|---|---|---|---|
| $c_k$ | 1 | 18 | 243 | 3,240 | 43,254 | $\approx 1.85 \times 10^{19}$ | $\approx 2.47 \times 10^{20}$ |
| positions at distance $k$ | 1 | 18 | 243 | 3,240 | 43,239 | | |

and $c_k$ grows by a factor of about 13.35 for each move. Since $\sum_{k \le 17} c_k \approx 2.00 \times 10^{19} < |G|$, the [counting argument](/counting-argument/) shows that some position needs at least 18 moves. The breadth-first layers in the table show that the canonical sequences differ in result up to length 3 and first collide at length 4.

In QTM a canonical sequence may also repeat a quarter turn once in the same direction, since two of them make a half turn. The same count gives $\sum_{k \le 19} c_k \approx 9.58 \times 10^{18} < |G|$, so some position needs 20 quarter turns. Parity gives one more: a quarter turn moves the corners by a 4-cycle, which is an odd permutation, so a position whose corner permutation is odd lies at an odd distance, and half of $G$ consists of such positions. The canonical sequences of odd length up to 19 are fewer than $|G|/2$, so some position needs at least 21 quarter turns.

### Lower bound by one position

The *superflip* has every piece in its place with every edge flipped. Reid showed in 1995 by a computer search that it needs 20 face turns, so $\max d_S \ge 20$. In QTM, the superflip composed with the pattern called *fourspot* needs 26 quarter turns, which Reid showed in 1998.

### Upper bound by computation

The computation uses the subgroup $H = \langle U, D, R2, L2, F2, B2 \rangle$ of [Kociemba's two-phase algorithm](/kociemba-algorithm/). It has $|H| = 19{,}508{,}428{,}800$ elements, so $G$ splits into $|G|/|H| = 2{,}217{,}093{,}120$ cosets of $H$. The steps were:

1. **Fewer cosets.** The 16 symmetries of the cube that keep the U-D axis map cosets of $H$ to cosets and keep distances, which leaves about 139 million cosets up to symmetry. The same position has three such cosets, one for each axis, so only enough cosets to cover every position must be solved, a [set cover](/set-cover/). This leaves 55,882,296 cosets.
2. **One coset at a time.** For a coset, the set solver keeps a bitmap with one bit per position, 19,508,428,800 bits, for the positions known to be solvable in at most $d$ moves. For $d = 0, 1, 2, \dots$ it first marks every position one move of $H$ beyond a marked one, by a scan of the whole bitmap with the ten moves $U, U2, U', D, D2, D', R2, L2, F2, B2$. Then it lists, as in phase 1 of Kociemba's algorithm, the sequences of $d$ moves that take the whole coset into $H$; each one solves exactly one position of the coset, which it marks. When every bit is set, every position of the coset is within $d$ moves.
3. **Scale.** Each coset took about 20 seconds, the whole run about 35 CPU-years, and Google ran it in a few weeks in July 2010.

Every one of the $|G|$ positions was thus shown to have a solution of at most 20 moves. Together with the superflip this gives $\max d_S = 20$. In August 2014 Rokicki and Davidson used the same 55,882,296 cosets with quarter turns, about 29 CPU-years, to show that every position has a solution of at most 26 quarter turns, and the superflip with fourspot gives $\max d_Q = 26$.

## Consequences

- **Optimal solvers stop at 20.** A search for a shortest solution, such as Kociemba's algorithm run to the end, or Korf's [IDA\*](/iterative-deepening-a-star/) with [pattern databases](/pattern-database/), never needs to look beyond depth 20 in HTM.
- **Few positions at the top.** cube20.org estimates that about 490 million positions are at distance 20, about one in $10^{11}$ of $|G|$.
- **Larger cubes.** For the $n \times n \times n$ cube the diameter is $\Theta(n^2 / \log n)$ (Demaine et al. 2011). The lower bound is a counting argument like the one above, and the upper bound moves many pieces in parallel.
- **The 2 by 2 by 2 cube.** The same question for the cube with only corner pieces can be settled by direct [breadth-first search](/breadth-first-search/). Fix one corner and turn only the three faces away from it; that gives all $7!\, 3^6 = 3{,}674{,}160$ positions. The search finds diameter 11 in HTM, with 2,644 positions at distance 11, and diameter 14 in QTM, with 276 positions at distance 14.

## Tightness

The two lower bounds by counting, 18 and 21, are below the true values 20 and 26. The gap comes from the many distinct canonical sequences that give the same position, which the count treats as different. The bounds by single positions are tight: there are positions at distance 20 in HTM and at distance 26 in QTM, and the computation shows there are none further out. In QTM, superflip with fourspot is the only known position at distance 26, up to rotations of the whole cube.

## History

The table lists the HTM bounds on cube20.org.

| Date | Lower | Upper | By |
|---|---|---|---|
| July 1981 | 18 | 52 | Thistlethwaite |
| December 1990 | 18 | 42 | Kloosterman |
| May 1992 | 18 | 39 | Reid |
| May 1992 | 18 | 37 | Winter |
| January 1995 | 18 | 29 | Reid |
| January 1995 | 20 | 29 | Reid |
| December 2005 | 20 | 28 | Radu |
| April 2006 | 20 | 27 | Radu |
| May 2007 | 20 | 26 | Kunkle and Cooperman |
| March 2008 | 20 | 25 | Rokicki |
| April 2008 | 20 | 23 | Rokicki and Welborn |
| August 2008 | 20 | 22 | Rokicki and Welborn |
| July 2010 | 20 | 20 | Rokicki, Kociemba, Davidson and Dethridge |

Thistlethwaite's 52 came from a four-stage method through a chain of subgroups. In 1995 Reid showed that Kociemba's 1992 algorithm needs at most 29 moves, and he found that the superflip needs 20. The bounds from 2008 on used the coset method above. In QTM, cube20.org lists a counting bound of 19 by 1980, 21 by Hoey in January 1981, 22 by Reid in 1995, 26 by Reid in August 1998, and the matching upper bound of 26 by Rokicki and Davidson in August 2014.

## References
