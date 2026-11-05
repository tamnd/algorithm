---
tag: AYZPG2
kind: definition
slug: maximal-repetition
name: Maximal repetition (run)
aliases:
- run
- maximal periodic substring
area: strings/string-combinatorics
level: core
summary: A maximal substring with minimal period p whose length is at least 2p.
prereqs: [square]
see_also: [runs-theorem, computing-runs, lyndon-based-runs-computation, main-lorentz-algorithm, string-period, fine-and-wilf-theorem, fibonacci-word, cube]
sources:
  - paper: doi:10.1109/sffcs.1999.814634
    title: Roman Kolpakov and Gregory Kucherov, Finding maximal repetitions in a word in linear time, 40th Annual Symposium on Foundations of Computer Science (FOCS 1999), 596-604
    locator: the definition of maximal repetitions, the linear bound on their number, and their computation in linear time
  - paper: doi:10.1137/15M1011032
    title: Hideo Bannai, Tomohiro I, Shunsuke Inenaga, Yuto Nakashima, Masayuki Takeda and Kazuya Tsuruta, The "Runs" Theorem, SIAM Journal on Computing 46(5), 2017, 1501-1514
    locator: the number of runs is less than n and the sum of their exponents is at most 3n, through Lyndon roots
  - paper: doi:10.1016/0166-218x(89)90051-6
    title: Michael G. Main, Detecting leftmost maximal periodicities, Discrete Applied Mathematics 25(1-2), 1989, 145-153
    locator: maximal periodicities (runs) and the leftmost occurrence of each, found from the Lempel-Ziv factorization
  - paper: doi:10.1016/j.jcss.2007.09.003
    title: Maxime Crochemore and Lucian Ilie, Maximal repetitions in strings, Journal of Computer and System Sciences 74(5), 2008, 796-807
    locator: the properties of runs used to bound their number, and computer bounds on the number of runs
---

A maximal repetition, or run, of a word is a factor $s[i..j]$ whose smallest period $p$ satisfies $j - i + 1 \ge 2p$, and that cannot be extended by one letter to the left or to the right without losing the period $p$. For example, `aabaabaa` has four runs: the whole word with period 3, and `aa` at indices 0, 3 and 6 with period 1. Runs hold all the repetitions of a word: every [square](/square/) $uu$ with $u$ primitive lies in exactly one run of period $|u|$. A word of length $n$ has fewer than $n$ runs, by the [runs theorem](/runs-theorem/), and they can all be [computed in linear time](/computing-runs/).

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/); only equality of letters is used. Let $s = s[0..n-1]$, with 0-based indices. A positive integer $p$ is a [period](/string-period/) of a word $x$ if $x[t] = x[t + p]$ for $0 \le t < |x| - p$; $\mathrm{per}(x)$ is the smallest period.

**Run.** A run of $s$ is a triple $(i, j, p)$ with $0 \le i \le j < n$ such that

1. $p = \mathrm{per}(s[i..j])$ and $j - i + 1 \ge 2p$;
2. $i = 0$ or $s[i-1] \ne s[i-1+p]$ (no extension to the left);
3. $j = n - 1$ or $s[j+1] \ne s[j+1-p]$ (no extension to the right).

The exponent of the run is $(j - i + 1)/p \ge 2$. Its root is any factor of length $p$ of it, for instance $s[i..i+p-1]$; the root is a [primitive word](/primitive-word/). A Lyndon root is a factor of length $p$ of the run that is a Lyndon word, for a fixed order on $\Sigma$.

**Runs and repetitions.** A repetition is a factor of exponent at least 2. A run is a repetition that is maximal both as an interval with the period $p$ and with $p$ smallest; the set of runs of $s$ is written $\mathrm{Runs}(s)$.

### Basic facts

1. **Every repetition extends to a unique run.** Let $s[a..b]$ have the smallest period $q$ and length at least $2q$. Extend it to the left and to the right while the period $q$ is kept; the result is a factor $s[i..j]$ with period $q$ that cannot be extended. Its smallest period is $q$: a smaller period $q' < q$ of $s[i..j]$ would also be a period of $s[a..b]$. So $(i, j, q)$ is a run, and it is the only run of period $q$ that contains $s[a..b]$.
2. **Primitively rooted squares.** If $uu$ occurs at index $a$ with $u$ primitive, then $\mathrm{per}(uu) = |u|$, so by fact 1 it lies in exactly one run, of period $|u|$. *Proof that $\mathrm{per}(uu) = |u|$.* If $uu$ had a period $q < |u|$, then $uu$ would have the periods $q$ and $|u|$ with $q + |u| \le 2|u|$, and by the [Fine and Wilf theorem](/fine-and-wilf-theorem/) the period $\gcd(q, |u|)$, a proper divisor of $|u|$; then $u$ would be a power of a shorter word, against primitivity. $\square$
3. **Same period, small overlap.** Two different runs with the same period $p$ share fewer than $p$ positions. If they shared at least $p$ consecutive positions, their union would have period $p$, and neither would be maximal.
4. **Number.** A word of length $n$ has fewer than $n$ runs, and the sum of the exponents of its runs is at most $3n$ ([runs theorem](/runs-theorem/), Bannai et al.). Kolpakov and Kucherov had proved a bound of $cn$ for some constant $c$.
5. **Counting all squares and cubes.** A run of period $p$ and length $L$ contains $L - 2p + 1$ occurrences of primitively rooted squares of period $p$, and every primitively rooted square occurrence of $s$ is counted once this way, by fact 2. The same holds for cubes, with the runs of exponent at least 3.

## Examples and non-examples

| $s$ | runs $(i, j, p)$ | sum of exponents |
|---|---|---|
| `aabaabaa` | $(0, 7, 3)$, $(0, 1, 1)$, $(3, 4, 1)$, $(6, 7, 1)$ | $8/3 + 2 + 2 + 2 = 26/3$ |
| `abaababa` | $(0, 5, 3)$, $(2, 3, 1)$, $(3, 7, 2)$ | $2 + 2 + 5/2 = 13/2$ |
| `mississippi` | $(1, 7, 3)$, $(2, 3, 1)$, $(5, 6, 1)$, $(8, 9, 1)$ | $7/3 + 2 + 2 + 2 = 25/3$ |
| `banana` | $(1, 5, 2)$ | $5/2$ |
| `abcabcab` | $(0, 7, 3)$ | $8/3$ |
| `aaaa` | $(0, 3, 1)$ | $4$ |

In `mississippi` the run $(1, 7, 3)$ is `ississi`, of period 3 and exponent $7/3$; it contains $7 - 6 + 1 = 2$ squares of period 3, `ississ` and `ssissi`.

**Maximum number of runs.** The largest number of runs of a binary word of length $n$, for $n = 1, \ldots, 20$, is 0, 1, 1, 2, 2, 3, 4, 5, 5, 6, 7, 8, 8, 10, 10, 11, 12, 13, 14, 15, reached for example by `aabaabbaabaabbaabb` with 13 runs at $n = 18$. For $n \le 12$, three letters do not give more runs than two.

**Non-examples.**

- `abaab` has no run of period 3: its smallest period is 3 but its length 5 is less than 6. Its only run is `aa`, $(2, 3, 1)$.
- In `aabaabaa`, the factor `aabaab` $= (aab)^2$ is a square, but not a run: it extends to the right with period 3 to the whole word.
- In `aaaa`, the factor `aaaa` has period 2, but $(0, 3, 2)$ is not a run, since the smallest period is 1.
- A word with no square, such as `abcacb`, has no run.

## Related definitions

- **[Square](/square/) and [cube](/cube/).** The repetitions of exponent 2 and 3; each primitively rooted one lies in a unique run (facts 2 and 5).
- **[Runs theorem](/runs-theorem/).** Fewer than $n$ runs and exponent sum at most $3n$, proved by assigning to each run a Lyndon root that starts at a distinct position.
- **[Computing runs](/computing-runs/).** The problem of listing all runs; it is solved in $O(n)$ time by the [Lyndon-based algorithm](/lyndon-based-runs-computation/) or by Kolpakov and Kucherov's method based on the Lempel-Ziv factorization, and in $O(n \log n)$ time by the [Main-Lorentz](/main-lorentz-algorithm/) divide and conquer.
- **[Fibonacci word](/fibonacci-word/).** The Fibonacci word $f_n$ has $2|f_{n-2}| - 3$ runs for $n \ge 3$, so the ratio of runs to length tends to $2/\varphi^2 \approx 0.76$.
- **Critical exponent.** The supremum of the exponents of the runs of an infinite word; see the [repetition threshold](/repetition-threshold/).

## References
