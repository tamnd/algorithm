---
tag: FSVMW5
kind: algorithm
slug: bit-parallel-lcs
name: Bit-parallel LCS algorithm
aliases:
- Allison-Dix bit-vector LCS
- Crochemore bit-parallel LCS
area: sequences/subsequence-problems
level: advanced
summary: Packs DP rows into machine words so LCS runs in about O(nm / w) word operations.
solves: [longest-common-subsequence]
model: word-ram
complexity:
  vars: {m: the length of X, n: the length of Y, w: the word size in bits, σ: the alphabet size}
  time: {worst: Θ(n ⌈m / w⌉ + σ ⌈m / w⌉ + m), best: Θ(n ⌈m / w⌉ + σ ⌈m / w⌉ + m)}
  space: {extra: Θ(σ ⌈m / w⌉)}
properties: {stable: false, in_place: false, adaptive: false, online: true, deterministic: true, comparison: false, recursive: false}
prereqs: [lcs-dynamic-programming, bit-parallelism, word-ram]
see_also: [myers-bit-parallel-algorithm, four-russians-method, longest-common-subsequence, hirschberg-lcs, hunt-szymanski, myers-diff, edit-distance, longest-palindromic-subsequence]
sources:
  - paper: "Lloyd Allison and Trevor I. Dix, A bit-string longest-common-subsequence algorithm, Information Processing Letters 23(6), 1986, 305-310"
    locator: the encoding of a row of the LCS table as a bit string of its 0 and 1 differences and the update with a subtraction and logical operations
  - paper: "Maxime Crochemore, Costas S. Iliopoulos, Yoan J. Pinzon and James F. Reid, A fast and practical bit-vector algorithm for the longest common subsequence problem, Information Processing Letters 80(6), 2001, 279-285"
    locator: the update V' = (V + (V AND M)) OR (V AND NOT M) with four word operations per column
  - paper: "Heikki Hyyrö, Bit-parallel LCS-length computation revisited, Proceedings of the 15th Australasian Workshop on Combinatorial Algorithms (AWOCA 2004), 2004"
    locator: the comparison of the bit-parallel LCS-length formulas of Allison and Dix and of Crochemore et al.
---

The bit-parallel LCS algorithm computes the length of a [longest common subsequence](/longest-common-subsequence/) of $X$ (length $m$) and $Y$ (length $n$) by storing a whole column of the [LCS table](/lcs-dynamic-programming/) in $\lceil m / w \rceil$ machine words of $w$ bits. Adjacent entries of a column differ by 0 or 1, so one bit per entry is enough, and the column for the next letter of $Y$ comes from the old one with one addition, two ANDs, a NOT and an OR. The time is $\Theta(n \lceil m / w \rceil)$ word operations after the setup, a speedup of about $w$ over the table. Allison and Dix gave the first such method in 1986; the short form used here is due to Crochemore, Iliopoulos, Pinzon and Reid (2001).

## In plain words

In the usual LCS grid, each number is the one above it or one more. So instead of the numbers you can store one bit for each cell of a column: 0 if the number goes up by one there, 1 if it stays the same. The answer is the number of 0 bits in the last column.

A computer adds two numbers of 64 bits in one step, and the carry runs from bit to bit by itself. The trick is that one addition, with the right bits, moves each 0 of the column to the place where the next column needs it. So a whole column of 64 cells costs a few steps instead of 64.

## The problem

The input is two sequences $X = \langle x_1, \ldots, x_m \rangle$ and $Y = \langle y_1, \ldots, y_n \rangle$ over an alphabet $\Sigma$ of size $\sigma$ whose letters can index a table. The output is $\mathrm{lcs}(X, Y)$. The method gives the length, and with it the edit distance without substitutions; a subsequence needs extra work (see the variants).

## The algorithm

Let $c[i, j] = \mathrm{lcs}(X_i, Y_j)$, the [LCS table](/lcs-dynamic-programming/). For a fixed column $j$, $c[i, j] - c[i - 1, j] \in \{0, 1\}$. The word $V_j$ has bit $i - 1$ equal to 0 if $c[i, j] = c[i - 1, j] + 1$ (a *step* at row $i$) and 1 if $c[i, j] = c[i - 1, j]$, for $i = 1, \ldots, m$. The match mask $M[c]$ has bit $i - 1$ set when $x_i = c$. All arithmetic is on $m$-bit words, modulo $2^m$; with $m > w$ each word is an array of $\lceil m / w \rceil$ machine words, and the addition passes its carry from one machine word to the next.

```pseudo id=main
BIT-PARALLEL-LCS(X[1 .. m], Y[1 .. n])
L1  for each letter c: M[c] ← the m-bit word with bit i − 1 set exactly when X[i] = c
L2  V ← 2^m − 1                                   ▷ column 0: all ones, no steps
L3  for j ← 1 to n do
L4      U ← V AND M[Y[j]]                         ▷ matches at rows that are not steps
L5      V ← ((V + U) OR (V AND NOT M[Y[j]])) mod 2^m
L6  return m − (the number of 1 bits of V)        ▷ the number of steps in column n
```

Why it works, in brief. Split the bits of $V$ into *blocks*: each block is a run of 1 bits, from the least significant end upward, closed by one 0 bit (the last block may have no 0). The rows of a block share one value of the old column, and the 0 marks where it steps up. In the new column, the step of each block moves down to the first row of the block where $x_i = y_j$, or stays where it is if there is no such row. The addition does exactly this: in a block, the lowest bit of $U$ is the first match, and adding it to the run of 1 bits sends a carry up to the 0 at the end of the block, which turns into a 1 and stops the carry. The OR restores the 1 bits at the rows above the first match that the carry cleared but that are not steps. The same update can be written as $(V + U)$ OR $(V - U)$, since $V - U = V$ AND NOT $M$ when $U \subseteq V$.

## Example

Take $X = \text{ABCBDAB}$ and $Y = \text{BDCABA}$. The match masks, written with row 1 first (bit 0 on the left):

| letter | A | B | C | D |
| --- | --- | --- | --- | --- |
| rows 1 to 7 | 1000010 | 0101001 | 0010000 | 0000100 |

The words $V_j$, with row 1 first, and the number of steps:

| $j$ | $y_j$ | $V_j$ (rows 1 to 7) | steps = $c[7, j]$ |
| --- | --- | --- | --- |
| 0 | | 1111111 | 0 |
| 1 | B | 1011111 | 1 |
| 2 | D | 1011011 | 2 |
| 3 | C | 1001111 | 2 |
| 4 | A | 0101101 | 3 |
| 5 | B | 0010110 | 4 |
| 6 | A | 0010101 | 4 |

The last column has 4 zero bits, so $\mathrm{lcs}(X, Y) = 4$. Column 1 in detail: $V = 1111111$ is one block without a 0. $U = V$ AND $M[\text{B}] = 0101001$, with first match at row 2. The sum $V + U$ clears rows 2 to 7 by the carry, which leaves the top of the word, and then sets the other bits of $U$: $1001001$. The term $V$ AND NOT $M[\text{B}] = 1010110$ restores rows 3, 5 and 6. The OR is $1011111$: one step, at row 2, as in column 1 of the table, where $c[i, 1]$ is 0 for $i = 1$ and 1 from $i = 2$ on.

## Correctness

The proof shows by induction on $j$ that $V$ after column $j$ encodes the steps of column $j$ of the LCS table. The key lemma is the block rule above: if rows $s, \ldots, e$ form a block of column $j - 1$ (no steps at $s, \ldots, e - 1$, a step at $e$), then column $j$ has exactly one step in these rows, at the first row $f \in [s, e]$ with $x_f = y_j$, or at $e$ if there is none; and $c[e, j] = c[e, j - 1]$, so the blocks of the two columns line up. It follows from the LCS recurrence and $0 \le c[i, j] - c[i, j - 1] \le 1$. Then a computation of $V + U$ block by block, where no carry passes from one block to the next, shows that line L5 produces exactly these bits. The number of steps in column $n$ is $c[m, n]$, which line L6 returns. The full proof is in the proof file.

## Complexity

- **Setup.** Line L1 builds $\sigma$ masks of $\lceil m / w \rceil$ words each and sets $m$ bits: $\Theta(\sigma \lceil m / w \rceil + m)$ time and $\Theta(\sigma \lceil m / w \rceil)$ space. Only the letters that occur in $X$ need a nonzero mask; with a hash table, $\Theta(\min(\sigma, m) \lceil m / w \rceil)$.
- **Main loop.** Each of the $n$ columns does one AND, one NOT, one AND, one addition with carry and one OR on $\lceil m / w \rceil$ words: $\Theta(n \lceil m / w \rceil)$.
- **Answer.** One population count over $\lceil m / w \rceil$ words.
- **In practice.** For $m \le 64$, each column is about five machine instructions, so the LCS length of two strings of length 64 takes a few hundred instructions. For $m = n = 10^5$ and $w = 64$, the loop does about $1.6 \times 10^8$ word steps, against $10^{10}$ cells of the plain table.

## Properties

- **Length only.** The method keeps one column; the subsequence is not recorded.
- **Online in $Y$.** $Y$ is read once, letter by letter, so it can be a stream; $X$ must be known in advance for the masks.
- **Not a comparison method.** The masks need the letters as table indices, so the $\Omega(mn)$ bound for equality tests does not apply. The speedup is by a factor $w$, not a change of the exponent.
- **Oblivious.** The same operations run on every input of the same lengths, which suits vector units and constant-time code.

## Variants and improvements

- **Allison-Dix.** The first bit-string method uses a subtraction and a few more logical operations per column; Crochemore et al. reduce it to the four operations of line L5, and Hyyrö compares the forms.
- **Recovering an LCS.** Store all $n$ words $V_j$, which is $n \lceil m / w \rceil$ words, and trace back through the bits; or use the bit-parallel column as the row routine inside [Hirschberg's algorithm](/hirschberg-lcs/), which gives an LCS in $O(mn / w)$ time and linear space.
- **Edit distance.** [Myers' bit-parallel algorithm](/myers-bit-parallel-algorithm/) does the same for the Levenshtein [edit distance](/edit-distance/), where adjacent cells differ by $-1$, 0 or 1, with two bit vectors per column.
- **Four Russians.** The [Four Russians method](/four-russians-method/) precomputes all blocks of small size and gets $O(mn / \log n)$ time for a fixed alphabet. The bit-parallel method gains a factor $w$ instead, which is larger in practice.
- **Palindromes.** With $X = S$ and $Y = S^R$, it gives the [longest palindromic subsequence](/longest-palindromic-subsequence/) length in $O(n^2 / w)$ word operations.

## When to use it

Use it to compute many LCS lengths or similarity scores of short and medium strings, such as DNA reads, words, or lines, where only the length matters, or as the length routine of a larger method. For an LCS itself in small memory, combine it with Hirschberg's split. For long similar inputs, [Myers' $O((m + n) D)$ algorithm](/myers-diff/) does less work. For a large alphabet with few matches, [Hunt-Szymanski](/hunt-szymanski/) can be faster.

## Pitfalls

- **Bit order.** Row 1 must be the least significant bit, so that the carry runs from low rows to high rows, in the direction of increasing $i$.
- **Overflow of the last block.** The carry of the last block leaves the top of the word. It must be dropped, by the mod $2^m$ of line L5; in a language with unbounded integers, mask with $2^m - 1$, or the count of line L6 is wrong.
- **Multiword carry.** With $m > w$, the carry out of each machine word must go into the next one, and the words must be added from low to high.
- **Missing letters.** A letter of $Y$ that does not occur in $X$ has the mask 0; then $U = 0$ and $V$ is unchanged, which is correct, but the lookup must not fail.
- **The 0 and 1 convention.** This page uses 0 for a step. Some papers use the complement; mixing the two gives wrong counts.

## Implementations

## History

Allison and Dix published a bit-string LCS algorithm in Information Processing Letters in 1986. Crochemore, Iliopoulos, Pinzon and Reid gave the shorter update with four operations per column in 2001, and Hyyrö (2004) compared the bit-parallel LCS formulas.

## References
