---
tag: 6DD0YJ
kind: algorithm
slug: warnsdorff-rule
name: Warnsdorff's rule
aliases:
- Warnsdorff's heuristic
area: games-and-search/puzzles
level: intro
summary: Greedy heuristic for knight's tours that always moves to the unvisited square with the fewest onward moves. It runs in linear time, finds tours on most boards, and can fail.
solves: [knights-tour-problem]
model: word-ram
complexity:
  vars: {m: the number of rows, n: the number of columns}
  time: {worst: Θ(m n), average: O(m n), best: Θ(1)}
  space: {extra: Θ(m n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [knights-tour-problem, greedy-algorithm]
see_also: [hamiltonian-path-problem, generic-backtracking-algorithm, depth-first-search, heuristic-function]
sources:
  - book: "H. C. von Warnsdorf, Des Rösselsprunges einfachste und allgemeinste Lösung, Schmalkalden, Varnhagen, 1823"
    locator: the whole book (the rule, and the claim that any choice among tied squares works)
  - paper: doi:10.1145/363427.363463
    title: Ira Pohl, A method for finding Hamilton paths and knight's tours, Communications of the ACM 10(7), 1967, 446 to 449
    locator: the whole paper (a tie-breaking rule for Warnsdorff's method and its use for Hamilton paths in general graphs)
  - paper: "Douglas Squirrel and Paul Cull, A Warnsdorff-rule algorithm for knight's tours on square boards, research report, Oregon State University, 1996"
    locator: the whole report (fixed move orders for breaking ties on square boards)
  - paper: doi:10.1016/0166-218X(92)00170-Q
    title: Axel Conrad, Tanja Hindrichs, Hussein Morsy and Ingo Wegener, Solution of the knight's Hamiltonian path problem on chessboards, Discrete Applied Mathematics 50(2), 1994, 125 to 134
    locator: the introduction (heuristics compared with the exact construction)
  - book: "John J. Watkins, Across the Board: The Mathematics of Chessboard Problems, Princeton University Press, 2004"
    locator: Chapter 2 (Knight's Tours, with Warnsdorff's rule)
---

Warnsdorff's rule is a [greedy](/greedy-algorithm/) method for the [knight's tour problem](/knights-tour-problem/): from the current square, move the knight to the unvisited square that has the fewest unvisited squares one knight move away. H. C. von Warnsdorf published it in 1823. It never backtracks, so it builds a path of at most $mn$ squares in $O(mn)$ time on an $m \times n$ board, and the path is always a valid partial tour. It is a heuristic: it can get stuck on boards and from start squares where a tour exists, and how ties are broken changes the result.

## In plain words

Squares near the edge and in the corners have few ways in and out. If the knight leaves them for later, it may never be able to reach them again. So the rule visits the hard squares first.

At each step, look at every square the knight can jump to that it has not visited. For each one, count how many unvisited squares the knight could jump to from there. Jump to the square with the smallest count. If several squares share the smallest count, a fixed tie rule picks one.

The knight never goes back, so the method is very fast. But it is only a rule of thumb: sometimes the knight gets stuck with squares left, even though a full tour exists.

## The problem

The input is a board of $m$ rows and $n$ columns and a start square $s$. A knight move goes from $(r, c)$ to $(r', c')$ with $\{|r - r'|, |c - c'|\} = \{1, 2\}$. The goal is an open tour from $s$: a sequence of all $mn$ squares, starting at $s$, each one a knight move from the one before. This is a [Hamiltonian path](/hamiltonian-path-problem/) of the knight's graph with a fixed first vertex. The [knight's tour problem](/knights-tour-problem/) page gives the boards that have tours and the exact constructions.

## The algorithm

For a square $u$ and the set $V$ of visited squares, let $d(u)$ be the number of squares one knight move from $u$ that are not in $V$. The moves are tried in a fixed order of the 8 knight steps, and this order is the tie rule.

```pseudo id=main
WARNSDORFF(m, n, s)
L1  v ← s; mark s visited; path ← [s]
L2  repeat m·n − 1 times
L3      C ← the unvisited squares one knight move from v, in the fixed move order
L4      if C is empty then return path            ▷ stuck: path is not a full tour
L5      for each u in C, compute d(u)
L6      v ← the first u in C with the least d(u)
L7      mark v visited; append v to path
L8  return path                                   ▷ a full tour
```

The result is a full tour exactly when it has $mn$ squares. The implementation uses the move order $(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)$ as (row step, column step).

## Example

Start at the top left corner $(0, 0)$ of the $5 \times 5$ board, with rows and columns numbered from 0. Each row of the table is one pass of line L2: the candidates of line L3 with their counts $d(u)$, and the choice of line L6.

| step | from | candidates $u$ with $d(u)$ | move to |
|---|---|---|---|
| 2 | (0, 0) | (1, 2): 5, (2, 1): 5 | (1, 2), the first of a tie |
| 3 | (1, 2) | (2, 4): 3, (3, 3): 3, (3, 1): 3, (2, 0): 3, (0, 4): 1 | (0, 4) |
| 4 | (0, 4) | (2, 3): 5 | (2, 3) |
| 5 | (2, 3) | (4, 4): 1, (4, 2): 3, (3, 1): 2, (1, 1): 3, (0, 2): 3 | (4, 4) |
| 6 | (4, 4) | (3, 2): 5 | (3, 2) |
| 7 | (3, 2) | (4, 0): 1, (2, 0): 2, (1, 1): 2, (1, 3): 3, (2, 4): 2 | (4, 0) |

The rule sends the knight into the corners $(0, 4)$, $(4, 4)$ and $(4, 0)$ as soon as it can, since a corner has only 2 knight moves. It goes on without a dead end and visits all 25 squares; the step numbers are:

```
 1 12 25 18  3
22 17  2 13 24
11  8 23  4 19
16 21  6  9 14
 7 10 15 20  5
```

**A failure.** From $(2, 0)$ on the same board the rule gets stuck after 17 squares (the dots are the 8 squares it never reaches):

```
11  .  5  . 17
 6  . 10  .  4
 1 12  . 16  9
 .  7 14  3  .
13  2  .  8 15
```

Yet an open tour from $(2, 0)$ exists, and exhaustive search finds one:

```
23 12  5 10 25
 6 17 24 13  4
 1 22 11 18  9
16  7 20  3 14
21  2 15  8 19
```

## Correctness

Warnsdorff's rule is *sound* but not *complete*. Sound: the path it returns always starts at $s$, never repeats a square, and moves by knight steps, so when it has $mn$ squares it is an open tour. This holds because line L3 offers only unvisited squares one knight move from the current square, and line L7 marks each chosen square. The loop of line L2 runs at most $mn - 1$ times, so the rule always stops. Not complete: the $5 \times 5$ example above has a tour from $(2, 0)$ that the rule misses, and on odd boards no rule can succeed from a square of the minority color, since every open tour there starts and ends on the majority color. The full proof is below.

## Complexity

- **Time.** Each pass of line L2 looks at at most 8 candidates in line L3 and, for each, at most 8 squares in line L5, so it costs $O(1)$. There are at most $mn - 1$ passes, so the time is $O(mn)$, and $\Theta(mn)$ when the rule succeeds, since it outputs $mn$ squares. It stops at once on a board where the start has no move, such as $2 \times 2$.
- **Space.** $\Theta(mn)$ for the visited marks and the path.
- **Faster counts.** Keeping $d(u)$ for every square and decrementing the counts of the neighbors of each newly visited square makes line L5 a lookup, but the bound stays $O(mn)$, with a smaller constant.

With the move order above and the start at the corner $(0, 0)$, the rule finds a tour on the $n \times n$ board for every $n$ from 5 to 30. Among $n$ from 5 to 66 it fails only for $n = 64$ and $n = 66$. Over all start squares the counts of successes are:

| $n$ | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|
| starts that give a tour | 12 | 35 | 18 | 63 | 41 | 98 | 61 | 138 |
| squares on the board | 25 | 36 | 49 | 64 | 81 | 100 | 121 | 144 |

On the odd boards only the majority color can start a tour, which is 13, 25, 41 and 61 squares for $n = 5, 7, 9, 11$. On the $8 \times 8$ board the only failing start is $(4, 2)$, and on $6 \times 6$ it is $(3, 3)$; from both of them a tour exists.

## Properties

- **Greedy.** Each choice is final; the rule never undoes a move.
- **Deterministic.** With a fixed move order the result depends only on the board and the start.
- **Local.** Each choice looks only one move ahead, at the counts of the candidate squares.
- **Sensitive to ties.** Changing the move order changes the result: with the order rotated to start at $(1, -2)$, the rule fails on $7 \times 7$ from the corner, where the order above succeeds.

## Variants and improvements

- **Tie-breaking by look-ahead.** Pohl (1967) broke ties by applying the same count one move further ahead, and used the method for Hamilton paths in general graphs.
- **Fixed move orders.** Squirrel and Cull (1996) studied fixed orders of the 8 moves for the tie rule on square boards.
- **Backtracking with the rule as an order.** Use $d(u)$ only to order the moves of an exhaustive [depth-first search](/depth-first-search/), as in the [generic backtracking algorithm](/generic-backtracking-algorithm/). This is complete: it finds a tour whenever one exists, but its worst case is exponential. The reference search of the implementation works this way.
- **Restarts.** Break ties at random and restart on failure. This turns the rule into a randomized search.

## When to use it

Use Warnsdorff's rule to produce a knight's tour quickly, by hand or by a short program, on boards up to a few dozen squares on a side. When a tour is required for every board size, use the divide and conquer constructions on the [knight's tour problem](/knights-tour-problem/) page, which always succeed in linear time, or use the rule only as the move order of a backtracking search.

## Pitfalls

- **The rule is not an algorithm for all boards.** It fails on some boards and starts where tours exist, and Warnsdorff's claim that any tie choice works is false, as the $7 \times 7$ example shows.
- **Counting the current square.** $d(u)$ counts the unvisited squares next to $u$; the current square $v$ is already visited and must not be counted.
- **Forgetting to check the result.** The rule returns a path even when it is stuck. Check its length before using it as a tour.
- **Odd boards.** From a square of the minority color no open tour exists at all, so a failure there says nothing about the rule.
- **Closed tours.** A successful run gives an open tour; it is closed only by chance, and none of the corner runs for $n$ from 5 to 30 happens to be closed with the order above.

## Implementations

## History

Warnsdorf described the rule in a small book printed at Schmalkalden in 1823, and he claimed that it always works, whatever square is chosen among ties. Pohl (1967) gave a rule for ties and applied the method to Hamilton paths in other graphs. Squirrel and Cull (1996) studied move orders for square boards. Exact linear time constructions came from Conrad, Hindrichs, Morsy and Wegener (1994) for open tours and Parberry (1997) for closed tours; see the [knight's tour problem](/knights-tour-problem/).

## References
