---
tag: BV1WAB
kind: algorithm
slug: wilber-algorithm
name: Wilber's algorithm
aliases:
- linear-time least weight subsequence
area: strings/text-processing-and-typesetting
level: research
summary: Solve the concave least weight subsequence problem in O(n) time by applying SMAWK to blocks of the online dynamic program.
solves: [least-weight-subsequence]
model: word-ram
complexity:
  vars: {n: the last index of the problem (the number of values F(1) to F(n))}
  time: {worst: O(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 1988
  people: [Robert Wilber]
  note: Wilber gave the O(n) algorithm in 1988 by applying the SMAWK matrix searching of 1987 to blocks of the dynamic program and checking guessed values.
prereqs: [hirschberg-larmore-algorithm, smawk-algorithm]
see_also: [least-weight-subsequence, row-minima-of-totally-monotone-matrices, monge-property, divide-and-conquer-optimization, convex-hull-trick, printing-neatly, optimal-text-wrapping, knuth-plass-line-breaking]
sources:
  - paper: doi:10.1016/0196-6774(88)90032-6
    title: "Robert Wilber, The concave least-weight subsequence problem revisited, Journal of Algorithms 9(3), 418-425, 1988"
    locator: "the O(n) algorithm for concave weights"
  - paper: doi:10.1007/BF01840359
    title: "Alok Aggarwal, Maria M. Klawe, Shlomo Moran, Peter Shor and Robert Wilber, Geometric applications of a matrix-searching algorithm, Algorithmica 2, 195-208, 1987"
    locator: "the SMAWK algorithm for the row minima of a totally monotone matrix"
  - paper: doi:10.1137/0216043
    title: "D. S. Hirschberg and L. L. Larmore, The least weight subsequence problem, SIAM Journal on Computing 16(4), 628-638, 1987"
    locator: "the problem, the concave condition and the O(n log n) algorithm that Wilber improves"
  - paper: doi:10.1016/0020-0190(90)90215-J
    title: "Zvi Galil and Kunsoo Park, A linear-time algorithm for concave one-dimensional dynamic programming, Information Processing Letters 33(6), 309-311, 1990"
    locator: "a simpler O(n) algorithm for the same problem"
---

Wilber's algorithm solves the [least weight subsequence](/least-weight-subsequence/) problem $F(0) = 0$, $F(j) = \min_{i < j} \bigl( F(i) + w(i, j) \bigr)$ in $O(n)$ time when the weight $w$ satisfies the quadrangle inequality, the case that Hirschberg and Larmore call concave. The array $B(j, i) = F(i) + w(i, j)$ is then totally monotone, so [SMAWK](/smawk-algorithm/) could find all its row minima in $O(n)$ time, if the array were known. But the column $i$ needs $F(i)$, which is itself a row minimum. Wilber's method works on blocks: it guesses the values of a block of targets from the candidates that are already final, uses the guesses to check themselves with a second SMAWK call, and restarts after the first target where the check fails. The block sizes are chosen so that the total work is linear. Robert Wilber, one of the authors of SMAWK, published it in 1988, improving the $O(n \log n)$ bound of the [Hirschberg-Larmore algorithm](/hirschberg-larmore-algorithm/).

## In plain words

The fast way to find the minimum of every row of a totally monotone table is SMAWK, but it needs the whole table at the start. Here the table fills in as the answers come: the entries of column $i$ are known only after the answer for $i$.

So the method guesses. It computes, for the next block of targets, the best value using only the candidates that are already final. These guesses may be too high, because the candidates inside the block were left out.

It then asks a second question with SMAWK: could a candidate inside the block, using the guessed values, beat a guess? If not, all the guesses are right. If yes, the first guess that is beaten is fixed, the guesses before it are right, and the method starts a new block after it.

## The problem

The input is an integer $n \ge 1$ and a finite weight $w(i, j)$ for $0 \le i < j \le n$, given by a procedure that returns any weight in $O(1)$ time, with

$$w(i, j) + w(i', j') \le w(i, j') + w(i', j) \qquad \text{for all } 0 \le i \le i' < j \le j' \le n.$$

The output is $F(0), \ldots, F(n)$ and, for each $j \ge 1$, an index $P(j) < j$ that attains the minimum. The weights must be finite; a line that is too long gets a large finite penalty instead of $+\infty$ (see Pitfalls).

## The algorithm

The array $G$ holds the final values $F(i)$ for $i \le c$ and guesses after $c$. A call of SMAWK on targets $J$ and candidates $I$ finds, for each $j \in J$, the leftmost $i \in I$ that minimizes $B(j, i) = G[i] + w(i, j)$, with $B(j, i) = +\infty$ when $i \ge j$. The state is a pair $(c, r)$: $F(0), \ldots, F(c)$ are final, and for every target after $c$, the candidates before $r$ can be ignored.

```pseudo id=main
WILBER(n, w)
W1  F[0] ← G[0] ← 0; c ← 0; r ← 0
W2  while c < n do
W3      p ← min(2c - r + 1, n)
W4      SMAWK on the targets c + 1 .. p and the candidates r .. c
W5      for j ← c + 1 to p do G[j] ← the minimum for j; P[j] ← its candidate
W6      if p ≥ c + 2 then SMAWK on the targets c + 2 .. p and the candidates c + 1 .. p - 1; H(j) ← the minimum for j
W7      j0 ← the least target j with H(j) < G[j], or none
W8      if there is no j0 then
W9          F[c + 1 .. p] ← G[c + 1 .. p]; c ← p
        else
W10         F[c + 1 .. j0 - 1] ← G[c + 1 .. j0 - 1]; F[j0] ← G[j0] ← H(j0); P[j0] ← its candidate
W11         r ← c + 1; c ← j0
W12 return F, P
```

Line W3 picks a block of at most $c - r + 1$ targets, the number of live candidates, so that the cost of the block is paid by the growth of $c$ or of $r$. Lines W4 and W5 compute the guess $G[j] = \min_{i \le c} g_i(j)$ for the block, where $g_i(j) = F(i) + w(i, j)$; all its candidates are final. Line W6 computes $H(j) = \min_{c < i < j} \bigl( G[i] + w(i, j) \bigr)$, the best value from a candidate inside the block, using the guesses as if they were final. Line W7 looks for the first target where a candidate inside the block beats the guess.

## Example

Take $n = 10$ and $w(i, j) = (j - i - 2)^2$, a weight that wants every jump to have length 2. The optimum is $F(j) = 0$ for even $j$ and $F(j) = 1$ for odd $j$.

| pass | $c$, $r$ | $p$ | guesses of lines W4 and W5 (candidate) | check of lines W6 and W7 | result |
|---|---|---|---|---|---|
| 1 | 0, 0 | 1 | $G[1] = 1$ (0) | none, the block has one target | $c = 1$ |
| 2 | 1, 0 | 3 | $G[2] = 0$ (0), $G[3] = 1$ (0) | $H(3) = 1$, not less | $c = 3$ |
| 3 | 3, 0 | 7 | $G[4] = 0$ (2), $G[5] = 1$ (2), $G[6] = 2$ (3), $G[7] = 5$ (3) | $H(5) = 1$, $H(6) = 0 < 2$ | failure at 6: $F(6) = 0$ from 4; $r = 4$, $c = 6$ |
| 4 | 6, 4 | 9 | $G[7] = 1$ (4), $G[8] = 0$ (6), $G[9] = 1$ (6) | $H(8) = 2$, $H(9) = 1$, not less | $c = 9$ |
| 5 | 9, 4 | 10 | $G[10] = 0$ (8) | none | $c = 10$ |

In pass 3 the guesses for 6 and 7 are too high, because the best last break for them is 4, a candidate inside the block. The check finds this at 6, keeps $F(4)$ and $F(5)$, sets $F(6)$ from candidate 4, and drops the candidates 0 to 3 for all later targets, since candidate 4 beats all of them at 6. The guess for 7 is thrown away and computed again in pass 4. The back pointers give $10 \to 8 \to 6 \to 4 \to 2 \to 0$, with weight 0.

On the check value $w(i, j) = (j - i - 3)^2$ of the [least weight subsequence](/least-weight-subsequence/) page, the check never fails, and the passes have $c = 0, 1, 3, 7$ and end at 10.

## Correctness

Two facts carry the proof. First, for candidates $i < i'$ and targets $j < j'$, with all entries finite, the inequality gives $B(j', i) - B(j', i') \ge B(j, i) - B(j, i')$, for any values in $G$, since only $G[i] + G[i']$ is added to both sides. So the arrays of lines W4 and W6 are totally monotone, and SMAWK returns their leftmost row minima with $O(|I| + |J|)$ evaluations. The entries $+\infty$ for $i \ge j$ lie in a staircase that keeps this property.

Second, the invariant: at line W2, $F[i] = F(i)$ for $i \le c$, and for every target after $c$, the best candidate among $0, \ldots, c$ is also found among $r, \ldots, c$. Then $G[j]$ from line W5 is the best value over the final candidates. By induction over the block, every guess before $j_0$ is right: the first target has no candidate inside the block, and for a later one the candidates inside the block have right values, so $H(j) \ge G[j]$ means that none of them is better. At $j_0$, the same argument shows $F(j_0) = H(j_0)$. A candidate $i^*$ in the block that beats every $i \le c$ at $j_0$ beats them at every later target, by the first fact, which allows $r \leftarrow c + 1$. The full proof is in the proof file.

## Complexity

By the bound of SMAWK, a pass costs $O((c - r + 1) + (p - c))$ evaluations, which is $O(c - r + 1)$ because line W3 makes $p - c \le c - r + 1$. A pass with no failure and $p = 2c - r + 1$ increases $c$ by $c - r + 1$. A pass with a failure increases $r$ from $r$ to $c + 1$, also by $c - r + 1$. The last pass may have $p = n$ and cost $O(n)$. Since $c$ and $r$ never decrease and stay at most $n$, the total is $O(n)$ evaluations and $O(n)$ time. The space is $\Theta(n)$ for $F$, $G$, $P$ and the lists of SMAWK.

Measured with the kind of weights that the tests of this page use, random weights $f(S_j - S_i - l) + a(i) + b(j)$ for a convex $f$, the program makes about $17.1 n$ evaluations for $n = 500$, $16.5 n$ for $n = 2000$, $14.8 n$ for $n = 8000$ and $14.9 n$ for $n = 32000$: the count per index does not grow. On $w(i, j) = (j - i - 3)^2$ it makes 12968 evaluations for $n = 1000$ and 103962 for $n = 8000$, against 21588 and 220912 for the Hirschberg-Larmore algorithm and 500500 for the dynamic program at $n = 1000$.

## Properties

- **Optimal.** The time $O(n)$ is the best possible, since the output has $n$ values.
- **Not online.** It guesses values ahead and reads weights $w(i, j)$ for targets in the whole block, so all weights must be known in advance.
- **Guesses are thrown away.** After a failure, the guesses after $j_0$ are computed again in the next pass. The analysis charges this work to the growth of $r$.
- **Exact.** It uses only comparisons and additions, so with integers or fractions the values are exact.

## Variants and improvements

- **Simpler linear methods.** Galil and Park gave a simpler $O(n)$ algorithm for the same concave problem in 1990.
- **The $O(n \log n)$ queue method.** The [Hirschberg-Larmore algorithm](/hirschberg-larmore-algorithm/) is much shorter and is often fast enough. On the weights above it makes about 1.4 to 2.1 times as many evaluations for $n$ from 1000 to 8000.
- **The reverse inequality.** For weights with the inequality reversed, the arrays are not totally monotone in the needed direction. The best known methods take almost linear time, see the [least weight subsequence](/least-weight-subsequence/) page.
- **Layers.** For a fixed number of parts, each layer of the dynamic program depends only on the layer before, so its matrix is known in advance and plain SMAWK ([row minima of totally monotone matrices](/row-minima-of-totally-monotone-matrices/)) applies with no guessing.

## When to use it

Use it when the strict linear bound matters, for very long sequences with a concave weight, such as line breaking with rigid spaces and a convex cost of the slack ([printing neatly](/printing-neatly/), [optimal text wrapping](/optimal-text-wrapping/)). For paragraphs of normal size, the $\log n$ factor of the Hirschberg-Larmore algorithm costs little, and that method is simpler to get right. Neither applies directly to the demerits of [Knuth-Plass line breaking](/knuth-plass-line-breaking/), which depend on more than the two ends of a line.

## Pitfalls

- **Infinite weights.** With $w(i, j) = +\infty$ for a line that is too long, two infinite entries compare equal, the strict condition of total monotonicity fails, and SMAWK can drop the column that holds the minimum. The test `test_infinite_weights_can_fail` finds such inputs. Use a large finite penalty that is a convex function of the width, such as $K \max(0, S_j - S_i - l_{\max})$ for a large $K$; it keeps the inequality.
- **Running SMAWK on the whole array.** The array is not known in advance, so a single call over all rows and columns reads values of $F$ that are not computed yet.
- **The block size.** A block larger than the number of live candidates breaks the bound, because a failure early in the block then wastes more work than the growth of $r$ pays for.
- **The strict check.** Line W7 must test $H(j) < G[j]$. A tie means the guess is already right.
- **The constant.** Each pass makes two SMAWK calls and some guesses are computed twice, so the constant factor is larger than that of the simple queue method.

## Implementations

## History

Aggarwal, Klawe, Moran, Shor and Wilber published the SMAWK algorithm in 1987, for the row minima of a totally monotone matrix given in advance. In the same year Hirschberg and Larmore defined the least weight subsequence problem and solved the concave case in $O(n \log n)$ time. Wilber showed in 1988 how to use SMAWK when the matrix is not given in advance, and so solved the concave case in $O(n)$ time. Galil and Park gave a simpler linear algorithm in 1990.

## References
