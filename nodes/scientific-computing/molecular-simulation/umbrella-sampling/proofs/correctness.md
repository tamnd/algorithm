---
title: Unbiasing of a window, the bin error, and the join of the windows
proves: [correctness]
status: full
---

Let $U(x)$ be a potential with $Z = \int e^{-\beta U}\,dx$ finite and positive, $s(x)$ a measurable collective variable, and $p(s)$ the density of $s(x)$ when $x$ has density $e^{-\beta U} / Z$; assume $p$ is continuous and positive on the interval of interest. Define $F(s) = -\beta^{-1} \ln p(s)$. Window $k$ samples the density proportional to $e^{-\beta (U(x) + w_k(s(x)))}$, where $w_k$ is continuous and $Z_k = \int e^{-\beta(U + w_k(s))}\,dx$ is finite.

**Claim 1 (unbiasing a window).** The density of $s$ in window $k$ is $p_k(s) = (Z / Z_k)\, p(s)\, e^{-\beta w_k(s)}$. Hence
$$F(s) = -\beta^{-1} \ln p_k(s) - w_k(s) + c_k, \qquad c_k = \beta^{-1} \ln(Z / Z_k),$$
with $c_k$ independent of $s$.

*Proof.* For a bounded measurable $g$, $E_k[g(s(x))] = Z_k^{-1} \int g(s(x))\, e^{-\beta w_k(s(x))} e^{-\beta U(x)}\,dx = (Z / Z_k)\, E[g(s(x))\, e^{-\beta w_k(s(x))}] = (Z / Z_k) \int g(s)\, e^{-\beta w_k(s)} p(s)\,ds$. So $p_k(s) = (Z/Z_k)\, p(s) e^{-\beta w_k(s)}$. Take $-\beta^{-1} \ln$ of both sides and rearrange. $\square$

The proof uses only that the bias depends on $x$ through $s(x)$. A bias on another variable would change the conditional distribution of $x$ given $s$, and the identity would fail.

**Claim 2 (one window, many samples).** Let bin $b$ be an interval $I_b$ with centre $m_b$ and half-width $h$, and define the bin free energy $F_b = -\beta^{-1} \ln \int_{I_b} p(s)\,ds$. Let $\delta_k(b) = \max_{s \in I_b} |w_k(s) - w_k(m_b)|$. If the samples of window $k$ come from an ergodic chain with stationary density $p_k$, then with probability 1, as $n \to \infty$,
$$-\beta^{-1} \ln \frac{n_k(b)}{n} - w_k(m_b) \to F_b - c_k + e_k(b), \qquad |e_k(b)| \le \delta_k(b).$$
For the harmonic bias $w_k(s) = \frac{\kappa}{2}(s - s_k)^2$, $\delta_k(b) \le \kappa h |m_b - s_k| + \frac{\kappa}{2} h^2$.

*Proof.* By the ergodic theorem $n_k(b) / n \to P_k(b) = \int_{I_b} p_k(s)\,ds$, which is positive, and $\ln$ is continuous on $(0, \infty)$. By Claim 1, $P_k(b) = (Z / Z_k) \int_{I_b} p(s) e^{-\beta w_k(s)}\,ds$, and on $I_b$ the factor $e^{-\beta w_k(s)}$ lies between $e^{-\beta (w_k(m_b) + \delta_k(b))}$ and $e^{-\beta (w_k(m_b) - \delta_k(b))}$. So
$$-\beta^{-1} \ln P_k(b) = -c_k + F_b + w_k(m_b) + e_k(b)$$
with $|e_k(b)| \le \delta_k(b)$. Subtract $w_k(m_b)$. For the harmonic bias, $w_k(s) - w_k(m_b) = \kappa (m_b - s_k)(s - m_b) + \frac{\kappa}{2}(s - m_b)^2$, and $|s - m_b| \le h$. $\square$

Taking $-\ln n_k(b)$ instead of $-\ln(n_k(b)/n)$, as line L4 does, only adds the constant $\beta^{-1} \ln n$ to every bin of the window, which is absorbed into the window constant. Thus each window profile converges to the bin free energy up to a constant, with an error that is small when the bins are narrow compared with $1 / (\beta \kappa |m_b - s_k|)$.

**Claim 3 (the join).** Let $G_k(b)$, for $b$ in a set $S_k$ of bins, be the window profiles of line L4, and suppose $G_k(b) = F_b + a_k + \epsilon_k(b)$ with constants $a_k$ and errors $|\epsilon_k(b)| \le \epsilon$. Suppose that for each $k \ge 2$ the set $S_k$ shares at least one bin with $S_1 \cup \dots \cup S_{k-1}$. Then lines L5 to L8 return a profile $\hat F$ with
$$\hat F(b) = F_b + a_1 - \min_{b'} \hat F'(b') + r(b), \qquad |r(b)| \le (2K - 1)\,\epsilon,$$
where $\hat F'$ is the profile before line L8, on every bin covered by some window. In particular, if all errors are 0, the output is $F_b - \min F$ exactly on the covered bins.

*Proof.* Induction on $k$. Let $\hat F_k$ be the profile after window $k$ is merged, and claim $\hat F_k(b) = F_b + a_1 + r_k(b)$ with $|r_k(b)| \le (2k - 1)\epsilon$. For $k = 1$, $\hat F_1 = G_1$ and $|r_1| \le \epsilon$. At step $k$ the shift is $c = \mathrm{mean}_{b \in S} (\hat F_{k-1}(b) - G_k(b)) = a_1 - a_k + \mathrm{mean}_{b \in S}(r_{k-1}(b) - \epsilon_k(b))$, where $S$ is the shared set, which is not empty by assumption. So $G_k(b) + c = F_b + a_1 + \rho(b)$ with $|\rho(b)| \le \epsilon + (2k - 3)\epsilon + \epsilon = (2k - 1)\epsilon$. Line L7 sets each bin either to this value or to a weighted mean of it and $\hat F_{k-1}(b)$, whose error is at most $(2k - 3)\epsilon$; a weighted mean with nonnegative weights has error at most the larger of the two. This gives the bound for $k$. Line L8 subtracts the same number from every bin. $\square$

The bound of Claim 3 is a worst case. Window errors of random sign add more like a random walk, so the error between the two ends of a chain of $K$ windows grows roughly like $\sqrt{K}\,\epsilon$, which matches the asymmetry error of the example on the page. WHAM avoids the order of joins by solving for all constants at once.

**Remark (the example).** In the example $s = x$, so $p(s) \propto e^{-\beta U(s)}$ and $F = U$ up to a constant. The bin free energy $F_b$ differs from $U(m_b)$ by at most the variation of $U$ over the bin, which is why the page compares with $U$ at the bin centres on bins where the variation is small.
