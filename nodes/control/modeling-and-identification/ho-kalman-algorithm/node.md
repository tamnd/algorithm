---
tag: A1602S
kind: algorithm
slug: ho-kalman-algorithm
name: Ho-Kalman algorithm
aliases:
- Ho-Kalman realization algorithm
area: control/modeling-and-identification
level: advanced
summary: Builds a minimal state-space realization from exact Markov parameters by a rank factorization of their block Hankel matrix.
solves: [realization-problem]
model: real-ram
complexity:
  vars: {N: the number of block rows and block columns of the Hankel matrix, n: the minimal order, m: the number of inputs, p: the number of outputs}
  time: {worst: O(N^2 m n p + n^3)}
  space: {extra: O(N^2 m p)}
properties: {deterministic: true, online: false, exact: true}
history:
  year: 1966
  people: [B. L. Ho, Rudolf E. Kalman]
  note: "Ho and Kalman showed in 1966 that a rank factorization of the block Hankel matrix of the Markov parameters gives a minimal realization, and that the rank of this matrix is the minimal order."
prereqs: [markov-parameters, minimal-realization, gaussian-elimination]
see_also: [realization-problem, eigensystem-realization-algorithm, kalman-rank-condition, similarity-transformation, prony-method, subspace-identification, balanced-realization, impulse-response]
sources:
  - paper: doi:10.1524/auto.1966.14.112.545
    title: "B. L. Ho and Rudolf E. Kalman, Effective construction of linear state-variable models from input/output functions, Regelungstechnik 14(1-12), 545-548, 1966"
    locator: the rank of the block Hankel matrix as the minimal order, and the construction of the realization from it
  - book: isbn:9780195117776
    title: "Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999"
    locator: "Chapter 7 (minimal realizations), the section on realization from Markov parameters"
  - book: isbn:9780130792112
    title: "Jer-Nan Juang, Applied System Identification, Prentice Hall, 1994"
    locator: the chapter on system realization (the Ho-Kalman construction as the noise-free case of ERA)
---

The Ho-Kalman algorithm takes the first $2N$ [Markov parameters](/markov-parameters/) $h_k = C A^{k-1} B$ of a discrete-time linear system and returns matrices $(A, B, C, D)$ of the smallest possible order that reproduce them. It puts the parameters in a block Hankel matrix, finds its rank $n$ by exact elimination, and reads the realization off an invertible $n \times n$ submatrix. The [realization problem](/realization-problem/) is the task, the [minimal realization](/minimal-realization/) theorem says that the answer is unique up to a change of coordinates, and Ho-Kalman is the exact construction for data without noise. For measured, noisy data use the [eigensystem realization algorithm](/eigensystem-realization-algorithm/), which replaces the exact rank by a truncated singular value decomposition.

## In plain words

Hit a system with a single short pulse and record the response at every sample. These numbers fix the input-output behaviour of the system, but they do not show its internal state. Write the numbers in a table where each row is the row above it moved one step to the left. A system with a small state can only make a few independent patterns, so the table has a low rank, and the rank is the number of state variables that you need. Pick that many independent rows and columns. A small square block of the table then gives the input map and the output map, and the same block taken from the table moved one step gives the state transition.

## The problem

**Input.** Matrices $h_0, h_1, \ldots, h_{2N}$ of size $p \times m$, and the integer $N \ge 1$.

**Precondition.** Some state-space system of order at most $N$ has $h_0 = D$ and $h_k = C A^{k-1} B$ for every $k \ge 1$. The system is $x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$ with $x_k \in \mathbb{R}^n$, $u_k \in \mathbb{R}^m$ and $y_k \in \mathbb{R}^p$.

**Output.** $(A, B, C, D)$ of the smallest order $n$ with $D = h_0$ and $C A^{k-1} B = h_k$ for every $k \ge 1$.

There is no page for the Hankel matrix, so here is the definition. The block Hankel matrix with $N$ block rows and $N$ block columns is

$$H = \begin{pmatrix} h_1 & h_2 & \cdots & h_N \\ h_2 & h_3 & \cdots & h_{N+1} \\ \vdots & & & \vdots \\ h_N & h_{N+1} & \cdots & h_{2N-1} \end{pmatrix} \in \mathbb{R}^{Np \times Nm},$$

with block $(i, j)$ equal to $h_{i+j-1}$. The shifted matrix $H_s$ has block $(i, j)$ equal to $h_{i+j}$, so it uses $h_2, \ldots, h_{2N}$.

## The algorithm

```pseudo id=main
HO-KALMAN(h, N)
L1  H ← the block Hankel matrix of h_1, ..., h_(2N-1)
L2  Hs ← the shifted block Hankel matrix of h_2, ..., h_(2N)
L3  J ← indices of a maximal set of independent columns of H;  n ← |J|
L4  I ← indices of n independent rows of H[:, J]
L5  M ← H[I, J]
L6  A ← M⁻¹ Hs[I, J]
L7  B ← M⁻¹ H[I, 1:m]
L8  C ← H[1:p, J]
L9  D ← h_0
L10 return (A, B, C, D)
```

L3 runs Gaussian elimination on $H$ and keeps a column when it is not a combination of the columns kept before it. The number of kept columns is the rank of $H$, and Lemma 2 of the proof shows that this rank is the minimal order. L4 does the same on the rows of the $Np \times n$ matrix $H[:, J]$, so the $n \times n$ matrix $M$ of L5 is invertible. L6 and L7 solve linear systems with $M$; they never form $M^{-1}$. L7 uses the first block column of $H$, which holds $h_1, \ldots, h_N$, and L8 uses the first block row. With integer or rational data every step is exact in rational arithmetic.

## Example

Take one input and one output ($m = p = 1$) and the data

$$h_0 = 1, \quad h_1 = 2, \quad h_2 = 0, \quad h_3 = \tfrac12, \quad h_4 = 0,$$

with $N = 2$. L1 and L2 give

$$H = \begin{pmatrix} 2 & 0 \\ 0 & 1/2 \end{pmatrix}, \qquad H_s = \begin{pmatrix} 0 & 1/2 \\ 1/2 & 0 \end{pmatrix}.$$

$H$ has rank 2, so L3 and L4 keep both columns and both rows, $n = 2$ and $M = H$. Then

$$A = M^{-1} H_s = \begin{pmatrix} 0 & 1/4 \\ 1 & 0 \end{pmatrix}, \qquad B = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \qquad C = \begin{pmatrix} 2 & 0 \end{pmatrix}, \qquad D = 1.$$

Check: $C B = 2$, $C A B = 0$, $C A^2 B = 1/2$ and $C A^3 B = 0$. The characteristic polynomial of $A$ is $s^2 - 1/4$, so the poles are $\pm 1/2$, and the realization predicts $h_5 = C A^4 B = 1/8$, which is the next value of the sequence $h_k = (1/2)^{k-1} + (-1/2)^{k-1}$. The test file checks the predicted values up to $h_{10}$ exactly in Fraction.

## Correctness

**Claim.** Under the precondition, HO-KALMAN returns a realization of order $n$, the minimal order, with $C A^{k-1} B = h_k$ for every $k \ge 1$, also for the $k > 2N$ that were not in the data.

**Key invariant.** For a minimal realization $(A_0, B_0, C_0)$ of order $n$, $H = \mathcal{O} \mathcal{C}$ and $H_s = \mathcal{O} A_0 \mathcal{C}$, where $\mathcal{O}$ stacks $C_0 A_0^{i}$ and $\mathcal{C}$ lines up $A_0^{j} B_0$ for $i, j = 0, \ldots, N-1$. Both factors have rank $n$ because a minimal realization is controllable and observable.

With $T = \mathcal{C}[:, J]$ and $S = \mathcal{O}[I, :]$ the selected block is $M = S T$, so both factors are invertible. The output is then $A = T^{-1} A_0 T$, $B = T^{-1} B_0$ and $C = C_0 T$, a change of coordinates of the minimal realization. The full proof is below.

## Complexity

In the [real RAM](/real-ram/), with exact arithmetic. L1 and L2 copy $O(N^2 m p)$ numbers. L3 eliminates on the $Np \times Nm$ matrix $H$; each of the $n$ pivots updates $O(N^2 m p)$ entries, and the search for pivots in the other columns costs $O(N^2 m p)$ in total, so L3 costs $O(N^2 m n p)$. L4 eliminates on an $Np \times n$ matrix in $O(N n^2 p)$. L6 and L7 factor $M$ once in $O(n^3)$ and solve for $n + m$ right-hand sides in $O(n^2 (n + m))$. The total is $O(N^2 m n p + n^3)$, which is $O(N^2 m n p)$ because $n \le N \min(m, p)$. The extra space is $O(N^2 m p)$ for $H$ and $H_s$.

With rational data the numbers in the elimination can grow; the operation count above does not include the bit length. In floating point, the rank decision of L3 needs a tolerance and becomes the weak point (see Pitfalls).

## Properties

- **Minimal (theorem).** The order of the result is the rank of $H$, and under the precondition this is the minimal order (Ho and Kalman 1966).
- **Exact extrapolation (theorem).** The result reproduces every Markov parameter, not only the $2N$ that were used.
- **Unique up to coordinates (theorem).** Any other choice of $I$ and $J$ gives a similar realization, because all minimal realizations are similar.
- **Enough data (theorem).** If the order is at most $n$, then $N = n$ is enough, so $2n$ Markov parameters $h_1, \ldots, h_{2n}$ fix the whole sequence.
- **Not robust to noise.** The rank of a matrix is not a continuous function of its entries. Any noise makes $H$ generically of full rank.

## Variants and improvements

- **[Eigensystem realization algorithm](/eigensystem-realization-algorithm/).** Replace L3 to L5 by a singular value decomposition of $H$ and keep the $n$ largest singular values. This gives a balanced realization on exact data and a good approximation on noisy data.
- **Kung's method.** The same SVD idea, published for signal processing in 1978, with the shift structure of the observability factor used to find $A$.
- **Rectangular Hankel matrices.** Use $r$ block rows and $c$ block columns with $r, c \ge n$. The proof does not change.
- **Partial realization.** When the sequence is only known up to $h_{2N}$ and no order is given, the minimal partial realization problem asks for the smallest system that matches the given terms. The Berlekamp-Massey algorithm solves the scalar case.
- **From input-output data.** Estimate the Markov parameters first, for example by an FIR fit, or skip them and use [subspace identification](/subspace-identification/).

## When to use it

Use it when the Markov parameters are exact: symbolic models, rational data, the conversion of a transfer function or an FIR model to state-space form, and teaching. It also checks other methods: on exact data, ERA and subspace methods must give a system similar to the Ho-Kalman result. For measured impulse responses, use ERA.

## Pitfalls

- **Too few block rows.** If $N$ is smaller than the order, the rank of $H$ can be smaller than the order and the result is wrong after the data. For $h_k = (1/2)^{k-1} + (-1/2)^{k-1}$ with $N = 1$ the algorithm returns $A = 0$, $B = 1$, $C = 2$, which matches $h_1$ and $h_2$ but predicts $h_3 = 0$ instead of $1/2$.
- **Floating-point rank decisions.** In floating point, a pivot of $10^{-14}$ can be noise or a real small mode. The result depends on a threshold that the algorithm does not give. Use the SVD of ERA, which shows the gap in the singular values.
- **Forgetting $h_0$.** $h_0 = D$ is not in the Hankel matrix. A strictly proper model has $h_0 = 0$; a model with a direct feedthrough needs L9.
- **Index shift.** Block $(i, j)$ of $H$ is $h_{i+j-1}$, starting at $h_1$. If $H$ starts at $h_0$, then $D$ enters the factorization and the rank is wrong.
- **Continuous time.** For $x' = A x + B u$ the same construction works with the coefficients $C A^{k-1} B$ of the expansion $G(s) = D + \sum_{k \ge 1} C A^{k-1} B s^{-k}$ at infinity. These are the derivatives of the impulse response at $t = 0$. They are not the samples of the impulse response, which are the Markov parameters of the discretized system.

## Implementations

## History

Ho and Kalman published the construction in 1966 in Regelungstechnik, in a paper on the effective construction of linear state-variable models from input-output functions. They showed that the rank of the block Hankel matrix of the Markov parameters is the dimension of a minimal realization, and they built the realization from a factorization of that matrix. The idea that a rational transfer function gives a Hankel matrix of finite rank is older, and goes back to Kronecker's work on rational functions in the nineteenth century. In the 1970s Kung, Zeiger and McEwen, and later Juang and Pappa in 1985, replaced the exact rank by a singular value decomposition, so that the method could use measured data.

## References
