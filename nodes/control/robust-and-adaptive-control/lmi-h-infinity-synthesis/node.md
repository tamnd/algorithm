---
tag: HWW5GT
kind: algorithm
slug: lmi-h-infinity-synthesis
name: LMI-based H-infinity synthesis
aliases:
- Gahinet-Apkarian synthesis
area: control/robust-and-adaptive-control
level: research
summary: Solves the H-infinity problem by linear matrix inequalities with no regularity assumptions, and builds the controller from their solution.
solves: [h-infinity-control-problem]
model: real-ram
complexity:
  vars: {n: the number of plant states, m: the number of inputs w and u together, p: the number of outputs z and y together, k: the number of Newton steps of the barrier method}
  time: {per-newton-step: "O(n^2 (n + m + p)^3 + n^4 (n + m + p)^2)", total: "O(k (n^2 (n + m + p)^3 + n^4 (n + m + p)^2))"}
  space: {extra: "O(n^4 + n^2 (n + m + p)^2)"}
properties: {deterministic: true, exact: false, recursive: false, iterative: true}
history:
  year: 1994
  people: [Pascal Gahinet, Pierre Apkarian, Tetsuya Iwasaki, Robert E. Skelton]
  note: "Gahinet and Apkarian (1994) and Iwasaki and Skelton (1994) independently reduced H-infinity synthesis to three LMIs in two symmetric matrices, with no rank conditions on the plant."
prereqs: [h-infinity-control-problem, bounded-real-lemma, linear-matrix-inequality, semidefinite-programming]
see_also: [dgkf-h-infinity-synthesis, interior-point-method, barrier-method, schur-complement, linear-fractional-transformation, mixed-sensitivity-design, dk-iteration, lpv-system]
sources:
  - paper: doi:10.1002/rnc.4590040403
    title: Pascal Gahinet and Pierre Apkarian, A linear matrix inequality approach to H-infinity control, International Journal of Robust and Nonlinear Control 4(4), 421-448, 1994
    locator: the projected LMIs in R and S, the coupling LMI, and the construction of the controller from a solution
  - paper: doi:10.1016/0005-1098(94)90110-4
    title: Tetsuya Iwasaki and Robert E. Skelton, All controllers for the general H-infinity control problem, LMI existence conditions and state space formulas, Automatica 30(8), 1307-1317, 1994
    locator: the same existence conditions, derived independently, and the set of all controllers
  - paper: doi:10.1109/9.599969
    title: Carsten Scherer, Pascal Gahinet and Mahmoud Chilali, Multiobjective output-feedback control via LMI optimization, IEEE Transactions on Automatic Control 42(7), 896-911, 1997
    locator: the change of variables that makes synthesis LMIs linear with several objectives and pole region constraints
  - book: doi:10.1137/1.9781611970777
    title: Stephen Boyd, Laurent El Ghaoui, Eric Feron and Venkataramanan Balakrishnan, Linear Matrix Inequalities in System and Control Theory, SIAM, 1994
    locator: the bounded real lemma as an LMI, interior point methods for LMI problems, and state feedback synthesis by LMIs
  - paper: doi:10.1016/0005-1098(96)00033-7
    title: Pascal Gahinet, Explicit controller formulas for LMI-based H-infinity synthesis, Automatica 32(7), 1007-1014, 1996
    locator: closed formulas for a controller from a solution R, S of the synthesis LMIs
  - paper: doi:10.1016/0005-1098(95)00038-X
    title: Pierre Apkarian, Pascal Gahinet and Greg Becker, Self-scheduled H-infinity control of linear parameter-varying systems, a design example, Automatica 31(9), 1251-1261, 1995
    locator: the LMI synthesis conditions extended to gain-scheduled controllers for LPV plants
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Chapter 11, Interior-point methods (the barrier method, phase I and its complexity analysis)
---

LMI-based H-infinity synthesis, also called Gahinet-Apkarian synthesis, solves the [H-infinity control problem](/h-infinity-control-problem/) as a [semidefinite program](/semidefinite-programming/). An output feedback controller of the same order as the plant with closed loop H-infinity norm below $\gamma$ exists if and only if two symmetric $n \times n$ matrices $R$ and $S$ satisfy three [linear matrix inequalities](/linear-matrix-inequality/). The inequalities are linear in $R$, $S$ and $\gamma$ together, so the smallest $\gamma$ is the optimum of a convex program, with no bisection on $\gamma$. A second LMI then gives the controller. Unlike the [two-Riccati method](/dgkf-h-infinity-synthesis/), the LMI method needs no rank or normalization assumptions on $D_{12}$ and $D_{21}$ and no condition on zeros on the imaginary axis. It also takes extra convex constraints, such as pole regions or bounds on other closed loop norms. The price is speed: the SDP has about $n^2$ variables, so it is much slower than solving two Riccati equations.

## In plain words

The [bounded real lemma](/bounded-real-lemma/) says that a system has gain below $\gamma$ if and only if a certain matrix inequality has a positive definite solution. For a closed loop, that inequality has products of the unknown controller and the unknown Lyapunov matrix, so it is not convex. Gahinet and Apkarian showed that you can remove the controller from the problem. What is left is three inequalities in two matrices, and they are linear. A convex solver finds the best $\gamma$ and the two matrices. From them you build the closed loop Lyapunov matrix, and then the controller is the solution of one more linear inequality.

## The problem

The generalized plant is

$$\dot x = A x + B_1 w + B_2 u, \qquad z = C_1 x + D_{11} w + D_{12} u, \qquad y = C_2 x + D_{21} w,$$

with $x \in \mathbb{R}^n$, $w \in \mathbb{R}^{m_1}$, $u \in \mathbb{R}^{m_2}$, $z \in \mathbb{R}^{p_1}$ and $y \in \mathbb{R}^{p_2}$. The only assumptions are that $(A, B_2)$ is [stabilizable](/stabilizability/), $(C_2, A)$ is [detectable](/detectability/) and $D_{22} = 0$. A nonzero $D_{22}$ is removed by a change of the controller. As on the two-Riccati page the loop is closed by $u = K y$, the lower [linear fractional transformation](/linear-fractional-transformation/), with $K = (A_K, B_K, C_K, D_K)$.

Let the columns of $N_R$ be a basis of the kernel of $[B_2^T \ D_{12}^T]$ and those of $N_S$ a basis of the kernel of $[C_2 \ D_{21}]$.

**Theorem** (Gahinet and Apkarian 1994; Iwasaki and Skelton 1994). There is an internally stabilizing controller of order $n$ with $\|T_{zw}\|_\infty < \gamma$ if and only if there are symmetric $R$ and $S$ with

$$\begin{bmatrix} N_R & 0 \\ 0 & I \end{bmatrix}^T \begin{bmatrix} A R + R A^T & R C_1^T & B_1 \\ C_1 R & -\gamma I & D_{11} \\ B_1^T & D_{11}^T & -\gamma I \end{bmatrix} \begin{bmatrix} N_R & 0 \\ 0 & I \end{bmatrix} < 0,$$

$$\begin{bmatrix} N_S & 0 \\ 0 & I \end{bmatrix}^T \begin{bmatrix} A^T S + S A & S B_1 & C_1^T \\ B_1^T S & -\gamma I & D_{11}^T \\ C_1 & D_{11} & -\gamma I \end{bmatrix} \begin{bmatrix} N_S & 0 \\ 0 & I \end{bmatrix} < 0, \qquad \begin{bmatrix} R & I \\ I & S \end{bmatrix} \ge 0.$$

If the third LMI holds with rank $n + r$, a controller of order $r$ exists, so controllers of order above $n$ give nothing new. A controller of any order with norm below $\gamma$ exists if and only if one of order $n$ does.

## The algorithm

```pseudo id=main
LMI-SYNTHESIS(A, B1, B2, C1, C2, D11, D12, D21, delta)
L1  N_R ← basis of ker [B2^T D12^T],  N_S ← basis of ker [C2 D21]
L2  γ* ← min γ over R, S, γ subject to LMI_R < 0, LMI_S < 0, [R I; I S] > 0
L3  γ ← (1 + delta) γ*
L4  (R, S) ← analytic center of the three LMIs with γ fixed
L5  N ← I - S R                                ▷ M = I
L6  X_cl ← [S N; N^T R S R - R]
L7  Ω ← a point with BRL(A_cl(Ω), B_cl(Ω), C_cl(Ω), D_cl(Ω), X_cl, γ) < 0
L8  return γ*, K = (A_K, B_K, C_K, D_K) read from Ω = [A_K B_K; C_K D_K]

BARRIER(c, G_1, ..., G_q, x)                   ▷ min c^T x subject to G_i(x) > 0
L9  x ← phase I: min s subject to G_i(x) + s I > 0, stop when s < 0
L10 repeat  x ← argmin of t c^T x - Σ log det G_i(x), by Newton steps from x
L11         t ← 8 t  until (Σ sizes of the G_i) / t < eps
```

**Line L2** is an SDP in the $n(n + 1) + 1$ entries of $R$, $S$ and $\gamma$. Its blocks have sizes $(n + p_1 - m_2) + m_1$, $(n + m_1 - p_2) + p_1$ and $2n$ when $D_{12}$ has full column rank and $D_{21}$ full row rank. The code also adds the scalar constraint $\mathrm{tr}\,R + \mathrm{tr}\,S + \gamma < 1000$, which keeps every SDP bounded.

**Lines L5 and L6** build a closed loop Lyapunov matrix with $(X_{\rm cl})_{11} = S$ and $(X_{\rm cl}^{-1})_{11} = R$. With $M = I$ and $N = I - SR$, the matrix is $X_{\rm cl} = \begin{bmatrix} S & N \\ N^T & RSR - R \end{bmatrix}$. It is positive definite because the third LMI holds strictly at the analytic center.

**Line L7.** With the closed loop matrices

$$A_{\rm cl} = \begin{bmatrix} A + B_2 D_K C_2 & B_2 C_K \\ B_K C_2 & A_K \end{bmatrix}, \quad B_{\rm cl} = \begin{bmatrix} B_1 + B_2 D_K D_{21} \\ B_K D_{21} \end{bmatrix},$$

$$C_{\rm cl} = \begin{bmatrix} C_1 + D_{12} D_K C_2 & D_{12} C_K \end{bmatrix}, \quad D_{\rm cl} = D_{11} + D_{12} D_K D_{21},$$

each of which is affine in $\Omega$, the bounded real LMI

$$\begin{bmatrix} A_{\rm cl}^T X_{\rm cl} + X_{\rm cl} A_{\rm cl} & X_{\rm cl} B_{\rm cl} & C_{\rm cl}^T \\ B_{\rm cl}^T X_{\rm cl} & -\gamma I & D_{\rm cl}^T \\ C_{\rm cl} & D_{\rm cl} & -\gamma I \end{bmatrix} < 0$$

is an LMI in $\Omega$ alone. The code solves it with a bound on the Frobenius norm of $\Omega$, written as an LMI by a [Schur complement](/schur-complement/), and takes its analytic center.

**The SDP solver.** The code uses the [barrier method](/barrier-method/): Newton's method with a backtracking line search on $t c^T x - \sum_i \log\det G_i(x)$, with the Cholesky factor of each $G_i$ to test feasibility and to get $\log\det$. Phase I starts from $R = S = I$ and a large slack $s$. When $s$ stays positive and the gap bound $(\sum \text{sizes})/t$ shows that the minimum of $s$ is positive, the LMIs are infeasible. A production code uses a primal-dual [interior point method](/interior-point-method/) instead.

## Example

Take the scalar plant of the two-Riccati page with $a = 1$: $\dot x = x + w_1 + u$, $z = (x, u)$, $y = x + w_2$. The kernel of $[B_2^T \ D_{12}^T] = [1, 0, 1]$ is spanned by $(0, 1, 0)$ and $(1, 0, -1)/\sqrt 2$. The first LMI becomes the $4 \times 4$ inequality

$$\begin{bmatrix} -\gamma & R/\sqrt 2 & 0 & 0 \\ R/\sqrt 2 & a R - \gamma/2 & 1/\sqrt 2 & 0 \\ 0 & 1/\sqrt 2 & -\gamma & 0 \\ 0 & 0 & 0 & -\gamma \end{bmatrix} < 0.$$

By a Schur complement on the two $-\gamma$ entries next to the middle, it is equivalent to $R^2 + 2 a \gamma R + 1 < \gamma^2$. The plant is its own dual, so the second LMI is $S^2 + 2 a \gamma S + 1 < \gamma^2$. The third LMI needs $R > 0$, $S > 0$ and $RS \ge 1$.

At $\gamma = 3$ the first inequality is $R^2 + 6R - 8 < 0$, that is $R < \sqrt{17} - 3 = 1.12311$, and $R = S = 1$ satisfies all three LMIs. At $\gamma = 2.7$ it gives $R < 0.98511$ and the same for $S$, so $RS < 1$ and the LMIs are infeasible. The boundary is at $R = S = 1$: $2 + 2\gamma = \gamma^2$, so $\gamma_{\rm opt} = 1 + \sqrt 3 = 2.73205$, the same value as the two-Riccati method.

The barrier code returns $\gamma^* = 2.7320508079$ (error $3.5 \times 10^{-10}$) with $R = S = 1.0000000001$. At $\gamma = 1.05\,\gamma^* = 2.86865$ the analytic center is $R = S = 1.02124$, and line L7 gives

$$K(s) = -0.02754 - \frac{187.830}{s + 71.597}, \qquad K(0) = -2.65097.$$

The closed loop poles are $-68.909$ and $-1.715$, and a frequency sweep gives the peak $2.78746 < 2.86865$. This controller differs from the central controller of the two-Riccati method: the LMI method gives some controller that meets the level, not a particular one.

## Correctness

The theorem is cited; the proof in Gahinet and Apkarian (1994) goes as follows. By the bounded real lemma, a controller meets the level if and only if some $X_{\rm cl} > 0$ satisfies the closed loop LMI. That LMI has the form $\Psi + P^T \Omega^T Q + Q^T \Omega P < 0$ with $\Psi$, $P$ and $Q$ fixed by $X_{\rm cl}$. The elimination lemma (also called the projection lemma) says such an $\Omega$ exists if and only if $\Psi$ is negative definite on the kernels of $P$ and $Q$. Written out, these two conditions are the first two LMIs with $S = (X_{\rm cl})_{11}$ and $R = (X_{\rm cl}^{-1})_{11}$. The third LMI says exactly when such $R$ and $S$ come from one $X_{\rm cl} > 0$ of size $2n$.

Given the theorem, the code is correct when each SDP is solved to its tolerance: line L2 finds $\gamma^*$ within $10^{-8}$ in the barrier gap, lines L4 to L6 give an $X_{\rm cl} > 0$ with the right blocks, and by the elimination lemma the LMI of line L7 is feasible, so the barrier method finds an $\Omega$. The proof file [proofs/correctness.md](proofs/correctness.md) shows the block identities of $X_{\rm cl}$, that the closed loop matrices are affine in $\Omega$ as written, that the barrier step keeps every iterate strictly feasible, and the scalar reduction of the example.

## Complexity

Let $v = n(n + 1) + 1$ be the number of SDP variables and $d \le 2(n + m + p)$ the largest block size. One Newton step forms $G_i^{-1} G_{ij}$ for all variables in $O(v d^3)$, the Hessian entries $\mathrm{tr}(G_i^{-1} G_{ij} G_i^{-1} G_{ik})$ in $O(v^2 d^2)$, and solves the Newton system in $O(v^3)$. With $v = \Theta(n^2)$ this is $O(n^2 (n + m + p)^3 + n^4 (n + m + p)^2)$ per Newton step, in the real-RAM model.

The number $k$ of Newton steps is a separate result. For the barrier method on a bounded problem with a strictly feasible start, the self-concordance analysis bounds the Newton steps per centering by a constant plus a term in the change of $t$, and the number of centerings by $O(\log(d_{\rm tot} / (t_0 \varepsilon)))$, where $d_{\rm tot}$ is the sum of block sizes (Boyd and Vandenberghe 2004, chapter 11). Short-step path following methods need $O(\sqrt{d_{\rm tot}} \log(1/\varepsilon))$ Newton steps. These are polynomial bounds only under those assumptions: a fixed accuracy $\varepsilon$, strict feasibility and a bound on the feasible set. In exact terms the problem of deciding feasibility of an LMI is not known to be in polynomial time. As a measurement, the code needs 50 Newton steps (phase I included) to minimize $\gamma$ for the scalar example and 293 for the test plant with two states, and 42 and 87 steps for the controller part.

The second SDP, line L7, has $(n + m_2)(n + p_2)$ variables and one block of size $2n + m_1 + p_1$, so its cost has the same order.

## Properties

- No rank assumptions: the method handles singular problems where $D_{12}$ or $D_{21}$ loses rank, or where the plant has zeros on the imaginary axis. Then $\gamma_{\rm opt}$ is often an infimum that no controller reaches, and the LMI solution grows without bound as $\gamma \to \gamma_{\rm opt}$.
- Convex in $\gamma$: the optimum is found directly, not by bisection.
- Extra constraints that are LMIs in $R$ and $S$ can be added, such as pole regions or an H2 bound on another channel (Scherer, Gahinet and Chilali 1997). With several objectives the common Lyapunov matrix makes the result conservative; that is a theorem about sufficiency, not an exact condition.
- The controller has order $n$, or order $r < n$ if the coupling LMI holds with rank $n + r$.
- The result depends on the solver: different SDP solutions give different valid controllers.

## Variants and improvements

- **Change of variables.** Scherer, Gahinet and Chilali (1997) use a nonlinear change of the controller variables that makes the synthesis inequality linear in all unknowns at once. The controller then comes from a linear system, not from a second SDP.
- **Explicit controller formulas.** Gahinet (1996) gave closed formulas for a controller from $R$ and $S$, which avoid the second SDP.
- **Reduced order.** Requiring rank $[R \ I; I \ S] \le n + r$ gives a controller of order $r$. The rank constraint is not convex, and the fixed-order problem is NP-hard in general (see the [problem page](/h-infinity-control-problem/)).
- **Parameter-dependent plants.** The same projection idea gives gain-scheduled controllers for [LPV systems](/lpv-system/) (Apkarian, Gahinet and Becker 1995).
- **Discrete time.** The discrete bounded real lemma gives similar LMIs.

## When to use it

Use it when the plant breaks the assumptions of the two-Riccati method, when you need extra convex constraints, or when the problem is a building block in a larger LMI design such as gain scheduling. For a plain H-infinity problem that meets the assumptions, the Riccati method is faster by a large factor and more accurate. Use a good SDP solver; the barrier code here is only for plants with a few states.

## Pitfalls

- **Strict versus non-strict.** SDP solvers return points on the boundary of the feasible set. At the optimum, $[R \ I; I \ S]$ is singular and the reconstruction of $X_{\rm cl}$ fails, so back off from $\gamma^*$ and re-center, as in lines L3 and L4.
- **Ill conditioning.** Near the optimum, or in singular problems, $R$ or $S$ can be huge, and the controller then has very fast poles. In the singular test problem of the code the optimum is 1 and the bound $\mathrm{tr}\,R + \mathrm{tr}\,S + \gamma < 1000$ is active.
- **Scaling.** Scale the plant before solving. Interior point solvers lose accuracy when the entries of the LMIs span many orders of magnitude.
- **Verification.** Check the result: compute the closed loop poles and the H-infinity norm of the closed loop with a reliable [norm computation](/h-infinity-norm-computation/). A small solver error can give a controller with a norm slightly above $\gamma$.

## Implementations

## History

The bounded real lemma and its LMI form were known from the 1970s, and LMIs for state feedback were in use by the late 1980s (Boyd, El Ghaoui, Feron and Balakrishnan 1994). In 1994, Gahinet and Apkarian and, independently, Iwasaki and Skelton reduced output feedback H-infinity synthesis to LMIs in two matrices. Packard (1994) and Apkarian, Gahinet and Becker (1995) used the same ideas for gain scheduling. Scherer, Gahinet and Chilali (1997) extended the approach to several objectives at once. Efficient interior point solvers for SDPs, from the work of Nesterov and Nemirovskii, made these results practical.

## References
