---
tag: PA1DQR
kind: model
slug: reed-frost-model
name: Reed-Frost model
aliases:
- Reed-Frost chain binomial
area: biology/epidemic-and-ecological-models
level: core
summary: A discrete-generation stochastic epidemic in which each susceptible escapes each infective independently, so new cases are binomial.
history:
  year: 1952
  people: [Lowell Reed, Wade Hampton Frost, Helen Abbey]
  note: Reed and Frost taught the model at Johns Hopkins but did not publish it, and Abbey published a full account of the theory and examined it against data in 1952.
prereqs: [binomial-distribution, markov-chain, sir-epidemic-model]
see_also: [stochastic-sir-model, galton-watson-process, epidemic-model, sir-epidemic-model, epidemic-threshold, final-size-relation, percolation, erdos-renyi-model]
sources:
  - paper: "Helen Abbey, An examination of the Reed-Frost theory of epidemics, Human Biology 24(3), 1952, pages 201 to 233"
    title: Abbey 1952
    locator: the account of the Reed-Frost theory and its comparison with data
  - book: isbn:9780387950501
    title: Hakan Andersson and Tom Britton, Stochastic Epidemic Models and Their Statistical Analysis, Lecture Notes in Statistics 151, Springer, 2000
    locator: Chapter 2 (the Reed-Frost model as the standard SIR model with a fixed infectious period) and Chapter 7 (epidemics and random graphs)
  - paper: doi:10.1103/PhysRevE.66.016128
    title: M. E. J. Newman, Spread of epidemic disease on networks, Physical Review E 66(1), 2002
    locator: the mapping of an SIR epidemic to bond percolation, with the fixed infectious period as the case of independent edges
---

The Reed-Frost model is a stochastic epidemic in discrete generations. A case is infectious for one generation and then recovers. During that generation, each susceptible person has an independent chance $p$ of an adequate contact with each case. A susceptible who meets at least one case becomes a case of the next generation. So the number of new cases, given the state, is binomial, and the sequence of case counts $I_0, I_1, I_2, \ldots$ is called a chain binomial. The model is the simplest exact stochastic version of the [SIR epidemic](/sir-epidemic-model/). It is small enough for exact calculation in a household, and in a large population it shows the two behaviours of the [epidemic threshold](/epidemic-threshold/): a minor outbreak or a major one.

## The machine

**The state.** After generation $t$, the state is $(S_t, I_t)$: $S_t$ susceptibles and $I_t$ new cases. The cases of earlier generations are removed and play no further part. The population has a fixed size $N = S_0 + I_0$ plus any people who are immune at the start, who do not take part.

**The parameters.** The contact probability $p \in [0, 1]$: the chance that one given case infects one given susceptible during the generation. Let $q = 1 - p$. Time is counted in generations, and a generation is about the length of the [generation interval](/generation-interval/) of the disease.

**The update rule.** A susceptible escapes all $I_t$ cases with probability $q^{I_t}$, independently of the other susceptibles. So

$$I_{t+1} \mid (S_t, I_t) \sim \operatorname{Binomial}\big(S_t,\ 1 - q^{I_t}\big), \qquad S_{t+1} = S_t - I_{t+1}.$$

The epidemic stops at the first $t$ with $I_t = 0$, and the final size is $S_0 - S_t$, the number of people infected after generation 0.

**The Greenwood variant.** In Greenwood's version the chance of infection does not depend on the number of cases, as long as there is at least one: $I_{t+1} \sim \operatorname{Binomial}(S_t, p)$ if $I_t > 0$. This fits a household where the exposure comes from the shared space more than from each case.

**The assumptions.** All people mix equally. Contacts between different pairs are independent. The infectious period is fixed and the same for every case, so the generations do not overlap. A case can infect only during its own generation.

**A simulation.** One binomial draw per generation.

```pseudo id=main
REED-FROST(S0, I0, p)
L1  S ← S0, I ← I0
L2  path ← [(S, I)]
L3  while I > 0 do
L4      π ← 1 - (1 - p)^I            ▷ Greenwood: π ← p
L5      C ← Binomial(S, π)
L6      S ← S - C, I ← C
L7      append (S, I) to path
L8  return path
```

Each round of the loop either ends the epidemic ($C = 0$) or lowers $S$ by at least one, so there are at most $S_0 + 1$ rounds. A run costs $O(S_0)$ binomial draws in the worst case.

**A worked example: a household of three.** One case brings the disease into a household with two susceptibles, and $p = 0.2$, $q = 0.8$. The possible chains and their probabilities are:

| chain $(I_0, I_1, \ldots)$ | probability | final size |
|---|---|---|
| 1, 0 | $q^2 = 0.64$ | 0 |
| 1, 1, 0 | $2pq \cdot q = 0.256$ | 1 |
| 1, 1, 1, 0 | $2pq \cdot p = 0.064$ | 2 |
| 1, 2, 0 | $p^2 = 0.04$ | 2 |

So the final size is 0, 1 or 2 with probabilities 0.64, 0.256 and 0.104. For a household of five (one case, four susceptibles, $p = 0.2$), the two variants first differ when two cases meet the same susceptible: the mean final size is 1.2701 under Reed-Frost and 1.2030 under Greenwood, and the probability that all four are infected is 0.0819 against 0.0502.

**A worked example: a small community.** With $S_0 = 10$, $I_0 = 1$ and $p = 0.15$, the exact law of the final size has two peaks: $P(0) = 0.19687$, a minimum of $0.04949$ at 3, and a second peak of $0.1237$ at 9. The mean is 4.911. With seed 2, the implementation draws the chain $1, 2, 1, 2, 2, 0$ (8 people infected after generation 0), and with seed 5 it draws $1, 5, 5, 0$ (all 10 infected). In 4000 runs with seed 20261118, 823 runs give final size 0, against $4000 \times 0.19687 = 787.5$ expected.

## What it counts

- **The probability of a chain.** For a complete chain $i_0, i_1, \ldots, i_T = 0$ with $s_{t+1} = s_t - i_{t+1}$,
  $$P = \prod_{t=0}^{T-1} \binom{s_t}{i_{t+1}} \big(1 - q^{i_t}\big)^{i_{t+1}} \big(q^{i_t}\big)^{s_{t+1}}.$$
  This is the likelihood used to fit the model to household data.
- **The final size.** The law of $S_0 - S_\infty$ follows from a pass over the states $(S, I)$: each generation spreads the mass of a state over its binomial successors. The implementation computes it exactly with rational arithmetic.
- **The probability of a minor outbreak**, and the size of a major one, in a large population (see below).
- **The duration** in generations, $T$, and the epidemic curve $I_0, I_1, \ldots$.

## Relation to other models

- **[Stochastic SIR model](/stochastic-sir-model/).** The Reed-Frost model is the continuous-time SIR model with a fixed infectious period of length 1 in place of an exponential one, seen at the ends of the generations. If each case infects each susceptible at rate $\beta / N$ during its infectious period, then $p = 1 - e^{-\beta / N}$. The final size law depends only on the law of the infectious period, not on the timing, so this gives the final size of the SIR model with a fixed infectious period ([Andersson and Britton](#references), chapter 2).
- **[Random graphs](/erdos-renyi-model/) and [percolation](/percolation/).** Draw an edge between each pair of the $N$ people with probability $p$, independently. Then the cases of generation $t$ are the people at graph distance $t$ from the initial cases, and the final size is the size of their connected component, less $I_0$. This holds because each pair is tested at most once, at the first generation in which one of the two is a case. So the final size of the Reed-Frost model is the component size in the [Erdos-Renyi graph](/erdos-renyi-model/) $G(N, p)$, the case of bond [percolation](/percolation/) with independent edges ([Newman](#references)). The tests of the implementation sum over all graphs on up to six people and get the same chain law.
- **[Galton-Watson process](/galton-watson-process/).** With $p = R_0 / N$, a case in an almost fully susceptible population infects a Binomial($N - 1$, $p$) number of people, which is close to Poisson($R_0$). So the start of the epidemic is a branching process with Poisson offspring.
- **[SIR epidemic model](/sir-epidemic-model/).** For large $N$ and $p = R_0 / N$, the fraction infected in a major outbreak follows the deterministic [final size relation](/final-size-relation/).
- **[Epidemic model](/epidemic-model/).** The Reed-Frost model is the discrete-time stochastic member of the family of compartmental models, with the compartments S, I and R.

## Known results in the model

**The threshold in a large population.** Let $N \to \infty$ with $p = R_0 / N$ and one initial case. By the [extinction theorem](/branching-process-extinction-theorem/) for Poisson offspring, the probability of a minor outbreak tends to $q_\infty$, the smallest root of $s = e^{R_0(s - 1)}$. It is 1 if $R_0 \le 1$ and $0.203188$ for $R_0 = 2$. A major outbreak infects a fraction close to the root $z > 0$ of $z = 1 - e^{-R_0 z}$, which is $0.796812$ for $R_0 = 2$. This is the giant component of $G(N, R_0/N)$. In 2000 runs with $N = 1000$, $R_0 = 2$ and seed 11, a fraction 0.197 of the runs stays minor, and the major outbreaks infect 0.795 of the population on average.

**Limit theorems.** Given a major outbreak, the final size is approximately normal around $N z$, with a standard deviation of order $\sqrt N$. The threshold limit theorem and the central limit theorem for the final size of the standard SIR model, which covers the Reed-Frost model, are in [Andersson and Britton](#references), chapter 4.

**Small populations.** In a household, there is no clear split into minor and major outbreaks, so the exact chain probabilities are used directly. A household of size $n$ has at most $2^{n-1}$ possible chains from one case, and the pass over the states $(S, I)$ takes $O(n^3)$ arithmetic operations. Households in a large population lead to the two-level mixing models, where the households play the role of individuals in a branching process.

**Estimation.** Given observed chains from many households, the likelihood is a product of the chain probabilities above, a polynomial in $q$. The [maximum likelihood estimate](/maximum-likelihood-estimation/) of $q$ follows by a one-dimensional search. Abbey (1952) examined the theory against outbreak data.

## References
