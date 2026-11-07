---
tag: ZXGZZS
kind: algorithm
slug: block-lanczos-algorithm
name: Block Lanczos algorithm
aliases:
- block Lanczos
- Montgomery's block Lanczos algorithm
area: algebra/exact-linear-algebra
level: research
summary: Block Lanczos iteration for finding nullspace vectors of large sparse matrices over GF(2) and other finite fields.
solves: [nullspace-computation]
model: algebraic-computation-tree
complexity:
  vars: {n: the number of columns of B, w: the number of nonzero entries of B, s: the block width}
  time: {worst: O(n w s + n^2 s^2), average: O(n w + n^2 s)}
  space: {extra: O(n s)}
  field_operations: {worst: O(n w s + n^2 s^2), average: 2 n w + O(n^2 s)}
properties: {deterministic: false, in_place: false, recursive: false}
prereqs: [lanczos-algorithm, krylov-subspace, black-box-matrix]
see_also: [block-wiedemann-algorithm, wiedemann-algorithm, lanczos-algorithm, conjugate-gradient-method, structured-gaussian-elimination, bitset-gaussian-elimination, quadratic-sieve, general-number-field-sieve]
sources:
  - paper: doi:10.1007/3-540-49264-X_9
    title: Peter L. Montgomery, A block Lanczos algorithm for finding dependencies over GF(2), EUROCRYPT 1995, Lecture Notes in Computer Science 921
    locator: pp. 106 to 120 (the recurrence with the subspaces S_i, the selection of S_i, the final step on X - Y and V_m, and the estimate of n/(N - 0.76) iterations)
  - paper: "Don Coppersmith, Solving linear equations over GF(2): block Lanczos algorithm, Linear Algebra and its Applications 192, 1993"
    locator: pp. 33 to 60 (the first block Lanczos method over GF(2), with look-ahead)
  - paper: doi:10.6028/jres.045.026
    title: Cornelius Lanczos, An iteration method for the solution of the eigenvalue problem of linear differential and integral operators, Journal of Research of the National Bureau of Standards 45(4), 1950
    locator: pp. 255 to 282 (the three-term recurrence that the block method generalizes)
  - paper: "Brian A. LaMacchia and Andrew M. Odlyzko, Solving large sparse linear systems over finite fields, CRYPTO 1990, Lecture Notes in Computer Science 537"
    locator: pp. 109 to 133 (Lanczos and conjugate gradient over finite fields, and structured Gaussian elimination)
  - paper: doi:10.1109/TIT.1986.1057137
    title: Douglas H. Wiedemann, Solving sparse linear equations over finite fields, IEEE Transactions on Information Theory 32(1), 1986
    locator: pp. 54 to 62 (the competing Krylov method for sparse systems over finite fields)
---

The block Lanczos algorithm finds vectors in the kernel of a large sparse matrix over $\mathbb{F}_2$. It touches the matrix only through products with blocks of vectors. It is the [Lanczos iteration](/lanczos-algorithm/) for symmetric matrices, run on $s$ vectors at once. Over a small field a single vector is often orthogonal to itself, which stops the scalar method. Working with blocks gets around this: at each step the method keeps the largest part of the block that is not self-orthogonal. With $s = 64$, a block row is one machine word, so each product with the matrix advances $64$ vectors for the price of one. Peter Montgomery's 1995 version is the linear algebra step of most [quadratic sieve](/quadratic-sieve/) and [number field sieve](/general-number-field-sieve/) programs.

Notation: $B$ is an $m \times n$ matrix over the field $K = \mathbb{F}_2$, with $w$ nonzero entries, given as a [black box](/black-box-matrix/) for products with $B$ and $B^T$. $A = B^T B$ is the symmetric $n \times n$ matrix that the iteration works with. $s$ is the block width, and $Y$ is a random $n \times s$ matrix. All costs count operations in $\mathbb{F}_2$. Each one is a single bit operation, and with word packing $s$ of them are one machine word operation. $\omega$ is the exponent of matrix multiplication.

## In plain words

Factoring a large number ends with a huge table of zeros and ones, and the goal is to find groups of rows that add up to zero. Ordinary elimination would fill the table with ones and run out of memory. This method never changes the table. It only multiplies it by a few dozen vectors at a time, and it builds new vectors that are balanced against all the earlier ones. After about as many rounds as the table has columns divided by the number of vectors in a block, it has seen everything. A last small elimination then turns its results into solutions.

## The problem

Input: a sparse $m \times n$ matrix $B$ over $\mathbb{F}_2$ and a block width $s$. Output: independent nonzero vectors $x \in \mathbb{F}_2^n$ with $Bx = 0$, up to about $s$ of them. This is [nullspace computation](/nullspace-computation/) for a sparse matrix, and with $b$ appended as a column it solves a [linear system modulo 2](/linear-system-modulo-2/). Since $\ker B \subseteq \ker A$, the method looks in the kernel of $A = B^T B$ and then removes what is not in $\ker B$. Cost is measured in products with $B$ and $B^T$ and in operations on $n \times s$ blocks.

## The algorithm

Each iteration takes a block $V_i$ and computes $T_i = V_i^T A V_i$. Then it chooses a set $S_i$ of columns such that $W_i = V_i S_i$ satisfies two conditions: $W_i^T A W_i = S_i^T T_i S_i$ is invertible, and every column left out at step $i - 1$ is taken now. Here $S_i$ also stands for the $s \times |S_i|$ matrix of the chosen unit columns. The next block is made $A$-orthogonal to the last three. Montgomery shows that this makes it $A$-orthogonal to all the earlier ones.

```pseudo id=main
BLOCK-LANCZOS(B, s)                       ▷ B is m × n over F_2, A = B^T B
L1  choose random Y ∈ F_2^{n×s}; V_0 ← A Y; X ← 0; S_{−1} ← all columns
L2  for i ← 0, 1, 2, … do
L3      compute A V_i, T_i ← V_i^T A V_i and V_i^T A^2 V_i
L4      if T_i = 0 then m ← i; stop the loop
L5      choose S_i ⊇ (complement of S_{i−1}) with S_i^T T_i S_i invertible; W_i^inv ← S_i (S_i^T T_i S_i)^{−1} S_i^T; on failure m ← i, stop the loop
L6      X ← X + V_i W_i^inv V_i^T V_0
L7      compute D_{i+1}, E_{i+1}, F_{i+1} from T_i, V_i^T A^2 V_i, W_i^inv, W_{i−1}^inv, W_{i−2}^inv
L8      V_{i+1} ← A V_i S_i S_i^T + V_i D_{i+1} + V_{i−1} E_{i+1} + V_{i−2} F_{i+1}
L9  Z ← [X + Y | V_m]                          ▷ an n × 2s matrix
L10 eliminate on the columns of B Z, keeping every combination u with B Z u = 0
L11 return a basis of the vectors Z u
```

Over $\mathbb{F}_2$ the signs vanish, and the coefficients of line L7 are

$$
\begin{aligned}
D_{i+1} &= I + W_i^{\mathrm{inv}} \big( V_i^T A^2 V_i\, S_i S_i^T + T_i \big), \\
E_{i+1} &= W_{i-1}^{\mathrm{inv}}\, T_i\, S_i S_i^T, \\
F_{i+1} &= W_{i-2}^{\mathrm{inv}} \big( I + T_{i-1} W_{i-1}^{\mathrm{inv}} \big) \big( V_{i-1}^T A^2 V_{i-1}\, S_{i-1} S_{i-1}^T + T_{i-1} \big) S_i S_i^T.
\end{aligned}
$$

Here $W_j^{\mathrm{inv}} = 0$ for $j < 0$. Each iteration needs one product with $B$ and one with $B^T$ on an $n \times s$ block. The inner products are $s \times s$ matrices. The vectors $V_{i-1}$ and $V_{i-2}$ are the only history kept.

Line L5 is Gauss-Jordan elimination on $[T_i \mid I]$. It takes the columns not chosen at step $i - 1$ first, and it drops a column when no pivot is found for it. The line also checks that every column left out at step $i - 1$ is now chosen. If the check fails, the iteration has broken down. The implementation then stops and goes to line L9 with the current block, because the final step is checked anyway.

Lines L9 to L11 are a small dense elimination on $2s$ columns. $X$ is the $A$-orthogonal projection of $Y$ onto the [Krylov space](/krylov-subspace/) of $V_0$. If the iteration ended with $V_m = 0$, then $AX = AY$, so $X + Y \in \ker A$. Over $\mathbb{F}_2$ it more often ends with a nonzero self-orthogonal $V_m$. Combining the columns of $X + Y$ with those of $V_m$ then gives the kernel vectors.

## Example

Take the $5 \times 6$ matrix $B$ whose rows have their ones in columns $\{0, 1\}$, $\{1, 2\}$, $\{0, 2\}$, $\{3, 4\}$ and $\{4, 5\}$. Its kernel has dimension $2$, with basis $(1,1,1,0,0,0)$ and $(0,0,0,1,1,1)$. With $s = 2$ the implementation, seeded with $0$, draws $Y$ with rows

$$
(1,1),\ (1,0),\ (1,1),\ (1,1),\ (1,0),\ (0,0).
$$

Then $V_0 = AY$ has rows $(0,1), (0,0), (0,1), (0,1), (1,1), (1,0)$, and $T_0 = V_0^T A V_0 = I$. So $S_0$ takes both columns and $W_0^{\mathrm{inv}} = I$.

Line L6 gives $X = V_0 (V_0^T V_0)$. Since $V_0^T V_0 = \left(\begin{smallmatrix} 0 & 1 \\ 1 & 0 \end{smallmatrix}\right)$, $X$ is $V_0$ with its columns swapped. Next, $V_0^T A^2 V_0 = \left(\begin{smallmatrix} 0 & 1 \\ 1 & 0 \end{smallmatrix}\right)$, so $D_1$ is also the swap, and $E_1 = F_1 = 0$. Then

$$
V_1 = A V_0 + V_0 D_1 \text{ has rows } (1,1),\ (0,0),\ (1,1),\ (0,0),\ (0,0),\ (0,0).
$$

Here $AV_1 = V_1$ and each column of $V_1$ has two ones, so $T_1 = 0$, and the loop stops with $m = 1$ after one iteration.

The matrix $Z = [X + Y \mid V_1]$ has columns

$$
z_0 = (0,1,0,0,0,0),\quad z_1 = (1,0,1,1,1,1),\quad z_2 = z_3 = (1,0,1,0,0,0).
$$

All four have the same image $(1,1,0,0,0)$ under $B$. So $z_0$ is a pivot, and $z_0 + z_1 = (1,1,1,1,1,1)$ and $z_0 + z_2 = (1,1,1,0,0,0)$ are kernel vectors. The last column gives the second one again, which the final echelon step drops. The output is a basis of $\ker B$, even though $X + Y$ alone is not in $\ker A$: $A(X+Y) = AV_1 \ne 0$. The tests check this run.

## Correctness

The final step is checked, so the method never returns a wrong vector. Lines L10 and L11 keep pairs $(Bh, h)$ with $h$ a combination of columns of $Z$, and a pair whose image reduces to zero gives $Bh = 0$. The same echelon argument shows that the output is a basis of $\operatorname{col}(Z) \cap \ker B$. So the vectors are nonzero, independent and in the kernel, and when $\ker B = 0$ nothing is returned. This holds for every random $Y$, even after a breakdown.

What the randomness controls is how big $\operatorname{col}(Z) \cap \ker B$ is. Montgomery proves that with no breakdown the spaces $W_i$ are pairwise $A$-orthogonal, so $X$ is the $A$-orthogonal projection of $Y$. His heuristic analysis explains why the combinations of $X + Y$ and $V_m$ usually contain most of $\ker B$. The [full proof](proofs/correctness.md) gives the output, termination and selection arguments, and cites the orthogonality theorem. The tests check the orthogonality on the iterates.

## Complexity

**Products.** Each iteration does one product with $B$ and one with $B^T$ on an $n \times s$ block, $2ws$ field operations. With word packing, that is $2w$ word XORs.

**Inner products.** $T_i$, $V_i^T A^2 V_i$ and $V_i^T V_0$ cost $O(n s^2)$ field operations each, as do the block updates of lines L6 and L8. The implementation does them in $O(ns)$ word operations on $s$-bit words.

**Iterations.** If no breakdown occurs, the sizes $|S_i|$ add up to at most $n$, so there are at most $n$ iterations. That gives the proved worst case $O(nws + n^2 s^2)$, and the implementation caps the loop at $n + 10$ iterations. Montgomery estimates that $|S_i|$ averages about $s - 0.76$ for random data. That gives about $n / (s - 0.76)$ iterations, for a total of about $2nw + O(n^2 s)$ field operations, or $2nw/s + O(n^2)$ word operations with word packing. The estimate is heuristic, not proved.

On random $290 \times 300$ matrices with $5$ ones per row, the implementation used these numbers of iterations in $10$ runs:

| block width $s$ | iterations | estimate $n / (s - 0.76)$ |
|---|---|---|
| $16$ | $19$ or $20$ | $19.7$ |
| $32$ | $9$ or $10$ | $9.6$ |
| $8$ | from $8$ to $41$ | $41.5$ |

For $s = 8$, the short runs ended in an early breakdown. These are observations.

**Success.** On $20$ random matrices of the same shape, with nullity $10.05$ on average, one try found:

| block width $s$ | runs with at least one vector | vectors found on average | runs that found the whole kernel |
|---|---|---|---|
| $8$ | $16$ of $20$ | $5.9$ | $0$ |
| $16$ | $20$ of $20$ | $10.0$ | $19$ |
| $32$ | $20$ of $20$ | $10.0$ | $20$ |

**Space.** $B$ plus about seven $n \times s$ blocks ($Y$, $X$, $V_0$, $V_i$, $V_{i-1}$, $V_{i-2}$, $AV_i$), which is $O(w + ns)$. With $s = 64$, a block is $8n$ bytes.

## Properties

- **Las Vegas.** Every returned vector is checked. A bad random choice can only lower the number of vectors found.
- **Black box.** Only products with $B$ and $B^T$ are needed. The matrix is never modified, and no fill-in occurs.
- **Bit parallel.** Over $\mathbb{F}_2$ with $s$ equal to the word size, one sparse product advances $s$ vectors.
- **Short memory.** Only the last three blocks are kept, unlike Gram-Schmidt or GMRES-style methods, which keep all of them.
- **Communication every step.** Each iteration needs the full product $A V_i$ before the next one. On a cluster, this means a global exchange per iteration. Block Wiedemann avoids this.

## Variants and improvements

- **Coppersmith's block Lanczos.** Coppersmith's 1993 method also works over $\mathbb{F}_2$ with blocks, but handles self-orthogonal vectors with look-ahead. Montgomery's subspace selection is simpler, and it replaced it in practice.
- **Scalar Lanczos over large fields.** For $\mathbb{F}_p$ with large $p$, the scalar [Lanczos](/lanczos-algorithm/) or [conjugate gradient](/conjugate-gradient-method/) iteration on $B^T B$, or on $B$ itself when $B$ is symmetric, rarely meets a self-orthogonal vector. LaMacchia and Odlyzko used this in 1990. A random diagonal scaling helps.
- **Block width.** $s = 64$ or $128$ matches the machine word or vector registers. Wider blocks give fewer iterations but cost more per inner product.
- **Parallel versions.** Splitting $B$ into a grid of blocks across processors, as in msieve and CADO-NFS, makes each iteration a distributed product followed by a reduction of $s \times s$ matrices.
- **Block Wiedemann.** The [block Wiedemann algorithm](/block-wiedemann-algorithm/) uses about the same number of products. It replaces the per-step communication by a matrix generator computation at the end.

## When to use it

Use block Lanczos for the kernel of a very large sparse matrix over $\mathbb{F}_2$, as in the last step of the [quadratic sieve](/quadratic-sieve/) and the [number field sieve](/general-number-field-sieve/), when the whole matrix fits on one machine or on a cluster with a fast network. Shrink the matrix first with [structured Gaussian elimination](/structured-gaussian-elimination/). For a few thousand columns, dense [bit-packed elimination](/bitset-gaussian-elimination/) is simpler and fast, at $O(n^\omega)$ or $O(n^3 / \text{word size})$ word operations. For loosely connected machines, use block Wiedemann.

## Pitfalls

- **Using $B$ instead of $B^T B$.** Lanczos needs a symmetric matrix. For a nonsymmetric or rectangular $B$, iterate on $A = B^T B$, and remove the vectors of $\ker A$ that are not in $\ker B$ in the final step.
- **Forgetting the selection condition.** Every column left out at step $i - 1$ must be chosen at step $i$, or the three-term recurrence loses orthogonality. Check it, and treat a failure as a breakdown.
- **Taking $X + Y$ alone.** Over $\mathbb{F}_2$ the iteration usually ends with a nonzero $V_m$, and $X + Y$ is then not in $\ker A$. The final elimination must include the columns of $V_m$, as in the example.
- **Small blocks.** With $s = 8$, about a third of the runs above broke down early. Use $s \ge 16$, and retry with a new $Y$ when nothing is found.
- **Expecting the whole kernel.** One run gives at most about $s$ independent vectors, and fewer if $\ker B$ is large. Factoring needs only a few dependencies, but a full nullspace needs repeated runs.
- **Empty and singleton columns.** These give trivial or useless dependencies. Remove them before the iteration.

## Implementations

## History

Cornelius Lanczos introduced his iteration in 1950 for eigenvalue problems, and it became the basis of the conjugate gradient family. Over finite fields, LaMacchia and Odlyzko (1990) used scalar Lanczos and conjugate gradient for sparse systems from factoring and discrete logarithms, and Wiedemann (1986) gave a different Krylov method. Don Coppersmith gave a block version over $\mathbb{F}_2$ in 1993. Peter Montgomery's 1995 version, with its choice of subspaces at each step, was simpler and faster. It became the standard linear algebra step of the quadratic and number field sieves, as in msieve and in many factoring records before block Wiedemann took over the largest ones.

## References
