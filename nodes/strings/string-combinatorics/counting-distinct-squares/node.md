---
tag: H44R4H
kind: problem
slug: counting-distinct-squares
name: Counting distinct squares
aliases:
- distinct square factors
area: strings/string-combinatorics
level: advanced
summary: Count the distinct square factors of a string.
prereqs: [square, maximal-repetition]
see_also: [computing-runs, runs-theorem, cube, fibonacci-word, suffix-tree, suffix-array, palindromic-tree, square-free-word]
sources:
  - paper: doi:10.1006/jcta.1997.2843
    title: Aviezri S. Fraenkel and Jamie Simpson, How many squares can a string contain?, Journal of Combinatorial Theory, Series A 82(1), 1998, 112-120
    locator: the bound of fewer than 2n distinct squares, from at most two squares with their rightmost occurrence at each position, and the family of words with close to n squares
  - paper: doi:10.1016/j.tcs.2007.03.025
    title: Lucian Ilie, A note on the number of squares in a word, Theoretical Computer Science 380(3), 2007, 373-376
    locator: the improved bound 2n - Θ(log n)
  - paper: doi:10.5070/c65165014
    title: Srečko Brlek and Shuo Li, On the number of squares in a finite word, Combinatorial Theory 5(1), 2025
    locator: the proof that a word of length n with σ distinct letters has at most n - σ distinct nonempty squares
  - paper: doi:10.1016/j.dam.2014.08.016
    title: Antoine Deza, Frantisek Franek and Adrien Thierry, How many double squares can a string contain?, Discrete Applied Mathematics 180, 2015, 52-69
    locator: the bound 11n/6 on distinct squares through double squares
  - paper: doi:10.1016/j.jcss.2004.03.004
    title: Dan Gusfield and Jens Stoye, Linear time algorithms for finding and representing all the tandem repeats in a string, Journal of Computer and System Sciences 69(4), 2004, 525-546
    locator: the vocabulary of tandem repeats (all distinct squares) found and marked in the suffix tree in O(n) time for a constant alphabet
  - paper: doi:10.1016/j.tcs.2013.11.018
    title: Maxime Crochemore, Costas S. Iliopoulos, Marcin Kubica, Jakub Radoszewski, Wojciech Rytter and Tomasz Waleń, Extracting powers and periods in a word from its runs structure, Theoretical Computer Science 521, 2014, 29-41
    locator: the distinct squares and their count computed from the runs and the suffix array in O(n) time over an integer alphabet
  - paper: doi:10.1016/s0304-3975(98)00252-7
    title: Aviezri S. Fraenkel and Jamie Simpson, The exact number of squares in Fibonacci words, Theoretical Computer Science 218(1), 1999, 95-106
    locator: the exact numbers of distinct squares and of square occurrences in the finite Fibonacci words
---

Counting distinct squares asks how many different words $uu$, with $u$ nonempty, occur as factors of a given string. A string of length $n$ has up to about $n^2/4$ square occurrences counted with position, but only fewer than $n$ distinct squares, a bound conjectured by Fraenkel and Simpson in 1998 and proved by Brlek and Li in 2025. The count can be computed in $O(n)$ time from the [runs](/maximal-repetition/) of the string or from its [suffix tree](/suffix-tree/).

## In plain words

A square is a block of text that is some piece written twice in a row, like "abab", or "ississ", which is "iss" written twice. A long text can hold the same square in many places; here each different square is counted once. The surprise is that the number of different squares is always smaller than the length of the text, even though the number of places where squares sit can be much larger. Finding them all quickly relies on the runs: every square lies inside one long stretch of text that repeats with a fixed period, and there are few such stretches.

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/); only equality of letters is needed for the definition, and the linear-time algorithms assume an integer alphabet. Indices are 0-based, and $s = s[0..n-1]$.

**Input.** A string $s \in \Sigma^n$.

**Output.** The number
$$ \mathrm{sq}(s) = \bigl|\{\, uu : u \in \Sigma^+,\ uu \text{ is a factor of } s \,\}\bigr|. $$

A factor $s[i..i+2m-1]$ is a [square](/square/) of half-length $m \ge 1$ exactly when $s[t] = s[t+m]$ for $i \le t < i+m$. The set is a set of words, so a square that occurs at several positions counts once. A square $uu$ is primitively rooted if $u$ is a [primitive word](/primitive-word/).

## Variants

- **Listing.** Output each distinct square once, for example as the pair (leftmost start, half-length). The output size is less than $n$, so listing costs no more than counting.
- **Primitively rooted squares.** Count only the distinct $uu$ with $u$ primitive. In $a^8$ there are 4 distinct squares, $a^2, a^4, a^6, a^8$, but only $aa$ is primitively rooted.
- **Occurrences.** Count the pairs (start, half-length). This number can be quadratic, as in $a^n$, and the number of occurrences of primitively rooted squares is $O(n \log n)$, attained by the [Fibonacci words](/fibonacci-word/).
- **Higher powers.** Count distinct [cubes](/cube/) or $k$-th powers. The map $uuu \mapsto uu$ is injective, so there are at most as many distinct cubes as distinct squares.
- **Square-freeness.** Decide whether $\mathrm{sq}(s) = 0$, that is, whether $s$ is a [square-free word](/square-free-word/).
- **Substring queries.** Preprocess $s$ and answer the number of distinct squares inside any factor $s[i..j]$.

## Examples

| String | $n$ | Distinct squares | Count |
|---|---|---|---|
| `aabaabaa` | 8 | `aa`, `aabaab`, `abaaba`, `baabaa` | 4 |
| `mississippi` | 11 | `ss`, `pp`, `ississ`, `ssissi` | 4 |
| `aaaaaaaa` | 8 | `aa`, `aaaa`, `aaaaaa`, `aaaaaaaa` | 4 |
| `abcacb` | 6 | none | 0 |
| `abaababaabaababaababa` | 21 | 14 squares, of half-lengths 1, 2, 3, 5, 8 | 14 |

In `aabaabaa`, the square `aa` occurs at the indices 0, 3 and 6 and counts once. The three squares of half-length 3 are the rotations `aab`, `aba`, `baa` doubled, and all lie in the single run of period 3 that covers the whole string. The last row is the Fibonacci word of length 21; its squares have the half-lengths 1 (`aa`), 2 (two), 3 (three), 5 (four) and 8 (four).

**Fibonacci words.** For the finite Fibonacci words of the lengths 8, 13, 21, 34, 55, 89, 144, 233 the counts are 4, 8, 14, 24, 40, 66, 108, 176. Each is $2(F - 1)$, where $F$ is the Fibonacci number two steps before the length, as Fraenkel and Simpson computed in 1999.

**Maximum over binary strings.** Let $M_2(n)$ be the largest $\mathrm{sq}(s)$ over $s \in \{a, b\}^n$.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $M_2(n)$ | 0 | 1 | 1 | 2 | 2 | 3 | 3 | 4 | 5 | 6 | 7 | 7 | 8 | 9 | 10 | 11 | 12 | 12 | 13 | 13 |

Strings attaining the maximum include `aabaababa` ($n = 9$), `aababbabba` ($n = 10$), `aabaababaababa` ($n = 14$) and `aababaababaabaab` ($n = 16$). Over three letters the maxima for $n \le 12$ are the same as over two letters.

## Known algorithms

- **Naive.** For each start $i$ and half-length $m$, test $s[i..i+m-1] = s[i+m..i+2m-1]$ and insert the square into a set of strings. This takes $O(n^3)$ time; with a rolling hash, the comparison and the insertion take $O(1)$ expected time, for $O(n^2)$ time with a small probability of error from hash collisions. A simpler $O(n^2)$ deterministic method fixes $m$, scans $t$ while counting the length of the current stretch with $s[t] = s[t+m]$, and reports a square whenever the stretch reaches $m$; deduplication then needs a [suffix array](/suffix-array/) or a trie.
- **Suffix tree.** Gusfield and Stoye (2004) find the vocabulary of tandem repeats, the set of all distinct squares, and mark the end of each in the [suffix tree](/suffix-tree/) in $O(n)$ time for a constant alphabet. They first compute a set of leftmost square occurrences that covers every distinct square, then walk the tree to extend it by rotations.
- **From runs.** Every square occurrence $s[i..i+2m-1]$ lies in a unique [run](/maximal-repetition/) $(a, b, p)$ whose period $p$ divides $m$. So the distinct squares are the factors $s[t..t+2kp-1]$ with $a \le t \le b - 2kp + 1$, over all runs and all $k \ge 1$. Crochemore, Iliopoulos, Kubica, Radoszewski, Rytter and Waleń (2014) keep, for each distinct square, only its leftmost occurrence, which they detect with the suffix array and [LCP array](/lcp-array/), and count all of them in $O(n)$ time over an integer alphabet. The runs come from [computing runs](/computing-runs/) in $O(n)$ time.

## Bounds

- **Output size.** $\mathrm{sq}(s) \le n - \sigma(s)$, where $\sigma(s)$ is the number of distinct letters of $s$ (Brlek and Li, 2025). This settled the conjecture $\mathrm{sq}(s) < n$ of Fraenkel and Simpson.
- **Earlier bounds.** Fraenkel and Simpson (1998) proved $\mathrm{sq}(s) < 2n$. Their argument looks at the rightmost occurrence of each distinct square and shows that at most two squares have their rightmost occurrence starting at any one position. The key step is the three-squares lemma: if $u^2$, $v^2$, $w^2$ are prefixes of a word, $|u| < |v| < |w|$ and $u$ is primitive, then $|u| + |v| \le |w|$. Ilie (2007) improved the bound to $2n - \Theta(\log n)$, and Deza, Franek and Thierry (2015) to $11n/6$.
- **Lower bounds.** Fraenkel and Simpson gave an infinite family of binary words with $\mathrm{sq}(s)/n \to 1$, so the factor 1 in $n - \sigma(s)$ cannot be improved. The table above shows that for small $n$ the true maximum is well below $n - 2$.
- **Time.** Any algorithm must read the whole input, so $\Omega(n)$ time is needed, and the algorithms above reach it over integer alphabets. Over a general alphabet with equality tests only, deciding whether $\mathrm{sq}(s) > 0$ already needs $\Omega(n \log n)$ comparisons in the worst case, by the lower bound of Main and Lorentz for square-freeness.

## Reductions

- **To runs.** As above, each distinct square is generated by a run and a multiple $2kp$ of its period, so counting distinct squares reduces to computing runs plus deduplication of the generated factors. The [runs theorem](/runs-theorem/) bounds the number of runs by $n$.
- **From square-freeness.** Square-freeness is the case "is the count 0?", so any algorithm for counting decides it.
- **Leftmost occurrences.** Two occurrences of the same square are equal factors, so counting distinct squares is counting the pairs (start, half-length) that are squares and are leftmost occurrences of their factor. Leftmost occurrences are tested with the suffix array: $s[i..i+\ell-1]$ is leftmost if no suffix starting before $i$ shares a prefix of length $\ell$ with the suffix at $i$.

## Applications

- **Tandem repeats in biology.** The vocabulary of tandem repeats lists the distinct repeated units of a DNA sequence once each, which is the form in which Gusfield and Stoye report them.
- **Combinatorics on words.** The count measures the repetitiveness of a word, and the extremal words, such as Fibonacci words, are standard test cases for repetition bounds.
- **Analogy with palindromes.** A string of length $n$ has at most $n + 1$ distinct palindromic factors, counting the empty word, and the [palindromic tree](/palindromic-tree/) lists them online. The square bound has the same flavor, but its proof is much harder.

## References
