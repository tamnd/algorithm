---
tag: Q2W4PA
kind: theorem
slug: runs-theorem
name: Runs theorem
aliases:
- Bannai et al. runs theorem
area: strings/string-combinatorics
level: research
summary: The number of runs in any string is less than its length.
prereqs: [maximal-repetition, lyndon-word]
see_also: [computing-runs, lyndon-based-runs-computation, lyndon-array, main-lorentz-algorithm, fibonacci-word, counting-distinct-squares, fine-and-wilf-theorem, square]
sources:
  - paper: "Hideo Bannai, Tomohiro I, Shunsuke Inenaga, Yuto Nakashima, Masayuki Takeda and Kazuya Tsuruta, The \"runs\" theorem, SIAM Journal on Computing 46(5), 2017, 1501-1514"
    locator: the proof that a string of length n has fewer than n runs and that the sum of their exponents is at most 3n, by assigning Lyndon roots to runs
  - paper: "Roman Kolpakov and Gregory Kucherov, Finding maximal repetitions in a word in linear time, Proceedings of the 40th IEEE Symposium on Foundations of Computer Science (FOCS 1999), 596-604"
    locator: the linear bound on the number of runs, the linear-time algorithm, and the conjecture that a string of length n has fewer than n runs
  - paper: "Maxime Crochemore, Lucian Ilie and Liviu Tinta, The \"runs\" conjecture, Theoretical Computer Science 412(27), 2011, 2931-2941"
    locator: the explicit bound 1.029n on the number of runs before the runs theorem
---

The runs theorem says that a string of length $n$ contains fewer than $n$ runs, that is, maximal repetitions, and that the exponents of its runs sum to at most $3n$. It was conjectured by Kolpakov and Kucherov in 1999, who proved a linear bound with an unspecified constant, and proved by Bannai, I, Inenaga, Nakashima, Takeda and Tsuruta in 2015 with a short argument. The proof gives every run a set of starting positions of its Lyndon roots, under one of two opposite letter orders, and shows that these sets are disjoint and avoid position 0. The theorem bounds the output of [run computation](/computing-runs/) and the number of squares and cubes counted through runs.

## Statement

Let $\Sigma$ be an [alphabet](/alphabet/) with a total order $<_0$, and let $<_1$ be the reverse order; only comparisons of letters are used. Let $s = s[0..n-1]$ with 0-based indices. As on the [maximal repetition](/maximal-repetition/) page, a *run* of $s$ is a triple $(i, j, p)$ such that $p$ is the least period of $s[i..j]$, $j - i + 1 \ge 2p$, and the period $p$ does not extend to $s[i-1]$ or $s[j+1]$. Its exponent is $(j - i + 1)/p$. Let $\mathrm{Runs}(s)$ be the set of runs.

**Theorem (Bannai et al., 2015).** For every string $s$ of length $n \ge 1$,
$$ |\mathrm{Runs}(s)| \le n - 1 \qquad \text{and} \qquad \sum_{(i,j,p) \in \mathrm{Runs}(s)} \frac{j - i + 1}{p} \le 3n - 3 . $$

## In plain words

A run is a stretch of a string that repeats a short block at least twice in a row and cannot be stretched further with the same block. Runs can overlap and nest, and it was long unclear how many fit in one string. The theorem says there are always fewer runs than letters.

The proof gives each run its own private positions. Inside a run, each turned version of the repeated block appears at regular steps. Choose the alphabetical order, forward or backward, under which the letter just after the run loses to the letter one block earlier, and pick the places where the run's block, read from there, comes first in that order among its turned versions, skipping the first place of the run. Two runs never pick the same place, and the first letter of the string is never picked, so the count stays below the length.

## Proof

A word $w$ is a *Lyndon word* for an order $<$ if it is nonempty and strictly smaller than each of its proper nonempty suffixes; see [Lyndon word](/lyndon-word/). For an order $<_\ell$ and a position $a$, let $\lambda_\ell(a)$ be the longest prefix of $s[a..n-1]$ that is a Lyndon word for $<_\ell$; it exists since the single letter $s[a]$ is a Lyndon word.

**Choice of the order for a run.** For a run $r = (i, j, p)$ with $j < n - 1$, the letters $s[j+1]$ and $s[j+1-p]$ differ by maximality, and $\ell_r \in \{0, 1\}$ is the index with $s[j+1] <_{\ell_r} s[j+1-p]$. If $j = n - 1$, put $\ell_r = 0$. A *Lyndon root* of $r$ is a factor $s[a..a+p-1]$ with $i \le a$ and $a + p - 1 \le j$ that is a Lyndon word for $<_{\ell_r}$. Let
$$ B(r) = \{ a : i < a \text{ and } s[a..a+p-1] \text{ is a Lyndon root of } r \}. $$

**Lemma 1 (the set is not empty, and is large).** $|B(r)| \ge (j - i + 1)/p - 2$, and $B(r) \ne \emptyset$. *Proof.* The least period $p$ makes the root of $r$ a [primitive word](/primitive-word/), and the factors $s[a..a+p-1]$ for $a$ in a window of $p$ consecutive positions inside the run are its $p$ rotations. These are distinct, and a primitive word that is the least of its rotations is a Lyndon word (the characterization on the Lyndon word page), so the least rotation for $<_{\ell_r}$ is a Lyndon root. Its starting positions form one residue class modulo $p$, and the positions $a$ with $i < a \le j - p + 1$ include at least $\lfloor (j - i + 1)/p \rfloor - 1 \ge 1$ members of each residue class. $\square$

**Lemma 2 (the root is the longest Lyndon prefix).** If $a \in B(r)$ then $\lambda_{\ell_r}(a) = s[a..a+p-1]$. *Proof.* Write $\ell = \ell_r$ and $\lambda = s[a..a+p-1]$, a Lyndon prefix of $s[a..n-1]$. Let $b > a + p - 1$; we show $s[a..b]$ is not a Lyndon word. If $b \le j$, then $s[a..b]$ has period $p$, so it is $\lambda^e \lambda'$ with $e \ge 1$ and $\lambda'$ a prefix of $\lambda$. If $\lambda' \ne \varepsilon$, its proper suffix $\lambda'$ is a prefix of it, hence smaller, and if $\lambda' = \varepsilon$ then $e \ge 2$ and its proper suffix $\lambda^{e-1}$ is again a prefix. If $b > j$, then $j < n - 1$, and the proper suffix $s[a+p..b]$ agrees with $s[a..b]$ up to the letter $s[j+1]$, which faces $s[j+1-p]$; by the choice of $\ell$, $s[j+1] <_\ell s[j+1-p]$, so this suffix is smaller. (It is nonempty because $a + p - 1 \le j$.) $\square$

**Lemma 3 (one of the two orders gives a single letter).** For every position $a$, $\lambda_0(a)$ or $\lambda_1(a)$ has length 1. Moreover a Lyndon word of length at least 2 has its first letter strictly smaller than its last letter. *Proof.* In a Lyndon word $w$, every suffix $w[t..]$ is larger than $w$, so $w[t] \ge w[0]$ for all $t$; and the last letter $c$ satisfies $c > w$, which fails if $c = w[0]$ and $|w| \ge 2$, since then $c$ is a proper prefix of $w$. Now let $t$ be the first position after $a$ with $s[t] \ne s[a]$. For the order $<_\ell$ with $s[t] <_\ell s[a]$, a Lyndon prefix of $s[a..]$ cannot reach $t$, and the words $s[a]^m$ with $m \ge 2$ are not Lyndon words, so $\lambda_\ell(a) = s[a]$. If there is no such $t$, both have length 1. $\square$

**Lemma 4 (the sets are disjoint).** If $r = (i, j, p)$ and $r' = (i', j', p')$ are different runs, then $B(r) \cap B(r') = \emptyset$. *Proof.* Let $a \in B(r) \cap B(r')$.

- If $\ell_r = \ell_{r'}$, Lemma 2 gives $s[a..a+p-1] = \lambda_{\ell_r}(a) = s[a..a+p'-1]$, so $p = p'$. Both runs then contain the $p$ positions $a, \ldots, a + p - 1$, and two runs with the same period that share $p$ positions have a union with period $p$, so by maximality they are equal, a contradiction.
- If $\ell_r \ne \ell_{r'}$, Lemma 2 says the two Lyndon roots at $a$ are $\lambda_0(a)$ and $\lambda_1(a)$, and by Lemma 3 one of them has length 1; say $p = 1$. If also $p' = 1$, the two runs have the same period and share position $a$, so they are equal as before. Otherwise $p' \ge 2$. Since $a > i$ and $p = 1$, $s[a-1] = s[a]$. Since $a > i'$, the position $a - 1$ lies in $r'$, so $s[a-1] = s[a - 1 + p']$, the last letter of the root $s[a..a+p'-1]$. That root is then a Lyndon word of length at least 2 whose first and last letters are equal, which Lemma 3 excludes. $\square$

**Conclusion.** Every $B(r)$ is a nonempty subset of $\{1, \ldots, n - 1\}$, since its elements exceed $i \ge 0$, and the sets are pairwise disjoint, so $|\mathrm{Runs}(s)| \le \sum_r |B(r)| \le n - 1$. By Lemma 1, $\sum_r \bigl((j - i + 1)/p - 2\bigr) \le \sum_r |B(r)| \le n - 1$, so the exponents sum to at most $n - 1 + 2|\mathrm{Runs}(s)| \le 3n - 3$. $\blacksquare$

**Checks.** For all binary strings of length at most 18, all ternary strings of length at most 11 and all unary strings of length at most 30, a script computed the runs by brute force and verified both bounds, that each $B(r)$ is nonempty with at least $(j - i + 1)/p - 2$ elements, that each root in $B(r)$ is the longest Lyndon prefix (Lemma 2), and that the sets $B(r)$ are pairwise disjoint.

**Example.** For $s = $ `aabaabbaabaa`, with $n = 12$, the order $<_0$ is $a < b$ and $<_1$ is $b < a$.

| run $(i, j, p)$ | factor | next letter vs. one period back | $\ell_r$ | $B(r)$ | Lyndon root |
| --- | --- | --- | --- | --- | --- |
| $(0, 1, 1)$ | `aa` | `b` vs `a` | 1 | $\{1\}$ | `a` |
| $(3, 4, 1)$ | `aa` | `b` vs `a` | 1 | $\{4\}$ | `a` |
| $(5, 6, 1)$ | `bb` | `a` vs `b` | 0 | $\{6\}$ | `b` |
| $(7, 8, 1)$ | `aa` | `b` vs `a` | 1 | $\{8\}$ | `a` |
| $(10, 11, 1)$ | `aa` | end of string | 0 | $\{11\}$ | `a` |
| $(0, 5, 3)$ | `aabaab` | `b` vs `a` | 1 | $\{2\}$ | `baa` |
| $(6, 11, 3)$ | `baabaa` | end of string | 0 | $\{7\}$ | `aab` |
| $(2, 9, 4)$ | `baabbaab` | `a` vs `b` | 0 | $\{3\}$ | `aabb` |

The eight sets are disjoint subsets of $\{1, \ldots, 11\}$. This string has the largest number of runs, 8, among binary strings of length 12.

## Consequences

- **Output size of run computation.** Every algorithm that lists all runs, such as the [Lyndon-based runs computation](/lyndon-based-runs-computation/) or the Kolpakov-Kucherov algorithm, outputs fewer than $n$ triples, so their linear running time is not dominated by the output.
- **The proof is an algorithm.** The proof shows that every run is found among the pairs $(a, \lambda_\ell(a))$ for $\ell \in \{0, 1\}$: extend the longest Lyndon prefix at each position by its period in both directions and keep the maximal repetitions. The longest Lyndon prefixes for all positions form the [Lyndon array](/lyndon-array/), computable in linear time, and this gives a simple $O(n)$ runs algorithm.
- **Few runs of high exponent.** The proof gives $\sum_r (e_r - 2) \le n - 1$, where $e_r$ is the exponent of run $r$. So for every $t > 2$, at most $(n-1)/(t-2)$ runs have exponent at least $t$; for instance fewer than $n$ runs contain a cube, and fewer than $n/2$ contain a fourth power.
- **Squares through runs.** Every occurrence of a square with a primitive root of length $p$ lies in exactly one run of period $p$, and a run of period $p$ and length $L$ contains $L - 2p + 1$ such occurrences. So the runs, fewer than $n$ of them, describe all primitively rooted square occurrences compactly, which is how runs-based methods enumerate or [count distinct squares](/counting-distinct-squares/).

## Tightness

- **Small cases.** The largest number of runs of a binary string of length $n = 1, \ldots, 18$ is $0, 1, 1, 2, 2, 3, 4, 5, 5, 6, 7, 8, 8, 10, 10, 11, 12, 13$, by exhaustive search; ternary strings of length at most 11 give the same values. For example `aabaabbaabaabbaabb` has 13 runs in 18 letters.
- **The constant is below 1 but close to it.** Let $\rho(n)$ be the largest number of runs of a string of length $n$. Constructions by Matsubara and coauthors and by Simpson give $\rho(n) \ge 0.9445\,n$ for infinitely many $n$, and Fischer, Holub, I and Lewenstein improved the upper bound of the theorem to $\rho(n) \le 22n/23$. The exact limit of $\rho(n)/n$ is unknown.
- **Fibonacci words.** Fibonacci words have about $0.76\,n$ runs: the prefixes of the [Fibonacci word](/fibonacci-word/) of lengths 233, 377 and 610 have 175, 285 and 463 runs.
- **Exponent sum.** A unary string has one run, of exponent $n$, so the sum of exponents can reach $n$. Exhaustive search over binary strings of length 18 gives a largest sum of about $27.01$, near $1.5n$, so the constant 3 in the second bound is not known to be tight.

## History

Kolpakov and Kucherov (1999) showed that the number of runs is $O(n)$, gave a linear-time algorithm to compute them through the Lempel-Ziv factorization, and conjectured that it is less than $n$; they also asked about the sum of exponents. A series of papers made the constant explicit and lowered it, from $5n$ by Rytter (2006) to $1.029n$ by Crochemore, Ilie and Tinta. Bannai, I, Inenaga, Nakashima, Takeda and Tsuruta settled the conjecture in a paper first circulated in 2014 and presented at SODA 2015, with the journal version in 2017; their proof by Lyndon roots also yields the bound $3n$ on the sum of exponents and a new linear-time algorithm.

## References
