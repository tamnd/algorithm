---
tag: BRQG51
kind: concept
slug: string-morphism
name: String morphism
aliases:
- substitution
- word morphism
- homomorphism of the free monoid
area: strings/string-combinatorics
level: core
summary: A map from letters to words, extended to words by concatenation.
prereqs: [alphabet, monoid]
see_also: [morphic-word, thue-morse-word, fibonacci-word, thue-theorem, zimin-word, parikh-vector, straight-line-program-grammar, avoidability]
sources:
  - book: isbn:9780521823326
    title: Jean-Paul Allouche and Jeffrey Shallit, Automatic Sequences, Cambridge University Press, 2003
    locator: Chapter 1, Stringology (morphisms), and Chapter 7, Morphic sequences (prolongable morphisms, fixed points and the incidence matrix)
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 1, Words (D. Perrin), morphisms of free monoids, and Chapter 2, Square-free words (J. Berstel and C. Reutenauer), square-free morphisms and the iteration of morphisms
  - book: isbn:9780521865722
    title: Jeffrey Shallit, A Second Course in Formal Languages and Automata Theory, Cambridge University Press, 2009
    locator: Chapter 2, Combinatorics on words (morphisms, their iteration and fixed points)
---

A string morphism is a map $h$ from words to words with $h(uv) = h(u)\,h(v)$ for all words $u$ and $v$. Such a map is fixed by the images of the single letters, and the image of a word is the concatenation of the images of its letters: with $h(a) = ab$ and $h(b) = ba$, $h(abb) = ab\,ba\,ba$. Iterating a morphism from a letter is the standard way to build infinite words with strong properties, such as the [Thue-Morse word](/thue-morse-word/), the [Fibonacci word](/fibonacci-word/) and the square-free words of [Thue's theorem](/thue-theorem/).

## In plain words

A morphism is a rewriting rule that replaces every letter of a word by a short word, all at the same time, using a fixed table with one entry per letter. Feed it `a` and you get what the table says for `a`; feed it a longer word and you get the pieces for its letters glued together in order. If the piece for `a` starts with `a`, then applying the rule again and again keeps the start of the word fixed and only adds to the end. In the limit you get one endless word that the rule turns into itself, and many famous endless words are made this way.

## The idea

Let $\Sigma$ and $\Delta$ be [alphabets](/alphabet/); only equality of letters is used. Indices are 0-based.

**Definition.** A *morphism* is a map $h : \Sigma^* \to \Delta^*$ with $h(uv) = h(u) h(v)$ for all $u, v \in \Sigma^*$, that is, a morphism of the free [monoids](/monoid/). Then $h(\varepsilon) = \varepsilon$, and $h(w[0] \cdots w[n-1]) = h(w[0]) \cdots h(w[n-1])$, so any choice of the images $h(a)$, $a \in \Sigma$, defines exactly one morphism. A morphism from $\Sigma^*$ to itself can be iterated: $h^0$ is the identity and $h^{k+1} = h \circ h^k$.

**Kinds of morphisms.**

- *Nonerasing:* $h(a) \ne \varepsilon$ for every letter $a$. Otherwise $h$ is *erasing*.
- *$k$-uniform:* $|h(a)| = k$ for every letter; a *coding* is a 1-uniform morphism, a letter-to-letter map.
- *Prolongable on $a$:* $h(a) = a x$ with $|h^k(x)| \ge 1$ for all $k$, which holds for instance when $x$ is nonempty and $h$ is nonerasing.
- *Square-free* (or overlap-free, and so on): $h$ maps every square-free word to a square-free word.

**Fixed points.** If $h$ is prolongable on $a$ with $h(a) = ax$, then $h^k(a)$ is a proper prefix of $h^{k+1}(a)$ for every $k$, and the limit $h^\omega(a) = a\,x\,h(x)\,h^2(x) \cdots$ is the unique infinite word that starts with $a$ and satisfies $h(w) = w$. *Proof.* $h^{k+1}(a) = h^k(ax) = h^k(a)\,h^k(x)$, and $h^k(x) \ne \varepsilon$, so the words grow and each is a prefix of the next. Their limit $w$ satisfies $h(w) = \lim h^{k+1}(a) = w$, since $h$ maps a prefix $h^k(a)$ of $w$ to the prefix $h^{k+1}(a)$. If $w'$ starts with $a$ and $h(w') = w'$, then $w' = h^k(w')$ starts with $h^k(a)$ for every $k$, so $w' = w$. $\square$

**The incidence matrix.** For $\Sigma = \{a_1, \ldots, a_m\}$, let $M$ be the $m \times m$ matrix with $M_{ij} = |h(a_j)|_{a_i}$. Then the [Parikh vector](/parikh-vector/) satisfies $\Psi(h(w)) = M\,\Psi(w)$, so $\Psi(h^k(a)) = M^k \Psi(a)$, and the lengths $|h^k(a)|$ grow like the powers of the largest eigenvalue of $M$.

## Examples

| morphism $h$ | kind | fixed point or iterates |
| --- | --- | --- |
| $0 \mapsto 01$, $1 \mapsto 10$ | 2-uniform | Thue-Morse word $0110100110010110\cdots$, overlap-free |
| $0 \mapsto 01$, $1 \mapsto 0$ | nonuniform | Fibonacci word $010010100100101001010\cdots$ |
| $a \mapsto abc$, $b \mapsto ac$, $c \mapsto b$ | nonuniform | $abcacbabcbacabcacbacabcbabcacb\cdots$, square-free |
| $a \mapsto ab$, $b \mapsto ccb$, $c \mapsto c$ | nonuniform, then a coding | $abccbccccb\cdots$, coded to the squares |
| $a \mapsto aa$, $b \mapsto \varepsilon$ | erasing | $h(abab) = aaaa$ |

- **Fibonacci lengths.** For $0 \mapsto 01$, $1 \mapsto 0$ the incidence matrix is $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$, and $|h^k(0)| = 1, 2, 3, 5, 8, 13, 21, 34, 55, 89$ for $k = 0, \ldots, 9$, the [Fibonacci numbers](/fibonacci-numbers/).
- **A morphic word.** The fixed point of $a \mapsto ab$, $b \mapsto ccb$, $c \mapsto c$ is $a\,b\,ccb\,ccccb\,ccccccb \cdots$, with blocks of $2, 4, 6, \ldots$ letters $c$. The coding $a, b \mapsto 1$ and $c \mapsto 0$ gives $1100100001000000100\cdots$, whose letter at index $i$ is 1 exactly when $i$ is a perfect square. This sequence is a [morphic word](/morphic-word/) but not the fixed point of any uniform morphism.
- **Square-free from Thue-Morse.** The square-free ternary word in the table, written with $a, b, c \mapsto 2, 1, 0$, is $2102012\cdots$, the sequence of the numbers of ones between consecutive zeros of the Thue-Morse word.
- **Not a morphism.** Reversal $w \mapsto w^R$ satisfies $(uv)^R = v^R u^R$, so it reverses the order of the factors and is an antimorphism, not a morphism. The map that sorts the letters of a word is not a morphism either: it sends `ba` to `ab`, while $h(b)h(a)$ would be `ba`.

## Where it is used

- **Avoiding repetitions.** Infinite square-free, overlap-free and cube-free words are built as fixed points of morphisms that preserve the property; see [Thue's theorem](/thue-theorem/), the [Thue-Morse word](/thue-morse-word/) and the [repetition threshold](/repetition-threshold/).
- **Patterns.** A word $w$ *encounters* a pattern $p$ if $w$ has a factor $h(p)$ for a nonerasing morphism $h$; [Zimin words](/zimin-word/) and the theory of [avoidability](/avoidability/) are stated this way.
- **Morphic and automatic sequences.** A [morphic word](/morphic-word/) is a coding of a fixed point; by Cobham's theorem the codings of fixed points of $k$-uniform morphisms are the $k$-automatic sequences.
- **Lindenmayer systems.** D0L systems in theoretical biology iterate a morphism on a start word to model the growth of organisms.
- **Compression and grammars.** The iterates $h^k(a)$ have [straight-line programs](/straight-line-program-grammar/) of size $O(k |\Sigma|)$, so morphic words are standard test cases for grammar compression.
- **Equations on words.** Solutions of word equations are morphisms from the unknowns to words, and morphisms between free monoids are the basic tool of combinatorics on words.

## References
