---
title: CROSS computes the crossing probability, and bisection finds the unique O'Brien-Fleming constant
proves: [correctness]
status: full
---

Notation is that of the page. Under $H_0$, $S_0 = 0$ and the increments $S_k - S_{k-1}$, $k = 1, \ldots, K$, are independent with distribution $N(0, \Delta_k)$, where $\Delta_k = I_k - I_{k-1} > 0$ and $I_0 = 0$. For $C > 0$ let $b = C\sqrt{I_K}$. The O'Brien-Fleming test with constant $C$ rejects at the first $k$ with $|S_k| \ge b$, which is the same as $|Z_k| \ge C\sqrt{I_K/I_k}$ since $Z_k = S_k/\sqrt{I_k}$. Let
$$Q(C) = P_0\bigl(|S_k| \ge b \text{ for some } k \le K\bigr).$$
We prove that CROSS$(C)$ equals $Q(C)$ when the integrals are exact, and that lines L1 to L5 converge to the unique solution of $Q(C) = \alpha$. Write $\varphi_v$ for the $N(0, v)$ density and $E_k = \{|S_j| < b \text{ for all } j \le k\}$, with $E_0$ the sure event.

**Lemma 1 (the sub-densities).** For $k = 1, \ldots, K$ and every Borel set $A \subseteq (-b, b)$,
$$P_0(E_{k-1} \cap \{S_k \in A\}) = \int_A h_k(s)\,ds,$$
where $h_1 = \varphi_{I_1}$ and, for $k \ge 2$, $h_k(s) = \int_{-b}^{b} h_{k-1}(u)\mathbf 1\{|u| < b\}\varphi_{\Delta_k}(s - u)\,du$. The same formula holds for every Borel $A \subseteq \mathbb R$.

*Proof.* By induction on $k$. For $k = 1$, $E_0$ is sure and $S_1 \sim N(0, I_1) = N(0, \Delta_1)$. For $k \ge 2$, $E_{k-1} = E_{k-2} \cap \{|S_{k-1}| < b\}$, and the increment $D = S_k - S_{k-1}$ is independent of $(S_1, \ldots, S_{k-1})$. By the induction hypothesis the restriction of the law of $S_{k-1}$ to $E_{k-2}$ has density $h_{k-1}$. Conditioning on $S_{k-1}$ and using the independence of $D$,
$$P_0(E_{k-1} \cap \{S_k \in A\}) = \int_{-b}^{b} h_{k-1}(u)\,P(u + D \in A)\,du = \int_{-b}^{b} h_{k-1}(u)\int_A \varphi_{\Delta_k}(s - u)\,ds\,du.$$
Tonelli's theorem exchanges the integrals, which gives $\int_A h_k(s)\,ds$. $\square$

**Lemma 2 (CROSS is the crossing probability).** If the integrals of lines L10 and L11 are evaluated exactly, then after the iteration of line L8 for $k$, $p = P_0(E_k^c)$ and $g = h_{k+1}$ restricted to $(-b, b)$. In particular line L12 returns $Q(C) = P_0(E_K^c)$.

*Proof.* The first crossing happens at exactly one $k$, so $P_0(E_k^c) = \sum_{j \le k} P_0(E_{j-1} \cap \{|S_j| \ge b\})$. Line L7 sets $p = P_0(|S_1| \ge b) = 2\bar\Phi(b/\sqrt{I_1})$ and $g = h_1$ on $[-b, b]$. At step $k \ge 2$, Lemma 1 with $A = \{|s| \ge b\}$ gives
$$P_0(E_{k-1} \cap \{|S_k| \ge b\}) = \int_{-b}^{b} g(u)\,P(|u + D| \ge b)\,du = \int_{-b}^{b} g(u)\left[\Phi\left(\frac{-b - u}{\sigma}\right) + \bar\Phi\left(\frac{b - u}{\sigma}\right)\right]du,$$
with $\sigma = \sqrt{\Delta_k}$, which is the term that line L10 adds. Line L11 computes $h_{k+1}$ from $g = h_k$ by the formula of Lemma 1. Induction on $k$ completes the proof. $\square$

**Lemma 3 (monotone and continuous).** $Q$ is continuous and strictly decreasing on $(0, \infty)$.

*Proof.* Let $0 < C < C'$, with $b = C\sqrt{I_K}$ and $b' = C'\sqrt{I_K}$. Every path with some $|S_k| \ge b'$ has $|S_k| \ge b$, so $Q(C') \le Q(C)$. The difference $Q(C) - Q(C')$ is at least the probability of the event $\{|S_j| < b \text{ for } j < K\} \cap \{b \le |S_K| < b'\}$. By Lemma 1 with the bound $b$, this probability is $\int_{b \le |s| < b'} h_K(s)\,ds$, and $h_K > 0$ everywhere because it is a convolution of a positive function on $(-b, b)$ with a normal density (for $K = 1$, $h_1$ is a normal density). So the difference is positive. For continuity, the events $\{\max_k |S_k| \ge C\sqrt{I_K}\}$ change with $C$ only through the event $\{\max_k |S_k| = C\sqrt{I_K}\}$, which has probability at most $\sum_k P(|S_k| = C\sqrt{I_K}) = 0$. By continuity of probability along monotone sequences of events, $Q$ is continuous from both sides. $\square$

**Lemma 4 (the bracket).** With $lo = z_{1-\alpha/2}$ and $hi = z_{1-\alpha/(2K)}$, $Q(lo) \ge \alpha \ge Q(hi)$.

*Proof.* The event of crossing contains $\{|S_K| \ge lo\sqrt{I_K}\} = \{|Z_K| \ge z_{1-\alpha/2}\}$, which has probability $\alpha$. For $hi$, the critical values $hi\sqrt{I_K/I_k}$ are all at least $hi$, so by the union bound $Q(hi) \le \sum_{k=1}^K P_0(|Z_k| \ge hi) = K \cdot \alpha/K = \alpha$. $\square$

**Theorem.** If CROSS is evaluated exactly, there is exactly one $C^* \in [lo, hi]$ with $Q(C^*) = \alpha$, and after every iteration of lines L2 to L4 it holds that $lo \le C^* \le hi$. The loop stops after $\lceil\log_2((hi - lo)/\mathrm{tol})\rceil$ iterations, and line L5 returns a value within $\mathrm{tol}$ of $C^*$, together with the boundary $c_k = C\sqrt{I_K/I_k}$.

*Proof.* Existence follows from Lemmas 3 and 4 and the intermediate value theorem; uniqueness from strict monotonicity. Line L1 establishes $lo \le C^* \le hi$ by Lemma 4. At line L4, if $Q(C) > \alpha = Q(C^*)$ then $C < C^*$ by Lemma 3, so setting $lo = C$ keeps $C^*$ in the interval; otherwise $Q(C) \le Q(C^*)$ and $C \ge C^*$, so setting $hi = C$ keeps it. Each iteration halves $hi - lo$. Line L5 returns a point of the final interval, of width at most tol, which contains $C^*$. By Lemma 2, CROSS$(C) = Q(C)$. $\blacksquare$

**Quadrature.** In the implementation the integrals of lines L10 and L11 are computed by Simpson's rule on $[-b, b]$. The integrands are smooth on this closed interval, so each step has error $O(h^4)$ in the grid spacing $h$; the computed CROSS is then a close approximation of $Q$, and the bisection finds the root of the approximation.
