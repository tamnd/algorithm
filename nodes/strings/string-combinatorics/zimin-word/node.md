---
tag: 3DCQEE
kind: definition
slug: zimin-word
name: Zimin word
aliases:
- Zimin words
area: strings/string-combinatorics
level: research
summary: A word Z_n built recursively, unavoidable among words over any alphabet.
prereqs: [string-morphism]
see_also: [avoidability, thue-theorem, square-free-word, thue-morse-word, pigeonhole-principle, ramsey-theorem, keranen-theorem, string-period]
sources:
  - paper: "A. I. Zimin, Blocking sets of terms, Mathematics of the USSR-Sbornik 47(2), 1984, 353-364"
    locator: the words Z_n and the theorem that a pattern with n variables is unavoidable exactly when Z_n encounters it
  - paper: "Dwight R. Bean, Andrzej Ehrenfeucht and George F. McNulty, Avoidable patterns in strings of symbols, Pacific Journal of Mathematics 85(2), 1979, 261-294"
    locator: the characterization of unavoidable patterns by deletion of free sets, found independently of Zimin
  - book: isbn:9780521812207
    title: M. Lothaire, Algebraic Combinatorics on Words, Encyclopedia of Mathematics and its Applications 90, Cambridge University Press, 2002
    locator: Chapter 3, Unavoidable patterns (J. Cassaigne), on Zimin words, Zimin's theorem and avoidability indices
  - paper: "Joshua Cooper and Danny Rorabaugh, Bounds on Zimin word avoidance, Electronic Journal of Combinatorics 21(1), 2014, paper P1.62"
    locator: the function f(n, k), its values for small n and k including f(3, 2) = 29, and tower-type bounds
---

The Zimin words are $Z_1 = x_1$ and $Z_{n+1} = Z_n\, x_{n+1}\, Z_n$, so $Z_2 = x_1 x_2 x_1$, $Z_3 = x_1 x_2 x_1 x_3 x_1 x_2 x_1$, and $Z_n$ has length $2^n - 1$. Read as patterns, they are unavoidable: for every $n$ and every finite alphabet, every long enough word contains an instance of $Z_n$. Zimin (1982) and, independently, Bean, Ehrenfeucht and McNulty (1979) showed that they are the universal unavoidable patterns: a pattern with $n$ variables is unavoidable exactly when it occurs, in the morphic sense, in $Z_n$.

## Definition

Let $X = \{x_1, x_2, \ldots\}$ be an alphabet of *variables* and $\Sigma$ a finite alphabet of $k \ge 1$ *letters*; only equality of letters is used, and positions are indexed from 0. A *pattern* is a nonempty word over $X$.

**Zimin words.** $Z_1 = x_1$ and $Z_{n+1} = Z_n\, x_{n+1}\, Z_n$ for $n \ge 1$. Writing $a, b, c, d$ for $x_1, x_2, x_3, x_4$:

| $n$ | $Z_n$ | length |
| --- | --- | --- |
| 1 | `a` | 1 |
| 2 | `aba` | 3 |
| 3 | `abacaba` | 7 |
| 4 | `abacabadabacaba` | 15 |

The letter at position $i$ of $Z_n$, for $0 \le i < 2^n - 1$, is $x_{t+1}$, where $2^t$ is the largest power of 2 dividing $i + 1$. *Proof.* By induction on $n$: positions $0, \ldots, 2^{n-1} - 2$ and $2^{n-1}, \ldots, 2^n - 2$ hold copies of $Z_{n-1}$, and $i$ and $i + 2^{n-1}$ have the same 2-adic valuation of $i + 1$ when $i + 1 < 2^{n-1}$; the middle position $i = 2^{n-1} - 1$ has $i + 1 = 2^{n-1}$ and holds $x_n$. $\square$

**Instances and encounters.** A morphism $h : X^* \to \Sigma^*$ is *nonerasing* if $h(x) \ne \varepsilon$ for every variable $x$; see [string morphisms](/string-morphism/). A word $u$ is an *instance* of a pattern $p$ if $u = h(p)$ for some nonerasing $h$, and a word $w$ *encounters* $p$ if some factor of $w$ is an instance of $p$; otherwise $w$ *avoids* $p$. The same definitions apply with $\Sigma$ replaced by $X$, so a pattern can encounter another pattern.

Since $x_{n+1}$ occurs once in $Z_{n+1}$, a word $u$ is an instance of $Z_{n+1}$ if and only if $u = v\,t\,v$ with $t$ nonempty and $v$ an instance of $Z_n$. So the instances of $Z_2$ are the words $vtv$ with $v, t$ nonempty, and the instances of $Z_n$ are the *sesquipowers* of order $n$, also called $n$-fold bi-ideals.

**Unavoidability.** For every $n \ge 1$ and $k \ge 1$ there is a least integer $f(n, k)$ such that every word of length $f(n, k)$ over $k$ letters encounters $Z_n$. *Proof.* $f(1, k) = 1$. Suppose every word of length $m$ over $k$ letters encounters $Z_n$, and let $w$ have length $(m + 1)(k^m + 1)$. Cut $w$ into $k^m + 1$ consecutive blocks of length $m + 1$. By the [pigeonhole principle](/pigeonhole-principle/), two blocks, starting at $s < s'$, have the same prefix $P$ of length $m$. $P$ contains an instance $v$ of $Z_n$ starting at some offset $o$, so $v$ occurs at $s + o$ and at $s' + o$. These occurrences do not overlap or touch, because $s' - s \ge m + 1 > |v|$, so $w$ has a factor $v\,t\,v$ with $t$ nonempty, an instance of $Z_{n+1}$. Hence $f(n + 1, k) \le (f(n, k) + 1)(k^{f(n, k)} + 1)$. $\square$

**Zimin's theorem.** A pattern $p$ is *unavoidable* if for every finite alphabet, all but finitely many words encounter $p$. Zimin's theorem states that a pattern with $n$ distinct variables is unavoidable if and only if $Z_n$ encounters it. The easy direction follows from the bound above: if $g(p)$ is a factor of $Z_n$ for a nonerasing $g : X^* \to X^*$, and $w$ has a factor $h(Z_n)$, then $h(g(p))$ is a factor of $h(Z_n)$, so every word that encounters $Z_n$ encounters $p$. The converse, that a pattern $Z_n$ does not encounter can be avoided on some finite alphabet, is the deeper half; Zimin's proof constructs, for such a pattern, an infinite word over a finite alphabet that avoids it.

## Examples and non-examples

- **$Z_2 = xyx$.** A word avoids $xyx$ exactly when no letter occurs at two positions with a gap between them and no letter occurs three times in a row, that is, when it is a product of blocks $c$ or $cc$ with all block letters distinct. So the longest words over $k$ letters avoiding $xyx$ have length $2k$, such as `aabbcc`, and $f(2, k) = 2k + 1$. Over two letters, the words of length 4 that avoid $xyx$ are exactly `aabb` and `bbaa`.
- **$Z_3$ over two letters.** Exhaustive search gives $f(3, 2) = 29$: every binary word of length 29 encounters $xyxzxyx$, while `aabbbbbbabbabbaabaabaaaaaabb`, of length 28, avoids it. This agrees with the value computed by Cooper and Rorabaugh.
- **One letter.** The word $a^m$ is an instance of $Z_n$ exactly when $m \ge 2^n - 1$, so $f(n, 1) = 2^n - 1$.
- **Unavoidable patterns.** $Z_3 = $ `abacaba` encounters $xyzyx$ (take $x \mapsto a$, $y \mapsto b$, $z \mapsto aca$), $xyzxy$ (take $x \mapsto a$, $y \mapsto b$, $z \mapsto ac$) and $xyxzx$, so these three patterns are unavoidable.
- **Avoidable patterns.** Zimin words are square-free, so $Z_n$ never encounters $xx$, and the patterns $xx$, $xyxy$, $xyyx$, $xxyx$ and $xyzxzy$ are not encountered by the Zimin word on their variables. By the theorem they are avoidable; for $xx$ this is [Thue's theorem](/thue-theorem/), which avoids it on three letters, and the pattern $xxx$ is avoided on two letters by the [Thue-Morse word](/thue-morse-word/).
- **Growth.** The values of $f(n, k)$ grow extremely fast in $n$: the bound in the proof is a tower of exponentials, and Conlon, Fox and Sudakov proved lower bounds showing that growth of tower type in $n$ cannot be avoided. Only a few small values are known exactly.

The values in these examples, the position formula, the characterization of instances of $Z_{n+1}$, the square-freeness of $Z_n$ for $n \le 6$ and the listed encounters were checked by script, with instances tested against a brute-force search over all nonerasing morphisms.

## Related definitions

- **Avoidable pattern and avoidability index.** A pattern is avoidable on $k$ letters if some infinite word over $k$ letters avoids it; its avoidability index is the least such $k$. These are the subject of [pattern avoidability](/avoidability/).
- **Sesquipower (bi-ideal sequence).** The instances of $Z_n$; every nonempty word is a sesquipower of order 1, and $v\,t\,v$ with $v$ of order $n$ is one of order $n + 1$. They appear in the study of finitely generated semigroups and Burnside-type problems.
- **Square-free word.** A [square-free word](/square-free-word/) avoids the pattern $xx$; Zimin words are themselves square-free.
- **Ruler sequence.** The position formula identifies $Z_n$ with the first $2^n - 1$ terms of the ruler sequence $1, 2, 1, 3, 1, 2, 1, 4, \ldots$ of 2-adic valuations of $1, 2, 3, \ldots$, plus one.
- **Abelian patterns.** Replacing equality of words by equality of letter counts gives abelian instances; [Keränen's theorem](/keranen-theorem/) shows that abelian squares are avoidable on four letters.
- **Unavoidable regularities.** The unavoidability of $Z_n$ is a word analogue of [Ramsey's theorem](/ramsey-theorem/): every long enough word must contain a fixed kind of structure, whatever the alphabet.

## References
