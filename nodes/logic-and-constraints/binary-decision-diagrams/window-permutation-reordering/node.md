---
tag: 83R3H0
kind: algorithm
slug: window-permutation-reordering
name: Window permutation reordering
aliases:
- window permutation
area: logic-and-constraints/binary-decision-diagrams
level: advanced
summary: A BDD reordering heuristic. It tries all orders of each window of w adjacent levels by adjacent swaps, keeps the best order of the window, and repeats until no window improves the size.
model: word-ram
complexity:
  vars: {n: the number of variables, w: the window width, s: the size of the shared BDD at the start, p: the number of passes}
  time: {worst: O(p n w! 2^w s)}
  space: {extra: O(2^w s)}
properties: {deterministic: true, exact: false, online: false, recursive: false, in_place: true}
history:
  year: 1991
  people: [Masahiro Fujita, Yusuke Matsunaga, Taeko Kakuda, Nagisa Ishiura, Hiroyuki Sawada, Shuzo Yajima]
  note: Two groups reordered BDDs by exchanges of adjacent variables in 1991; the exhaustive search of a small window became the method called window permutation.
prereqs: [variable-ordering, reduced-ordered-bdd, bdd-sifting, steinhaus-johnson-trotter]
see_also: [bdd-sifting, variable-ordering, friedman-supowit-ordering, variable-ordering-np-hardness, steinhaus-johnson-trotter, generating-all-permutations, local-search, reduced-ordered-bdd]
sources:
  - paper: "Nagisa Ishiura, Hiroyuki Sawada and Shuzo Yajima, Minimization of binary decision diagrams based on exchanges of variables, ICCAD 1991"
    title: Ishiura, Sawada and Yajima, Minimization of binary decision diagrams based on exchanges of variables
    locator: the exchange of adjacent variables and the search over a window of levels
  - paper: "Masahiro Fujita, Yusuke Matsunaga and Taeko Kakuda, On variable ordering of binary decision diagrams for the application of multi-level logic synthesis, European Design Automation Conference 1991"
    title: Fujita, Matsunaga and Kakuda, On variable ordering of binary decision diagrams for the application of multi-level logic synthesis
    locator: the improvement of an order by exchanges of adjacent variables
  - paper: doi:10.1109/ICCAD.1993.580029
    title: Richard Rudell, Dynamic variable ordering for ordered binary decision diagrams, ICCAD 1993, pages 42 to 47
    locator: the swap of adjacent levels in place, and the comparison of window permutation with sifting
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 5, The variable-ordering problem (heuristics based on local changes of the order)
---

Window permutation is a local search for a better [variable order](/variable-ordering/) of a BDD. A window is a block of $w$ adjacent levels, usually with $w = 2$, 3 or 4. The method visits all $w!$ orders of the variables in the window by swaps of adjacent levels, puts the window into the best order that it saw, and moves the window one level down. It repeats the passes over the whole order until no window gives an improvement. The method came from Fujita, Matsunaga and Kakuda (1991) and Ishiura, Sawada and Yajima (1991). It uses the same swap as [sifting](/bdd-sifting/), and that swap changes only the two levels that it exchanges. It never makes the diagram larger, but it has no approximation guarantee, and its quality is known only from measurements.

## In plain words

A BDD asks yes or no questions in a fixed order, and the order changes the size of the diagram. Window permutation looks at a few neighbouring questions at a time, for example three. It tries every order of those three questions, counts the nodes for each, and keeps the best one. Then it moves one place along and does the same with the next three questions. When it reaches the end, it starts again from the top. It stops when a whole run gives no gain. The method only makes small changes, so it is safe and fairly cheap. But it can get stuck: a question that belongs far away cannot get there if each small step makes the diagram larger first.

## The problem

**Input:** a shared reduced ordered BDD with the variables $x_1, \ldots, x_n$ in an order $\pi$, its roots, and a window width $w$ with $2 \le w \le n$.

**Output:** the same root functions, with the same root ids, in a shared reduced ordered BDD with an order $\pi'$ such that

- the size for $\pi'$ is at most the size for $\pi$, and
- $\pi'$ is a local optimum for windows: no order of the variables on $w$ adjacent levels of $\pi'$ gives a smaller size.

The size counts the nodes that some root reaches, with the sinks.

## The algorithm

The basic step is the swap of two adjacent levels, described on the page [sifting](/bdd-sifting/). It rewrites the nodes of the upper variable in place, so the node ids stay the same, and it changes no other level.

To visit all orders of a window, the method uses the [Steinhaus-Johnson-Trotter](/steinhaus-johnson-trotter/) sequence: a list of $w! - 1$ offsets $j \in \{0, \ldots, w - 2\}$ such that swapping the positions $j$ and $j + 1$ of the window, one offset after the other, visits each of the $w!$ orders once. For $w = 3$ the offsets are $1, 0, 1, 0, 1$.

```pseudo id=main
WINDOW-PERMUTATION(B, w)
L1  improved ← true; while improved do
L2      improved ← false
L3      for k ← 1 to n − w + 1 do
L4          start ← best ← size(B); best_window ← the variables on levels k to k + w − 1
L5          for each offset j of the Steinhaus-Johnson-Trotter sequence for w do
L6              swap the levels k + j and k + j + 1
L7              if size(B) < best then best ← size(B); best_window ← the variables on levels k to k + w − 1
L8          move the variables of best_window back to levels k to k + w − 1, in that order, by swaps
L9          if best < start then improved ← true
L10 return size(B)
```

Line L8 moves the first variable of `best_window` up to level $k$, then the second up to level $k + 1$, and so on. This takes at most $w(w-1)/2$ swaps. If no order of the window was better, `best_window` is the start order of the window, and line L8 restores it.

## Example

Take $f = x_1 x_2 \vee x_3 x_4 \vee x_5 x_6$ with the order $x_1, x_3, x_5, x_2, x_4, x_6$. Its BDD has 16 nodes, and the optimum is 8. The tables list each window that improved the size; the other windows left the order as it was. These numbers come from the implementation.

With $w = 2$:

| pass | window levels | size before | size after | order after |
|---|---|---|---|---|
| 1 | 3, 4 | 16 | 12 | $x_1, x_3, x_2, x_5, x_4, x_6$ |
| 1 | 4, 5 | 12 | 10 | $x_1, x_3, x_2, x_4, x_5, x_6$ |
| 2 | 2, 3 | 10 | 8 | $x_1, x_2, x_3, x_4, x_5, x_6$ |
| 3 | none | 8 | 8 | same |

With $w = 3$:

| pass | window levels | size before | size after | order after |
|---|---|---|---|---|
| 1 | 2 to 4 | 16 | 10 | $x_1, x_2, x_3, x_5, x_4, x_6$ |
| 1 | 3 to 5 | 10 | 8 | $x_1, x_2, x_3, x_4, x_5, x_6$ |
| 2 | none | 8 | 8 | same |

Both widths reach the optimum here. The wider window needs one pass fewer, but each window costs 5 swaps plus the swaps back instead of 1.

A local optimum need not be good. For one random function of 8 variables, an OR of random products of two variables (seed 5), the start order has 15 nodes. Windows of 2 and of 3 levels both stop at 14 nodes, sifting reaches 11 nodes, and the optimum is 10 nodes.

## Correctness

Each swap keeps the root functions and ids and gives the reduced diagram for the new order, by the swap lemma on the page [sifting](/bdd-sifting/). By [canonicity](/bdd-canonicity/), the size depends only on the order.

- **One window.** The Steinhaus-Johnson-Trotter sequence visits all $w!$ orders of the window, and the order outside the window never changes. Line L8 restores the window order with the smallest recorded size, so after the window the size is `best`, at most `start`.
- **Termination.** A pass that sets `improved` makes the size smaller by at least 1. So there are at most $s$ such passes, plus one last pass without an improvement.
- **Local optimum.** In the last pass no window improved, so each window ended in its start order, and the order did not change during that pass. So each window of the final order was searched completely, and none of its orders is smaller.

The full proof is in [the proof file](proofs/correctness.md).

## Complexity

**Swaps.** A window costs $w! - 1$ swaps for the search and at most $w(w - 1)/2$ swaps back. A pass has $n - w + 1$ windows, so it makes $O(n \cdot w!)$ swaps. For $w = 3$ this is at most 8 swaps per window.

**Size during the search.** Fix a window on levels $k$ to $k + w - 1$. The levels outside the window keep their nodes, by the swap lemma. Each node inside the window is a subfunction $g|_\gamma$, where $g$ is one of the at most $s'$ functions that cross the top of the window ($s'$ is the current size) and $\gamma$ fixes fewer than $w$ window variables. So for every order of the window the size is at most $2^w s'$, and since the size never ends a window above its start, $s' \le s$.

**Time.** In the implementation on this page, a swap with its garbage collection takes time linear in the size, so a pass takes $O(n \cdot w! \cdot 2^w s)$ time, and $p$ passes take $p$ times as much. In theory $p$ can be as large as $s$; in the example above $p$ is 2 or 3. With Rudell's swap, which costs time linear in the number of nodes on the two levels, a pass is faster in practice. The extra space is the largest intermediate size, $O(2^w s)$.

## Properties

- **Keeps the functions and the ids.** The roots have the same ids and functions after each swap.
- **Never grows the size.** Each window ends at most at its start size.
- **Local optimum for windows** at the end, as shown above.
- **No approximation guarantee.** Improving the order is [NP-complete](/variable-ordering-np-hardness/), and no polynomial-time method has a constant-factor guarantee unless P = NP.
- **Short moves only.** A variable moves at most $w - 1$ levels per window, and it moves far only if every window on the way gives a strict gain. This is the main weakness against sifting.

## Variants and improvements

- **Width.** Packages offer $w = 2$, 3 and 4. The cost per window grows as $w!$, so larger windows are rare.
- **One pass or until convergence.** Some packages make one pass; others repeat the passes, as here.
- **Combination with sifting.** Window permutation after sifting can fix small local errors that sifting leaves, because sifting moves only one variable at a time.
- **[Sifting](/bdd-sifting/)** moves one variable over all levels, so it can make long moves through bad intermediate orders.
- **Exact search.** The [Friedman-Supowit](/friedman-supowit-ordering/) program is exact, but takes $O(n^2 3^n)$ time.

## When to use it

Use window permutation as a cheap local improvement, or after sifting as a final cleanup. It is a good choice when the order is already close to good, for example when only a few neighbouring variables are in the wrong order. When the order is far from good, sifting usually does better. On 200 random functions of 8 variables (seed 5, see the page [variable ordering](/variable-ordering/)), windows of 3 levels reached the optimum in 137 cases, windows of 2 levels in 90 cases, and sifting in 193 cases. These are measurements on one small family of functions, not a guarantee.

## Pitfalls

- **Dead nodes.** As with sifting, the size must count only the reached nodes, so dead nodes must be collected after each swap.
- **Restore the best order, not the last one.** After the $w! - 1$ swaps the window is in the last order of the sequence, not the start order. Line L8 is needed even when no order was better.
- **Strict improvement.** Use a strict comparison at line L7 and line L9. With a non-strict one, the passes can cycle between orders of the same size.
- **Large windows.** With $w = 5$ a window costs 119 swaps, and the intermediate sizes can grow by a factor up to $2^w$.

## Implementations

## History

Fujita, Matsunaga and Kakuda (1991) improved BDD orders by exchanges of adjacent variables for logic synthesis. Ishiura, Sawada and Yajima (1991) also minimized BDDs by exchanges of variables, and searched over all orders of a few adjacent levels. Rudell (1993) made the swap work in place inside a BDD package, which made all these methods dynamic, and compared window permutation with his new sifting method. Packages such as CUDD offer windows of 2, 3 and 4 levels next to sifting. Bollig and Wegener (1996) showed that improving the order is NP-complete, so local methods of this kind are the practical choice.

## References
