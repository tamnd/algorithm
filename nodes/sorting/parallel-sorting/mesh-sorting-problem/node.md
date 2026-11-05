---
tag: KF3BDB
kind: problem
slug: mesh-sorting-problem
name: Mesh sorting problem
aliases:
- sorting on a mesh
area: sorting/parallel-sorting
level: advanced
summary: Sort n keys held one per processor of a square mesh, where only neighbours communicate.
prereqs: [parallel-sorting-problem, odd-even-transposition-sort, zero-one-principle]
see_also: [shearsort, odd-even-transposition-sort, columnsort, permutation-routing, dimension-order-routing, bitonic-sort, parallel-sorting-problem, zero-one-principle]
sources:
  - book: isbn:9781558601178
    title: F. Thomson Leighton, Introduction to Parallel Algorithms and Architectures, Arrays, Trees, Hypercubes, Morgan Kaufmann, 1992
    locator: Chapter 1, Arrays and trees (sorting on linear and two-dimensional arrays, shearsort, and lower bounds for mesh sorting)
  - paper: "C. D. Thompson and H. T. Kung, Sorting on a mesh-connected parallel computer, Communications of the ACM 20(4), 1977"
    locator: sorting a square mesh of n processors in O(sqrt n) steps by a merge sort
  - paper: "Claus P. Schnorr and Adi Shamir, An optimal sorting algorithm for mesh connected computers, Proceedings of the 18th ACM Symposium on Theory of Computing (STOC), 1986"
    locator: an upper bound of 3 sqrt n + o(sqrt n) steps for snake order, and a lower bound of 3 sqrt n - o(sqrt n) steps
  - paper: "Isaac D. Scherson, Sandeep Sen and Adi Shamir, Shear sort: a true two-dimensional sorting technique for VLSI networks, Proceedings of the International Conference on Parallel Processing (ICPP), 1986"
    locator: shearsort, with about sqrt n (lg n + 1) steps
---

The mesh sorting problem asks to sort $n$ keys on a square mesh of $\sqrt{n} \times \sqrt{n}$ processors, one key per processor, where each processor talks only to its four neighbours. The output must put the keys in a fixed order of the processors, usually row-major or snake order. The cost is the number of parallel steps, and the diameter of the mesh gives a lower bound of $2\sqrt{n} - 2$ steps. The best algorithms take about $3\sqrt{n}$ steps for snake order, and this is optimal up to lower-order terms.

## In plain words

People sit in a square hall, in rows and columns, each with a number card. Each person can pass cards only to the person in front, behind, left or right. They must end up with the cards in order, row by row.

Moving a card across the hall takes many passes, one seat at a time. So the smallest card, if it starts in the far corner, needs as many steps as there are seats along the edges between the corners. Good methods sort the whole hall in a few times that number of steps, by sorting rows and columns again and again in clever ways.

## Definition

**Machine.** A mesh of $r$ rows and $c$ columns has a processor $P(i, j)$ for $0 \le i < r$ and $0 \le j < c$. Processor $P(i, j)$ has a link to each of $P(i \pm 1, j)$ and $P(i, j \pm 1)$ that exists. The square case has $r = c = \sqrt{n}$. Each processor holds one key. In one step, each processor can send one key along each of its links and do $O(1)$ local work. A step of the common special form is a set of compare-exchanges on disjoint pairs of neighbours, as in [odd-even transposition sort](/odd-even-transposition-sort/).

**Input.** Keys from a total order, one in each processor.

**Output.** The same keys, one in each processor, sorted with respect to a fixed indexing of the processors. The common indexings are:

- **Row-major.** $P(i, j)$ gets the key of rank $ic + j$.
- **Snake order.** Row $i$ runs left to right when $i$ is even and right to left when $i$ is odd, so $P(i, j)$ gets rank $ic + j$ for even $i$ and $ic + c - 1 - j$ for odd $i$. Consecutive ranks are always neighbours.
- **Column-major.** As row-major with the roles of rows and columns swapped.

**Cost.** The number of steps in the worst case over the inputs. The total work is not the main measure, because all $n$ processors run in every step.

## Variants

- **Linear array.** For $r = 1$, the mesh is a line of $n$ processors. Odd-even transposition sort takes $n$ steps, and the diameter gives a lower bound of $n - 1$.
- **Higher dimensions.** A $d$-dimensional mesh with side $n^{1/d}$ has diameter $d(n^{1/d} - 1)$, and sorting on it takes $\Theta(d \, n^{1/d})$ steps for fixed $d$.
- **Torus.** A mesh with wrap-around links has half the diameter, about $\sqrt{n}$, and the bounds change by constant factors.
- **Many keys per processor.** With $k$ keys per processor, each compare-exchange becomes a merge-split of two sorted blocks of $k$ keys, and the step count is multiplied by the cost of a merge-split.
- **Oblivious algorithms.** An algorithm whose compare-exchange pattern does not depend on the keys is a [sorting network](/sorting-network/) laid out on the mesh. For these the [zero-one principle](/zero-one-principle/) applies, which is how most mesh sorts are proved.

## Examples

**A 2 by 2 mesh.** Let the keys be $\begin{smallmatrix} 4 & 1 \\ 3 & 2 \end{smallmatrix}$. In snake order the target is $\begin{smallmatrix} 1 & 2 \\ 4 & 3 \end{smallmatrix}$. Sort the rows in alternating directions, giving $\begin{smallmatrix} 1 & 4 \\ 3 & 2 \end{smallmatrix}$. Then compare-exchange each column, top smaller, giving $\begin{smallmatrix} 1 & 2 \\ 3 & 4 \end{smallmatrix}$. Sort the rows in alternating directions again, giving $\begin{smallmatrix} 1 & 2 \\ 4 & 3 \end{smallmatrix}$. This is [shearsort](/shearsort/) in three steps.

**The corner argument.** On a $4 \times 4$ mesh, put the smallest key at $P(3, 3)$. In row-major and in snake order it must end at $P(0, 0)$, which is $3 + 3 = 6$ links away. A key moves at most one link per step, so any algorithm needs at least $6$ steps on this input. For a $1024 \times 1024$ mesh with $n = 2^{20}$ keys, the same argument gives $2046$ steps, while shearsort takes $1024 \cdot 21 = 21504$ steps and the algorithm of Schnorr and Shamir about $3 \cdot 1024 = 3072$ steps plus lower-order terms.

## Known algorithms

All step counts are for a $\sqrt{n} \times \sqrt{n}$ mesh with one key per processor.

| algorithm | output order | steps |
| --- | --- | --- |
| [Odd-even transposition sort](/odd-even-transposition-sort/) on the snake | snake | $n$ |
| [Shearsort](/shearsort/) | snake | $\sqrt{n}(\lg n + 1)$, for $\sqrt{n}$ a power of 2 |
| [Columnsort](/columnsort/) on the mesh | column-major | $O(\sqrt{n})$ |
| [Bitonic sort](/bitonic-sort/) laid out on the mesh | row-major with shuffled indexing | $O(\sqrt{n})$ |
| Thompson and Kung | row-major and snake | $O(\sqrt{n})$ |
| Schnorr and Shamir | snake | $3\sqrt{n} + o(\sqrt{n})$ |

## Bounds

**Diameter.** For row-major or snake order, the smallest key must end at $P(0, 0)$. If it starts at $P(\sqrt{n} - 1, \sqrt{n} - 1)$, it must cross $2\sqrt{n} - 2$ links, one per step at most. So every algorithm needs at least $2\sqrt{n} - 2$ steps. The same argument for any target order gives the largest distance between a processor and the target of the smallest key.

**Bisection.** The links between the left half and the right half of the mesh number $\sqrt{n}$. If all keys in the left half must move to the right half, at least $n/2$ keys cross these links, and at most $\sqrt{n}$ cross in each direction per step, so at least $\sqrt{n}/2$ steps are needed. This bound is weaker than the diameter bound for meshes, but it is the stronger one for some other networks.

**The constant 3.** Schnorr and Shamir proved that sorting into snake order needs $3\sqrt{n} - o(\sqrt{n})$ steps in a model where each processor holds one key and moves keys only to neighbours, and they gave an algorithm with $3\sqrt{n} + o(\sqrt{n})$ steps. The argument for the lower bound uses the fact that the keys in one corner region cannot have any effect on far-away processors until late in the computation, so the algorithm must decide where they go only near its end.

**Linear array.** On a line of $n$ processors, $n - 1$ steps are needed by the diameter argument, and odd-even transposition sort uses $n$.

## Reductions

- **Rows and columns to lines.** Each row and each column of a mesh is a linear array, so one row or column sort by odd-even transposition takes $\sqrt{n}$ steps, on all rows or all columns at once.
- **Sorting to routing.** Once each key knows its rank, sorting is a [permutation routing](/permutation-routing/) problem. On a mesh, routing a permutation by [dimension-order routing](/dimension-order-routing/) takes $2\sqrt{n} - 2$ steps with queues at the processors. But computing the ranks is itself a sort, so this reduction does not give a fast sort by itself.
- **Matrix sorts to mesh sorts.** Algorithms such as [columnsort](/columnsort/) that only sort rows, sort columns and apply fixed permutations run on a mesh, with each fixed permutation done by routing in $O(\sqrt{n})$ steps.

## Applications

- **VLSI sorters.** Mesh sorts need only short wires of equal length, which suits chips with processors in a grid.
- **Image and grid computing.** Data that lives on a 2D grid of processors, such as image pixels or the cells of a simulation, is sorted in place on the grid.
- **Lower bounds for other networks.** The diameter and bisection arguments carry over to other fixed networks, and the mesh is the standard example of how the network limits parallel sorting.

## References
