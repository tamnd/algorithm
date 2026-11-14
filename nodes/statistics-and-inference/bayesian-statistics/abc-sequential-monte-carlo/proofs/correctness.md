---
title: The importance weights of ABC sequential Monte Carlo
proves: [correctness]
status: full
---

**Setting.** $\pi$ is a prior density on $\Theta \subseteq \mathbb{R}^d$. For a tolerance $\varepsilon$, write $a_\varepsilon(\theta) = P_\theta(\rho(S(Y), s_{\mathrm{obs}}) \le \varepsilon)$ and let

$$\pi_\varepsilon(\theta) = \frac{\pi(\theta)\, a_\varepsilon(\theta)}{A_\varepsilon}, \qquad A_\varepsilon = \int \pi\, a_\varepsilon > 0,$$

be the $\varepsilon$-posterior. The tolerances are $\varepsilon_1 \ge \varepsilon_2 \ge \cdots \ge \varepsilon_T$. At generation $t \ge 2$ the previous population is a fixed set of particles $\theta_1, \ldots, \theta_N$ with weights $W_j > 0$, $\sum_j W_j = 1$, and $K_t(\cdot \mid \theta')$ is a transition density, for example the normal density with mean $\theta'$ and variance $s_t^2$. The mixture

$$g_t(\theta) = \sum_{j=1}^N W_j\, K_t(\theta \mid \theta_j)$$

is the density of a proposal on lines L6 and L7.

## Claim 1: generation 1

The particles of generation 1 are independent draws from $\pi_{\varepsilon_1}$, with equal weights.

*Proof.* Line L1 is the ABC rejection algorithm at tolerance $\varepsilon_1$; the law of its kept values is $\pi_{\varepsilon_1}$, with independence, by Claim 1 of the proof on the [ABC rejection algorithm](/abc-rejection-sampling/) page. $\blacksquare$

## Claim 2: the law of an accepted proposal

Given the previous population, the new particles $\theta_1^*, \ldots, \theta_N^*$ of generation $t$ are independent with density

$$q_t(\theta) = \frac{g_t(\theta)\, \mathbf{1}\{\pi(\theta) > 0\}\, a_{\varepsilon_t}(\theta)}{c_t}, \qquad c_t = \int g_t\, \mathbf{1}\{\pi > 0\}\, a_{\varepsilon_t},$$

provided $c_t > 0$.

*Proof.* One attempt on lines L6 to L8 draws $j$ with probability $W_j$ and then $\theta^* \sim K_t(\cdot \mid \theta_j)$, so $\theta^*$ has density $g_t$. It is kept with probability $\mathbf{1}\{\pi(\theta^*) > 0\}\, a_{\varepsilon_t}(\theta^*)$, using fresh simulations. As in rejection sampling, for a set $B$, $P(\theta^* \in B \text{ and kept}) = \int_B g_t \mathbf{1}\{\pi > 0\} a_{\varepsilon_t}$, so a kept value has density $q_t$. Attempts are independent given the previous population, so the kept values are independent and identically distributed. $\blacksquare$

## Claim 3: the weights correct the proposal exactly

Assume $g_t(\theta) > 0$ wherever $\pi(\theta)a_{\varepsilon_t}(\theta) > 0$ (true for a normal kernel). Let $w(\theta) = \pi(\theta)/g_t(\theta)$, the weight of line L9. Then for every function $h$ with $\int \pi_{\varepsilon_t}|h| < \infty$,

$$\frac{\mathbb{E}_{q_t}[w(\theta^*)h(\theta^*)]}{\mathbb{E}_{q_t}[w(\theta^*)]} = \mathbb{E}_{\pi_{\varepsilon_t}}[h].$$

This holds for every previous population: the particles $\theta_j$ and weights $W_j$ need not be correct.

*Proof.* Where $\pi(\theta) > 0$,

$$q_t(\theta)\, w(\theta) = \frac{g_t(\theta)\, a_{\varepsilon_t}(\theta)}{c_t} \cdot \frac{\pi(\theta)}{g_t(\theta)} = \frac{\pi(\theta)\, a_{\varepsilon_t}(\theta)}{c_t} = \frac{A_{\varepsilon_t}}{c_t}\, \pi_{\varepsilon_t}(\theta),$$

and where $\pi(\theta) = 0$ both sides are $0$. So $\mathbb{E}_{q_t}[wh] = (A_{\varepsilon_t}/c_t)\,\mathbb{E}_{\pi_{\varepsilon_t}}[h]$ and $\mathbb{E}_{q_t}[w] = A_{\varepsilon_t}/c_t$. Divide. $\blacksquare$

The unknown acceptance probability $a_{\varepsilon_t}$ appears in both the target and the proposal law and cancels, so the weight needs only $\pi$ and $g_t$. This is the weight of Beaumont, Cornuet, Marin and Robert (2009).

## Claim 4: consistency for a fixed previous population

Fix the previous population and draw $M$ new particles. With normalized weights $W_i^* = w(\theta_i^*)/\sum_k w(\theta_k^*)$ and a function $h$ with $\int \pi_{\varepsilon_t}|h| < \infty$, $\sum_i W_i^* h(\theta_i^*) \to \mathbb{E}_{\pi_{\varepsilon_t}}[h]$ almost surely as $M \to \infty$.

*Proof.* By Claim 2 the $\theta_i^*$ are independent with density $q_t$. $\mathbb{E}_{q_t}|wh| = (A_{\varepsilon_t}/c_t)\int\pi_{\varepsilon_t}|h| < \infty$ and $\mathbb{E}_{q_t}w = A_{\varepsilon_t}/c_t \in (0, \infty)$, so the strong [law of large numbers](/law-of-large-numbers/) applies to the numerator $\frac1M\sum_i w(\theta_i^*)h(\theta_i^*)$ and to the denominator $\frac1M\sum_i w(\theta_i^*)$. The ratio converges to the ratio of the limits, which is $\mathbb{E}_{\pi_{\varepsilon_t}}[h]$ by Claim 3. $\blacksquare$

## Claim 5: equal weights target the wrong law

If line L9 is replaced by $w \equiv 1$, the weighted population of generation $t$ targets $q_t$, not $\pi_{\varepsilon_t}$, and

$$\frac{q_t(\theta)}{\pi_{\varepsilon_t}(\theta)} = \frac{A_{\varepsilon_t}}{c_t}\cdot\frac{g_t(\theta)}{\pi(\theta)}.$$

*Proof.* The first statement is Claim 2 with all weights equal, and the ratio is the display in the proof of Claim 3. $\blacksquare$

Since $g_t$ is concentrated where the previous particles are, $q_t$ puts too much mass near the centre of the previous population and too little in the tails. With a uniform prior, $q_t$ is the product of $\pi_{\varepsilon_t}$ and a bump, which is narrower than $\pi_{\varepsilon_t}$.

## What is proved and what is measured

Claims 1 to 5 are exact. Claim 4 is a limit in the number of particles of one generation, with the previous population held fixed; the joint behaviour of all generations as $N$ grows, and the size of the error at a fixed $N$, are not proved here. The page measures them against the exact posterior of a binomial model. The tests check Claim 3 in rational arithmetic on $500$ random finite models.
