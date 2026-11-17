---
tag: 1C6A7G
kind: model
slug: ross-macdonald-model
name: Ross-Macdonald model
aliases:
- Ross malaria model
area: biology/epidemic-and-ecological-models
level: core
summary: "A model of a vector-borne disease with coupled infection of hosts and mosquitoes. Here R0 is the square root of the product of the two legs; Macdonald used the product."
history:
  year: 1911
  people: [Ronald Ross, George Macdonald]
  note: Ross gave the coupled equations for humans and mosquitoes in 1911; Macdonald added the latent period in the mosquito and the analysis of R0 in the 1950s.
prereqs: [sis-epidemic-model, next-generation-matrix]
see_also: [basic-reproduction-number, sis-epidemic-model, next-generation-matrix, herd-immunity-threshold, power-iteration, compartmental-epidemic-model, metapopulation-epidemic-model, seir-epidemic-model]
sources:
  - book: "Ronald Ross, The Prevention of Malaria, second edition, John Murray, London, 1911"
    locator: the addendum with the mathematical theory of malaria transmission, pages 651 to 686, as cited by Smith and others (2012)
  - book: "George Macdonald, The Epidemiology and Control of Malaria, Oxford University Press, London, 1957"
    locator: the basic reproduction rate of malaria and its sensitivity to the survival of adult mosquitoes
  - paper: doi:10.1371/journal.ppat.1002588
    title: David L. Smith, Katherine E. Battle, Simon I. Hay, Christopher M. Barker, Thomas W. Scott and F. Ellis McKenzie, Ross, Macdonald, and a theory for the dynamics and control of mosquito-transmitted pathogens, PLoS Pathogens 8(4), 2012
    locator: e1002588 (the history of the model from Ross to Macdonald, the standard form of the equations, the vectorial capacity, and the common assumptions of the model)
  - paper: doi:10.1016/j.idm.2017.06.002
    title: P. van den Driessche, Reproduction numbers of infectious disease models, Infectious Disease Modelling 2(3), 2017
    locator: pages 288 to 303 (the next-generation matrix of a vector-host model, and the square root in its R0 as the geometric mean of the two legs)
  - book: isbn:9780691116174
    title: Matt J. Keeling and Pejman Rohani, Modeling Infectious Diseases in Humans and Animals, Princeton University Press, 2008
    locator: Section 4.2.2, vectored transmission (4.2.2.1 mosquito vectors)
---

The Ross-Macdonald model is the classical model of malaria and of other diseases carried by mosquitoes. It couples two [SIS models](/sis-epidemic-model/), one for humans and one for mosquitoes: an infected mosquito infects a human with a bite, and a mosquito that bites an infected human can become infected. Humans recover; mosquitoes stay infected until they die. Ronald Ross gave the first form in 1911 and showed that malaria cannot persist when the density of mosquitoes is below a critical value, so that it is not necessary to kill every mosquito. George Macdonald added the incubation period in the mosquito in the 1950s and showed that the transmission depends most strongly on the daily survival of adult mosquitoes. The model has two forms of $R_0$, and this page states both: the spectral radius of the [next-generation matrix](/next-generation-matrix/), which is the square root of the product of the two legs and is the form used on this page, and Macdonald's form, which is the product itself.

## The machine

**State.** The fraction $x$ of humans that are infected and the fraction $y$ of mosquitoes that are infectious. The total numbers of humans $H$ and of mosquitoes $M$ are constant, with $m = M / H$ mosquitoes per human.

**Parameters.**

| Symbol | Meaning |
|---|---|
| $m$ | mosquitoes per human |
| $a$ | bites on humans per mosquito per day |
| $b$ | probability that a bite by an infectious mosquito infects a human |
| $c$ | probability that a mosquito becomes infected when it bites an infected human |
| $r$ | human recovery rate per day |
| $g$ | mosquito death rate per day, so the mean life of a mosquito is $1/g$ days |
| $n$ | the extrinsic incubation period in the mosquito, in days |

**Equations.** Without the incubation period,

$$
\frac{dx}{dt} = m a b\, y (1 - x) - r x, \qquad \frac{dy}{dt} = a c\, x (1 - y) - g y .
$$

Each human receives $m a$ bites per day, a fraction $y$ of them infectious, and each infects with probability $b$. Each mosquito bites $a$ times per day, a fraction $x$ of the bites are on infected humans, and each infects the mosquito with probability $c$. With the incubation period $n$, a mosquito that is infected becomes infectious only if it survives the $n$ days, which it does with probability $e^{-g n}$. In the ODE form this adds a factor $e^{-g n}$ to the mosquito leg, or an exposed class for mosquitoes.

**Assumptions.** Homogeneous mixing of humans and mosquitoes, a constant mosquito population, no immunity in humans, no recovery in mosquitoes, and bites spread evenly over humans. Smith and others (2012) list the assumptions that later models relax, such as uneven biting and seasonal mosquito numbers.

## What it counts

**The two legs.** One infected human, during the $1/r$ days of its infection, is bitten by $m a / r$ mosquitoes, and each becomes infected with probability $c$: it infects $m a c / r$ mosquitoes. One infected mosquito survives the incubation period with probability $e^{-g n}$, then bites $a / g$ times during the rest of its life, and each bite infects a human with probability $b$: it infects $a b e^{-g n} / g$ humans.

**$R_0$ in this page: the next-generation form.** With the infected classes (infected humans, infected mosquitoes), the next-generation matrix is

$$
K = \begin{pmatrix} 0 & a b e^{-g n} / g \\ m a c / r & 0 \end{pmatrix},
$$

and

$$
R_0 = \rho(K) = \sqrt{\frac{m a^2 b c\, e^{-g n}}{r g}} .
$$

It counts infections per generation, where one generation is one leg, from human to mosquito or from mosquito to human. van den Driessche (2017) describes the square root as the geometric mean of the two legs and notes that it is often left out.

**Macdonald's form: the product.** The number of humans infected by one human through one round of mosquitoes is the product of the two legs,

$$
R_0^2 = \frac{m a^2 b c\, e^{-g n}}{r g}.
$$

Macdonald and much of the malaria literature call this product $R_0$. Both forms have the threshold 1, and they are larger than 1 together. They differ in derived numbers: the fraction by which you must cut the mosquito density to stop transmission is $1 - 1/R_0^2$ in the notation of this page.

**Vectorial capacity.** The part that depends on mosquitoes alone, $C = m a^2 e^{-g n} / g$, is the vectorial capacity: the number of infectious bites that will come in the end from all the mosquitoes that bite one infected human on one day, if every such mosquito becomes infected. Then $R_0^2 = C\, b c / r$.

**A hand example.** Take $m = 2$, $a = 0.5$, $b = c = 0.5$, $r = 0.05$, $g = 0.25$ and no incubation period. The human leg is $m a c / r = 2 \cdot 0.5 \cdot 0.5 / 0.05 = 10$ mosquitoes per human case, and the mosquito leg is $a b / g = 0.25 / 0.25 = 1$ human per mosquito. The product is 10, and $R_0 = \sqrt{10} \approx 3.162$.

## Relation to other models

- **[SIS](/sis-epidemic-model/).** Each species alone follows an SIS model, with the force of infection supplied by the other species. There is no direct transmission between humans.
- **[Next-generation matrix](/next-generation-matrix/).** The model is the standard example of an imprimitive next-generation matrix: $K$ has zero diagonal and the eigenvalues $\pm R_0$, so plain [power iteration](/power-iteration/) on $K$ alternates between two values. With the hand example, the estimates from $v = (1, 1)$ alternate between 10 and 1. Iterate with $K^2$, or with $K + I$, instead.
- **Models with more classes.** Dengue and Zika models add exposed classes in both species and immunity in humans; this gives SEIR for humans and SEI for mosquitoes, and the [SEIR model](/seir-epidemic-model/) shows how the exposed class changes $R_0$ through survival probabilities.
- **Spatial versions.** With patches of humans and mosquitoes and human travel, the model becomes a [metapopulation model](/metapopulation-epidemic-model/), and $R_0$ is again the spectral radius of a next-generation matrix.
- **Uneven biting.** If some humans are bitten more than others, $R_0$ increases; the model with even biting is a lower bound in that sense.

## Known results in the model

**Threshold.** Write $Q = R_0^2 = m a^2 b c / (r g)$ for the model without incubation. If $Q \le 1$, the infection-free state $(0, 0)$ attracts every solution. If $Q > 1$, it is unstable, and there is one endemic equilibrium in $(0, 1)^2$, which attracts every solution that starts with some infection. The system is cooperative (more infection in one species increases the growth of infection in the other), and this is the standard result for such two-dimensional SIS systems.

**The endemic equilibrium.** Set $dy/dt = 0$: $y^* = a c x^* / (a c x^* + g)$. Put this into $dx/dt = 0$ and divide by $r g$:

$$
Q (1 - x^*) = \frac{a c}{g} x^* + 1, \qquad x^* = \frac{Q - 1}{Q + a c / g} .
$$

In the hand example, $Q = 10$ and $a c / g = 1$, so $x^* = 9/11 \approx 0.818$ and $y^* = 0.2045 / 0.4545 = 0.45$. Check: $m a b y^* (1 - x^*) = 0.5 \cdot 0.45 \cdot 0.1818 \approx 0.0409 = r x^*$. So with $R_0 \approx 3.16$, about 82 percent of humans are infected at equilibrium, but fewer than half of the mosquitoes.

**Critical mosquito density.** $Q$ is linear in $m$, so transmission stops when $m < m_c = r g e^{g n} / (a^2 b c)$. In the hand example $m_c = 2 / 10 = 0.2$ mosquitoes per human. This is Ross's result: control does not need to remove all mosquitoes, only enough to bring $m$ below $m_c$.

**Sensitivity to mosquito survival.** $Q$ is proportional to $a^2$ (a mosquito must bite twice, once to be infected and once to transmit) and to $e^{-g n} / g$. Take $m = 10$, $a = 0.3$, $b = c = 0.5$, $r = 0.01$, $g = 0.1$ and $n = 10$. Then $m a^2 b c / (r g) = 225$, the survival factor is $e^{-1} \approx 0.368$, and $Q \approx 82.8$, so $R_0 \approx 9.10$. Halving the mosquito density halves $Q$ to 41.4. Doubling the death rate to $g = 0.2$, which halves the mean life of a mosquito, gives $Q = 10 \cdot 0.09 \cdot 0.25 \cdot e^{-2} / 0.002 \approx 15.2$, a reduction by a factor of 5.4. This was Macdonald's argument for insecticides that kill adult mosquitoes, which became the basis of the global eradication campaign of the 1950s and 1960s (Smith and others 2012).

**Control needed.** To bring $Q$ from 82.8 to 1 by reducing mosquito density alone, you must remove $1 - 1/82.8 \approx 98.8$ percent of the mosquitoes. In terms of the next-generation $R_0 \approx 9.10$, the same number is $1 - 1/R_0^2$, not $1 - 1/R_0 \approx 89$ percent, because a cut in mosquito density acts on only one of the two legs.

## References
