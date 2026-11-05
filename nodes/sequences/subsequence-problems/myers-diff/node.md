---
tag: 245ETE
kind: algorithm
slug: myers-diff
name: Myers diff algorithm
aliases:
- Myers O(ND) difference algorithm
- diff algorithm
area: sequences/subsequence-problems
level: core
summary: Computes a shortest edit script in O((n + m) D) time, where D is the edit distance.
solves: [shortest-edit-script, longest-common-subsequence]
model: word-ram
complexity:
  vars: {m: the length of A, n: the length of B, D: the least number of insertions and deletions}
  time: {worst: O((m + n) D), best: Θ(m + n)}
  space: {extra: O(m + n + D^2)}
properties: {stable: false, in_place: false, adaptive: true, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [shortest-edit-script, lcs-dynamic-programming]
see_also: [longest-common-subsequence, hirschberg-lcs, hunt-szymanski, alignment-graph, edit-distance, banded-alignment, breadth-first-search, bit-parallel-lcs]
sources:
  - paper: doi:10.1007/BF01840446
    title: Eugene W. Myers, An O(ND) difference algorithm and its variations, Algorithmica 1, 1986, 251-266
    locator: the edit graph, the furthest reaching D-paths on each diagonal (Lemmas 1 and 2), the greedy algorithm, the O((N + M) D) bound, the linear-space refinement with the middle snake, and the expected-case analysis
  - paper: "Esko Ukkonen, Algorithms for approximate string matching, Information and Control 64, 1985, 100-118"
    locator: the computation of the edit distance by diagonals in time proportional to the distance times the length
  - paper: "Webb Miller and Eugene W. Myers, A file comparison program, Software: Practice and Experience 15(11), 1985, 1025-1040"
    locator: a file comparison program based on the greedy search by increasing distance
---

Myers' algorithm computes a [shortest edit script](/shortest-edit-script/) between two sequences $A$ and $B$ of lengths $m$ and $n$, and so a [longest common subsequence](/longest-common-subsequence/), in $O((m + n) D)$ time, where $D$ is the least number of insertions and deletions. It searches the edit graph by increasing cost $d = 0, 1, 2, \ldots$, and for each cost and each diagonal it keeps only the furthest point that a path of that cost can reach, after it follows the run of free diagonal edges as far as it goes. Myers published it in 1986. When the two inputs are similar, as two versions of a file usually are, $D$ is small and the method is close to linear; this is why diff programs use it.

## In plain words

Lay the two sequences on the two sides of a grid. A walk from the top left corner to the bottom right corner is a way to change the first sequence into the second. A step to the right removes an item of the first sequence and costs one. A step down adds an item of the second sequence and costs one. A step down and to the right is free, but only where the two items are equal.

Search the cheapest walks first: all walks of cost 0, then of cost 1, and so on. For each cost and each diagonal of the grid, keep only the walk that got furthest. Each walk takes all the free steps it can. When a walk reaches the corner, its cost is the answer, and its steps are the edit script.

## The problem

The input is two sequences $A = \langle a_1, \ldots, a_m \rangle$ and $B = \langle b_1, \ldots, b_n \rangle$ over a set with an equality test. The output is a [shortest edit script](/shortest-edit-script/): a list of deletions of items of $A$ and insertions of items of $B$ of least length $D$ that turns $A$ into $B$. The kept items form an LCS, and $D = m + n - 2\,\mathrm{lcs}(A, B)$.

## The algorithm

The edit graph has the points $(x, y)$, $0 \le x \le m$, $0 \le y \le n$, a *right* edge $(x - 1, y) \to (x, y)$ that deletes $a_x$, a *down* edge $(x, y - 1) \to (x, y)$ that inserts $b_y$, and a free *diagonal* edge $(x - 1, y - 1) \to (x, y)$ when $a_x = b_y$. The point $(x, y)$ lies on *diagonal* $k = x - y$. A *snake* is a run of diagonal edges. Let $V_d[k]$ be the largest $x$ such that a path of cost $d$ from $(0, 0)$ ends at a point $(x, x - k)$; it is defined for $k \in \{-d, -d + 2, \ldots, d\}$, since a path of cost $d$ ends on a diagonal of the same parity as $d$.

```pseudo id=main
MYERS(A[1 .. m], B[1 .. n])
L1  V[1] ← 0
L2  for d ← 0 to m + n do
L3      for k ← −d to d step 2 do
L4          if k = −d or (k ≠ d and V[k − 1] < V[k + 1]) then x ← V[k + 1]      ▷ down edge from diagonal k + 1
L5          else x ← V[k − 1] + 1                                                ▷ right edge from diagonal k − 1
L6          y ← x − k
L7          while x < m and y < n and A[x + 1] = B[y + 1] do (x, y) ← (x + 1, y + 1)   ▷ follow the snake
L8          V[k] ← x
L9      save V_d ← V[−d .. d]; if some k has V[k] ≥ m and V[k] − k ≥ n then return d and V_0, ..., V_d

TRACEBACK(V_0, ..., V_D)
L10 (x, y) ← (m, n)
L11 for d ← D downto 1 do
L12     k ← x − y; p ← k + 1 if k = −d or (k ≠ d and V_{d−1}[k − 1] < V_{d−1}[k + 1]), else p ← k − 1
L13     (px, py) ← (V_{d−1}[p], V_{d−1}[p] − p); (sx, sy) ← the end of the edge from (px, py) to diagonal k
L14     output the items of the snake from (sx, sy) to (x, y) as kept
L15     output "insert B[py + 1]" if p = k + 1, else "delete A[px + 1]"; (x, y) ← (px, py)
L16 output the snake from (0, 0) to (x, y) as kept; return the outputs in reverse order
```

Lines L4 and L5 pick the better of the two ways to reach diagonal $k$ at cost $d$: a down edge from the furthest point of cost $d - 1$ on diagonal $k + 1$, or a right edge from the furthest point on diagonal $k - 1$. Line L7 then takes the snake greedily. The choice is safe because a point further along a diagonal is never worse: everything a path can do from an earlier point of the same diagonal, the path from the later point can match. Line L1 sets a virtual entry so that round 0 starts at $(0, 0)$. The array $V$ is indexed from $-(m + n)$ to $m + n$; in round $d$ the entries of diagonals $k \pm 1$ hold the values of round $d - 1$, since round $d$ writes only diagonals of the other parity.

## Example

Take Myers' example $A = \text{ABCABBA}$ ($m = 7$) and $B = \text{CBABAC}$ ($n = 6$). The values $V_d[k]$:

| $d$ | $k = -5$ | $-4$ | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | | | | | | 0 | | | | | |
| 1 | | | | | 0 | | 1 | | | | |
| 2 | | | | 2 | | 2 | | 3 | | | |
| 3 | | | 3 | | 4 | | 5 | | 5 | | |
| 4 | | 3 | | 4 | | 5 | | 7 | | 7 | |
| 5 | 3 | | 4 | | 5 | | 7 | | 8 | | 8 |

Some steps in detail. In round 0, $a_1 = $ A and $b_1 = $ C differ, so the snake is empty and $V_0[0] = 0$. In round 2 on diagonal 0, line L4 compares $V_1[-1] = 0$ and $V_1[1] = 1$ and takes the down edge from $(1, 0)$ to $(1, 1)$; then $a_2 = b_2 = $ B gives a snake to $(2, 2)$. In round 5, diagonal $m - n = 1$ reaches $x = 7$, the point $(7, 6)$, so $D = 5$. The entries $V_5[3] = 8$ and $V_5[5] = 8$ are points $(8, 5)$ and $(8, 3)$ beyond the right side of the graph, and $V_4[2] = 7$ is the point $(7, 5)$, on the right side but not at the corner; such points can occur, but they never pass the test of line L9 before $(m, n)$ does (see the proof file).

The traceback from $(7, 6)$ gives the script

| op | delete A | delete B | keep C | insert B | keep A | keep B | delete B | keep A | insert C |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| point after it | (1, 0) | (2, 0) | (3, 1) | (3, 2) | (4, 3) | (5, 4) | (6, 4) | (7, 5) | (7, 6) |

with 5 operations and the LCS CABA, the script of the [shortest edit script](/shortest-edit-script/) page.

## Correctness

Three facts give correctness; the proof file has the details. First, a path of cost $d$ ends on a diagonal $k$ with $|k| \le d$ and $k \equiv d \pmod 2$, since each right edge adds 1 to $x - y$, each down edge subtracts 1, and diagonals keep it. Second (Myers' Lemma 2), the furthest point of cost $d$ on diagonal $k$ is reached by taking the furthest point of cost $d - 1$ on diagonal $k - 1$ or $k + 1$, one edge to diagonal $k$, and then the longest snake; this rests on the fact that from two points on the same diagonal, the snake of the earlier one never ends beyond the snake of the later one. So lines L4 to L8 compute $V_d[k]$ exactly, by induction on $d$. Third, the first round in which a point reaches $x \ge m$ and $y \ge n$ is the round $d = D$, and the point is $(m, n)$. The traceback walks back the choices of line L4, so it outputs a path of cost $D$ from $(0, 0)$ to $(m, n)$, that is, a shortest edit script.

## Complexity

- **Time.** Round $d$ handles $d + 1$ diagonals, with $O(1)$ work each outside the snakes, so $O(D^2)$ in total. On each diagonal, a snake of round $d$ starts beyond the end of the snake of round $d - 2$, so no diagonal edge is walked twice, and the snakes of one diagonal take at most $\min(m, n)$ steps over the whole run. The $2D + 1$ diagonals give $O((m + n) D)$ snake steps. With $D \le m + n$ the total is $O((m + n) D)$. If $A = B$, $D = 0$ and round 0 walks one snake of length $m$: $\Theta(m + n)$.
- **Space.** The array $V$ takes $O(m + n)$. The traceback needs the rows $V_0, \ldots, V_D$, which take $O(D^2)$ entries. So $O(m + n + D^2)$.
- **Linear space.** Myers' refinement runs the search from both corners at the same time until the two meet on a *middle snake*, then solves the two halves recursively, as in [Hirschberg's algorithm](/hirschberg-lcs/). This gives $O((m + n) D)$ time and $O(m + n)$ space.
- **Expected time.** Myers shows that under a probabilistic model of the inputs the expected time is $O(m + n + D^2)$.

## Properties

- **Adaptive.** The cost grows with $D$, not with $mn$. Two files of $10^6$ lines with 100 changed lines need at most about $2 \cdot 10^8$ steps by the bound, and in practice far fewer.
- **Equality only.** The items need only an equality test; diff tools first hash each line to a number to make the test fast.
- **Greedy and exact.** The snakes are taken greedily, and the result is still a shortest script.
- **Many shortest scripts.** The tie rule of line L4 picks one of them; the edit graph of the example has 7 cheapest paths.

## Variants and improvements

- **Middle snake.** The bidirectional search in linear space, described above.
- **Suffix-tree snakes.** With a suffix tree of $A$ and $B$ and constant-time longest common extension queries, each snake takes $O(1)$ time, which gives $O((m + n) \log (m + n) + D^2)$ time; Myers describes this variation.
- **Bounded distance.** Stop after round $k$ to decide whether $D \le k$, in $O((m + n) k)$ time. This is a form of [banded alignment](/banded-alignment/).
- **Edit distance with substitutions.** The same diagonal method with a substitution edge solves the unit-cost [edit distance](/edit-distance/); Ukkonen gave this in 1985.

## When to use it

Use it to compare two similar sequences, the usual case for versions of a file, where $D$ is much smaller than $m$ and $n$. For two unrelated sequences, $D$ is close to $m + n$ and the time is quadratic, like the [LCS table](/lcs-dynamic-programming/), with more overhead. For sequences with few matching pairs but many differences, [Hunt-Szymanski](/hunt-szymanski/) can be faster.

## Pitfalls

- **Negative indices.** $k$ runs from $-d$ to $d$, so the array $V$ needs an offset of $m + n$, or a dictionary.
- **The tie rule in the traceback.** Line L12 must use the same rule as line L4, with the row $V_{d-1}$; with the current row, or another rule, the traceback can step to a point that the search never reached.
- **Points outside the graph.** $V_d[k]$ can exceed $m$ or $y$ can exceed $n$. The test of line L9 must check both coordinates, not only $x \ge m$: in the example, $V_4[2] = 7$ reaches $x = m$ at $(7, 5)$ in round 4, one round before the corner.
- **Quadratic memory.** Keeping all rows $V_0, \ldots, V_D$ costs $O(D^2)$, which is large for very different inputs. Use the middle snake.
- **Off by one in the snake.** With 1-based items, the snake from $(x, y)$ compares $A[x + 1]$ with $B[y + 1]$.

## Implementations

## History

Myers published the algorithm in Algorithmica in 1986, with the linear-space refinement, the suffix-tree variation and the expected-case analysis. Ukkonen (1985) independently gave a diagonal method of the same kind for edit distance. Miller and Myers (1985) described a file comparison program based on this greedy search.

## References
