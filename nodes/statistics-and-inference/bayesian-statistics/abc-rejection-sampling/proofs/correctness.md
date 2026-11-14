---
title: The law of the values kept by the ABC rejection algorithm
proves: [correctness]
status: full
---

**Setting.** $\pi$ is a proper prior on $\Theta$. For each $\theta$, $Y \sim f(\cdot \mid \theta)$ is a simulated data set, $S$ is a summary map, $s_{\mathrm{obs}} = S(x)$ is the observed summary, $\rho \ge 0$ is a distance with $\rho(s, s') = 0$ only if $s = s'$, and $\varepsilon \ge 0$. One proposal draws $\theta \sim \pi$, then $Y \sim f(\cdot \mid \theta)$, and keeps $\theta$ when $\rho(S(Y), s_{\mathrm{obs}}) \le \varepsilon$. Write

$$a_\varepsilon(\theta) = P_\theta\big(\rho(S(Y), s_{\mathrm{obs}}) \le \varepsilon\big), \qquad A_\varepsilon = \int a_\varepsilon(\theta)\, \pi(d\theta).$$

## Claim 1: the kept values follow the $\varepsilon$-posterior

If $A_\varepsilon > 0$, the kept values are independent with law

$$\pi_\varepsilon(d\theta) = \frac{a_\varepsilon(\theta)\, \pi(d\theta)}{A_\varepsilon},$$

each proposal is kept with probability $A_\varepsilon$, and the number of proposals per kept value is geometric with mean $1/A_\varepsilon$.

*Proof.* For one proposal and a measurable set $B$, conditioning on $\theta$ gives

$$P(\theta \in B \text{ and kept}) = \int_B P_\theta(\rho(S(Y), s_{\mathrm{obs}}) \le \varepsilon)\, \pi(d\theta) = \int_B a_\varepsilon\, d\pi.$$

With $B = \Theta$ the probability of being kept is $A_\varepsilon$, and $P(\theta \in B \mid \text{kept}) = \int_B a_\varepsilon\, d\pi / A_\varepsilon = \pi_\varepsilon(B)$. Proposals use fresh randomness, so they are independent and identically distributed. The first kept proposal therefore comes after a geometric number of trials with success probability $A_\varepsilon$, its value has law $\pi_\varepsilon$, and the process starts afresh after it, which makes the kept values independent. $\blacksquare$

## Claim 2: tolerance zero with discrete data

Assume that $S(Y)$ takes countably many values and $\varepsilon = 0$. Then $a_0(\theta) = P_\theta(S(Y) = s_{\mathrm{obs}}) = f_S(s_{\mathrm{obs}} \mid \theta)$, the probability function of the summary, and the kept values follow

$$\pi_0(\theta) \propto \pi(\theta) f_S(s_{\mathrm{obs}} \mid \theta) = \pi(\theta \mid S(x) = s_{\mathrm{obs}}).$$

The acceptance probability is $A_0 = m_S(s_{\mathrm{obs}}) = \int f_S(s_{\mathrm{obs}} \mid \theta)\, \pi(d\theta)$, the marginal likelihood of the summary.

If moreover the data are discrete and $S$ is a [sufficient statistic](/sufficient-statistic/), then $\pi_0$ is the exact posterior $\pi(\theta \mid x)$.

*Proof.* Since $\rho(s, s') = 0$ only if $s = s'$, the event $\rho(S(Y), s_{\mathrm{obs}}) \le 0$ is $\{S(Y) = s_{\mathrm{obs}}\}$; Claim 1 gives the first two statements by Bayes' theorem for the observation $S(x)$. For the last one, the [Fisher-Neyman factorization theorem](/fisher-neyman-factorization-theorem/) gives $f(y \mid \theta) = g(S(y), \theta)\, h(y)$. Summing over the data sets with the observed summary,

$$f_S(s_{\mathrm{obs}} \mid \theta) = \sum_{y : S(y) = s_{\mathrm{obs}}} g(s_{\mathrm{obs}}, \theta)\, h(y) = g(s_{\mathrm{obs}}, \theta)\, c(s_{\mathrm{obs}}),$$

where $c(s_{\mathrm{obs}}) = \sum_{y : S(y) = s_{\mathrm{obs}}} h(y)$ does not depend on $\theta$. Also $f(x \mid \theta) = g(s_{\mathrm{obs}}, \theta)\, h(x)$. So $f_S(s_{\mathrm{obs}} \mid \theta)$ and $f(x \mid \theta)$ are proportional as functions of $\theta$ (when $h(x) > 0$, which holds because $x$ was observed), and the two posteriors coincide. $\blacksquare$

**Example.** For $n$ Bernoulli trials with $S$ = the number of successes and a uniform prior on $p$, $A_0 = \int_0^1 \binom{n}{s}p^s(1-p)^{n-s}\, dp = \binom{n}{s}B(s+1, n-s+1) = 1/(n+1)$ for every $s$. For $n = 10$, one proposal in $11$ is kept. With a window $|S(Y) - s| \le k$ that stays inside $\{0, \ldots, n\}$, $A_k = (2k+1)/(n+1)$.

**Insufficient summaries.** If $S$ is not sufficient, Claim 2 still holds with $\pi(\theta \mid S(x) = s_{\mathrm{obs}})$, which is a valid posterior given less information, and usually wider than $\pi(\theta \mid x)$.

## Claim 3: tolerance tending to zero with continuous summaries

Assume that $S(Y) \in \mathbb{R}^q$ has a density $f_S(s \mid \theta)$ that is continuous in $s$ at $s_{\mathrm{obs}}$ for every $\theta$ and bounded by a constant $M$, that $\rho$ is a norm, and that $m_S(s_{\mathrm{obs}}) = \int f_S(s_{\mathrm{obs}} \mid \theta)\, \pi(d\theta) > 0$. Then, as $\varepsilon \to 0$, $\pi_\varepsilon(B) \to \pi(B \mid S(x) = s_{\mathrm{obs}})$ for every measurable $B$, and $A_\varepsilon / (V_q\varepsilon^q) \to m_S(s_{\mathrm{obs}})$, where $V_q$ is the volume of the unit ball of $\rho$.

*Proof.* Let $\mathcal{B}_\varepsilon$ be the ball of radius $\varepsilon$ around $s_{\mathrm{obs}}$, of volume $V_q\varepsilon^q$. Then $a_\varepsilon(\theta)/(V_q\varepsilon^q)$ is the mean of $f_S(\cdot \mid \theta)$ over $\mathcal{B}_\varepsilon$, which tends to $f_S(s_{\mathrm{obs}} \mid \theta)$ by continuity and is bounded by $M$. By dominated convergence ($\pi$ is a probability measure), $\int_B a_\varepsilon\, d\pi / (V_q\varepsilon^q) \to \int_B f_S(s_{\mathrm{obs}} \mid \theta)\, \pi(d\theta)$ for every $B$, including $B = \Theta$. Divide the two limits. $\blacksquare$

The second limit is the curse of dimensionality: for small $\varepsilon$ the expected number of simulations per kept value is about $1/(m_S(s_{\mathrm{obs}})V_q\varepsilon^q)$, which grows like $\varepsilon^{-q}$.

## What is exact and what is measured

Claims 1 and 2 are exact: with discrete data, a sufficient summary and $\varepsilon = 0$, ABC rejection is an exact posterior sampler. The tests check Claims 1 and 2 with exact rational probabilities by listing every random path of one proposal. Claim 3 is a limit; at a fixed $\varepsilon > 0$ the error of $\pi_\varepsilon$ is not bounded here, and the page measures it.
