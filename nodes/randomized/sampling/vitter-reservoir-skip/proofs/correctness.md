---
title: Algorithms X and Z draw the exact skip law, so the sample is uniform
proves: [correctness, termination]
status: full
---

**Statement.** Assume exact real arithmetic and independent uniform random reals. Let $k \ge 1$ and $t \ge k$, and let $S$ be the number of items that Algorithm R would reject after item $t$ before the next item it accepts. Then:

1. $\Pr[S \ge s] = \prod_{j=1}^{s} \frac{t+j-k}{t+j}$ and $f(s) := \Pr[S = s] = \frac{k}{t+s+1} \prod_{i=0}^{k-1} \frac{t-i}{t+s-i}$ for $s = 0, 1, 2, \ldots$
2. SKIP-X$(t, k)$ returns a value with law $f$.
3. If the state $W$ has the law of $U^{-1/k}$ for a uniform $U$ and is independent of the past, then SKIP-Z$(t, k)$ returns a value with law $f$, and the new state $W$ again has the law of $U^{-1/k}$ and is independent of the returned value and of the past.
4. Hence VITTER-RESERVOIR returns each $k$-subset of the $n \ge k$ positions with probability $1/\binom{n}{k}$, for every switch constant $T \ge 0$.

**Proof of 1.** In [Algorithm R](/reservoir-sampling/), item $t + j$ is accepted with probability $k/(t+j)$, independently of the other items (the draw of line L5 for item $t+j$ is fresh). So the first $s$ items after $t$ are all rejected with probability $\prod_{j=1}^{s} (1 - \frac{k}{t+j})$, which is the first formula. Then $f(s) = \Pr[S \ge s] \cdot \frac{k}{t+s+1}$. The product telescopes:
$$\prod_{j=1}^{s} \frac{t+j-k}{t+j} = \frac{(t+s-k)!/(t-k)!}{(t+s)!/t!} = \frac{t!/(t-k)!}{(t+s)!/(t+s-k)!} = \prod_{i=0}^{k-1} \frac{t-i}{t+s-i}.$$

**Proof of 2.** Write $P_s = \Pr[S \ge s]$, so $P_0 = 1$ and $P_s$ decreases to 0. Line L8 sets $q = P_1$, and each run of line L10 turns $q = P_s$ into $q = P_{s+1}$ while it increases $S$ from $s$ to $s+1$. So the loop returns the least $s$ with $P_{s+1} \le V$. The loop stops because $P_s \to 0$ and $V > 0$ with probability 1. The returned value is at least $s$ if and only if $P_s > V$, which has probability $P_s$ for a uniform $V$. So the returned value has the law of $S$.

**Proof of 3.** Let $c = \frac{t+1}{t-k+1}$, let $\mathit{term} = t - k + 1$, and define on $x \ge 0$
$$g(x) = \frac{k}{t+x}\left(\frac{t}{t+x}\right)^{k}, \qquad h(s) = \frac{k}{t+1}\left(\frac{\mathit{term}}{\mathit{term}+s}\right)^{k+1}.$$

*Step 3a: $g$ is the density of $X$.* With $W = U^{-1/k}$ and $X = t(W - 1)$, $\Pr[X > x] = \Pr[U < (t/(t+x))^k] = (t/(t+x))^k$. Its derivative is $-g(x)$, so $X$ has density $g$ on $[0, \infty)$.

*Step 3b: the envelope, $f(s) \le c\,g(x)$ for $s \le x < s+1$.* Since $x < s + 1$, $\frac{k}{t+s+1} < \frac{k}{t+x}$ and $\frac{t}{t+s+1} < \frac{t}{t+x}$. So it suffices to show $\prod_{i=0}^{k-1} \frac{t-i}{t+s-i} \le c \left(\frac{t}{t+s+1}\right)^k$. Write $c = \prod_{i=0}^{k-1} \frac{t+1-i}{t-i}$ (the product telescopes). We show the inequality factor by factor: $\frac{t-i}{t+s-i} \le \frac{t+1-i}{t-i} \cdot \frac{t}{t+s+1}$. Put $a = t - i \ge 1$, so $t = a + i$. Clearing the positive denominators, the claim is $a^2 (a + i + s + 1) \le (a + i)(a + 1)(a + s)$. Expanding, the right side minus the left side is $as + ias + ia + is \ge 0$.

*Step 3c: the squeeze, $h(s) \le f(s)$.* Each factor $\frac{t-i}{t+s-i}$ with $0 \le i \le k-1$ is at least $\frac{\mathit{term}}{\mathit{term}+s}$, because $a \mapsto a/(a+s)$ does not decrease and $t - i \ge \mathit{term}$. So $f(s) \ge \frac{k}{t+s+1} (\frac{\mathit{term}}{\mathit{term}+s})^k$. Also $\frac{1}{t+s+1} \ge \frac{\mathit{term}}{(t+1)(\mathit{term}+s)}$, since $(t+1)(\mathit{term}+s) - \mathit{term}(t+s+1) = ks \ge 0$. Together these give $f(s) \ge h(s)$.

*Step 3d: what the tests compute.* Put $S = \lfloor X \rfloor$. Dividing, $\frac{h(S)}{c\,g(X)} = \frac{\mathit{term}\,(t+X)}{(t+1)^2} \left(\frac{\mathit{term}}{\mathit{term}+S}\right)^{k+1} \left(\frac{t+X}{t}\right)^{k}$. The inequality $U \le \frac{h(S)}{c\,g(X)}$ is equivalent, after moving the factors without exponent $k$ to the left and taking $k$-th roots of positive numbers, to $\mathit{lhs} \le \mathit{rhs}$ with the values of lines L15 and L16. In the same way, $U \le \frac{f(S)}{c\,g(X)}$ is equivalent to $y \le ((t+X)/t)^k$ with the $y$ of line L18, which is the test of line L20. So line L17 accepts when $U \le h(S)/(c\,g(X))$, and line L20 accepts when $U \le f(S)/(c\,g(X))$. Since $h \le f$, line L17 never accepts a round that line L20 would reject, and a round that reaches line L20 has $U > h(S)/(c\,g(X))$, where the test $U \le f(S)/(c\,g(X))$ decides. So each round accepts if and only if $U \le f(S)/(c\,g(X))$.

*Step 3e: rejection.* In one round, the probability to accept with value $s$ is $\int_s^{s+1} g(x) \frac{f(s)}{c\,g(x)}\,dx = f(s)/c$, by step 3b (the ratio is at most 1). The rounds are independent, so the returned value is $s$ with probability $\frac{f(s)/c}{\sum_{s'} f(s')/c} = f(s)$. The number of rounds is geometric with mean $c$, so the loop stops with probability 1.

*Step 3f: the new state.* If line L19 runs, $W$ is a fresh $U^{-1/k}$. If line L17 accepts, then given $X$ and the acceptance, $U$ is uniform on $[0, q]$ with $q = h(S)/(c\,g(X))$, so $U/q$ is uniform on $[0, 1]$ and independent of $X$. Line L17 sets $W = \mathit{rhs}/\mathit{lhs} = (q/U)^{1/k} = (U/q)^{-1/k}$, which has the law of $U^{-1/k}$ and is independent of $S$.

**Proof of 4.** Algorithm R accepts item $t$ with probability $k/t$ and then puts it in a uniform slot, all independently. VITTER-RESERVOIR draws the gap to the next accepted item with the exact law of part 1 (by part 2 or part 3, whichever line L4 picks, and by part 3 the state $W$ is always fresh), then puts the item in a uniform slot, and then continues from $t + S + 1$ with fresh randomness. So, by induction on the number of accepted items, the sequence of (accepted position, slot) pairs has the same joint law as in Algorithm R, and so has the final reservoir. By the correctness of Algorithm R, it is a uniform $k$-subset. Each round of line L3 moves $t$ forward by at least 1, so the loop stops after at most $n - k + 1$ rounds. $\blacksquare$
