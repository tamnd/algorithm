---
tag: 1ZKR7A
kind: model
slug: galton-watson-process
name: Galton-Watson branching process
aliases:
- Bienayme-Galton-Watson process
area: biology/epidemic-and-ecological-models
level: core
summary: A population in generations where each individual has an independent random number of children with a fixed offspring distribution.
history:
  year: 1875
  people: [Francis Galton, Henry William Watson]
  note: Galton asked for the chance that a family name dies out, and Watson set up the generating function recursion in their joint paper of 1875.
prereqs: [markov-chain, poisson-distribution, moment-generating-function]
see_also: [branching-process-extinction-theorem, birth-death-process, martingale, stochastic-sir-model, reed-frost-model, epidemic-renewal-equation, next-generation-matrix, yule-model]
sources:
  - paper: "H. W. Watson and Francis Galton, On the probability of the extinction of families, Journal of the Anthropological Institute of Great Britain and Ireland 4, 1875, pages 138 to 144"
    title: Watson and Galton 1875
    locator: the question of the extinction of surnames, and the iteration of the generating function of the number of sons
  - book: "Theodore E. Harris, The Theory of Branching Processes, Springer, 1963"
    title: Harris 1963
    locator: Chapter I, the Galton-Watson process (generating functions, moments, the extinction probability and the limit of Z_n / m^n)
  - book: "Krishna B. Athreya and Peter E. Ney, Branching Processes, Springer, 1972"
    title: Athreya and Ney 1972
    locator: Chapter I, the Galton-Watson process (the critical case, the Kesten-Stigum theorem and the limit laws)
  - book: isbn:9780387950501
    title: Hakan Andersson and Tom Britton, Stochastic Epidemic Models and Their Statistical Analysis, Lecture Notes in Statistics 151, Springer, 2000
    locator: Chapter 3, Coupling methods (the approximation of the early phase of an epidemic by a branching process)
---

The Galton-Watson process is the simplest model of a population that grows by reproduction. Time runs in generations. Each individual of a generation has a random number of children, drawn independently from one fixed offspring distribution, and the children form the next generation. The model answers the question of Galton and Watson (1875): what is the chance that a family line dies out? In epidemiology, an individual is an infected person and the children are the people that this person infects, so the model describes the start of an outbreak, before the supply of susceptible people runs short. The main result about it is the [extinction theorem](/branching-process-extinction-theorem/).

## The machine

**The state.** $Z_t \in \{0, 1, 2, \ldots\}$ is the number of individuals in generation $t$, for $t = 0, 1, 2, \ldots$. Usually $Z_0 = 1$. The state 0 is absorbing: a generation with no individuals has no children.

**The parameters.** The offspring distribution $p_k = P(\text{one individual has } k \text{ children})$, for $k = 0, 1, 2, \ldots$, with $\sum_k p_k = 1$. Its probability generating function is

$$f(s) = \sum_{k \ge 0} p_k s^k, \qquad 0 \le s \le 1,$$

its mean is $m = f'(1) = \sum_k k p_k$ and its variance is $\sigma^2$. The mean $m$ is the number of children per individual. In an epidemic it is the reproduction number of the early phase. Time is in generations, not in days.

**The update rule.** Let $\xi_{t,1}, \xi_{t,2}, \ldots$ be independent draws from $(p_k)$, independent of everything before generation $t$. Then

$$Z_{t+1} = \sum_{i=1}^{Z_t} \xi_{t,i}.$$

So $(Z_t)$ is a [Markov chain](/markov-chain/) on the non-negative integers, and the law of $Z_{t+1}$ given $Z_t = z$ is the $z$-fold convolution of $(p_k)$.

**The assumptions.** Individuals reproduce independently of each other. All individuals have the same offspring distribution, in every generation. There is no limit from resources or from the depletion of susceptibles: the offspring law does not depend on $Z_t$. Generations do not overlap. Each of these fails in a real population sooner or later, so the model describes a population that is small compared with its environment.

**A simulation and the extinction probability.** The first procedure finds the extinction probability $q$ by the iteration of the [extinction theorem](/branching-process-extinction-theorem/). The second one simulates a path.

```pseudo id=main
EXTINCTION-PROBABILITY(f, ε)
L1  q ← 0
L2  repeat
L3      q_old ← q
L4      q ← f(q_old)                    ▷ q is now P(Z_n = 0) for the next n
L5  until q - q_old < ε
L6  return q

SIMULATE-GW(p, Z0, T)
L7  Z ← Z0, path ← [Z0]
L8  for t ← 1 to T do
L9      Z ← sum of Z independent draws from p
L10     append Z to path
L11     if Z = 0 then return path
L12 return path
```

After $n$ rounds of line L4, $q = f_n(0) = P(Z_n = 0)$, where $f_n$ is $f$ composed with itself $n$ times (see below). SIMULATE-GW draws one offspring count per individual, so a path costs $O(Z_0 + Z_1 + \cdots + Z_T)$ draws. For Poisson offspring, the sum of $z$ independent Poisson($m$) counts is Poisson($m z$), so one draw per generation is enough, and the implementation uses this.

**A worked example.** Take $p_0 = 1/4$, $p_1 = 1/4$ and $p_2 = 1/2$. Then $f(s) = \tfrac14 + \tfrac14 s + \tfrac12 s^2$, $m = 5/4$ and $\sigma^2 = 11/16$. The equation $f(s) = s$ is $2s^2 - 3s + 1 = 0$, with the roots $1/2$ and $1$, so $q = 1/2$. The iterates of line L4 are

| $n$ | 1 | 2 | 3 | 4 | 5 | 10 | 20 |
|---|---|---|---|---|---|---|---|
| $P(Z_n = 0) = f_n(0)$ | 0.25 | 0.34375 | 0.39502 | 0.42678 | 0.44776 | 0.48882 | 0.49939 |

They increase to $1/2$. The law of $Z_2$ comes from $f_2(s) = f(f(s)) = \tfrac{11}{32} + \tfrac18 s + \tfrac{9}{32} s^2 + \tfrac18 s^3 + \tfrac18 s^4$. Its mean is $25/16 = m^2$ and its variance is $495/256$, as the formulas below give. With seed 2, the implementation draws the path $1, 2, 2, 2, 4, 7, 10, 11, 13$ over 8 generations. With seeds 1, 3 and 4 the line dies in the first generation, and with seed 7 it dies in the second. Over 3000 paths with seed 20261118, a fraction 0.438 is extinct by generation 4, against the exact $f_4(0) = 0.427$, a difference of 1.3 standard errors.

## What it counts

- **The law of $Z_n$.** Given $Z_n = z$, the generating function of $Z_{n+1}$ is $f(s)^z$. So $E[s^{Z_{n+1}}] = E[f(s)^{Z_n}]$, and by induction $E[s^{Z_n}] = f_n(s)$, with $f_0(s) = s$ and $f_{n+1} = f \circ f_n = f_n \circ f$. With $Z_0 = k$, the generating function is $f_n(s)^k$, because the $k$ lines are independent.
- **The probability of extinction by generation $n$.** $P(Z_n = 0) = f_n(0)$. This is also $P(T \le n)$ for the extinction time $T = \min\{n : Z_n = 0\}$.
- **The probability of ultimate extinction.** $q = P(Z_n = 0 \text{ for some } n) = \lim_n f_n(0)$, the smallest root of $f(s) = s$ in $[0, 1]$. From $Z_0 = k$ it is $q^k$.
- **The mean and the variance.** $E[Z_n] = m^n$, and $\operatorname{Var}(Z_n) = \sigma^2 m^{n-1} (m^n - 1)/(m - 1)$ for $m \ne 1$, and $n \sigma^2$ for $m = 1$.
- **The total progeny.** $Y = \sum_{n \ge 0} Z_n$, the number of individuals that ever live. In an epidemic, it is the size of a minor outbreak.

## Relation to other models

- **[Birth-death process](/birth-death-process/).** In the linear birth-death process, each individual lives an exponential time with rate $\mu$ and gives birth at rate $\lambda$ while it lives. The number of children of one individual is geometric, $p_k = \frac{\mu}{\lambda + \mu} \left(\frac{\lambda}{\lambda + \mu}\right)^k$, with mean $\lambda / \mu$. So the generations of a birth-death process form a Galton-Watson process with this offspring law, while the birth-death process itself runs in continuous time.
- **[Stochastic SIR model](/stochastic-sir-model/).** While almost everyone is susceptible, a case infects others at rate $\beta$ during an exponential infectious period of rate $\gamma$. This is the birth-death process above with $\lambda = \beta$ and $\mu = \gamma$, so the early phase is a Galton-Watson process with geometric offspring of mean $R_0 = \beta / \gamma$. [Andersson and Britton](#references) (chapter 3) make the approximation exact with a coupling as the population size grows.
- **[Reed-Frost model](/reed-frost-model/).** In a population of $N$ with a contact probability $p = R_0 / N$, one case infects a Binomial($N - 1$, $p$) number of others at the start. For large $N$ this is close to Poisson($R_0$), so the early phase is a Galton-Watson process with Poisson offspring.
- **[Epidemic renewal equation](/epidemic-renewal-equation/).** The Poisson renewal model with a constant reproduction number $R$ gives each case Poisson($R$) children, spread over the days by the generation interval. Counted by generations, not by days, it is a Galton-Watson process.
- **Multitype processes and the [next-generation matrix](/next-generation-matrix/).** With several types of individual, the mean numbers of children form a matrix. Its spectral radius plays the role of $m$, and the extinction probabilities solve a system of equations of the form $q = f(q)$.
- **[Yule model](/yule-model/) and [Kingman coalescent](/kingman-coalescent/).** The Yule model is a pure birth process in continuous time, a branching process with no deaths. The coalescent looks at a population of constant size backward in time; a branching process looks forward with no constraint on the size.

## Known results in the model

**Mean and variance.** $E[Z_{n+1} \mid Z_n] = m Z_n$ and $\operatorname{Var}(Z_{n+1} \mid Z_n) = \sigma^2 Z_n$, because $Z_{n+1}$ is a sum of $Z_n$ independent draws. So $E[Z_{n+1}] = m E[Z_n]$, which gives $E[Z_n] = m^n$. The law of total variance gives $V_{n+1} = \sigma^2 m^n + m^2 V_n$ with $V_0 = 0$, where $V_n = \operatorname{Var}(Z_n)$. The solution is $V_n = \sigma^2 m^{n-1} (1 + m + \cdots + m^{n-1})$, which is $\sigma^2 m^{n-1}(m^n - 1)/(m - 1)$ for $m \ne 1$ and $n \sigma^2$ for $m = 1$. Check: $V_1 = \sigma^2$, and $\sigma^2 m^{n} + m^2 \sigma^2 m^{n-2}(1 + \cdots + m^{n-2}) = \sigma^2 m^n (1 + m + \cdots + m^{n-1})$. $\square$

**The extinction theorem.** Assume $p_1 < 1$. Then $q$ is the smallest root of $f(s) = s$ in $[0, 1]$, and $q = 1$ if and only if $m \le 1$. If $p_1 = 1$, every individual has exactly one child, and the line never dies. The proof is on the page of the [extinction theorem](/branching-process-extinction-theorem/). For Poisson($m$) offspring, $f(s) = e^{m(s - 1)}$, and $q = 0.417188$ for $m = 1.5$, $q = 0.203188$ for $m = 2$ and $q = 0.059520$ for $m = 3$. For geometric offspring with mean $R$, $f(s) = 1/(1 + R - R s)$, and $q = 1/R$ for $R > 1$.

**The three regimes.** For $m < 1$ (subcritical), $P(Z_n > 0) \le E[Z_n] = m^n$, so the line dies out fast, and the expected total progeny is $\sum_n m^n = 1/(1 - m)$. For $m = 1$ (critical), the line dies out with probability 1, but slowly: if $\sigma^2 < \infty$, then $P(Z_n > 0) \sim 2/(n \sigma^2)$ (Kolmogorov's estimate; see [Athreya and Ney](#references), chapter I). For Poisson(1) offspring, $1 - f_{1000}(0) = 0.001992$, against $2/1000$. The expected total progeny is infinite in the critical case, even though the line dies. For $m > 1$ (supercritical), the line survives with probability $1 - q > 0$.

**Growth on survival.** For $1 < m < \infty$, $W_n = Z_n / m^n$ is a non-negative [martingale](/martingale/), since $E[Z_{n+1} \mid Z_n] = m Z_n$. So $W_n$ converges almost surely to a limit $W$. The Kesten-Stigum theorem says that $E[W] = 1$, and $P(W = 0) = q$, if and only if $E[Z_1 \ln Z_1] < \infty$; otherwise $W = 0$ almost surely ([Athreya and Ney](#references), chapter I). So in the usual case a surviving line grows like $W m^n$ with $W > 0$: the growth is exponential with the rate $\ln m$ per generation, and the random factor $W$ is fixed by the first few generations.

**No middle ground.** If $p_1 < 1$, every state $k \ge 1$ is transient, so with probability 1 either $Z_n \to 0$ or $Z_n \to \infty$. A population in this model never settles at a stable size.

**Total progeny.** In the subcritical or critical case, the total progeny $Y$ is finite with probability 1, and the hitting time theorem gives $P(Y = k) = \frac1k P(\xi_1 + \cdots + \xi_k = k - 1)$ for $Z_0 = 1$. For Poisson($m$) offspring the sum is Poisson($m k$), so $P(Y = k) = e^{-mk} (mk)^{k-1} / k!$, the Borel distribution. For $m = 0.5$: $P(Y = 1) = 0.606531$, $P(Y = 2) = 0.183940$, $P(Y = 3) = 0.083674$, with mean $1/(1 - m) = 2$.

**Use in epidemics.** For an outbreak that starts with one case in a large, fully susceptible population, the probability of a minor outbreak is about $q$, and $1 - q$ is the probability of a major outbreak. For Poisson offspring, $1 - q$ solves $1 - q = 1 - e^{-R_0 (1 - q)}$, the same equation as the [final size relation](/final-size-relation/): for $R_0 = 2$, $1 - q = 0.796812$, equal to the final size $z$. For geometric offspring (an exponential infectious period), the probability of a minor outbreak is $1/R_0$ instead. So two diseases with the same $R_0$ can have different chances to take off.

## References
