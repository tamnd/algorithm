---
tag: 6M5F40
kind: definition
slug: alphabet
name: Alphabet
area: strings/string-combinatorics
level: intro
summary: Finite set of characters used by strings, with a mapping between characters and indices that supports radix-based algorithms.
see_also: [lexicographic-order, parikh-vector, word-ram, radix-sort, counting-sort, border, lyndon-word, string-matching]
sources:
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 1, Words (D. Perrin), Section 1.1 (free monoids, words, length, the empty word)
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 1, Tools (words, alphabets, the lexicographic order and the assumptions on the alphabet)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 32, String Matching (the introduction, notation for the alphabet, strings and the empty string)
  - paper: "Martin Farach, Optimal suffix tree construction with large alphabets, Proceedings of the 38th IEEE Symposium on Foundations of Computer Science (FOCS), 1997, 137-143"
    title: Martin Farach, Optimal suffix tree construction with large alphabets
    locator: the introduction (the integer alphabet, in which the letters are integers in a range polynomial in n)
---

An alphabet is a finite nonempty set $\Sigma$ whose elements are called letters, symbols or characters, and a word (or string) is a finite sequence of letters. All objects of combinatorics on words, such as a [border](/border/), a [Lyndon word](/lyndon-word/) or a [Parikh vector](/parikh-vector/), are defined over an alphabet. For algorithms, the alphabet comes with a model that says what a program may do with one letter: test equality, compare in an order, or use the letter as an array index. The choice of model changes the best possible running time of many string algorithms.

## Definition

**Alphabet.** An alphabet is a finite nonempty set $\Sigma$. Its size is $\sigma = |\Sigma|$. An alphabet of size 2 is binary, of size 3 ternary.

**Words.** For $n \ge 0$, a word of length $n$ over $\Sigma$ is a sequence $w = w[0]\,w[1] \cdots w[n-1]$ with each $w[i] \in \Sigma$. Its length is $|w| = n$. The unique word of length 0 is the empty word $\varepsilon$. We write $\Sigma^n$ for the set of words of length $n$, $\Sigma^* = \bigcup_{n \ge 0} \Sigma^n$ for the set of all words and $\Sigma^+ = \Sigma^* \setminus \{\varepsilon\}$ for the nonempty ones. Since $|\Sigma^n| = \sigma^n$, the set $\Sigma^*$ is countably infinite.

**Indices.** Indices are 0-based on this page and on all pages of the string combinatorics area. The factor $w[i..j]$ is $w[i]\,w[i+1] \cdots w[j]$, both ends included, and it is $\varepsilon$ when $j < i$. Some books, for example Lothaire, number the letters from 1; the formulas then shift by one.

**Concatenation.** The product of $u \in \Sigma^m$ and $v \in \Sigma^n$ is the word $uv \in \Sigma^{m+n}$ with $(uv)[i] = u[i]$ for $i < m$ and $(uv)[i] = v[i-m]$ for $i \ge m$. The product is associative, $\varepsilon$ is its neutral element, and $|uv| = |u| + |v|$. So $\Sigma^*$ is a monoid, the free monoid on $\Sigma$. Powers are $u^0 = \varepsilon$ and $u^{k+1} = u^k u$.

**Factors.** If $w = xuy$ for words $x, u, y$, then $u$ is a factor (substring) of $w$, a prefix when $x = \varepsilon$ and a suffix when $y = \varepsilon$. It is proper when $u \ne w$. For a letter $a$, $|w|_a$ is the number of indices $i$ with $w[i] = a$.

**Ordered alphabet.** An ordered alphabet is an alphabet with a total order $<$ on $\Sigma$. The order extends to words by the [lexicographic order](/lexicographic-order/): $u < v$ if $u$ is a proper prefix of $v$, or if $u = xay$ and $v = xbz$ for letters $a < b$. This is the order of a dictionary, and it is the order that defines [Lyndon words](/lyndon-word/), [minimal rotations](/minimal-rotation/) and suffix arrays.

**Alphabet models.** An algorithm on words assumes one of these models of the letters.

| model | what a program may do with letters | typical use |
|---|---|---|
| general alphabet | test $a = b$ only | [KMP](/knuth-morris-pratt/), [Z-algorithm](/z-algorithm/), [Main-Lorentz](/main-lorentz-algorithm/) |
| general ordered alphabet | compare $a < b$ | [Duval's algorithm](/duval-algorithm/), [Booth's algorithm](/booth-algorithm/) |
| integer alphabet | letters are integers in $\{0, \ldots, n^c\}$ for a constant $c$, usable as indices on a [word RAM](/word-ram/) | suffix arrays and suffix trees in $O(n)$ time |
| constant alphabet | $\sigma = O(1)$ | tables of size $\sigma$ per state, as in automata |

**Index map.** For an integer alphabet, or after a reduction, each letter $a$ has an index $\mathrm{ord}(a) \in \{0, \ldots, \sigma - 1\}$, a bijection between $\Sigma$ and $\{0, \ldots, \sigma - 1\}$ that respects the order. With it, a program can keep a table indexed by letters, and it can sort letters by [counting sort](/counting-sort/) and words by [radix sort](/radix-sort/).

**Alphabet reduction.** Each word $w$ of length $n$ over an ordered alphabet uses at most $n$ distinct letters. Replace each letter by its rank among the distinct letters of $w$. This gives a word over $\{0, \ldots, \sigma_w - 1\}$ with $\sigma_w \le n$ and the same equalities and the same order between any two factors. It takes $O(n \log n)$ comparisons by sorting, or $O(n)$ time by radix sort when the input is already an integer alphabet. After the reduction, an ordered alphabet behaves as an integer alphabet, which is why many linear-time results are stated for integer alphabets.

## Examples and non-examples

**Examples.**

- The binary alphabet $\{a, b\}$ or $\{0, 1\}$. The number of binary words of length $n = 0, 1, \ldots, 5$ is $1, 2, 4, 8, 16, 32$. Over three letters it is $1, 3, 9, 27, 81, 243$.
- The DNA alphabet $\{A, C, G, T\}$, with $\sigma = 4$. There are $4^{10} = 1{,}048{,}576$ words of length 10 and $(4^{11} - 1)/3 = 1{,}398{,}101$ words of length at most 10.
- Bytes, $\{0, \ldots, 255\}$, an integer alphabet of size 256 used by most file formats. ASCII has 128 letters.
- Unicode code points, $\{0, \ldots, \mathtt{0x10FFFF}\}$, an alphabet of $1{,}114{,}112$ letters, of which $2048$ (the surrogates $\mathtt{0xD800}$ to $\mathtt{0xDFFF}$) are not characters.
- The reduction of `banana` over the order $a < b < n$ is $1\,0\,2\,0\,2\,0$, a word over $\{0, 1, 2\}$.

**Non-examples and traps.**

- The empty set is not an alphabet: $\Sigma^*$ would hold only $\varepsilon$, and statements such as "$\sigma^n$ words of length $n$" or "the minimal letter" would need exceptions.
- $\mathbb{N}$ is not an alphabet in the sense of this page, because it is infinite. Some authors allow infinite alphabets. A single word still uses only finitely many letters, so the reduction above makes any word finite-alphabet.
- A string type of a programming language is not always a word over code points. A Java or JavaScript string is a word over 16-bit code units (UTF-16). The emoji U+1F600 is one code point but the two code units $\mathtt{D83D}\ \mathtt{DE00}$, so its length is 2. Comparison by code units is not code point order: U+FF5E is smaller than U+1F600 as code points, but larger in UTF-16, because $\mathtt{FF5E} > \mathtt{D83D}$. UTF-8 bytes keep code point order.
- Letters are not always comparable in a meaningful way. For DNA, the order $A < C < G < T$ is a convention, and a result that depends on the order, such as the [Lyndon factorization](/lyndon-factorization/), changes when the convention changes.

## Related definitions

- **[Lexicographic order](/lexicographic-order/).** The extension of the order of $\Sigma$ to $\Sigma^*$. Another common order is the radix (shortlex) order: shorter words first, then lexicographic.
- **[Parikh vector](/parikh-vector/).** The vector $(|w|_a)_{a \in \Sigma}$ of letter counts. Two words with the same vector are [Abelian equivalent](/abelian-equivalence/).
- **[Border](/border/) and [period](/string-period/).** The first notions of the structure of one word, defined with equality of letters only.
- **[Lyndon word](/lyndon-word/) and [necklace](/necklace/).** Notions that need an ordered alphabet and that count words up to rotation.
- **[String morphism](/string-morphism/).** A map $h : \Sigma^* \to \Delta^*$ with $h(uv) = h(u)h(v)$. It is fixed by the images of the letters, because $\Sigma^*$ is free.
- **[Word RAM](/word-ram/).** The machine model in which an integer alphabet allows letters to be used as indices in $O(1)$ time.

## References
