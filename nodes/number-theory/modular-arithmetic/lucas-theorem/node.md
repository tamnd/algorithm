---
tag: Q523G2
kind: theorem
slug: lucas-theorem
name: Lucas's theorem
aliases:
- Lucas's binomial theorem mod p
area: number-theory/modular-arithmetic
level: advanced
summary: Gives binomial coefficients mod a prime p from the base-p digits of the arguments.
prereqs: [binomial-coefficient, congruence]
see_also: [binomial-coefficient-computation, legendre-formula, wilson-theorem, fermat-little-theorem, pascal-triangle-dp, chinese-remainder-theorem, modular-inverse, binomial-theorem]
sources:
  - paper: "Édouard Lucas, Sur les congruences des nombres eulériens et des coefficients différentiels des fonctions trigonométriques suivant un module premier, Bulletin de la Société Mathématique de France 6 (1878), 49 to 54"
    locator: pages 49 to 54
  - paper: "N. J. Fine, Binomial coefficients modulo a prime, American Mathematical Monthly 54 (1947), 589 to 592"
    locator: pages 589 to 592
  - paper: "Andrew Granville, Arithmetic properties of binomial coefficients I: Binomial coefficients modulo prime powers, in Organic Mathematics, CMS Conference Proceedings 20 (1997), 253 to 276"
    locator: pages 253 to 276
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 1.2.6, Binomial coefficients, Exercise 10 (Lucas's congruence) and the exercises that follow it
---

Lucas's theorem computes a [binomial coefficient](/binomial-coefficient/) modulo a prime $p$ digit by digit: if $n$ and $m$ have base-$p$ digits $n_k \ldots n_0$ and $m_k \ldots m_0$, then $\binom{n}{m} \equiv \prod_i \binom{n_i}{m_i} \pmod p$. Each factor has both arguments below $p$, so $\binom{n}{m} \bmod p$ for $n$ near $10^{18}$ costs $O(\log_p n)$ small binomials after a table of factorials modulo $p$. It also shows that $p \nmid \binom{n}{m}$ exactly when no digit of $m$ exceeds the matching digit of $n$, which explains the fractal pattern of Pascal's triangle modulo $p$. Édouard Lucas published it in 1878. It holds only for prime moduli; prime powers need Granville's extension.

## Statement

**Theorem (Lucas, 1878).** Let $p$ be a prime, and let $n, m \ge 0$ be integers with base-$p$ expansions

$$n = \sum_{i=0}^{k} n_i p^i, \qquad m = \sum_{i=0}^{k} m_i p^i, \qquad 0 \le n_i, m_i < p.$$

Then

$$\binom{n}{m} \equiv \prod_{i=0}^{k} \binom{n_i}{m_i} \pmod p,$$

with the convention $\binom{a}{b} = 0$ for $b > a$. Equivalently, in recursive form,

$$\binom{n}{m} \equiv \binom{\lfloor n/p \rfloor}{\lfloor m/p \rfloor} \binom{n \bmod p}{m \bmod p} \pmod p.$$

In particular, $p \mid \binom{n}{m}$ if and only if $m_i > n_i$ for some digit $i$.

**Examples.** Modulo $p = 13$: $1000 = 5 \cdot 13^2 + 11 \cdot 13 + 12$ and $300 = 1 \cdot 13^2 + 10 \cdot 13 + 1$, so

$$\binom{1000}{300} \equiv \binom{5}{1}\binom{11}{10}\binom{12}{1} = 5 \cdot 11 \cdot 12 = 660 \equiv 10 \pmod{13}.$$

Modulo $p = 3$: $26 = 222_3$ and $8 = 022_3$, so $\binom{26}{8} \equiv \binom{2}{0}\binom{2}{2}\binom{2}{2} = 1$, and indeed $\binom{26}{8} = 1562275 = 3 \cdot 520758 + 1$. Also $10 = 101_3$ and $3 = 010_3$; the middle digit of 3 exceeds that of 10, so $3 \mid \binom{10}{3} = 120$.

Modulo $p = 10^9 + 7$: $10^{18} + 5 = 999999993 \cdot p + 54$ and $10^9 + 9 = 1 \cdot p + 2$, so

$$\binom{10^{18} + 5}{10^9 + 9} \equiv \binom{999999993}{1}\binom{54}{2} = 999999993 \cdot 1431 \equiv -14 \cdot 1431 \equiv 999979973 \pmod p.$$

Modulo $p = 2$: $\binom{n}{m}$ is odd exactly when every 1 digit of $m$ in binary is also a 1 digit of $n$, that is, when $m \mathbin{\&} n = m$.

## In plain words

To find a binomial coefficient modulo a prime, write both numbers in base p. Pair up their digits, one pair per position. For each pair, compute the small binomial coefficient of the two digits. Multiply these small results together and reduce modulo p. If any digit of the lower number is bigger than the matching digit of the upper number, the result is zero. Each small coefficient involves numbers below p, so the work grows with the number of digits, not with the size of the numbers.

## Proof

**Lemma 1.** For a prime $p$ and $0 < j < p$, $p \mid \binom{p}{j}$.

*Proof.* $\binom{p}{j} = \frac{p!}{j!(p-j)!}$. The prime $p$ divides the numerator once and does not divide $j!(p-j)!$, since all factors there are less than $p$. Since $\binom{p}{j}$ is an integer, $p$ divides it. $\square$

**Lemma 2.** In the polynomial ring $\mathbb{Z}_p[x]$, $(1 + x)^p = 1 + x^p$, and more generally $(1 + x)^{p^i} = 1 + x^{p^i}$ for all $i \ge 0$.

*Proof.* Expand by the [binomial theorem](/binomial-theorem/): $(1 + x)^p = \sum_j \binom{p}{j} x^j$, and the middle terms vanish modulo $p$ by Lemma 1. For the general case, induct on $i$: $(1 + x)^{p^{i+1}} = ((1 + x)^{p^i})^p = (1 + x^{p^i})^p = 1 + x^{p^{i+1}}$, the last step by the case already shown with $x^{p^i}$ in place of $x$. $\square$

**Proof of the theorem.** In $\mathbb{Z}_p[x]$, by Lemma 2,

$$(1 + x)^n = \prod_{i=0}^{k} \left((1 + x)^{p^i}\right)^{n_i} = \prod_{i=0}^{k} \left(1 + x^{p^i}\right)^{n_i} = \prod_{i=0}^{k} \sum_{j_i = 0}^{n_i} \binom{n_i}{j_i} x^{j_i p^i}.$$

Multiplying out, each choice of indices $(j_0, \ldots, j_k)$ with $0 \le j_i \le n_i$ gives the term $\prod_i \binom{n_i}{j_i} \cdot x^{\sum_i j_i p^i}$. Since $0 \le j_i \le n_i < p$, the exponent $\sum_i j_i p^i$ is a number whose base-$p$ digits are $j_0, \ldots, j_k$, and base-$p$ expansions are unique. So the exponent equals $m$ for at most one choice, namely $j_i = m_i$ for all $i$, and that choice is allowed exactly when $m_i \le n_i$ for all $i$.

On the left, the coefficient of $x^m$ is $\binom{n}{m} \bmod p$. On the right, it is $\prod_i \binom{n_i}{m_i}$ if all $m_i \le n_i$, and 0 otherwise. With the convention $\binom{a}{b} = 0$ for $b > a$, both cases read $\prod_i \binom{n_i}{m_i}$. Two polynomials over $\mathbb{Z}_p$ are equal only if their coefficients are equal, which proves the congruence.

The recursive form is the same statement split into the lowest digit and the rest: $\lfloor n/p \rfloor$ and $\lfloor m/p \rfloor$ have digits $n_k \ldots n_1$ and $m_k \ldots m_1$. The divisibility statement follows because each $\binom{n_i}{m_i}$ with $m_i \le n_i < p$ divides $n_i!$, which is not divisible by $p$, while a factor with $m_i > n_i$ is 0. $\blacksquare$

## Consequences

- **Computing $\binom{n}{m} \bmod p$.** Precompute $j! \bmod p$ for $j < p$ and their inverses, in $O(p)$ time. Then each query takes $O(\log_p n)$ digit steps, with $\binom{a}{b} = a! \cdot (b!)^{-1} \cdot ((a - b)!)^{-1}$ for each digit pair, using [modular inverses](/modular-inverse/), which exist because the factorials of numbers below $p$ are coprime to $p$. For a squarefree modulus $M = p_1 \cdots p_r$, apply the theorem modulo each $p_i$ and combine by the [Chinese remainder theorem](/chinese-remainder-theorem/).
- **Counting entries not divisible by $p$ (Fine, 1947).** The number of $m \in \{0, \ldots, n\}$ with $p \nmid \binom{n}{m}$ is $\prod_i (n_i + 1)$, since each digit $m_i$ ranges over $0, \ldots, n_i$. For $p = 2$, row $n$ of Pascal's triangle has $2^{s(n)}$ odd entries, where $s(n)$ is the number of 1 digits of $n$. Row 100 has $2^3 = 8$ odd entries, and row 26 has $27$ entries prime to 3.
- **Self-similarity.** Pascal's triangle modulo $p$ has a fractal structure: the first $p^{k+1}$ rows are made of $p^k$-row copies of the first $p^k$ rows, each multiplied by $\binom{a}{b}$ for its block position $(a, b)$. Modulo 2 this is the Sierpinski triangle.
- **Rows of the form $p^k$ and $p^k - 1$.** $p \mid \binom{p^k}{m}$ for $0 < m < p^k$. All digits of $p^k - 1$ equal $p - 1$, so $\binom{p^k - 1}{m} \not\equiv 0$ for every $m$, and $\binom{p - 1}{m} \equiv (-1)^m \pmod p$.
- **Scaling.** $\binom{np}{mp} \equiv \binom{n}{m} \pmod p$, since the lowest digits are $0$ and $0$.
- **Central binomial coefficients.** $\binom{2n}{n}$ is even for all $n \ge 1$, because the lowest 1 digit of $n$ in binary sits above a 0 digit of $2n$: if that digit is in position $j$, then digit $j$ of $2n$ is digit $j - 1$ of $n$, which is 0.
- **Kummer's theorem.** The exponent of $p$ in $\binom{m + r}{m}$ is the number of carries when $m$ and $r$ are added in base $p$ (Kummer, 1852). No carry means no digit of $m$ exceeds the corresponding digit of $m + r$, so this extends the divisibility statement. For example, adding $3 = 10_3$ and $7 = 21_3$ makes one carry, and $\binom{10}{3} = 120$ has exactly one factor 3. It follows from [Legendre's formula](/legendre-formula/).

## Tightness

The theorem fails for prime powers and for composite moduli. Modulo 4, the digits of 4 and 2 in base 4 are $10$ and $02$, so the product formula predicts $\binom{0}{2}\binom{1}{0} = 0$, but $\binom{4}{2} = 6 \equiv 2 \pmod 4$. Modulo 6, it predicts $\binom{6}{3} \equiv 0$, but $\binom{6}{3} = 20 \equiv 2 \pmod 6$. The proof breaks at Lemma 1: $\binom{4}{2} = 6$ is not divisible by 4, so $(1 + x)^4 \ne 1 + x^4$ in $\mathbb{Z}_4[x]$.

Stronger congruences hold for special arguments. Babbage (1819) proved $\binom{2p - 1}{p - 1} \equiv 1 \pmod{p^2}$ for $p \ge 3$, and Wolstenholme (1862) improved this to $p^3$ for $p \ge 5$. More generally $\binom{np}{mp} \equiv \binom{n}{m} \pmod{p^3}$ for $p \ge 5$. For general arguments modulo $p^e$, Granville (1997) gave a digit-by-digit formula in terms of products of integers prime to $p$, and Davis and Webb (1990) gave an earlier version. Modulo a general $M$, the usual method factors $M$, works modulo each prime power with such formulas, and combines by the Chinese remainder theorem.

## History

Édouard Lucas proved the theorem in 1878, in a short note in the Bulletin de la Société Mathématique de France, and used it in his long memoir on Lucas sequences in the American Journal of Mathematics the same year. Kummer had found the carry rule for the exact power of $p$ in 1852. The count of odd entries in a row of Pascal's triangle is due to Glaisher (1899), and Fine (1947) gave the count of entries prime to $p$ for any prime. The fractal picture of Pascal's triangle modulo a prime became popular in the 1980s with the study of cellular automata. Granville's 1997 survey collects the extensions to prime powers.

## References
