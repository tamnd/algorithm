---
tag: 9RHJGA
kind: algorithm
slug: hire-assistant
name: Hire-assistant
aliases:
- hire-assistant strategy
area: foundations/probabilistic-analysis
level: intro
summary: Interview each candidate and hire whenever one beats the current best; expected hires are H_n.
solves: [hiring-problem]
model: comparison-model
complexity:
  vars: {n: the number of candidates, m: the number of hires}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: true, deterministic: true, comparison: true, recursive: false}
prereqs: [find-maximum, indicator-random-variable, linearity-of-expectation, random-permutation]
see_also: [hiring-problem, secretary-problem, randomized-algorithm, fisher-yates-shuffle, average-case-analysis]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 5, Section 5.1 (the procedure HIRE-ASSISTANT), Section 5.2 (expected number of hires) and Section 5.3 (RANDOMIZED-HIRE-ASSISTANT)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.10, Algorithm M (find the maximum) and its analysis
---

Hire-assistant is the procedure of the [hiring problem](/hiring-problem/): interview the candidates one at a time and hire each one who is better than the best so far. It does $n$ interviews, $n - 1$ comparisons and $m$ hires, where $m$ is between $1$ and $n$. On a uniformly random order, the expected number of hires is $H_n \approx \ln n$, and the randomized version, which shuffles first, has this expected value on each input. It is the [find-maximum](/find-maximum/) scan, with a cost charged at each change of the maximum.

## In plain words

You see the candidates one by one. You keep in mind the best person you have seen so far. When a new person is better than that best person, you hire the new person, and they become the new best. Otherwise you send the new person away.

At the end, the person you hired last is the best of all. The work of comparing is the same for every order of the candidates. The number of hires is what changes. It is large when the candidates get better and better, and small when a very good one comes early. If you mix the list into a random order before you start, you can expect only a few hires.

## The problem

The input is a list of $n$ candidates $C[1 \ldots n]$ from a total order, "better" meaning larger. The output is the list of hires: the positions $i$ such that $C[i]$ is better than each of $C[1], \ldots, C[i-1]$. The cost model gives each interview cost $c_i$ and each hire cost $c_h$. This is the [hiring problem](/hiring-problem/), which also covers the analysis of the number of hires and the online variants.

## The algorithm

```pseudo id=main
HIRE-ASSISTANT(C[1 .. n])
L1  best ← 0                         ▷ candidate 0 is a dummy, worse than all
L2  for i ← 1 to n do
L3      interview candidate C[i]
L4      if C[i] is better than C[best] then
L5          best ← i
L6          hire candidate i
```

The dummy candidate 0 makes candidate 1 a hire. In code, the test $best = 0$ replaces the dummy. The test is a strict "better", so of several equal candidates only the first is hired.

**Randomized version.** RANDOMIZED-HIRE-ASSISTANT first puts the list in a uniformly random order, for example with the [Fisher-Yates shuffle](/fisher-yates-shuffle/), and then runs HIRE-ASSISTANT. The output is then a random set of hires, but the last hire is still a best candidate.

## Example

Run HIRE-ASSISTANT on $C = [5, 2, 8, 6, 9, 1, 10, 3, 7, 4]$.

| $i$ | $C[i]$ | best before | hired? | best after |
| --- | --- | --- | --- | --- |
| 1 | 5 | dummy | yes | 5 |
| 2 | 2 | 5 | no | 5 |
| 3 | 8 | 5 | yes | 8 |
| 4 | 6 | 8 | no | 8 |
| 5 | 9 | 8 | yes | 9 |
| 6 | 1 | 9 | no | 9 |
| 7 | 10 | 9 | yes | 10 |
| 8 to 10 | 3, 7, 4 | 10 | no | 10 |

There are 10 interviews and 4 hires, so the cost is $10c_i + 4c_h$. The sorted order $[1, 2, \ldots, 10]$ gives 10 hires, and any order with 10 first gives 1 hire.

## Correctness

The loop of line L2 keeps this [loop invariant](/loop-invariant/): before the iteration for $i$, $C[best]$ is a best candidate among $C[1 \ldots i-1]$ (the dummy if $i = 1$), and the hires so far are exactly the positions $j < i$ such that $C[j]$ is better than each of $C[1 \ldots j-1]$. Line L4 compares $C[i]$ with a best earlier candidate, so it is true if and only if $C[i]$ is better than all earlier candidates, which is the rule for a hire. Lines L5 and L6 then restore the invariant. At the end, the hires are the required positions, and the last hire is a best candidate of the list. The full proof is below.

## Complexity

- **Comparisons and time.** One comparison for each $i \ge 2$, so $n - 1$ comparisons and $\Theta(n)$ time on every input. The extra space is $\Theta(1)$ besides the output.
- **Hires in the worst case.** $m = n$, when the candidates arrive in increasing order. The cost is then $\Theta(c_h n)$.
- **Hires in the best case.** $m = 1$, when the best candidate arrives first.
- **Hires on a random order.** If the order is a uniform [random permutation](/random-permutation/), let $X_i$ be the [indicator](/indicator-random-variable/) that candidate $i$ is hired. Each of the first $i$ candidates is equally likely to be the best of them, so $\Pr[X_i = 1] = 1/i$, and by [linearity of expectation](/linearity-of-expectation/)
$$ \mathbb{E}[m] = \sum_{i=1}^{n}\frac1i = H_n = \ln n + O(1). $$
The expected cost is $c_i n + c_h H_n = O(c_i n + c_h \ln n)$. The [hiring problem](/hiring-problem/) page proves that the $X_i$ are independent and derives the variance $H_n - H_n^{(2)}$ and the exact distribution.
- **Randomized version.** After the shuffle, the order is uniform whatever the input was. So $\mathbb{E}[m] = H_n$ for each input, the expectation being over the random choices of the shuffle. The shuffle costs $\Theta(n)$ time.

The table gives $H_n$, the expected number of hires, and the worst case $n$:

| $n$ | 10 | 100 | 1000 | $10^6$ |
| --- | --- | --- | --- | --- |
| $\mathbb{E}[m] = H_n$ | 2.929 | 5.187 | 7.486 | 14.393 |
| worst case | 10 | 100 | 1000 | $10^6$ |

## Properties

- **Online.** The decision about candidate $i$ uses only candidates $1$ to $i$. The algorithm can fire an earlier hire later, which the strict online version, the [secretary problem](/secretary-problem/), does not allow.
- **Deterministic.** HIRE-ASSISTANT has no random choices, so its number of hires is a function of the input. Only the randomized version has random choices.
- **Comparison-based.** It uses only comparisons of candidates, so it works for any total order.
- **Oblivious comparisons.** The number of comparisons does not depend on the input. Only the number of writes to $best$ does.

## Variants and improvements

- **Randomized hire-assistant.** Shuffle first. This moves the randomness from an assumption about the input to the algorithm, as a [Las Vegas](/las-vegas-algorithm/) style guarantee: the output is always correct and only the cost is random.
- **Ties hired.** With "better or equal" in line L4, each equal best candidate is hired too. The last hire is then the last best candidate.
- **Threshold rule.** For the one-hire version, skip the first $k \approx n/e$ candidates and then hire the first one who beats them all. It hires the best with probability about $1/e$. See the [hiring problem](/hiring-problem/) and the [secretary problem](/secretary-problem/).
- **Minimum and maximum together.** If both the best and the worst are needed, compare the items in pairs, as in [minimum and maximum finding](/minimum-and-maximum-finding/), with about $3n/2$ comparisons instead of $2n - 2$.

## When to use it

Use the scan to find a maximum in one pass when the items arrive as a stream. Use the randomized version when each update of the maximum is expensive and the input order may be adversarial, for example sorted: shuffling first reduces the expected number of updates from $n$ to about $\ln n$. Do not shuffle when the order is already random or the updates are cheap, because the shuffle costs $\Theta(n)$ random numbers.

## Pitfalls

- **Expected over what.** The bound $H_n$ for HIRE-ASSISTANT holds only if the input order is uniformly random. On a sorted input it hires $n$ times. Only the randomized version has expected $H_n$ hires on each input.
- **A biased shuffle.** A shuffle that swaps each item with an item at a uniform position of the whole array does not give a uniform order, and the bound $H_n$ then fails. Use Fisher-Yates.
- **Strict and non-strict tests.** With repeated qualities, "better" and "better or equal" give different numbers of hires.
- **Counting comparisons.** With the dummy, line L4 runs $n$ times, but the first test is free. Code that starts with $best = 1$ does $n - 1$ comparisons.

## Implementations

## History

CLRS uses HIRE-ASSISTANT as the running example of Chapter 5, on probabilistic analysis and randomized algorithms. The same scan, analyzed for the number of changes of the maximum, is Algorithm M in Section 1.2.10 of Knuth's first volume, where the mean $H_n - 1$ of the number of changes and its variance are derived.

## References
