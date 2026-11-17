---
tag: W8MAKB
kind: concept
slug: compartmental-epidemic-model
name: Compartmental epidemic model
aliases:
- compartmental model
area: biology/epidemic-and-ecological-models
level: intro
summary: Split a population into classes such as susceptible, infected and recovered, and model the flows between classes with ODEs or Markov chains.
prereqs: [ode-initial-value-problem, markov-chain]
see_also: [kermack-mckendrick-sir-model, sis-epidemic-model, seir-epidemic-model, basic-reproduction-number, mass-action-kinetics, gillespie-algorithm, sir-epidemic-model, epidemic-model]
sources:
  - paper: doi:10.1098/rspa.1927.0118
    title: W. O. Kermack and A. G. McKendrick, A contribution to the mathematical theory of epidemics, Proceedings of the Royal Society of London A 115(772), 1927
    locator: pages 700 to 721 (classes of susceptible, infected and removed individuals, the rates of infection and removal, the threshold and the final size)
  - paper: doi:10.1137/S0036144500371907
    title: Herbert W. Hethcote, The mathematics of infectious diseases, SIAM Review 42(4), 2000
    locator: pages 599 to 653 (the compartment letters M, S, E, I and R, the SIR, SIS and MSEIR models, and their threshold quantities)
  - book: isbn:9780691116174
    title: Matt J. Keeling and Pejman Rohani, Modeling Infectious Diseases in Humans and Animals, Princeton University Press, 2008
    locator: Chapter 2, Introduction to simple epidemic models (sections 2.1 to 2.5, the SIR, SI, SIS, SIRS and SEIR models), and Section 3.3.1, SEIR and multi-compartment models
  - paper: "Thomas G. Kurtz, Solutions of ordinary differential equations as limits of pure jump Markov processes, Journal of Applied Probability 7(1), 1970, pages 49 to 58"
    locator: the convergence of density-dependent Markov jump processes to the solution of their ODE on finite time intervals as the population size grows
---

A compartmental epidemic model splits a population into classes, called compartments, by infection state, for example susceptible (S), infected (I) and recovered (R), and it describes how individuals flow from one class to another. The flows are written either as [ordinary differential equations](/ode-initial-value-problem/) for the class sizes or as a continuous-time [Markov chain](/markov-chain/) on the integer counts. Kermack and McKendrick (1927) gave the first general model of this type. The shorter name, without the word "epidemic", also names a different family of models in pharmacokinetics, where a drug flows between compartments of the body; this page is about epidemics only.

## In plain words

Put each person of a population into one box by health state: can catch the disease, has it and can pass it on, or is immune. Arrows join the boxes. Each arrow carries people at a rate. Recovery is the simple arrow: each sick person leaves the sick box at the same steady rate. Infection is the hard arrow: a healthy person catches the disease only by contact with a sick person, so its rate grows with both the number of healthy people and the number of sick people. The model does not follow single people. It follows only how many people are in each box. With large numbers, the counts change smoothly and you can solve equations for them. With small numbers, chance matters, and you simulate random events one at a time.

## The idea

**The state.** A model with compartments $X_1, \ldots, X_c$ has a state $x = (x_1, \ldots, x_c)$, the number of individuals in each class. In a closed population, with no births, deaths or travel, the total $N = x_1 + \cdots + x_c$ is constant. Some pages use the fractions $s = S/N$, $i = I/N$ and $r = R/N$ instead of counts, with $s + i + r = 1$; each page says which.

**The transitions.** Each arrow is a transition with a rate that depends on the state. There are two kinds:

| Transition | Change of the state | Rate | Kind |
|---|---|---|---|
| infection | $(S, I) \to (S - 1, I + 1)$ | $\beta S I / N$ | needs a contact, nonlinear |
| recovery | $(I, R) \to (I - 1, R + 1)$ | $\gamma I$ | per individual, linear |

Here $\beta$ is the transmission rate (the rate of contacts of one individual that would transmit, per unit of time) and $\gamma$ is the recovery rate. These two arrows make the SIR structure. The infection rate $\beta S I / N$ is the frequency-dependent form: the contact rate of one person does not grow with the population size. The density-dependent form $\beta S I$ assumes that the contact rate grows with the density of the population. The pages of this sub-area use the frequency-dependent form unless a page says otherwise.

**Two readings of the same arrows.** In the deterministic reading, each rate is a flow per unit of time, and the class sizes solve

$$
\frac{dS}{dt} = -\frac{\beta S I}{N}, \qquad \frac{dI}{dt} = \frac{\beta S I}{N} - \gamma I, \qquad \frac{dR}{dt} = \gamma I.
$$

In the stochastic reading, each rate is the rate of an exponential clock in a continuous-time Markov chain on integer states, and each event moves one individual. The two readings are linked by a law of large numbers: for a fixed time horizon, the fractions of the Markov chain converge in probability to the solution of the ODE as $N \to \infty$ (Kurtz 1970). For small populations, or at the start of an outbreak when only a few individuals are infected, the two readings differ, and only the stochastic one can show that an outbreak dies out by chance. The [Gillespie algorithm](/gillespie-algorithm/) simulates the stochastic reading exactly.

**The waiting time in a class.** A constant per capita exit rate $\gamma$ makes the time that one individual spends in the class exponential with mean $1/\gamma$. Real infectious periods are less spread out than an exponential. A standard fix is to split one class into $k$ stages in series, each left at rate $k \gamma$. The total time is then a sum of $k$ exponentials, with the same mean $1/\gamma$ and the variance $1/(k \gamma^2)$ instead of $1/\gamma^2$.

**The link with reaction networks.** The SIR arrows are the reactions $S + I \to 2I$ and $I \to R$ of a [chemical reaction network](/chemical-reaction-network/) under [mass action kinetics](/mass-action-kinetics/). So the tools of that field apply directly: the stoichiometric matrix, the [chemical master equation](/chemical-master-equation/) for the stochastic reading, and the ODE solvers for the deterministic one, such as the [Runge-Kutta methods](/runge-kutta-methods/).

**Threshold quantities.** The basic question about a model is whether one infected individual starts a growing outbreak in a susceptible population. The answer is the [basic reproduction number](/basic-reproduction-number/) $R_0$: the outbreak grows when $R_0 > 1$. For the SIR equations above, $R_0 = \beta / \gamma$. For models with several infected classes, $R_0$ comes from the [next-generation matrix](/next-generation-matrix/).

## Examples

**A hand computation of the flows.** Take SIR flows with $N = 1000$, $\beta = 0.3$ per day and $\gamma = 0.1$ per day, and the state $S = 990$, $I = 10$, $R = 0$. The infection flow is $0.3 \cdot 990 \cdot 10 / 1000 = 2.97$ per day, and the recovery flow is $0.1 \cdot 10 = 1$ per day. In the deterministic reading, $dI/dt = 2.97 - 1 = 1.97$ per day, so the outbreak grows. In the stochastic reading, the total event rate is $3.97$ per day, the mean time to the next event is $1/3.97 \approx 0.252$ days, and the next event is an infection with probability $2.97 / 3.97 \approx 0.748$. Here $R_0 = 0.3 / 0.1 = 3$.

**The standard structures.** The letters name the classes in the order in which an individual passes through them (Hethcote 2000):
- SI: no recovery; each infected individual stays infected. Push gossip in [distributed systems](/epidemic-model/) has this form.
- [SIS](/sis-epidemic-model/): recovery gives no immunity, so the infection can persist at an endemic level. Many bacterial infections are modeled this way.
- [SIR](/kermack-mckendrick-sir-model/): recovery gives lasting immunity. The epidemic ends with some susceptibles left.
- SIRS: immunity wanes, and recovered individuals return to S at a rate.
- [SEIR](/seir-epidemic-model/): an exposed class E holds individuals who are infected but not yet infectious.
- MSEIR: a class M of newborns protected by maternal antibodies comes before S.

**Models with more structure.** Classes can also be split by a second variable, which gives more compartments with the same rules:
- by host species, as in the [Ross-Macdonald model](/ross-macdonald-model/) of malaria, with infected humans and infected mosquitoes
- by place, as in the [metapopulation epidemic model](/metapopulation-epidemic-model/), with one set of classes for each city
- by number of contacts, as in the [degree-based mean-field model](/heterogeneous-mean-field-epidemic/), with one set of classes for each degree of a contact network
- by age or risk group, with a contact matrix between groups (Keeling and Rohani 2008, chapter 3)

**A non-example.** An agent-based simulation that stores the full state of each person, with a home, a workplace and a contact list, is not a model of this kind, because the state is not a vector of class counts. The [SIR model on networks](/sir-epidemic-model/) is also not compartmental in this sense: its state is the class of each node of a graph.

## Where it is used

- **Outbreak response.** Fitted SIR and SEIR models estimate the growth rate and $R_0$ at the start of an outbreak, and project the peak and the final size under different interventions.
- **Vaccination policy.** The models give the [herd immunity threshold](/herd-immunity-threshold/) and show how a vaccination program changes the age at infection and the interval between epidemics.
- **Theory.** The [final size relation](/final-size-relation/), the threshold theorem and the endemic equilibria are results about compartmental epidemic models.
- **Computation.** The deterministic reading is an [initial value problem](/ode-initial-value-problem/), often solved with the [classical Runge-Kutta method](/classical-runge-kutta-4/). The stochastic reading is simulated event by event or approximated with leaps.
- **Outside biology.** The same equations model the spread of messages in [gossip protocols](/epidemic-model/), where "infected" means a node that has an update and spreads it, and the spread of rumors.

## References
