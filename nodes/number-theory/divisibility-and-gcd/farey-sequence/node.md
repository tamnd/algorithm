---
tag: 5K9FMP
kind: definition
slug: farey-sequence
name: Farey sequence
aliases:
- Farey series
area: number-theory/divisibility-and-gcd
level: core
summary: The ordered list of reduced fractions in [0, 1] with denominators at most n.
prereqs: [coprime-integers, bezouts-identity, euler-totient]
see_also: [stern-brocot-tree, continued-fraction-convergents, rational-approximation, counting-coprime-pairs, reducing-fractions, calkin-wilf-tree, euler-totient, continued-fraction]
sources:
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 3, Farey series and a theorem of Minkowski (the definition, the neighbour and mediant theorems, and their history)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 4.5, Relative primality (the Stern-Brocot tree and Farey series)
  - url: "https://en.wikipedia.org/wiki/Farey_sequence"
    locator: Wikipedia, Farey sequence (the next-term formula, the length, Ford circles and the Franel-Landau theorem)
---

The Farey sequence $F_n$ of order $n$ is the increasing list of all fractions $h/k$ in lowest terms with $0 \le h \le k \le n$. Its terms are close neighbours in a precise sense: two consecutive terms $a/b < c/d$ always satisfy $bc - ad = 1$, and each term is the mediant $(a + c)/(b + d)$ of its two neighbours. These facts give a simple rule that lists $F_n$ term by term in constant memory, and they make Farey sequences a tool for [rational approximation](/rational-approximation/) with a bounded denominator. The length of $F_n$ is $1 + \sum_{k \le n} \varphi(k)$, about $3n^2/\pi^2$, where $\varphi$ is the [Euler totient](/euler-totient/).

## Definition

Let $n \ge 1$. The **Farey sequence of order $n$** is the set

$$F_n = \left\{ \frac{h}{k} : 0 \le h \le k \le n, \; \gcd(h, k) = 1 \right\},$$

listed in increasing order. It starts with $0/1$ and ends with $1/1$. Each rational number in $[0, 1]$ is written once, in lowest terms ([reducing fractions](/reducing-fractions/)). Some authors use the whole real line or the interval $(0, 1]$; the structure is the same after shifting by integers.

**Theorem 1 (neighbours).** If $a/b < c/d$ are consecutive in $F_n$, then $bc - ad = 1$ and $b + d > n$.

*Proof.* Since $\gcd(a, b) = 1$, [Bézout's identity](/bezouts-identity/) gives integers $x, y$ with $bx - ay = 1$, and the solutions in $y$ form a residue class modulo $b$, so we can choose $n - b < y \le n$. Then $\gcd(x, y) = 1$, $y \ge 1$, and $x/y - a/b = 1/(by) > 0$. Also $x \le y$: here $a < b$, because $a/b$ is not the last term, so $(b - a) y \ge 1$ and $bx = 1 + ay \le by$. So $x/y \in F_n$ and $x/y > a/b$, hence $x/y \ge c/d$. Suppose $x/y > c/d$. Then $x/y - c/d \ge 1/(yd)$ and $c/d - a/b \ge 1/(bd)$, so

$$\frac{1}{by} = \frac{x}{y} - \frac{a}{b} \ge \frac{1}{yd} + \frac{1}{bd} = \frac{b + y}{byd},$$

which gives $d \ge b + y > n$, impossible. So $c/d = x/y$, both in lowest terms, so $c = x$, $d = y$, and $bc - ad = 1$, $b + d = b + y > n$. $\square$

**Theorem 2 (mediants).** If $a/b < h/k < c/d$ are three consecutive terms of $F_n$, then $h/k = (a + c)/(b + d)$.

*Proof.* By Theorem 1, $bh - ak = 1$ and $kc - hd = 1$. Subtracting, $h(b + d) = k(a + c)$, so $h/k = (a + c)/(b + d)$. $\square$

**Theorem 3 (from $F_{n-1}$ to $F_n$).** $F_n$ arises from $F_{n-1}$ by inserting, between each pair of neighbours $a/b, c/d$ with $b + d = n$, their mediant $(a + c)/n$. *Proof.* A new term $h/n$ of $F_n$ has neighbours $a/b, c/d$ in $F_n$ that are both in $F_{n-1}$ (two consecutive terms cannot both have denominator $n$, by $b + d > n$), and by Theorem 2, $h/n = (a + c)/(b + d)$, so $b + d = n \lambda$ for an integer $\lambda \ge 1$; since $b, d \le n - 1$, $\lambda = 1$ and $b + d = n$. Conversely, if $a/b, c/d$ are neighbours in $F_{n-1}$ with $b + d = n$, their mediant has denominator $n$ and is in lowest terms, because $(b + d)c - (a + c)d = bc - ad = 1$, so it is a new term of $F_n$ between them. $\square$

**The next term.** If $a/b < c/d$ are consecutive in $F_n$ and $c/d < 1$, the next term is

$$\frac{e}{f} = \frac{kc - a}{kd - b}, \qquad k = \left\lfloor \frac{n + b}{d} \right\rfloor.$$

By Theorem 1 the next term satisfies $de - cf = 1$ and $n - d < f \le n$. The pair $(kc - a, kd - b)$ satisfies $d(kc - a) - c(kd - b) = bc - ad = 1$ for each $k$, all solutions have this form, and $k = \lfloor (n + b)/d \rfloor$ is the one value with $n - d < kd - b \le n$. Starting from $0/1$ and $1/n$, this rule lists $F_n$ with $O(1)$ arithmetic operations per term and $O(1)$ memory.

**Length.** The fractions of $F_n$ with denominator $k \ge 2$ are the $h/k$ with $1 \le h < k$, $\gcd(h, k) = 1$, so there are $\varphi(k)$ of them; denominator $1$ gives $0/1$ and $1/1$. So

$$|F_n| = 1 + \sum_{k=1}^{n} \varphi(k) = \frac{3}{\pi^2} n^2 + O(n \log n).$$

The asymptotic form is the density $6/\pi^2$ of coprime pairs, see [counting coprime pairs](/counting-coprime-pairs/).

## Examples and non-examples

**Small orders.**

$$F_1 = \tfrac01, \tfrac11 \qquad F_2 = \tfrac01, \tfrac12, \tfrac11 \qquad F_3 = \tfrac01, \tfrac13, \tfrac12, \tfrac23, \tfrac11 \qquad F_4 = \tfrac01, \tfrac14, \tfrac13, \tfrac12, \tfrac23, \tfrac34, \tfrac11$$

$$F_5 = \tfrac01, \tfrac15, \tfrac14, \tfrac13, \tfrac25, \tfrac12, \tfrac35, \tfrac23, \tfrac34, \tfrac45, \tfrac11.$$

**Neighbours.** In $F_5$, $2/5$ and $1/2$ give $5 \cdot 1 - 2 \cdot 2 = 1$, and $1/3, 2/5, 1/2$ show the mediant rule: $(1 + 1)/(3 + 2) = 2/5$. From $F_4$ to $F_5$, the mediants with denominator sum $5$ are inserted: $1/5$ between $0/1$ and $1/4$, $2/5$ between $1/3$ and $1/2$, $3/5$ between $1/2$ and $2/3$, and $4/5$ between $3/4$ and $1/1$.

**The next-term rule.** In $F_5$, starting from $0/1, 1/5$: $k = \lfloor 6/5 \rfloor = 1$ gives $(1 - 0)/(5 - 1) = 1/4$. From $1/5, 1/4$: $k = \lfloor 10/4 \rfloor = 2$ gives $(2 - 1)/(8 - 5) = 1/3$. From $1/4, 1/3$: $k = \lfloor 9/3 \rfloor = 3$ gives $(3 - 1)/(9 - 4) = 2/5$.

**Lengths.** $|F_5| = 1 + (1 + 1 + 2 + 2 + 4) = 11$. $|F_{10}| = 33$, $|F_{100}| = 3045$ and $|F_{1000}| = 304193$, against $3n^2/\pi^2 \approx 30.4$, $3039.6$ and $303963.6$.

**Non-examples.** $2/4$ is not a term of any $F_n$ as written, since it is not in lowest terms; it is the term $1/2$. $1/6$ is not in $F_5$, because its denominator is too large. $1/3$ and $1/2$ are neighbours in $F_3$ and $F_4$ but not in $F_5$, where $2/5$ lies between them; neighbours in $F_n$ stay neighbours only up to order $b + d - 1$. And $1/3, 3/4$ satisfy $3 \cdot 3 - 1 \cdot 4 = 5 \ne 1$, so they are neighbours in no Farey sequence.

## Related definitions

- **Mediant.** The mediant of $a/b$ and $c/d$ is $(a + c)/(b + d)$, which lies strictly between them. If $bc - ad = 1$, the mediant is the fraction with the smallest denominator between them.
- **[Stern-Brocot tree](/stern-brocot-tree/).** The binary tree of all positive fractions built by repeated mediants. Its nodes with denominator at most $n$, read in order and restricted to $[0, 1]$, form $F_n$. The [Calkin-Wilf tree](/calkin-wilf-tree/) lists the same fractions in a different order.
- **[Convergents](/continued-fraction-convergents/).** Consecutive convergents $p_{n-1}/q_{n-1}$ and $p_n/q_n$ satisfy $|p_n q_{n-1} - p_{n-1} q_n| = 1$, so they are Farey neighbours. The best approximations of $x$ with denominator at most $n$ from below and from above are the two neighbours of $x$ in $F_n$.
- **Ford circles.** For each $h/k$ in lowest terms, the circle of radius $1/(2k^2)$ tangent to the real line at $h/k$. Two Ford circles touch exactly when their fractions are Farey neighbours, and otherwise they do not meet.
- **Farey dissection.** The division of $[0, 1]$ into arcs around the terms of $F_n$, used in the Hardy-Littlewood circle method.
- **Franel-Landau theorem.** The Riemann hypothesis is equivalent to the statement that the terms $f_j$ of $F_n$ are spread almost evenly: $\sum_j |f_j - j/|F_n|| = O(n^{1/2 + \varepsilon})$ for each $\varepsilon > 0$.

The name comes from John Farey, who stated the mediant property in a letter of 1816; Haros had found the sequences in 1802, and Cauchy gave a proof, as Hardy and Wright relate.

## References
