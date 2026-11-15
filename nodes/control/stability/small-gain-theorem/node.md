---
tag: KKAMQ1
kind: theorem
slug: small-gain-theorem
name: Small-gain theorem
aliases:
- Zames small-gain theorem
area: control/stability
level: core
summary: A well-posed feedback loop of two systems with finite gains in the same signal norm (L2 or L-infinity) is finite-gain stable if the product of the two gains is less than one.
prereqs: [feedback-control-loop, bibo-stability]
see_also: [passivity-theorem, iss-small-gain-theorem, circle-criterion, h-infinity-norm, bounded-real-lemma, model-uncertainty, structured-singular-value, dissipativity]
sources:
  - paper: doi:10.1109/TAC.1966.1098316
    title: George Zames, On the input-output stability of time-varying nonlinear feedback systems, Part I, Conditions derived using concepts of loop gain, conicity, and positivity, IEEE Transactions on Automatic Control 11(2), 228-238, 1966
    locator: the small-gain theorem in extended spaces, and the conic sector form
  - paper: doi:10.1002/j.1538-7305.1964.tb04100.x
    title: Irwin W. Sandberg, A frequency-domain condition for the stability of feedback systems containing a single time-varying nonlinear element, Bell System Technical Journal 43(4), 1601-1608, 1964
    locator: the L2 stability of a loop with one nonlinear element by a contraction argument
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Sections 5.1 to 5.3 (L stability, L stability of state models, L2 gain) and Section 5.4 (feedback systems and the small-gain theorem)
  - book: isbn:9780898716702
    title: "Charles A. Desoer and M. Vidyasagar, Feedback Systems: Input-Output Properties, SIAM Classics in Applied Mathematics, 2009 (reprint of the Academic Press edition of 1975)"
    locator: Chapter 3 (the small-gain theorem and the extended spaces) and Chapter 5 (applications of the small-gain theorem)
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 9 (model uncertainty and robustness, the small-gain theorem for unstructured uncertainty)
---

The small-gain theorem gives a test for a feedback loop of two systems that uses only their gains. If each system amplifies the size of its input signal at most by a fixed factor, in the same signal norm, and the product of the two factors is less than one, then a signal that goes around the loop shrinks, and the loop is finite-gain stable: bounded inputs give bounded internal signals, with an explicit bound. The systems can be nonlinear, time-varying or infinite-dimensional, and the loop must be well posed. The test is conservative, because it ignores the phase; a worked example below shows how much it loses. The [passivity theorem](/passivity-theorem/) is the companion result that uses phase in place of gain, and the [ISS small-gain theorem](/iss-small-gain-theorem/) extends the idea to nonlinear gain functions and initial states.

## Statement

**Signals.** Fix $q \in \{2, \infty\}$ (the same proof works for every $q \in [1, \infty]$). $L_q^k$ is the space of signals $u : [0, \infty) \to \mathbb{R}^k$ with finite norm $\|u\|_{L_q}$: the energy norm $(\int_0^\infty |u|^2\, dt)^{1/2}$ for $q = 2$, and the peak $\operatorname{ess\,sup} |u(t)|$ for $q = \infty$. The truncation $u_T$ equals $u$ on $[0, T]$ and $0$ after $T$. The extended space $L_{qe}^k$ holds the signals with $u_T \in L_q^k$ for every $T \ge 0$; it contains signals that grow, such as $e^t$.

**Systems.** $H_1 : L_{qe}^m \to L_{qe}^p$ and $H_2 : L_{qe}^p \to L_{qe}^m$ are causal maps. $H_i$ is finite-gain $L_q$ stable if there are constants $\gamma_i \ge 0$ and $\beta_i \ge 0$ with

$$\|(H_i e)_T\|_{L_q} \ \le\ \gamma_i \|e_T\|_{L_q} + \beta_i \qquad \text{for every } e \in L_{qe} \text{ and every } T \ge 0.$$

**Loop.** Negative feedback with external inputs $u_1, u_2$:

$$e_1 = u_1 - H_2 e_2, \qquad e_2 = u_2 + H_1 e_1.$$

The loop is well posed if for every $u_1 \in L_{qe}^m$ and $u_2 \in L_{qe}^p$ there are unique $e_1 \in L_{qe}^m$ and $e_2 \in L_{qe}^p$ that satisfy the two equations, and the map from $(u_1, u_2)$ to $(e_1, e_2)$ is causal.

**Theorem (Zames 1966).** Suppose the loop is well posed, $H_1$ and $H_2$ are finite-gain $L_q$ stable with the same $q$, and $\gamma_1 \gamma_2 < 1$. Then for every $T \ge 0$,

$$\|e_{1T}\| \le \frac{\|u_{1T}\| + \gamma_2 \|u_{2T}\| + \beta_2 + \gamma_2 \beta_1}{1 - \gamma_1 \gamma_2}, \qquad \|e_{2T}\| \le \frac{\|u_{2T}\| + \gamma_1 \|u_{1T}\| + \beta_1 + \gamma_1 \beta_2}{1 - \gamma_1 \gamma_2},$$

with all norms in $L_q$. In particular, if $u_1, u_2 \in L_q$, then $e_1, e_2 \in L_q$, and the loop from $(u_1, u_2)$ to $(e_1, e_2)$, and to the outputs $y_1 = H_1 e_1$, $y_2 = H_2 e_2$, is finite-gain $L_q$ stable.

## In plain words

Each block in the loop can make a signal bigger, but only up to a fixed factor. Go once around the loop and the total factor is the product of the two. If that product is below one, a signal that circulates gets smaller on every turn, so it cannot build up. The size of every signal inside the loop is then at most a fixed multiple of the size of the signals that enter from outside. The test looks only at how much each block amplifies, never at the timing or the sign of what comes out. That is why it works for almost any kind of system, and also why it often says nothing about loops that are perfectly well behaved.

## Proof

Fix $T \ge 0$. By causality, $(H_2 e_2)_T$ depends only on $e_{2T}$, so truncating the loop equations gives $e_{1T} = u_{1T} - (H_2 e_2)_T$ and $e_{2T} = u_{2T} + (H_1 e_1)_T$. The triangle inequality and the gain bounds give

$$\|e_{1T}\| \le \|u_{1T}\| + \gamma_2 \|e_{2T}\| + \beta_2, \qquad \|e_{2T}\| \le \|u_{2T}\| + \gamma_1 \|e_{1T}\| + \beta_1.$$

Put the second bound into the first:

$$\|e_{1T}\| \le \|u_{1T}\| + \gamma_2 \|u_{2T}\| + \gamma_2 \beta_1 + \beta_2 + \gamma_1 \gamma_2 \|e_{1T}\|.$$

Well-posedness gives $e_1 \in L_{qe}$, so $\|e_{1T}\|$ is a finite number. Subtract $\gamma_1 \gamma_2 \|e_{1T}\|$ from both sides and divide by $1 - \gamma_1 \gamma_2 > 0$. This is the first bound; the second follows in the same way. If $u_1, u_2 \in L_q$, the right sides stay bounded as $T \to \infty$, and $\|e_{iT}\|$ increases to $\|e_i\|$, so $e_i \in L_q$. Then $\|y_{1T}\| \le \gamma_1 \|e_{1T}\| + \beta_1$ bounds $y_1$, and $y_2$ is the same. $\square$

The step "subtract from both sides" is where the extended space matters. Without $e_1 \in L_{qe}$, the inequality $a \le c + \gamma_1 \gamma_2 a$ is also true for $a = \infty$ and proves nothing.

## Consequences

**Linear systems.** For a stable proper transfer function $G$ (all poles in $\operatorname{Re} s < 0$), the $L_2$ gain is the [H-infinity norm](/h-infinity-norm/) $\|G\|_\infty = \sup_\omega \sigma_{\max}(G(j\omega))$, and $\beta = 0$ from the zero state. The $L_\infty$ gain is a different number: for a scalar $G$ it is the $L_1$ norm of the impulse response, which is at least $\|G\|_\infty$. The [bounded real lemma](/bounded-real-lemma/) computes the $L_2$ gain from a state model. A loop of two stable linear systems with $\|G_1\|_\infty \|G_2\|_\infty < 1$ is well posed, because $|G_2(\infty) G_1(\infty)| < 1$ makes $I + G_2(\infty) G_1(\infty)$ invertible.

**Robust stability.** Let $G$ be stable and $\Delta$ any stable linear system with $\|\Delta\|_\infty \le 1/\gamma$. The loop of $G$ and $\Delta$ is stable for every such $\Delta$ if $\|G\|_\infty < \gamma$. For complex unstructured $\Delta$ the converse also holds: if $\|G\|_\infty \ge \gamma$, some such $\Delta$ makes the loop unstable (Zhou, Doyle and Glover 1996, Chapter 9). This is the basis of [model uncertainty](/model-uncertainty/) descriptions with norm bounds. For structured $\Delta$ the small-gain test is again only sufficient, and the [structured singular value](/structured-singular-value/) measures the gap.

**Sector nonlinearities.** A static map $\varphi$ with $|\varphi(t, e)| \le c|e|$ has gain at most $c$ in every $L_q$. A shift and scaling of the loop (a loop transformation) turns a sector $[k_1, k_2]$ into such a bound, and the small-gain theorem then gives the [circle criterion](/circle-criterion/).

**State form.** With storage functions, the theorem is a case of a rule for loops of [dissipative](/dissipativity/) systems: $\alpha S_1 + S_2$ with $\gamma_1^2 < \alpha < 1/\gamma_2^2$ does not increase along the loop.

**Worked example.** Take $H_1 = G(s) = 2/(s + 1)$, with the dimensionless DC gain $2$ and the time constant 1 s, and $H_2 = \varphi$, a static nonlinearity with $|\varphi(t, e)| \le 0.4|e|$. Here $\|G\|_\infty = |G(0)| = 2$, and the impulse response $2e^{-t}$ has $L_1$ norm $2$, so $\gamma_1 = 2$ in $L_2$ and in $L_\infty$, with $\beta_1 = 0$ from the zero state. Also $\gamma_2 = 0.4$, so $\gamma_1 \gamma_2 = 0.8 < 1$, and the theorem gives $\|e_1\| \le (\|u_1\| + 0.4\|u_2\|)/0.2 = 5\|u_1\| + 2\|u_2\|$. The test needs $c < 1/2$ for a bound $|\varphi(e)| \le c|e|$.

**Conservatism.** For the linear gain $\varphi(e) = k e$ in the same example, the closed loop has the pole $s = -1 - 2k$, so it is exponentially stable for every $k > -1/2$. The small-gain test covers only $|k| < 1/2$. The real part of $G(j\omega) = 2/(1 + j\omega)$ is positive, so the circle criterion covers every sector $[0, \beta]$ with $\beta > 0$, a much larger set. The small-gain test throws away the phase of $G$.

**Pitfalls.**
- The two gains must be in the same norm. An $L_2$ gain of one block and an $L_\infty$ gain of the other give no result.
- Finite gain is more than boundedness. The static map $y = e^3$ maps bounded inputs to bounded outputs, but no bound $\|y_T\| \le \gamma \|e_T\| + \beta$ holds for large inputs, so it has no finite gain.
- Well-posedness is a hypothesis, not a result. The loop of the static gains $H_1 = 1$ and $H_2 = -1$ gives $0 = u_1 + u_2$, so it has no solution for most inputs. Here the product of the gains is $1$ and the theorem does not apply, but the example shows what can go wrong. For a loop of state models, well-posedness holds when the closed loop equations have a unique solution for all $t \ge 0$.

## Tightness

The condition $\gamma_1 \gamma_2 < 1$ cannot be relaxed to $\gamma_1 \gamma_2 \le 1$. Take $H_1 = 1/(s + 1)$ with $\|H_1\|_\infty = 1$ and the static gain $H_2 = -1$. Then $e_1 = u_1 + e_2$ and $e_2 = u_2 + H_1 e_1$, so $e_1 = \frac{s + 1}{s}(u_1 + u_2)$, which has a pole at $s = 0$. The input $u_1 = e^{-t}$, $u_2 = 0$ is in $L_2$, but $e_1 = \mathcal{L}^{-1}[1/s] = 1$ for $t > 0$, which is not in $L_2$.

For a fixed $G$ and the set of all stable linear $\Delta$ with $\|\Delta\|_\infty \le 1/\gamma$, the test is exact, as in the robust stability result above. For one given loop, it is only sufficient, as the worked example shows.

## History

Sandberg (1964) proved the $L_2$ stability of a loop with one time-varying nonlinear element by a contraction argument in function space. Zames (1966) stated the small-gain theorem in its general form in extended spaces, together with the conic sector and positivity results; Part II of the same paper gives the circle criterion. Desoer and Vidyasagar (1975) made the input-output approach a textbook subject. In robust control the theorem became the base of the H-infinity theory of unstructured uncertainty. Zames and Falb (1968) added multipliers, Megretski and Rantzer (1997) gave the framework of integral quadratic constraints, and Jiang, Teel and Praly (1994) gave the [ISS small-gain theorem](/iss-small-gain-theorem/) with nonlinear gains.

## References
