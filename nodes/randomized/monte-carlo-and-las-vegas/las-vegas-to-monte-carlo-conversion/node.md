---
tag: BW62YR
kind: technique
slug: las-vegas-to-monte-carlo-conversion
name: Converting Las Vegas to Monte Carlo
aliases:
- Las Vegas truncation
- Monte Carlo to Las Vegas with a verifier
area: randomized/monte-carlo-and-las-vegas
level: advanced
summary: Stop a Las Vegas algorithm after a time bound; Markov's inequality then bounds the error probability of the resulting Monte Carlo algorithm.
prereqs: [las-vegas-algorithm, monte-carlo-algorithm, markov-inequality, geometric-distribution]
see_also: [error-amplification, one-sided-error, zpp, rp, co-rp, expected-running-time, karger-min-cut, randomized-quicksort]
sources:
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 1, Section 1.2 (Las Vegas and Monte Carlo, and the conversion by Markov's inequality) and Section 1.5 (ZPP equals RP intersected with co-RP)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.1 (Markov's inequality), and Chapter 6 (the probabilistic method, the large cut example turned into a Las Vegas algorithm)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 7, Randomized computation (the classes RP, co-RP and ZPP, and ZPP = RP intersected with co-RP)
  - paper: "Michael Luby, Alistair Sinclair and David Zuckerman, Optimal speedup of Las Vegas algorithms, Information Processing Letters 47(4), 1993"
    locator: pages 173 to 180 (restart strategies for an unknown running time distribution)
---

The Las Vegas to Monte Carlo conversion stops a [Las Vegas algorithm](/las-vegas-algorithm/) after a fixed number of steps. If the expected running time is at most $t$, then by [Markov's inequality](/markov-inequality/) a run is still going at step $2t$ with probability at most $1/2$, so the stopped algorithm is a [Monte Carlo algorithm](/monte-carlo-algorithm/) with a worst-case time bound. The converse, from Monte Carlo to Las Vegas, works only with a verifier that checks an answer; then the algorithm repeats until the verifier accepts. Together the two directions prove that [ZPP](/zpp/) equals [RP](/rp/) $\cap$ [co-RP](/co-rp/).

## In plain words

A program that is always right but sometimes slow can be given a deadline. If it usually finishes quickly, it rarely misses a generous deadline. When it misses, you report "no answer" or a safe default, and you accept that small chance of failure in exchange for a fixed time.

To go the other way, you need a fast way to check an answer. Then you run the fast but sometimes wrong program, check its answer, and run it again until the check passes. The answer you give is always right, and the number of tries is small on average. Without a checker, no general trick turns a program that can be wrong into one that is never wrong.

## When it applies

- **Las Vegas to Monte Carlo.** You have a Las Vegas algorithm with a bound $\mathbb{E}[T(x)] \le t(n)$ on every input $x$ of size $n$, and you need a hard time limit: a real-time system, a step of a larger algorithm with a fixed budget, or a proof that a problem is in a class defined by worst-case time.
- **Monte Carlo to Las Vegas.** You have a Monte Carlo algorithm that is correct with probability at least $p$ on every input, and a deterministic verifier that decides whether a proposed output is correct, faster than solving the problem. Typical cases: a factor can be checked by division, a large cut by counting its edges, a solution of a system by substitution.

Notation on this page: $n$ is the input size, $\delta$ is the failure probability, and $\Pr$ and $\mathbb{E}$ are over the random bits of the algorithm for one fixed input. Each run uses fresh, independent random bits.

## The template

```pseudo id=main
LAS-VEGAS-TO-MONTE-CARLO(x, A, t, δ)    ▷ A is Las Vegas, E[T_A(x)] ≤ t
L1  k ← ⌈ln(1/δ)⌉                         ▷ hole: the number of runs
L2  for i ← 1 to k do
L3      run A(x) with fresh random bits for at most ⌈e·t⌉ steps   ▷ hole: the cut-off
L4      if A stopped then return its output
L5  return ⊥                               ▷ hole: the answer on time-out

MONTE-CARLO-TO-LAS-VEGAS(x, M, V)       ▷ M correct with probability ≥ p; V verifies
L6  repeat
L7      y ← M(x) with fresh random bits
L8  until V(x, y) accepts
L9  return y
```

**The cut-off (lines L1 to L5).** One run stopped at step $\tau$ fails when $T > \tau$. Since $T \ge 0$, Markov's inequality gives

$$\Pr[T > \tau] \le \Pr[T \ge \tau] \le \frac{\mathbb{E}[T]}{\tau} \le \frac{t}{\tau}.$$

With $\tau = c\,t$ for a constant $c > 1$, one run fails with probability at most $1/c$. The $k$ runs are independent, so all of them fail with probability at most $c^{-k}$, and the total time is at most $k c t$. To reach failure probability $\delta$, take $k = \lceil \ln(1/\delta) / \ln c \rceil$, for a total time of about $(c / \ln c)\, t \ln(1/\delta)$. The factor $c/\ln c$ is smallest at $c = e$, where it equals $e$; the template uses this choice, with failure at most $e^{-k} \le \delta$. With $c = 2$ the factor is $2/\ln 2 \approx 2.885$, close to $e \approx 2.718$, and the program is simpler: $k = \lceil \log_2(1/\delta) \rceil$ runs of $2t$ steps.

**The time-out answer (line L5).** Three choices:

- Return $\bot$. The result never gives a wrong answer and fails with probability at most $\delta$. This is the second form of a Las Vegas algorithm.
- For a decision problem, return the fixed answer "no". Then the result is wrong only on "yes" inputs, so it has [one-sided error](/one-sided-error/) at most $\delta$. Returning "yes" gives one-sided error on the other side.
- For a search problem, return any output. This gives a Monte Carlo algorithm with error at most $\delta$, but it hides the failure from the caller, so $\bot$ is usually better.

**The verifier loop (lines L6 to L9).** Let $M$ run in time at most $t_M$ and be correct with probability at least $p$ on every input, and let $V$ run in time at most $t_V$ and accept $y$ if and only if $y$ is a correct output for $x$. The loop returns only outputs that $V$ accepts, so it is never wrong. The rounds are independent and each one ends the loop with probability at least $p$, so the number of rounds $R$ satisfies $\Pr[R > j] \le (1 - p)^j$ and

$$\mathbb{E}[R] = \sum_{j \ge 0} \Pr[R > j] \le \sum_{j \ge 0} (1 - p)^j = \frac{1}{p}, \qquad \mathbb{E}[T] \le \frac{t_M + t_V}{p}.$$

The verifier is necessary. If $V$ can accept a wrong output, the loop can return it, and the result is only a Monte Carlo algorithm.

**ZPP = RP ∩ co-RP.** Both directions of the template prove it.

- *ZPP ⊆ RP and ZPP ⊆ co-RP.* A ZPP algorithm has expected time at most a polynomial $t(n)$. Stop it at $2t(n)$ steps and answer "no" on time-out. On a "no" input it is never wrong; on a "yes" input it is wrong only on time-out, with probability at most $1/2$. That is an RP algorithm. Answering "yes" on time-out gives a co-RP algorithm.
- *RP ∩ co-RP ⊆ ZPP.* Let $A$ be an RP algorithm and $B$ a co-RP algorithm for the same language $L$. A "yes" from $A$ is always correct, and a "no" from $B$ is always correct; these two answers are the verifier. In each round, run both. If $x \in L$, $A$ says "yes" with probability at least $1/2$; if $x \notin L$, $B$ says "no" with probability at least $1/2$. So each round gives a certain answer with probability at least $1/2$, and the expected number of rounds is at most 2.

## Classic examples

- **Randomized quicksort with a deadline.** [Randomized quicksort](/randomized-quicksort/) on $n$ distinct keys has expected $2(n+1)H_n - 4n$ comparisons. Stopping it at twice that number gives a sort with a worst-case $O(n \log n)$ bound that fails with probability at most $1/2$. For $n = 10$ the cut-off is about $48.9$ comparisons, above the worst case of 45, so this run never fails: Markov's bound is often far from tight.
- **Search with a geometric running time.** To find a 1 in an array in which at least half the entries are 1, probe random positions. The expected number of probes is at most 2. Stopping at 4 probes fails with probability at most $(1/2)^4 = 1/16$, while Markov's inequality promises only $2/4 = 1/2$. When the tail of $T$ is known, use it instead of Markov.
- **ZPP ⊆ RP.** The proof above is the standard use of the cut-off with a default answer.
- **A large cut, Monte Carlo to Las Vegas.** In a graph with $m$ edges, a uniformly random 2-coloring of the vertices cuts $m/2$ edges in expectation, so it cuts at least $m/2$ edges with probability at least $1/(m/2 + 1)$. Counting the cut edges in $O(m)$ time is a verifier. The loop finds a cut with at least $m/2$ edges in expected $O(m^2)$ time, never failing. For the Petersen graph ($m = 15$) the bound is $2/17 \approx 0.118$; the exact probability of at least 8 cut edges is $460/1024 \approx 0.449$.
- **No verifier: minimum cut.** [Karger's algorithm](/karger-min-cut/) returns a minimum cut with probability at least $2/(n(n-1))$, but nothing cheaper than solving the problem tells whether a given cut is minimum. So the loop of lines L6 to L9 does not apply, and the algorithm stays Monte Carlo, used with [error amplification](/error-amplification/).

## Variations

- **One long run.** Stop a single run at $t/\delta$. The failure probability is at most $\delta$, but the time grows as $1/\delta$. For $\delta = 10^{-6}$ that is $10^6 t$, against $\lceil \ln 10^6 \rceil e\, t = 14e\,t \approx 38.1\, t$ for the template. Repetition is exponentially better.
- **Restarts with an unknown distribution.** If $\mathbb{E}[T]$ is not known, restart the algorithm with the cut-offs $1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8, \ldots$. Luby, Sinclair and Zuckerman (1993) proved that this sequence has expected time $O(\ell \log \ell)$, where $\ell$ is the expected time of the best fixed cut-off strategy for the unknown distribution, and that, on the worst distributions, no universal strategy does better by more than a constant factor. SAT solvers use this sequence for restarts.
- **High-probability bounds instead of Markov.** For algorithms with known tails, such as randomized quicksort, a [Chernoff bound](/chernoff-bound/) gives cut-offs of $O(n \log n)$ with failure probability $n^{-c}$, much better than $2\,\mathbb{E}[T]$ with failure $1/2$.
- **Two-sided error.** No verifier is known in general for [BPP](/bpp/) algorithms, and it is open whether BPP equals ZPP.

## Pitfalls

- **An average over inputs.** Markov's inequality needs $\mathbb{E}[T(x)] \le t$ for the fixed input $x$, with the expectation over the coins. A bound on the time averaged over random inputs gives nothing for a bad input.
- **Reused random bits.** If the runs of line L3 or line L7 reuse the same random bits, they repeat the same run, and the bounds $c^{-k}$ and $1/p$ fail. Each run needs fresh bits.
- **A wrong time-out answer.** Returning an arbitrary answer at line L5 for a decision problem makes the error two-sided. Return $\bot$ or a fixed answer on the side that should carry the error.
- **A probabilistic verifier.** Checking $AB = C$ with [Freivalds' algorithm](/freivalds-algorithm/) as the verifier at line L8 can accept a wrong product, so the loop is not Las Vegas.
- **Reading Markov as tight in practice.** The bound $\Pr[T \ge 2t] \le 1/2$ is attained only by distributions such as $T = 0$ or $T = 2t$ with probability $1/2$ each. For most algorithms the real failure rate at the cut-off is much smaller, so measure it before choosing a large $k$.

## Exercises

1. Show that with cut-off $c\,t$ and $\lceil \ln(1/\delta)/\ln c \rceil$ runs, the total time bound $c\,t \ln(1/\delta) / \ln c$ is smallest at $c = e$.
2. Let $A$ be a Las Vegas algorithm with $\mathbb{E}[T] \le t$ and $\mathrm{Var}[T] \le t^2$. Use [Chebyshev's inequality](/chebyshev-inequality/) to find a cut-off with failure probability at most $1/10$, and compare it with the one from Markov's inequality.
3. Prove that if a search problem has a Monte Carlo algorithm with success probability at least $1/n^2$ in time $O(n)$ and a verifier in time $O(n)$, then it has a Las Vegas algorithm with expected time $O(n^3)$.

## References
