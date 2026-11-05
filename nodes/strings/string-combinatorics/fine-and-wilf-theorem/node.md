---
tag: DHJBTE
kind: theorem
slug: fine-and-wilf-theorem
name: Fine and Wilf theorem
aliases:
- Fine and Wilf periodicity lemma
- Fine-Wilf theorem
- periodicity lemma
area: strings/string-combinatorics
level: advanced
summary: A string with periods p and q of length at least p+q-gcd(p,q) also has period gcd(p,q).
prereqs: [string-period, greatest-common-divisor]
see_also: [primitive-word, word-conjugacy, border, maximal-repetition, christoffel-word, sturmian-word, two-way-string-matching, euclidean-algorithm]
sources:
  - paper: doi:10.1090/s0002-9939-1965-0174934-9
    title: N. J. Fine and H. S. Wilf, Uniqueness theorems for periodic functions, Proceedings of the American Mathematical Society 16(1), 1965, 109-114
    locator: Theorem 1, two periodic sequences that agree on p + q - gcd(p, q) consecutive terms agree everywhere, and the example showing the bound is best possible
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 1, Words (D. Perrin), Section 1.3, Proposition 1.3.5 (the theorem of Fine and Wilf) and the commutation of words
  - book: isbn:9780521812207
    title: M. Lothaire, Algebraic Combinatorics on Words, Encyclopedia of Mathematics and its Applications 90, Cambridge University Press, 2002
    locator: Chapter 8, Periodicity (F. Mignosi and A. Restivo), the periodicity lemma, its extremal words and its generalizations
  - paper: doi:10.1016/s0304-3975(96)00101-6
    title: Jean Berstel and Aldo de Luca, Sturmian words, Lyndon words and trees, Theoretical Computer Science 178(1-2), 1997, 171-203
    locator: central words as the words of length p + q - 2 with coprime periods p and q
  - paper: "R. C. Lyndon and M. P. Schützenberger, The equation a^M = b^N c^P in a free group, Michigan Mathematical Journal 9(4), 1962, 289-298"
    title: R. C. Lyndon and M. P. Schützenberger, The equation a^M = b^N c^P in a free group
    locator: the lemmas on commuting words and on words with two periods, used in the solution of the equation
---

The Fine and Wilf theorem, also called the periodicity lemma, says that a word with two periods $p$ and $q$ that is long enough also has the period $\gcd(p, q)$, and "long enough" means length at least $p + q - \gcd(p, q)$. This length is the best possible: shorter words can have both periods without the period $\gcd(p, q)$. The theorem is the basic tool of combinatorics on words for periodicity, and it underlies the uniqueness of [primitive roots](/primitive-word/), the structure of [runs](/maximal-repetition/), and the analysis of string matching algorithms that use periods.

## Statement

Let $\Sigma$ be an [alphabet](/alphabet/); only equality of letters is used. Indices are 0-based. For a word $w = w[0..n-1]$ and an integer $p \ge 1$, $p$ is a [period](/string-period/) of $w$ if $w[i] = w[i+p]$ for $0 \le i < n - p$. Each $p \ge n$ is a period, vacuously.

**Theorem (Fine and Wilf, 1965).** Let $w$ be a word of length $n$ with the periods $p$ and $q$, and let $d = \gcd(p, q)$. If
$$ n \ge p + q - d, $$
then $d$ is a period of $w$.

**Example.** The word `abaababaaba` of length 11 has the periods 5 and 8, and $5 + 8 - 1 = 12 > 11$, so the theorem does not apply, and indeed 1 is not a period. Adding one letter so that both periods survive forces period 1: the word would have length 12, and the theorem says it is constant, which it is not, so no letter extends `abaababaaba` keeping both periods. Two more examples:

| Periods $p, q$ | $d$ | Bound $p + q - d$ | A word of length $p + q - d - 1$ with periods $p, q$ but not $d$ |
|---|---|---|---|
| 3, 5 | 1 | 7 | `abaaba` |
| 4, 6 | 2 | 8 | `aaabaaa` |
| 3, 7 | 1 | 9 | `aabaabaa` |
| 4, 7 | 1 | 10 | `aabaaabaa` |
| 5, 8 | 1 | 12 | `abaababaaba` |

## In plain words

Suppose a word repeats every 3 letters and also every 5 letters. Moving 5 forward and then 3 back shifts by 2, and doing that again shifts by 1, so if the word is long enough to make these moves without falling off its end, every letter equals its neighbor and the word is one letter repeated. In general the two shifts combine into a shift by their greatest common divisor, like the steps of Euclid's algorithm. The theorem says exactly how long the word must be for this to work, and the examples in the table show that one letter less is not enough.

## Proof

The proof is by induction on $p + q$, following the subtractive form of the [Euclidean algorithm](/euclidean-algorithm/).

**Lemma 1 (a prefix with two periods).** Let $w$ have length $n$ and the periods $p < q$, and let $r = q - p$. Then the prefix $v = w[0..n-p-1]$, of length $n - p$, has the periods $p$ and $r$.

*Proof.* $v$ has the period $p$ because it is a factor of $w$. For the period $r$, let $0 \le i < |v| - r = n - q$. Then $i + q < n$, so $w[i] = w[i+q]$ by the period $q$. Also $0 \le i + q - p$ and $(i + q - p) + p = i + q < n$, so $w[i+q-p] = w[i+q]$ by the period $p$. Hence $v[i] = w[i] = w[i+r] = v[i+r]$, since $i + r < n - p$. $\square$

**Lemma 2 (lifting a period).** Let $w$ have length $n$ and period $p$, let $d$ divide $p$, and suppose the prefix $v = w[0..n-p-1]$ has length at least $p$ and has the period $d$. Then $w$ has the period $d$.

*Proof.* Since $w$ has the period $p$, $w[x] = w[x \bmod p]$ for each $x < n$, by repeated steps back by $p$. Since $v$ has the period $d$, $v[y] = v[y \bmod d]$ for each $y < |v|$. For $x < n$, $x \bmod p < p \le |v|$, and $d$ divides $p$, so
$$ w[x] = w[x \bmod p] = v[x \bmod p] = v[(x \bmod p) \bmod d] = w[x \bmod d]. $$
So $w[x] = w[x \bmod d] = w[(x + d) \bmod d] = w[x + d]$ for $0 \le x < n - d$. $\square$

**Proof of the theorem.** By strong induction on $p + q$. By symmetry, $p \le q$. If $p = q$, then $d = p$ is a period. Let $p < q$, $r = q - p$, and $n \ge p + q - d$. Note that $\gcd(p, r) = \gcd(p, q) = d$. By Lemma 1, $v = w[0..n-p-1]$ has the periods $p$ and $r$, and
$$ |v| = n - p \ge q - d = p + r - d. $$
Since $p + r < p + q$, the induction hypothesis gives that $v$ has the period $d$. Since $d$ divides $q - p$ and $q > p$, $q \ge p + d$, so $|v| \ge q - d \ge p$. By Lemma 2, $w$ has the period $d$. $\blacksquare$

**A graph view.** Join the positions $i$ and $i + p$, and $i$ and $i + q$, for all positions inside $[0, n)$. The words with the periods $p$ and $q$ are exactly the words that are constant on each connected component. Every component lies in one residue class modulo $d$, and the theorem says that for $n \ge p + q - d$ there are exactly $d$ components, the residue classes. For $n = p + q - d - 1$ and $p, q$ not dividing each other, there are $d + 1$ components: one residue class splits into two.

## Consequences

1. **Common powers.** If some powers of words $x$ and $y$ share a prefix of length $|x| + |y| - \gcd(|x|, |y|)$, then $x$ and $y$ are powers of a common word. *Proof.* That prefix $z$ has the periods $|x|$ and $|y|$, hence the period $d = \gcd(|x|, |y|)$, and its length is at least $\max(|x|, |y|)$. So $x$ and $y$ are prefixes of $z$ whose lengths are multiples of $d$, and both are powers of $z[0..d-1]$. $\square$
2. **Commutation.** $xy = yx$ if and only if $x$ and $y$ are powers of a common word. *Proof.* If $z = xy = yx$, then $z[i + |x|] = y[i] = z[i]$ for $i < |y|$, and $z[i + |y|] = x[i] = z[i]$ for $i < |x|$. So $z$, of length $|x| + |y|$, has the periods $|x|$ and $|y|$, and consequence 1 applies. The converse is clear. $\square$
3. **Primitive roots.** A [primitive word](/primitive-word/) $w$ occurs in $ww$ only at the indices 0 and $|w|$. *Proof.* If $w$ occurs at the index $k$ with $0 < k < |w|$, write $w = uv$ with $|u| = k$; then $ww = uvuv$ and the occurrence gives $w = vu$. So $uv = vu$, and by consequence 2, $u$ and $v$ are powers of a word $z$, and $w = z^m$ with $m \ge 2$, so $w$ is not primitive. $\square$ It follows that each nonempty word is $z^m$ for a unique primitive $z$, and that a primitive word of length $n$ has $n$ distinct [conjugates](/word-conjugacy/).
4. **Squares in runs.** If a factor of $w$ has the period $p$ and contains a primitively rooted square $uu$ with $|u| \ge p$, then $|u| = p$. *Proof.* $uu$ has the periods $m = |u|$ and $p$, and $2m \ge m + p$, so it has the period $g = \gcd(m, p)$. Then $u = (u[0..g-1])^{m/g}$, and since $u$ is primitive, $g = m$, so $m$ divides $p$ and $m = p$. $\square$ This is why a [run](/maximal-repetition/) of period $p$ generates its primitively rooted squares of half-length at least $p$ only with half-length $p$.
5. **Smallest period.** If $p$ is the smallest period of $w$ and $q$ is another period with $p + q \le |w|$, then $p$ divides $q$, since $\gcd(p, q)$ is a period and $p$ is the smallest one. String matching algorithms, such as the [two-way algorithm](/two-way-string-matching/) and the Galil-Seiferas algorithm, use this to shift a pattern by its period without missing occurrences.

## Tightness

- **One less letter.** Let $p < q$ with $p$ not dividing $q$, and $d = \gcd(p, q)$. There is a binary word of length $p + q - d - 1$ with the periods $p$ and $q$ but not the period $d$. *Proof.* By induction on $p + q$. Let $r = q - p$, so $\gcd(p, r) = d$. If $r = d$, take $w = a^{p-1} b a^{p-1}$, of length $2p - 1 = p + q - d - 1$. It has the period $p$, and the period $q = p + d$ because $w[i] = w[i + p + d] = a$ for $i < p - 1 - d$, since only $w[p-1]$ is $b$. It lacks the period $d$, since $w[p-1-d] = a \ne b = w[p-1]$, and $d < p$. If $r \ne d$, then neither of $p$ and $r$ divides the other: $p \mid r$ would give $p \mid q$, and $r \mid p$ would give $r = \gcd(p, r) = d$. By induction there is a word $v$ of length $p + r - d - 1$ with the periods $p$ and $r$ but not $d$. Extend it to $w$ of length $n = p + q - d - 1 = |v| + p$ by $w[x] = w[x - p]$ for $x \ge |v|$. Then $w$ has the period $p$, its prefix $v$ shows that it lacks the period $d$, and for $i < n - q = |v| - r$, $w[i+q] = w[i+r] = v[i+r] = v[i] = w[i]$, so $w$ has the period $q$. $\square$ The table in the statement lists such words.
- **Divisible periods.** If $p$ divides $q$, then $d = p$ is a period already, and no length condition is needed. So the bound $p + q - d$ is sharp exactly when neither period divides the other.
- **The extremal words.** For coprime $p$ and $q$, the word of length $p + q - 2$ with the periods $p$ and $q$ but not 1 is unique up to renaming the two letters, it is a palindrome, and it uses exactly two letters. These are the central words, the middle parts of the [Christoffel words](/christoffel-word/), and they are the factors of [Sturmian words](/sturmian-word/) studied by Berstel and de Luca. For $d > 1$ the other $d - 1$ residue classes are free, so the extremal words are not unique.

## History

Fine and Wilf proved the theorem in 1965 for sequences, in the form "two periodic sequences with the periods $p$ and $q$ that agree on $p + q - \gcd(p, q)$ consecutive terms agree everywhere", and gave the example that shows the bound is sharp; they also proved a version for continuous periodic functions. Lyndon and Schützenberger, in their 1962 paper on the equation $a^M = b^N c^P$ in free groups, used the commutation lemma and lemmas of the same kind on words with two periods. Lothaire's 1983 book made the theorem the standard tool of combinatorics on words, and the extremal words were later identified with the central words of Sturmian theory.

## References
