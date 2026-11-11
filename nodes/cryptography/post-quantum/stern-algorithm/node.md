---
tag: 3YXVP5
kind: algorithm
slug: stern-algorithm
name: Stern's algorithm
aliases:
- Stern's information set decoding
area: cryptography/post-quantum
level: advanced
summary: An information set decoder that splits the information set in two halves, puts p errors in each, and matches the halves on l rows with a hash table. The first gain in the exponent over Prange.
solves: [syndrome-decoding-problem]
model: word-ram
complexity:
  vars: {n: the code length, k: the code dimension, w: the error weight, p: the number of errors in each half, l: the number of rows in the collision window, M: "binomial(k/2, p), the size of one list", N: "the expected number of rounds, binomial(n, w) over binomial(k/2, p) squared times binomial(n - k - l, w - 2p)"}
  time: {expected: O((n^3 + n M + n M^2 / 2^l) N), best: O(n^3 + n M + n M^2 / 2^l)}
  space: {extra: O(n^2 + n M)}
properties: {deterministic: false, randomized: true}
history:
  year: 1989
  people: [Jacques Stern]
  note: Stern presented the method at the third International Colloquium on Coding Theory and Applications in 1988, and it appeared in LNCS 388 in 1989. It combines Leon's window of zero positions with a birthday collision.
prereqs: [lee-brickell-algorithm, birthday-paradox]
see_also: [prange-algorithm, information-set-decoding, meet-in-the-middle-attack, syndrome-decoding-problem, mceliece-cryptosystem, representation-technique]
sources:
  - paper: "Jacques Stern, A method for finding codewords of small weight, Coding Theory and Applications, LNCS 388, pages 106 to 113, Springer, 1989"
    locator: the whole paper (the split of the information set in two halves, the window of l zero positions, and the collision search)
  - paper: "Daniel J. Bernstein, Tanja Lange and Christiane Peters, Attacking and defending the McEliece cryptosystem, PQCrypto 2008, LNCS 5299, pages 31 to 46"
    locator: Sections 2 to 4 (Stern's algorithm in the decoding form that this page uses, its cost, and the improvements used to break the original McEliece parameters)
  - paper: "Jeffrey S. Leon, A probabilistic algorithm for computing minimum weights of large error-correcting codes, IEEE Transactions on Information Theory 34(5), pages 1354 to 1359, 1988"
    locator: the whole paper (the window of positions that must be zero)
  - paper: "Pil Joong Lee and Ernest F. Brickell, An observation on the security of McEliece's public-key cryptosystem, Eurocrypt 1988, LNCS 330, pages 275 to 280"
    locator: the whole paper (the enumeration of p errors in the information set that Stern splits in two)
  - paper: "Alexander May, Alexander Meurer and Enrico Thomae, Decoding random linear codes in O(2^(0.054n)), Asiacrypt 2011, LNCS 7073, pages 107 to 124"
    locator: the introduction (Stern's algorithm as the base of the later collision decoders)
---

Stern's algorithm is an [information set decoding](/information-set-decoding/) algorithm for the [syndrome decoding problem](/syndrome-decoding-problem/): given a parity check matrix $H$, a syndrome $s$ and a weight $w$, find $e$ with $He = s$ and $\mathrm{wt}(e) = w$. Like the [Lee-Brickell algorithm](/lee-brickell-algorithm/), it turns $n - k$ random columns into the identity and allows a few errors on the other $k$ columns. It splits those $k$ columns into two halves, puts $p$ errors in each half, and asks that the two partial sums agree on a window of $\ell$ rows. A hash table finds the agreeing pairs, as in a [birthday attack](/birthday-paradox/), so the algorithm never forms most of the pairs. This is the first decoder with a smaller exponent than [Prange's algorithm](/prange-algorithm/). Jacques Stern published it in 1989 for finding codewords of small weight, and this page states it in the decoding form of Bernstein, Lange and Peters (2008).

**Notation.** All vectors and matrices are over $\mathbb{F}_2$. The code has length $n$ and dimension $k$, and $r = n - k$. $H \in \mathbb{F}_2^{r \times n}$ has rank $r$, $s \in \mathbb{F}_2^{r}$, and $\mathrm{wt}(x)$ is the [Hamming weight](/hamming-weight/). $I$ is a set of $r$ positions with $H_I$ invertible, and its complement, the information set, is split into halves $J_1$ and $J_2$ of sizes $k_1 = \lfloor k/2 \rfloor$ and $k_2 = k - k_1$. $\Lambda$ is a set of $\ell$ rows of the reduced matrix, and $x|_\Lambda$ is the restriction of a column vector to those rows. $p$ and $\ell$ are integer parameters, and $\binom{a}{b}$ is the [binomial coefficient](/binomial-coefficient/). The page is about an attack, so there is no security game; the cost is counted in bit operations or word operations on the [word RAM](/word-ram/).

## In plain words

You must find a few flipped bits in a long string from a short fingerprint of them. As in the Lee-Brickell method, you guess a large group of positions, and you allow a few flipped bits outside it.

Stern splits the outside positions into a left half and a right half, with exactly $p$ flipped bits in each. He also asks that a small window of $\ell$ positions inside the group has no flipped bits. On that window, the left part of the fingerprint and the right part must cancel. So he lists all left choices by their value on the window, and looks up each right choice in the list. Only the pairs that match are checked in full.

The lookup skips most of the pairs, and this saving grows with the size of the problem.

## The problem

Input: a matrix $H \in \mathbb{F}_2^{(n-k) \times n}$ of rank $n - k$, a syndrome $s \in \mathbb{F}_2^{n-k}$, a weight $w$, and parameters $p$ and $\ell$ with $2p \le w$ and $\ell \le n - k$. Output: a vector $e \in \mathbb{F}_2^n$ with $He = s$ and $\mathrm{wt}(e) = w$. In cryptanalysis the instance has a planted solution $e^\ast$, and $s = He^\ast$. This is the search form of the [syndrome decoding problem](/syndrome-decoding-problem/).

## The algorithm

```pseudo id=main
STERN(H, s, w, p, ℓ)                       ▷ H is r × n with r = n − k
L1  repeat
L2      I ← a uniform random set of r columns; split the other k columns at random into halves J1, J2
L3      H', s' ← U·H, U·s for an invertible U with U·H_I = identity; Λ ← the first ℓ pivot rows
L4      if H_I is singular then go to L2
L5      T ← a hash table that maps (s' + Σ_{j ∈ A1} H'_j)|Λ to A1, for each A1 ⊆ J1 with |A1| = p
L6      for each A2 ⊆ J2 with |A2| = p do
L7          for each A1 in T at the key (Σ_{j ∈ A2} H'_j)|Λ do
L8              t ← s' + Σ_{j ∈ A1 ∪ A2} H'_j
L9              if wt(t) = w − 2p then
L10                 return e with e_I = t, e_j = 1 for j ∈ A1 ∪ A2, and zeros elsewhere
```

The algebra is the same as for Lee-Brickell. After the elimination, $H' = UH$ has the identity on $I$, and a vector $e$ whose support meets the information set in $A = A_1 \cup A_2$ satisfies $He = s$ exactly when $e_I = s' + \sum_{j \in A} H'_j = t$. Stern asks for $|A_1| = |A_2| = p$ and for $t$ to be zero on the window $\Lambda$. The condition $t|_\Lambda = 0$ is the same as

$$\Big(s' + \sum_{j \in A_1} H'_j\Big)\Big|_\Lambda = \Big(\sum_{j \in A_2} H'_j\Big)\Big|_\Lambda ,$$

so the pairs that pass it are exactly the collisions of two lists, and the hash table of line L5 finds them in time linear in the sizes of the lists plus the number of collisions. Line L9 then checks the full weight. Because the rows of $\Lambda$ pivot on $\ell$ of the random columns of $I$, the window is a random set of $\ell$ positions of $I$ where the error must be zero.

Stern's 1989 paper finds a codeword of small weight in the code with generator matrix $G$; decoding $s$ is the same as finding a low weight word in the code extended by $s$. The decoding form above is the one that Bernstein, Lange and Peters use for attacks on McEliece.

## Example

Take $n = 8$, $k = 4$, $w = 3$, $p = 1$ and $\ell = 1$. The matrix $H$ already has the identity on columns 0 to 3 (0-based), and the other columns, read with row 0 as the low bit, are $H_4 = (1,0,0,1)$, $H_5 = (1,1,0,1)$, $H_6 = (0,1,1,0)$ and $H_7 = (1,0,1,0)$. The error is $e^\ast = \{1, 4, 7\}$, so $s = H_1 + H_4 + H_7 = (0,1,1,1)$.

Suppose line L2 draws $I = \{0, 1, 2, 3\}$, $J_1 = \{4, 5\}$ and $J_2 = \{6, 7\}$, and the window is row 0. Then $U = \mathrm{Id}$ and $s' = s$, and row 0 of $s'$ is 0.

| list | set | value on row 0 |
|---|---|---|
| left, $s' + H'_j$ | $\{4\}$ | $0 + 1 = 1$ |
| left, $s' + H'_j$ | $\{5\}$ | $0 + 1 = 1$ |
| right, $H'_j$ | $\{6\}$ | 0 |
| right, $H'_j$ | $\{7\}$ | 1 |

The right entry $\{6\}$ has key 0 and no partner. The right entry $\{7\}$ has key 1 and two partners. For $A = \{4, 7\}$, $t = s' + H_4 + H_7 = (0, 1, 0, 0)$, of weight $1 = w - 2p$, so the round returns $e$ with $e_1 = e_4 = e_7 = 1$. For $A = \{5, 7\}$, $t = (0,0,0,0)$, of weight 0, and this pair is rejected. Lee-Brickell with $p = 2$ can form up to $1 + 4 + 6 = 11$ sums on these four columns; Stern forms 4 list entries and 2 full candidates.

On random $[60, 30]$ codes with $w = 6$, $p = 1$ and $\ell = 4$, a round succeeds with probability $\binom{15}{1}^2\binom{26}{4}/\binom{60}{6} \approx 0.0672$, so the formula gives about 14.88 rounds. Over 100 random instances with the seed 31415 the implementation below needs 13.72 rounds on average. On 60 instances with the seed 2718, Stern needs 13.8 rounds and forms 588 column sums on average, while Lee-Brickell with $p = 2$ needs 2.8 rounds and forms 1044 sums. At this toy size the Gaussian elimination still dominates the time, so Stern is not faster in seconds; the saving in sums is what grows with $n$.

## Correctness

Each output is a solution: line L10 builds $e$ with $e_I = t$ and ones exactly on $A_1 \cup A_2$, so $UHe = t + \sum_{j \in A_1 \cup A_2} H'_j = s'$, hence $He = s$, and $\mathrm{wt}(e) = (w - 2p) + 2p = w$. The weight count uses $A_1 \cap A_2 = \emptyset$, which holds because $J_1$ and $J_2$ are disjoint. Conversely, if a solution $e^\ast$ has exactly $p$ ones in $J_1$, exactly $p$ in $J_2$, none on the window $\Lambda$, and $H_I$ is invertible, then the pair $(A_1, A_2) = (\mathrm{supp}(e^\ast) \cap J_1, \mathrm{supp}(e^\ast) \cap J_2)$ collides in the table and gives $t = e^\ast_I$, so the round returns a solution. For a uniform random support of $e^\ast$, a round succeeds with probability at least

$$P = \frac{\binom{k_1}{p}\binom{k_2}{p}\binom{n-k-\ell}{w-2p}}{\binom{n}{w}} .$$

The full proof is in the correctness proof below.

## Complexity

**One round.** The elimination costs $O(r^2 n)$ bit operations. Line L5 builds a table of $M_1 = \binom{k_1}{p}$ entries, line L6 forms $M_2 = \binom{k_2}{p}$ sums, and for random columns the expected number of collisions is $M_1 M_2 / 2^\ell$. Each sum or candidate costs $O(r)$ bit operations with incremental sums. With $M = \binom{k/2}{p}$, a round costs

$$O\left(n^3 + nM + n\frac{M^2}{2^\ell}\right).$$

**Number of rounds and total.** The number of rounds is about $1/P$, so the expected time is the cost of a round times $1/P$. The usual choice makes $2^\ell \approx M$, so that the number of collisions is about the size of a list.

**Asymptotics.** For $w = \omega n$, $p = \pi n$ and $\ell = \lambda n$, the exponent is the maximum of the list and collision exponents minus the exponent of $P$, minimized over $\pi$ and $\lambda$. A numerical optimization of this formula gives about $2^{0.1166 n}$ for full distance decoding at the worst rate $R \approx 0.44$, against $2^{0.1207 n}$ for Prange, and about $2^{0.0556 n}$ for half distance decoding. Later algorithms lower the exponent further; see the table on the [information set decoding](/information-set-decoding/) page.

**Space.** The reduced matrix and the hash table: $O(rn + rM) = O(n^2 + nM)$ bits. For cryptographic sizes the table is large, and memory is often the limit in practice.

## Properties

- **Las Vegas.** Every output is correct; only the running time is random.
- **Time against memory.** The table has $\binom{k/2}{p}$ entries. A larger $p$ means fewer rounds but more memory.
- **Exactly p in each half.** Unlike Lee-Brickell, a round accepts only errors with exactly $p$ positions in each half and none on the window. This loses a polynomial factor in the success probability, which the birthday collision more than pays back for large $n$.
- **Generic.** It uses no structure of the code.

## Variants and improvements

- **Collision decoding with tuned steps.** Bernstein, Lange and Peters (2008) reuse most of the elimination from one round to the next, pick several windows, and reuse the sums of the first half. With this code they decoded a ciphertext of the original McEliece parameters ($n = 1024$, $t = 50$).
- **Dumer (1991).** Puts the window inside the enumerated part, which gives the same exponent with a cleaner analysis.
- **Ball collision decoding.** Bernstein, Lange and Peters (2011) allow a few errors inside the window, which gives a small gain in the exponent.
- **Representations.** MMT (2011) and BJMM (2012) split the errors into overlapping parts with many representations, a use of the [representation technique](/representation-technique/), and May-Ozerov (2015) replaces the last collision step with nearest neighbor search.

## When to use it

Use Stern's algorithm as the standard decoder for estimates of the security of code-based schemes when you want a simple algorithm with an exponential gain over Prange. It is the base of most practical attack records on McEliece-type challenges. When memory is very small, Prange or Lee-Brickell are better, and for the most accurate estimates use the later decoders in the family.

## Pitfalls

- **A window that is not error free.** The window rows must pivot on columns of $I$. A window chosen on the original rows of $H$ before elimination has no meaning.
- **Overlapping halves.** If $J_1$ and $J_2$ share a column, a pair can use the same column twice, the column cancels, and the output has the wrong weight.
- **Too small a window.** With $2^\ell$ much smaller than $M$, the number of collisions $M^2/2^\ell$ dominates and the algorithm is slower than Lee-Brickell.
- **Comparing seconds at toy sizes.** For small $n$ the elimination dominates, so a toy timing can make Stern look slower than Lee-Brickell. Count the operations of each part.

## Implementations

The Python code below is for study only. It is not constant time, it uses the random module, and it must not be used to protect real data or to attack real systems. Use a FIPS 140 validated module or libsodium for real cryptography. Stern's algorithm is an attack, not a standard, so there are no official test vectors. The tests compare the output with brute force on 500 small random codes, compare the mean number of rounds with $1/P$, and compare the work with a local copy of Lee-Brickell on the same instances.

## History

Leon proposed in 1988 to require a window of zero positions before a full weight check. Lee and Brickell published in the same year the enumeration of a few errors in the information set. Stern combined both ideas with a collision between two halves, and presented the result in 1988, with publication in 1989. Canteaut and Chabaud improved the steps between rounds in 1998, and Bernstein, Lange and Peters used a tuned version in 2008 to break the original McEliece parameters in practice. The representation decoders from 2011 on are refinements of Stern's collision step.

## References
