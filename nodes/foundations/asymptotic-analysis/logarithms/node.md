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
see_also: [logarithmic-time, iterated-logarithm, order-of-growth, binary-search]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 3.3, Standard notations and common functions
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 3 (floors and ceilings) and Section 9.1
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms
---

The logarithm to base $b$ of a number $x$ is the exponent to which $b$ must be raised to give $x$. It is the inverse of exponentiation, and the logarithm to base 2 counts, up to rounding, how many times a quantity can be halved before it reaches 1. Logarithms appear in the cost of [binary search](/binary-search/), of [balanced trees](/balanced-binary-search-tree/) and of the best [comparison sorts](/sorting-problem/). This page fixes the notation of the site and proves the rules that the other pages use.

## In plain words

Ask how many times you can cut 1000 in half before you reach 1, rounding down each time. The numbers are 1000, 500, 250, 125, 62, 31, 15, 7, 3, 1. That is 9 cuts. Doubling the input adds only one more cut. A logarithm measures this count.

One more than this count is the number of binary digits that the number needs, and the count itself is the height of a complete binary tree with that many nodes. So an algorithm that throws away half of the input with a fixed amount of work at each step, or that walks down a balanced tree, has a cost that grows like a logarithm.

A logarithm has no bound, but it grows slower than any power of the input size with a positive exponent. The square root of a million is 1000, but a million halves only 19 times.

## The idea

### Definition and notation

Let $b > 0$ with $b \ne 1$, and let $x > 0$. The number $\log_b x$ is the unique real number $y$ with $b^y = x$. The function $y \mapsto b^y$ is strictly monotone and continuous from the reals onto the positive reals, so $y$ exists and is unique.

This site uses three names.

- $\lg x$ means $\log_2 x$. This is the convention of Cormen, Leiserson, Rivest and Stein (CLRS) and of most algorithm texts.
- $\ln x$ means $\log_e x$, the natural logarithm, where $e = 2.71828\ldots$
- $\log x$ with no base is written only inside $O$, $\Omega$ and $\Theta$, where the base does not matter (see below). Outside them, a page writes $\lg$ or $\ln$.

Some texts use $\log$ for base 10 or for base $e$. A reader who sees $\log$ outside a bound must check the convention of the text.

Powers and compositions have their own notation, as in CLRS:

- $\lg^k n$ means $(\lg n)^k$, a power.
- $\lg \lg n$ means $\lg(\lg n)$, and $\lg^{(i)} n$ means $\lg$ applied $i$ times. Do not confuse $\lg^{(i)} n$ with $\lg^i n$.
- $\lg n^k$ means $\lg(n^k)$, and $\lg n + k$ means $(\lg n) + k$.

### The rules

Let $b$, $x$, $y$ be positive, with $b \ne 1$, and let $r$ be a real number.

1. **Product.** $\log_b(xy) = \log_b x + \log_b y$.
2. **Quotient.** $\log_b(x/y) = \log_b x - \log_b y$.
3. **Power.** $\log_b(x^r) = r \log_b x$.
4. **Inverse.** $b^{\log_b x} = x$, and $\log_b(b^r) = r$.
5. **Change of base.** For $a > 0$ with $a \ne 1$: $\log_b x = \dfrac{\log_a x}{\log_a b}$.
6. **Swap.** $x^{\log_b y} = y^{\log_b x}$.

Proof. Rule 4 is the definition. For rule 1, put $s = \log_b x$ and $t = \log_b y$. Then $x = b^s$ and $y = b^t$, so $xy = b^s b^t = b^{s+t}$. By the definition, $\log_b(xy) = s + t$.

For rule 3, put $s = \log_b x$. Then $x^r = (b^s)^r = b^{rs}$, so $\log_b(x^r) = rs$.

Rule 2 follows from rules 1 and 3: $\log_b(x/y) = \log_b(x \cdot y^{-1}) = \log_b x + (-1)\log_b y$.

For rule 5, put $s = \log_b x$, so $x = b^s$. Take $\log_a$ of both sides and use rule 3: $\log_a x = s \log_a b$. The number $\log_a b$ is not zero, because $b \ne 1$ and $a^0 = 1$. Divide by it to get $s = \log_a x / \log_a b$.

For rule 6, use rules 4 and 3: $x^{\log_b y} = b^{\log_b x \cdot \log_b y}$, and this expression is symmetric in $x$ and $y$. ∎

A special case of rule 5 is $\log_b a \cdot \log_a b = 1$, from $x = a$.

### The base does not matter inside $O$

By rule 5, $\log_a n = \log_b n / \log_b a = c \cdot \log_b n$ with $c = 1/\log_b a$, a positive constant that does not depend on $n$. So $\log_a n = \Theta(\log_b n)$ for any two bases $a, b > 1$. This is why $O(\log n)$ needs no base. For example, $\lg n = \ln n / \ln 2 \approx 1.4427 \ln n$.

Rule 3 gives a second fact: for each fixed constant $k > 0$, $\log(n^k) = k \log n = \Theta(\log n)$. So $O(\log(n^2))$ and $O(\log n)$ are the same class. A power of the logarithm is different: $(\log n)^2 \ne O(\log n)$, because the ratio $\log n$ is unbounded.

### Floors of $\lg$

Three quantities are fixed by $k = \lfloor \lg n \rfloor$, for an integer $n \ge 1$. By the definition, $2^k \le n < 2^{k+1}$.

- **Halving.** Start with $n$ and replace it by $\lfloor n/2 \rfloor$ until it is 1. This takes exactly $k$ steps, because $\lfloor n/2 \rfloor$ drops the last binary digit and $n$ has $k+1$ binary digits.
- **Bits.** The binary form of $n$ has exactly $k + 1 = \lfloor \lg n \rfloor + 1$ digits, because $2^k \le n < 2^{k+1}$. Equivalently, it has $\lceil \lg(n+1) \rceil$ digits. For $n = 10^6$ this is 20 digits, since $\lg 10^6 \approx 19.93$.
- **Tree height.** A binary tree with $n$ nodes has height at least $\lfloor \lg n \rfloor$, because a tree of height $h$ has at most $2^{h+1} - 1$ nodes, so $n \le 2^{h+1} - 1 < 2^{h+1}$ and $h + 1 > \lg n$, which gives $h \ge \lfloor \lg n \rfloor$. A complete binary tree, such as the tree of a [binary heap](/binary-heap/), reaches this height.

### Slower than any positive power

**Claim.** For each real $\varepsilon > 0$, $\lg n = o(n^{\varepsilon})$. That is, $\lg n / n^{\varepsilon} \to 0$.

Proof. For $x > 0$, $\ln x \le x - 1$: the function $f(x) = x - 1 - \ln x$ has $f'(x) = 1 - 1/x$, which is negative for $x < 1$ and positive for $x > 1$, so $f$ has its minimum $f(1) = 0$. Apply this with $x = n^{\varepsilon/2}$ and drop the $-1$: $\frac{\varepsilon}{2} \ln n < n^{\varepsilon/2}$. So $\ln n < \frac{2}{\varepsilon} n^{\varepsilon/2}$, and
$$\frac{\ln n}{n^{\varepsilon}} < \frac{2}{\varepsilon}\, n^{-\varepsilon/2} \to 0.$$
For $n \ge 1$ the ratio is at least 0, so it tends to 0. Since $\lg n = \ln n / \ln 2$, the claim follows. ∎

So $\lg n = O(n^{\varepsilon})$ for each $\varepsilon > 0$, and $n^{\varepsilon} \ne O(\lg n)$. Apply the claim with $\varepsilon/k$ in place of $\varepsilon$ and raise both sides to the power $k$: this gives $(\lg n)^k = o(n^{\varepsilon})$ for each fixed $k > 0$. Each power of a logarithm grows slower than each positive power of $n$. The convergence is slow when $\varepsilon$ is small: for $\varepsilon = 1/2$ the ratio $\lg n / \sqrt{n}$ is 0.315 at $n = 10^3$ and 0.0199 at $n = 10^6$.

## Examples

- $\lg 1024 = 10$, since $2^{10} = 1024$. $\log_{10} 1000 = 3$.
- Change of base: $\lg 1000 = \log_{10} 1000 / \log_{10} 2 = 3 / 0.30103 \approx 9.966$. Also $\ln 1000 \approx 6.908$ and $6.908 / 0.6931 \approx 9.966$.
- Product: $\lg(8 \cdot 32) = \lg 256 = 8 = 3 + 5$.
- Bits: $\lfloor \lg 1000 \rfloor + 1 = 10$, and $1000$ is $1111101000$ in binary, which has 10 digits.
- Binary search on a sorted array of $n$ items looks at a range that halves each time. It makes at most $\lfloor \lg n \rfloor + 1$ probes.
- Not an example: $\log_2 n$ and $\log_3 n$ differ by the constant factor $\log_2 3 \approx 1.585$. This is harmless in $O$. In an exponent it is not harmless: $2^{\lg n} = n$, but $2^{\log_3 n} = n^{\log_3 2} \approx n^{0.631}$.

## Where it is used

- [Logarithmic time](/logarithmic-time/): algorithms that halve their input, such as [binary search](/binary-search/), and operations on balanced trees and heaps, have cost $\Theta(\log n)$.
- [Linearithmic time](/linearithmic-time/): [merge sort](/merge-sort/) and [heapsort](/heapsort/) have cost $\Theta(n \log n)$. The lower bound for a comparison sort uses $\lg(n!) = \Theta(n \log n)$ (see [Stirling's approximation](/stirling-approximation/)).
- The [iterated logarithm](/iterated-logarithm/) $\lg^* n$ is the number of times $\lg$ must be applied to $n$ before the result is at most 1. It is at most 5 for each $n \le 2^{65536}$.
- Sums of the form $\sum 1/k$ give a logarithm: see the [harmonic series](/harmonic-series/).
- Choosing the number of bits for an integer, or the depth of a recursion that halves its input.

## References
