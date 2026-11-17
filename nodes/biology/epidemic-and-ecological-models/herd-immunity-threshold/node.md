---
tag: 3R3M65
kind: definition
slug: herd-immunity-threshold
name: Herd immunity threshold
aliases:
- critical vaccination fraction
area: biology/epidemic-and-ecological-models
level: intro
summary: "The immune fraction 1 - 1/R0 above which each infection causes less than one new infection on average, for homogeneous mixing and a sterilizing vaccine."
prereqs: [basic-reproduction-number]
see_also: [final-size-relation, next-generation-matrix, kermack-mckendrick-sir-model, heterogeneous-mean-field-epidemic, epidemic-threshold, branching-process-extinction-theorem, galton-watson-process, seir-epidemic-model]
sources:
  - paper: doi:10.1093/cid/ciq152
    title: Paul Fine, Ken Eames and David L. Heymann, Herd immunity, a rough guide, Clinical Infectious Diseases 52(7), 2011
    locator: pages 911 to 916 (the meanings of the term, the threshold 1 - 1/R0 under random mixing, the effect of vaccine efficacy, and a table of R0 values and thresholds for common infections)
  - book: isbn:9780691116174
    title: Matt J. Keeling and Pejman Rohani, Modeling Infectious Diseases in Humans and Animals, Princeton University Press, 2008
    locator: Section 8.1, vaccination (8.1.3 random mass vaccination, 8.1.4 imperfect vaccines, 8.1.7 targeted vaccination), and Section 3.2.1.3, control by vaccination in age-structured models
  - book: isbn:9780198545996
    title: Roy M. Anderson and Robert M. May, Infectious Diseases of Humans, Dynamics and Control, Oxford University Press, 1991
    locator: Part I, microparasites (the vaccination coverage needed to eliminate an infection, and its dependence on R0 and on the age at vaccination)
---

The herd immunity threshold is the fraction of a population that must be immune so that an infection, on average, cannot replace itself: each case then causes fewer than one new case, and an introduced infection dies out. In the simplest setting, with homogeneous mixing and immunity that fully blocks infection, it is $p_c = 1 - 1/R_0$, where $R_0$ is the [basic reproduction number](/basic-reproduction-number/). Above the threshold, people who are not immune are also protected, because the chains of transmission that would reach them break. The term "herd immunity" itself is used in several senses (Fine, Eames and Heymann 2011); this page is about the threshold.

## Definition

Take a population with homogeneous mixing, and let a fraction $p$ of it be immune at the start, by vaccination or past infection. Assume that the immunity is sterilizing: an immune person can neither be infected nor transmit. A new case then meets a susceptible person with probability $1 - p$ instead of 1, so it causes on average

$$
R_{\mathrm{eff}} = R_0 (1 - p)
$$

new infections. The herd immunity threshold is the value of $p$ at which $R_{\mathrm{eff}} = 1$:

$$
p_c = 1 - \frac{1}{R_0}, \qquad R_0 > 1 .
$$

If $p > p_c$, then $R_{\mathrm{eff}} < 1$, the disease-free state is stable, and an introduced infection causes only a small outbreak. If $p < p_c$, a large outbreak is possible. In the [Kermack-McKendrick model](/kermack-mckendrick-sir-model/) the same number appears in a second way: the number of infected people grows while the susceptible fraction is above $1/R_0$ and falls once it is below, so the epidemic peaks exactly when the immune fraction reaches $p_c$.

**Vaccine efficacy.** Most vaccines do not protect everyone. If a vaccine gives full, lasting immunity to a fraction $E$ of the people who receive it and none to the rest, then a coverage $v$ makes a fraction $v E$ immune, and the vaccine coverage needed is

$$
v_c = \frac{1 - 1/R_0}{E} .
$$

A vaccine that instead lowers the susceptibility of every vaccinated person by the factor $1 - E$ gives the same $R_{\mathrm{eff}} = R_0 (1 - v E)$ at the start of an outbreak, so the same $v_c$. If $v_c > 1$, vaccination with that vaccine alone cannot stop transmission.

## Examples and non-examples

**Hand values.** For $R_0 = 2$, $p_c = 0.5$; for $R_0 = 3$, $p_c = 2/3$; for $R_0 = 4$, $p_c = 0.75$. Measles has an $R_0$ that is often given as 12 to 18, which gives $p_c = 11/12 \approx 0.917$ to $17/18 \approx 0.944$ (Fine, Eames and Heymann 2011 give a table for many infections).

**With efficacy.**

| $R_0$ | efficacy $E$ | $p_c$ | coverage needed $v_c$ |
|---|---|---|---|
| 2 | 0.9 | 0.5 | 0.556 |
| 4 | 0.9 | 0.75 | 0.833 |
| 10 | 0.8 | 0.9 | 1.125, so impossible |

**Small outbreaks above the threshold.** Above the threshold, cases still happen; they come in short chains. At the start of an outbreak the cases form a [Galton-Watson process](/galton-watson-process/) with mean offspring $R_{\mathrm{eff}} < 1$, and the expected total size of a chain started by one case is

$$
1 + R_{\mathrm{eff}} + R_{\mathrm{eff}}^2 + \cdots = \frac{1}{1 - R_{\mathrm{eff}}} .
$$

With $R_0 = 4$ and $p = 0.8$, $R_{\mathrm{eff}} = 0.8$ and the mean chain size is 5 cases. Just above the threshold, chains are long: with $R_{\mathrm{eff}} = 0.95$, the mean is 20 cases. Below the threshold, with $R_{\mathrm{eff}} > 1$, a chain becomes a large outbreak with a positive probability, given by the [branching process extinction theorem](/branching-process-extinction-theorem/).

**Non-example: the final size.** The fraction of people infected in an epidemic without control is larger than $p_c$. For $R_0 = 2$, the [final size relation](/final-size-relation/) gives about 0.797, against $p_c = 0.5$. The epidemic overshoots the threshold, because many people are still infectious when the immune fraction reaches $p_c$. So "the share infected when herd immunity is reached" and "the share infected at the end" are different numbers.

**Non-example: uneven mixing.** With groups that mix unevenly, $R_0$ is the spectral radius of the [next-generation matrix](/next-generation-matrix/), and the coverage needed depends on who is vaccinated. Take two groups of equal size with

$$
K = \begin{pmatrix} 3 & 1 \\ 1 & 0.5 \end{pmatrix},
$$

so $R_0 \approx 3.351$. The same coverage in both groups must reach $1 - 1/3.351 \approx 0.702$. Vaccinating 80 percent of group 1 only multiplies the first row by 0.2 and gives $K' = \begin{pmatrix} 0.6 & 0.2 \\ 1 & 0.5 \end{pmatrix}$, with $\operatorname{tr} K' = 1.1$, $\det K' = 0.1$ and the eigenvalues 1 and 0.1. So the threshold is reached with an overall coverage of only 0.4. On contact networks with a wide spread of degrees, the same effect is much larger: vaccinating the people with the most contacts is far more effective than random vaccination (see the [degree-based mean-field model](/heterogeneous-mean-field-epidemic/)).

**Non-example: immunity that does not block transmission.** A vaccine that prevents disease but not infection or transmission protects the person who receives it, but it does not lower $R_{\mathrm{eff}}$ and does not count toward the threshold.

**Non-example: waning immunity and births.** The threshold is a statement about one moment. With births of susceptible children or with immunity that wanes, the immune fraction falls over time, and it must be kept above $p_c$, for example by vaccinating each birth cohort at coverage at least $v_c$.

## Related definitions

- **[Basic reproduction number](/basic-reproduction-number/).** The only input of the simple threshold.
- **Effective and control reproduction numbers.** $R_{\mathrm{eff}} = R_0 (1 - p)$ in the simple model; the threshold is the point where the control reproduction number is 1.
- **[Epidemic threshold](/epidemic-threshold/).** The value of a spreading parameter at which $R_0 = 1$. The herd immunity threshold moves the population to that boundary by removing susceptibles.
- **[Final size relation](/final-size-relation/).** The fraction infected in an uncontrolled epidemic, always larger than $p_c$.
- **Vaccine coverage needed.** The coverage $v_c = p_c / E$ for a vaccine of efficacy $E$. It equals $p_c$ only for a perfect vaccine in a population with homogeneous mixing.

## References
