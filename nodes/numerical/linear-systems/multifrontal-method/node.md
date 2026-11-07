---
tag: QT9W33
kind: algorithm
slug: multifrontal-method
name: Multifrontal method
aliases:
- multifrontal factorization
- multifrontal Cholesky
area: numerical/linear-systems
level: research
summary: Sparse direct factorization that organizes work into dense frontal matrices along the elimination tree.
solves: [sparse-linear-systems]
model: floating-point-model
complexity:
  vars: {n: "the order of A", m: "the number of off-diagonal nonzero pairs of A", z: "the number of nonzeros of L below the diagonal", f: "the sum over columns of the squared column counts of L", p: "the peak stack storage in words"}
  time: {worst: O(n + m + f), best: O(n + m + f)}
  space: {extra: O(z + p)}
  flops: {worst: "f + 2 z + n"}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [elimination-tree, cholesky-decomposition, schur-complement, postorder-traversal]
see_also: [nested-dissection, minimum-degree-ordering, fill-in, fill-reducing-ordering, sparse-matrix, blocked-matrix-multiplication, lu-decomposition, stack]
sources:
  - paper: doi:10.1145/356044.356047
    title: I. S. Duff and J. K. Reid, The multifrontal solution of indefinite sparse symmetric linear equations, ACM Transactions on Mathematical Software 9(3), 1983
    locator: frontal matrices, update matrices on a stack, and the assembly tree
  - paper: doi:10.1137/1034004
    title: Joseph W. H. Liu, The multifrontal method for sparse matrix solution, theory and practice, SIAM Review 34(1), 1992
    locator: extend-add, the correctness of the method along the elimination tree, and the stack storage recurrence and child ordering
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: Chapter 4, Cholesky factorization (elimination tree, postorder, column counts, supernodal and multifrontal methods)
  - paper: doi:10.1017/S0962492916000076
    title: Timothy A. Davis, Sivasankaran Rajamanickam and Wissam M. Sid-Lakhdar, A survey of direct methods for sparse linear systems, Acta Numerica 25, 2016
    locator: the section on multifrontal methods
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 10, Cholesky Factorization (the componentwise backward error bound)
---

The multifrontal method factors a sparse symmetric positive definite matrix $A = L L^T$ as a sequence of small dense partial factorizations, one per node of the [elimination tree](/elimination-tree/). Node $j$ gathers its column of $A$ and the *update matrices* left by its children into a dense *frontal matrix*. It eliminates the pivot $j$, which is one step of dense Cholesky. It then passes the remaining [Schur complement](/schur-complement/), its own update matrix, to its parent. A postorder of the tree makes the pending update matrices behave like a stack. Grouping columns with the same structure into supernodes turns the work into dense matrix-matrix operations, so the sparse factorization runs at the speed of dense linear algebra. This is why multifrontal codes such as MUMPS, UMFPACK, the multifrontal option of CHOLMOD and MA57 are among the fastest sparse direct solvers. The arithmetic is that of [Cholesky](/cholesky-decomposition/), so the backward error bound is the usual one.

## In plain words

A large sparse factorization can be split into many small dense ones arranged in a tree. Each node of the tree collects the numbers its own column needs, eliminates one unknown, and hands what is left to its parent as a small dense block. The parent adds up the blocks from all its children, which is a matter of placing entries at matching positions, and continues. Working bottom up, every block is consumed right after it is made, so the blocks waiting for use form a stack. Dense blocks are what computers process fastest.

## The problem

**Notation.**
- $A \in \mathbb{R}^{n \times n}$ is symmetric positive definite, already ordered by a fill-reducing permutation. It has $m$ off-diagonal nonzero pairs, and $A = L L^T$.
- $\mathcal{S}_j = \{i > j : l_{ij} \ne 0\}$ is the structure of column $j$ of $L$, $c_j = |\mathcal{S}_j|$ is its column count, and $I_j = \{j\} \cup \mathcal{S}_j$.
- $z = \sum_j c_j$ is the number of nonzeros of $L$ below the diagonal, and $f = \sum_j c_j^2$.
- The elimination tree has $\mathrm{parent}(j) = \min \mathcal{S}_j$.
- The frontal matrix $F_j$ is dense of order $c_j + 1$. The update matrix $U_j$ is dense of order $c_j$.
- *Extend-add* $F \oplus U$ adds the entries of $U$ to the entries of $F$ with the same global indices.

For floating point: $u = 2^{-53}$, $\gamma_k = k u/(1 - k u)$, $\hat L$ is the computed factor, $\hat x$ the computed solution, and $\kappa_2(A) = \|A\|_2\|A^{-1}\|_2$.

**Input.** $A$, after ordering by [minimum degree](/minimum-degree-ordering/) or [nested dissection](/nested-dissection/).

**Output.** $L$, or $L$ and $D$ for $A = L D L^T$. Then $A x = b$ is solved by two triangular solves.

## The algorithm

```pseudo id=main
MULTIFRONTAL-CHOLESKY(A)
L1  compute the elimination tree and the structures I_j = {j} ∪ S_j            ▷ symbolic phase
L2  stack ← empty
L3  for j in a postorder of the elimination tree do
L4      F ← a zero dense symmetric matrix indexed by I_j
L5      F[I_j, j] ← A[I_j, j]                                                    ▷ assemble column j of A
L6      for each child c of j do
L7          U_c ← pop(stack);  F ← F ⊕ U_c                                       ▷ extend-add
L8      l_jj ← sqrt(F[j, j]);  L[S_j, j] ← F[S_j, j] / l_jj                     ▷ eliminate the pivot
L9      U_j ← F[S_j, S_j] − L[S_j, j] L[S_j, j]^T                               ▷ the Schur complement
L10     if S_j ≠ ∅ then push(stack, U_j)
L11 return L
```

The symbolic phase computes three things:
- the elimination tree, by Liu's algorithm with path compression;
- the structures, by the recurrence $\mathcal{S}_j = (\{i > j : a_{ij} \ne 0\} \cup \bigcup_{c} \mathcal{S}_c) \setminus \{j\}$ over the children $c$;
- a postorder, in which each node's children are visited in the order that minimizes the stack peak (Liu): by decreasing (subtree peak minus update size).

The **supernodal** form merges a chain of columns $j, j+1, \ldots, j+s-1$ in which each column is the only child of the next and the structures nest, $\mathcal{S}_{j} = \{j+1\} \cup \mathcal{S}_{j+1}$. Such a supernode has one front of order $s + c_{j+s-1}$. It eliminates $s$ pivots at once by a dense partial Cholesky, and its update is a dense rank-$s$ product. For LU of unsymmetric matrices the fronts are square, and pivoting is done inside the front. Pivots that fail a threshold test are *delayed* to the parent front.

## Example

Let
$$A = \begin{pmatrix} 4 & 0 & 2 & 0 \\ 0 & 9 & 3 & 3 \\ 2 & 3 & 6 & -1 \\ 0 & 3 & -1 & 6 \end{pmatrix}.$$
The structures are $\mathcal{S}_0 = \{2\}$, $\mathcal{S}_1 = \{2, 3\}$ and $\mathcal{S}_2 = \{3\}$, so the tree has parent $(2, 2, 3, -)$: columns 0 and 1 are leaves under 2, and 3 is the root.

- **Node 0.** The front on $\{0, 2\}$ is $\begin{pmatrix} 4 & \\ 2 & 0 \end{pmatrix}$. It gives $l_{00} = 2$, $l_{20} = 1$, and $U_0 = (-1)$ on $\{2\}$. Push.
- **Node 1.** The front on $\{1, 2, 3\}$ has first column $(9, 3, 3)$. It gives $l_{11} = 3$ and $l_{21} = l_{31} = 1$, and $U_1 = -\begin{pmatrix} 1 & 1 \\ 1 & 1\end{pmatrix}$ on $\{2, 3\}$. Push.
- **Node 2.** The front on $\{2, 3\}$ starts as $\begin{pmatrix} 6 & \\ -1 & 0 \end{pmatrix}$. Popping $U_1$ and $U_0$ and extend-adding them gives $\begin{pmatrix} 4 & \\ -2 & -1 \end{pmatrix}$. So $l_{22} = 2$ and $l_{32} = -1$, and $U_2 = -1 - (-1)^2 = -2$ on $\{3\}$.
- **Node 3.** The front is $6 + (-2) = 4$, so $l_{33} = 2$.

The result is
$$L = \begin{pmatrix} 2 & & & \\ 0 & 3 & & \\ 1 & 1 & 2 & \\ 0 & 1 & -1 & 2 \end{pmatrix}.$$
The extend-add at node 2 added $U_0$'s single entry to position $(2, 2)$ and $U_1$'s three entries to positions $(2,2)$, $(3,2)$ and $(3,3)$.

**Grids.** The $k \times k$ five-point Laplacian, factored by the implementation, column by column without supernodes. The table gives the largest front order, the height of the elimination tree, the factor flops $f + 2z + n$, and the stack peak in words (lower triangles) with Liu's child order. It also gives the extend-add additions:

| $k$ | ordering | max front | tree height | flops | stack peak | extend-add additions |
|---|---|---|---|---|---|---|
| 16 | natural (band) | 17 | 256 | 68301 | 289 | 32095 |
| 16 | AMD | 23 | 49 | 24245 | 582 | 11048 |
| 16 | nested dissection | 24 | 41 | 31539 | 708 | 14517 |
| 32 | natural (band) | 33 | 1024 | 1070493 | 1089 | 518847 |
| 32 | AMD | 52 | 115 | 263797 | 3291 | 125725 |
| 32 | nested dissection | 48 | 83 | 283872 | 2862 | 135156 |

With the band order the tree is a chain, so only one update matrix waits at a time, but the work is four times larger. Fill-reducing orders give bushy, short trees with independent subtrees, at the cost of more stack. For AMD on $k = 32$, Liu's child order lowers the peak from 3520 to 3291 words. The extend-add additions are about half the factor flops in this column form. Supernodes remove most of them, because within a supernode the updates are applied in place.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).

- **Structure inheritance.** If column $j$ has nonzeros in rows $p < i$, then $l_{ip} \ne 0$. Hence $\mathcal{S}_j \setminus \{\mathrm{parent}(j)\} \subseteq \mathcal{S}_{\mathrm{parent}(j)}$, which justifies the symbolic recurrence. It also gives that $l_{jk} \ne 0$ implies that $k$ is a descendant of $j$.
- **Stack.** In a postorder, processing a subtree adds exactly its root's update matrix to the stack. So at node $j$ the top of the stack holds exactly the children's updates.
- **Numbers.** By induction, $U_j = -\sum_{k \in T[j]} L(\mathcal{S}_j, k) L(\mathcal{S}_j, k)^T$, where $T[j]$ is the subtree of $j$. The first column of the assembled front is then $a_{ij} - \sum_{k < j} l_{ik} l_{jk}$, and line L8 is the Cholesky formula. In exact rational arithmetic the $LDL^T$ form agrees with a dense $LDL^T$ entry for entry, which the tests check.
- **Storage.** Liu's recurrence gives the stack peak. Ordering children by decreasing (peak minus update size) is optimal, by an exchange argument; the tests confirm this against brute force.

**Numerical stability.** For symmetric positive definite $A$, each computed $\hat l_{ij}$ is $a_{ij}$ minus the products $\hat l_{ik}\hat l_{jk}$, summed in an order set by the tree, then divided by $\hat l_{jj}$. The rounding analysis of Cholesky does not depend on the summation order. So if the factorization runs to completion, $\hat L\hat L^T = A + \Delta A$ with $|\Delta A| \le \gamma_{n+1}|\hat L||\hat L^T|$ (Higham, Chapter 10). This is proved, and the tests check it elementwise with exact residuals. It gives $\|\Delta A\|_2 \le n\gamma_{n+1}\|A\|_2$ and a forward error of order $\kappa_2(A)u$ for the solution, in the worst case. The constant can be sharpened to $\gamma_{c_j + 2}$ per column, since each inner product has at most $c_j + 1$ terms. For symmetric indefinite and unsymmetric matrices, stability needs pivoting inside the fronts: Bunch-Kaufman $1 \times 1$ and $2 \times 2$ pivots for $LDL^T$, or threshold partial pivoting with parameter $\tau$ for LU. Pivots that fail the test are delayed to an ancestor front. This increases fill and work, but keeps the growth bounded as in dense pivoting, which is a worst-case statement.

## Complexity

- **Flops.** The column form does $f + 2z + n$ flops: per column, one square root, $c_j$ divisions and $c_j(c_j + 1)$ for the update. This is the same leading term $\sum_j c_j^2$ as any sparse Cholesky. Extend-add adds $\sum_{j \text{ non-root}} c_j(c_j + 1)/2$ additions, less with supernodes.
- **Symbolic phase.** The elimination tree costs $O(m \log n)$ with path compression alone, close to $O(m)$ in practice, and the structures $O(z)$. The column counts alone can be found in nearly $O(m)$ time.
- **Space.** $L$ needs $z + n$ words, and the stack and current front need at most $p$, given by Liu's recurrence. On 2D grids in nested dissection order, $p = O(n)$. On 3D grids the top separator front alone has order $\Theta(n^{2/3})$, so $p = \Theta(n^{4/3})$.
- **Memory traffic.** A supernode with $s$ pivots and front order $t$ does about $s t^2$ flops on $t^2$ words. For large fronts the work is then dominated by Level 3 BLAS, matrix-matrix products and triangular solves with many right-hand sides, and runs near peak speed. A column-at-a-time sparse Cholesky does $O(1)$ flops per word moved and is memory-bound. The extend-adds are indirect scatter operations and are memory-bound. Their share of the time is large for small fronts, which is why codes amalgamate small supernodes even at the price of a few explicit zeros.
- **Parallelism.** Independent subtrees can be factored concurrently, which is tree parallelism. Large fronts near the root are factored with parallel dense kernels, which is node parallelism.

## Properties

- **Exact arithmetic of Cholesky**, reorganized. It produces the same $L$ up to rounding, and the same backward error bound.
- **Dense kernels.** All numerical work is on dense fronts. Indirect addressing appears only in extend-add.
- **Stack storage.** The update matrices are used in last-in, first-out order, which suits out-of-core and memory-limited implementations.
- **Tree parallel.** The elimination tree exposes independent tasks. Nested dissection gives short, balanced trees.
- **Extra memory.** It needs extra memory for the stack beyond $L$ itself, unlike left-looking supernodal methods.

## Variants and improvements

- **Supernodal multifrontal.** Merge columns with nested structure. Relaxed amalgamation also merges nearly identical columns, trading a few stored zeros for larger dense blocks.
- **Multifrontal LU** (Duff and Reid; UMFPACK by Davis and Duff). Square fronts with threshold partial pivoting, and an assembly tree that is a DAG for unsymmetric patterns.
- **Symmetric indefinite** (Duff and Reid 1983, MA27 and MA57). $LDL^T$ with $1 \times 1$ and $2 \times 2$ pivots, and delayed pivots passed up the tree.
- **Left-looking and right-looking supernodal Cholesky.** These are alternatives that use the same supernodes but accumulate updates differently. Left-looking needs no stack.
- **Parallel and distributed** (MUMPS, WSMP, PaStiX). Tree and node parallelism, with dynamic scheduling.
- **Low-rank compressed fronts** (block low-rank, HSS). They compress the large separator fronts of PDE matrices and reduce the 3D cost below $O(n^2)$, at a controlled loss of accuracy.
- **Frontal method** (Irons, 1970). A single front sweeps across a finite element mesh; it is the origin of the name.

## When to use it

Use a multifrontal or supernodal solver for large sparse systems that must be solved directly: many right-hand sides, ill-conditioned or indefinite systems where iterative methods struggle, or as an exact inner solver. Use it for 2D problems and moderately sized 3D problems, and on parallel machines. Combine it with nested dissection or AMD orderings. For very large 3D problems where $O(n^2)$ flops or $O(n^{4/3})$ memory is too much, use preconditioned iterative methods or low-rank compressed variants.

## Pitfalls

- **No fill-reducing ordering.** The multifrontal method does not choose the ordering. With a poor one, the fronts become huge.
- **Small fronts.** Without amalgamation, most of the time goes to extend-add and bookkeeping rather than flops.
- **Stack memory.** The stack can exceed the memory of $L$'s largest columns many times over. Use Liu's child ordering and estimate the peak in the symbolic phase.
- **Indefinite matrices without pivoting.** $LDL^T$ without pivoting can break down or become unstable. Use delayed pivots or static pivoting with iterative refinement.
- **Deep trees and recursion.** Band orderings give chains of length $n$. Traverse the tree iteratively.

## Implementations

## History

Irons (1970) introduced the frontal method for finite element equations, assembling and eliminating along a single moving front. Duff and Reid (1983) generalized it to the multifrontal method for symmetric indefinite sparse systems, with many fronts organized by the assembly tree and a stack of update matrices (MA27). Liu developed the theory of elimination trees and the stack storage recurrence in the 1980s, and surveyed the method in 1992. Ashcraft and others introduced supernodal and amalgamated variants. The method underlies MUMPS (Amestoy, Duff, L'Excellent and Koster, 2001), UMFPACK and the multifrontal parts of CHOLMOD and MA57.

## References
