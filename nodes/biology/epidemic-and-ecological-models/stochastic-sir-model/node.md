---
tag: EFGZYZ
kind: model
slug: stochastic-sir-model
name: Stochastic SIR model
aliases:
- general stochastic epidemic
area: biology/epidemic-and-ecological-models
level: core
summary: The continuous-time Markov chain version of SIR, with infection rate beta S I / N and recovery rate gamma I, simulated exactly by Gillespie.
history:
  year: 1955
  people: [Norman Bailey, Peter Whittle]
  note: Bailey studied the general stochastic epidemic in the early 1950s, and Whittle's note on Bailey's paper gave the threshold result for the probability of a minor outbreak.
prereqs: [sir-epidemic-model, markov-chain, gillespie-algorithm]
see_also: [sir-epidemic-model, epidemic-model, epidemic-threshold, kermack-mckendrick-sir-model, reed-frost-model, galton-watson-process, birth-death-process, epidemic-data-augmentation-mcmc]
sources:
  - paper: doi:10.1093/biomet/42.1-2.116
    title: "P. Whittle, The outcome of a stochastic epidemic, a note on Bailey's paper, Biometrika 42, 1955"
    locator: pages 116 to 122 (the probability of a minor outbreak through a comparison with birth-death processes)
  - book: isbn:9780387950501
    title: Hakan Andersson and Tom Britton, Stochastic Epidemic Models and Their Statistical Analysis, Lecture Notes in Statistics 151, Springer, 2000
    locator: Chapter 2 (the standard SIR epidemic model), Chapter 3 (coupling with a branching process), Chapter 4 (the threshold limit theorem) and Chapter 5 (density dependent jump Markov processes and the deterministic limit)
  - book: isbn:9780691116174
    title: Matt J. Keeling and Pejman Rohani, Modeling Infectious Diseases in Humans and Animals, Princeton University Press, 2008
    locator: the chapter on stochastic dynamics (event-driven simulation of the SIR model and the extinction of small outbreaks)
---

The stochastic SIR model, also called the general stochastic epidemic, is the [SIR epidemic](/sir-epidemic-model/) as a [Markov chain](/markov-chain/) in continuous time. The state counts the susceptible, infectious and removed people of a closed population. Each infectious person meets others at random times, and each such meeting with a susceptible is a new infection. Each infectious person recovers after an exponential time. The model keeps the chance events that the [Kermack-McKendrick equations](/kermack-mckendrick-sir-model/) average away. So it answers questions that the deterministic model cannot: the probability that one case starts a large outbreak, the spread of the final size, and the chance that the disease dies out early. Gillespie's [direct method](/gillespie-algorithm/) simulates it exactly.

## The machine

**The state.** $(S, I)$, the numbers of susceptible and infectious people, in a population of fixed size $N$. The number of removed people is $R = N - S - I$. The state space is $\{(s, i) : s, i \ge 0,\ s + i \le N\}$, and every state with $i = 0$ is absorbing.

**The parameters.** The contact rate $\beta > 0$ and the recovery rate $\gamma > 0$. The basic reproduction number is $R_0 = \beta / \gamma$: a case is infectious for a mean time $1/\gamma$ and makes contacts at rate $\beta$, each with a person chosen uniformly from the population.

**The transitions.** From the state $(s, i)$:

| event | change | rate |
|---|---|---|
| infection | $(s, i) \to (s - 1, i + 1)$ | $\beta s i / N$ |
| recovery | $(s, i) \to (s, i - 1)$ | $\gamma i$ |

This is the frequency-dependent form: the rate of contacts per case does not grow with $N$. The holding time in a state is exponential with the total rate $a_0 = \beta s i / N + \gamma i$, and the next event is an infection with probability

$$\frac{\beta s i / N}{\beta s i / N + \gamma i} = \frac{R_0 s}{R_0 s + N}.$$

**The assumptions.** The population is closed and mixes homogeneously. A recovered person is immune for good. The infectious period is exponential with rate $\gamma$, so a case has no memory of how long it has been infectious. There is no latent period. Each of these can be changed, but then the process is no longer a Markov chain on $(S, I)$ alone.

**A simulation.** The direct method draws the time to the next event and then the type of the event.

```pseudo id=main
SIR-DIRECT(N, S0, I0, β, γ, T)
L1  t ← 0, S ← S0, I ← I0
L2  while I > 0 do
L3      a_inf ← β S I / N, a_rec ← γ I, a0 ← a_inf + a_rec
L4      t ← t + Exponential(a0)
L5      if t > T then stop
L6      if Uniform(0, a0) < a_inf then S ← S - 1, I ← I + 1
L7      else I ← I - 1
L8      record (t, S, I)
```

Each event lowers $2S + I$ by one, so a run has at most $2 S_0 + I_0$ events and costs $O(N)$ time. The implementation draws its random numbers in the same order as the generic `ssa_direct` of the shared helper, and with the same seed both give the same path.

**A worked example: three people.** Take $N = 3$, one case, two susceptibles and $R_0 = 2$. The first event is an infection with probability $\frac{2 \cdot 2}{2 \cdot 2 + 3} = 4/7$. If it is a recovery, no one else is infected. If it is an infection, the state is $(1, 2)$, and the next event is an infection with probability $2/5$. Going on in this way gives the exact final size law $P(0) = 3/7$, $P(1) = 36/175$ and $P(2) = 64/175$.

**A worked example: twenty people.** With $N = 20$, one case and $R_0 = 1.5$, the probability that the first case recovers before it infects anyone is $20/(1.5 \cdot 19 + 20) = 0.41237$. The exact final size law falls to $0.02173$ at 8 infections and rises again to a second peak of $0.03085$ at 15. With seed 4, the implementation draws a run whose first events are infections at times 0.115, 0.229 and 0.240, and 9 people are infected in total. With seeds 1, 2 and 5 the first case recovers first. In a population of $N = 1000$ with $R_0 = 2$ and seed 4, the run infects 794 people, the number of cases peaks at 143, and the last recovery is at time 19.5 (in units of the mean infectious period).

## What it counts

- **The final size**, $S_0 - S_\infty$. Its exact law follows from the embedded jump chain above, by a pass over the states in decreasing order of $2S + I$.
- **The probability of a minor outbreak** in a large population, about $(1/R_0)^{I_0}$ when $R_0 > 1$.
- **The epidemic curve** $I(t)$, its peak, and the duration of the outbreak.
- **The likelihood of an observed epidemic.** For a fully observed path, the likelihood is a product of the event rates times $\exp(-\int a_0\, dt)$. This is the basis of [data augmentation MCMC](/epidemic-data-augmentation-mcmc/) when the infection times are not observed.

## Relation to other models

- **[Kermack-McKendrick SIR model](/kermack-mckendrick-sir-model/).** If $N \to \infty$ with $S(0)/N$ and $I(0)/N$ fixed, the fractions $S/N$ and $I/N$ converge on any finite time interval to the solution of $s' = -\beta s i$, $i' = \beta s i - \gamma i$. This is Kurtz's law of large numbers for density dependent jump Markov processes ([Andersson and Britton](#references), chapter 5). The fluctuations around the limit are of order $1/\sqrt N$.
- **[Birth-death process](/birth-death-process/) and [Galton-Watson process](/galton-watson-process/).** While $S \approx N$, each case infects at rate $\beta$ and recovers at rate $\gamma$, independently of the others. That is a linear birth-death process, and counted by generations it is a Galton-Watson process with geometric offspring of mean $R_0$. [Andersson and Britton](#references) (chapter 3) couple the two processes so that they agree until a number of cases that grows with $N$.
- **[Reed-Frost model](/reed-frost-model/).** The same model with a fixed infectious period in place of the exponential one. Its final size law is that of a continuous-time SIR model with a fixed infectious period.
- **[Chemical master equation](/chemical-master-equation/).** The forward equation of the chain is the master equation of the reaction network $S + I \to 2I$, $I \to R$. Methods for reaction networks, such as [tau-leaping](/tau-leaping/), apply to the model without change.
- **Other compartments.** The [SIS](/sis-epidemic-model/) and [SEIR](/seir-epidemic-model/) models have stochastic versions built in the same way. In the SIS version there are no removed people, and in a finite population the disease always dies out in the end, but the expected time to extinction grows exponentially with $N$ when $R_0 > 1$.

## Known results in the model

**The threshold theorem.** Let $N \to \infty$ with $I_0$ fixed. If $R_0 \le 1$, the number of infections stays bounded in probability: every outbreak is minor. If $R_0 > 1$, the probability of a minor outbreak tends to $(1/R_0)^{I_0}$, the extinction probability of the birth-death process that starts with $I_0$ individuals. Whittle (1955) gave this result through a comparison with birth-death processes, and [Andersson and Britton](#references) (chapter 4) prove it as the threshold limit theorem. For $N = 1000$, the exact probability of at most 100 infections is $0.50207$ for $R_0 = 2$ and one case (limit $0.5$), $0.12774$ for three cases (limit $0.125$), and $0.67322$ for $R_0 = 1.5$ and one case (limit $2/3$).

**Exponential and fixed infectious periods differ.** The probability of a minor outbreak from one case is $1/R_0$ for an exponential infectious period. For a fixed infectious period, the offspring law is Poisson($R_0$), and the probability is the smallest root of $q = e^{R_0(q - 1)}$, which is $0.203188$ at $R_0 = 2$, against $0.5$ here. So the variance of the infectious period matters for the early phase. It does not matter for the deterministic final size.

**The size of a major outbreak.** Given a major outbreak, the final fraction infected tends to the root $z > 0$ of the [final size relation](/final-size-relation/) $z = 1 - e^{-R_0 z}$, for any law of the infectious period with mean $1/\gamma$. For $R_0 = 2$, $z = 0.796812$. The number infected is approximately normal around $N z$, with a variance of order $N$ that depends on the variance of the infectious period ([Andersson and Britton](#references), chapter 4).

**The Sellke construction.** Give each susceptible $j$ an independent threshold $Q_j$, exponential with mean 1, and order the people by their thresholds. Person $j$ is infected when the total infection pressure $\frac{\beta}{N} \int_0^t I(u)\, du$ first passes $Q_j$. This builds the same process, and it shows that the final size depends on the infectious periods only through their sum over the people infected. The final size is then the smallest $k$ for which the $(k+1)$-th smallest threshold is larger than $\frac{\beta}{N}$ times the total infectious time of the first $k$ cases plus the initial ones. The construction gives the final size law without the timing ([Andersson and Britton](#references), chapter 2).

**The duration.** A major outbreak lasts a time of order $\log N$: about $\log N / (\gamma (R_0 - 1))$ to grow, and another time of order $\log N$ to fade out at the end. A minor outbreak lasts a time of order 1.

## References
