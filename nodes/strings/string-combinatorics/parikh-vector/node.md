---
tag: FWJFMJ
kind: definition
slug: parikh-vector
name: Parikh vector
aliases:
- letter-count vector
- letter-frequency vector
area: strings/string-combinatorics
level: intro
summary: The vector of the number of occurrences of each letter in a word.
prereqs: [alphabet, monoid]
see_also: [abelian-equivalence, abelian-square, abelian-complexity, parikh-theorem, word-conjugacy, context-free-language, histogram, necklace]
sources:
  - paper: doi:10.1145/321356.321364
    title: Rohit J. Parikh, On context-free languages, Journal of the ACM 13(4), 1966, 570-581
    locator: the commutative image of a language and the theorem that the image of a context-free language is semilinear
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Supplementary Lecture H, Parikh's theorem (the map from words to letter-count vectors and semilinear sets)
---

The Parikh vector of a word lists how many times each letter of the alphabet occurs in it, forgetting the order: over the alphabet `a`, `b`, `c`, `d`, `r`, the word `abracadabra` has the Parikh vector $(5, 2, 1, 1, 2)$. The map from words to Parikh vectors turns concatenation into addition of vectors. Two words with the same vector are *abelian equivalent*, or anagrams, and the image of a whole language under the map is the subject of Parikh's theorem on context-free languages.

## Definition

Let $\Sigma = \{a_1, \ldots, a_k\}$ be a finite [alphabet](/alphabet/), listed in a fixed order; the order only fixes the coordinates, and only equality of letters is used. Indices are 0-based. For a word $w$ and a letter $a$, $|w|_a$ is the number of indices $i$ with $w[i] = a$.

**Parikh vector.** The *Parikh vector* (or Parikh image) of $w \in \Sigma^*$ is
$$ \Psi(w) = \big( |w|_{a_1}, |w|_{a_2}, \ldots, |w|_{a_k} \big) \in \mathbb{N}^k. $$
Its coordinates sum to $|w|$.

**A morphism of monoids.** $\Psi(uv) = \Psi(u) + \Psi(v)$ and $\Psi(\varepsilon) = 0$, so $\Psi$ is a morphism from the free [monoid](/monoid/) $\Sigma^*$ onto the additive monoid $\mathbb{N}^k$. It is onto because $\Psi(a_1^{n_1} \cdots a_k^{n_k}) = (n_1, \ldots, n_k)$. For a language $L$, $\Psi(L) = \{\Psi(w) : w \in L\}$.

**Abelian equivalence.** Words $u$ and $v$ are *abelian equivalent* if $\Psi(u) = \Psi(v)$, that is, if one is a permutation of the letters of the other. See [abelian equivalence](/abelian-equivalence/).

**Counts.** The number of distinct Parikh vectors of words of length $n$ is $\binom{n + k - 1}{k - 1}$, the number of ways to write $n$ as an ordered sum of $k$ nonnegative parts. The number of words with Parikh vector $(n_1, \ldots, n_k)$ is the multinomial coefficient $\frac{n!}{n_1! \cdots n_k!}$, because such a word is an arrangement of $n_1$ copies of $a_1$, $n_2$ copies of $a_2$, and so on.

**Factors of a fixed length.** For a word $s$, a letter $a$ and $1 \le m \le |s|$, the set $\{ |s[i..i+m-1]|_a : 0 \le i \le |s| - m \}$ is an interval of integers. *Proof.* Sliding the window from $i$ to $i + 1$ removes $s[i]$ and adds $s[i+m]$, so the count changes by $-1$, $0$ or $+1$. A sequence of integers whose steps are at most 1 in absolute value takes every value between its minimum and its maximum. $\square$ On a binary alphabet the count of `a` determines the whole vector, so the Parikh vectors of the factors of length $m$ form an interval in this sense. This fact underlies the indexes for jumbled pattern matching on binary strings, which ask whether some factor has a given Parikh vector.

## Examples and non-examples

- **A worked word.** Over $a < b < c < d < r$, $\Psi($`abracadabra`$) = (5, 2, 1, 1, 2)$. The sum is $11$, the length.
- **All binary words of length 3.** The vectors are $(3, 0)$ for `aaa`, $(2, 1)$ for `aab`, `aba`, `baa`, $(1, 2)$ for `abb`, `bab`, `bba`, and $(0, 3)$ for `bbb`: four vectors, $\binom{4}{1} = 4$, with $1, 3, 3, 1$ words each.
- **Abelian equivalent, not conjugate.** `aabb` and `abab` both have vector $(2, 2)$, but they are not rotations of each other. [Conjugate](/word-conjugacy/) words always have the same Parikh vector, so each [necklace](/necklace/) has one vector, but a vector can hold several necklaces.
- **Factor counts.** In `abaababaab`, the factors of length 3 contain 1 or 2 letters `a`, and the factors of length 5 all contain exactly 3.
- **Non-example: the map is not injective.** $\Psi($`ab`$) = \Psi($`ba`$)$, so the order of letters cannot be recovered. It is injective only on a one-letter alphabet, where $\Psi(w) = (|w|)$.
- **Languages.** The language $\{a^n b^n : n \ge 0\}$ is not regular, but its image $\{(n, n)\}$ equals $\Psi((ab)^*)$, the image of a regular language. Parikh's theorem says this always happens for context-free languages.

## Related definitions

- **Abelian equivalence and abelian powers.** [Abelian equivalence](/abelian-equivalence/) compares Parikh vectors; an [abelian square](/abelian-square/) is a word $uv$ with $\Psi(u) = \Psi(v)$, such as `abba`.
- **Abelian complexity.** The number of distinct Parikh vectors among the factors of length $m$ of an infinite word is its [abelian complexity](/abelian-complexity/); the interval fact above shows it is at most $m + 1$ on two letters, and Sturmian words have abelian complexity 2.
- **Parikh's theorem.** The image of a [context-free language](/context-free-language/) is a semilinear set, a finite union of sets $\{v_0 + n_1 v_1 + \cdots + n_r v_r : n_i \in \mathbb{N}\}$, and equals the image of some [regular language](/regular-language/). See [Parikh's theorem](/parikh-theorem/).
- **Histogram.** A Parikh vector is the [histogram](/histogram/) of the letters of the word.
- **Parikh matrix.** An extension that also counts scattered subwords such as `ab`, and so keeps some order information.

## References
