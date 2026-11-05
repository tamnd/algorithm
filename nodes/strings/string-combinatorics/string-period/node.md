---
tag: 6N4YD6
kind: definition
slug: string-period
name: Period of a string
aliases:
- minimal period
- period
- periodicity of a string
area: strings/string-combinatorics
level: intro
summary: A shift p such that s[i]=s[i+p] for all valid i; equivalently, n minus the longest border.
prereqs: [alphabet, border]
see_also: [fine-and-wilf-theorem, periodicity-detection, primitive-root-of-a-word, prefix-function, string-compression-by-period, maximal-repetition, critical-factorization, primitive-word]
sources:
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 1, Words (D. Perrin), the sections on conjugacy and periodicity (periods, conjugate words and the theorem of Fine and Wilf)
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 1, Tools (periods and borders of a word, the duality between them, the periodicity lemma, and the border table)
  - paper: doi:10.1090/S0002-9939-1965-0174934-9
    title: N. J. Fine and H. S. Wilf, Uniqueness theorems for periodic functions, Proceedings of the American Mathematical Society 16(1), 1965, 109-114
    locator: the first theorem (two sequences with periods p and q that agree on p + q - gcd(p, q) consecutive terms are equal)
  - paper: doi:10.1137/0206024
    title: Donald E. Knuth, James H. Morris and Vaughan R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2), 1977, 323-350
    locator: the failure function and its relation to the periods of the pattern
---

A period of a string $s$ of length $n$ is an integer $p$ with $1 \le p \le n$ such that $s[i] = s[i + p]$ for each index $i$ where both sides exist. The smallest period $\mathrm{per}(s)$ is called *the* period of $s$, and it equals $n$ minus the length of the longest [border](/border/) of $s$. Periods are the main tool to describe repetitions in strings: they decide the shifts of [Knuth-Morris-Pratt](/knuth-morris-pratt/), the [primitive root](/primitive-root-of-a-word/) of a word, and the [runs](/maximal-repetition/) of a text.

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/). Only equality tests between letters are used, so the alphabet need not be ordered or finite. Indices are 0-based: $s = s[0]s[1]\cdots s[n-1]$, and $s[i..j]$ includes both ends.

**Period.** An integer $p$ is a *period* of $s \in \Sigma^n$, $n \ge 1$, if $1 \le p \le n$ and
$$ s[i] = s[i + p] \qquad \text{for all } 0 \le i \le n - p - 1. $$
The length $n$ is always a period, because the condition is then empty. The *smallest period* is $\mathrm{per}(s) = \min\{p : p \text{ is a period of } s\}$. The empty string has no period in this definition; some authors set $\mathrm{per}(\varepsilon) = 0$.

**Exponent.** The *exponent* of $s$ is the rational number $\exp(s) = n / \mathrm{per}(s) \ge 1$. The string is *periodic* when $\mathrm{per}(s) \le n/2$, that is, when $\exp(s) \ge 2$. Some texts write $s = u^{e}$ with $u = s[0..p-1]$ and $e = n/p$, a *fractional power*: $s$ is a prefix of the infinite word $uuu\cdots$.

**Three equivalent forms.** For $1 \le p \le n$ the following are equivalent, and each one is used as the definition in some texts.

1. $p$ is a period of $s$.
2. $s[0..n-p-1] = s[p..n-1]$, that is, $s$ has a border of length $n - p$.
3. $s$ is a prefix of $u^k$ for $u = s[0..p-1]$ and some $k \ge 1$.

*Proof.* (1) and (2) say the same thing letter by letter: the $i$-th letter of $s[0..n-p-1]$ is $s[i]$ and the $i$-th letter of $s[p..n-1]$ is $s[i+p]$, for $0 \le i \le n - p - 1$. For (1) implies (3), induction on $i$ gives $s[i] = s[i \bmod p] = u[i \bmod p]$ for every $i < n$: if $i \ge p$, then $s[i] = s[i - p]$ by (1) applied at $i - p$. So $s$ is the prefix of length $n$ of $u^k$ with $k = \lceil n/p \rceil$. For (3) implies (1), the letter of $u^k$ at index $i$ is $u[i \bmod p]$, and $i$ and $i + p$ have the same residue modulo $p$. $\square$

**The smallest period and the longest border.** By (2), the map $p \mapsto n - p$ is a bijection from the periods of $s$ to the lengths of its borders, the empty border included. The longest border gives the smallest period:
$$ \mathrm{per}(s) = n - |\mathrm{Border}(s)|. $$
So the [prefix function](/prefix-function/) gives $\mathrm{per}(s[0..i]) = i + 1 - \pi[i]$ for every prefix, and the chain $\pi[n-1], \pi[\pi[n-1]-1], \ldots, 0$ lists all borders of $s$ and so all its periods, in increasing order of the period. This is the method of [periodicity detection](/periodicity-detection/).

**Two basic facts.**

- *Multiples.* If $p$ is a period and $kp \le n$ for an integer $k \ge 1$, then $kp$ is a period. *Proof:* $s[i] = s[i+p] = \cdots = s[i + kp]$, and each intermediate index $i + tp$ with $t < k$ is at most $n - 1 - (k - t)p$, so each step is allowed.
- *Two periods.* If $p$ and $q$ are periods and $p + q - \gcd(p, q) \le n$, then $\gcd(p, q)$ is a period. This is the [Fine and Wilf theorem](/fine-and-wilf-theorem/). The bound on $n$ is exact, see the examples. A consequence: $\mathrm{per}(s)$ divides every period $q$ with $q \le n - \mathrm{per}(s)$, because then $\mathrm{per}(s) + q \le n$, so $\gcd(\mathrm{per}(s), q)$ is a period, and it cannot be smaller than $\mathrm{per}(s)$.

## Examples and non-examples

| $s$ | $n$ | all periods | borders (lengths) | $\mathrm{per}(s)$ | exponent |
| --- | --- | --- | --- | --- | --- |
| `abcd` | 4 | 4 | 0 | 4 | 1 |
| `aba` | 3 | 2, 3 | 0, 1 | 2 | 3/2 |
| `abab` | 4 | 2, 4 | 0, 2 | 2 | 2 |
| `abaab` | 5 | 3, 5 | 0, 2 | 3 | 5/3 |
| `aabaa` | 5 | 3, 4, 5 | 0, 1, 2 | 3 | 5/3 |
| `aaaa` | 4 | 1, 2, 3, 4 | 0, 1, 2, 3 | 1 | 4 |
| `abaababa` | 8 | 5, 7, 8 | 0, 1, 3 | 5 | 8/5 |
| `abaababaab` | 10 | 5, 8, 10 | 0, 2, 5 | 5 | 2 |

- **A period need not divide the length.** `aba` has period 2 and length 3. It is a prefix of $(ab)^2$, a fractional power $(ab)^{3/2}$.
- **Not every period is a multiple of the smallest one.** `aabaa` has the periods 3 and 4. Here $3 + 4 - \gcd(3, 4) = 6 > 5 = n$, so Fine and Wilf does not apply, and indeed 1 is not a period. For $n \ge 6$, Fine and Wilf shows that the two periods 3 and 4 force the period 1.
- **A non-example: shifts that fail.** In `abaab`, $p = 1$ fails at $i = 0$ ($a \ne b$), $p = 2$ fails at $i = 1$ ($b \ne a$), and $p = 4$ fails at $i = 0$ ($a \ne b$). So 3 is the smallest period although 4 is not a period.
- **A non-example: 0 is not a period.** The shift 0 would make each string periodic in a trivial way, so the definition needs $p \ge 1$.
- **The prefix function.** For `abaababaab` the prefix function is $[0, 0, 1, 1, 2, 3, 2, 3, 4, 5]$. The last value 5 gives $\mathrm{per} = 10 - 5 = 5$, and the border chain $5, \pi[4] = 2, \pi[1] = 0$ gives the periods $5, 8, 10$.

## Related definitions

- **Border.** The dual notion: a border of length $b$ is the same thing as the period $n - b$. See [border](/border/).
- **Primitive word and primitive root.** $s$ is a power $u^k$ with $k \ge 2$ exactly when $\mathrm{per}(s)$ divides $n$ and $\mathrm{per}(s) < n$; see [primitive word](/primitive-word/) and [primitive root of a word](/primitive-root-of-a-word/).
- **Repetitions.** A [square](/square/) is a string of exponent 2 with even length, an [overlap](/overlap/) is a string $axaxa$ of exponent more than 2, and a [cube](/cube/) has exponent at least 3. A [run](/maximal-repetition/) is a maximal periodic substring.
- **Local period.** The local period at a cut of $s$ is the length of the shortest square centered at that cut. The [critical factorization](/critical-factorization/) theorem says that some cut has local period $\mathrm{per}(s)$.
- **Compression by the period.** Storing $s$ as the pair $(s[0..\mathrm{per}(s)-1], n)$ is [compression by the period](/string-compression-by-period/).

## References
