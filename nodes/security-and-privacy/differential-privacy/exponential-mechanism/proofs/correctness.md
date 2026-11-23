---
title: The exponential mechanism samples the right distribution, is epsilon-DP, and has high utility
proves: [correctness]
status: full
---

We work in the real RAM. Fix a neighbor relation $\sim$, a finite list $R = (r_1, \ldots, r_m)$ of candidates with $m \ge 1$, a utility $u$, a number $\Delta \ge \Delta u = \max_{r} \max_{x \sim x'} |u(x, r) - u(x', r)|$ with $\Delta > 0$, and $\varepsilon > 0$. Let $c$ be the value of line L1. For a dataset $x$ write

$$s_x(r) = \frac{\varepsilon u(x, r)}{c\Delta}, \qquad Z_x = \sum_{r \in R} e^{s_x(r)}, \qquad P_x(r) = \frac{e^{s_x(r)}}{Z_x}.$$

**Lemma 1 (the sampler).** In exact arithmetic, EXPONENTIAL-MECHANISM returns $r_j$ with probability $P_x(r_j)$, and line L10 is reached with probability 0.

*Proof.* Lines L2 to L4 give $w_r = e^{s_x(r) - M} = e^{s_x(r)}/e^M$, and line L5 gives $W = Z_x / e^M$. So $w_r / W = P_x(r)$; the shift by $M$ does not change the ratios. Every $w_r > 0$, and $w_r \le 1$ with equality for a candidate with the largest score, so no weight overflows. Let $C_j = w_{r_1} + \cdots + w_{r_j}$, with $C_0 = 0$ and $C_m = W$. After the $j$-th pass of line L8, $t = UW - C_j$. So the loop returns $r_j$ at the first $j$ with $UW < C_j$, which is the $j$ with $C_{j-1} \le UW < C_j$. Since $U$ is uniform on $[0, 1)$, $UW$ is uniform on $[0, W)$, and this event has probability $(C_j - C_{j-1})/W = w_{r_j}/W = P_x(r_j)$. Since $UW < W = C_m$, some $j \le m$ returns, and line L10 is never reached. $\square$

**Theorem 1 (privacy with $c = 2$).** If $c = 2$, then for all $x \sim x'$ and every set $S \subseteq R$, $\Pr[M(x) \in S] \le e^{\varepsilon}\Pr[M(x') \in S]$.

*Proof.* Fix $x \sim x'$. For every $r$, $|u(x, r) - u(x', r)| \le \Delta u \le \Delta$, so $|s_x(r) - s_{x'}(r)| \le \varepsilon/2$. Hence $e^{s_x(r)} \le e^{\varepsilon/2} e^{s_{x'}(r)}$ for every $r$, and the sum over $r$ gives $Z_{x'} \le e^{\varepsilon/2} Z_x$. So

$$\frac{P_x(r)}{P_{x'}(r)} = \frac{e^{s_x(r)}}{e^{s_{x'}(r)}} \cdot \frac{Z_{x'}}{Z_x} \le e^{\varepsilon/2} \cdot e^{\varepsilon/2} = e^{\varepsilon}.$$

The sum over $r \in S$ of $P_x(r) \le e^{\varepsilon} P_{x'}(r)$ gives the claim, and Lemma 1 says that $P_x$ is the output distribution. The relation is symmetric, so the claim also holds with $x$ and $x'$ swapped. $\square$

**Theorem 2 (privacy with $c = 1$ for a monotone utility).** Assume that for every pair $x \sim x'$, either $u(x, r) \le u(x', r)$ for all $r$, or $u(x, r) \ge u(x', r)$ for all $r$. If $c = 1$, then for all $x \sim x'$ and every $S \subseteq R$, $\Pr[M(x) \in S] \le e^{\varepsilon}\Pr[M(x') \in S]$.

*Proof.* Fix $x \sim x'$. By symmetry of the relation we may name the pair so that $u(x, r) \le u(x', r)$ for all $r$, and we must prove the bound in both orders. With $c = 1$, $s_x(r) \le s_{x'}(r) \le s_x(r) + \varepsilon$ for every $r$. Summing the exponentials over $r$ gives $Z_x \le Z_{x'} \le e^{\varepsilon} Z_x$. Then

$$\frac{P_x(r)}{P_{x'}(r)} = \underbrace{e^{s_x(r) - s_{x'}(r)}}_{\le 1} \cdot \underbrace{\frac{Z_{x'}}{Z_x}}_{\le e^{\varepsilon}} \le e^{\varepsilon}, \qquad \frac{P_{x'}(r)}{P_x(r)} = \underbrace{e^{s_{x'}(r) - s_x(r)}}_{\le e^{\varepsilon}} \cdot \underbrace{\frac{Z_x}{Z_{x'}}}_{\le 1} \le e^{\varepsilon}.$$

The sum over $r \in S$ gives the claim in both orders. $\square$

The hypothesis is needed. Under replace neighbors, the count of one candidate rises by 1 and the count of another falls by 1, so the counts are not monotone. Take $R = (A, B)$, $u$ the count, $\Delta = 1$, $\varepsilon = 1$ and $c = 1$, with the replace neighbors $x = (A, A)$ and $x' = (A, B)$. The scores are $(2, 0)$ and $(1, 1)$, so $P_x(B) = 1/(e^2 + 1) = 0.119203$ and $P_{x'}(B) = 1/2$. The log ratio is $\ln((e^2 + 1)/2) = 1.433781 > 1$, so the version with $c = 1$ is not $1$-DP under replace. Both factors of the ratio move against $B$ here: its own score falls, and the normalizer grows.

**Theorem 3 (utility).** For every $x$ and $t \ge 0$, let $\mathrm{OPT} = \max_r u(x, r)$ and $\tau = \mathrm{OPT} - (c\Delta/\varepsilon)(\ln m + t)$. Then $\Pr[u(x, M(x)) \le \tau] \le e^{-t}$.

*Proof.* Let $B = \{r : u(x, r) \le \tau\}$. For $r \in B$, $s_x(r) \le \varepsilon\tau/(c\Delta) = \varepsilon\,\mathrm{OPT}/(c\Delta) - \ln m - t$. There are at most $m$ candidates in $B$, so $\sum_{r \in B} e^{s_x(r)} \le m \cdot e^{\varepsilon\,\mathrm{OPT}/(c\Delta)} \cdot e^{-\ln m - t} = e^{\varepsilon\,\mathrm{OPT}/(c\Delta) - t}$. A candidate $r^*$ with $u(x, r^*) = \mathrm{OPT}$ gives $Z_x \ge e^{s_x(r^*)} = e^{\varepsilon\,\mathrm{OPT}/(c\Delta)}$. By Lemma 1, $\Pr[M(x) \in B] = \sum_{r \in B} e^{s_x(r)} / Z_x \le e^{-t}$. $\square$

If the set $R_{\mathrm{OPT}}$ of best candidates has more than one element, the bound on $Z_x$ improves by the factor $|R_{\mathrm{OPT}}|$, and the same proof gives $\ln(m/|R_{\mathrm{OPT}}|)$ in place of $\ln m$, which is Dwork-Roth Theorem 3.11.

**Lemma 2 (the Gumbel max trick).** Let $G_1, \ldots, G_m$ be independent standard Gumbel variables, with $\Pr[G \le g] = \exp(-e^{-g})$. Then $\arg\max_j (s_x(r_j) + G_j)$ has the distribution $P_x$.

*Proof.* Write $s_j = s_x(r_j)$. The index $j$ wins when $G_i < s_j + G_j - s_i$ for all $i \ne j$; ties have probability 0. Given $G_j = g$, this has probability $\prod_{i \ne j} \exp(-e^{-(s_j + g - s_i)}) = \exp(-e^{-g - s_j}(Z - e^{s_j}))$, with $Z = \sum_i e^{s_i}$. The density of $G_j$ is $e^{-g}\exp(-e^{-g})$, so

$$\Pr[j \text{ wins}] = \int_{-\infty}^{\infty} e^{-g} \exp\big(-e^{-g} Z e^{-s_j}\big)\, dg = \frac{1}{Z e^{-s_j}} = \frac{e^{s_j}}{Z},$$

with the substitution $v = e^{-g}$, which turns the integral into $\int_0^\infty e^{-v Z e^{-s_j}}\,dv$. $\square$
