---
tag: 3XZ095
kind: theorem
slug: bucket-sort-expected-linear
name: Bucket sort expected linear time
area: sorting/distribution-sorts
level: core
summary: On independent uniform keys in [0,1), bucket sort with n buckets runs in expected O(n) time.
prereqs: [bucket-sort, uniform-input-model, indicator-random-variable, linearity-of-expectation]
see_also: [bucket-sort, uniform-input-model, balls-into-bins, binomial-distribution, insertion-sort, expected-running-time, average-case-analysis]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8, Section 8.4, Bucket sort (the analysis of the expected running time with indicator random variables)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 5, Section 5.2.2, Application, Bucket Sort
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.1, Sorting by Insertion (multiple list insertion and its analysis)
---

This theorem says that [bucket sort](/bucket-sort/) with $n$ buckets and [insertion sort](/insertion-sort/) inside each bucket runs in expected $\Theta(n)$ time when its $n$ keys are independent and uniform on $[0, 1)$. The reason is that the expected square of a bucket size is $2 - 1/n$, so the quadratic cost of insertion sort adds up to only $O(n)$ over all buckets. The expectation is over the input distribution, the [uniform input model](/uniform-input-model/), not over random choices of the algorithm. The proof is the standard first use of [indicator random variables](/indicator-random-variable/) for a sorting algorithm.

## Statement

Let $X_1, \ldots, X_n$ be independent random keys, each uniform on $[0, 1)$, with $n \ge 1$. Run BUCKET-SORT with the bucket map $\beta(x) = \lfloor n x \rfloor$, and let $N_j = |\{i : \beta(X_i) = j\}|$ be the size of bucket $j$, for $j = 0, \ldots, n-1$.

**Theorem.**

1. For each $j$, $\mathbb{E}[N_j] = 1$ and $\mathbb{E}[N_j^2] = 2 - 1/n$. So $\mathbb{E}\big[\sum_j N_j^2\big] = 2n - 1$.
2. The expected total number of shifts (moves of one key one place to the right) that insertion sort does in all buckets is $(n - 1)/4$.
3. Let the running time be $T(n) \le a n + b + c \sum_j N_j^2$ for constants $a, b, c$, which holds for BUCKET-SORT on the [real RAM](/real-ram/) with a floor operation. Then $\mathbb{E}[T(n)] \le (a + 2c) n + b = O(n)$. Since each run reads all $n$ keys, $\mathbb{E}[T(n)] = \Theta(n)$.

## In plain words

Throw a number of balls at random into the same number of boxes. On average each box gets one ball. A few boxes get two or three, many get none, and almost never does a box get many. Insertion sort is slow only on a box with many items, because its cost grows with the square of the size of the box. The theorem says that the average of these squares is less than two, so the total cost of all the small sorts is less than twice the number of items, plus the cost of filling and reading the boxes. The whole sort therefore takes time in proportion to the number of items, on average, if the keys are random and spread evenly.

## Proof

**Each key falls in each bucket with probability $1/n$.** For a fixed $i$ and $j$, $\beta(X_i) = j$ if and only if $j/n \le X_i < (j+1)/n$. This interval has length $1/n$ and lies in $[0, 1)$, so its probability under the uniform distribution is $1/n$.

**Part 1.** Fix $j$, and let $Y_i$ be the [indicator](/indicator-random-variable/) of the event $\beta(X_i) = j$. Then $N_j = \sum_{i=1}^n Y_i$ and $\Pr[Y_i = 1] = 1/n$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[N_j] = n \cdot (1/n) = 1$. Expand the square:
$$ N_j^2 = \sum_{i=1}^n Y_i^2 + \sum_{i \ne k} Y_i Y_k. $$
An indicator satisfies $Y_i^2 = Y_i$, so $\mathbb{E}[Y_i^2] = 1/n$. For $i \ne k$, the keys $X_i$ and $X_k$ are independent, so $\mathbb{E}[Y_i Y_k] = \Pr[Y_i = 1] \Pr[Y_k = 1] = 1/n^2$. There are $n(n-1)$ ordered pairs $(i, k)$ with $i \ne k$. So
$$ \mathbb{E}[N_j^2] = n \cdot \frac{1}{n} + n(n-1) \cdot \frac{1}{n^2} = 1 + \frac{n-1}{n} = 2 - \frac{1}{n}. $$
Summing over the $n$ buckets gives $\mathbb{E}[\sum_j N_j^2] = n(2 - 1/n) = 2n - 1$.

**Part 2.** Insertion sort on a list does exactly one shift for each inversion of the list, that is, for each pair of positions $p < q$ with a larger key at $p$. Two keys $X_i, X_k$ with $i < k$ form an inversion in bucket $j$ if both are in bucket $j$ and $X_i > X_k$, because line L3 appends in order of index. For fixed $i < k$ and $j$, the pair $(X_i, X_k)$ is uniform on the square $[0,1)^2$. The event "both in bucket $j$" is the small square $[j/n, (j+1)/n)^2$, of probability $1/n^2$, and it is symmetric under the swap of the two coordinates, while the diagonal $X_i = X_k$ has probability 0. So the probability that both are in bucket $j$ and $X_i > X_k$ is $1/(2n^2)$. Summing over the $n$ buckets and the $\binom{n}{2}$ pairs, the expected number of shifts is
$$ \binom{n}{2} \cdot n \cdot \frac{1}{2n^2} = \frac{n(n-1)}{2} \cdot \frac{1}{2n} = \frac{n-1}{4}. $$

**Part 3.** Lines L1 to L3 and L6 of BUCKET-SORT do $O(1)$ work per key and per bucket, which gives the term $a n + b$. Insertion sort on $N_j$ keys does at most $N_j - 1$ outer steps and at most $\binom{N_j}{2}$ shifts, so its time is at most $c (N_j^2 + 1)$ for a constant $c$; the term $c \cdot 1$ per bucket goes into $a n$. So $T(n) \le a n + b + c \sum_j N_j^2$. By linearity of expectation and Part 1, $\mathbb{E}[T(n)] \le a n + b + c(2n - 1) \le (a + 2c) n + b$. Each run does at least $n$ steps in line L3, so $\mathbb{E}[T(n)] \ge n$, and $\mathbb{E}[T(n)] = \Theta(n)$. $\blacksquare$

**Numbers.** With $n = 1000$, Part 1 gives $\mathbb{E}[\sum_j N_j^2] = 1999$ and Part 2 gives $249.75$ expected shifts. A simulation of 500 runs with seed 5 gave means of $1999.05$ and $251.34$, and the largest bucket had 5.5 keys on average.

## Consequences

- **Linear-time sorting of random reals.** On the [uniform input model](/uniform-input-model/), bucket sort beats the $\Omega(n \log n)$ [comparison lower bound](/comparison-sort-lower-bound/) in expectation. This does not contradict the bound: bucket sort uses the floor of $n x$, which a comparison sort cannot compute, and the bound for comparison sorts holds also on average.
- **Other distributions.** If the keys are independent with a known continuous distribution function $F$, then the values $F(X_i)$ are independent and uniform on $[0, 1)$ (up to a set of probability 0), and bucket sort on these values runs in expected linear time.
- **Fewer or more buckets.** With $m$ buckets, the same computation gives $\mathbb{E}[N_j^2] = n/m \cdot (1 - 1/m) + n^2/m^2$, so $\mathbb{E}[\sum_j N_j^2] = n + n(n-1)/m$, and the expected time is $\Theta(n + m + n^2/m)$. It is linear for each $m = \Theta(n)$. This is the base of the choice of about $0.1 n$ classes in [flashsort](/flashsort/) and of the bucket counts of [proxmap sort](/proxmap-sort/).
- **The largest bucket.** The bucket sizes are the loads of [balls into bins](/balls-into-bins/) with $n$ balls and $n$ bins. The largest bucket has $\Theta(\log n / \log \log n)$ keys with high probability, so the worst bucket alone costs $O((\log n / \log\log n)^2)$ with high probability.

## Tightness

**The expectation is not a worst-case bound.** For each $n$ there are inputs, all keys in $[0, 1/n)$ in decreasing order, on which insertion sort in bucket 0 does $n(n-1)/2$ shifts, so the worst-case time is $\Theta(n^2)$.

**The assumption cannot be dropped.** Let the keys be independent and uniform on $[0, 1/n)$ instead of $[0, 1)$. Then all keys fall in bucket 0, they arrive in a uniformly random order, and the expected number of shifts is $n(n-1)/4$. So the expected time is $\Theta(n^2)$ for this distribution, although each key is still uniform on an interval.

**The constant in Part 1 is exact.** $\mathbb{E}[N_j^2] = 2 - 1/n$ is an equality, not a bound. For $n = 1$ it gives 1, and as $n \to \infty$ it tends to 2, the second moment of a Poisson variable with mean 1.

## History

The analysis with indicator variables and the second moment $2 - 1/n$ is the one in CLRS, Section 8.4. Mitzenmacher and Upfal (Section 5.2.2) give the same bound for integer keys with the balls and bins model, and Knuth (Section 5.2.1) analyses the related method of multiple list insertion, which spreads keys into many short sorted lists by their value.

## References
