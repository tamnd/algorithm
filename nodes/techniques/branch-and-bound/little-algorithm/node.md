---
tag: 10HFCT
kind: algorithm
slug: little-algorithm
name: Little's algorithm
aliases:
- Little-Murty-Sweeney-Karel algorithm
- branch and bound for TSP
area: techniques/branch-and-bound
level: core
summary: Branch and bound for the TSP that branches on including or excluding an arc and bounds with a reduced cost matrix.
solves: [traveling-salesman-problem, asymmetric-tsp]
model: real-ram
complexity:
  vars: {n: the number of cities, N: the number of nodes of the search tree}
  time: {worst: O(N (n^3 + log N))}
  space: {extra: O(N n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [traveling-salesman-problem, best-first-branch-and-bound, bounding-function]
see_also: [held-karp-algorithm, assignment-problem, hungarian-algorithm, branching-rule, subtour-elimination-lp, nearest-neighbor-tsp, gilmore-lawler-bound, land-doig-algorithm]
sources:
  - paper: doi:10.1287/opre.11.6.972
    title: John D. C. Little, Katta G. Murty, Dura W. Sweeney and Caroline Karel, An algorithm for the traveling salesman problem, Operations Research 11(6), 1963
    locator: pp. 972 to 989
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 8, Branch-and-Bound (traveling salesperson, reduced cost matrix)
  - paper: doi:10.1287/opre.14.4.699
    title: E. L. Lawler and D. E. Wood, Branch-and-bound methods, a survey, Operations Research 14(4), 1966
    locator: pp. 699 to 719
---

Little's algorithm finds a shortest tour of the [traveling salesman problem](/traveling-salesman-problem/) on a cost matrix, which need not be symmetric. It subtracts the smallest entry of each row and each column from the matrix; the sum of these amounts is a lower bound on every tour. It then picks one arc $(i, j)$ of reduced cost 0 and splits the set of tours in two: the tours that use the arc and the tours that do not. Little, Murty, Sweeney and Karel published it in 1963, in the paper that gave branch and bound its name.

## In plain words

A salesman must visit every city once and come back home. Each trip from one city to another has a price. Every city must be left once, so its cheapest way out is a price that every tour pays at least. Take that amount out of every row of the price table and remember the total. Do the same with the cheapest way into each city. The total taken out is a limit: no tour costs less.

Now some trips cost 0 in the new table. Pick the one that would hurt most to give up. Split the problem into two: tours that use this trip and tours that do not. Each part gets its own table and its own limit. Always work on the part with the smallest limit, and stop when a complete tour costs no more than every limit that is left.

## The problem

Given an $n \times n$ matrix $C$ with entries $c_{uv} \ge 0$ or $c_{uv} = \infty$ for a forbidden arc, find a cyclic order $\pi$ of the cities $1, \ldots, n$ that minimizes $\sum_{k} c_{\pi(k) \pi(k+1)}$, with $\pi(n+1) = \pi(1)$. The diagonal is ignored. If every cyclic order uses a forbidden arc, the answer is that there is no tour.

## The algorithm

A node is a triple $(lb, M, S)$. The set $S$ holds the arcs fixed in the tour, $M$ is a reduced matrix on the rows and columns of the cities that have no fixed arc out of them and no fixed arc into them, and $lb$ is the lower bound. The node stands for the tours that contain every arc of $S$ and no arc with $M_{uv} = \infty$. REDUCE$(M)$ subtracts from each row its smallest entry, then from each column its smallest entry, and returns the total. The *penalty* of a zero $M_{ij}$ is $\theta(i, j) = \min_{k \ne j} M_{ik} + \min_{k \ne i} M_{kj}$: the least amount that any tour without the arc $(i, j)$ must add to the bound.

```pseudo id=main
LITTLE(C)
L1  M ← C with ∞ on the diagonal; lb ← REDUCE(M)
L2  z ← ∞; best ← NIL; insert (lb, M, ∅) into a min-priority queue H
L3  while H is not empty do
L4      (lb, M, S) ← EXTRACT-MIN(H)                 ▷ the live node with the least bound
L5      if lb ≥ z then break                         ▷ no live node can beat z
L6      if |S| = n then                              ▷ a complete tour of cost lb
L7          z ← lb; best ← S; continue
L8      choose a zero M_ij with the largest penalty θ(i, j)
L9      if lb + θ(i, j) < z then                     ▷ exclude child: tours without (i, j)
L10         M′ ← M with M′_ij = ∞; reduce row i and column j of M′; insert (lb + θ(i, j), M′, S)
L11     M″ ← M without row i and column j; S″ ← S ∪ {(i, j)}   ▷ include child
L12     if |S″| < n − 1 then let s → ⋯ → e be the path of S″ through (i, j); M″_es ← ∞
L13     h ← REDUCE(M″)
L14     if lb + h < z then insert (lb + h, M″, S″) into H
L15 return (z, best)
```

Line L12 forbids the arc that would close the path through $(i, j)$ into a cycle shorter than $n$. When $n - 1$ arcs are fixed, they form one path through all cities, and the last arc must close it, so line L12 does nothing. After line L10, the smallest entry of row $i$ is the first term of $\theta(i, j)$ and the smallest entry of column $j$ is the second, so the reduction adds exactly $\theta(i, j)$. A penalty of $\infty$ means that the arc $(i, j)$ is the only way out of $i$ or into $j$, and then there is no exclude child.

## Example

Five cities, with the cost matrix (rows are the start, columns the end)

$$C = \begin{pmatrix} - & 13 & 14 & 2 & 9 \\ 17 & - & 16 & 13 & 10 \\ 16 & 12 & - & 19 & 7 \\ 17 & 5 & 10 & - & 5 \\ 4 & 20 & 9 & 18 & - \end{pmatrix}.$$

The row minima are $2, 10, 7, 5, 4$, with sum 28. After they are subtracted, column 3 has the smallest entry 5 and the other columns contain a 0, so the root bound is $28 + 5 = 33$. The reduced matrix is

$$M = \begin{pmatrix} \infty & 11 & 7 & 0 & 7 \\ 7 & \infty & 1 & 3 & 0 \\ 9 & 5 & \infty & 12 & 0 \\ 12 & 0 & 0 & \infty & 0 \\ 0 & 16 & 0 & 14 & \infty \end{pmatrix}.$$

| node taken | bound | arc chosen | penalty | exclude child | include child |
|---|---|---|---|---|---|
| root | 33 | $1 \to 4$ | $7 + 3 = 10$ | 43 | 33, forbid $4 \to 1$ |
| $\{1 \to 4\}$ | 33 | $5 \to 1$ | 7 | 40 | 33, forbid $4 \to 5$ |
| $\{1 \to 4, 5 \to 1\}$ | 33 | $3 \to 5$ | 5 | 38 | 34, forbid $4 \to 3$ |
| $\{1 \to 4, 5 \to 1, 3 \to 5\}$ | 34 | $2 \to 3$ | $\infty$ | none | 34 |
| $\{\ldots, 2 \to 3\}$ | 34 | $4 \to 2$ | $\infty$ | none | 34 |
| $\{\ldots, 4 \to 2\}$ | 34 | | | | complete tour, $z = 34$ |
| exclude $3 \to 5$ | 38 | | | | $38 \ge 34$: stop |

At the third step, the include child forbids $4 \to 3$, so row 2 has only the entry 1 left in column 3, and its reduction raises the bound to 34. The tour is $1 \to 4 \to 2 \to 3 \to 5 \to 1$ with cost $2 + 5 + 16 + 7 + 4 = 34$. The search makes 9 nodes, splits 5 of them, and never takes the exclude children with bounds 38, 40 and 43 apart.

## Correctness

For a node $(lb, M, S)$, every tour $T$ that the node stands for satisfies

$$\mathrm{cost}(T) = lb + \sum_{(u, v) \in T \setminus S} M_{uv}.$$

This holds at the root with $lb = 0$ and $M = C$. Subtracting $h$ from row $u$ keeps it true, because $T$ uses exactly one arc out of $u$ that is not in $S$; the same holds for columns. Fixing the arc $(i, j)$ with $M_{ij} = 0$ and deleting its row and column keeps it true too. As $M \ge 0$, this gives $\mathrm{cost}(T) \ge lb$, so $lb$ is a valid bound, and when $|S| = n$ the only tour is $S$ itself and its cost is $lb$.

The two children split the tours of a node: those without $(i, j)$ go to the exclude child, and those with $(i, j)$ go to the include child. Line L12 forbids only an arc that would make a cycle shorter than $n$ together with $S''$, which no tour has. So each tour of the parent is in exactly one child, every pruned node has only tours of cost at least $z$, and the loop ends with an optimal tour, as in [best-first branch and bound](/best-first-branch-and-bound/). Each step either fixes an arc or changes a finite entry to $\infty$, so the search is finite. The [proof](proofs/correctness.md) gives the details.

## Complexity

At a node with $m$ free rows, REDUCE takes $O(m^2)$ time. Line L8 as written, with a scan of the row and the column for each zero, takes $O(m^3)$ in the worst case; with the two smallest entries of each row and column stored, it takes $O(m^2)$. Copying the matrix takes $O(m^2)$. So with $N$ nodes the time is $O(N (n^3 + \log N))$ as written, and $O(N (n^2 + \log N))$ with the stored minima. Each live node holds a matrix, so the memory is $O(N n^2)$.

The number of nodes $N$ is exponential in $n$ in the worst case. The traveling salesman problem is NP-hard, and the reduced matrix bound is at most the value of the [assignment problem](/assignment-problem/) relaxation, which can be far below the cost of the shortest tour.

## Properties

- **Exact.** It returns a shortest tour, or reports that there is none.
- **Asymmetric costs.** Nothing in the method needs $c_{uv} = c_{vu}$.
- **Bound below the assignment bound.** The reduced matrix bound is a feasible dual solution of the assignment problem on $C$, so it is at most the optimal assignment value, which the [Hungarian algorithm](/hungarian-algorithm/) computes in $O(n^3)$ time.
- **Binary tree.** Every node has at most two children, and the include branch shrinks the matrix by one row and one column.
- **Free completion.** Once $n - 1$ arcs are fixed, the last arc is forced.

## Variants and improvements

- **Node order.** The page uses best-first order. With a depth-first order that takes the include child first, the search reaches complete tours early and keeps only $O(n)$ live nodes on the path, at the cost of more nodes; see [depth-first branch and bound](/depth-first-branch-and-bound/).
- **Branching on the next city.** Horowitz, Sahni and Rajasekaran describe a branch and bound for the traveling salesperson problem whose children fix the next city of a path, with the same reduced matrix bound.
- **Assignment bound.** Solving the assignment problem at each node gives a stronger bound. Arcs that the assignment uses form cycles, and the search can branch on the arcs of a short cycle.
- **Better bounds for symmetric costs.** The [Held-Karp](/held-karp-algorithm/) one-tree bound and the [subtour elimination LP](/subtour-elimination-lp/) are much stronger, and modern exact solvers use branch and cut on the LP.
- **A start tour.** A heuristic tour, such as from the [nearest neighbor](/nearest-neighbor-tsp/) rule, gives a finite $z$ from the start, so more nodes are pruned at lines L9 and L14.

## When to use it

Use Little's algorithm to solve small instances exactly, to teach branch and bound with a bound that is easy to compute by hand, or for asymmetric instances where simple code matters more than speed. For large instances use branch and cut with LP bounds.

## Pitfalls

- **Forgetting the subtour arc.** Without line L12, the include branch can fix arcs that form a cycle of fewer than $n$ cities, and the search returns something that is not a tour.
- **Forbidding the last arc.** When $n - 1$ arcs are fixed, the arc that closes the path is the one the tour needs. Forbidding it, as a rule of "always forbid $e \to s$" would, loses every tour.
- **Reducing the wrong lines.** In the exclude child, the row $i$ is reduced over all free columns and the column $j$ over all free rows. Reducing column $j$ only over row $i$ gives a bound that is too high and can prune the optimum.
- **Memory.** Each live node keeps a matrix. In best-first order with weak bounds, the queue can fill memory before the search ends.

## Implementations

## History

Little, Murty, Sweeney and Karel (1963) gave the method with the reduced matrix bound, the choice of the zero of largest penalty, and the split into the tours with and without one arc, and they used the name branch and bound for it. Lawler and Wood (1966) surveyed it with other early branch and bound methods. Horowitz, Sahni and Rajasekaran give the reduced cost matrix bound for the traveling salesperson problem in their chapter on branch and bound.

## References
