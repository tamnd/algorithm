---
tag: D3C8ZM
kind: concept
slug: geometric-series
name: Geometric series
aliases:
- geometric progression sum
area: foundations/asymptotic-analysis
level: intro
summary: The sum of a geometric progression, which for a constant positive ratio other than one is within a constant factor of its largest term.
prereqs: [asymptotic-notation]
see_also: [arithmetic-series, harmonic-series, dynamic-array, master-theorem, binary-heap, heapsort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix A, Section A.1, Summation formulas and properties (geometric series and the differentiated series); Section 6.3, Building a heap
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 2.3, Manipulation of sums (the perturbation method applied to the geometric sum and to the sum of k 2^k)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.3, Sums and Products (the sum of a geometric progression)
---

A geometric series is the sum of the terms of a geometric progression: a list $a, ar, ar^2, \dots$ in which each term is the previous term times a fixed ratio $r$. For $r \ne 1$ the sum of the first $n+1$ terms of $1, r, r^2, \dots$ is $(r^{n+1} - 1)/(r - 1)$. When $r$ is a positive constant other than 1, the sum is $\Theta$ of its largest term, in [asymptotic notation](/asymptotic-notation/). This rule gives many bounds in the analysis of algorithms in one line.

## In plain words

Take a stick of length 1. Cut off half of it, then half of what is left, then half again. The pieces have lengths 1/2, 1/4, 1/8, and so on. All the pieces together never pass the original length 1. A sum in which each term is a fixed fraction of the previous term is small: it is at most a constant times the first term.

Now reverse the direction. Each term is twice the previous one. The last term is then larger than all the earlier terms together. So the sum is less than twice the last term. In both cases one end of the sum decides the size of the whole sum, and the other terms add only a constant factor.

## The idea

**Finite sum.** For each real $r \ne 1$ and each integer $n \ge 0$,

$$ \sum_{k=0}^{n} r^k = \frac{r^{n+1} - 1}{r - 1}. $$

For $r = 1$ the sum is $n + 1$. With a first term $a$, each term is multiplied by $a$, so $\sum_{k=0}^{n} a r^k = a\,(r^{n+1} - 1)/(r - 1)$ for $r \ne 1$. The factor $a$ does not change the rule below.

*Proof.* Let $S = \sum_{k=0}^{n} r^k$. Then $rS = \sum_{k=1}^{n+1} r^k$. The two sums share the terms $r^1, \dots, r^n$. So $rS - S = r^{n+1} - r^0$, that is $(r - 1)S = r^{n+1} - 1$. Divide by $r - 1$, which is not zero. $\square$

**Infinite sum.** For real $r$ with $|r| < 1$, $r^{n+1} \to 0$ when $n \to \infty$. So the partial sums converge and

$$ \sum_{k=0}^{\infty} r^k = \frac{1}{1 - r}. $$

For real $r$ with $|r| \ge 1$ the terms do not tend to 0 and the series diverges. A common case is $\sum_{k \ge 0} 2^{-k} = 2$, with ratio $1/2$.

**The largest term rule.** Let $r$ be a constant with $r > 0$ and $r \ne 1$, and let $S_n = \sum_{k=0}^{n} r^k$.

- If $r > 1$, then $r^n \le S_n < \frac{r}{r-1}\, r^n$. So $S_n = \Theta(r^n)$, the last term.
- If $r < 1$, then $1 \le S_n < \frac{1}{1-r}$. So $S_n = \Theta(1)$, the first term.

*Proof.* Each term is positive, so $S_n$ is at least its largest term. This is $r^n$ if $r > 1$ and $r^0 = 1$ if $r < 1$. For $r > 1$, the closed form gives $S_n = (r^{n+1} - 1)/(r-1) < r^{n+1}/(r-1)$. For $r < 1$, the infinite sum bounds the partial sum: $S_n < 1/(1-r)$. $\square$

The constants depend on $r$. They grow when $r$ comes close to 1: for $r = 2$ the factor is 2, for $r = 1.01$ it is about 101.

**Bounding by a geometric series.** A series that is not exactly geometric can still be bounded by one. If $a_k \ge 0$ and $a_{k+1} \le r\,a_k$ for each $k$, with a constant $0 < r < 1$, then $a_k \le a_0 r^k$ by induction, so $\sum_{k \ge 0} a_k \le a_0/(1-r)$. For example, in $\sum_{k \ge 1} k/3^k$ the ratio of consecutive terms is $(k+1)/(3k) \le 2/3$, so the sum is at most $(1/3)/(1 - 2/3) = 1$. The exact value is $3/4$.

**The weighted sum $\sum k/2^k$.** For $\sum_{k \ge 1} k\, 2^{-k}$ there is a short proof with no calculus. Write $k = \sum_{j=1}^{k} 1$. Then $\sum_{k \ge 1} k\,2^{-k} = \sum_{j \ge 1} \sum_{k \ge j} 2^{-k}$, where the order of summation can change because all terms are non-negative. The inner sum is $2^{1-j}$ by the infinite geometric sum. So the total is $\sum_{j \ge 1} 2^{1-j} = 2$. The same exchange of sums gives the general form: for $|x| < 1$, the inner sum is $\sum_{k \ge j} x^k = x^j/(1-x)$, so $\sum_{k \ge 0} k\,x^k = \sum_{j \ge 1} x^j/(1-x) = x/(1-x)^2$. The exchange is valid for negative $x$ too, because the series converges absolutely.

**The finite weighted sum.** The same exchange works for a finite sum. For $n \ge 0$,
$$ \sum_{k=1}^{n} \frac{k}{2^k} = 2 - \frac{n+2}{2^n}. $$
*Proof.* By induction on $n$. For $n = 0$ both sides are 0. If the formula holds for $n$, then adding the term $(n+1)/2^{n+1}$ gives $2 - \frac{2(n+2) - (n+1)}{2^{n+1}} = 2 - \frac{n+3}{2^{n+1}}$, which is the formula for $n + 1$. $\square$

So the partial sums approach 2 from below, and the gap $(n+2)/2^n$ falls fast: it is $0.0117$ at $n = 10$.

## Examples

**Exact values.** For $r = 3$ and $n = 5$: $1 + 3 + 9 + 27 + 81 + 243 = 364 = (3^6 - 1)/2$. For $r = 2$ and $n = 4$: $1 + 2 + 4 + 8 + 16 = 31 = 2^5 - 1$.

**Negative ratio.** For $r = -2$ and $n = 5$: $1 - 2 + 4 - 8 + 16 - 32 = -21 = ((-2)^6 - 1)/(-3)$. The closed form holds, but the largest term rule does not apply: the terms cancel, and the sum can be much smaller than its largest term in absolute value. With one more term the sum is $43$.

**Bounding a sum that is not geometric.** In $\sum_{k \ge 1} k/3^k$ the ratio bound gives at most $1$. The exact value from $x/(1-x)^2$ at $x = 1/3$ is $(1/3)/(4/9) = 3/4$.

**Non-example.** The rule needs a constant ratio. Take $r = 1 + 1/n$ with $n + 1$ terms. The last term is $(1 + 1/n)^n < e$, but the sum is $n\big((1 + 1/n)^{n+1} - 1\big)$, which is about $(e - 1)\,n$. So the sum is $\Theta(n)$ while the largest term is $\Theta(1)$. The sum of a series with $r = 1$ is also not covered: it is $n + 1$, and each term is the largest. For $n = 100$ the sum with $r = 1 + 1/n$ is $173.19$, against the estimate $(e-1)n = 171.83$, while the largest term is $2.70$. The ratio $r = 1 - 1/n$ fails in the same way: the sum is $n\big(1 - (1 - 1/n)^{n+1}\big)$, which is about $(1 - 1/e)\,n$, and for $n = 100$ it is $63.76$.

### Pitfalls

- **A ratio that depends on $n$.** The constants $\frac{r}{r-1}$ and $\frac{1}{1-r}$ blow up when $r$ tends to 1. A bound such as "the sum is $O(\text{largest term})$" is valid only when $r$ stays at a fixed distance from 1. The non-examples above show the failure.
- **Off by one in the number of terms.** $\sum_{k=0}^{n} r^k$ has $n + 1$ terms, and its closed form has the exponent $n + 1$. Writing $(r^n - 1)/(r - 1)$ for it loses the last term. The sum $1 + 2 + \dots + 2^m$ is $2^{m+1} - 1$, not $2^m - 1$.
- **The case $r = 1$.** The closed form divides by zero. The sum is $n + 1$, and it must be handled as a separate case. This is the source of the extra $\log n$ factor in the middle case of the master theorem.
- **Negative or complex ratios.** The closed form holds, but the sum is not $\Theta$ of its largest term, because terms cancel. Use $|r|$ for an upper bound: $\big|\sum_{k=0}^n r^k\big| \le \sum_{k=0}^n |r|^k$.
- **The infinite sum for $|r| \ge 1$.** The formula $1/(1-r)$ is meaningless there. For example, $\sum_{k \ge 0} 2^k$ is not $-1$ in the real numbers; the series diverges.
- **A ratio that holds only from some point.** If $a_{k+1} \le r\,a_k$ holds only for $k \ge k_0$, the bound is $\sum_{k < k_0} a_k + a_{k_0}/(1-r)$. The first terms must be added separately.

## Where it is used

**Array doubling.** A [dynamic array](/dynamic-array/) starts with capacity 1 and doubles its capacity when it is full. The copies happen at sizes $1, 2, 4, \dots, 2^m$, where $m$ is the integer with $2^m < n \le 2^{m+1}$ (for $n \ge 2$). The total number of copied items is $2^{m+1} - 1 < 2n$. For example, 17 appends copy $1 + 2 + 4 + 8 + 16 = 31$ items, and $31 < 34$. So the copies cost $O(1)$ per append on average over the sequence, which is an [amortized](/amortized-cost/) bound.

**Recursion trees.** Sum the cost of a [recursion tree](/recursion-tree-method/) level by level. Often the level costs form a geometric progression, and the rule gives the answer from one end.

- For $T(n) = 2T(n/2) + n^2$ the cost of level $i$ is $2^i (n/2^i)^2 = n^2/2^i$. The ratio is $1/2$, so the sum over $i = 0, \dots, \lg n$ is at most $2n^2$ and at least $n^2$. The root decides: $T(n) = \Theta(n^2)$.
- For $T(n) = 3T(n/2) + n$ the cost of level $i$, for $i = 0, \dots, \lg n$, is $n(3/2)^i$. The ratio is $3/2$, so the last level decides. It costs $n (3/2)^{\lg n} = n^{\lg 3}$, so $T(n) = \Theta(n^{\lg 3})$.
- When the ratio is exactly 1 each level costs the same, and the total is the number of levels times the cost of one level. This is the middle case of the [master theorem](/master-theorem/).

**Building a heap.** The bottom-up construction of a [binary heap](/binary-heap/) calls a sift-down at each internal node. A node of height $h$ costs at most $h$ swaps. A heap of $n$ nodes has at most $\lceil n/2^{h+1} \rceil$ nodes of height $h$, and for $0 \le h \le \lfloor \lg n \rfloor$ this is at most $n/2^h$, because $n/2^{h+1} \ge 1/2$ and $\lceil x \rceil \le 2x$ for $x \ge 1/2$. So the total number of swaps is at most
$$ \sum_{h=0}^{\lfloor \lg n \rfloor} \frac{n}{2^h}\, h \;\le\; n \sum_{h \ge 0} \frac{h}{2^h} = 2n. $$
The build takes $O(n)$ time, not the $O(n \log n)$ that the bound $h \le \lg n$ for each node suggests. For $n = 1000$ the heights of all nodes in the heap add up to $994$, below the bound $2n = 2000$. The first phase of [heapsort](/heapsort/) uses this.

## References
