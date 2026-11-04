---
tag: VNK43J
kind: theorem
slug: merge-sort-optimality
name: Mergesort optimality
area: foundations/lower-bounds
level: core
summary: Shows that mergesort uses a number of comparisons that matches the lower bound for comparison sorting, up to lower order terms.
prereqs: [merge-sort, comparison-sort-lower-bound, stirling-approximation]
see_also: [merge-sort, comparison-sort-lower-bound, ford-johnson-algorithm, information-theoretic-bound, merging-lower-bound, optimality, asymptotic-optimality, stirling-approximation]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.4 (sorting by merging, the number of comparisons of merge sort), Section 5.3.1 (minimum-comparison sorting, binary insertion, the Ford and Johnson merge insertion and its count, the table of S(n)), Section 5.3.2 (minimum-comparison merging)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.3 (merge sort and its recurrence) and Section 8.1 (Theorem 8.1, the bound Omega(n lg n), and Corollary 8.2, heapsort and merge sort are asymptotically optimal comparison sorts)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 5.1, A first recurrence, the mergesort algorithm
  - paper: "Lester R. Ford Jr. and Selmer M. Johnson, A tournament problem, American Mathematical Monthly 66 (1959)"
    locator: pp. 387 to 389 (merge insertion)
---

Mergesort optimality is the statement that [merge sort](/merge-sort/) makes, in the worst case, a number of comparisons that matches the [comparison sort lower bound](/comparison-sort-lower-bound/) $\lceil \lg(n!) \rceil$ in its leading term $n \lg n$. Its worst case is exactly $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$, which exceeds $\lg(n!)$ by between about $0.44n$ and $0.53n$. So merge sort is optimal up to lower-order terms, and [asymptotically optimal](/asymptotic-optimality/) in the $\Theta$ sense, but it is not exactly optimal: for every $n \ge 5$ the [Ford and Johnson algorithm](/ford-johnson-algorithm/) makes fewer comparisons in the worst case.

## Statement

Let $S(n)$ be the least number $t$ such that some comparison algorithm sorts every input of $n$ distinct keys with at most $t$ comparisons. Let $W(n)$ be the worst-case number of comparisons of top-down merge sort, which splits $n$ items into parts of $\lceil n/2 \rceil$ and $\lfloor n/2 \rfloor$, and let $F(n)$ be the worst-case number of comparisons of the Ford and Johnson merge insertion.

**Theorem.** For every $n \ge 1$:

1. **(Exact count.)** $W(n) = \displaystyle\sum_{k=1}^{n} \lceil \lg k \rceil = n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1.$
2. **(Optimal up to lower-order terms.)** $\lceil \lg(n!) \rceil \le S(n) \le W(n)$, and
$$W(n) = n \lg n - \theta_n n + 1 \ \text{ with } 0.9139 < \theta_n \le 1, \qquad \lg(n!) = n \lg n - n \lg e + O(\lg n),$$
so $W(n) - \lg(n!) = c_n n + O(\lg n)$ with $0.4426 < c_n < 0.5288$, and $W(n)/S(n) \to 1$.
3. **(Not exactly optimal.)** $W(n) = S(n)$ for $n \le 4$. For $n \ge 5$, $W(n) > F(n) \ge S(n)$, and $W(n) - F(n) \ge n/4 - O(\lg n)$.

## In plain words

Any method that sorts by comparing pairs must, in its worst case, make enough comparisons to tell apart every possible order of the items. That number grows like the number of items times the number of times you can halve it.

Merge sort splits the items into two halves, sorts each half, and merges them. Its count of comparisons in the worst case has the same main part. The extra part grows only like the number of items, so for large inputs the ratio of the two counts goes to one. In that sense merge sort cannot be improved by much.

But it can be improved by a little. From five items on, a more careful method that inserts items into well-chosen places always makes fewer comparisons in the worst case. So merge sort is close to the best, not the best.

## Proof

**Step 1, the recurrence.** Merging sorted lists of sizes $a \ge 1$ and $b \ge 1$ by the usual method makes at most $a + b - 1$ comparisons, since each comparison outputs one item and the last item needs none. It makes exactly $a + b - 1$ when the two largest items are in different lists, since then neither list is used up before the last output. So the merge of the top level costs at most $n - 1$, and

$$W(1) = 0, \qquad W(n) \le W(\lceil n/2 \rceil) + W(\lfloor n/2 \rfloor) + n - 1.$$

The bound is an equality. An order of $n$ keys is fixed by three independent choices: the relative order of the keys that go to the left half, the relative order of the keys that go to the right half, and the interleaving of the two halves in the sorted output. The comparisons inside each half depend only on the relative order of that half, and the merge depends only on the interleaving. Choose a worst order for each half, and an interleaving where the two largest keys are in different halves. This input makes all three parts reach their worst case together. So

$$W(n) = W(\lceil n/2 \rceil) + W(\lfloor n/2 \rfloor) + n - 1 \quad (n \ge 2).$$

**Step 2, the differences.** Let $D(n) = W(n) - W(n-1)$ for $n \ge 2$. We show $D(n) = \lceil \lg n \rceil$ by strong induction. $D(2) = 1 = \lceil \lg 2 \rceil$ and $D(3) = W(3) - W(2) = 3 - 1 = 2 = \lceil \lg 3 \rceil$. Let $n \ge 4$.

- If $n = 2m$ with $m \ge 2$: $W(2m) = 2W(m) + 2m - 1$ and $W(2m - 1) = W(m) + W(m - 1) + 2m - 2$. So $D(2m) = D(m) + 1 = \lceil \lg m \rceil + 1 = \lceil \lg(2m) \rceil$.
- If $n = 2m + 1$ with $m \ge 2$: $W(2m + 1) = W(m + 1) + W(m) + 2m$ and $W(2m) = 2W(m) + 2m - 1$. So $D(2m + 1) = D(m + 1) + 1 = \lceil \lg(2m + 2) \rceil$. Since $2m + 1 \ge 3$ is odd, it is not a power of 2, so $\lceil \lg(2m + 2) \rceil = \lceil \lg(2m + 1) \rceil$.

With $W(1) = 0 = \lceil \lg 1 \rceil$, this gives $W(n) = \sum_{k=1}^{n} \lceil \lg k \rceil$.

**Step 3, the closed form.** Let $L = \lceil \lg n \rceil$. The value $\lceil \lg k \rceil = j \ge 1$ holds for the $2^{j-1}$ integers $2^{j-1} < k \le 2^j$. So

$$\sum_{k=1}^{n} \lceil \lg k \rceil = \sum_{j=1}^{L-1} j\, 2^{j-1} + L\,(n - 2^{L-1}) = (L - 2)\, 2^{L-1} + 1 + L n - L\, 2^{L-1} = nL - 2^L + 1,$$

using $\sum_{j=1}^{m} j\, 2^{j-1} = (m - 1)\, 2^m + 1$. This proves part 1.

**Step 4, the comparison with $\lg(n!)$.** The lower bound $S(n) \ge \lceil \lg(n!) \rceil$ is the [comparison sort lower bound](/comparison-sort-lower-bound/), and $S(n) \le W(n)$ because merge sort is one comparison sort. Write $L = \lg n + u$ with $0 \le u < 1$. Then

$$W(n) = n(\lg n + u) - n\, 2^u + 1 = n \lg n - (2^u - u)\, n + 1.$$

The function $\theta(u) = 2^u - u$ on $[0, 1)$ has $\theta(0) = 1$, tends to 1 as $u \to 1$, and has its least value at $u = \lg(1/\ln 2) \approx 0.5288$, where $\theta = 1/\ln 2 - \lg(1/\ln 2) \approx 0.91393$. So $0.9139 < \theta_n \le 1$. By [Stirling's approximation](/stirling-approximation/), $\lg(n!) = n \lg n - n \lg e + O(\lg n)$ with $\lg e \approx 1.4427$. Subtracting gives $W(n) - \lg(n!) = (\lg e - \theta_n)\, n + O(\lg n)$, and $\lg e - \theta_n$ lies between $0.4426$ and $0.5288$. Since $\lg(n!) \sim n \lg n$, $W(n)/\lg(n!) \to 1$, and $\lg(n!) \le S(n) \le W(n)$ gives $W(n)/S(n) \to 1$. This proves part 2.

**Step 5, merge sort against merge insertion.** Knuth, Section 5.3.1, shows that merge insertion sorts $n$ keys with at most

$$F(n) = \sum_{k=1}^{n} \left\lceil \lg \tfrac{3k}{4} \right\rceil$$

comparisons. So $S(n) \le F(n)$, and

$$W(n) - F(n) = \sum_{k=1}^{n} \Big( \lceil \lg k \rceil - \lceil \lg k - \lg \tfrac{4}{3} \rceil \Big).$$

Since $0 < \lg(4/3) < 1$, each term is 0 or 1, and it is 1 exactly when some integer $j$ satisfies $\lg k - \lg(4/3) \le j < \lg k$, that is, $2^j < k \le \tfrac{4}{3} 2^j$. For $k = 5$ and $j = 2$ this holds ($4 < 5 \le 5.33$). So $W(n) - F(n) \ge 1$ for all $n \ge 5$, and $W(n) > F(n) \ge S(n)$.

For $k \le 4$ no such $j$ exists, so $W(n) = F(n)$ for $n \le 4$. Also $W(n) = \lceil \lg(n!) \rceil$ for $n \le 4$ (the values are 0, 1, 3, 5), so $W(n) = S(n)$ there.

For the linear gap: the interval $2^j < k \le \tfrac{4}{3} 2^j$ holds $\lfloor 2^j/3 \rfloor$ integers. Let $J$ be the largest $j$ with $\tfrac{4}{3} 2^J \le n$, so $2^{J+1} > \tfrac{3}{4} n$. Then $W(n) - F(n) \ge \sum_{j=0}^{J} \lfloor 2^j/3 \rfloor \ge \tfrac{1}{3}(2^{J+1} - 1) - (J + 1) \ge \tfrac{n}{4} - O(\lg n)$. This proves part 3. ∎

## Consequences

- **Asymptotic optimality.** Merge sort and [heapsort](/heapsort/) both run in $O(n \lg n)$ time, which matches the $\Omega(n \lg n)$ bound, so both are asymptotically optimal comparison sorts (CLRS, Corollary 8.2). The theorem is sharper for merge sort: it fixes the constant of the leading term at 1, and puts the second term between $0.44n$ and $0.53n$ above the bound.
- **Merge sort equals binary insertion.** The sum $\sum_{k=1}^{n} \lceil \lg k \rceil$ is also the worst case of binary insertion sort, which inserts the $k$th item with $\lceil \lg k \rceil$ comparisons by the [sorted search lower bound](/sorted-search-lower-bound/). Merge insertion beats both by inserting items into lists of size $2^j - 1$, where a binary search is not wasteful.
- **The merge step is optimal.** Merging lists of sizes $m$ and $m$, or $m$ and $m + 1$, needs $2m - 1$ and $2m$ comparisons in the worst case ([merging lower bound](/merging-lower-bound/)), which is what the merge makes. The loss is in the plan of the whole sort, not in the merge.
- **The ratio tends to 1 slowly.** The gap is linear, while the bound grows like $n \lg n$, so the ratio $W(n)/\lceil \lg(n!) \rceil$ falls only like $1 + O(1/\lg n)$.

| $n$ | $\lceil \lg(n!) \rceil$ | $S(n)$ | $F(n)$ | $W(n)$ |
|---|---|---|---|---|
| 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 1 | 1 | 1 |
| 3 | 3 | 3 | 3 | 3 |
| 4 | 5 | 5 | 5 | 5 |
| 5 | 7 | 7 | 7 | 8 |
| 6 | 10 | 10 | 10 | 11 |
| 7 | 13 | 13 | 13 | 14 |
| 8 | 16 | 16 | 16 | 17 |
| 9 | 19 | 19 | 19 | 21 |
| 10 | 22 | 22 | 22 | 25 |
| 11 | 26 | 26 | 26 | 29 |
| 12 | 29 | 30 | 30 | 33 |

For larger $n$, with $S(n)$ between the first two columns:

| $n$ | $\lceil \lg(n!) \rceil$ | $F(n)$ | $W(n)$ | $W(n) - \lg(n!)$ | $W(n) / \lceil \lg(n!) \rceil$ |
|---|---|---|---|---|---|
| 16 | 45 | 46 | 49 | 4.75 | 1.0889 |
| 100 | 525 | 534 | 573 | 48.24 | 1.0914 |
| 1000 | 8530 | 8641 | 8977 | 447.6 | 1.0524 |
| $10^4$ | 118459 | 119085 | 123617 | 5158.86 | 1.0435 |
| $10^5$ | 1516705 | 1525247 | 1568929 | 52224.83 | 1.0344 |
| $10^6$ | 18488885 | 18601910 | 18951425 | 462540.18 | 1.0250 |

## Tightness

Part 1 is exact: the recurrence and the closed form are equalities for every $n$. The constants in part 2 are the best possible: $\theta_n = 1$ when $n$ is a power of 2, and $\theta_n$ comes arbitrarily close to $0.91393$ for $n$ near $2^{L}/2^{0.5288} \approx 0.693 \cdot 2^L$. For $n = 2^L$ the formula gives $W(n) = n \lg n - n + 1$, for example $W(1024) = 9217$.

Part 3 cannot be extended to all $n$: for $n \le 4$ merge sort is exactly optimal. The lower bound $\lceil \lg(n!) \rceil$ is not always reached either: $S(12) = 30$, while $\lceil \lg(12!) \rceil = 29$ (Knuth, Section 5.3.1). And merge insertion is not exactly optimal for all $n$; see the [Ford and Johnson algorithm](/ford-johnson-algorithm/).

### Pitfalls

- **"Optimal" needs a qualifier.** Merge sort is optimal in the $\Theta$ sense and up to lower-order terms, $W(n) \sim S(n)$. It is not exactly optimal. Say which one is meant. See [optimality](/optimality/).
- **The formula is for the top-down split.** Bottom-up merge sort that merges runs of size $1, 2, 4, \dots$ makes a different number of comparisons when $n$ is not a power of 2, and it can be larger.
- **$n \lg n - n + 1$ is not the general formula.** It holds only when $n$ is a power of 2. For other $n$ the term $-\theta_n n$ uses $\theta_n < 1$.
- **The worst case of the merge is $a + b - 1$, not $a + b$.** The last item is output with no comparison.
- **Comparisons are not time.** Merge sort is optimal in comparisons up to lower-order terms, but it moves $\Theta(n \lg n)$ items and uses $\Theta(n)$ extra memory. A sort with more comparisons can be faster in practice.
- **Worst cases add only because the parts are independent.** In Step 1 the equality needs one input that is worst for both halves and for the merge at once. This holds for merge sort, but for other algorithms the sum of the worst cases of the parts is only an upper bound.

## History

Knuth, Volume 3, Section 5.2.4, analyses the number of comparisons of merge sort, and Section 5.3.1 gives the sum $\sum \lceil \lg k \rceil$ for binary insertion, the information-theoretic bound and the table of $S(n)$ for small $n$. Ford and Johnson (1959) published merge insertion, whose worst case $F(n)$ is below the count of merge sort and binary insertion for $n \ge 5$. CLRS, Section 8.1, states that merge sort and heapsort are asymptotically optimal comparison sorts, and Kleinberg and Tardos, Section 5.1, use merge sort as their first example of a recurrence of the form $T(n) \le 2T(n/2) + cn$.

## References
