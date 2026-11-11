---
title: Rumor mongering is safe, stops with probability 1, can miss sites, and has s = e^(-m) in its rate equations
proves: [correctness]
status: full
---

**Setting.** Sites run lines L1 to L8 in lock-step cycles on the complete graph with $n \ge 3$ sites and no failures. Each infective site makes one contact per cycle. $K_t$ is the set of sites that know the update after cycle $t$, with $K_0 = \{s_0\}$ for the source $s_0$. The parameter $k \ge 1$ is an integer for the counter and a real number at least 1 for the coin.

**Lemma 1 (safety and monotonicity).** For every $t$, $K_t \subseteq K_{t+1}$, and every site in $K_t$ holds the update of the source.

*Proof.* A site starts to know the update only at line L4, on receiving UPDATE, and UPDATE is sent only at line L3 by a site that knows the update. By induction on $t$, every UPDATE carries the update of the source. No line removes the update from a site. $\square$

**Lemma 2 (one message per infective site per cycle).** The traffic is $m = \frac{1}{n}\sum_{t \ge 1} I_{t-1}$, where $I_t$ is the number of infective sites after cycle $t$.

*Proof.* Lines L1 to L3 send exactly one UPDATE for each site that is infective at the start of the cycle, and no other line sends an update. $\square$

**Theorem 1 (termination).** With probability 1 there is a finite cycle after which no site is infective.

*Proof.* In cycle 1 only the source is infective, and its contact reaches a site that does not know the update, so $|K_1| = 2$. From then on $|K_t| \ge 2$ by Lemma 1. Take any cycle $t \ge 2$ and any site $p$ infective at its start. At least one site other than $p$ knew the update at the start of the cycle, so $p$'s contact is not needed with probability at least $1/(n - 1)$, independently of everything before the cycle and of the choices of the other sites.

Counter. If the contacts of $p$ in $k$ consecutive cycles are all not needed, then $p$ stops at line L7 in the last of them, with or without the reset at line L6 and with or without feedback. Given the past, this happens with probability at least $(n - 1)^{-k}$ in each block of $k$ cycles. Coin. In each cycle from 2 on, $p$ stops at line L8 with probability at least $1/(k(n - 1))$, given the past.

So in each block of $k$ cycles every infective site stops with probability at least $q = \min\{(n - 1)^{-k}, 1/(k(n - 1))\} > 0$, given the past. A site that becomes infective later is also infective for a finite time with probability 1 by the same bound. At most $n$ sites ever become infective, since by Lemma 1 and line L4 each site becomes infective at most once. The time each one is infective is at most a geometric number of blocks with success probability $q$, which is finite with probability 1. A finite union of events of probability 1 has probability 1. $\square$

**Theorem 2 (incomplete delivery has positive probability).** For every fixed $k$ and every $n \ge 3$, with positive probability the process stops with $n - 2$ sites that never received the update.

*Proof.* Let $q$ be the site that the source calls in cycle 1. Consider the event that in each of the cycles 2 to $k + 1$ the source calls $q$ and $q$ calls the source. It has probability $(n - 1)^{-2k} > 0$. On this event, every contact from cycle 2 on is not needed, because both sites knew the update at the start of the cycle. Counter: each of the two sites adds one to its count in each of these $k$ cycles, and the reset at line L6 never applies, so both stop at the end of cycle $k + 1$. Coin: use only cycle 2, in which the two sites call each other and both coins say stop; this has probability $(n - 1)^{-2} k^{-2} > 0$. Blind forms: the same argument works, since every contact counts. After that no site is infective, and the other $n - 2$ sites never received an update. $\square$

**Theorem 3 (the rate equations).** Let $s(t), i(t)$ solve
$$\frac{ds}{dt} = -s i, \qquad \frac{di}{dt} = s i - \frac{1}{k}(1 - s) i, \qquad \frac{dm}{dt} = i,$$
with $s(0) = 1 - \varepsilon$, $i(0) = \varepsilon$, $m(0) = 0$ and $\varepsilon \in (0, 1)$. Then $s(t) = (1 - \varepsilon) e^{-m(t)}$ for all $t$. In the limit $\varepsilon \to 0$, the final value $s_\infty$ is the root in $(0, 1)$ of $s = e^{-(k + 1)(1 - s)}$, and $m_\infty = (k + 1)(1 - s_\infty) = \ln(1/s_\infty)$.

*Proof.* While $s > 0$, $\frac{d}{dt}\ln s = -i = -\frac{dm}{dt}$, so $\ln s(t) - \ln(1 - \varepsilon) = -m(t)$. This is the first claim. While $i > 0$, $s$ is strictly decreasing, so $s$ can serve as the variable. Dividing the second equation by the first gives
$$\frac{di}{ds} = -1 + \frac{1 - s}{k s} = -\frac{k + 1}{k} + \frac{1}{k s},$$
and integrating from $s(0)$ gives
$$i(s) = \varepsilon + \frac{k + 1}{k}\bigl(1 - \varepsilon - s\bigr) + \frac{1}{k}\ln\frac{s}{1 - \varepsilon}.$$
As $\varepsilon \to 0$ this tends to $g(s) = \frac{k + 1}{k}(1 - s) + \frac{1}{k}\ln s$. Here $g'(s) = -(k + 1)/k + 1/(k s)$ and $g''(s) = -1/(k s^2) < 0$, so $g$ is concave on $(0, 1]$, with $g(1) = 0$ and $g'(1) = -1$. Also $g(s) \to -\infty$ as $s \to 0$. Since $g$ is concave with $g(1) = 0$ and $g'(1) = -1 < 0$, $g$ is positive just below 1 and has exactly one root $s_\infty$ in $(0, 1)$. Then $i$ falls to 0 as $s$ reaches $s_\infty$, and setting $g(s_\infty) = 0$ gives $\ln s_\infty = -(k + 1)(1 - s_\infty)$. By the first claim, $m_\infty = -\ln s_\infty = (k + 1)(1 - s_\infty)$. $\square$

**Corollary (blind and coin).** With $\frac{di}{dt} = s i - i/k$ instead, the same steps give $\frac{di}{ds} = -1 + \frac{1}{k s}$ and $g(s) = (1 - s) + \frac{1}{k}\ln s$. For $k > 1$, $g'(1) = -1 + 1/k < 0$, so there is one root in $(0, 1)$, the root of $s = e^{-k(1 - s)}$, and again $s_\infty = e^{-m_\infty}$. For $k = 1$, $g'(s) = -1 + 1/s > 0$ on $(0, 1)$, so $g < 0$ there and the only root is $s = 1$: in the limit nobody else hears the update. $\square$

**What is not proved here.** Theorem 3 is about the rate equations. That the residue of the random process tends to $s_\infty$ in probability as $n \to \infty$ is cited: Sudbury (1985) proved it for $k = 1$ with feedback and a coin. For the counter forms, the relation $s \approx e^{-m}$ is an observation of Demers et al. and of the simulator, not a theorem.
