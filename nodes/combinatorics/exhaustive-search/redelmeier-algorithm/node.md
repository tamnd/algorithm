---
tag: R79V1G
kind: algorithm
slug: redelmeier-algorithm
name: Redelmeier's algorithm
aliases:
- Redelmeier polyomino enumeration
area: combinatorics/exhaustive-search
level: advanced
summary: Enumerates polyominoes by growing them cell by cell from an untried-cell set, without repetition.
solves: [polyomino-enumeration]
model: word-ram
complexity:
  vars: {n: the largest number of cells, A: the number of fixed polyominoes with at most n cells}
  time: {worst: O(n A), best: O(n A)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: true}
history:
  year: 1981
  people: [D. Hugh Redelmeier]
  note: Redelmeier published the method in Discrete Mathematics in 1981 and used it to count polyominoes up to 24 cells.
prereqs: [polyomino-enumeration, depth-first-search, generic-backtracking-algorithm]
see_also: [polyomino-enumeration, self-avoiding-walk-enumeration, polyomino-tiling-problem, transfer-matrix-method, reverse-search, enumeration-problem, generic-backtracking-algorithm, combinatorial-explosion]
sources:
  - paper: doi:10.1016/0012-365X(81)90237-5
    title: D. Hugh Redelmeier, Counting polyominoes, yet another attack, Discrete Mathematics 36(2), 1981, 191 to 203
    locator: the method of growing a polyomino from an untried set of cells, so that each fixed polyomino is produced once, and the counts it gave
  - url: https://oeis.org/A001168
    title: OEIS A001168, number of fixed polyominoes with n cells
    locator: the table of values and the references to the methods that computed them
  - paper: "Iwan Jensen, Enumerations of lattice animals and trees, Journal of Statistical Physics 102, 2001, 865 to 881"
    locator: the comparison of Redelmeier's method with the transfer-matrix method, which counts fixed polyominoes much further
---

Redelmeier's algorithm lists all fixed [polyominoes](/polyomino-enumeration/) with at most $n$ cells, each exactly once, by growing them one cell at a time. It keeps a set of *untried* cells next to the current polyomino, places each in turn, and adds to the set only the neighbors of the new cell that no earlier step has seen. This rule makes every fixed polyomino appear exactly once with no table of polyominoes found so far, so the memory stays tiny. Redelmeier (1981) used it to count polyominoes up to 24 cells, and its depth-first form remains the standard way to *list* polyominoes, while the [transfer-matrix method](/transfer-matrix-method/) counts them further.

## In plain words

A polyomino is a shape made of equal squares joined edge to edge. Two shapes count as the same when one is a shift of the other.

Start with one square. Keep a list of empty squares that touch the shape and that you are still allowed to add. Take one square from the list, add it to the shape, and count the new shape. Then put on the list the new neighbors of that square, but only those that no earlier step has put on a list. Grow further in the same way, then take the square away again and try the next one.

A square that you have taken from the list stays forbidden for the rest of this branch. This simple rule makes sure that each shape is made exactly once.

## The problem

A *fixed polyomino* with $k$ cells is a connected set of $k$ cells of the square grid, where connection is through shared edges, up to translation. Given $n$, the task is to list, or count, all fixed polyominoes with $k$ cells for every $k \le n$. Their numbers $a(k)$ are $1, 2, 6, 19, 63, 216, 760, 2725, 9910, 36446$ for $k = 1, \ldots, 10$ (OEIS A001168).

Order the cells by row and then by column: $(x, y)$ comes before $(x', y')$ when $y < y'$, or $y = y'$ and $x < x'$. Every fixed polyomino has exactly one translate whose first cell in this order is the origin $(0, 0)$. All cells of this translate lie in the *allowed region*, the cells with $y > 0$ or with $y = 0$ and $x \ge 0$. So the task is to list the connected sets of cells in the allowed region that contain the origin.

## The algorithm

The state is the list $P$ of occupied cells and the set $R$ of *reached* cells: the cells that are in $P$ or that some placed cell of the current branch has added to an untried set. A call of EXTEND gets its own copy of an untried set $U$.

```pseudo id=main
REDELMEIER(n)
L1  count[1..n] ← 0, P ← empty list, R ← {(0, 0)}
L2  EXTEND({(0, 0)})
EXTEND(U)
L3  while U ≠ ∅ do
L4      remove a cell c from U
L5      append c to P, count[|P|] ← count[|P|] + 1
L6      if |P| < n then
L7          N ← the neighbors of c in the allowed region that are not in R
L8          R ← R ∪ N
L9          EXTEND(U ∪ N)                ▷ a copy: the changes of U stay in the call
L10         R ← R \ N
L11     remove c from P
```

Line L4 removes $c$ from $U$ for good: later iterations of the same loop, and all calls below them, never place $c$, because it stays in $R$ and is no longer untried. Line L7 is the key rule. A neighbor of $c$ that is already in $R$ is either occupied, or untried at this level, or was tried before and is forbidden. In each case adding it again would make a polyomino twice.

To list the polyominoes instead of counting them, output $P$ at line L5.

## Example

Run the algorithm with $n = 3$. Cells are $(x, y)$ with $y$ upward, and $U$ is used as a stack: the last cell added is removed first.

1. Place $(0, 0)$. Count $a(1) = 1$. Its allowed neighbors $(1, 0)$ and $(0, 1)$ are new, so $R = \{(0,0), (1,0), (0,1)\}$.
2. Place $(0, 1)$, with $(1, 0)$ left untried. Count the vertical domino. New neighbors of $(0, 1)$: $(1, 1)$, $(-1, 1)$, $(0, 2)$. The cell $(0, 0)$ is in $R$.
   - Place $(0, 2)$: the vertical I-tromino.
   - Place $(-1, 1)$: an L-tromino.
   - Place $(1, 1)$: an L-tromino.
   - Place $(1, 0)$: an L-tromino.
3. Back at the first level, place $(1, 0)$, the only untried cell left. Count the horizontal domino. The cell $(0, 1)$ was tried in step 2 and is still in $R$, so it is forbidden now. New neighbors of $(1, 0)$: $(2, 0)$ and $(1, 1)$.
   - Place $(1, 1)$: the fourth L-tromino.
   - Place $(2, 0)$: the horizontal I-tromino.

The counts are $1$, $2$ and $6$, as expected. The shape $\{(0,0), (1,0), (0,1)\}$ appears in step 2 only. In step 3 it would need the forbidden cell $(0, 1)$, which is exactly the repeat that the rule removes.

## Correctness

Call the cells of $R \setminus (P \cup U)$ *forbidden* in a call. The invariant is that, when EXTEND$(U)$ is called with occupied list $P$, the set $R$ is $P$ together with the allowed neighbors of $P$ (or $\{(0,0)\}$ at the start), and the untried cells are allowed neighbors of $P$. The claim is that the call counts each connected set $Q$ in the allowed region with $P \subsetneq Q$, $|Q| \le n$, and no forbidden cell, exactly once. Since $Q$ is connected and larger than $P$, it contains an untried cell. Split the sets $Q$ by the first untried cell, in the order of line L4, that they contain. The iteration that places this cell counts exactly that class: the cells removed before it become forbidden, and the new untried cells are its unreached neighbors. With the first call, the claim gives every connected set that contains the origin, which is every fixed polyomino once. The full proof is below.

## Complexity

Every node of the search tree places a cell and counts one fixed polyomino, so the tree has exactly $A = a(1) + \cdots + a(n)$ nodes. At each node, line L7 looks at 4 neighbors, and the copy of $U$ at line L9 takes $O(|U|)$ time. Each placed cell adds at most 3 new cells to the untried sets, since at least one of its neighbors is already reached, so $|U| \le 3n + 2$ and a node costs $O(n)$. The total time is $O(nA)$. Redelmeier's own version shares the untried set between levels as a stack and gets $O(1)$ amortized time per polyomino.

The depth is at most $n$. In the simple version each level holds a copy of $U$, which is $O(n^2)$ space. With a shared stack the space is $O(n)$. In both cases the space is tiny compared with $A$: the method never stores the polyominoes it has found.

Since $a(k)$ grows like $\lambda^k$ with $\lambda \approx 4.06$, each extra cell multiplies the running time by about 4.

## Properties

- **No repeats and no memory of the output.** Each fixed polyomino is produced once, with no hash table.
- **Every node is an output.** The search has no dead ends, so it lists the polyominoes with $O(n)$ time each.
- **Counts all sizes at once.** One run up to $n$ counts every size $k \le n$.
- **Works on any graph.** Only the neighbor function and the allowed region depend on the square grid.

## Variants and improvements

- **Other lattices and dimensions.** Replace the neighbor function to count polyiamonds (triangles), polyhexes (hexagons), or polycubes in three or more dimensions. On a general graph with a fixed vertex as the root, the method lists the connected vertex sets whose first vertex in a fixed order is the root.
- **Free and one-sided polyominoes.** Count each fixed polyomino with its symmetry, and use Burnside's lemma to get the number of polyominoes up to rotation and reflection. See [polyomino enumeration](/polyomino-enumeration/).
- **Parallel runs.** Split the search tree at a small depth and give the subtrees to different processors.
- **Transfer matrices.** To count but not list, the [transfer-matrix method](/transfer-matrix-method/) of Jensen is exponentially faster in practice and counts sizes far beyond the reach of any listing method.
- **Properties along the way.** The same search counts polyominoes by perimeter, by width or by the number of holes, at no extra cost in the order of growth.

## When to use it

Use Redelmeier's algorithm when every polyomino, or every connected subgraph of a graph, must be visited, for example to test each shape for a property, or when a simple and reliable counter for small $n$ is needed. To count only, for large $n$, use transfer matrices. To list polyominoes up to rotation and reflection, add a canonical-form test or count with symmetries.

## Pitfalls

- **Forgetting that tried cells stay forbidden.** If a cell removed at line L4 goes back into $U$ for a later iteration, polyominoes are counted several times.
- **Undoing $R$ wrongly.** Line L10 must remove exactly the cells that line L8 added in this iteration, and nothing else.
- **Sharing $U$ by mistake.** In a language with shared lists, the call at line L9 must not change the list that the caller still loops over, unless the stack trick is done with care.
- **The allowed region.** The region must contain exactly the cells after the origin in the order. With a wrong region, some polyominoes have no translate that starts at the origin and are missed, or some are counted more than once.
- **Mixing fixed, one-sided and free counts.** The algorithm counts fixed polyominoes. The free counts are smaller by a factor close to 8 for large $n$.

## Implementations

## History

Redelmeier (1981) introduced the method in *Counting polyominoes: yet another attack* and counted polyominoes up to 24 cells, far beyond the earlier methods that stored all polyominoes of one size to grow the next. Later work ran it on parallel machines and on other lattices. Jensen's transfer-matrix method (2001) and its successors count fixed polyominoes much further, but Redelmeier's method is still the usual way to list them.

## References
