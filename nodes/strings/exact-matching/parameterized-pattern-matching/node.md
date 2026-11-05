---
tag: EV75E5
kind: problem
slug: parameterized-pattern-matching
name: Parameterized pattern matching
aliases:
- p-matching
- matching up to variable renaming
area: strings/exact-matching
level: advanced
summary: Find substrings that match the pattern under a consistent bijective renaming of symbols.
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern}
  time: {worst: Θ(n + m)}
prereqs: [string-matching, knuth-morris-pratt, prefix-function]
see_also: [order-preserving-matching, suffix-tree, generalized-suffix-tree, aho-corasick, circular-pattern-matching, string-matching, prefix-function]
sources:
  - paper: doi:10.1145/167088.167115
    title: Brenda S. Baker, A theory of parameterized pattern matching, Proceedings of the 25th ACM Symposium on Theory of Computing (STOC 1993), 71-80
    locator: the definitions of parameterized strings and parameterized matches, the parameterized suffix tree, and the software duplication application
  - paper: doi:10.1006/jcss.1996.0003
    title: Brenda S. Baker, Parameterized pattern matching, algorithms and applications, Journal of Computer and System Sciences 52(1) (1996), 28-42
    locator: the journal version of the STOC 1993 paper (parameterized matching algorithms and their applications)
  - paper: doi:10.1137/s0097539793246707
    title: Brenda S. Baker, Parameterized duplication in strings, algorithms and an application to software maintenance, SIAM Journal on Computing 26(5) (1997), 1343-1362
    locator: the parameterized suffix tree, built in linear time for fixed alphabets, and the report of all maximal parameterized matches over a threshold length
  - paper: doi:10.1016/0020-0190(94)90086-8
    title: Amihood Amir, Martin Farach and S. Muthukrishnan, Alphabet dependence in parameterized matching, Information Processing Letters 49(3) (1994), 111-115
    locator: the main theorems (an O(n log π) algorithm with π the smaller of m and the number of parameter symbols, and a matching lower bound in the comparison model)
  - paper: doi:10.1137/s0097539701424465
    title: Richard Cole and Ramesh Hariharan, Faster suffix tree construction with missing suffix links, SIAM Journal on Computing 33(1) (2003), 26-42
    locator: the randomized linear-time construction of parameterized suffix trees
  - paper: doi:10.1007/3-540-58094-8_20
    title: Ramana M. Idury and Alejandro A. Schäffer, Multiple matching of parameterized patterns, Combinatorial Pattern Matching (CPM 1994), Lecture Notes in Computer Science, 226-239
    locator: the dictionary version of the problem
---

Parameterized pattern matching asks for every window of a text $T$ of length $n$ that becomes equal to a pattern $P$ of length $m$ after a consistent one-to-one renaming of some symbols, the *parameters*, while the other symbols, the *constants*, must match exactly. Brenda Baker introduced it in 1993 to find duplicated code in large programs, where two copies differ only in the names of their variables. Replacing each parameter by the distance to its previous occurrence turns the problem into a variant of [Knuth-Morris-Pratt](/knuth-morris-pratt/) that runs in $\Theta(n + m)$ time over an integer alphabet, and in $O(n \log \pi)$ comparisons in general, which Amir, Farach and Muthukrishnan proved optimal.

## In plain words

Two pieces of code, `x = x + y` and `a = a + b`, do the same thing: one is the other with x renamed to a and y to b. A plain search for one will not find the other.

In parameterized matching, some symbols are names that may be changed, and the rest, like `=` and `+`, must stay as they are. A window of the text matches the pattern if the names can be renamed one for one so that the window becomes the pattern. Renaming must be consistent: the same name always becomes the same new name, and two different names never become the same one.

The trick is to forget the names and remember only how far back each name was last used. Two pieces of code match exactly when these distances agree, and distances can be compared with an ordinary fast search.

## Definition

**Alphabet.** The symbols are split into a set $\Sigma$ of constants and a set $\Pi$ of parameters. The stated bounds assume an integer alphabet whose size is polynomial in $n$, so that symbols can be renamed to small integers by [radix sort](/radix-sort/) and looked up in an array; over a general alphabet where symbols can only be compared, last occurrences are kept in a balanced search tree.

**Parameterized match.** Strings $u$ and $v$ of the same length *p-match* when there is a bijection $f$ of $\Sigma \cup \Pi$ that is the identity on $\Sigma$, maps $\Pi$ onto $\Pi$, and satisfies $f(u[i]) = v[i]$ for every $i$. Equivalently, for all positions $i, j$: $u[i]$ is a constant exactly when $v[i]$ is; constants agree, $u[i] = v[i]$; and for parameters, $u[i] = u[j]$ exactly when $v[i] = v[j]$. The relation is an equivalence, and it is kept by taking factors at the same positions.

**Input.** A text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$. Indices are 0-based.

**Output.** The set $\{\, i : 0 \le i \le n - m,\ T[i \ldots i+m-1] \text{ p-matches } P \,\}$, in increasing order. Occurrences may overlap. As on the other pages of this area, if $m = 0$ every position $0, \ldots, n$ is reported, and if $m > n$ nothing is.

**Prev encoding (Baker).** For a string $S$, $\mathrm{prev}(S)[i]$ is $S[i]$ if it is a constant; 0 if it is a parameter that does not occur in $S[0 \ldots i-1]$; and $i - j$ if it is a parameter whose last earlier occurrence is at $j$. Then $u$ and $v$ p-match exactly when $\mathrm{prev}(u) = \mathrm{prev}(v)$. The encoding of a window is obtained from that of the whole text: for the window starting at $s$, an entry $d = \mathrm{prev}(T)[s + i] > 0$ is kept when $d \le i$ and becomes 0 when $d > i$, because the earlier occurrence lies outside the window.

## Variants

- **Constants only.** If $\Pi$ is empty, this is ordinary [string matching](/string-matching/).
- **Parameters only.** If $\Sigma$ is empty, a window matches when it has the same pattern of equal and distinct positions as $P$, as for "abba", which matches "xyyx" and "cddc".
- **Duplication finding.** Report all pairs of long factors of one string that p-match, Baker's original application; it uses the parameterized suffix tree.
- **Indexing.** Build the parameterized [suffix tree](/suffix-tree/) of the text, the suffix tree of the prev encodings of all suffixes, and answer queries in time proportional to the pattern. Suffix links are missing in this tree, which makes linear-time construction harder; Baker builds it in linear time for fixed alphabets, and Cole and Hariharan in randomized linear time in general.
- **Many patterns.** A dictionary version in the manner of [Aho-Corasick](/aho-corasick/), studied by Idury and Schäffer.
- **Order-preserving matching.** A different relaxation, in which values may change but their relative order must not; see [order-preserving matching](/order-preserving-matching/).

## Examples

Let all lowercase letters be parameters. Take $P$ = xyxz and $T$ = abacbcbdaba, with $n = 11$ and $m = 4$. Then $\mathrm{prev}(P)$ = (0, 0, 2, 0) and $\mathrm{prev}(T)$ = (0, 0, 2, 0, 3, 2, 2, 0, 6, 3, 2).

| position $i$ | window | prev of the window | p-match |
|---|---|---|---|
| 0 | abac | 0, 0, 2, 0 | yes, with x, y, z for a, b, c |
| 1 | bacb | 0, 0, 0, 3 | no |
| 3 | cbcb | 0, 0, 2, 2 | no, the last symbol repeats |
| 4 | bcbd | 0, 0, 2, 0 | yes, with x, y, z for b, c, d |
| 5 | cbda | 0, 0, 0, 0 | no |

The output is $\{0, 4\}$. At position 4 the text entries are 3, 2, 2, 0, and the first two become 0 because they point before the window.

More cases, with uppercase letters as constants: $P$ = xAy in $T$ = uAvvAuu gives 0 and 3 (uAv and vAu), but not 1, because A is a constant and cannot stand for a parameter; $P$ = xy in $T$ = abab gives 0, 1, 2, overlapping; $P$ = xx in $T$ = abba gives only 1.

## Known algorithms

| method | alphabet | time | extra space |
|---|---|---|---|
| test each window with a renaming table | integer | $O(nm)$ | $O(m)$ |
| prev encoding and a failure function | integer, polynomial in $n$ | $O(n + m)$ | $O(n + m)$, or $O(m + \lvert\Pi\rvert)$ streaming |
| Amir, Farach and Muthukrishnan | general, comparisons only | $O(n \log \pi)$ | $O(m)$ |
| parameterized suffix tree of $T$ (Baker; Cole and Hariharan) | integer | $O(n)$ preprocessing, randomized in general | $O(n)$ |

**Prev encoding and a failure function.** Compute $\mathrm{prev}(P)$, and the entries of $\mathrm{prev}(T)$ one at a time with an array of last occurrences. Run [KMP](/knuth-morris-pratt/) on the two encodings with one change: when $q$ characters of the window are matched and the next text entry is $d$, compare $P$'s entry $\mathrm{prev}(P)[q]$ with $d$ if $d \le q$ and with 0 if $d > q$, since an earlier occurrence more than $q$ back lies outside the window. The [prefix function](/prefix-function/) of $\mathrm{prev}(P)$ is computed with the same rule, as the longest proper prefix of $P[0 \ldots q]$ that p-matches its suffix of the same length. Because p-matching is kept by factors, the usual KMP argument shows that no occurrence is skipped, and the amortized count gives $O(n + m)$ steps. For $P$ = xyxz the failure function is (0, 1, 2, 2): for example xy p-matches yx, and xy p-matches xz.

**Alphabet dependence.** Over a general alphabet, finding the last occurrence of a parameter costs $O(\log \pi)$ comparisons with a search tree, where $\pi$ is the smaller of $m$ and $\lvert\Pi\rvert$, since only the last $m$ positions matter.

## Bounds

**Upper bound.** $O(n + m)$ time over an integer alphabet of size polynomial in $n$, and $O(n \log \pi)$ comparisons in general.

**Lower bound.** $\Omega(n + m)$, because with no parameters the problem is ordinary string matching and the [lower bound](/string-matching-lower-bound/) of $n - m + 1$ text reads applies. In the comparison model, Amir, Farach and Muthukrishnan show that the factor $\log \pi$ cannot be avoided, so the dependence on the alphabet is inherent there, unlike for exact matching, whose [KMP](/knuth-morris-pratt/) bound uses only equality tests.

**Output size.** Up to $n - m + 1$ positions, as for $T = a^n$ and $P = x^m$ with parameters.

## Reductions

- **To exact matching on encodings, with a sliding correction.** The prev encoding reduces p-matching to exact matching, except that text entries must be clipped to the window, which is why the encodings are compared by a modified KMP and not by any exact matcher.
- **From exact matching.** With $\Pi$ empty, p-matching is equality.
- **Checking one window.** Testing a single window is the test that a partial map between two strings is a bijection, done with two arrays in $O(m)$ time; this gives the naive $O(nm)$ method.

## Applications

- Finding duplicated code in large software systems, where copies differ by a systematic renaming of identifiers and constants, Baker's motivation; her tool was run on C code.
- Detecting copied programs whose variables have been renamed.

## References
