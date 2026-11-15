---
tag: G1ZE25
kind: theorem
slug: iss-small-gain-theorem
name: ISS small-gain theorem
aliases:
- nonlinear small-gain theorem
- Jiang-Teel-Praly small-gain theorem
area: control/stability
level: research
summary: A feedback loop of two ISS systems is ISS if the composition of their nonlinear gains is less than the identity.
prereqs: [input-to-state-stability, small-gain-theorem]
see_also: [input-to-state-stability, small-gain-theorem, backstepping, lyapunov-function, control-lyapunov-function, dissipativity, passivity-theorem, converse-lyapunov-theorem]
sources:
  - paper: doi:10.1007/BF01211469
    title: Zhong-Ping Jiang, Andrew R. Teel and Laurent Praly, Small-gain theorem for ISS systems and applications, Mathematics of Control, Signals, and Systems 7(2), 95-120, 1994
    locator: the small-gain theorem for interconnected ISS systems with nonlinear gains, stated for input-to-output practical stability, and its use in design
  - paper: doi:10.1016/0005-1098(96)00051-9
    title: Zhong-Ping Jiang, Iven M. Y. Mareels and Yuan Wang, A Lyapunov formulation of the nonlinear small-gain theorem for interconnected ISS systems, Automatica 32(8), 1211-1215, 1996
    locator: the small-gain condition on ISS-Lyapunov functions and a Lyapunov function of the loop built from them
  - paper: doi:10.1007/s00498-007-0014-8
    title: Sergey Dashkovskiy, Bjorn S. Ruffer and Fabian R. Wirth, An ISS small gain theorem for general networks, Mathematics of Control, Signals, and Systems 19(2), 93-122, 2007
    locator: the small-gain condition for networks of many ISS systems with a gain matrix
  - paper: doi:10.1109/9.536498
    title: Eduardo D. Sontag and Yuan Wang, New characterizations of input-to-state stability, IEEE Transactions on Automatic Control 41(9), 1283-1294, 1996
    locator: ISS as the asymptotic gain property together with Lyapunov stability for zero input, used in the proof
  - paper: doi:10.1007/978-3-540-77653-6_3
    title: "Eduardo D. Sontag, Input to state stability: Basic concepts and results, in Nonlinear and Optimal Control Theory, Lecture Notes in Mathematics 1932, Springer, 163-220, 2008"
    locator: the survey section on the small-gain theorem for ISS systems
---

The ISS small-gain theorem is the [small-gain theorem](/small-gain-theorem/) for nonlinear gains. Two systems are connected in a loop, and each one is [input-to-state stable](/input-to-state-stability/) with the state of the other as its input. Each gain is a class $\mathcal{K}$ function, not a number, so it can be cubic for large signals and a cube root for small ones, as nonlinear systems often are. The theorem says that the loop is input-to-state stable if the composition of the two gains is less than the identity: a signal that goes once around the loop comes back smaller, at every size. For linear gains this is the classic condition that the product of the gains is less than one. Jiang, Teel and Praly proved it in 1994. It is a main tool for the robust design of nonlinear controllers, for example to show that [backstepping](/backstepping/) designs keep working when a part of the model is left out.

## Statement

**Setting.** Two systems

$$\Sigma_1: \ \dot x_1 = f_1(x_1, x_2, u), \qquad \Sigma_2: \ \dot x_2 = f_2(x_2, x_1, u),$$

with $x_i \in \mathbb{R}^{n_i}$, an external input $u \in \mathbb{R}^m$, $f_i$ locally Lipschitz and $f_i(0, 0, 0) = 0$. The comparison functions of class $\mathcal{K}$, $\mathcal{K}_\infty$ and $\mathcal{KL}$ are as in Khalil (2002, Section 4.4). For a signal $v$, $\|v\|_{[0, t]}$ is the supremum of $|v|$ on $[0, t]$, and $\|u\|$ is the essential supremum of $|u|$ on $[0, \infty)$.

**Hypotheses.** Each system is ISS in the maximum form, with the other state as one of its inputs: there are $\beta_1, \beta_2$ of class $\mathcal{KL}$ and $\gamma_{12}, \gamma_{21}, \gamma_1, \gamma_2$ of class $\mathcal{K}$ such that, for every initial state and all continuous $x_2$ and $x_1$ used as inputs,

$$|x_1(t)| \le \max\{\beta_1(|x_1(0)|, t),\ \gamma_{12}(\|x_2\|_{[0, t]}),\ \gamma_1(\|u\|)\},$$

$$|x_2(t)| \le \max\{\beta_2(|x_2(0)|, t),\ \gamma_{21}(\|x_1\|_{[0, t]}),\ \gamma_2(\|u\|)\}.$$

**Theorem (small-gain condition).** If

$$\gamma_{12}(\gamma_{21}(r)) < r \qquad \text{for all } r > 0,$$

then the loop of $\Sigma_1$ and $\Sigma_2$, with the state $x = (x_1, x_2)$ and the input $u$, is ISS. With $u = 0$, its origin is globally asymptotically stable.

## In plain words

Two systems feed each other. Each one, on its own, settles down when its input is small, and its state is at most some function of the size of its input. That function is its gain, and it need not be a straight line. Follow a disturbance once around the loop: the first system turns it into something of size given by its gain, and the second system turns that into something of size given by its own gain. If the result is always smaller than the disturbance you started with, at every size, then the loop settles down too, and outside inputs only move its state by a bounded amount. If at some size the trip around the loop gives back the same size or more, the test says nothing.

## Proof

**Step 0, the other order.** The condition also gives $\gamma_{21}(\gamma_{12}(s)) < s$ for $s > 0$. If $\gamma_{21}(\gamma_{12}(s)) \ge s$ for some $s > 0$, let $r = \gamma_{12}(s) > 0$; then $\gamma_{12}(\gamma_{21}(r)) \ge \gamma_{12}(s) = r$, since $\gamma_{12}$ is increasing, which contradicts the condition.

**Step 1, bounds and existence.** Let $[0, T)$ be the maximal interval of the solution of the loop. By causality, the two estimates hold on $[0, T)$, since the estimate at time $t$ uses the inputs on $[0, t]$ only. Fix $t < T$ and let $a_i = \|x_i\|_{[0, t]}$, which is finite by continuity, and

$$b_i = \max\{\beta_i(|x_i(0)|, 0),\ \gamma_i(\|u\|)\}.$$

Since $\beta_i(r, s) \le \beta_i(r, 0)$, the estimates give $a_1 \le \max\{b_1, \gamma_{12}(a_2)\}$ and $a_2 \le \max\{b_2, \gamma_{21}(a_1)\}$. An increasing function commutes with the maximum, so

$$a_1 \le \max\{b_1,\ \gamma_{12}(b_2),\ \gamma_{12}(\gamma_{21}(a_1))\}.$$

If $a_1 > 0$ and the maximum were the last term, then $a_1 \le \gamma_{12}(\gamma_{21}(a_1)) < a_1$, which is false. So $a_1 \le \max\{b_1, \gamma_{12}(b_2)\}$, and in the same way, with Step 0, $a_2 \le \max\{b_2, \gamma_{21}(b_1)\}$. These bounds do not depend on $t$. A solution of a locally Lipschitz equation that stays in a compact set cannot end in finite time, so $T = \infty$. The bounds also give $|x(t)| \le \sigma(|x(0)|) + \gamma_0(\|u\|)$ for all $t \ge 0$, with $\sigma$ and $\gamma_0$ of class $\mathcal{K}$ built from the $\beta_i(\cdot, 0)$ and the gains. With $u = 0$, this says that the origin is Lyapunov stable.

**Step 2, asymptotic gain.** Let $l_i = \limsup_{t \to \infty} |x_i(t)|$, which is finite by Step 1. The systems do not depend on time, so the estimate for $\Sigma_1$ also holds from any start time $\tau \ge 0$:

$$|x_1(t)| \le \max\{\beta_1(|x_1(\tau)|, t - \tau),\ \gamma_{12}(\textstyle\sup_{s \ge \tau} |x_2(s)|),\ \gamma_1(\|u\|)\} \quad \text{for } t \ge \tau.$$

The first term tends to $0$ as $t \to \infty$, because $|x_1(\tau)|$ is bounded. Then let $\tau \to \infty$; by continuity of $\gamma_{12}$, $l_1 \le \max\{\gamma_{12}(l_2), \gamma_1(\|u\|)\}$. In the same way $l_2 \le \max\{\gamma_{21}(l_1), \gamma_2(\|u\|)\}$. Substituting,

$$l_1 \le \max\{\gamma_{12}(\gamma_{21}(l_1)),\ \gamma_{12}(\gamma_2(\|u\|)),\ \gamma_1(\|u\|)\},$$

and the argument of Step 1 removes the first term: $l_1 \le \max\{\gamma_1(\|u\|), \gamma_{12}(\gamma_2(\|u\|))\}$. Likewise $l_2 \le \max\{\gamma_2(\|u\|), \gamma_{21}(\gamma_1(\|u\|))\}$. So the loop has the asymptotic gain property.

**Step 3, ISS.** The loop is a system $\dot x = f(x, u)$ with $f$ locally Lipschitz. Sontag and Wang (1996) proved that such a system is ISS if and only if it has the asymptotic gain property and its origin is Lyapunov stable for $u = 0$. Steps 1 and 2 give both properties, so the loop is ISS. With $u = 0$, the asymptotic gain gives $x(t) \to 0$, and with Step 1 the origin is globally asymptotically stable.

## Consequences

**Linear gains.** If $\gamma_{12}(r) = g_{12} r$ and $\gamma_{21}(r) = g_{21} r$, the condition is $g_{12} g_{21} < 1$, the condition of the classic [small-gain theorem](/small-gain-theorem/). The ISS version adds the effect of initial states and gives a bound on the state, not only on an output.

**Cascades.** If $\Sigma_1$ does not depend on $x_2$, then $\gamma_{12}$ can be taken as small as we like, and the condition holds. So the theorem contains the result that a cascade of ISS systems is ISS.

**The sum form.** Jiang, Teel and Praly (1994) state the result for estimates in the sum form, $\beta + \gamma_{12} + \gamma_1$, and for outputs with constant offsets, a property they call input-to-output practical stability. Passing from sums to maxima costs a factor, so their condition has the form $(\mathrm{id} + \rho_1) \circ \gamma_{12} \circ (\mathrm{id} + \rho_2) \circ \gamma_{21} \le \mathrm{id}$ with $\rho_1, \rho_2$ of class $\mathcal{K}_\infty$. Rule of thumb: in the sum form, ask that the composition of the gains is less than the identity with some margin; in the maximum form, no margin is needed.

**Lyapunov form.** Jiang, Mareels and Wang (1996) state the condition on ISS-Lyapunov functions $V_1, V_2$ of the two systems, with gains between the values of $V_1$ and $V_2$. The loop then has a Lyapunov function of the form $\max\{V_1, \sigma(V_2)\}$ with a suitable $\sigma$ of class $\mathcal{K}_\infty$. It is locally Lipschitz but not smooth in general.

**Networks.** Dashkovskiy, Ruffer and Wirth (2007) extend the theorem to networks of $N$ ISS systems with a matrix of gains $\gamma_{ij}$. In the maximum form, their condition is equivalent to a cycle condition: along every cycle of the network, the composition of the gains is less than the identity.

**Worked example, linear.** Take $\dot x_1 = -x_1 + a x_2$ and $\dot x_2 = -x_2 + b x_1$. From $x_1(t) = e^{-t}x_1(0) + \int_0^t e^{-(t-s)} a x_2(s)\, ds$, $|x_1(t)| \le e^{-t}|x_1(0)| + |a|\,\|x_2\|_{[0, t]}$. For $p, q \ge 0$ and $\varepsilon > 0$, $p + q \le \max\{(1 + 1/\varepsilon)p,\ (1 + \varepsilon)q\}$, so $\Sigma_1$ has the maximum form gain $\gamma_{12}(r) = (1 + \varepsilon)|a| r$, and $\Sigma_2$ has $\gamma_{21}(r) = (1 + \varepsilon)|b| r$. The condition is $(1 + \varepsilon)^2 |ab| < 1$, which some $\varepsilon > 0$ meets exactly when $|ab| < 1$. The true answer: the matrix $\begin{bmatrix} -1 & a \\ b & -1 \end{bmatrix}$ has the eigenvalues $-1 \pm \sqrt{ab}$, and it is Hurwitz exactly when $ab < 1$. The theorem misses the case $ab \le -1$, where the signs help, because the gains ignore signs.

**Worked example, nonlinear.** Take $\dot x_1 = -x_1 + a x_2^3$ and $\dot x_2 = -x_2^3 + x_1$.
- $\Sigma_1$: as above, $|x_1(t)| \le e^{-t}|x_1(0)| + |a|\,\|x_2\|_{[0, t]}^3$, so $\gamma_{12}(r) = (1 + \varepsilon)|a| r^3$.
- $\Sigma_2$: with $V = \frac{1}{2}x_2^2$ and $0 < \theta < 1$, $\dot V = -x_2^4 + x_2 x_1 \le -(1 - \theta)x_2^4$ whenever $|x_2|^3 \ge |x_1|/\theta$. So $|x_2|$ decreases while it is larger than $(\|x_1\|/\theta)^{1/3}$, and $|x_2(t)| \le \max\{|x_2(0)|/\sqrt{1 + 2(1 - \theta)x_2(0)^2 t},\ (\|x_1\|_{[0, t]}/\theta)^{1/3}\}$. So $\gamma_{21}(r) = (r/\theta)^{1/3}$.
- The composition is $\gamma_{12}(\gamma_{21}(r)) = (1 + \varepsilon)|a| r/\theta$. It is less than $r$ when $|a| < \theta/(1 + \varepsilon)$, and $\theta$ close to $1$ and $\varepsilon$ close to $0$ cover every $|a| < 1$. So the loop is globally asymptotically stable for $|a| < 1$.
- Check: for $0 \le a < 1$, $W = \frac{1}{2}x_1^2 + \frac{2 - a}{4}x_2^4$ gives $\dot W = -(x_1 - x_2^3)^2 - (1 - a)x_2^6$, and for $a < 0$, $W = \frac{1}{2}x_1^2 - \frac{a}{4}x_2^4$ gives $\dot W = -x_1^2 + a x_2^6$. Both are negative definite, so the true answer is $a < 1$. At $a = 1$ every point with $x_1 = x_2^3$ is an equilibrium.

The classic small-gain theorem cannot treat this loop: $\Sigma_2$ has no finite $L_\infty$ gain, since its gain behaves like $r^{1/3}$ near $0$, and the gain of $\Sigma_1$ grows like $r^3$. Only the composition is linear.

## Tightness

**No constant factor can be given away.** Take the linear example with $a = b = 1$. The gains $(1 + \varepsilon)r$ have the composition $(1 + \varepsilon)^2 r$, which is within any factor $c > 1$ of the identity for small $\varepsilon$. But every point with $x_1 = x_2$ is an equilibrium, since the eigenvalues are $0$ and $-2$, so the origin is not asymptotically stable. A version of the theorem that accepted $\gamma_{12} \circ \gamma_{21} \le c \cdot \mathrm{id}$ for some $c > 1$ would prove a false claim.

**The condition is needed at every size.** Take $\dot x_1 = -x_1 + x_2^3$ and $\dot x_2 = -x_2 + x_1$. The gains are $\gamma_{12}(r) = (1 + \varepsilon)r^3$ and $\gamma_{21}(r) = (1 + \varepsilon)r$, with the composition $(1 + \varepsilon)^4 r^3$. It is less than $r$ only for $r < (1 + \varepsilon)^{-2}$. The origin is locally exponentially stable, since the linearization has the eigenvalues $-1, -1$. But the points $(1, 1)$ and $(-1, -1)$ are also equilibria, so the origin is not globally asymptotically stable. A small-gain condition for small sizes only gives a local result.

**Only sufficient.** In the linear example, the loop is globally exponentially stable for every $ab \le -1$, where the theorem says nothing. The gains measure size only, and lose the sign information that the [passivity theorem](/passivity-theorem/) uses.

## History

Zames (1966) and Sandberg (1964) proved the small-gain theorem for linear gains in an input-output setting. Sontag (1989) introduced input-to-state stability, with class $\mathcal{K}$ gains and the effect of initial states. Jiang, Teel and Praly (1994) combined the two ideas in a small-gain theorem for ISS systems with nonlinear gains, and used it for robust nonlinear design with unmodeled dynamics. Jiang, Mareels and Wang (1996) gave the Lyapunov form, and Dashkovskiy, Ruffer and Wirth (2007) the form for networks. Sontag (2008) surveys the theory.

## References
