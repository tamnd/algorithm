---
tag: G7SXQF
kind: concept
slug: critical-factorization
name: Critical factorization
aliases:
- critical point of a word
area: strings/string-combinatorics
level: research
summary: A split of a word where the local period equals the global period.
prereqs: [string-period, border]
see_also: [two-way-string-matching, fine-and-wilf-theorem, lyndon-word, duval-algorithm, primitive-word, knuth-morris-pratt, galil-seiferas, minimal-rotation]
sources:
  - paper: doi:10.1016/0304-3975(79)90003-3
    title: Jean-Pierre Duval, Périodes et répétitions des mots du monoïde libre, Theoretical Computer Science 9(1), 1979, 17-26
    locator: local periods and the critical factorization theorem, with a critical point among any p - 1 consecutive positions
  - paper: doi:10.1145/116825.116845
    title: Maxime Crochemore and Dominique Perrin, Two-way string-matching, Journal of the ACM 38(3), 1991, 650-674
    locator: the critical factorization obtained from the maximal suffixes for an order and its reverse, and its use in the two-way string matching algorithm
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 8, The critical factorization theorem
  - paper: doi:10.1051/ita:2002016
    title: Tero Harju and Dirk Nowotka, Density of critical factorizations, RAIRO Theoretical Informatics and Applications 36(3), 2002, 315-327
    locator: how many of the positions of a word must be critical
---

A critical factorization of a word $x$ is a cut $x = uv$ at which the shortest repetition centered at the cut is as long as the smallest [period](/string-period/) $p$ of the whole word. Locally, the word cannot look more periodic than it is globally there. The critical factorization theorem says that every word of length at least 2 has such a cut, and in fact one among any $p - 1$ consecutive cuts. Crochemore and Perrin showed how to find a critical cut before position $p$ in linear time from two maximal suffixes, which is the heart of [two-way string matching](/two-way-string-matching/).

## In plain words

Cut a word into a left part and a right part. Look for the shortest block that agrees with the letters just left of the cut when placed ending at the cut, and with the letters just right of the cut when placed starting at the cut. Its length is the local period at that cut. At some cuts the local period is small: in `abaabaa`, the cut after `aba` sees a single `a` on both sides. The whole word repeats every three letters, so no local period exceeds three. A cut is critical if its local period reaches that maximum. The surprise is that a critical cut always exists, and that it can be found quickly by sorting suffixes in two opposite alphabetical orders.

## The idea

**Local period.** Let $x = x[0..n-1]$ be a word, with 0-based indices; only equality of letters is used in the definitions, and an order on the letters is used to find a critical cut. A cut is a position $\ell$ with $0 \le \ell \le n$, splitting $x = uv$ with $u = x[0..\ell-1]$ and $v = x[\ell..n-1]$. A nonempty word $z$ is a repetition at $\ell$ if $z$ is a suffix of $u$ or $u$ is a suffix of $z$, and $z$ is a prefix of $v$ or $v$ is a prefix of $z$. In words, $z$ placed so that it ends at the cut agrees with $x$, and so does $z$ placed so that it starts at the cut. The local period $r(\ell)$ is the least length of a repetition at $\ell$.

**Local periods never exceed the period.** Let $p = \mathrm{per}(x)$. Then $x[i] = x[i \bmod p]$ for all $i$, so $x$ is a factor of the infinite periodic word $y$ with $y[i] = x[i \bmod p]$ for all integers $i$. The word $z = y[\ell..\ell + p - 1]$ is a repetition at $\ell$: placed to end at the cut it occupies $y[\ell - p..\ell - 1]$, which equals $z$ because $y$ has the period $p$. So $r(\ell) \le p$ for every cut.

**Critical cuts.** A cut $\ell$ with $0 < \ell < n$ is critical if $r(\ell) = p$. In `abaabaa`, $p = 3$ and the local periods at the cuts 1 to 6 are 2, 3, 1, 3, 3, 1, so the cuts 2, 4 and 5 are critical. If $p = 1$, every cut is critical.

**The critical factorization theorem.** Every word with $n \ge 2$ has a critical cut. Duval's form says more: if $p \ge 2$, every set of $p - 1$ consecutive cuts among $1, \ldots, n - 1$ contains a critical cut, and $p - 1$ cannot be replaced by $p - 2$, as `aab`, with $p = 3$ and local periods 1 and 3, shows. It follows that the period of a word is the largest of its local periods.

**Finding a critical cut (Crochemore and Perrin).** Let $<$ be an order on the letters and $\tilde{<}$ the reverse order, both extended to words lexicographically with a proper prefix smaller. Let $x = uv$ where $v$ is the largest suffix of $x$ for $<$, and $x = u'v'$ where $v'$ is the largest suffix for $\tilde{<}$. If $|v| \le |v'|$, the cut $\ell = |u|$ is critical; otherwise $|u'|$ is. Moreover the cut chosen is smaller than $p$.

*Proof.* Assume $|v| \le |v'|$, so $|u'| \le |u| = \ell$; the other case is symmetric. Let $z$ be a repetition at $\ell$ of length $r$. We show $r \ge p$ by four cases.

- *$|z| \le |u|$ and $|z| \le |v|$.* Then $z$ is a suffix of $u$ and a prefix of $v$. Write $v = zt$. The suffix $zv = zzt$ of $x$ is at most $v = zt$, so $zt \le t$, that is $v \le t$. But $t$ is a shorter suffix of $x$, so $t < v$, a contradiction.
- *$|z| \le |u|$ and $|z| > |v|$.* Then $z = vs$ is a suffix of $u$, and $vsv$ is a suffix of $x$ that has $v$ as a proper prefix, so $vsv > v$, against the choice of $v$.
- *$|z| > |u|$ and $|z| > |v|$.* Then $u$ is a suffix of $z$ and $v$ a prefix of $z$, so $x = uv$ is a factor of $zz$ and has the period $r$; so $r \ge p$.
- *$|z| > |u|$ and $|z| \le |v|$.* Write $z = yu$ with $y \ne \varepsilon$ and $v = zt = yut$, so $x = uyut$. The suffix $t$ of $x$ is shorter than $v$, so $t < v$. If $t$ is not a prefix of $v$, they first differ at an offset $d < |t|$ with $t[d] < v[d]$. Write $u = u_1 u_2$ with $|u_1| = |u'|$, so $v' = u_2 v$, and $u_2 t$ is a suffix of $x$, because $ut$ is. The words $u_2 t$ and $u_2 v = v'$ first differ at the offset $|u_2| + d$, where $t[d] < v[d]$; in the reverse order this makes $u_2 t$ larger than $v'$, against the choice of $v'$. So $t$ is a prefix of $v = yut$, hence $ut$ is a prefix of $x = u \cdot yut$, and $x$ has the period $|yu| = r$. So $r \ge p$.

Hence $r(\ell) \ge p$, and $r(\ell) = p$ by the bound above. Finally, if $\ell \ge p$, the suffix $x[\ell - p..n-1]$ agrees with $v$ on its first $|v|$ letters, by the period $p$, so it has $v$ as a proper prefix and is larger than $v$, a contradiction. So $\ell < p$; in particular, if $p \ge 2$ then $\ell \ge 1$ because $r(0) = 1$. $\square$

The maximal suffix of a word for a given order is found in linear time with constant extra space, by a variant of [Duval's algorithm](/duval-algorithm/), which is how the two-way algorithm preprocesses its pattern.

## Examples

| $x$ | $p$ | local periods at cuts $1..n-1$ | critical cuts | Crochemore-Perrin cut |
|---|---|---|---|---|
| `abaabaa` | 3 | 2, 3, 1, 3, 3, 1 | 2, 4, 5 | 2 |
| `aabab` | 5 | 1, 5, 2, 2 | 2 | 2 |
| `aabaa` | 3 | 1, 3, 3, 1 | 2, 3 | 2 |
| `abacabad` | 8 | 2, 4, 4, 8, 8, 8, 8 | 4 to 7 | 7 |
| `aab` | 3 | 1, 3 | 2 | 2 |

For `abaabaa` with $a < b$, the largest suffix is $v = $ `baabaa`, starting at 1, and for $b \mathbin{\tilde{<}} a$ it is $v' = $ `aabaa`, starting at 2. The shorter one is $v'$, so the cut is 2: `ab` | `aabaa`. A repetition at the cut must end with `ab` and start with `aab`, and the shortest such word is `aab`, of length 3. At the cut 3, `aba` | `abaa`, the single letter `a` is a repetition, so that cut is not critical. In `abacabad`, $p = 8$ because the last letter occurs only once. At the cut 4, `abac` | `abad`, a repetition must end with `abac` and start with `abad`, and these overlap in no consistent way shorter than 8 letters, so the cut is critical, as are the cuts after it.

## Where it is used

- **[Two-way string matching](/two-way-string-matching/).** Crochemore and Perrin split the pattern at a critical cut $\ell < p$, compare the right part from left to right and then the left part from right to left, and shift by the period or by a length derived from the mismatch. The result runs in linear time with constant extra space; it is used for substring search in some C libraries.
- **Constant-space matching.** Critical factorizations and periodicity are the tools of other constant-space matchers, such as the [Galil-Seiferas algorithm](/galil-seiferas/), and of comparison-saving refinements of the two-way algorithm.
- **Periodicity of words.** The theorem gives the global period as the largest local period, a tool in proofs about periods next to the [Fine and Wilf theorem](/fine-and-wilf-theorem/).
- **Maximal suffixes.** Computing a critical cut needs only two maximal suffixes, which are found in linear time with constant extra space by the same kind of scan as [Duval's algorithm](/duval-algorithm/) for the [Lyndon factorization](/lyndon-factorization/).
- **Density.** Harju and Nowotka studied how many of the cuts of a word must be critical.

## References
