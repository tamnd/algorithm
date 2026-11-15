---
tag: RKCE24
kind: definition
slug: barrier-certificate
name: Barrier certificate
aliases:
- Prajna-Jadbabaie barrier certificate
area: control/discrete-event-and-hybrid-systems
level: research
summary: A function that is at most zero on the initial set, positive on the unsafe set, and does not increase along trajectories, which proves that no trajectory reaches the unsafe set.
prereqs: [lyapunov-function, sum-of-squares-programming]
see_also: [control-barrier-function, cbf-safety-filter, lyapunov-function, sum-of-squares-programming, semidefinite-programming, positively-invariant-set, reachable-set-computation, hamilton-jacobi-reachability]
sources:
  - paper: doi:10.1007/978-3-540-24743-2_32
    title: "S. Prajna and A. Jadbabaie, Safety verification of hybrid systems using barrier certificates, Hybrid Systems: Computation and Control (HSCC 2004), LNCS 2993, Springer, 2004, pages 477 to 492"
    locator: the definition for continuous and hybrid systems, the safety theorem, and the search by sum of squares programming
  - paper: doi:10.1109/TAC.2007.902736
    title: "S. Prajna, A. Jadbabaie and G. J. Pappas, A framework for worst-case and stochastic safety verification using barrier certificates, IEEE Transactions on Automatic Control 52(8), 2007, pages 1415 to 1428"
    locator: barrier certificates with disturbances, for hybrid systems, and for stochastic systems with a bound on the probability of reaching the unsafe set
  - paper: doi:10.1137/050645178
    title: "S. Prajna and A. Rantzer, Convex programs for temporal verification of nonlinear dynamical systems, SIAM Journal on Control and Optimization 46(3), 2007, pages 999 to 1021"
    locator: convex certificates for eventuality and other temporal properties
  - paper: doi:10.1109/TAC.2015.2476155
    title: "R. Wisniewski and C. Sloth, Converse barrier certificate theorems, IEEE Transactions on Automatic Control 61(5), 2016, pages 1356 to 1361"
    locator: conditions under which a safe system has a barrier certificate
  - paper: doi:10.23919/ECC.2019.8796030
    title: "A. D. Ames, S. Coogan, M. Egerstedt, G. Notomista, K. Sreenath and P. Tabuada, Control barrier functions: theory and applications, European Control Conference, 2019, pages 3420 to 3431"
    locator: the relation between barrier certificates, barrier functions and control barrier functions
---

A barrier certificate is a function of the state that proves a safety property: no trajectory that starts in an initial set ever enters an unsafe set. It is at most zero on the initial set, positive on the unsafe set, and it does not increase along the solutions, so a solution cannot cross from the first set to the second. Prajna and Jadbabaie (2004) defined it for continuous and hybrid systems and showed that, for polynomial data, the search for a polynomial certificate is a [sum of squares program](/sum-of-squares-programming/), so a [semidefinite program](/semidefinite-programming/) can find one. The idea is the safety counterpart of a [Lyapunov function](/lyapunov-function/): the proof needs no computation of the solutions or of the [reachable set](/reachable-set-computation/).

## Definition

Let $x' = f(x, d)$ with $x \in X \subseteq \mathbb{R}^n$ and a disturbance $d(t) \in D$, with $f$ such that solutions exist and are unique. Let $X_0 \subseteq X$ be the initial set and $X_u \subseteq X$ the unsafe set. A barrier certificate is a continuously differentiable function $B : X \to \mathbb{R}$ with

$$B(x) \le 0 \ \text{ for } x \in X_0, \qquad B(x) > 0 \ \text{ for } x \in X_u, \qquad \nabla B(x) \cdot f(x, d) \le 0 \ \text{ for } x \in X, \ d \in D.$$

**Theorem (Prajna and Jadbabaie 2004).** If a barrier certificate exists, then no solution that starts in $X_0$ and stays in $X$ reaches $X_u$.

*Proof.* Along a solution, $\frac{d}{dt}B(x(t)) = \nabla B \cdot f \le 0$, so $B(x(t)) \le B(x(0)) \le 0$ for all $t \ge 0$. A point of $X_u$ has $B > 0$, so the solution never reaches one. $\blacksquare$

**The convex search.** The three conditions are linear in $B$, so the set of barrier certificates is convex. If $f$ is polynomial and $X_0 = \{g_0 \ge 0\}$, $X_u = \{g_u \ge 0\}$ and $X = \{g \ge 0\}$ are semialgebraic, a sufficient condition is that there are a polynomial $B$, a constant $\epsilon > 0$, and sums of squares $\sigma_0$, $\sigma_u$, $\sigma$ with

$$-B - \sigma_0 g_0, \qquad B - \epsilon - \sigma_u g_u, \qquad -\nabla B \cdot f - \sigma g \qquad \text{all sums of squares}.$$

A polynomial of degree $2d$ in $n$ variables is a sum of squares if and only if it equals $z^T G z$ for a positive semidefinite $G$, where $z$ lists the $\binom{n + d}{d}$ monomials of degree at most $d$. So each condition is a semidefinite constraint with a matrix of that size, and the coefficients of $B$ and of the multipliers are the decision variables. For $n = 2$ and $d = 2$ the matrices are $6 \times 6$; for $n = 6$ and $d = 3$ they are $84 \times 84$. The size grows fast with $n$ and $d$, and this limits the method to systems of moderate dimension.

**Variants of the definition.**

- *Zero level only.* It is enough that $\nabla B \cdot f < 0$ where $B(x) = 0$, but the set of such $B$ is not convex, so the convex condition on all of $X$ is the one used for search.
- *Hybrid systems.* One function $B_q$ for each location $q$, the conditions above in each location, and a condition at each jump that the reset map keeps the state in the zero sublevel set of the function of the new location (Prajna and Jadbabaie 2004).
- *Stochastic systems.* For a stochastic differential equation, a nonnegative $B$ whose expected value does not increase (a [martingale](/martingale/) argument) bounds the probability of ever reaching $X_u$ by $\sup_{X_0} B / \inf_{X_u} B$ (Prajna, Jadbabaie and Pappas 2007).

## Examples and non-examples

**Example (a scalar contraction).** For $x' = -x$, $X_0 = [-1, 1]$ and $X_u = \{|x| \ge 2\}$, take $B(x) = x^2 - 1$. Then $B \le 0$ on $X_0$, $B \ge 3$ on $X_u$, and $\nabla B \cdot f = -2x^2 \le 0$.

**Example (a level set of a Lyapunov function).** For $x_1' = x_2$, $x_2' = -x_1 - x_2$, the Lyapunov equation $A^T P + PA = -I$ gives $P = \begin{pmatrix} 3/2 & 1/2 \\ 1/2 & 1 \end{pmatrix}$, and $V = x^T P x$ has $V' = -\|x\|^2$. Let $X_0$ be the disk of radius $0.5$ and $X_u = \{x_1 \ge 1\}$. On $X_0$, $V \le 0.25\,\lambda_{\max}(P) = 0.25 \cdot 1.809 = 0.452$. On $X_u$, $V \ge \min_{x_2}(1.5 + x_2 + x_2^2) = 1.25$, at $x_2 = -0.5$. So $B = V - 0.46$ is a barrier certificate.

**Example (safe but not asymptotically stable).** For the harmonic oscillator $x_1' = -x_2$, $x_2' = x_1$, with $X_0$ the unit disk and $X_u = \{\|x\| \ge 1.5\}$, $B = x_1^2 + x_2^2 - 1$ has $\nabla B \cdot f = 0$. It proves safety, although no solution converges to the origin. A barrier certificate needs no decrease to zero, only no increase.

**Non-example (an unsafe system).** For $x' = x$, $X_0 = [-1, 1]$ and $X_u = \{|x| \ge 2\}$, the solution from $x_0 = 1$ is $e^t$, which reaches $2$ at $t = \ln 2$. So no barrier certificate exists. The candidate $B = x^2 - 1$ meets the first two conditions, but $\nabla B \cdot f = 2x^2 > 0$.

**Non-example (the third condition only on the sets).** A function that decreases on $X_0$ and on $X_u$ but increases between them proves nothing: the condition on the derivative must hold on all of $X$, or at least on the zero level set of $B$, which is where a solution would cross.

## Related definitions

- **[Lyapunov function](/lyapunov-function/).** A Lyapunov function is positive definite and decreases, and proves stability. A barrier certificate has no sign condition at an equilibrium and need not decrease strictly. A sublevel set of a Lyapunov function that contains $X_0$ and misses $X_u$ gives a barrier certificate, as in the second example.
- **[Control barrier function](/control-barrier-function/).** For a system with an input, a control barrier function $h$ asks that some input makes $h$ satisfy a decrease condition, with the safe set $\{h \ge 0\}$; the sign convention is the opposite. It is a tool for design: it gives a set of safe inputs at each state (Ames et al. 2019). A barrier certificate is a tool for verification of a closed system.
- **[CBF safety filter](/cbf-safety-filter/).** The online quadratic program that picks the safe input closest to a nominal input, using a control barrier function (Ames, Xu, Grizzle and Tabuada 2017).
- **[Positively invariant set](/positively-invariant-set/).** The set $\{B \le 0\}$ of a barrier certificate is positively invariant, for solutions that stay in $X$, and it contains $X_0$ and misses $X_u$.
- **[Reachable set](/reachable-set-computation/).** The set $\{B \le 0\}$ contains the reachable set from $X_0$, so a barrier certificate is a reachable set over-approximation in implicit form. [Hamilton-Jacobi reachability](/hamilton-jacobi-reachability/) computes the reachable set itself on a grid, instead of a certificate.
- **Converse results.** Wisniewski and Sloth (2016) gave conditions under which a safe system has a barrier certificate, so the search is not hopeless by construction. Prajna and Rantzer (2007) gave convex certificates for the dual property, that solutions do reach a target set.

## References
