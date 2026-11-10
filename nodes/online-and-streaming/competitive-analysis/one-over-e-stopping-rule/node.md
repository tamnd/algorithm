---
tag: 19FPEC
kind: algorithm
slug: one-over-e-stopping-rule
name: 1/e stopping rule
aliases:
- classic secretary algorithm
- 37 percent rule
- cutoff rule
area: online-and-streaming/competitive-analysis
level: intro
summary: Observe the first ⌊n/e⌋ candidates without hiring, then hire the first one who is better than all before. It hires the best with probability tending to 1/e.
solves: [secretary-problem]
model: comparison-model
complexity:
  vars: {n: the number of candidates, r: the cutoff}
  time: {worst: Θ(n), best: Θ(r)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, comparison: true, recursive: false}
history:
  year: 1963
  people: [E. B. Dynkin]
  note: Lindley (1961) and Dynkin (1963) showed that a cutoff rule of this form is optimal for the secretary problem and that its success probability tends to 1/e.
prereqs: [secretary-problem, random-permutation, harmonic-series]
see_also: [secretary-problem, online-hiring-problem, prophet-inequality, hire-assistant, hiring-problem, online-algorithm, competitive-ratio]
sources:
  - paper: doi:10.1214/ss/1177012493
    title: "Thomas S. Ferguson, Who solved the secretary problem?, Statistical Science 4(3) (1989), 282-296"
    locator: Section 2, the classical secretary problem, the cutoff rule and its success probability, and the history of Lindley and Dynkin
  - paper: doi:10.1080/01621459.1966.10502008
    title: "John P. Gilbert and Frederick Mosteller, Recognizing the maximum of a sequence, Journal of the American Statistical Association 61(313) (1966), 35-73"
    locator: Section 2, the no-information problem, the optimal cutoff for each n and its success probability
  - paper: "E. B. Dynkin, The optimum choice of the instant for stopping a Markov process, Soviet Mathematics Doklady 4 (1963), 627-629"
    locator: the cutoff rule as an optimal stopping time and the limit 1/e
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 5, Section 5.4.4, the on-line hiring problem, the rule that rejects the first k candidates, and the choice k = n/e
---

The 1/e stopping rule is the classic algorithm for the [secretary problem](/secretary-problem/): with $n$ candidates in uniformly random order, observe the first $r = \lfloor n/e \rfloor$ of them without hiring, then hire the first candidate who is better than each one before. It hires the best candidate with probability $P_n(r) = \frac{r}{n}\sum_{j=r+1}^{n} \frac{1}{j-1}$, which tends to $1/e \approx 0.3679$. It is an [online algorithm](/online-algorithm/) that only compares candidates, and the best rule of its form is optimal among all rules.

## In plain words

You interview people one at a time, and you must decide about each one before you see the next. A rejected person does not come back. You want to hire the single best person, and you know how many people will come.

The rule has two phases. In the first phase you hire nobody: you only look, and you remember the best person so far. This phase covers about 37 percent of the people. In the second phase you hire the first person who is better than everybody you saw before. If the best person of all is in the second phase, and the best person seen before them is in the first phase, you hire the best person. This happens a little more than one time in three.

## The problem

The input is a sequence $C[1 \ldots n]$ of distinct candidates from a total order, in uniformly random order, with $n$ known in advance. At step $i$ the algorithm sees only how $C[i]$ compares with $C[1], \ldots, C[i-1]$, and it must hire $C[i]$ or reject it for ever. It may hire at most one candidate. It succeeds if it hires the maximum of $C$. The goal is to maximize the probability of success. This is the [secretary problem](/secretary-problem/), which also covers the proof that no rule does better.

## The algorithm

```pseudo id=main
ONE-OVER-E(C[1 .. n])                       ▷ the candidates arrive in this order
L1  r ← ⌊n / e⌋                             ▷ the cutoff: observe only
L2  best ← −∞
L3  for i ← 1 to r do best ← max(best, C[i])
L4  for i ← r + 1 to n do
L5      if C[i] > best then return i        ▷ hire the first candidate who beats the first r
L6  return none                             ▷ no hire
```

Lines L2 and L3 compute the best of the first $r$ candidates. In the second phase, $best$ does not change: the first candidate after position $r$ who beats $best$ also beats each candidate between $r + 1$ and $i - 1$, because none of them beat $best$. So line L5 hires the first candidate after the cutoff who is better than all earlier candidates.

The value $\lfloor n/e \rfloor$ is the cutoff of the rule as it is usually stated. The exactly optimal cutoff $r^*$ is the least $r \ge 1$ with $\frac{1}{r+1} + \cdots + \frac{1}{n-1} \le 1$ (for $n \ge 3$); the [secretary problem](/secretary-problem/) page proves this. For each $n \le 200$, $r^*$ is $\lfloor n/e \rfloor$ or $\lfloor n/e \rfloor + 1$, and the two values give almost the same probability. For example, at $n = 100$, $r^* = 37$ gives $0.371043$ and $\lfloor 100/e \rfloor = 36$ gives $0.371015$.

## Example

Take $n = 10$ and $C = [6, 3, 8, 5, 9, 2, 10, 1, 7, 4]$. Line L1 gives $r = \lfloor 10/e \rfloor = \lfloor 3.679 \rfloor = 3$.

| $i$ | $C[i]$ | phase | $best$ after the step | action |
|---|---|---|---|---|
| 1 | 6 | observe | 6 | none |
| 2 | 3 | observe | 6 | none |
| 3 | 8 | observe | 8 | none |
| 4 | 5 | select | 8 | reject, $5 < 8$ |
| 5 | 9 | select | 8 | hire, $9 > 8$ |

The rule hires the candidate of value 9 at step 5, and it fails: the best candidate, 10, comes at step 7. With cutoff $r = 5$ the rule would see $best = 9$ after step 5, reject 2, and hire 10 at step 7. With cutoff $r = 1$ it would hire 8 at step 3.

Over all $10!$ orders, the rule with $r = 3$ succeeds with probability

$$P_{10}(3) = \frac{3}{10}\left(\frac12 + \frac13 + \cdots + \frac19\right) = \frac{3349}{8400} \approx 0.3987.$$

This is also the best value over all cutoffs for $n = 10$. The table gives the optimal cutoff and the exact optimum for small $n$:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 10 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\lfloor n/e \rfloor$ | 0 | 0 | 1 | 1 | 1 | 2 | 2 | 2 | 3 | 7 |
| optimal $r^*$ | 0 | 0 | 1 | 1 | 2 | 2 | 2 | 3 | 3 | 7 |
| $P_n(r^*)$ | 1 | 1/2 | 1/2 | 11/24 | 13/30 | 77/180 | 29/70 | 459/1120 | 3349/8400 | 0.3842 |

## Correctness

There are two claims. First, the rule hires the first candidate after position $r$ who is better than all earlier candidates, as the walk-through above shows. Second, if the order is uniformly random and the values are distinct, it hires the best candidate with probability

$$P_n(r) = \frac{r}{n} \sum_{j=r+1}^{n} \frac{1}{j-1} \quad (1 \le r < n), \qquad P_n(0) = \frac1n.$$

The key fact: the rule succeeds exactly when the best candidate is at a position $j > r$ and the best of the first $j - 1$ candidates is among the first $r$. The best is at $j$ with probability $1/n$, and given that, the best of the other first $j - 1$ positions is at each of them with the same probability, so it is in the first $r$ with probability $r/(j-1)$. The sum over $j$ gives $P_n(r)$. From the bounds $\ln(n/r) \le \sum_{i=r}^{n-1} 1/i \le 1/r + \ln(n/r)$ it follows that $P_n(\lfloor n/e \rfloor) \to 1/e$ and that no cutoff gives more than $1/e + 1/n$. The full proof is below.

## Complexity

- **Comparisons.** Line L3 makes $r - 1$ comparisons for $r \ge 1$, and the loop of line L4 makes at most $n - r$. So the rule makes at most $n - 1$ comparisons, and the time is $\Theta(n)$ in the worst case. If the candidate at position $r + 1$ is hired, the time is $\Theta(r)$.
- **Space.** The rule keeps only $best$ and the index, so the extra space is $\Theta(1)$. It does not store the candidates.
- **Success probability.** For $n \to \infty$, $P_n(\lfloor n/e \rfloor) = 1/e + O(1/n)$. The value $P_n(r^*)$ of the optimal cutoff is more than $1/e$ for each $n \le 100$ and it does not increase with $n$ for $3 \le n \le 100$; $P_{100}(37) = 0.371043$ and $P_{1000}(368) = 0.368196$.
- **Probability of no hire.** The rule hires nobody exactly when the best of all is among the first $r$. This has probability $r/n \to 1/e$.

## Properties

- **Online and irrevocable.** The decision at step $i$ uses only $C[1 \ldots i]$, and a decision is never changed.
- **Rank based.** The rule uses only comparisons, so it works for any total order, and its success probability does not depend on the values.
- **Needs $n$.** The cutoff depends on the number of candidates, so the rule must know $n$ before it starts.
- **Deterministic.** The randomness is in the order of the input, not in the rule. On a fixed adversarial order, for example increasing values with the maximum last, the rule always hires the candidate at position $r + 1$ and fails for $n \ge 3$.

## Variants and improvements

- **Optimal cutoff.** Use $r^*$, the least $r \ge 1$ with $\sum_{j=r+1}^{n-1} 1/j \le 1$. It is the exactly optimal rule for each $n$; see the [secretary problem](/secretary-problem/).
- **Hire the last one.** If no candidate qualifies, hire the last candidate. The probability of hiring the best does not change, because the last candidate is then not the best (the best was among the first $r$).
- **A fixed fraction.** A cutoff of $\lfloor tn \rfloor$ with $t \in (0, 1)$ succeeds with probability tending to $-t \ln t$, which is at least $0.3$ for $t$ between about $0.2$ and $0.6$. The rule is robust to a rough choice of $t$.
- **Full information.** If the values are i.i.d. from a known distribution and the rule sees the values, not only ranks, the optimal rule uses a decreasing sequence of thresholds and succeeds with probability tending to about $0.5802$ (Gilbert and Mosteller 1966).
- **Prophet setting.** If the goal is the expected value, not the probability of the best, and the distributions are known and independent, a single threshold earns half the expected maximum; see the [prophet inequality](/prophet-inequality/).
- **Hiring many.** If the company hires without limit and wants a good rate and good quality, the problem is the [online hiring problem](/online-hiring-problem/) of Broder et al., a different model with different rules.

## When to use it

Use the rule when the items arrive in an order that is random or close to random, when a decision is final, when you know the number of items, and when only the very best counts. If any good item is acceptable, the rule wastes the first 37 percent; a threshold on the value, as in the [prophet inequality](/prophet-inequality/), or the [hire-assistant](/hire-assistant/) scan (when earlier decisions can be changed) fits better. If an adversary sets the order, the rule has no guarantee.

## Pitfalls

- **Comparing with the previous candidate.** Line L5 must compare $C[i]$ with the best of all earlier candidates. A test `C[i] > C[i − 1]` hires a candidate who is only a local improvement, and the success probability drops.
- **Updating before the test.** Code that sets $best \leftarrow \max(best, C[i])$ before the test of line L5 makes the test always false, and it hires nobody. Test first, then stop.
- **Using $\ge$ with ties.** With equal values, `C[i] ≥ best` in line L5 can hire a candidate equal to the first-phase best. The analysis assumes distinct values; break ties at random before the run to keep the success probability.
- **Off by one in the cutoff.** The rule observes $r$ candidates and can hire from position $r + 1$. Code with 0-based indices observes positions $0$ to $r - 1$ and tests from position $r$.
- **Rounding $n/e$.** $\lfloor n/e \rfloor$ is not always the optimal cutoff (it fails for $n = 5, 8, 13, 16, 19, \ldots$). The loss is small, but the exactly optimal rule uses $r^*$.

## Implementations

## History

Ferguson (1989) traces the problem to the late 1950s and to Martin Gardner's column of 1960. Lindley (1961) solved it by dynamic programming, and Dynkin (1963) solved it as an optimal stopping problem for a Markov chain, both with the cutoff rule and the limit $1/e$. Gilbert and Mosteller (1966) computed the optimal cutoffs for each $n$ and studied many variants, among them the full-information version. CLRS presents the rule as the on-line hiring problem of Section 5.4.4.

## References
