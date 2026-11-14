---
tag: KAW0FH
kind: technique
slug: karnaugh-map
name: Karnaugh map
aliases:
- K-map
- Veitch diagram
area: eda/logic-synthesis
level: intro
summary: A grid of the truth table in Gray code order so that adjacent cells differ in one variable, which lets a person read prime implicants as rectangles.
prereqs: [gray-code, prime-implicant, dont-care-condition]
see_also: [quine-mccluskey, petricks-method, two-level-logic-minimization, sum-of-products, implicant, espresso, hamming-distance, boolean-function]
sources:
  - paper: doi:10.1109/TCE.1953.6371932
    title: M. Karnaugh, The map method for synthesis of combinational logic circuits, Transactions of the AIEE, Part I, 72(5), 593 to 599, 1953
    locator: the map with its rows and columns in reflected binary order, and the reading of products as groups of adjacent cells
  - paper: doi:10.1145/609784.609801
    title: E. W. Veitch, A chart method for simplifying truth functions, Proceedings of the 1952 ACM national meeting (Pittsburgh), 127 to 133, 1952
    locator: the earlier chart of the truth table that the map refines
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 7, Two-Level Combinational Logic Optimization (the map view of implicants and primes)
  - book: isbn:9780792397465
    title: Gary D. Hachtel and Fabio Somenzi, Logic Synthesis and Verification Algorithms, Kluwer, 1996
    locator: Chapter 4, Synthesis of Two-Level Circuits (maps as a picture of the Boolean cube)
---

A Karnaugh map draws the truth table of a Boolean function of two to four variables as a grid, with the rows and the columns in [Gray code](/gray-code/) order. In this order, two cells next to each other differ in one variable, also across the edges of the grid, which wrap around. A rectangle of cells with sides 1, 2 or 4 is then exactly the set of points of one cube, so a person can see the [implicants](/implicant/) of the function as rectangles of 1 cells and the [prime implicants](/prime-implicant/) as the largest such rectangles. Reading a cover from the map means choosing a few large rectangles that together hold every 1. Cells marked as [don't-cares](/dont-care-condition/) can join a rectangle but need not be covered. Karnaugh (1953) refined the chart of Veitch (1952). The map is a hand method for small functions, and its reading of the cover is not always minimum.

## In plain words

Write the outputs of a small function in a square grid. Put the inputs along the sides in a special order, where each step changes one bit, so that cells that touch differ in one input. The left edge also touches the right edge, and the top touches the bottom.

Now draw boxes around the 1s. A box must be a block of 1, 2, 4 or 8 cells, and it can hold cells marked "do not care". Make each box as large as you can. Each box is one AND term, and the inputs that stay the same inside the box are its letters. A bigger box has fewer letters. Pick boxes until every 1 is inside one, and use as few boxes as you can.

## When it applies

- The function has two to four variables. For five or six variables, two or four maps of four variables are laid side by side, and the extra adjacency between maps is hard to see. Beyond six, the map is not used.
- The goal is a [sum of products](/sum-of-products/) of few cubes and literals, or a product of sums, which is the same task for the 0 cells.
- A person does the work, or a program needs a picture of the function for teaching. A program that minimizes should use [Quine-McCluskey](/quine-mccluskey/) or [Espresso](/espresso/).

## The template

The variables are $x_1, \ldots, x_n$, and $x_1$ is the high bit of a minterm. For $n = 4$ the rows are $x_1 x_2$ and the columns are $x_3 x_4$, both in the order 00, 01, 11, 10. For $n = 3$ the rows are $x_1$ and the columns are $x_2 x_3$. A group is a rectangle of the map, with wrap-around, whose sides are 1, 2 or 4 cells.

```pseudo id=main
READ-MAP(n, on, dc)
L1  big ← GROUPS(n, on, dc)
    GROUPS:
L2      ok ← every group whose cells are all 1 or x
L3      return the groups of ok that lie in no larger group of ok and hold a 1
L4  for each 1 cell m that lies in exactly one group of big do
L5      choose that group                         ▷ an essential group
L6  while some 1 cell is not in a chosen group do
L7      choose the group of big with the most uncovered 1 cells, then the larger one
L8      mark its cells as covered
    return the cube of each chosen group: fix each variable that is constant on the group
```

**Why a group is a cube.** An axis of length 4 in Gray order is 00, 01, 11, 10. Its runs of length 2 with wrap-around are 00 01, 01 11, 11 10 and 10 00, and each one fixes one bit and frees the other. The run of length 4 frees both bits. So a run of length $2^k$ on an axis frees $k$ variables and fixes the rest, and a rectangle of two runs is a cube. Conversely, each cube is the product of one run on each axis. So the groups are exactly the $3^n$ cubes, and line L2 lists the implicants of the function with its don't-cares.

**Why the large groups are the primes.** A group contains another group exactly when the cube contains the cube. So a group of ok that lies in no larger group of ok is a prime implicant of the function with its don't-cares, and line L3 keeps those that hold at least one 1. A prime made of don't-cares only is not useful in a cover, and line L3 drops it.

**Why the essential groups are safe.** If a 1 cell lies in one prime only, every cover by primes must take that prime. Lines L4 and L5 take it. By Quine's theorem, some minimum cover is made of primes, so this choice keeps a minimum cover in reach.

**Why the last step is a heuristic.** After the essential groups, the rest is a [set cover](/set-cover/) problem on the groups of big. Line L7 picks greedily, and the greedy choice can take one group too many. An exact reading must solve this step with [Petrick's method](/petricks-method/) or a search.

**Cost.** A map of $2^n$ cells has $3^n$ groups. For $n \le 4$, there are at most 81 groups and 16 cells, so the work is small. The steps of lines L4 to L8 take time polynomial in the number of groups.

**Example.** Take $f = \sum m(0, 2, 8, 10) + d(5)$ on four variables. The map, with rows $x_1 x_2$ and columns $x_3 x_4$, is

| $x_1 x_2 \backslash x_3 x_4$ | 00 | 01 | 11 | 10 |
|---|---|---|---|---|
| 00 | 1 | 0 | 0 | 1 |
| 01 | 0 | x | 0 | 0 |
| 11 | 0 | 0 | 0 | 0 |
| 10 | 1 | 0 | 0 | 1 |

The four 1s are the four corners. The top row and the bottom row are neighbors across the edge, and so are the left and the right columns, so the corners form one group of four cells. It fixes $x_2 = 0$ and $x_4 = 0$, and the cover is the single cube $\bar{x}_2 \bar{x}_4$, the cube -0-0. The don't-care at minterm 5 lies in no group with a 1, so it stays out.

## Classic examples

- **Corners and edges.** The example above: the wrap-around joins cells that look far apart. Missing the corner group gives two or four cubes in place of one.
- **Seven-segment decoder.** Each segment of a BCD to seven-segment decoder is a function of four inputs, where the codes 10 to 15 never occur and are [don't-cares](/dont-care-condition/). With them, the groups grow, as in $\sum m(5, 6, 7, 8, 9) + d(10, \ldots, 15)$, which becomes $x_1 + x_2 x_4 + x_2 x_3$.
- **The checkerboard.** Parity on four variables has 1 cells where no two touch. Every group has one cell, and the cover needs 8 cubes of 4 literals each, which matches the bound on the [sum of products](/sum-of-products/) page.
- **A cyclic map.** $\sum m(1, 2, 3, 4, 5, 6)$ on three variables has six primes and no essential one. The reader must choose, and two of the choices give three cubes, the minimum. This is the cyclic core that [Petrick's method](/petricks-method/) solves.
- **Teaching Quine-McCluskey.** The prime implicants that [Quine-McCluskey](/quine-mccluskey/) lists are the largest groups of the map, and the prime implicant table is the question of which groups to keep.

## Variations

- **Product of sums.** Group the 0 cells in place of the 1 cells. Each group gives a sum term of the complement, and the product of these sums is a product of sums form of $f$.
- **Five and six variables.** Use two or four maps of four variables for the values of $x_1$, or of $x_1 x_2$. Cells in the same place of neighbor maps are adjacent, so a group can span several maps.
- **Map-entered variables.** Write a variable or a small expression in a cell in place of 0 or 1. This folds one more variable into a smaller map, at the cost of a harder reading.
- **Multiple outputs.** Draw one map for each output and look for groups that several outputs can share.
- **Hazard covers.** For a circuit without static hazards, add a group for every pair of adjacent 1 cells that no single chosen group holds. The cover is then not minimum, but each single input change keeps one cube at 1.

## Pitfalls

- **Binary order.** If the axis is in the order 00, 01, 10, 11, the cells for 01 and 10 sit side by side but differ in two bits. A group across them, as a reading by line L2 would allow, is not a cube.
- **Groups that are not powers of two.** A block of 3 or 6 cells is not a cube. Line L2 allows sides of 1, 2 or 4 only.
- **Forgetting the wrap-around.** The edges of the map touch. The corner group of the example and the groups across the left and right edges are easy to miss.
- **Covering the don't-cares.** A don't-care can join a group, but it never needs a group of its own. A group of don't-cares only adds a cube for nothing, which line L3 avoids.
- **Trusting the greedy step.** Line L7 can take more groups than needed when no group is essential. For $\sum m(1, 2, 4, 5, 6, 8, 9, 10)$ on four variables, all eight groups hold two 1s and no 1 cell is in one group only. The greedy reading takes 5 cubes, but 4 cubes, $\bar{x}_2 \bar{x}_3 x_4 + \bar{x}_1 x_3 \bar{x}_4 + \bar{x}_1 x_2 \bar{x}_3 + x_1 \bar{x}_2 \bar{x}_4$, cover the function. In our own test of all functions without don't-cares, the reading of the template was a minimum cover for all 256 functions of three variables and missed the minimum for 596 of the 65536 functions of four variables, about 0.9 percent. These counts are measured for this greedy rule only, not for all ways a person can read a map.

## Exercises

1. Show that a rectangle of a four-variable map with wrap-around is a cube if and only if each of its sides has 1, 2 or 4 cells.
2. Draw the map of $\sum m(0, 1, 2, 5, 6, 7)$ on three variables, list its primes, and find both minimum covers.
3. Find the minimum sum of products of $\sum m(0, 2, 3, 4, 5, 7) + d(1, 6)$ on three variables, and say which don't-cares the cover uses.
4. Read a minimum product of sums of $\sum m(1, 3, 5, 7, 9, 11, 12, 13)$ on four variables from its 0 cells.
5. Prove that the number of groups of an $n$-variable map is $3^n$.

## References
