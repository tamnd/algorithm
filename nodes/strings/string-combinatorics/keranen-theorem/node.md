---
tag: 7K2T8P
kind: theorem
slug: keranen-theorem
name: Keränen's theorem
aliases:
- Keranen theorem on abelian square-free words
area: strings/string-combinatorics
level: advanced
summary: Infinite abelian square-free words exist over a four-letter alphabet.
prereqs: [abelian-square, abelian-equivalence]
see_also: [square-free-word, thue-theorem, avoidability, abelian-complexity, parikh-vector, cube, dejean-theorem, thue-morse-word]
sources:
  - paper: doi:10.1007/3-540-55719-9_62
    title: Veikko Keränen, Abelian squares are avoidable on 4 letters, Automata, Languages and Programming (ICALP 1992), Lecture Notes in Computer Science 623, 1992, 41-52
    locator: the 85-uniform morphism on four letters, its invariance under the cyclic shift of the letters, and the computer-assisted proof that it maps Abelian-square-free words to Abelian-square-free words
  - paper: doi:10.1016/j.tcs.2009.05.027
    title: Veikko Keränen, A powerful abelian square-free substitution over 4 letters, Theoretical Computer Science 410(38-40), 2009, 3893-3900
    locator: a new Abelian-square-free substitution over four letters and its consequences for the growth of Abelian-square-free words
  - paper: doi:10.1016/s0166-218x(97)88002-x
    title: Arturo Carpi, On the number of Abelian square-free words on four letters, Discrete Applied Mathematics 81(1-3), 1998, 155-167
    locator: the exponential growth of the number of Abelian-square-free words over four letters
  - paper: "Peter A. B. Pleasants, Non-repetitive sequences, Proceedings of the Cambridge Philosophical Society 68(2), 1970, 267-274"
    title: Peter A. B. Pleasants, Non-repetitive sequences
    locator: an infinite word over five letters without Abelian squares
  - paper: "F. Michel Dekking, Strongly non-repetitive sequences and progression-free sets, Journal of Combinatorial Theory, Series A 27(2), 1979, 181-185"
    title: F. Michel Dekking, Strongly non-repetitive sequences and progression-free sets
    locator: the infinite ternary word without Abelian cubes, the binary word without Abelian fourth powers, and the history of the question of Erdős
---

Keränen's theorem says that there is an infinite word over four letters that contains no [Abelian square](/abelian-square/), that is, no factor $uv$ with $v$ a rearrangement of $u$. Over three letters this is impossible, since every ternary word of length 8 contains an Abelian square, so four letters is the least alphabet size. The question was asked by Erdős in 1961, and Keränen settled it in 1992 with an 85-uniform morphism found and checked by computer.

## Statement

Let $\Sigma$ be a finite [alphabet](/alphabet/); only equality of letters is used. Indices are 0-based. For a word $w$, $\Psi(w)$ is its [Parikh vector](/parikh-vector/), the vector of letter counts. A finite or infinite word $w$ is Abelian-square-free if there are no $i \ge 0$ and $m \ge 1$ with $\Psi(w[i..i+m-1]) = \Psi(w[i+m..i+2m-1])$.

**Theorem (Keränen, 1992).** There is an infinite Abelian-square-free word over the four letters $\{a, b, c, d\}$.

**The morphism.** Let $\sigma$ be the cyclic shift $a \mapsto b \mapsto c \mapsto d \mapsto a$. Keränen's morphism $g$ is the 85-uniform morphism with
```
g(a) = abcacdcbcdcadcdbdabacabadbabcbdbcbacbcdcacbabdabacadcbcdcacdbcbacbcdcacdcbdcdadbdcbca
```
and $g(\sigma^k(a)) = \sigma^k(g(a))$ for $k = 1, 2, 3$; for example $g(b)$ starts with `bcdbdadcdadbadacabcb`. The word $g(a)$ contains 19 letters $a$, 21 letters $b$, 27 letters $c$ and 18 letters $d$. Since $g(a)$ starts with $a$, the words $a, g(a), g^2(a), \ldots$ are prefixes of each other, and their limit $g^\omega(a)$ is the infinite Abelian-square-free word of the theorem.

**Small alphabets.** Over $\{a, b\}$, the longest Abelian-square-free words have length 3 (`aba`), and over $\{a, b, c\}$ length 7 (`abacaba`). The numbers of ternary Abelian-square-free words of the lengths 0 to 8 are 1, 3, 6, 12, 18, 30, 30, 18, 0.

## In plain words

Take a word and look at any two neighboring blocks of the same length. If the second block uses exactly the same letters as the first, just in another order, the word has an Abelian square. With two or three different letters, every long enough word has one, and in fact any word of length 8 over three letters does. The theorem says that with four letters one can write forever without ever making such a pair of blocks. Keränen found an explicit rule: replace each letter by a fixed block of 85 letters, and repeat. Each step keeps the word free of Abelian squares, so the process builds an infinite such word.

## Proof

The proof has three parts: a compactness step, an iteration step, and the key lemma on the morphism $g$, which is a finite check done by computer.

**Lemma 1 (prefixes of the iterates).** If $h$ is a uniform morphism of length $L \ge 2$ with $h(a)$ starting with $a$, then $h^k(a)$ is a proper prefix of $h^{k+1}(a)$ for each $k \ge 0$, and the iterates have a unique infinite limit $h^\omega(a)$ whose prefixes are the $h^k(a)$.

*Proof.* $a$ is a proper prefix of $h(a)$. If $h^k(a)$ is a prefix of $h^{k+1}(a)$, apply $h$: $h^{k+1}(a)$ is a prefix of $h^{k+2}(a)$, and it is proper since $|h^{k+2}(a)| = L^{k+2} > L^{k+1} = |h^{k+1}(a)|$. The limit is the infinite word whose prefix of length $|h^k(a)|$ is $h^k(a)$ for each $k$. $\square$

**Lemma 2 (iteration).** Suppose $h$ maps each Abelian-square-free word to an Abelian-square-free word, and $h(a)$ starts with $a$. Then $h^\omega(a)$ is Abelian-square-free.

*Proof.* The word $a$ is Abelian-square-free, so by induction each $h^k(a)$ is. An Abelian square in $h^\omega(a)$ is a finite factor, so it lies inside some prefix $h^k(a)$, which has no Abelian square. $\square$

**Lemma 3 (Keränen's morphism).** The morphism $g$ above maps each Abelian-square-free word over $\{a, b, c, d\}$ to an Abelian-square-free word.

This is the heart of the theorem. Keränen reduced it to a finite set of cases, using the 85-uniformity and the symmetry $g \circ \sigma = \sigma \circ g$, and checked the cases by computer; the argument is in the 1992 paper. For instance, $g(a)$ and $g^2(a)$, of length 7225, contain no Abelian square.

**Proof of the theorem.** By Lemma 3, $g$ preserves Abelian-square-freeness, and $g(a)$ starts with $a$. By Lemmas 1 and 2, $g^\omega(a)$ is an infinite Abelian-square-free word over four letters. $\blacksquare$

**Compactness.** The theorem is equivalent to the existence of arbitrarily long finite Abelian-square-free words over four letters. *Proof.* One direction takes prefixes. For the other, the Abelian-square-free words form a tree under the prefix order, closed under prefixes, with finitely many children per node and infinitely many nodes. By König's lemma it has an infinite path, and every finite prefix along that path is Abelian-square-free, so the infinite word is. $\square$

**Three letters do not suffice.** Every word of length 8 over $\{a, b, c\}$ contains an Abelian square. *Proof.* By an exhaustive search that extends Abelian-square-free words one letter at a time and tests each new suffix of even length: the numbers of survivors at the lengths 0 to 8 are 1, 3, 6, 12, 18, 30, 30, 18, 0. Since a factor $xx$ is an Abelian square, adjacent letters differ, which keeps the search small. $\square$

## Consequences

1. **Square-free words.** An Abelian-square-free word is square-free, so $g^\omega(a)$ is also an infinite [square-free word](/square-free-word/) over four letters. This is weaker than the [Thue theorem](/thue-theorem/), which gives square-free words over three letters.
2. **Exponential growth.** Carpi (1998) proved that the number of Abelian-square-free words of length $n$ over four letters grows exponentially in $n$. The counts for the lengths 1 to 8 are 4, 12, 36, 96, 264, 648, 1584, 3576.
3. **Optimality of the alphabet.** With the bound of length 7 over three letters and length 3 over two letters, four is the least alphabet size on which Abelian squares are [avoidable](/avoidability/).
4. **Abelian powers.** Together with Dekking's results (1979) that Abelian cubes are avoidable over three letters and Abelian fourth powers over two letters, the theorem completes the table of the least alphabets that avoid Abelian $k$-th powers: 4 letters for $k = 2$, 3 for $k = 3$, and 2 for $k \ge 4$.
5. **Abelian pattern avoidance.** The theorem is the base case of the study of patterns avoided in the Abelian sense, where an instance of a pattern only has to match up to rearrangement of each block.

## Tightness

- **Alphabet size.** Three letters are not enough: every ternary word of length 8 contains an Abelian square, as shown above. Two letters are not enough: every binary word of length 4 contains $aa$, $bb$, or the square $abab$ or $baba$.
- **Squares versus Abelian squares.** For ordinary squares three letters suffice, by the Thue theorem. The Abelian relaxation costs exactly one more letter.

## History

Erdős asked in 1961 whether there is an infinite word over a small alphabet without Abelian squares, and in particular over four letters. Evdokimov constructed one over 25 letters in 1968, Pleasants reduced the alphabet to five letters in 1970, and Dekking settled the questions for Abelian cubes and fourth powers in 1979. The four-letter case resisted until Keränen found the 85-uniform morphism by computer search and proved it Abelian-square-free in 1992. In 2009 he gave a further substitution with stronger properties, which yields more such words.

## References
