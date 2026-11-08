---
tag: GD4NTE
kind: algorithm
slug: parareal-algorithm
name: Parareal algorithm
aliases:
- parallel-in-time algorithm
- parareal
area: numerical/differential-equations
level: research
summary: "Cut [t0, T] into N slices; iterate U(n+1) = G(U(n) new) + F(U(n) old) - G(U(n) old) with a cheap coarse G and an accurate fine F whose N solves run in parallel. Exact after N iterations."
solves: [ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of time slices", K: "the number of iterations", P: "the cost of one fine solve over one slice", Q: "the cost of one coarse solve over one slice", d: "the dimension of y"}
  time: {worst: "Θ(K N (P + Q) + N Q)", parallel: "Θ(K P + (K + 1) N Q)"}
  space: {extra: "Θ(N d)"}
  evaluations: {fine: "K N", coarse: "(K + 1) N"}
properties: {deterministic: true, parallel_in_time: true, exact_after_n_iterations: true, speedup_bound: "N / K"}
history:
  year: 2001
  people: [Jacques-Louis Lions, Yvon Maday, Gabriel Turinici]
  note: "Lions, Maday and Turinici introduced parareal in 2001; Gander and Vandewalle (2007) identified it as a multiple shooting and multigrid method and proved its convergence bounds."
prereqs: [ode-initial-value-problem, backward-euler-method, classical-runge-kutta-4]
see_also: [shooting-method, stiff-ode-problem, global-error, order-of-accuracy, stability-region, method-of-lines, picard-iteration, parallel-prefix]
sources:
  - paper: doi:10.1016/S0764-4442(00)01793-6
    title: "Jacques-Louis Lions, Yvon Maday and Gabriel Turinici, Résolution d'EDP par un schéma en temps pararéel, Comptes Rendus de l'Académie des Sciences Paris, Série I, 332 (2001) 661-668"
  - paper: doi:10.1137/05064607X
    title: "Martin J. Gander and Stefan Vandewalle, Analysis of the parareal time-parallel time-integration method, SIAM Journal on Scientific Computing 29 (2007) 556-578"
    locator: Section 2 (multiple shooting and multigrid interpretations) and Section 4 (linear convergence bounds on bounded and unbounded intervals)
  - paper: doi:10.1145/355588.365137
    title: "Jürg Nievergelt, Parallel methods for integrating ordinary differential equations, Communications of the ACM 7 (1964) 731-733"
  - paper: doi:10.1007/978-3-319-23321-5_3
    title: "Martin J. Gander, 50 years of time parallel time integration, in Multiple Shooting and Time Domain Decomposition Methods, Springer, 2015, 69-113"
  - book: isbn:9783540566700
    title: "Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I: Nonstiff Problems, 2nd ed., Springer, 1993"
    locator: Section II.3 (convergence of one-step methods, used for the order of the coarse and fine propagators)
---

The parareal algorithm solves an [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$, $y(t_0) = y_0$ on $[t_0, T]$ with parallelism across time. The interval is cut into $N$ slices $[T_n, T_{n+1}]$. A coarse propagator $\mathcal{G}$ (one [backward Euler](/backward-euler-method/) step, say) and a fine propagator $\mathcal{F}$ (many [RK4](/classical-runge-kutta-4/) steps, say) both map a value at $T_n$ to an approximation at $T_{n+1}$. Starting from a coarse sweep $U^0$, the iteration

$$U^{k+1}_0 = y_0, \qquad U^{k+1}_{n+1} = \mathcal{G}(U^{k+1}_n) + \mathcal{F}(U^k_n) - \mathcal{G}(U^k_n)$$

needs the $N$ fine solves $\mathcal{F}(U^k_n)$ only at the old iterate, so they run on $N$ processors at once; only the cheap coarse sweep is sequential. After $k$ iterations the values $U^k_0, \dots, U^k_k$ equal the sequential fine solution exactly, so the method terminates in at most $N$ iterations. It is useful when it converges in far fewer, which happens for diffusive problems and fails for long oscillatory ones.

## In plain words

Solving an equation forward in time looks hopelessly sequential: the state at noon is needed before the afternoon can be computed. Parareal breaks this chain by guessing. A quick, rough solver runs through the whole time range and produces guesses for the state at the start of every time slice. Many processors then each run the accurate, slow solver on one slice, starting from these guesses, all at the same moment.

The accurate results do not fit together, because the guesses were rough. So the rough solver runs through again, and at every slice boundary it corrects itself by the difference it saw between the accurate and the rough answer last time. Each round makes at least one more slice exactly right, and in practice a handful of rounds makes all slices about as accurate as the slow solver alone.

## The problem

Given $f$, $y_0$, $T \ge t_0$, the number of slices $N \ge 1$, and two propagators $\mathcal{F}(T_a, T_b, y)$ and $\mathcal{G}(T_a, T_b, y)$, compute values $U_n \approx u_n$ at $T_n = t_0 + n(T - t_0)/N$, where $u_0 = y_0$, $u_{n+1} = \mathcal{F}(T_n, T_{n+1}, u_n)$ is the sequential fine solution. The target accuracy is that of $u_n$; the error of parareal is measured against $u_n$, not against the exact solution. Cost is counted in fine and coarse slice solves (each made of $f$ evaluations, and of Jacobians and linear solves for implicit propagators), and the figure of merit is the wall-clock time with $N$ processors compared to the $N$ sequential fine solves.

## The algorithm

```pseudo id=main
PARAREAL(G, F, t0, y0, T, N, K, tol)
L1  U_0 ← y0;  for n ← 0 to N − 1: g_n ← G(T_n, T_{n+1}, U_n), U_{n+1} ← g_n
L2  for k ← 1 to K do
L3      for n ← 0 to N − 1 in parallel: F_n ← F(T_n, T_{n+1}, U_n)
L4      V_0 ← y0
L5      for n ← 0 to N − 1 do                   ▷ sequential coarse sweep
L6          g_new ← G(T_n, T_{n+1}, V_n)
L7          V_{n+1} ← g_new + F_n − g_n;  g_n ← g_new
L8      δ ← max_n ‖V_n − U_n‖;  U ← V
L9      if δ ≤ tol then return U
L10 return U
```

Line L7 is the whole method: the new coarse value plus the correction $\mathcal{F} - \mathcal{G}$ measured at the old iterate. The coarse values $g_n$ of the previous sweep are stored, so each iteration costs $N$ fine and $N$ coarse solves. In the implementation $K$ defaults to $N$, and the result reports the number of calls of each propagator.

## Example

**By hand, in fractions.** $y' = -y$ on $[0, 3]$, $N = 3$ slices of length 1. $\mathcal{G}$ is one backward Euler step, multiplication by $\frac12$. $\mathcal{F}$ is four forward Euler steps of size $\frac14$, multiplication by $(\frac34)^4 = \frac{81}{256}$. The fine solution is $u_n = (\frac{81}{256})^n$. For instance $U^1_2 = \frac12U^1_1 + \frac{81}{256}U^0_1 - \frac12U^0_1 = \frac{81}{512} + \frac{81}{512} - \frac14 = \frac{17}{256}$.

| | $U_0$ | $U_1$ | $U_2$ | $U_3$ |
|---|---|---|---|---|
| $k = 0$ (coarse) | 1 | 1/2 | 1/4 | 1/8 |
| $k = 1$ | 1 | 81/256 | 17/256 | −13/1024 |
| $k = 2$ | 1 | 81/256 | 6561/65536 | 4963/131072 |
| $k = 3$ | 1 | 81/256 | 6561/65536 | 531441/16777216 |
| fine | 1 | 81/256 | 6561/65536 | 531441/16777216 |

After iteration $k$ the first $k + 1$ entries are exact, as the theorem below says; iteration 1 even produces a negative value at $T_3$, so intermediate iterates need not look like solutions.

**Convergence rates.** Errors $\max_n\|U^k_n - u_n\|$ against the sequential fine solution, all observed with the implementation:

| problem | $k = 0$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $y' = -y$, $T = 10$, $N = 20$, $\mathcal{G}$ = backward Euler, $\mathcal{F}$ = 50 RK4 steps | 7.7e-2 | 9.8e-3 | 1.4e-3 | 2.2e-4 | 3.6e-5 | 5.9e-6 | 9.9e-7 |
| $y' = -1000(y - \cos t)$, $T = 1$, $N = 10$, $\mathcal{G}$ = backward Euler, $\mathcal{F}$ = 1000 RK4 steps | 9.9e-3 | 9.9e-5 | 9.8e-7 | 9.7e-9 | 9.6e-11 | 9.5e-13 | |
| Brusselator, $T = 20$, $N = 20$, $\mathcal{G}$ = 4 RK4 steps, $\mathcal{F}$ = 100 RK4 steps | 1.1e-1 | 1.5e-2 | 3.8e-4 | 2.2e-6 | 8.3e-9 | 2.2e-11 | 2.3e-14 |
| oscillator $y'' = -y$, $T = 10$, $N = 10$, $\mathcal{G}$ = 1 RK4 step, $\mathcal{F}$ = 100 RK4 steps | 7.7e-2 | 2.7e-3 | 6.1e-5 | 8.9e-7 | 8.4e-9 | 6.3e-11 | 2.6e-13 |
| oscillator, $T = 100$, $N = 50$, same propagators | 1.00 | 0.999 | 0.999 | 0.999 | 0.996 | 0.988 | 0.973 |

For the stiff problem the contraction factor per iteration is $0.0099$, which is $\alpha = |\mathcal{F} - \mathcal{G}| \approx \frac1{101}$ for $\lambda\Delta T = -100$: backward Euler damps the stiff mode just as the fine solver does, and the error shrinks by $\alpha$ per iteration. For the decay problem $\alpha = |e^{-1/2} - \frac23| = 0.060$, and the observed factors 0.13 to 0.16 fit the bound $\alpha^k\binom{n-1}{k}$, whose ratio is $\alpha(n - 1 - k)/(k + 1)$. The Brusselator (the system $x' = 1 + x^2y - 4x$, $y' = 3x - x^2y$ from $(1.5, 3)$) converges as quickly as the scalar problems. With 2 RK4 steps per slice for $\mathcal{G}$ it stalls near error 3 for four iterations before converging, and with 1 step the coarse sweep itself is unstable and the iterates overflow. The oscillator over 50 slices is the hyperbolic difficulty: after 12 iterations the error is still 0.5.

**Speedup.** For the decay problem a fine solve costs 200 evaluations of $f$ and a coarse solve about 1. Reaching the fine accuracy level of $10^{-8}$ takes $K = 8$ iterations, so with 20 processors the wall clock is about $8 \cdot 200 + 9 \cdot 20 = 1780$ evaluations against $20 \cdot 200 = 4000$ sequentially: a speedup of about 2.2 on 20 processors. This is a cost-model estimate, not a timing.

## Correctness

The following are proved in the correctness file, in exact arithmetic.

**Exactness after $k$ iterations.** For any propagators $\mathcal{F}$ and $\mathcal{G}$ (nonlinear, any order), $U^k_n = u_n$ for $n \le k$. Induction on $k$: if $U^k_n = u_n$ for $n \le k$, then $U^{k+1}_0 = y_0 = u_0$, and $U^{k+1}_n = u_n$ with $n \le k$ gives $U^{k+1}_{n+1} = \mathcal{G}(u_n) + \mathcal{F}(u_n) - \mathcal{G}(u_n) = u_{n+1}$. Hence after $N$ iterations $U^N = u$, which is the termination guarantee, and a fixed point of the iteration is the fine solution.

**Linear error bound.** For $y' = \lambda y$ (or a normal matrix, mode by mode) with $\mathcal{F}$ and $\mathcal{G}$ multiplication by $\varphi$ and $\gamma$, the error $e^k_n = U^k_n - u_n$ satisfies $e^{k+1}_{n+1} = \gamma e^{k+1}_n + (\varphi - \gamma)e^k_n$. With $\alpha = |\varphi - \gamma|$ and $|\gamma| \le 1$,

$$|e^k_n| \le \alpha^k\binom{n-1}{k}\max_j|e^0_j| \le \frac{(\alpha(N - 1))^k}{k!}\max_j|e^0_j|.$$

If $\mathcal{G}$ has order $p$ and $\mathcal{F}$ is much more accurate, $\alpha = O(\Delta T^{p+1})$ and $\max|e^0| = O(\Delta T^p)$ on a fixed interval, so $\max_n|e^k_n| = O(\Delta T^{p(k+1)})$: each iteration adds $p$ to the order (asymptotic, proved for the linear case; Gander and Vandewalle prove the superlinear bound, and a linear bound $(\alpha/(1 - |\gamma|))^k$ on unbounded intervals).

For nonlinear $f$ the analogous bounds need Lipschitz conditions on $\mathcal{F} - \mathcal{G}$ and on $\mathcal{G}$; they are cited (Gander and Hairer 2008), not proved here. The rates in the example tables are observations.

## Complexity

Sequentially the method does $KN$ fine and $(K + 1)N$ coarse solves, more than the $N$ fine solves of the plain sequential method; parareal only pays off in parallel. With $N$ processors each iteration takes the time of one fine solve plus a sequential coarse sweep, so the wall clock is $\Theta(KP + (K + 1)NQ)$ against $NP$ sequentially, and the speedup is

$$S = \frac{NP}{KP + (K + 1)NQ} \le \min\Bigl(\frac NK, \frac{P}{(1 + 1/K)Q}\Bigr).$$

So the parallel efficiency $S/N$ is at most $1/K$, independent of the number of processors: parareal with 5 iterations cannot exceed 20% efficiency. Storage is $\Theta(Nd)$ for the slice values, the fine results and the coarse values (the model is the [real RAM](/real-ram/), with the cost of a solve counted in $f$ evaluations, Jacobians and linear solves). Pipelining the coarse sweep with the next fine solves, so that a processor starts its fine solve as soon as its new start value is known, removes part of the $NQ$ term.

## Properties

- **Exact in $N$ iterations**, for any propagators; useful only if $K \ll N$.
- **Order increase.** In the linear analysis the error after $k$ iterations is $O(\Delta T^{p(k+1)})$ for a coarse propagator of order $p$, until the fine accuracy is reached.
- **Multiple shooting and multigrid.** Parareal is a multiple shooting method in time whose Newton Jacobian is approximated by the coarse propagator, and equivalently a two-level multigrid method in time with aggressive coarsening (Gander and Vandewalle).
- **Stability requires a stable coarse propagator.** If $|\gamma| > 1$ on some mode the coarse sweep amplifies errors along the slices, as for the explicit Euler coarse solver on a stiff problem.
- **Poor for hyperbolic and oscillatory problems.** For $y' = i\omega y$ any coarse propagator has $|\varphi - \gamma|$ of order 1 once $\omega\Delta T$ is not small, and the bound $\alpha^k\binom{n-1}{k}$ grows with $n$ before it decays; the long oscillator run shows this.
- **Deterministic and non-intrusive.** It wraps existing solvers; neither propagator needs to know about the other.

## Variants and improvements

- **Coarse propagators.** Fewer steps of the same method, a lower-order method, a coarser spatial grid for PDEs, or a simplified model.
- **Adaptive stopping.** Stop when the iterate update falls below the fine solver's own error, as line L9 does with tol; for long intervals restart parareal on windows of slices.
- **PFASST and spectral deferred corrections.** Minion's PFASST interleaves parareal-like coarse sweeps with spectral deferred corrections so that each fine solve is only one correction sweep.
- **MGRIT.** Multigrid reduction in time (Falgout and coauthors, 2014) generalises parareal to more than two levels with F- and C-relaxation; parareal is two-level MGRIT with F-relaxation.
- **Krylov-enhanced and symplectic variants** for hyperbolic and Hamiltonian problems. The Krylov variant (Gander and Petcu, 2008) improves the coarse propagator for linear problems by projecting onto the span of earlier fine results.
- **Earlier time-parallel ideas.** Nievergelt's 1964 method solves from many starting values in parallel and interpolates; multiple shooting and waveform relaxation are relatives.

## When to use it

Use parareal when many processors are available, parallelism in space is exhausted (strong scaling has saturated), and the problem is diffusive or dissipative, so that a much cheaper coarse propagator is accurate and stable over a slice. Expect modest efficiency, typically $1/K$ with $K$ between 2 and 10. Do not use it for long-time integration of wave or Hamiltonian problems without a specialised variant, and do not use it with a single processor, where it only adds work.

## Pitfalls

- **Unstable coarse propagator.** An explicit coarse step that is unstable for the slice length makes the coarse sweep blow up; for stiff problems use an L-stable implicit coarse step.
- **Measuring against the wrong reference.** Parareal converges to the fine solution; its error against the exact solution cannot fall below the fine error (here $3.1 \cdot 10^{-11}$ for the decay problem).
- **Stopping on a small update.** A small $\delta$ in line L8 does not prove a small error; on oscillatory problems iterates can stagnate before they converge.
- **Forgetting the coarse cost.** If $\mathcal{G}$ is not much cheaper than $\mathcal{F}$, the sequential coarse sweep dominates and there is no speedup.
- **Too many slices.** The bound $\alpha^k\binom{n-1}{k}$ grows with $n$; more slices than the convergence can handle make $K$ grow.

## Implementations

## History

Nievergelt proposed parallel integration of ODEs across time in 1964. Lions, Maday and Turinici introduced parareal in a 2001 note in the Comptes Rendus, for the parallel solution of evolution PDEs, with the predictor-corrector form used here suggested by Baffico, Bernard, Maday, Turinici and Zérah in 2002. Gander and Vandewalle (2007) showed that parareal is a multiple shooting method and a two-level time multigrid method, and proved superlinear convergence bounds for linear problems; Gander and Hairer (2008) extended the analysis to nonlinear problems. Gander's 2015 survey places it among fifty years of time-parallel methods, and PFASST and MGRIT are its most used descendants.

## References
