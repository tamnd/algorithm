---
tag: ZKD5QR
kind: model
slug: wright-fisher-model
name: Wright-Fisher model
aliases:
- Wright-Fisher process
area: biology/population-genetics
level: intro
summary: "A population of N diploids (2N gene copies) in discrete generations: each new copy picks a parent copy uniformly at random, so the allele count is binomial each generation."
history:
  year: 1931
  people: [Sewall Wright, Ronald A. Fisher]
  note: "Fisher (1930) and Wright (1931) used this sampling model to study random changes of gene frequencies in a finite population. It is named after both."
prereqs: [allele-frequency, binomial-distribution, markov-chain]
see_also: [moran-model, genetic-drift, wright-fisher-diffusion, kimura-fixation-probability, effective-population-size, kingman-coalescent, infinite-alleles-model, martingale]
sources:
  - paper: "Sewall Wright, Evolution in Mendelian populations, Genetics 16(2), 1931"
    title: Wright 1931
    locator: pp. 97-159 (random sampling of the gametes in a population of size N, and the loss of heterozygosity at the rate 1/(2N) per generation)
  - book: "Ronald A. Fisher, The Genetical Theory of Natural Selection, Oxford, Clarendon Press, 1930"
    title: Fisher 1930
    locator: the random survival of genes in a finite population
  - book: isbn:9780387201917
    title: Warren J. Ewens, Mathematical Population Genetics I, Theoretical Introduction, 2nd edition, Springer, 2004
    locator: Section 3.2 (the Wright-Fisher model with two alleles, p. 92), Section 3.3 (Cannings models, p. 99) and Section 4.4 (the absorption time in the diffusion approximation, p. 140)
  - book: isbn:9780801880094
    title: John H. Gillespie, Population Genetics, A Concise Guide, 2nd edition, Johns Hopkins University Press, 2004
    locator: Section 2.2 (the decay of heterozygosity) and Section 2.6 (the coalescent)
---

The Wright-Fisher model is the standard model of a finite population in population genetics. A population of $N$ diploid individuals carries $2N$ copies of a gene, generations do not overlap, and each copy of the next generation is a copy of a parent copy chosen uniformly at random. So the number of copies of an allele is a [Markov chain](/markov-chain/) whose steps are [binomial](/binomial-distribution/) draws. It is the base of the theory of [genetic drift](/genetic-drift/), of the [diffusion approximation](/wright-fisher-diffusion/) and of the [Kingman coalescent](/kingman-coalescent/).

## The machine

**The state.** One locus with two alleles, $A$ and $a$. The state is $X_t \in \{0, 1, \ldots, 2N\}$, the number of copies of $A$ in generation $t$, and $p_t = X_t/(2N)$ is the [allele frequency](/allele-frequency/). Time is in generations. For a haploid population of $N$ copies, replace $2N$ by $N$ everywhere on this page.

**The step without selection.** Each of the $2N$ copies of generation $t + 1$ picks a parent copy among the $2N$ copies of generation $t$, uniformly and independently of the other copies. So, given $X_t = i$,

$$X_{t+1} \sim \text{Binomial}\Big(2N, \frac{i}{2N}\Big), \qquad P_{ij} = \binom{2N}{j} \Big(\frac{i}{2N}\Big)^j \Big(1 - \frac{i}{2N}\Big)^{2N - j}.$$

The states 0 (loss of $A$) and $2N$ (fixation of $A$) are absorbing; all other states are transient.

**The step with selection.** Give the genotypes $AA$, $Aa$ and $aa$ the fitnesses $1 + s$, $1 + hs$ and $1$. Selection acts first, as in an infinite population, and then the $2N$ copies are drawn with the frequency $p'$ after selection. With $q = 1 - p$ and the mean fitness $\bar w = p^2(1 + s) + 2pq(1 + hs) + q^2$,

$$p' = \frac{p\,\big(p(1 + s) + q(1 + hs)\big)}{\bar w}, \qquad X_{t+1} \sim \text{Binomial}(2N, p').$$

Kimura's genic form, with fitnesses $1$, $1 + s$ and $1 + 2s$, is the case $s \to 2s$, $h = 1/2$. Mutation enters the same way: change $p'$ by the mutation step before the draw.

**A simulation.**

```pseudo id=main
WRIGHT-FISHER(i0, 2N, T, s, h)
L1  X_0 ← i0
L2  for t ← 0 to T - 1 do
L3      p ← X_t / (2N);  q ← 1 - p
L4      p' ← p (p (1 + s) + q (1 + h s)) / (p² (1 + s) + 2 p q (1 + h s) + q²)
L5      X_{t+1} ← a draw from Binomial(2N, p')
L6  return X_0, ..., X_T
```

Each generation costs one binomial draw, which takes $O(1)$ expected time with a good sampler, so $T$ generations take $O(T)$ time. The implementation stops early when $X_t$ reaches 0 or $2N$. It also builds the exact $(2N + 1) \times (2N + 1)$ transition matrix and solves for the absorption probabilities and times; the tests compare the simulation with these exact values for $2N = 20$.

**A trace.** With seed 7, $2N = 20$, no selection and $X_0 = 5$, the implementation gives $5, 3, 2, 1, 1, 0$: the allele is lost in generation 5. From 5 copies the exact chance of loss is $15/20 = 0.75$.

## What it counts

- $X_t$ and $p_t$, the count and frequency of an allele in each generation.
- The probability that an allele fixes or is lost, and the time until one of these happens.
- The expected heterozygosity $H_t = \mathbb E[2 p_t q_t]$, the chance that two copies drawn with replacement carry different alleles.
- The genealogy of a sample of copies, by following parents back in time.
- With mutation, the number of alleles and their frequencies at equilibrium, as in the [infinite alleles model](/infinite-alleles-model/).

## Relation to other models

- **[Moran model](/moran-model/).** One birth and one death per step, so generations overlap. Many results agree after a change of time scale: genetic drift is twice as fast per generation in the Moran model, which has [effective population size](/effective-population-size/) $N/2$ in Wright-Fisher units for $N$ copies.
- **Cannings models.** Wright-Fisher is the exchangeable model in which the offspring numbers of the $2N$ copies are multinomial. Other offspring laws with variance $\sigma^2$ per copy behave like a Wright-Fisher population of size $2N/\sigma^2$ copies (Ewens 2004, Section 3.3).
- **[Wright-Fisher diffusion](/wright-fisher-diffusion/).** For large $N$, with time in units of $2N$ generations and $Ns$ fixed, $p_t$ tends to a diffusion with generator $\tfrac12 x(1 - x)\,d^2/dx^2$ plus a selection drift. The [Kimura fixation probability](/kimura-fixation-probability/) is a result of this limit.
- **[Kingman coalescent](/kingman-coalescent/).** Two copies have the same parent copy with probability $1/(2N)$. With time in units of $2N$ generations, the genealogy of a sample tends to the Kingman coalescent.
- **[Galton-Watson process](/galton-watson-process/).** While an allele is rare, the copies of it reproduce almost independently with Poisson offspring numbers of mean $1 + s$ for a genic advantage $s$, so its early fate is that of a branching process.

## Known results in the model

Each result is for the neutral chain ($s = 0$) unless it says otherwise, with time in generations.

**The frequency is a martingale, and an allele fixes with probability equal to its frequency.** $\mathbb E[X_{t+1} \mid X_t] = X_t$, and $\Pr(\text{fixation} \mid X_0 = i) = i/(2N)$.

*Proof.* The mean of $\text{Binomial}(2N, i/(2N))$ is $i$, so $X_t$ is a [martingale](/martingale/). From each transient state the chain moves to 0 in one step with probability $(1 - i/(2N))^{2N} > 0$, so it is absorbed in finite time with probability 1, and the absorption time $\tau$ has a geometric tail. $X_t$ is bounded by $2N$, so the [optional stopping theorem](/optional-stopping-theorem/) gives $\mathbb E[X_\tau] = i$. Since $X_\tau \in \{0, 2N\}$, $\mathbb E[X_\tau] = 2N \Pr(X_\tau = 2N)$. $\square$

**Heterozygosity decays at the rate $1/(2N)$.** $H_t = H_0\,(1 - 1/(2N))^t$, where $H_t = \mathbb E[2 p_t q_t]$.

*Proof.* Given $p_t = p$, $p_{t+1}$ has mean $p$ and variance $pq/(2N)$. So $\mathbb E[p_{t+1}^2 \mid p_t] = p^2 + pq/(2N)$ and $\mathbb E[p_{t+1} q_{t+1} \mid p_t] = p - p^2 - pq/(2N) = pq\,(1 - 1/(2N))$. Take expectations and use induction on $t$. $\square$

For $N = 50$ and $t = 10$ the ratio is $0.99^{10} \approx 0.904382$. The half-life of the heterozygosity is about $2N \ln 2$ generations, so drift removes variation in a time of order $N$ generations.

**The variance of the frequency.** $\operatorname{Var}(p_t) = p_0 q_0 \big(1 - (1 - 1/(2N))^t\big)$, which tends to $p_0 q_0$, the variance of a frequency that is 0 or 1 with chances $q_0$ and $p_0$.

*Proof.* $\mathbb E[p_t] = p_0$ and, from the previous result, $\mathbb E[p_t q_t] = p_0 q_0 (1 - 1/(2N))^t$. Then $\operatorname{Var}(p_t) = \mathbb E[p_t] - \mathbb E[p_t q_t] - p_0^2$. $\square$

**The eigenvalues of the transition matrix.** They are $\lambda_0 = \lambda_1 = 1$ and $\lambda_j = \prod_{i=0}^{j-1} \big(1 - \tfrac{i}{2N}\big)$ for $j = 2, \ldots, 2N$.

*Proof.* For $Y \sim \text{Binomial}(n, p)$ the falling factorial moments are $\mathbb E[Y(Y-1)\cdots(Y-j+1)] = n(n-1)\cdots(n-j+1)\,p^j$. With $n = 2N$ and $p = x/(2N)$, the matrix maps the polynomial $x(x-1)\cdots(x-j+1)$ to $\lambda_j x^j$ plus a polynomial of lower degree. So in the basis of falling factorials of degree $0, \ldots, 2N$, which spans all functions on $\{0, \ldots, 2N\}$, the matrix is triangular with diagonal $\lambda_0, \ldots, \lambda_{2N}$. $\square$

The two eigenvalues equal to 1 belong to the two absorbing states. The largest other one, $\lambda_2 = 1 - 1/(2N)$, is the rate of the heterozygosity result above, and it sets the time scale of absorption.

**The time to absorption.** The exact mean comes from the linear system $(I - Q)\,t = \mathbf 1$ on the transient states. For $2N = 20$ it is $26.229$ generations from $X_0 = 10$ and $7.231$ from $X_0 = 1$. The diffusion approximation gives $-4N(p \ln p + q \ln q)$ generations, here $27.726$ and $7.941$: about 6 and 10 percent too high at this small size.

**The genealogy.** Two copies of one generation have the same parent copy with probability $1/(2N)$, so the number of generations back to their common ancestor is geometric with mean $2N$. A sample of $k$ copies loses a lineage with probability $\binom{k}{2}/(2N) + O(1/N^2)$ per generation. This gives the [Kingman coalescent](/kingman-coalescent/) in units of $2N$ generations.

**With selection.** There is no closed form for the fixation probability of the discrete chain. The implementation solves the linear system exactly. For $N = 10$ ($2N = 20$) and fitnesses $1$, $1.05$ and $1.1$, one new copy fixes with probability $0.10765$, against $0.05$ without selection and $0.11006$ by Kimura's diffusion formula.

## References
