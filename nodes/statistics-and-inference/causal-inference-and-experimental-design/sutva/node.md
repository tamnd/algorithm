---
tag: W2HGJS
kind: definition
slug: sutva
name: Stable unit treatment value assumption
aliases:
- SUTVA
- no interference assumption
area: statistics-and-inference/causal-inference-and-experimental-design
level: core
summary: The assumption that a unit's outcome depends only on its own treatment, and that there is only one version of each treatment.
prereqs: [potential-outcomes-framework]
see_also: [average-treatment-effect, randomized-experiment, ignorability, randomized-block-design, structural-causal-model, instrumental-variables-estimation, mediation-analysis]
sources:
  - paper: doi:10.2307/2287653
    title: "Donald B. Rubin, comment on D. Basu, Randomization analysis of experimental data: the Fisher randomization test, Journal of the American Statistical Association 75(371), 1980"
    locator: the comment starting on p. 591, where the assumption is stated and named SUTVA
  - book: "D. R. Cox, Planning of Experiments, Wiley, New York, 1958"
    title: Planning of Experiments
    locator: the early chapters, on the assumption of no interference between different units (general locator, page not confirmed)
  - book: isbn:9780521885881
    title: Guido W. Imbens and Donald B. Rubin, Causal Inference for Statistics, Social, and Biomedical Sciences, Cambridge University Press, 2015
    locator: Section 1.6 (the stable unit treatment value assumption, no interference and no hidden variations of treatments)
  - paper: doi:10.1198/016214508000000292
    title: Michael G. Hudgens and M. Elizabeth Halloran, Toward causal inference with interference, Journal of the American Statistical Association 103(482), 2008
    locator: pp. 832 to 842 (partial interference, direct, indirect, total and overall effects, two-stage randomization)
  - book: isbn:9781420076165
    title: Miguel A. Hernán and James M. Robins, Causal Inference, What If, Chapman and Hall/CRC, 2020
    locator: Chapter 3 (well-defined interventions and consistency; general locator, section numbers not confirmed)
---

The stable unit treatment value assumption, SUTVA, is what makes it valid to write the outcome of unit $i$ as $Y_i(1)$ or $Y_i(0)$, with one number per treatment level. Without it, the [potential outcomes framework](/potential-outcomes-framework/) would need an outcome for each treatment vector of all $n$ units, $2^n$ numbers per unit, and the usual estimands would not be defined. Rubin named it in 1980, and the no-interference half goes back to Cox (1958). SUTVA is an assumption about the science and the treatment, not about the assignment, so randomization does not make it true.

## Definition

Let $t = (t_1, \ldots, t_n)$ be a treatment vector for $n$ units, and let $Y_i(t)$ be the outcome unit $i$ would have under $t$. SUTVA has two parts.

1. **No interference.** For every unit $i$ and all treatment vectors $t$ and $t'$ with $t_i = t'_i$, we have $Y_i(t) = Y_i(t')$. So the outcome of unit $i$ depends on $t$ only through $t_i$, and we can write $Y_i(t_i)$.
2. **No hidden versions of treatments.** Each level of treatment is one well-defined intervention. If a unit receives level $t_i$, it receives the same thing whatever the way it came to receive it, so there is one value $Y_i(t_i)$ and not one value per version.

Together the two parts give the *consistency* equation $Y_i = T_iY_i(1) + (1 - T_i)Y_i(0)$, which links the observed outcome to the potential outcomes. Some authors, such as Hernán and Robins, list consistency and no interference as separate assumptions; the content is the same.

SUTVA is not testable from the data of one ordinary design. Under a design where each unit's treatment is drawn on its own, every observed outcome is consistent with some table of outcomes $Y_i(t)$ that depends on the whole vector $t$. Designs that vary the share of treated units on purpose, such as two-stage randomization, can detect some forms of interference.

## Examples and non-examples

**Example: separate plants.** Plants in separate pots, each given a fertilizer or not. One plant's growth does not depend on what the other pots got, and the fertilizer is one product at one dose. SUTVA is plausible.

**Non-example: interference in households.** Four people live in two households, $\{1, 2\}$ and $\{3, 4\}$. The treatment is a vaccine, and the outcome is 1 if the person is protected. Suppose a person is protected if they or their housemate is vaccinated, because a vaccinated housemate does not pass the infection on. Then $Y_i(t)$ depends on the housemate's treatment, and no table of $Y_i(1), Y_i(0)$ describes it. Assign 2 of the 4 people to the vaccine at random; there are 6 assignments.

- In 2 of them, both vaccinated people share a household. The treated are protected (mean 1) and the controls, in the other household, are not (mean 0). The difference in means is 1.
- In the other 4, each household has one vaccinated person, everyone is protected, and the difference in means is 0.

The expected difference in means is $2/6 = 1/3$. But the effect of vaccinating everyone against vaccinating no one is $1 - 0 = 1$. The experiment is randomized and the estimator is the usual one, and it still estimates neither the total effect nor any per-unit effect, because the estimand it was built for does not exist here. Hudgens and Halloran (2008) give estimands for this case under *partial interference*, where units interfere only within groups: the direct effect (of one's own treatment at a fixed coverage of the group), the indirect or spillover effect (of the coverage at a fixed own treatment), and the total and overall effects.

**Non-example: hidden versions.** The treatment is "takes the drug", but some treated patients take 10 mg and others 20 mg, and the dose changes the outcome. Then $Y_i(1)$ is not one number. The observed treated outcomes mix two versions, and the estimated effect depends on the mix of doses in the study. A fix is to define the treatment more finely (two treatment levels, one per dose), or to define the estimand as the effect of the dose policy actually used.

**Non-example: an ill-defined treatment.** "Being obese" as a treatment has many versions (less food, more exercise, a different genotype), each with different effects on health. Hernán and Robins use cases like this to argue that a causal question needs a well-defined intervention before it has an answer.

**Example: a market with fixed prices.** A small online shop shows a new page to some visitors and the old page to others, and stock is never short. Each visitor's purchase depends only on the page they saw. SUTVA is plausible. In a two-sided market where treated buyers can take the stock that control buyers would have bought, it fails, and the measured difference overstates the effect of a full rollout.

## Related definitions

- [Potential outcomes framework](/potential-outcomes-framework/): the model that SUTVA makes small enough to use, with two outcomes per unit.
- [Average treatment effect](/average-treatment-effect/): defined only when each $Y_i(1)$ and $Y_i(0)$ is one number, so it needs SUTVA.
- [Ignorability](/ignorability/): the assumption on the assignment that, with SUTVA and overlap, identifies causal effects from observational data. SUTVA is about the outcomes, ignorability about who gets treated.
- [Randomized experiment](/randomized-experiment/): randomization gives ignorability by design but does not give SUTVA. Cluster designs, which randomize whole groups, are a common response to interference inside groups.
- [Structural causal model](/structural-causal-model/): in a structural model, no interference holds when the equation for $Y_i$ has $T_i$ but no other unit's treatment as an input.
- [Instrumental variables estimation](/instrumental-variables-estimation/) and [mediation analysis](/mediation-analysis/): both state a SUTVA for each of their variables, for the instrument and for the mediator as well as the treatment.

## References
