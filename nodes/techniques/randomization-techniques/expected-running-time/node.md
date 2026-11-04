---
tag: Y71M88
kind: concept
slug: expected-running-time
name: Expected running time
aliases:
- average running time over random choices
- expected complexity
area: techniques/randomization-techniques
level: intro
summary: The mean running time of a randomized algorithm over its internal random choices, for a fixed input.
prereqs: [randomized-algorithm, random-variable, expected-value]
see_also: [quicksort-expected-running-time, markov-inequality, chernoff-bound, linearity-of-expectation, average-case-analysis, las-vegas-algorithm, randomized-quickselect, yao-minimax-principle]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 5.2 (indicator random variables) and Section 5.3 (randomized algorithms, and expected running time versus average-case running time)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 1, Introduction (the expected running time of RandQS, Las Vegas algorithms, and the model of computation)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 2, Discrete Random Variables and Expectation (linearity of expectation, Jensen's inequality, the geometric distribution and the analysis of quicksort)
---

The expected running time of a [randomized algorithm](/randomized-algorithm/) on an input $x$ is the mean of its number of steps over its own random choices, with $x$ fixed. The expected running time of the algorithm on size $n$ is the largest of these means over all inputs of size $n$. So it is a worst case over the inputs of an average over the coins, and no assumption is made on how the inputs are chosen. It is the standard cost measure of [Las Vegas algorithms](/las-vegas-algorithm/) such as [randomized quicksort](/randomized-quicksort/).

## In plain words

A randomized program flips coins while it runs, so on the same input it can be fast one time and slow the next time. Run it many times on one input and take the average time. That average is the expected running time on that input.

Now let an opponent pick the input. The opponent can pick the hardest input, but cannot see or control the coins. The expected running time of the program is the average time on the hardest input. A good bound means that no input is bad on average.

This is different from an average over inputs. There, the program is fixed, and a bad input stays bad each time you run it. Here, every input gets the same promise, because the luck comes from inside the program.

## The idea

### Definition

Let $A$ be a randomized algorithm, and $T_A(x)$ the number of steps of $A$ on input $x$, a [random variable](/random-variable/) over the random bits of $A$. Then

$$ \bar T_A(n) = \max_{|x| = n} \mathbb{E}[T_A(x)]. $$

Two other measures are easy to confuse with it.

- The *worst-case* running time $\max_{|x| = n} \max_r T_A(x, r)$ takes the worst coins as well. For randomized quicksort it is $n(n - 1)/2$ comparisons, the same as for the deterministic version.
- The *average-case* running time $\mathbb{E}_{x \sim D}[T_B(x)]$ of a deterministic algorithm $B$ averages over a distribution $D$ of inputs. See [average-case analysis](/average-case-analysis/). Its value is only as good as the model $D$ of the inputs.

For quicksort the two averages have the same value, $2(n + 1)H_n - 4n$ comparisons on $n$ distinct keys, because a random pivot on a fixed input and a fixed pivot on a random order give the same distribution of splits. The guarantees differ: the randomized bound holds for each input, the average-case bound only for random inputs.

### How to compute it

- **Indicators and linearity.** Write $T$ as a sum $\sum_j X_j$ of [indicator random variables](/indicator-random-variable/), one for each unit of work that may happen, and use $\mathbb{E}[T] = \sum_j \Pr[X_j = 1]$. [Linearity of expectation](/linearity-of-expectation/) needs no independence. This is the proof for quicksort on the page [quicksort expected running time](/quicksort-expected-running-time/): keys $z_i < z_j$ are compared with probability $2/(j - i + 1)$.
- **Repeat until success.** A loop whose rounds succeed independently with probability $p$ runs a geometric number $R$ of rounds, and $\mathbb{E}[R] = 1/p$. If each round costs at most $c$, the loop costs at most $c/p$ in expectation.
- **A recurrence in expectation.** If one step on a problem of size $n$ costs $an$ and leaves one subproblem of random size $S$, then $\bar T(n) \le an + \mathbb{E}[\bar T(S)]$, where $\bar T$ is non-decreasing. When $\Pr[S \le 3n/4] \ge 1/2$, the solution is $\bar T(n) \le 8an$, which gives the linear bound of [randomized quickselect](/randomized-quickselect/).

### What an expectation does not give

The expectation is a single number. Three rules about it are wrong in general.

- **$\mathbb{E}[f(T)] \neq f(\mathbb{E}[T])$.** For a convex $f$, Jensen's inequality gives $\mathbb{E}[f(T)] \ge f(\mathbb{E}[T])$, and the gap can be infinite. Let $T$ be the number of fair coin flips up to the first head. Then $\mathbb{E}[T] = 2$ and $2^{\mathbb{E}[T]} = 4$, but $\mathbb{E}[2^T] = \sum_{k \ge 1} 2^{-k} 2^k$ diverges. So an algorithm that flips coins until a head and then does $2^T$ steps stops with probability 1 and has infinite expected running time.
- **$\mathbb{E}[XY] \neq \mathbb{E}[X]\,\mathbb{E}[Y]$** unless $X$ and $Y$ are independent, and **$\mathbb{E}[\max_i X_i] \neq \max_i \mathbb{E}[X_i]$**. A loop of $k$ rounds, each with expected cost $c$, costs $kc$ in expectation, but its slowest round can cost much more than $c$.
- **A bound on $\mathbb{E}[T]$ is not a bound on $T$.** It gives only [Markov's inequality](/markov-inequality/), $\Pr[T \ge \alpha\,\mathbb{E}[T]] \le 1/\alpha$. Sharper tails need more structure, for example a sum of independent parts and a [Chernoff bound](/chernoff-bound/).

### From expectation to high probability

A Las Vegas algorithm with $\bar T_A(n) \le t$ can be given an exponential tail by restarts. Run it with a budget of $2t$ steps; if it has not stopped, start again with fresh random bits.

**Claim.** With restarts, $\Pr[\text{more than } 2tk \text{ steps}] \le 2^{-k}$ for each integer $k \ge 0$, and the expected time stays at most $4t$.

*Proof.* By Markov's inequality, each round fails to stop with probability at most $1/2$, for every input. The rounds use independent bits, so the first $k$ rounds all fail with probability at most $2^{-k}$, and only then are more than $2tk$ steps used. The number of rounds is at most geometric with $p = 1/2$, so its mean is at most 2, and each round costs at most $2t$. $\square$

For a lower bound on $\bar T_A(n)$ for every randomized algorithm, the standard tool is [Yao's minimax principle](/yao-minimax-principle/): pick a distribution of inputs and bound the average cost of every deterministic algorithm on it.

## Examples

### Randomized quicksort

The expected number of comparisons on $n$ distinct keys, from [quicksort expected running time](/quicksort-expected-running-time/), against the worst case:

| $n$ | expected, $2(n + 1)H_n - 4n$ | worst case, $n(n - 1)/2$ |
| --- | --- | --- |
| 10 | 24.44 | 45 |
| 100 | 647.85 | 4,950 |
| 1,000 | 10,985.91 | 499,500 |

The expected value is the same for every input order, including a sorted input, which is the worst input for quicksort with a fixed first pivot.

### Search in a half-full array

An array of $n$ cells, $n$ even, holds the letter $a$ in exactly half of its cells, and the task is to return the index of an $a$. Any deterministic algorithm that probes cells in a fixed order can be given an input in which its first $n/2$ probes all find $b$, so it needs $n/2 + 1$ probes in the worst case: 6 for $n = 10$ and 501 for $n = 1000$. The Las Vegas algorithm that probes a uniformly random cell until it finds an $a$ succeeds in each probe with probability $1/2$, so it uses 2 probes in expectation on every input, and more than $k$ probes with probability $2^{-k}$, for example less than $10^{-6}$ for $k = 20$.

### An infinite expectation

The algorithm "flip a fair coin until a head appears, at flip $T$, then count to $2^T$" stops on every run with probability 1. The partial sums of $\mathbb{E}[2^T] = \sum_k 2^{-k} \cdot 2^k$ are 10 after 10 terms and 20 after 20 terms, and they grow without bound. This is the reason to state the cost as a bound on $\mathbb{E}[T]$ and not on $\mathbb{E}$ of a function of the coins.

## Where it is used

The expected running time is the cost measure of most Las Vegas algorithms: [randomized quicksort](/randomized-quicksort/) with $O(n \log n)$, [randomized quickselect](/randomized-quickselect/) with $O(n)$, the expected $O(\log n)$ search time of [treaps](/treap/) and [skip lists](/skip-list/), the expected $O(1)$ time of an operation on a [hash table](/hash-table/) with [universal hashing](/universal-hashing/), where the random choice is the hash function, and the expected bounds of [randomized incremental construction](/randomized-incremental-construction/) in geometry, which are often proved by [backwards analysis](/backwards-analysis/). In each case the bound holds for every input, and Markov's inequality or a restart turns it into a bound with high probability when one is needed.

## References
