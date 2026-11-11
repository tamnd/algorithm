---
title: The phi accrual detector is monotone, accrues after a crash, stays bounded under bounded delays, and has mistake rate 10^(-Phi) under its model
proves: [correctness]
status: full
---

**Setting.** The monitor runs lines L1 to L7. Write $Q(x) = 1 - F(x)$ for the tail of the model distribution with the current window, so $\varphi(x) = -\log_{10} Q(x)$, where $x = t_{now} - T_{last}$. For the normal model, $F$ is the normal CDF with mean $\mu$ and standard deviation $\sigma > 0$ (a floor on $\sigma$ guarantees $\sigma > 0$).

**Claim.**

1. *Monotone.* Between two heartbeats, $\varphi$ is a nondecreasing function of $t_{now}$, and for the normal model $\varphi(\mu) = \log_{10} 2$.
2. *Accruement.* If the monitored process crashes, then after its last heartbeat arrives, $\varphi \to \infty$ as $t_{now} \to \infty$. So every threshold $\Phi$ is crossed in finite time, and stays crossed.
3. *Upper bound.* If every inter-arrival time is at most $B$, and the window values lie in $[b, B]$ with standard deviation at least $\sigma_0 > 0$, then $\varphi \le -\log_{10} Q_{\min}(B) < \infty$, where $Q_{\min}(B)$ is the smallest normal tail at $B$ over means in $[b, B]$ and standard deviations in $[\sigma_0, B - b + \sigma_0]$.
4. *Mistake rate.* If the inter-arrival times are independent with a continuous CDF $F$ that the detector uses, the probability that $\varphi$ reaches $\Phi$ in an interval of a live process before its next heartbeat is exactly $10^{-\Phi}$.

**Proof of 1.** Between heartbeats the window, and so $F$, does not change. $Q$ is nonincreasing because $F$ is a CDF, and $-\log_{10}$ is decreasing, so $\varphi$ is nondecreasing in $x$. For the normal model $F(\mu) = 1/2$, so $\varphi(\mu) = -\log_{10}(1/2) = \log_{10} 2$. $\square$

**Proof of 2.** After the last heartbeat the window is fixed, with $\sigma > 0$, and $x = t_{now} - T_{last} \to \infty$. For the normal model $Q(x) \to 0$, so $\varphi(x) \to \infty$; by claim 1 it never decreases again, so once $\varphi \ge \Phi$ it stays so. $\square$

**Proof of 3.** At any time $x \le B$, because the next heartbeat comes within $B$ of the previous one, and line L2 resets $T_{last}$. By claim 1, $\varphi(x) \le \varphi(B) = -\log_{10} Q(B)$ for the current window. The mean of values in $[b, B]$ lies in $[b, B]$, and their standard deviation is at most $B - b$, so with the floor it lies in $[\sigma_0, B - b + \sigma_0]$. The normal tail at $B$ is continuous and positive in the mean and the standard deviation, so on this compact set it has a positive minimum $Q_{\min}(B)$. $\square$

**Proof of 4.** Let $\tau_\Phi = \inf\{x : Q(x) \le 10^{-\Phi}\}$. By claim 1, $\varphi$ reaches $\Phi$ before the next heartbeat exactly when the inter-arrival time $X$ is at least $\tau_\Phi$. Since $F$ is continuous, $Q(\tau_\Phi) = 10^{-\Phi}$, and $P(X \ge \tau_\Phi) = Q(\tau_\Phi) = 10^{-\Phi}$. $\square$

**What is not proved.** Claim 4 assumes the detector knows the true distribution. With a mean and variance estimated from a window of $w$ values the rate is close to $10^{-\Phi}$ only when $w$ is large and the true distribution is normal; with a heavier tail it can be much higher. These cases are measured on the page.
