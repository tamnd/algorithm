---
tag: J8QR5C
kind: definition
slug: addition-chain
name: Addition chain
aliases:
- addition chain for n
- star chain
- Brauer chain
area: algebra/integer-arithmetic
level: advanced
summary: A sequence starting at 1 where each term is the sum of two earlier terms, ending at n.
prereqs: [integer-exponentiation, binary-exponentiation]
see_also: [addition-chain-problem, scholz-brauer-conjecture, sliding-window-exponentiation, integer-exponentiation, non-adjacent-form, modular-exponentiation]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.3, Evaluation of powers (addition chains, star chains, the bounds on l(n) and the table of l(n))
  - paper: doi:10.1090/S0002-9904-1939-07068-7
    title: Alfred Brauer, On addition chains, Bulletin of the American Mathematical Society 45(10), 1939
    locator: pp. 736 to 739 (the 2^k-ary upper bound and star chains)
  - paper: doi:10.1016/0304-3975(75)90008-0
    title: Arnold Schönhage, A lower bound for the length of addition chains, Theoretical Computer Science 1(1), 1975
    locator: pp. 1 to 12 (the bound l(n) >= log2 n + log2 v(n) - 2.13)
  - paper: P. Erdős, Remarks on number theory III. On addition chains, Acta Arithmetica 6, 1960
    title: Paul Erdős, Remarks on number theory III. On addition chains
    locator: pp. 77 to 81 (the lower bound for almost all n that matches Brauer's upper bound)
---

An addition chain for a positive integer $n$ is a sequence of integers that starts at 1, ends at $n$, and in which every term after the first is the sum of two earlier terms, possibly the same term twice. Its length is the number of additions, one less than the number of terms. An addition chain is a program for computing $x^n$ by multiplications alone: each sum $a_j + a_k$ becomes the product $x^{a_j} \cdot x^{a_k}$, so the shortest chain gives the fewest multiplications. [Binary exponentiation](/binary-exponentiation/) is one particular chain; finding a shortest one is the [addition chain problem](/addition-chain-problem/).

## Definition

An *addition chain* for $n \ge 1$ is a sequence of integers

$$1 = a_0 < a_1 < \cdots < a_r = n$$

such that for each $i$ with $1 \le i \le r$ there are indices $j \le k < i$ with $a_i = a_j + a_k$. The number $r$ is the *length* of the chain, and $\ell(n)$ denotes the least length of an addition chain for $n$. A step with $j = k = i - 1$ is a *doubling*. A step with $k = i - 1$, which uses the previous term, is a *star step*, and a chain made only of star steps is a *star chain*, or Brauer chain; $\ell^*(n)$ is the least length of a star chain for $n$. Writing $\lambda(n) = \lfloor \log_2 n \rfloor$ and $\nu(n)$ for the number of 1s in the binary form of $n$, a step is *small* if $\lambda(a_i) = \lambda(a_{i-1})$, and the number of small steps of a chain of length $r$ is $r - \lambda(n)$.

Requiring the terms to increase loses nothing: any sequence with the sum property that reaches $n$ can be sorted and stripped of repeated terms and of terms larger than $n$, and it stays a chain of no greater length.

**Basic facts.**

- *Lower bound.* $a_i \le 2^i$ by induction, since $a_i \le 2a_{i-1}$. So $\ell(n) \ge \lceil \log_2 n \rceil$, with equality for powers of 2.
- *The binary chain.* Doubling for each bit of $n$ after the leading one and adding 1 for each further 1 bit gives a star chain of length $\lambda(n) + \nu(n) - 1$. So $\ell(n) \le \ell^*(n) \le \lambda(n) + \nu(n) - 1$.
- *Products.* $\ell(mn) \le \ell(m) + \ell(n)$: follow a chain for $m$, then a chain for $n$ with every term multiplied by $m$.
- *Asymptotics.* The $2^k$-ary method gives $\ell(n) \le \lambda(n) + (1 + o(1)) \lambda(n) / \lambda(\lambda(n))$ (Brauer, 1939), and Erdős (1960) proved that this is the right value for almost all $n$. Schönhage (1975) proved $\ell(n) \ge \log_2 n + \log_2 \nu(n) - 2.13$ for every $n$.

**Theorem.** For every $n \ge 1$, $\lceil \log_2 n \rceil \le \ell(n) \le 2 \lfloor \log_2 n \rfloor$.

*Proof.* The lower bound is the first basic fact. For the upper bound, the binary chain has length $\lambda(n) + \nu(n) - 1$, and $\nu(n) \le \lambda(n) + 1$. $\blacksquare$

## Examples and non-examples

**Chains for 15.** The binary chain is $1, 2, 3, 6, 7, 14, 15$, of length 6: it reads the bits $1111$ by doubling and adding 1. The chain $1, 2, 3, 6, 12, 15$, with $15 = 12 + 3$, has length 5, and so does $1, 2, 4, 5, 10, 15$. No chain of length 4 reaches 15. If step $i$ is not a doubling, then $a_i = a_j + a_k$ with $j \le i - 2$, so $a_i \le a_{i-1} + a_{i-2} \le 3 \cdot 2^{i-2}$, and the later terms at most double; so a chain of length $r$ with a non-doubling step ends at most at $3 \cdot 2^{r-2}$, which is 12 for $r = 4$, and the all-doubling chain ends at 16. So $\ell(15) = 5$. So 15 is the smallest $n$ for which the binary method is not optimal: $x^{15} = (x^3)^{4} \cdot x^3$ needs 5 multiplications, not 6.

**Small values.** A search over all chains, run for this page, gives the values of $\ell(n)$ for $n = 1, \ldots, 20$:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\ell(n)$ | 0 | 1 | 2 | 2 | 3 | 3 | 4 | 3 | 4 | 4 | 5 | 4 | 5 | 5 | 5 | 4 | 5 | 5 | 6 | 5 |

Further values from the same search: $\ell(23) = 6$, by $1, 2, 4, 5, 9, 18, 23$; $\ell(31) = 7$; $\ell(127) = 10$; and $\ell(191) = \ell(382) = 11$, so doubling $n$ does not always lengthen the shortest chain.

**Star chains are not always enough.** The smallest $n$ with $\ell^*(n) > \ell(n)$ is $12509$, for which $\ell(12509) = 17$ and $\ell^*(12509) = 18$ (Knuth, Section 4.6.3, after Hansen).

**Non-examples.**

- $1, 2, 4, 7$ is not an addition chain: $7$ is not a sum of two of $1, 2, 4$.
- $1, 2, 4, 8, 16, 32, 31$ is not an addition chain, since $31 = 32 - 1$ uses a subtraction; it is an *addition-subtraction chain* of length 6, while $\ell(31) = 7$. With division allowed, as on elliptic curves where inverses are cheap, such chains can be shorter.
- $1, 3, 4, 7$ is not an addition chain because $3$ is not a sum of earlier terms; every chain starts $1, 2$.

## Related definitions

- **Addition sequence.** A chain that contains each of several given numbers $n_1, \ldots, n_m$, used to compute several powers of one base at once. Deciding whether a short addition sequence exists is NP-complete (Downey, Leong and Sethi, 1981); see the [addition chain problem](/addition-chain-problem/).
- **Vectorial addition chain.** A chain of vectors starting from the unit vectors, used to compute $x_1^{e_1} \cdots x_k^{e_k}$. By Olivos's duality, a vectorial chain for the rows of a matrix and an addition sequence for its columns have related lengths.
- **Lucas chain**, or differential addition chain. A chain where each sum $a_j + a_k$ with $j \ne k$ also has its difference $a_j - a_k$ in the chain. It is what the Montgomery ladder and Lucas sequences need, since there $x^{a_j + a_k}$ is computed from $x^{a_j}$, $x^{a_k}$ and $x^{a_j - a_k}$.
- **Windowed and signed-digit chains.** The $2^k$-ary and [sliding-window](/sliding-window-exponentiation/) methods produce star chains from a table of small odd powers; signed-digit forms such as the [non-adjacent form](/non-adjacent-form/) give addition-subtraction chains.
- **Scholz-Brauer conjecture.** The statement $\ell(2^n - 1) \le n - 1 + \ell(n)$, proved by Brauer for star chains; see the [Scholz-Brauer conjecture](/scholz-brauer-conjecture/).

## References
