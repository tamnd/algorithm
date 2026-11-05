---
tag: WMP5CC
kind: theorem
slug: thue-theorem
name: Thue's theorem on square-free words
aliases:
- Thue square-free theorem
area: strings/string-combinatorics
level: core
summary: Infinite square-free words exist over a three-letter alphabet.
prereqs: [square, thue-morse-word]
see_also: [square-free-word, overlap-free-word, string-morphism, repetition-threshold, dejean-theorem, avoidability, zimin-word, keranen-theorem]
sources:
  - paper: "Axel Thue, Über unendliche Zeichenreihen, Norske Vid. Selsk. Skr. I. Mat.-Nat. Kl. Christiania 7, 1906, 1-22; English translation in J. Berstel, Axel Thue's papers on repetitions in words: a translation, Publications du LaCIM 20, Université du Québec à Montréal, 1995"
    locator: the construction of an infinite word over three letters without two adjacent equal blocks
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 2, Square-free words (J. Berstel and C. Reutenauer), the square-free ternary word obtained from the Thue-Morse word
  - book: isbn:9780521823326
    title: Jean-Paul Allouche and Jeffrey Shallit, Automatic Sequences, Cambridge University Press, 2003
    locator: Chapter 1, Stringology (overlap-free and square-free words, and the ternary square-free word derived from the Thue-Morse sequence)
  - paper: doi:10.1007/978-1-4471-0551-0_1
    title: Jean-Paul Allouche and Jeffrey Shallit, The ubiquitous Prouhet-Thue-Morse sequence, in Sequences and their Applications (SETA '98), Springer, 1999, 1-16
    locator: the section on the square-free ternary sequence that counts the ones between consecutive zeros
---

Thue's theorem states that there is an infinite word over three letters with no [square](/square/), that is, with no two equal blocks next to each other. One such word counts, between consecutive zeros of the [Thue-Morse word](/thue-morse-word/), how many ones occur, which gives $2102012\cdots$; it is also the fixed point of the [morphism](/string-morphism/) $2 \mapsto 210$, $1 \mapsto 20$, $0 \mapsto 1$. Three letters are needed, because every binary word of length 4 contains a square.

## Statement

**Theorem (Thue, 1906).** There exists an infinite [square-free word](/square-free-word/) over a three-letter alphabet. One example is the word $c = c_0 c_1 c_2 \cdots$ over $\{0, 1, 2\}$ where $c_n$ is the number of ones between the $n$-th and the $(n+1)$-th zero of the Thue-Morse word $t$ (counting from $n = 0$):
$$ c = 2102012101202102012021012102012\cdots $$
The word $c$ is the fixed point $\varphi^\omega(2)$ of the morphism $\varphi(2) = 210$, $\varphi(1) = 20$, $\varphi(0) = 1$.

**The binary case.** Every binary word of length at least 4 contains a square, so the number of letters in the theorem cannot be lowered.

Conventions: words are indexed from 0, and only equality of letters matters, so any three letters can replace $0, 1, 2$.

## In plain words

You want an endless line of three kinds of symbols in which no chunk is ever followed right away by an exact copy of itself, not even a single symbol twice in a row. With two kinds of symbols this is impossible: after three symbols you are stuck. With three kinds it can go on forever. The recipe starts from another famous endless line of zeros and ones in which no chunk appears twice and then a third time overlapping. Count the ones between each zero and the next: you always get 0, 1 or 2, and that list of counts never repeats a chunk twice in a row.

## Proof

Let $t = 0110100110010110\cdots$ be the Thue-Morse word. The proof uses one fact proved on the [Thue-Morse word](/thue-morse-word/) page: $t$ contains no [overlap](/overlap/), that is, no factor $y\,y\,a$ where $y$ is a nonempty word and $a$ is the first letter of $y$.

*Step 1: the counts are 0, 1 or 2.* $t$ has no factor $111$, since $111$ is an overlap. It has infinitely many zeros, since otherwise it would end with $111\cdots$. Since $t$ starts with $0$, it splits uniquely as
$$ t = g(c_0)\, g(c_1)\, g(c_2) \cdots, \qquad g(i) = 0\,1^{i}, $$
where $c_n$ is the number of ones after the $n$-th zero, and $c_n \in \{0, 1, 2\}$.

*Step 2: $c$ is square-free.* Extend $g$ to a morphism on words over $\{0, 1, 2\}$. Suppose $c$ contains a square $uu$ with $u$ nonempty, at position $m$. The blocks $g(c_m), \ldots, g(c_{m+2|u|-1})$ form the factor $g(u)\,g(u)$ of $t$, and the next block $g(c_{m+2|u|})$ starts with $0$. So $t$ contains $g(u)\,g(u)\,0$. The word $y = g(u)$ is nonempty and starts with $0$, so $y\,y\,0$ is an overlap in $t$, a contradiction. $\square$

*Step 3: the morphic form.* The Thue-Morse morphism $\mu(0) = 01$, $\mu(1) = 10$ fixes $t$, and $\mu(g(i)) = 01\,(10)^i$. Splitting these images into blocks $0\,1^j$ gives
$$ \mu(g(0)) = 01 = g(1), \quad \mu(g(1)) = 0110 = g(2)\,g(0), \quad \mu(g(2)) = 011010 = g(2)\,g(1)\,g(0). $$
So $t = \mu(t) = \mu(g(c_0))\,\mu(g(c_1)) \cdots = g(\varphi(c_0))\, g(\varphi(c_1)) \cdots$, and the uniqueness of the split in Step 1 gives $c = \varphi(c)$. Since $c_0 = 2$ and $\varphi(2)$ starts with $2$, $c$ is the fixed point $\varphi^\omega(2)$. $\square$

*The binary case.* Let $w$ be a binary word of length 4 with no square. Neighbours differ, since $xx$ is a square, so $w[0] \ne w[1] \ne w[2] \ne w[3]$, and with two letters $w$ is `abab` or `baba`, which are squares. So every binary word of length at least 4 contains a square. $\square$

## Consequences

- **Every alphabet with at least three letters.** An infinite square-free word over three letters is also one over any larger alphabet.
- **Many square-free words.** Each prefix of $c$ is square-free, so there are square-free ternary words of every length, and in fact their number grows exponentially. The numbers of ternary square-free words of lengths $1, \ldots, 20$ are $3, 6, 12, 18, 30, 42, 60, 78, 108, 144, 204, 264, 342, 456, 618, 798, 1044, 1392, 1830, 2388$.
- **Another morphism.** Renaming $2, 1, 0$ to $a, b, c$ turns $\varphi$ into $a \mapsto abc$, $b \mapsto ac$, $c \mapsto b$, whose fixed point $abcacbabcbac\cdots$ is the same square-free word; it is sometimes called the ternary Thue-Morse word.
- **Infinite sequences of moves.** Square-free sequences give infinite plays in games whose rules forbid repeating a block of moves twice in a row; Morse and Hedlund used this to discuss unending chess.
- **Avoidability.** The theorem says that the pattern $xx$ is avoidable on three letters; it starts the theory of [avoidable patterns](/avoidability/), and [Zimin words](/zimin-word/) describe which patterns are unavoidable.

## Tightness

- **Two letters.** The binary case above shows that three letters are necessary; the longest binary square-free words, `aba` and `bab`, have length 3.
- **Overlaps instead of squares.** On two letters one can avoid overlaps (the Thue-Morse word), but not squares; so on two letters the exponent 2 is the exact threshold.
- **Smaller exponents on three letters.** Square-freeness forbids exponent 2. Dejean showed that ternary words can avoid every exponent greater than $7/4$ but not $7/4$ itself, so the [repetition threshold](/repetition-threshold/) for three letters is $7/4$; see [Dejean's theorem](/dejean-theorem/).
- **Abelian squares.** Avoiding [abelian squares](/abelian-square/) needs four letters ([Keränen's theorem](/keranen-theorem/)); over three letters every word of length 8 has one.

## History

Thue (1906) gave the first infinite square-free word over three letters, and in 1912 he constructed the overlap-free binary word now named after him and Morse. His papers, written in German in a Norwegian journal, were little known for decades, and the results were found again by others: Morse (1921) met the binary sequence in the study of geodesics, Arshon (1937) and Morse and Hedlund (1944) built square-free sequences, and Leech (1957) gave a square-free morphism. Berstel's 1995 translation made Thue's papers widely available.

## References
