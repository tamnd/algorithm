---
tag: SRWCJ4
kind: concept
slug: series-links
name: Series links of palindromic suffixes
aliases:
- palindromic suffix series
- series link
area: strings/palindromes
level: research
summary: Links grouping palindromic suffixes into arithmetic series, giving O(n log n) palindromic factorization.
prereqs: [palindromic-tree, border, fine-and-wilf-theorem]
see_also: [minimum-palindrome-partition, palindrome-partitioning, palindrome-partition-dp, string-period, palindrome-count-bound]
sources:
  - paper: doi:10.1016/j.jda.2014.08.001
    title: Gabriele Fici, Travis Gagie, Juha Kärkkäinen and Dominik Kempa, A subquadratic algorithm for minimum palindromic factorization, Journal of Discrete Algorithms 28 (2014), 41-48
    locator: the lemmas on the palindromic suffixes of a string (O(log n) groups with lengths in arithmetic progression) and the O(n log n) factorization algorithm
  - paper: doi:10.1007/978-3-319-07566-2_16
    title: Tomohiro I, Shiho Sugimoto, Shunsuke Inenaga, Hideo Bannai and Masayuki Takeda, Computing palindromic factorizations and palindromic covers on-line, CPM 2014, Lecture Notes in Computer Science 8486, 150-161
    locator: the grouping of the palindromic suffixes of each prefix into O(log n) groups and the on-line O(n log n) factorization
  - paper: doi:10.1016/j.ejc.2017.07.021
    title: Mikhail Rubinchik and Arseny M. Shur, EERTREE, an efficient data structure for processing palindromes in strings, European Journal of Combinatorics 68 (2018), 249-265
    locator: the section on palindromic factorization (the fields diff and series link in the eertree, and the O(n log n) dynamic program)
  - paper: doi:10.4230/LIPIcs.CPM.2017.23
    title: Kirill Borozdin, Dmitry Kosolobov, Mikhail Rubinchik and Arseny M. Shur, Palindromic length in linear time, CPM 2017, LIPIcs 78, 23:1-23:12
    locator: the preliminaries on series of palindromic suffixes, the base of the linear-time algorithm
---

Series links group the palindromic suffixes of a string into a few runs whose lengths form arithmetic progressions. In the [palindromic tree](/palindromic-tree/), each node $v$ gets the difference $\mathrm{diff}[v] = \mathrm{len}[v] - \mathrm{len}[\mathrm{link}[v]]$ and the series link $\mathrm{slink}[v]$, the first node below $v$ on the suffix-link path with another difference. A palindrome of length $\ell$ has at most $\lfloor \log_2 \ell \rfloor + 1$ series, so a dynamic program that must look at all palindromic suffixes of each prefix can work series by series. This is how [minimum palindrome partition](/minimum-palindrome-partition/) and the counting of palindromic partitions get $O(n \log n)$ time.

## In plain words

A word can end with many palindromes, one inside the other: think of `aaaaaa`, which ends with six of them. Looking at all of them at each step of a long computation is slow. But they are not random. Whenever two of them are long, the word repeats a short block, and the palindromes in that part come at equal steps, like rungs of a ladder. So the palindromes that end at a position fall into a few ladders. Each ladder is described by its top, its step and its bottom. There are only a few ladders, because each new ladder starts at less than half the length of the previous one.

## The idea

**Conventions.** Strings are indexed from 0, and $s[i..j]$ includes both ends. Symbols are only tested for equality. Palindromes may be odd or even; the suffix lists below include all nonempty palindromic suffixes.

**Palindromic suffixes are borders.** Let $u$ be a palindrome and $v$ a palindromic suffix of $u$. Then $v$, read backwards, is a prefix of $u^R = u$, so $v = v^R$ is also a prefix of $u$: $v$ is a [border](/border/) of $u$. Conversely, a border of a palindrome is a palindrome. So the palindromic suffixes of $u$ are its borders, and $|u| - |v|$ is a [period](/string-period/) of $u$.

**The upper half is one progression.** Let $p_0 = |u| - |\mathrm{link}(u)|$, the smallest period of $u$. If $v$ is a palindromic suffix with $|v| \ge |u|/2$, then $p = |u| - |v| \le |u|/2$ is a period, so $p_0 + p \le |u|$ and, by the [theorem of Fine and Wilf](/fine-and-wilf-theorem/), $\gcd(p_0, p)$ is a period; since $p_0$ is the smallest, $p_0$ divides $p$. Each multiple of $p_0$ up to $|u|/2$ is also a period, and gives a border. So the palindromic suffixes of $u$ of length at least $|u|/2$ have the lengths $|u|, |u| - p_0, |u| - 2p_0, \ldots$, down to the last one that is at least $|u|/2$.

**Series.** List the palindromic suffixes of $u$ as the suffix-link path $u = v_0, v_1, v_2, \ldots$ down to the empty string. A *series* is a maximal run of consecutive nodes with the same difference $\mathrm{diff}[v_t] = |v_t| - |v_{t+1}|$. By the previous paragraph, the first series holds all palindromic suffixes of length at least $|u|/2$, so the top of the second series is shorter than $|u|/2$. The palindromic suffixes of that top are the remaining ones, so the same argument applies to it, and the number of series of $u$ is at most $\lfloor \log_2 |u| \rfloor + 1$.

**The links.** In the palindromic tree, compute for each new node $w$:
$$ \mathrm{diff}[w] = \mathrm{len}[w] - \mathrm{len}[\mathrm{link}[w]], \qquad \mathrm{slink}[w] = \begin{cases} \mathrm{slink}[\mathrm{link}[w]] & \text{if } \mathrm{diff}[w] = \mathrm{diff}[\mathrm{link}[w]], \\ \mathrm{link}[w] & \text{otherwise.} \end{cases} $$
Both take $O(1)$ time when $w$ is made. Following series links from $\mathrm{last}$ visits the top of each series of the current longest palindromic suffix, so $O(\log n)$ steps reach the empty root.

**Use in dynamic programs.** Suppose $\mathrm{best}[i]$ is a minimum, or a sum, over the palindromic suffixes $s[j..i-1]$ of $s[0..i-1]$ of a value $\mathrm{best}[j]$. The series of $v$ with difference $d$ covers the starts $j = i - \mathrm{len}[v], i - \mathrm{len}[v] + d, \ldots, i - (\mathrm{len}[\mathrm{slink}[v]] + d)$. When $\mathrm{diff}[\mathrm{link}[v]] = d$ too, the node $\mathrm{link}[v]$ was the top of a series at position $i - d$, and that series covered exactly the same starts except the last one, $i - (\mathrm{len}[\mathrm{slink}[v]] + d)$ (Fici et al.; I et al.; Rubinchik and Shur). So a value $\mathrm{ser}[v]$ stored at that time is updated with one new term:
$$ \mathrm{ser}[v] = \mathrm{best}[i - \mathrm{len}[\mathrm{slink}[v]] - \mathrm{diff}[v]] \ \oplus\ \big(\mathrm{ser}[\mathrm{link}[v]] \text{ if } \mathrm{diff}[v] = \mathrm{diff}[\mathrm{link}[v]]\big), $$
where $\oplus$ is $\min$ or $+$. Then $\mathrm{best}[i]$ combines $\mathrm{ser}[v] + 1$, or $\mathrm{ser}[v]$, over the $O(\log n)$ series tops. The full loop is on the [minimum palindrome partition](/minimum-palindrome-partition/) page.

## Examples

| string $u$ | lengths of its palindromic suffixes | differences | series |
| --- | --- | --- | --- |
| `aaaaaa` | 6, 5, 4, 3, 2, 1 | 1, 1, 1, 1, 1, 1 | one: 6 to 1, step 1 |
| `aabaabaabaa` | 11, 8, 5, 2, 1 | 3, 3, 3, 1, 1 | two: 11, 8, 5 (step 3); 2, 1 (step 1) |
| `abaabaabaabaaba` | 15, 12, 9, 6, 3, 1 | 3, 3, 3, 3, 2, 1 | three: 15 to 6 (step 3); 3; 1 |
| `abaababaaba` | 11, 6, 3, 1 | 5, 3, 2, 1 | four, each of one element |
| `abacabaabacaba` | 14, 7, 3, 1 | 7, 4, 2, 1 | four, each of one element |

The difference of the last node is its own length, since its link is the empty string. In `aabaabaabaa` the smallest period is 3, and the suffixes of length at least $11/2$ are 11, 8 and 5, all in the first series, as the half lemma says. The prefix `abaababaaba` of the [Fibonacci word](/fibonacci-word/) has four series for length 11, and the bound $\lfloor \log_2 11 \rfloor + 1 = 4$ is reached there. In the tree of `aabaabaabaa`, $\mathrm{slink}$ goes from the node of length 11 to the node of length 2, and from there to the empty root.

## Where it is used

- **Palindromic length.** The $O(n \log n)$ algorithms for the [minimum palindrome partition](/minimum-palindrome-partition/) of Fici, Gagie, Kärkkäinen and Kempa and of I, Sugimoto, Inenaga, Bannai and Takeda, and their form with the eertree by Rubinchik and Shur. Borozdin, Kosolobov, Rubinchik and Shur build on the same series for the linear-time algorithm.
- **Counting partitions.** With sums in place of minima, the same loop counts the [palindromic partitions](/palindrome-partitioning/) of each prefix in $O(n \log n)$ time.
- **Partitions with constraints.** Partitions into an even number of palindromes, or with pieces of bounded length, keep one value per series and per class.
- **Structure of palindromes.** The half lemma bounds the number of palindromic suffixes that are long compared with the string, a tool in proofs about palindromes and periods.

## References
