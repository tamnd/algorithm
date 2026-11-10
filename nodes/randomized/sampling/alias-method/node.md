---
tag: 95DG3T
kind: algorithm
slug: alias-method
name: Alias method
aliases:
- Walker's alias method
- Vose's alias method
area: randomized/sampling
level: core
summary: Preprocess n weights in O(n) time so that each weighted sample takes O(1) time.
solves: [weighted-sampling]
model: word-ram
complexity:
  vars: {n: the number of weights}
  time: {build: Θ(n), query: Θ(1), worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: false, exact: true, online: false, recursive: false}
history:
  year: 1974
  people: [Alastair J. Walker, Michael D. Vose]
  note: Walker published the method in 1974 and 1977. Vose gave the linear-time construction in 1991.
prereqs: [weighted-sampling, discrete-probability-distribution, uniform-distribution]
see_also: [inverse-transform-sampling, rejection-sampling, gumbel-max-trick, weighted-reservoir-sampling, random-variate-generation, fenwick-tree, prefix-sums, binary-search]
sources:
  - paper: "Alastair J. Walker, New fast method for generating discrete random numbers with arbitrary frequency distributions, Electronics Letters 10(8), 1974"
    locator: pages 127 to 128
  - paper: doi:10.1145/355744.355749
    title: Alastair J. Walker, An efficient method for generating discrete random variables with general distributions, ACM Transactions on Mathematical Software 3(3), 1977
    locator: pages 253 to 256
  - paper: doi:10.1109/32.92917
    title: Michael D. Vose, A linear algorithm for generating random numbers with a given distribution, IEEE Transactions on Software Engineering 17(9), 1991
    locator: pages 972 to 975 (the O(n) setup with the small and large lists)
  - book: isbn:9780387963051
    title: Luc Devroye, Non-Uniform Random Variate Generation, Springer, 1986
    locator: Chapter III, Section 4 (the alias method and the alias-urn method)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 3.4.1 (the alias method for discrete distributions)
---

The alias method draws an index $i \in \{0, \ldots, n-1\}$ with probability $w_i / W$, where $W = \sum_j w_j$, in $O(1)$ time per draw after $O(n)$ preprocessing. It solves the [weighted sampling](/weighted-sampling/) problem with replacement. The table has one column for each index, and each column holds at most two indices: the index itself and one *alias*. A draw picks a column uniformly and then one of its two entries with a biased coin. Walker invented the method, and Vose gave the simple linear-time construction that is used today.

## In plain words

Think of a bar chart with one bar for each item, where the height of a bar is the weight of its item. Scale the chart so that the average height is one. Some bars are taller than one, and some are shorter.

Now cut pieces from the tall bars and put them on top of the short bars, until each bar has height exactly one. Do it so that each bar gets a piece from at most one other bar. Then each bar has at most two colors: its own color at the bottom, and the color of one other item at the top.

To draw an item, pick one bar at random, all bars equally likely. Then pick a random height in that bar. Return the color at that height. Each draw costs two random numbers and one comparison, for any number of items.

## The problem

The input is a list of $n \ge 1$ non-negative weights $w_0, \ldots, w_{n-1}$ with $W = \sum_i w_i > 0$. Each query must return an index $i$ with probability $w_i / W$, independently of the other queries. This is the [weighted sampling](/weighted-sampling/) problem, in the form with replacement.

Notation: $n$ is the number of items, $\Pr$ is probability. The model is the [word RAM](/word-ram/) with a source of independent uniform integers: a call RANDOM-INT$(m)$ returns each of $0, \ldots, m-1$ with probability $1/m$. A source of random bits gives such an integer by rejection: draw $\lceil \lg m \rceil$ bits and try again if the value is at least $m$, which takes at most $2 \lceil \lg m \rceil$ bits in expectation, because each attempt succeeds with probability $m / 2^{\lceil \lg m \rceil} > 1/2$.

## The algorithm

The weights are integers here. Rational weights are first scaled by their common denominator. All arithmetic is then exact. Line L1 scales each weight by $n$, so that the average scaled weight is exactly $W$, and $W$ plays the role of the height "one".

```pseudo id=main
ALIAS-BUILD(w[0 .. n − 1])                ▷ integer weights, sum W > 0
L1  W ← w[0] + ... + w[n − 1];  q[i] ← n · w[i] for each i
L2  small ← [i : q[i] < W];  large ← [i : q[i] ≥ W]
L3  while small ≠ ∅ and large ≠ ∅ do
L4      l ← POP(small);  g ← POP(large)
L5      prob[l] ← q[l];  alias[l] ← g      ▷ column l is finished
L6      q[g] ← q[g] − (W − q[l])           ▷ g gave W − q[l] to column l
L7      if q[g] < W then PUSH(small, g) else PUSH(large, g)
L8  for each i still in large or small do prob[i] ← W;  alias[i] ← i
L9  return (prob, alias, W)

ALIAS-SAMPLE(prob, alias, W)
L10 i ← RANDOM-INT(n)                     ▷ the column
L11 t ← RANDOM-INT(W)                     ▷ the height in the column
L12 if t < prob[i] then return i else return alias[i]
```

The lists *small* and *large* can be stacks or queues. Each iteration of the loop finishes one short column $l$. It fills the top $W - q_l$ of the column with item $g$, a column that is at least full, and lowers $q_g$ by the same amount. Column $g$ can become short. Then it goes to *small* and is finished later with an alias of its own. At the end, each column that is left is exactly full, so line L8 gives it no alias.

## Example

Take $w = [1, 2, 3, 4, 6]$, so $n = 5$ and $W = 16$. Line L1 gives $q = [5, 10, 15, 20, 30]$. Line L2 gives *small* $= [0, 1, 2]$ and *large* $= [3, 4]$, used as stacks.

| step | $l$ | $g$ | set | new $q_g$ | small | large |
|---|---|---|---|---|---|---|
| start | | | | | [0, 1, 2] | [3, 4] |
| 1 | 2 | 4 | prob[2] = 15, alias[2] = 4 | $30 - 1 = 29$ | [0, 1] | [3, 4] |
| 2 | 1 | 4 | prob[1] = 10, alias[1] = 4 | $29 - 6 = 23$ | [0] | [3, 4] |
| 3 | 0 | 4 | prob[0] = 5, alias[0] = 4 | $23 - 11 = 12$ | [4] | [3] |
| 4 | 4 | 3 | prob[4] = 12, alias[4] = 3 | $20 - 4 = 16$ | [ ] | [3] |
| L8 | | | prob[3] = 16, alias[3] = 3 | | | |

The table is $\mathit{prob} = [5, 10, 15, 16, 12]$ and $\mathit{alias} = [4, 4, 4, 3, 3]$. Each of the $5 \cdot 16 = 80$ pairs $(i, t)$ of lines L10 and L11 is equally likely. Item 4 gets $12$ pairs from its own column and $11 + 6 + 1 = 18$ pairs from columns 0, 1 and 2, so $30$ pairs, and $30/80 = 6/16$. Item 3 gets $16 + 4 = 20$ pairs, and $20/80 = 4/16$. Items 0, 1 and 2 get $5$, $10$ and $15$ pairs. These are exactly $w_i / W$.

## Correctness

The key fact is an invariant of the loop of line L3. Let $A$ be the set of columns that are not finished. Then $\sum_{i \in A} q_i = |A| \cdot W$, and for each item $j$ the mass that the finished columns give to $j$, plus $q_j$ when $j \in A$, is $n w_j$. Each iteration finishes one column and moves exactly $W$ out of the sum, so the invariant holds. When the loop stops, *small* must be empty: if only short columns were left, their sum would be below $|A| W$. So each column that is left has $q_i = W$ exactly. Then each item $j$ gets exactly $n w_j$ of the $nW$ equally likely pairs $(i, t)$, which gives the probability $w_j / W$. The full proof, with the existence of the table and the bound on the steps, is in the proof below.

The method is exact in this form: with integer weights and exact uniform integers, the probabilities are exactly $w_i / W$, with no rounding.

## Complexity

- **Build.** Lines L1, L2 and L8 take $\Theta(n)$. Each iteration of the loop finishes one column, and the last column is never finished in the loop, so there are at most $n - 1$ iterations of $O(1)$ each. The build takes $\Theta(n)$ time in the worst case. The integers have at most $\lceil \lg(nW) \rceil + 1$ bits.
- **Sample.** Lines L10 to L12 take $O(1)$ time and two uniform integers. The cost does not depend on the weights.
- **Space.** Two arrays of $n$ entries.
- **Random bits.** With a source of random bits and rejection, a sample uses at most $2(\lceil \lg n \rceil + \lceil \lg W \rceil)$ bits in expectation. One draw of $s = $ RANDOM-INT$(nW)$, with $i = \lfloor s / W \rfloor$ and $t = s \bmod W$, gives the same pair and needs at most $\lceil \lg (nW) \rceil$ bits in each attempt.

No method can build a table in $o(n)$ time in general, because it must read each weight: a weight that is not read could be the only positive one.

## Properties

- **Exact** with integer or rational weights and exact uniform integers.
- **Static.** A change of one weight changes $W$ and the scale of all columns, so the table must be rebuilt in $\Theta(n)$ time.
- **With replacement.** The draws are independent. The method does not give a sample without replacement.
- **Not unique.** Many correct tables exist for the same weights. The order of the stacks in line L4 changes the table, but not the law of a sample.

## Variants and improvements

- **Float tables.** Most libraries store $\mathit{prob}[i]$ as a float in $[0, 1]$ and compare it with a uniform float. Line L6 then rounds, and the loop can end with a column in *small* whose value is a little below 1. Vose sets such columns to 1. The law of a sample is then off by the rounding errors of line L6, which add up over the updates of one column. The comparison with a uniform float on a grid of $2^{-53}$ also rounds each $\mathit{prob}[i]$ to that grid.
- **One uniform for both draws.** Some code takes $U$ uniform in $[0, 1)$, uses $i = \lfloor nU \rfloor$, and uses the fraction $nU - i$ as the second uniform. This saves a call but loses $\lg n$ bits of the second uniform.
- **Alias-urn method.** Devroye describes a version with more columns than items, where most columns hold one item only, so that most draws need one uniform.
- **Prefix sums with a search.** Store the [prefix sums](/prefix-sums/) and do a [binary search](/binary-search/) for a uniform $t \in [0, W)$. This is [inverse transform sampling](/inverse-transform-sampling/) on a discrete law. A draw costs $O(\log n)$, but a [Fenwick tree](/fenwick-tree/) of the weights allows an update of one weight in $O(\log n)$.
- **Sampling without replacement.** Use the [Gumbel-max trick](/gumbel-max-trick/) in its top-$k$ form, or [weighted reservoir sampling](/weighted-reservoir-sampling/).

## When to use it

Use the alias method when the weights are fixed and you need many draws: after $\Theta(n)$ setup, $m$ draws cost $\Theta(n + m)$. A sequential search costs $O(n)$ for each draw, which is better only for very few draws. A binary search over prefix sums costs $O(\log n)$ per draw, and it is the right choice when the weights change between draws. For one draw, a linear scan is simplest. For a weighted sample without replacement, the alias method does not apply.

## Pitfalls

- **Forgetting the scale by $n$.** Line L1 must use $q_i = n w_i$, with the threshold $W$. With $q_i = w_i$ and the same threshold, the columns hold the wrong mass, and the law is wrong.
- **Leftover columns in floating point.** In a float version, the loop of line L3 can stop with *small* not empty. If line L8 handles only *large*, those columns keep an undefined $\mathit{prob}[i]$. Line L8 must set every column that is left, in both lists.
- **Modulo bias.** Line L11 needs a uniform integer in $[0, W)$. The expression `rand32() % W` is not uniform unless $W$ divides $2^{32}$. Use rejection.
- **Float index.** The code `int(n * random())` maps $2^{53}$ equally likely floats onto $n$ columns, so the columns get unequal shares unless $n$ divides $2^{53}$. The bias grows with $n$. Use an integer draw for line L10.

## Implementations

## History

Walker published the method in Electronics Letters in 1974 and in ACM Transactions on Mathematical Software in 1977. Vose (1991) gave the construction with two lists that runs in $O(n)$ time, together with a treatment of its rounding errors. Knuth and Devroye both present the method in their books on random number generation.

## References
