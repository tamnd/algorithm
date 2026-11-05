---
tag: 2CCGRH
kind: concept
slug: subword-complexity
name: Subword complexity
aliases:
- factor complexity
- complexity function of a word
area: strings/string-combinatorics
level: core
summary: The function p(n) counting distinct factors of length n in a word.
prereqs: [alphabet]
see_also: [morse-hedlund-theorem, sturmian-word, abelian-complexity, count-distinct-substrings, thue-morse-word, morphic-word, lempel-ziv-complexity, de-bruijn-sequence]
sources:
  - book: isbn:9780521515979
    title: Valérie Berthé and Michel Rigo (editors), Combinatorics, Automata and Number Theory, Encyclopedia of Mathematics and its Applications 135, Cambridge University Press, 2010
    locator: Chapter 4, Factor complexity (J. Cassaigne and F. Nicolas), special factors, the Morse-Hedlund theorem, and the complexity of morphic words
  - book: isbn:9780521823326
    title: Jean-Paul Allouche and Jeffrey Shallit, Automatic Sequences, Cambridge University Press, 2003
    locator: Chapter 10, Subword complexity (basic properties, Sturmian words and the complexity of automatic sequences)
  - paper: doi:10.2307/2371264
    title: Marston Morse and Gustav A. Hedlund, Symbolic dynamics, American Journal of Mathematics 60(4), 1938, 815-866
    locator: the theorem that a sequence with at most n blocks of some length n is ultimately periodic
  - paper: "Jean-Jacques Pansiot, Complexité des facteurs des mots infinis engendrés par morphismes itérés, in Automata, Languages and Programming (ICALP 1984), Lecture Notes in Computer Science 172, Springer, 1984, 380-389"
    locator: the classification of the complexity of pure morphic words into five growth classes
---

The subword complexity of a word $w$ is the function $p_w(n)$ that counts the distinct factors (contiguous blocks) of length $n$ in $w$. It measures how varied a word is: periodic infinite words have bounded complexity, the [Sturmian words](/sturmian-word/) have the least complexity $n + 1$ among the others, the [Thue-Morse word](/thue-morse-word/) has linear complexity, and a random binary word has $p(n) = 2^n$. The [Morse-Hedlund theorem](/morse-hedlund-theorem/) turns this into a sharp dividing line: an infinite word is ultimately periodic if and only if $p(n) \le n$ for some $n$.

## In plain words

Slide a window of fixed width along a word and write down every different stretch of letters you see through it. The number of different stretches, for each window width, is the complexity of the word. A word that just repeats one short block shows only a few stretches however wide the window gets. A word made by flipping coins shows every possible stretch once it is long enough. Words in between, built by careful rules, show a number of stretches that grows slowly with the window width, and how fast it grows tells a lot about how the word was built.

## The idea

Let $\Sigma$ be a finite [alphabet](/alphabet/) with $k$ letters; only equality of letters is used. Words are indexed from 0, and $w[i..j]$ includes both ends.

**Definition.** For a finite or infinite word $w$ and $n \ge 0$,
$$ p_w(n) = \big| \{ w[i..i+n-1] : i \ge 0,\ i + n \le |w| \} \big|, $$
the number of distinct factors of length $n$. So $p_w(0) = 1$ (the empty word), and $p_w(1)$ is the number of letters that occur.

**Simple bounds.** $p_w(n) \le k^n$. For a finite word of length $N$, also $p_w(n) \le N - n + 1$, since there are only that many windows. For every word, $p_w(m + n) \le p_w(m)\, p_w(n)$, because a factor of length $m + n$ is determined by its prefix of length $m$ and its suffix of length $n$. So $\log p_w$ is subadditive, and the *entropy* $\lim_{n \to \infty} \frac{1}{n} \log_k p_w(n)$ exists for infinite $w$.

**Special factors and the growth.** Let $w$ be infinite. Each factor $u$ of length $n$ has at least one right extension $ua$ that is a factor, and every factor of length $n + 1$ arises this way exactly once. So
$$ p_w(n+1) - p_w(n) = \sum_{u} \big( r(u) - 1 \big), $$
where the sum is over the factors $u$ of length $n$ and $r(u)$ is the number of letters $a$ with $ua$ a factor. A factor with $r(u) \ge 2$ is *right special*. In particular $p_w$ is nondecreasing for infinite words, and on two letters $p_w(n+1) - p_w(n)$ is the number of right special factors of length $n$.

**The dividing line.** If $p_w(n) = p_w(n+1)$ for some $n$, then no factor of length $n$ is right special, each factor has a unique continuation, and the word is ultimately periodic. Hence for an aperiodic infinite word $p_w(n+1) \ge p_w(n) + 1$, so $p_w(n) \ge n + 1$ for all $n$. This is the [Morse-Hedlund theorem](/morse-hedlund-theorem/), and the words with exactly $p_w(n) = n + 1$ are the [Sturmian words](/sturmian-word/).

**Growth classes for morphic words.** Pansiot (1984) showed that for the fixed point of a [morphism](/string-morphism/) (a pure [morphic word](/morphic-word/)) the complexity is, up to constants, one of $1$, $n$, $n \log \log n$, $n \log n$ and $n^2$. Fixed points of uniform morphisms, and more generally automatic sequences, have complexity $O(n)$.

## Examples

| word | $p(1), p(2), \ldots$ | growth |
| --- | --- | --- |
| periodic $(abc)^\infty$ | 3, 3, 3, 3, ... | bounded |
| Fibonacci word $0100101001001\cdots$ | 2, 3, 4, 5, 6, 7, 8, ... | $n + 1$ |
| Thue-Morse word $0110100110010110\cdots$ | 2, 4, 6, 10, 12, 16, 20, 22, 24, 28, 32, 36, ... | linear |
| $0\,1\,00\,1\,000\,1\,0000\,1 \cdots$ | 2, 3, 4, 6, 9, 12, 16, 20, 25, 30, 36, ... | quadratic |
| binary Champernowne word $1\,10\,11\,100\,101 \cdots$ | 2, 4, 8, 16, 32, 64, 128, ... | $2^n$ |

- **Thue-Morse differences.** The differences $p(n+1) - p(n)$ for $n = 0, \ldots, 11$ are $1, 2, 2, 4, 2, 4, 4, 2, 2, 4, 4, 4$, and on this binary word each equals the number of right special factors of length $n$; for example, of the four factors of length 2, the factors `01` and `10` are right special (`010`, `011`, `100`, `101` all occur) while `00` and `11` are not.
- **A finite word.** For $w = $ `abaababaab` the values $p(0), \ldots, p(10)$ are $1, 2, 3, 4, 5, 5, 5, 4, 3, 2, 1$: they rise while the alphabet allows and then fall as the number of windows $N - n + 1$ drops. The word has $35$ distinct factors in all, the empty one included; computing this total is the problem of [counting distinct substrings](/count-distinct-substrings/).
- **De Bruijn words.** A cyclic [de Bruijn sequence](/de-bruijn-sequence/) of order $n$ contains each of the $k^n$ words of length $n$ exactly once, so it attains the maximum $p(n) = k^n$ with the fewest windows.

## Where it is used

- **Characterizing periodicity.** The [Morse-Hedlund theorem](/morse-hedlund-theorem/) characterizes ultimately periodic words, and the minimal aperiodic words are the [Sturmian words](/sturmian-word/), see the [Sturmian characterization](/sturmian-characterization/).
- **Classifying sequences.** Complexity separates automatic, morphic and random sequences; for example a sequence of complexity larger than linear is not automatic, and the factor complexity of a number's expansion in base $b$ is used to study whether the number is normal or transcendental.
- **Symbolic dynamics.** The entropy $\lim \frac{1}{n} \log p(n)$ is the topological entropy of the shift generated by the word.
- **Algorithms on finite strings.** For a finite string, $p(n)$ for all $n$ is read from a [suffix array](/suffix-array/) with its [LCP array](/lcp-array/) in linear time: the number of distinct factors of length $n$ is the number of suffixes of length at least $n$ whose longest common prefix with the previous suffix in sorted order is less than $n$.
- **Related complexities.** [Abelian complexity](/abelian-complexity/) counts [Parikh vectors](/parikh-vector/) of factors instead of factors; palindromic complexity counts palindromic factors; [Lempel-Ziv complexity](/lempel-ziv-complexity/) counts phrases of a parse.

## References
