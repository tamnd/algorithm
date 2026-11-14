---
title: The CUSUM statistic is the maximum log likelihood ratio over change times, its false alarm run length is at least e^h, and its worst-case delay is E_1[T]
proves: [correctness]
status: full
---

Notation is that of the page. The scores are $Z_t = \log f_1(x_t) - \log f_0(x_t)$, the threshold is $h > 0$, $S_t$ is the value of $S$ after line L5 at time $t$, $k_t$ is the value of $k$ at that point, and $T = \inf\{t : S_t \ge h\}$ is the alarm time. Write $\Lambda_{k,t} = \sum_{i=k}^{t} Z_i$, with $\Lambda_{t+1,t} = 0$. Under $P_\nu$ the observations $x_1, \ldots, x_{\nu-1}$ have density $f_0$ and $x_\nu, x_{\nu+1}, \ldots$ have density $f_1$, all independent; $P_\infty$ means no change. We assume that $f_0$ and $f_1$ have the same support, so that every $Z_t$ is finite, and that $D = D(f_1 \,\|\, f_0) = E_1[Z_1]$ is finite and positive.

**Lemma 1 (the recursion is the maximum over change times).** For every $t \ge 0$,
$$S_t = \max_{1 \le k \le t+1}\Lambda_{k,t},$$
and $k_t$ is the largest $k$ in $\{1, \ldots, t+1\}$ at which the maximum is attained.

*Proof.* By induction on $t$. For $t = 0$, line L1 sets $S_0 = 0 = \Lambda_{1,0}$ and $k_0 = 1$, the only index. Let $t \ge 1$ and assume the claim for $t - 1$. Lines L4 and L5 give $S_t = \max(0, S_{t-1} + Z_t)$. Since $\Lambda_{k,t} = \Lambda_{k,t-1} + Z_t$ for $k \le t$,
$$\max_{1 \le k \le t+1}\Lambda_{k,t} = \max\Bigl(\max_{1 \le k \le t}\Lambda_{k,t-1} + Z_t,\ \Lambda_{t+1,t}\Bigr) = \max(S_{t-1} + Z_t,\ 0) = S_t.$$
For the index: if $S_{t-1} + Z_t \le 0$, then every $\Lambda_{k,t}$ with $k \le t$ is at most 0, so $k = t + 1$ attains the maximum and it is the largest index; line L5 sets $k_t = t + 1$. If $S_{t-1} + Z_t > 0$, then $k = t + 1$ does not attain the maximum, and $\Lambda_{k,t} = \Lambda_{k,t-1} + Z_t$ attains it for $k \le t$ exactly when $\Lambda_{k,t-1}$ attains $S_{t-1}$. By the induction hypothesis the largest such $k$ is $k_{t-1}$, and line L5 leaves $k$ unchanged. $\square$

**Corollary (what the procedure returns).** Line L6 returns at the first $t$ with $S_t \ge h$, which is $T$, and the returned $k$ maximizes $\Lambda_{k,T}$, the log likelihood ratio of a change at time $k$ against no change, given $x_1, \ldots, x_T$. If no score reaches $h$, line L7 is reached when the input ends. Each pass of the loop does a constant number of operations.

**Lemma 2 (false alarm run length).** $E_\infty[T] \ge e^h$.

*Proof.* If $E_\infty[T] = \infty$ there is nothing to prove, so assume $E_\infty[T] < \infty$; then $T < \infty$ almost surely. Define the Shiryaev-Roberts statistic $R_0 = 0$ and
$$R_t = \sum_{k=1}^{t}e^{\Lambda_{k,t}} = (1 + R_{t-1})e^{Z_t}.$$
Under $P_\infty$, $Z_t$ is independent of $x_1, \ldots, x_{t-1}$ and $E_\infty[e^{Z_t}] = \int f_1 = 1$. So $E_\infty[R_t \mid x_1, \ldots, x_{t-1}] = 1 + R_{t-1}$, and $M_t = R_t - t$ is a [martingale](/martingale/) with $M_0 = 0$. The stopped process $M_{T \wedge n}$ is a martingale for each fixed $n$, so $E_\infty[R_{T \wedge n}] = E_\infty[T \wedge n] \le E_\infty[T]$. As $n \to \infty$, $R_{T \wedge n} \to R_T$ almost surely, and Fatou's lemma, which applies because $R_t \ge 0$, gives $E_\infty[R_T] \le E_\infty[T]$.

At the alarm, $S_T \ge h > 0$, so by Lemma 1 the maximum is attained at some $k \le T$, and $R_T \ge e^{\Lambda_{k,T}} = e^{S_T} \ge e^h$. Hence $e^h \le E_\infty[R_T] \le E_\infty[T]$. $\square$

**Lemma 3 (monotone in the start).** Run the recursion $S' = \max(0, S' + Z)$ on the same scores from two start values $0 \le a \le a'$. Then the two statistics satisfy $S_t(a) \le S_t(a')$ for all $t$, so the alarm from $a'$ comes no later than the alarm from $a$.

*Proof.* The map $s \mapsto \max(0, s + z)$ is nondecreasing for each $z$. Induction on $t$ gives the inequality, and the first time $S_t(a) \ge h$ also has $S_t(a') \ge h$. $\square$

**Lemma 4 (worst-case delay).** $\bar d(T) = E_1[T]$, where $\bar d$ is Lorden's worst-case delay defined on the page.

*Proof.* Fix $\nu \ge 1$ and the pre-change data $x_1, \ldots, x_{\nu-1}$. If $T \le \nu - 1$, then $(T - \nu + 1)^+ = 0$. Otherwise the alarm has not sounded by time $\nu - 1$, and from time $\nu$ on the statistic follows the recursion from the start value $a = S_{\nu-1} \ge 0$, driven by scores that are i.i.d. under $f_1$, with the same law as $Z_1, Z_2, \ldots$ under $P_1$. So $(T - \nu + 1)^+$ is at most the alarm time of the recursion started at $a$, and by Lemma 3 this is at most the alarm time $T^{(0)}$ of the recursion started at 0. Its conditional expectation is at most $E_1[T^{(0)}] = E_1[T]$. Hence $\bar d(T) \le E_1[T]$. The case $\nu = 1$ gives equality, since then there are no pre-change data and the delay is $T$ itself. $\square$

**Lemma 5 (bound on the delay).** Let $\tau = \inf\{t : \Lambda_{1,t} \ge h\}$. Then $T \le \tau$, and
$$E_1[T] \le E_1[\tau] = \frac{h + E_1[\Lambda_{1,\tau} - h]}{D}.$$

*Proof.* By Lemma 1, $S_t \ge \Lambda_{1,t}$ for every $t$, so $S_\tau \ge h$ and $T \le \tau$. Under $P_1$, $\Lambda_{1,t}$ is a random walk with i.i.d. increments of mean $D > 0$. Then $E_1[\tau] < \infty$: by the strong law of large numbers $\tau < \infty$ almost surely, and the standard renewal argument for a random walk with positive drift gives a finite mean. The time $\tau$ is a stopping time for $x_1, x_2, \ldots$, so [Wald's equation](/walds-equation/) gives $E_1[\Lambda_{1,\tau}] = D\,E_1[\tau]$. Write $\Lambda_{1,\tau} = h + (\Lambda_{1,\tau} - h)$, where the second term is the overshoot, which is nonnegative. $\square$

**Theorem.** The procedure returns the first time $T$ at which the maximum log likelihood ratio over change times reaches $h$, together with a maximizing change time. Its false alarm run length satisfies $E_\infty[T] \ge e^h$, and its worst-case delay satisfies $\bar d(T) = E_1[T] \le (h + E_1[\text{overshoot}])/D$. In particular, for a target run length $\gamma$, the choice $h = \log\gamma$ gives $E_\infty[T] \ge \gamma$ and a worst-case delay of $(\log\gamma)/D$ plus a term that stays bounded when the overshoot has a bounded mean.

*Proof.* The first sentence is the Corollary. The bounds are Lemmas 2, 4 and 5. $\blacksquare$

**What is cited.** Lorden (1971) proved that every stopping time with $E_\infty[T] \ge \gamma$ has $\bar d(T) \ge (1 + o(1))(\log\gamma)/D$ as $\gamma \to \infty$, so the Theorem shows that the CUSUM is first-order optimal. Moustakides (1986) proved exact optimality. Neither result is proved here.
