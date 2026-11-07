---
tag: JZS0VF
kind: concept
slug: scholz-brauer-conjecture
name: Scholz-Brauer conjecture
aliases:
- Scholz conjecture
- Scholz-Brauer addition chain conjecture
- Scholz-Brauer problem
area: algebra/integer-arithmetic
level: research
summary: Conjectured bound l(2^n - 1) <= n - 1 + l(n) on the length of addition chains; open.
prereqs: [addition-chain, binary-exponentiation]
see_also: [addition-chain, addition-chain-problem, integer-exponentiation, sliding-window-exponentiation, binary-exponentiation, mersenne-prime, modular-exponentiation]
sources:
  - paper: A. Scholz, Aufgabe 253, Jahresbericht der Deutschen Mathematiker-Vereinigung 47, 1937
    title: Arnold Scholz, Aufgabe 253
    locator: Part II, pp. 41 to 42 (the problem as posed, with the conjectured inequality)
  - paper: doi:10.1090/S0002-9904-1939-07068-7
    title: Alfred Brauer, On addition chains, Bulletin of the American Mathematical Society 45(10), 1939
    locator: pp. 736 to 739 (star chains, the inequality for star chains, and the 2^k-ary upper bound)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.3, Evaluation of powers (star chains, Hansen's l^0 chains, the numbers with l(n) < l*(n), and the discussion of l(2^n - 1) in the text and exercises)
  - paper: W. Hansen, Zum Scholz-Brauerschen Problem, Journal für die reine und angewandte Mathematik 202, 1959
    title: Walter Hansen, Zum Scholz-Brauerschen Problem
    locator: pp. 129 to 136 (the conjecture for l^0 chains, and star chains that are not optimal)
  - paper: Neill Michael Clift, Calculating optimal addition chains, Computing 91(3), 2011
    title: Neill Michael Clift, Calculating optimal addition chains, Computing 91(3), 2011
    locator: pp. 265 to 284 (the computation of l(n) and the check of l(2^n - 1) = n - 1 + l(n) for small n)
  - paper: Toshiya Itoh and Shigeo Tsujii, A fast algorithm for computing multiplicative inverses in GF(2^m) using normal bases, Information and Computation 78(3), 1988
    title: Toshiya Itoh and Shigeo Tsujii, A fast algorithm for computing multiplicative inverses in GF(2^m) using normal bases, Information and Computation 78(3), 1988
    locator: pp. 171 to 177 (inversion by x^(2^m - 2) with an addition chain for m - 1)
---

The Scholz-Brauer conjecture says that the number $2^n - 1$, written in binary as $n$ ones, has an addition chain of length at most $n - 1 + l(n)$, where $l(n)$ is the length of a shortest [addition chain](/addition-chain/) for $n$:

$$l(2^n - 1) \le n - 1 + l(n) .$$

In terms of powers: $x^{2^n - 1}$ can be computed from $x$ with $n - 1$ squarings and $l(n)$ further multiplications. Arnold Scholz posed it in 1937. Alfred Brauer proved it in 1939 for star chains, in which every step uses the previous element, so it holds for every $n$ whose shortest chain can be taken to be a star chain. This covers all small $n$, but not all $n$, and the general case is open. Computations by Clift and others have confirmed it, with equality, for all $n$ up to a fairly large bound.

## In plain words

An addition chain for a number is a list that starts at 1, in which each new entry is the sum of two earlier ones. A chain for 13 is 1, 2, 3, 6, 12, 13. The fewest steps needed is written $l(13)$. Such a chain says how to compute $x^{13}$ with as many multiplications as it has steps.

The numbers $2^n - 1$ are 1, 3, 7, 15, 31 and so on: in binary, all ones. For them, the plain binary method is bad, because every digit is a 1. Scholz guessed that you can always do it with $n - 1$ doublings plus only $l(n)$ additions, that is, by following the best chain for the small number $n$. Nobody has proved this for every $n$, and nobody has found an $n$ where it fails.

## The idea

**Brauer's construction.** Let $1 = a_0 < a_1 < \cdots < a_r = n$ be an addition chain in which each $a_i = a_{i-1} + a_j$ for some $j < i$: a star chain, or Brauer chain. Write $E(a) = 2^a - 1$. Then

$$E(a_{i-1} + a_j) = E(a_{i-1}) \cdot 2^{a_j} + E(a_j),$$

so from $E(a_{i-1})$ we reach $E(a_i)$ by $a_j$ doublings and one addition of $E(a_j)$, which is already in the chain. The doublings add up to $\sum_i (a_i - a_{i-1}) = n - 1$, and there are $r$ additions, so $2^n - 1$ has a chain of length $n - 1 + r$. Writing $l^*(n)$ for the length of a shortest star chain, this proves $l(2^n - 1) \le n - 1 + l^*(n)$. The same chain computes $x^{2^n - 1}$ with $n - 1$ squarings and $r$ multiplications by earlier powers $x^{2^{a_j} - 1}$.

**Why this is not a proof.** Every shortest chain for small $n$ can be taken to be a star chain, so $l(n) = l^*(n)$ and the conjecture follows. But Hansen showed in 1959 that there are $n$ with $l^*(n) > l(n)$, where the optimal chains must use an element other than the last one; the smallest such $n$ is 12509, as reported in Knuth's Section 4.6.3. Hansen extended Brauer's argument to a wider class of chains, his $l^0$ chains, which proves the conjecture for every $n$ with $l(n) = l^0(n)$. Whether every $n$ has an optimal chain in this class, or whether the conjecture holds some other way, is not known.

**How close it is to the truth.** The general lower bound of Schönhage, $l(m) \ge \log_2 m + \log_2 \nu(m) - 2.13$ with $\nu(m)$ the number of ones of $m$ in binary, gives $l(2^n - 1) > n - 1 + \log_2 n - 1.55$ for $n \ge 2$, since $\log_2(2^n - 1) \ge n - 0.42$. With $l(n) \ge \log_2 n$, the conjectured bound and the lower bound differ by less than $l(n) - \log_2 n + 1.55$, which is $O(\log n / \log\log n)$ by Brauer's upper bound on $l(n)$. So the conjecture, if true, determines $l(2^n - 1)$ up to this small error, much more precisely than for a typical number.

**What is known.** The inequality holds whenever $l(n) = l^*(n)$ (Brauer) or $l(n) = l^0(n)$ (Hansen), and for all $n$ up to the bounds of exhaustive computations. Clift's algorithm for optimal chains (2011) found that equality $l(2^n - 1) = n - 1 + l(n)$ holds for all $n \le 64$, and later computations reported the conjecture for all $n$ below about $5.8 \cdot 10^6$. No counterexample is known. It is also open whether equality always holds.

## Examples

All values were computed by an exhaustive search over addition chains, by script.

- **$n = 5$.** The star chain $1, 2, 4, 5$ has $l(5) = 3$ steps. Brauer's construction gives the chain $1, 2, 3, 6, 12, 15, 30, 31$ for $2^5 - 1 = 31$: from $E(1) = 1$, one doubling and adding $1$ gives $E(2) = 3$; two doublings and adding $3$ give $E(4) = 15$; one doubling and adding $1$ give $E(5) = 31$. It has $7 = 4 + 3$ steps, and $l(31) = 7$.
- **Small $n$, with equality.** For $n = 1, \ldots, 9$, the search gives $l(n) = 0, 1, 2, 2, 3, 3, 4, 3, 4$ and $l(2^n - 1) = 0, 2, 4, 5, 7, 8, 10, 10, 12$, which is exactly $n - 1 + l(n)$ each time. For $n = 7$, a shortest chain for 127 is $1, 2, 4, 8, 16, 32, 40, 42, 84, 126, 127$, with 10 steps.
- **Against the binary method.** The binary method computes $x^{2^n - 1}$ with $n - 1$ squarings and $n - 1$ multiplications, since all $n$ digits are 1. For $n = 64$ it uses 126 steps, against $63 + l(64) = 69$.
- **Inversion in $\mathrm{GF}(2^{163})$.** There $x^{-1} = x^{2^{163} - 2} = (x^{2^{162} - 1})^2$. The star chain $1, 2, 4, 8, 16, 32, 64, 128, 160, 162$ for 162 has 9 steps, and $l(162) = 9$: 162 has 8 binary digits and three ones, and a number with at least three ones needs at least 2 steps more than its number of binary digits minus 1 (Knuth, Section 4.6.3). So the inverse costs 162 squarings and 9 multiplications.

## Where it is used

- **Inversion in binary fields.** The Itoh-Tsujii method (1988) computes $x^{-1} = x^{2^m - 2}$ in $\mathrm{GF}(2^m)$ by Brauer's construction for $m - 1$. Squarings are cheap in such fields, nearly free with a normal basis, so the cost is dominated by the $l(m - 1)$ multiplications. It is used in elliptic curve cryptography over binary fields, and in the analogous form $x^{(p^m - 1)/(p - 1)}$ for other extension fields.
- **Powers with all-ones exponents.** Exponents near $2^n - 1$ appear in Fermat inversion $x^{p-2} \bmod p$ for primes such as Mersenne primes and the primes $2^{255} - 19$ and $2^{521} - 1$ of elliptic curve cryptography, where hand-made chains follow Brauer's idea; see [modular exponentiation](/modular-exponentiation/).
- **The theory of addition chains.** The conjecture is a test case for the structure of optimal chains, for the difference between star chains and general chains, and for the computer searches of the [addition chain problem](/addition-chain-problem/).

## References
