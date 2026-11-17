---
tag: T66PPF
kind: model
slug: metapopulation-epidemic-model
name: Metapopulation epidemic model
aliases:
- patch epidemic model
area: biology/epidemic-and-ecological-models
level: advanced
summary: Local epidemics in linked subpopulations coupled by travel or migration, used to model spatial spread between cities.
prereqs: [kermack-mckendrick-sir-model, next-generation-matrix]
see_also: [levins-metapopulation-model, sir-epidemic-model, agent-based-epidemic-simulation, laplacian-matrix, fisher-kpp-equation, ross-macdonald-model, final-size-relation, classical-runge-kutta-4]
sources:
  - paper: "L. A. Rvachev and I. M. Longini, A mathematical model for the global spread of influenza, Mathematical Biosciences 75(1), 1985, pages 3 to 22"
    locator: a model of influenza in a set of cities linked by air travel, with a transport operator that moves individuals between the cities, applied to the 1968 to 1969 pandemic
  - paper: doi:10.1073/pnas.0510525103
    title: Vittoria Colizza, Alain Barrat, Marc Barthelemy and Alessandro Vespignani, The role of the airline transportation network in the prediction and predictability of global epidemics, Proceedings of the National Academy of Sciences 103(7), 2006
    locator: pages 2015 to 2020 (a stochastic metapopulation model on the worldwide airline network, and the effect of the structure of that network on the predictability of the spread)
  - book: isbn:9780691116174
    title: Matt J. Keeling and Pejman Rohani, Modeling Infectious Diseases in Humans and Animals, Princeton University Press, 2008
    locator: Section 7.2, metapopulations (7.2.1.4 commuter approximations, 7.2.2 coupling and synchrony, 7.2.4 Levins-type metapopulations)
  - paper: doi:10.1016/S0025-5564(02)00108-6
    title: P. van den Driessche and James Watmough, Reproduction numbers and sub-threshold endemic equilibria for compartmental models of disease transmission, Mathematical Biosciences 180(1-2), 2002
    locator: pages 29 to 48 (R0 as the spectral radius of F V^(-1), where V holds all transfers between infected classes, such as travel)
---

A metapopulation epidemic model splits a population into subpopulations, called patches, such as the cities of a country or the countries of the world. Inside each patch, the infection follows a [compartmental epidemic model](/compartmental-epidemic-model/) with homogeneous mixing, usually SIR or SEIR. Between patches, the only link is travel: individuals move from one patch to another, or residents of one patch spend part of their day in another. The model sits between the [Kermack-McKendrick model](/kermack-mckendrick-sir-model/), which has one well-mixed population, and the [SIR model on networks](/sir-epidemic-model/), which has one node per person: here each node of the travel network is a whole well-mixed population. Rvachev and Longini (1985) used a model of this type for the global spread of influenza by air travel. The [basic reproduction number](/basic-reproduction-number/) of the whole system is the spectral radius of a [next-generation matrix](/next-generation-matrix/) that has travel in its transition part.

## The machine

**State.** For each patch $k = 1, \ldots, n$, the numbers $S_k$, $I_k$ and $R_k$, with $N_k = S_k + I_k + R_k$.

**Parameters.** A transmission rate $\beta_k$ in each patch, a recovery rate $\gamma$, and a travel rate $m_{kj} \ge 0$ at which each individual in patch $j$ moves to patch $k$, for $k \ne j$.

**Migration form.** Individuals move between patches and take their state with them:

$$
\begin{aligned}
\frac{dS_k}{dt} &= -\frac{\beta_k S_k I_k}{N_k} + \sum_{j \ne k} \left( m_{kj} S_j - m_{jk} S_k \right), \\
\frac{dI_k}{dt} &= \frac{\beta_k S_k I_k}{N_k} - \gamma I_k + \sum_{j \ne k} \left( m_{kj} I_j - m_{jk} I_k \right), \\
\frac{dR_k}{dt} &= \gamma I_k + \sum_{j \ne k} \left( m_{kj} R_j - m_{jk} R_k \right).
\end{aligned}
$$

With the matrix $L$ that has $L_{jj} = \sum_{k \ne j} m_{kj}$ (the total rate of leaving patch $j$) and $L_{kj} = -m_{kj}$ for $k \ne j$, the travel terms are $-L S$, $-L I$ and $-L R$. Every column of $L$ sums to zero, because travel moves individuals and does not create them; $L$ is a [Laplacian matrix](/laplacian-matrix/) of the directed travel network. The patch sizes $N_k$ are assumed to be at an equilibrium of the travel, $L N = 0$.

**Commuter form.** Residents of patch $k$ stay residents but spend a fraction $c_{kj}$ of their time in patch $j$. The force of infection on a resident of $k$ is then a mix of the infection levels in the patches that they visit (Keeling and Rohani 2008, section 7.2.1.4). This form fits daily travel to work; the migration form fits travel over longer times, as by air.

**Stochastic form.** For small patches or for the arrival of the first cases, each infection, recovery and trip is a random event. In the model of Colizza and others (2006), each patch is a city with an airport, and travel follows the passenger flows of the worldwide airline network.

## What it counts

The model counts the epidemic in each patch over time: when the infection arrives, when it peaks, how large the peak is, and how many people are infected in the whole system. The threshold is the $R_0$ of the whole system. With the infected classes $(I_1, \ldots, I_n)$ at the disease-free state $S_k = N_k$,

$$
F = \operatorname{diag}(\beta_1, \ldots, \beta_n), \qquad V = \gamma I + L, \qquad R_0 = \rho\left( F (\gamma I + L)^{-1} \right).
$$

Travel goes into $V$, because a trip moves an infected individual and does not make a new one.

**A hand example.** Two patches of equal size, with $\beta_1 = 0.3$, $\beta_2 = 0.15$ and $\gamma = 0.2$ per day, so the local reproduction numbers are $\beta_1 / \gamma = 1.5$ and $\beta_2 / \gamma = 0.75$. Infected individuals travel at rate $m$ each way. For $m = 0.05$,

$$
V = \begin{pmatrix} 0.25 & -0.05 \\ -0.05 & 0.25 \end{pmatrix}, \qquad V^{-1} = \frac{1}{0.06} \begin{pmatrix} 0.25 & 0.05 \\ 0.05 & 0.25 \end{pmatrix}, \qquad K = F V^{-1} = \begin{pmatrix} 1.25 & 0.25 \\ 0.125 & 0.625 \end{pmatrix}.
$$

With $\operatorname{tr} K = 1.875$ and $\det K = 0.75$, $R_0 = (1.875 + \sqrt{1.875^2 - 3}) / 2 \approx 1.2965$. For other travel rates:

| travel rate $m$ per day | 0 | 0.01 | 0.05 | 0.2 | 1 | 10 | $\to \infty$ |
|---|---|---|---|---|---|---|---|
| $R_0$ | 1.5 | 1.4351 | 1.2965 | 1.1830 | 1.1374 | 1.1262 | 1.125 |

Without travel, $R_0$ is that of the worse patch. With very fast travel, every infected individual spends half its time in each patch, and $R_0$ tends to $(\beta_1 + \beta_2) / (2 \gamma) = 1.125$.

## Relation to other models

- **[Kermack-McKendrick SIR](/kermack-mckendrick-sir-model/).** One patch. Very fast travel between identical patches also gives back one well-mixed population.
- **[SIR model on networks](/sir-epidemic-model/).** One node per person, with states on nodes. The metapopulation model has one node per well-mixed subpopulation, and the network carries flows of people, not single contacts.
- **[Levins metapopulation model](/levins-metapopulation-model/).** The ecological model that gave the name. It tracks only whether a patch is occupied, with rates of colonization and extinction; Keeling and Rohani (2008, section 7.2.4) treat epidemic models of this Levins type, where each patch is either infected or not.
- **Reaction-diffusion models.** With patches on a line and travel only to neighbors, the model is a discretization of a reaction-diffusion equation, and the infection spreads as a traveling wave, as in the [Fisher-KPP equation](/fisher-kpp-equation/).
- **[Agent-based epidemic simulation](/agent-based-epidemic-simulation/).** Large models for pandemic planning often combine a metapopulation model between cities with agent-based or age-structured models inside each city.
- **Vector-borne diseases.** Patches with both humans and mosquitoes give a spatial [Ross-Macdonald model](/ross-macdonald-model/).

## Known results in the model

**$R_0$ lies between the local values.** For the migration form with a common recovery rate $\gamma$, the global $R_0$ lies between the smallest and the largest local reproduction number $\beta_k / \gamma$. Proof: since the columns of $L$ sum to zero, $\mathbf{1}^\top (\gamma I + L) = \gamma \mathbf{1}^\top$, so $\mathbf{1}^\top (\gamma I + L)^{-1} = \mathbf{1}^\top / \gamma$. Let $M = (\gamma I + L)^{-1} F$. It has the same spectral radius as $K = F (\gamma I + L)^{-1}$, because $\rho(AB) = \rho(BA)$, and it is non-negative, because $(\gamma I + L)^{-1} \ge 0$. The column sums of $M$ are $\mathbf{1}^\top (\gamma I + L)^{-1} F = (\beta_1, \ldots, \beta_n) / \gamma$. The spectral radius of a non-negative matrix lies between its smallest and its largest column sum. $\blacksquare$ So travel cannot make the whole system more dangerous than its worst patch; in the example, $R_0$ falls from 1.5 toward 1.125 as travel increases, because infected individuals from patch 1 spend time in patch 2, where they transmit less.

**$R_0$ does not decide the final size.** Start the example with $10^{-4}$ of patch 1 infected and patch 2 free of infection, and solve with the [classical Runge-Kutta method](/classical-runge-kutta-4/). The fraction of the whole population ever infected is:

| travel rate $m$ | 0 | 0.001 | 0.01 | 0.05 | 0.2 |
|---|---|---|---|---|---|
| $R_0$ | 1.5 | 1.4926 | 1.4351 | 1.2965 | 1.1830 |
| fraction ever infected | 0.292 | 0.301 | 0.368 | 0.389 | 0.291 |

Without travel, the epidemic stays in patch 1 and infects the fraction $0.583$ given by the [final size relation](/final-size-relation/) with $R_0 = 1.5$, which is $0.292$ of the whole population. A little travel lowers $R_0$ but carries the epidemic to people in patch 2 who would not be reached otherwise, so the total grows. Much more travel lowers $R_0$ so far that the total falls again. In the migration form recovered individuals also travel, so at the end the counts per patch are mixed; only the total is meaningful.

**Arrival and delay.** With weak coupling, the epidemic arrives in a second patch late, after a few infected travelers start local chains. In the example with $m = 0.001$, the prevalence peaks on day 81 in patch 1 and on day 94 in patch 2. In a stochastic model, the arrival time is random, and an imported case can fail to start a local epidemic. For a patch with local $R_0$ larger than 1 and an exponential infectious period, each imported case starts a local epidemic with probability about $1 - 1/R_0$.

**Synchrony and persistence.** Stronger coupling makes the epidemics in different patches more synchronous. For an endemic infection, this has two effects that pull against each other: travel brings the infection back to a patch where it died out by chance, but synchronous patches tend to have their troughs at the same time, so all can lose the infection together (Keeling and Rohani 2008, section 7.2.2).

**Predictability on real networks.** On the worldwide airline network, Colizza and others (2006) found that the heterogeneity of the traffic flows makes the stochastic spread more predictable: a few routes carry most of the traffic, so the infection tends to follow the same paths from one run to the next.

**Computation.** The model is an ODE system with $3n$ unknowns for SIR; for $n$ in the thousands it is still small. The travel matrix is sparse, so each step of an explicit method costs time linear in the number of patches plus the number of routes.

## References
