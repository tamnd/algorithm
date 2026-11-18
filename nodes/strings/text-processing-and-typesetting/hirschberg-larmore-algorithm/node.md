---
tag: HFGGSH
kind: algorithm
slug: hirschberg-larmore-algorithm
name: Hirschberg-Larmore algorithm
aliases:
- concave least weight subsequence algorithm
area: strings/text-processing-and-typesetting
level: advanced
summary: Solve the least weight subsequence problem with a concave weight in O(n log n) time with a queue of candidates and binary search.
solves: [least-weight-subsequence]
model: word-ram
complexity:
  vars: {n: the last index of the problem (the number of values F(1) to F(n))}
  time: {worst: O(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1987
  people: [Daniel S. Hirschberg, Lawrence L. Larmore]
  note: Hirschberg and Larmore defined the least weight subsequence problem in 1987 and gave an O(n log n) algorithm for concave weights, with line breaking as the main application.
prereqs: [least-weight-subsequence, binary-search, deque]
see_also: [wilber-algorithm, smawk-algorithm, monge-property, row-minima-of-totally-monotone-matrices, convex-hull-trick, divide-and-conquer-optimization, printing-neatly, knuth-plass-line-breaking]
sources:
  - paper: doi:10.1137/0216043
    title: "D. S. Hirschberg and L. L. Larmore, The least weight subsequence problem, SIAM Journal on Computing 16(4), 628-638, 1987"
    locator: "the definition of the problem, the concave condition and the O(n log n) algorithm"
  - paper: doi:10.1016/0196-6774(88)90032-6
    title: "Robert Wilber, The concave least-weight subsequence problem revisited, Journal of Algorithms 9(3), 418-425, 1988"
    locator: "the O(n) algorithm that improves on the O(n log n) bound"
  - paper: doi:10.1016/0020-0190(90)90215-J
    title: "Zvi Galil and Kunsoo Park, A linear-time algorithm for concave one-dimensional dynamic programming, Information Processing Letters 33(6), 309-311, 1990"
    locator: "a simpler O(n) algorithm for the same problem"
---

The Hirschberg-Larmore algorithm solves the [least weight subsequence](/least-weight-subsequence/) problem $F(0) = 0$, $F(j) = \min_{i < j} \bigl( F(i) + w(i, j) \bigr)$ in $O(n \log n)$ time when the weight $w$ is concave, that is, when it satisfies the quadrangle inequality. The plain dynamic program tries every earlier index for every $j$ and takes $\Theta(n^2)$ time. The concave condition gives the earlier indices a simple structure: each one is the best last break for an interval of targets $j$, and the intervals are in the order of the indices. The algorithm keeps these intervals in a [deque](/deque/), reads $F(j)$ from its front, and places each new index at the back with a [binary search](/binary-search/). Daniel Hirschberg and Lawrence Larmore gave it in 1987, with line breaking as the main application. [Wilber's algorithm](/wilber-algorithm/) later reduced the time to $O(n)$.

## In plain words

You compute the best cost $F(j)$ for each position $j$ from left to right. Each earlier position $i$ is a candidate for the last step before $j$.

The concave condition says this: if a later candidate is at least as good as an earlier one at some target, it stays at least as good at every later target. So an old candidate, once beaten, never comes back.

Hence each candidate is the best one for a run of targets, and the runs come in the order of the candidates. Keep a list of the runs. The front of the list gives $F(j)$. A new candidate takes over a final run of targets: remove the runs at the back that it wins completely, and find where its own run starts by binary search.

## The problem

The input is an integer $n \ge 1$ and a weight $w(i, j)$ for $0 \le i < j \le n$, given by a procedure that returns any weight in $O(1)$ time. The weight must satisfy

$$w(i, j) + w(i', j') \le w(i, j') + w(i', j) \qquad \text{for all } 0 \le i \le i' < j \le j' \le n,$$

the condition that Hirschberg and Larmore call concave. The weight $+\infty$ is allowed for a pair that may not be used, such as a line that is too long, if the infinite pairs are closed under lengthening: when $w(i, j) = +\infty$, also $w(i'', j'') = +\infty$ for all $i'' \le i$ and $j'' \ge j$. The output is $F(0), \ldots, F(n)$ and, for each $j \ge 1$, an index $P(j) < j$ that attains the minimum. Following $P$ back from $n$ gives an optimal subsequence.

## The algorithm

Write $g_i(j) = F(i) + w(i, j)$ for the cost of reaching $j$ with $i$ as the last break. The queue $Q$ holds pairs $(c, s)$: the candidate $c$ is the best of all candidates so far for the targets from $s$ up to the start of the next pair.

```pseudo id=main
HIRSCHBERG-LARMORE(n, w)
L1  F[0] ← 0; F[1..n] ← ∞
L2  Q ← a deque that holds the pair (0, 1)
L3  for j ← 1 to n do
L4      while Q has a second pair (c', s') with s' ≤ j do remove the front pair
L5      (c, s) ← the front pair; F[j] ← g_c(j); P[j] ← c; if j = n then stop
L6      while Q is not empty do
            (c, s) ← the back pair; s ← max(s, j + 1)
L7          if g_j(s) ≤ g_c(s) then remove the back pair; continue
L8          binary search for the least t in s + 1 .. n with g_j(t) ≤ g_c(t), or t = n + 1 if there is none
L9          if t ≤ n then append (j, t) at the back
            stop this loop
L10     if Q is empty then append (j, j + 1)
    return F, P
```

Line L4 drops the candidates whose run ended before $j$. Line L5 reads the answer for $j$ from the front, which owns $j$. Lines L6 to L10 add $j$ as a candidate for the targets after $j$. Line L7 removes a back candidate that $j$ already beats at the first target of its run, because then $j$ beats it on the whole run. Line L8 searches in the run of the first back candidate that survives, where the test "$j$ is at least as good" is false and then true, so binary search finds the point where it changes. If $j$ never wins (line L9 with $t = n + 1$), it is not stored at all.

## Example

Take $n = 10$ and $w(i, j) = (j - i - 3)^2$, the check value of the [least weight subsequence](/least-weight-subsequence/) page. The table shows each step: the pairs that line L4 drops at the front, the values set by line L5, the pairs that line L7 removes at the back, and the queue at the end of the step.

| $j$ | front drops | $F(j)$ | $P(j)$ | back removals | queue after the step |
|---|---|---|---|---|---|
| 1 | | 4 | 0 | | (0, 1), (1, 6) |
| 2 | | 1 | 0 | (1, 6) | (0, 1), (2, 5) |
| 3 | | 0 | 0 | (2, 5) | (0, 1), (3, 5) |
| 4 | | 1 | 0 | | (0, 1), (3, 5), (4, 7) |
| 5 | (0, 1) | 1 | 3 | | (3, 5), (4, 7), (5, 8) |
| 6 | | 0 | 3 | (5, 8) | (3, 5), (4, 7), (6, 8) |
| 7 | (3, 5) | 1 | 4 | | (4, 7), (6, 8), (7, 10) |
| 8 | (4, 7) | 1 | 6 | | (6, 8), (7, 10) |
| 9 | | 0 | 6 | | (6, 8), (7, 10) |
| 10 | (6, 8) | 1 | 7 | | (7, 10) |

At step 1 the new candidate 1 loses to 0 at target 2 ($g_1(2) = 4 + 4 = 8$ against $g_0(2) = 1$), and the binary search over $3, \ldots, 10$ finds that it wins from target 6 on ($g_1(6) = 8 \le g_0(6) = 9$, but $g_1(5) = 5 > g_0(5) = 4$). At step 2 the candidate 2 beats 1 at target 6, so line L7 removes $(1, 6)$, and the search against 0 gives the start 5. At steps 8 and 9 the new candidate never wins, so it is not stored. The values $F$ are the ones of the dynamic program, and the back pointers give $10 \to 7 \to 4 \to 0$, the subsequence 0, 4, 7, 10 with weight $1 + 0 + 0 = 1$. The dynamic program, which keeps the first minimizer, gives 0, 3, 6, 10 with the same weight; both are optimal.

## Correctness

The proof rests on one lemma. Let $i < i' < j \le j'$. If $g_{i'}(j) \le g_i(j)$, then $g_{i'}(j') \le g_i(j')$: adding $F(i) + F(i')$ to both sides of the inequality with the four indices $i \le i' < j \le j'$ gives $g_{i'}(j') - g_i(j') \le g_{i'}(j) - g_i(j) \le 0$. The closure of the infinite pairs makes the four values finite whenever $g_i(j')$ is finite. From the lemma, the targets where a new candidate $j$ is at least as good as all earlier candidates form a final interval $\{d, \ldots, n\}$ or the empty set.

The invariant is that at the start of step $j$, the queue lists the candidates in increasing order with increasing starts, the front start is at most $j$, and for every target $j' \ge j$, the candidate of the last pair whose start is at most $j'$ attains $\min_{i < j} g_i(j')$. Line L4 keeps this and makes the front own $j$, so line L5 sets $F[j] = F(j)$. Lines L6 to L10 cut the old runs at $d$ and append $(j, d)$: a removed back candidate has all its targets in the final interval, and the binary search is on a monotone test, so it returns $d$. So the invariant holds for $j + 1$. The full proof is in the proof file.

## Complexity

Each candidate enters the queue at most once and leaves at most once, so lines L4 and L7 remove fewer than $2n$ pairs in all. Each step evaluates $w$ once in line L5, twice for each removed pair, twice at line L7 for the pair that survives, and twice for each step of a binary search over at most $n$ targets. So the number of evaluations is at most about $2 n \log_2 n + 5 n$, and the time is $O(n \log n)$. The space is $\Theta(n)$ for $F$, $P$ and the queue.

Measured with the kind of weights that the tests of this page use, random concave weights of the form $f(S_j - S_i - l) + a(i) + b(j)$ for a convex $f$, the program makes about $19.4 n$ evaluations for $n = 500$, $23.5 n$ for $n = 2000$, $27.4 n$ for $n = 8000$ and $31.3 n$ for $n = 32000$: the count per index grows by about 4 each time $n$ grows by a factor of 4, as $2 \log_2 n$ predicts. On $w(i, j) = (j - i - 3)^2$ with $n = 1000$ it makes 21588 evaluations, while the dynamic program makes $n(n+1)/2 = 500500$.

## Properties

- **Values in order.** It finds $F(1), F(2), \ldots$ in this order, and $F(j)$ is final at step $j$.
- **Not online in the weights.** At step $j$ it reads $w(j, t)$ for targets $t$ up to $n$, so all weights must be known in advance. For line breaking with prefix sums this is no problem.
- **Exact.** It uses only comparisons and additions of values of $F$ and $w$, so with exact numbers, such as integers or fractions, the values are exact.
- **Ties.** The test $\le$ at lines L7 and L8 lets a later candidate win a tie. The value $F(j)$ is the same, but the back pointers can give another optimal subsequence than the dynamic program, as in the example.

## Variants and improvements

- **Linear time.** [Wilber's algorithm](/wilber-algorithm/) uses the matrix searching of [SMAWK](/smawk-algorithm/) on blocks of targets and takes $O(n)$ time. Galil and Park gave a simpler $O(n)$ method in 1990.
- **The reverse inequality.** If $w$ satisfies the inequality with $\ge$, a later candidate that wins can lose again later, the runs are no longer in the order of the candidates, and the queue method fails. Other methods are needed, and the best known ones take almost linear time (see the [least weight subsequence](/least-weight-subsequence/) page).
- **Linear cost per candidate.** If $g_i(j)$ is a linear function of a value of $j$ for each fixed $i$, the [convex hull trick](/convex-hull-trick/) finds the minima with a hull of lines. The queue of runs is the same idea for any weight with the quadrangle inequality.
- **Layers.** For a fixed number of parts, each layer of the dynamic program is a matrix whose row minima can be found by the [divide and conquer optimization](/divide-and-conquer-optimization/) in $O(n \log n)$ per layer, or by SMAWK in $O(n)$.
- **Free last line.** When the last line of a paragraph costs nothing, the weight to $n$ breaks the inequality. Run the algorithm up to $n - 1$ with the concave weight, then take $F(n) = \min_i \bigl( F(i) + w(i, n) \bigr)$ in one more pass.

## When to use it

Use it for a dynamic program of the form $F(j) = \min_{i < j} F(i) + w(i, j)$ whose weight satisfies the quadrangle inequality, such as line breaking with rigid spaces and a convex cost of the slack, as in [printing neatly](/printing-neatly/), or splitting a sequence into blocks with a convex cost of the block size. It is short and simple, and its $\log n$ factor is small in practice. For the strict $O(n)$ bound use Wilber's algorithm, which is more complex. For the demerits of [Knuth-Plass line breaking](/knuth-plass-line-breaking/), which depend on more than the two ends of a line, it does not apply directly.

## Pitfalls

- **Check the inequality.** The method gives wrong answers, with no error, for a weight that is not concave. The test `test_not_concave_can_fail` shows a weight that is small only for jumps of length 1 and 4, where the program differs from the dynamic program. The capped badness of TeX is not concave either.
- **Concave or convex.** Papers use both words for the same inequality. Check the inequality itself, not the name.
- **Infinite weights in a hole.** An infinite weight is safe only when the infinite pairs are closed under lengthening, as for lines that are too long. A single forbidden pair inside a region of finite weights can break the monotone test of the binary search.
- **The range of the search.** The search must start after $\max(s, j + 1)$, because targets at or before $j$ are already done. The program also must not append a pair whose start is beyond $n$.

## Implementations

## History

Hirschberg and Larmore defined the least weight subsequence problem in a paper in SIAM Journal on Computing in 1987, named the concave condition, and gave the $O(n \log n)$ algorithm, with the breaking of paragraphs into lines as the main application. Wilber reduced the time to $O(n)$ in 1988 by applying the matrix searching of Aggarwal, Klawe, Moran, Shor and Wilber, and Galil and Park gave a simpler linear method in 1990.

## References
