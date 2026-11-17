---
tag: ND9J7H
kind: technique
slug: moment-closure
name: Moment closure
aliases:
- moment closure approximation
area: biology/systems-biology
level: advanced
summary: Turn the infinite chain of moment equations of a stochastic network into a finite ODE system by writing high moments in terms of low ones.
prereqs: [chemical-master-equation, variance]
see_also: [linear-noise-approximation, chemical-langevin-equation, finite-state-projection, moment-generating-function, linearity-of-expectation, stochastic-sir-model, mass-action-kinetics, newton-raphson-method]
sources:
  - paper: doi:10.1111/j.2517-6161.1957.tb00263.x
    title: Peter Whittle, On the use of the normal approximation in the treatment of stochastic processes, Journal of the Royal Statistical Society Series B 19(2), 1957, 268-281
    locator: the closure of the moment equations by setting the cumulants above order 2 to zero
  - paper: doi:10.1063/1.4934990
    title: David Schnoerr, Guido Sanguinetti and Ramon Grima, Comparison of different moment-closure approximations for stochastic chemical kinetics, Journal of Chemical Physics 143(18), 2015, 185101
    locator: the normal, Poisson, log-normal and other closures compared on networks with known solutions, and their unphysical solutions
  - paper: doi:10.1088/1751-8121/aa54d9
    title: David Schnoerr, Guido Sanguinetti and Ramon Grima, Approximation and inference methods for stochastic biochemical kinetics, a tutorial review, Journal of Physics A 50(9), 2017, 093001
    locator: the section on moment closure approximations
  - paper: doi:10.2307/3212214
    title: Donald A. McQuarrie, Stochastic approach to chemical kinetics, Journal of Applied Probability 4(3), 1967, 413-478
    locator: the moment equations of the master equation and their exact solution for first order reactions
---

Moment closure is a way to get approximate means and variances of a stochastic reaction network without solving the [chemical master equation](/chemical-master-equation/) or simulating it. From the master equation, the time derivative of each moment of the counts is an expected value of a function of the state, and for mass action that function is a polynomial. If every reaction has order 0 or 1, the equations for the moments of order up to $k$ involve only those moments, and they close. If some reaction has order 2 or more, the equation for a moment of order $k$ involves moments of order $k + 1$, and the system is an infinite chain. Moment closure cuts the chain: it assumes a form for the distribution (normal, Poisson, log-normal, or another) and writes the moments of order $k + 1$ as functions of the lower ones. The result is a small system of nonlinear ODEs. It is fast and often accurate for unimodal distributions, but it is an uncontrolled approximation: there is no error bound, and it can give negative variances or spurious steady states.

## In plain words

To know how a noisy system behaves on average, you would like an equation for the average count. But in a network where molecules meet in pairs, the average depends on how spread out the counts are. The spread depends on the lopsidedness. The lopsidedness depends on something finer still, and so on without end.

Moment closure stops this chain by a guess. It says: suppose the counts follow a familiar bell-like shape. For such a shape, the finer quantities are fixed by the average and the spread. Put that into the equations, and you get a few equations that you can solve on a computer in a moment.

The guess may be wrong, and nothing warns you when it is. So check it against an exact method on a small case first.

## When it applies

- **Moments are the question.** You want means, variances and covariances over time, not the full distribution or the probability of rare events.
- **Unimodal distributions.** The distribution has one peak and moderate skew. The closures assume a shape with one peak.
- **Too many states for exact methods.** The network has too many species or too large counts for [finite state projection](/finite-state-projection/), and simulation is too slow, for example inside a parameter fit with many evaluations.
- **Mass action or polynomial propensities.** The moment equations are then polynomial in the moments, so the closure is explicit. Other propensities need a Taylor expansion first, which adds another approximation.

## The template

1. **Moment equations.** For a function $g$ of the state, the master equation gives
$$\frac{d}{dt} \mathbb{E}[g(X)] = \sum_{j=1}^{m} \mathbb{E}\bigl[a_j(X)\, \bigl(g(X + \nu_j) - g(X)\bigr)\bigr].$$
With $g(x) = x_i$, $x_i x_k$, and so on, this gives the equations for the means, the second moments, and higher moments. In particular $\frac{d}{dt}\mathbb{E}[X] = S\, \mathbb{E}[a(X)]$.
2. **Find the order.** Expand the right sides as polynomials in $X$. If a reaction has order $r$, the equation for moments of order $k$ involves moments up to order $k + r - 1$.
3. **Choose the order of closure.** Keep the moments up to order $K$ (usually 2), and list the moments of order $K + 1$ (and higher) that appear.
4. **Choose a closure.** Write each extra moment as a function of the kept ones:
   - normal: the cumulants of order 3 and more are 0, so for one species $\mathbb{E}[X^3] = 3\mu_1\mu_2 - 2\mu_1^3$, where $\mu_k = \mathbb{E}[X^k]$;
   - Poisson: the cumulants are all equal to the mean;
   - log-normal: $\mathbb{E}[X^3] = \mu_2^3/\mu_1^3$ for one species, from the moments of a log-normal law;
   - cumulant neglect of order $K$: the cumulants above order $K$ are 0, which is the normal closure for $K = 2$.
5. **Solve.** Integrate the closed ODE system from the start moments, or solve for its steady states with [Newton's method](/newton-raphson-method/), and keep only the solutions with positive means and variances that are stable.
6. **Check.** Compare with exact simulation or with finite state projection on a small case, and change the closure or the order if they disagree.

## Classic examples

**First order networks close exactly.** For immigration-death, $\emptyset \to X$ at rate $k$ and $X \to \emptyset$ at rate $\gamma x$, the template gives $\dot\mu_1 = k - \gamma\mu_1$ and $\dot\mu_2 = k(2\mu_1 + 1) + \gamma(\mu_1 - 2\mu_2)$, with no higher moments. At steady state, $\mu_1 = k/\gamma$ and the variance is $k/\gamma$, the moments of the exact Poisson law. No closure is needed.

**Dimerization decay.** $\emptyset \to A$ at rate $k = 10$, and $2A \to \emptyset$ with propensity $c\, x(x-1)/2$, $c = 1$ (the convention $c = 2k_2/(N_A V)$ for a molar rate constant $k_2$). The second reaction removes 2 molecules. The template gives

$$\dot\mu_1 = k - c(\mu_2 - \mu_1), \qquad \dot\mu_2 = k(2\mu_1 + 1) - 2c\,(\mu_3 - 2\mu_2 + \mu_1),$$

and $\mu_3$ is not determined. At steady state the first equation gives $\mu_2 = \mu_1 + k/c$. With the normal closure, the second equation becomes the cubic $4m^3 - 6m^2 - 38m + 50 = 0$ in $m = \mu_1$, which has three real roots.

| method | stationary mean | stationary variance |
|---|---|---|
| exact (master equation) | 3.295346 | 2.436040 |
| rate equation and LNA | 3.162278 | 2.371708 |
| normal closure | 3.241154 | 2.736074 |
| log-normal closure | 3.377172 | 1.971881 |

The normal closure has a better mean than the rate equation and a worse variance (12 percent high). The log-normal closure errs the other way. Neither is always better. The other two roots of the normal closure are $m = 1.277575$ with variance 9.645, a saddle point, and $m = -3.018729$ with variance $-2.131$, which has a negative mean and a negative variance. Integrating the closed ODEs from $\mu_1 = \mu_2 = 0$ reaches the right root, but a solver for the steady state started elsewhere can return one of the others.

**Epidemics.** In the [stochastic SIR model](/stochastic-sir-model/), the infection reaction $S + I \to 2I$ has order 2, and the mean number of infected depends on $\mathbb{E}[SI]$. The closure $\mathbb{E}[SI] \approx \mathbb{E}[S]\mathbb{E}[I]$, of order 1, gives the deterministic SIR equations. Closures of order 2 add the covariance and give the effect of noise on the mean of the epidemic, for example in the early phase when counts are small.

## Variations

- **Higher order.** Keep moments up to order 3 or 4 and close the next order. This can improve accuracy, but not always, and the number of moments grows as $\binom{n + K}{K}$ for $n$ species.
- **Closures in cumulants or factorial moments.** Writing the equations in cumulants, central moments or factorial moments changes the algebra and sometimes the result of the same closure assumption. Factorial moments make the equations simpler for mass action.
- **Derivative matching and other fitted closures.** Choose the closure so that the closed system matches the time derivatives of the true moments at some point, or fit it to simulations.
- **Closure of the Langevin equation.** The same template applied to the [chemical Langevin equation](/chemical-langevin-equation/) gives other moment equations for nonlinear networks, because the CLE does not keep the higher order terms of the jumps.
- **Relation to the LNA.** The [linear noise approximation](/linear-noise-approximation/) gives the same results as the normal closure for linear networks, and for nonlinear networks it decouples the mean from the variance, while moment closure keeps them coupled.

## Pitfalls

- **Unphysical solutions.** A closed system can have steady states with negative means or variances, as in the example, and its ODEs can diverge or oscillate in finite time. Check every solution for positivity and stability.
- **No error bound.** The error of a closure is not known from the closure itself. Always check it against an exact method on a small case before using it in a parameter study.
- **Bimodal laws.** For a bistable network, such as a [genetic toggle switch](/genetic-toggle-switch/), the mean of the two peaks is a value that the system rarely takes, and closures based on one peak give wrong moments.
- **Low counts.** With counts near 0, the normal shape puts mass on negative counts, and the closure can give negative moments. The log-normal and Poisson closures avoid negative values, but they can still be wrong.
- **Conventions.** For $2A$, the propensity $c\, x(x-1)/2$ and the change of 2 molecules must both appear in the moment equations. Using $c\, x^2/2$ changes the equations by terms of lower order, which matter at low counts.
- **The order is not a guarantee.** A closure of higher order is not always more accurate, and different closures of the same order can disagree with each other more than with the exact answer.

## Exercises

1. Derive the equation for $\dot\mu_2$ of immigration-death from the template, and show that its steady state gives the variance $k/\gamma$.
2. For the dimerization decay example, derive the cubic $4m^3 - 6m^2 - 38m + 50 = 0$ from the normal closure.
3. Show that the Poisson closure, applied to the first moment equation of the dimerization decay example with $\mu_2 = \mu_1 + \mu_1^2$, gives the mean $\sqrt{k/c}$ of the rate equation.
4. Show that for a log-normal law $\mathbb{E}[X^3] = \mathbb{E}[X^2]^3/\mathbb{E}[X]^3$.
5. For a network with one species and one reaction $3A \to \emptyset$ of order 3, find the highest moment that appears in the equation for $\mathbb{E}[X^2]$.

## References
