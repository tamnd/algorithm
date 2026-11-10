---
title: Algorithm S returns each n-subset with probability 1 over C(N, n)
proves: [correctness, termination]
status: full
---

**Statement.** Let $0 \le n \le N$, let the items be $x_1, \ldots, x_N$, and assume that line L3 draws a uniform integer in $\{0, \ldots, N - t - 1\}$, independently each time. Then SELECTION-SAMPLE stops, it returns exactly $n$ items in their input order, and each $n$-subset of the positions is returned with probability $1/\binom{N}{n}$. The number of random integers it draws is the position of the last selected item, and its expectation is $n(N+1)/(n+1)$ for $n \ge 1$.

**The invariant.** At the test of line L2, $0 \le n - m \le N - t$: the number still needed is at most the number of items not yet seen.

It holds at the start, with $m = t = 0$. Suppose it holds and $m < n$, so $N - t \ge n - m \ge 1$ and line L3 draws from a non-empty range. If $n - m = N - t$, every integer in the range is below $n - m$, so the item is selected, and both sides drop by 1. If $n - m < N - t$, then either the item is selected and both sides drop by 1, or it is not, and only $N - t$ drops by 1, which keeps $n - m \le N - t$. In both cases $m \le n$ stays true.

**Termination and size.** Each round increases $t$ by 1, and the invariant gives $t \le N - (n - m) \le N$, so there are at most $N$ rounds. The loop stops only when $m = n$, so the output has exactly $n$ items. Items are appended in increasing order of position.

**Uniformity.** Fix an $n$-subset $A$ of the positions, with $n \ge 1$, and let $L$ be its largest element. The algorithm returns $A$ exactly when, for $t = 0, \ldots, L - 1$, the decision about item $t + 1$ is "select" when $t + 1 \in A$ and "skip" otherwise; after the decision at $t = L - 1$, $m = n$ and the loop stops. Before the decision at step $t$, with $m$ items of $A$ among the first $t$ positions, the probability of "select" is $\frac{n - m}{N - t}$ and of "skip" is $\frac{N - t - (n - m)}{N - t}$, and the draws are independent. So the probability of $A$ is a product of $L$ fractions:

- The denominators are $N, N - 1, \ldots, N - L + 1$.
- The numerators of the "select" steps are $n - m$ for $m = 0, 1, \ldots, n - 1$, that is, $n, n - 1, \ldots, 1$, with product $n!$.
- At a "skip" step, $N - t - (n - m)$ is the number of positions among $t + 1, \ldots, N$ that are not in $A$, since $n - m$ of these $N - t$ positions are in $A$. Each skip uses up one such position, so these numerators are $N - n, N - n - 1, \ldots, N - n - (L - n) + 1$, with product $\frac{(N - n)!}{(N - L)!}$.

Hence
$$\Pr[\text{output} = A] = \frac{n! \cdot (N - n)!/(N - L)!}{N!/(N - L)!} = \frac{n!\,(N - n)!}{N!} = \frac{1}{\binom{N}{n}}.$$
For $n = 0$ the loop does not run and the empty set is returned with probability 1.

**The number of draws.** One integer is drawn per round, and the number of rounds is the largest element $L$ of the output, which is a uniform $n$-subset of $\{1, \ldots, N\}$. The number of such subsets with largest element $\ell$ is $\binom{\ell - 1}{n - 1}$, and $\ell \binom{\ell - 1}{n - 1} = n \binom{\ell}{n}$. So
$$E[L] = \frac{1}{\binom{N}{n}} \sum_{\ell = n}^{N} n \binom{\ell}{n} = \frac{n \binom{N+1}{n+1}}{\binom{N}{n}} = \frac{n(N+1)}{n+1},$$
using the hockey-stick identity $\sum_{\ell=n}^{N} \binom{\ell}{n} = \binom{N+1}{n+1}$. $\blacksquare$
