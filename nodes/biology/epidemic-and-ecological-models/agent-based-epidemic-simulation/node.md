---
tag: Z8MG22
kind: technique
slug: agent-based-epidemic-simulation
name: Agent-based epidemic simulation
aliases:
- individual-based epidemic model
area: biology/epidemic-and-ecological-models
level: core
summary: Simulate each person with a household, workplace and contacts, and spread infection by chance events between them over time.
history:
  year: 2004
  people: [Stephen Eubank, Neil M. Ferguson]
  note: Eubank and coauthors simulated a city as a network of people and places in 2004, and Ferguson and coauthors used an agent-based model of a population in Southeast Asia to test plans for containing pandemic influenza in 2005.
prereqs: [sir-epidemic-model, stochastic-sir-model, reed-frost-model]
see_also: [reed-frost-model, stochastic-sir-model, metapopulation-epidemic-model, configuration-model, approximate-bayesian-computation, particle-filter, gillespie-algorithm, cellular-automaton]
sources:
  - paper: "Stephen Eubank, Hasan Guclu, V. S. Anil Kumar, Madhav V. Marathe, Aravind Srinivasan, Zoltan Toroczkai and Nan Wang, Modelling disease outbreaks in realistic urban social networks, Nature 429, 2004"
    title: Eubank et al. 2004
    locator: a synthetic population of a city with daily activities at locations, the contact network it implies, and the simulation of smallpox outbreaks and interventions on it
  - paper: "Neil M. Ferguson, Derek A. T. Cummings, Simon Cauchemez, Christophe Fraser, Steven Riley, Aronrag Meeyai, Sopon Iamsirithaworn and Donald S. Burke, Strategies for containing an emerging influenza pandemic in Southeast Asia, Nature 437, 2005"
    title: Ferguson et al. 2005
    locator: an individual-based model with households, schools, workplaces and random contacts in space, and the effect of antiviral treatment, prophylaxis and social distancing on containment
  - book: isbn:9780691116174
    title: Matt J. Keeling and Pejman Rohani, Modeling Infectious Diseases in Humans and Animals, Princeton University Press, 2008
    locator: the chapters on stochastic dynamics and on spatial and network structure
---

An agent-based epidemic simulation represents every person of a population as a separate object. Each agent has a disease state, such as susceptible, exposed, infectious or recovered, and fixed attributes, such as age, household, school or workplace, and place of home. The agents meet in these settings, and at each meeting with an infectious agent, a susceptible agent is infected with a probability that depends on the setting and on the time they spend together. A run of the simulation is one possible course of the epidemic. Many runs with different random seeds give the distribution of outcomes, such as the attack rate, the peak and the effect of an intervention. The compartmental [SIR model](/sir-epidemic-model/) and its [stochastic form](/stochastic-sir-model/) are the special case where every agent is the same and everybody meets everybody.

## In plain words

Instead of tracking only how many people are sick, the computer keeps a record for each person: where the person lives, works or goes to school, and whether the person is healthy, sick or immune. Each day, the people in the same home, class or office meet. A sick person can pass the disease on at each meeting, and the computer decides by a roll of a die whether this happens.

So you can try rules on single people or places, like closing schools, or giving a vaccine to old people first, and see what changes. Because chance decides the result, one run is only one possible story. You run it many times and look at the spread of the results.

## When it applies

- **Heterogeneity matters.** Contacts differ by age, household size, job and place, and the differences change the outcome. An average rate in a compartmental model hides them.
- **Interventions act on people or places.** School closures, workplace closures, contact tracing, quarantine of households and vaccination of chosen groups are rules on individuals or settings. An agent-based model represents each of them directly.
- **Small numbers and chance.** Early in an outbreak, or in a small community, chance decides whether the disease dies out or spreads. The model keeps every chance event, as the [Reed-Frost model](/reed-frost-model/) does for a single group.
- **Contact structure.** Infection spreads along a contact network, such as a [configuration model](/configuration-model/) or a [small-world network](/small-world-network/), and the [epidemic threshold](/epidemic-threshold/) depends on the network, not only on the mean number of contacts.

It is the wrong tool when only the aggregate curve is needed and the data cannot support the extra parameters. A compartmental [epidemic model](/epidemic-model/) is then simpler, faster and easier to fit.

## The template

1. **Build the population.** Make $N$ agents with attributes drawn from census data, and group them into households, schools, workplaces and other settings. The result is a synthetic population: no agent is a real person, but the joint distribution of the attributes matches the data.
2. **Define the contacts.** For each setting $c$, set a transmission rate $\beta_c$ and a rule for who meets whom: all members of a household, the pupils of a class, a random sample of a workplace, or random contacts that fall off with distance.
3. **Define the natural history.** Give each agent a state machine, for example S to E to I to R. When an agent enters a state, draw the time it stays there from a distribution, such as a gamma law for the latent and infectious periods. Fixed or gamma periods are more realistic than the exponential periods of a Markov model.
4. **Step through time.** In each step of length $\Delta t$, compute for each susceptible agent $k$ the force of infection $\lambda_k = \sum_c \beta_c \sum_{j} w_{jk}^{c}$, where the inner sum runs over the infectious agents $j$ that share setting $c$ with $k$ and $w_{jk}^{c}$ is the weight of their contact. Agent $k$ is infected in the step with probability $1 - e^{-\lambda_k \Delta t}$. Then advance the timers of the natural history and update all states together.
5. **Add the interventions.** Write each one as a rule that changes the settings, the weights or the states, for example "close schools when the weekly count of cases passes a threshold".
6. **Repeat.** Run the model from many seeds, with a separate random stream for each run, and report the distribution of the outcomes. To compare two interventions, use the same seeds for both.
7. **Calibrate.** Fit the free rates to data, such as the growth rate, the attack rates by age or the household secondary attack rate. The likelihood of an agent-based model is rarely available, so use methods that need only simulation, such as [approximate Bayesian computation](/approximate-bayesian-computation/), or a [particle filter](/particle-filter/) inside [sequential Monte Carlo](/sequential-monte-carlo/) when there is a time series of counts.

The rule $1 - e^{-\lambda \Delta t}$ in step 4 is the probability that at least one infectious contact succeeds when the sources act independently with constant hazards. It equals $1 - \prod_j (1 - p_j)$ with $p_j = 1 - e^{-\beta_c w_{jk}^c \Delta t}$, the escape form of the Reed-Frost chain binomial. An event-driven version replaces the time steps by the [Gillespie algorithm](/gillespie-algorithm/) on the individual events, which avoids the error of a fixed step but is slower when there are many agents.

## Classic examples

**The Reed-Frost model as the smallest case.** Put all agents in one setting where everybody meets everybody, give each infectious agent a period of exactly one step, and let each contact infect with probability $p$. Then the number of new cases in each step, given the current state, is binomial with $S$ trials and the probability $1 - (1 - p)^{I}$. This is the [Reed-Frost model](/reed-frost-model/), and it gives a check for any implementation: the distribution of the final size from many runs must match the exact one.

**The general stochastic epidemic.** With one setting, $\lambda_k = \beta I / N$ for every susceptible agent, exponential infectious periods and an event-driven update, the model is the [stochastic SIR model](/stochastic-sir-model/). The labels of the agents carry no information, and the counts $(S, I)$ form a Markov chain.

**A city as a network of places.** Eubank and coauthors built a synthetic population of a large city, with the daily activities of each person at locations, and simulated smallpox outbreaks on the contact network that this gave. They used it to compare interventions, such as targeted and mass vaccination.

**Containment of pandemic influenza.** Ferguson and coauthors simulated a population in Southeast Asia with households, schools, workplaces and random contacts in space. They asked whether a new influenza strain could be stopped at the source by antiviral treatment of cases and of their contacts, with social distancing. The answer depended on $R_0$ and on how fast cases were found.

**Households and wards.** Smaller agent-based models of households, hospital wards or farms track every person by name. For these the likelihood is sometimes tractable once the event times are known, and [data augmentation MCMC](/epidemic-data-augmentation-mcmc/) fits them.

## Variations

- **Network models.** The contacts are the edges of a fixed or changing graph, and infection passes along edges. On a static network, a model with fixed infectious periods maps to bond [percolation](/percolation/).
- **Metapopulation models.** Agents of the same patch are grouped into counts, and only movement between patches is explicit. A [metapopulation model](/metapopulation-epidemic-model/) is a middle way between an agent-based model and one compartmental model.
- **Degree-based mean field.** The [heterogeneous mean-field model](/heterogeneous-mean-field-epidemic/) keeps only the number of contacts of each agent, and it gives the threshold on a network with a known degree distribution in closed form.
- **Lattices and cellular automata.** Agents sit on the cells of a grid and infect their neighbours, as in a [cellular automaton](/cellular-automaton/). This suits plant disease and other spread in space.
- **Approximate time stepping.** For counts in large groups, [tau-leaping](/tau-leaping/) moves many events in one step. Hybrid models treat large groups as counts and small groups as agents.
- **Emulators.** A statistical model trained on runs of the simulation predicts its output at new parameter values. This makes calibration and the study of sensitivity possible when each run is costly.

## Pitfalls

- **Too many parameters.** Every setting, age group and stage adds rates and distributions. Most of them cannot be estimated from the available data, so different values fit equally well and give different predictions. Fix what other studies measure, fit few rates, and report the sensitivity to the rest.
- **Too few runs.** One run is one random outcome. Near the threshold, the runs split into small outbreaks and large ones. Report the share of each and the distribution within each, not one mean.
- **The size of the time step.** The rule $\beta \Delta t$ in place of $1 - e^{-\beta \Delta t}$ can give a probability above 1. A long step also lets an agent infect others in the same step in which it was infected, or misses it, depending on the order of the updates. Update all states together at the end of a step, and check that the results do not change when $\Delta t$ is halved.
- **Comparing interventions with independent noise.** If two scenarios use different random draws, their difference has the noise of both. Use the same seeds for both, so the variance of the difference falls when the outcomes are positively correlated.
- **The reproduction number is an output.** In an agent-based model, $R_0$ follows from the rates, the settings and the periods. Fit the rates so that the model gives the observed growth rate, and compute $R_0$ from the simulated first generations, not from one rate alone.
- **Errors in the synthetic population.** If households, schools or workplaces have the wrong sizes or mix the wrong ages, the model is wrong in exactly the places where it should be better than a compartmental model.
- **Reproducibility.** Results depend on the code, the seeds and many small choices. Publish the code and the seeds, and describe the model fully enough that others can build it again.

## Exercises

1. Show that the model in the first classic example is the Reed-Frost model. Find the probability that one initial case in a group of 3 susceptibles infects nobody, and the probability that all 3 are infected.
2. Let agent $k$ have independent contacts with infectious agents $j = 1, \ldots, m$, each with a constant hazard $h_j$ over a step of length $\Delta t$. Show that the probability that $k$ escapes infection in the step is $e^{-\Delta t \sum_j h_j}$, and that this equals $\prod_j (1 - p_j)$ with $p_j = 1 - e^{-h_j \Delta t}$.
3. In a model with one setting, $\lambda_k = \beta I/N$ and exponential infectious periods with rate $\gamma$, take a step $\Delta t$ in which each infectious agent recovers with probability $1 - e^{-\gamma \Delta t}$. Show that the probability of two or more events in one step is $O(\Delta t^2)$, and explain why the time-stepped model approaches the stochastic SIR model as $\Delta t \to 0$.
4. Two scenarios give outcomes $X$ and $Y$ with the same variance $\sigma^2$ and correlation $\rho$. Find the variance of $X - Y$, and the factor by which common seeds reduce the number of runs needed for a given precision of the difference when $\rho = 0.9$.
5. A population is made of households of size 2. In a household, an infectious person infects the other member with probability $q$, and outside the household each infectious person causes on average $m$ infections in other households, which have no other cases. Show that the mean number of households infected by one infected household is $m(1 + q)$, and find the condition on $m$ and $q$ for a large outbreak.

## References
