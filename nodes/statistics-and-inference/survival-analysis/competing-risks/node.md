---
tag: 15GS60
kind: concept
slug: competing-risks
name: Competing risks
aliases:
- competing risks analysis
- cause-specific hazard
area: statistics-and-inference/survival-analysis
level: advanced
summary: Several kinds of event can end follow-up, and one prevents the others. One minus Kaplan-Meier then overstates the risk of each kind.
prereqs: [survival-function, hazard-function, censoring, kaplan-meier-estimator]
see_also: [aalen-johansen-estimator, fine-gray-model, nelson-aalen-estimator, cox-proportional-hazards-model, markov-chain, frailty-model, log-rank-test, inverse-probability-weighting]
sources:
  - paper: doi:10.1073/pnas.72.1.20
    title: Anastasios Tsiatis, A nonidentifiability aspect of the problem of competing risks, Proceedings of the National Academy of Sciences 72(1), 1975
    locator: pp. 20 to 22 (every joint law of the latent failure times has an independent counterpart with the same observable law)
  - paper: doi:10.1002/sim.2712
    title: H. Putter, M. Fiocco and R. B. Geskus, Tutorial in biostatistics, competing risks and multi-state models, Statistics in Medicine 26(11), 2007
    locator: pp. 2389 to 2430 (cause-specific hazards, cumulative incidence, the bias of one minus Kaplan-Meier, and regression on the cause-specific and subdistribution hazards)
  - paper: doi:10.1214/aos/1176350951
    title: Robert J. Gray, A class of K-sample tests for comparing the cumulative incidence of a competing risk, Annals of Statistics 16(3), 1988
    locator: pp. 1141 to 1154 (the subdistribution hazard and the test that compares cumulative incidence functions between groups)
  - paper: doi:10.1080/01621459.1999.10474144
    title: Jason P. Fine and Robert J. Gray, A proportional hazards model for the subdistribution of a competing risk, Journal of the American Statistical Association 94(446), 1999
    locator: pp. 496 to 509 (regression on the subdistribution hazard, so that coefficients act on the cumulative incidence)
  - book: isbn:9780471363576
    title: John D. Kalbfleisch and Ross L. Prentice, The Statistical Analysis of Failure Time Data, 2nd edition, Wiley, 2002
    locator: Chapter 8 (competing risks and multistate models, cause-specific hazards and the latent failure time approach)
---

In a competing risks problem each subject can have one of several kinds of event, and the first event ends the follow-up for the others. A patient who dies of heart disease can no longer die of cancer. A loan that is repaid early can no longer default. The data are the time of the first event and its cause, or a censoring time. The quantity people usually want is the cumulative incidence of one cause, $F_k(t) = P(T \le t, \text{cause} = k)$, the probability of having had an event of that kind by time $t$. The common mistake is to treat the other causes as censoring and report one minus the [Kaplan-Meier](/kaplan-meier-estimator/) estimate. That estimates a different quantity, and it is never smaller than $F_k$.

## In plain words

Suppose half of a group of old patients die of cancer and the other half die of something else first. Count the deaths from other causes as "censored", meaning "we stopped watching, but they could still get cancer later", and Kaplan-Meier pretends those people stay in a world where they might still die of cancer. In that pretend world, almost everyone eventually dies of cancer. But a person who died of a stroke will never die of cancer. So one minus Kaplan-Meier answers a question about a world without the other causes, and it overstates the real chance of dying of cancer. The cumulative incidence counts each person's actual first event.

## The idea

**The data.** Each subject has a time $T$ to the first event and a cause $\varepsilon \in \{1, \ldots, K\}$. With censoring at $C$ we observe $y = \min(T, C)$ and $\varepsilon$ when $T \le C$, or $0$ when censored. Censoring is assumed independent, as on the [censoring](/censoring/) page.

**Cause-specific hazards.** The hazard of cause $k$ is

$$h_k(t) = \lim_{\Delta \downarrow 0}\frac{P(t \le T < t + \Delta,\ \varepsilon = k \mid T \ge t)}{\Delta}.$$

It is the rate of events of type $k$ among the subjects still free of any event. The all-cause hazard is $h = \sum_k h_k$, with $H_k(t) = \int_0^t h_k$ and the all-cause survival $S(t) = P(T > t) = \exp(-\sum_k H_k(t))$ for continuous $T$. The cause-specific hazards are identified from the data: the [Nelson-Aalen estimator](/nelson-aalen-estimator/) that counts only the events of cause $k$ estimates $H_k$, with all subjects that are event-free and uncensored in the risk set.

**Cumulative incidence.** The cumulative incidence function (CIF) of cause $k$ is

$$F_k(t) = P(T \le t, \varepsilon = k) = \int_0^t S(u-)\, dH_k(u).$$

To have an event of cause $k$ at $u$, a subject must be free of all events just before $u$, which has probability $S(u-)$, and then have cause $k$ at rate $h_k(u)$. So $F_k$ depends on all the cause-specific hazards through $S$, not only on $h_k$.

**The CIFs and $S$ add up to $1$.** For every $t$, $\sum_{k=1}^K F_k(t) + S(t) = 1$. *Proof (continuous $T$).* $\sum_k F_k(t) = \int_0^t S(u)\sum_k h_k(u)\,du = \int_0^t S(u)h(u)\,du = \int_0^t (-S'(u))\,du = 1 - S(t)$, since $S' = -hS$. $\square$ Each subject has either had exactly one first event by $t$ or is still event-free, so this is what one expects. The [Aalen-Johansen estimator](/aalen-johansen-estimator/) has the same property exactly, as its correctness proof shows.

**One minus Kaplan-Meier overstates the risk.** Treating the other causes as censoring, the Kaplan-Meier product with only cause-$k$ events estimates $S_k^\ast(t) = \exp(-H_k(t))$. For every $t$, $1 - S_k^\ast(t) \ge F_k(t)$. *Proof.* $1 - e^{-H_k(t)} = \int_0^t e^{-H_k(u)}h_k(u)\,du$, and $S(u) = e^{-H_k(u)}e^{-\sum_{l \ne k}H_l(u)} \le e^{-H_k(u)}$. So the integrand of $F_k$ is never larger. $\square$ Equality holds only when the other causes have no hazard before $t$ where $h_k > 0$. The gap grows with the other hazards. The sum $\sum_k (1 - S_k^\ast(t))$ can exceed $1$, which no set of probabilities of disjoint events can do.

**What $1 - S_k^\ast$ means.** Think of latent times $T_1, \ldots, T_K$, one for each cause, with $T = \min_k T_k$. If they are independent, $S_k^\ast(t) = P(T_k > t)$, the survival from cause $k$ in a world where the other causes are removed. That is a hypothetical quantity. Worse, Tsiatis (1975) showed that for every joint law of the latent times there is a law with independent latent times that gives the same distribution of $(T, \varepsilon)$. So independence cannot be checked from the data, and the "net" risk $1 - S_k^\ast$ is not identified without it. The cause-specific hazards and the CIFs are identified without any assumption about the latent times.

**Regression.** Two kinds of model are used, and they answer different questions.

- *Cause-specific hazards.* Fit a [Cox model](/cox-proportional-hazards-model/) to $h_k$, censoring the other causes. This is valid for the cause-specific hazard. Its coefficients describe the rate of cause $k$ among event-free subjects, which is the right target for questions of cause and mechanism.
- *Subdistribution hazards.* The [Fine-Gray model](/fine-gray-model/) puts the proportional hazards form on $\tilde h_k = -\frac{d}{dt}\log(1 - F_k(t))$, so its coefficients act directly on $F_k$. This is the right target for prediction of the absolute risk of cause $k$.

A covariate can have no effect on $h_1$ and still change $F_1$, by changing $h_2$: if it doubles the hazard of death from other causes, fewer subjects live long enough to have cause 1, so $F_1$ falls.

## Examples

**Constant hazards.** Let $h_1 = \lambda_1$ and $h_2 = \lambda_2$ be constant. Then $S(t) = e^{-(\lambda_1 + \lambda_2)t}$ and

$$F_1(t) = \frac{\lambda_1}{\lambda_1 + \lambda_2}\bigl(1 - e^{-(\lambda_1 + \lambda_2)t}\bigr), \qquad 1 - S_1^\ast(t) = 1 - e^{-\lambda_1 t}.$$

With $\lambda_1 = \lambda_2 = 1$, as $t \to \infty$, $F_1 \to 1/2$, the true share of cause 1, while $1 - S_1^\ast \to 1$. At $t = 1$, $F_1 = (1 - e^{-2})/2 = 0.432$ and $1 - S_1^\ast = 1 - e^{-1} = 0.632$.

**A hand example with censoring.** Six subjects with times $1, 2, 2, 3, 4, 5$ and causes $1, 2, 0, 1, 0, 2$, where $0$ means censored. The Aalen-Johansen estimate, computed in exact fractions by the reference code of the [Aalen-Johansen](/aalen-johansen-estimator/) page:

| $t$ | at risk | event | $\hat F_1(t)$ | $\hat F_2(t)$ | $\hat S(t)$ | $1 - \hat S_1^\ast(t)$ | $1 - \hat S_2^\ast(t)$ |
|---|---|---|---|---|---|---|---|
| 1 | 6 | cause 1 | 1/6 | 0 | 5/6 | 1/6 | 0 |
| 2 | 5 | cause 2, one censored | 1/6 | 1/6 | 2/3 | 1/6 | 1/5 |
| 3 | 3 | cause 1 | 7/18 | 1/6 | 4/9 | 4/9 | 1/5 |
| 5 | 1 | cause 2 | 7/18 | 11/18 | 0 | 4/9 | 1 |

At every row $\hat F_1 + \hat F_2 + \hat S = 1$. The naive estimates are larger: $4/9 > 7/18$ for cause 1 at $t = 3$, and $1 > 11/18$ for cause 2 at $t = 5$. At $t = 5$ the two naive risks add up to $13/9 > 1$.

**Not competing risks.** If the second event does not prevent the first, as with a hospital admission that a later death does not erase, the data are a multi-state or recurrent event problem. If the "other cause" is a loss to follow-up that has nothing to do with the event, it is ordinary censoring and Kaplan-Meier is right.

## Where it is used

- **Medicine.** Death from the disease under study against death from other causes, relapse against death in remission, and graft failure against death with a working graft. Elderly populations, where other causes are common, are where one minus Kaplan-Meier is most wrong.
- **Reliability.** A device with several failure modes, where the first failure ends its life.
- **Finance.** Default against prepayment of loans and mortgages.
- **Estimation.** The [Aalen-Johansen estimator](/aalen-johansen-estimator/) gives the CIFs nonparametrically, and it extends to multi-state models, where competing risks is the case with one starting state and $K$ absorbing states of a [Markov chain](/markov-chain/) in continuous time.
- **Testing.** Gray's (1988) test compares the CIFs of groups. The [log-rank test](/log-rank-test/) applied to one cause, with the others censored, compares the cause-specific hazards, which is a different hypothesis.
- **Regression.** Cause-specific Cox models and the [Fine-Gray model](/fine-gray-model/). Putter, Fiocco and Geskus (2007) recommend reporting both kinds of model.
- **Dependent latent times.** Models with correlated [frailties](/frailty-model/) for the causes describe dependent latent times, but by Tsiatis's result their dependence comes from the model, not from the data.

## References
