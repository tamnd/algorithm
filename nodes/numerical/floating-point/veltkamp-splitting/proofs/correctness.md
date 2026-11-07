---
title: Veltkamp splitting returns an exact split into short parts
proves: [correctness]
status: full
---

**Setting.** Radix 2, precision $p$, round to nearest with a symmetric tie rule (the rounded value of $-x$ is the negative of the rounded value of $x$), $1 \le s \le p - 1$, $\sigma = 2^s$, $C = \sigma + 1$. The input $a$ is a normal float, and no operation overflows. We use two facts about binary floats.

- **(F1)** If $U$ is a power of two and $k$ is an integer with $|k| \le 2^p$, then $kU$ is a float, provided $U \ge 2^{e_{\min} - p + 1}$ and no overflow occurs.
- **(F2)** If $x$ lies in a binade $[2^e, 2^{e+1}]$, every float in that binade is a multiple of $2^{e - p + 1}$, and rounding to nearest gives the nearest multiple of $2^{e-p+1}$ (ties by the tie rule).

**Theorem.** Lines L1 to L5 return $a_h$ and $a_l$ with $a_h + a_l = a$, $a_h$ a multiple of $\sigma\,\mathrm{ulp}(a)$, and $|a_l| \le \tfrac{\sigma}{2}\,\mathrm{ulp}(a)$.

*Proof.* Everything commutes with multiplication by a power of two (as long as nothing underflows or overflows) and with negation (by the symmetric tie rule), so assume $1 \le a < 2$. Then $\mathrm{ulp}(a) = q = 2^{1-p}$, and $a$ is a multiple of $q$.

**Step 1: $\gamma$ is a multiple of $\sigma q$ and $\gamma \ge \sigma + 1$.** The exact product $Ca = \sigma a + a$ satisfies $\sigma + 1 \le Ca < 2\sigma + 2$. If $Ca < 2\sigma$, it lies in $[\sigma, 2\sigma)$, where the float spacing is $\sigma q$; otherwise it lies in $[2\sigma, 4\sigma)$, with spacing $2\sigma q$. In both cases $\gamma = \mathrm{fl}(Ca)$ is a multiple of $\sigma q$ by (F2). Since $\sigma + 1$ is a float (by (F1), as $s \le p - 1$) and rounding is monotone, $\gamma \ge \sigma + 1$.

**Step 2: $\sigma \le \gamma - a \le 2\sigma$.** Write $\gamma = Ca + \epsilon_1$, so $\gamma - a = \sigma a + \epsilon_1$.

- *Upper bound.* If $\gamma \le 2\sigma$, then $\gamma - a \le 2\sigma - 1$. If $\gamma > 2\sigma$, then $Ca \ge 2\sigma$, because $2\sigma$ is a float and rounding is monotone; so $Ca$ lies in $[2\sigma, 4\sigma)$, the spacing there is $2\sigma q$, $|\epsilon_1| \le \sigma q$, and $\gamma - a = \sigma a + \epsilon_1 \le \sigma(2 - q) + \sigma q = 2\sigma$.
- *Lower bound.* If $a = 1$, then $Ca = \sigma + 1$ is a float, $\epsilon_1 = 0$ and $\gamma - a = \sigma$. If $a \ge 1 + q$ and $\gamma < 2\sigma$, then $|\epsilon_1| \le \sigma q / 2$ and $\gamma - a \ge \sigma(1 + q) - \sigma q/2 > \sigma$. If $\gamma \ge 2\sigma$, then $\gamma - a > 2\sigma - 2 \ge \sigma$, since $a < 2$ and $\sigma \ge 2$.

**Step 3: $\delta = -\mathrm{rnd}_{\sigma q}(\gamma - a)$.** By Step 2, $\gamma - a$ lies in $[\sigma, 2\sigma]$. Every float in that interval is a multiple of $\sigma q$ and every multiple of $\sigma q$ in it is a float by (F1), so rounding $\gamma - a$ to nearest is rounding it to the nearest multiple of $\sigma q$. By the symmetric tie rule, $\delta = \mathrm{fl}(a - \gamma) = -\mathrm{fl}(\gamma - a)$ is a multiple of $\sigma q$ with $|\delta - (a - \gamma)| \le \sigma q/2$.

**Step 4: line L4 is exact and $a_h$ is $a$ rounded to a multiple of $\sigma q$.** Since $\gamma$ is a multiple of $\sigma q$, $\gamma + \delta$ is a multiple of $\sigma q$, and $\gamma + \delta = a + (\delta - (a - \gamma))$, so $|\gamma + \delta - a| \le \sigma q / 2$. With $x = \gamma - a$, $\gamma + \delta = \gamma - \mathrm{rnd}_{\sigma q}(x)$, and since $\gamma$ is a multiple of $\sigma q$ this is the multiple of $\sigma q$ nearest to $\gamma - x = a$ (ties resolved by the tie rule applied to $x$). Because $1$ and $2$ are multiples of $\sigma q = 2^{s+1-p} \le 1$ and $1 \le a < 2$, we get $1 \le \gamma + \delta \le 2$, and $\gamma + \delta = k\sigma q$ with $|k| \le 2/(\sigma q) = 2^{p-s}$. By (F1) it is a float, so $a_h = \gamma + \delta$ exactly.

**Step 5: line L5 is exact.** $a - a_h$ is a multiple of $q$ with $|a - a_h| \le \sigma q / 2 = 2^{s-1} q$. Since $s - 1 \le p - 2$, by (F1) it is a float, so $a_l = a - a_h$ exactly. Consequently $a_h + a_l = a$.

**Bit counts.** $a_h = k\sigma q$ with $2^{p-s-1} \le |k| \le 2^{p-s}$, so $a_h$ has at most $p - s$ significant bits (when $|k| = 2^{p-s}$ it is a power of two). $a_l = mq$ with $|m| \le 2^{s-1}$; if $|m| = 2^{s-1}$ it is a power of two, otherwise $|m| < 2^{s-1}$ and $a_l$ has at most $s - 1$ bits. So for $s \ge 2$ the low part has at most $s - 1$ significant bits. $\square$

**Where the hypotheses are used.** Normality of $a$ and of the intermediate values lets (F1) and (F2) use the binade spacing; overflow of $Ca$ breaks Step 1. The symmetric tie rule is used in Step 3. Under directed rounding Steps 3 and 4 no longer give the nearest multiple of $\sigma q$, and this proof does not cover that case.
