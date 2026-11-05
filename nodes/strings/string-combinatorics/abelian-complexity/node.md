---
tag: RZMSVM
kind: concept
slug: abelian-complexity
name: Abelian complexity
aliases:
- Parikh complexity
area: strings/string-combinatorics
level: advanced
summary: The number of distinct Parikh vectors of factors of length n.
prereqs: [parikh-vector, abelian-equivalence]
see_also: [subword-complexity, sturmian-word, thue-morse-word, fibonacci-word, abelian-square, christoffel-word, sliding-window, morphic-word]
sources:
  - paper: doi:10.1112/jlms/jdq063
    title: Gwénaël Richomme, Kalle Saari and Luca Q. Zamboni, Abelian complexity of minimal subshifts, Journal of the London Mathematical Society 83(1), 2011, 79-95
    locator: the definition of Abelian complexity, bounded Abelian complexity and C-balance, the Thue-Morse word, and Abelian powers in words of bounded Abelian complexity
  - paper: doi:10.1007/bf01762232
    title: Ethan M. Coven and Gustav A. Hedlund, Sequences with minimal block growth, Mathematical Systems Theory 7(2), 1973, 138-153
    locator: aperiodic binary words in which all factors of each length have one of two Parikh vectors are the Sturmian words
  - paper: doi:10.1016/j.aam.2010.01.006
    title: Gwénaël Richomme, Kalle Saari and Luca Q. Zamboni, Balance and Abelian complexity of the Tribonacci word, Advances in Applied Mathematics 45(2), 2010, 212-231
    locator: the Tribonacci word is 2-balanced and its Abelian complexity takes values in 3 to 7
  - book: isbn:9780521812207
    title: M. Lothaire, Algebraic Combinatorics on Words, Cambridge University Press, 2002
    locator: Chapter 2, Sturmian words (J. Berstel and P. Séébold), balanced words and the equivalence between balanced aperiodic words and Sturmian words
---

The Abelian complexity of a word counts its factors of each length up to rearrangement: $\rho^{ab}_w(n)$ is the number of distinct [Parikh vectors](/parikh-vector/) of the factors of length $n$ of $w$. It is the Abelian analogue of the [factor complexity](/subword-complexity/) $p_w(n)$, which counts the distinct factors themselves, and it is never larger. It measures how evenly the letters are spread: [Sturmian words](/sturmian-word/) have Abelian complexity 2 at every length, and the [Thue-Morse word](/thue-morse-word/) alternates between 2 and 3, although both have unbounded factor complexity.

## In plain words

Slide a window of fixed width along a word and, at each place, write down how many of each letter you see, ignoring their order. Count how many different tallies you get. That number, for each window width, is the Abelian complexity. A word whose letters are spread very evenly gives almost the same tally everywhere, so the count stays small. A word with long clusters of one letter gives many different tallies. The count is never more than the number of different windows, because two equal windows give equal tallies.

## The idea

**Definition.** Let $\Sigma = \{a_1, \ldots, a_\sigma\}$ be a finite [alphabet](/alphabet/); only equality of letters is used. Indices are 0-based. For a finite or infinite word $w$ and $n \ge 1$, let $F_n(w)$ be the set of factors of length $n$ of $w$, and $\Psi(u) = (|u|_{a_1}, \ldots, |u|_{a_\sigma})$. Then
$$ \rho^{ab}_w(n) = |\{\Psi(u) : u \in F_n(w)\}|, \qquad p_w(n) = |F_n(w)|. $$
Two factors have the same Parikh vector exactly when they are [Abelian equivalent](/abelian-equivalence/), so $\rho^{ab}_w(n)$ is the number of Abelian classes in $F_n(w)$.

**Basic bounds.** $1 \le \rho^{ab}_w(n) \le \min\left(p_w(n), \binom{n + \sigma - 1}{\sigma - 1}\right)$, when $w$ has a factor of length $n$. The first upper bound holds because $\Psi$ is a map from $F_n(w)$; the second counts all vectors of $\mathbb{N}^\sigma$ with sum $n$, by [stars and bars](/stars-and-bars/).

**Value 1 means a period.** $\rho^{ab}_w(n) = 1$ if and only if $n$ is a period of $w$, that is, $w[i] = w[i + n]$ wherever both exist. *Proof.* Moving the window from index $i$ to $i + 1$ removes $w[i]$ and adds $w[i + n]$, so the vector stays the same if and only if $w[i] = w[i + n]$. All windows have one vector if and only if every move keeps it. $\square$ So an infinite word that is not ultimately periodic has $\rho^{ab}_w(n) \ge 2$ for all $n$.

**Two letters: an interval.** Over $\{a, b\}$, the vector of a factor of length $n$ is fixed by its number of $b$s. Moving the window by one changes this number by at most 1, so the numbers that occur form an interval, and
$$ \rho^{ab}_w(n) = \max_i |w[i..i+n-1]|_b - \min_i |w[i..i+n-1]|_b + 1. $$
A word is $C$-balanced if any two factors of the same length differ by at most $C$ in the number of each letter. So a binary word is $C$-balanced if and only if $\rho^{ab}_w(n) \le C + 1$ for all $n$. Richomme, Saari and Zamboni proved that, over any finite alphabet, an infinite word has bounded Abelian complexity if and only if it is $C$-balanced for some $C$, and that such a word contains Abelian $k$-th powers for every $k$.

**Sturmian words.** Balanced means 1-balanced. An infinite binary word is Sturmian if and only if it is balanced and not ultimately periodic (Lothaire, Chapter 2). With the two facts above, a binary word that is not ultimately periodic has $\rho^{ab}_w(n) = 2$ for every $n \ge 1$ if and only if it is Sturmian, a result of Coven and Hedlund. Sturmian words have the least factor complexity, $p_w(n) = n + 1$, among aperiodic words, and the least Abelian complexity as well.

**The Thue-Morse word.** Let $t = t_0 t_1 \cdots$ be the Thue-Morse word, the fixed point of $a \mapsto ab$, $b \mapsto ba$. It is a sequence of blocks $t[2j..2j+1] \in \{ab, ba\}$, where $t[2j] = t_j$ and $t[2j+1]$ is the other letter. Then $\rho^{ab}_t(n) = 2$ for odd $n$ and $3$ for even $n \ge 2$.

- *Odd $n = 2r + 1$.* A factor is $r$ full blocks and one letter, either after them (start at an even index) or before them (start at an odd index), so it has $r$ or $r + 1$ letters $a$. Both occur, since $t$ is not periodic.
- *Even $n = 2r$.* A factor that starts at an even index is $r$ blocks and has $r$ letters $a$. A factor that starts at the odd index $2j + 1$ is the second letter of block $j$, then $r - 1$ blocks, then the first letter $t_{j+r}$ of block $j + r$; it has $r - 1 + [t_j = b] + [t_{j+r} = a]$ letters $a$, so at most three values. All three occur: $t$ has no period $r$, so some $j$ has $t_j \ne t_{j+r}$, and the factors of $t$ are closed under exchanging $a$ and $b$, because $t[2^k..2^{k+1}-1]$ is the prefix of length $2^k$ with the letters exchanged. So both $t_j = a, t_{j+r} = b$ and $t_j = b, t_{j+r} = a$ occur. $\square$

**Computing it for a finite word.** For a word of length $N$ and one length $n$, slide a window and update the vector in $O(1)$ time per step, as in a [sliding window](/sliding-window/); with a hash of the vector that is also updated in $O(1)$ time, the number of distinct vectors is found in $O(N)$ expected time. All lengths together take $O(N^2)$ expected time. Over two letters, the interval formula gives each value from a running minimum and maximum, with no hashing.

## Examples

| word | $\rho^{ab}(1), \rho^{ab}(2), \ldots$ | reason |
|---|---|---|
| `abaab` | 2, 2, 1, 2, 1 | the length 3 is a period; 5 is the whole word |
| `abcacb` | 3, 3, 2, 2, 2, 1 | for $n = 3$: `abc`, `bca`, `acb` have one vector, `cac` another |
| $(aab)^\omega$ | 2, 2, 1, 2, 2, 1, ... | periodic with period 3 |
| Fibonacci word `abaababaabaab`... | 2, 2, 2, ... | Sturmian |
| Thue-Morse word `abbabaabbaab`... | 2, 3, 2, 3, ... | the proof above |
| Tribonacci word `abacabaabacab`... | 3, 3, 4, 3, 4, 4, 4, 3, 4, ... | 2-balanced; values in 3 to 7 |

- For `abaab` and $n = 2$, the factors `ab`, `ba`, `aa`, `ab` give the vectors $(1, 1)$ and $(2, 0)$, so $\rho^{ab}(2) = 2$, while $p(2) = 3$.
- The [Fibonacci word](/fibonacci-word/) has $p(n) = n + 1$ but $\rho^{ab}(n) = 2$: the factors of length 4 are `abaa`, `baab`, `aaba`, `abab`, `baba`, with one or two letters `b`.
- The Thue-Morse word has $p(n)$ growing linearly in $n$, yet a bounded Abelian complexity.
- The Tribonacci word, the fixed point of $a \mapsto ab$, $b \mapsto ac$, $c \mapsto a$, has $p(n) = 2n + 1$, and Richomme, Saari and Zamboni proved that its Abelian complexity takes only values in $\{3, 4, 5, 6, 7\}$. The values 3 to 6 already occur for $n < 400$.
- A word with unbounded Abelian complexity: $a b a^2 b^2 a^3 b^3 \cdots$, where the windows inside long blocks give every count of $b$ from 0 to $n$, so $\rho^{ab}(n) = n + 1$, the largest value on two letters.

## Where it is used

- **Characterizing Sturmian and balanced words.** Abelian complexity 2 at every length is the Abelian form of the Sturmian property, and bounded Abelian complexity is the same as finite imbalance. Balanced words describe evenly spread schedules, such as [Christoffel words](/christoffel-word/) and the cutting sequences of lines.
- **Abelian repetitions.** Bounded Abelian complexity forces Abelian powers of every order, so a word that avoids [Abelian squares](/abelian-square/), or Abelian $k$-th powers, must have unbounded Abelian complexity.
- **Morphic words.** For fixed points of morphisms, such as the Thue-Morse, Fibonacci and Tribonacci words, the Abelian complexity is studied together with the [factor complexity](/subword-complexity/) to classify [morphic words](/morphic-word/).
- **Jumbled pattern matching.** Searching for a factor with a given Parikh vector asks whether that vector is among those counted by $\rho^{ab}_w(n)$; over two letters the interval property reduces this to a minimum and a maximum per length.

## References
