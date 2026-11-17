---
tag: XRWW02
kind: model
slug: hill-equation
name: Hill equation
aliases:
- Hill function
- cooperative binding curve
area: biology/systems-biology
level: core
summary: The sigmoid response x^n / (K^n + x^n) with Hill coefficient n, used for cooperative binding and switch-like gene regulation.
history:
  year: 1910
  people: [A. V. Hill]
  note: Hill fitted the oxygen binding curve of haemoglobin in 1910 with this form, with the exponent n read as the number of molecules in an aggregate.
prereqs: [mass-action-kinetics]
see_also: [michaelis-menten-kinetics, quasi-steady-state-approximation, genetic-toggle-switch, repressilator, feed-forward-loop, gene-regulatory-network, logistic-regression, chemical-reaction-network]
sources:
  - paper: "A. V. Hill, The possible effects of the aggregation of the molecules of haemoglobin on its dissociation curves, Journal of Physiology 40, 1910, iv-vii (Proceedings of the Physiological Society)"
    title: Hill 1910
    locator: the binding equilibrium of aggregates of n haemoglobin molecules with oxygen, and the fit of the curve y = K x^n / (1 + K x^n) to measured dissociation curves
  - book: isbn:9781439837177
    title: Uri Alon, An Introduction to Systems Biology, Design Principles of Biological Circuits, 2nd edition, CRC Press, 2019
    locator: Chapter 1 (transcription networks, activator and repressor input functions) and Appendix A (the input functions of genes, Michaelis-Menten and Hill equations)
  - paper: doi:10.1038/35002131
    title: Timothy S. Gardner, Charles R. Cantor and James J. Collins, Construction of a genetic toggle switch in Escherichia coli, Nature 403(6767), 2000, 339-342
    locator: the model of two mutual repressors with Hill exponents, and the need for exponents above 1 for bistability
---

The Hill equation is the curve
$$\theta(x) = \frac{x^n}{K^n + x^n},$$
the fraction of a receptor, a protein or a promoter that a ligand at concentration $x$ occupies. $K > 0$ is the concentration of half occupation, and the Hill coefficient $n > 0$ sets the steepness. For $n = 1$ it is the hyperbola of [Michaelis-Menten kinetics](/michaelis-menten-kinetics/). For $n > 1$ it is sigmoid and acts as a soft switch: the response goes from 10 percent to 90 percent while $x$ changes by the factor $81^{1/n}$ only. Gene circuit models, such as the [genetic toggle switch](/genetic-toggle-switch/) and the [repressilator](/repressilator/), use it for activation and repression.

## The machine

**The reaction scheme.** A protein $P$ binds $n$ ligand molecules $L$ at once, and the intermediates with fewer ligands are so rare that they can be ignored:
$$P + n L \;\rightleftharpoons\; P L_n .$$
This is the limit of strong cooperativity: when one site is filled, the others fill at once.

**The assumptions.**
- The binding is at equilibrium. It is fast against the process that uses $\theta$, such as transcription.
- The ligand is in excess, so its free concentration is the total concentration $x$.
- The [mass action](/mass-action-kinetics/) equilibrium holds: $[P][L]^n / [PL_n] = K_d$.

**The rate law.** The occupied fraction is $\theta = [PL_n]/([P] + [PL_n]) = x^n / (K_d + x^n)$. Write $K_d = K^n$ to get the form above, with $K$ in the unit of $x$. Some sources keep $K_d$ (in the unit of $x^n$) or write $\theta = K_a x^n/(1 + K_a x^n)$ with $K_a = 1/K_d$; Hill (1910) used this last form. This page uses $K$.

**Gene regulation.** For a gene with an activator $X$, the production rate is $f(x) = \beta\, x^n / (K^n + x^n)$; with a repressor, it is $f(x) = \beta / (1 + (x/K)^n)$, the unoccupied fraction times the maximal rate $\beta$ (Alon 2019, Chapter 1). A small basal rate $\beta_0$ is often added for a leaky promoter.

## What it counts

**The curve.** With $u = x/K$:

| $u$ | 0.25 | 0.5 | 1 | 2 | 4 |
|---|---|---|---|---|---|
| $n = 1$ | 0.2 | 0.3333 | 0.5 | 0.6667 | 0.8 |
| $n = 2$ | 0.0588 | 0.2 | 0.5 | 0.8 | 0.9412 |
| $n = 4$ | 0.0039 | 0.0588 | 0.5 | 0.9412 | 0.9961 |

At $x = K$, $\theta = 1/2$ for every $n$. The curve for $n$ at $u$ equals the curve for $n = 1$ at $u^n$: so $n = 2$ at $u = 2$ gives $4/5$, as $n = 1$ does at $u = 4$.

**Steepness.** $\theta = 0.1$ at $u = 9^{-1/n}$ and $\theta = 0.9$ at $u = 9^{1/n}$, so $x_{90}/x_{10} = 81^{1/n}$: 81 for $n = 1$, 9 for $n = 2$ and 3 for $n = 4$. The slope at the midpoint is $\theta'(K) = n/(4K)$. The logarithmic gain is
$$\frac{d \ln \theta}{d \ln x} = n\,(1 - \theta),$$
close to $n$ for small $x$. A 1 percent change of a small input changes the output by about $n$ percent.

**The Hill plot.** $\ln\frac{\theta}{1 - \theta} = n \ln x - n \ln K$. So the plot of the log odds against $\ln x$ is a line with slope $n$, and $\theta$ is the logistic function of $n(\ln x - \ln K)$. For real data the plot is not a line, and the *Hill coefficient* $n_H$ of the data is its slope at $\theta = 1/2$.

## Relation to other models

- **[Michaelis-Menten kinetics](/michaelis-menten-kinetics/).** The case $n = 1$ has the same form. Michaelis-Menten comes from a steady state of catalysis, the Hill equation from a binding equilibrium.
- **Models with intermediates.** Real proteins fill their sites one at a time. The Adair scheme (Adair 1925) gives each step its own constant, and the Monod-Wyman-Changeux and Koshland-Nemethy-Filmer models explain the constants by changes of shape. There is no page for these models here. The Hill curve is the limit where the intermediates vanish, and it fits their middle part.
- **Gene circuits.** The [toggle switch](/genetic-toggle-switch/) needs $n > 1$ for two stable states. The [repressilator](/repressilator/) needs a large enough $n$ to oscillate. A [feed-forward loop](/feed-forward-loop/) is often modeled with Hill functions or with their step limit $n \to \infty$.
- **The step limit.** As $n \to \infty$, $\theta(x) \to 0$ for $x < K$ and $1$ for $x > K$. Boolean models of [gene regulatory networks](/gene-regulatory-network/) use this limit.
- **[Logistic regression](/logistic-regression/).** A fit of the Hill curve in $\ln x$ is a logistic curve with slope $n$ and midpoint $\ln K$.

## Known results in the model

**The Hill coefficient of two sites is at most 2.** Take two sites with the binding polynomial $Q(x) = 1 + a x + b x^2$ ($a, b > 0$, Adair constants). The fraction of filled sites is $\theta = (a x + 2 b x^2)/(2 Q)$, and the Hill coefficient at $\theta = 1/2$ is
$$n_H = \frac{2}{1 + a/(2\sqrt b)} .$$
*Proof.* $\theta = 1/2$ gives $a x + 2 b x^2 = 1 + a x + b x^2$, so $b x^2 = 1$ and $x = 1/\sqrt b$. Next, $\theta/(1 - \theta) = (a x + 2 b x^2)/(2 + a x)$. Its log derivative in $\ln x$ is $\frac{a x + 4 b x^2}{a x + 2 b x^2} - \frac{a x}{2 + a x}$. Put $r = a x = a/\sqrt b$ and $b x^2 = 1$: this is $\frac{r + 4}{r + 2} - \frac{r}{r + 2} = \frac{4}{r + 2} = \frac{2}{1 + r/2}$. $\square$

So $n_H < 2$ for all $a, b > 0$, and $n_H \to 2$ only when $a \to 0$ with $b$ fixed, that is, when the singly bound state vanishes. Two independent equal sites with constant $k$ have $a = 2k$ and $b = k^2$, so $a/(2\sqrt b) = 1$ and $n_H = 1$: no cooperativity. With $a/(2\sqrt b) = 0.5$ and $0.1$, $n_H = 1.333$ and $1.818$. The same holds in general: a protein with $N$ sites has $n_H \le N$, so $n_H$ is a lower bound on the number of sites, not a count of them. A measured non-integer $n_H$ is normal.

**Repression is the mirror image.** $1/(1 + u^n) = 1 - u^n/(1 + u^n)$, so the repressor curve is $1 - \theta$, with the same 81-fold rule and the same slope at $K$ with the opposite sign.

**Stability needs the steepness.** In the symmetric toggle switch $\dot u = \alpha/(1 + v^n) - u$, $\dot v = \alpha/(1 + u^n) - v$, the symmetric state becomes a saddle when the slope of the Hill function there exceeds 1. This happens for some $\alpha$ only when $n > 1$. With $n = 1$ the toggle switch has one equilibrium for each $\alpha$. See the [genetic toggle switch](/genetic-toggle-switch/) page for the proof.

**Where the form comes from.** The Hill form is an approximation in two steps: binding at equilibrium (a fast time scale, as in the [quasi-steady-state approximation](/quasi-steady-state-approximation/)) and no intermediates (strong cooperativity). A fit of $n$ and $K$ to data is a measurement of an effective curve. It does not show that $n$ ligands bind at once.

## References
