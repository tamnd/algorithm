---
tag: MJD075
kind: theorem
slug: ballot-theorem
name: Ballot theorem
aliases:
- ballot problem
- Bertrand's ballot theorem
- Bertrand's ballot problem
area: combinatorics/counting-algorithms
level: core
summary: Counts vote sequences in which one candidate stays strictly ahead.
prereqs: [binomial-coefficient, bijective-proof]
see_also: [cycle-lemma, catalan-numbers, reflection-principle, ballot-number, dyck-word, counting-lattice-paths, double-counting, binomial-coefficient]
sources:
  - paper: doi:10.1080/0025570X.2007.11953509
    title: Marc Renault, Four proofs of the ballot theorem, Mathematics Magazine 80(5), 345 to 352 (2007)
    locator: the statement for general k, the proofs by André's method and by the cycle lemma, and the history
  - paper: doi:10.1215/S0012-7094-47-01423-3
    title: A. Dvoretzky and Th. Motzkin, A problem of arrangements, Duke Mathematical Journal 14(2), 305 to 313 (1947)
    locator: the cycle lemma and its use to solve the ballot problem
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume 1, third edition
    locator: Chapter III, Fluctuations in Coin Tossing and Random Walks (Section 1, the reflection principle and the ballot theorem)
---

The ballot theorem counts the orders in which the votes of an election can be counted so that the winner is always strictly ahead. If candidate A gets $a$ votes and candidate B gets $b < a$ votes, and all orders are equally likely, then A leads throughout the count with probability $\frac{a - b}{a + b}$. The general form says that A keeps more than $k$ times as many votes as B with probability $\frac{a - kb}{a + b}$, for an integer $k \ge 1$ and $a \ge kb$. The case $a = n + 1$, $b = n$ gives the [Catalan numbers](/catalan-numbers/).

## Statement

Notation: a **ballot sequence** for $(a, b)$ is a word with $a$ letters A and $b$ letters B; there are $\binom{a+b}{a}$ of them. For a word $w$ and $0 \le t \le a + b$, let $A_t(w)$ and $B_t(w)$ be the numbers of A and B among the first $t$ letters. Numbers here are exact integers or rationals.

**Theorem (ballot theorem).** Let $k \ge 1$ be an integer and let $a, b \ge 0$ be integers with $a \ge kb$ and $a + b \ge 1$. The number of ballot sequences $w$ for $(a, b)$ with
$$A_t(w) > k\,B_t(w) \quad \text{for all } t = 1, \ldots, a + b$$
is
$$\frac{a - kb}{a + b}\binom{a + b}{a}.$$
For $k = 1$ and $a \ge b$ this is $\frac{a - b}{a + b}\binom{a+b}{a} = \binom{a+b-1}{a-1} - \binom{a+b-1}{a}$.

**Weak form.** For $a \ge b \ge 0$, the number of ballot sequences with $A_t \ge B_t$ for all $t$ is $\frac{a + 1 - b}{a + 1}\binom{a + b}{a}$.

Call a sequence that meets the condition **good**, and the others **bad**.

## In plain words

Two people run in an election, and the votes are counted one at a time in a random order. The winner has more votes in the end, but early in the count the loser can be ahead or level. The theorem says how likely it is that the winner is ahead after every single vote.

The answer is simple: the winning margin divided by the total number of votes. If the result is 6 votes to 4, the margin is 2 of 10 votes, so the winner leads all the way in one count of every five. A close election makes a lead from start to end rare, and a landslide makes it likely.

## Proof

**Proof for $k = 1$ (André's method).** Let $a > b$. A sequence that starts with B is bad, since after one vote $A_1 = 0 \not> 1 = B_1$. There are $\binom{a+b-1}{b-1}$ such sequences: the first letter is fixed and the other $a + b - 1$ letters hold $b - 1$ letters B.

Now let $w$ be bad and start with A. Since $A_1 - B_1 = 1$ and $A_t - B_t$ changes by $\pm 1$ at each step, there is a first $t \ge 2$ with $A_t = B_t$. Swap A and B in the first $t$ letters. The prefix keeps the same numbers of A and B, since it is tied, so the new word is a ballot sequence for $(a, b)$, and it starts with B. Conversely, a word $v$ that starts with B has $A_1 - B_1 = -1$ and ends with $a - b > 0$, so it has a first tie at some $t \ge 2$; swapping the first $t$ letters gives a bad word that starts with A and has its first tie at the same $t$. The two maps are inverse, so by the [bijective proof](/bijective-proof/) lemma the bad words that start with A also number $\binom{a+b-1}{b-1}$. Hence the good words number
$$\binom{a+b}{a} - 2\binom{a+b-1}{b-1} = \binom{a+b}{a}\Bigl(1 - \frac{2b}{a+b}\Bigr) = \frac{a - b}{a + b}\binom{a+b}{a},$$
using $\binom{a+b-1}{b-1} = \frac{b}{a+b}\binom{a+b}{a}$. If $a = b$ there are no good words, and the formula gives $0$. $\square$

**Proof for general $k$ (cycle lemma).** Write each A as $+1$ and each B as $-k$. A word is good when all its prefix sums $S_t = A_t - kB_t$, $1 \le t \le a + b$, are positive. The total is $S_{a+b} = a - kb \ge 0$. For $0 \le i < m = a + b$, let $\rho_i(w)$ be the rotation of $w$ that starts at letter $i + 1$. The [cycle lemma](/cycle-lemma/) says that for every word $w$ exactly $a - kb$ of the indices $i \in \{0, \ldots, m - 1\}$ make $\rho_i(w)$ good.

Count the pairs $(w, i)$ with $w$ a ballot sequence and $\rho_i(w)$ good, in two ways, by [double counting](/double-counting/). By the cycle lemma, each of the $\binom{m}{a}$ words gives $a - kb$ pairs. On the other side, for each good word $g$ and each $i$, there is exactly one $w$ with $\rho_i(w) = g$, namely the rotation of $g$ by $i$ steps the other way; so there are $m \cdot \#\{\text{good}\}$ pairs. Hence $m \cdot \#\{\text{good}\} = (a - kb)\binom{m}{a}$. This argument also works when $w$ is periodic and some rotations are equal. $\square$

**Proof of the weak form.** Add one letter A at the front. Then $A_t \ge B_t$ for all prefixes of $w$ exactly when the new word, a ballot sequence for $(a + 1, b)$, has $A_t > B_t$ for all $t \ge 1$. The theorem with $k = 1$ gives $\frac{a + 1 - b}{a + 1 + b}\binom{a + b + 1}{a + 1} = \frac{a + 1 - b}{a + 1}\binom{a + b}{a}$. $\square$

## Consequences

- **The election.** With 6 votes for A and 4 for B, $\frac{2}{10}\binom{10}{6} = \frac{1}{5} \cdot 210 = 42$ of the orders keep A strictly ahead. With 3 to 2, only the two orders AAABB and AABAB do. With 55 to 45 the probability is $\frac{1}{10}$; the good orders number $\frac{1}{10}\binom{100}{45}$, a number of 93 bits.
- **Catalan numbers.** With $a = n + 1$ and $b = n$, the good words number $\frac{1}{2n+1}\binom{2n+1}{n} = C_n$. Removing the first A gives the Dyck words of semilength $n$; equivalently, the weak form with $a = b = n$ gives $\frac{1}{n+1}\binom{2n}{n} = C_n$. See [Catalan numbers](/catalan-numbers/) and [Dyck words](/dyck-word/).
- **Random walks.** For a simple random walk $S_0 = 0, S_1, \ldots, S_n$ with steps $\pm 1$, and $h > 0$, $\Pr[S_1, \ldots, S_n > 0 \mid S_n = h] = h/n$. For $n = 10$ and $h = 4$, 48 of the $\binom{10}{7} = 120$ paths stay positive, and $48/120 = 2/5$. This is the form in Feller, Chapter III, and it leads to the arcsine laws and the distribution of first passage times.
- **Lattice paths with a slope.** The paths with $a$ steps $(1, 1)$ and $b$ steps $(1, -k)$ that stay strictly above the axis after the start number $\frac{a - kb}{a + b}\binom{a+b}{a}$. For $a = 7$, $b = 3$ and $k = 2$ this gives $\frac{1}{10} \cdot 120 = 12$. The case $a - kb = 1$ counts $(k+1)$-ary trees, which gives the Fuss-Catalan numbers; see [counting lattice paths](/counting-lattice-paths/).
- **Ballot numbers.** The counts of the theorem, and of the weak form, for all $(a, b)$ form Catalan's triangle; see [ballot numbers](/ballot-number/).

## Tightness

- **The condition $a \ge kb$.** If $a < kb$, the full word has $A_{a+b} \le k B_{a+b}$, so there are no good words, but the formula is negative. If $a = kb$, both are $0$.
- **Strict versus weak.** The two forms count different sets, and the difference matters: for $a = b = n$ the strict count is $0$ and the weak count is $C_n$.
- **Integer $k$.** The proof by the cycle lemma removes blocks of $k$ letters A and one B, so it needs an integer $k$. For a ratio that is not an integer, the formula fails. With $\mu = 3/2$, $a = 3$ and $b = 1$, the words with $A_t > \tfrac32 B_t$ for all $t$ are AAAB and AABA, so there are 2, while $\frac{a - \mu b}{a + b}\binom{4}{3} = \frac{3}{2}$ is not an integer. With $a = 5$, $b = 2$ the count is 7 and the formula gives 6.
- **Exact formula.** The count is an exact integer for all $a \ge kb$, and the equality holds for every admissible $(a, b, k)$, not only asymptotically; a script checks it for all $a \le 10$, $b \le 7$ and $k \le 3$.

## History

Joseph Bertrand stated the problem in 1887 for $k = 1$, gave the answer $\frac{a - b}{a + b}$, outlined a proof by induction, and asked for a direct proof. In the same year Émile Barbier stated the result for general $k$, without a proof, and Désiré André gave the short combinatorial proof for $k = 1$ shown above. André's proof swaps a prefix; the reflection of a lattice path across a line, often called André's reflection, came later, in papers by Aebly and by Mirimanoff in 1923, and it does not extend to $k > 1$. Aeppli announced a proof for general $k$ in 1923. Dvoretzky and Motzkin introduced the cycle lemma in 1947 and used it to solve the general problem. Goulden and Serrano gave a proof in 2003 that keeps the spirit of reflection for a boundary of any integer slope ([doi:10.1016/j.jcta.2003.09.004](https://doi.org/10.1016/j.jcta.2003.09.004)). Renault's survey of 2007 tells this history and gives four proofs.

## References
