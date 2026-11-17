---
tag: EZD9HD
kind: model
slug: genetic-toggle-switch
name: Genetic toggle switch
aliases:
- Gardner-Collins toggle switch
area: biology/systems-biology
level: core
summary: "Two genes that repress each other: a bistable circuit whose nullclines cross three times when the repression is cooperative and strong enough."
history:
  year: 2000
  people: [Timothy S. Gardner, Charles R. Cantor, James J. Collins]
  note: Gardner, Cantor and Collins built the toggle switch in Escherichia coli in 2000 and used a two-variable model to choose its design.
prereqs: [hill-equation, jacobian-linearization]
see_also: [repressilator, quasi-steady-state-approximation, deficiency-zero-theorem, gene-regulatory-network, network-motif, gillespie-algorithm, bisection-method, classical-runge-kutta-4]
sources:
  - paper: doi:10.1038/35002131
    title: Timothy S. Gardner, Charles R. Cantor and James J. Collins, Construction of a genetic toggle switch in Escherichia coli, Nature 403(6767), 2000, 339-342
    locator: the model of two mutually repressing genes, its bistable region, and the construction and switching of the circuit in E. coli
  - book: isbn:9781439837177
    title: Uri Alon, An Introduction to Systems Biology, Design Principles of Biological Circuits, 2nd edition, CRC Press, 2019
    locator: Chapter 5 (positive feedback, bistability and memory)
---

The genetic toggle switch is a circuit of two genes, each of which makes a repressor of the other. If gene 1 is on, its protein keeps gene 2 off, and gene 2 then cannot repress gene 1. The opposite state is also self-sustaining. So the circuit has two stable states and keeps a memory of one bit. A pulse of an inducer that blocks one repressor moves the circuit from one state to the other, and it stays there after the pulse. Gardner, Cantor and Collins (2000) built it in *Escherichia coli*. Its model is a pair of differential equations with [Hill functions](/hill-equation/), and the question of bistability is a question about the crossings of two curves.

## The machine

**The circuit.** Repressor $U$ is made from a promoter that $V$ represses, and $V$ from a promoter that $U$ represses. Each protein is diluted by cell growth and degraded.

**The assumptions.**
- The binding of each repressor to its promoter is fast, so the [quasi-steady-state approximation](/quasi-steady-state-approximation/) gives a Hill function as the rate of synthesis.
- The mRNA is short-lived and is removed in the same way, so each gene is one variable.
- Dilution and degradation are first order with the same rate. Time is measured in units of the protein lifetime, and concentrations in units of the repression constant $K$.
- The counts are large enough for a deterministic model.

**The equations (Gardner et al. 2000).**
$$\frac{du}{dt} = \frac{\alpha_1}{1 + v^{\beta}} - u, \qquad \frac{dv}{dt} = \frac{\alpha_2}{1 + u^{\gamma}} - v.$$
Here $u$ and $v$ are the two repressor levels, $\alpha_1$ and $\alpha_2$ are the effective rates of synthesis, and $\beta$ and $\gamma$ are the Hill exponents of repression. This page writes $h(x) = \alpha/(1 + x^n)$ and studies mostly the symmetric case $\alpha_1 = \alpha_2 = \alpha$ and $\beta = \gamma = n$. An inducer that inactivates a repressor lowers its effective level in the Hill term, and so shifts one nullcline.

## What it counts

**Equilibria.** They are the crossings of the nullclines $u = h(v)$ and $v = h(u)$. For $\alpha = 10$ and $n = 2$ there are three:
$$(u, v) = (5 - \sqrt{24},\, 5 + \sqrt{24}) = (0.101021, 9.898979), \qquad (2, 2), \qquad (9.898979, 0.101021).$$

**Stability.** The [Jacobian](/jacobian-linearization/) is $\begin{pmatrix} -1 & h'(v) \\ h'(u) & -1 \end{pmatrix}$ with $h'(x) = -\alpha n x^{n-1}/(1 + x^n)^2$, and its eigenvalues are $-1 \pm \sqrt{h'(u) h'(v)}$. At the two outer points $h'(u) h'(v) = 0.04$, so the eigenvalues are $-0.8$ and $-1.2$: both are stable nodes. At $(2, 2)$, $h'(2) = -1.6$, so the eigenvalues are $0.6$ and $-2.6$: a saddle. By symmetry the diagonal $u = v$ is invariant, and it is the stable manifold of the saddle. It divides the plane into the two basins.

**Trajectories.** A [classical Runge-Kutta](/classical-runge-kutta-4/) run to $t = 30$ from $(5, 0)$ ends at $(9.898979, 0.101021)$, and from $(0, 5)$ at the mirror point. From $(1, 1.1)$, close to the diagonal, it ends at $(0.101021, 9.898979)$: the gene that starts slightly ahead wins.

**The threshold of bistability.** The symmetric equilibrium $u^* = h(u^*)$ is a saddle exactly when $|h'(u^*)| > 1$. With $\alpha = u^*(1 + u^{*n})$, this slope is $n u^{*n}/(1 + u^{*n})$. It equals $1$ at $u^{*n} = 1/(n - 1)$, so the threshold is
$$\alpha_c(n) = \frac{n}{n - 1}\,(n - 1)^{-1/n}.$$

| $n$ | 1.5 | 2 | 3 | 4 |
|---|---|---|---|---|
| $\alpha_c(n)$ | 4.7622 | 2 | 1.1906 | 1.0131 |

For $n \le 1$ the slope $n u^n/(1 + u^n)$ is below $1$ for every $u$, so there is no threshold.

## Relation to other models

- **[Hill equation](/hill-equation/).** The repression terms are Hill functions. The steepness $n$ decides whether the circuit can be bistable at all.
- **Positive feedback.** Two repressions in a loop make a positive feedback loop: an increase of $u$ lowers $v$, which raises $u$. A single gene that activates itself with a Hill exponent above 1 is the other common bistable motif (Alon 2019, Chapter 5). See [network motifs](/network-motif/) and [gene regulatory networks](/gene-regulatory-network/).
- **[Repressilator](/repressilator/).** Three repressors in a ring give negative feedback, and an oscillator instead of a switch. An odd number of repressions in a loop gives negative feedback; an even number gives positive feedback.
- **[Deficiency zero theorem](/deficiency-zero-theorem/).** A mass action network with deficiency zero cannot have two positive equilibria in one class. So any mass action reaction scheme behind a bistable toggle switch has deficiency at least 1.
- **The stochastic model.** With small numbers of molecules, noise can flip the switch. The [Gillespie algorithm](/gillespie-algorithm/) samples this; the mean time between flips grows fast with the height of the barrier between the basins.

## Known results in the model

**For $n = 2$, there are three equilibria exactly when $\alpha > 2$.** *Proof.* Equilibria satisfy $u(1 + v^2) = \alpha$ and $v(1 + u^2) = \alpha$. Subtract: $u - v + uv(v - u) = 0$, that is $(u - v)(1 - uv) = 0$. If $u = v$, then $u^3 + u - \alpha = 0$, which has exactly one positive root because the left side increases. If $uv = 1$, the first equation gives $u + v = \alpha$, so $u$ and $v$ are the roots of $x^2 - \alpha x + 1 = 0$. These are real, distinct and positive exactly when $\alpha > 2$. At $\alpha = 2$ all three equilibria meet at $(1, 1)$, a pitchfork bifurcation of the symmetric system. $\square$

**For $n = 1$, there is one equilibrium for every $\alpha$.** With $h(x) = \alpha/(1 + x)$, the map $h \circ h$ is $u \mapsto \alpha(1 + u)/(1 + \alpha + u)$, and its fixed points solve $u^2 + u - \alpha = 0$. The only positive root is $u = v = (\sqrt{1 + 4\alpha} - 1)/2$, which is $2.7016$ for $\alpha = 10$. Its slope $|h'| = u/(1 + u) < 1$, so it is stable. So a toggle switch with non-cooperative repression is never bistable.

**For general $n > 1$ and $\alpha > \alpha_c(n)$, there are at least two asymmetric equilibria.** Each equilibrium is a fixed point $u$ of $h \circ h$ with $v = h(u)$. Let $F(u) = h(h(u)) - u$. Then $F(0) = h(\alpha) > 0$, and $F(u^*) = 0$ with $F'(u^*) = h'(u^*)^2 - 1 > 0$. So $F < 0$ just below $u^*$, and $F$ has a root in $(0, u^*)$ by the intermediate value theorem. This gives the equilibrium with $u < u^* < v$, and the mirror gives the other. A [bisection](/bisection-method/) on $F$ finds them.

**Every trajectory converges to an equilibrium.** Both off-diagonal entries of the Jacobian are negative everywhere, so the system is competitive, and the change $w = -v$ makes it cooperative. A planar cooperative system has no periodic orbits, and its bounded trajectories converge to equilibria (a classical result of the theory of monotone systems). The square $[0, \alpha_1] \times [0, \alpha_2]$ attracts all trajectories, so for $\alpha > \alpha_c$ almost every start ends at one of the two stable states.

**Unequal rates.** For $\alpha_1 \ne \alpha_2$ the system is not symmetric, and the bistable region is a wedge in the $(\alpha_1, \alpha_2)$ plane that becomes narrower as the exponents decrease (Gardner et al. 2000). Outside the wedge, one gene wins for all starts. An inducer pulse moves the circuit across the edge of the wedge and back, which is how the switch is flipped.

## References
