---
tag: TTP87R
kind: theorem
slug: cycle-lemma
name: Cycle lemma
aliases:
- Dvoretzky-Motzkin cycle lemma
- Raney's lemma
- Raney lemma
area: combinatorics/counting-algorithms
level: advanced
summary: Among cyclic shifts of a sequence with a suitable sum, exactly some shifts are good.
prereqs: [binomial-coefficient, double-counting]
see_also: [ballot-theorem, catalan-numbers, dyck-word, reflection-principle, counting-lattice-paths, double-counting, rooted-tree, prefix-sums]
sources:
  - paper: doi:10.1215/S0012-7094-47-01423-3
    title: A. Dvoretzky and Th. Motzkin, A problem of arrangements, Duke Mathematical Journal 14(2), 305 to 313 (1947)
    locator: the cycle lemma in its general form, and its use for the ballot problem
  - paper: doi:10.1016/S0195-6698(13)80053-4
    title: Nachum Dershowitz and Shmuel Zaks, The cycle lemma and some applications, European Journal of Combinatorics 11(1), 35 to 40 (1990)
    locator: two proofs of the lemma, its history, and applications to trees and lattice paths
  - paper: doi:10.1090/S0002-9947-1960-0114765-9
    title: George N. Raney, Functional composition patterns and power series reversion, Transactions of the American Mathematical Society 94(3), 441 to 451 (1960)
    locator: the lemma for sequences with sum 1, and its link to the reversion of power series
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 7.5, Convolutions (Raney's lemma and the Catalan and Fuss-Catalan numbers)
---

The cycle lemma says that if a sequence of integers, each at most 1, has a positive sum $s$, then exactly $s$ of its cyclic shifts have all partial sums positive. With sum 1 it holds for any integers, and then exactly one shift is good (Raney's lemma). It turns a count with a prefix condition into a plain count divided by the length, and so gives the [ballot theorem](/ballot-theorem/), the [Catalan numbers](/catalan-numbers/) as $\frac{1}{2n+1}\binom{2n+1}{n}$, and the number of trees with given node degrees.

## Statement

Notation: let $x = (x_1, \ldots, x_m)$ be a sequence of $m \ge 1$ integers with sum $s = x_1 + \cdots + x_m$. For $0 \le i < m$, the **rotation** $\rho_i(x)$ is $(x_{i+1}, \ldots, x_m, x_1, \ldots, x_i)$. A sequence $y$ of length $m$ is **good** if all its partial sums $y_1 + \cdots + y_t$, $1 \le t \le m$, are positive. Rotations are counted by their index $i$, so a periodic sequence can have equal good rotations with different indices.

**Theorem (cycle lemma).**

1. If $x_i \le 1$ for all $i$ and $s \ge 1$, then exactly $s$ of the indices $i \in \{0, \ldots, m - 1\}$ make $\rho_i(x)$ good.
2. (Raney's lemma.) If $s = 1$, then exactly one index $i$ makes $\rho_i(x)$ good, with no condition on the size of the $x_i$.

**Corollary (Dvoretzky and Motzkin).** Let $k \ge 1$ be an integer, and let $x$ consist of $a$ entries $+1$ and $b$ entries $-k$ in any order, with $a - kb \ge 1$. Then exactly $a - kb$ of the $a + b$ rotations of $x$ are good. This is part 1 with $s = a - kb$.

## In plain words

Write some numbers around a circle. Each number is at most one, and together they add up to a positive total. Pick a starting point, walk once around the circle, and keep a running total. Call the start good if the running total is above zero at every step.

The lemma says the number of good starts is exactly the total of the numbers. If the numbers add up to three, exactly three starts are good, whatever the order. So instead of checking each start, you can count all arrangements, which is easy, and then take the right share of them. This is the key step in many counting proofs about elections, bracket strings and trees.

## Proof

Extend $x$ periodically, $x_{j+m} = x_j$ for all integers $j$, and let $P_j$ be the walk with $P_0 = 0$ and $P_j - P_{j-1} = x_j$ for all $j \in \mathbb{Z}$. Then $P_{j+m} = P_j + s$. The rotation $\rho_i(x)$ has partial sums $P_{i+t} - P_i$ for $t = 1, \ldots, m$, so $\rho_i(x)$ is good exactly when $P_j > P_i$ for $i < j \le i + m$. Since $P_{j+m} = P_j + s > P_j$ when $s \ge 1$, this is the same as $P_j > P_i$ for all $j > i$. Call such an index $i \in \mathbb{Z}$ a **record** of the walk.

*Proof of part 1.* Since $s \ge 1$, $P_j \to +\infty$ as $j \to +\infty$ and $P_j \to -\infty$ as $j \to -\infty$. For an integer level $v$, let $r(v)$ be the largest $j$ with $P_j \le v$; it exists by the two limits. Then $P_{r(v)+1} > v \ge P_{r(v)}$, and the step $x_{r(v)+1}$ is at most 1, so $P_{r(v)} = v$. All later values are above $v$, so $r(v)$ is a record. Conversely, a record $i$ is the last index with $P_j \le P_i$, so $i = r(P_i)$. Hence $v \mapsto r(v)$ is a bijection from $\mathbb{Z}$ onto the records, increasing in $v$, with $r(v + s) = r(v) + m$ because $P_{j+m} = P_j + s$. Let $v_0$ be the smallest level with $r(v_0) \ge 0$. Then $r(v_0 - 1) < 0$, so $r(v_0 + s - 1) = r(v_0 - 1) + m < m$ and $r(v_0 + s) = r(v_0) + m \ge m$. So the records in $\{0, \ldots, m-1\}$ are exactly $r(v_0), \ldots, r(v_0 + s - 1)$, which are $s$ indices. $\square$

*Proof of part 2.* Let $s = 1$, and let $i$ be the largest index in $\{0, \ldots, m-1\}$ where $P_0, \ldots, P_{m-1}$ takes its minimum. For $i < j \le m - 1$, $P_j > P_i$ because $i$ is the last minimum. For $m \le j \le i + m$, $P_j = P_{j-m} + 1 \ge P_i + 1 > P_i$. So $\rho_i(x)$ is good. If $i < i'$ in $\{0, \ldots, m-1\}$ were both good, then $P_{i'} > P_i$ since $i' > i$, and $P_i + 1 = P_{i+m} > P_{i'}$ since $i + m > i'$. Then $P_i < P_{i'} < P_i + 1$, which is impossible for integers. $\square$

*A second proof of the corollary (Dershowitz and Zaks).* Read $x$ around the circle. If $b = 0$, all $a$ rotations are good. Otherwise, since $a \ge kb + 1$, some $k$ consecutive entries $+1$ are followed by a $-k$, by the [pigeonhole principle](/pigeonhole-principle/). No position inside this block starts a good rotation, since the running sum drops to at most 0 at the $-k$. The block has sum 0, so removing it changes no other position's status. Repeat until $a - kb$ entries $+1$ remain; each of them starts a good rotation.

**Worked example.** $x = (1, -2, 1, 1, -2, 1, 1, 1)$ has $m = 8$, $a = 6$ entries $+1$, $b = 2$ entries $-2$ and $s = 2$. The walk $P_0, \ldots, P_8$ is $0, 1, -1, 0, 1, -1, 0, 1, 2$. The records in $\{0, \ldots, 7\}$ are $i = 5$ (level $-1$) and $i = 6$ (level $0$): the rotations $(1, 1, 1, 1, -2, 1, 1, -2)$ and $(1, 1, 1, -2, 1, 1, -2, 1)$ have partial sums $1, 2, 3, 4, 2, 3, 4, 2$ and $1, 2, 3, 1, 2, 3, 1, 2$. Every other rotation reaches a partial sum at most 0.

**Finding the good rotations.** With $P_0, \ldots, P_{m-1}$, index $i$ is good exactly when $P_i < P_j$ for $i < j < m$ and $P_i < P_j + s$ for $0 \le j < i$. One pass for suffix minima and one for prefix minima find all good indices in $O(m)$ time, using [prefix sums](/prefix-sums/).

## Consequences

- **Ballot theorem.** Count the pairs (word, rotation index) in which the rotation is good, in two ways, by [double counting](/double-counting/). The corollary gives $(a - kb)\binom{a+b}{a}$ pairs, and each good word appears $a + b$ times. So the good words number $\frac{a - kb}{a + b}\binom{a+b}{a}$; see the [ballot theorem](/ballot-theorem/).
- **Catalan numbers.** Words with $n + 1$ letters U ($+1$) and $n$ letters D ($-1$) have sum 1, so exactly one of the $2n + 1$ rotations is good, and the good words number $\frac{1}{2n+1}\binom{2n+1}{n} = C_n$. Removing the first U from a good word gives a [Dyck word](/dyck-word/).
- **Fuss-Catalan numbers.** In the preorder of a full $q$-ary tree, write $q - 1$ for each internal node and $-1$ for each leaf; a tree with $n$ internal nodes gives a word of sum $-1$. Reversed and negated, it becomes a word of $n$ entries $-(q-1)$ and $(q-1)n + 1$ entries $+1$ with sum 1. Raney's lemma then gives $\frac{1}{(q-1)n+1}\binom{qn}{n}$ trees: $1, 1, 3, 12, 55, 273$ for $q = 3$.
- **Trees with given degrees.** A plane [rooted tree](/rooted-tree/) with $n$ nodes is determined by the list $d_1, \ldots, d_n$ of the numbers of children in preorder, and a list is valid exactly when $\sum_{i \le j}(d_i - 1) \ge 0$ for $j < n$ and the total is $-1$. Read in reverse order, the entries $1 - d_i$ have sum 1, and the list is valid exactly when this reversed sequence is good. Each arrangement of the degrees has one good rotation by Raney's lemma, so the trees with $n_j$ nodes of $j$ children for each $j$ number $\frac{1}{n}\binom{n}{n_0, n_1, \ldots}$. For $n = 5$ these counts are $1, 4, 2, 6, 1$ over the five possible degree lists, with total $14 = C_4$.
- **Hitting times.** For a random walk with independent, identically distributed integer steps that are each at most 1, the first time $T_k$ at which it reaches level $k \ge 1$ satisfies $\Pr[T_k = n] = \frac{k}{n}\Pr[S_n = k]$ (the hitting time theorem). The event $T_k = n$ says that $S_n = k$ and the reversed steps have positive partial sums, and the steps are exchangeable, so part 1 gives the factor $k/n$.
- **Uniform random generation.** To draw a uniform Dyck word of semilength $n$, draw a uniform word with $n + 1$ letters U and $n$ letters D, rotate it to its unique good rotation, and remove the first letter. Each good word has exactly $2n + 1$ preimages, since $\gcd(n + 1, 2n + 1) = 1$ makes all rotations distinct, so the output is uniform, and the time is $O(n)$. The same method draws uniform random trees with given degrees.
- **Lagrange inversion.** Raney's lemma is the combinatorial form of the Lagrange inversion formula: the coefficient of $z^n$ in the series $T(z)$ with $T = z\,\phi(T)$ is $\frac{1}{n}[u^{n-1}]\phi(u)^n$, and the factor $\frac{1}{n}$ is the share of good rotations.

## Tightness

- **Entries at most 1.** Part 1 fails without this condition. $x = (3, -1)$ has $s = 2$ but only one good rotation, $(3, -1)$; the rotation $(-1, 3)$ starts below 0. Likewise $(2, 2, -1, -1)$ has $s = 2$ and one good rotation. Raney's lemma shows that the case $s = 1$ needs no such condition.
- **Positive sum.** If $s \le 0$, no rotation is good, since its last partial sum is $s$.
- **Strict partial sums.** With "nonnegative" in place of "positive", the count changes: $(1, -1, 1)$ has $s = 1$ and one good rotation, $(1, 1, -1)$, but two rotations with all partial sums at least 0, $(1, -1, 1)$ and $(1, 1, -1)$.
- **Periodic sequences.** The count is of indices, not of distinct sequences. $(1, 1, -1, 1, 1, -1)$ has $s = 2$, and the two good indices 0 and 3 give the same sequence. The double counting in the consequences is correct for this reason; counting distinct rotations would not be.

## History

Dvoretzky and Motzkin stated and proved the lemma in 1947, in its general form with entries $+1$ and $-k$ and also for some non-integer $k$, to solve the ballot problem. Spitzer gave a version for sequences of real numbers in 1956 and used it for fluctuations of random walks. Raney proved the case of sum 1 in 1960, in a paper on the reversion of power series, and Concrete Mathematics calls it Raney's lemma. Dershowitz and Zaks called it a "frequently rediscovered combinatorial lemma" in 1990: they listed many independent proofs, most of them only for $k = 1$ or for sum 1, gave two short proofs, and applied it to trees and lattice paths.

## References
