---
tag: T3NT92
kind: theorem
slug: binomial-coefficient-bounds
name: Binomial coefficient bounds
aliases:
- Binomial bounds
- estimates of n choose k
area: combinatorics/counting-algorithms
level: core
summary: Upper and lower estimates for n choose k, such as (n/k)^k and (en/k)^k, used to bound counts in analyses.
prereqs: [binomial-coefficient, binomial-theorem]
see_also: [stirling-approximation, binary-entropy-function, binomial-tail-bounds, chernoff-bound, counting-argument, binomial-coefficient-computation]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C.1, Counting (Binomial bounds, including the bounds (n/k)^k and (en/k)^k and the entropy bound)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition
    locator: Chapter 11, Section 11.1, The method of types (the bounds 2^(nH(k/n))/(n+1) and 2^(nH(k/n)) on the size of a type class)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Chapter 9, Asymptotics (Stirling's approximation and the estimates of the central binomial coefficient)
---

The binomial coefficient bounds are simple upper and lower estimates for $\binom{n}{k}$ that hold for all $n$ and $k$ in a stated range, not only in the limit. The main ones are $(n/k)^k \le \binom{n}{k} \le (en/k)^k$, the entropy bounds $2^{nH(k/n)}/(n+1) \le \binom{n}{k} \le 2^{nH(k/n)}$, and $4^m/(2\sqrt m) \le \binom{2m}{m} \le 4^m/\sqrt{2m+1}$. They let an analysis replace a [binomial coefficient](/binomial-coefficient/) by a power, which is easy to take logarithms of: in a [counting argument](/counting-argument/), in a union bound over all $k$-subsets, or in the size of a hash table or a code.

## Statement

Notation: $\ln$ is the natural logarithm, $\lg = \log_2$, $e = 2.71828\ldots$, and $H(p) = -p \lg p - (1-p)\lg(1-p)$ for $0 < p < 1$ is the [binary entropy function](/binary-entropy-function/), with $H(0) = H(1) = 0$.

**Theorem.** Let $n$ and $k$ be integers.

1. **(Power bounds.)** If $1 \le k \le n$, then
$$\Bigl(\frac{n}{k}\Bigr)^{k} \;\le\; \binom{n}{k} \;\le\; \frac{n^k}{k!} \;\le\; \Bigl(\frac{en}{k}\Bigr)^{k}.$$
2. **(Entropy bounds.)** If $0 \le k \le n$ and $n \ge 1$, then
$$\frac{2^{nH(k/n)}}{n+1} \;\le\; \binom{n}{k} \;\le\; 2^{nH(k/n)}.$$
3. **(Sums.)** If $1 \le k \le n$, then $\sum_{i=0}^{k} \binom{n}{i} \le (en/k)^k$. If moreover $k \le n/2$, then $\sum_{i=0}^{k} \binom{n}{i} \le 2^{nH(k/n)}$.
4. **(Central coefficient.)** If $m \ge 1$, then
$$\frac{4^m}{2\sqrt{m}} \;\le\; \binom{2m}{m} \;\le\; \frac{4^m}{\sqrt{2m+1}}.$$
5. **(Small $k$.)** If $0 \le k \le n$ and $n \ge 1$, then $\bigl(1 - \frac{k(k-1)}{2n}\bigr)\frac{n^k}{k!} \le \binom{n}{k} \le \frac{n^k}{k!}$. So $\binom{n}{k} \sim n^k/k!$ when $n \to \infty$ and $k^2/n \to 0$.

All parts are exact inequalities about integers and reals; no part depends on a model of computation.

## In plain words

The number of ways to choose a few items from many items is hard to work with directly, because it is a fraction of large factorials. These bounds replace it by a simple power. Choosing a small group from a large crowd gives about "crowd size over group size" options for each member of the group, raised to the group size, give or take a constant factor of about three per member.

For a group that is a fixed fraction of the crowd, the count is close to two raised to the crowd size times a number between zero and one that measures how mixed the choice is. Choosing half of the crowd gives the most options, close to two to the crowd size, divided by a little more than the square root of the crowd size.

## Proof

**Part 1.** Write $\binom{n}{k} = \prod_{i=0}^{k-1} \frac{n - i}{k - i}$. For $0 \le i \le k - 1$, $\frac{n-i}{k-i} \ge \frac{n}{k}$ is equivalent to $k(n - i) \ge n(k - i)$, that is to $in \ge ik$, which holds because $n \ge k$. Multiplying the $k$ factors gives the lower bound. For the middle bound, $\binom{n}{k} = n(n-1)\cdots(n-k+1)/k! \le n^k/k!$. For the last bound, $e^k = \sum_{j \ge 0} k^j/j! \ge k^k/k!$, so $k! \ge (k/e)^k$ and $n^k/k! \le (en/k)^k$.

**Part 2.** For $k = 0$ or $k = n$, $H = 0$ and $\binom{n}{k} = 1$, and $1/(n+1) \le 1 \le 1$. Let $0 < k < n$ and $p = k/n$. Then $p^k (1-p)^{n-k} = 2^{k \lg p + (n-k)\lg(1-p)} = 2^{-nH(p)}$. Let $t_j = \binom{n}{j} p^j (1-p)^{n-j}$. By the [binomial theorem](/binomial-theorem/), $\sum_{j=0}^{n} t_j = (p + 1 - p)^n = 1$, and all $t_j \ge 0$.

- Upper bound: $1 \ge t_k = \binom{n}{k} 2^{-nH(p)}$.
- Lower bound: for $0 \le j < n$, $\frac{t_{j+1}}{t_j} = \frac{(n-j)\,k}{(j+1)(n-k)}$. This is at least 1 exactly when $(n - j)k \ge (j + 1)(n - k)$, which simplifies to $n(j + 1 - k) \le k$, that is to $j + 1 - k \le k/n$. Since $0 < k/n < 1$ and $j$ is an integer, this holds exactly when $j \le k - 1$. So $t_0 \le \cdots \le t_k$ and $t_k \ge t_{k+1} \ge \cdots \ge t_n$, and $t_k$ is the largest of the $n + 1$ terms. Their sum is 1, so $t_k \ge 1/(n+1)$, which gives $\binom{n}{k} \ge 2^{nH(p)}/(n+1)$.

**Part 3.** Let $1 \le k \le n$ and $x = k/n \in (0, 1]$. For $i \le k$, $x^i \ge x^k$, so
$$x^k \sum_{i=0}^{k} \binom{n}{i} \le \sum_{i=0}^{k} \binom{n}{i} x^i \le (1 + x)^n \le e^{xn} = e^k,$$
using the binomial theorem and $1 + x \le e^x$. Divide by $x^k = (k/n)^k$. For the second claim, let $p = k/n \le 1/2$, so $p/(1-p) \le 1$. For $i \le k$, $p^i(1-p)^{n-i} = (1-p)^n (p/(1-p))^i \ge (1-p)^n (p/(1-p))^k = 2^{-nH(p)}$. So $1 \ge \sum_{i \le k} \binom{n}{i} p^i (1-p)^{n-i} \ge 2^{-nH(p)} \sum_{i \le k} \binom{n}{i}$.

**Part 4.** Let $P = \binom{2m}{m}/4^m$. Since $\binom{2m}{m} = \frac{(2m)!}{m!\,m!}$ and $(2m)! = \prod_{i=1}^{m}(2i - 1)(2i)$ with $\prod_{i=1}^{m} 2i = 2^m m!$, we get $P = \prod_{i=1}^{m} \frac{2i-1}{2i}$.

- Upper bound: $\frac{2i-1}{2i} \le \frac{2i}{2i+1}$ because $(2i-1)(2i+1) = 4i^2 - 1 < 4i^2$. So $P^2 \le \prod_{i=1}^{m} \frac{2i-1}{2i} \cdot \frac{2i}{2i+1} = \prod_{i=1}^{m}\frac{2i-1}{2i+1} = \frac{1}{2m+1}$, since the product telescopes.
- Lower bound: for $i \ge 2$, $\frac{2i-1}{2i} \ge \frac{2i-2}{2i-1}$ because $(2i-1)^2 > 2i(2i-2)$. So $P^2 \ge \frac14 \prod_{i=2}^{m} \frac{2i-1}{2i} \cdot \frac{2i-2}{2i-1} = \frac14 \prod_{i=2}^{m} \frac{i-1}{i} = \frac{1}{4m}$.

Taking square roots gives $1/(2\sqrt m) \le P \le 1/\sqrt{2m+1}$.

**Part 5.** The upper bound is part 1. For $k \le 1$ both sides are equal. For $k \ge 2$, $\binom{n}{k} = \frac{n^k}{k!}\prod_{i=0}^{k-1}\bigl(1 - \frac{i}{n}\bigr)$, and for numbers $a_i \in [0, 1]$, $\prod (1 - a_i) \ge 1 - \sum a_i$ (by induction: $(1 - s)(1 - a) \ge 1 - s - a$ when $s, a \ge 0$ and $1 - s \ge 0$; when $1 - s < 0$ the bound is negative and holds trivially). With $\sum_{i<k} i/n = k(k-1)/(2n)$ this gives the lower bound. $\blacksquare$

### Worked numbers

For $n = 20$ and $k = 5$, $\binom{20}{5} = 15504$, and the bounds of part 1 are $4^5 = 1024$, $20^5/5! \approx 26667$ and $(4e)^5 \approx 151975$. The entropy bounds, with $H(1/4) \approx 0.8113$, are about $3649$ and $76627$. The sum $\sum_{i \le 5}\binom{20}{i} = 21700$ is below both bounds of part 3. For $m = 10$, $\binom{20}{10} = 184756$ lies between $4^{10}/(2\sqrt{10}) \approx 165794$ and $4^{10}/\sqrt{21} \approx 228818$. For $n = 1000$ and $k = 10$, $\binom{n}{k} / (n^k/k!) \approx 0.9559$, and part 5 gives at least $0.955$.

## Consequences

- **Logarithms.** Part 1 gives $\lg \binom{n}{k} = k \lg(n/k) + O(k)$ for $1 \le k \le n$. So a $k$-subset of $[n]$ needs about $k \lg(n/k)$ bits to encode, which is the [information-theoretic bound](/information-theoretic-bound/) for sets and the space of succinct dictionaries.
- **Union bounds over subsets.** A typical analysis bounds a probability by a sum over all $k$-subsets, each with probability $q^k$. Part 1 turns $\binom{n}{k} q^k$ into $(enq/k)^k$, which is small once $k > e n q$. This is how the size of the largest bucket in hashing and the maximum load in balls into bins are bounded.
- **Entropy and codes.** Part 2 says that $\lg \binom{n}{pn} = nH(p) + O(\log n)$. The number of bit strings of length $n$ with $pn$ ones is about $2^{nH(p)}$, the basis of the method of types (Cover and Thomas, Section 11.1) and of the Hamming bound for codes. Part 3 bounds the volume of a Hamming ball of radius $pn$ by $2^{nH(p)}$ for $p \le 1/2$.
- **Tails of the binomial distribution.** Part 3 is a tail bound for a fair coin: $\Pr[\text{at most } k \text{ heads in } n \text{ tosses}] \le 2^{-n(1 - H(k/n))}$ for $k \le n/2$. See [binomial tail bounds](/binomial-tail-bounds/) and the [Chernoff bound](/chernoff-bound/).
- **Central coefficients.** Part 4 shows that $\binom{2m}{m} = \Theta(4^m/\sqrt m)$. The [Catalan number](/catalan-numbers/) $\binom{2m}{m}/(m+1)$ is therefore $\Theta(4^m / m^{3/2})$, and $\binom{2m}{m}$ has $2m - \tfrac12 \lg m + O(1)$ bits, which sets the cost of exact [computation](/binomial-coefficient-computation/).
- **Merging.** The lower bound for merging two sorted lists of length $m$ is $\lceil \lg \binom{2m}{m} \rceil \ge 2m - \tfrac12 \lg m - 1$ comparisons, from part 4 and the [counting argument](/counting-argument/).

## Tightness

- **Part 1, lower bound.** Equality holds for $k = 1$ and $k = n$. For fixed $k \ge 2$ and $n \to \infty$, $\binom{n}{k}/(n/k)^k \to k^k/k!$, so the bound loses a factor of about $e^k/\sqrt{2\pi k}$ by [Stirling's approximation](/stirling-approximation/).
- **Part 1, upper bound.** For fixed $k$ and $n \to \infty$, $\binom{n}{k}/(en/k)^k \to k^k/(e^k k!) \sim 1/\sqrt{2\pi k}$. So the factor $e$ in $(en/k)^k$ cannot be replaced by any smaller constant $c$: $(cn/k)^k/\binom{n}{k}$ tends to $(c/e)^k\sqrt{2\pi k}$, which is less than 1 for large $k$ when $c < e$.
- **Part 2.** The exponent $nH(k/n)$ is exact up to $O(\log n)$, but the factor $1/(n+1)$ is not: the true ratio $\binom{n}{k}/2^{nH(k/n)}$ is $\Theta(1/\sqrt{n})$ for $k/n$ in a fixed closed subinterval of $(0, 1)$, by Stirling's approximation.
- **Part 4.** Both bounds have the correct order $4^m/\sqrt m$. The true value is $\binom{2m}{m} \sim 4^m/\sqrt{\pi m}$, with $1/\sqrt\pi \approx 0.564$ between the constants $1/2$ and $1/\sqrt 2 \approx 0.707$ of the bounds.
- **Part 5.** The condition $k^2/n \to 0$ is needed: for $k = \sqrt n$, $\prod_{i<k}(1 - i/n) \to e^{-1/2}$, so the ratio does not tend to 1.

## History

The power bounds and the entropy bound are folklore of combinatorics and information theory; CLRS (Appendix C.1) collects them for the analysis of algorithms, and Cover and Thomas (Chapter 11) use the entropy form for the method of types. The precise asymptotics come from Stirling's formula for $n!$ (Concrete Mathematics, Chapter 9).

## References
