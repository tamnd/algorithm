---
tag: KV4EXG
kind: algorithm
slug: bdd-sifting
name: Rudell's sifting
aliases:
- dynamic variable reordering by sifting
- sifting algorithm
area: logic-and-constraints/binary-decision-diagrams
level: advanced
summary: A reordering heuristic for BDDs. Each variable in turn moves through all levels by swaps of adjacent levels and then goes back to the level with the smallest size (Rudell 1993).
model: word-ram
complexity:
  vars: {n: the number of variables, s: the size of the shared BDD at the start}
  time: {worst: O(n^2 s)}
  space: {extra: O(s)}
properties: {deterministic: true, exact: false, online: false, recursive: false, in_place: true}
history:
  year: 1993
  people: [Richard Rudell]
  note: Rudell gave sifting and the swap of two adjacent levels in place, so that a BDD package can reorder its variables while it runs.
prereqs: [variable-ordering, reduced-ordered-bdd, bdd-canonicity, local-search]
see_also: [variable-ordering, window-permutation-reordering, friedman-supowit-ordering, variable-ordering-np-hardness, reduced-ordered-bdd, computed-table, reference-counting, local-search]
sources:
  - paper: doi:10.1109/ICCAD.1993.580029
    title: Richard Rudell, Dynamic variable ordering for ordered binary decision diagrams, ICCAD 1993, pages 42 to 47
    locator: the sifting algorithm, the swap of adjacent levels in place, and the experiments
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 5, The variable-ordering problem (heuristics and the swap of adjacent variables)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (reordering by swaps of adjacent levels, and sifting)
  - paper: doi:10.1109/12.537122
    title: Beate Bollig and Ingo Wegener, Improving the variable ordering of OBDDs is NP-complete, IEEE Transactions on Computers 45(9), 1996, pages 993 to 1002
    locator: main theorem (the reason why packages use heuristics)
---

Sifting is the standard method that BDD packages use to improve the [variable order](/variable-ordering/) while they run. It takes the variables one at a time. It moves the current variable through all the levels of the shared [reduced ordered BDD](/reduced-ordered-bdd/) by swaps of two adjacent levels, records the size at each level, and then moves the variable back to the level with the smallest size. Rudell (1993) gave the method together with a swap that rewrites the nodes in place, so the node ids that the user holds stay valid. A swap changes only the two levels that it exchanges. Sifting never makes the diagram larger, but it has no approximation guarantee: finding the best order is [NP-hard](/variable-ordering-np-hardness/), and the quality of sifting is known only from measurements.

## In plain words

A BDD asks yes or no questions in a fixed order, and a good order can make the diagram much smaller. Sifting tries to find a better order by small steps. Pick one question. Move it one place up or down in the order, and count the nodes. Go on until the question has visited every place. Then put it back at the place where the count was smallest. Do this for each question, one after the other. Each step exchanges only two neighbouring questions, and that change is cheap, because only the nodes of those two questions change. The method is greedy. It often finds a good order, but nothing guarantees that it finds the best one.

## The problem

**Input:** a shared reduced ordered BDD with the variables $x_1, \ldots, x_n$ in an order $\pi$, and a set of roots, the functions that the user holds.

**Output:** the same functions, with the same root ids, in a shared reduced ordered BDD with an order $\pi'$ whose size is at most the size for $\pi$. The size counts the nodes that some root reaches, with the sinks.

Sifting does not solve the optimization problem exactly. It returns a local optimum: after the step for a variable $v$, no other level of $v$, with the order of the other variables fixed, gives a smaller size.

## The algorithm

The basic step is the swap of the variables on levels $k$ and $k+1$. Let $x$ be on level $k$ and $y$ on level $k+1$. A node $u$ that tests $x$ has a low child $f_0$ and a high child $f_1$. Write $f_{ab}$ for the function of $u$ with $x = a$ and $y = b$. If a child tests $y$, its children give $f_{a0}$ and $f_{a1}$; otherwise both are the child itself. By the [Shannon expansion](/shannon-expansion/) in the other order,

$$f_u = \neg y \, (\neg x \, f_{00} \vee x \, f_{10}) \vee y \, (\neg x \, f_{01} \vee x \, f_{11}).$$

So the swap does this for each node $u$ on level $k$:

- If no child of $u$ tests $y$, then $f_u$ does not depend on $y$, and $u$ stays as it is. It moves down to level $k + 1$ with $x$.
- Otherwise rewrite $u$ in place as a $y$-node with the low child MK$(x, f_{00}, f_{10})$ and the high child MK$(x, f_{01}, f_{11})$.

Here MK is the node constructor with the unique table of $x$: it returns the low child if the two children are equal, and the one node with this key otherwise. The node $u$ keeps its id and its function, so all the pointers from above stay correct. The old $y$-nodes that only $u$ used become dead, and a garbage collection removes them. No node above level $k$ or below level $k + 1$ changes.

Sifting uses the swap as follows. The growth limit $g$ (for example $g = 2$) ends a move early when the size gets much larger than the best size so far.

```pseudo id=main
SIFT(B, g)
L1  for each variable v, in the order of decreasing number of nodes do
L2      best ← size(B); best_pos ← level(v)
L3      choose the direction to the nearer end first, the other direction second
L4      for each direction d of the two do
L5          while v can move one level in direction d do
L6              swap v with its neighbour in direction d
L7              if size(B) < best then best ← size(B); best_pos ← level(v)
L8              if size(B) > g · best then stop the moves in this direction
L9      move v back to level best_pos by swaps
L10 return size(B)
```

Line L1 takes the variables with many nodes first, as Rudell did, because they give the largest gains. Line L3 goes to the nearer end first, so the first move is short. At line L9 the order of the other variables is the same as when the size `best` was recorded, so the size is `best` again.

## Example

Take $f = x_1 x_2 \vee x_3 x_4 \vee x_5 x_6$ with the bad order $x_1, x_3, x_5, x_2, x_4, x_6$. Its BDD has 16 nodes. The numbers of nodes per variable are 1, 4, 2, 2, 4 and 1 for $x_1, \ldots, x_6$, so sifting takes $x_2$ and $x_5$ first. The table gives the size with the variable on each level 1 to 6 (the other variables keep their order), and the growth limit is $g = 2$. These numbers come from the implementation.

| step | variable | size on levels 1 to 6 | best level | size after | order after |
|---|---|---|---|---|---|
| start | | | | 16 | $x_1, x_3, x_5, x_2, x_4, x_6$ |
| 1 | $x_2$ (level 4) | 10, 10, 12, 16, 16, 16 | 2 | 10 | $x_1, x_2, x_3, x_5, x_4, x_6$ |
| 2 | $x_5$ (level 4) | 12, 12, 10, 10, 8, 8 | 5 | 8 | $x_1, x_2, x_3, x_4, x_5, x_6$ |
| 3 to 6 | $x_3$, $x_4$, $x_1$, $x_6$ | no level is better | same | 8 | same |

In step 1, $x_2$ is on level 4, which is not nearer to the top end, so it goes up first: the sizes are 12, 10 and 10 on levels 3, 2 and 1. Then it goes down to level 6. The first strict minimum is on level 2. The final order pairs each $x_{2i-1}$ with $x_{2i}$, and 8 nodes is the optimum for this function.

## Correctness

Two facts carry the proof.

- **The swap is correct.** Each rewritten node keeps its function, by the expansion above. The result has no node with equal children, because a rewritten node depends on $y$. It has no two nodes with the same key on one level: a new $x$-node has no $y$-child, so it cannot match an $x$-node that is still to be rewritten, and a rewritten node has an $x$-child on level $k + 1$, so it cannot match an old $y$-node. So the store is again a reduced ordered BDD, and by [canonicity](/bdd-canonicity/) it is the unique one for the new order.
- **The size depends only on the order.** By canonicity, the size of the shared reduced diagram is a function of the roots and the order. Line L9 restores an order that was seen at line L7, so the size is `best`, which is at most the size at line L2.

So each step keeps the functions and does not increase the size, and the result after all steps is at most the start size. The full proof is in [the proof file](proofs/correctness.md).

## Complexity

One swap of levels $k$ and $k + 1$ visits the $x$-nodes and makes at most two new $x$-nodes for each of them. With the unique tables per variable and [reference counts](/reference-counting/) to find the dead nodes, Rudell's swap takes time proportional to the number of nodes on the two levels. The implementation on this page uses a simpler garbage collection, which takes $O(s)$ time per swap.

One pass of sifting makes $O(n^2)$ swaps. A variable on level $l$ moves at most $\min(l, n - 1 - l)$ levels to the nearer end, then at most $n - 1$ levels to the other end, then at most $n - 1$ levels back, so at most $2.5n$ swaps per variable.

A swap at most doubles the size, because each $x$-node gives at most two new $x$-nodes. The growth limit stops a move after the first size above $g$ times the best size, so every size in the pass is at most $2g$ times the start size $s$. With $g$ fixed, one pass takes $O(n^2 s)$ time and $O(s)$ extra space in this implementation. Without the growth limit, the intermediate sizes can be exponential in $n$.

## Properties

- **Keeps the functions and the ids.** The roots have the same ids and the same functions after sifting, so a package can sift between two user operations.
- **Never grows the size.** The final size is at most the start size.
- **No approximation guarantee.** By [Sieling's theorem](/variable-ordering-np-hardness/), no polynomial-time method finds a size within a constant factor of the optimum unless P = NP. Sifting runs in polynomial time per pass when the sizes stay polynomial.
- **Local optimum per step.** After the step for $v$, no level of $v$ visited at lines L5 to L8 gives a smaller size with the other variables in their order. The next steps can change this.
- **Depends on the start.** The result depends on the start order and on the order in which the variables are taken.

## Variants and improvements

- **Sifting to convergence.** Repeat the passes while the size goes down.
- **Symmetric and group sifting.** Move groups of variables together, for example symmetric variables or the present-state and next-state variables of a transition relation (Panda and Somenzi 1995).
- **Linear sifting.** Also try the linear transformation $x \mapsto x \oplus y$ at each swap (Meinel, Somenzi and Theobald 1997).
- **Window permutation.** [Window permutation](/window-permutation-reordering/) tries all orders of a few adjacent levels instead of moving one variable far. It is the older method.
- **Lower bounds.** Stop a move when a lower bound on the size in that direction is already larger than the best size.
- **Exact method for small $n$.** The [Friedman-Supowit](/friedman-supowit-ordering/) program finds the optimum in $O(n^2 3^n)$ time from a truth table.

## When to use it

Use sifting when a BDD computation runs out of memory or time and the order may be the cause. Most packages start it automatically when the number of nodes passes a threshold, and raise the threshold after each run. Sifting is the default first choice because each pass is cheap and it often gives a large gain. On a small test, 200 random functions of 8 variables (an OR of 3 to 6 random products of two variables, seed 5), it reached the optimum in 193 cases; the same test is on the page [variable ordering](/variable-ordering/). These are measurements on one family of functions, not a guarantee.

Do not use sifting when the order must stay fixed, for example when node ids are stored as keys outside the package with the order as part of their meaning, or when no order can help, as for the [middle bit of multiplication](/multiplier-bdd-lower-bound/).

## Pitfalls

- **Dead nodes.** The size must count only the nodes that a root reaches. Without garbage collection after each swap, the counts include the dead $y$-nodes, and the method takes wrong decisions.
- **External references.** All the nodes that the user holds must be roots. A node that is held but not registered can be collected or changed by a swap.
- **Computed table.** A rewritten node keeps its function, so cached results stay true, but entries that point to collected nodes must be removed.
- **Growth.** Without a growth limit, one move can make the diagram very large in the middle of a pass and exhaust the memory.
- **Complemented edges.** With [complemented edges](/complemented-edges/), the swap must keep the normal form, for example no complement on the high edge, when it makes the new $x$-nodes.

## Implementations

## History

Fujita, Matsunaga and Kakuda (1991) and Ishiura, Sawada and Yajima (1991) reordered BDDs by exchanges of adjacent variables in a window. Rudell (1993) made reordering dynamic. His swap rewrites the nodes in place, so a package can reorder in the middle of a computation without a change of the user's node ids, and his sifting moves each variable over the whole order. Sifting became the default reordering of BDD packages such as CUDD. Later work moved groups of variables (symmetric and group sifting) and added linear transformations (linear sifting). Bollig and Wegener (1996) showed that improving the order is NP-complete, and Sieling (2002) that no constant-factor approximation exists unless P = NP, so heuristics are the practical method.

## References
