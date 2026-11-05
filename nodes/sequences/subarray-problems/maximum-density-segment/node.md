---
tag: W9HT0X
kind: problem
slug: maximum-density-segment
name: Maximum density segment
aliases:
- maximum average segment with minimum length
area: sequences/subarray-problems
level: advanced
summary: Find the contiguous segment of at least a given length with the largest average, with values as weights.
prereqs: [subarray, prefix-sums, maximum-sum-subarray-of-fixed-length]
see_also: [monotonic-deque-prefix-sums, fractional-programming, dinkelbach-algorithm, binary-search-on-real-numbers, convex-hull, shortest-subarray-sum-at-least-k, maximum-subarray-problem, parametric-search]
sources:
  - paper: doi:10.1093/bioinformatics/10.3.219
    title: "Xiaoqiu Huang, An algorithm for identifying regions of a DNA sequence that satisfy a content requirement, Bioinformatics 10(3) (1994), 219-225"
    locator: the problem with a minimum length, motivated by GC-rich regions, and the bound of less than 2L on the length of an optimal segment
  - paper: doi:10.1016/s0022-0000(02)00010-7
    title: "Yaw-Ling Lin, Tao Jiang and Kun-Mao Chao, Efficient algorithms for locating the length-constrained heaviest segments with applications to biomolecular sequence analysis, Journal of Computer and System Sciences 65(3) (2002), 570-586"
    locator: the O(n log L) algorithm for the maximum average segment of length at least L
  - paper: doi:10.1016/s0020-0190(03)00225-4
    title: "Sung Kwon Kim, Linear-time algorithm for finding a maximum-density segment of a sequence, Information Processing Letters 86(6) (2003), 339-342"
    locator: the linear-time algorithm with a lower bound on the length, by slopes of prefix-sum points
  - paper: doi:10.1016/j.jcss.2004.08.001
    title: "Michael H. Goldwasser, Ming-Yang Kao and Hsueh-I Lu, Linear-time algorithms for computing maximum-density sequence segments with bioinformatics applications, Journal of Computer and System Sciences 70(2) (2005), 128-144"
    locator: linear time with both a lower and an upper bound on the length
  - paper: doi:10.1137/s0097539704440430
    title: "Kai-Min Chung and Hsueh-I Lu, An Optimal Algorithm for the Maximum-Density Segment Problem, SIAM Journal on Computing 34(2) (2005), 373-387"
    locator: the optimal O(n) algorithm with widths and both length bounds, which also works online
  - url: https://leetcode.com/problems/maximum-average-subarray-ii/
    title: LeetCode, problem 644, Maximum Average Subarray II
    locator: problem statement and example (length at least k)
---

The maximum density segment problem gives a sequence of numbers and a minimum length $L$, and asks for the contiguous segment of length at least $L$ with the largest average. In the weighted form each item has a value $a_i$ and a width $w_i > 0$, and the density of a segment is the sum of its values over the sum of its widths. Without the bound $L$ the answer is just the largest item, so the bound is what makes the problem interesting. With [prefix sums](/prefix-sums/), the density of a segment is the slope between two points $(W_i, P_i)$ and $(W_j, P_j)$, so the problem is a largest slope between two points that are far enough apart. Linear-time algorithms exist (Kim 2003; Goldwasser, Kao and Lu 2005; Chung and Lu 2005), and a simpler binary search on the average reduces it to a [maximum sum](/maximum-subarray-problem/) test.

## In plain words

You have a long string of letters from a DNA sample, and you want the stretch with the highest share of the letters G and C. A stretch of one letter is not useful, since any single G gives a share of 100 percent. So you ask for the best stretch that is at least some length long.

In general, you have a row of numbers, and you want a run of at least a given length whose average is as high as possible.

An average is not a sum, so the usual methods for the best sum do not apply directly. But you can ask an easier question: is there a run of the given length with an average of at least some value? Subtract that value from every number, and ask if some run has a total of at least zero. Guess the value by halving.

## Definition

**Input.** An array $A[0..n-1]$ of numbers, widths $w_0, \dots, w_{n-1} > 0$ (all $1$ in the plain form), and a bound $L$ with $1 \le L \le n$. In the plain form $L$ bounds the number of items; in the weighted form it can bound the total width.

**Output.** A pair $0 \le i < j \le n$ with $j - i \ge L$ that maximizes the density
$$d(i, j) = \frac{A[i] + \dots + A[j-1]}{w_i + \dots + w_{j-1}},$$
and the value $d^* = d(i, j)$.

**Slopes.** Let $P_t = A[0] + \dots + A[t-1]$ and $W_t = w_0 + \dots + w_{t-1}$. Then $d(i, j) = (P_j - P_i)/(W_j - W_i)$, the slope of the line through the points $(W_i, P_i)$ and $(W_j, P_j)$. For a fixed $j$, the best start is a point of contact of a tangent from $(W_j, P_j)$ to the lower [convex hull](/convex-hull/) of the points with $i \le j - L$.

**Short optimal segments.** In the plain form, some optimal segment has length less than $2L$ (Huang, 1994). A segment of length at least $2L$ splits into two segments of length at least $L$, and one of the two has an average at least that of the whole.

## Variants

- **Fixed length.** All segments of length exactly $L$ have the same denominator, so the problem is the [maximum sum subarray of fixed length](/maximum-sum-subarray-of-fixed-length/), solved by a sliding window.
- **Upper bound.** Lengths between $L$ and $U$. Goldwasser, Kao and Lu (2005) and Chung and Lu (2005) solve this in linear time.
- **Widths.** Items of different widths, such as runs of a sequence compressed to (value, length) pairs. Chung and Lu (2005) handle widths with both bounds in $O(n)$ time.
- **Minimum density.** Negate the values.
- **Binary values.** The share of the items with a given property, such as the GC content of a DNA sequence, with $a_i \in \{0, 1\}$.
- **Density at least a threshold.** For a given $\lambda$, the longest or shortest segment with density at least $\lambda$ becomes, after subtracting $\lambda w_i$ from each item, a problem on segments with sum at least $0$, as in the [shortest subarray with sum at least K](/shortest-subarray-sum-at-least-k/).
- **Two dimensions.** The densest rectangle of a matrix with a lower bound on its area.

## Examples

**LeetCode 644.** $A = [1, 12, -5, -6, 50, 3]$ and $L = 4$. The segments of length $4$ have averages $2/4 = 0.5$, $51/4 = 12.75$ and $42/4 = 10.5$. The two of length $5$ have $52/5 = 10.4$ and $54/5 = 10.8$, and the whole array has $55/6 \approx 9.17$. The answer is $12.75$, from $[12, -5, -6, 50]$. Its length $4$ is less than $2L = 8$, as the bound on short optimal segments says.

**A longer segment wins.** $A = [1, 3, 1, 3, 1]$ and $L = 2$. Every segment of length $2$ has average $2$. The segment $[3, 1, 3]$ of length $3$ has average $7/3$, and it is the answer. So the shortest allowed length is not always best, and the problem is not the fixed-length one.

**The test by subtraction.** For $A = [1, 12, -5, -6, 50, 3]$, $L = 4$ and $\lambda = 12$, the shifted items are $[-11, 0, -17, -18, 38, -9]$. The segment $[0, -17, -18, 38]$ has sum $3 \ge 0$, so $d^* \ge 12$. For $\lambda = 13$ the shifted items are $[-12, -1, -18, -19, 37, -10]$, and the best segment of length at least $4$ has sum $-1 < 0$, so $d^* < 13$.

## Known algorithms

| method | time | notes |
|---|---|---|
| all pairs | $\Theta(n^2)$ | every segment, with prefix sums |
| Huang (1994) | $O(nL)$ | only lengths below $2L$ |
| binary search on $\lambda$ | $O(n \log(R/\varepsilon))$ | test with a prefix minimum; $R$ is the range of the values, $\varepsilon$ the precision |
| [Dinkelbach's algorithm](/dinkelbach-algorithm/) | $O(n)$ per round | exact, with a small number of rounds in practice |
| Lin, Jiang and Chao (2002) | $O(n \log L)$ | plain form with a lower bound |
| Kim (2003) | $O(n)$ | lower bound, by tangents to the convex hull of prefix points |
| Goldwasser, Kao and Lu (2005) | $O(n)$ | lower and upper bounds |
| Chung and Lu (2005) | $O(n)$ | widths, both bounds, online |

The test for a fixed $\lambda$ works on $b_i = a_i - \lambda w_i$ with prefix sums $Q_t$. Some segment of length at least $L$ has density at least $\lambda$ exactly when $\max_{j \ge L} (Q_j - \min_{i \le j - L} Q_i) \ge 0$, and the inner minimum is a running minimum, so the test takes $O(n)$ time. This is the parametric method of [fractional programming](/fractional-programming/), and the binary search is a [binary search on real numbers](/binary-search-on-real-numbers/).

## Bounds

**Linear time is optimal.** Each item can change the answer, so $\Omega(n)$ time is needed. Kim, Goldwasser, Kao and Lu, and Chung and Lu meet it, and Chung and Lu also handle widths and an upper bound.

**Exact answers.** The binary search gives $d^*$ to a precision $\varepsilon$, and the segment it reports has density within $\varepsilon$ of $d^*$. With integer values and unit widths, two distinct densities with denominators at most $n$ differ by at least $1/n^2$, so a precision below $1/n^2$ identifies $d^*$ exactly, in $O(n \log(nR))$ time.

## Reductions

- **To a sign test on sums.** $d^* \ge \lambda$ exactly when some segment of length at least $L$ has $\sum (a_i - \lambda w_i) \ge 0$. The left side is monotone in $\lambda$, so the largest such $\lambda$ is $d^*$.
- **To slopes.** The problem is the largest slope between two points of the polyline $(W_t, P_t)$ with horizontal gap at least $L$, solved by tangents to a lower convex hull, as in the [convex hull trick](/convex-hull-trick/).
- **From the maximum sum.** For a fixed length the problem becomes a sum problem, and the test step uses a maximum sum with a length bound, as in the [monotonic deque over prefix sums](/monotonic-deque-prefix-sums/).

## Applications

- **DNA sequence analysis.** Regions with a high content of G and C, which tend to be rich in genes, and similar regions for other content measures (Huang, 1994).
- **Time series.** The best moving average over windows of at least a given length, such as the best stretch of sales or of a stock price.
- **Scheduling and networks.** The busiest period of a given minimum duration in a log of events, with the durations as widths.

## References
