---
tag: 0VRFHM
kind: technique
slug: brun-sieve
name: Brun's sieve
aliases:
- Brun's pure sieve
- Brun sieve
- Brun's combinatorial sieve
area: number-theory/sieves
level: research
summary: Cut inclusion-exclusion off after the terms with at most m prime factors. Even m gives an upper bound, odd m a lower bound, and the error term stays small enough to bound twin primes.
prereqs: [sieve-theory, inclusion-exclusion-principle, mobius-function, legendre-phi-function]
see_also: [selberg-sieve, large-sieve-inequality, sieve-of-eratosthenes, prime-gaps, prime-number-theorem, buchstab-function, mobius-inversion, harmonic-series]
sources:
  - book: isbn:9780821849705
    title: John Friedlander and Henryk Iwaniec, Opera de Cribro, American Mathematical Society Colloquium Publications 57, 2010
    locator: Chapter 6, Brun's sieve (pp. 55 to 88), starting with Section 6.1, Brun's Pure Sieve (p. 55)
  - book: isbn:9780821898543
    title: Gérald Tenenbaum, Introduction to Analytic and Probabilistic Number Theory, third edition, American Mathematical Society, Graduate Studies in Mathematics 163, 2015
    locator: Part I, Chapter 4, Section 4.2, Brun's combinatorial sieve (p. 68), and Section 4.3, application to twin primes (p. 71)
  - book: isbn:9780521612753
    title: Alina Carmen Cojocaru and M. Ram Murty, An Introduction to Sieve Methods and Their Applications, London Mathematical Society Student Texts 66, Cambridge University Press, 2006
    locator: Chapter 6, Brun's sieve (p. 80)
  - book: isbn:9780821836330
    title: Henryk Iwaniec and Emmanuel Kowalski, Analytic Number Theory, American Mathematical Society Colloquium Publications 53, 2004
    locator: Chapter 6, Elementary sieve methods (pp. 153 to 167)
---

Brun's sieve is the first method that made the sieve of Eratosthenes and Legendre usable for sifting by many primes. Legendre's identity counts the integers free of primes below $z$ by full [inclusion-exclusion](/inclusion-exclusion-principle/), which has $2^{\pi(z)}$ terms, each with an error. Viggo Brun noticed that the partial sums of inclusion-exclusion alternate around the true value, so stopping after the divisors with at most $m$ prime factors gives an upper bound when $m$ is even and a lower bound when $m$ is odd, with only about $z^m$ error terms. With $m$ of size $\log\log x$ and $z = x^{1/(c\log\log x)}$, this pure sieve gives $\pi_2(x) = O(x(\log\log x)^2/\log^2 x)$ for the number of twin primes up to $x$, which is already enough to prove Brun's theorem: the sum of $1/p$ over twin primes converges. Brun's later combinatorial sieve, with truncation rules that depend on the sizes of the primes, removes the $\log\log$ factor.

## In plain words

To count the numbers in a list that no small prime divides, start with the whole list, subtract the multiples of each prime, add back the multiples of each product of two primes, subtract the multiples of each product of three, and so on. Done to the end this is exact, but there are far too many terms, and each one carries a small rounding error.

The key fact is that every running total along the way is an overestimate or an underestimate, alternately. So you can stop early, after the products of a few primes, and still have a correct bound. Stopping early leaves out most of the terms, and with them most of the rounding errors. The price is that the bound is a little off from the true main term, and choosing where to stop balances the two losses.

## When it applies

- You want to count, or bound, $S(\mathcal{A}, z) = \#\{a \in \mathcal{A} : \gcd(a, P(z)) = 1\}$ for a finite sequence $\mathcal{A}$ and $P(z) = \prod_{p < z,\, p \in \mathcal{P}} p$.
- For each squarefree $d \mid P(z)$ you know $\mathcal{A}_d = \#\{a \in \mathcal{A} : d \mid a\}$ in the form $\mathcal{A}_d = g(d) X + r_d$ with $g$ multiplicative, $0 \le g(p) < 1$, and a usable bound on $|r_d|$ (for instance $|r_d| \le \kappa^{\omega(d)}$).
- The sieve dimension $\kappa$, the average of $p\,g(p)$, is fixed, and you are content with bounds that are right up to a constant factor (the combinatorial sieve) or up to a power of $\log\log x$ (the pure sieve).
- The sifting range $z$ is a small power of $X$ (pure sieve: $z = X^{1/(c\log\log X)}$; combinatorial sieve: $z = X^{c}$ for a small constant $c$).

## The template

**Step 1: the truncated Möbius identity.** For a positive integer $n$ with $\nu$ distinct prime factors, all dividing $P(z)$, and any $m \ge 0$,

$$\sum_{\substack{d \mid n \\ \omega(d) \le m}} \mu(d) = \sum_{j=0}^{m} (-1)^j \binom{\nu}{j} = (-1)^m \binom{\nu - 1}{m} \qquad (\nu \ge 1),$$

and the sum is $1$ when $\nu = 0$. The identity follows by induction on $m$ from Pascal's rule $\binom{\nu}{j} = \binom{\nu-1}{j} + \binom{\nu-1}{j-1}$: the sum telescopes. Hence

$$\sum_{\substack{d \mid n \\ \omega(d) \le m}} \mu(d) \;\ge\; [n = 1] \ \text{ for even } m, \qquad \sum_{\substack{d \mid n \\ \omega(d) \le m}} \mu(d) \;\le\; [n = 1] \ \text{ for odd } m.$$

These are the Bonferroni inequalities. Apply them to $n = \gcd(a, P(z))$ and sum over $a \in \mathcal{A}$:

$$S(\mathcal{A}, z) \le \sum_{\substack{d \mid P(z) \\ \omega(d) \le m}} \mu(d)\, \mathcal{A}_d \quad (m \text{ even}), \qquad S(\mathcal{A}, z) \ge \sum_{\substack{d \mid P(z) \\ \omega(d) \le m}} \mu(d)\, \mathcal{A}_d \quad (m \text{ odd}).$$

**Step 2: split main term and remainder.** Insert $\mathcal{A}_d = g(d) X + r_d$:

$$\sum_{\substack{d \mid P(z) \\ \omega(d) \le m}} \mu(d)\, \mathcal{A}_d = X \sum_{\substack{d \mid P(z) \\ \omega(d) \le m}} \mu(d)\, g(d) + \sum_{\substack{d \mid P(z) \\ \omega(d) \le m}} \mu(d)\, r_d.$$

**Step 3: the truncated main term.** The full sum $\sum_{d \mid P(z)} \mu(d) g(d)$ is $W(z) = \prod_{p < z}(1 - g(p))$. Think of independent events $E_p$ with probabilities $g(p)$, and let $N$ count those that occur. Then $\sum_{\omega(d) = j} g(d) = \mathbb{E}\binom{N}{j}$, and the identity of Step 1 gives

$$\Big| \sum_{\substack{d \mid P(z) \\ \omega(d) \le m}} \mu(d)\, g(d) - W(z) \Big| = \mathbb{E}\Big[\binom{N-1}{m}[N \ge 1]\Big] \le \mathbb{E}\binom{N}{m+1} = \sum_{\substack{d \mid P(z) \\ \omega(d) = m+1}} g(d) \le \frac{L^{m+1}}{(m+1)!},$$

where $L = \sum_{p < z} g(p)$, and the last step expands $L^{m+1}$ and keeps the products of distinct primes.

**Step 4: the remainder.** If $|r_d| \le \kappa^{\omega(d)}$, the remainder is at most $\kappa^m$ times the number of $d \mid P(z)$ with $\omega(d) \le m$, which is at most $\sum_{j \le m} \binom{\pi(z)}{j} \le z^m$ for $z \ge 2$.

**Step 5: choose $m$ and $z$.** Altogether

$$S(\mathcal{A}, z) = X W(z) + O\Big( X \frac{L^{m+1}}{(m+1)!} + \kappa^m z^m \Big)$$

as an upper bound for even $m$ and a lower bound for odd $m$. With $L \approx \kappa \log\log z$, take $m$ a large constant times $\log\log X$, so that $L^{m+1}/(m+1)!$ is smaller than $W(z) \asymp (\log z)^{-\kappa}$ by Stirling's formula, and take $\log z = \log X / (c\, m)$ so that $\kappa^m z^m \le X^{1/2}$, say. Then the sifted count is $X W(z)(1 + o(1))$, with $z = X^{1/(c'\log\log X)}$.

**Step 6: from sifted count to the target set.** Elements of the target set (primes, twin primes) with $a \ge z$ survive the sieve, so the target count is at most $S(\mathcal{A}, z)$ plus the at most $z$ elements below $z$.

## Classic examples

- **Exact alternation, one integer.** Take $n = 210 = 2 \cdot 3 \cdot 5 \cdot 7$, so $\nu = 4$. The truncated sums for $m = 0, 1, 2, 3, 4$ are $1, -3, 3, -1, 0$, which equal $(-1)^m \binom{3}{m}$ and alternate around the true value $[n = 1] = 0$.
- **Alternation on a real count.** Sift $\{1, \ldots, 10^6\}$ by the ten primes below 30. The true count is $157939$, and $X W(z) = 157947.2$. The truncated sums $\sum_{\omega(d) \le m} \mu(d)\lfloor 10^6/d \rfloor$ for $m = 0, \ldots, 7$ are

  | $m$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
  |---|---|---|---|---|---|---|---|---|
  | sum | 1000000 | $-533436$ | 419754 | 101839 | 165287 | 157392 | 157946 | 157939 |
  | error | $+842061$ | $-691375$ | $+261815$ | $-56100$ | $+7348$ | $-547$ | $+7$ | 0 |

  The even rows are upper bounds and the odd rows lower bounds. The sum is exact from $m = 7$ on, since the product of the 8 smallest primes, $9699690$, exceeds $10^6$ and all later terms are zero. Truncating at $m = 6$ uses 848 of the 1024 divisors and is already within 7 of the truth.
- **Twin primes, Brun's theorem.** Take $\mathcal{A} = \{n(n+2) : n \le x\}$. Then $g(2) = 1/2$, $g(p) = 2/p$ for odd $p$, $|r_d| \le 2^{\omega(d)}$, so $\kappa = 2$ and $W(z) \asymp (\log z)^{-2}$. The pure sieve with $\log z \asymp \log x / \log\log x$ gives $\pi_2(x) \ll x (\log\log x)^2 / \log^2 x$. By partial summation, $\sum 1/p$ over the twin primes converges, because $\int^\infty (\log\log t)^2 / (t \log^2 t)\, dt$ is finite. Numerically there are $8169$ twin prime pairs with $p + 2 \le 10^6$, and the sum of $1/p + 1/(p+2)$ over them is $1.710777$; at $10^7$ there are $58980$ pairs and the sum is $1.738357$. The limit, Brun's constant, is estimated at about $1.90216$, but that estimate is an extrapolation that assumes the Hardy-Littlewood conjecture; no proved digits follow from these partial sums.
- **Almost primes.** The lower bound version (odd $m$), with $z$ a small power of $x$, shows that many $n$ have $n$ and $n+2$ both free of prime factors below $x^{c}$, hence each with at most $1/c$ prime factors. Brun used this to show that every large even number is a sum of two numbers each with at most nine prime factors.

## Variations

- **Brun's combinatorial sieve.** Instead of one truncation level $m$, keep $d = p_1 p_2 \cdots p_k$ (with $p_1 > p_2 > \cdots$) only when each $p_j$ is below a threshold depending on $p_1, \ldots, p_{j-1}$, chosen so that $d$ stays below a level $D$. This removes the $\log\log$ loss: $\pi_2(x) = O(x/\log^2 x)$, and for sifting $X^{c}$-rough numbers one gets the fundamental lemma $S = X W(z)(1 + O(e^{-s}))$ with $s = \log D/\log z$.
- **Beta sieve (Rosser-Iwaniec).** A specific choice of the truncation rule that is optimal in dimension 1; it gives the linear sieve with the sharp functions $F$ and $f$.
- **Selberg's sieve.** For upper bounds, replacing the combinatorial weights by optimized quadratic weights gives better constants with less work; see [Selberg's sieve](/selberg-sieve/).
- **Bonferroni in probability.** The same truncated inclusion-exclusion bounds the probability of a union of events; Step 3 above is that version.

## Pitfalls

- **Wrong parity of $m$.** Only even $m$ gives an upper bound. The table above shows how large the error of a wrongly signed bound can be.
- **Truncating too early.** With $m$ fixed and $z$ growing, $L^{m+1}/(m+1)!$ grows like $(\log\log z)^{m+1}$ while $W(z)$ tends to zero, so the "main term" is swamped. The level $m$ must grow with $\log\log X$.
- **Sifting too far.** Taking $z$ close to $X^{1/2}$, as in Eratosthenes, makes $z^m$ exceed $X$; the pure sieve is a method for $z = X^{o(1)}$ only.
- **Overstating the twin prime result.** The sieve gives an upper bound of the conjectured order, not a lower bound; it does not show there are infinitely many twin primes. That would need a way around the parity problem described in [sieve theory](/sieve-theory/).
- **Reading Brun's constant as known.** Its digits come from extrapolating finite sums with a conjectural error term.

## Exercises

1. Prove $\sum_{j=0}^{m}(-1)^j\binom{\nu}{j} = (-1)^m\binom{\nu-1}{m}$ for $\nu \ge 1$ by induction on $m$.
2. With $g(d) = 1/d$ and $\mathcal{A} = \{1, \ldots, x\}$, show that the pure sieve gives $\pi(x) \ll x \log\log x / \log x$.
3. Check the table above by computing $\sum_{\omega(d) \le m}\mu(d)\lfloor 10^6/d\rfloor$ for the divisors $d$ of $2 \cdot 3 \cdots 29$.

## References
