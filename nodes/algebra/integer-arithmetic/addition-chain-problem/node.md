---
tag: 4GVP8H
kind: problem
slug: addition-chain-problem
name: Addition chain problem
aliases:
- shortest addition chain
- optimal addition chain
- addition sequence problem
area: algebra/integer-arithmetic
level: advanced
summary: Find a shortest addition chain for a given n; NP-complete for addition sequences, open for a single n.
model: word-ram
complexity:
  vars: {b: the number of binary digits of n}
  time: {worst: 2^(O(b log b))}
prereqs: [addition-chain, np-complete]
see_also: [addition-chain, scholz-brauer-conjecture, binary-exponentiation, sliding-window-exponentiation, integer-exponentiation, vertex-cover, iterative-deepening-search]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.3, Evaluation of powers (the factor method, the search for l(n), the tables of l(n) and the open questions)
  - paper: doi:10.1137/0210047
    title: Peter Downey, Benton Leong and Ravi Sethi, Computing sequences with addition chains, SIAM Journal on Computing 10(3), 1981
    locator: pp. 638 to 646 (NP-completeness of the shortest addition sequence for a set of numbers, by a reduction from vertex cover)
  - paper: doi:10.1137/S0097539795295663
    title: Edward G. Thurber, Efficient generation of minimal length addition chains, SIAM Journal on Computing 28(4), 1999
    locator: pp. 1247 to 1263 (the branch and bound search with lower bounds on the remaining steps)
  - paper: doi:10.1007/s00607-010-0118-8
    title: Neill M. Clift, Calculating optimal addition chains, Computing 91(3), 2011
    locator: pp. 265 to 284 (a faster search and the tabulation of l(n) for large ranges of n)
---

The addition chain problem asks for a shortest [addition chain](/addition-chain/) for a given positive integer $n$: a sequence $1 = a_0 < a_1 < \cdots < a_r = n$ in which each term is the sum of two earlier ones, with $r$ as small as possible. Its value $\ell(n)$ is the least number of multiplications that compute $x^n$ from $x$ when only products of computed powers are allowed. The problem is easy to state and surprisingly hard: the generalization to several targets, the *addition sequence problem*, is [NP-complete](/np-complete/) (Downey, Leong and Sethi, 1981), but for a single $n$ no polynomial algorithm and no NP-hardness proof is known. In practice it is solved by search for exponents up to a few dozen bits, and approximated within a factor $1 + o(1)$ by windowed methods.

## In plain words

You want to reach a number $n$ starting from 1, and at each step you may add together any two numbers you already have, or double one. The question is the fewest steps. Doubling alone reaches the powers of two quickly, but most numbers need a few extra additions, and finding the very best set of them is a puzzle.

This matters because each step is one multiplication when you compute a power: to get $x^{15}$, a good chain gives it in five multiplications instead of six. For a single power the saving is small, but if one exponent is used millions of times, as in cryptography, it is worth finding the best chain once.

## Definition

**Input.** A positive integer $n$, given in binary with $b = \lfloor \log_2 n \rfloor + 1$ digits.

**Output.** An addition chain $1 = a_0 < a_1 < \cdots < a_r = n$, with each $a_i = a_j + a_k$ for some $j \le k < i$, of the least length $r = \ell(n)$.

The decision version asks, for $n$ and $r$ given in binary, whether $\ell(n) \le r$. Since $\ell(n) \le 2\lfloor \log_2 n \rfloor$, a chain is a certificate of polynomial size, so the decision version is in NP.

**Cost model.** A word RAM with words of $O(b)$ bits, so each addition and comparison of chain terms costs $O(1)$. The search bound $2^{O(b \log b)}$ is proved; running times of the search programs are observed.

## Variants

- **Addition sequence.** Given $n_1 < \cdots < n_m$, find a shortest chain that contains all of them. This is the version proved NP-complete.
- **Star chains.** Restrict every step to use the previous term; the optimum $\ell^*(n)$ is at least $\ell(n)$ and equal to it for all $n < 12509$.
- **Vectorial addition chains.** Reach a vector $(e_1, \ldots, e_k)$ from the unit vectors, which computes $x_1^{e_1} \cdots x_k^{e_k}$. Olivos (1981) showed that this problem and the addition sequence problem are dual, with optimal lengths related by a simple formula in the number of targets and the dimension.
- **Addition-subtraction chains.** Subtraction is also allowed; useful when inverses are cheap, as on elliptic curves.
- **Lucas chains.** Each sum of two different terms must have its difference in the chain too; these drive the Montgomery ladder.
- **Weighted versions.** Doublings (squarings) are cheaper than general products, so the cost is $s \cdot (\text{doublings}) + (\text{other steps})$ with $s < 1$; the optimal chain can change.

## Examples

| $n$ | binary chain | length | shortest chain | $\ell(n)$ |
|---|---|---|---|---|
| 15 | 1, 2, 3, 6, 7, 14, 15 | 6 | 1, 2, 3, 6, 12, 15 | 5 |
| 23 | 1, 2, 4, 5, 10, 11, 22, 23 | 7 | 1, 2, 4, 5, 9, 18, 23 | 6 |
| 63 | 1, 2, 3, 6, 7, 14, 15, 30, 31, 62, 63 | 10 | 1, 2, 4, 8, 16, 20, 21, 42, 63 | 8 |
| 65537 | 1, 2, 4, ..., 65536, 65537 | 17 | the same | 17 |

The shortest chains were found by an exhaustive search with iterative deepening, run for this page; the value for $65537 = 2^{16} + 1$ follows from $\ell(n) \ge \lambda(n) + 1$ for $n$ not a power of 2. For $63 = 3 \cdot 21$ the factor method, a chain for 3 followed by a chain for 21 scaled by 3, gives $2 + 6 = 8$ steps.

## Known algorithms

- **Binary method.** The chain read off the binary digits of $n$ has length $\lambda(n) + \nu(n) - 1 \le 2 \lambda(n)$, where $\lambda(n) = \lfloor \log_2 n \rfloor$ and $\nu(n)$ is the number of 1 bits. Since $\ell(n) \ge \lceil \log_2 n \rceil$, this is within a factor 2 of the optimum, in time $O(b)$. See [binary exponentiation](/binary-exponentiation/).
- **$2^k$-ary and sliding-window methods.** With $k \approx \log_2 b - 2\log_2 \log_2 b$ they give chains of length $\lambda(n) + (1 + o(1)) \lambda(n) / \log_2 \lambda(n)$, which is $\ell(n)(1 + o(1))$ (Brauer, 1939). See [sliding-window exponentiation](/sliding-window-exponentiation/).
- **Factor method.** If $n = pq$, concatenate a chain for $p$ with a chain for $q$ scaled by $p$. It beats the binary method on 15, with 2 + 3 = 5 steps against 6, and loses on 33 = 3 · 11, with 2 + 5 = 7 steps against 6.
- **Exhaustive search.** Try all chains of length $r = \lceil \log_2 n \rceil, \lceil \log_2 n \rceil + 1, \ldots$, by [iterative deepening](/iterative-deepening-search/), and stop at the first that reaches $n$. Pruning by the bound $a_i 2^{r-i} \ge n$, and by stronger bounds on the number of small steps, makes it practical. Thurber (1999) and Clift (2011) gave the best such searches, which have tabulated $\ell(n)$ over large ranges.

## Bounds

**Upper bound on the search, proved.** There are at most $\binom{i+1}{2} \le (i+1)^2$ choices for step $i$ and at most $2b$ steps, so at most $(2b + 1)^{4b} = 2^{O(b \log b)}$ chains to try, each checked in $O(b)$ time.

**Value of $\ell(n)$, proved.** $\log_2 n + \log_2 \nu(n) - 2.13 \le \ell(n) \le \lambda(n) + \nu(n) - 1$, the lower bound by Schönhage (1975). Also $\ell(n) = \lambda(n) + (1 + o(1)) \lambda(n)/\log_2 \lambda(n)$ for almost all $n$, the upper bound by Brauer and the matching lower bound by Erdős (1960).

**Hardness, proved and open.** The addition sequence problem is NP-complete. Whether computing $\ell(n)$ for one $n$ is NP-hard is open; the reduction of Downey, Leong and Sethi needs many targets. No lower bound beyond the trivial one on the time to compute $\ell(n)$ is known.

## Reductions

- **Vertex cover to addition sequences.** Downey, Leong and Sethi encode a graph by numbers whose binary digits mark its vertices and edges, so that an addition sequence of a given length exists exactly when the graph has a [vertex cover](/vertex-cover/) of a given size.
- **Addition sequences and vectorial chains.** Olivos's duality turns each into the other, so the vectorial problem is also NP-hard.
- **Powering to chains.** Any algorithm that computes $x^n$ in a group using only products of computed powers yields an addition chain for $n$ of the same length, so $\ell(n)$ is the exact multiplication count for powering in this model.

## Applications

- **Fixed exponents in cryptography.** RSA verification with $e = 65537$, inversion by Fermat's little theorem $a^{p-2} \bmod p$ for a fixed prime $p$ such as $2^{255} - 19$, and square roots modulo fixed primes use hand-optimized chains, since the same exponent is used for every operation.
- **Inversion in binary fields.** The Itoh-Tsujii method computes inverses in $\mathrm{GF}(2^m)$ with a number of multiplications set by an addition chain for $m - 1$.
- **Compilers.** Constant powers $x^n$ in source code are expanded into short chains of multiplications.
- **Theory.** $\ell(n)$ is a basic measure in the study of the complexity of powering and of the [Scholz-Brauer conjecture](/scholz-brauer-conjecture/).

## References
