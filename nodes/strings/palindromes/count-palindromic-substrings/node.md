---
tag: C1HGK0
kind: problem
slug: count-palindromic-substrings
name: Counting palindromic substrings
aliases:
- number of palindromic substrings
- palindromic substring count
area: strings/palindromes
level: core
summary: Count the palindromic substrings of a string, either by occurrence or as distinct strings.
model: comparison-model
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n)}
  space: {aux: Θ(n)}
prereqs: [palindrome, manacher]
see_also: [palindrome-count-bound, palindromic-tree, longest-palindromic-substring, palindrome-substring-queries, rich-string, count-distinct-substrings, longest-palindromic-subsequence]
sources:
  - paper: doi:10.1145/321892.321896
    title: Glenn Manacher, A new linear-time on-line algorithm for finding the smallest initial palindrome of a string, Journal of the ACM 22(3) (1975), 346-351
    locator: the whole paper (the linear scan over centers)
  - paper: doi:10.1016/j.ipl.2010.07.018
    title: Richard Groult, Élise Prieur and Gwénaël Richomme, Counting distinct palindromes in a word in linear time, Information Processing Letters 110(20) (2010), 908-912
    locator: the main algorithm (maximal palindromes combined with the longest previous factor array) and the linear-time test of richness
  - paper: doi:10.1016/j.ejc.2017.07.021
    title: Mikhail Rubinchik and Arseny M. Shur, EERTREE, an efficient data structure for processing palindromes in strings, European Journal of Combinatorics 68 (2018), 249-265
    locator: the construction of the eertree and its applications to counting palindromes (distinct palindromes and occurrences of palindromes)
  - paper: doi:10.1007/978-3-319-67428-5_25
    title: Mikhail Rubinchik and Arseny M. Shur, Counting palindromes in substrings, SPIRE 2017, Lecture Notes in Computer Science 10508, 290-303
    locator: the main result (the number of distinct palindromes in a query substring)
---

Counting palindromic substrings asks how many substrings of a string are [palindromes](/palindrome/). There are two different counts. The number of *occurrences*, pairs $(i, j)$ with $s[i..j]$ a palindrome, lies between $n$ and $n(n+1)/2$ and is computed in $O(n)$ time from [Manacher's algorithm](/manacher/). The number of *distinct* palindromes is at most $n$, by the [palindrome count bound](/palindrome-count-bound/), and is computed in $O(n)$ time with the [palindromic tree](/palindromic-tree/).

## In plain words

Take a string and look at every unbroken piece of it. Some pieces read the same from both ends. You can count them in two ways. In the first way, you count each piece at each place where it appears, so the piece `a` in `banana` counts three times. In the second way, you count each different piece one time only. The first number can be very large: in a string of only `a` letters every piece counts. The second number is never more than the number of letters. Both numbers can be found in one pass over the string with the right method.

## Definition

**Input.** A string $s = s[0..n-1]$ over an [alphabet](/alphabet/) $\Sigma$, $n \ge 0$, with 0-based indices. Algorithms only test symbols for equality, except where a method says otherwise.

**Output, occurrence count.** The number
$$ N_{\mathrm{occ}}(s) = \big|\{(i, j) : 0 \le i \le j \le n - 1,\ s[i..j] \text{ is a palindrome}\}\big|. $$

**Output, distinct count.** The number $N_{\mathrm{dist}}(s)$ of distinct nonempty strings $u$ that are palindromes and occur in $s$.

Both counts include odd and even palindromes and exclude the empty string. On the [palindrome count bound](/palindrome-count-bound/) page the empty string is counted, which adds 1. A page or a program must say which of the two counts it means.

## Variants

- **For each prefix, online.** After each appended symbol, report the number of palindromes that end at the last position, or the distinct count so far. The [palindromic tree](/palindromic-tree/) gives both in $O(1)$ amortized time per symbol for a constant-size alphabet.
- **In a substring.** Many queries "how many palindromes, or distinct palindromes, occur in $s[i..j]$?". Rubinchik and Shur (2017) answer the distinct version in $O(\log n)$ time per query after $O(n \log n)$ preprocessing. See [palindrome substring queries](/palindrome-substring-queries/).
- **Palindromic subsequences.** Count the index sets, not the intervals, whose symbols form a palindrome. This is a different problem with an $O(n^2)$ interval dynamic program, like the one of the [longest palindromic subsequence](/longest-palindromic-subsequence/).
- **Pairs and products.** Count pairs of non-overlapping palindromic occurrences, or count palindromes by length. With the arrays "number of palindromes that start at $i$" and "that end at $j$", which follow from Manacher's array by difference arrays in $O(n)$ time, such counts take $O(n)$ more time.
- **Richness test.** A string $s$ is [rich](/rich-string/) if and only if $N_{\mathrm{dist}}(s) = n$. Groult, Prieur and Richomme note that their linear-time count gives a linear-time test of richness.

## Examples

| $s$ | $n$ | $N_{\mathrm{occ}}$ | $N_{\mathrm{dist}}$ | distinct palindromes |
| --- | --- | --- | --- | --- |
| $\varepsilon$ | 0 | 0 | 0 | none |
| `abc` | 3 | 3 | 3 | `a`, `b`, `c` |
| `aaa` | 3 | 6 | 3 | `a`, `aa`, `aaa` |
| `abba` | 4 | 6 | 4 | `a`, `b`, `bb`, `abba` |
| `abaab` | 5 | 8 | 5 | `a`, `b`, `aa`, `aba`, `baab` |
| `banana` | 6 | 10 | 6 | `a`, `b`, `n`, `ana`, `nan`, `anana` |
| `abacaba` | 7 | 12 | 7 | `a`, `b`, `c`, `aba`, `aca`, `bacab`, `abacaba` |

For `abaab`, Manacher's array is $P = [0, 1, 0, 3, 0, 1, 4, 1, 0, 1, 0]$, and $\sum_c \lceil P[c]/2 \rceil = 1 + 2 + 1 + 2 + 1 + 1 = 8$. The center $c = 6$, the gap between the two `a`, holds `aa` and `baab`.

## Known algorithms

**Brute force, $\Theta(n^3)$.** Test each of the $n(n+1)/2$ substrings with the two-pointer scan. For the distinct count, put the palindromes in a [hash table](/hash-table/), which costs $\Theta(n^3)$ more symbol work in the worst case.

**Interval table, $\Theta(n^2)$.** Fill $\mathrm{pal}(i, j) = (s[i] = s[j]) \wedge \mathrm{pal}(i+1, j-1)$ by increasing length, as on the [longest palindromic substring](/longest-palindromic-substring/) page, and count the true entries.

**Expand around the centers, $O(n + N_{\mathrm{occ}})$.** From each of the $2n - 1$ centers inside the string, step outward while the two symbols match. Each successful step finds one more palindromic occurrence, and each center has at most one failed step. So the time is output-sensitive: $O(n)$ when the count is small and $\Theta(n^2)$ on $a^n$.

**Manacher's algorithm, $\Theta(n)$ for the occurrence count.** The palindromes with center $c$ are nested and their lengths in $s$ are $P[c], P[c] - 2, \ldots$, down to 1 or 2. So center $c$ holds exactly $\lceil P[c]/2 \rceil$ nonempty palindromes.

```pseudo id=count
COUNT-PALINDROMIC-OCCURRENCES(s)
L1  P ← MANACHER(s)                 ▷ P[0 .. 2n], radii on # s[0] # ... # s[n − 1] #
L2  total ← 0
L3  for c ← 0 to 2n do
L4      total ← total + ⌈P[c] / 2⌉
L5  return total
```

*Correctness.* Each palindromic occurrence $s[i..j]$ has exactly one center $c = i + j + 1$, and it is counted at that center because $j - i + 1 \le P[c]$ and $j - i + 1 \equiv P[c] \pmod 2$. *Cost.* $O(n)$ time after Manacher's algorithm, which is also $O(n)$.

**Palindromic tree, $O(n)$ for both counts.** The [palindromic tree](/palindromic-tree/) has one node per distinct palindrome plus two roots, so $N_{\mathrm{dist}}(s)$ is its number of nodes minus 2. For the occurrence count, store at each node the number of palindromic suffixes of its palindrome, which is one more than the value at its suffix link; adding $s[i]$ moves to the node of the longest palindromic suffix of $s[0..i]$, and the stored value is the number of palindromes that end at $i$. The sum over $i$ is $N_{\mathrm{occ}}(s)$. The build takes $O(n)$ time for a constant-size alphabet, or $O(n \log \sigma)$ with sorted child maps.

**Maximal palindromes and previous factors, $O(n)$ for the distinct count.** Groult, Prieur and Richomme (2010) count the distinct palindromes from the maximal palindromes and the longest previous factor array, in linear time for a constant-size alphabet.

## Bounds

**Range of the occurrence count.** For $n \ge 1$, $n \le N_{\mathrm{occ}}(s) \le n(n+1)/2$. The lower bound counts the single symbols, and it is reached by `abcabc` $\cdots$ over three letters, which has no palindrome of length 2 or 3 and so none longer than 1. The upper bound is reached only by $a^n$: if every substring is a palindrome, each pair $s[i]s[i+1]$ is one, so all symbols are equal.

**Binary strings.** Over two letters, $N_{\mathrm{occ}}(s) \ge 2n - 2$ for $n \ge 2$, and the prefixes of `aababb` `aababb` $\cdots$ of length $n \ge 3$ reach this value. *Proof.* Write $s$ as blocks of equal symbols, $s = x_1^{k_1} x_2^{k_2} \cdots x_t^{k_t}$ with $x_q \ne x_{q+1}$ and $k_1 + \cdots + k_t = n$. A block of length $k$ holds $k(k+1)/2 \ge 2k - 1$ palindromic occurrences. Each inner block $x_q^{k_q}$ with $2 \le q \le t - 1$ also gives the palindrome $x_{q-1}\, x_q^{k_q}\, x_{q+1}$, because over two letters $x_{q-1} = x_{q+1}$. These occurrences are all different, so for $t \ge 2$ the total is at least $\sum_q (2k_q - 1) + (t - 2) = 2n - 2$. For $t = 1$ the total is $n(n+1)/2 \ge 2n - 2$. $\square$

**Distinct count.** $N_{\mathrm{dist}}(s) \le n$ by the [palindrome count bound](/palindrome-count-bound/), with equality exactly for [rich strings](/rich-string/), and $N_{\mathrm{dist}}(s) \ge$ the number of different symbols in $s$.

**Time.** For $n \ge 2$ and $|\Sigma| \ge 2$, the occurrence count needs at least $\lceil n/2 \rceil$ equality tests in the comparison model. *Proof.* If the algorithm never tests position $k$ on the input $a^n$, then on the input with $s[k] = b$ every test gets the same answer, so the output is the same. But $a^n$ is the only string of length $n$ with $n(n+1)/2$ palindromic occurrences, so the output is wrong for one of the two inputs. So each position is in some test, and a test covers two positions. $\square$ The linear algorithms above reach the order $\Theta(n)$. The input $a^n$ does not work for the distinct count, because $a^k b a^{n-1-k}$ also has $n$ distinct palindromes.

## Reductions

- **To Manacher's array.** The occurrence count is a sum over the $2n + 1$ radii, as in the block above.
- **To the palindromic tree.** The distinct count is a node count, and the occurrence count is a sum of suffix-link depths.
- **To counts by position.** The number of palindromes that start at each $i$ and that end at each $j$ follows from Manacher's array: center $c$ adds 1 to each start in an interval of starts, which a difference array records in $O(1)$ per center. Counts of pairs of disjoint palindromes reduce to these two arrays.

## Applications

- **Richness of words.** The distinct count tests whether a word is [rich](/rich-string/) and computes its palindromic defect $n - N_{\mathrm{dist}}(s)$.
- **Combinatorics on words.** Palindromic complexity, the number of distinct palindromes of each length, is a standard measure of infinite words such as the [Fibonacci word](/fibonacci-word/).
- **Programming tasks.** Counting palindromic substrings, and pairs of disjoint ones, are standard exercises for Manacher's algorithm and the palindromic tree.

## References
