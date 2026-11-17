---
tag: ET1T47
kind: technique
slug: wright-fisher-diffusion
name: Wright-Fisher diffusion
aliases:
- diffusion approximation in population genetics
- Kimura diffusion
area: biology/population-genetics
level: advanced
summary: Approximate allele frequency dynamics in a large population by a diffusion process, and solve its Kolmogorov equations for fixation and sojourn times.
prereqs: [wright-fisher-model, stochastic-differential-equation]
see_also: [kimura-fixation-probability, wright-fisher-model, moran-model, genetic-drift, stochastic-differential-equation, euler-maruyama-method, site-frequency-spectrum, heat-equation]
sources:
  - paper: doi:10.1093/genetics/47.6.713
    title: Motoo Kimura, On the probability of fixation of mutant genes in a population, Genetics 47(6), 1962
    locator: pp. 713-719 (the backward equation for the fixation probability and its solution with the scale function)
  - paper: "Motoo Kimura, Solution of a process of random genetic drift with a continuous model, Proceedings of the National Academy of Sciences of the USA, 1955"
    title: Kimura 1955
    locator: the solution of the forward equation for neutral drift
  - paper: "Motoo Kimura, Diffusion models in population genetics, Journal of Applied Probability, 1964"
    title: Kimura 1964
    locator: a survey of the diffusion method for gene frequencies
  - book: isbn:9780387201917
    title: Warren J. Ewens, Mathematical Population Genetics I, Theoretical Introduction, 2nd edition, Springer, 2004
    locator: Section 4.2 (the Kolmogorov equations, p. 137), Section 4.3 (fixation probabilities, p. 139), Section 4.4 (absorption time, p. 140), Section 4.5 (the stationary distribution, p. 145) and Section 5.7 (diffusion approximations and boundary conditions, p. 176)
---

The Wright-Fisher diffusion replaces the discrete allele count of a large population by a continuous frequency that moves like a diffusion process. The mean and variance of the change in one generation fix the drift and diffusion coefficients, and questions about the population become ordinary or partial differential equations: the backward equation gives fixation probabilities and mean times, and the forward equation gives the density of the frequency. Kimura made this the main tool of theoretical population genetics. It is an approximation, good when the population is large and selection and mutation are weak, and this page shows where it breaks.

## In plain words

In a big population, the share of a gene variant changes only a little in each generation, partly by chance and partly by selection. Over many generations these small steps look like the path of a particle that is pushed by a weak wind (selection) and shaken at random (chance). The shaking is strongest when the variant is at middle frequency and dies out when the variant is lost or fixed. Physicists have tools for such particles: the answer to "where does it end up?" or "how long does it take?" is the solution of one equation. The technique replaces the real, step-by-step population by this particle, solves the equation, and so gives simple formulas. The price is a small error, which grows when the population is small or selection is strong.

## When it applies

- **A large population.** $N$ diploid individuals ($2N$ copies), with $N$ large. The change of frequency per generation is then small, of order $1/\sqrt N$.
- **Weak forces on the scale of drift.** The selection coefficient $s$ and mutation rate $\mu$ are of order $1/N$, so that $Ns$ and $N\mu$ stay fixed as $N$ grows. Then selection, mutation and drift all act on the same time scale of $N$ generations.
- **Finite offspring variance.** The model is Wright-Fisher, Moran or another exchangeable model in which no individual has a large share of the next generation. Then only the mean and variance of the change matter in the limit.
- **Questions on long time scales.** Fixation probabilities, mean times to absorption, sojourn times and stationary densities. The diffusion does not describe the first few generations of a single copy under strong selection; a branching process does that better.

## The template

Write $x$ for the frequency of $A$, with fitnesses $1 + s$, $1 + hs$ and $1$ for $AA$, $Aa$ and $aa$.

```pseudo id=main
DIFFUSION-APPROXIMATION(chain, question)
L1  compute M(x) = E[Δx | x] and V(x) = Var(Δx | x) for one generation, to first order in s and 1/N
L2  measure time in units of 2N generations, so the coefficients 2N M(x) and x(1 - x)/2 stay of order one as N grows with Ns fixed
L3  write the backward equation (V/2) f'' + M f' = -g for the question, with its boundary values at 0 and 1
L4  solve it with the scale density ψ(y) = exp(- ∫_0^y 2M/V): the fixation probability is u(p) = ∫_0^p ψ / ∫_0^1 ψ
L5  for mean times and sojourn densities, integrate the Green function G(p, y) of the equation over y
L6  check the result against the exact chain for a small N
```

**Line L1.** For the Wright-Fisher chain, given $x$, the next frequency is a binomial frequency with mean $x'$ (the frequency after selection) and variance $x'(1 - x')/(2N)$. To first order,

$$M(x) = s\,x(1 - x)\big(h + (1 - 2h)x\big), \qquad V(x) = \frac{x(1 - x)}{2N}.$$

**Line L2.** In units of $2N$ generations the generator is

$$\mathcal L = \tfrac12 x(1 - x) \frac{d^2}{dx^2} + 2Ns\,x(1 - x)\big(h + (1 - 2h)x\big) \frac{d}{dx}.$$

With time in units of $N$ or $4N$ generations, the factor $\tfrac12$ becomes $1$ or $2$. With Kimura's fitnesses $1$, $1 + s$, $1 + 2s$, the drift is $2Ns\,x(1-x)$ in units of $2N$ generations, and the scaled selection coefficient is $4Ns$ in the formulas.

**Lines L3 and L4.** A quantity $f(p) = \mathbb E[\,\cdot \mid x_0 = p]$ that depends only on where the path ends satisfies $\tfrac12 V f'' + M f' = 0$. For fixation the boundary values are $u(0) = 0$ and $u(1) = 1$. Writing the equation as $(f'/\psi)' = 0$ shows that $f' = c\,\psi$, which gives the formula of line L4.

**Line L5.** The mean time to absorption, in generations, solves $\tfrac12 V t'' + M t' = -1$ with $t(0) = t(1) = 0$. With $S(y) = \int_0^y \psi$,

$$t(p) = \int_0^1 G(p, y)\,dy, \quad G(p, y) = \begin{cases} 2\,(1 - u(p))\,S(y)/(V(y)\psi(y)), & y \le p,\\ 2\,u(p)\,(S(1) - S(y))/(V(y)\psi(y)), & y > p.\end{cases}$$

$G(p, y)\,dy$ is the mean number of generations that the frequency spends in $(y, y + dy)$ before absorption.

**Line L6.** The implementation solves the exact Wright-Fisher chain by Gaussian elimination for $2N \le 100$ and compares it with the diffusion, in a regime where the error is small and in one where it is large.

## Classic examples

**Neutral fixation and absorption time.** With $s = 0$, $\psi = 1$, so $u(p) = p$, which is also exact for the chain. The Green function is $4N(1 - p)/(1 - y)$ for $y \le p$ and $4Np/y$ for $y > p$, and the integral is

$$t(p) = -4N\big(p \ln p + (1 - p)\ln(1 - p)\big) \text{ generations}.$$

| $2N$ | start | exact chain | diffusion |
|---|---|---|---|
| 20 | $p = 1/2$ | 26.229 | 27.726 |
| 100 | $p = 1/2$ | 136.602 | 138.629 |
| 20 | one copy | 7.231 | 7.941 |
| 100 | one copy | 10.537 | 11.200 |

The relative error falls from about 6 percent to 1.5 percent as $2N$ grows from 20 to 100.

**Fixation with genic selection.** With $h = 1/2$ and Kimura's form ($s \to 2s$), $\psi(y) = e^{-4Nsy}$ and $u(p) = (1 - e^{-4Nsp})/(1 - e^{-4Ns})$. This is the [Kimura fixation probability](/kimura-fixation-probability/). For $N = 50$ and $s = 0.01$, one new copy fixes with probability $0.022901$ in the diffusion and $0.022793$ in the exact chain, an error of $0.5$ percent.

**Dominance.** With general $h$, $\psi(y) = \exp(-4Ns(hy + (1 - 2h)y^2/2))$ has no closed integral, but a numerical integral is easy. For $N = 50$, $s = 0.1$ and one copy, the diffusion gives $0.03567$ for a recessive allele ($h = 0$), against $0.03534$ in the chain, and $0.17094$ for a dominant one ($h = 1$), against $0.16474$. A new recessive allele is almost invisible to selection while it is rare, so it fixes nearly as rarely as a neutral one would at this $N$ ($0.01$), while the dominant allele does much better.

**Sojourn times and the frequency spectrum.** For a new neutral mutant, $p = 1/(2N)$, the Green function for $y > p$ is $4Np/y = 2/y$. So a new mutation spends on average $2\,dy/y$ generations at frequencies in $(y, y + dy)$. With new mutations arriving at rate $2N\mu$ per generation, the expected number of sites at frequency $y$ is $4N\mu\,dy/y = \theta\,dy/y$, the continuous form of the neutral [site frequency spectrum](/site-frequency-spectrum/).

**The stationary density with mutation.** With mutation from $A$ to $a$ at rate $u$ and back at rate $v$ per generation, $M(x) = v(1 - x) - ux$. The forward equation has the stationary density $\phi(x) \propto \exp\big(\int 2M/V\big)/V$, which is

$$\phi(x) \propto x^{4Nv - 1}(1 - x)^{4Nu - 1},$$

a beta density (Ewens 2004, Section 4.5). For $4Nu, 4Nv < 1$ it is U-shaped (drift wins and most loci are near loss or fixation); for $4Nu = 4Nv = 1$ it is flat; for larger values it peaks near $v/(u + v)$.

## Variations

- **Other population models.** The Moran model of $N$ haploid individuals has the same limit with time in units of $N^2/2$ steps, which is $N/2$ generations. A Cannings model with offspring variance $\sigma^2$ uses $V(x) = \sigma^2 x(1 - x)/(2N)$. In all cases one can write $N_e$ in place of $N$ in $V$, with $N_e$ the [effective population size](/effective-population-size/).
- **The forward equation.** The density $\phi(x, t)$ of the frequency solves $\partial_t \phi = \tfrac12 \partial_x^2(V\phi) - \partial_x(M\phi)$. Kimura (1955) solved it for neutral drift as a series of eigenfunctions; the eigenvalues $j(j+1)/2$ (in units of $2N$ generations) match the eigenvalues of the discrete chain to first order. For constant coefficients the forward equation is the [heat equation](/heat-equation/).
- **Many alleles.** For $K$ alleles the frequencies move on a simplex, with covariance $-x_i x_j/(2N)$ between different alleles.
- **Stochastic differential equation.** The frequency solves $dX = M(X)\,dt + \sqrt{V(X)}\,dW$ (time in generations), a [stochastic differential equation](/stochastic-differential-equation/). The [Euler-Maruyama method](/euler-maruyama-method/) simulates it, with care at the boundaries.
- **Changing population size.** With $N(t)$, the variance term carries $1/N(t)$, and time can be rescaled so that it becomes constant.

## Pitfalls

- **The time unit.** The generator $\tfrac12 x(1 - x)\,d^2/dx^2$ belongs to time in units of $2N$ generations. Per generation the diffusion term is $x(1 - x)/(4N)$. Mixing units gives answers that are off by a factor 2 or 4.
- **The definition of s.** Kimura's genic form $1, 1 + s, 1 + 2s$ gives $4Ns$ in the exponent; the form $1, 1 + s/2, 1 + s$ gives $2Ns$. Check the fitnesses before you use a formula from a paper.
- **Strong selection.** The diffusion keeps only first order terms in $s$. For $N = 10$ and Kimura's $s = 0.5$, it gives $0.63212$ for one copy, but the exact chain gives $0.56423$: 12 percent too high. Use the exact chain, or a branching process for a rare allele, when $s$ is not small.
- **Small populations.** For $2N = 20$ the neutral absorption time from $p = 1/2$ is 6 percent too high. The error is of order $1/N$.
- **Heavy-tailed offspring numbers.** If one parent can have a fraction of the next generation that does not vanish as $N$ grows, the limit is not this diffusion, and the genealogy is a coalescent with multiple mergers.
- **Numerical work at the boundaries.** $V(x)$ vanishes at 0 and 1, so explicit schemes can step outside $[0, 1]$. Keep the frequency in range, or work with the backward equation, which has smooth solutions here.

## Exercises

1. Derive $M(x)$ and $V(x)$ for the fitnesses $1 + s$, $1 + hs$ and $1$, and show that $M(x) = sx(1 - x)/2$ when $h = 1/2$.
2. Compute the neutral Green function and integrate it to get $t(p) = -4N(p \ln p + q \ln q)$. Show that $t(1/(2N)) \approx 2 + 2\ln(2N)$ generations.
3. Expand Kimura's formula for small $4Ns$ and show that $u(p) \approx p + 2Ns\,p(1 - p)$.
4. Find the stationary density for $4Nu = 4Nv = 1$ and for $4Nu = 4Nv = 1/2$, and say which one is U-shaped.
5. Show that the Moran model with $N$ haploid individuals has $V(x) = 2x(1 - x)/N$ per generation, and find its effective size on the Wright-Fisher scale.

## References
