---
tag: 4X1VCA
kind: theorem
slug: deterministic-linear-selection
name: Linear-time deterministic selection theorem
aliases:
- BFPRT theorem
area: sorting/selection-and-order-statistics
level: core
summary: Selection of any order statistic can be done in worst-case O(n) comparisons.
prereqs: [median-of-medians, substitution-method]
see_also: [selection-problem, quickselect-expected-linear, selection-lower-bound, introselect, median-finding, akra-bazzi-theorem, prune-and-search, quicksort]
sources:
  - paper: doi:10.1016/S0022-0000(73)80033-9
    title: Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest and Robert E. Tarjan, Time bounds for selection, Journal of Computer and System Sciences 7(4) (1973)
    locator: pages 448 to 461 (the algorithm PICK, at most 5.4305n comparisons for each rank)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Section 9.3, Selection in worst-case linear time (SELECT with groups of 5, and the exercises on groups of 3 and 7)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (linear upper bounds on V_t(n))
  - paper: doi:10.1007/978-3-319-21840-3_16
    title: Ke Chen and Adrian Dumitrescu, Select with groups of 3 or 4, Algorithms and Data Structures (WADS 2015), Lecture Notes in Computer Science 9214
    locator: the linear-time variants with groups of 3 and 4
  - paper: doi:10.1137/S0097539795288611
    title: Dorit Dor and Uri Zwick, Selecting the median, SIAM Journal on Computing 28(5) (1999)
    locator: pages 1722 to 1758 (the median with fewer than 2.95n comparisons)
---

The linear-time deterministic selection theorem says that the item of each rank $k$ among $n$ items can be found with $O(n)$ comparisons and in $O(n)$ time in the worst case, by a deterministic algorithm in the [comparison model](/comparison-model/). Blum, Floyd, Pratt, Rivest and Tarjan proved it in 1973 with a pivot chosen as the [median of medians](/median-of-medians/) of groups of five, and bounded the number of comparisons by $5.4305n$. The heart of the proof is a recurrence whose two recursive calls together get less than the whole input, $n/5 + 7n/10 = 9n/10$, so that the work per level shrinks geometrically.

## Statement

**Theorem.** There is a constant $c$ and a deterministic comparison algorithm that, for each $n \ge 1$, each list $S$ of $n$ items with a [total order](/total-order/), and each $1 \le k \le n$, returns the item of rank $k$ of $S$ with at most $cn$ comparisons and $O(n)$ other operations. Blum, Floyd, Pratt, Rivest and Tarjan (1973) give $c = 5.4305$.

The proof below is for SELECT with groups of five as on the [median of medians](/median-of-medians/) page, and it gives a constant of $40$ comparisons per item. It rests on a lemma about recurrences that is useful on its own.

**Lemma (two shrinking calls).** Let $\alpha, \beta > 0$ with $\alpha + \beta < 1$, and let $c_1, c_2 \ge 0$, $a > 0$ and $n_0 \ge 1$ be constants. Let $T$ be a function from the integers $n \ge 0$ to the reals with $T(0) = 0$ and $T(n) \ge 0$, such that for each $n \ge n_0$

$$ T(n) \le T(p) + T(q) + an \quad \text{for some integers } 0 \le p \le \alpha n + c_1,\; 0 \le q \le \beta n + c_2, \text{ with } p, q < n. $$

Then $T(n) = O(n)$.

## In plain words

To find the item of a given rank, the algorithm splits the items around a pivot and keeps only one side, as quickselect does. The difficulty is the choice of the pivot: a bad pivot keeps almost everything, and then the work can grow like the square of the input size.

The trick is to spend a little work on a pivot that is never bad. Cut the items into groups of five, take the middle of each group, and find the middle of those middles by the same method. This pivot is known to have at least three tenths of the items on each side. So the work has two parts, a search among one fifth of the items and a search among at most seven tenths of them. Together these are less than all of the items, so the total work is a constant times the input size.

## Proof

### Proof of the lemma

Let $\varepsilon = 1 - \alpha - \beta > 0$. Choose $N = \max\bigl(n_0, \lceil 2(c_1 + c_2)/\varepsilon \rceil\bigr)$ and

$$ c = \max\Bigl(\frac{2a}{\varepsilon},\ \max_{1 \le n < N} \frac{T(n)}{n}\Bigr). $$

We show $T(n) \le cn$ for each $n \ge 0$, by strong induction on $n$, in the style of the [substitution method](/substitution-method/). For $n = 0$ this is $T(0) = 0$, and for $1 \le n < N$ it holds by the choice of $c$. Let $n \ge N$ and assume the claim for each $m < n$. Then $n \ge n_0$, and with the $p$ and $q$ of the hypothesis, both less than $n$,

$$ T(n) \le cp + cq + an \le c(\alpha + \beta)n + c(c_1 + c_2) + an = cn - \bigl(c\varepsilon n - c(c_1 + c_2) - an\bigr). $$

Since $c \ge 2a/\varepsilon$, $an \le c\varepsilon n/2$. Since $n \ge N \ge 2(c_1 + c_2)/\varepsilon$, $c(c_1 + c_2) \le c\varepsilon n/2$. So the bracket is at least $0$, and $T(n) \le cn$. $\square$

### The pivot is balanced

Recall SELECT$(S, k)$: if $n \le 5$, sort and answer; else split $S$ into $g = \lceil n/5 \rceil$ groups of five consecutive items, the last of $r \in \{1, \ldots, 5\}$ items; let $M$ be the list of the lower medians of the groups; let $x$ = SELECT$(M, \lceil g/2 \rceil)$; split $S$ into $L$, $E$ and $G$, the items less than, equal to and greater than $x$; and recurse on $L$ or $G$, or return $x$. Its correctness is proved on the [median of medians](/median-of-medians/) page; it uses only that $x$ is an item of $S$.

**Claim.** For $n \ge 6$, $|G| \le \lfloor 7n/10 + 2 \rfloor$ and $|L| \le \lfloor 7n/10 + 1/2 \rfloor$. Also $|L|, |G| \le n - 1$.

*Proof.* The item $x$ has rank $\lceil g/2 \rceil$ in $M$, so at least $\lceil g/2 \rceil$ group medians are at most $x$. In a full group, its median and the two items below it are at most the median, so at most $x$: three items. The last group, if it is one of these, gives at least one item, its median. So at least $3\lceil g/2 \rceil - 2 \ge 3n/10 - 2$ items are at most $x$, using $g \ge n/5$. Hence $|G| \le n - (3n/10 - 2) = 7n/10 + 2$. In the same way, at least $\lfloor g/2 \rfloor + 1$ medians are at least $x$, each full group among them gives three items at least $x$, and the last group gives at least one, so at least $3\lfloor g/2 \rfloor + 1 \ge 3(g-1)/2 + 1 \ge 3(n/5 - 1)/2 + 1 = 3n/10 - 1/2$ items are at least $x$, using $g \ge n/5$. Hence $|L| \le 7n/10 + 1/2$. Sizes are integers, which gives the floors. Since $x$ is in $E$, neither $L$ nor $G$ holds all $n$ items. $\square$

### Linear time

Let $T(n)$ be the largest number of comparisons that SELECT makes on a list of $n$ items, over all lists and ranks, and $T(0) = 0$. For $n \ge 6$, a run makes:

- at most $10$ comparisons per group to sort it by insertion sort and take its lower median, so at most $10g \le 2n + 8$;
- at most $T(g)$ comparisons in the call on $M$;
- at most $2$ comparisons per item to split $S$ into $L$, $E$ and $G$, so at most $2n$;
- at most $\max(T(|L|), T(|G|))$ comparisons in the last call.

So $T(n) \le T(g) + T(q) + 4n + 8$ with $g = \lceil n/5 \rceil \le n/5 + 1$ and $q \le 7n/10 + 2$, and both less than $n$. The term $8$ is at most $8n/6$ for $n \ge 6$, so the lemma applies with $\alpha = 1/5$, $\beta = 7/10$, $\varepsilon = 1/10$, $c_1 = 1$, $c_2 = 2$, $a = 4 + 8/6$ and $n_0 = 6$, and $T(n) = O(n)$.

The lemma's choice of $c$ is loose. The leading constant of $T$ is $4/(1 - 9/10) = 40$: if $T(n) \le \lambda n + \mu$ for smaller lists, then $T(n) \le \lambda (n/5 + 7n/10) + 4n + O(\lambda) = \lambda n - (\lambda/10 - 4)n + O(\lambda)$, which is at most $\lambda n + \mu$ for large $n$ once $\lambda > 40$. Evaluating the recurrence $T(n) = T(\lceil n/5 \rceil) + T(\min(n - 1, \lfloor 7n/10 + 2 \rfloor)) + 4n$ with $T(n) = 10$ for $n \le 5$ gives $T(n)/n = 31.7$, $34.2$, $36.0$ and $37.3$ for $n = 10^3$, $10^4$, $10^5$ and $10^6$, which approaches $40$ slowly.

The other operations of a run, the grouping, the copying into $M$, $L$, $E$ and $G$, and the tests, take $O(1)$ time per comparison plus $O(n)$ per call on $n$ items, so the same recurrence with a larger $a$ bounds the time, which is $O(n)$. $\blacksquare$

## Consequences

- **Selection is linear.** With the trivial lower bound of $n - 1$ comparisons, the theorem shows that the [selection problem](/selection-problem/) takes $\Theta(n)$ comparisons and $\Theta(n)$ time in the worst case, for each rank. Sorting needs $\Omega(n \log n)$, so selection is strictly easier than sorting.
- **Quicksort in $O(n \log n)$ worst case.** With the exact median as pivot at each step, [quicksort](/quicksort/) splits each range into halves and runs in $O(n \log n)$ time on each input. The constant is large, so libraries use [introsort](/introsort/) instead.
- **A fallback with a guarantee.** [Introselect](/introselect/) runs quickselect and switches to median of medians when the ranges shrink too slowly, which keeps the speed of quickselect and the worst-case bound of this theorem.
- **Many derived problems become linear.** The [weighted median](/weighted-median-post-office-location/), the $k$ items nearest to the median ([k nearest to the median](/k-nearest-to-median/)), and the step of [prune and search](/prune-and-search/) that throws away a fixed fraction of the input all take $O(n)$ worst-case time by this theorem. The $q$-[quantiles](/quantile/) take $O(n \log q)$.

## Tightness

- **The order is tight.** Each algorithm must look at each item, and the [selection lower bound](/selection-lower-bound/) shows that at least $n - 1 + \min(k - 1, n - k)$ comparisons are needed, about $1.5n$ for the median.
- **The constant is open.** For the median the best upper bound is fewer than $2.95n$ comparisons (Dor and Zwick, 1999), and the best lower bound is $(2 + 2^{-80})n$ (Dor and Zwick, 2001). The constant $40$ of the proof above, and even the $5.4305$ of the original paper, are far from these.
- **The fractions must sum to less than one.** The proof needs $\alpha + \beta < 1$. With groups of $2r + 1$ items, the pivot has at least about $(r+1)/(2(2r+1))$ of the items on each side, so $\beta = 1 - (r+1)/(2(2r+1))$ and $\alpha = 1/(2r+1)$. For groups of five, $\alpha + \beta = 1/5 + 7/10 = 9/10$; for groups of seven, $1/7 + 5/7 = 6/7$. For groups of three, $1/3 + 2/3 = 1$, and the recurrence $T(n) = T(n/3) + T(2n/3) + n$ has the solution $\Theta(n \log n)$, so this proof fails. Chen and Dumitrescu (2015) showed that variants with groups of three and four do run in linear time, with an extra round that refines the pivot.
- **Randomization helps the constant.** A random pivot gives fewer than $4n$ expected comparisons ([expected linear time of randomized selection](/quickselect-expected-linear/)), and random samples give $1.5n + o(n)$ for the median, below the deterministic lower bound of $2n$.

## History

Before 1973 it was not known whether selection, in particular the median, could be done with $O(n)$ comparisons in the worst case; Hoare's FIND of 1961 had a linear average but a quadratic worst case. Blum, Floyd, Pratt, Rivest and Tarjan answered the question in "Time bounds for selection" (1973), with the algorithm PICK and a bound of $5.4305n$ comparisons, and they also gave lower bounds on the number of comparisons. Schönhage, Paterson and Pippenger lowered the upper bound for the median to $3n + o(n)$ in 1976, and Dor and Zwick to $2.95n$ in 1999.

## References
