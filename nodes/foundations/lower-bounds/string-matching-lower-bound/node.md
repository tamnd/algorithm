---
tag: 3BD2SG
kind: theorem
slug: string-matching-lower-bound
name: String matching lower bound
aliases:
- Rivest bound
- exact pattern matching lower bound
area: foundations/lower-bounds
level: advanced
summary: Searching a text of length n for a known pattern of length m needs n - m + 1 character reads in the worst case, and about (n/m) log_sigma m on random text for most patterns.
prereqs: [string-matching, decision-tree-model, counting-argument]
see_also: [knuth-morris-pratt, boyer-moore, boyer-moore-horspool, backward-dawg-matching, naive-string-matching, adversary-argument, average-case-analysis, worst-case-analysis]
sources:
  - paper: doi:10.1137/0206048
    title: "R. L. Rivest, On the worst-case behavior of string-searching algorithms, SIAM Journal on Computing 6(4) (1977), 669-674"
    locator: the main theorem (the bound n - k + 1 for a pattern of length k, and its tightness for the pattern 00...0)
  - paper: doi:10.1137/0208029
    title: "A. C. Yao, The complexity of pattern matching for a random string, SIAM Journal on Computing 8(3) (1979), 368-387"
    locator: the main theorem on the minimum average number of characters examined
  - paper: doi:10.4230/LIPIcs.ESA.2018.45
    title: "Xiaoyu He, Neng Huang and Xiaoming Sun, On the decision tree complexity of string matching, 26th European Symposium on Algorithms (ESA 2018), LIPIcs 112, 45:1-45:13"
    locator: Section 1.1 (Theorem 3, Rivest's bound; Theorem 5, Tuza's evasive patterns; the summary of Yao's result) and Theorem 7
  - paper: doi:10.1016/j.tcs.2004.03.058
    title: "G. Navarro and K. Fredriksson, Average complexity of exact and approximate multiple string matching, Theoretical Computer Science 321(2-3) (2004), 283-290"
    locator: Section 1 (Yao's bound and its tightness by BDM) and Section 2 (the block decomposition of Yao's proof)
  - paper: doi:10.1007/bf01185427
    title: "M. Crochemore, A. Czumaj, L. Gasieniec, S. Jarominek, T. Lecroq, W. Plandowski and W. Rytter, Speeding up two string-matching algorithms, Algorithmica 12 (1994), 247-267"
    locator: the backward DAWG matching algorithm and its average-case analysis
  - paper: doi:10.1016/0304-3975(76)90053-0
    title: "R. L. Rivest and J. Vuillemin, On recognizing graph properties from adjacency matrices, Theoretical Computer Science 3(3) (1976), 371-384"
    locator: the counting argument on the leaves of a decision tree
  - paper: doi:10.1137/S0097539793245829
    title: "R. Cole, R. Hariharan, M. Paterson and U. Zwick, Tighter lower bounds on the exact complexity of string matching, SIAM Journal on Computing 24(1) (1995), 30-45"
    locator: the main results (bounds on the number of character comparisons)
  - paper: doi:10.1137/0206024
    title: "D. E. Knuth, J. H. Morris and V. R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2) (1977), 323-350"
    locator: the linear-time algorithm
  - paper: doi:10.1145/359842.359859
    title: "R. S. Boyer and J S. Moore, A fast string searching algorithm, Communications of the ACM 20(10) (1977), 762-772"
    locator: the algorithm and its behaviour on typical texts
---

The string matching lower bound says that any deterministic algorithm that looks for a known pattern of length $m$ in a text of length $n$ must read at least $n - m + 1$ characters of the text on some text, even if it only has to decide whether the pattern occurs. Rivest proved this in 1977, so no algorithm for [string matching](/string-matching/) can be sublinear in the worst case. On a random text the situation is different: Yao proved in 1979 that for almost all patterns the minimum average number of reads is $\Theta((n/m)\log_\sigma m)$, which skipping algorithms such as [Boyer-Moore](/boyer-moore/) variants and [backward DAWG matching](/backward-dawg-matching/) reach.

## Statement

**Model.** Fix an alphabet $\Sigma$ with $\sigma = |\Sigma| \ge 2$ letters and a pattern $p = p_1 \cdots p_m \in \Sigma^m$ with $m \ge 1$. The algorithm knows $p$ completely, and any work on $p$ is free. It accesses the text $T = T_1 \cdots T_n \in \Sigma^n$ only by *reads*: a read names a position $j$ and returns the letter $T_j$. The next position to read may depend on all earlier answers. The cost is the number of reads; computation between reads is free. A deterministic algorithm for texts of length $n$ is a [decision tree](/decision-tree-model/) whose inner nodes read one position and have $\sigma$ children. Let

$$
\mathrm{Occ}_{p,n}(T) = \begin{cases} 1 & \text{if } T_{i} \cdots T_{i+m-1} = p \text{ for some } i, \\ 0 & \text{otherwise,} \end{cases}
$$

and let $D_p(n)$ be the least height of a decision tree that computes $\mathrm{Occ}_{p,n}$ on $\Sigma^n$. This is the worst-case number of reads of the best deterministic algorithm.

**Theorem 1 (Rivest 1977, worst case).** For every alphabet with $\sigma \ge 2$, every pattern $p$ of length $m \ge 1$ and every $n \ge 0$,

$$
D_p(n) \ \ge\ n - m + 1 .
$$

An algorithm that reports the first occurrence, or all occurrences, also determines $\mathrm{Occ}_{p,n}(T)$. So each such algorithm reads at least $n - m + 1$ text characters on some text of length $n$.

**Theorem 2 (every text).** Let $n \ge m$. A correct algorithm that reports all occurrences of $p$ reads at least $\lfloor n/m \rfloor$ text characters on *every* text of length $n$.

**Theorem 3 (Yao 1979, average case; quoted).** Let the text be uniformly random in $\Sigma^n$, and let $c_p(n)$ be the least expected number of reads of a deterministic algorithm that finds the occurrences of $p$. Yao proved that for almost all patterns of length $m$ (a fraction of the $\sigma^m$ patterns that tends to $1$ as $m \to \infty$) and for $n > 2m$,

$$
c_p(n) = \Theta\!\left( \frac{n}{m} \log_\sigma m \right).
$$

This page proves Theorems 1 and 2 in full and gives a sketch for Theorem 3. The form of Theorem 3 is the one in which He, Huang and Sun (2018) state Yao's result.

## In plain words

Suppose you search for a word in a long text, and each letter you look at costs one unit. Rivest's theorem says that for some texts you must look at almost every letter. A clever algorithm can never skip a fixed fraction of the text on every input.

The proof counts texts. If an algorithm always stops before it looks at every letter, then each final answer covers a group of texts whose size is a multiple of the alphabet size. Then the number of texts that contain the word is a multiple of the alphabet size too. A short counting argument shows that this fails for at least one text length in every window of pattern length many consecutive lengths.

On random text the picture changes. Most letters rule out many possible places at once, and a good algorithm reads only a few letters per pattern length of text.

## Proof

### Theorem 1

Write $A(N)$ for the number of strings in $\Sigma^N$ that do not contain $p$. Then $A(0) = 1$, because $m \ge 1$.

**Lemma 1 (padding).** If $N \le n$, then $D_p(N) \le D_p(n)$.

*Proof.* Choose a letter $c \ne p_m$; it exists because $\sigma \ge 2$. Let $z = c^{\,n-N}$. For every $S \in \Sigma^N$, the string $Sz$ contains $p$ if and only if $S$ contains $p$. Indeed an occurrence of $p$ in $Sz$ that is not inside $S$ ends inside $z$, so its last letter is $c \ne p_m$, which is impossible. Now take a tree of height $D_p(n)$ for length $n$. Run it on $Sz$: answer a read of a position $j > N$ with $c$ at no cost, and answer a read of $j \le N$ by reading $S_j$. This is a tree for length $N$ with at most $D_p(n)$ reads on each path. $\square$

**Lemma 2 (leaf counting).** Let $N \ge 1$. If $D_p(N) < N$, then $\sigma$ divides $A(N)$.

*Proof.* Take a tree of height $h < N$ for $\mathrm{Occ}_{p,N}$. If a path reads a position twice, the second read has a known answer and can be removed, so assume that each path reads distinct positions. The texts that reach a leaf at depth $d$ are exactly the texts that agree with the $d$ answers on the path. There are $\sigma^{N-d}$ of them, and $N - d \ge N - h \ge 1$, so $\sigma$ divides this number. The leaves labelled $1$ split the set of texts that contain $p$ into disjoint parts. So $\sigma$ divides $\sigma^N - A(N)$, and hence $\sigma$ divides $A(N)$. $\square$

**Lemma 3 (a recurrence).** For $t \ge 1$, let $F(t)$ be the number of strings $u \in \Sigma^t$ in which $p$ occurs and every occurrence ends at position $t$. Let $J = \{ j \in \{1, \ldots, m\} : j = m \text{ or } m - j \text{ is a period of } p \}$, where $s$ is a *period* of $p$ if $p_i = p_{i+s}$ for $1 \le i \le m - s$. Then:

1. $\sigma A(t-1) = A(t) + F(t)$ for every $t \ge 1$;
2. $A(N - m) = \sum_{j \in J} F(N - m + j)$ for every $N \ge m$.

*Proof.* (1) Append one letter to each string of length $t - 1$ that avoids $p$. This gives $\sigma A(t-1)$ distinct strings of length $t$. A result either avoids $p$, or contains $p$, and then every occurrence ends at position $t$ because the first $t - 1$ letters avoid $p$. Conversely, each string that avoids $p$ and each string counted by $F(t)$ has a prefix of length $t - 1$ that avoids $p$. So the strings of length $t$ obtained are exactly those counted by $A(t)$ and $F(t)$.

(2) Let $w \in \Sigma^{N-m}$ avoid $p$, and look at $v = wp$. Let $e$ be the end of the first occurrence of $p$ in $v$. An occurrence ending at $e \le N - m$ would lie inside $w$, so $e = N - m + j$ with $1 \le j \le m$. Let $s = N - e = m - j$. If $s > 0$, the occurrences that end at $e$ and at $N$ overlap in $m - s$ positions, and comparing the letters there gives $p_i = p_{i+s}$ for $1 \le i \le m - s$. So $j \in J$. The prefix $u = v_1 \cdots v_e$ is counted by $F(e)$: it contains $p$ at its end, and an earlier occurrence would contradict the choice of $e$. Map $w$ to the pair $(j, u)$.

The map is one to one, because $v = u \, p_{m-s+1} \cdots p_m$ is determined by $(j, u)$. It is onto: let $j \in J$, $s = m - j$, and let $u$ be counted by $F(N - m + j)$. Put $v = u \, p_{m-s+1} \cdots p_m$, a string of length $N$. Its last $m$ letters equal $p$: the last $s$ letters are $p_{m-s+1} \cdots p_m$ by construction, and for the other $m - s$ letters the period $s$ gives $v_{N-m+i} = p_{i+s} = p_i$ for $1 \le i \le m - s$. The prefix $w = v_1 \cdots v_{N-m}$ avoids $p$, since an occurrence in $w$ would be an occurrence in $u$ that ends before position $N - m + j$. So the pair comes from $w$. $\square$

**Lemma 4.** For every $M \ge 0$, at least one of $A(M), A(M+1), \ldots, A(M+m-1)$ is not divisible by $\sigma$.

*Proof.* By Lemma 3(1), $F(t) \equiv -A(t) \pmod{\sigma}$ for $t \ge 1$. Put this into Lemma 3(2):

$$
A(N - m) \equiv - \sum_{j \in J} A(N - m + j) \pmod{\sigma} \qquad (N \ge m).
$$

All indices on the right lie in $\{N - m + 1, \ldots, N\}$. Suppose that $\sigma$ divides $A(M), \ldots, A(M + m - 1)$. If $M = 0$ this contradicts $A(0) = 1$. If $M \ge 1$, the congruence with $N = M + m - 1$ shows that $\sigma$ divides $A(M - 1)$. So $\sigma$ divides the $m$ values $A(M-1), \ldots, A(M+m-2)$. Repeat this step $M$ times to reach $\sigma \mid A(0) = 1$, a contradiction. $\square$

*Proof of Theorem 1.* If $n \le m - 1$, the bound is at most $0$. Let $n \ge m$ and $M = n - m + 1 \ge 1$. By Lemma 4, some $N$ with $M \le N \le n$ has $\sigma \nmid A(N)$. By Lemma 2, $D_p(N) \ge N$. By Lemma 1, $D_p(n) \ge D_p(N) \ge N \ge n - m + 1$. $\blacksquare$

The proof shows more: in every run of $m$ consecutive lengths there is a length $N$ with $D_p(N) = N$, where the best algorithm must read the whole text.

### Theorem 2

Let a correct algorithm report all occurrences on a text $T$ of length $n \ge m$, and let $R$ be the set of positions it reads on $T$. Every text that agrees with $T$ on $R$ gets the same run and the same output. Take a window $W_i = \{i, \ldots, i + m - 1\}$ with $1 \le i \le n - m + 1$.

- If the output says that $p$ occurs at $i$, then $W_i \subseteq R$. Otherwise change one unread position of $W_i$ to a different letter; the output stays, but now $p$ does not occur at $i$.
- If the output says that $p$ does not occur at $i$, then $W_i \cap R$ contains a position $j$ with $T_j \ne p_{j-i+1}$. Otherwise set the unread positions of $W_i$ to the letters of $p$; the output stays, but now $p$ occurs at $i$.

So $R$ meets every window. The $\lfloor n/m \rfloor$ windows $W_1, W_{m+1}, W_{2m+1}, \ldots$ are disjoint, so $|R| \ge \lfloor n/m \rfloor$. $\blacksquare$

### Theorem 3 (sketch)

This is a sketch of the structure of Yao's proof, in the form used by Navarro and Fredriksson (2004). It is not a complete proof.

1. *Blocks.* Cut the text into $\lfloor n/(2m-1) \rfloor$ disjoint blocks of length $2m - 1$. An algorithm for the whole text also decides, for each block, which of the $m$ windows that start in the first $m$ positions of the block are occurrences. Ignoring the windows that cross block borders only makes the problem easier.
2. *Linearity of expectation.* The blocks are independent and identically distributed, so the expected total cost is at least $\lfloor n/(2m-1) \rfloor$ times the expected cost in one block.
3. *One block.* The $m$ windows of a block are the *candidates*. A read of position $j$ with answer $b$ removes a candidate that covers $j$ exactly when the pattern letter that the candidate puts at $j$ differs from $b$. A fresh position matches a given candidate with probability $1/\sigma$, so after $t$ reads a fixed candidate survives with probability at least $\sigma^{-t}$. For a typical pattern, the letters that different candidates put at one position behave like independent letters, so one read removes only about a fraction $1 - 1/\sigma$ of the surviving candidates. Then about $\log_\sigma m$ reads are needed before no candidate survives. Yao's paper makes this precise for almost all patterns; the condition on the pattern is needed (see the example under Tightness).

## Consequences

- **No worst-case sublinear search.** For fixed $m$ and growing $n$, every deterministic algorithm reads $n - O(1)$ characters on some text. An algorithm that reads at most $\alpha n$ characters with $\alpha < 1$ on every text of every large length $n$ does not exist. [Knuth-Morris-Pratt](/knuth-morris-pratt/) reads each text character, so it makes $n$ reads, within $m - 1$ of the optimum in the worst case.
- **The skip is an average-case effect.** Boyer-Moore and its relatives skip text and read far fewer than $n$ characters on typical texts, and the $\lfloor n/m \rfloor$ bound of Theorem 2 shows that this is the least possible on *every* text for an algorithm that reports all occurrences. Yao's theorem adds the factor $\log_\sigma m$ for most patterns.
- **Average optimality.** Backward DAWG matching (Crochemore et al. 1994) reads $O((n/m)\log_\sigma m)$ characters on average for a random text and pattern, so by Theorem 3 it is optimal on average up to a constant factor. Navarro and Fredriksson state this and extend the lower bound to $r$ patterns as $\Omega((n/m)\log_\sigma(rm))$.

### Pitfalls

- **Reads, not comparisons or time.** The theorems count distinct text positions that are read. A comparison-based algorithm may compare a text letter many times; the exact number of comparisons is a different measure, studied for example by Cole, Hariharan, Paterson and Zwick (1995). The running time of any algorithm is at least the number of reads, so Theorem 1 also bounds time from below.
- **Text, not pattern.** The pattern is known in advance and reading it is free. If the pattern is part of the input, reading it costs $m$ more reads.
- **Decision, first and all.** Theorem 1 holds already for the decision problem, so it holds for all three tasks. Theorem 2 needs the algorithm to report all occurrences; a "yes" answer of the decision problem can be certified without reading a whole occurrence.
- **Deterministic algorithms.** Theorem 1 is a worst-case bound for deterministic algorithms. Theorem 3 is an average over random text with a fixed pattern, not a bound for randomized algorithms on a worst-case text.
- **Alphabet size.** Lemma 1 and Lemma 2 use $\sigma \ge 2$. For $\sigma = 1$ the problem needs no reads.

## Tightness

**Worst case.** The trivial upper bound is $D_p(n) \le n$, so for every pattern the truth lies between $n - m + 1$ and $n$. Rivest showed that the bound $n - m + 1$ is reached for the pattern $0^m$, so it cannot be improved for all patterns. The exact values of $D_p(n)$ for binary patterns and small $n$, from an exhaustive search over all decision trees, are:

| pattern | $n = 4$ | $n = 5$ | $n = 6$ | $n = 7$ | $n = 8$ |
|---|---|---|---|---|---|
| $00$ | 3 | 5 | 6 | 6 | 8 |
| $000$ | 4 | 4 | 4 | 7 | 8 |
| $0000$ | 4 | 5 | 5 | 5 | 5 |
| $001$ | 3 | 3 | 6 | 6 | 6 |
| $010$ | 3 | 5 | 6 | 7 | 8 |

The bound $n - m + 1$ is met by $00$ at $n = 4$ and $n = 7$, by $000$ at $n = 6$, by $0000$ at $n = 8$, and by $001$ at $n = 5$ and $n = 8$. The pattern $010$ needs all $n$ reads for $5 \le n \le 8$. Rivest conjectured that every pattern meets his bound for infinitely many $n$. Tuza disproved this: some patterns are *evasive*, which means $D_p(n) = n$ for all large $n$, and more than half of the binary patterns of each large length are evasive. He, Huang and Sun (2018) proved that $D_p(n) = n - (n \bmod c)$, where $c$ is the greatest common divisor of the periods of $p$, for all patterns except a fraction $O(m^5 \sigma^{-m/2})$ of them.

**Theorem 2** is tight up to a constant factor for some patterns. Let $p = a^m$ for a letter $a$, and $n \ge m$. Read positions $m, 2m, \ldots, \lfloor n/m \rfloor m$; every window contains one of them. If the letter at $km$ is not $a$, every window that covers $km$ is ruled out. If it is $a$, read to the left and to the right of $km$ until a letter other than $a$ appears or $m - 1$ letters were read on that side; this settles every window that covers $km$. On a uniformly random text, each side scan reads at most $\sigma/(\sigma - 1)$ letters on average, so the expected number of reads is at most $\lfloor n/m \rfloor\,(1 + 2/(\sigma - 1)) \le 3\lfloor n/m \rfloor$. So the factor $\log_\sigma m$ of Theorem 3 does not hold for every pattern.

**Average case.** Theorem 3 is tight for almost all patterns; backward DAWG matching meets it.

## History

Knuth, Morris and Pratt (1977) and Boyer and Moore (1977) gave the linear-time algorithms, and Boyer-Moore was known to read fewer than $n$ characters on typical texts. In the same year Rivest proved Theorem 1 and showed that it is best possible for the pattern $00 \cdots 0$. Yao (1979) found the average complexity on random text. Tuza later disproved Rivest's conjecture that every pattern meets the bound for infinitely many lengths, and He, Huang and Sun (2018) settled the decision tree complexity for almost all patterns; they also used the algebraic method of Rivest and Vuillemin (1976), first developed for graph properties, to prove that more patterns are evasive. The proof of Theorem 1 on this page counts texts modulo the alphabet size, in the spirit of the Rivest and Vuillemin counting argument.

## References
