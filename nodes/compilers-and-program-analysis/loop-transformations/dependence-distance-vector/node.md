---
tag: 0X40N7
kind: definition
slug: dependence-distance-vector
name: Dependence distance vector
aliases:
- distance vector
area: compilers-and-program-analysis/loop-transformations
level: core
summary: The difference between the iteration vectors of the sink and the source of a dependence in a loop nest.
prereqs: [data-dependence]
see_also: [dependence-direction-vector, loop-carried-dependence, loop-transformation-legality, unimodular-transformations, loop-skewing, loop-tiling, lamport-hyperplane-method, practical-dependence-tests]
sources:
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 2 (distance and direction vectors, and the rule that the leftmost nonzero entry of a legal distance vector is positive)
  - paper: "Michael E. Wolf and Monica S. Lam, A loop transformation theory and an algorithm to maximize parallelism, IEEE Transactions on Parallel and Distributed Systems 2(4), 1991"
    locator: the representation of dependences by distance vectors, the legality condition for unimodular transformations, and fully permutable loops
  - paper: "Leslie Lamport, The parallel execution of DO loops, Communications of the ACM 17(2), 1974"
    locator: the sets of iteration differences of a loop nest and the hyperplane method that uses them
  - book: "Michael Wolfe, High Performance Compilers for Parallel Computing, Addison-Wesley, 1996"
    locator: the chapter on data dependence (distance vectors and direction vectors in loop nests)
---

The distance vector of a [data dependence](/data-dependence/) in a loop nest is the iteration vector of the sink minus the iteration vector of the source. If the sink $T(\vec{j})$ depends on the source $S(\vec{i})$, the distance is $\vec{d} = \vec{j} - \vec{i}$. It says how many iterations of each loop lie between the two accesses. Its first nonzero entry gives the loop that [carries](/loop-carried-dependence/) the dependence, and the distances of all dependences decide which reorderings of the loops are [legal](/loop-transformation-legality/). When the distance is not one fixed vector, compilers keep only its signs, the [direction vector](/dependence-direction-vector/).

## Definition

Let $S$ and $T$ have $k$ common loops, and let a dependence go from $S(\vec{i})$ to $T(\vec{j})$, where $\vec{i}, \vec{j} \in \mathbb{Z}^k$ are the parts of the iteration vectors for these loops. The **distance vector** of this pair of instances is

$$\vec{d} = \vec{j} - \vec{i} \in \mathbb{Z}^k.$$

The **distance set** of the dependence $S \to T$ of one kind is the set of all such vectors,

$$\Delta(S, T) = \{\, \vec{j} - \vec{i} : S(\vec{i}) \to T(\vec{j}) \,\}.$$

In the isl notation, this is the set of deltas of the dependence relation: for `{ S[i, j] -> S[i + 1, j - 1] : ... }` the deltas are `{ [1, -1] }`. The dependence is **uniform**, or has a *constant distance*, when $\Delta(S, T)$ has one element.

**Lexicographic sign.** Each distance vector is lexicographically positive or zero, $\vec{d} \succeq \vec{0}$. The source runs first, so $\vec{i} \preceq \vec{j}$ on the common loops: either $\vec{i} = \vec{j}$, or at the first index $l$ where they differ, $i_l < j_l$. In the first case $\vec{d} = \vec{0}$; in the second, $d_1 = \dots = d_{l-1} = 0$ and $d_l > 0$. A pair of accesses with $\vec{j} - \vec{i} \prec \vec{0}$ is a dependence in the other direction, from $T(\vec{j})$ to $S(\vec{i})$, and its distance is $\vec{i} - \vec{j}$.

**The zero vector.** $\vec{d} = \vec{0}$ means that the source and the sink run in the same iteration. Such a dependence is loop independent, not carried by any loop. It exists only between two different statements, with the source first in the body.

**Index values against iteration numbers.** The definition uses the values of the loop indices. For a loop with step $s \ne 1$, these values differ by multiples of $s$. Most texts first *normalize* each loop to start at 0 or 1 with step 1, and then measure distances in iterations. Say which one a table uses.

### When the distance is constant

Let $S$ access $X[F\vec{i} + \vec{f}]$ and $T$ access $X[G\vec{j} + \vec{g}]$, with integer matrices $F$ and $G$ of size $m \times k$. A dependence needs $F\vec{i} + \vec{f} = G\vec{j} + \vec{g}$.

- If $F = G$ (the two references are *uniformly generated*), then $F\vec{d} = \vec{f} - \vec{g}$. If moreover $F$ has full column rank, this has at most one solution $\vec{d}$, so the distance is constant whenever a dependence exists. In one dimension this is the case of the strong SIV test: $a i + c_1 = a j + c_2$ gives $d = (c_1 - c_2)/a$, see [practical dependence tests](/practical-dependence-tests/).
- If $F = G$ but $F$ has a nonzero kernel, the distances form the solutions of $F\vec{d} = \vec{f} - \vec{g}$ that fit in the bounds: one solution plus the kernel vectors. A loop index that the subscript does not use has every distance within its bounds.
- If $F \ne G$, the distance usually changes from one pair to the next.

## Examples and non-examples

### A constant distance

```
for i = 1 to n:
  for j = 1 to n:
    S: A[i][j] = A[i-1][j] + A[i][j-1]
```

$S(i, j)$ writes $A[i][j]$. $S(i+1, j)$ reads it as $A[i][j]$ through the first read, and $S(i, j+1)$ reads it through the second. So there are two flow dependences, with distances $(1, 0)$ and $(0, 1)$. There is no anti dependence: each element is read only after it is written. Both distances have nonnegative entries, so the two loops are *fully permutable*: interchange is legal, and so is [tiling](/loop-tiling/). The time function $\pi(i, j) = i + j$ has $\pi \cdot \vec{d} = 1 > 0$ for both distances, so all points on one line $i + j = c$ can run at the same time ([wavefront parallelism](/wavefront-parallelism/), the [hyperplane method](/lamport-hyperplane-method/)).

### A distance that changes

```
for i = 1 to 8:
  S1: A[2*i] = B[i]
  S2: C[i] = A[i]
```

$S1(i)$ writes $A[2i]$, and $S2(i')$ reads it when $i' = 2i \le 8$. The flow dependence has the distances $i' - i = i$ for $i = 1, 2, 3, 4$, so $\Delta(S1, S2) = \{1, 2, 3, 4\}$. There is no anti dependence, since $S2(i')$ would have to read $A[2i]$ before $S1(i)$ writes it, which needs $2i < i$. The dependence is not uniform. Its direction vector is $(<)$.

### A subscript that does not use a loop index

```
for i = 1 to n:
  for j = 1 to m:
    S: A[i] = A[i-1] + B[i][j]
```

The read $A[i-1]$ of $S(i', j')$ meets the write $A[i]$ of $S(i, j)$ when $i' = i + 1$, for any $j$ and $j'$. The flow distances are $(1, \delta)$ for all $\delta$ with $1 - m \le \delta \le m - 1$. Each is lexicographically positive, also those with a negative second entry. The output dependence of $S$ on itself has the distances $(0, \delta)$ for $1 \le \delta \le m - 1$: all writes of one row go to $A[i]$. No single vector describes either set; the direction vectors are $(<, *)$ and $(=, <)$.

### Legality with distances

For a [unimodular transformation](/unimodular-transformations/) $T$ of a perfect nest, the new distance of each dependence is $T\vec{d}$, and $T$ is legal if $T\vec{d} \succ \vec{0}$ for each nonzero distance. Take $\vec{d} = (1, -1)$ from `A[i][j] = A[i-1][j+1]`:

| transformation | matrix | $T\vec{d}$ | legal |
|---|---|---|---|
| [interchange](/loop-interchange/) | $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ | $(-1, 1)$ | no |
| [skewing](/loop-skewing/) of $j$ by $i$ | $\begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$ | $(1, 0)$ | yes |
| skewing, then interchange | $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$ | $(0, 1)$ | yes |

### Non-examples

- $\vec{d} = (0, -1)$ is never the distance of a dependence: its first nonzero entry is negative. If a test finds a solution with $\vec{j} - \vec{i} = (0, -1)$, it has found a dependence from $T$ to $S$ with distance $(0, 1)$.
- Two references to different arrays that cannot overlap have no dependence, so no distance set; an empty distance set is not the same as the distance $\vec{0}$.

## Related definitions

- **Direction vector.** The vector of signs of $\vec{d}$, written with $<$, $=$ and $>$; it summarizes a distance set that has more than one element. See [dependence direction vector](/dependence-direction-vector/).
- **Level of a dependence.** The index of the first nonzero entry of $\vec{d}$. See [loop-carried dependence](/loop-carried-dependence/).
- **Reuse vector.** The same subtraction on two accesses that both read a location gives a reuse vector, used for locality ([Wolf-Lam locality algorithm](/wolf-lam-locality-algorithm/)); it is not a dependence.
- **Dependence cone and polyhedron.** In the [polyhedral model](/polyhedral-model/), the exact set of pairs is kept as a polyhedron, and the distances are a projection of it.

## References
