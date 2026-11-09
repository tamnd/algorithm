---
tag: SA6TXV
kind: problem
slug: nuts-and-bolts
name: Nuts and bolts
aliases:
- matching nuts and bolts
- nuts and bolts problem
area: randomized/monte-carlo-and-las-vegas
level: core
summary: Matches each of n nuts to its bolt using only nut-bolt comparisons, solved by a randomized quicksort variant in expected O(n log n) time.
prereqs: [randomized-quicksort, linearity-of-expectation, las-vegas-algorithm]
see_also: [randomized-quicksort, quicksort-expected-running-time, comparison-sort-lower-bound, decision-tree-model, yao-minimax-principle, quickselect, las-vegas-to-monte-carlo-conversion, aks-sorting-network]
sources:
  - paper: "Noga Alon, Manuel Blum, Amos Fiat, Sampath Kannan, Moni Naor and Rafail Ostrovsky, Matching nuts and bolts, Proceedings of the 5th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 1994"
    title: Noga Alon, Manuel Blum, Amos Fiat, Sampath Kannan, Moni Naor and Rafail Ostrovsky, Matching nuts and bolts
    locator: pages 690 to 696 (the problem, the randomized algorithm, and a deterministic algorithm with n (log n)^O(1) comparisons)
  - paper: doi:10.1016/0020-0190(96)00104-4
    title: Noga Alon, Phillip G. Bradford and Rudolf Fleischer, Matching nuts and bolts faster, Information Processing Letters 59(3), 1996
    locator: pages 123 to 127 (a simpler deterministic algorithm based on expanders)
  - paper: "Janos Komlos, Yuan Ma and Endre Szemeredi, Matching nuts and bolts in O(n log n) time, SIAM Journal on Discrete Mathematics 11(3), 1998"
    title: Janos Komlos, Yuan Ma and Endre Szemeredi, Matching nuts and bolts in O(n log n) time
    locator: pages 347 to 372 (a deterministic algorithm with O(n log n) comparisons that also sorts the nuts and the bolts)
  - url: https://courses.grainger.illinois.edu/cs473/fa2022/notes/02-nutsbolts.pdf
    title: Jeff Erickson, Nuts and bolts, lecture notes for CS 473, University of Illinois Urbana-Champaign
    locator: the randomized algorithm and the analysis of its expected number of comparisons
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, third edition, MIT Press, 2009
    locator: Chapter 8, end-of-chapter problem on water jugs (the same problem with red and blue jugs, with the lower bound and the randomized algorithm)
---

The nuts and bolts problem gives $n$ nuts and $n$ bolts. Each nut fits exactly one bolt. The only allowed test puts a nut on a bolt and tells if the nut is too large, too small, or a fit. Two nuts cannot be compared with each other, and two bolts cannot either. The task is to find the matching bolt for every nut. A variant of [randomized quicksort](/randomized-quicksort/) solves it with exactly $4(n+1)H_n - 7n \approx 2.77\, n \log_2 n$ comparisons in expectation, and a decision-tree argument shows that every algorithm, randomized or not, needs at least $\log_3(n!) = \Omega(n \log n)$. A deterministic algorithm with $O(n \log n)$ comparisons exists, but it is complex and is not used in practice. The problem is a standard example of a [Las Vegas algorithm](/las-vegas-algorithm/) where randomness is the simple route and determinism is the hard one.

## In plain words

You have a box of nuts and a box of bolts of slightly different sizes. You can only put a nut on a bolt and feel whether it is loose, tight, or a fit.

The fast method is quicksort with a twist. Take a random bolt and try it with every nut. This splits the nuts into small ones, large ones, and the one nut that fits. Use that nut to split the other bolts in the same way. You get one matched pair, a pile of small nuts with its pile of small bolts, and the same for the large ones. Repeat on each pair of piles. On average this takes a few times $n \log n$ tries.

The twist: each pile is split by an item of the other kind, and the nut pivot is simply the nut that fits the bolt pivot.

## Definition

**Input.** A set $N$ of $n$ nuts and a set $B$ of $n$ bolts. There is a hidden size function $s$ with distinct values on the nuts, distinct values on the bolts, and $s(N) = s(B)$. So each nut $x$ has exactly one bolt $b$ with $s(x) = s(b)$.

**Allowed operation.** A comparison takes one nut $x$ and one bolt $b$ and returns one of three answers: $s(x) < s(b)$, $s(x) = s(b)$, or $s(x) > s(b)$. No other access to the sizes is allowed.

**Output.** The matching: the bijection $\pi : N \to B$ with $s(\pi(x)) = s(x)$ for every nut $x$.

**Cost.** The number of comparisons. Other work, such as moving items in arrays, is counted in the running time but is within a constant factor of the comparisons in all algorithms on this page.

The input order of the nuts and of the bolts is arbitrary. For a randomized algorithm the cost is a random variable, and the usual measure is its expected value on the worst input.

## Variants

- **Sorting nuts and bolts.** Output the nuts and the bolts in increasing order of size. A sorted output gives the matching at once (the $i$-th nut fits the $i$-th bolt), so sorting is at least as hard as matching. The randomized algorithm below sorts as a side effect, and so does the deterministic algorithm of Komlós, Ma and Szemerédi.
- **Water jugs.** The same problem with $n$ red jugs and $n$ blue jugs of distinct volumes, where the only test fills a red jug and pours it into a blue jug. It appears as an end-of-chapter problem in Chapter 8 of Cormen, Leiserson, Rivest and Stein.
- **Selection.** Find the nut and bolt of rank $k$. A variant of [quickselect](/quickselect/) that recurses into only one pair of piles uses $O(n)$ comparisons in expectation.
- **Parallel matching.** Do the comparisons in rounds, where each round compares disjoint pairs. The deterministic algorithms are built from expander graphs, the same tool that gives the [AKS sorting network](/aks-sorting-network/).

## Examples

**Two pairs.** Nuts of sizes 1 and 2, bolts of sizes 1 and 2. Any bolt pivot is compared with both nuts (2 comparisons), the fitting nut is compared with the other bolt (1 comparison), and the algorithm then checks the remaining single pair (1 comparison). Every run uses 4 comparisons.

**Five pairs, one run.** Nuts in the order $[4, 1, 5, 3, 2]$ and bolts in the order $[3, 5, 2, 1, 4]$, where the numbers stand for the hidden sizes. Suppose that the random choice is always the first bolt of the current range.

| Step | Range | Bolt pivot | Comparisons | Result |
|---|---|---|---|---|
| 1 | all 5 pairs | 3 | 5 with nuts, 4 with bolts | small nuts $[1, 2]$, small bolts $[2, 1]$, pair $(3, 3)$, large nuts $[4, 5]$, large bolts $[5, 4]$ |
| 2 | small piles | 2 | 2 with nuts, 1 with bolts | pair $(2, 2)$, and nut 1 with bolt 1 left |
| 3 | nut 1, bolt 1 | 1 | 1 | pair $(1, 1)$ |
| 4 | large piles | 5 | 2 with nuts, 1 with bolts | pair $(5, 5)$, and nut 4 with bolt 4 left |
| 5 | nut 4, bolt 4 | 4 | 1 | pair $(4, 4)$ |

The run uses $9 + 3 + 1 + 3 + 1 = 17$ comparisons. The expected count for $n = 5$ is $99/5 = 19.8$, and the worst run uses $n^2 = 25$. The tests in the implementation check these numbers by running the algorithm on every possible sequence of random choices for every input order with $n \le 5$.

**Counts for larger $n$.** The table compares the expected count of the randomized algorithm with the lower bound and with randomized quicksort on ordinary keys.

| $n$ | expected comparisons $4(n+1)H_n - 7n$ | lower bound $\log_3(n!)$ | randomized quicksort $2(n+1)H_n - 4n$ |
|---|---|---|---|
| 5 | 19.80 | 4.36 | 7.40 |
| 10 | 58.87 | 13.75 | 24.44 |
| 100 | 1395.70 | 331.09 | 647.85 |
| 1000 | 22971.83 | 5381.45 | 10985.91 |

The nuts and bolts count is exactly twice the quicksort count plus $n$. Each partition step does two passes instead of one, and the extra $n$ comes from the comparisons of each nut with its own bolt.

## Known algorithms

**Brute force.** For each bolt, try the remaining nuts one by one until one fits. The worst case uses $\sum_{m=2}^{n} (m - 1) = n(n-1)/2$ comparisons (the last nut tried does not need a test), and a random input order uses about $n^2/4$ on average. This is $\Theta(n^2)$.

**Randomized partition (the standard solution).** This is a Las Vegas algorithm: the output is always correct, and only the number of comparisons is random. The version below uses an explicit stack, so the depth of the recursion does not matter.

```pseudo id=main
MATCH(N, B)
L1  push the pair of piles (N, B) on a stack
L2  while the stack is not empty do
L3      (N', B') ← pop the stack
L4      if N' is empty then continue
L5      b ← a uniform random bolt of B'
L6      compare b with every nut of N': N< (too small), x (fits), N> (too large)   ▷ |N'| comparisons
L7      compare x with every other bolt of B': B< (too small), B> (too large)       ▷ |N'| − 1 comparisons
L8      record the pair (x, b)
L9      push (N<, B<) and (N>, B>)
```

Line L7 splits the bolts correctly because $s(x) = s(b)$: a bolt is smaller than $x$ if and only if it is smaller than $b$. So $N_<$ and $B_<$ hold the same set of sizes, and so do $N_>$ and $B_>$. Each pile pair is again an instance of the problem, and each step records one correct pair, so the algorithm stops after $n$ steps with the full matching. Its expected cost is analyzed in the next section; its worst case is $n^2$, when every pivot is the smallest or the largest of its range.

**Deterministic algorithms.** Finding a deterministic algorithm with $o(n^2)$ comparisons is much harder, because there is no simple deterministic way to find a good pivot. Alon, Blum, Fiat, Kannan, Naor and Ostrovsky (1994) gave the first one, with $n (\log n)^{O(1)}$ comparisons. Alon, Bradford and Fleischer (1996) gave a simpler and faster one with expander graphs. Bradford (1995) and Komlós, Ma and Szemerédi (1998) gave algorithms with $O(n \log n)$ comparisons, which is optimal up to the constant factor. Their constants are very large, so the randomized algorithm is the one used in practice.

## Bounds

**Upper bound: the expected count is $4(n+1)H_n - 7n$.** Here $H_n = \sum_{i=1}^{n} 1/i$ is the $n$-th [harmonic number](/harmonic-series/). Name the sizes $1, 2, \dots, n$ in increasing order. Nut $i$ means the nut of size $i$, and bolt $j$ the bolt of size $j$.

*Claim 1: each nut-bolt pair is compared at most once.* Nut $i$ and bolt $j$ are compared only in a step where one of them is a pivot: either bolt $j$ is the bolt pivot (line L6) or nut $i$ is the fitting nut (line L7). After that step the pivot is in a recorded pair and never takes part in a comparison again. A step with both pivots, $i = j$, makes exactly one comparison between them, in line L6.

*Claim 2: nut $i$ and bolt $i$ are compared exactly once.* They stay in the same pile pair until size $i$ becomes a pivot, which happens in some step, and that step compares them in line L6.

*Claim 3: for $i \ne j$, nut $i$ and bolt $j$ are compared with probability exactly $2/(|i - j| + 1)$.* Let $I = \{\min(i,j), \dots, \max(i,j)\}$, a set of $|i - j| + 1$ sizes. Every pile pair holds a contiguous range of sizes. As long as no size of $I$ has been a pivot, all of $I$ lies in one pile pair, because a pivot outside $I$ puts all of $I$ on the same side. Consider the first step whose pivot size lies in $I$. The pivot is uniform over the range of that step, and the range contains all of $I$, so conditioned on the pivot lying in $I$ it is uniform over $I$. If the pivot size is $j$, line L6 compares bolt $j$ with nut $i$. If it is $i$, line L7 compares nut $i$ with bolt $j$. If it is any other size of $I$, the pivot lies strictly between $i$ and $j$, so nut $i$ and bolt $j$ go to different piles and are never compared. So the probability is $2/|I|$.

*The sum.* By [linearity of expectation](/linearity-of-expectation/) over [indicator variables](/indicator-random-variable/) for the pairs,

$$\mathbb{E}[C(n)] = n + \sum_{i \ne j} \frac{2}{|i - j| + 1} = n + 2\sum_{d=1}^{n-1} \frac{2(n - d)}{d + 1}.$$

With $k = d + 1$, $\sum_{d=1}^{n-1} \frac{n-d}{d+1} = \sum_{k=2}^{n} \frac{n + 1 - k}{k} = (n+1)(H_n - 1) - (n - 1) = (n+1)H_n - 2n$. So

$$\mathbb{E}[C(n)] = n + 4\big((n+1)H_n - 2n\big) = 4(n+1)H_n - 7n.$$

The same value follows from the recurrence $C(0) = 0$ and $C(m) = 2m - 1 + \frac{1}{m}\sum_{k=1}^{m} \big(C(k-1) + C(m-k)\big)$ for $m \ge 1$, since the pivot has rank $k$ with probability $1/m$. The tests check that the recurrence and the closed form agree exactly for $n < 60$, and that the per-pair probabilities are exact for $n = 5$. Since $H_n = \ln n + O(1)$, the count is $4 n \ln n + O(n) \approx 2.77\, n \log_2 n$. The same argument as for [quicksort](/quicksort-expected-running-time/) shows that the count is $O(n \log n)$ also [with high probability](/high-probability-bounds/), not only in expectation.

**Lower bound: $\log_3(n!)$ comparisons, also for randomized algorithms.** Fix the order of the nuts and let the bolts come in any of the $n!$ orders. Different orders need different outputs, so a correct algorithm must tell all $n!$ inputs apart.

*Deterministic algorithms.* A deterministic algorithm is a ternary [decision tree](/decision-tree-model/): each internal node is a nut-bolt comparison with three children, one per answer, and each leaf gives an output. The $n!$ inputs reach $n!$ different leaves, and a ternary tree of height $h$ has at most $3^h$ leaves. So the worst case uses at least $\lceil \log_3(n!) \rceil$ comparisons.

*Randomized algorithms.* Fix the random bits; the algorithm is then a deterministic ternary tree. Take the input uniformly at random from the $n!$ orders. The inputs reach $n!$ distinct leaves at depths $d_1, \dots, d_{n!}$, and the [Kraft inequality](/kraft-inequality/) gives $\sum_\ell 3^{-d_\ell} \le 1$. By Jensen's inequality for the convex function $3^{-d}$, $3^{-\bar d} \le \frac{1}{n!}\sum_\ell 3^{-d_\ell} \le \frac{1}{n!}$, so the average depth $\bar d$ is at least $\log_3(n!)$. This holds for every value of the random bits, so it holds for the average over the bits too. An average over inputs that is at least $\log_3(n!)$ means that some input has an expected count of at least $\log_3(n!)$. This is the easy direction of [Yao's minimax principle](/yao-minimax-principle/).

By Stirling's formula, $\log_3(n!) = n \log_3 n - n \log_3 e + O(\log n)$, which is $\Omega(n \log n)$. The base is 3, not 2 as in the [comparison sort lower bound](/comparison-sort-lower-bound/), because a nut-bolt comparison has three possible answers and the answer "fits" carries information.

**The gap.** The randomized algorithm uses about $2.77\, n \log_2 n$ comparisons and the lower bound is about $0.63\, n \log_2 n$, so the two differ by a factor of about 4.4. This page does not give the best known constant for either side.

## Reductions

- **Matching reduces to sorting nuts and bolts.** A sorted output gives the matching with no more comparisons. The converse direction is not free: from a matching, sorting still needs $\Omega(n \log n)$ comparisons, because two matched pairs can only be compared through a nut of one and the bolt of the other.
- **Ordinary sorting reduces to sorting nuts and bolts.** Given $n$ distinct keys, make each key both a nut and a bolt. A nut-bolt comparison is then an ordinary comparison. So an algorithm for nuts and bolts sorts ordinary keys with the same number of comparisons. The reverse fails: an ordinary sorting algorithm compares two items of the same kind, which the nuts and bolts model forbids. This is why mergesort and heapsort do not apply, and why a deterministic $O(n \log n)$ algorithm was hard to find.
- **Las Vegas to Monte Carlo.** Stop the randomized algorithm after $2\,\mathbb{E}[C(n)]$ comparisons. By Markov's inequality it has finished with probability at least $1/2$. This is the general [conversion from Las Vegas to Monte Carlo](/las-vegas-to-monte-carlo-conversion/): the truncated algorithm has a fixed budget, and it may fail to give an answer.

## Applications

The problem is mainly a teaching and research model, not an industrial task. It is a clean case where:

- the natural fast algorithm is randomized, and the deterministic one needs deep tools such as expander graphs;
- the analysis of randomized quicksort carries over almost unchanged, with the per-pair probability $2/(|i-j|+1)$ and linearity of expectation;
- a lower bound counts leaves of a ternary decision tree, and Yao's principle extends it to randomized algorithms.

The same structure appears when items of two kinds can be compared only across kinds: keys and locks, or two sets of measurements on different scales that can only be tested against each other. In each case the answer is the same: use a random item of one kind to split the other kind, then use its match to split the first.

**Pitfalls when you implement it.**

- The pivot for the bolts must be the nut that fits the bolt pivot, found during the nut pass. Using any other nut gives piles with different sets of sizes.
- If the input breaks the promise (some bolt has no fitting nut), line L6 finds no $x$. A robust implementation must detect this case instead of reading an undefined value.
- A range with one nut and one bolt needs no comparison, because the promise says they fit. The counts on this page include that comparison, to match the recurrence above. Skipping it saves one comparison for each range of size 1.
- A fixed pivot, such as the first bolt, makes the worst case $n^2$ on inputs in sorted order, the same failure as deterministic quicksort.

## References
