---
tag: QX46AW
kind: model
slug: repressilator
name: Repressilator
aliases:
- Elowitz-Leibler oscillator
area: biology/systems-biology
level: core
summary: A ring of three genes, each repressing the next, which oscillates when the repression is steep and strong enough to destabilize the single equilibrium.
history:
  year: 2000
  people: [Michael B. Elowitz, Stanislas Leibler]
  note: Elowitz and Leibler built the repressilator in Escherichia coli in 2000 from three repressor genes and used a model of mRNA and protein to choose its parameters.
prereqs: [hill-equation, limit-cycle]
see_also: [genetic-toggle-switch, lyapunov-stability, jacobian-linearization, routh-hurwitz-criterion, eigenvalue, classical-runge-kutta-4, gillespie-algorithm, gene-regulatory-network]
sources:
  - paper: doi:10.1038/35002125
    title: Michael B. Elowitz and Stanislas Leibler, A synthetic oscillatory network of transcriptional regulators, Nature 403(6767), 2000, 335-338
    locator: the model of three repressors with mRNA and protein, the condition for the instability of its steady state, and the construction of the circuit in E. coli
  - book: isbn:9781439837177
    title: Uri Alon, An Introduction to Systems Biology, Design Principles of Biological Circuits, 2nd edition, CRC Press, 2019
    locator: Chapter 6 (how to build a biological oscillator)
---

The repressilator is a ring of three genes. The protein of gene 1 represses gene 2, the protein of gene 2 represses gene 3, and the protein of gene 3 represses gene 1. Three repressions in a loop make a negative feedback with a delay, and such a loop can oscillate: when protein 1 is high, protein 2 falls, protein 3 rises, and protein 1 then falls. Elowitz and Leibler (2000) built it in *Escherichia coli* from the repressors LacI, TetR and the cI protein of phage lambda, with a green fluorescent reporter, and saw oscillations in single cells. Their model predicts when the single equilibrium of the ring is unstable, and then the state goes to a [limit cycle](/limit-cycle/).

## The machine

**The circuit.** Gene $i$ makes mRNA $m_i$, which makes protein $p_i$. Protein $p_{i-1}$ represses gene $i$, with the indices taken modulo 3.

**The assumptions.**
- The binding of each repressor to its promoter is fast, so the rate of transcription is a [Hill function](/hill-equation/) of the repressor level, plus a small leak.
- The three genes have the same constants.
- mRNA and protein decay with first order rates. Time is in units of the mRNA lifetime, protein levels are in units of the repression constant, and mRNA levels are scaled by the translation efficiency.
- The counts are large enough for a deterministic model.

**The equations (Elowitz and Leibler 2000).**
$$\frac{dm_i}{dt} = -m_i + \frac{\alpha}{1 + p_{i-1}^{\,n}} + \alpha_0, \qquad \frac{dp_i}{dt} = -\beta\,(p_i - m_i), \qquad i = 1, 2, 3.$$
Here $\alpha + \alpha_0$ is the rate of transcription of a free promoter, $\alpha_0$ is the leak of a fully repressed one, $\beta$ is the ratio of the protein decay rate to the mRNA decay rate, and $n$ is the Hill exponent.

## What it counts

**The equilibrium.** At an equilibrium $p_i = m_i$, and the map $p \mapsto \alpha/(1 + p^n) + \alpha_0$ is decreasing, so all three genes have the same level $p^*$, the unique root of
$$p = \frac{\alpha}{1 + p^n} + \alpha_0 .$$
Put $g = \alpha n p^{*\,n-1}/(1 + p^{*n})^2$, the size of the slope of the repression at $p^*$.

**The condition for instability.** The equilibrium is unstable exactly when
$$\frac{(\beta + 1)^2}{\beta} < \frac{3 g^2}{4 - 2 g} \quad (g < 2),$$
and it is unstable for every $\beta$ when $g \ge 2$. Elowitz and Leibler wrote this with $X = -g$ as $3X^2/(4 + 2X)$. The proof is below.

**An example.** For $\alpha = 216$, $\alpha_0 = 0.216$, $\beta = 5$ and $n = 2$: $p^* = 6.018662$ and $g = 1.876423$. The left side is $7.2$ and the right side is $42.74$, so the equilibrium is unstable, with the leading eigenvalues $0.2085 \pm 1.2662\,i$. A [classical Runge-Kutta](/classical-runge-kutta-4/) run with step $0.001$ from $m = (1, 0, 0)$, $p = (2, 1, 3)$ settles after $t = 200$ on a limit cycle with period $8.69$ mRNA lifetimes, on which $p_1$ goes from $1.25$ to $59.2$. The three proteins peak in turn, in the order $p_1, p_3, p_2$, one third of a period ($2.90$) apart.

**More cases** (with $\alpha_0 = 0$ and $\beta = 1$ unless stated):

| $\alpha$ | $n$ | $p^*$ | $g$ | $(\beta+1)^2/\beta$ | $3g^2/(4 - 2g)$ | leading eigenvalue | result |
|---|---|---|---|---|---|---|---|
| 2 | 2 | 1 | 1 | 4 | 1.5 | $-0.134 \pm 0.5\,i$ | stable |
| 5 | 2 | 1.516 | 1.394 | 4 | 4.80 | $0.022 \pm 0.590\,i$ | oscillates |
| 10 | 2 | 2 | 1.6 | 4 | 9.6 | $0.095 \pm 0.632\,i$ | oscillates |
| 10 | 1.5 | 2.266 | 1.160 | 4 | 2.40 | $-0.067 \pm 0.539\,i$ | stable |
| 1000 | 1 | 31.13 | 0.969 | 4 | 1.37 | $-0.148 \pm 0.492\,i$ | stable |

## Relation to other models

- **[Genetic toggle switch](/genetic-toggle-switch/).** Two repressors in a loop give positive feedback and two stable states. Three repressors give negative feedback and one unstable state. A ring of repressors with an odd length is a candidate oscillator; with an even length it is a candidate switch.
- **The protein-only model.** If the mRNA is removed by a [quasi-steady-state approximation](/quasi-steady-state-approximation/), the model is $\dot p_i = \alpha/(1 + p_{i-1}^n) + \alpha_0 - p_i$. It oscillates only for $g > 2$, which needs $n > 2$ when $\alpha_0 = 0$ (see below). The mRNA step adds delay and makes oscillation easier.
- **Delay and negative feedback.** A single gene that represses itself with a long enough delay also oscillates. The ring is one way to build the delay from the time each stage needs to respond (Alon 2019, Chapter 6).
- **The stochastic model.** With small numbers of molecules per cell, the [Gillespie algorithm](/gillespie-algorithm/) gives noisy cycles whose period and amplitude vary from cycle to cycle, as in the measured cells.
- **[Gene regulatory networks](/gene-regulatory-network/).** Natural clocks, such as circadian circuits, combine negative feedback with delay as the repressilator does, but with more parts.

## Known results in the model

**The eigenvalues.** Linearize at $p^*$ with $X = -g$:
$$\dot{\delta m_i} = -\delta m_i + X\, \delta p_{i-1}, \qquad \dot{\delta p_i} = -\beta\, \delta p_i + \beta\, \delta m_i.$$
The [Jacobian](/jacobian-linearization/) commutes with the rotation of the three genes, so it has eigenvectors of the form $\delta m_i = M \omega^i$, $\delta p_i = P \omega^i$ with $\omega^3 = 1$. Then $(\lambda + 1) M = X \omega^{-1} P$ and $(\lambda + \beta) P = \beta M$, so
$$(\lambda + 1)(\lambda + \beta) = \beta X \omega^{-1}.$$
The six [eigenvalues](/eigenvalue/) are the roots of $\big((\lambda + 1)(\lambda + \beta)\big)^3 = (\beta X)^3$, a polynomial of degree 6 to which the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/) also applies. For $\omega = 1$ the right side $\beta X$ is negative, and both roots have real part $-(1 + \beta)/2$ or are negative reals: this mode is stable.

**The proof of the condition.** For $\omega^{-1} = e^{\mp 2\pi i/3}$ the right side is $\beta g\, e^{\pm i\pi/3}$. Put $z = \lambda + (1 + \beta)/2$. Then $(\lambda + 1)(\lambda + \beta) = z^2 - ((\beta - 1)/2)^2$, so $z^2 = D$ with
$$D = a + i b, \qquad a = \Big(\frac{\beta - 1}{2}\Big)^2 + \frac{\beta g}{2}, \qquad b = \pm\frac{\sqrt 3}{2}\, \beta g .$$
A root has $\operatorname{Re} \lambda > 0$ exactly when $\operatorname{Re}\sqrt D > q^{1/2}$ with $q = ((1 + \beta)/2)^2$. Since $(\operatorname{Re}\sqrt D)^2 = (|D| + a)/2$, this is $|D| > 2q - a$, and with $|D|^2 = a^2 + b^2$ it is equivalent to $b^2 > 4q(q - a)$ (the case $2q - a \le 0$ included, since then $q - a < 0$). Now $q - a = \beta(1 - g/2)$. So the condition is
$$\frac{3}{4}\beta^2 g^2 > (1 + \beta)^2\, \beta \Big(1 - \frac g2\Big),$$
which for $g < 2$ is the inequality above, and which holds for all $\beta$ when $g \ge 2$. $\square$

**What the condition means.** The left side $(\beta + 1)^2/\beta$ is at least $4$, with equality at $\beta = 1$. So oscillation is easiest when the protein and the mRNA have similar lifetimes. The right side grows with $g$, so oscillation needs a large slope of repression: a large $\alpha$, a small leak $\alpha_0$ and a large $n$. These are the design rules that Elowitz and Leibler drew from the model.

**$n = 1$ never oscillates.** With $\alpha_0 \ge 0$, $\alpha \le p^*(1 + p^*)$, so $g = \alpha/(1 + p^*)^2 \le p^*/(1 + p^*) < 1$. Then the right side is below $3/2$, and the left side is at least $4$. So the equilibrium is stable for every $\alpha$ and $\beta$, as in the last row of the table. In the same way, $\alpha_0 = 0$ gives $g = n p^{*n}/(1 + p^{*n}) < n$, so the protein-only model, which needs $g > 2$ (its eigenvalues are $-1 + X \omega^{-1}$, with real part $-1 + g/2$), never oscillates for $n \le 2$.

**The limit cycle.** When the equilibrium is unstable, the state does not converge to it. The ring is a monotone cyclic feedback system, and for such systems Mallet-Paret and Smith (1990) proved a Poincaré-Bendixson theorem: the limit set of a bounded trajectory is a periodic orbit or is made of equilibria and orbits that connect them. With one equilibrium that is unstable through a complex pair of eigenvalues, this gives a nonconstant periodic orbit. As a parameter moves across the instability boundary, a pair of complex eigenvalues crosses the imaginary axis, and a small cycle appears (a Hopf bifurcation). Far from the boundary the cycle has a large amplitude, as in the example. In the runs above the cycle attracts the tested starts. This is a numerical observation, not a proof of its orbital stability (see [Lyapunov stability](/lyapunov-stability/) for the definitions).

## References
