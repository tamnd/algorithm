---
tag: MVMQPG
kind: algorithm
slug: maximal-positively-invariant-set
name: Maximal positively invariant set computation
aliases:
- Gilbert-Tan algorithm
- MPI set algorithm
area: control/optimal-and-predictive-control
level: advanced
summary: Computes the largest positively invariant set of x_(k+1) = A x_k inside polyhedral output limits by adding the limits of step t + 1 until a linear program shows they are redundant.
model: real-ram
complexity:
  vars: {n: the number of states, c: the number of rows of the output limits F y <= g, t: "the index at which the algorithm stops, the determinedness index", L: "the cost of one linear program in n variables with at most c (t + 1) rows"}
  time: {worst: "O(t (n^3 + c n^2 + c L))"}
  space: {extra: "O(c t n)"}
properties: {deterministic: true, exact: true, recursive: false, online: false}
history:
  year: 1991
  people: [Elmer G. Gilbert, K. T. Tan]
  note: "Gilbert and Tan (1991) defined the maximal output admissible set, proved that it is finitely determined under stability, observability and boundedness conditions, and computed it with linear programs."
prereqs: [positively-invariant-set, polyhedron, linear-programming-problem, observability]
see_also: [control-invariant-set, linear-mpc, mpc-stability-theorem, recursive-feasibility, simplex-method, reference-governor, fourier-motzkin-elimination, reachable-set-computation]
sources:
  - paper: doi:10.1109/9.83532
    title: Elmer G. Gilbert and K. T. Tan, Linear systems with state and control constraints, the theory and application of maximal output admissible sets, IEEE Transactions on Automatic Control 36(9), 1008-1020, 1991
    locator: the definition of the maximal output admissible set, the conditions for finite determination, and the algorithm that tests redundancy by linear programming
  - paper: doi:10.1016/S0005-1098(99)00113-2
    title: Franco Blanchini, Set invariance in control, Automatica 35(11), 1747-1767, 1999
    locator: the survey sections on polyhedral invariant sets for linear systems and their computation
  - book: isbn:9783319179322
    title: Franco Blanchini and Stefano Miani, Set-Theoretic Methods in Control, 2nd edition, Birkhäuser, 2015
    locator: the chapters on invariant sets and on the computation of polyhedral invariant sets
  - book: isbn:9781107016880
    title: Francesco Borrelli, Alberto Bemporad and Manfred Morari, Predictive Control for Linear and Hybrid Systems, Cambridge University Press, 2017
    locator: the chapter on invariant sets, with the algorithm for the maximal positive invariant set of an autonomous linear system
---

The maximal positively invariant set of the linear system $x_{k+1} = A x_k$ under the output limits $y_k = C x_k \in \mathbb{Y}$ is the set of all initial states whose whole trajectory meets the limits:

$$O_\infty = \{x : C A^k x \in \mathbb{Y} \text{ for all } k \ge 0\}.$$

It is the largest [positively invariant set](/positively-invariant-set/) inside $\{x : C x \in \mathbb{Y}\}$. Gilbert and Tan (1991) called it the maximal output admissible set. For a [polyhedron](/polyhedron/) $\mathbb{Y} = \{y : F y \le g\}$, the algorithm of this page adds the limits of steps $1, 2, \dots$ one block at a time and checks with one [linear program](/linear-programming-problem/) per row whether the new limits cut anything off. It stops at the first $t$ at which nothing is cut, and then $O_\infty = O_t$ is a polyhedron with a finite description. Gilbert and Tan proved that such a $t$ exists when $A$ is Schur, $(C, A)$ is [observable](/observability/), and $\mathbb{Y}$ is bounded with 0 in its interior. In MPC the set is the usual terminal set of [linear MPC](/linear-mpc/): $A$ is the closed loop $A - B K$ of the LQR gain, and $C$ stacks the state limits and the input $-K x$.

## In plain words

A system moves by itself under a fixed rule, and its outputs must stay inside some limits. Some starting points are safe forever. Others are inside the limits now but leave them later. This method finds all the safe starting points. It first keeps the points that meet the limits now. Then it adds the condition for one step later, then two steps later, and so on. After each new step it asks whether the new condition removes any point that is still in the set. When a new step removes nothing, every later step also removes nothing, so the set is final. Each check is a small optimization problem with a linear goal and linear limits.

## The problem

Input: $A \in \mathbb{R}^{n \times n}$, $C \in \mathbb{R}^{p \times n}$, and the output limits $F y \le g$ with $F \in \mathbb{R}^{c \times p}$ and $g \in \mathbb{R}^c$. Output: an index $t^*$ and a finite list of inequalities $H x \le h$ whose solution set is $O_\infty$, with

$$O_t = \{x : F C A^k x \le g \text{ for } k = 0, \dots, t\}, \qquad O_\infty = \bigcap_{t \ge 0} O_t.$$

The sets shrink: $O_0 \supseteq O_1 \supseteq \dots$. The set $O_\infty$ is finitely determined if $O_\infty = O_t$ for some finite $t$; the smallest such $t$ is the determinedness index $t^*$. The algorithm can only return a finite description, so it needs finite determination. For an MPC terminal set with the gain $K$, take $A_K = A - B K$ in place of $A$, the stacked output $C = \begin{bmatrix} I \\ -K \end{bmatrix}$ and the limits on states and inputs as $F y \le g$.

## The algorithm

```pseudo id=main
MPI(A, C, F, g)
L1   (rows, bounds) ← (F C, g)                         ▷ O_0 = {x : F C x ≤ g}
L2   for t = 0, 1, 2, ...
L3       R ← F C A^(t+1)                               ▷ the limits of step t + 1
L4       for each row r_i of R, with bound g_i
L5           v_i ← max r_i x subject to rows · x ≤ bounds   ▷ one LP; v_i = ∞ if unbounded
L6           if v_i > g_i then mark row i as new
L7       if no row is new then return (rows, bounds, t)   ▷ O_t = O_(t+1) = O_∞
L8       append the new rows to rows and bounds         ▷ the stored set is O_(t+1)
```

Line L5 asks how far the set $O_t$ reaches in the direction of the new row. If the answer is at most $g_i$, the row holds on all of $O_t$ and it is redundant. Only the rows that cut $O_t$ are stored, so the stored description is shorter than the full list of $c (t + 1)$ rows, and it still describes $O_{t+1}$, because the dropped rows hold on it. The implementation solves each LP with a two-phase [simplex method](/simplex-method/) with Bland's rule, in exact rational arithmetic for rational data. It stops with an error after a set number of passes, because without the hypotheses of finite determination the loop need not end. A last pass that removes redundant rows among the stored ones gives the facets of $O_\infty$.

## Example

**A damped rotation.** Let $A = s \begin{bmatrix} 3/5 & -4/5 \\ 4/5 & 3/5 \end{bmatrix}$, a rotation by $\theta = \arccos(3/5) \approx 53.13°$ scaled by $s$, with $C = I$ and the box $|x_1| \le 1$, $|x_2| \le 1$ ($c = 4$ rows). For $s = 9/10$:

- Line L1 stores the 4 rows of the box.
- Pass $t = 0$: the rows of $A$ are $(27/50, -18/25)$, $(18/25, 27/50)$ and their negatives. Each LP over the box gives $v = 63/50 > 1$, so all 4 rows are new.
- Pass $t = 1$: the rows of $A^2$ are $(-567/2500, -486/625)$, $(486/625, -567/2500)$ and their negatives. Each LP over the 8 rows gives $v = 369/400 < 1$. Nothing is new, so $t^* = 1$.

$O_\infty$ is the octagon with the vertices

$$(1, \tfrac{14}{27}),\ (\tfrac{23}{36}, 1),\ (-\tfrac{14}{27}, 1),\ (-1, \tfrac{23}{36}),\ (-1, -\tfrac{14}{27}),\ (-\tfrac{23}{36}, -1),\ (\tfrac{14}{27}, -1),\ (1, -\tfrac{23}{36}).$$

The vertex $(1, 14/27)$ lies on $x_1 = 1$ and on the new row $\tfrac{18}{25} x_1 + \tfrac{27}{50} x_2 = 1$: $0.72 + 0.28 = 1$. The tests check exactly, in fractions, that $A$ maps each vertex into the octagon.

Slower decay needs more passes (measurement with the implementation):

| $s$ | $t^*$ | facets of $O_\infty$ |
|---|---|---|
| 9/10 | 1 | 8 |
| 19/20 | 2 | 12 |
| 99/100 | 4 | 20 |

For $s = 1$ the loop never stops. The rotation keeps the length of $x$, and $\theta$ is not a rational multiple of $\pi$ (by Niven's theorem, the only rational values of $\cos$ at rational multiples of $\pi$ are $0$, $\pm 1/2$ and $\pm 1$). So every orbit on a circle of radius $r$ is dense on that circle, and $O_\infty$ is the closed unit disc. A disc is not a polyhedron, so no finite $t$ works.

**An unbounded first set.** Let $A = \begin{bmatrix} 1/2 & 1 \\ 0 & 1/2 \end{bmatrix}$, $C = \begin{bmatrix} 1 & 0 \end{bmatrix}$ and $|y| \le 1$. $O_0$ is the strip $|x_1| \le 1$, so the LP of pass 0 is unbounded and the row of step 1 is new. Because $(C, A)$ is observable, $O_1$ is bounded. The algorithm returns $t^* = 2$, and $O_\infty$ is the hexagon with the vertices $(1, 1/2)$, $(0, 1)$, $(-1, 5/4)$, $(-1, -1/2)$, $(0, -1)$ and $(1, -5/4)$.

**The terminal set of the linear MPC example.** For the double integrator $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$, $B = \begin{bmatrix} 0.5 \\ 1 \end{bmatrix}$ with the LQR gain $K = (0.434483, 1.028466)$ of $Q = I$, $R = 1$, take $A_K = A - B K$, the limits $|x_i| \le 5$ and $|K x| \le 1$ ($c = 6$). The algorithm stops at $t^* = 1$ with 8 stored rows, and the redundancy pass leaves 6 facets:

$$|x_1| \le 5, \qquad |0.434483\, x_1 + 1.028466\, x_2| \le 1, \qquad |0.106756\, x_1 - 0.181781\, x_2| \le 1.$$

The last pair is the input limit one step ahead, $|K A_K x| \le 1$. This is the terminal set used on the [linear MPC](/linear-mpc/) page.

## Correctness

The proofs are in proofs/correctness.md.

1. **$O_\infty$ is the maximal positively invariant set in $O_0$.** If $x \in O_\infty$, every limit of $A x$ is a limit of $x$ one step later, so $A x \in O_\infty$. If $S \subseteq O_0$ is positively invariant, every trajectory from $S$ stays in $S \subseteq O_0$, so $S \subseteq O_\infty$.
2. **The stopping test is correct.** The sets satisfy $O_{t+1} = \{x \in O_0 : A x \in O_t\}$. If $O_{t+1} = O_t$, then $O_{t+2} = \{x \in O_0 : A x \in O_{t+1}\} = O_{t+1}$, and by induction all later sets are equal, so $O_t = O_\infty$. The LP of line L5 decides $O_{t+1} = O_t$ row by row: the rows of step $t + 1$ hold on all of $O_t$ exactly when each maximum is at most its bound. An unbounded LP means the row cuts $O_t$.
3. **The loop ends under the hypotheses (theorem, Gilbert and Tan 1991).** Suppose $A$ is Schur, $(C, A)$ is observable, $\mathbb{Y}$ is bounded and contains a ball of radius $\rho > 0$ around 0. Observability and boundedness make $O_{n-1}$ bounded, say $|x| \le \beta$. Since $A^k \to 0$, there is $k_0$ with $\|C A^k\| \beta \le \rho$ for $k \ge k_0$, so all limits of later steps hold automatically on $O_{n-1}$. Hence $t^* \le \max(n - 1, k_0)$.
4. **The LP answers are exact.** The simplex method with Bland's rule does not cycle and stops with an optimum, an unbounded ray, or an infeasibility proof. With rational data the arithmetic is exact, so the comparison of line L6 has no rounding error.

The hypotheses of point 3 are sufficient, not necessary. The unbounded-strip example above has $0$ in the interior of $\mathbb{Y}$ but an unbounded $O_0$, and observability still bounds $O_1$.

## Complexity

Costs are in the [real-RAM model](/real-ram/).

- **One pass.** Line L3 costs $O(c n^2)$ if $F C A^{t}$ is kept and multiplied by $A$ once per pass (the implementation recomputes the power, which adds $O(n^3 \log t)$). Lines L4 to L6 solve $c$ linear programs in $n$ variables with at most $c (t + 1)$ rows.
- **All passes.** $t^* + 1$ passes give $O(t^* (n^3 + c n^2 + c L))$, with $L$ the cost of one LP. With the simplex method, $L$ has no polynomial bound in the worst case. An [interior point method](/interior-point-method/) is polynomial in the bit model, in the size of the LP and the bit length of the data; in the real-RAM model no strongly polynomial LP algorithm is known.
- **The index $t^*$.** It is not bounded by a function of $n$ and $c$ alone. The bound $\max(n - 1, k_0)$ grows as the spectral radius of $A$ tends to 1, and the table above shows the growth (measurement).
- **Space.** The stored rows number at most $c (t^* + 1)$, each of length $n$.

## Properties

- **Exact output.** In exact arithmetic the returned inequalities describe $O_\infty$ exactly. It is a polyhedron, and a polytope when it is bounded.
- **Convex and symmetric.** $O_\infty$ is convex because it is an intersection of half-spaces. If $\mathbb{Y}$ is symmetric about 0, so is $O_\infty$.
- **Contains a neighborhood of 0.** If $A$ is Schur and 0 is in the interior of $\mathbb{Y}$, then $O_\infty$ contains a ball around 0, because $|C A^k x| \le \sup_k \|C A^k\| \, |x|$ and the supremum is finite.
- **Monotone in the limits.** Larger limits give a larger set.
- **Redundant rows.** The stored list can contain rows that are redundant at the end. One LP per row removes them.

## Variants and improvements

- **Systems with inputs and a fixed gain.** The terminal set of MPC: apply the algorithm to $A - B K$ with the stacked output above.
- **Constant references.** For a reference governor, the state is augmented with a constant reference. The matrix then has an eigenvalue 1, the set is in general not finitely determined, and the limits are tightened by a small margin on the steady-state part to restore finite determination. See [reference governor](/reference-governor/).
- **Maximal control invariant set.** With a free input, iterate $\Omega_{t+1} = \{x \in \Omega_t : \exists u, \ A x + B u \in \Omega_t, \ u \in \mathbb{U}\}$. Each step needs a projection, for example by [Fourier-Motzkin elimination](/fourier-motzkin-elimination/), which is much more expensive. See [control-invariant set](/control-invariant-set/).
- **Disturbances.** For $x^+ = A x + w$ with $w$ in a polytope, tighten each limit of step $k$ by the support function of $C A^j w$ summed over $j < k$. The result is the maximal robust positively invariant set. Robust methods such as [tube MPC](/tube-mpc/) use sets of this kind.
- **Ellipsoidal sets.** A level set $\{x : x^T P x \le \gamma\}$ of a Lyapunov function, with $\gamma$ chosen so that it fits inside the limits, is positively invariant and simpler, but in general smaller than $O_\infty$.

## When to use it

Use it to compute the terminal set of [linear MPC](/linear-mpc/), to check that a fixed linear controller keeps a constraint for all time from a given state, or to build the admissible sets of a reference governor. It suits small $n$ and moderate $t^*$, where the number of LPs is small. For a large $n$, or a spectral radius close to 1, the number of rows can grow large; then use an ellipsoidal set or a simpler terminal constraint.

## Pitfalls

- **No finite determination.** If $A$ is not Schur, or $(C, A)$ is not observable, the loop may not end. Set a pass limit and report failure, as the implementation does. The rotation with $s = 1$ shows the case.
- **Rounding.** In floating point a row whose maximum is very close to its bound can be judged wrongly. Use a tolerance, and check the result by testing $A v$ for each vertex $v$ in two or three dimensions. Rational arithmetic avoids the problem for rational data.
- **Unbounded LPs.** When $\mathbb{Y}$ does not bound all states, $O_0$ is unbounded, and the LP of line L5 can be unbounded. Treat that answer as "the row is new", not as an error.
- **Not the terminal set by itself.** For MPC stability the terminal set must also go with a terminal cost that is a Lyapunov function for $A - B K$. The set alone does not give a decreasing cost. See [MPC stability theorem](/mpc-stability-theorem/).
- **The input limit.** For an MPC terminal set, include $|K x| \le u_{\max}$ in the output. Without it, the set does not ensure that $u = -K x$ meets the input limits.

## Implementations

## History

Gilbert and Tan (1991) defined the maximal output admissible set for linear systems with state and control limits, gave conditions for finite determination, and computed the set with linear programs. Blanchini (1999) surveyed set invariance in control, and the book of Blanchini and Miani covers polyhedral invariant sets and their computation. The book of Borrelli, Bemporad and Morari presents the same iteration as the standard way to compute the terminal set of linear MPC with polyhedral limits.

## References
