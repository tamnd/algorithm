---
title: MWEM is epsilon-DP, and its average has error 2n sqrt(ln N / T) + 10 T ln|Q| / epsilon
proves: [correctness]
status: full
---

We use the pseudocode of the page. The domain $D$ has $N$ elements. The data is a histogram $B$ over $D$ with $n = \sum_x B(x) \ge 1$ records, and $n$ is public. A query is a vector $q \in \{0,1\}^D$, with $q(H) = \sum_x q(x) H(x)$ for any histogram $H$. Two datasets are neighbors if one record is replaced by another, so $n$ is the same and $|q(B) - q(B')| \le 1$ for every query. The proof also works for $q \in [-1, 1]^D$, as in Hardt, Ligett and McSherry, with sensitivity 2 in place of 1 under replace.

**Claim 1 (privacy).** The run, and so the output, is $\varepsilon$-DP.

*Proof.* Let $\varepsilon_0 = \varepsilon/(2T)$. Round $i$ makes two releases: the index of $q_i$ (line L3) and the value $m_i$ (line L4). The histogram $A_{i-1}$ is a fixed function of the earlier releases $q_1, m_1, \ldots, q_{i-1}, m_{i-1}$ and of the public $n$, not of $B$.

*Line L3.* Given $A_{i-1}$, the score $s(B, q) = |q(A_{i-1}) - q(B)|$ moves by at most 1 between neighbors, by the triangle inequality. The selection has $P(q) = e^{\varepsilon_0 s(B,q)/2} / Z(B)$ with $Z(B) = \sum_{r \in Q} e^{\varepsilon_0 s(B,r)/2}$. For neighbors, $e^{\varepsilon_0 s(B,q)/2} \le e^{\varepsilon_0/2} e^{\varepsilon_0 s(B',q)/2}$ and $Z(B') \le e^{\varepsilon_0/2} Z(B)$, so $P_B(q) \le e^{\varepsilon_0} P_{B'}(q)$.

*Line L4.* Given $q_i$, the value $q_i(B) + \mathrm{Lap}(1/\varepsilon_0)$ is the Laplace mechanism for a function of sensitivity 1, so it is $\varepsilon_0$-DP.

The $2T$ releases are each $\varepsilon_0$-DP given the earlier ones. By adaptive basic composition the sequence of all releases is $2T\varepsilon_0 = \varepsilon$-DP. The output of line L6 is a function of the releases and $n$, so it is $\varepsilon$-DP by post-processing. $\square$

**Lemma (one update).** Let $a = A/n$ and $b = B/n$ be the normalized histograms, $\Psi(A) = \sum_x b(x) \ln(b(x)/a(x))$ the relative entropy, $u = q(A)$, $v = q(B)$, and $A'$ the update of line L5 with the measurement $m$. If $|m - u| \le 2n$, then

$$\Psi(A) - \Psi(A') \ge \frac{(u - v)^2 - (m - v)^2}{4n^2}.$$

*Proof.* Let $\eta = (m - u)/(2n)$, so $|\eta| \le 1$, and $Z = \sum_x a(x) e^{\eta q(x)}$. Line L5 sets $a'(x) = a(x) e^{\eta q(x)}/Z$. Then

$$\Psi(A) - \Psi(A') = \sum_x b(x) \ln\frac{a'(x)}{a(x)} = \eta \sum_x b(x) q(x) - \ln Z = \frac{\eta v}{n} - \ln Z.$$

For $|y| \le 1$, $e^y \le 1 + y + y^2$. With $y = \eta q(x)$ and $q(x)^2 \le 1$, $Z \le 1 + \eta u/n + \eta^2$, and $\ln Z \le \eta u/n + \eta^2$ because $\ln(1+w) \le w$. So the drop is at least $\eta(v - u)/n - \eta^2$. Put $m - u = (v - u) + \nu$ with $\nu = m - v$:

$$\frac{(m-u)(v-u)}{2n^2} - \frac{(m-u)^2}{4n^2} = \frac{2(v-u)^2 + 2\nu(v-u) - (v-u)^2 - 2\nu(v-u) - \nu^2}{4n^2} = \frac{(v-u)^2 - \nu^2}{4n^2}. \qquad \square$$

**Claim 2 (accuracy).** Let $\bar A = \frac{1}{T}\sum_{i=0}^{T-1} A_i$ be the output of line L6, $\beta \in (0,1)$, and

$$\gamma = \frac{4T}{\varepsilon} \ln\frac{2T|Q|}{\beta}, \qquad \lambda = \frac{2T}{\varepsilon} \ln\frac{2T}{\beta}.$$

If $\lambda \le n$, then with probability at least $1 - \beta$,

$$\max_{q \in Q} |q(\bar A) - q(B)| \le 2n\sqrt{\frac{\ln N}{T}} + \lambda + \gamma.$$

*Proof.* Write $u_i = q_i(A_{i-1})$, $v_i = q_i(B)$, $\nu_i = m_i - v_i$, and $\mathrm{err}(H) = \max_q |q(H) - q(B)|$.

*Good event.* (a) For a Laplace draw, $P(|\nu_i| > \lambda) = e^{-\lambda\varepsilon/(2T)} = \beta/(2T)$. (b) For the exponential mechanism with $\varepsilon_0$ and scores of sensitivity 1, the chosen score is below $\max_q s(B,q) - (2/\varepsilon_0)\ln(|Q|/p)$ with probability at most $p$: each such $q$ has probability at most $e^{-\ln(|Q|/p)}$ times that of the best one, and there are at most $|Q|$ of them. With $p = \beta/(2T)$ and $2/\varepsilon_0 = 4T/\varepsilon$, this is the event $|u_i - v_i| < \mathrm{err}(A_{i-1}) - \gamma$. By the union bound over the $2T$ events, with probability at least $1 - \beta$, for all $i$: $|\nu_i| \le \lambda$ and $|u_i - v_i| \ge \mathrm{err}(A_{i-1}) - \gamma$.

*Potential.* On this event $|m_i - u_i| \le |v_i - u_i| + |\nu_i| \le n + n$, so the lemma applies in every round. $\Psi(A_0) = \ln N - H(b) \le \ln N$ and $\Psi(A_T) \ge 0$. Summing the lemma over the $T$ rounds,

$$\sum_{i=1}^{T} \big((u_i - v_i)^2 - \nu_i^2\big) \le 4n^2 \ln N, \quad\text{so}\quad \frac{1}{T}\sum_{i=1}^{T} (u_i - v_i)^2 \le \frac{4n^2 \ln N}{T} + \lambda^2.$$

*Average.* $q(\bar A) - q(B)$ is the mean of $q(A_{i-1}) - q(B)$ over $i$, so $\mathrm{err}(\bar A) \le \frac{1}{T}\sum_i \mathrm{err}(A_{i-1}) \le \frac{1}{T}\sum_i |u_i - v_i| + \gamma$. By the Cauchy-Schwarz inequality and $\sqrt{s + t} \le \sqrt{s} + \sqrt{t}$,

$$\frac{1}{T}\sum_i |u_i - v_i| \le \sqrt{\frac{1}{T}\sum_i (u_i - v_i)^2} \le 2n\sqrt{\frac{\ln N}{T}} + \lambda. \qquad \square$$

With $\beta = 2T/|Q|$ (which needs $|Q| > 2T$), $\gamma = (8T/\varepsilon)\ln|Q|$ and $\lambda = (2T/\varepsilon)\ln|Q|$, so the bound is $2n\sqrt{\ln N/T} + 10T\ln|Q|/\varepsilon$ with probability at least $1 - 2T/|Q|$. This is Theorem 2.2 of Hardt, Ligett and McSherry. Our condition $\lambda \le n$ is mild: if it fails, the bound exceeds $n$ and holds anyway for counting queries with values in $[0, n]$.

**Cost.** Line L1 costs $O(N)$. Each round evaluates all $|Q|$ queries on $A_{i-1}$ in $O(|Q|N)$, samples in $O(|Q|)$, and updates in $O(N)$. The true answers $q(B)$ are computed one time in $O(|Q|N)$. So $T$ rounds cost $O(T|Q|N)$, and the extra space is $O(N + |Q|)$.
