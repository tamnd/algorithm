---
title: The Milstein step is the truncated Ito-Taylor expansion, and local errors of mean order h^2 and mean-square order h^3 give strong order 1
proves: [correctness, termination, convergence]
status: full
---

**Setting.** Scalar Itô equation $dX = a(X)\,dt + b(X)\,dW$ on $[t_0, T]$ with a Brownian motion $W$ and its filtration $\mathcal{F}_t$ (time-dependent coefficients and diagonal noise work the same way, componentwise). Steps $h_n \le h \le 1$, $\Delta W_n = W(t_{n+1}) - W(t_n)$, which is independent of $\mathcal{F}_{t_n}$ with mean 0 and variance $h_n$. The Milstein map is

$$\Phi_n(x) = x + a(x)h_n + b(x)\Delta W_n + \tfrac12 b(x)b'(x)\bigl(\Delta W_n^2 - h_n\bigr).$$

**Lemma 1 (the loop).** After iteration $n$ of lines L3 to L9, $t = t_{n+1}$ and $X = \Phi_n(\cdots\Phi_0(x_0))$, with $t_k = t_0 + kh$ for $k < N$ and $t_N = T$; the increment used in step $n$ has variance $h_n = t_{n+1} - t_n$.

*Proof.* Induction on $n$. Line L4 sets the grid point and $h_n$, line L5 the increment ($\sqrt{h_n}$ times a standard normal, or the given value), lines L6 to L8 apply $\Phi_n$ to the current value, line L9 advances $t$. $\square$

**Termination.** The loop runs $N = \lceil (T - t_0)/h \rceil$ times, with three coefficient evaluations and $O(d)$ arithmetic each.

**Lemma 2 (the double integral).** $I_{(1,1)} := \int_{t_n}^{t_{n+1}}\bigl(W(s) - W(t_n)\bigr)\,dW(s) = \frac12\bigl(\Delta W_n^2 - h_n\bigr)$.

*Proof.* Let $V(s) = W(s) - W(t_n)$. Itô's formula for $V^2$ gives $d(V^2) = 2V\,dW + ds$, so $V(t_{n+1})^2 = 2\int_{t_n}^{t_{n+1}} V\,dW + h_n$. $\square$

**Where the correction comes from.** Write the exact solution over one step as $X(t_{n+1}) = X(t_n) + \int a(X)\,ds + \int b(X)\,dW$. Applying Itô's formula to $b(X(s))$ gives $b(X(s)) = b(X(t_n)) + \int_{t_n}^{s}b'b(X)\,dW + \int_{t_n}^s(\ldots)\,dr$, and inserting this,

$$X(t_{n+1}) = X(t_n) + a h_n + b\,\Delta W_n + bb'\,I_{(1,1)} + R_n,$$

with coefficients at $X(t_n)$ and a remainder $R_n$ made of multiple integrals that contain at least one $ds$ beyond the terms kept, or three $dW$. By Lemma 2 the first four terms are exactly $\Phi_n(X(t_n))$, so $R_n$ is the local error $\delta_n = X(t_{n+1}) - \Phi_n(X(t_n))$. Kloeden and Platen (Chapter 5 and Section 10.3) prove, for coefficients with the stated smoothness and growth, that $|\mathbb{E}[\delta_n \mid \mathcal{F}_{t_n}]| \le K(1 + |X(t_n)|)h^2$ and $\mathbb{E}[\delta_n^2 \mid \mathcal{F}_{t_n}] \le K(1 + |X(t_n)|^2)h^3$; since the moments $\mathbb{E}|X(t)|^2$ are bounded on $[t_0, T]$, this gives the hypothesis (H) of Theorem 4. This part is cited. For linear equations it is proved in Lemma 3.

For Euler-Maruyama the local error contains $bb'I_{(1,1)}$ itself, and $\mathbb{E}[I_{(1,1)}^2] = \frac14\mathbb{E}[(\Delta W^2 - h)^2] = \frac14(3h^2 - 2h^2 + h^2) = \frac12h^2$. So its mean-square local error is of order $h^2$ only, which gives strong order $\frac12$ in Theorem 4 (with $p_2 = 1$).

**Lemma 3 (local error for linear equations).** Let $a(x) = \mu x$, $b(x) = \sigma x$. Then $|\mathbb{E}[\delta_n \mid \mathcal{F}_{t_n}]| \le K|X(t_n)|h_n^2$ and $\mathbb{E}[\delta_n^2 \mid \mathcal{F}_{t_n}] \le K X(t_n)^2h_n^3$ for $h_n \le 1$, with $K$ depending on $\mu, \sigma$ only.

*Proof.* The solution is $X(t_{n+1}) = X(t_n)e^{Z}$ with $Z = c h + \sigma\Delta W$, $c = \mu - \frac12\sigma^2$, and $\Phi_n(x) = x\,m$ with $m = 1 + \mu h + \sigma\Delta W + \frac12\sigma^2(\Delta W^2 - h)$ (write $h = h_n$). So $\delta_n = X(t_n)(e^Z - m)$ with $X(t_n)$ independent of $\Delta W$. Mean: $\mathbb{E}e^Z = e^{ch + \sigma^2h/2} = e^{\mu h}$ and $\mathbb{E}m = 1 + \mu h$, so $|\mathbb{E}(e^Z - m)| = e^{\mu h} - 1 - \mu h \le \frac12\mu^2h^2e^{|\mu|}$. Mean square: $1 + Z + \frac12Z^2 - m = c\sigma h\Delta W + \frac12c^2h^2$, because the terms $ch + \frac12\sigma^2h - \mu h$ cancel. Hence

$$e^Z - m = c\sigma h\Delta W + \tfrac12c^2h^2 + \rho, \qquad |\rho| \le \tfrac16|Z|^3e^{|Z|}.$$

$\mathbb{E}(c\sigma h\Delta W)^2 = c^2\sigma^2h^3$, $(\frac12c^2h^2)^2 \le c^4h^3/4$, and $\mathbb{E}\rho^2 \le \frac1{36}(\mathbb{E}Z^{12})^{1/2}(\mathbb{E}e^{4|Z|})^{1/2} = O(h^3)$, since $\mathbb{E}Z^{12} = O(h^6)$ for $h \le 1$ and $\mathbb{E}e^{4|Z|}$ is bounded. Combine with $(u + v + w)^2 \le 3(u^2 + v^2 + w^2)$. $\square$

**Theorem 4 (Milstein's fundamental theorem, the case used here).** Suppose $a$, $b$ and $bb'$ are Lipschitz with constant $L$, and the local errors satisfy, for some $K$,

$$\text{(H)} \qquad \bigl(\mathbb{E}\,|\mathbb{E}[\delta_n \mid \mathcal{F}_{t_n}]|^2\bigr)^{1/2} \le Kh^2, \qquad \mathbb{E}\,\delta_n^2 \le Kh^3.$$

Then $\bigl(\mathbb{E}\,|X(t_n) - X_n|^2\bigr)^{1/2} \le C h$ for all $n \le N$, with $C$ depending on $K$, $L$ and $T - t_0$ only.

*Proof.* Let $e_n = X(t_n) - X_n$, $E_n = \mathbb{E}e_n^2$, $E_0 = 0$. Then $e_{n+1} = e_n + u_n + \delta_n$ with

$$u_n = \Phi_n(X(t_n)) - \Phi_n(X_n) - e_n = \Delta a\,h_n + \Delta b\,\Delta W_n + \tfrac12\Delta(bb')(\Delta W_n^2 - h_n),$$

where $\Delta a = a(X(t_n)) - a(X_n)$, and so on, are $\mathcal{F}_{t_n}$-measurable with $|\Delta a|, |\Delta b|, |\Delta(bb')| \le L|e_n|$. Since $\Delta W_n$ is independent of $\mathcal{F}_{t_n}$ and $\mathbb{E}\Delta W_n = \mathbb{E}(\Delta W_n^2 - h_n) = 0$,

$$\mathbb{E}[u_n \mid \mathcal{F}_{t_n}] = \Delta a\,h_n, \qquad \mathbb{E}[u_n^2 \mid \mathcal{F}_{t_n}] \le 3L^2e_n^2\bigl(h_n^2 + h_n + \tfrac12h_n^2\bigr) \le 8L^2h\,e_n^2.$$

Expanding $e_{n+1}^2$ and conditioning on $\mathcal{F}_{t_n}$ in the cross terms:

- $2\mathbb{E}[e_nu_n] = 2\mathbb{E}[e_n\Delta a]h_n \le 2Lh\,E_n$;
- $2\mathbb{E}[e_n\delta_n] = 2\mathbb{E}[e_n\mathbb{E}(\delta_n \mid \mathcal{F}_{t_n})] \le 2E_n^{1/2}Kh^2 \le hE_n + K^2h^3$;
- $\mathbb{E}(u_n + \delta_n)^2 \le 2\mathbb{E}u_n^2 + 2\mathbb{E}\delta_n^2 \le 16L^2hE_n + 2Kh^3$.

So $E_{n+1} \le (1 + \gamma h)E_n + \beta h^3$ with $\gamma = 2L + 1 + 16L^2$ and $\beta = K^2 + 2K$. By induction (the discrete [Gronwall inequality](/gronwall-inequality/)), $E_n \le \beta h^3\,n\,e^{\gamma nh} \le \beta(T - t_0 + h)e^{\gamma(T - t_0 + h)}h^2$, using $nh \le T - t_0 + h$. Taking square roots gives the claim. $\blacksquare$

**Consequences.** For the linear equations of the examples, Lemma 3 gives (H), since $\mathbb{E}X(t)^2$ is bounded on $[t_0, T]$; so the strong order 1 of the experiments is proved there, and the measured slopes near 1 are consistent with it. For general coefficients (H) is cited from Kloeden and Platen. By Jensen's inequality $\mathbb{E}|X(T) - X_N| \le (\mathbb{E}|X(T) - X_N|^2)^{1/2}$, so the mean absolute error measured on the page is also $O(h)$. The weak order 1 is cited (Kloeden and Platen, Chapter 14); it follows from the fact that $\mathbb{E}\delta_n = O(h^2)$ together with smoothness of the test functions.
