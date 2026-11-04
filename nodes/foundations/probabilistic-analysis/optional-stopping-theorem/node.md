---
tag: 5M9HKN
kind: theorem
slug: optional-stopping-theorem
name: Optional stopping theorem
aliases:
- Doob's optional stopping theorem
area: foundations/probabilistic-analysis
level: advanced
summary: A martingale stopped at a stopping time T keeps its mean, E[X_T] = E[X_0], when T is bounded, or E[T] is finite and the steps are bounded, or the stopped process is bounded.
prereqs: [martingale, conditional-expectation, expected-value]
see_also: [walds-equation, azuma-inequality, 2-sat, schoning-algorithm, markov-inequality, monte-carlo-algorithm, markov-chain]
sources:
  - book: isbn:9780521406055
    title: David Williams, Probability with Martingales, Cambridge University Press, 1991
    locator: Chapter 10, Martingales (stopping times, the stopped process, and Theorem 10.10, Doob's Optional-Stopping Theorem, with the three conditions)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 13, Section 13.2, Stopping Times (the martingale stopping theorem and the gambler's ruin); Chapter 7, Section 7.1.1, Application, A Randomized Algorithm for 2-Satisfiability
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 4, Tail Inequalities, Section 4.4, Martingales (stopping times and the stopping theorem)
  - paper: doi:10.1109/SFCS.1991.185365
    title: Christos H. Papadimitriou, On selecting a satisfying truth assignment, Proceedings of the 32nd IEEE Symposium on Foundations of Computer Science (FOCS), 1991
    locator: the random walk algorithm for 2-SAT
---

The optional stopping theorem says that a [martingale](/martingale/), observed at a random time $T$ that is chosen without looking into the future, has the same mean as at the start, $\mathbb E[X_T] = \mathbb E[X_0]$, provided that $T$ is bounded, or $\mathbb E[T]$ is finite and the steps are bounded, or the stopped process is bounded. It turns a martingale into an equation, and it gives exact ruin probabilities, expected hitting times, and expected running times of random walk algorithms such as the one for [2-SAT](/2-sat/). Without a condition of this kind it is false: a fair game played until the first win always ends with a profit.

## Statement

Let $(\mathcal F_n)_{n \ge 0}$ be a filtration. A *stopping time* is a random variable $T$ with values in $\{0, 1, 2, \ldots\} \cup \{\infty\}$ such that $\{T = n\} \in \mathcal F_n$ for each $n \ge 0$. Then also $\{T \le n\} \in \mathcal F_n$ and $\{T > n\} \in \mathcal F_n$. Write $n \wedge T = \min(n, T)$, and, on the event $\{T < \infty\}$, $X_T = X_{T(\omega)}(\omega)$.

**Theorem.** Let $(X_n)_{n \ge 0}$ be a martingale with respect to $(\mathcal F_n)$, and let $T$ be a stopping time. Suppose that one of the following holds.

- **(a)** $T$ is bounded: $T \le N$ almost surely for a constant $N$.
- **(b)** $\mathbb E[T] < \infty$, and there is a constant $c$ with $\mathbb E\big[|X_{n+1} - X_n| \,\big|\, \mathcal F_n\big] \le c$ almost surely on the event $\{T > n\}$, for each $n \ge 0$.
- **(c)** $T < \infty$ almost surely, and there is a constant $K$ with $|X_{n \wedge T}| \le K$ almost surely for each $n \ge 0$.

Then $X_T$ is integrable and $\mathbb E[X_T] = \mathbb E[X_0]$. If $(X_n)$ is a supermartingale instead, then under the same conditions $\mathbb E[X_T] \le \mathbb E[X_0]$, and for a submartingale $\mathbb E[X_T] \ge \mathbb E[X_0]$.

Condition (b) holds in particular when $\mathbb E[T] < \infty$ and $|X_{n+1} - X_n| \le c$ always. The form with a conditional bound on $\{T > n\}$ only is the one that [Wald's equation](/walds-equation/) and the duration of the gambler's ruin need.

**Lemma (the stopped process).** For each stopping time $T$, the stopped process $X^T_n = X_{n \wedge T}$ is a martingale (a supermartingale, a submartingale) when $(X_n)$ is one. In particular $\mathbb E[X_{n \wedge T}] = \mathbb E[X_0]$ for each fixed $n$ ($\le$, $\ge$).

## In plain words

You play a fair game and you may stop whenever you like. Your rule to stop can use everything that happened so far, but not the future. The theorem says that no such rule makes the game favourable, as long as the game cannot run too long or swing too wide. Then, on average, you leave with what you brought.

The conditions matter. A player who doubles the bet after each loss and stops at the first win always ends one unit ahead. This needs unlimited credit. With a limit on credit, the rare large loss cancels the many small gains exactly.

The theorem is also a tool for computing. If a quantity that keeps its average is known at the start, and its value at the end is known in terms of an unknown probability or time, the equation gives that unknown.

## Proof

**Proof of the lemma.** For each $n \ge 0$ the telescoping sum gives
$$ X_{n \wedge T} = X_0 + \sum_{k=0}^{n-1} 1_{\{T > k\}}\,(X_{k+1} - X_k), \tag{1} $$
because the terms with $k < n \wedge T$ are exactly those with $k < n$ and $T > k$. Each event $\{T > k\}$ with $k \le n - 1$ is in $\mathcal F_k \subseteq \mathcal F_n$, so $X_{n \wedge T}$ is $\mathcal F_n$-measurable. It is integrable because $|X_{n \wedge T}| \le |X_0| + \sum_{k < n}(|X_{k+1}| + |X_k|)$. By (1), $X_{(n+1) \wedge T} - X_{n \wedge T} = 1_{\{T > n\}}(X_{n+1} - X_n)$. The factor $1_{\{T > n\}}$ is $\mathcal F_n$-measurable, so it comes out of the conditional expectation:
$$ \mathbb E\big[X_{(n+1) \wedge T} - X_{n \wedge T} \,\big|\, \mathcal F_n\big] = 1_{\{T > n\}}\,\mathbb E[X_{n+1} - X_n \mid \mathcal F_n] = 0, $$
and the value is $\le 0$ for a supermartingale and $\ge 0$ for a submartingale. Taking expectations and summing over $n$ gives $\mathbb E[X_{n \wedge T}] = \mathbb E[X_0]$ ($\le$, $\ge$). $\square$

**Proof under (a).** Since $T \le N$, $N \wedge T = T$, so $X_T = X_{N \wedge T}$ is integrable, and the lemma with $n = N$ gives $\mathbb E[X_T] = \mathbb E[X_{N \wedge T}] = \mathbb E[X_0]$ ($\le$, $\ge$). $\square$

**Proof under (c).** On the event $\{T < \infty\}$, which has probability 1, $n \wedge T = T$ for each $n \ge T$, so $X_{n \wedge T} \to X_T$ almost surely as $n \to \infty$. Since $|X_{n \wedge T}| \le K$, also $|X_T| \le K$, so $X_T$ is integrable. The bounded convergence theorem (the dominated convergence theorem with the constant $K$ as the bound) gives $\mathbb E[X_T] = \lim_n \mathbb E[X_{n \wedge T}]$, and by the lemma each $\mathbb E[X_{n \wedge T}]$ equals $\mathbb E[X_0]$ ($\le$, $\ge$). The limit keeps the equality or the inequality. $\square$

**Proof under (b).** Since $\mathbb E[T] < \infty$, $T < \infty$ almost surely, and again $X_{n \wedge T} \to X_T$ almost surely. Let
$$ W = |X_0| + \sum_{k=0}^{\infty} 1_{\{T > k\}}\,|X_{k+1} - X_k|. $$
By (1), $|X_{n \wedge T}| \le W$ for each $n$, and so $|X_T| \le W$. The terms of $W$ are not negative, so the expectation of the sum is the sum of the expectations (monotone convergence). For each $k$, $1_{\{T > k\}}$ is $\mathcal F_k$-measurable, so by the tower property and the hypothesis of (b),
$$ \mathbb E\big[1_{\{T > k\}}|X_{k+1} - X_k|\big] = \mathbb E\Big[1_{\{T > k\}}\,\mathbb E\big[|X_{k+1} - X_k| \,\big|\, \mathcal F_k\big]\Big] \le c\,\Pr(T > k). $$
Hence $\mathbb E[W] \le \mathbb E|X_0| + c\sum_{k \ge 0}\Pr(T > k) = \mathbb E|X_0| + c\,\mathbb E[T] < \infty$, by the tail sum formula for the [expected value](/expected-value/) of a variable with values in $\{0, 1, 2, \ldots\}$. So $X_T$ is integrable, and the dominated convergence theorem with the bound $W$ gives $\mathbb E[X_T] = \lim_n \mathbb E[X_{n \wedge T}] = \mathbb E[X_0]$ ($\le$, $\ge$). $\square$

## Consequences

### The gambler's ruin, fair game

Let $S_n$ be the simple random walk: $S_0 = 0$ and $S_n = \xi_1 + \cdots + \xi_n$ with independent $\xi_i = \pm 1$, each with probability $\frac12$. Fix integers $a, b \ge 1$, and let $T$ be the first $n$ with $S_n = -a$ or $S_n = b$. A gambler with $a$ units who wants to win $b$ units is ruined at $S_T = -a$.

1. *$\mathbb E[T] < \infty$.* In any block of $a + b$ consecutive steps, all steps are $+1$ with probability $2^{-(a+b)}$, and then the walk leaves the interval $(-a, b)$. The blocks are independent, so $\Pr(T > j(a+b)) \le (1 - 2^{-(a+b)})^j$, and $\mathbb E[T] = \sum_{k \ge 0}\Pr(T > k) \le (a + b)\sum_{j \ge 0}(1 - 2^{-(a+b)})^j = (a+b)2^{a+b}$.
2. *The probability to win.* $|S_{n \wedge T}| \le \max(a, b)$, so (c) applies: $0 = \mathbb E[S_T] = b\,P - a(1 - P)$, where $P = \Pr(S_T = b)$. So $P = \dfrac{a}{a + b}$.
3. *The expected duration.* $M_n = S_n^2 - n$ is a martingale (see [martingale](/martingale/)). Its step is $M_{n+1} - M_n = 2S_n\xi_{n+1}$, and on $\{T > n\}$, $|S_n| < \max(a, b)$, so the step is at most $2\max(a, b)$. With step 1, (b) applies: $0 = \mathbb E[M_T] = \mathbb E[S_T^2] - \mathbb E[T]$. So $\mathbb E[T] = b^2\frac{a}{a+b} + a^2\frac{b}{a+b} = ab$.

For $a = 3$ and $b = 7$: the gambler wins with probability $3/10$, and the game lasts $21$ rounds on average. For $a = 1$ and $b = 1000$, the gambler wins with probability $1/1001$, and the game lasts $1000$ rounds on average.

### The gambler's ruin, unfair game

Now let $\Pr(\xi_i = 1) = p \ne \frac12$ and $q = 1 - p$. Step 1 above holds with $\min(p, q)^{a+b}$ in place of $2^{-(a+b)}$. Let $r = q/p$.

- $r^{S_n}$ is a martingale, since $\mathbb E[r^{\xi}] = pr + q/r = q + p = 1$. On $[0, T]$ it is between $r^{-a}$ and $r^{b}$, so (c) gives $1 = P\,r^b + (1 - P)\,r^{-a}$, that is, $P = \dfrac{r^a - 1}{r^{a+b} - 1}$.
- $S_n - (p - q)n$ is a martingale with steps at most 2, so (b) gives $\mathbb E[T] = \mathbb E[S_T]/(p - q)$, with $\mathbb E[S_T] = bP - a(1 - P)$.

At American roulette a bet on red wins with probability $p = 18/38$. A player who bets 1 unit at a time and stops at a gain of 10 or a loss of 10 has $a = b = 10$, $r = 10/9$, and wins with probability $P = 0.2585$ instead of $\frac12$. The expected result is $\mathbb E[S_T] = -4.829$, and the expected number of rounds is $\mathbb E[T] = 91.76$.

### The random walk algorithm for 2-SAT

A 2-CNF formula on $n$ variables has clauses with at most two literals ([2-SAT](/2-sat/)). The algorithm of Papadimitriou (1991) starts from any assignment and repeats: if the assignment satisfies the formula, stop; otherwise take any unsatisfied clause, choose one of its literals uniformly at random, and flip that variable.

**Claim.** If the formula is satisfiable, the expected number of flips is at most $n^2$, from every starting assignment.

*Proof.* Fix a satisfying assignment $A^*$. Let $D_t$ be the number of variables on which the assignment after $t$ flips differs from $A^*$, let $\mathcal F_t$ hold the random choices of the first $t$ flips, and let $T$ be the number of flips until the algorithm stops; set $D_t = D_T$ for $t \ge T$. $T$ is a stopping time.

1. *The walk.* Each flip changes $D$ by exactly 1. If $t < T$, the chosen clause is false under the current assignment and true under $A^*$, so at least one of its literals has a variable on which the two assignments differ. Flipping that variable lowers $D$ by 1. So, given $\mathcal F_t$, $D_{t+1} = D_t - 1$ with probability $p_t \ge \frac12$, and $D_{t+1} = D_t + 1$ otherwise. If $t < T$ then $D_t \ge 1$, because $D_t = 0$ means the assignment is $A^*$ and the algorithm has stopped.
2. *The potential.* Let $h(d) = d(2n - d)$ for $0 \le d \le n$. Then $h \ge 0$, $h(d-1) + h(d+1) = 2h(d) - 2$, $h(d-1) - h(d+1) = 4(d - n) \le 0$, and $h(n-1) = h(n) - 1$. For $1 \le d \le n - 1$ and $p \ge \frac12$,
$$ p\,h(d-1) + (1-p)\,h(d+1) = h(d+1) + p\,\big(h(d-1) - h(d+1)\big) \le h(d+1) + \tfrac12\big(h(d-1) - h(d+1)\big) = h(d) - 1. $$
For $d = n$ every variable differs from $A^*$, so the flip lowers $D$ with probability 1, and $h(D_{t+1}) = h(n) - 1$.
3. *A supermartingale.* Let $M_t = h(D_t) + t \wedge T$. By step 2, $\mathbb E[M_{t+1} - M_t \mid \mathcal F_t] = 1_{\{T > t\}}\big(\mathbb E[h(D_{t+1}) \mid \mathcal F_t] - h(D_t) + 1\big) \le 0$. So $(M_t)$ is a supermartingale.
4. *Optional stopping with a bounded time.* For each fixed $t$, taking expectations in step 3 and summing over the first $t$ flips (case (a) of the theorem for the constant stopping time $t$) gives $\mathbb E[h(D_t)] + \mathbb E[t \wedge T] = \mathbb E[M_t] \le M_0 = h(D_0)$. Since $h \ge 0$, $\mathbb E[t \wedge T] \le h(D_0)$. As $t \to \infty$, $t \wedge T$ increases to $T$, and the monotone convergence theorem gives $\mathbb E[T] \le h(D_0) \le h(n) = n^2$. $\square$

For $n = 100$ variables this is at most $10^4$ expected flips. By [Markov's inequality](/markov-inequality/), a run of $2n^2$ flips fails to find a satisfying assignment with probability at most $\frac12$. The claim holds from every start, so $m$ runs of $2n^2$ flips, each starting where the last one stopped, all fail with probability at most $2^{-m}$. For $n = 100$ and $m = 30$ this is $600000$ flips and a failure probability of at most $9.3 \times 10^{-10}$. On an unsatisfiable formula the algorithm never stops by itself, so the bounded version is a one-sided [Monte Carlo algorithm](/monte-carlo-algorithm/). [Schöning's algorithm](/schoning-algorithm/) for 3-SAT uses a random walk of the same kind, with restarts.

### The stopped walk keeps its mean at fixed times

The lemma alone has content. Let $T$ be the first time that the simple random walk hits $+1$. Then $\mathbb E[S_{n \wedge T}] = 0$ for each $n$, so $\Pr(T \le n) + \mathbb E[S_n\,1_{\{T > n\}}] = 0$: the walks that have not yet reached $+1$ are, on average, deep below 0.

| $n$ | $\Pr(T \le n)$ | $\mathbb E[S_n \mid T > n]$ |
| --- | --- | --- |
| 10 | 0.7539 | $-3.063$ |
| 100 | 0.9204 | $-11.56$ |
| 1000 | 0.9748 | $-38.64$ |

## Tightness

None of the three conditions can be dropped, and the stopping time condition cannot be dropped either. Each example below breaks exactly one hypothesis.

**$\mathbb E[T] = \infty$: the walk stopped at $+1$.** Let $T$ be the first time that the simple random walk hits $+1$. By the fair gambler's ruin with $a$ and $b = 1$, the walk reaches $-a$ before $+1$ with probability $\frac{1}{a+1}$, so $\Pr(T = \infty) \le \frac1{a+1}$ for every $a$, and $T < \infty$ almost surely. But $S_T = 1$, so $\mathbb E[S_T] = 1 \ne 0 = \mathbb E[S_0]$. The steps are bounded by 1, so if $\mathbb E[T]$ were finite, (b) would give $\mathbb E[S_T] = 0$. Hence $\mathbb E[T] = \infty$. Condition (c) fails too, because $S_{n \wedge T}$ is not bounded below; the table above shows the walks that have not stopped drifting down.

**Unbounded steps: the doubling strategy.** In a fair game, bet $1$, and after each loss double the bet; stop at the first win. Let $X_n$ be the net gain after $n$ bets. If the first win is at bet $T$, the gain is $-(1 + 2 + \cdots + 2^{T-2}) + 2^{T-1} = 1$. $T$ has the [geometric distribution](/geometric-distribution/) with parameter $\frac12$, so $\mathbb E[T] = 2 < \infty$, and still $\mathbb E[X_T] = 1 \ne 0$. Condition (b) fails because on $\{T > n\}$ the next step has size $2^n$, which has no bound. With a credit limit that allows at most $m$ bets, the stopping time $T \wedge m$ is bounded, and (a) restores the mean: for $m = 10$ the player wins 1 with probability $1023/1024$ and loses $1023$ with probability $1/1024$, which is exactly 0 on average. At roulette, with $p = 18/38$, the same rule loses all $1023$ units with probability $0.001631$ and has expected result $-0.6702$ per session.

**Not a stopping time.** Let $\tau$ be the time in $\{0, 1, 2\}$ at which the fair walk reaches its maximum over the first two steps (the first such time). The four paths $++$, $+-$, $-+$, $--$ give $S_\tau = 2, 1, 0, 0$, so $\mathbb E[S_\tau] = \frac34 \ne 0$, although $\tau \le 2$. The event $\{\tau = 1\}$ depends on the second step, so $\tau$ is not a stopping time, and the lemma does not apply.

**Sufficient, not necessary.** The three conditions are not the weakest possible. Each of them makes the stopped process $X_{n \wedge T}$ dominated by one integrable variable ($\max_{k \le N}|X_k|$, $W$ or $K$), and more general versions ask only for uniform integrability of the stopped process. The three conditions here are the forms that are easy to check in algorithm analysis.

### Pitfalls

- **Check the conditions before using the equation.** The equation $\mathbb E[X_T] = \mathbb E[X_0]$ is false for the doubling strategy and for the walk stopped at $+1$, and both look harmless. In an analysis, first prove $\mathbb E[T] < \infty$ (as in step 1 of the gambler's ruin), or work with the bounded time $T \wedge n$ and let $n \to \infty$ with monotone convergence, as in the 2-SAT proof.
- **$T < \infty$ is not $\mathbb E[T] < \infty$.** The walk stopped at $+1$ stops with probability 1, but its expected stopping time is infinite.
- **Bounded steps are needed only before $T$.** For $S_n^2 - n$ the steps are not bounded in general, but they are bounded on $\{T > n\}$, and that is what (b) asks.
- **The future is not allowed.** A rule such as "stop at the highest point" or "stop one step before the first loss" is not a stopping time. With such a rule the mean is not kept.
- **The direction for supermartingales.** For a supermartingale the theorem gives only $\mathbb E[X_T] \le \mathbb E[X_0]$. In the 2-SAT proof this is the direction that bounds $\mathbb E[T]$ from above.

## History

The theorem is part of the theory of martingales that J. L. Doob built, and Williams states it as Doob's Optional-Stopping Theorem, Theorem 10.10, with the three conditions used here. The gambler's ruin is a classical problem of probability; Mitzenmacher and Upfal solve it with the martingale stopping theorem in Section 13.2. Papadimitriou gave the random walk algorithm for 2-SAT in 1991. Mitzenmacher and Upfal, Section 7.1.1, analyse it with a Markov chain argument and the bound $n^2$ on the expected number of steps; the potential $d(2n - d)$ in the proof above is the expected hitting time of the worst case walk, where the probability to move toward $A^*$ is exactly $\frac12$.

## References
