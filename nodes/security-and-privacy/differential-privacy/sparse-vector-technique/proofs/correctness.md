---
title: AboveThreshold is epsilon-DP and (alpha, beta)-accurate
proves: [correctness]
status: full
---

We use the pseudocode of the page. The queries $f_1, f_2, \ldots$ have sensitivity at most $\Delta$ for the neighbor relation in use: $|f_i(x) - f_i(x')| \le \Delta$ for all neighbors $x \sim x'$. The threshold noise has scale $b_1 = 2\Delta/\varepsilon$ and the query noise has scale $b_2 = 4\Delta/\varepsilon$. We write $p_1$ for the density of $\hat T$ (Laplace with center $T$ and scale $b_1$) and $p_2$ for the density of $\mathrm{Lap}(b_2)$. For a Laplace density $p$ with scale $b$ and any shift $s$, $p(z - s) \le e^{|s|/b} p(z)$, by the triangle inequality $|z| \le |z - s| + |s|$.

**Claim 1 (privacy).** For any neighbors $x \sim x'$ and any output sequence $a$, $P[\mathcal{A}(x) = a] \le e^{\varepsilon} P[\mathcal{A}(x') = a]$, also when each query is chosen as a function of the earlier outputs.

*Proof.* The output has one of two forms: $a = (\bot^{k-1}, \top)$ for some $k \ge 1$, or $a = (\bot^m)$ when the stream ends after $m$ queries with no top. The set of outputs is countable, so a bound for each single output gives the bound for each set of outputs.

*Adaptivity.* The query $f_i$ may depend on $a_1, \ldots, a_{i-1}$. On the event $\mathcal{A}(\cdot) = (\bot^{k-1}, \top)$, these earlier outputs are all $\bot$. So the queries $f_1, \ldots, f_k$ that are asked on this event are the same functions for $x$ and for $x'$. We fix them.

*Case $a = (\bot^{k-1}, \top)$.* Fix the values $\nu_1, \ldots, \nu_{k-1}$. They have the same distribution in both runs and are independent of $\hat T$ and $\nu_k$. Let $g(x) = \max_{i<k} (f_i(x) + \nu_i)$, with $g = -\infty$ when $k = 1$. The output is $a$ exactly when $(\hat T, \nu_k)$ lies in

$$A(x) = \{(t, v) : t > g(x) \text{ and } f_k(x) + v \ge t\}.$$

Each $f_i$ moves by at most $\Delta$, so the maximum $g$ moves by at most $\Delta$: $|g(x') - g(x)| \le \Delta$. Let $s_1 = g(x') - g(x)$ and $s_2 = s_1 + f_k(x) - f_k(x')$. Then $|s_1| \le \Delta$ and $|s_2| \le 2\Delta$. Define the translation $\varphi(t, v) = (t + s_1, v + s_2)$. If $(t, v) \in A(x)$, then $t + s_1 > g(x) + s_1 = g(x')$, and

$$f_k(x') + v + s_2 = f_k(x) + v + s_1 \ge t + s_1.$$

So $\varphi(A(x)) \subseteq A(x')$. A translation has Jacobian 1, so

$$P[(\hat T, \nu_k) \in A(x)] = \int_{\varphi(A(x))} p_1(t' - s_1)\, p_2(v' - s_2)\, dt'\, dv' \le e^{|s_1|/b_1} e^{|s_2|/b_2} \int_{A(x')} p_1(t')\, p_2(v')\, dt'\, dv'.$$

Here $|s_1|/b_1 \le \Delta \varepsilon/(2\Delta) = \varepsilon/2$ and $|s_2|/b_2 \le 2\Delta \varepsilon/(4\Delta) = \varepsilon/2$. So the probability of $a$ on $x$, for the fixed $\nu_1, \ldots, \nu_{k-1}$, is at most $e^{\varepsilon}$ times the probability on $x'$ for the same values. Take the expectation over $\nu_1, \ldots, \nu_{k-1}$ on both sides.

*Case $a = (\bot^m)$.* With $g(x) = \max_{i \le m} (f_i(x) + \nu_i)$ for fixed $\nu_1, \ldots, \nu_m$, the output is $a$ exactly when $\hat T > g(x)$. The shift $t \mapsto t + s_1$ maps this event on $x$ into the event on $x'$, and the density changes by at most $e^{\varepsilon/2}$. So the bound holds with $e^{\varepsilon/2} \le e^{\varepsilon}$.

Ties $f_k(x) + \nu_k = \hat T$ have probability 0, so the choice of $\ge$ in line L4 does not matter. $\square$

**Claim 2 (accuracy).** Let $k \ge 1$, $0 < \beta < 1$ and $\alpha = 8\Delta(\ln k + \ln(2/\beta))/\varepsilon$. With probability at least $1 - \beta$, over the first $k$ queries, every $\top$ is for a query with $f_i(x) \ge T - \alpha$ and every $\bot$ is for a query with $f_i(x) < T + \alpha$.

*Proof.* Let $E$ be the event that $|\hat T - T| \le \alpha/2$ and $|\nu_i| \le \alpha/2$ for all $i \le k$. By $P(|Z| > t) = e^{-t/b}$ for $Z \sim \mathrm{Lap}(b)$,

$$P(|\hat T - T| > \alpha/2) = e^{-\alpha \varepsilon/(4\Delta)}, \qquad P(|\nu_i| > \alpha/2) = e^{-\alpha\varepsilon/(8\Delta)} = \frac{\beta}{2k}.$$

By the union bound, $P(\bar E) \le (\beta/(2k))^2 + k \cdot \beta/(2k) \le \beta/2 + \beta/2 = \beta$. On $E$, a $\top$ at query $i$ means $f_i(x) \ge \hat T - \nu_i \ge T - \alpha/2 - \alpha/2 = T - \alpha$, and a $\bot$ means $f_i(x) < \hat T - \nu_i \le T + \alpha$. $\square$

Dwork and Roth state Claim 2 as Theorem 3.24, with the extra condition that no query before the $k$-th has $f_i(x) \ge T - \alpha$. On $E$ that condition makes the run reach query $k$, so the output has length $k$.

**Claim 3 (Sparse).** Sparse with cutoff $c$ and $\delta = 0$ is $\varepsilon$-DP.

*Proof.* With $\sigma = 2c\Delta/\varepsilon$, each segment between two tops is a run of AboveThreshold with $\varepsilon/c$ in place of $\varepsilon$: the threshold noise is $\mathrm{Lap}(2\Delta/(\varepsilon/c))$ and the query noise is $\mathrm{Lap}(4\Delta/(\varepsilon/c))$. Each run is $(\varepsilon/c)$-DP by Claim 1, and its queries may depend on the outputs of the earlier runs. There are at most $c$ runs, so adaptive basic composition gives $\varepsilon$-DP. $\square$

**Cost.** Each query asked costs one evaluation of $f_i$, one Laplace draw (line L3) and one comparison (line L4). With one more draw in line L1, $k$ queries cost $O(k)$ draws and comparisons in the real-RAM model. The run stores only $\hat T$ and the current noise, so the extra space is $O(1)$.
