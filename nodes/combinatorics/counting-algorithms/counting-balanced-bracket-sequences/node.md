---
tag: 60RDXN
kind: problem
slug: counting-balanced-bracket-sequences
name: Counting balanced bracket sequences
aliases:
- counting Dyck words
- number of balanced parentheses strings
area: combinatorics/counting-algorithms
level: core
summary: Problem of counting balanced bracket sequences of length 2n, answered by the Catalan numbers or by dynamic programming with bounded depth.
prereqs: [catalan-numbers, reflection-principle]
see_also: [catalan-numbers, dyck-word, balanced-parentheses, balanced-bracket-sequence-ranking, balanced-parentheses-generation, kth-balanced-bracket-sequence, counting-parenthesizations, reflection-principle]
sources:
  - book: isbn:9781107427747
    title: Richard P. Stanley, Catalan Numbers, Cambridge University Press, 2015
    locator: Chapter 1, Basic properties, and Chapter 2, Bijective exercises (ballot sequences and Dyck paths)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.6, Generating all trees (nested parentheses and the ballot numbers)
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter V, Applications of rational and meromorphic asymptotics (lattice paths of bounded height and continued fractions)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 7.5, Convolutions (the Catalan numbers from their generating function)
---

Counting balanced bracket sequences asks how many strings of $n$ opening and $n$ closing brackets are correctly nested. The answer is the Catalan number $C_n = \frac{1}{n + 1} C(2n, n)$, which a [reflection](/reflection-principle/) proves in one line. The variants that matter in practice, such as a bound on the nesting depth, a fixed prefix, several kinds of brackets or a pattern with unknown characters, are solved by closed forms or by a dynamic program over the current depth. The exact count has about $2n$ bits, and modulo a prime it can be found even for huge $n$.

## In plain words

A string of round brackets is balanced if every closing bracket matches an earlier opening one, as in "(()())". Count the balanced strings with a given number of pairs. Read the string from left to right and keep a counter that goes up at "(" and down at ")". The string is balanced when the counter never goes below zero and ends at zero. So the task is to count walks of up and down steps that stay above the floor, and both a formula and a simple table do this.

## Definition

**Notation.** $n \ge 0$ is the number of pairs, $C(n, k)$ is the binomial coefficient, with $C(n, k) = 0$ outside $0 \le k \le n$, $[n] = \{1, \ldots, n\}$, and $C_n = \frac{1}{n + 1} C(2n, n)$ is the $n$-th [Catalan number](/catalan-numbers/). The *depth* of a prefix is its number of "(" minus its number of ")".

A string over $\{ (, ) \}$ of length $2n$ is *balanced* if every prefix has depth $\ge 0$ and the whole string has depth $0$. These strings are the [Dyck words](/dyck-word/), and their nesting structure is that of [balanced parentheses](/balanced-parentheses/).

**Input:** $n$, and in the variants a depth bound $h$, a prefix, a number $k$ of bracket types, a pattern over $\{ (, ), ? \}$, or a modulus.

**Output:** the number $N$ of balanced strings with the given properties, exactly or modulo the given number.

**Theorem 1.** The number of balanced strings of length $2n$ is $C(2n, n) - C(2n, n + 1) = C_n$.

*Proof.* A string with $n$ letters of each kind is a walk of length $2n$ from depth $0$ to depth $0$, and it is balanced unless it touches depth $-1$. By the [reflection principle](/reflection-principle/), the walks that touch $-1$ are as many as all walks from $0$ to $-2$, which have $n - 1$ up steps and $n + 1$ down steps. So the count is $C(2n, n) - C(2n, n + 1)$, and $C(2n, n + 1) = \frac{n}{n + 1} C(2n, n)$ gives $C_n$. $\square$

**Theorem 2 (first return).** $C_0 = 1$ and $C_{n+1} = \sum_{i=0}^{n} C_i\, C_{n-i}$.

*Proof.* A nonempty balanced string $w$ has a unique first prefix of depth $0$, of length $2(i + 1)$ for some $i$. So $w = (\,A\,)\,B$ with $A$ balanced of length $2i$ and $B$ balanced of length $2(n - i)$, and this decomposition is a bijection. $\square$

**Theorem 3 (completions).** A prefix of depth $d \ge 0$ (and no prefix of negative depth) with $m$ characters left to write has

$$C(m, u) - C(m, u - 1), \qquad u = \frac{m - d}{2},$$

balanced completions when $m - d$ is even and $m \ge d$, and none otherwise.

*Proof.* A completion is a walk of length $m$ from $d$ to $0$ that never touches $-1$. It has $u$ up steps, so there are $C(m, u)$ free walks. Reflecting in $-1$ maps the bad ones one to one onto the walks from $d$ to $-2$, which have $u - 1$ up steps. $\square$

## Variants

- **Bounded depth.** Count the balanced strings whose depth never exceeds $h$. These are the walks in the strip $[0, h]$, counted by the table below or by the alternating sum of binomials of the two-barrier [reflection principle](/reflection-principle/).
- **Fixed prefix.** Count the balanced strings that start with a given prefix, by Theorem 3. This is the step that [ranking](/balanced-bracket-sequence-ranking/) and [finding the $k$-th sequence](/kth-balanced-bracket-sequence/) repeat at each position.
- **Several bracket types.** With $k$ kinds of brackets, such as "()" and "[]", that must match by kind, the count is $k^n C_n$: the shape is a balanced string, and each of the $n$ matched pairs chooses its kind freely. For $k = 2$ and $n = 3$ this is $8 \cdot 5 = 40$.
- **Patterns with unknown characters.** Given a string over $\{ (, ), ? \}$, count the ways to replace each "?" so that the result is balanced. This needs the table, because the fixed characters break the symmetry of the formula.
- **Huge $n$ modulo a prime.** Compute $C_n \bmod p$ for $n$ up to $10^{18}$.
- **Ordered by length only.** The balanced strings of any length up to $2n$ number $C_0 + C_1 + \cdots + C_n$.

## Examples

**Example 1.** For $n = 3$ the $C_3 = 5$ balanced strings are ((())), (()()), (())(), ()(()) and ()()(). The counts for $n = 0, \ldots, 10$ are $1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796$ (OEIS A000108).

**Example 2: bounded depth.** The counts with depth at most $h$, for $n = 0, \ldots, 8$:

| $h$ | $n = 0$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 |
| 3 | 1 | 1 | 2 | 5 | 13 | 34 | 89 | 233 | 610 |
| none | 1 | 1 | 2 | 5 | 14 | 42 | 132 | 429 | 1430 |

The row $h = 3$ is the Fibonacci numbers of odd index (OEIS A001519), and the last row is the Catalan numbers.

**Example 3: completions.** The prefix "(()(" has depth $d = 2$. For $n = 5$ there are $m = 6$ characters left, so $u = 2$ and the number of completions is $C(6, 2) - C(6, 1) = 15 - 6 = 9$.

**Example 4: a pattern.** The pattern "(??)??" has 3 balanced fillings: ((())), (())() and ()()().

## Known algorithms

**Closed form, exact.** Use $C_0 = 1$ and $C_{j+1} = \frac{2(2j + 1)}{j + 2} C_j$, where each division is exact. This is $O(n)$ multiplications and divisions of an $O(n)$-bit number by an $O(\log n)$-bit number, so $O(n^2)$ word operations. Computing $C(2n, n)$ from its prime factorization, with Legendre's formula for the exponents and a product tree, takes $O(M(n) \log n)$ bit operations, where $M(n)$ is the cost of multiplying two $n$-bit numbers. See [binomial coefficient computation](/binomial-coefficient-computation/).

**Closed form, modulo a prime.** For a prime $p > 2n$, a table of factorials gives $C_n = (2n)!\,/\,(n!\,(n + 1)!) \bmod p$ in $O(n)$ operations. For a small prime $p$, the factor $n + 1$ may be divisible by $p$, so use the difference $C_n = C(2n, n) - C(2n, n + 1)$ and compute both binomials by [Lucas's theorem](/lucas-theorem/) in $O(p + \log_p n)$ operations.

**Depth table.** Let $T[i][d]$ be the number of ways to write the first $i$ characters so that the depth is $d$ and no prefix is negative. Then $T[0][0] = 1$ and

$$T[i][d] = T[i-1][d-1] + T[i-1][d+1],$$

with only the terms allowed by the pattern, and with $T[i][d] = 0$ for $d < 0$ or $d > h$. The answer is $T[2n][0]$. This uses $O(n \min(n, h))$ additions. Each value has at most $2n$ bits, so the exact bit cost is $O(n^2 \min(n, h))$, and modulo a word-size prime the cost is $O(n \min(n, h))$ word operations. The same table handles bounded depth, fixed prefixes and patterns.

**Parity.** $C_n$ is odd if and only if $n + 1$ is a power of 2. *Proof.* $C(2n + 1, n) = (2n + 1) C_n$ and $2n + 1$ is odd, so $C_n$ and $C(2n + 1, n)$ have the same parity. By Lucas's theorem modulo 2, $C(2n + 1, n)$ is odd exactly when every binary 1 of $n$ is also a 1 of $2n + 1$. Bit $i \ge 1$ of $2n + 1$ is bit $i - 1$ of $n$, and bit $0$ of $2n + 1$ is 1, so the condition says that bit $i$ of $n$ implies bit $i - 1$ of $n$, that is, $n = 2^j - 1$. $\square$

**Listing.** [Balanced parentheses generation](/balanced-parentheses-generation/) lists the strings one by one, with total time at least $C_n$. Use it only to check counts for small $n$.

## Bounds

- **Growth.** $C_n \sim \frac{4^n}{\sqrt{\pi}\, n^{3/2}}$. The ratio of $C_n$ to this estimate is $0.898$ for $n = 10$, $0.9889$ for $n = 100$ and $0.9989$ for $n = 1000$.
- **Bits.** $C_n \le C(2n, n) \le 4^n$, so $C_n$ has fewer than $2n$ bits. For $n = 1000$ it has 1985 bits, or 598 decimal digits. So any exact method needs $\Omega(n)$ bit operations to write the answer.
- **Bounded depth.** For a fixed $h$, the count grows like $(2 \cos \frac{\pi}{h + 2})^{2n}$, the square of the largest eigenvalue of the path graph with $h + 1$ vertices. For $h = 3$ this is $\varphi^{2n}$, with $\varphi$ the golden ratio.

## Reductions

- Balanced strings of length $2n$ correspond one to one to Dyck paths, to binary trees with $n$ nodes (the first-return decomposition of Theorem 2 gives the left and right subtrees), and to the ways to fully parenthesize a product of $n + 1$ factors, see [counting parenthesizations](/counting-parenthesizations/).
- They also correspond to the paths with steps $E$ and $N$ from $(0, 0)$ to $(n, n)$ that stay below the diagonal, see [counting lattice paths](/counting-lattice-paths/).
- The depth table is the [transfer-matrix method](/transfer-matrix-method/) on the path graph with $h + 1$ vertices, so the bounded-depth count for huge $n$ is a matrix power.
- Counting the fillings of a pattern is counting the accepted strings of a one-counter automaton along a fixed template, which the depth table does.

## Applications

- **Stacks.** A sequence of $n$ pushes and $n$ pops on an initially empty stack is valid exactly when it is balanced, so $C_n$ counts the valid operation sequences, and also the permutations that one stack can produce from $1, 2, \ldots, n$.
- **Parsing and testing.** Counting and ranking balanced strings lets a test generator pick a uniform random expression shape, or enumerate all shapes of a given size.
- **Combinatorial identities.** Many families counted by Catalan numbers, such as triangulations of a polygon and noncrossing matchings, are proved equinumerous by a bijection with balanced strings.
- **Dynamic programming exercises.** The depth table with wildcards is a standard problem that teaches counting with a state for the depth.

## References
