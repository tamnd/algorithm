---
tag: 365XBX
kind: concept
slug: avoidability
name: Pattern avoidability
aliases:
- unavoidable pattern
- avoidable pattern
area: strings/string-combinatorics
level: research
summary: Whether an infinite word can avoid every instance of a given pattern.
prereqs: [square-free-word, string-morphism]
see_also: [zimin-word, thue-theorem, thue-morse-word, keranen-theorem, repetition-threshold, dejean-theorem, abelian-square, cube]
sources:
  - paper: doi:10.2140/pjm.1979.85.261
    title: Dwight R. Bean, Andrzej Ehrenfeucht and George F. McNulty, Avoidable patterns in strings of symbols, Pacific Journal of Mathematics 85(2), 1979, 261-294
    locator: the definition of patterns and their instances, the characterization of unavoidable patterns by free sets, and the decidability of avoidability
  - paper: doi:10.1070/sm1984v047n02abeh002647
    title: A. I. Zimin, Blocking sets of terms, Mathematics of the USSR-Sbornik 47(2), 1984, 353-364
    locator: the words Z_n and the theorem that a pattern on n variables is unavoidable exactly when Z_n encounters it
  - book: isbn:9780521812207
    title: M. Lothaire, Algebraic Combinatorics on Words, Cambridge University Press, 2002
    locator: Chapter 3, Unavoidable patterns (J. Cassaigne), Zimin words, the avoidability index, and the binary patterns
  - paper: doi:10.1016/0304-3975(89)90071-6
    title: Kirby A. Baker, George F. McNulty and Walter Taylor, Growth problems for avoidable words, Theoretical Computer Science 69(3), 1989, 319-345
    locator: a pattern that is avoidable on four letters but not on three
  - paper: doi:10.1142/s0218196706002950
    title: Ronald J. Clark, The existence of a pattern which is 5-avoidable but 4-unavoidable, International Journal of Algebra and Computation 16(2), 2006, 351-367
    locator: the main theorem, a pattern of avoidability index 5
  - paper: doi:10.1016/j.tcs.2005.01.004
    title: "James D. Currie, Pattern avoidance: themes and variations, Theoretical Computer Science 339(1), 2005, 7-18"
    locator: the survey of avoidable patterns, the avoidability index and the open problems on it
---

A pattern is a word over variables, such as $xx$ or $xyx$, and a word encounters it if some factor is obtained from the pattern by replacing each variable with a nonempty word, the same word at each occurrence. The pattern is avoidable on $k$ letters if some infinite word over $k$ letters does not encounter it. Squares $xx$ are avoidable on three letters but not on two, while $xyx$ is unavoidable on every finite alphabet. Bean, Ehrenfeucht and McNulty, and independently Zimin, characterized the unavoidable patterns, and the [Zimin words](/zimin-word/) $Z_n$ are the hardest of them.

## In plain words

A pattern describes a shape of repetition. The pattern xx means "some block written twice in a row", and xyx means "some block, then anything, then the same block again". A long text matches a pattern if some piece of it has that shape. Some shapes can be dodged forever: a clever infinite sequence over three symbols never repeats a block twice in a row. Other shapes cannot be dodged: in any long enough text, some symbol appears three times, so the shape xyx is always there. Avoidability asks, for each shape and each number of symbols, which of these two cases holds. A surprising answer is that there is a simple test for the shapes that can never be dodged, whatever the number of symbols.

## The idea

**Patterns and instances.** Let $\Delta$ be a set of variables and $\Sigma$ an [alphabet](/alphabet/) of $k$ letters; only equality of letters is used, and indices are 0-based. A pattern is a nonempty word $P \in \Delta^+$. An instance of $P$ is a word $h(P)$, where $h : \Delta^* \to \Sigma^*$ is a nonerasing [morphism](/string-morphism/), that is, $h(x) \ne \varepsilon$ for each variable $x$. A word $w$ encounters $P$ if some factor $w[i..j]$ is an instance of $P$, and avoids $P$ otherwise. For example, the instances of $xx$ are the [squares](/square/), and $w$ encounters $xx$ exactly when it is not [square-free](/square-free-word/).

**Avoidable patterns.** $P$ is $k$-avoidable if there is an infinite word over $k$ letters that avoids it. By König's lemma on the tree of finite words that avoid $P$, this holds exactly when infinitely many finite words over $k$ letters avoid $P$. $P$ is avoidable if it is $k$-avoidable for some $k$, and unavoidable otherwise. The avoidability index $\mu(P)$ is the least such $k$, or $\infty$. Every pattern is unavoidable on one letter, since $a^{|P|}$ is an instance, so $\mu(P) \ge 2$.

**Encountering is transitive.** If a pattern $W$ encounters $P$, and a word $w$ encounters $W$, then $w$ encounters $P$: if $g(P)$ is a factor of $W$ and $h(W)$ a factor of $w$, then $h(g(P))$ is a factor of $w$, and $h \circ g$ is nonerasing. So every pattern encountered by an unavoidable pattern is unavoidable.

**Zimin words are unavoidable.** Let $Z_1 = x_1$ and $Z_{n+1} = Z_n x_{n+1} Z_n$, so $Z_2 = x_1 x_2 x_1$ and $|Z_n| = 2^n - 1$. For every $n$ and $k$, there is a length $f(n, k)$ such that every word over $k$ letters of length $f(n, k)$ encounters $Z_n$. *Proof.* By induction on $n$, with $f(1, k) = 1$. Let $L = f(n, k)$ and let $w$ have length $(L + 1)(k^L + 1)$. Cut it into $k^L + 1$ consecutive blocks of length $L + 1$. There are only $k^L$ words of length $L$, so two blocks, starting at $q_1 < q_2$, begin with the same word $u$ of length $L$. By induction, $u$ has a factor $h(Z_n)$ at some offset $o$. Its two copies, at $q_1 + o$ and $q_2 + o$, are separated by a nonempty gap $g$, because $q_2 - q_1 \ge L + 1 > |u|$. So $h(Z_n)\,g\,h(Z_n)$ is a factor of $w$, an instance of $Z_{n+1}$ with $x_{n+1} \mapsto g$. $\square$

**The characterization.** Bean, Ehrenfeucht and McNulty (1979) and Zimin (1982) proved the converse: a pattern $P$ with $n$ distinct variables is unavoidable if and only if $Z_n$ encounters $P$. Since $Z_n$ is finite, this decides unavoidability. It also gives a length bound: an unavoidable pattern on $n$ variables has length at most $2^n - 1$, so every pattern on $n$ variables of length at least $2^n$ is avoidable. Bean, Ehrenfeucht and McNulty gave the equivalent test by free sets: draw a bipartite graph with a left copy and a right copy of each variable, and an edge from $x$ on the left to $y$ on the right for each factor $xy$ of $P$. A set $F$ of variables is free if no left copy of a variable of $F$ is connected to a right copy of a variable of $F$. Then $P$ is unavoidable if and only if it can be reduced to the empty word by deleting, step by step, all occurrences of the variables of a free set.

**The index of avoidable patterns.** The characterization says which patterns are avoidable, but not on how many letters. The avoidability index is known for many families: by results of Roth and Cassaigne, every avoidable pattern on two variables is 3-avoidable. Baker, McNulty and Taylor (1989) found a pattern with $\mu = 4$, and Clark (2006) one with $\mu = 5$. Whether some avoidable pattern has $\mu \ge 6$, and whether $k$-avoidability is decidable for a fixed $k$, are open.

## Examples

| Pattern | $\mu$ | Why |
|---|---|---|
| $xyx$ | $\infty$ | It is $Z_2$. Over $k$ letters, every word of length $2k + 1$ has a letter at three positions $i < j < l$, and $w[i..l]$ is an instance; the word $a_1 a_1 a_2 a_2 \cdots a_k a_k$ of length $2k$ avoids it. |
| $xyxzxyx$ | $\infty$ | It is $Z_3$. The longest binary words that avoid it have length 28, and there are 48 of them. |
| $xx$ | 3 | Every binary word of length 4 contains a square; there are infinite ternary square-free words, by the [Thue theorem](/thue-theorem/). |
| $xxx$ | 2 | The [Thue-Morse word](/thue-morse-word/) has no [cube](/cube/). |
| $xyxyx$ | 2 | Its instances are words $uvuvu$, which contain overlaps; the Thue-Morse word is overlap-free. |
| $xyxy$ | 3 | Its instances are the squares $uu$ with $|u| \ge 2$. The longest binary words without them have length 18, and square-free ternary words avoid it. |
| $xyzxy$ | $\infty$ | $Z_3 = x_1 x_2 x_1 x_3 x_1 x_2 x_1$ encounters it with $x \mapsto x_1$, $y \mapsto x_2 x_1$, $z \mapsto x_3$. |
| $xxy$ | 3 | $Z_2 = x_1 x_2 x_1$ has no square, so it does not encounter $xxy$, and a ternary square-free word avoids it. Every binary word of length 5 contains a square that is not a suffix, hence an instance. |

The free-set test on $xyx$: its factors of length 2 are $xy$ and $yx$, so the left $x$ is joined to the right $y$, and the left $y$ to the right $x$. No left copy is joined to the right copy of the same variable, so $\{x\}$ and $\{y\}$ are both free. Deleting $y$ gives $xx$, a dead end, since the factor $xx$ joins the left and right $x$ and so $\{x\}$ is not free there. Deleting $x$ instead gives $y$, which has no factor of length 2, so $\{y\}$ is free and deleting it gives the empty word. One successful sequence is enough, so $xyx$ is unavoidable, in agreement with $Z_2 = x_1 x_2 x_1$. For $xx$, the only nonempty set $\{x\}$ is not free, so $xx$ is avoidable.

## Where it is used

- **Square-free and overlap-free words.** The questions of Thue on squares and overlaps are the cases $xx$ and $xyxyx$, and the [repetition threshold](/repetition-threshold/) with [Dejean's theorem](/dejean-theorem/) extends them to fractional powers.
- **Abelian patterns.** Replacing equality of the images by [Abelian equivalence](/abelian-equivalence/) gives Abelian avoidability; [Abelian squares](/abelian-square/) are avoidable on four letters by [Keränen's theorem](/keranen-theorem/) and not on three.
- **Algebra.** Bean, Ehrenfeucht and McNulty studied patterns to understand which identities hold in algebras built from words, and non-repetitive words give infinite finitely generated semigroups in which every square is zero, a semigroup version of the Burnside problem.
- **Unavoidable regularities.** The function $f(n, k)$ of Zimin words is a Ramsey-type bound: every long enough word over $k$ letters has the structure of $Z_n$. Its growth has been studied as a problem in its own right.
- **Pattern languages.** In learning theory, the language of all instances of a pattern is a pattern language, and deciding whether a word is an instance of a pattern with variables is NP-complete in general.

## References
