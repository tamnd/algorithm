---
tag: ZCK1AD
kind: theorem
slug: kimura-fixation-probability
name: Kimura fixation probability
aliases:
- probability of fixation
area: biology/population-genetics
level: core
summary: "Under the diffusion approximation, a new additive mutant with advantage s in a diploid population of size N fixes with probability (1 - e^(-2s)) / (1 - e^(-4Ns)), and 1/(2N) if neutral."
prereqs: [wright-fisher-model, wright-fisher-diffusion]
see_also: [wright-fisher-diffusion, wright-fisher-model, moran-model, genetic-drift, effective-population-size, galton-watson-process, branching-process-extinction-theorem, mutation-selection-balance]
sources:
  - paper: doi:10.1093/genetics/47.6.713
    title: Motoo Kimura, On the probability of fixation of mutant genes in a population, Genetics 47(6), 1962
    locator: pp. 713-719 (the backward equation for the fixation probability and the formula for a new mutant with genic selection)
  - paper: doi:10.1017/S0305004100015644
    title: J. B. S. Haldane, A mathematical theory of natural and artificial selection, Part V, Selection and mutation, Proceedings of the Cambridge Philosophical Society 23(7), 1927
    locator: pp. 838-844 (the survival probability of about 2s for a single advantageous mutant)
  - book: isbn:9780387201917
    title: Warren J. Ewens, Mathematical Population Genetics I, Theoretical Introduction, 2nd edition, Springer, 2004
    locator: Section 4.3 (fixation probabilities, p. 139) and Section 5.3 (diffusion theory with selection, p. 165)
---

Kimura's formula gives the probability that an allele with a small selective advantage spreads to the whole population and does not get lost by chance. It is the exact solution of the [Wright-Fisher diffusion](/wright-fisher-diffusion/), so for a real finite population it is an approximation, good when $N$ is large and $s$ is small. For a single new copy the answer is about $2s$ when selection is strong compared with drift and about $1/(2N)$ when it is weak.

## Statement

**The setting.** A diploid population of constant size $N$ ($2N$ gene copies) that follows the [Wright-Fisher model](/wright-fisher-model/), so its effective size is $N_e = N$. One locus has two alleles, and the genotypes $aa$, $Aa$ and $AA$ have fitnesses $1$, $1 + s$ and $1 + 2s$ (genic or additive selection, Kimura's form). There is no further mutation. In the diffusion limit, the frequency $x$ of $A$ has, per generation, the mean change $M(x) = s\,x(1 - x)$ and the variance $V(x) = x(1 - x)/(2N)$.

**Theorem (Kimura 1962).** In this diffusion, the probability that $x$ reaches 1 before 0, from the start $x_0 = p$, is

$$u(p) = \frac{1 - e^{-4Nsp}}{1 - e^{-4Ns}} \quad (s \ne 0), \qquad u(p) = p \quad (s = 0).$$

For a new mutant, a single copy with $p = 1/(2N)$,

$$u\Big(\frac{1}{2N}\Big) = \frac{1 - e^{-2s}}{1 - e^{-4Ns}}.$$

The formula for $s \ne 0$ tends to $p$ as $s \to 0$, so $u$ is continuous in $s$. Here $s$ can be negative.

## In plain words

When a new useful gene variant appears, it is in one individual only. Even if it helps, that individual can by bad luck have few offspring, and the variant can be lost in the first generations. Kimura's result says how often the variant escapes this early danger and takes over. If selection is strong compared with chance, about twice the advantage: a variant with a 1 percent advantage wins about 2 times in 100. If chance is strong, because the population is small, the advantage does not matter much, and the variant wins about as often as a neutral one, which is one divided by the number of gene copies. A harmful variant can still win, but this becomes very rare as the population grows.

## Proof

**The equation.** Let $u(p)$ be the probability of fixation from frequency $p$. One generation moves $p$ to $p + \Delta x$, and the process then starts again, so $u(p) = \mathbb E[u(p + \Delta x)]$. A Taylor expansion with $\mathbb E[\Delta x] = M(p)$ and $\mathbb E[(\Delta x)^2] = V(p) + O(s^2)$ gives, to first order,

$$\tfrac12 V(p)\,u''(p) + M(p)\,u'(p) = 0, \qquad u(0) = 0, \quad u(1) = 1.$$

For the diffusion this step is exact: the generator of the diffusion is $\mathcal L f = \tfrac12 V f'' + M f'$, and a function with $\mathcal L u = 0$ makes $u(X_t)$ a bounded martingale. The diffusion reaches 0 or 1 in finite time with probability 1, so optional stopping gives $u(p) = \mathbb E[u(X_\tau)] = \Pr(X_\tau = 1)$, which is the fixation probability.

**The solution.** With $M = s\,x(1 - x)$ and $V = x(1 - x)/(2N)$, the factor $x(1 - x)$ cancels, and the equation is

$$u'' + 4Ns\,u' = 0.$$

So $u'(x) = C e^{-4Nsx}$ and $u(p) = C(1 - e^{-4Nsp})/(4Ns)$ with $u(0) = 0$. The condition $u(1) = 1$ fixes $C = 4Ns/(1 - e^{-4Ns})$, which gives the formula. For $s = 0$ the equation is $u'' = 0$ and $u(p) = p$. A linear equation of second order with two boundary values has only one solution, so this is the fixation probability. $\square$

For other fitnesses the same proof gives $u(p) = \int_0^p \psi / \int_0^1 \psi$ with $\psi(y) = \exp(-\int_0^y 2M/V)$, which has no closed form when there is dominance.

## Consequences

**Neutral alleles.** With $s = 0$, a new mutant fixes with probability $1/(2N)$. This is exact for the chain too, because the count is a martingale. If new neutral mutations arise at rate $2N\mu$ per generation, they fix at rate $2N\mu \cdot 1/(2N) = \mu$, which does not depend on $N$. This is the basis of the neutral theory of molecular evolution and of the molecular clock.

**Haldane's 2s.** If $4Ns \gg 1$, then $e^{-4Ns} \approx 0$ and $u(1/(2N)) \approx 1 - e^{-2s} \approx 2s$. Haldane (1927) found $2s$ with a branching process: a rare copy has a Poisson number of offspring copies with mean $1 + s$, and the survival probability of such a [Galton-Watson process](/galton-watson-process/) is the positive root of $1 - x = e^{-(1 + s)x}$, which is about $2s$ for small $s$ (see the [branching process extinction theorem](/branching-process-extinction-theorem/)). Most advantageous mutations are lost: a 1 percent advantage still means loss in 98 cases of 100.

**Nearly neutral alleles.** The product $Ns$ decides whether selection or drift dominates. For $N = 100$ and one new copy:

| $s$ | $4Ns$ | $u(1/(2N))$ | compared with $1/(2N) = 0.005$ |
|---|---|---|---|
| $-0.01$ | $-4$ | $0.000377$ | 13 times smaller |
| $-0.001$ | $-0.4$ | $0.004071$ | 19 percent smaller |
| $0.001$ | $0.4$ | $0.006060$ | 21 percent larger |
| $0.01$ | $4$ | $0.020171$ | about $2s$ |

When $|4Ns|$ is below about 1, the allele behaves almost as a neutral one, and slightly deleterious alleles fix often. For $s < 0$ and $4N|s| \gg 1$, $u(1/(2N)) \approx 2|s|\,e^{-4N|s|}$, which falls fast as $N$ grows.

**Effective size.** If the effective size $N_e$ differs from the census size $N$, drift uses $N_e$ while the start uses $N$: $u(p) = (1 - e^{-4N_e s p})/(1 - e^{-4N_e s})$ with $p = 1/(2N)$, so for $4N_e s \gg 1$ the single copy fixes with probability about $2s N_e/N$ (Kimura 1962). See [effective population size](/effective-population-size/).

**Fixation from a standing frequency.** With $N = 100$ and $s = 0.01$, the allele fixes with probability $0.336$ from $p = 0.1$ and $0.881$ from $p = 1/2$. Selection works well on alleles that are already common.

## Tightness

The formula is exact for the diffusion and approximate for the population. Its hypotheses are a single new copy at $1/(2N)$, $N_e = N$, genic selection and $s$ small. Each one matters.

**Comparison with the exact chain.** The table compares the formula with the exact Wright-Fisher chain (fitnesses $1$, $1 + s$, $1 + 2s$, solved by Gaussian elimination in the [Wright-Fisher diffusion](/wright-fisher-diffusion/) implementation) and with the branching approximation $1 - x = e^{-(1+s)x}$.

| $N$ | $s$ | exact chain | Kimura | branching |
|---|---|---|---|---|
| 100 | $0.001$ | $0.006060$ | $0.006060$ | |
| 100 | $0.01$ | $0.020058$ | $0.020171$ | $0.019736$ |
| 50 | $0.01$ | $0.022793$ | $0.022901$ | |
| 10 | $0.2$ | $0.303838$ | $0.329791$ | $0.313698$ |
| 10 | $0.5$ | $0.564232$ | $0.632121$ | $0.582812$ |

For small $s$ the error is below 1 percent. For $N = 10$ and $s = 0.5$, the formula is 12 percent too high. The diffusion keeps only the mean and variance of the change, to first order in $s$. The fate of a rare copy depends on its whole offspring distribution: the branching survival probability solves $1 - x = e^{-(1+s)x}$, which gives $0.583$ for $s = 0.5$, while the diffusion gives $1 - e^{-2s} = 0.632$. The two agree only to first order, $2s$. So the formula fails for strong selection in a small population; the exact chain or a branching process is better there.

**Dominance.** With fitnesses $1$, $1 + hs$, $1 + s$ and $h \ne 1/2$, the formula does not hold. A new recessive allele ($h = 0$) is almost invisible to selection while rare: for $N = 50$ and $s = 0.1$, it fixes with probability $0.0353$ in the exact chain, against $0.165$ for a dominant allele ($h = 1$). Kimura's formula for the additive case with the same homozygote effect ($s = 0.05$ in Kimura's form) gives $0.0952$, between the two.

**Offspring variance.** The formula uses the Wright-Fisher variance $x(1 - x)/(2N)$. In a [Moran model](/moran-model/) of $N$ haploid individuals with fitness $r = 1 + s$, a single mutant fixes with probability about $s$ for large $N$, not $2s$, because the offspring variance is twice as large. Replacing $N$ by $N_e$ corrects for this.

## History

Fisher (1922, 1930) and Haldane (1927) found the survival probability of about $2s$ for a single advantageous mutant in a large population, with branching processes. Wright (1931) found the stationary distributions of allele frequencies under drift. Kimura (1957, 1962) used the backward equation of the diffusion and got the formula for any $N$, $s$ and starting frequency, with the correction for $N_e$. It became the central result of his neutral theory of molecular evolution (1968).

## References
