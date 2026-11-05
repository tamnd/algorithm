---
tag: FM952M
kind: algorithm
slug: fibonacci-search-unimodal
name: Fibonacci search
aliases:
- Fibonacci minimum search
- Fibonacci search technique
area: searching/search-on-answers
level: intro
summary: Unimodal search that shrinks the interval by Fibonacci-number ratios, reusing evaluations exactly.
solves: [unimodal-optimization]
model: query-model
complexity:
  vars: {n: the number of integer points}
  time: {worst: Θ(log n), average: Θ(log n), best: Θ(log n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1953
  people: [Jack Kiefer]
  note: Kiefer proved in 1953 that the Fibonacci placement of evaluations is the minimax optimal search for the maximum of a unimodal function.
prereqs: [unimodal-function, fibonacci-numbers, ternary-search]
see_also: [unimodal-optimization, golden-section-search, ternary-search, fibonacci-search, unimodal-maximum, peak-finding, bitonic-sequence]
sources:
  - paper: doi:10.1090/S0002-9939-1953-0055639-3
    title: "J. Kiefer, Sequential minimax search for a maximum, Proceedings of the American Mathematical Society 4(3) (1953), 502-506"
    locator: the minimax theorem for N evaluations and the Fibonacci strategy
  - book: isbn:9780521880688
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 10.2, Golden Section Search in One Dimension (the relation to the Fibonacci method)
---

Fibonacci search finds the maximum of a strictly [unimodal function](/unimodal-function/) on $n$ integer points with the least number of evaluations that any method can guarantee: the smallest $N$ with $n \le F_{N+2} - 1$, where $F_k$ are the [Fibonacci numbers](/fibonacci-numbers/). It keeps a bracket whose two parts around the best point are consecutive Fibonacci numbers, and evaluates one new point in the larger part, at a Fibonacci distance from the best point, so that both outcomes leave a bracket of the same shape one size smaller. Kiefer proved this optimal in 1953, and its ratios tend to the golden ratio, which gives [golden-section search](/golden-section-search/). It is a different method from the [Fibonacci search](/fibonacci-search/) for a key in a sorted array, which uses the same numbers to split the array.

## In plain words

A hill goes up and then down along a row of numbered places, and each look at a height costs money. You keep a stretch of places where the top must be, and the highest place seen so far inside it. You look at one new place on the longer side of that best place. If the new place is higher, the top is on its side; if it is lower, the top is on the other side. Either way, one end moves in.

The trick is the size of the two sides. If they are always two neighbouring numbers of the sequence 1, 1, 2, 3, 5, 8, 13 (each number is the sum of the two before it), then after each look they are again neighbours, one step down. When both sides are 1, the best place is the top. No other method needs fewer looks.

## The problem

The input is $n \ge 1$ and an oracle for a function $f$ on $\{1, \ldots, n\}$ that is **strictly unimodal for a maximum**: there is a mode $m$ with $f(1) < \cdots < f(m)$ and $f(m) > \cdots > f(n)$. The output is $m$. The cost is the number of evaluations of $f$, as in the [query model](/query-model/). For a minimum, reverse the comparison. This is the discrete form of [unimodal optimization](/unimodal-optimization/).

The method uses the comparison lemma: for $x_1 < x_2$, $f(x_1) < f(x_2)$ implies $m > x_1$, $f(x_1) > f(x_2)$ implies $m < x_2$, and $f(x_1) = f(x_2)$ implies $x_1 < m < x_2$.

## The algorithm

The state is an open bracket $(lo, hi)$ that holds $m$, a best point $p$ in it with its value $fp$, and the number $k$ of evaluations left. The two parts $p - lo$ and $hi - p$ are always $F_{k+1}$ and $F_{k+2}$. Indices above $n$ are padding: they count as smaller than every value of $f$ and are never evaluated.

```pseudo id=main
FIB-MAX(f, n)                              ▷ f strictly unimodal for a maximum on 1..n
L1  compute F_0, F_1, …, F_{N+2}, with N the smallest number such that F_{N+2} ≥ n + 1
L2  lo ← 0;  hi ← F_{N+2}                    ▷ the mode is in the open interval (lo, hi)
L3  p ← F_N;  fp ← f(p)
L4  k ← N − 1                                ▷ evaluations left; the parts are F_{k+1}, F_{k+2}
L5  while k > 0 do
L6      if p − lo > hi − p then q ← p − F_k else q ← p + F_k      ▷ in the larger part
L7      if q ≤ n then fq ← f(q) else fq ← −∞                   ▷ padding
L8      if fq > fp then (if q > p then lo ← p else hi ← p);  p ← q;  fp ← fq
L9      else (if q > p then hi ← q else lo ← q)
L10     k ← k − 1
L11 return p
```

**Why the parts stay Fibonacci.** Say the right part is the larger, $hi - p = F_{k+2}$, so $q = p + F_k$. If $q$ wins, the new bracket is $(p, hi)$ around $q$, with parts $F_k$ and $F_{k+2} - F_k = F_{k+1}$. If $q$ loses, the new bracket is $(lo, q)$ around $p$, with parts $F_{k+1}$ and $F_k$. Both outcomes give the parts $\{F_k, F_{k+1}\}$, so the worst case is the same as every case.

## Example

Take the 12 values $f = (2, 5, 9, 14, 20, 23, 21, 18, 11, 8, 4, 1)$ at the indices $1$ to $12$, with the mode $6$. Since $F_7 = 13 \ge 13$ and $F_6 = 8 < 13$, the budget is $N = 5$. The search starts with the bracket $(0, 13)$ and evaluates $p = F_5 = 5$, with $f(5) = 20$.

| k | bracket | p | parts | q | f(q) | outcome |
|---|---|---|---|---|---|---|
| 4 | (0, 13) | 5 | 5, 8 | 5 + 3 = 8 | 18 | loses, bracket (0, 8) |
| 3 | (0, 8) | 5 | 5, 3 | 5 − 2 = 3 | 9 | loses, bracket (3, 8) |
| 2 | (3, 8) | 5 | 2, 3 | 5 + 1 = 6 | 23 | wins, bracket (5, 8), p = 6 |
| 1 | (5, 8) | 6 | 1, 2 | 6 + 1 = 7 | 21 | loses, bracket (5, 7) |

The bracket $(5, 7)$ holds only the index $6$, which is returned after 5 evaluations, at $5, 8, 3, 6, 7$. [Ternary search](/ternary-search/) needs 10 evaluations on the same values.

**Padding.** For $n = 10$ and the increasing values $f(i) = i$, the budget is again $N = 5$ and the bracket starts as $(0, 13)$. The points $5$, $8$ and $10$ win in turn, then $q = 11 > n$ loses without an evaluation, and $q = 9$ loses. The bracket $(9, 11)$ leaves $10$, after 4 evaluations.

## Correctness

The invariant at line L5 has four parts: $lo < m < hi$; the parts around $p$ are $F_{k+1}$ and $F_{k+2}$; $p \le n$ and $fp = f(p)$; and at most $N - k$ evaluations were made. In a step, $q$ lies strictly inside the larger part because $1 \le F_k < F_{k+2}$. If $q$ wins, the comparison lemma gives $m$ on the side of $p$ that holds $q$; if $q$ loses, or ties, it gives $m$ on the side of $q$ that holds $p$. Padded indices are consistent with a strictly unimodal extension of $f$ with the same mode. When $k = 0$ both parts are $1$, so $p$ is the only index left in the open bracket and equals $m$. The full proof is below.

## Complexity

- **Evaluations.** At most $N$, where $N$ is the smallest number with $n \le F_{N+2} - 1$; exactly $N$ when $n = F_{N+2} - 1$. Since $F_{N+2} \approx \varphi^{N+2}/\sqrt5$ with $\varphi = (1 + \sqrt5)/2$, this is $N \approx \log_\varphi n - 0.33 \approx 1.44 \lg n$. For $n = 10, 100, 1000, 10^6$ the budget is $5, 10, 15, 29$.
- **Optimality.** No method can guarantee the mode on $n$ points with fewer evaluations; the theorem and its adversary proof are on the page [unimodal optimization](/unimodal-optimization/).
- **Time and space.** $O(N)$ time to compute the Fibonacci numbers, $O(1)$ work per step, and $O(1)$ extra space if $F_k$ is updated by $F_{k} = F_{k+2} - F_{k+1}$ instead of stored.

## Properties

- **Optimal in the worst case.** Both outcomes of each comparison leave the same amount of work, which is the condition that an adversary cannot exploit.
- **Needs the budget in advance.** The first point depends on $N$, so the method must know $n$, or for real intervals the number of evaluations, before it starts.
- **Comparisons only.** Only the order of values is used.
- **Exact reuse on integers.** The best point is always reused, and all evaluated points are distinct integers.

## Variants and improvements

- **Real intervals.** On $[a, b]$ with $N$ evaluations, place the first two points at the fractions $F_{N-1}/F_{N+1}$ and $F_N/F_{N+1}$, and keep the same rule. Each step shrinks the interval by $F_{k+1}/F_{k+2}$. At the last evaluation the interval has length $2(b - a)/F_{N+1}$ and the two inner points would coincide at its middle. Shifting the last point by a small $\delta$ gives a final interval of length $(b - a)/F_{N+1} + \delta$, the optimum of Kiefer's theorem.
- **Golden-section search.** The ratio $F_{k+1}/F_{k+2}$ tends to $1/\varphi$. Using the limit at every step gives [golden-section search](/golden-section-search/), which does not need $N$ in advance and loses only a factor $\varphi^2/\sqrt5 \approx 1.17$ in the final length.
- **A minimum.** Reverse the comparisons of lines L7 and L8 (padding is then $+\infty$).
- **Binary search on the slope.** A [binary search](/binary-search/) for the first $i$ with $f(i) > f(i + 1)$ uses $2\lceil \lg n \rceil$ evaluations, about $1.39$ times as many, but is simpler; on an array it is the [unimodal maximum](/unimodal-maximum/) search.
- **Fibonacci search in a sorted array.** Kiefer's numbers also give a search for a key in a sorted array that splits at Fibonacci positions with only additions and subtractions. That is a separate algorithm: [Fibonacci search](/fibonacci-search/).

## When to use it

Use Fibonacci search when each evaluation is expensive, the domain is a set of integers or the number of evaluations is fixed, and the function is strictly unimodal: tuning an integer parameter by running an experiment, or finding the peak of a [bitonic sequence](/bitonic-sequence/) stored on a slow device. When the number of evaluations is not known in advance, or the domain is real and a tolerance is the goal, use golden-section search. When evaluations are cheap, ternary search or the binary search on the slope is simpler.

## Pitfalls

- **Plateaus.** The method needs strict unimodality. If equal values occur away from the mode, a tie can send the bracket to the wrong side, as for every comparison method; see [peak finding](/peak-finding/) for the weaker goal of finding a local maximum.
- **Off-by-one in the budget.** The condition is $n \le F_{N+2} - 1$, with an open bracket $(0, F_{N+2})$. Starting with a closed bracket $[1, F_{N+2}]$ or with $p = F_{N+1}$ breaks the Fibonacci shape of the parts.
- **Evaluating the padding.** Calling $f$ above $n$ reads outside the array. Treat these indices as losing without a call, as in line L7.
- **Choosing the smaller part.** If $q$ is put in the smaller part, the losing outcome leaves parts that are not Fibonacci numbers and the bound fails.

## Implementations

## History

Jack Kiefer posed and solved the minimax problem of locating the maximum of a unimodal function with a fixed number of evaluations in 1953. He showed that the Fibonacci placement is optimal and that the best final interval is $1/F_{N+1}$ of the initial one, up to an arbitrarily small $\delta$. The method entered numerical analysis and operations research textbooks under the name Fibonacci search, and the golden-section search was adopted as its version without a fixed budget.

## References
