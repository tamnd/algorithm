---
tag: T8ANBE
kind: definition
slug: sturmian-word
name: Sturmian word
aliases:
- Sturmian sequence
- mechanical word
area: strings/string-combinatorics
level: advanced
summary: An aperiodic balanced infinite binary word with subword complexity n+1.
prereqs: [subword-complexity, morse-hedlund-theorem]
see_also: [sturmian-characterization, fibonacci-word, christoffel-word, morphic-word, abelian-complexity, continued-fraction, thue-morse-word, lyndon-word]
sources:
  - book: isbn:9780521812207
    title: M. Lothaire, Algebraic Combinatorics on Words, Encyclopedia of Mathematics and its Applications 90, Cambridge University Press, 2002
    locator: Chapter 2, Sturmian words (J. Berstel and P. Séébold), on balanced and mechanical words, standard words, special factors and Sturmian morphisms
  - paper: "Marston Morse and Gustav A. Hedlund, Symbolic dynamics II. Sturmian trajectories, American Journal of Mathematics 62(1), 1940, 1-42"
    locator: the introduction of Sturmian sequences and their description by rotations of the circle
  - book: isbn:9780521823326
    title: Jean-Paul Allouche and Jeffrey Shallit, Automatic Sequences, Cambridge University Press, 2003
    locator: Chapter 9, Characteristic words, and Chapter 10, Subword complexity
  - paper: "Ethan M. Coven and Gustav A. Hedlund, Sequences with minimal block growth, Mathematical Systems Theory 7, 1973, 138-153"
    locator: the sequences with exactly n + 1 blocks of length n
---

A Sturmian word is an infinite binary word with exactly $n + 1$ distinct factors of each length $n$. By the [Morse-Hedlund theorem](/morse-hedlund-theorem/) no aperiodic word has fewer, so Sturmian words are the simplest words that never become periodic. They are also the aperiodic balanced words and the codings of a line of irrational slope, as the [Sturmian characterization theorem](/sturmian-characterization/) shows, and the [Fibonacci word](/fibonacci-word/) is the standard example.

## Definition

Words are over the binary [alphabet](/alphabet/) $\{0, 1\}$, and an infinite word $x = x[0]\,x[1]\,x[2] \cdots$ is indexed from 0. For $n \ge 0$, $p_x(n)$ is the number of distinct factors of $x$ of length $n$, its [subword complexity](/subword-complexity/), and $|u|_1$ is the number of 1s in a finite word $u$.

**Sturmian word.** An infinite word $x$ is *Sturmian* if $p_x(n) = n + 1$ for every $n \ge 0$.

Since $p_x(1) = 2$, the word uses both letters, and since $p_x(n) \le n$ never holds, $x$ is not ultimately periodic by the Morse-Hedlund theorem.

**Balanced word.** A finite or infinite word $w$ is *balanced* if $\bigl||u|_1 - |v|_1\bigr| \le 1$ for all factors $u, v$ of $w$ with $|u| = |v|$.

**Mechanical word.** For a real $\alpha$ with $0 \le \alpha \le 1$, the *slope*, and a real $\rho$, the *intercept*, the lower and upper mechanical words are
$$ s_{\alpha,\rho}[n] = \lfloor (n+1)\alpha + \rho \rfloor - \lfloor n\alpha + \rho \rfloor, \qquad s'_{\alpha,\rho}[n] = \lceil (n+1)\alpha + \rho \rceil - \lceil n\alpha + \rho \rceil \qquad (n \ge 0). $$
So $s_{\alpha,\rho}[n] = 1$ exactly when the fractional part of $n\alpha + \rho$ lies in $[1 - \alpha, 1)$: the word records which steps of the rotation by $\alpha$ on the circle of length 1 land in a fixed arc of length $\alpha$, or which unit columns the line $y = \alpha t + \rho$ crosses a horizontal grid line in. A mechanical word of rational slope is periodic.

**The three views agree.** For an infinite binary word $x$, these are equivalent: $x$ is Sturmian; $x$ is balanced and not ultimately periodic; $x$ is a lower or upper mechanical word with irrational slope. This is the [Sturmian characterization theorem](/sturmian-characterization/), and any of the three is used as the definition, which is why Sturmian words are also called mechanical words. The slope $\alpha$ is the frequency of the letter 1 in $x$.

**Characteristic word.** For irrational $\alpha \in (0, 1)$, the *characteristic word* of slope $\alpha$ is $c_\alpha = s_{\alpha,\alpha}$, that is, $c_\alpha[n] = \lfloor (n+2)\alpha \rfloor - \lfloor (n+1)\alpha \rfloor$. Then $s_{\alpha,0} = 0\,c_\alpha$ and $s'_{\alpha,0} = 1\,c_\alpha$.

## Examples and non-examples

The table lists infinite binary words with their first 24 letters and the values $p(1), \ldots, p(8)$.

| word | first letters | $p(1), \ldots, p(8)$ | balanced | Sturmian |
| --- | --- | --- | --- | --- |
| Fibonacci word, $c_\alpha$ with $\alpha = (3 - \sqrt5)/2$ | `010010100100101001010010` | $2, 3, 4, 5, 6, 7, 8, 9$ | yes | yes |
| $c_\alpha$ with $\alpha = \sqrt2 - 1$ | `010100101001010100101001` | $2, 3, 4, 5, 6, 7, 8, 9$ | yes | yes |
| $s_{\alpha,\rho}$ with $\alpha = \pi - 3$, $\rho = 1/2$ | `000100000010000001000000` | $2, 3, 4, 5, 6, 7, 8, 9$ | yes | yes |
| [Thue-Morse word](/thue-morse-word/) | `011010011001011010010110` | $2, 4, 6, 10, 12, 16, 20, 22$ | no | no |
| $(01)^\omega$ | `010101010101010101010101` | $2, 2, 2, 2, 2, 2, 2, 2$ | yes | no |
| $1\,0^\omega$ | `100000000000000000000000` | $2, 2, 2, 2, 2, 2, 2, 2$ | yes | no |

- **The Fibonacci word.** The fixed point $0100101001001\cdots$ of the [morphism](/morphic-word/) $0 \mapsto 01$, $1 \mapsto 0$ equals the characteristic word of slope $\alpha = (3 - \sqrt5)/2 \approx 0.382$, the frequency of its letter 1; this was checked letter by letter on the first 20000 letters. Its lower mechanical word with intercept 0 is $0\,c_\alpha$, and $1\,c_\alpha$ is Sturmian too.
- **Other slopes.** Every irrational $\alpha \in (0, 1)$ and every intercept $\rho$ give a Sturmian word, so there are uncountably many. For the three Sturmian words of the table, the complexity was checked to be $n + 1$ for $n \le 8$ and the balance for factors of length up to 30, on prefixes of 20000 letters.
- **Thue-Morse.** It is aperiodic but has the factors `00` and `11`, so it is not balanced, and $p(2) = 4$.
- **Periodic balanced words.** $(01)^\omega$ is balanced, a mechanical word of slope $1/2$, but periodic, with $p(n) = 2$. The word $1\,0^\omega$ is balanced and ultimately periodic. Neither is Sturmian; this is why the characterization requires aperiodicity.
- **Finitely many lengths are not enough.** The word $0^N\,1\,0^\omega$ has $p(n) = n + 1$ for $n \le N + 1$ but is ultimately periodic, so no finite set of values of $p$ decides that a word is Sturmian.
- **Suffixes.** Every suffix of a Sturmian word is Sturmian: its factors are factors of the word, so $p(n) \le n + 1$, and it is still aperiodic, so $p(n) \ge n + 1$.

## Related definitions

- **Finite balanced words.** The finite factors of Sturmian words are exactly the finite balanced binary words. Their number for length $n$ is $1 + \sum_{i=1}^{n} (n - i + 1)\,\varphi(i)$, with $\varphi$ the [Euler totient](/euler-totient/), giving $1, 2, 4, 8, 14, 24, 36, 54, 76, 104$ for $n = 0, \ldots, 9$; the formula was checked against exhaustive enumeration for $n \le 14$. The [Christoffel words](/christoffel-word/) are the balanced words that are also Lyndon words.
- **Standard words.** If $\alpha = [0; 1 + d_1, d_2, d_3, \ldots]$ is the [continued fraction](/continued-fraction/) of $\alpha$, set $s_{-1} = 1$, $s_0 = 0$ and $s_k = s_{k-1}^{d_k}\,s_{k-2}$. Each $s_k$ is a prefix of $c_\alpha$, and $c_\alpha = \lim s_k$. For the Fibonacci word every $d_k = 1$ and the $s_k$ are the finite Fibonacci words $0, 01, 010, 01001, 01001010, \ldots$; for $\alpha = \sqrt2 - 1$, $d_1 = 1$ and $d_k = 2$ afterwards, giving $0, 01, 01010, 010100101001, \ldots$.
- **Special factors.** Since $p(n + 1) - p(n) = 1$, a Sturmian word has exactly one right special factor $u$ of each length, one with both $u0$ and $u1$ factors, and likewise exactly one left special factor. The set of factors depends only on the slope, is closed under reversal, and its left special factors are the prefixes of $c_\alpha$. These facts were checked for lengths up to 12 on several intercepts for the two slopes of the table.
- **Abelian complexity.** A balanced aperiodic binary word has exactly two values of $|u|_1$ among its factors $u$ of each length $n \ge 1$, so its [abelian complexity](/abelian-complexity/) is constantly 2.
- **Sturmian morphisms.** A morphism is Sturmian if it maps every Sturmian word to a Sturmian word. They form the monoid generated by the exchange $0 \leftrightarrow 1$, the Fibonacci morphism $0 \mapsto 01$, $1 \mapsto 0$, and $0 \mapsto 10$, $1 \mapsto 0$.
- **Larger alphabets.** Arnoux-Rauzy words over $k$ letters have one left and one right special factor of each length, each extended by all $k$ letters, so $p(n) = (k - 1)n + 1$; the fixed point of $a \mapsto ab$, $b \mapsto ac$, $c \mapsto a$, the Tribonacci word, is one. Episturmian words generalize further, keeping closure under reversal.

## References
