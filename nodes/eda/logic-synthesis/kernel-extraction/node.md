---
tag: 6VFGF9
kind: algorithm
slug: kernel-extraction
name: Kernel extraction
aliases:
- common divisor extraction
- rectangle covering extraction
area: eda/logic-synthesis
level: core
summary: Finds kernels shared by several nodes of a Boolean network as rectangles of a kernel-cube matrix, and makes each one a new node when this saves literals.
solves: [multi-level-logic-synthesis]
model: word-ram
complexity:
  vars: {P: the number of cokernel and kernel pairs of all nodes, K: the largest number of cubes of a kernel, n: the number of variables, E: the number of extraction steps}
  time: {worst: O(E P^4 K n)}
  space: {extra: O(P K n)}
properties: {deterministic: true, exact: false, online: false, recursive: true}
history:
  year: 1982
  people: [Robert K. Brayton, Curtis T. McMullen]
  note: Brayton and McMullen defined kernels and showed that common multi-cube divisors are found among them. MIS made kernel extraction a main command, and Rudell cast it as the covering of a kernel-cube matrix by rectangles.
prereqs: [algebraic-kernel, algebraic-division, boolean-network]
see_also: [multi-level-logic-synthesis, common-subexpression-elimination, set-cover, greedy-algorithm, local-search, sum-of-products, aig-rewriting, hypergraph]
sources:
  - paper: "Robert K. Brayton and Curtis T. McMullen, The decomposition and factorization of Boolean expressions, Proceedings of the International Symposium on Circuits and Systems (ISCAS), 1982, pages 49 to 54"
    locator: kernels, cokernels, the recursive computation of all kernels, and the theorem that common multi-cube divisors come from intersections of kernels
  - paper: doi:10.1109/TCAD.1987.1270347
    title: Robert K. Brayton, Richard Rudell, Alberto Sangiovanni-Vincentelli and Albert R. Wang, MIS, a multiple-level logic optimization system, IEEE Transactions on Computer-Aided Design 6(6), 1987, pages 1062 to 1081
    locator: the extraction of common kernels across the nodes of a network as a command of MIS
  - paper: doi:10.1109/5.52213
    title: Robert K. Brayton, Gary D. Hachtel and Alberto L. Sangiovanni-Vincentelli, Multilevel logic synthesis, Proceedings of the IEEE 78(2), 1990, pages 264 to 300
    locator: the kernel-cube matrix, rectangles and their value in literals, and the extraction of common divisors
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 8, Multiple-Level Combinational Logic Optimization, the sections on kernels and on the extraction of common subexpressions
---

Kernel extraction is a step of [multi-level logic synthesis](/multi-level-logic-synthesis/) that finds a sum of cubes used by several nodes of a [Boolean network](/boolean-network/), makes it a new node, and rewrites the other nodes to use it. It looks for these divisors among the [algebraic kernels](/algebraic-kernel/) of the nodes, because two expressions share a divisor with two or more cubes only if they share two cubes of some kernels. The kernels of all nodes go into a *kernel-cube matrix*, and a shared divisor that saves literals is a *rectangle* of this matrix. The method is a greedy heuristic: each step keeps every function and saves literals, but the result is not proved to be the smallest network.

## In plain words

Several formulas of a circuit may hold the same piece, such as $c + d$, multiplied by different terms. If you compute that piece once as its own signal and let each formula use the signal, you need fewer gate inputs.

To find such pieces, first list for each formula the ways to write part of it as a term times a sum: these sums are its kernels. Then write a table with one row for each term and formula, and one column for each product that occurs in some kernel. A block of rows and columns that is filled in everywhere means that the same sum appears in all these rows. Pull it out if it saves inputs, and repeat until no block saves anything.

## The problem

A Boolean network maps each node $v$ to a [sum of products](/sum-of-products/) $F_v$ over the primary inputs and the other nodes, with no cycle. Its cost is the number of literals, $\sum_v \ell(F_v)$. Given a network, find new nodes $x_1, x_2, \ldots$, each a sum of cubes, and algebraic rewrites of the nodes that use them, so that every node keeps its function and the number of literals is small. Kernel extraction uses only algebraic rewrites: $F_v$ is changed only by replacing a set of its cubes $\{c \cup k : k \in X\}$ by the one cube $c \cup \{x\}$, where $X$ is the sum of cubes of a new node $x$ and $c$ shares no variable with $X$.

**Kernel-cube matrix.** The rows are the pairs $(v, c)$ where $c$ is a cokernel of $F_v$, and the row holds the kernel $K_{v,c} = F_v / c$. The columns are the distinct cubes that occur in any kernel. The entry at row $(v, c)$ and column $k$ is 1 if $k \in K_{v,c}$, which means that $c \cup k$ is a cube of $F_v$.

**Rectangle and value.** A rectangle is a set $R$ of rows and a set $C$ of at least two columns with all entries 1. Its value is the number of literals it saves:
$$\mathrm{value}(R, C) = \sum_{(v, q) \in U} |q| - \sum_{(v, c) \in R} (|c| + 1) - \sum_{k \in C} |k|,$$
where $U = \{(v, c \cup k) : (v, c) \in R, k \in C\}$ is the set of covered cubes of the nodes, each counted once. The first sum is the literals removed, the second the new cubes $c \cup \{x\}$, and the third the new node $x = \sum_{k \in C} k$.

## The algorithm

```pseudo id=main
KERNELS(g, cok, j)          ▷ g = F / cok is cube-free; literals l_0 < l_1 < ... of F
L1  for i ← j to the last literal:
L2      if fewer than two cubes of g contain l_i then continue
L3      C ← the intersection of the cubes of g that contain l_i   ▷ the largest such common cube
L4      if C holds some l_k with k < i then continue              ▷ this kernel is found elsewhere
L5      KERNELS(g / C, cok ∪ C, i + 1)
L6  output (cok, g)

EXTRACT(N)
L7  loop: rows ← the outputs of KERNELS(F_v / c_v, c_v, 0) for every node v, c_v the common cube of F_v
L8      (R, C) ← for each seed row, add the row that raises the value most, keeping |C| ≥ 2; take the best
L9      if value(R, C) ≤ 0 then return N
L10     add a node x with F_x = the sum of the cubes of C
L11     for each row (v, c) of R:
L12         F_v ← (F_v minus {c ∪ k : k ∈ C}) plus the cube c ∪ {x}
```

KERNELS is the recursion of Brayton and McMullen. Line L3 extends the cokernel by the literal $l_i$ and by every literal that comes with it, so the new quotient is cube-free. Line L4 skips the call when the extended cokernel holds an earlier literal, since that kernel is reached from the earlier literal. Each call outputs its own kernel at line L6, including the node itself, with cokernel 1, when it is cube-free.

EXTRACT computes all rows at line L7 and grows rectangles from each row at line L8: the columns start as the whole kernel of the seed row, and each added row cuts them down to the common cubes. Lines L10 to L12 make the new node and rewrite the rows. The loop runs until the best rectangle found saves nothing.

## Example

Take the network $y = ac + ad + bc + bd + e$ and $z = cf + df + g$, with 9 and 5 literals. KERNELS gives these rows.

| row | cokernel | kernel | columns |
|---|---|---|---|
| 1 | $y$, $a$ | $c + d$ | $c$, $d$ |
| 2 | $y$, $b$ | $c + d$ | $c$, $d$ |
| 3 | $y$, $c$ | $a + b$ | $a$, $b$ |
| 4 | $y$, $d$ | $a + b$ | $a$, $b$ |
| 5 | $y$, $1$ | $ac + ad + bc + bd + e$ | $ac$, $ad$, $bc$, $bd$, $e$ |
| 6 | $z$, $f$ | $c + d$ | $c$, $d$ |
| 7 | $z$, $1$ | $cf + df + g$ | $cf$, $df$, $g$ |

The matrix has 7 rows and 12 columns. The rectangle with rows 1, 2 and 6 and columns $c$ and $d$ covers the 6 cubes $ac, ad, bc, bd, cf, df$ with 12 literals. It adds the cubes $ax$, $bx$ and $fx$ with 6 literals and the node $x = c + d$ with 2, so its value is $12 - 6 - 2 = 4$. This is the best rectangle, and the new network is

$$x = c + d, \qquad y = ax + bx + e, \qquad z = fx + g,$$

with 10 literals in place of 14. In the next round, $y$ has the kernel $a + b$ with cokernel $x$, but extracting it adds as many literals as it removes, so EXTRACT stops. In the first round, the rectangle with rows 3 and 4 and columns $a$ and $b$ has value $8 - 4 - 2 = 2$, and a rectangle with one row and the two columns of one kernel, such as row 1 with $c$ and $d$, has value $4 - 2 - 2 = 0$.

## Correctness

The [full proof](proofs/correctness.md) has two parts. First, KERNELS outputs every pair (cokernel, kernel) of $F$ exactly once. A cube $c$ is a cokernel exactly when the cubes of $F$ that contain $c$ number at least two and have no other common literal, and the recursion builds each such cube from a unique parent by the test of line L4, as in the enumeration of closed sets. Second, each step of EXTRACT keeps the function of every node and lowers the number of literals by exactly the value of the rectangle. The cubes removed at line L12 are exactly the products $c \cup k$, and substituting $x = \sum_{k \in C} k$ into $c \cup \{x\}$ gives them back. The new node uses only fanins of the rewritten nodes, so the network has no cycle. The number of literals falls by at least 1 at each step, so the loop ends.

## Complexity

The number of kernels can be exponential in the size of a node. A product of $k$ sums $(a_1 + b_1) \cdots (a_k + b_k)$, multiplied out, has $2^k$ cubes, $2^k - 1$ distinct kernels and $3^k - 2^k$ pairs of cokernel and kernel, which the test file checks for $k \le 4$. KERNELS does $O(L m n)$ work in each call for $L$ literals, $m$ cubes and $n$ variables, and makes one call for each pair. With $P$ rows and kernels of at most $K$ cubes, the greedy search of line L8 starts at $P$ seeds, adds at most $P$ rows to each, and tries $P$ rows at each step, each in $O(P K n)$ time to compute the value. So one step costs $O(P^4 K n)$ in the code of this page, and $E$ steps cost $O(E P^4 K n)$. Tools keep this small by using only kernels of low level or by limiting the matrix, and by updating the matrix after each step in place of building it again.

## Properties

**What is proved.** KERNELS finds every kernel of a node with every cokernel, and by the kernel theorem every multi-cube divisor shared by two nodes is a subset of the cubes of a kernel of each, so no algebraic multi-cube divisor is out of reach of the matrix. Each extraction keeps every function, makes no cycle, and lowers the literal count by exactly the value of the rectangle.

**What is not proved.** The greedy search of line L8 need not find the rectangle of largest value, and picking the best rectangle at each step need not give the smallest network. The number of rectangles grows exponentially with the number of rows, which is why tools use heuristics. Algebraic rewrites also miss Boolean divisors, such as $a + b$ in $a + bc = (a + b)(a + c)$.

**What is measured.** On 200 random networks of 4 nodes over 8 inputs, each node a sum of up to two products of a random cube and one of 3 shared random kernels plus one or two random cubes (seed 4), the code of this page lowered the mean literal count from 57.1 to 37.2 in a mean of 2.9 steps. On 2132 smaller networks of this kind (3 nodes over 6 inputs, seed 1, at most 16 rows), the greedy search found a rectangle of the largest value every time. These are toy cases with planted kernels, not benchmark results.

## Variants and improvements

- **Cube extraction.** A rectangle with one column is a common cube, such as $ab$ in $abc + abd$ of one node and $abe$ of another. It is found in a cube-literal matrix, where the rows are cubes and the columns literals, and tools run both kinds of extraction.
- **Double-cube and fast extraction.** The fast extraction command of SIS uses only divisors with two cubes and cubes with two literals, together with their complements, which are few and can be updated quickly, and gets most of the gain of full kernel extraction in much less time.
- **Level-0 kernels.** A kernel that has no kernel other than itself is of level 0. Restricting the matrix to low levels makes it much smaller.
- **Boolean extraction.** Divisors found by algebraic means can be checked with [don't-cares](/dont-care-condition/) for a Boolean division, which uses rules that algebraic division ignores.
- **Common subexpressions in compilers.** The same idea, with sums and products of numbers in place of cubes, is [common subexpression elimination](/common-subexpression-elimination/).

## When to use it

Use kernel extraction on networks given as sums of products, such as the output of [two-level minimization](/two-level-logic-minimization/) for many outputs, where large shared sums exist. It is the main area step of the classical MIS and SIS scripts. On an [and-inverter graph](/and-inverter-graph/), local rewriting such as [AIG rewriting](/aig-rewriting/) is the usual tool. Use exact methods only for tiny networks.

## Pitfalls

- **Counting a covered cube twice.** Two entries of one rectangle can name the same cube of a node. The value must count each covered cube once, or it overstates the saving.
- **Single-column rectangles.** A rectangle with one column is a cube, not a multi-cube divisor, and needs the cube-literal matrix.
- **Ignoring the cokernel 1 rows.** The node itself is a kernel when it is cube-free, and many shared divisors use its cubes. Leaving out these rows misses them.
- **Too many kernels.** Products of many sums have exponentially many kernels, so a tool must limit the level or the number of kernels for each node.
- **Stopping rules that allow value 0.** Extracting a rectangle of value 0 adds a node and saves nothing, and a loop that accepts it may not end.

## Implementations

## History

Brayton and McMullen (ISCAS 1982) introduced kernels and cokernels, gave the recursion that computes them, and proved that multi-cube common divisors arise from intersections of kernels. MIS (Brayton, Rudell, Sangiovanni-Vincentelli and Wang 1987) extracted common kernels across the nodes of a network. Rudell recast the search as rectangle covering of the kernel-cube matrix, and the survey of Brayton, Hachtel and Sangiovanni-Vincentelli (1990) set out the matrix and the value of a rectangle. SIS added the faster double-cube extraction. Later synthesis moved to AIG rewriting, but algebraic extraction stays in use for sums of products and in teaching.

## References
