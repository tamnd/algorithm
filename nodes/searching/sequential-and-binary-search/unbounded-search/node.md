---
tag: 9145YV
kind: problem
slug: unbounded-search
name: Search in an unbounded sorted array
aliases:
- unbounded binary search
area: searching/sequential-and-binary-search
level: core
summary: Find a key in a sorted sequence whose length is not known in advance.
model: comparison-model
complexity:
  vars: {N: "the answer, the first index whose item is at least the key"}
  time: {worst: Θ(log N)}
prereqs: [search-in-sorted-array, binary-search]
see_also: [exponential-search, binary-search-on-answer, elias-gamma-coding, elias-delta-coding, elias-omega-coding, kraft-inequality, iterated-logarithm, decision-tree-model]
sources:
  - paper: doi:10.1016/0020-0190(76)90071-5
    title: Jon Louis Bentley and Andrew Chi-Chih Yao, An almost optimal algorithm for unbounded searching, Information Processing Letters 5(3) (1976)
    locator: pp. 82 to 87 (the problem, algorithms B0, B1, B2 and Bk, and the lower bound)
  - paper: doi:10.1109/TIT.1975.1055349
    title: Peter Elias, Universal codeword sets and representations of the integers, IEEE Transactions on Information Theory 21(2) (1975)
    locator: pp. 194 to 203 (the gamma, delta and omega codes)
---

Unbounded search asks for the position of a key in a sorted sequence that has no known end: the sequence $A[0], A[1], A[2], \ldots$ can be read at any index, but its length is unknown or infinite. In the cleanest form, a test $P(i)$ on the integers $0, 1, 2, \ldots$ is false up to an unknown index $N$ and true from $N$ on, and the task is to find $N$. The cost is counted as a function of $N$. A scan costs $N + 1$ tests. [Exponential search](/exponential-search/) costs $2\lfloor \lg N \rfloor + 2$, and Bentley and Yao showed in 1976 how to get down to $\lg N + \lg \lg N + \cdots$, close to the best possible. The problem is the same as the design of a prefix code for the integers, such as the [Elias codes](/elias-gamma-coding/).

## In plain words

A long road has houses with sorted numbers, and you do not know where the road ends. You want the first house whose number is at least the one you are looking for. You cannot jump to the middle, because there is no known middle.

So you first look for an end. You look at house 1, then 2, then 4, then 8, and you double each time, until you pass your number. Now you have a stretch of road with both ends known, and you halve it as in a normal binary search. Both steps take about as many looks as the number of digits of the answer in base 2. A smarter plan first finds that number of digits in the same way, and then saves about half of the looks.

## Definition

**Input.** A test $P$ on the integers $i \ge 0$ that is monotone: there is an integer $N \ge 0$ with $P(i)$ false for $i < N$ and true for $i \ge N$. The test can be asked at any $i$, at a cost of 1. The value of $N$ is not given, and there is no upper bound on it.

**Output.** The value $N$.

**The sorted-array form.** For a sorted sequence $A[0] \le A[1] \le \cdots$ with no known end and a key $x$, take $P(i) = (A[i] \ge x)$. Then $N$ is the [lower bound](/lower-bound-query/) of $x$, and $x$ is present when $A[N] = x$. If the sequence is finite but its length is unknown, a read past the end returns $+\infty$, so that $P$ is true there.

**The cost.** A deterministic algorithm is a rule that picks each next index from the answers so far. Its cost $c(N)$ is the number of tests it makes when the answer is $N$. Since $N$ has no bound, the goal is a function $c(N)$ that is small for every $N$, not one worst-case number.

## Variants

- **Bounded search.** When an upper bound $n \ge N$ is known, binary search on $[0, n]$ makes $\lceil \lg(n + 1) \rceil$ tests, which depends on $n$, not on $N$. The unbounded algorithms are better when $N \ll n$.
- **Search from a finger.** The sequence is unbounded on one or both sides of a known index $f$, and the answer is $f + d$ for an unknown distance $d$. The cost is then a function of $d$; see the finger variant of [exponential search](/exponential-search/).
- **Search on the answer.** $P(t)$ is "a solution of size $t$ exists", for a monotone feasibility question with no known upper bound on the answer: the smallest feasible capacity, time or length. See [binary search on the answer](/binary-search-on-answer/).
- **Real numbers.** Find the place where a monotone function on $[0, \infty)$ changes sign, to a given precision. Doubling first finds a bracket, then bisection halves it.
- **Noisy tests.** Each answer of $P$ is wrong with some probability. The doubling and halving phases must then repeat or weight their tests.

## Examples

**One search.** For $N = 10$, the doubling search tests $P(0), P(1), P(3), P(7)$, which are false, and $P(15)$, which is true. So $8 \le N \le 15$, and a binary search on the 7 positions $8, \ldots, 14$ (with $15$ known to be true) makes 3 more tests, here $P(11)$, $P(9)$ and $P(10)$. That is 8 tests: $2\lfloor \lg 10 \rfloor + 2$.

**Costs of three algorithms.** The table gives the exact number of tests, computed by running each algorithm. B0 is the scan, B1 the doubling search, and B2 the doubling search on the exponent, as in the next section:

| $N$ | 1 | 10 | 100 | 1000 | $10^6$ | $10^9$ |
|---|---|---|---|---|---|---|
| B0, scan, $N + 1$ | 2 | 11 | 101 | 1001 | $10^6 + 1$ | $10^9 + 1$ |
| B1, doubling, $2\lfloor \lg N \rfloor + 2$ | 2 | 8 | 14 | 20 | 40 | 60 |
| B2, $k + 2\lfloor \lg k \rfloor + 1$ with $k = \lceil \lg(N+1) \rceil$ | 2 | 9 | 12 | 17 | 29 | 39 |
| bounded binary search, $\lceil \lg(N + 1) \rceil$ if $N$ were the bound | 1 | 4 | 7 | 10 | 20 | 30 |

For small $N$ the doubling search is as good as B2 or better; for large $N$, B2 saves about half of the tests.

## Known algorithms

Let $k = \lceil \lg(N + 1) \rceil$, the number of bits of $N$. Then $k$ is the smallest $j \ge 0$ with $P(2^j - 1)$ true.

- **B0, the scan.** Test $P(0), P(1), \ldots$ until one is true: $N + 1$ tests.
- **B1, [exponential search](/exponential-search/).** Test $P(2^j - 1)$ for $j = 0, 1, 2, \ldots$ until one is true. This finds $k$ with $k + 1$ tests and shows $2^{k-1} \le N \le 2^k - 1$. A binary search on the $2^{k-1} - 1$ open positions then makes $k - 1$ tests. For $N \ge 1$ the total is $2k = 2\lfloor \lg N \rfloor + 2$.
- **B2, doubling on the exponent.** Find $k$ itself by B1, with the test $Q(j) = P(2^j - 1)$, which is false for $j < k$ and true from $k$ on. This costs $2\lfloor \lg k \rfloor + 2$ tests for $k \ge 1$. Then the binary search costs $k - 1$, so the total is $k + 2\lfloor \lg k \rfloor + 1 = \lg N + 2\lg \lg N + O(1)$.
- **Bk and the limit.** Apply the same step again: find $\lfloor \lg k \rfloor$ by a doubling search, then $k$, then $N$. With $j$ levels the cost is $\lg N + \lg \lg N + \cdots + \lg^{(j-1)} N + 2\lg^{(j)} N + O(j)$. Bentley and Yao also give an algorithm that picks the number of levels from the answers, with cost $\lg N + \lg \lg N + \cdots + O(\lg^* N)$, where the sum runs over the [iterated logarithms](/iterated-logarithm/) that are at least 1.

All of these use $O(1)$ extra space and only the monotone test.

## Bounds

**Upper bound.** $2\lfloor \lg N \rfloor + 2$ tests by B1 and $\lg N + 2\lg \lg N + O(1)$ by B2, so $\Theta(\log N)$.

**A simple lower bound.** For each $n$, some answer $N \le n$ costs at least $\lceil \lg(n + 1) \rceil$ tests, because on the answers $0, \ldots, n$ the algorithm solves the bounded problem, whose decision tree needs $n + 1$ leaves. The unbounded problem costs more than this, by a term that grows with $N$.

**Theorem.** No deterministic algorithm has $c(N) < \lg N + \lg \lg N$ for all large $N$.

*Proof.* Fix an algorithm. Its run on each answer $N$ is a finite path in a binary [decision tree](/decision-tree-model/): each test goes left on false and right on true, and different answers end at different leaves, since the algorithm must output different values. Write the path to the leaf of $N$ as a binary word $w_N$ of length $c(N)$. No word is a prefix of another, since they end at different leaves of one tree. By the [Kraft inequality](/kraft-inequality/), every finite set of these words has $\sum 2^{-c(N)} \le 1$, so the infinite sum is at most 1 too. Now assume that $c(N) < \lg N + \lg \lg N$ for all $N \ge N_0 \ge 2$. Then $2^{-c(N)} > 1/(N \lg N)$, and

$$ \sum_{N \ge N_0} 2^{-c(N)} > \sum_{N \ge N_0} \frac{1}{N \lg N} = \infty, $$

since the series $\sum 1/(N \ln N)$ diverges by the integral test. This is a contradiction. $\blacksquare$

The same argument with the divergent series $\sum 1/(N \lg N \lg \lg N \cdots)$ shows that the sum of iterated logarithms in the cost of the Bentley and Yao algorithm cannot be cut much further. They prove a lower bound of this form and show that their best algorithm is within lower-order terms of it.

## Reductions

- **Unbounded search is the same as a prefix code for the integers.** A search algorithm gives the code $w_N$ of the proof, and a prefix code $w$ gives an algorithm that reads the bits of the unknown code word with tests, when the code is monotone in the order of the integers. Under this match, B1 corresponds to the [Elias gamma code](/elias-gamma-coding/), B2 to the [Elias delta code](/elias-delta-coding/), and the many-level algorithm to the [Elias omega code](/elias-omega-coding/).
- **Bounded search reduces to it.** Run an unbounded algorithm and treat each $i \ge n$ as true. The cost is a function of the answer, so it can beat $\lceil \lg(n + 1) \rceil$ when the answer is small.
- **[Search in a sorted array](/search-in-sorted-array/) of unknown length reduces to it** with $P(i) = (A[i] \ge x)$, and one more equality test.

## Applications

- Search a sorted list that arrives as a stream, or is stored in a structure that does not report its length, such as a sorted linked file read in blocks.
- Find the smallest $t$ with a monotone property when no upper bound is known: the smallest precision that makes a numerical result stable, the shortest timeout that lets a job finish, the size of a table that holds the data.
- Merge two sorted runs of very different lengths: the place of each item of the short run in the long run is found by an unbounded search from the last place, which is the galloping step of [Timsort](/timsort/).
- Encode integers of unknown size with few bits, by the matching prefix codes.

## References
