---
tag: KBHPWA
kind: algorithm
slug: h-infinity-norm-computation
name: H-infinity norm computation by bisection
aliases:
- Boyd-Balakrishnan-Bruinsma-Steinbuch algorithm
- Hamiltonian bisection for the H-infinity norm
area: control/robust-and-adaptive-control
level: advanced
summary: Decides whether the H-infinity norm of a system with A Hurwitz is at least gamma from the imaginary eigenvalues of a Hamiltonian matrix, then bisects on gamma or raises gamma by the level set method.
model: real-ram
complexity:
  vars: {n: the state dimension, m: the number of inputs, p: the number of outputs, e: "the relative accuracy (epsilon on the page)"}
  time: {worst: "O((n + m + p)^3 log(n / e))"}
  space: {extra: "O((n + m + p)^2)"}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 1989
  people: [Stephen Boyd, Venkataramanan Balakrishnan, Pierre Kabamba, N. A. Bruinsma, Maarten Steinbuch]
  note: "Boyd, Balakrishnan and Kabamba gave the Hamiltonian test and the bisection in 1989. In 1990 Bruinsma and Steinbuch, and Boyd and Balakrishnan, gave the level set iteration and its quadratic convergence."
prereqs: [h-infinity-norm, hamiltonian-matrix, bisection-method]
see_also: [h-infinity-norm, bounded-real-lemma, hankel-singular-values, balanced-truncation-error-bound, continuous-algebraic-riccati-equation, h-infinity-control-problem, singular-value-decomposition, h2-norm]
sources:
  - paper: doi:10.1007/BF02551385
    title: Stephen Boyd, Venkataramanan Balakrishnan and Pierre Kabamba, A bisection method for computing the H-infinity norm of a transfer matrix and related problems, Mathematics of Control, Signals, and Systems 2(3) (1989) 207-219
    locator: the whole paper (the Hamiltonian test for a level gamma and the bisection on gamma)
  - paper: "N. A. Bruinsma and M. Steinbuch, A fast algorithm to compute the H-infinity-norm of a transfer function matrix, Systems and Control Letters 14(4), 287-293, 1990"
    locator: the whole paper (the level set iteration with midpoints of the imaginary eigenvalues, and its start value)
  - paper: "Stephen Boyd and Venkataramanan Balakrishnan, A regularity result for the singular values of a transfer matrix and a quadratically convergent algorithm for computing its L-infinity-norm, Systems and Control Letters 15(1), 1-7, 1990"
    locator: the whole paper (the regularity of the largest singular value and the quadratic convergence of the level set iteration)
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 4, Performance Specifications (the computation of the H2 and H-infinity norms), and Chapter 8, Hankel Norm Approximation (the bounds by the Hankel singular values)
---

H-infinity norm computation finds the [H-infinity norm](/h-infinity-norm/) of a linear system with a Hurwitz state matrix, the peak over all frequencies of the largest singular value of its transfer matrix, to a chosen relative accuracy. It does not search over frequency. Instead it answers the question "is the norm at least gamma?" exactly, by checking whether a $2n \times 2n$ [Hamiltonian matrix](/hamiltonian-matrix/) built from the state-space data has an eigenvalue on the imaginary axis. Boyd, Balakrishnan and Kabamba (1989) used this test inside a [bisection](/bisection-method/) on gamma, and Bruinsma and Steinbuch (1990) used the frequencies of the imaginary eigenvalues to raise gamma at each step, which converges quadratically.

## In plain words

A system whose free motion dies out amplifies some input signals more than others, and the amount depends on how fast the input oscillates. The H-infinity norm is the largest amplification over all inputs and all speeds. You could test many speeds one by one, but you can miss a narrow peak between two test points. This method asks a different question: is there any speed at which the amplification reaches a given level? A small matrix built from the system answers this question with certainty, and it also tells you at which speeds the amplification crosses that level. Bisection then halves the range of possible levels until it is small enough. The faster variant uses the crossing speeds: the peak lies between two crossings, so it tests the middle of each such gap and moves the level up to the best value found.

## The problem

**Input.** Real matrices $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$ and $D \in \mathbb{R}^{p \times m}$ of the system $x' = A x + B u$, $y = C x + D u$, with $A$ [Hurwitz](/hurwitz-matrix/), and a relative accuracy $\varepsilon > 0$. The realization need not be minimal.

**Output.** Numbers $lo \le hi$ with

$$lo \le \|G\|_\infty \le hi, \qquad hi - lo \le 2\varepsilon\, lo,$$

where $G(s) = C(sI - A)^{-1}B + D$ is the [transfer function](/transfer-function/) and $\|G\|_\infty = \sup_{\omega \in \mathbb{R}} \sigma_{\max}(G(j\omega))$, with $\sigma_{\max}$ the largest [singular value](/singular-value-decomposition/). The level set method also returns a frequency $\omega$ (possibly $\infty$) with $\sigma_{\max}(G(j\omega)) = lo$.

**The test.** For $\gamma > 0$ that is not a singular value of $D$, let $M_\gamma = \begin{bmatrix} D & -\gamma I_p \\ -\gamma I_m & D^T \end{bmatrix}$ and

$$H_\gamma = \begin{bmatrix} A & 0 \\ 0 & -A^T \end{bmatrix} + \begin{bmatrix} B & 0 \\ 0 & -C^T \end{bmatrix} M_\gamma^{-1} \begin{bmatrix} -C & 0 \\ 0 & -B^T \end{bmatrix}, \qquad H_\gamma = \begin{bmatrix} A & \gamma^{-1} B B^T \\ -\gamma^{-1} C^T C & -A^T \end{bmatrix} \text{ if } D = 0.$$

If $A$ has no imaginary eigenvalue, then $\gamma$ is a singular value of $G(j\omega_0)$ exactly when $j\omega_0$ is an eigenvalue of $H_\gamma$. With $A$ Hurwitz and $\gamma > \sigma_{\max}(D)$ it follows that $\|G\|_\infty \ge \gamma$ if and only if $H_\gamma$ has an imaginary eigenvalue. The characteristic polynomial of $H_\gamma$ is even, $\det(sI - H_\gamma) = r(s^2)$ with $\deg r = n$, so the imaginary eigenvalues $\pm j\omega$ are the real roots $t = -\omega^2 \le 0$ of $r$.

## The algorithm

```pseudo id=main
IMAGINARY-FREQUENCIES(A, B, C, D, γ)
L1  M ← [[D, -γ I_p], [-γ I_m, D^T]]; H ← [[A, 0], [0, -A^T]] + [[B, 0], [0, -C^T]] M^(-1) [[-C, 0], [0, -B^T]]
L2  r ← the polynomial of degree n with det(sI - H) = r(s²)
L3  return the sorted list of ω = √(-t) for the real roots t ≤ 0 of r

HINF-BISECTION(A, B, C, D, ε)
L4  check that A is Hurwitz; d ← σ_max(D)
L5  σ_1 ≥ ... ≥ σ_n ← the Hankel singular values, the square roots of the eigenvalues of W_c W_o
L6  lo ← max(d, σ_1); hi ← d + 2 (σ_1 + ... + σ_n)
L7  while hi - lo > 2ε lo
L8      γ ← (lo + hi) / 2
L9      if IMAGINARY-FREQUENCIES(A, B, C, D, γ) is not empty then lo ← γ else hi ← γ
L10 return (lo, hi)

HINF-LEVEL-SET(A, B, C, D, ε)
L11 check that A is Hurwitz; lb ← the largest of σ_max(D), σ_max(G(0)) and σ_max(G(j|λ|)) for the eigenvalues λ of A
L12 loop
L13     γ ← (1 + 2ε) lb; F ← IMAGINARY-FREQUENCIES(A, B, C, D, γ)
L14     if F is empty then return (lb, γ)
L15     ω_1 < ... < ω_k ← F together with -F; best ← max(lb, max over i < k of σ_max(G(j (ω_i + ω_(i+1)) / 2)))
L16     if best ≤ γ then return (best, γ) else lb ← best
```

Lines L1 to L3 are the test. Line L1 needs $M_\gamma$ invertible, which holds for every $\gamma > \sigma_{\max}(D)$; both callers only use such levels. Line L2 drops the odd coefficients of the characteristic polynomial, which are zero in exact arithmetic. Line L3 turns each real root $t \le 0$ of $r$ into a frequency $\omega \ge 0$ at which some singular value of $G(j\omega)$ equals $\gamma$. These crossings belong to any singular value, not only the largest one.

Lines L5 and L6 give the start interval. Here $W_c$ and $W_o$ are the [controllability gramian](/controllability-gramian/) and the [observability gramian](/observability-gramian/), from $A W_c + W_c A^T + B B^T = 0$ and $A^T W_o + W_o A + C^T C = 0$. The norm is at least $\sigma_{\max}(D)$ (its limit at infinity) and at least the largest [Hankel singular value](/hankel-singular-values/), and at most $\sigma_{\max}(D) + 2 \sum \sigma_i$ by the [balanced truncation error bound](/balanced-truncation-error-bound/) with nothing kept. Lines L7 to L9 keep the norm in $[lo, hi]$ and halve the interval at each pass.

Line L11 starts the level set method from values of $\sigma_{\max}$ at three kinds of points: infinity, zero, and the moduli of the poles, where lightly damped peaks sit. Bruinsma and Steinbuch use a similar rule with one pole frequency. Each pass of lines L12 to L16 tests the level just above the current lower bound. If the test fails, the norm is below $\gamma$ and the interval $[lb, \gamma]$ is the answer. If it passes, the frequencies where some singular value equals $\gamma$ cut the axis into pieces. On every piece where $\sigma_{\max} > \gamma$ both ends are crossings, so the midpoint of two consecutive crossings falls inside, and line L15 finds a value above $\gamma$. Line L15 uses negative frequencies too, so that a peak at $\omega = 0$, between $-\omega_1$ and $\omega_1$, is found.

The implementation forms $H_\gamma$, computes its characteristic polynomial with the [Faddeev-LeVerrier algorithm](/faddeev-leverrier-algorithm/), and finds the roots of $r$ with the [Durand-Kerner method](/durand-kerner-method/) of the shared helper module. A root $t$ counts as real when $|\operatorname{Im} t| \le 10^{-6}(1 + |t|)$ and as nonpositive when $\operatorname{Re} t \le 10^{-10}(1 + |t|)$. This is fine for the small $n$ of the tests ($2n \le 6$); a production code computes the eigenvalues of $H_\gamma$ with a structure preserving variant of the [QR algorithm](/qr-algorithm/).

## Example

**A lightly damped mode.** Take $G(s) = 1/(s^2 + 0.2 s + 1)$, with damping ratio $\zeta = 0.1$ and natural frequency 1 rad/s, as $A = \begin{bmatrix} 0 & 1 \\ -1 & -0.2 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C = \begin{bmatrix} 1 & 0 \end{bmatrix}$ and $D = 0$. The exact norm is $1/(2\zeta\sqrt{1 - \zeta^2}) = 5.025189$, reached at $\omega = \sqrt{1 - 2\zeta^2} = 0.98995$ rad/s. Here

$$H_\gamma = \begin{bmatrix} 0 & 1 & 0 & 0 \\ -1 & -0.2 & 0 & 1/\gamma \\ -1/\gamma & 0 & 0 & 1 \\ 0 & 0 & -1 & 0.2 \end{bmatrix}, \qquad r(t) = t^2 + 1.96\, t + 1 - \frac{1}{\gamma^2}.$$

The sum of the roots of $r$ is $-1.96$, so its real roots are negative whenever they exist, and they exist exactly when $1.96^2 \ge 4(1 - 1/\gamma^2)$, that is $\gamma \le 1/\sqrt{0.0396} = 5.025189$. This matches the exact norm, as the test promises. The same follows from $|G(j\omega)|^2 = 1/((1 - \omega^2)^2 + 0.04\,\omega^2)$ with $t = -\omega^2$.

The gramians are $W_c = 2.5\, I$ and $W_o = \begin{bmatrix} 2.6 & 0.5 \\ 0.5 & 2.5 \end{bmatrix}$, and the Hankel singular values are $2.76247$ and $2.26247$. Line L6 gives $lo = 2.76247$ and $hi = 2(2.76247 + 2.26247) = 10.04988$. The first passes of the bisection are:

| pass | γ | frequencies of line L3 (rad/s) | update |
|---|---|---|---|
| 1 | 6.40617 | none | hi ← 6.40617 |
| 2 | 4.58432 | 0.94374, 1.03409 | lo ← 4.58432 |
| 3 | 5.49525 | none | hi ← 5.49525 |
| 4 | 5.03978 | none | hi ← 5.03978 |
| 5 | 4.81205 | 0.95923, 1.01975 | lo ← 4.81205 |
| 6 | 4.92592 | 0.96946, 1.01003 | lo ← 4.92592 |
| 7 | 4.98285 | 0.97673, 1.00299 | lo ← 4.98285 |
| 8 | 5.01132 | 0.98244, 0.99741 | lo ← 5.01132 |

With $\varepsilon = 10^{-8}$ the bisection stops after 27 passes with $[5.0251890604, 5.0251891147]$. The two crossing frequencies close in on the peak frequency from both sides as $\gamma$ rises.

The level set method starts from $lb = |G(j \cdot 1)| = 5$, because both poles have modulus 1, against $|G(0)| = 1$ and $\sigma_{\max}(D) = 0$.

| pass | γ | frequencies | midpoints | new lower bound |
|---|---|---|---|---|
| 1 | 5.0000001 | 0.979796, 1.000000 | 0, ±0.989898 | 5.02518842 at 0.989898 |
| 2 | 5.0251885 | 0.989902, 0.989997 | 0, ±0.989949 | 5.0251890763 at 0.989949 |
| 3 | 5.0251892 | none | | stop |

It returns $[5.0251890763, 5.0251891768]$, and the lower end equals the exact norm to all printed digits. The error of the lower bound drops from $1.3 \times 10^{-7}$ (relative) after pass 1 to below $10^{-15}$ after pass 2: the quadratic convergence of Boyd and Balakrishnan.

**A realization that is not minimal.** With $A = \begin{bmatrix} -4 & -8 & 12 \\ 0 & -8 & 0 \\ 0 & 0 & -16 \end{bmatrix}$, $B = (1, 0, 0)^T$, $C = (1, 1, 1)$ and $D = 0$, the modes at $-8$ and $-16$ are not controllable, and $G(s) = 1/(s + 4)$. The Hankel singular values are $0.125$, $0$ and $0$, and both methods return the norm $0.25$, reached at $\omega = 0$.

**A peak at infinity.** For $G(s) = (s + 1)/(s + 2)$, written as $A = -2$, $B = 1$, $C = -1$, $D = 1$, the gain $|G(j\omega)|$ rises from $0.5$ at $\omega = 0$ toward 1 and never reaches it. The norm is $\sigma_{\max}(D) = 1$. No level above 1 gives an imaginary eigenvalue, so the bisection shrinks $hi$ to $lo = 1$, and the level set method stops at once with $\omega = \infty$.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md). They hold in exact arithmetic.

- **Hamiltonian test (proved).** If $A$ has no imaginary eigenvalue and $\gamma$ is not a singular value of $D$, then $\gamma$ is a singular value of $G(j\omega_0)$ if and only if $j\omega_0$ is an eigenvalue of $H_\gamma$. The proof turns a pair of singular vectors $(u, v)$ into an eigenvector $(x, q)$ with $x = (j\omega_0 I - A)^{-1} B u$, and back.
- **Even polynomial (proved).** $J H_\gamma$ is symmetric for $J = \begin{bmatrix} 0 & I \\ -I & 0 \end{bmatrix}$, so $H_\gamma$ is similar to $-H_\gamma^T$ and $\det(sI - H_\gamma)$ is a polynomial in $s^2$.
- **Level test (proved).** For $A$ Hurwitz and $\gamma > \sigma_{\max}(D)$: $\|G\|_\infty \ge \gamma$ if and only if $H_\gamma$ has an imaginary eigenvalue. The proof uses the continuity of $\sigma_{\max}(G(j\omega))$, its limit $\sigma_{\max}(D)$ at infinity, and the intermediate value theorem.
- **Bisection (proved).** The interval $[lo, hi]$ always holds the norm, and the loop runs at most $\lceil \log_2(n/\varepsilon) \rceil$ times, because the start interval has width at most $2n\, lo$.
- **Level set (proved).** The lower bound is always a value of $\sigma_{\max}$, so it never exceeds the norm. A pass that does not stop raises it by a factor larger than $1 + 2\varepsilon$, so the method stops. At a stop the norm is at most $\gamma$.

## Complexity

The model is the [real RAM](/real-ram/), with $n$ the state dimension, $m$ the number of inputs, $p$ the number of outputs and $\varepsilon$ the relative accuracy. Dense factorizations count as $O(k^3)$ flops for a $k \times k$ matrix, and the eigenvalues of a $2n \times 2n$ matrix count as $O(n^3)$, as is usual for the QR algorithm.

- **One test (lines L1 to L3).** Solving with $M_\gamma$ costs $O((m + p)^3 + n (m + p)^2)$, the products cost $O(n^2 (m + p))$, and the eigenvalues cost $O(n^3)$. The implementation instead spends $O(n^4)$ on the Faddeev-LeVerrier recursion and $O(k n^2)$ on $k$ Durand-Kerner iterations.
- **Start of the bisection (lines L4 to L6).** Two Lyapunov equations and the eigenvalues of $W_c W_o$ cost $O(n^3)$ with the Bartels-Stewart method (see [the Lyapunov equation](/lyapunov-equation/)). The implementation solves the $n^2 \times n^2$ Kronecker system instead, in $O(n^6)$, which is fine for $n \le 3$.
- **Bisection.** At most $\lceil \log_2(n/\varepsilon) \rceil$ tests, so $O((n + m + p)^3 \log(n/\varepsilon))$ in all. The convergence is linear: one bit of accuracy per pass.
- **Level set, per pass.** One test, plus at most $2n - 1$ evaluations of $G$ at midpoints, because $r$ has at most $n$ roots. Each evaluation costs $O(n^3 + n^2 (m + p) + n m p)$ and a singular value computation $O(m p \min(m, p))$. After a one time reduction of $A$ to [Hessenberg form](/hessenberg-reduction/), each evaluation of $G(j\omega)$ costs $O(n^2 (m + p))$.
- **Level set, number of passes.** The proved bound is $1 + \log(\|G\|_\infty / lb_0) / \log(1 + 2\varepsilon)$, which is poor. The convergence result of Boyd and Balakrishnan (1990) is local and quadratic. In the tests of this page the level set method used 0 to 3 passes (a measurement, not a bound).
- **Space.** $O((n + m + p)^2)$ for the matrices.

## Properties

- **Certified interval.** In exact arithmetic the output interval holds the norm. A frequency sweep only gives a lower bound, and it can miss a narrow peak by any amount.
- **Independent of the realization.** Uncontrollable or unobservable modes do not change $G$, and they do not change the answer; they add eigenvalues of $H_\gamma$ that are never on the imaginary axis when $A$ is Hurwitz.
- **Peak frequency.** The level set method returns a frequency at which the lower bound is reached. The bisection returns only the interval, but the crossings of its last successful test bracket a frequency near the peak.
- **Not exact.** The norm is in general an algebraic number with no closed form, so every method returns an interval.
- **Deterministic.** The same input gives the same output.

## Variants and improvements

- **Level set iteration.** Lines L11 to L16, from Bruinsma and Steinbuch (1990) and Boyd and Balakrishnan (1990). It is the method used in practice, because it needs few passes.
- **Discrete time.** For $G(z) = C(zI - A)^{-1}B + D$ with $A$ Schur, the frequencies are points $e^{j\theta}$ on the unit circle. The Hamiltonian matrix becomes a symplectic matrix or pencil, and the test looks for its eigenvalues of modulus 1. A [bilinear transform](/bilinear-transform/) to continuous time is another way.
- **Structure preserving eigenvalue solvers.** A general eigenvalue solver can move a true imaginary eigenvalue of $H_\gamma$ off the axis by rounding. Solvers that keep the Hamiltonian structure keep the eigenvalues in pairs $\lambda, -\bar\lambda$, so a simple imaginary eigenvalue stays on the axis.
- **Descriptor systems and large systems.** The test extends to $E x' = A x + B u$ through a [generalized eigenvalue problem](/generalized-eigenvalue-problem/) with the [QZ algorithm](/qz-algorithm/). For large sparse systems, only the eigenvalues near the imaginary axis are needed, and Krylov methods are used.
- **Related levels.** The same idea tests other quantities: the distance of a Hurwitz matrix to the set of unstable matrices (with $B = C = I$), and the [bounded real lemma](/bounded-real-lemma/) gives the Riccati and LMI forms of the same question "is the norm below gamma?".

## When to use it

Use it whenever you need the H-infinity norm of a system with a state-space model: to check a robustness margin with the [small-gain theorem](/small-gain-theorem/), to report the peak of a sensitivity function, to check the result of an [H-infinity synthesis](/h-infinity-control-problem/), or as the inner test of a gamma iteration. For one lightly damped mode a sweep near the resonance gives a good lower bound, but only the Hamiltonian test certifies the upper bound. For the [H2 norm](/h2-norm/) no iteration is needed; one Lyapunov equation gives it.

## Pitfalls

- **A must be Hurwitz.** If $A$ has an imaginary eigenvalue the norm is infinite or the test of Lemma 1 fails, and if $A$ has an eigenvalue in the right half plane the supremum over $j\omega$ is the $L_\infty$ norm, not the H-infinity norm. Check $A$ first, as lines L4 and L11 do.
- **Levels at or below the norm of D.** At $\gamma = \sigma_{\max}(D)$ the matrix $M_\gamma$ is singular, and below it the test is not valid. The start values keep every level above $\sigma_{\max}(D)$.
- **Tangency is ill-conditioned.** At $\gamma = \|G\|_\infty$ two imaginary eigenvalues merge, and near this level they split by about the square root of the unit roundoff. A tolerance on the real part is needed; too small a tolerance turns a correct "yes" into "no" near the norm, and too large a tolerance turns a "no" into "yes". The implementation works on $t = s^2$, where a crossing at $\omega = 0$ is a simple root and stays well conditioned.
- **Crossings of other singular values.** For a system with several inputs and outputs, a frequency in line L3 can be a crossing of a smaller singular value. The bisection does not care, but a level set code that only uses pairs of crossings as intervals must use consecutive crossings, as line L15 does, and not assume that they alternate between rising and falling.
- **Scaling.** Badly scaled $A$, $B$, $C$ give a badly scaled $H_\gamma$. Balance the realization first.
- **Sweeps are lower bounds.** A grid of frequencies can miss a peak of width about $\zeta \omega_n$ by a large factor. Use a sweep only to check, never to bound the norm from above.

## Implementations

## History

Before 1989 the H-infinity norm was found by sweeping the frequency or by a gamma iteration on a Riccati equation. Boyd, Balakrishnan and Kabamba (1989) showed that the question "is the norm at least gamma?" has an exact answer from the imaginary eigenvalues of a Hamiltonian matrix, and they used it in a bisection with the Hankel singular value bounds as the start interval. They also noted that the test applies to related problems, such as the distance to instability. In 1990 Bruinsma and Steinbuch used the crossing frequencies to raise the level, and Boyd and Balakrishnan proved that this level set iteration converges quadratically, from a regularity result on the largest singular value near a peak. The level set method is now the standard way to compute the norm.

## References
