---
tag: WR4Z1J
kind: theorem
slug: bakushinskii-veto
name: Bakushinskii veto
aliases:
- Bakushinskii theorem
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: advanced
summary: "If a regularization method with a rule alpha(y^delta) that ignores the noise level converges for all data and all noise, then A^dagger is bounded. So such rules fail in the worst case."
prereqs: [regularization-method, pseudoinverse, well-posed-problem]
see_also: [morozov-discrepancy-principle, generalized-cross-validation, l-curve-method, quasi-optimality-criterion, lepskii-balancing-principle, regularization-parameter-choice, tikhonov-convergence-rates, semi-convergence]
sources:
  - paper: "A. B. Bakushinskii, Remarks on choosing a regularization parameter using the quasi-optimality and ratio criterion, USSR Computational Mathematics and Mathematical Physics 24(4), 1984, 181 to 182"
    locator: the whole note (general locator)
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 3, Regularization Operators (the theorem that a convergent method with a parameter choice that does not depend on delta forces A^dagger to be bounded)
  - paper: "S. Kindermann, Convergence analysis of minimization-based noise level-free parameter choice rules for linear ill-posed problems, Electronic Transactions on Numerical Analysis 38, 2011, 233 to 257"
    locator: noise conditions under which heuristic rules converge (general locator)
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: the chapter on parameter choice methods (general locator)
---

The Bakushinskii veto says that a parameter choice rule which does not use the noise level cannot make a regularization method converge for every ill-posed problem in the worst case. Precisely: if a method computes its answer from the data $y^\delta$ alone, with a rule $\alpha = \alpha(y^\delta)$ that does not know $\delta$, and the answer tends to the true solution for every exact $y$ and every noise with $\|y^\delta - y\| \le \delta$ as $\delta \to 0$, then the pseudoinverse $A^\dagger$ is bounded, so the problem was well posed after all. The proof is three lines and uses nothing about the method, so it covers Tikhonov regularization, truncated SVD, stopped [Landweber](/landweber-iteration/) and [CGLS](/cgls/) iterations and every other method. It is the reason why the theory insists on rules such as the [discrepancy principle](/morozov-discrepancy-principle/), and why [GCV](/generalized-cross-validation/), the [L-curve](/l-curve-method/) and the [quasi-optimality criterion](/quasi-optimality-criterion/) are called heuristic. It is a worst-case statement: heuristic rules can and do converge when the noise is restricted (Kindermann 2011).

## Statement

**Setting.** $A: X \to Y$ is a bounded linear operator between Hilbert spaces. $A^\dagger$ is its Moore-Penrose [pseudoinverse](/pseudoinverse/), defined on the dense subspace $D(A^\dagger) = R(A) + R(A)^\perp$ of $Y$. $A^\dagger$ is bounded if and only if $R(A)$ is closed; otherwise the problem $A x = y$ is ill posed (see [well-posed problem](/well-posed-problem/)).

A method with a noise-free rule is a map $R: Y \to X$. Typically $R(y^\delta) = R_{\alpha(y^\delta)}\, y^\delta$ for a family of regularization operators $R_\alpha$ and a parameter choice $\alpha(y^\delta)$ that depends only on the data. The family and the rule may be nonlinear; $R$ need not be continuous.

**Theorem (Bakushinskii 1984; EHN Chapter 3).** Suppose that for every $y \in D(A^\dagger)$,
$$\lim_{\delta \to 0}\ \sup \{ \|R(y^\delta) - A^\dagger y\| : y^\delta \in D(A^\dagger),\ \|y^\delta - y\| \le \delta \} = 0 .$$
Then $A^\dagger$ is bounded.

Equivalently: if $R(A)$ is not closed, then for every noise-free rule there are $y \in D(A^\dagger)$, $\varepsilon > 0$ and data $y_n$ with $\|y_n - y\| \to 0$ but $\|R(y_n) - A^\dagger y\| \ge \varepsilon$ for all $n$.

## In plain words

Suppose a method sees only the data, not how noisy they are. Then exact data for one solution and noisy data for another solution can be the same numbers, and the method must give the same answer for both. For a well-posed problem this is harmless, because two solutions with almost the same data are almost the same. For an ill-posed problem they can be far apart, so the method is wrong for one of them. Making the noise smaller does not help, because one can always find a pair of solutions that are far apart and whose data differ by less than the noise. So a reliable rule must know the noise level, or must assume something about the noise.

## Proof

Write $s_y(\delta)$ for the supremum in the hypothesis, so $s_y(\delta) \to 0$ as $\delta \to 0$ for every $y \in D(A^\dagger)$.

**Step 1: $R = A^\dagger$ on $D(A^\dagger)$.** Fix $y \in D(A^\dagger)$. For every $\delta > 0$ the data $y^\delta = y$ are admissible, so $\|R(y) - A^\dagger y\| \le s_y(\delta)$. Let $\delta \to 0$: $R(y) = A^\dagger y$.

**Step 2: $A^\dagger$ is continuous on $D(A^\dagger)$.** Let $y_n \to y$ with $y_n, y \in D(A^\dagger)$, and put $\delta_n = \|y_n - y\|$. Then $y_n$ is admissible data for $y$ with noise level $\delta_n$, and by step 1,
$$\|A^\dagger y_n - A^\dagger y\| = \|R(y_n) - A^\dagger y\| \le s_y(\delta_n) \to 0 .$$

**Step 3: $A^\dagger$ is bounded.** $A^\dagger$ is linear on the subspace $D(A^\dagger)$, and by step 2 it is continuous at $0$. A linear map that is continuous at $0$ is bounded. $\square$

The proof never uses how $R$ is built. It only uses that $R$ gives one answer for one set of data, whatever the noise level was.

## Consequences

**A small example.** Let $A = \mathrm{diag}(1, 0.01)$ and $y^\delta = (1, 0.01)$. These data fit two situations. In situation A they are exact data for $x = (1, 1)$, with $\delta = 0$. In situation B they are data for $x^\dagger = (1, 0)$ with noise $(0, 0.01)$, so $\delta = 0.01$. A rule $\alpha(y^\delta)$ must give the same $\alpha$ in both. Tikhonov regularization gives $x_\alpha = (1/(1 + \alpha),\ 10^{-4}/(10^{-4} + \alpha))$:

| $\alpha$ | $x_\alpha$ | error in situation A | error in situation B |
|---|---|---|---|
| $10^{-6}$ | $(0.999999, 0.990099)$ | 0.0099 | 0.9901 |
| $10^{-4}$ | $(0.999900, 0.500000)$ | 0.5000 | 0.5000 |
| $10^{-2}$ | $(0.990099, 0.009901)$ | 0.9901 | 0.0140 |

The two errors add up to at least $\|(1,1) - (1,0)\| = 1$ for every $\alpha$, by the triangle inequality, so one of them is at least $1/2$. A rule that knows $\delta$ picks a small $\alpha$ in A and a large one in B. Replace $0.01$ by a smaller singular value $\sigma$, both in $A$ and in the data. Then situation B has noise level $\delta = \sigma$, and one of the two errors is still at least $1/2$. In this finite example $A^\dagger$ is bounded, with $\|A^\dagger\| = 100$. For a compact operator with infinitely many nonzero singular values, $\sigma_n \to 0$ gives such pairs for noise levels that tend to 0, which is the theorem.

**For practice.**

- Every convergent regularization method for an ill-posed problem needs $\delta$ or some other information beyond $y^\delta$. The [discrepancy principle](/morozov-discrepancy-principle/) and the [Lepskii principle](/lepskii-balancing-principle/) use $\delta$.
- [GCV](/generalized-cross-validation/), the [L-curve](/l-curve-method/), the [quasi-optimality criterion](/quasi-optimality-criterion/) and the Hanke-Raus rule do not use $\delta$, so for each of them there is noise that makes it fail. They are still used, often with success, because real noise is rarely the worst case.
- Stopping an iteration such as [Landweber](/landweber-iteration/), [CGLS](/cgls/) or [LSQR](/lsqr/) at an index chosen from the data alone falls under the theorem too. The [semi-convergence](/semi-convergence/) of these methods makes a stopping rule necessary, and the veto says that rule must use $\delta$ to be safe.
- For random noise the setting changes: white noise does not have a finite norm in infinite dimensions, and statements about GCV and similar rules are made in expectation or with high probability. The veto is about deterministic noise with $\|y^\delta - y\| \le \delta$.

## Tightness

- **The conclusion is sharp.** If $A^\dagger$ is bounded, the rule "no regularization", $R = A^\dagger$ extended to $Y$ by $A^\dagger P$ with $P$ the projection onto $\overline{R(A)} = R(A)$, gives $\|R(y^\delta) - A^\dagger y\| \le \|A^\dagger\|\,\delta$. So the condition in the theorem holds exactly for the well-posed problems.
- **The worst case is essential.** The hypothesis asks for convergence for all noise with norm $\delta$. If the noise is restricted, for example to noise that is not too smooth relative to $A$ in a sense made precise by noise conditions, heuristic rules such as quasi-optimality and the Hanke-Raus rule converge and can even reach rates (Kindermann 2011). In the example above, the noise in situation B is exactly the smooth kind that such conditions exclude.
- **Extra information breaks the veto.** A rule that knows a bound on $\|x^\dagger\|$, the variance of random noise, or a second independent measurement uses more than $y^\delta$, and the theorem does not apply to it.

## History

A. B. Bakushinskii published the result in 1984 in a two-page note on the quasi-optimality and ratio criteria. Engl, Hanke and Neubauer included it in Chapter 3 of their 1996 monograph in the general form above, and it became the standard reason to call noise-free rules heuristic. The name "Bakushinskii veto" is common in later work on heuristic rules, such as the papers of S. Kindermann; we could not confirm who first used it. Kindermann (2011) and later papers turned the veto around and asked which restrictions on the noise make heuristic rules converge.

## References
