---
tag: QM5Y7F
kind: model
slug: moran-model
name: Moran model
aliases:
- Moran process
area: biology/population-genetics
level: core
summary: "A population model with overlapping generations: at each step one individual reproduces and one dies, so the allele count is a birth-death chain that moves by at most one."
history:
  year: 1958
  people: [P. A. P. Moran]
  note: "Moran introduced the model in 1958. Because the count moves by at most one per step, many quantities that have no closed form for the Wright-Fisher model have one here."
prereqs: [wright-fisher-model, birth-death-process]
see_also: [wright-fisher-model, genetic-drift, kimura-fixation-probability, effective-population-size, wright-fisher-diffusion, kingman-coalescent, galton-watson-process, infinite-alleles-model]
sources:
  - paper: "P. A. P. Moran, Random processes in genetics, Proceedings of the Cambridge Philosophical Society 54(1), 1958"
    title: Moran 1958
    locator: pp. 60-71 (the model with one birth and one death per step, and the rate at which variation is lost)
  - book: isbn:9780387201917
    title: Warren J. Ewens, Mathematical Population Genetics I, Theoretical Introduction, 2nd edition, Springer, 2004
    locator: Section 3.4 (Moran models, p. 104), Section 3.6.4 (the Moran model with infinitely many alleles, p. 117) and Section 10.6 (exact results for the Moran model, p. 338)
  - book: isbn:9781605351537
    title: Rasmus Nielsen and Montgomery Slatkin, An Introduction to Population Genetics, Theory and Applications, Sinauer, 2013
    locator: Chapter 2 (genetic drift) and Chapter 8 (selection in a finite population)
---

The Moran model is a model of a finite population in which generations overlap. At each step one individual is chosen to reproduce and one is chosen to die, and the offspring takes the place of the one that died. So the number of individuals of one type changes by at most one per step, and it is a [birth-death process](/birth-death-process/) in discrete time. This makes exact formulas for fixation probabilities and absorption times easy to get, which is why the model is used next to the [Wright-Fisher model](/wright-fisher-model/).

## The machine

**The state.** A haploid population of $N$ individuals of two types, $A$ and $a$. The state is $X \in \{0, \ldots, N\}$, the number of $A$ individuals. Time is in steps, and one generation is $N$ steps, so each individual lives one generation on average. For a diploid population, Moran models are usually applied to the $2N$ gene copies; this page keeps $N$ for the number of individuals of the haploid model.

**The step.** Type $A$ has fitness $r$ and type $a$ has fitness 1 (the neutral case is $r = 1$). In each step:

1. One individual is chosen to reproduce, with probability proportional to fitness, so it is of type $A$ with probability $rX/(rX + N - X)$.
2. One individual is chosen uniformly to die, so it is of type $A$ with probability $X/N$. The same individual can be chosen in both draws.
3. The offspring, of the type of its parent, replaces the one that died.

So from $X = i$ the chain moves to $i + 1$ with probability $b_i$, to $i - 1$ with probability $d_i$, and stays with probability $1 - b_i - d_i$, where

$$b_i = \frac{r i}{r i + N - i} \cdot \frac{N - i}{N}, \qquad d_i = \frac{N - i}{r i + N - i} \cdot \frac{i}{N}.$$

The states 0 and $N$ are absorbing. The ratio $d_i/b_i = 1/r$ does not depend on $i$; this is the reason for the simple closed forms below.

**A simulation.**

```pseudo id=main
MORAN(i0, N, r, T)
L1  X ← i0
L2  for k ← 1 to T do
L3      B ← 1 with probability r X / (r X + N - X), else 0      (the parent is of type A)
L4      D ← 1 with probability X / N, else 0                    (the one that dies is of type A)
L5      X ← X + B - D
L6  return the path of X
```

Each step costs two Bernoulli draws, so $T$ steps take $O(T)$ time. The implementation stops when $X$ reaches 0 or $N$, and it solves the tridiagonal systems for the exact absorption times.

**A trace.** With seed 7, $N = 10$, $r = 1$ and $X_0 = 3$, the implementation goes down to 1 copy, back up to 3, down to 1 again, and then rises to fixation after 86 steps (8.6 generations). The exact mean time to absorption from 3 is $56.4$ steps. With $r = 1.1$, $X_0 = 1$ and the same seed, the mutant dies in the second step.

## What it counts

- The number $X$ of individuals of one type after each birth and death.
- The probability that a type fixes, in particular a single mutant.
- The number of steps (or generations, dividing by $N$) to fixation or loss.
- With mutation, the number of types and their frequencies, as in the [infinite alleles model](/infinite-alleles-model/).
- The genealogy of a sample, which merges two lineages when the newborn and its parent are both ancestors of the sample.

## Relation to other models

- **[Wright-Fisher model](/wright-fisher-model/).** In Wright-Fisher, all individuals are replaced at once in each generation; in Moran, one at a time. Per generation, drift in the Moran model is twice as fast as in a haploid Wright-Fisher population of the same size: a Moran population of $N$ individuals behaves like a Wright-Fisher population of $N/2$ copies. So its [effective population size](/effective-population-size/) is $N/2$. The variance of the number of offspring per generation is 2 in Moran and 1 in Wright-Fisher, and this factor explains the difference.
- **[Wright-Fisher diffusion](/wright-fisher-diffusion/).** With time in units of $N^2/2$ steps ($N/2$ generations) and $Ns$ fixed, the frequency $X/N$ tends to the same diffusion as the Wright-Fisher frequency.
- **[Kingman coalescent](/kingman-coalescent/).** A step merges two of $k$ sample lineages with probability $k(k-1)/N^2$, so the genealogy tends to the Kingman coalescent in units of $N^2/2$ steps.
- **[Galton-Watson process](/galton-watson-process/) and [birth-death process](/birth-death-process/).** A rare type in a large population grows like a birth-death process with birth rate $r$ and death rate 1 per unit of time, and its survival probability $1 - 1/r$ is the large $N$ limit of the fixation probability.
- **Moran process on graphs.** If individuals sit on the vertices of a graph and the offspring replaces a neighbour, the fixation probability can depend on the graph. On a complete graph it is the model of this page.

## Known results in the model

**Fixation probability.** With $r \ne 1$, a type $A$ that starts with $i$ individuals fixes with probability

$$\pi_i = \frac{1 - r^{-i}}{1 - r^{-N}}, \qquad \pi_1 = \frac{1 - 1/r}{1 - 1/r^N},$$

and with $r = 1$, $\pi_i = i/N$.

*Proof.* The steps that stay in place do not change the outcome, so $\pi_i = \frac{b_i}{b_i + d_i}\pi_{i+1} + \frac{d_i}{b_i + d_i}\pi_{i-1}$ for $0 < i < N$, with $\pi_0 = 0$ and $\pi_N = 1$. Write $\gamma = d_i/b_i = 1/r$. Then $\pi_{i+1} - \pi_i = \gamma (\pi_i - \pi_{i-1})$, so $\pi_{i+1} - \pi_i = \gamma^i \pi_1$, and $\pi_i = \pi_1 (1 + \gamma + \cdots + \gamma^{i-1})$. The condition $\pi_N = 1$ fixes $\pi_1$, and summing the geometric series gives the formula. For $r = 1$ all differences are equal. $\square$

For $N = 10$ and $r = 1.1$, $\pi_1 = 0.147950$, against $1/N = 0.1$ without selection. As $N \to \infty$ with $r$ fixed, $\pi_1 \to 1 - 1/r$, which is about $s$ for $r = 1 + s$. For $r = 1.01$ it is $0.0157$ with $N = 100$ and $0.009901$ with $N = 1000$. A haploid Wright-Fisher population gives about $2s$, twice as much, because its offspring variance is half as large.

**Absorption time, neutral case.** With $r = 1$, the mean number of steps to absorption from $i$ is

$$t_i = N \Big( (N - i) \sum_{j=1}^{i} \frac{1}{N - j} + i \sum_{j=i+1}^{N-1} \frac{1}{j} \Big).$$

*Proof.* The mean time satisfies $t_i = 1 + b_i t_{i+1} + d_i t_{i-1} + (1 - b_i - d_i) t_i$, so $b(t_{i+1} - 2t_i + t_{i-1}) = -1$ with $b = b_i = d_i = i(N - i)/N^2$, and $t_0 = t_N = 0$. The solution is $t_i = \sum_j G(i, j)/b_j$ with the Green function $G(i, j) = j(N - i)/N$ for $j \le i$ and $i(N - j)/N$ for $j > i$ of the second difference. Substituting $b_j$ gives the formula. $\square$

From one copy, $t_1 = N(1 + 1/2 + \cdots + 1/(N-1)) \approx N \ln N$ steps, which is only $\ln N$ generations: a new neutral mutant is usually lost fast. From $i = N/2$, $t_i \approx N^2 \ln 2$ steps, or $N \ln 2$ generations. For $N = 10$, $t_1 = 28.29$ and $t_5 = 64.56$ steps; the value $N^2 \ln 2 = 69.3$ is the large $N$ form.

**Eigenvalues, neutral case (Moran 1958).** The transition matrix has the eigenvalues $1 - k(k-1)/N^2$ for $k = 0, 1, \ldots, N$.

*Proof.* With $b_i = d_i = i(N - i)/N^2$, for any function $f$, $\mathbb E[f(X') \mid X = x] = f(x) + \frac{x(N - x)}{N^2}\big(f(x+1) - 2f(x) + f(x-1)\big)$. For the falling factorial $f(x) = x(x-1)\cdots(x-k+1)$, the second difference is $k(k-1)$ times the falling factorial of degree $k - 2$ at $x - 1$, and $x(N - x)$ times that is $-(x)_k + $ terms of lower degree. So the matrix maps $(x)_k$ to $(1 - k(k-1)/N^2)(x)_k$ plus lower terms: it is triangular in the basis of falling factorials, with these values on the diagonal. $\square$

The value for $k = 2$ is $1 - 2/N^2$, so the heterozygosity $\mathbb E[X(N - X)]$ drops by this factor per step and by about $1 - 2/N$ per generation. A haploid Wright-Fisher population of $N$ copies loses it at $1 - 1/N$ per generation; this is the factor 2 of the effective size.

**With selection, times.** There is no short closed form, but the times are the solution of a tridiagonal linear system, which takes $O(N)$ operations. For $N = 10$ and $r = 1.1$, a single mutant needs $30.58$ steps on average until fixation or loss.

## References
