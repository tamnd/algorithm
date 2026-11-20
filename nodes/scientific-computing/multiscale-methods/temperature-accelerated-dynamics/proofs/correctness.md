---
title: Why the extrapolated times give the low temperature event, and the error of the stop time
proves: [correctness]
status: full
---

The claim of TAD is a claim under harmonic transition state theory (HTST). We state the model, prove that the extrapolation is exact in the model, and bound the error of the stop rule.

**Model.** The basin has events $1, \ldots, M$. Under HTST, event $i$ has the rate $k_i(T) = \nu_i e^{-E_i / k_B T}$ at temperature $T$, with a prefactor $\nu_i$ and a barrier $E_i$ that do not depend on $T$. At the high temperature, the system is put back into the basin after each escape, so the occurrences of event $i$ form a Poisson process of rate $k_i^h = k_i(T_{\mathrm{high}})$, independent of the other events. Let $T_i^h$ be the first occurrence of event $i$; then $T_1^h, \ldots, T_M^h$ are independent and exponential with the rates $k_i^h$. Write $k_i^l = k_i(T_{\mathrm{low}})$, $\beta_l = 1 / k_B T_{\mathrm{low}}$, $\beta_h = 1 / k_B T_{\mathrm{high}}$, and $r = T_{\mathrm{high}} / T_{\mathrm{low}} > 1$.

**Lemma 1 (the extrapolation).** The extrapolated times $T_i^l = T_i^h e^{E_i (\beta_l - \beta_h)}$ of line L5 are independent and exponential with the rates $k_i^l$.

*Proof.* Under HTST, $e^{E_i (\beta_l - \beta_h)} = k_i^h / k_i^l$, because the prefactor cancels. If $T$ is exponential with rate $k$, then $a T$ is exponential with rate $k / a$. So $T_i^l$ is exponential with rate $k_i^h / (k_i^h / k_i^l) = k_i^l$. Independence carries over from the $T_i^h$. $\square$

**Theorem 1 (exact without a stop).** If the high temperature run continues until every event has occurred once, the event with the shortest $T_i^l$ and the time $\min_i T_i^l$ have the law of the first event at the low temperature: the time is exponential with rate $\sum_i k_i^l$, and the event is $i$ with probability $k_i^l / \sum_j k_j^l$.

*Proof.* By Lemma 1, the $T_i^l$ are independent exponential clocks with the low temperature rates. The first of independent exponential clocks has these two laws; this is the race of the [kinetic Monte Carlo](/kinetic-monte-carlo/) method. $\blacksquare$

**Theorem 2 (the stop rule).** Suppose that $\nu_i \ge \nu_{\min}$ for every event. Let $L = \ln(1/\delta)$, and let the run stop at $t_{\mathrm{stop}} = (L / \nu_{\min}) (\nu_{\min} t_{\mathrm{short}} / L)^{1/r}$, where $t_{\mathrm{short}}$ is the shortest extrapolated time of the events seen so far (line L7). Then for each event $i$, the probability that $i$ is not seen before the stop and would have had a shorter extrapolated time than the accepted event is less than $\delta$. So the result differs from the exact result of Theorem 1 with probability less than $M \delta$.

*Proof.* Fix $i$ and condition on the first occurrences of all other events. The value $t_{\mathrm{short}}$ at the stop, and so $t_{\mathrm{stop}}$, depend only on the events seen, so if $i$ is not seen they are fixed numbers, independent of $T_i^h$. Event $i$ causes an error only if $T_i^h > t_{\mathrm{stop}}$ and $T_i^l < t_{\mathrm{short}}$.

First, a bound on the low temperature rate. From $k_i^l = \nu_i e^{-\beta_l E_i}$ and $k_i^h = \nu_i e^{-\beta_h E_i}$ we get $k_i^l = \nu_i^{1 - r} (k_i^h)^r$. Since $1 - r < 0$ and $\nu_i \ge \nu_{\min}$, $k_i^l \le \nu_{\min}^{1-r} (k_i^h)^r$. With $x = k_i^h t_{\mathrm{stop}}$ and the definition of $t_{\mathrm{stop}}$, which gives $\nu_{\min} t_{\mathrm{short}} / L = (\nu_{\min} t_{\mathrm{stop}} / L)^r$:
$$k_i^l t_{\mathrm{short}} \le \nu_{\min} t_{\mathrm{short}} \left(\frac{k_i^h}{\nu_{\min}}\right)^r = L \left(\frac{\nu_{\min} t_{\mathrm{stop}}}{L}\right)^r \left(\frac{k_i^h}{\nu_{\min}}\right)^r = L \left(\frac{x}{L}\right)^r.$$

Now the probability. $T_i^l < t_{\mathrm{short}}$ means $T_i^h < t_{\mathrm{short}}\, k_i^l / k_i^h$. So the error has the probability
$$P\left(t_{\mathrm{stop}} < T_i^h < t_{\mathrm{short}} \frac{k_i^l}{k_i^h}\right) = \max\left(0,\ e^{-x} - e^{-k_i^l t_{\mathrm{short}}}\right) \le \max\left(0,\ e^{-x} - e^{-L (x/L)^r}\right).$$
The right side is positive only if $L (x/L)^r > x$, that is, $x > L$, because $r > 1$. Then it is less than $e^{-x} < e^{-L} = \delta$. The bound holds for every value of the other events, so it holds without the condition. A union bound over the $M$ events gives the last claim. $\blacksquare$

**What the theorems need.** Both theorems use HTST at both temperatures: the same prefactor and barrier at $T_{\mathrm{low}}$ and $T_{\mathrm{high}}$, and independent exponential escapes. Anharmonic effects change the prefactor with temperature, and at a high temperature new events (with high barriers and large prefactors) can become important; then the extrapolation is wrong by the ratio of the true rates to the HTST rates. Theorem 2 also needs $\nu_{\min}$ to be a true lower bound on the prefactors. The test with $\nu_{\min} = 100$, above every prefactor, shows the failure: the slow event with the lowest barrier is missed.

**What is not proved.** The boost $t_{\mathrm{short}} / t_{\mathrm{stop}}$ is not part of the theorems. It is a measurement of each run.

The derivation of $t_{\mathrm{stop}}$ here is ours. We did not compare it line by line with the equation in the paper of Sorensen and Voter.
