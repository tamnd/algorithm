---
tag: 3QVT6M
kind: theorem
slug: master-theorem
name: Master theorem
aliases:
- master method
- Bentley-Haken-Saxe theorem
area: foundations/recurrences
level: core
summary: Gives the asymptotic solution of T(n) = aT(n/b) + f(n) by comparing f(n) with n^(log_b a) in three cases.
prereqs: [divide-and-conquer-recurrence, watershed-function, asymptotic-notation, geometric-series, recursion-tree-method]
see_also: [akra-bazzi-theorem, continuous-master-theorem, smoothness-rules, iteration-method, substitution-method, change-of-variables, harmonic-series, strassen-algorithm]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 4.5, The master method for solving recurrences; Section 4.6, Proof of the continuous master theorem
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 4.6, Proof of the master theorem (the subsection on floors and ceilings)
  - paper: doi:10.1145/1008861.1008865
    title: Jon L. Bentley, Dorothea Haken and James B. Saxe, A general method for solving divide-and-conquer recurrences, SIGACT News 12(3), 36 to 44 (1980)
  - url: "https://courses.csail.mit.edu/6.046/spring04/handouts/akrabazzi.pdf"
    locator: Tom Leighton, Notes on Better Master Theorems for Divide-and-Conquer Recurrences, MIT, October 9, 1996 (Theorem 2 and the examples)
  - paper: doi:10.1145/375827.375837
    title: Salvador Roura, Improved master theorems for divide-and-conquer recurrences, Journal of the ACM 48(2), 170 to 205 (2001)
  - book: isbn:9780321905758
    title: Robert Sedgewick and Philippe Flajolet, An Introduction to the Analysis of Algorithms, second edition
    locator: Section 2.6, Binary Divide-and-Conquer Recurrences and Binary Numbers; Section 2.7, General Divide-and-Conquer Recurrences
---

The master theorem gives the order of growth of the solution of a [divide-and-conquer recurrence](/divide-and-conquer-recurrence/) $T(n) = aT(n/b) + f(n)$, where $a > 0$ and $b > 1$ are constants, by comparing the driving function $f$ with the [watershed function](/watershed-function/) $n^{\log_b a}$. If $f$ is polynomially smaller, the leaves of the recursion tree dominate and $T(n) = \Theta(n^{\log_b a})$; if $f$ matches $n^{\log_b a}$ up to a power of $\log n$, each level contributes and one more factor $\log n$ appears; if $f$ is polynomially larger and regular, the root dominates and $T(n) = \Theta(f(n))$. The three cases do not cover each $f$, and the gaps between them are as important as the cases.

## Statement

Let $a > 0$ and $b > 1$ be real constants, and let $w = \log_b a$. Let $f$ be a function on the reals $n \ge 1$ such that $f(n) \ge 0$ and $f$ is bounded on each bounded interval $[1, x]$. Let $T$ be a function on the reals $n > 0$ with

$$c_1 \le T(n) \le c_2 \quad (0 < n < 1), \qquad T(n) = aT(n/b) + f(n) \quad (n \ge 1),$$

for constants $0 < c_1 \le c_2$. Then:

1. If $f(n) = O(n^{w - \varepsilon})$ for some constant $\varepsilon > 0$, then $T(n) = \Theta(n^w)$.
2. If $f(n) = \Theta(n^w \lg^k n)$ for some constant $k \ge 0$, then $T(n) = \Theta(n^w \lg^{k+1} n)$.
3. If $f(n) = \Omega(n^{w + \varepsilon})$ for some constant $\varepsilon > 0$, and the *regularity condition* holds, that is, there are constants $c < 1$ and $\hat n$ such that $a f(n/b) \le c f(n)$ for each $n \ge \hat n$, then $T(n) = \Theta(f(n))$.

The base case can be any bounded positive values: changing $c_1$ and $c_2$ changes only the constants in $\Theta$. In this real-valued form the recurrence determines $T$ completely. CLRS, fourth edition, Section 4.6, calls this form the continuous master theorem; it is not the [continuous master theorem](/continuous-master-theorem/) of Roura, which treats a different kind of recurrence.

**Integer version.** CLRS, fourth edition, Section 4.5, states the theorem for $n$ a natural number and $aT(n/b)$ read as $a'T(\lfloor n/b \rfloor) + a''T(\lceil n/b \rceil)$ with constants $a', a'' \ge 0$ and $a' + a'' = a$, the recurrence holding for $n$ above a threshold and $T(n) = \Theta(1)$ below it. The three conclusions are the same.

## In plain words

Picture the tree of recursive calls. The top call does some work. Below it, more calls each do less work, and at the bottom there are many tiny calls. The question is which part of the tree holds most of the work.

If the work per call shrinks fast as the calls get smaller, the top of the tree dominates, and the total is about the work of the top call. If the work per call shrinks slowly, the many calls at the bottom dominate, and the total is about the number of bottom calls. If the two forces balance, each level of the tree does about the same work, and the total is that work times the number of levels.

The theorem makes this race exact. It also says when the race has no clear winner. In those cases you need a finer tool.

## Proof

Throughout, $n \ge 1$, $L = \lfloor \log_b n \rfloor$, and $x = \log_b n$. Then $1 \le n/b^L < b$ and $1/b \le n/b^{L+1} < 1$.

### Lemma 1 (the level sum)

For each $n \ge 1$,

$$T(n) = a^{L+1}\, T(n/b^{L+1}) + \sum_{j=0}^{L} a^j f(n/b^j).$$

*Proof.* By induction on $i$, $T(n) = a^i T(n/b^i) + \sum_{j=0}^{i-1} a^j f(n/b^j)$ for $0 \le i \le L + 1$. For $i = 0$ this is trivial. For the step from $i$ to $i + 1 \le L + 1$: since $i \le L$, the argument $n/b^i$ is at least 1, so the recurrence gives $T(n/b^i) = aT(n/b^{i+1}) + f(n/b^i)$, and substitution gives the claim for $i + 1$. Take $i = L + 1$. $\square$

### Lemma 2 (the leaves)

The first term of Lemma 1 is $\Theta(n^w)$.

*Proof.* Since $x < L + 1 \le x + 1$, the number $a^{L+1}$ lies between $a^x$ and $a \cdot a^x$, and $a^x = a^{\log_b n} = n^{\log_b a} = n^w$. So $\min(1, a)\, n^w \le a^{L+1} \le \max(1, a)\, n^w$. The argument $n/b^{L+1}$ lies in $(0, 1)$, so $T$ of it lies in $[c_1, c_2]$. $\square$

### Lemma 3 (small arguments cost $O(n^w)$)

Let $n_1 \ge 1$ be a constant. The terms of the sum in Lemma 1 with $n/b^j < n_1$ add up to $O(n^w)$.

*Proof.* Let $M$ be a bound of $f$ on $[1, n_1]$ and $J = \lfloor \log_b n_1 \rfloor + 1$. A term with $n/b^j < n_1$ has $j > x - \log_b n_1 \ge L - J$, so there are at most $J + 1$ such terms, each with $L - J < j \le L$. For such $j$, $a^j \le a^L \max(1, a^{-J})$, and $a^L \le \max(1, a^{-1})\, a^x = \max(1, a^{-1})\, n^w$. So the terms add up to at most $(J + 1) M \max(1, a^{-J}) \max(1, a^{-1})\, n^w$. $\square$

In each case below, let $n_1 \ge b$ be a constant above which the hypothesis on $f$ holds. Split the sum of Lemma 1 into $S(n)$, the terms with $n/b^j \ge n_1$, and the rest, which is $O(n^w)$ by Lemma 3. Since $f \ge 0$, each term is non-negative, and $T(n) \ge \min(1,a)\, c_1 n^w$ by Lemma 2. Note the identity $a^j (n/b^j)^w = n^w$, since $b^w = a$.

### Case 1

Let $f(m) \le C m^{w - \varepsilon}$ for $m \ge n_1$. Then

$$S(n) \le C \sum_{j=0}^{L} a^j \left(\frac{n}{b^j}\right)^{w-\varepsilon} = C n^{w-\varepsilon} \sum_{j=0}^{L} (b^{\varepsilon})^j = C n^{w-\varepsilon}\, \frac{b^{\varepsilon(L+1)} - 1}{b^\varepsilon - 1} \le \frac{C b^\varepsilon}{b^\varepsilon - 1}\, n^w,$$

because $b^{\varepsilon L} \le b^{\varepsilon x} = n^\varepsilon$. With Lemmas 2 and 3, $T(n) = O(n^w)$, and the lower bound $T(n) = \Omega(n^w)$ is Lemma 2. The level costs form a [geometric series](/geometric-series/) that grows by the factor $b^\varepsilon$ towards the leaves, so the last levels dominate.

### Case 2

Let $C_1 m^w \lg^k m \le f(m) \le C_2 m^w \lg^k m$ for $m \ge n_1$, with $k \ge 0$.

*Upper bound.* Each term of $S(n)$ is at most $C_2 a^j (n/b^j)^w \lg^k(n/b^j) \le C_2 n^w \lg^k n$, and there are at most $L + 1 \le x + 1$ terms. So $S(n) \le C_2 n^w (\log_b n + 1)\lg^k n = O(n^w \lg^{k+1} n)$.

*Lower bound.* Let $n \ge \max(n_1^2, b^2)$. For each integer $j$ with $0 \le j \le x/2$, $n/b^j \ge \sqrt n \ge n_1$, so the term belongs to $S(n)$ and is at least $C_1 n^w \lg^k \sqrt n = C_1 2^{-k} n^w \lg^k n$. There are at least $x/2$ such $j$. So $S(n) \ge C_1 2^{-k-1} (\log_b n)\, n^w \lg^k n = \Omega(n^w \lg^{k+1} n)$.

The leaves and the small arguments add $O(n^w)$, which is $O(n^w \lg^{k+1} n)$. So $T(n) = \Theta(n^w \lg^{k+1} n)$.

### Case 3

Let $n_1 \ge \hat n$ also be large enough that $f(m) \ge C m^{w+\varepsilon}$ for $m \ge n_1$. If $n/b^j \ge n_1$, then each of $n, n/b, \ldots, n/b^{j-1}$ is at least $n_1$, and $j$ applications of the regularity condition give

$$a^j f(n/b^j) \le c\, a^{j-1} f(n/b^{j-1}) \le \cdots \le c^j f(n).$$

So $S(n) \le f(n) \sum_{j \ge 0} c^j = f(n)/(1 - c)$. The other parts are $O(n^w)$, and $n^w = O(f(n))$ because $f(n) \ge C n^{w+\varepsilon} \ge C n^w$. So $T(n) = O(f(n))$. The term $j = 0$ gives $T(n) \ge f(n)$ for $n \ge n_1$. So $T(n) = \Theta(f(n))$. $\blacksquare$

### Floors and ceilings

For the integer version, follow the arguments down the tree. With $n_0 = n$ and $n_{j+1} = \lceil n_j/b \rceil$, induction gives $n_j \le n/b^j + \sum_{i<j} b^{-i} < n/b^j + b/(b-1)$; with floors, $n_j > n/b^j - b/(b-1)$. So until the arguments drop to a constant size, each argument on level $j$ is within a constant factor of $n/b^j$. In cases 1 and 2 the bounds on $f$ are products of powers and powers of logarithms, which change by at most a constant factor when the argument changes by a constant factor, so each level sum keeps its order. In case 3 the regularity condition is applied at the actual arguments. The details are in CLRS, third edition, Section 4.6, and a general form, with arguments $b_i n + h_i(n)$ and $|h_i(n)| \le n/\lg^{1+\varepsilon} n$, is Theorem 2 of Leighton's notes. The [smoothness rules](/smoothness-rules/) give a second route: solve on powers of $b$ and extend by monotonicity.

## Consequences

### Worked recurrences

The exact values are for the integer recurrence with $T(1) = 1$ and $n$ a power of $b$; they follow from the exact level sum of the [divide-and-conquer recurrence](/divide-and-conquer-recurrence/).

| Recurrence | $n^w$ | Case | Solution | Exact on powers of $b$ |
|---|---|---|---|---|
| $T(n/2) + 1$ ([binary search](/binary-search/)) | $1$ | 2, $k = 0$ | $\Theta(\log n)$ | $\lg n + 1$ |
| $2T(n/2) + n$ ([merge sort](/merge-sort/)) | $n$ | 2, $k = 0$ | $\Theta(n \log n)$ | $n\lg n + n$ |
| $2T(n/2) + n\lg n$ | $n$ | 2, $k = 1$ | $\Theta(n \log^2 n)$ | $\frac12 n\lg^2 n + \frac12 n \lg n + n$ |
| $3T(n/2) + n$ ([Karatsuba](/karatsuba-multiplication/)) | $n^{\lg 3}$ | 1 | $\Theta(n^{\lg 3})$ | $3n^{\lg 3} - 2n$ |
| $4T(n/2) + n$ | $n^2$ | 1 | $\Theta(n^2)$ | $2n^2 - n$ |
| $7T(n/2) + n^2$ ([Strassen](/strassen-algorithm/)) | $n^{\lg 7}$ | 1 | $\Theta(n^{\lg 7})$ | |
| $8T(n/2) + n^2$ | $n^3$ | 1 | $\Theta(n^3)$ | $2n^3 - n^2$ |
| $2T(n/2) + n^2$ | $n$ | 3, $c = \frac12$ | $\Theta(n^2)$ | $2n^2 - n$ |
| $3T(n/4) + n\lg n$ | $n^{\log_4 3}$ | 3, $c = \frac34$ | $\Theta(n \log n)$ | |

In the last row, $\log_4 3 \approx 0.792$, so $f(n) = n\lg n = \Omega(n^{0.792 + 0.2})$, and $3 \cdot \frac n4 \lg\frac n4 \le \frac34 n\lg n$ for $n \ge 4$.

### A coefficient below one

The hypothesis is $a > 0$, not $a \ge 1$. For $T(n) = \frac12 T(n/2) + 1/n$, $w = \log_2 \frac12 = -1$ and $f(n) = n^{-1} = \Theta(n^w \lg^0 n)$, so case 2 gives $T(n) = \Theta((\log n)/n)$. With $T = 1$ on $(0, 1)$ and $n = 2^k$, Lemma 1 gives exactly $T(n) = (k + 1)/n + 1/(2n)$. This example is in Leighton's notes.

### Case 2 for each real k

The proof of case 2 extends to each real $k$ when $f(n) = \Theta(n^w \lg^k n)$:

- $k > -1$: $T(n) = \Theta(n^w \lg^{k+1} n)$.
- $k = -1$: $T(n) = \Theta(n^w \lg\lg n)$.
- $k < -1$: $T(n) = \Theta(n^w)$.

*Proof sketch.* With $\lg(n/b^j) = \lg b\,(x - j)$, the sum $S(n)$ is $\Theta\big(n^w \sum_j (x - j)^k\big)$, where $x - j$ runs through numbers spaced by 1 from about $\log_b n_1$ up to $x$. Compare the sum with $\int_{\log_b n_1}^{x} y^k\, dy$ by [integral bounds](/integral-bounds-for-sums/): this is $\Theta(x^{k+1})$ for $k > -1$, $\Theta(\log x)$ for $k = -1$, and $\Theta(1)$ for $k < -1$. Add the $\Theta(n^w)$ of the leaves.

For $k = -1$, the recurrence $T(n) = 2T(n/2) + n/\lg n$ with $T(1) = 1$ has the exact value $T(n) = n(1 + H_m)$ on $n = 2^m$, where $H_m$ is the $m$-th [harmonic number](/harmonic-series/), since level $j$ costs $n/(m - j)$. So $T(n) = \Theta(n \log\log n)$.

### Regularity implies a polynomial gap

If $a f(n/b) \le c f(n)$ for $n \ge \hat n$ with $c < 1$, and $f \ge \delta > 0$ on $[\hat n, b\hat n)$, then $f(n) = \Omega(n^{w + \log_b(1/c)})$. Indeed, for $n \in [\hat n b^j, \hat n b^{j+1})$, $j$ applications give $f(n) \ge (a/c)^j f(n/b^j) \ge \delta (a/c)^j$, and $(a/c)^j = \Theta(n^{\log_b (a/c)})$. So under this mild condition the $\Omega$ hypothesis of case 3 follows from regularity.

### Monotonicity in f

Lemma 1 shows that $T$ is a non-decreasing function of $f$: if $f \le g$ pointwise, the solution for $f$ is at most the solution for $g$, with the same base values. So a driving function squeezed between two functions that satisfy the same case has the same solution.

## Tightness

### The gap between cases 1 and 2

Case 1 needs $f$ smaller than $n^w$ by a polynomial factor $n^\varepsilon$, and case 2 (as stated) needs $f = \Theta(n^w \lg^k n)$ with $k \ge 0$. The function $f(n) = n^w/\lg n$ is in neither. For $T(n) = 2T(n/2) + n/\lg n$, $f(n) = n/\lg n$ is $o(n)$ but not $O(n^{1 - \varepsilon})$ for any $\varepsilon > 0$, since $n^\varepsilon/\lg n \to \infty$. The exact value $n(1 + H_{\lg n})$ shows $T(n) = \Theta(n\log\log n)$, which is neither $\Theta(n)$, the answer of case 1, nor $\Theta(n \log n)$. The extended case 2 above, or the [Akra-Bazzi theorem](/akra-bazzi-theorem/), covers it.

### The gap between cases 2 and 3

The function $f(n) = n^w \cdot 2^{\sqrt{\lg n}}$ grows faster than $n^w \lg^k n$ for each $k$, and slower than $n^{w+\varepsilon}$ for each $\varepsilon > 0$. For $T(n) = 2T(n/2) + n 2^{\sqrt{\lg n}}$ with $T(1) = 1$ and $n = 2^m$, the level sum is

$$T(n) = n\Big(1 + \sum_{i=1}^{m} 2^{\sqrt i}\Big).$$

Comparison with $\int 2^{\sqrt y}\,dy$ (substitute $y = u^2$) gives $\sum_{i \le m} 2^{\sqrt i} \sim \frac{2}{\ln 2}\sqrt m\, 2^{\sqrt m}$, so $T(n) = \Theta(f(n)\sqrt{\lg n})$. This is neither $\Theta(f(n))$, the answer of case 3, nor $\Theta(n^w \lg^{k+1} n)$ for any $k$. The ratio of the sum to $\sqrt m\, 2^{\sqrt m}$ is about $2.52$ at $m = 100$, $2.70$ at $m = 400$ and $2.79$ at $m = 1600$, and it approaches $2/\ln 2 \approx 2.885$ slowly.

### Regularity cannot be dropped

Let $T(n) = T(n/2) + f(n)$, so $a = 1$, $b = 2$ and $w = 0$, with

$$f(n) = \begin{cases} n & \text{if } \lfloor \lg n \rfloor \text{ is even,} \\ \sqrt n & \text{if } \lfloor \lg n \rfloor \text{ is odd.} \end{cases}$$

Then $f(n) \ge \sqrt n$, so $f = \Omega(n^{0 + 1/2})$. But for $n \ge 4$ with $\lfloor \lg n \rfloor$ odd, $\lfloor \lg(n/2) \rfloor$ is even, so $T(n) = T(n/4) + f(n/2) + f(n) \ge f(n/2) = n/2$, and $T(n)/f(n) \ge \sqrt n/2$, which is unbounded. So $T(n) \ne \Theta(f(n))$; in fact $T(n) = \Theta(n)$. Regularity fails here: $f(n/2)/f(n) = \sqrt n/2$ at the same $n$.

### Regularity is not necessary

For $T(n) = T(n/2) + n(2 - \cos n)$, regularity fails: at $n = 2\pi(2m + 1)$, $\cos n = 1$ and $\cos(n/2) = -1$, so $f(n/2)/f(n) = 3/2 > 1$. But $n \le f(n) \le 3n$, and by monotonicity in $f$ the solution lies between the solutions for $n$ and for $3n$, both $\Theta(n)$. So $T(n) = \Theta(n) = \Theta(f(n))$. The Akra-Bazzi theorem handles such $f$ with its polynomial-growth condition instead of regularity.

### Other recurrences outside the theorem

- **A non-constant number of subproblems.** $T(n) = nT(n/2) + 1$ or $T(n) = 2^n T(n/2) + n$: $a$ is not a constant.
- **Unequal parts.** $T(n) = T(n/3) + T(2n/3) + n$: not of the form $aT(n/b)$. The [Akra-Bazzi theorem](/akra-bazzi-theorem/) gives $\Theta(n\log n)$.
- **Subtractive recurrences.** $T(n) = 2T(n-1) + 1$: the size does not shrink by a constant factor. The [iteration method](/iteration-method/) gives $2^n - 1$.
- **Negative driving functions.** $T(n) = 2T(n/2) - n$ violates $f \ge 0$; with $T(1) = 1$ it gives $n - n\lg n < 0$ on powers of 2.
- **Roots.** $T(n) = 2T(\sqrt n) + \lg n$ needs a [change of variables](/change-of-variables/) first.

## History

Bentley, Haken and Saxe (1980) published a general method for the recurrences of divide-and-conquer algorithms, and the chapter notes of CLRS give their paper as the origin of the master method. CLRS presents the result as the master method, and its fourth edition states case 2 with the factor $\lg^k n$, $k \ge 0$, and proves the real-valued form in Section 4.6. Leighton's notes of 1996 gave a short proof of the more general theorem of Akra and Bazzi, published in 1998, which needs neither equal parts nor a regularity condition. Roura (2001) proved master theorems with exact leading constants, both for $T(n) = aT(n/b) + f(n)$ with floors and ceilings (his discrete master theorem) and for full-history recurrences (his [continuous master theorem](/continuous-master-theorem/)).

## References
