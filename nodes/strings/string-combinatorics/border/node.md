---
tag: FVBF0C
kind: definition
slug: border
name: Border of a string
aliases:
- bordered word
- proper border
area: strings/string-combinatorics
level: intro
summary: A nonempty proper prefix of a string that is also a suffix of it.
prereqs: [alphabet]
see_also: [string-period, prefix-function, knuth-morris-pratt, primitive-word, lyndon-word, fine-and-wilf-theorem, critical-factorization, palindrome]
sources:
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 1, Tools (borders and periods, the duality between them, and the border table)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 2, Section 2.3 (the Knuth-Morris-Pratt algorithm and the values sp_i, the longest proper suffix that matches a prefix)
  - paper: doi:10.1137/0206024
    title: Donald E. Knuth, James H. Morris and Vaughan R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2), 1977, 323-350
    locator: the failure function and its computation
  - paper: "Peter Tolstrup Nielsen, A note on bifix-free sequences, IEEE Transactions on Information Theory 19(5), 1973, 704-706"
    title: Peter Tolstrup Nielsen, A note on bifix-free sequences
    locator: the recurrence for the number of bifix-free (unbordered) sequences
---

A border of a string $w$ is a string $u \ne w$ that is both a prefix and a suffix of $w$. Borders are the dual of [periods](/string-period/): $w$ has a border of length $b$ if and only if it has the period $|w| - b$. The longest border of each prefix of a pattern is the [prefix function](/prefix-function/) on which [KMP](/knuth-morris-pratt/) is built, and a string without a nonempty border, an unbordered string, is the building block of [Lyndon words](/lyndon-word/) and of the [critical factorization](/critical-factorization/) theorem.

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/). Only equality tests between letters are used on this page, so the alphabet need not be ordered. Indices are 0-based: $w = w[0] \cdots w[n-1]$ and $w[i..j]$ includes both ends.

**Border.** A word $u$ is a border of $w \in \Sigma^n$ if $u \ne w$, $u$ is a prefix of $w$ and $u$ is a suffix of $w$. Equivalently, for $0 \le b < n$, the word $w[0..b-1]$ is a border if
$$ w[i] = w[n - b + i] \qquad \text{for } 0 \le i \le b - 1. $$
The empty word is a border of every nonempty word, the trivial border. The words "proper border" and "nonempty border" are used to stress $u \ne w$ and $u \ne \varepsilon$. A word with a nonempty border is **bordered**. A nonempty word whose only border is $\varepsilon$ is **unbordered** (also bifix-free or self-uncorrelated). The two occurrences of a border may overlap: `aa` is a border of `aaa`.

**The longest border.** $\mathrm{Border}(w)$ is the longest border of $w$, for $w \ne \varepsilon$. The prefix function of a string $x$ is $\pi[k] = |\mathrm{Border}(x[0..k])|$.

### Basic facts

1. **Duality with periods.** For $1 \le p \le n$, $p$ is a period of $w$ (that is, $w[i] = w[i+p]$ for $0 \le i < n - p$) if and only if $w[0..n-p-1]$ is a border. *Proof.* Put $b = n - p$. The border condition $w[i] = w[n-b+i] = w[i+p]$ for $0 \le i < b$ is the period condition for $0 \le i < n - p$. $\square$ So the longest border gives the smallest period, $\mathrm{per}(w) = n - |\mathrm{Border}(w)|$.
2. **A border of a border is a border.** If $u$ is a border of $v$ and $v$ is a border of $w$, then $u$ is a border of $w$: $u$ is a prefix of $v$, which is a prefix of $w$, and the same for suffixes. Conversely, if $u$ and $v$ are borders of $w$ with $|u| < |v|$, then $u$ is a border of $v$, because $u$ and $v$ are both prefixes of $w$, so $u$ is a prefix of $v$, and both are suffixes of $w$, so $u$ is a suffix of $v$.
3. **The border chain.** By fact 2, the borders of $w$ are exactly $\mathrm{Border}(w)$, $\mathrm{Border}(\mathrm{Border}(w))$, and so on, down to $\varepsilon$. *Proof.* Let $v = \mathrm{Border}(w)$. Each border $u$ of $w$ with $u \ne v$ is shorter than $v$, so it is a border of $v$; and each border of $v$ is a border of $w$. Induction on the length gives the chain. $\square$ This is why the prefix function lists all borders: they are $\pi[n-1]$, $\pi[\pi[n-1] - 1]$, and so on.
4. **The shortest nonempty border is unbordered and short.** If $w$ is bordered, its shortest nonempty border $u$ is unbordered, and $|u| \le |w|/2$. *Proof.* A nonempty border of $u$ would be, by fact 2, a shorter nonempty border of $w$. If $|u| > |w|/2$, the prefix and suffix occurrences of $u$ overlap in $w$, so $u$ has the period $|w| - |u| < |u|$, hence by fact 1 the nonempty border of length $2|u| - |w|$, a contradiction. $\square$
5. **Unbordered words are primitive.** If $w = z^k$ with $k \ge 2$, then $z^{k-1}$ is a nonempty border. So an unbordered word is a [primitive word](/primitive-word/). The converse fails: `aba` is primitive and bordered.
6. **The number of unbordered words.** Let $u_\sigma(n)$ be the number of unbordered words of length $n$ over $\sigma$ letters, with $u_\sigma(1) = \sigma$. Then for $n \ge 1$
$$ u_\sigma(2n+1) = \sigma\, u_\sigma(2n), \qquad u_\sigma(2n) = \sigma\, u_\sigma(2n-1) - u_\sigma(n). $$
*Proof.* By fact 4, a word is bordered if and only if it has a nonempty border of length at most half its length. For length $2n+1$, the borders of length at most $n$ do not use the middle letter $w[n]$, so $w$ is unbordered if and only if $w$ without its middle letter is unbordered, and the middle letter is free. For length $2n$, the borders of length at most $n - 1$ do not use $w[n-1]$ and $w[n]$. So the words with no nonempty border of length at most $n - 1$ number $\sigma^2 u_\sigma(2n-2) = \sigma u_\sigma(2n-1)$ (for $n = 1$ this count is $\sigma^2 = \sigma\, u_\sigma(1)$). From them remove the words with a border of length exactly $n$ and no shorter one. These are the squares $vv$ with $|v| = n$ and $v$ unbordered, because a border of $vv$ shorter than $n$ is a prefix and a suffix of $v$, and conversely. There are $u_\sigma(n)$ of them. $\square$ For $\sigma = 2$ the values for $n = 1$ to $12$ are 2, 2, 4, 6, 12, 20, 40, 74, 148, 284, 568, 1116, and for $\sigma = 3$ and $n = 1$ to $9$ they are 3, 6, 18, 48, 144, 414, 1242, 3678, 11034.

## Examples and non-examples

**Examples.**

- $w = $ `abacaba`, $n = 7$. Its nonempty borders are `a` and `aba`. So $\mathrm{Border}(w) = $ `aba`, and the periods are $7 - 3 = 4$, $7 - 1 = 6$ and $7$. The chain is `aba`, then $\mathrm{Border}($`aba`$) = $ `a`, then $\varepsilon$.
- $w = $ `aabaabaa`, $n = 8$. The borders have lengths 1, 2 and 5: `a`, `aa`, `aabaa`. The periods are 3, 6, 7 and 8. The two occurrences of `aabaa` overlap in 2 letters.
- $a^n$ has the borders $a^0, a^1, \ldots, a^{n-1}$ and every period from 1 to $n$.
- The prefix function of `abacaba` is $0, 0, 1, 0, 1, 2, 3$. Its last value is 3, the length of `aba`.

**Non-examples.**

- `ab`, `aab`, `abb` and `aabb` are unbordered. Every [Lyndon word](/lyndon-word/) of length at least 2 is unbordered.
- $w$ itself is not a border of $w$. Without this rule, every word would have the period 0.
- `abab` with the factor `ba`: the word `ba` occurs inside, but it is not a prefix, so it is not a border. A border must touch both ends.
- `abba` reversed is still `abba`, but `ab` is not a border, because the suffix of length 2 is `ba`. A border is a repeated prefix, not a mirrored one. For a [palindrome](/palindrome/), the borders are exactly its palindromic suffixes.

## Related definitions

- **[Period](/string-period/).** The dual notion of fact 1. Two periods interact by the [Fine and Wilf theorem](/fine-and-wilf-theorem/).
- **[Prefix function](/prefix-function/).** The table of the longest borders of all prefixes, computed in $O(n)$ time by the [KMP](/knuth-morris-pratt/) preprocessing.
- **[Overlap](/overlap/).** The longest suffix of one word that is a prefix of another; a border is the overlap of a word with itself.
- **[Primitive word](/primitive-word/).** Fact 5 shows that unbordered words are primitive.
- **[Lyndon word](/lyndon-word/).** A Lyndon word is unbordered, and each primitive word has an unbordered conjugate, namely its Lyndon conjugate.
- **[Critical factorization](/critical-factorization/).** The local period at a cut of a word is the length of the shortest square centered at the cut, with overhangs allowed. The critical factorization theorem says that some cut has a local period equal to the smallest period.

## References
