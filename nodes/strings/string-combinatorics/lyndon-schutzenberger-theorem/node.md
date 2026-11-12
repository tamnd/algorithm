---
tag: 340NN5
kind: theorem
slug: lyndon-schutzenberger-theorem
name: Chen-Fox-Lyndon factorization theorem
aliases:
- Chen-Fox-Lyndon theorem
- Lyndon factorization theorem
area: strings/string-combinatorics
level: core
summary: Every word factors uniquely as a nonincreasing sequence of Lyndon words.
prereqs: [lyndon-word, lexicographic-order]
see_also: [lyndon-factorization, duval-algorithm, witt-formula, lyndon-array, bijective-burrows-wheeler-transform, minimal-rotation, necklace, mobius-inversion]
sources:
  - paper: doi:10.2307/1970044
    title: Kuo-Tsai Chen, Ralph H. Fox and Roger C. Lyndon, Free differential calculus IV. The quotient groups of the lower central series, Annals of Mathematics 68(1), 1958, 81-95
    locator: the unique factorization of a word into a nonincreasing product of standard (Lyndon) words, used to build a basis of the free Lie algebra
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 5, Lyndon words (D. Perrin), Section 5.1 (the factorization theorem and the merge of two Lyndon words)
  - paper: doi:10.1016/0196-6774(83)90017-2
    title: Jean-Pierre Duval, Factorizing words over an ordered alphabet, Journal of Algorithms 4(4), 1983, 363-381
    locator: the statement of the factorization theorem and its linear-time computation
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1, Generating all n-tuples (prime strings and the factorization of a string into nonincreasing primes, with exercises)
---

The Chen-Fox-Lyndon theorem says that each nonempty word $w$ over an ordered alphabet can be written in exactly one way as $w = \ell_1 \ell_2 \cdots \ell_k$, where each $\ell_i$ is a [Lyndon word](/lyndon-word/) and $\ell_1 \ge \ell_2 \ge \cdots \ge \ell_k$ in [lexicographic order](/lexicographic-order/). For example, `banana` $=$ `b` $\cdot$ `an` $\cdot$ `an` $\cdot$ `a`. The factors are the "primes" of the word, and the theorem is a unique factorization result for the free monoid. The computational task of finding the factors is the [Lyndon factorization](/lyndon-factorization/) problem, solved in linear time by [Duval's algorithm](/duval-algorithm/).

## Statement

Let $\Sigma$ be a totally ordered [alphabet](/alphabet/), finite or not; only comparisons of letters are used. Indices are 0-based. Words are compared in lexicographic order: $u < v$ if $u$ is a proper prefix of $v$, or if $u$ and $v$ first differ at an index $d$ with $u[d] < v[d]$. A Lyndon word is a nonempty word that is strictly smaller than each of its proper rotations; by the suffix characterization on the [Lyndon word](/lyndon-word/) page, this holds if and only if the word is strictly smaller than each of its proper nonempty suffixes. This page uses the suffix form.

**Theorem (Chen, Fox and Lyndon, 1958).** For each $w \in \Sigma^+$ there are a unique $k \ge 1$ and unique Lyndon words $\ell_1, \ldots, \ell_k$ with
$$ w = \ell_1 \ell_2 \cdots \ell_k \quad\text{and}\quad \ell_1 \ge \ell_2 \ge \cdots \ge \ell_k. $$

This is the Lyndon factorization of $w$. Grouping equal factors, it is also written $w = m_1^{e_1} \cdots m_r^{e_r}$ with $m_1 > \cdots > m_r$ and $e_i \ge 1$.

**Example.** Over $a < b$, take $w = $ `bbababaab`. Its Lyndon factorization is `b` $\cdot$ `b` $\cdot$ `ab` $\cdot$ `ab` $\cdot$ `aab`, since `b` $=$ `b` $>$ `ab` $=$ `ab` $>$ `aab`. Other factorizations into Lyndon words exist, such as `b` $\cdot$ `b` $\cdot$ `ab` $\cdot$ `ab` $\cdot$ `a` $\cdot$ `ab`, but they are not nonincreasing: there `a` $<$ `ab`. More examples:

| $w$ | Lyndon factorization |
|---|---|
| `banana` | `b` $\cdot$ `an` $\cdot$ `an` $\cdot$ `a` |
| `cabaab` | `c` $\cdot$ `ab` $\cdot$ `aab` |
| `abcabacab` | `abc` $\cdot$ `abac` $\cdot$ `ab` |
| `abaabaabb` | `ab` $\cdot$ `aabaabb` |
| `aabaab` | `aab` $\cdot$ `aab` |
| `aabab` | `aabab` (a Lyndon word) |

## In plain words

Some words are "prime": they come strictly first in dictionary order among all the ways to cut them into two parts and swap the parts. Each single letter is prime. The theorem says that any word can be cut into prime pieces so that the pieces never get larger from left to right, and that there is only one way to do it. You can find the pieces by starting from single letters and gluing two neighbours together each time the left one is smaller; when no such pair is left, you have the answer.

## Proof

The proof uses one lemma for existence and one for uniqueness.

**Lemma 1 (merge).** If $u$ and $v$ are Lyndon words and $u < v$, then $uv$ is a Lyndon word.

*Proof.* First, $uv < v$. If $u$ is not a prefix of $v$, then $u < v$ means that they first differ at some index $d < |u|$ with $u[d] < v[d]$, so $uv < v$. If $u$ is a proper prefix of $v$, write $v = u v''$ with $v''$ nonempty. Then $v''$ is a proper suffix of the Lyndon word $v$, so $v < v''$, and therefore $uv < uv'' = v$. Now check the proper nonempty suffixes of $uv$; there are three kinds.

- The suffix $v$: $uv < v$, as shown.
- A proper suffix $v'$ of $v$: $v < v'$ since $v$ is Lyndon, so $uv < v < v'$.
- A suffix $u'v$ with $u'$ a proper nonempty suffix of $u$: $u < u'$ since $u$ is Lyndon. The word $u'$ is not a prefix of $u$, because a proper prefix of $u$ is smaller than $u$. Since $|u'| < |u|$, $u$ is not a prefix of $u'$ either, so $u$ and $u'$ first differ at an index $d < |u'|$ with $u[d] < u'[d]$. Hence $uv < u'v$.

So $uv$ is smaller than each of its proper nonempty suffixes, and it is a Lyndon word. $\square$

**Existence.** Start with the factorization of $w$ into its $|w|$ letters; each letter is a Lyndon word. While the current factorization $w = \ell_1 \cdots \ell_k$ has an index $i$ with $\ell_i < \ell_{i+1}$, replace the two factors by $\ell_i \ell_{i+1}$, which is a Lyndon word by Lemma 1. Each step lowers $k$ by one, so after at most $|w| - 1$ steps no such index is left, and then $\ell_1 \ge \cdots \ge \ell_k$.

**Lemma 2 (first factor).** If $w = \ell_1 \cdots \ell_k$ with Lyndon words $\ell_1 \ge \cdots \ge \ell_k$, then $\ell_1$ is the longest prefix of $w$ that is a Lyndon word.

*Proof.* Suppose a Lyndon prefix $p$ of $w$ is longer than $\ell_1$. Then $p = \ell_1 \cdots \ell_{i-1} \ell_i'$ for some $i \ge 2$, where $\ell_i'$ is a nonempty prefix of $\ell_i$. The word $\ell_i'$ is a proper nonempty suffix of $p$, so $p < \ell_i'$, because $p$ is Lyndon. A prefix is never larger than the word, so $\ell_i' \le \ell_i$. Next, $\ell_i \le \ell_1$ by the order of the factors, and $\ell_1 \le p$ because $\ell_1$ is a prefix of $p$. Together, $p < \ell_i' \le \ell_i \le \ell_1 \le p$, a contradiction. $\square$

**Uniqueness.** By induction on $|w|$. Let $w = \ell_1 \cdots \ell_k = \ell_1' \cdots \ell_{k'}'$ be two nonincreasing factorizations into Lyndon words. By Lemma 2, $\ell_1$ and $\ell_1'$ are both the longest Lyndon prefix of $w$, so $\ell_1 = \ell_1'$. If $\ell_1 = w$, then $k = k' = 1$. Otherwise the rest $w' = \ell_2 \cdots \ell_k = \ell_2' \cdots \ell_{k'}'$ is a shorter nonempty word with two nonincreasing factorizations, so $k = k'$ and $\ell_i = \ell_i'$ for every $i$ by the induction hypothesis. $\blacksquare$

## Consequences

1. **Greedy description.** By Lemma 2, $\ell_1$ is the longest Lyndon prefix of $w$, $\ell_2$ the longest Lyndon prefix of the rest, and so on. This gives a direct quadratic algorithm, and Duval's algorithm finds the same factors in linear time.
2. **Last factor.** $\ell_k$ is the lexicographically least nonempty suffix of $w$. *Proof.* A nonempty suffix $z$ of $w$ is $\ell_i' \ell_{i+1} \cdots \ell_k$ with $\ell_i'$ a nonempty suffix of $\ell_i$. Then $\ell_i' \ge \ell_i \ge \ell_k$, with $\ell_i' > \ell_i$ when $\ell_i'$ is a proper suffix. If $\ell_k$ is a prefix of $\ell_i'$, then $\ell_k$ is a prefix of $z$ and $z \ge \ell_k$. Otherwise $\ell_i'$ is not a proper prefix of $\ell_k$, since that would make $\ell_i' < \ell_k$, so the two words first differ at an index inside $\ell_i'$, where $\ell_i'$ has the larger letter, and $z > \ell_k$. $\square$
3. **Lyndon test.** $w$ is a Lyndon word if and only if $k = 1$. In particular, by the merge lemma and its converse, for Lyndon words $u$ and $v$, $uv$ is a Lyndon word if and only if $u < v$: if $u \ge v$, then $u \cdot v$ is already a nonincreasing factorization with two factors.
4. **Counting Lyndon words.** A nonincreasing sequence of Lyndon words is the same as a finite multiset of Lyndon words, so the theorem gives a bijection between $\Sigma^n$ and the multisets of Lyndon words of total length $n$. For $|\Sigma| = \sigma$ and $L_\sigma(m)$ Lyndon words of length $m$, this reads
$$ \frac{1}{1 - \sigma z} = \prod_{m \ge 1} \left(\frac{1}{1 - z^m}\right)^{L_\sigma(m)}. $$
Taking logarithms and comparing the coefficients of $z^n$ gives $\sigma^n = \sum_{d \mid n} d\,L_\sigma(d)$, and [Möbius inversion](/mobius-inversion/) gives the [Witt formula](/witt-formula/) $L_\sigma(n) = \frac{1}{n} \sum_{d \mid n} \mu(d)\,\sigma^{n/d}$. For $\sigma = 2$ the values for $n = 1, \ldots, 12$ are 2, 1, 2, 3, 6, 9, 18, 30, 56, 99, 186, 335, and for $\sigma = 3$ and $n = 1, \ldots, 8$ they are 3, 3, 8, 18, 48, 116, 312, 810.
5. **Least rotation.** The least rotation of a word $s$ starts at the start of the last Lyndon factor of $ss$ that begins in the first copy, at an index below $|s|$, which gives a way to compute [minimal rotations](/minimal-rotation/) from the factorization.
6. **Data structures and transforms.** The factorization is the base of the [Lyndon array](/lyndon-array/), of the Lyndon-based proof of the [runs theorem](/runs-theorem/), and of the [bijective Burrows-Wheeler transform](/bijective-burrows-wheeler-transform/), which sorts the rotations of the Lyndon factors.

## Tightness

Each hypothesis is needed.

- **The order condition.** Without it, factorizations into Lyndon words are not unique: `ab` $=$ `a` $\cdot$ `b`, and `ab` is itself Lyndon; only the second is nonincreasing.
- **Nonincreasing, not decreasing.** With strict decrease, existence fails: `aa` has only the factorization `a` $\cdot$ `a`, because `aa` is not a Lyndon word.
- **Nonincreasing, not nondecreasing.** A nondecreasing factorization into Lyndon words need not exist: `ba` is not a Lyndon word, and `b` $\cdot$ `a` is decreasing.
- **The lexicographic order.** The theorem depends on the order: over $b < a$, the word `ab` factors as `a` $\cdot$ `b`, and over $a < b$ it is one factor. Each total order on $\Sigma$ gives its own factorization.

## History

Lyndon studied the words now named after him in 1954, under the name standard lexicographic sequences, in work on the lower central series of free groups; Shirshov studied them independently as regular words. Chen, Fox and Lyndon proved the unique factorization in 1958, in their work on free differential calculus, and used the words to build a basis of the free Lie algebra. Schützenberger developed the same factorization in the setting of factorizations of free monoids, and the theorem is sometimes given with his name; the result usually called the Lyndon-Schützenberger theorem is a different one, on word equations: $uv = vu$ holds exactly when $u$ and $v$ are powers of a common word, and $xz = zy$ with $x \ne \varepsilon$ exactly when $x = pq$, $y = qp$ and $z = (pq)^r p$. This page keeps the slug of the catalog, but states the factorization theorem. Duval gave the linear-time algorithm in 1983.

## References
