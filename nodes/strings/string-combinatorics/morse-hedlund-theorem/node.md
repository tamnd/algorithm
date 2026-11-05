---
tag: Y9HEJW
kind: theorem
slug: morse-hedlund-theorem
name: Morse-Hedlund theorem
aliases:
- Morse-Hedlund ultimate periodicity theorem
area: strings/string-combinatorics
level: advanced
summary: An infinite word with subword complexity at most n for some n is ultimately periodic.
prereqs: [subword-complexity, string-period]
see_also: [sturmian-word, sturmian-characterization, fibonacci-word, thue-morse-word, morphic-word, fine-and-wilf-theorem, abelian-complexity, de-bruijn-graph]
sources:
  - paper: doi:10.2307/2371264
    title: Marston Morse and Gustav A. Hedlund, Symbolic dynamics, American Journal of Mathematics 60(4), 1938, 815-866
    locator: the theorem that a sequence with at most n distinct blocks of some length n is periodic, and the minimal block growth n + 1
  - paper: "Ethan M. Coven and Gustav A. Hedlund, Sequences with minimal block growth, Mathematical Systems Theory 7, 1973, 138-153"
    locator: the characterization of ultimately periodic sequences by block growth and the study of sequences with exactly n + 1 blocks of length n
  - book: isbn:9780521823326
    title: Jean-Paul Allouche and Jeffrey Shallit, Automatic Sequences, Cambridge University Press, 2003
    locator: Chapter 10, Subword complexity (basic properties and the theorem that bounded complexity is equivalent to ultimate periodicity)
  - book: isbn:9780521812207
    title: M. Lothaire, Algebraic Combinatorics on Words, Encyclopedia of Mathematics and its Applications 90, Cambridge University Press, 2002
    locator: Chapter 2, Sturmian words (J. Berstel and P. Séébold), the complexity of ultimately periodic words and Sturmian words as the words of complexity n + 1
---

The Morse-Hedlund theorem says that an infinite word is ultimately periodic if and only if, for some length $n \ge 1$, it has at most $n$ distinct factors of length $n$. Equivalently, every infinite word that never becomes periodic has at least $n + 1$ distinct factors of each length $n$. The [subword complexity](/subword-complexity/) thus has a gap: it is either bounded or at least $n + 1$, and the words that reach $n + 1$ exactly are the [Sturmian words](/sturmian-word/). The proof follows the unique continuation of factors once the complexity stops growing.

## Statement

Let $\Sigma$ be a finite [alphabet](/alphabet/); only equality of letters is used. An infinite word $x = x[0]\,x[1] \cdots$ over $\Sigma$ is indexed from 0, and $p_x(n)$ is the number of distinct factors $x[i..i+n-1]$ of length $n$, with $p_x(0) = 1$. The word $x$ is *ultimately periodic* if there are $i_0 \ge 0$ and $q \ge 1$ with $x[t] = x[t + q]$ for all $t \ge i_0$, that is, $x = u\,v^\omega$ for finite words $u$ and $v \ne \varepsilon$.

**Theorem (Morse and Hedlund, 1938).** For an infinite word $x$ the following are equivalent.

1. $x$ is ultimately periodic.
2. $p_x$ is bounded.
3. $p_x(n) \le n$ for some $n \ge 1$.
4. $p_x(n) = p_x(n+1)$ for some $n \ge 0$.

In particular, if $x$ is not ultimately periodic, then $p_x(n) \ge n + 1$ for every $n \ge 0$. Moreover, if $p_x(n) = p_x(n+1) = m$, then $x[t] = x[t + q]$ for all $t \ge i_0$ with some $0 \le i_0 < i_0 + q \le m$; and if $x = u\,v^\omega$ then $p_x(n) \le |u| + |v|$ for all $n$.

## In plain words

Slide a window of fixed width along an endless line of letters and count the different stretches you see. If the line eventually repeats one block forever, you see only a few stretches, however wide the window. The theorem says the converse with a sharp threshold: if for some width $n$ you see at most $n$ different stretches, the line must eventually repeat forever. So a line that never settles shows at least two stretches of width one, three of width two, four of width three, and so on. The reason is that once wider windows stop showing new stretches, each stretch can be continued in only one way, and the line is then forced to cycle.

## Proof

Write $F_n$ for the set of factors of $x$ of length $n$, so $p_x(n) = |F_n|$, and $W_i = x[i..i+n-1]$ for the window of length $n$ at position $i$, with $n$ fixed by context.

*Step 1: $p_x$ is nondecreasing.* Every factor of length $n + 1$ has its prefix of length $n$ in $F_n$, and every $u \in F_n$ is such a prefix: if $u = W_i$ then $u$ is the prefix of $x[i..i+n]$, which exists because $x$ is infinite. So the prefix map $F_{n+1} \to F_n$ is onto and $p_x(n) \le p_x(n+1)$.

*(1) ⇒ (2).* Let $x[t] = x[t + q]$ for $t \ge i_0$. Then $W_i = W_{i+q}$ for $i \ge i_0$, so every window equals one of $W_0, \ldots, W_{i_0 + q - 1}$, and $p_x(n) \le i_0 + q$ for every $n$. With $x = u\,v^\omega$ one may take $i_0 = |u|$ and $q = |v|$, which gives the bound $|u| + |v|$.

*(2) ⇒ (3).* If $p_x(n) \le B$ for all $n$, with $B \ge 1$, then $p_x(B) \le B$.

*(3) ⇒ (4).* Suppose $p_x(m) < p_x(m+1)$ for every $m < n$. Since the values are integers, $p_x(m+1) \ge p_x(m) + 1$, and from $p_x(0) = 1$ we get $p_x(n) \ge n + 1$. So if $p_x(n) \le n$, some $m < n$ has $p_x(m) = p_x(m+1)$ by Step 1.

*(4) ⇒ (1).* Let $p_x(n) = p_x(n+1) = m$. The prefix map $F_{n+1} \to F_n$ is onto by Step 1, and both sets have $m$ elements, so it is a bijection: every $u \in F_n$ has exactly one letter $c(u)$ such that $u\,c(u)$ is a factor of $x$. Then for every $i$, $x[i + n] = c(W_i)$, because $W_i\,x[i+n]$ is a factor, and $W_{i+1}$ is $W_i\,c(W_i)$ without its first letter. So $W_{i+1}$ is a function of $W_i$.

Among the $m + 1$ windows $W_0, \ldots, W_m$ only $m$ values occur, so $W_{i_0} = W_{j}$ for some $0 \le i_0 < j \le m$. Let $q = j - i_0$. By induction on $t$, $W_{i_0 + t} = W_{j + t}$ for all $t \ge 0$: it holds for $t = 0$, and if it holds for $t$ then the next windows are the same function of equal windows. Comparing first letters, $x[i_0 + t] = x[i_0 + t + q]$ for all $t \ge 0$, so $x$ is ultimately periodic with preperiod $i_0$ and period $q$, where $i_0 + q = j \le m$. (For $n = 0$ the windows are empty, $m = 1$, the word uses one letter, and the argument gives $x[t] = x[t+1]$.)

*The lower bound.* If $x$ is not ultimately periodic, (4) fails, so $p_x(m+1) \ge p_x(m) + 1$ for every $m$, and $p_x(n) \ge n + 1$ for all $n$ by induction from $p_x(0) = 1$. $\blacksquare$

**Checks.** For every binary and ternary pair $(u, v)$ with $|v| \ge 1$ and $|u| + |v| \le 6$, the word $u\,v^\omega$ was checked by script for lengths $n \le 14$: $p$ is nondecreasing and at most $|u| + |v|$, some $n \le |u| + |v|$ has $p(n) \le n$, and at the first $n$ with $p(n) = p(n+1)$ the repeated window found among $W_0, \ldots, W_{p(n)}$ gives a valid preperiod and period. For prefixes of length $10^5$ of the Fibonacci word and $2^{16}$ of the Thue-Morse word, $p(n) \ge n + 1$ for all $n \le 30$.

## Consequences

- **Sturmian words.** The least complexity of an aperiodic word is $n + 1$, and the binary aperiodic words with $p(n) = n + 1$ for all $n$ are by definition the [Sturmian words](/sturmian-word/), such as the [Fibonacci word](/fibonacci-word/); the [Sturmian characterization](/sturmian-characterization/) describes them as balanced and mechanical words.
- **Larger alphabets.** If $x$ is aperiodic and uses $k$ letters, then $p_x(1) = k$ and $p_x$ increases strictly, so $p_x(n) \ge n + k - 1$ for every $n \ge 1$.
- **Testing periodicity.** For a [morphic word](/morphic-word/) or any word given by a finite device, ultimate periodicity reduces to finding $n$ with $p(n) = p(n+1)$, and the proof then yields the preperiod and the period, both at most $p(n)$.
- **Right special factors.** Since $p(n+1) - p(n) = \sum_{u \in F_n} (r(u) - 1)$, where $r(u)$ counts the letters that extend $u$, an aperiodic word has at least one right special factor of each length.
- **Two dimensions.** Nivat's conjecture, that a two-dimensional configuration with at most $mn$ distinct $m \times n$ blocks for some $m, n$ is periodic, is the analogue in the plane; it is open in general.

## Tightness

- **The bound $n + 1$.** The Fibonacci word has $p(n) = n + 1$ for all $n$ and is not ultimately periodic, so in (3) the threshold $n$ cannot be replaced by $n + 1$.
- **No finite test.** The word $0^N\,1\,0^\omega$ has $p(n) = n + 1$ for $n \le N + 1$ and $p(n) = N + 2$ for larger $n$. So the first values of $p$ do not decide periodicity: $p(n) \ge n + 1$ for all $n$ up to any fixed bound does not imply aperiodicity.
- **Finite words.** For a finite word of length $N$, $p(n) \le N - n + 1$, so small complexity is forced near $n = N$, and the theorem has no direct finite analogue; finite versions need a condition at a length $n$ much smaller than $N$, as in the [Fine-Wilf theorem](/fine-and-wilf-theorem/).

## History

Morse and Hedlund introduced symbolic dynamics in their 1938 paper and proved there that a sequence with at most $n$ blocks of length $n$ is periodic. Their 1940 sequel, on Sturmian trajectories, studied the sequences that just miss periodicity, with $n + 1$ blocks of each length $n$. Coven and Hedlund (1973) revisited sequences of minimal block growth and gave the characterization of Sturmian words by complexity. The theorem is now the first result in every treatment of subword complexity.

## References
