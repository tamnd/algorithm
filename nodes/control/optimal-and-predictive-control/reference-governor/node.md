---
tag: JN3QT7
kind: algorithm
slug: reference-governor
name: Reference governor
aliases:
- command governor
area: control/optimal-and-predictive-control
level: advanced
summary: An add-on that changes the reference of a closed loop with a Schur state matrix as little as needed so that constraints on the future response are never violated.
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of references, N: "the number of rows of the admissible set, at most q (t + 1) + q for q rows of the constraint and the index t at which the offline loop stops"}
  time: {worst: "O(N (n + m))"}
  space: {extra: "O(N (n + m))"}
properties: {deterministic: true, exact: true, recursive: false, online: true}
history:
  year: 1995
  people: [Elmer G. Gilbert, Ilya Kolmanovsky, Kok Tin Tan]
  note: "Gilbert, Kolmanovsky and Tan (1995) gave the discrete-time reference governor that scales the change of the reference by one number per step, using the maximal output admissible set of Gilbert and Tan (1991)."
prereqs: [maximal-positively-invariant-set, positively-invariant-set, linear-programming-problem, simplex-method]
see_also: [model-predictive-control, recursive-feasibility, anti-windup, linear-mpc, control-invariant-set, explicit-mpc, offset-free-mpc, input-to-state-stability]
sources:
  - paper: doi:10.1002/rnc.4590050508
    title: Elmer G. Gilbert, Ilya Kolmanovsky and Kok Tin Tan, Discrete-time reference governors and the nonlinear control of systems with state and control constraints, International Journal of Robust and Nonlinear Control 5(5), 487-504, 1995
    locator: the discrete-time reference governor for linear systems and the proofs of its properties
  - paper: doi:10.1109/9.83532
    title: Elmer G. Gilbert and Kok Tin Tan, Linear systems with state and control constraints, the theory and application of maximal output admissible sets, IEEE Transactions on Automatic Control 36(9), 1008-1020, 1991
    locator: the maximal output admissible set, its finite determination, and its computation by linear programs
  - paper: "Alberto Bemporad, Reference governor for constrained nonlinear systems, IEEE Transactions on Automatic Control 43(3), 415-419, 1998"
    locator: the reference governor for nonlinear systems, based on prediction of the future response
  - paper: doi:10.1016/j.automatica.2016.08.013
    title: Emanuele Garone, Stefano Di Cairano and Ilya Kolmanovsky, Reference and command governors for systems with constraints, a survey on theory and applications, Automatica 75, 306-328, 2017
    locator: the survey of scalar reference governors, command governors and their applications
---

A reference governor is an add-on to a control loop that already works well when no limit is active. It sits between the user and the loop and passes on a modified reference $v_k$ instead of the requested reference $r_k$. At each step it moves $v_k$ from its last value toward $r_k$ by the largest fraction $\kappa_k \in [0, 1]$ for which the future response, with $v$ held constant from now on, meets all constraints. The test uses a set of states and references computed offline by linear programs. The governor keeps the constraints for all time, and it reaches a constant reference that is strictly admissible in finitely many steps. The online work is one ratio per row of that set.

## In plain words

A good controller can still overshoot. If the operator asks for a big change at once, a valve can hit its limit or a temperature can go too high. The reference governor watches each request and asks one question: if I pass this request on and keep it fixed, will every future value stay within the limits? If yes, it passes the request on. If no, it passes on only part of the change, as much as is safe. The answer to the question comes from a list of simple linear checks prepared ahead of time. As the loop settles, more of the change becomes safe, and the full request goes through.

## The problem

Input: a discrete-time closed loop $x_{k+1} = A x_k + B v_k$, $y_k = C x_k + D v_k$ with $A$ Schur, a constraint $H y_k \le h$ with $h > 0$ that describes a bounded set, a margin $\varepsilon \in (0, 1)$, an initial pair $(x_0, v_{-1})$, and a reference sequence $r_0, r_1, \dots$. The steady state gain is $G_0 = C (I - A)^{-1} B + D$. Assume that $(C, A)$ is observable and $G_0$ has full column rank.

Output: a sequence $v_k = v_{k-1} + \kappa_k (r_k - v_{k-1})$ with $\kappa_k \in [0, 1]$ as large as possible, such that $H y_k \le h$ for all $k$.

**The admissible set.** With $v$ held constant from the state $x$, the output at time $t$ is $y_t(x, v) = C A^t x + (C S_t B + D) v$, with $S_t = I + A + \dots + A^{t-1}$. Let

$$O = \{(x, v) : H y_t(x, v) \le h \text{ for all } t \ge 0, \ H G_0 v \le (1 - \varepsilon) h\}.$$

Without the margin, the set is in general not finitely determined, because the pair $(x, v)$ has the dynamics $\mathrm{diag}(A, I)$ with eigenvalues 1. The margin $\varepsilon$ costs a little of the steady state range and makes $O$ a polyhedron with finitely many rows ([maximal positively invariant set](/maximal-positively-invariant-set/)).

## The algorithm

```pseudo id=main
REFERENCE-GOVERNOR(A, B, C, D, H, h, ε, x₀, v₋₁, r₀, r₁, ...)
L1   O ← {(x, v) : H G₀ v ≤ (1 - ε) h},  G₀ = C (I - A)⁻¹ B + D      ▷ steady state rows
L2   for t = 0, 1, 2, ... do                                       ▷ offline part
L3       R_t ← rows of H (C Aᵗ x + (C Sₜ B + D) v) ≤ h
L4       if every row of R_t is redundant in O (one LP per row) then stop
L5       O ← O ∩ R_t
L6   for k = 0, 1, 2, ... do                                       ▷ online part
L7       κ ← largest value in [0, 1] with (x_k, v_{k-1} + κ (r_k - v_{k-1})) ∈ O
L8       v_k ← v_{k-1} + κ (r_k - v_{k-1});  apply v_k;  x_{k+1} ← A x_k + B v_k
```

Lines L1 to L5 build $O$ once, as in the algorithm of Gilbert and Tan (1991). Line L4 checks a row $a^T z \le b$ by solving $\max\{a^T z : z \in O\}$; the row is redundant when the maximum is at most $b$. The code solves each LP by the [simplex method](/simplex-method/) on its dual, with Bland's rule. When all rows of one time step are redundant, the rows of all later steps are redundant too, so the loop stops.

Line L7 is cheap. Each row $a_x^T x + a_v^T v \le b$ becomes $\kappa \alpha \le \beta$ with $\alpha = a_v^T (r_k - v_{k-1})$ and $\beta = b - a_x^T x_k - a_v^T v_{k-1}$. Rows with $\alpha \le 0$ do not limit $\kappa$, and the others give $\kappa \le \beta / \alpha$. So $\kappa$ is the minimum of 1 and these ratios. Since $(x_k, v_{k-1})$ is in $O$, $\beta \ge 0$, and $\kappa = 0$ is always allowed.

## Example

Take the closed loop

$$A = \begin{bmatrix} 0 & 1 \\ -\tfrac12 & 1 \end{bmatrix}, \quad B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}, \quad C = \begin{bmatrix} \tfrac12 & 0 \end{bmatrix}, \quad D = 0.$$

The eigenvalues of $A$ are $\tfrac12 \pm \tfrac12 j$, of modulus $0.707$, so $A$ is Schur, and $G_0 = 1$. The response to a unit step of $v$ from rest is $y = 0, 0, 0.5, 1, 1.25, 1.25, 1.125, 1, 0.9375, \dots$, with a peak of 1.25.

Let the constraint be $|y| \le 1.1$ and $\varepsilon = 0.05$, so the steady state rows are $|v| \le 1.045$. In exact rational arithmetic, the offline loop adds the rows of $t = 0, \dots, 6$ and finds all rows of $t = 7$ redundant, so $O$ has 16 rows. For example, the row of $t = 4$ is $-\tfrac18 x_1 + \tfrac54 v \le 1.1$, which from rest is the peak $1.25\, v \le 1.1$.

Start at rest with $v_{-1} = 0$ and request $r = 1$. The governor gives:

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $\kappa_k$ | 0.88 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| $v_k$ | 0.88 | 0.88 | 0.88 | 0.88 | 1 | 1 | 1 | 1 | 1 |
| $y_k$ | 0 | 0 | 0.44 | 0.88 | 1.1 | 1.1 | 1.05 | 1 | 0.975 |

At $k = 0$ the row of $t = 4$ limits the step to $v = 1.1 / 1.25 = 0.88$. At $k = 4$ the full reference is safe, and $v$ jumps to 1. The output touches the limit 1.1 at $k = 4$ and $k = 5$ and never passes it, and then settles at 1. Without the governor the output would reach 1.25.

If the request is $r = 1.2$, which is beyond the steady state range, $v$ stops at $1.045$, the largest admissible steady state value, and the output stays within $\pm 1.1$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). One step with $v$ held maps $(x, v)$ to $(A x + B v, v)$, and the output at time $t$ from the new state is the output at time $t + 1$ from the old one. Hence the set $O_t$ of the rows up to time $t$ satisfies $O_t = O_0 \cap M^{-1}(O_{t-1})$, and once $O_t = O_{t-1}$, the set stays the same for all later $t$. Observability and the bounded constraint make $O_{n-1}$ bounded. Since $A$ is Schur, $y_t$ approaches $G_0 v$, which is at least $\varepsilon h$ inside the limits, so all rows beyond some time are redundant, and the offline loop stops. $O$ is invariant when $v$ is held, so $\kappa = 0$ is always feasible and $(x_k, v_k) \in O$ for all $k$, which gives $H y_k \le h$. For a constant reference $r$ with $H G_0 r \le (1 - \varepsilon) h$, the margin gives every state near a steady state a uniform amount of room, so $v_k$ reaches $r$ after finitely many steps.

## Complexity

The online step costs $O(N (n + m))$ for the $N$ rows of $O$: one inner product and one ratio per row. The offline part runs $t^* + 1$ rounds with $q$ LPs each, where $q$ is the number of rows of $H$; each LP has $n + m$ variables and at most $N$ rows. The proof bounds $t^*$ by the first $t$ with $\|C A^t\|$ below a constant times $\varepsilon$, which is of the order of $\log(1/\varepsilon) / \log(1/\rho(A))$ for the spectral radius $\rho(A)$; so $t^*$ grows when $\rho(A)$ is close to 1 or $\varepsilon$ is small. Memory is $O(N (n + m))$.

## Properties

- **Constraint satisfaction for all time,** for every reference sequence, if the loop starts in $O$, for example at rest at an admissible steady state.
- **Recursive feasibility.** $\kappa = 0$ is always allowed, so the governor never fails.
- **Finite-time convergence** to a constant reference $r$ with $H G_0 r \le (1 - \varepsilon) h$. For a constant reference outside this range, $v$ stops on the boundary of the admissible range.
- **No change to the loop.** If the reference is far from the limits, $\kappa = 1$ and the loop behaves as designed. The governor does not alter the stability or the robustness of the inner loop, since it only filters its reference.
- **Monotone in one direction.** For a constant reference, $v_k$ moves along a segment toward $r$ and never back.

## Variants and improvements

- **Command governor.** Choose $v_k$ freely in the admissible set, closest to $r_k$ in a quadratic norm, instead of on the segment. This needs a small QP per step instead of the ratio test.
- **Extended command governor.** Add a few free future corrections of $v$, which enlarges the admissible set at the cost of a larger QP.
- **Disturbances.** With a bounded additive disturbance, tighten each row by the worst case effect of the disturbance up to time $t$, as in [tube MPC](/tube-mpc/).
- **Nonlinear plants.** Bemporad (1998) checks admissibility by simulating the nonlinear response with $v$ held, instead of a precomputed set.
- **Explicit form.** Since $\kappa$ is a minimum of ratios, the map from $(x, v_{k-1}, r)$ to $v_k$ is piecewise rational and can be stored, but the online ratio test is already cheap.

## When to use it

Use a reference governor when a linear loop is already tuned for small signals, and the only problem is that large reference changes violate limits on the state or the input. It is much simpler than [MPC](/model-predictive-control/): the online step has no optimization, and it leaves the inner loop unchanged, so existing controllers and certifications stay valid. Use MPC instead when the limits are active most of the time, when performance near the limits matters, or when the plant is open-loop unstable without a stabilizing inner loop. For an integrator in the loop that winds up during saturation, [anti-windup](/anti-windup/) is the simpler fix.

## Pitfalls

- **Forgetting the margin.** With $\varepsilon = 0$ the admissible set has infinitely many rows in general, and the offline loop does not stop.
- **Starting outside the set.** The guarantees need $(x_0, v_{-1}) \in O$. A loop that starts far from a steady state may need $v_{-1}$ chosen to match the state, or a check before switching on.
- **A slow loop.** If $A$ has eigenvalues near the unit circle, $t^*$ and the number of rows grow large. Remove redundant rows, or use a larger $\varepsilon$.
- **Model errors.** The guarantee is only for the model. Unmodeled dynamics or disturbances can push the output over the limit; add a disturbance tightening, or keep a margin in $h$.
- **Rounding.** With floating point, a row can be violated by a rounding error, and $\beta$ can come out slightly negative. Clip $\kappa$ to 0 in that case, as the code does.

## Implementations

## History

Gilbert and Tan (1991) defined the maximal output admissible set of a linear system, showed when it is finitely determined, and computed it by linear programs. Gilbert, Kolmanovsky and Tan (1995) applied it to the state together with a constant reference to build the discrete-time reference governor with one scalar per step and proved constraint satisfaction and finite-time convergence. Bemporad (1998) extended the idea to nonlinear systems. Later work added command governors with a free choice of $v$, robust versions for disturbances, and many applications in automotive and aerospace control, which Garone, Di Cairano and Kolmanovsky (2017) survey.

## References
