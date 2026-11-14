---
tag: RH6JHQ
kind: algorithm
slug: stockmeyer-floorplan-sizing
name: Stockmeyer's floorplan sizing
aliases:
- optimal orientation of slicing floorplans
area: eda/partitioning-floorplanning-and-placement
level: core
summary: Finds the least area realization of a slicing floorplan with shape choices per block by merging shape lists bottom up, in O(n d) time for depth d.
solves: [floorplanning]
model: word-ram
complexity:
  vars: {n: the number of blocks, d: the depth of the slicing tree}
  time: {worst: O(n d), average: O(n d), best: O(n)}
  space: {extra: O(n d)}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1983
  people: [Larry Stockmeyer]
  note: Stockmeyer gave the algorithm for the best orientations of the blocks of a slicing floorplan in 1983, and proved that the same problem is NP-complete for general floorplans.
prereqs: [slicing-floorplan, shape-function, normalized-polish-expression, pareto-front]
see_also: [wong-liu-floorplanning, shape-function, floorplanning, pareto-dominance, np-complete, floorplan-constraint-graphs]
sources:
  - paper: doi:10.1016/S0019-9958(83)80038-2
    title: Larry Stockmeyer, Optimal orientations of cells in slicing floorplan designs, Information and Control 57(2-3), 91 to 101, 1983
    locator: the bottom-up merge of the lists of non-dominated shapes, the O(n d) time bound, and the NP-completeness of the orientation problem for general floorplans
  - paper: "Ralph H. J. M. Otten, Efficient floorplan optimization, Proceedings of the IEEE International Conference on Computer Design (ICCD), 499 to 502, 1983"
    locator: shape functions of slicing floorplans and their addition at the cuts
  - paper: "Weiping Shi, An optimal algorithm for area minimization of slicing floorplans, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design, 480 to 484, 1995"
    locator: the O(n log n) algorithm in the number of realizations, the lower bound, and the statement that Stockmeyer's algorithm takes O(n^2) time in the worst case
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 3, Chip Planning (floorplan sizing with shape functions; general locator)
---

Stockmeyer's floorplan sizing chooses a shape for each block of a [slicing floorplan](/slicing-floorplan/) so that the area of the floorplan is the least possible. Each block has a few allowed shapes, for example a rectangle and its rotation. The algorithm goes up the slicing tree and keeps, at each node, only the width and height pairs that no other pair beats in both coordinates, the [Pareto front](/pareto-front/) of the node. Two fronts are merged in time linear in their lengths, so the whole run takes $O(n d)$ time for $n$ blocks and a tree of depth $d$. Stockmeyer gave it in 1983 and proved in the same paper that the orientation problem is [NP-complete](/np-complete/) for floorplans that are not slicing.

## In plain words

You build a wall from boxes, and each box can lie flat or stand up. The plan says which boxes go side by side and which go on top of each other, but not how each box turns. You want the wall to fit in the smallest frame.

For each part of the plan, write down every useful size the part can have: a size is useful if no other size of the same part is both narrower and lower. Two parts side by side have a width that is the sum and a height that is the taller one. Go through both lists at the same time, and each time make the taller part lower. At the top of the plan you have a short list of sizes, and you take the one with the least area.

## The problem

The input is a slicing tree, given as a Polish expression $E$ on $n$ blocks (see [normalized Polish expression](/normalized-polish-expression/); here $E$ need not be normalized), and for each block $i$ a list $S_i$ of allowed shapes $(w, h)$ of positive integers. A *realization* gives each block one shape of its list. The floorplan of a realization has the width and the height computed by the tree: a $V$ node adds the widths of its parts and takes the larger height, and an $H$ node takes the larger width and adds the heights. The output is a realization with the least area $W \cdot H$, its width and height, and the front of all $(W, H)$ pairs.

In Stockmeyer's paper each block is a fixed rectangle that may turn by 90 degrees, so $S_i = \{(w_i, h_i), (h_i, w_i)\}$. The same algorithm works for any finite lists, which is the form used with [shape functions](/shape-function/).

## The algorithm

A shape $(w, h)$ *dominates* $(w', h')$ if $w \le w'$, $h \le h'$ and the two differ. A *front* is a list of shapes, none of which dominates another, by increasing width. In a front the heights strictly decrease.

```pseudo id=main
STOCKMEYER(E, S)                         ▷ E: a Polish expression; S_i: the allowed shapes of block i
L1  for each token t of E, from left to right, with a stack do
L2      if t is a block i then push PARETO(S_i), the front of S_i
L3      else pop B, then pop A; push MERGE-V(A, B) if t = V, else MERGE-H(A, B)
L4  R ← the list that is left on the stack
L5  k ← the entry of R with the least W · H
L6  follow the back pointers down from entry k, and give each block its shape
L7  return W_k · H_k and the shapes

MERGE-V(A, B)                            ▷ A, B: fronts, widths increasing, heights decreasing
L8  i ← 1, j ← 1, R ← an empty list
L9  loop
L10     append (w_A[i] + w_B[j], max(h_A[i], h_B[j])) with the back pointer (i, j) to R
L11     if h_A[i] > h_B[j] then (if i = |A| then return R); i ← i + 1
L12     else if h_B[j] > h_A[i] then (if j = |B| then return R); j ← j + 1
L13     else (if i = |A| or j = |B| then return R); i ← i + 1, j ← j + 1
```

MERGE-H is MERGE-V with the roles of width and height exchanged: it starts at the widest entry of each list and moves the pointer of the wider part. The idea of MERGE-V is in lines L11 to L13. The height of the combination is the height of the taller part, so the only way to get a lower combination is to give the taller part its next, lower shape. The other part keeps its narrowest shape that is low enough. Each entry of $R$ is the narrowest combination with its height.

## Example

The tree is $E = 1\,2\,V\,3\,4\,V\,H$: blocks 1 and 2 side by side at the bottom, blocks 3 and 4 side by side on top. The blocks are $1: 2 \times 4$, $2: 1 \times 3$, $3: 3 \times 2$ and $4: 2 \times 2$ (width by height), and each one may turn.

| node | front (width by height) | how it is made |
|---|---|---|
| 1 | $2 \times 4$, $4 \times 2$ | the two orientations |
| 2 | $1 \times 3$, $3 \times 1$ | the two orientations |
| $1\,2\,V$ | $3 \times 4$, $5 \times 3$, $7 \times 2$ | $(2{\times}4, 1{\times}3)$, then move 1, then move 2 |
| 3 | $2 \times 3$, $3 \times 2$ | the two orientations |
| 4 | $2 \times 2$ | a square has one shape |
| $3\,4\,V$ | $4 \times 3$, $5 \times 2$ | $(2{\times}3, 2{\times}2)$, then move 3; then the heights are equal and 4 is at its end |
| root, $H$ | $4 \times 7$, $5 \times 5$, $7 \times 4$ | see below |

MERGE-H at the root starts with the widest entries $7 \times 2$ and $5 \times 2$, which give $7 \times 4$. The first part is wider, so it moves to $5 \times 3$, which gives $5 \times 5$. Now both widths are 5, so both move, to $3 \times 4$ and $4 \times 3$, which give $4 \times 7$. The second part is wider and at its end, so the merge stops. The areas are 28, 25 and 28, so the least area is 25. The back pointers of $5 \times 5$ lead to $5 \times 3$ and $5 \times 2$, and from there to block 1 turned to $4 \times 2$, block 2 as $1 \times 3$, block 3 as $3 \times 2$ and block 4. The block area is 21, so 4 units are empty. Without any turn the floorplan is $5 \times 6 = 30$.

## Correctness

Two facts carry the proof. First, the width and the height of a node only grow when the width or the height of a part grows. So a part may replace a dominated shape by one that dominates it, and the front of a node is the front of the combinations of the fronts of its children. Second, MERGE-V keeps this invariant: when it writes an entry of height $M$, every earlier entry of each list is taller than $M$. Then the current pair is the narrowest combination of height at most $M$, so it is on the front. A lower combination must lower the taller part, which is the move of lines L11 to L13, so no front pair is skipped. The area is monotone in both coordinates, so the least area is on the root front. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Each step of a merge, except the last one, moves at least one pointer. So a merge of fronts of lengths $p$ and $q$ takes $O(p + q)$ time and returns at most $p + q - 1$ entries. By induction, a node with $\ell$ blocks below it has at most $\ell + 1$ entries when each block has two orientations, and at most $K - (\ell - 1)$ entries when the blocks below it have $K$ non-dominated shapes in total.

- **Time.** The merge at a node costs $O(\ell)$, and the sum of $\ell$ over the internal nodes counts each block one time for each ancestor. So the time is $O(n d)$ with two shapes for each block, and $O(K d)$ for lists with $K$ shapes in total, plus the sorting of the input lists.
- **Worst and best.** The depth is at most $n - 1$, so the worst case is $O(n^2)$, for a tree that is a long chain. A balanced tree has depth $O(\log n)$, which gives $O(n \log n)$. If all fronts stay short, for example with square blocks, the time is $O(n)$.
- **Space.** The fronts of all nodes are kept for the back pointers, which is $O(n d)$ entries in the worst case. If only the least area is needed, the fronts of the children can be freed after the merge, and the space is $O(n)$ at a time on the stack.

Shi gave in 1995 an algorithm that takes $O(N \log N)$ time on every tree, where $N$ is the total number of shapes at the leaves, and a lower bound of $\Omega(N \log N)$ that matches it. Stockmeyer's bound and Shi's bound agree for balanced trees.

## Properties

- **Exact for a fixed tree.** The algorithm finds the least area over all realizations, not over a sample. It does not change the slicing tree.
- **Returns the whole front.** A floorplanner that has a limit on the width or on the aspect ratio takes the best entry of the front that obeys the limit.
- **Deterministic and integer.** All values are sums and maxima of the input integers.
- **Slicing only.** For a general floorplan, given by [constraint graphs](/floorplan-constraint-graphs/), Stockmeyer proved that the choice of orientations with the least area is NP-complete.

## Variants and improvements

- **Soft blocks.** A block of fixed area $A$ and variable aspect ratio has the shape curve $w h = A$. A staircase approximation of it gives a finite list, and the merge is the same. For an exact solution of soft blocks with a convex model, [geometric programming](/geometric-programming/) is used.
- **Shi's algorithm.** Shi changes the way the fronts are stored and merged, so that a chain-like tree no longer costs $O(N^2)$. The time is $O(N \log N)$ on every tree.
- **Inside a search.** [Wong-Liu floorplanning](/wong-liu-floorplanning/) calls the sizing for each new tree that the annealing visits. A move changes a small part of the tree, so only the fronts of the changed nodes and of their ancestors need a new merge.
- **Bounded fronts.** If the fronts are too long, keep only a fixed number of evenly spaced entries. The result is then a heuristic.

## When to use it

Use the algorithm whenever the floorplan is slicing and each block has a list of shapes: rotations, a few layouts of a macro, or a staircase approximation of a soft block. It gives the exact best sizes in near-linear time. It does not choose the slicing tree. That is the job of a search such as [Wong-Liu floorplanning](/wong-liu-floorplanning/).

## Pitfalls

- **Taking the best shape of each part.** The least area of a part is not the right choice for the parent. In the example, the least area of $1\,2\,V$ is $3 \times 4 = 12$ and the least area of $3\,4\,V$ is $5 \times 2 = 10$, but together they give $5 \times 6 = 30$, not 25. Keep the whole front.
- **Equal heights.** When the two heights are equal, both pointers must move. If only one moves, the next entry has the same height and a larger width, and the list is no longer a front.
- **The wrong end for H.** MERGE-H must start at the widest entries. Starting at the narrow end gives wrong pairs.
- **Duplicate shapes.** A square block gives the same shape twice. Remove duplicates and dominated shapes before the merge, or the length bound fails.
- **Recursion depth.** A chain of $n$ blocks has depth $n - 1$. Use the stack of the Polish expression, not a recursive walk.

## Implementations

The Python module takes a Polish expression and a list of shapes for each block. It builds the fronts with a stack, merges with MERGE-V and with MERGE-H by exchanging the coordinates, and follows the back pointers to the chosen shapes. The tests check the example, and compare the least area and the whole root front with all $2^n$ orientations of 600 random trees of up to 8 blocks, and with all choices of 300 random trees of up to 6 blocks with up to 3 shapes each. They also check the length bounds of the fronts.

## History

Otten introduced shape functions for slicing floorplans in 1982 and 1983, and added them at each cut. Stockmeyer gave the merge of non-dominated shape lists with the $O(n d)$ bound in 1983, in Information and Control, and proved that the orientation problem is NP-complete for general floorplans. Wong and Liu used the same combination of shapes inside their annealing floorplanner in 1986. Shi gave an algorithm with an optimal $O(N \log N)$ time in 1995.

## References
