---
tag: 7W7A4V
kind: algorithm
slug: galil-seiferas
name: Galil-Seiferas algorithm
aliases:
- Galil-Seiferas string matching
area: strings/exact-matching
level: advanced
summary: Linear-time matching using O(1) extra space, based on a delay-based periodicity decomposition.
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern}
  time: {worst: O(n + m), best: Θ(n), preprocessing: O(m)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [string-matching, string-period, primitive-word, fine-and-wilf-theorem, knuth-morris-pratt]
see_also: [two-way-string-matching, knuth-morris-pratt, morris-pratt, prefix-function, turbo-boyer-moore, critical-factorization, naive-string-matching]
sources:
  - paper: doi:10.1016/0022-0000(83)90002-8
    title: Zvi Galil and Joel Seiferas, Time-space-optimal string matching, Journal of Computer and System Sciences 26(3) (1983), 280-294
    locator: the algorithm, the notions of prefix period and of a perfect factorization, and the linear time bound with constant extra space
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node25.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Galil-Seiferas algorithm (definition of reach and of prefix periods with k = 4, the perfect factorization, the C code with the functions newP1, newP2, parse and search, the bound of 5n comparisons, and the example x = GCAGAGAG)
  - paper: doi:10.1145/800076.802463
    title: Zvi Galil and Joel Seiferas, Time-space-optimal string matching (preliminary report), Proceedings of the 13th ACM Symposium on Theory of Computing (1981), 106-113
    locator: the conference version of the algorithm
  - book: isbn:9780195086096
    title: Maxime Crochemore and Wojciech Rytter, Text Algorithms, Oxford University Press, 1994
    locator: the chapter on time-space optimal string matching
---

The Galil-Seiferas algorithm solves [string matching](/string-matching/) in $O(n + m)$ time with only a constant number of integer variables besides the text and the pattern. It splits the pattern as $P = uv$ so that $v$ starts with at most one highly repetitive prefix, then scans the text for $v$ from left to right, shifting either by that one period or by a fixed fraction of the matched length, and checks $u$ naively at each occurrence of $v$. It needs only equality tests between characters, so it works over any alphabet.

## In plain words

[KMP](/knuth-morris-pratt/) never reads a text letter twice, but it keeps a table as long as the word. This algorithm keeps no table at all, only a handful of counters.

The trick is a cheap rule for sliding the word: after a mismatch, slide it by about a quarter of the stretch that matched. This is safe unless the word begins with many copies of one short piece, since only then can a copy of the word hide in that stretch. If the word begins with such repeats, slide by the length of the piece instead, so the match can continue where it was.

Some words begin with two different repeating pieces, which spoils this. The algorithm first cuts off a short head of the word so that the rest begins with at most one. It searches for the rest and, on each find, checks the head letter by letter.

## The problem

The input is a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ over a general alphabet: characters are only compared for equality, never ordered or used as indices. Indices are 0-based. The output is every shift $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. Occurrences may overlap. If $m = 0$, every shift $0, \ldots, n$ is output, and if $m > n$, nothing is output.

## The algorithm

Fix an integer $k \ge 3$; Galil and Seiferas suggest $k = 4$ in practice, and the code uses it. For a string $v$ and $1 \le p \le |v|$, let $\mathrm{reach}(p)$ be the length of the longest prefix of $v$ that has [period](/string-period/) $p$. A *prefix period* of $v$ is a length $p$ such that $v[0 \ldots p-1]$ is [primitive](/primitive-word/) and $\mathrm{reach}(p) \ge kp$: $v$ starts with at least $k$ copies of a primitive word of length $p$.

A *perfect factorization* is a split $P = uv$, $u = P[0 \ldots s-1]$, $v = P[s \ldots m-1]$, such that $v$ has at most one prefix period and $|u|$ is $O(\mathrm{per}(v))$. The procedure FACTORIZE returns $s$ and two numbers $p_1, q_1$ with these properties: if $v$ has a prefix period, its length is $p_1$; $p_1 + q_1 = \mathrm{reach}(p_1)$; and $p_1$ is the smallest period of $v[0 \ldots p_1 + q_1 - 1]$. When $v$ has no prefix period, $p_1 + q_1 = |v|$ and $p_1 = \mathrm{per}(v)$.

The search keeps $p$, the current shift of $P$, and $q$, the number of characters of $v$ already known to match at text position $p + s$. After a mismatch with $q$ characters matched, it shifts by $p_1$ if $q = p_1 + q_1$, keeping $q - p_1$ matched characters, and otherwise by $\lfloor q/k \rfloor + 1$, starting again with $q = 0$.

```pseudo id=main
GALIL-SEIFERAS(T, P)                                   ▷ k = 4
L1  n ← |T|, m ← |P|
L2  if m = 0 then output 0, 1, …, n and return
L3  (s, p1, q1) ← FACTORIZE(P)                          ▷ u = P[0 .. s−1], v = P[s .. m−1]
L4  p ← 0, q ← 0                                         ▷ T[p+s .. p+s+q−1] = v[0 .. q−1]
L5  while p ≤ n − m do
L6      while s + q < m and P[s + q] = T[p + s + q] do q ← q + 1
L7      if q = m − s and P[0 .. s−1] = T[p .. p+s−1] then output p
L8      if q = p1 + q1 then p ← p + p1, q ← q − p1
L9      else p ← p + ⌊q/k⌋ + 1, q ← 0

FACTORIZE(P)
L10 s ← 0, p1 ← 1, q1 ← 0
L11 loop                                                 ▷ newP1: next candidate p1
L12     while s + p1 + q1 < m and P[s + q1] = P[s + p1 + q1] do q1 ← q1 + 1
L13     if p1 + q1 < k·p1 then                           ▷ p1 is not a prefix period
L14         if s + p1 + q1 = m then return (s, p1, q1)
L15         p1 ← p1 + ⌊q1/k⌋ + 1, q1 ← 0
L16     else                                             ▷ p1 is the shortest prefix period
L17         p2 ← q1, q2 ← 0                              ▷ newP2: look for a second one
L18         loop
L19             while p2 + q2 < k·p2 and s + p2 + q2 < m and P[s + q2] = P[s + p2 + q2] do q2 ← q2 + 1
L20             if p2 + q2 = k·p2 then exit loop          ▷ p2 is a second prefix period
L21             if s + p2 + q2 = m then return (s, p1, q1)
L22             if q2 = p1 + q1 then p2 ← p2 + p1, q2 ← q2 − p1
L23             else p2 ← p2 + ⌊q2/k⌋ + 1, q2 ← 0
L24         repeat                                       ▷ parse: drop copies of short prefix periods
L25             while s + p1 + q1 < m and P[s + q1] = P[s + p1 + q1] do q1 ← q1 + 1
L26             while p1 + q1 ≥ k·p1 do s ← s + p1, q1 ← q1 − p1
L27             if s + p1 + q1 = m then return (s, p1, q1)
L28             p1 ← p1 + ⌊q1/k⌋ + 1, q1 ← 0
L29         until p1 ≥ p2
```

The search, lines L4 to L9, is a left-to-right scan for $v$ in which $q$ plays the part of the [prefix function](/prefix-function/) value of KMP, but the next value is computed from $p_1$, $q_1$ and $k$ alone. FACTORIZE runs the same kind of scan on the pattern against itself. Lines L11 to L15 try the candidates $p_1 = 1, 2, \ldots$ for the shortest prefix period, skipping $\lfloor q_1/k \rfloor$ candidates after each failure. When one is found, lines L17 to L23 look for a second prefix period $p_2$ with the shifts of the search phase. If there is none, $v$ is good as it is. If there is one, lines L24 to L29 move $s$ to the right past copies of every prefix period shorter than $p_2$, and then FACTORIZE continues at line L11 with $p_1 \ge p_2$.

The procedures newP1, newP2, parse and search of the C code of Charras and Lecroq call each other recursively; here they are loops. Line L27 is a test that the C code does not have: in parse it stops if $v$ turns out to be entirely periodic with period $p_1$. Our tests never trigger it, but it makes the correctness proof self-contained and costs one comparison of integers.

## Example

Search for $P$ = gcagagag in $T$ = gcatcgcagagagtatacagtacg, with $n = 24$ and $m = 8$, the example of Charras and Lecroq. FACTORIZE tries $p_1 = 1, \ldots, 7$ with $q_1$ = 0, 0, 1, 0, 1, 0, 1. No candidate reaches $4p_1$, and at $p_1 = 7$, $q_1 = 1$ the scan reaches the end of $P$. So $s = 0$, $u$ is empty, $v = P$ has no prefix period, and its smallest period is $p_1 = 7$, with $p_1 + q_1 = 8$.

| shift $p$ | $q$ at start | comparisons | $q$ after the scan | output | rule | next shift |
|---|---|---|---|---|---|---|
| 0 | 0 | 4 | 3 | | L9 | 1 |
| 1, 2, 3, 4 | 0 | 1 each | 0 | | L9 | 1 each |
| 5 | 0 | 8 | 8 | 5 | L8 | 7, keeping $q = 1$ |
| 12 | 1 | 1 | 1 | | L9 | 1 |
| 13, 14, 15, 16 | 0 | 1 each | 0 | | L9 | 1 each |

The output is the single shift 5, after 21 comparisons. At $p = 12$, the text character $T[12]$ = g is known to match $P[0]$ from the previous window, so the scan starts at $P[1]$.

A pattern with two prefix periods: $P = (\text{aaaab})^4$, with $m = 20$. At $s = 0$, the candidate $p_1 = 1$ has $\mathrm{reach}(1) = 4 = 4 \cdot 1$, so a is the shortest prefix period. The search for a second one tries $p_2 = 3$ ($q_2 = 1$), then $p_2 = 4$ ($q_2 = 0$), then $p_2 = 5$, where $q_2 = 15$ and $p_2 + q_2 = 20 = 4 \cdot 5$: aaaab is a second prefix period. Line L26 then drops one a, giving $s = 1$ and $q_1 = 2$, because the rest starts with only three a's. The candidates $p_1 = 2, 3, 4$ fail with $q_1$ = 1, 0, 3, and $p_1 = 5 \ge p_2$ ends the parse. Back at line L12, $p_1 = 5$ has $q_1 = 14$, which reaches the end of $P$, and FACTORIZE returns $(1, 5, 14)$: $u$ = a and $v$ = aaab(aaaab)$^3$, which has no prefix period and smallest period 5. Searching this $P$ in $T$ = a$P$aaaabb, of length 27, outputs 1 and 6 with 30 comparisons.

## Correctness

The search outputs $p$ only after checking all of $v$ at line L6 and all of $u$ at line L7, so every output is an occurrence; the work is to show that no shift skips an occurrence of $v$. After a scan that matched $q = p_1 + q_1$ characters, an occurrence of $v$ at a distance $d < p_1$ would give $v[0 \ldots p_1 + q_1 - 1]$ the period $d$, below its smallest period $p_1$. After a scan that matched $q$ characters with $q \ne p_1 + q_1$, an occurrence at a distance $d \le q/k$ would make $v[0 \ldots q-1]$ periodic with period $d$ and length at least $kd$; its smallest period is then a prefix period, hence $p_1$, and with the [Fine and Wilf theorem](/fine-and-wilf-theorem/) the occurrence would force the mismatched text character to equal $v[q]$. The factorization has the properties used here because each skipped candidate in FACTORIZE would, by the same periodicity argument, give a prefix period shorter than the current candidate, and dropping whole copies of a primitive prefix period at line L26 cannot create a shorter one. The full proof is below.

## Complexity

- **Preprocessing.** FACTORIZE takes $O(m)$ time and $O(1)$ space; this is the main technical result of Galil and Seiferas, and Charras and Lecroq state the same bound for this code.
- **The scan of line L6.** Each successful comparison increases $q$, and $q$ only decreases at line L8, by $p_1$ while $p$ grows by $p_1$, or at line L9, by $q$ while $p$ grows by more than $q/k$. So the successful comparisons number at most $|v|$ plus $k$ times the total growth of $p$, which is at most $n$, and each window has at most one failed comparison: $O(kn)$ comparisons in total.
- **The check of line L7.** It costs at most $s$ comparisons per occurrence of $v$. Two occurrences of $v$ closer than $\mathrm{per}(v)$ would give $v$ a smaller period, so there are at most $n/\mathrm{per}(v) + 1$ of them, and in a perfect factorization $s = O(\mathrm{per}(v))$: $O(n)$ comparisons.
- **Worst case.** $O(n + m)$ time; Charras and Lecroq give at most $5n$ text character comparisons for the search with $k = 4$. The input $T = a^{1000}$, $P = a^{10}$ takes exactly 1000.
- **Best case.** The search is never sublinear. Let $r = p + s + q$ be the next text position to compare: a successful comparison raises $r$ by 1, line L8 keeps it, and line L9 raises it by at most 1. Since $r$ must pass $n - m + s$ and each window makes at least one comparison, the search makes more than $(n - m)/2$ comparisons, which is $\Theta(n)$ for $m \le n/2$.
- **Space.** Eight integers: $s, p_1, q_1, p_2, q_2, p, q$ and $k$.

| claim | value |
|---|---|
| preprocessing | $O(m)$ time, $O(1)$ space |
| search, worst case | $O(n)$, at most $5n$ comparisons for $k = 4$ |
| search, best case | more than $(n - m)/2$ comparisons |
| extra space | $O(1)$ |

The test `test_comparison_bound` checks the bound of $5n$ comparisons on all binary texts of length at most 10 and on repetitive random inputs, for $k = 3, 4, 5$.

## Properties

- **Constant extra space.** No table depends on $m$; this is the point of the algorithm. KMP and Boyer-Moore need $\Theta(m)$ words.
- **General alphabet.** Only equality tests are used, unlike the [two-way algorithm](/two-way-string-matching/), which also has constant extra space but needs an ordered alphabet to compute its critical factorization.
- **Left to right, not online.** The scan of $v$ moves forward, but after line L9 it restarts at $v[0]$, which may lie up to about $m$ positions back, and line L7 reads $u$ before $v$. A stream needs a buffer of the last $m$ characters.
- **Not sublinear.** Shifts are at most about $q/k$ or $p_1$, so it reads a constant fraction of the text, unlike [Boyer-Moore](/boyer-moore/).

## Variants and improvements

- **The constant $k$.** Any $k \ge 3$ works for correctness, as the proof below shows. A larger $k$ makes prefix periods rarer but shifts at line L9 shorter.
- **Two-way matching.** Crochemore and Perrin replaced the periodicity decomposition by a [critical factorization](/critical-factorization/) computed from two maximal suffixes. Over an ordered alphabet, the [two-way algorithm](/two-way-string-matching/) is simpler, makes at most $2n - m$ comparisons, and is the usual choice for a constant-space library routine.
- **Squares and cubes.** Crochemore and Rytter revisited time-space efficient searching through the squares and cubes that occur in the pattern ("Squares, cubes, and time-space efficient string searching", Algorithmica 13, 1995), in the same spirit as the prefix periods here.

## When to use it

Use Galil-Seiferas when the alphabet supports only equality tests, memory beyond a few integers is not available, and the worst case must be linear, for example on a small device or inside a routine that must not allocate. Over bytes or any ordered alphabet, the [two-way algorithm](/two-way-string-matching/) gives the same guarantees and is simpler and faster. If $\Theta(m)$ memory is fine, [KMP](/knuth-morris-pratt/) is easier to get right, and for long patterns over large alphabets the Boyer-Moore family is faster in practice.

## Pitfalls

- **Bounds hidden by a sentinel.** The C code reads $P[m]$, the terminating null character, to stop the loops of lines L12, L19 and L25 at the end of the pattern, and lets the scan of line L6 stop the same way. In a language without the sentinel, each loop needs the explicit test $s + \ldots < m$ shown in the pseudocode. The test `test_edges` covers patterns whose whole length is periodic, such as $a^4$ in $a^{10}$.
- **Deep recursion.** The four C procedures call each other in tail position, and the depth can grow with $m$. The implementation uses loops; the test `test_long_pattern` runs a pattern of 5000 distinct characters, which tries 5000 candidates for $p_1$.
- **Forgetting the kept prefix at line L8.** After a shift by $p_1$ the scan resumes at $v[q - p_1]$, not at $v[0]$. Resetting $q$ to 0 is still correct but breaks the linear bound on periodic text; the test `test_periodic_input_is_linear` checks exactly 1000 comparisons for $a^{10}$ in $a^{1000}$.
- **A wrong factorization.** If $v$ still has two prefix periods, the shift of line L9 can jump over an occurrence. The test `test_factorization_exhaustive` checks the three properties of the factorization on all binary words of length at most 12 and all ternary words of length at most 7, and `test_random_against_oracle` checks the search on random strings over alphabets of sizes 1, 2 and 4.

## Implementations

## History

Galil and Seiferas worked on saving space in string matching from 1977, in "Saving space in fast string-matching" (FOCS 1977, SIAM Journal on Computing 1980) and "Linear-time string-matching using only a fixed number of local storage locations" (Theoretical Computer Science, 1981). "Time-space-optimal string matching" appeared at STOC in 1981 and in the Journal of Computer and System Sciences in 1983, with linear time and constant extra space at once; the paper also shows that the algorithm can be carried out by a multihead finite automaton. Crochemore and Perrin's two-way algorithm of 1991 reached the same bounds by a different route. The compact C version with the functions newP1, newP2 and parse is from Charras and Lecroq's catalog of exact string-matching algorithms.

## References
