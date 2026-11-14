---
tag: PFFNK7
kind: technique
slug: tolerance-stack-up
name: Tolerance stack-up analysis
aliases:
- tolerance analysis
- worst-case and RSS tolerance analysis
area: cad/cam-and-additive-manufacturing
level: core
summary: Computes the variation of an assembly dimension from the tolerances of the parts, by the worst case sum or by the root sum of squares.
prereqs: [variance, central-limit-theorem]
see_also: [monte-carlo-integration, interval-arithmetic, chebyshev-inequality, hoeffding-inequality, law-of-large-numbers, convex-function, linear-programming-problem]
sources:
  - paper: doi:10.1007/BF01580066
    title: Kenneth W. Chase and Alan R. Parkinson, A survey of research in the application of tolerance analysis to the design of mechanical assemblies, Research in Engineering Design 3(1), 1991, 23 to 37
    locator: the worst case and the statistical models of a stack, the linearization of nonlinear assembly functions, Monte Carlo simulation, and tolerance allocation
  - paper: "W. H. Greenwood and K. W. Chase, A new tolerance analysis method for designers and manufacturers, Journal of Engineering for Industry 109(2), 1987, 112 to 116"
    locator: the estimated mean shift model, between the worst case and the root sum of squares
  - paper: "K. W. Chase and W. H. Greenwood, Design issues in mechanical tolerance analysis, Manufacturing Review 1(1), 1988, 50 to 59"
    locator: the assumptions of the statistical models (independence, distribution, mean shift) and the choice between the worst case and the statistical sum
---

Tolerance stack-up analysis computes how much a dimension of an assembly, such as a gap or a clearance, can vary when each part is made within its own tolerance. Each part dimension is a nominal value plus or minus a tolerance, and the assembly dimension is a function of them, most often a signed sum along a chain of dimensions. The *worst case* method adds the tolerances: it gives the exact range of a linear sum when every part is anywhere inside its tolerance, so the assembly always works if the parts are in tolerance. The *root sum of squares* (RSS) method adds the squares of the tolerances and takes the root: it gives the spread of the sum when the part errors are independent random variables, and it is much smaller than the worst case for long chains. RSS is right only under its assumptions: independent errors, centered on the nominal, with a known spread per tolerance, usually a normal distribution with the tolerance at three standard deviations. When those fail, or the function is not linear, [Monte Carlo simulation](/monte-carlo-integration/) of the assembly is the usual check. This page is about mechanical tolerances of parts. It is not the timing or the process variation analysis of chip design.

## In plain words

A shaft goes into a housing, with three spacers on it. Each piece is made a little too long or a little too short, within a tolerance printed on its drawing. Will there always be a gap at the end, or can the pieces jam?

The safe answer adds up all the tolerances, as if every piece came out at its worst at the same time. If the gap is still positive, it always fits. This is the worst case method.

But pieces are rarely all at their worst together. If the errors are random and independent, they partly cancel. Then the spread of the total grows like the square root of the sum of the squares of the tolerances, not like their sum. This is the RSS method. It lets you use looser and cheaper tolerances, but a small fraction of assemblies can then fail.

## When it applies

- An assembly requirement is a function $G = f(X_1, \dots, X_n)$ of part dimensions, such as a gap, a clearance, an overlap or a position.
- Each $X_i$ has a nominal value $\mu_i$ and a tolerance $T_i$: an accepted part has $|X_i - \mu_i| \le T_i$ (symmetric tolerances; an asymmetric one is turned into a symmetric one about its middle).
- The question is the range of $G$ (worst case), or the fraction of assemblies outside a limit (statistical), or the inverse: tolerances $T_i$ that keep $G$ within a limit at the least cost (tolerance allocation).
- For the RSS method, the $X_i$ are independent random variables with means $\mu_i$ and known standard deviations $\sigma_i$, often $\sigma_i = T_i / 3$.

## The template

**Step 1: the chain.** Write $G$ as a function of the part dimensions. For a one-dimensional chain of dimensions, $G = \sum_i a_i X_i$ with $a_i = +1$ for a dimension that increases the gap and $a_i = -1$ for one that decreases it. For a nonlinear $f$, linearize at the nominal: $a_i = \partial f / \partial x_i (\mu)$, and $G \approx f(\mu) + \sum_i a_i (X_i - \mu_i)$.

**Step 2: the nominal.** $G_0 = \sum_i a_i \mu_i$ (or $f(\mu)$).

**Step 3: the worst case.**
$$ T_{\mathrm{WC}} = \sum_i |a_i| T_i, \qquad G \in [G_0 - T_{\mathrm{WC}}, G_0 + T_{\mathrm{WC}}]. $$
*Why it is exact for a linear $G$.* Each term $a_i X_i$ ranges over $[a_i \mu_i - |a_i| T_i, a_i \mu_i + |a_i| T_i]$ independently of the others, since the box of allowed $X$ is a product. The sum of independent ranges is the sum of the intervals, and both ends are reached at corners of the box, where each $X_i$ is at the end that pushes $G$ the same way. This is [interval arithmetic](/interval-arithmetic/) on a sum, which is exact because each variable appears once.

**Step 4: the statistical sum.** If the $X_i$ are independent with standard deviations $\sigma_i$, then by the additivity of [variance](/variance/) for independent variables,
$$ \sigma_G = \sqrt{\sum_i a_i^2 \sigma_i^2}. $$
This is exact for a linear $G$ and needs no assumption on the shape of the distributions. With $\sigma_i = T_i/3$, the RSS tolerance is
$$ T_{\mathrm{RSS}} = 3 \sigma_G = \sqrt{\sum_i a_i^2 T_i^2}. $$
If every $X_i$ is normal, $G$ is normal, and $G_0 \pm T_{\mathrm{RSS}}$ holds $99.73\%$ of assemblies. If the $X_i$ are not normal, the [central limit theorem](/central-limit-theorem/) makes $G$ close to normal for many terms of similar size. That is an approximation, and it is weakest in the tails, which are what a failure rate measures.

**Step 5: compare and decide.** Always $T_{\mathrm{RSS}} \le T_{\mathrm{WC}} \le \sqrt{n}\, T_{\mathrm{RSS}}$, by the inequalities between the 1-norm and the 2-norm of the vector $(|a_i| T_i)$. Use the worst case when every assembly must work or when $n$ is small, and the statistical sum when a small, stated fraction of failures is acceptable and the assumptions hold. A bound that needs no distribution comes from the [Chebyshev inequality](/chebyshev-inequality/): $P(|G - G_0| \ge k \sigma_G) \le 1/k^2$ when the errors are centered.

**Step 6: if the assumptions fail, simulate.** Draw each $X_i$ from its distribution with a fixed seed, compute $f$, and count the failures. With $N$ samples, the estimate of a failure rate $p$ has standard error $\sqrt{p(1 - p)/N}$, so a rate of $10^{-6}$ needs many millions of samples to estimate well.

## Classic examples

**A linear stack.** A housing of length $A = 50.00 \pm 0.10$ holds three parts $B = 20.00 \pm 0.05$, $C = 15.00 \pm 0.05$ and $D = 14.80 \pm 0.05$ in a row. The end gap is $G = A - B - C - D$.

| method | tolerance on $G$ | range of $G$ | can $G < 0$? |
| --- | --- | --- | --- |
| nominal | | $0.20$ | |
| worst case | $0.10 + 3 \cdot 0.05 = 0.25$ | $[-0.05, 0.45]$ | yes |
| RSS | $\sqrt{0.10^2 + 3 \cdot 0.05^2} \approx 0.1323$ | $[0.0677, 0.3323]$ | with probability $\approx 2.9 \cdot 10^{-6}$ |

The worst case range was checked at all $16$ corners of the tolerance box. Under the RSS model, $\sigma_G = 0.1323/3 \approx 0.04410$, the nominal gap is $z = 0.20/0.04410 \approx 4.54$ standard deviations above $0$, and a normal $G$ is negative with probability $\Phi(-4.54) \approx 2.87 \cdot 10^{-6}$. A Monte Carlo run with normal errors ($\sigma_i = T_i/3$, seed 2026, $N = 400\,000$) saw $1$ negative gap, a rate of $2.5 \cdot 10^{-6}$, which agrees but is far too few events to estimate the rate. Without the normal assumption, the Chebyshev bound only gives $P(G < 0) \le 1/4.54^2 \approx 0.049$.

**The same stack with uniform errors.** If each part is spread uniformly over its whole tolerance, $\sigma_i = T_i / \sqrt 3$, so $\sigma_G \approx 0.0764$. The normal approximation then gives $P(G < 0) \approx \Phi(-0.20/0.0764) \approx 0.0044$, while a Monte Carlo run (seed 2026, $N = 400\,000$) gives $0.0012$. The sum of four uniforms has lighter tails than a normal, and the approximation is off by a factor of about $3.6$ in the tail. These are runs on one toy input, not data from a factory.

**Allocation.** Five parts of equal tolerance $t$ in a chain must keep $G$ within $\pm 0.1$. The worst case allows $t = 0.1/5 = 0.02$, and RSS allows $t = 0.1/\sqrt 5 \approx 0.0447$, more than twice as loose.

## Variations

- **Estimated mean shift.** Real processes are not centered on the nominal. Greenwood and Chase (1987) add a fraction $m_i \in [0, 1]$ of each tolerance in the worst case way and the rest statistically, $T = \sum_i m_i |a_i| T_i + \sqrt{\sum_i (1 - m_i)^2 a_i^2 T_i^2}$. With all $m_i = 0$ it is RSS, and with all $m_i = 1$ it is the worst case.
- **Inflated RSS.** A factor larger than $1$ on $T_{\mathrm{RSS}}$ is used in industry to cover the gap between the model and real processes.
- **Nonlinear functions.** The linearization of Step 1 with the same sums, or Monte Carlo on $f$ itself.
- **Two and three dimensions.** Clearances that depend on angles and positions, as in the fit of features, are modeled as a vector loop of dimensions and angles, which is nonlinear.
- **Allocation.** The inverse problem: choose the $T_i$ to minimize a cost that falls as tolerances loosen, subject to $T_{\mathrm{WC}} \le T$ or $T_{\mathrm{RSS}} \le T$. With costs $c_i / T_i$ and the worst case constraint, the Lagrange condition gives $T_i \propto \sqrt{c_i}$ for $|a_i| = 1$.

## Pitfalls

- **The worst case is not at a corner for a nonlinear $G$.** Take $G = L \cos\theta$ with $L = 10 \pm 0.01$ and $\theta = 0 \pm 0.1$ radians. The four corners give $G \in [9.9401, 9.9600]$, but the true range is $[9.9401, 10.01]$, with the maximum at $\theta = 0$ inside the box. Linearization at $\theta = 0$ is worse: $\partial G / \partial \theta = 0$ there, so the angle seems to add no variation at all. When $f$ is not monotone in each variable, find its range by optimization over the box, which is easy when $f$ is a [convex function](/convex-function/) or its negative.
- **Correlated errors.** Two dimensions machined in one setup, or from one fixture, can err together. RSS assumes independence and then underestimates the spread. With correlations $\rho_{ij}$, $\sigma_G^2 = \sum_{i,j} a_i a_j \rho_{ij} \sigma_i \sigma_j$.
- **Few terms.** With two or three terms the central limit theorem does not help, and the shape of each distribution matters. The uniform example above shows a factor of $3.6$ in the tail with four terms.
- **The three-sigma rule is a model.** $\sigma_i = T_i/3$ says that the process spread fills the tolerance at three standard deviations. A process with a better or a worse capability changes every statistical number.
- **Signs in the chain.** A dimension counted with the wrong sign, or counted twice, gives a wrong answer that no statistics repairs. Draw the chain as a loop of arrows first.
- **Tail estimates from simulation.** Rare failures need many samples. A run with no failures does not show that the rate is $0$.

## Exercises

1. Three parts with tolerances $\pm 0.1$ each form a chain. Give $T_{\mathrm{WC}}$ and $T_{\mathrm{RSS}}$. *Answer:* $0.3$ and $\sqrt{0.03} \approx 0.1732$.
2. Prove $T_{\mathrm{RSS}} \le T_{\mathrm{WC}} \le \sqrt n\, T_{\mathrm{RSS}}$, and say when each side is an equality. *Hint:* square the left side, and use the Cauchy-Schwarz inequality on the right. Equality on the left holds when at most one term is nonzero, and on the right when all the $|a_i| T_i$ are equal.
3. In the linear stack above, how large can the tolerance of $A$ be, with the others fixed, so that the worst case gap is never negative? *Answer:* $0.20 - 0.15 = 0.05$.
4. For $n$ parts with equal tolerance $t$ and an assembly limit $\pm T$, show that RSS allows $\sqrt n$ times the tolerance that the worst case allows.
5. For $G = L \cos \theta$ above, find the range of $G$ by hand, and explain why a check of the corners of the box misses the maximum.

## References
