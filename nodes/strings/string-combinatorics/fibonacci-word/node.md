---
tag: 4ABXXT
kind: definition
slug: fibonacci-word
name: Fibonacci word
aliases:
- Fibonacci infinite word
area: strings/string-combinatorics
level: core
summary: The fixed point of the morphism a to ab, b to a, a Sturmian word.
prereqs: [morphic-word, sturmian-word]
see_also: [fibonacci-numbers, zeckendorf-theorem, christoffel-word, subword-complexity, maximal-repetition, thue-morse-word, knuth-morris-pratt, computing-runs]
sources:
  - paper: doi:10.1007/978-3-642-95486-3_2
    title: Jean Berstel, Fibonacci words, a survey, in G. Rozenberg and A. Salomaa (eds.), The Book of L, Springer, 1986, 13-27
    locator: the finite and infinite Fibonacci words, the morphism, the palindromic structure and the repetitions
  - book: isbn:9780521812207
    title: M. Lothaire, Algebraic Combinatorics on Words, Encyclopedia of Mathematics and its Applications 90, Cambridge University Press, 2002
    locator: Chapter 2, Sturmian words (J. Berstel and P. Séébold), the Fibonacci word as the standard example of a characteristic Sturmian word
  - paper: doi:10.1051/ita/1992260301991
    title: Filippo Mignosi and Giuseppe Pirillo, Repetitions in the Fibonacci infinite word, RAIRO Theoretical Informatics and Applications 26(3), 1992, 199-204
    locator: the Fibonacci word contains no fourth power and its critical exponent is 2 + φ
  - paper: doi:10.2307/2371431
    title: Marston Morse and Gustav A. Hedlund, Symbolic dynamics II. Sturmian trajectories, American Journal of Mathematics 62(1), 1940, 1-42
    locator: Sturmian sequences, their factor complexity n + 1 and their description by rotations of the circle
  - paper: doi:10.1137/0206024
    title: Donald E. Knuth, James H. Morris and Vaughan R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2), 1977, 323-350
    locator: the Fibonacci strings as the patterns that make the delay of the matcher about log_φ m
---

The Fibonacci word is the infinite word `abaababaabaababaababa`$\cdots$ obtained by iterating the morphism $\varphi : a \mapsto ab,\ b \mapsto a$ from $a$. Its prefixes $f_n = \varphi^n(a)$, the finite Fibonacci words, satisfy $f_n = f_{n-1} f_{n-2}$ and have [Fibonacci numbers](/fibonacci-numbers/) as lengths. It is the standard example of a [Sturmian word](/sturmian-word/): it has exactly $m + 1$ distinct factors of each length $m$, the least possible for a word that is not eventually periodic. Its finite prefixes are extreme cases for string algorithms: they have many runs and squares, and they make the delay of the [Knuth-Morris-Pratt](/knuth-morris-pratt/) matcher as large as possible.

## Definition

The alphabet is $\{a, b\}$, with $a < b$ where an order is needed. Indices are 0-based. Let $F_1 = F_2 = 1$ and $F_{j+2} = F_{j+1} + F_j$ be the Fibonacci numbers, and $\phi = (1 + \sqrt 5)/2$ the golden ratio.

**The morphism.** $\varphi$ is the [morphism](/morphic-word/) of $\{a, b\}^*$ with $\varphi(a) = ab$ and $\varphi(b) = a$, extended by $\varphi(uv) = \varphi(u)\varphi(v)$.

**Finite Fibonacci words.** $f_n = \varphi^n(a)$ for $n \ge 0$, so $f_0 = a$, $f_1 = ab$, $f_2 = aba$, $f_3 = abaab$, $f_4 = abaababa$. Equivalently, $f_0 = a$, $f_1 = ab$ and $f_n = f_{n-1} f_{n-2}$ for $n \ge 2$. *Proof of the equivalence.* By induction, $\varphi^{n}(a) = \varphi^{n-1}(ab) = \varphi^{n-1}(a)\,\varphi^{n-1}(b) = \varphi^{n-1}(a)\,\varphi^{n-2}(a)$, using $\varphi(b) = a$. $\square$

**The infinite Fibonacci word.** Each $f_n$ is a prefix of $f_{n+1}$, so the $f_n$ have a limit $\mathbf{f}$, the unique infinite word with every $f_n$ as a prefix. It is the fixed point of $\varphi$: $\varphi(\mathbf{f}) = \mathbf{f}$.

### Basic facts

1. **Lengths and letter counts.** $|f_n| = F_{n+2}$, and $f_n$ has $F_{n+1}$ letters $a$ and $F_n$ letters $b$, by induction from $f_n = f_{n-1} f_{n-2}$. So the frequency of $b$ in $\mathbf{f}$ is $\lim F_n / F_{n+2} = 1/\phi^2 \approx 0.382$, and that of $a$ is $1/\phi \approx 0.618$.
2. **Mechanical form.** With $\alpha = 1/\phi^2 = (3 - \sqrt 5)/2$, the letter $\mathbf{f}[i]$ is $b$ exactly when $\lfloor (i + 2)\alpha \rfloor - \lfloor (i + 1)\alpha \rfloor = 1$. So $\mathbf{f}$ is the characteristic Sturmian word of slope $\alpha$, and the positions of $b$ are $\lfloor (j + 1)\phi^2 \rfloor - 1$ for $j \ge 0$, that is, 1, 4, 6, 9, 12, $\ldots$
3. **Zeckendorf form.** $\mathbf{f}[i] = b$ exactly when the [Zeckendorf representation](/zeckendorf-theorem/) of $i$, as a sum of nonconsecutive Fibonacci numbers from $F_2 = 1, F_3 = 2, F_4 = 3, \ldots$, uses $F_2 = 1$.
4. **Factor complexity.** $\mathbf{f}$ has exactly $m + 1$ distinct factors of length $m$ for each $m \ge 0$, so its [subword complexity](/subword-complexity/) is $m + 1$; the factors of length 3 are `aab`, `aba`, `baa`, `bab`. A word with at most $m$ factors of some length $m$ is eventually periodic (Morse and Hedlund), so $m + 1$ is the least complexity of an aperiodic word.
5. **Balance.** Any two factors of the same length have numbers of $b$ that differ by at most 1. In particular `bb` and `aaa` do not occur.
6. **Palindromes.** For $n \ge 2$, $f_n$ with its last two letters removed is a palindrome: `a`, `aba`, `abaaba`, `abaababaaba`, $\ldots$ These are the central words of the Sturmian theory.
7. **Repetitions.** $\mathbf{f}$ contains squares, such as `aa` and `abaaba`, and cubes, such as $(aba)^3$ $=$ `abaabaaba` at index 5, but no fourth power. Its critical exponent, the supremum of the exponents of its factors, is $2 + \phi \approx 3.618$ (Mignosi and Pirillo).
8. **Runs.** The number of [maximal repetitions](/maximal-repetition/) in $f_n$ is $2|f_{n-2}| - 3$ for $n \ge 3$, so the ratio of runs to length tends to $2/\phi^2 \approx 0.764$.

## Examples and non-examples

| $n$ | $f_n$ | $|f_n|$ | runs |
|---|---|---|---|
| 0 | `a` | 1 | 0 |
| 1 | `ab` | 2 | 0 |
| 2 | `aba` | 3 | 0 |
| 3 | `abaab` | 5 | 1 |
| 4 | `abaababa` | 8 | 3 |
| 5 | `abaababaabaab` | 13 | 7 |
| 6 | `abaababaabaababaababa` | 21 | 13 |

The three runs of $f_4 = $ `abaababa` are `aa` at index 2 (period 1), `abaaba` at index 0 (period 3) and `ababa` at index 3 (period 2).

**Non-examples.**

- The [Thue-Morse word](/thue-morse-word/) `abbabaab`$\cdots$ is also the fixed point of a morphism, $a \mapsto ab$, $b \mapsto ba$, but it is not Sturmian: it contains `aa` and `bb`, and it has 6 factors of length 3.
- $(ab)^\infty$ has only 2 factors of each length $m \ge 1$; it is periodic, so it is not Sturmian.
- $(aba)^4$ $=$ `abaabaabaaba` is not a factor of $\mathbf{f}$, which has no fourth power, although $(aba)^3$ is.

## Related definitions

- **[Sturmian word](/sturmian-word/).** An infinite word with $m + 1$ factors of each length $m$, equivalently an aperiodic balanced binary word, or a mechanical word of irrational slope. The Fibonacci word is the one of slope $1/\phi^2$.
- **[Morphic word](/morphic-word/).** A word obtained by iterating a morphism, possibly followed by a letter-to-letter map; the Fibonacci word is a pure morphic word.
- **[Christoffel word](/christoffel-word/) and standard words.** The finite words $f_n$ are standard words, the finite approximations of characteristic Sturmian words; the lower Christoffel word with $F_{n+1}$ letters $a$ and $F_n$ letters $b$ is a conjugate of $f_n$, for example `aabab` of `abaab`.
- **[Fibonacci numbers](/fibonacci-numbers/) and [Zeckendorf's theorem](/zeckendorf-theorem/).** The lengths, and the numeration system that decides each letter.
- **[Maximal repetition](/maximal-repetition/).** The Fibonacci words are the classical family with many runs, and the starting point of the search for words with the most runs.

## References
