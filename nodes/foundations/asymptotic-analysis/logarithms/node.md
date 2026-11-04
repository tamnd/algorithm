---
tag: CBSPT6
kind: concept
slug: logarithms
name: Logarithms
aliases:
- logarithmic functions
- log identities
area: foundations/asymptotic-analysis
level: intro
summary: Logarithm laws and base conversion, which are needed to manipulate logarithmic bounds.
prereqs: []
see_also: [logarithmic-time, iterated-logarithm, order-of-growth, binary-search, floor-log2, stirling-approximation]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 3.3, Standard notations and common functions (logarithms)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.2, Numbers, Powers, and Logarithms
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 3, Integer Functions (floors and ceilings of logarithms), and Chapter 9, Asymptotics
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms
---

The logarithm to base $b$ of a positive number $x$ is the exponent to which $b$ must be raised to give $x$. It is the inverse of exponentiation, and the logarithm to base 2 of an integer counts, after rounding down, how many times the integer can be halved before it reaches 1. Logarithms appear in the cost of [binary search](/binary-search/), of [balanced search trees](/balanced-binary-search-tree/) and of the best [comparison sorts](/sorting-problem/). This page fixes the notation of the site and proves the rules that the other pages use.

## In plain words

Count how many times you can cut 1000 in half, rounding down, before you reach 1. The numbers are 1000, 500, 250, 125, 62, 31, 15, 7, 3, 1. That is 9 cuts. Doubling the input adds only one more cut. A logarithm measures this count.

One more than this count is the number of binary digits of the number. The count itself is the height of a complete binary tree with that many nodes. So an algorithm that throws away half of the input with a fixed amount of work at each step, or that walks down a balanced tree, has a cost that grows like a logarithm.

A logarithm has no upper limit, but it grows more slowly than any power of the input size with a positive exponent. The square root of a million is 1000, but a million can be halved only 19 times.

## The idea

### Definition and notation

Let $b > 0$ with $b \ne 1$, and let $x > 0$. The number $\log_b x$ is the unique real number $y$ with $b^y = x$. It exists and is unique because the function $y \mapsto b^y$ is continuous and strictly monotone (increasing for $b > 1$, decreasing for $b < 1$), and it maps the real line onto the positive reals. The logarithm of 0 or of a negative number is not defined.

The site uses three names, as Cormen, Leiserson, Rivest and Stein (CLRS) do.

- $\lg x$ means $\log_2 x$.
- $\ln x$ means $\log_e x$, the natural logarithm, with $e = 2.71828\ldots$
- $\log x$ without a base appears only inside $O$, $\Omega$ and $\Theta$, where the base does not matter (see below). Outside them, a page writes $\lg$ or $\ln$.

Other texts use $\log$ for base 10 or for base $e$. When $\log$ appears outside a bound, check the convention of the text.

Powers and compositions have their own notation:

- $\lg^k n$ means $(\lg n)^k$, a power.
- $\lg\lg n$ means $\lg(\lg n)$, and $\lg^{(i)} n$ means $\lg$ applied $i$ times. Do not confuse $\lg^{(i)} n$ with $\lg^i n$.
- $\lg n^k$ means $\lg(n^k)$, and $\lg n + k$ means $(\lg n) + k$.

### The rules

Let $b$, $x$, $y$ be positive, with $b \ne 1$, and let $r$ be real.

1. **Inverse.** $b^{\log_b x} = x$, and $\log_b(b^r) = r$.
2. **Product.** $\log_b(xy) = \log_b x + \log_b y$.
3. **Power.** $\log_b(x^r) = r \log_b x$.
4. **Quotient.** $\log_b(x/y) = \log_b x - \log_b y$.
5. **Change of base.** For $a > 0$ with $a \ne 1$: $\log_b x = \dfrac{\log_a x}{\log_a b}$.
6. **Swap.** $x^{\log_b y} = y^{\log_b x}$.
7. **Monotonicity.** If $b > 1$ and $0 < x < y$, then $\log_b x < \log_b y$.

*Proof.* Rule 1 is the definition. For rule 2, put $s = \log_b x$ and $t = \log_b y$. Then $xy = b^s b^t = b^{s+t}$, so $\log_b(xy) = s + t$. For rule 3, $x^r = (b^s)^r = b^{rs}$, so $\log_b(x^r) = rs$. Rule 4 follows from rules 2 and 3 with $x/y = x \cdot y^{-1}$. For rule 5, take $\log_a$ of $x = b^s$ and use rule 3: $\log_a x = s \log_a b$. The number $\log_a b$ is not 0, because $b \ne 1 = a^0$, so $s = \log_a x/\log_a b$. For rule 6, by rules 1 and 3 both sides equal $b^{\log_b x \cdot \log_b y}$. For rule 7, if $\log_b x \ge \log_b y$ then $x = b^{\log_b x} \ge b^{\log_b y} = y$, since $t \mapsto b^t$ is increasing for $b > 1$. $\square$

A special case of rule 5 is $\log_b a \cdot \log_a b = 1$, from $x = a$.

### The base does not matter inside $O$

By rule 5, $\log_a n = c \cdot \log_b n$ with $c = 1/\log_b a$, a positive constant when $a, b > 1$. So $\log_a n = \Theta(\log_b n)$, and $O(\log n)$ needs no base. For example, $\lg n = \ln n/\ln 2 = 1.4427\ldots \cdot \ln n$.

Rule 3 gives a second fact: for each constant $k > 0$, $\log(n^k) = k\log n = \Theta(\log n)$. So $O(\log(n^2)) = O(\log n)$. A power of the logarithm is different: $(\log n)^2 \notin O(\log n)$, because the ratio is $\log n$, which is unbounded.

The base matters in three places: in an exponent (see the examples), in [tilde notation](/tilde-notation/), where $\lg n \not\sim \ln n$, and in an exact count, such as the number of bits.

### Two inequalities

For each real $x > -1$,
$$\frac{x}{1+x} \le \ln(1 + x) \le x,$$
with equality only at $x = 0$.

*Proof.* Let $\varphi(y) = y - 1 - \ln y$ for $y > 0$. Then $\varphi'(y) = 1 - 1/y$, which is negative for $y < 1$ and positive for $y > 1$. So $\varphi$ has its minimum $\varphi(1) = 0$, and $\ln y \le y - 1$ with equality only at $y = 1$. Put $y = 1 + x$ for the right inequality. Put $y = 1/(1+x)$ for the left: $-\ln(1+x) \le 1/(1+x) - 1 = -x/(1+x)$. $\square$

With $x = 1/n$ this gives $\frac{1}{n+1} \le \ln(n+1) - \ln n \le \frac1n$. So the logarithm grows by about $1/n$ from $n$ to $n + 1$, and $\lg(n + 1) = \lg n + O(1/n)$. This is the step behind the bounds on the [harmonic series](/harmonic-series/).

### Floors of $\lg$

Let $n \ge 1$ be an integer and $k = \lfloor \lg n \rfloor$. By rule 7 and the definition of the floor, $2^k \le n < 2^{k+1}$.

- **Halving.** Start with $n$ and replace it by $\lfloor n/2 \rfloor$ until it is 1. This takes exactly $k$ steps. In binary, $\lfloor n/2 \rfloor$ drops the last digit, and $n$ has $k+1$ digits, so $k$ steps leave the single digit 1.
- **Bits.** The binary form of $n$ has exactly $k + 1 = \lfloor \lg n \rfloor + 1$ digits, because $2^k \le n < 2^{k+1}$. This also equals $\lceil \lg(n+1) \rceil$, because $2^k < n + 1 \le 2^{k+1}$. For $n = 10^6$ both give 20, since $\lg 10^6 = 19.93\ldots$
- **Tree height.** A binary tree with $n$ nodes has height at least $\lfloor \lg n \rfloor$. A tree of height $h$ has at most $2^{h+1} - 1$ nodes, so $n < 2^{h+1}$, which gives $\lg n < h + 1$ and $\lfloor \lg n \rfloor \le h$. A complete binary tree, such as the tree of a [binary heap](/binary-heap/), has exactly this height.

### Slower than any positive power

**Claim.** For each real $\varepsilon > 0$, $\lg n = o(n^{\varepsilon})$, and for each real $k > 0$, $(\lg n)^k = o(n^{\varepsilon})$.

*Proof.* By the inequality $\ln y \le y - 1$ with $y = n^{\varepsilon/2}$, we get $\frac{\varepsilon}{2}\ln n \le n^{\varepsilon/2} - 1 < n^{\varepsilon/2}$. So for $n \ge 1$,
$$0 \le \frac{\ln n}{n^{\varepsilon}} < \frac{2}{\varepsilon}\, n^{-\varepsilon/2} \to 0.$$
Since $\lg n = \ln n/\ln 2$, this gives $\lg n = o(n^\varepsilon)$. For the power, apply this with $\varepsilon/k$ in place of $\varepsilon$: $\lg n/n^{\varepsilon/k} \to 0$, and raising to the power $k$ keeps the limit 0. $\square$

So $n^{\varepsilon} \notin O(\lg n)$ for each $\varepsilon > 0$. The limit can be reached late when $\varepsilon$ is small or $k$ is large. For $\varepsilon = \frac12$ and $k = 1$, the ratio $\lg n/\sqrt n$ is $0.315$ at $n = 10^3$ and $0.0199$ at $n = 10^6$. The page [comparing growth by limits](/comparing-growth-by-limits/) shows that $(\lg n)^3 \ge \sqrt n$ for all $n$ from 3 to about $6.2 \times 10^8$.

### Pitfalls

- **Floating-point floors.** In Python, `math.log(1000, 10)` returns `2.9999999999999996`, so `int(math.log(1000, 10))` is 2, not 3. Also `math.log2(2**53 - 1)` returns `53.0`, but $\lfloor \lg(2^{53} - 1) \rfloor = 52$. For an integer, compute $\lfloor \lg n \rfloor$ exactly, as `n.bit_length() - 1` in Python, or by a loop of halvings. See [floor of log2](/floor-log2/).
- **Off by one in counts.** $\lfloor \lg n \rfloor$ halvings, $\lfloor \lg n \rfloor + 1$ bits, and $\lfloor \lg n \rfloor + 1$ probes of [binary search](/binary-search/) in the worst case are three different counts. Check each formula at $n = 1$ and at a power of two.
- **Power or composition.** $\lg^2 n$ is $(\lg n)^2$, and $\lg\lg n$ is $\lg(\lg n)$. At $n = 10^6$ the first is $397.3$ and the second is $4.32$.
- **The base in an exponent.** $2^{\lg n} = n$, but $2^{\log_3 n} = n^{\log_3 2}$, about $n^{0.631}$, by the swap rule. Changing the base of a logarithm inside an exponent changes the order of growth.
- **The logarithm of a sum.** $\lg(x + y)$ is not $\lg x + \lg y$. What is true for $x, y > 0$ is $\max(\lg x, \lg y) \le \lg(x + y) \le 1 + \max(\lg x, \lg y)$, since $\max(x, y) \le x + y \le 2\max(x,y)$.
- **Logarithms of small values.** $\lg 1 = 0$ and $\lg x < 0$ for $0 < x < 1$. A bound such as $O(n\log n)$ is meant for $n \ge 2$, and a formula with $\lg n$ in a denominator fails at $n = 1$.

## Examples

- $\lg 1024 = 10$, since $2^{10} = 1024$. $\log_{10} 1000 = 3$.
- Change of base: $\lg 1000 = \log_{10} 1000/\log_{10} 2 = 3/0.30103 = 9.9658\ldots$, and also $\ln 1000/\ln 2 = 6.9078/0.69315 = 9.9658\ldots$
- Product: $\lg(8 \cdot 32) = \lg 256 = 8 = 3 + 5$.
- Bits: $\lfloor \lg 1000 \rfloor + 1 = 10$, and 1000 is $1111101000$ in binary, with 10 digits.
- Halving: 1000 halves 9 times to reach 1, and $\lfloor \lg 1000 \rfloor = 9$.
- Swap: $8^{\lg 32} = 8^5 = 32768$ and $32^{\lg 8} = 32^3 = 32768$.
- Non-example: $\lg n$ and $\log_3 n$ differ by the constant factor $\lg 3 = 1.585\ldots$ This is harmless in $O$. In an exponent it is not harmless, as the pitfalls show.

## Where it is used

- [Logarithmic time](/logarithmic-time/): algorithms that halve their input, such as [binary search](/binary-search/), and operations on balanced trees and heaps, have cost $\Theta(\log n)$.
- [Linearithmic time](/linearithmic-time/): [merge sort](/merge-sort/) and [heapsort](/heapsort/) have cost $\Theta(n\log n)$. The lower bound for a comparison sort uses $\lg(n!) = n\lg n - n\lg e + O(\log n)$, see [Stirling's approximation](/stirling-approximation/).
- The [iterated logarithm](/iterated-logarithm/) $\lg^* n$ is the number of times $\lg$ must be applied to $n$ before the result is at most 1. It is at most 5 for each $n \le 2^{65536}$.
- Sums of the form $\sum 1/k$ give a logarithm: see the [harmonic series](/harmonic-series/).
- The number of bits of an integer, the depth of a recursion that halves its input, and the number of levels of a [recursion tree](/recursion-tree-method/) with ratio 2.

## References
