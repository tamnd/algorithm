---
tag: 45DQ4D
kind: definition
slug: input-to-state-stability
name: Input-to-state stability
aliases:
- ISS
area: control/stability
level: advanced
summary: A system is input-to-state stable if its state is bounded by a decaying function of the initial state plus a gain function of the peak size of the input.
prereqs: [asymptotic-stability, lyapunov-function]
see_also: [iss-small-gain-theorem, lyapunov-function, converse-lyapunov-theorem, control-lyapunov-function, backstepping, bibo-stability, small-gain-theorem, dissipativity]
sources:
  - paper: doi:10.1109/9.28018
    title: Eduardo D. Sontag, Smooth stabilization implies coprime factorization, IEEE Transactions on Automatic Control 34(4), 435-443, 1989
    locator: the definition of input-to-state stability
  - paper: doi:10.1016/0167-6911(94)00050-6
    title: Eduardo D. Sontag and Yuan Wang, On characterizations of the input-to-state stability property, Systems and Control Letters 24(5), 351-359, 1995
    locator: ISS if and only if an ISS-Lyapunov function exists
  - paper: doi:10.1109/9.536498
    title: Eduardo D. Sontag and Yuan Wang, New characterizations of input-to-state stability, IEEE Transactions on Automatic Control 41(9), 1283-1294, 1996
    locator: ISS as the asymptotic gain property together with zero-input stability
  - paper: doi:10.1007/978-3-540-77653-6_3
    title: "Eduardo D. Sontag, Input to state stability: Basic concepts and results, in Nonlinear and Optimal Control Theory, Lecture Notes in Mathematics 1932, Springer, 163-220, 2008"
    locator: the survey of the definition, the Lyapunov characterization, the cascade result and the integral variant
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.4 (class K and KL functions) and Section 4.9 (input-to-state stability and the Lyapunov sufficient condition)
---

Input-to-state stability (ISS) is a stability notion for a system with an input, $\dot x = f(x, u)$. It asks that the state is bounded by two terms: one that depends on the initial state and decays to zero with time, and one that depends only on the peak size of the input and does not decay. With zero input, ISS gives global asymptotic stability of the origin; with a bounded input, the state stays bounded and ends up in a region whose size depends on the input size alone. Sontag introduced the notion in 1989. For linear systems it is the same as a [Hurwitz](/hurwitz-matrix/) matrix $A$, but for nonlinear systems [global asymptotic stability](/asymptotic-stability/) with zero input does not imply it, as an example below shows. The [ISS small-gain theorem](/iss-small-gain-theorem/) is built on it.

## Definition

**Setting.** $\dot x = f(x, u)$ with $x \in \mathbb{R}^n$ and $u \in \mathbb{R}^m$. The map $f$ is locally Lipschitz in $(x, u)$ (see [Lipschitz condition](/lipschitz-condition/)) and $f(0, 0) = 0$. Inputs are measurable and essentially bounded functions $u : [0, \infty) \to \mathbb{R}^m$, with $\|u\|_\infty = \operatorname{ess\,sup}_{t \ge 0} |u(t)|$. Here $|\cdot|$ is the Euclidean norm.

**Comparison functions** (Khalil 2002, Section 4.4). A continuous function $\alpha : [0, a) \to [0, \infty)$ is of class $\mathcal{K}$ if it is strictly increasing and $\alpha(0) = 0$. It is of class $\mathcal{K}_\infty$ if $a = \infty$ and $\alpha(r) \to \infty$ as $r \to \infty$. A continuous function $\beta : [0, a) \times [0, \infty) \to [0, \infty)$ is of class $\mathcal{KL}$ if $\beta(\cdot, s)$ is of class $\mathcal{K}$ for each fixed $s$, and $\beta(r, \cdot)$ is decreasing with $\beta(r, s) \to 0$ as $s \to \infty$ for each fixed $r$.

**Definition (Sontag 1989).** The system is input-to-state stable if there are $\beta$ of class $\mathcal{KL}$ and $\gamma$ of class $\mathcal{K}$ such that for every initial state $x(0)$ and every input $u$, the solution exists for all $t \ge 0$ and

$$|x(t)| \ \le\ \beta(|x(0)|, t) + \gamma(\|u\|_\infty) \qquad \text{for all } t \ge 0.$$

The function $\gamma$ is an ISS gain. By causality, $\|u\|_\infty$ can be replaced by the supremum of $|u|$ over $[0, t]$. The sum can be replaced by a maximum: the maximum form with $\beta$ and $\gamma$ implies the sum form with the same functions, and the sum form implies the maximum form with $2\beta$ and $2\gamma$. The maximum form is the one that the ISS small-gain theorem uses.

**ISS-Lyapunov functions.** A continuously differentiable $V : \mathbb{R}^n \to \mathbb{R}$ is an ISS-Lyapunov function if there are $\alpha_1, \alpha_2$ of class $\mathcal{K}_\infty$, $\alpha_3$ of class $\mathcal{K}$ and $\chi$ of class $\mathcal{K}$ with

$$\alpha_1(|x|) \le V(x) \le \alpha_2(|x|), \qquad |x| \ge \chi(|u|) \ \Rightarrow\ \frac{\partial V}{\partial x}(x)\, f(x, u) \le -\alpha_3(|x|).$$

An equivalent form is $\frac{\partial V}{\partial x} f(x, u) \le -\alpha(|x|) + \sigma(|u|)$ with $\alpha$ of class $\mathcal{K}_\infty$ and $\sigma$ of class $\mathcal{K}$. If an ISS-Lyapunov function exists, the system is ISS with the gain $\gamma = \alpha_1^{-1} \circ \alpha_2 \circ \chi$ (Khalil 2002, Section 4.9). Sontag and Wang (1995) proved the converse: every ISS system has an ISS-Lyapunov function, and it can be taken smooth.

**Other characterizations** (Sontag and Wang 1996). The system has the *asymptotic gain* property if there is $\gamma$ of class $\mathcal{K}$ with $\limsup_{t \to \infty} |x(t)| \le \gamma(\|u\|_\infty)$ for every solution. The system is ISS if and only if it has the asymptotic gain property and the origin of $\dot x = f(x, 0)$ is Lyapunov stable.

**Consequences.**
- *Linear systems.* $\dot x = Ax + Bu$ is ISS if and only if $A$ is Hurwitz. If $\|e^{At}\| \le k e^{-\lambda t}$ with $\lambda > 0$ (induced 2-norm), the variation of constants formula gives $|x(t)| \le k e^{-\lambda t}|x(0)| + \frac{k \|B\|}{\lambda} \|u\|_\infty$, so the gain is linear.
- *Cascades.* If $\dot x_1 = f_1(x_1, x_2)$ is ISS with $x_2$ as its input and $\dot x_2 = f_2(x_2, u)$ is ISS, then the cascade is ISS with input $u$. With $u = 0$, this gives global asymptotic stability of a cascade of an ISS system and a globally asymptotically stable one, a step that [backstepping](/backstepping/) designs use.
- *Bounded states.* An ISS system maps bounded inputs to bounded states, and the state converges to the ball of radius $\gamma(\|u\|_\infty)$ in the sense of the asymptotic gain.

## Examples and non-examples

- **A first-order lag.** $\dot x = -x + u$ gives $x(t) = e^{-t} x(0) + \int_0^t e^{-(t-s)} u(s)\, ds$, so $|x(t)| \le e^{-t}|x(0)| + \|u\|_\infty$. It is ISS with $\beta(r, t) = r e^{-t}$ and $\gamma(r) = r$.
- **A cubic sink.** $\dot x = -x^3 + u$ with $V = \frac{1}{2}x^2$: $\dot V = -x^4 + xu \le -\frac{1}{2}x^4$ whenever $|x|^3 \ge 2|u|$. So the system is ISS with $\chi(r) = (2r)^{1/3}$. From $\frac{d}{dt} x^2 \le -x^4$ outside that ball, $|x(t)| \le \max\{ |x(0)| / \sqrt{1 + x(0)^2 t},\ (2\|u\|_\infty)^{1/3} \}$. The constant input $u = 1$ gives the equilibrium $x = 1$, below the bound $2^{1/3} = 1.25992$. The gain is not linear: the input $u = \varepsilon$ gives the equilibrium $\varepsilon^{1/3}$, and the ratio $\varepsilon^{-2/3}$ has no bound as $\varepsilon \to 0$. So the system is ISS but has no finite L-infinity gain.
- **Non-example, globally asymptotically stable but not ISS.** $\dot x = -x + x^2 u$. With $u = 0$ it is $\dot x = -x$, which is globally exponentially stable. With $u = 1$ and $x(0) = 2$, the equation $\dot x = x^2 - x$ has the solution $x(t) = 1/(1 - e^t/2)$, which escapes to infinity at $t = \ln 2 = 0.69315$ s. A bounded input gives an unbounded state, so the system is not ISS. Every constant input $u = \varepsilon > 0$ does the same from $x(0) > 1/\varepsilon$.
- **Non-example, the integrator.** $\dot x = u$ is Lyapunov stable with zero input, but $u = 1$ gives $x(t) = x(0) + t$. It is not ISS, and the matrix $A = 0$ is not Hurwitz.
- **A saturated input.** $\dot x = -x + \operatorname{sat}(u)$ satisfies $|x(t)| \le e^{-t}|x(0)| + \min(\|u\|_\infty, 1)$. It is ISS with the gain $\gamma(r) = 2r/(1 + r)$, which is of class $\mathcal{K}$ and at least $\min(r, 1)$. A class $\mathcal{K}$ gain can be bounded, which is not possible for a nonzero linear gain.

## Related definitions

- [Asymptotic stability](/asymptotic-stability/) and [Lyapunov function](/lyapunov-function/): the zero-input notions that ISS extends. The [converse Lyapunov theorem](/converse-lyapunov-theorem/) has an ISS version, the result of Sontag and Wang (1995).
- [BIBO stability](/bibo-stability/) and the finite-gain stability of the [small-gain theorem](/small-gain-theorem/): input-output notions with linear gains and no initial state term. ISS bounds the state, allows nonlinear gains, and keeps the effect of the initial state.
- Integral ISS: a weaker notion, with a bound by the integral of $\sigma(|u(t)|)$ in place of the peak. The system $\dot x = -x + xu$ is integral ISS but not ISS.
- Input-to-output stability: the same bound for an output $y = h(x)$ in place of the state.
- [Dissipativity](/dissipativity/): the dissipation form of an ISS-Lyapunov function is a dissipation inequality with a supply rate that depends on the state.
- [ISS small-gain theorem](/iss-small-gain-theorem/): a feedback loop of two ISS systems is ISS if the composition of the gains is less than the identity.
- [Control Lyapunov function](/control-lyapunov-function/): input-to-state stabilization designs a feedback that makes a closed loop ISS with respect to a disturbance.

## References
