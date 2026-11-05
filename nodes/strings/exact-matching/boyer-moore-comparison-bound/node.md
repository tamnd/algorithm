---
tag: TC18E4
kind: theorem
slug: boyer-moore-comparison-bound
name: Cole's bound on Boyer-Moore comparisons
aliases:
- Cole's theorem
- 3n comparison bound
area: strings/exact-matching
level: advanced
summary: Boyer-Moore with the strong good-suffix rule makes at most about 3n comparisons on a non-periodic pattern, and this is tight; the Galil rule keeps it linear for every pattern.
prereqs: [boyer-moore, good-suffix-rule, string-period]
see_also: [galil-rule, turbo-boyer-moore, apostolico-giancarlo, fine-and-wilf-theorem, string-matching-lower-bound, worst-case-analysis]
sources:
  - paper: doi:10.1137/S0097539791195543
    title: R. Cole, Tight bounds on the complexity of the Boyer-Moore string matching algorithm, SIAM Journal on Computing 23(5) (1994), 1075-1091
    locator: the abstract and main theorems (upper bound 3n - 3(n - m + 1)/(m + 2), lower bound 3n(1 - o(1)), and the simpler 4n bound); conference version in SODA 1991, 224-233
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 3, Section 3.2 (Cole's linear worst-case bound for Boyer-Moore with the strong good suffix rule, and its extension with the Galil rule), pages 35-69
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node14.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Boyer-Moore algorithm (at most 3n text character comparisons when searching for a non periodic pattern)
  - paper: doi:10.1145/359146.359148
    title: Z. Galil, On improving the worst case running time of the Boyer-Moore string matching algorithm, Communications of the ACM 22(9) (1979), 505-508
    locator: the rule that makes the search linear when the pattern occurs
---

## Statement

Let $P[0 \ldots m-1]$ be a pattern and $T[0 \ldots n-1]$ a text, with 0-based indices and equality tests only. Call $P$ *non-periodic* when its smallest [period](/string-period/) is larger than $m/2$. Run [Boyer-Moore](/boyer-moore/) with the strong [good-suffix rule](/good-suffix-rule/), comparing each window from right to left.

**Theorem (Cole, 1994).** For a non-periodic pattern, the search makes at most

$$3n - \frac{3(n - m + 1)}{m + 2}$$

character comparisons. Conversely, there are non-periodic patterns and texts for which it makes $3n(1 - o(1))$ comparisons, as $m \to \infty$ and $n/m \to \infty$.

**Companion result.** For an arbitrary pattern, including periodic ones with many overlapping occurrences, Boyer-Moore with the [Galil rule](/galil-rule/) makes $O(n + m)$ comparisons in total, preprocessing included.

## In plain words

Boyer-Moore can read some text letters more than once, because each new window starts comparing from its right end again. One might fear that this costs about $m$ comparisons per letter on bad inputs. Cole showed that, as long as the word does not consist mostly of one repeated block, the total is never more than three comparisons per text letter, and that some inputs really reach three.

If the word is very repetitive, a text full of its copies can make plain Boyer-Moore slow, and the Galil rule repairs that by remembering the copy just found.

## Proof

This is a sketch of Cole's argument, following his paper and Gusfield's Section 3.2, where the details are given in full.

**Phases.** Split the search into phases, one per window. In phase $i$ the window is at shift $s_i$, the comparison matches a suffix $t_i$ of length $g_i$ and then fails, so the phase makes $g_i + 1$ comparisons, and then the pattern shifts by $d_i \ge 1$. The shifts add up to at most $n$, so $\sum_i d_i \le n$, and it suffices to show that the comparisons can be paid for at a rate of about 3 per unit of shift.

**Short matches.** If $g_i + 1 \le 3 d_i$, charge the phase to its own shift: at most $3 d_i$ comparisons.

**Long matches are periodic.** Suppose $g_i + 1 > 3 d_i$. The strong good-suffix shift $d_i$ is smaller than $g_i$, so by condition 1 of the [good-suffix rule](/good-suffix-rule/), $P[k - d_i] = P[k]$ for every $k$ in the matched part: the suffix of $P$ of length $g_i$, and so the text $t_i$, has period $d_i$. A string of length more than $3 d_i$ with period $d_i$ is long compared to the period, and the [Fine and Wilf theorem](/fine-and-wilf-theorem/) controls how two such periodic stretches can overlap.

**Using non-periodicity.** Because the smallest period of $P$ exceeds $m/2$, the periodic stretch with period $d_i$ cannot extend over the whole pattern, and the same text stretch cannot be matched again with long periodic matches in many later phases. Cole shows that in a phase with $g_i + 1 > 3 d_i$, all but $O(d_i)$ of the compared text characters are compared for the first time in such a role, so they can be charged to the text positions themselves, each text position receiving such a charge at most once. Adding the two kinds of charges, with a careful accounting of the constant, gives the bound $3n - 3(n-m+1)/(m+2)$; the same structure with a cruder accounting gives the simpler bound $4n$.

**Lower bound.** Cole builds non-periodic patterns made of long almost-periodic blocks, and texts made of shifted copies of these blocks, on which each phase matches about $3 d_i$ characters before failing; summing over the phases gives $3n(1 - o(1))$ comparisons. $\blacksquare$

## Consequences

- Boyer-Moore, which can be sublinear on average, is also linear in the worst case when the pattern is non-periodic: at most $3n$ comparisons, against $2n$ for [KMP](/knuth-morris-pratt/) and $n$ for the [string-matching automaton](/string-matching-automaton/), which looks at each character once.
- With the [Galil rule](/galil-rule/), finding all occurrences of any pattern takes $O(n + m)$ time, so the textbook version of Boyer-Moore has the same worst-case order as KMP.
- The bound settles a conjecture: Guibas and Odlyzko had proved $4n$ and conjectured $2n$; the lower bound of Cole shows that $2n$ is false.
- Algorithms that remember more of the previous windows go below $3n$: [Turbo Boyer-Moore](/turbo-boyer-moore/) and [Apostolico-Giancarlo](/apostolico-giancarlo/) make at most $2n$ comparisons.

## Tightness

- **The constant 3.** Tight, by Cole's lower bound $3n(1 - o(1))$.
- **Non-periodicity.** Needed for the plain algorithm when the pattern occurs often: for $T = a^n$ and $P = a^m$ (period 1), every window is a full match costing $m$ comparisons, so the search makes $(n - m + 1)m$ comparisons. The Galil rule removes this case.
- **The strong rule.** The bound is proved for the strong good-suffix rule; the analysis relies on condition 2 of that rule, which forbids the shift to repeat the failed character.

## History

Boyer and Moore (1977) gave no worst-case bound. Knuth, in the 1977 paper with Morris and Pratt, proved that the algorithm is linear when the pattern does not occur in the text, with a bound of about $6n$ comparisons. Guibas and Odlyzko (1980) improved it to $4n$ and conjectured $2n$. Galil (1979) added the rule that keeps the search linear when the pattern occurs. Richard Cole presented the tight $3n$ bound at SODA 1991, and the journal version appeared in the SIAM Journal on Computing in 1994.

## References
