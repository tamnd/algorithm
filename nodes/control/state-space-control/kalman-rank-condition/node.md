---
tag: A2NF3D
kind: theorem
slug: kalman-rank-condition
name: Kalman rank condition
aliases:
- controllability matrix test
- Kalman controllability test
area: control/state-space-control
level: core
summary: An LTI system is controllable if and only if the matrix [B, AB, ..., A^(n-1)B] has full rank n, and observable by the dual test.
prereqs: [controllability, observability, cayley-hamilton-theorem]
see_also: [popov-belevitch-hautus-test, controllability-gramian, kalman-decomposition, ackermann-formula, pole-placement-theorem, krylov-subspace, condition-number]
sources:
  - paper: "R. E. Kalman, Y. C. Ho and K. S. Narendra, Controllability of linear dynamical systems, Contributions to Differential Equations 1, 189-213, 1963"
    locator: the rank condition for controllability of time-invariant linear systems
  - paper: "R. E. Kalman, Contributions to the theory of optimal control, Boletín de la Sociedad Matemática Mexicana (2) 5, 102-119, 1960"
    locator: controllability and its test by the gramian integral
  - paper: doi:10.1109/TAC.1981.1102563
    title: C. C. Paige, Properties of numerical algorithms related to computing controllability, IEEE Transactions on Automatic Control 26(1), 130-138, 1981
    locator: why the rank of the controllability matrix is a poor numerical test, and a numerically stable orthogonal alternative
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 6.2 (controllability and controllability indices), Section 6.3 (observability) and Section 6.6 (discrete time)
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Section 3.2, Controllability and Observability
---

The Kalman rank condition decides [controllability](/controllability/) of a linear time-invariant system by one rank computation: the pair $(A, B)$ is controllable if and only if the controllability matrix $[B, AB, \dots, A^{n-1} B]$ has rank $n$, the dimension of the state. The transposed test decides [observability](/observability/). The proof also shows that the range of this matrix is exactly the set of states the input can reach. The test is exact in rational arithmetic, but in floating point it is badly conditioned, and numerical codes use orthogonal methods or the [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/) instead.

## Statement

Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$ and $C \in \mathbb{R}^{p \times n}$. Define the controllability matrix and the observability matrix

$$\mathcal{C} = \begin{bmatrix} B & AB & \cdots & A^{n-1} B \end{bmatrix} \in \mathbb{R}^{n \times nm}, \qquad \mathcal{O} = \begin{bmatrix} C \\ CA \\ \vdots \\ CA^{n-1} \end{bmatrix} \in \mathbb{R}^{pn \times n}.$$

**Theorem.** For the system $\dot x = A x + B u$, $y = C x + D u$ with piecewise continuous inputs, and for every $T > 0$:

1. The set of states $x(T)$ reachable from $x(0) = 0$ is the subspace $\operatorname{range} \mathcal{C}$.
2. $(A, B)$ is controllable if and only if $\operatorname{rank} \mathcal{C} = n$.
3. The set of initial states $x_0$ with $C e^{At} x_0 = 0$ for all $t \in [0, T]$ is the subspace $\ker \mathcal{O}$.
4. $(C, A)$ is observable if and only if $\operatorname{rank} \mathcal{O} = n$.

For the discrete-time system $x_{k+1} = A x_k + B u_k$, the states reachable from $x_0 = 0$ in $N \ge n$ steps form $\operatorname{range} \mathcal{C}$, and the outputs $y_0, \dots, y_{N-1}$ with zero input determine $x_0$ if and only if $\operatorname{rank} \mathcal{O} = n$.

## In plain words

Push the system with the input and watch where the state can go. The input moves the state along the columns of the input matrix. The dynamics then turn those directions, and turned again, and so on. The theorem says that a finite list is enough: the input directions and their images under the dynamics, applied up to one time less than the number of state variables. If these directions span the whole state space, every state can be reached. If they span less, the states the input can reach form exactly their span, whatever input and whatever time is used. Observability is the same test on the transposed system: the output must see every direction of the state.

## Proof

**Step 0: an invariant subspace.** By the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/), $A^n = -a_1 A^{n-1} - \dots - a_n I$, where $s^n + a_1 s^{n-1} + \dots + a_n$ is the characteristic polynomial of $A$. By induction on $k$, every $A^k B$ with $k \ge n$ is a linear combination of $B, AB, \dots, A^{n-1} B$. So the columns of $A^k B$ lie in $\operatorname{range} \mathcal{C}$ for every $k \ge 0$.

**Step 1: reachable states lie in $\operatorname{range} \mathcal{C}$.** With $x(0) = 0$, $x(T) = \int_0^T e^{A(T - s)} B u(s)\, ds$. The series $e^{A\tau} B = \sum_{k \ge 0} \frac{\tau^k}{k!} A^k B$ converges, and each term has its columns in $\operatorname{range} \mathcal{C}$ by Step 0. A subspace of $\mathbb{R}^n$ is closed, so $e^{A\tau} B u(s) \in \operatorname{range} \mathcal{C}$ for every $\tau$ and $s$, and so is the integral.

**Step 2: the gramian has the same range.** Let $W = \int_0^T e^{As} B B^T e^{A^T s} ds$, a symmetric matrix. If $v^T \mathcal{C} = 0$, then $v^T A^k B = 0$ for all $k$ by Step 0, so $v^T e^{As} B = 0$ for all $s$, and $W v = 0$. Conversely, if $W v = 0$, then

$$0 = v^T W v = \int_0^T \bigl| B^T e^{A^T s} v \bigr|^2 ds .$$

The integrand is continuous and nonnegative, so $v^T e^{As} B = 0$ for all $s \in [0, T]$. Differentiate $k$ times at $s = 0$: $v^T A^k B = 0$ for $k = 0, \dots, n - 1$, so $v^T \mathcal{C} = 0$. Hence $\ker W = \ker \mathcal{C}^T$. Since $W$ is symmetric, $\operatorname{range} W = (\ker W)^\perp = (\ker \mathcal{C}^T)^\perp = \operatorname{range} \mathcal{C}$.

**Step 3: every state of $\operatorname{range} \mathcal{C}$ is reachable.** Let $x_1 \in \operatorname{range} \mathcal{C} = \operatorname{range} W$, and pick $z$ with $W z = x_1$. The input $u(s) = B^T e^{A^T (T - s)} z$ gives, with the substitution $\sigma = T - s$,

$$x(T) = \int_0^T e^{A(T - s)} B B^T e^{A^T (T - s)} z\, ds = \int_0^T e^{A\sigma} B B^T e^{A^T \sigma} d\sigma\, z = W z = x_1 .$$

Steps 1 and 3 prove part 1.

**Part 2.** From $x(0) = x_0$ the state at time $T$ is $e^{AT} x_0 + r$ with $r$ in the reachable set of part 1. So $x_0$ can be steered to $x_1$ at time $T$ if and only if $x_1 - e^{AT} x_0 \in \operatorname{range} \mathcal{C}$. This holds for all $x_0, x_1$ if and only if $\operatorname{range} \mathcal{C} = \mathbb{R}^n$, that is, $\operatorname{rank} \mathcal{C} = n$. If the rank is less than $n$, it fails for every $T$, so no time helps.

**Parts 3 and 4.** If $\mathcal{O} x_0 = 0$, then $C A^k x_0 = 0$ for all $k$ by Step 0 applied to $A^T$ and $C^T$, so $C e^{At} x_0 = \sum_k \frac{t^k}{k!} C A^k x_0 = 0$. Conversely, if $C e^{At} x_0 = 0$ on $[0, T]$, differentiating $k$ times at $t = 0$ gives $C A^k x_0 = 0$ for $k = 0, \dots, n - 1$. So the set in part 3 is $\ker \mathcal{O}$. By the reduction on the [observability](/observability/) page, the system is observable if and only if this set is $\{0\}$, that is, if $\operatorname{rank} \mathcal{O} = n$.

**Discrete time.** By induction, $x_N = \sum_{k=0}^{N-1} A^{N-1-k} B u_k$ when $x_0 = 0$. As the $u_k$ vary over $\mathbb{R}^m$, these sums fill $\operatorname{range} [B, AB, \dots, A^{N-1} B]$, which equals $\operatorname{range} \mathcal{C}$ for $N \ge n$ by Step 0. With zero input, $y_k = C A^k x_0$ for $k = 0, \dots, N - 1$, and the stacked map $x_0 \mapsto (y_0, \dots, y_{N-1})$ has the same kernel as $\mathcal{O}$ for $N \ge n$, again by Step 0. $\blacksquare$

## Consequences

**Example.** For $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$ and $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $AB = \begin{bmatrix} 1 \\ -3 \end{bmatrix}$ and $\mathcal{C} = \begin{bmatrix} 0 & 1 \\ 1 & -3 \end{bmatrix}$ has determinant $-1$: the pair is controllable. With $C = [1, 1]$, $CA = [-2, -2]$ and $\mathcal{O} = \begin{bmatrix} 1 & 1 \\ -2 & -2 \end{bmatrix}$ has rank 1: the pair $(C, A)$ is not observable, and $\ker \mathcal{O}$ is spanned by $(1, -1)$.

**Invariance.** For an invertible $T$, the controllability matrix of $(T A T^{-1}, T B)$ is $T \mathcal{C}$, so the rank is a property of the system. For state feedback, $\operatorname{range}$ of the controllability matrix of $(A - BK, B)$ equals $\operatorname{range} \mathcal{C}$, so feedback neither creates nor destroys controllability.

**Fewer powers are enough with more inputs.** Let $r = \operatorname{rank} B$. Then $\operatorname{range} \mathcal{C} = \operatorname{range} [B, AB, \dots, A^{n-r} B]$. Proof: the subspaces $K_j = \operatorname{range} [B, \dots, A^j B]$ grow with $j$, and $K_{j+1} = \operatorname{range} B + A K_j$. If $K_j = K_{j+1}$, then $K_{j+2} = \operatorname{range} B + A K_{j+1} = \operatorname{range} B + A K_j = K_{j+1}$, so the sequence is constant from then on. The dimension starts at $r$ for $j = 0$, grows by at least one at each step before it stops, and cannot pass $n$, so it stops by $j = n - r$. For a controllable pair, the least $k$ with $\operatorname{rank} [B, AB, \dots, A^{k-1} B] = n$ is the *controllability index* of the pair (Chen 1999, Section 6.2.1).

**Controllability is generic.** The pair is uncontrollable exactly when every $n \times n$ minor of $\mathcal{C}$ vanishes. These minors are polynomials in the entries of $A$ and $B$, and at least one is not the zero polynomial: it is nonzero at the chain of integrators of the Tightness section, extended to dimension $n$ and with $e_n$ as the first column of $B$. So the uncontrollable pairs form a closed set with empty interior, and a perturbation of an uncontrollable pair by a random matrix with a density is controllable with probability 1. This is why a model that is "nearly uncontrollable" must be judged by a distance, not by a rank.

**Uses.** The single-input [Ackermann formula](/ackermann-formula/) inverts $\mathcal{C}$, and the [pole placement theorem](/pole-placement-theorem/) needs $\operatorname{rank} \mathcal{C} = n$. The range of $\mathcal{C}$ is the [Krylov subspace](/krylov-subspace/) of $A$ and $B$ of order $n$, and the [Kalman decomposition](/kalman-decomposition/) uses it as the first block of coordinates.

**Cost.** In the [real RAM](/real-ram/), forming $\mathcal{C}$ takes $n - 1$ products of $A$ with an $n \times m$ block, $O(n^3 m)$ operations, and its rank by [Gaussian elimination](/gaussian-elimination/) takes $O(n^3 m)$ more. With rational data and exact rational arithmetic the rank is exact.

**Numerical use: a pitfall.** In floating point the rank of $\mathcal{C}$ is a poor test (Paige 1981). The columns $A^k B$ turn toward the dominant eigenvector, as in [power iteration](/power-iteration/), so $\mathcal{C}$ is close to rank deficient even for systems far from any uncontrollable one. For $A = \operatorname{diag}(-1, -2, \dots, -n)$ and $B$ the vector of ones, the pair is controllable for every $n$ (distinct eigenvalues, and $B$ reaches each mode). In double precision, the [condition number](/condition-number/) of $\mathcal{C}$ is about $2.1 \times 10^{12}$ for $n = 10$ and about $4 \times 10^{19}$ for $n = 15$, and for $n = 15$ the usual rank tolerance (largest singular value times $n$ times the unit roundoff) gives rank 8. Yet at every eigenvalue $\lambda$ of $A$ the smallest singular value of $[A - \lambda I, B]$ stays above $0.46$. The robust measure is the distance to the nearest uncontrollable pair, $\min_{\lambda \in \mathbb{C}} \sigma_{\min} [A - \lambda I, B]$ (Eising 1984, Systems and Control Letters 4(5)). Software uses an orthogonal staircase reduction instead of $\mathcal{C}$.

## Tightness

The power $n - 1$ cannot be lowered in general. Take the single-input chain $A = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix}$ and $B = e_3$, a triple integrator. Then $AB = e_2$ and $A^2 B = e_1$, so $[B, AB]$ has rank 2 and only $[B, AB, A^2 B] = [e_3, e_2, e_1]$ has rank 3. The same holds in dimension $n$: with one input ($r = 1$) the bound $n - r = n - 1$ of the Consequences section is attained.

The test is for time-invariant systems. For $\dot x = A(t) x + B(t) u$ the pointwise rank of $[B(t), A(t) B(t), \dots]$ does not decide controllability; the test is the time-varying gramian on the [linear time-varying system](/linear-time-varying-system/) page.

## History

Kalman introduced controllability for linear systems in 1960 and tested it with the integral now called the [controllability gramian](/controllability-gramian/) (Kalman 1960). The rank form of the test appears in Kalman, Ho and Narendra (1963), together with the discrete-time case and the effect of sampling. Gilbert (1963) gave the test for systems with distinct eigenvalues in modal coordinates. Paige (1981) showed why the rank test fails as a numerical method and gave a numerically stable orthogonal algorithm.

## References
