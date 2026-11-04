---
tag: 2YCV99
kind: concept
slug: order-of-growth
name: Order of growth
aliases:
- growth rate
area: foundations/asymptotic-analysis
level: intro
summary: The Θ-class of a running-time function, found from its dominant term, which tells how the cost scales as the input size grows.
prereqs: [time-complexity, asymptotic-notation]
see_also: [common-growth-rates, doubling-hypothesis, comparing-growth-by-limits, tilde-notation, logarithms, constant-time, linear-time, quadratic-time]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 3, Characterizing Running Times (Section 3.1 on dropping lower-order terms and constants, Section 3.2 on the formal definitions, Section 3.3 on standard functions)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms (order-of-growth classifications and the table of common orders)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11.1, The O-notation
---

The order of growth of a running time $T(n)$ is its $\Theta$-class: the set of functions that grow at the same rate as $T$ when $n$ becomes large. You usually find it by keeping the fastest-growing term of $T(n)$ and dropping its constant factor. When one order is $o$ of the other, the algorithm with the smaller order is faster for all large $n$, whatever the constants are.

## In plain words

Suppose a program has two parts. For each item, the first part looks at every item. The second part looks at each item once. With ten items, the first part takes a hundred steps and the second part takes ten. With a thousand items, the first part takes a million steps and the second part takes only a thousand. As the input grows, the part that grows fastest takes almost all of the time, and the other parts stop mattering.

That fastest part gives the order of growth. It tells how the cost scales: here, an input ten times larger takes about a hundred times longer. It does not give the exact time. A machine that is twice as fast halves the time, but it does not change the order of growth. For large inputs, the order of growth decides which algorithm is faster.

## The idea

**Leading term.** Write $T(n)$ as a sum of a fixed number of terms. The leading term is the one that grows fastest. If $T$ is a polynomial $a_d n^d + \cdots + a_1 n + a_0$ with $a_d > 0$, then $T(n)/n^d \to a_d$ when $n \to \infty$. So $T(n) = \Theta(n^d)$. The proof is by the limit: for large $n$ we have $a_d/2 \le T(n)/n^d \le 2a_d$, and this gives the constants of the definition of $\Theta$ in [asymptotic notation](/asymptotic-notation/).

**Drop constants and lower terms.** The order of growth of $3n^2 + 10n + 7$ is $n^2$. The constant $3$ depends on the machine, the language and how you count a step. The terms $10n$ and $7$ are smaller than $n^2$ for large $n$. Two functions $f$ and $g$ have the same order of growth when $f = \Theta(g)$. This is an equivalence relation on functions that are eventually positive, and the order of growth of $f$ is its equivalence class $\Theta(f)$. We name the class by its simplest member, for example $n^2$. See also [asymptotic equivalence](/asymptotic-equivalence/) and [tilde notation](/tilde-notation/), where you keep the constant of the leading term.

**The base of a logarithm does not matter.** For bases $a, b > 1$ we have $\log_a n = \log_b n / \log_b a$, a constant multiple. So $\Theta(\log n)$ needs no base. See [logarithms](/logarithms/). The base of an exponential does matter: $2^n$ and $3^n$ have different orders of growth, because $3^n/2^n = 1.5^n \to \infty$.

**The usual ladder.** From slow to fast growth, each function is $o$ of the next one:

$$1,\ \log n,\ \sqrt{n},\ n,\ n \log n,\ n^2,\ n^3,\ 2^n,\ n!$$

The names are [constant](/constant-time/), [logarithmic](/logarithmic-time/), square root, [linear](/linear-time/), [linearithmic](/linearithmic-time/), [quadratic](/quadratic-time/), [cubic](/cubic-time/), exponential and factorial time. Any polynomial of fixed degree is below any exponential $c^n$ with $c > 1$. The page [common growth rates](/common-growth-rates/) lists them with examples, and [comparing growth by limits](/comparing-growth-by-limits/) shows how to compare two functions with a limit.

**Why the order wins over the constant.** Let algorithm A take $100n$ steps and algorithm B take $n^2/2$ steps. B has the smaller constant, but B takes more steps than A for each $n \ge 201$ (at $n = 200$ they are equal: $20000$). For any constants $c_1, c_2 > 0$, the function $c_1 n$ is below $c_2 n^2$ for all $n > c_1/c_2$. So a linear algorithm beats a quadratic one from some size on, however large $c_1$ and however small $c_2$ is. The size where this happens can be large. Below that size, the algorithm with the higher order can be faster, so the order of growth is a statement about large inputs only.

## Examples

The table gives the value of each function for some $n$. Here $\lg n = \log_2 n$, and the values are rounded.

| $n$ | $\lg n$ | $n \lg n$ | $n^2$ | $n^3$ | $2^n$ |
| --- | --- | --- | --- | --- | --- |
| 10 | 3.3 | 33 | 100 | $10^3$ | 1024 |
| 100 | 6.6 | 664 | $10^4$ | $10^6$ | $1.27 \times 10^{30}$ |
| 1000 | 10.0 | 9966 | $10^6$ | $10^9$ | more than $10^{301}$ |
| $10^4$ | 13.3 | $1.33 \times 10^5$ | $10^8$ | $10^{12}$ | more than $10^{3010}$ |
| $10^6$ | 19.9 | $1.99 \times 10^7$ | $10^{12}$ | $10^{18}$ | more than $10^{301029}$ |

The row for $n = 100$ shows the gap. At $10^9$ steps in each second, $2^{100}$ steps take about $4 \times 10^{13}$ years. Also, going from $n = 1000$ to $n = 10^6$, the $n \lg n$ column grows by a factor of about $2000$, and the $n^2$ column by a factor of $10^6$.

The next table shows the largest $n$ that a computer can solve in a fixed number of steps, if the algorithm takes exactly $f(n)$ steps. The value is rounded down.

| Steps available | $n$ with $f(n) = n$ | $n \lg n$ | $n^2$ | $n^3$ | $2^n$ |
| --- | --- | --- | --- | --- | --- |
| $10^9$ | $10^9$ | 39 620 077 | 31 622 | 1000 | 29 |
| $10^{10}$ | $10^{10}$ | 352 213 444 | 100 000 | 2154 | 33 |

A machine ten times faster gives a ten times larger input for a linear algorithm, but about $3.16$ times for a quadratic one, and only 4 more items for an exponential one (29 to 33).

Non-examples:

- $n^2$ and $n^2 + n$ have the same order of growth, but $n^2$ and $n^3$ do not.
- $2^n$ and $2^{2n} = 4^n$ do not have the same order of growth, although the exponents differ by a constant factor.
- Not every pair of functions is in an order. The functions $n$ and $n^{1 + \sin n}$ are incomparable: neither is $O$ of the other, because $\sin n \ge 1/2$ for infinitely many $n$ and $\sin n \le -1/2$ for infinitely many $n$. The running times of real algorithms are usually comparable, but the ladder is not a total order on all functions.
- A function that oscillates between two orders has no single simple order. A program that takes $n$ steps on odd $n$ and $n^2$ steps on even $n$ is $O(n^2)$ and $\Omega(n)$, but it is $\Theta$ of neither.

### Pitfalls

- **$O$ is not the order.** "Insertion sort is $O(n^3)$" is true, but $n^3$ is not its order of growth. The order of growth is a $\Theta$-class, so it needs a matching upper and lower bound.
- **The order depends on the case.** [Insertion sort](/insertion-sort/) has worst-case order $n^2$ and best-case order $n$. Say which case you mean, see [worst-case analysis](/worst-case-analysis/).
- **A sum with a growing number of terms.** The leading-term rule needs a fixed number of terms. In $\sum_{i=1}^{n} i$ no single term dominates, and keeping only the largest term $n$ gives the wrong order. Evaluate the sum first: it is $\Theta(n^2)$, see [arithmetic series](/arithmetic-series/).
- **Equal order does not mean equal speed.** Two $\Theta(n \log n)$ sorts, for example [merge sort](/merge-sort/) and [heapsort](/heapsort/), have the same order, yet their running times on a real machine can differ by a clear constant factor, because heapsort jumps around the array and makes poor use of the cache. The order of growth does not show this.

## Where it is used

The order of growth is the main summary of an algorithm. A page on this site gives the order for the worst, average or best case, and it names the model. Experiments use a sharper form: if the time is $\sim a n^b$ (see [tilde notation](/tilde-notation/)), then doubling $n$ multiplies the time by a ratio that tends to $2^b$, and this is the [doubling hypothesis](/doubling-hypothesis/). A $\Theta$ bound alone does not give this, because the ratio $T(2n)/T(n)$ of a $\Theta(n^b)$ function only stays between two constants. Problem classes such as [polynomial time](/polynomial-time/) are defined by upper bounds on the order of growth, such as $O(n^k)$ for a constant $k$. The order of growth is not enough to choose between two algorithms of the same order, or for small inputs. Then the constants and the real machine matter.

## References
