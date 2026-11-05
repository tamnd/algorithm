---
tag: NQK46C
kind: problem
slug: shortest-palindrome
name: Shortest palindrome
aliases:
- shortest palindrome by prepending
- palindrome by adding characters in front
area: strings/palindromes
level: core
summary: Find the shortest palindrome obtained by adding symbols to the front of a string.
model: comparison-model
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n)}
  space: {aux: Θ(n)}
prereqs: [palindrome, prefix-function]
see_also: [palindromic-closure, manacher, longest-palindromic-substring, palindrome-edit-distance, z-algorithm, knuth-morris-pratt, border, polynomial-rolling-hash]
sources:
  - paper: doi:10.1016/j.ejc.2008.04.006
    title: Amy Glen, Jacques Justin, Steve Widmer and Luca Q. Zamboni, Palindromic richness, European Journal of Combinatorics 30 (2009), 510-531
    locator: Section 2 (the right palindromic closure w(+) by the longest palindromic suffix, and Proposition 2.6)
  - paper: doi:10.1145/321892.321896
    title: Glenn Manacher, A new linear-time on-line algorithm for finding the smallest initial palindrome of a string, Journal of the ACM 22(3) (1975), 346-351
    locator: the whole paper (the online test of the prefixes of a string for being palindromes)
  - url: https://leetcode.com/problems/shortest-palindrome/
    title: LeetCode, Problem 214, Shortest Palindrome
    locator: the problem statement (add characters in front) and its two examples, aacecaaa and abcd
---

The shortest palindrome problem asks for the shortest [palindrome](/palindrome/) that can be made from a string $s$ by adding symbols in front of it. The answer is unique: write $s = p\,t$ where $p$ is the longest palindromic prefix of $s$, and the answer is $t^R\,p\,t$, of length $2n - |p|$. So the problem is to find the longest palindromic prefix, which the [prefix function](/prefix-function/) of $s\,\#\,s^R$ gives in $\Theta(n)$ time. Adding symbols at the end instead gives the right [palindromic closure](/palindromic-closure/) of combinatorics on words.

## In plain words

You have a word and you may write new letters only in front of it, until the whole thing reads the same from both ends. To write as few letters as possible, keep the longest start of the word that already reads the same from both ends. The rest of the word, after that start, has no partner yet. Copy that rest in reverse order and write the copy in front. Now every letter has a partner at the same distance from the other end. You cannot do with fewer new letters, because a shorter front part would mean a longer start that reads the same from both ends, and you took the longest one.

## Definition

**Input.** A string $s = s[0..n-1]$ over an [alphabet](/alphabet/) $\Sigma$, $n \ge 0$, with 0-based indices. Algorithms test symbols for equality only. The method with the prefix function also needs one separator symbol $\#$ that does not occur in $s$, or a sentinel value of another type.

**Output.** The shortest string $w$ such that $w = x\,s$ for some string $x$ and $w$ is a palindrome. Both odd and even palindromes are allowed; the parity of $w$ is whatever the shortest one has.

**Theorem.** Let $p = s[0..\ell - 1]$ be the longest palindromic prefix of $s$ ($\ell = 0$ only for $n = 0$) and $t = s[\ell..n-1]$. Then $t^R s$ is the unique shortest palindrome of the form $x\,s$, and its length is $2n - \ell$.

*Proof.* $t^R s = t^R\, p\, t$, and its reversal is $t^R\, p^R\, t = t^R\, p\, t$, so it is a palindrome. Now let $w = x\,s$ be any palindrome with $|x| = k \le n$. For $0 \le i \le n - k - 1$, the symbol $w[k + i] = s[i]$ has the mirror $w[n - 1 - i]$, and $n - 1 - i \ge k$, so $w[n - 1 - i] = s[n - 1 - i - k]$. So $s[i] = s[n - k - 1 - i]$ for these $i$, that is, the prefix $s[0..n-k-1]$ is a palindrome, and $n - k \le \ell$. So $k \ge n - \ell$. If $k > n$, then $w$ is longer than $t^R s$ anyway. For $k = n - \ell$, the first $k$ symbols of $w$ are the mirrors of the last $k$ symbols, which are $t$, so $x = t^R$. $\square$

## Variants

- **Add at the end.** The shortest palindrome of the form $s\,y$ is $s\,u^R$, where $s = u\,v$ and $v$ is the longest palindromic suffix of $s$. This is the right [palindromic closure](/palindromic-closure/) $s^{(+)}$ (Glen, Justin, Widmer and Zamboni, Section 2). It is the same problem for $s^R$.
- **Add at both ends.** The shortest palindrome $x\,s\,y$ adds $n - \max(\ell, \ell')$ symbols, where $\ell'$ is the length of the longest palindromic suffix. *Proof sketch.* If $|x| \le |y|$, remove $x$ and its mirror at the end of $y$; what is left is a palindrome $s\,y'$, so $|y'| \ge n - \ell'$ by the previous variant. The case $|x| \ge |y|$ is symmetric.
- **Insert anywhere.** With insertions at any position, the minimum number is $n - \mathrm{LPS}(s)$, where $\mathrm{LPS}$ is the length of the [longest palindromic subsequence](/longest-palindromic-subsequence/). See [palindrome edit distance](/palindrome-edit-distance/).
- **Every prefix, online.** For each prefix $s[0..i]$, the shortest palindrome that has it as a suffix. The answer for $s[0..i]$ uses the longest palindromic prefix of $s$ of length at most $i + 1$, and the palindromic prefixes of $s$ are found online, one symbol at a time, by Manacher's 1975 algorithm.

## Examples

| $s$ | longest palindromic prefix $p$ | $t$ | shortest palindrome $t^R s$ | added |
| --- | --- | --- | --- | --- |
| $\varepsilon$ | $\varepsilon$ | $\varepsilon$ | $\varepsilon$ | 0 |
| `a` | `a` | $\varepsilon$ | `a` | 0 |
| `ab` | `a` | `b` | `bab` | 1 |
| `aba` | `aba` | $\varepsilon$ | `aba` | 0 |
| `abab` | `aba` | `b` | `babab` | 1 |
| `abcd` | `a` | `bcd` | `dcbabcd` | 3 |
| `aacecaaa` | `aacecaa` | `a` | `aaacecaaa` | 1 |
| `abaab` | `aba` | `ab` | `baabaab` | 2 |

For `abaab` the prefix function of `abaab#baaba` ends with the value 3, the length of `aba`. Adding at the end instead gives `abaaba`, because the longest palindromic suffix of `abaab` is `baab`.

## Known algorithms

**Brute force, $\Theta(n^2)$.** Test the prefixes $s[0..j]$ for $j = n-1, n-2, \ldots$ with the two-pointer scan and stop at the first palindrome. On $a^m b\, a^{m-1}$ ($n = 2m$) the prefixes $a^m b\, a^j$ for $j = m-1, \ldots, 0$ fail, each after about $j$ comparisons, so the total is $\Theta(n^2)$.

**Prefix function, $\Theta(n)$.** A prefix $u$ of $s$ is a palindrome if and only if $u$ is also a suffix of $s^R$: if $u = u^R$, then $u^R$ is a prefix of $s$, so $u$ is a suffix of $s^R$; and conversely, if $u$ is a suffix of $s^R$, then $u^R$ and $u$ are prefixes of $s$ of the same length, so $u = u^R$. So the longest palindromic prefix is the longest string that is a prefix of $s$ and a suffix of $s^R$, which is the last value of the [prefix function](/prefix-function/) of $s\,\#\,s^R$. The separator keeps the [border](/border/) from being longer than $n$.

```pseudo id=prefix-function
SHORTEST-PALINDROME(s)                ▷ s[0 .. n − 1]
L1  u ← s · # · reverse(s)            ▷ # does not occur in s
L2  π ← PREFIX-FUNCTION(u)            ▷ π[k] = longest proper border of u[0 .. k]
L3  ℓ ← π[2n] if n ≥ 1, else 0
L4  return reverse(s[ℓ .. n − 1]) · s
```

The prefix function of a string of length $2n + 1$ takes $O(n)$ time, so the whole method is $\Theta(n)$ time and space. The same idea runs as the [Knuth-Morris-Pratt](/knuth-morris-pratt/) matcher with pattern $s$ and text $s^R$: the state at the end of the text is $\ell$.

**Z-algorithm, $\Theta(n)$.** Run the [Z-algorithm](/z-algorithm/) on $s\,\#\,s^R$. At the position of $s^R[k]$, the Z-value is the length of the longest common prefix of $s^R[k..n-1]$ and $s$. The suffix $s^R[k..n-1]$ is the reversal of the prefix $s[0..n-1-k]$, so the Z-value is $n - k$ exactly when that prefix is a palindrome. So $\ell = n - k$ for the smallest such $k$.

**Manacher's algorithm, $\Theta(n)$.** The prefix $s[0..j]$ is a palindrome if and only if $P[j+1] \ge j + 1$ in [Manacher's](/manacher/) array, so $\ell$ is the largest such $j + 1$. No separator symbol is needed.

**Rolling hashes, $O(n)$.** Keep the forward and the backward [polynomial hash](/polynomial-rolling-hash/) of each prefix and compare them; the answer is correct with high probability.

## Bounds

**Upper bound.** $\Theta(n)$ time with equality tests only.

**Lower bound.** In the comparison model with $|\Sigma| \ge 2$, an algorithm needs at least $\lfloor n/2 \rfloor$ tests on $a^n$, because the output is $s$ itself if and only if $s$ is a palindrome, and [palindrome recognition](/palindrome-recognition/) needs that many tests. The output also has length up to $2n - 1$, reached by strings whose first symbol does not occur again, such as `abcd`.

## Reductions

- **To the longest palindromic prefix.** The theorem reduces the problem to one number $\ell$, and the output is then built in $O(n)$ time.
- **To border computation.** The longest palindromic prefix is the longest border of $s\,\#\,s^R$.
- **From palindrome recognition.** $s$ is a palindrome if and only if the answer equals $s$.
- **Front and end.** Adding at the end of $s$ is adding in front of $s^R$ and reversing.

## Applications

- **Palindromic closure in combinatorics on words.** Iterating the right closure with new symbols builds the standard episturmian words, and in the binary case the standard Sturmian words, such as the prefixes `a`, `aba`, `abaaba` of the [Fibonacci word](/fibonacci-word/). See [palindromic closure](/palindromic-closure/).
- **A test of string tools.** The problem is a standard exercise for the prefix function, the Z-algorithm and Manacher's algorithm.

## References
