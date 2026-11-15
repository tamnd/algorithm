---
tag: 55N3T2
kind: algorithm
slug: invariant-subspace-algorithm
name: Invariant subspace algorithm
aliases:
- ISA
- V-star algorithm
area: control/state-space-control
level: advanced
summary: "Computes the largest controlled invariant subspace inside a subspace K by the descending recursion V_(k+1) = K meet A^(-1)(V_k + im B), which stops after at most dim K + 1 passes."
solves: [disturbance-decoupling-problem]
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs}
  time: {worst: "O(n^3 (n + m))"}
  space: {extra: "O(n (n + m))"}
properties: {deterministic: true, exact: true, recursive: false, online: false}
history:
  year: 1970
  people: [Giuseppe Basile, Giovanni Marro, W. Murray Wonham, A. Stephen Morse]
  note: "Basile and Marro defined controlled invariant subspaces in 1969; Wonham and Morse gave the supremal (A, B)-invariant subspace in ker C and the recursion that computes it in 1970."
prereqs: [controlled-invariant-subspace, reduced-row-echelon-form]
see_also: [disturbance-decoupling-problem, zero-dynamics, transmission-zero, unknown-input-observer, kalman-decomposition, gaussian-elimination, singular-value-decomposition, condition-number]
sources:
  - paper: doi:10.1137/0308001
    title: W. M. Wonham and A. S. Morse, Decoupling and pole assignment in linear multivariable systems, a geometric approach, SIAM Journal on Control 8(1), 1-18, 1970
    locator: the supremal (A, B)-invariant subspace contained in a given subspace and the descending recursion for it
  - paper: doi:10.1007/BF00931370
    title: G. Basile and G. Marro, Controlled and conditioned invariant subspaces in linear system theory, Journal of Optimization Theory and Applications 3(5), 306-315, 1969
    locator: the controlled and conditioned invariant subspaces and the algorithms for the extreme ones
  - book: isbn:9780387960715
    title: W. Murray Wonham, Linear Multivariable Control, A Geometric Approach, third edition, Springer, 1985
    locator: Chapter 4, Disturbance Decoupling and Output Stabilization (the algorithm for the supremal (A, B)-invariant subspace)
  - book: isbn:9781852333164
    title: Harry L. Trentelman, Anton A. Stoorvogel and Malo Hautus, Control Theory for Linear Systems, Springer, 2001
    locator: Chapter 4, Controlled invariant subspaces
---

The invariant subspace algorithm (ISA) computes $\mathcal{V}^\ast(\mathcal{K})$, the largest [controlled invariant subspace](/controlled-invariant-subspace/) of $\dot x = A x + B u$ inside a given subspace $\mathcal{K}$. It starts from $\mathcal{V}_0 = \mathcal{K}$ and repeats $\mathcal{V}_{k+1} = \mathcal{K} \cap A^{-1}(\mathcal{V}_k + \operatorname{im} B)$, where $A^{-1}\mathcal{S} = \{x : A x \in \mathcal{S}\}$ is the preimage, not an inverse matrix. The subspaces shrink, and once two of them have the same dimension the last one is $\mathcal{V}^\ast$. So the algorithm stops after at most $\dim \mathcal{K} + 1$ passes, and each pass is a few rank computations. With $\mathcal{K} = \ker C$ it gives the subspace that decides the [disturbance decoupling problem](/disturbance-decoupling-problem/) and that carries the [zero dynamics](/zero-dynamics/) of a linear system. The algorithm is due to Wonham and Morse (1970), after the controlled invariant subspaces of Basile and Marro (1969).

## In plain words

Some states of a machine are safe: from them, a well chosen input can keep the machine safe for all future time. The safe region of interest here is a flat region through the origin, for example all states where a sensor reads zero. Not every state in that region is good, because from some of them the machine must leave the region at once, whatever input you apply. The algorithm removes those states. After the removal, other states may become bad, because their only way to stay was through a removed state. So it removes again, and again. The region gets smaller at each step, and it cannot get smaller more often than its number of dimensions. When a step removes nothing, every remaining state can stay in the region forever.

## The problem

Input: $A \in \mathbb{Q}^{n \times n}$, $B \in \mathbb{Q}^{n \times m}$ and a basis of a subspace $\mathcal{K} \subseteq \mathbb{Q}^n$. Output: a basis of

$$\mathcal{V}^\ast(\mathcal{K}) = \text{the largest subspace } \mathcal{V} \subseteq \mathcal{K} \text{ with } A \mathcal{V} \subseteq \mathcal{V} + \operatorname{im} B.$$

The largest one exists because the sum of two controlled invariant subspaces is controlled invariant (see [controlled invariant subspace](/controlled-invariant-subspace/)). The implementation also returns the list of dimensions $\dim \mathcal{V}_0, \dim \mathcal{V}_1, \dots$, and a friend $K$ with $(A - BK)\mathcal{V}^\ast \subseteq \mathcal{V}^\ast$ on request. The usual case is $\mathcal{K} = \ker C$ for an output $y = C x$, and then $\mathcal{V}^\ast$ is written without the argument.

## The algorithm

```pseudo id=main
ISA(A, B, K)
L1  V ← K                                    ▷ V_0 = K
L2  repeat
L3      W ← K ∩ A⁻¹(V + im B)                ▷ V_(k+1); A⁻¹ is the preimage
L4      if dim W = dim V then
L5          return W                         ▷ W = V = V*
L6      V ← W
```

Line L1 starts with the whole subspace $\mathcal{K}$. Line L3 is the only real work. The sum $\mathcal{V} + \operatorname{im} B$ is the span of the two bases, reduced to a basis by [reduced row echelon form](/reduced-row-echelon-form/). The preimage of a subspace $\mathcal{S}$ with basis matrix $S$ is the $x$ part of the kernel of $[A, -S]$, because $A x = S z$ for some $z$ exactly when $x \in A^{-1}\mathcal{S}$. The intersection of two subspaces with basis matrices $U$ and $V$ is $U$ times the $a$ part of the kernel of $[U, -V]$. Line L4 compares only dimensions. This is enough, because $\mathcal{V}_{k+1} \subseteq \mathcal{V}_k$ always holds, and a subspace of the same dimension inside another one is equal to it. Line L6 makes the new subspace the current one.

The implementation uses exact rational arithmetic (Python `Fraction`), so every rank decision is exact. It also builds a friend: on a basis $v_1, \dots, v_q$ of $\mathcal{V}^\ast$ it solves $A v_i = \sum_j w_{ij} v_j - B u_i$, and it sets $K v_i = -u_i$ and $K = 0$ on a complement.

## Example

**A disturbance decoupling example.** Take

$$A = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & -1 \end{bmatrix}, \quad B = e_2, \quad C = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix}, \quad \mathcal{K} = \ker C = \operatorname{span}(e_2, e_3).$$

| pass | $\mathcal{V}_k$ | $\mathcal{V}_k + \operatorname{im} B$ | $A^{-1}(\mathcal{V}_k + \operatorname{im} B)$ | $\mathcal{V}_{k+1}$ | dimensions |
| --- | --- | --- | --- | --- | --- |
| 1 | $\operatorname{span}(e_2, e_3)$ | $\operatorname{span}(e_2, e_3)$ | $\{x : x_2 = 0\} = \operatorname{span}(e_1, e_3)$ | $\operatorname{span}(e_3)$ | 2 to 1 |
| 2 | $\operatorname{span}(e_3)$ | $\operatorname{span}(e_2, e_3)$ | $\operatorname{span}(e_1, e_3)$ | $\operatorname{span}(e_3)$ | 1 to 1, stop |

In pass 1, $A x = (x_2, x_3, -x_3)$ lies in $\operatorname{span}(e_2, e_3)$ exactly when $x_2 = 0$. The intersection with $\mathcal{K}$ leaves $\operatorname{span}(e_3)$. In pass 2 the sum with $\operatorname{im} B$ is the same as before, so line L4 stops and line L5 returns $\mathcal{V}^\ast = \operatorname{span}(e_3)$. The list of dimensions is $[2, 1, 1]$. The friend from the code is $K = \begin{bmatrix} 0 & 0 & 1 \end{bmatrix}$: then $(A - BK) e_3 = e_2 - e_3 - e_2 = -e_3$. The [disturbance decoupling problem](/disturbance-decoupling-problem/) page uses this result.

**A chain of four integrators.** For $\dot x_1 = x_2$, $\dot x_2 = x_3$, $\dot x_3 = x_4$, $\dot x_4 = u$ and $y = x_1$, the passes give $\operatorname{span}(e_2, e_3, e_4)$, then $\operatorname{span}(e_3, e_4)$, then $\operatorname{span}(e_4)$, then $\{0\}$, and the dimensions are $[3, 2, 1, 0, 0]$. Each pass removes one state, because the output must have zero derivatives up to order 3, and the input reaches only the fourth derivative. The result $\mathcal{V}^\ast = \{0\}$ says that this system has no zero dynamics. This example needs the maximum number of passes: three passes that shrink and one that confirms, which is $\dim \mathcal{K} + 1 = 4$.

## Correctness

The full proof is in proofs/correctness.md. It has four steps, and each is a theorem.

1. **The sequence decreases.** $\mathcal{V}_1 \subseteq \mathcal{K} = \mathcal{V}_0$. If $\mathcal{V}_k \subseteq \mathcal{V}_{k-1}$, then $\mathcal{V}_k + \operatorname{im} B \subseteq \mathcal{V}_{k-1} + \operatorname{im} B$, and the preimage and the intersection keep this order, so $\mathcal{V}_{k+1} \subseteq \mathcal{V}_k$.
2. **It stops.** Each pass either lowers the dimension or gives $\mathcal{V}_{k+1} = \mathcal{V}_k$. The dimension starts at $\dim \mathcal{K}$ and cannot go below 0, so line L4 succeeds at the latest in pass $\dim \mathcal{K} + 1$.
3. **The result is controlled invariant and lies in $\mathcal{K}$.** At the stop, $\mathcal{V} = \mathcal{K} \cap A^{-1}(\mathcal{V} + \operatorname{im} B)$. So $\mathcal{V} \subseteq A^{-1}(\mathcal{V} + \operatorname{im} B)$, which says $A \mathcal{V} \subseteq \mathcal{V} + \operatorname{im} B$.
4. **The result contains every controlled invariant subspace in $\mathcal{K}$.** Let $\mathcal{U} \subseteq \mathcal{K}$ with $A\mathcal{U} \subseteq \mathcal{U} + \operatorname{im} B$. Then $\mathcal{U} \subseteq \mathcal{V}_0$, and if $\mathcal{U} \subseteq \mathcal{V}_k$, then $A \mathcal{U} \subseteq \mathcal{V}_k + \operatorname{im} B$, so $\mathcal{U} \subseteq \mathcal{K} \cap A^{-1}(\mathcal{V}_k + \operatorname{im} B) = \mathcal{V}_{k+1}$.

A second description of $\mathcal{V}_k$ gives an independent check. By induction on $k$, $\mathcal{V}_k$ is the set of states $x_0$ for which some inputs $u_0, \dots, u_{k-1}$ keep the discrete-time sequence $x_{j+1} = A x_j + B u_j$ in $\mathcal{K}$ for $j = 0, \dots, k$. With $\mathcal{K} = \ker C$ this is the set of $x_0$ for which $\mathcal{O}_k x_0 \in \operatorname{im} T_k$, where $\mathcal{O}_k$ stacks $C, CA, \dots, CA^k$ and $T_k$ is the block Toeplitz matrix of the [Markov parameters](/markov-parameters/) $CA^iB$. The tests compare the algorithm with this formula for $k = n$ on 500 random integer systems, and they check the friend, the dimension list, and a brute force search over feedback gains for the decoupling problem.

## Complexity

In the [real RAM](/real-ram/), with exact arithmetic on the entries:

- Line L3 builds a matrix with $n$ rows and at most $n + m$ columns for the sum, one with $n$ rows and at most $2n + m$ columns for the preimage, and one with $n$ rows and at most $2n$ columns for the intersection. Each kernel or rank by [Gaussian elimination](/gaussian-elimination/) costs $O(n^2 (n + m))$.
- Lines L4 and L6 cost $O(n^2)$.
- Lines L2 to L6 run at most $\dim \mathcal{K} + 1 \le n + 1$ times.

So the time is $O(n^3 (n + m))$ and the extra space is $O(n (n + m))$. This is a theorem about the number of arithmetic operations. With `Fraction` entries the cost in bit operations is higher, because the numerators and denominators grow; for integer data of bit size $\beta$ the sizes stay polynomial in $n$ and $\beta$ if the elimination is done in a fraction-free way, but the implementation does not bound them.

## Properties

- **The result for one input and one output.** If $C A^{i} B = 0$ for $i < \rho - 1$ and $C A^{\rho - 1} B \ne 0$, the relative degree is $\rho$. Then the rows $C, CA, \dots, CA^{\rho - 1}$ are linearly independent, $\mathcal{V}^\ast = \ker \begin{bmatrix} C \\ CA \\ \vdots \\ CA^{\rho - 1} \end{bmatrix}$ and $\dim \mathcal{V}^\ast = n - \rho$. This is a theorem; for the chain it gives $4 - 4 = 0$, and for the first example $3 - 2 = 1$.
- **Fixed poles are zeros.** The eigenvalues of $A - BK$ restricted to $\mathcal{V}^\ast$ that are the same for every friend $K$ are the invariant zeros of $(A, B, C)$. For a system with as many inputs as outputs and an invertible transfer function they are the [transmission zeros](/transmission-zero/). This is a theorem of the geometric theory; in the first example the only friend eigenvalue on $\mathcal{V}^\ast$ is $-1$, and $C(sI - A)^{-1} B = (s + 1)/(s^2 (s + 1))$ before cancellation, so $-1$ is the invariant zero.
- **Dual algorithm.** The smallest conditioned invariant subspace containing a subspace $\mathcal{S}_0$ comes from the increasing recursion $\mathcal{S}_{k+1} = \mathcal{S}_0 + A(\mathcal{S}_k \cap \ker C)$. It is the ISA for $(A^T, C^T)$ applied to orthogonal complements, and it is used for observers with unknown inputs (see [unknown input observer](/unknown-input-observer/)).
- **Not continuous in the data.** $\mathcal{V}^\ast$ can jump when the matrices change by a small amount, as the second pitfall below shows. The exact algorithm computes the right answer for the given rational data, but that answer can be a poor model of a physical system whose matrices are known only approximately.

## Variants and improvements

- **Controllability subspace algorithm.** The largest controllability subspace $\mathcal{R}^\ast$ in $\ker C$ comes from a second, increasing recursion inside $\mathcal{V}^\ast$: $\mathcal{S}_0 = \{0\}$, $\mathcal{S}_{k+1} = \mathcal{V}^\ast \cap (A \mathcal{S}_k + \operatorname{im} B)$. It is needed for the decoupling problems with pole placement (Wonham and Morse 1970).
- **Stabilizable version.** For disturbance decoupling with internal stability one needs the largest stabilizability subspace in $\ker C$. It is computed from $\mathcal{V}^\ast$, $\mathcal{R}^\ast$ and the fixed poles: keep the part of $\mathcal{V}^\ast$ that belongs to fixed poles in the open left half plane.
- **Orthonormal bases in floating point.** Numerical versions replace the echelon forms by [QR decompositions](/qr-decomposition/) with column pivoting or by the [singular value decomposition](/singular-value-decomposition/), and decide each rank with a tolerance. They give a nearby subspace for a nearby system, which is what one can ask for an ill-posed problem.
- **Pencil methods.** $\mathcal{V}^\ast$ can also be read from the Kronecker structure of the system pencil $\begin{bmatrix} A - \lambda I & B \\ C & 0 \end{bmatrix}$, which staircase algorithms compute with orthogonal transformations. This is the usual route in numerical libraries.

## When to use it

Use the exact ISA to decide structural questions about a model with known rational entries: whether a disturbance can be decoupled, what the zero dynamics of a linear system are, whether an observer with unknown inputs exists. It is also the right tool in teaching and in symbolic work, because each pass has a clear meaning. For models with measured or rounded entries, use a numerical version with orthogonal bases and an explicit rank tolerance, and check the answer for a few tolerances. If you need only the invariant zeros of a square system, a [generalized eigenvalue](/generalized-eigenvalue-problem/) computation on the system pencil is cheaper and better conditioned.

## Pitfalls

- **Line L3 without the intersection with $\mathcal{K}$.** Without "$\mathcal{K} \cap$", the recursion $\mathcal{V}_{k+1} = A^{-1}(\mathcal{V}_k + \operatorname{im} B)$ does not stay in $\mathcal{K}$, and its limit is a controlled invariant subspace that has nothing to do with the output. In the first example it gives $\operatorname{span}(e_1, e_3)$ in pass 1, which is not in $\ker C$.
- **Line L3 with floating-point rank decisions.** Take $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $C = \begin{bmatrix} 1 & 0 \end{bmatrix}$ and $B = \begin{bmatrix} \varepsilon \\ 1 \end{bmatrix}$. For $\varepsilon \ne 0$ the sum $\ker C + \operatorname{im} B$ is the whole plane and $\mathcal{V}^\ast = \ker C$, of dimension 1. For $\varepsilon = 0$ it is $\ker C$ itself, and $\mathcal{V}^\ast = \{0\}$. The exact code returns dimension lists $[1, 1]$ for $\varepsilon = 1/1000$ and $[1, 0, 0]$ for $\varepsilon = 0$. In floating point an $\varepsilon$ near the rounding unit of the [floating-point model](/floating-point-model/) can fall on either side of the rank tolerance. State the tolerance, and look at the gaps of the singular values next to each rank decision.
- **Line L3 with the image instead of the preimage.** The recursion $\mathcal{K} \cap A(\mathcal{V}_k + \operatorname{im} B)$ is a different map. The forward image belongs to the dual, increasing algorithm for conditioned invariant subspaces, and it does not give $\mathcal{V}^\ast$.
- **Line L4 that compares bases.** Two bases of the same subspace can differ entrywise, so a test "$W = V$ as matrices" can fail to stop. Compare dimensions, as line L4 does, or compare the reduced row echelon forms, which are unique.
- **Line L5 is not the end of a design.** $\mathcal{V}^\ast$ alone does not give a usable feedback. The friend is not unique, and its fixed poles, the invariant zeros, may be in the right half plane. A disturbance decoupling design with such a friend has an unstable closed loop; use the stabilizable version.

## Implementations

## History

Basile and Marro (1969) introduced controlled and conditioned invariant subspaces as tools for linear system theory. Wonham and Morse (1970) introduced the name $(A, B)$-invariant subspace, proved that the supremal one in a given subspace exists, gave the descending recursion to compute it, and used it to solve the disturbance decoupling problem and the decoupling of outputs by state feedback. Wonham's book *Linear Multivariable Control, A Geometric Approach* (first edition 1974, third edition 1985) made the method a standard part of linear control theory. The book of Trentelman, Stoorvogel and Hautus (2001) gives a modern treatment with the stabilizability subspaces.

## References
