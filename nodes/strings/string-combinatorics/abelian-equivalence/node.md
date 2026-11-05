---
tag: XWYTQ2
kind: definition
slug: abelian-equivalence
name: Abelian equivalence
aliases:
- commutative equivalence
area: strings/string-combinatorics
level: intro
summary: Two words are Abelian equivalent if they have the same letter counts.
prereqs: [parikh-vector, equivalence-relation]
see_also: [abelian-square, abelian-complexity, keranen-theorem, multinomial-coefficient, stars-and-bars, sliding-window, word-conjugacy, permutation]
sources:
  - paper: doi:10.1145/321356.321364
    title: Rohit J. Parikh, On context-free languages, Journal of the ACM 13(4), 1966, 570-581
    locator: the commutative image of a word and of a language (the map to letter counts)
  - paper: "F. Michel Dekking, Strongly non-repetitive sequences and progression-free sets, Journal of Combinatorial Theory, Series A 27(2), 1979, 181-185"
    title: F. Michel Dekking, Strongly non-repetitive sequences and progression-free sets
    locator: the definition of Abelian powers, words u_1 ... u_k with the u_i permutations of each other
  - paper: "Juhani Karhumäki, Aleksi Saarela and Luca Q. Zamboni, On a generalization of Abelian equivalence and complexity of infinite words, Journal of Combinatorial Theory, Series A 120(8), 2013, 2189-2206"
    title: Juhani Karhumäki, Aleksi Saarela and Luca Q. Zamboni, On a generalization of Abelian equivalence and complexity of infinite words
    locator: the definition of k-Abelian equivalence and its relation to Abelian equivalence (k = 1)
---

Two words are Abelian equivalent when each letter occurs the same number of times in both, so one is a rearrangement (an anagram) of the other, as `listen` and `silent`. In other words, they have the same [Parikh vector](/parikh-vector/). Abelian equivalence replaces equality in the Abelian versions of the notions of combinatorics on words: an [Abelian square](/abelian-square/) is $uv$ with $u$ and $v$ Abelian equivalent, and the [Abelian complexity](/abelian-complexity/) counts the Abelian classes of the factors of each length.

## Definition

Let $\Sigma = \{a_1, \ldots, a_\sigma\}$ be a finite [alphabet](/alphabet/); no order is needed, but the letters are listed in a fixed order to form vectors. For $w \in \Sigma^*$ and a letter $a$, $|w|_a$ is the number of indices $i$ with $w[i] = a$, with 0-based indices. The Parikh vector of $w$ is
$$ \Psi(w) = (|w|_{a_1}, \ldots, |w|_{a_\sigma}) \in \mathbb{N}^\sigma. $$

**Abelian equivalence.** Words $u, v \in \Sigma^*$ are Abelian equivalent, written $u \sim_{ab} v$, if $\Psi(u) = \Psi(v)$, that is, $|u|_a = |v|_a$ for each $a \in \Sigma$.

**Equivalent forms.** For $u, v$ of the same length $n$, these are equivalent: (1) $u \sim_{ab} v$; (2) there is a [permutation](/permutation/) $\pi$ of $\{0, \ldots, n-1\}$ with $v[i] = u[\pi(i)]$ for each $i$; (3) the sorted words are equal, for any order on $\Sigma$. *Proof.* (1 ⇒ 2) For each letter $a$, the sets $\{i : u[i] = a\}$ and $\{i : v[i] = a\}$ have the same size; choose a bijection between them for each letter and join them into $\pi$. (2 ⇒ 3) A permutation of positions does not change the multiset of letters, and the sorted word depends only on that multiset. (3 ⇒ 1) The sorted word is $a_1^{|w|_{a_1}} \cdots a_\sigma^{|w|_{a_\sigma}}$, which gives back each count. $\square$ Words of different lengths are never equivalent, since $|w| = \sum_a |w|_a$.

### Basic facts

1. **An equivalence relation and a congruence.** $\sim_{ab}$ is reflexive, symmetric and transitive, since it is equality of an image. Since $\Psi(uv) = \Psi(u) + \Psi(v)$, if $u \sim_{ab} u'$ and $v \sim_{ab} v'$ then $uv \sim_{ab} u'v'$. The quotient $\Sigma^* / \sim_{ab}$ is the free commutative monoid, isomorphic to $(\mathbb{N}^\sigma, +)$ through $\Psi$.
2. **The number of classes.** The classes inside $\Sigma^n$ are the vectors $(k_1, \ldots, k_\sigma)$ of non-negative integers with sum $n$. By [stars and bars](/stars-and-bars/), there are $\binom{n + \sigma - 1}{\sigma - 1}$ of them.
3. **The size of a class.** The class of the vector $(k_1, \ldots, k_\sigma)$ has $\binom{n}{k_1, \ldots, k_\sigma} = n!/(k_1! \cdots k_\sigma!)$ words, a [multinomial coefficient](/multinomial-coefficient/): choose the positions of each letter.
4. **Conjugates are equivalent.** Each rotation of $w$ is a permutation of its letters, so [conjugate words](/word-conjugacy/) are Abelian equivalent. The converse fails, see below.
5. **Factors by a sliding window.** For $w$ of length $n$ and a fixed length $m$, the Parikh vectors of the factors $w[i..i+m-1]$ for $i = 0, \ldots, n - m$ are found in $O(n + \sigma)$ time on an integer alphabet: $\Psi(w[i+1..i+m]) = \Psi(w[i..i+m-1]) - e_{w[i]} + e_{w[i+m]}$, where $e_a$ is the unit vector of $a$. With a counter of the letters whose count differs from a target vector, this finds all factors that are Abelian equivalent to a pattern of length $m$ in $O(n + m + \sigma)$ time, the [sliding window](/sliding-window/) method of anagram search.

## Examples and non-examples

**Equivalent pairs.**

- `listen` $\sim_{ab}$ `silent`: both have one each of `e`, `i`, `l`, `n`, `s`, `t`.
- Over $\{a, b, c\}$, `aabc` $\sim_{ab}$ `abca` $\sim_{ab}$ `caba`, all with $\Psi = (2, 1, 1)$. This class has $4!/(2!\,1!\,1!) = 12$ words.
- `aabb` $\sim_{ab}$ `abab`, with $\Psi = (2, 2)$. They are not conjugate: the rotations of `aabb` are `aabb`, `abba`, `bbaa`, `baab`, and `abab` is not among them.
- $\varepsilon \sim_{ab} \varepsilon$, the only word with the zero vector.

**Non-equivalent pairs.**

- `aab` and `abb`: $\Psi = (2, 1)$ and $(1, 2)$.
- `ab` and `aab`: different lengths.
- `Listen` and `silent` as written: the letters `L` and `l` differ. A program must say whether it folds case before counting.

**Counts.** In $\{a, b\}^4$ there are $\binom{5}{1} = 5$ classes, with sizes 1, 4, 6, 4, 1. In $\{a, b, c\}^4$ there are $\binom{6}{2} = 15$ classes, and in $\{a, b, c\}^6$ there are $\binom{8}{2} = 28$.

## Related definitions

- **[Parikh vector](/parikh-vector/).** The vector of letter counts; Abelian equivalence is equality of Parikh vectors.
- **[Abelian square](/abelian-square/).** A word $uv$ with $u \sim_{ab} v$ and $u \ne \varepsilon$. Abelian squares are unavoidable on three letters and avoidable on four, by [Keränen's theorem](/keranen-theorem/).
- **[Abelian complexity](/abelian-complexity/).** The number of Abelian classes among the factors of length $n$ of a word.
- **$k$-Abelian equivalence.** Karhumäki, Saarela and Zamboni require equal numbers of occurrences of each factor of length at most $k$. For $k = 1$ it is Abelian equivalence; as $k$ grows it gets closer to equality.
- **[Conjugacy](/word-conjugacy/).** Equality up to rotation, a finer relation than Abelian equivalence (fact 4).

## References
