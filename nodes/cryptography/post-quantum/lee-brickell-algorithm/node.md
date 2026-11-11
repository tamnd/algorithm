---
tag: XC780W
kind: algorithm
slug: lee-brickell-algorithm
name: Lee-Brickell algorithm
aliases:
- Lee-Brickell attack
area: cryptography/post-quantum
level: advanced
summary: Prange's information set decoder that also allows p errors outside the chosen identity columns and tries all of them. With p = 2 it saves a polynomial factor over Prange.
solves: [syndrome-decoding-problem]
model: word-ram
complexity:
  vars: {n: the code length, k: the code dimension, w: the error weight, p: the number of errors guessed in the information set, N: "the expected number of rounds, binomial(n, w) over the sum for i up to p of binomial(k, i) binomial(n - k, w - i)"}
  time: {expected: O((n^3 + n k^p) N), best: O(n^3 + n k^p)}
  space: {extra: O(n^2)}
properties: {deterministic: false, randomized: true}
history:
  year: 1988
  people: [Pil Joong Lee, Ernest F. Brickell]
  note: Lee and Brickell presented the attack at Eurocrypt 1988 as an observation on the security of the McEliece cryptosystem. Their analysis showed that two guessed errors is the best choice.
prereqs: [prange-algorithm]
see_also: [stern-algorithm, information-set-decoding, syndrome-decoding-problem, mceliece-cryptosystem, lexicographic-combinations]
sources:
  - paper: "Pil Joong Lee and Ernest F. Brickell, An observation on the security of McEliece's public-key cryptosystem, Eurocrypt 1988, LNCS 330, pages 275 to 280"
    locator: the whole paper (the attack with j errors among the k chosen positions, and the analysis that gives j = 2 as the best value)
  - paper: "Daniel J. Bernstein, Tanja Lange and Christiane Peters, Attacking and defending the McEliece cryptosystem, PQCrypto 2008, LNCS 5299, pages 31 to 46"
    locator: Section 2 (information set decoding in syndrome form, of which this page uses the Lee-Brickell step)
  - paper: "Christiane Peters, Information-set decoding for linear codes over Fq, PQCrypto 2010, LNCS 6061, pages 81 to 94"
    locator: Section 3 (the Lee-Brickell algorithm stated in the parity check form and its cost)
  - paper: "Eugene Prange, The use of information sets in decoding cyclic codes, IRE Transactions on Information Theory 8(5), pages 5 to 9, 1962"
    locator: the whole paper (the algorithm that this page extends)
  - book: isbn:9783540887010
    title: Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009
    locator: the chapter Code-based cryptography by Raphael Overbeck and Nicolas Sendrier (decoding attacks and information set decoding)
---

The Lee-Brickell algorithm is an [information set decoding](/information-set-decoding/) algorithm for the [syndrome decoding problem](/syndrome-decoding-problem/): given a parity check matrix $H$, a syndrome $s$ and a weight $w$, find $e$ with $He = s$ and $\mathrm{wt}(e) = w$. It extends [Prange's algorithm](/prange-algorithm/). Prange needs all $w$ errors to lie on the $n - k$ columns that it turns into the identity. Lee-Brickell also accepts up to $p$ errors on the other $k$ columns, the information set, and tries every choice of them. A round now costs more, but it succeeds much more often. Pil Joong Lee and Ernest Brickell published it in 1988 as an attack on the [McEliece cryptosystem](/mceliece-cryptosystem/), and they showed that $p = 2$ is the best choice.

**Notation.** All vectors and matrices are over $\mathbb{F}_2$. The code has length $n$ and dimension $k$, and $r = n - k$. $H \in \mathbb{F}_2^{r \times n}$ has rank $r$, $s \in \mathbb{F}_2^{r}$, and $\mathrm{wt}(x)$ is the [Hamming weight](/hamming-weight/). $I$ is a set of $r$ positions with $H_I$ invertible, $J$ is its complement (the information set, of size $k$), and $p$ is a small integer parameter with $0 \le p \le w$. $\binom{a}{b}$ is the [binomial coefficient](/binomial-coefficient/). This page is about an attack, so there is no security game; the cost is counted in bit operations or in operations on machine words of the [word RAM](/word-ram/).

## In plain words

You must find a few flipped bits in a long string, and you only see a short fingerprint of them. Prange's method guesses a large group of positions and hopes that every flipped bit is inside it. If one flipped bit is outside, the guess is lost.

Lee and Brickell keep the same guess but allow a few flipped bits, say two, outside the group. They try every way to put one or two flipped bits outside. Each of these tries is a cheap addition of columns, and each one gives a candidate that they check by its weight.

The tries cost some work in every round. But a guess with one or two flipped bits outside is much more common than a perfect guess, so far fewer rounds are needed. With two bits outside the gain is the best.

## The problem

Input: a matrix $H \in \mathbb{F}_2^{(n-k) \times n}$ of rank $n - k$, a syndrome $s \in \mathbb{F}_2^{n-k}$, a weight $w$ and a parameter $p$. Output: a vector $e \in \mathbb{F}_2^n$ with $He = s$ and $\mathrm{wt}(e) = w$. In cryptanalysis the instance has a planted solution $e^\ast$: $H$ is a public key or a random matrix, and $s = He^\ast$. This is the search form of the [syndrome decoding problem](/syndrome-decoding-problem/).

## The algorithm

```pseudo id=main
LEE-BRICKELL(H, s, w, p)                   ▷ H is r × n with r = n − k
L1  repeat
L2      I ← a uniform random set of r column indices; J ← the other k indices
L3      H', s' ← U·H, U·s for an invertible U with U·H_I = identity
L4      if H_I is singular then go to L2
L5      for each set A ⊆ J with |A| ≤ p do
L6          t ← s' + the sum of the columns H'_j for j ∈ A
L7          if wt(t) = w − |A| then
L8              e ← the vector with e_I = t, e_j = 1 for j ∈ A, and zeros elsewhere
L9              return e
```

Lines L2 to L4 are the same as in Prange's algorithm. Gauss-Jordan elimination on $[H \mid s]$, pivoting only on the columns of $I$, gives $H' = UH$ with $H'_I = \mathrm{Id}$ and $s' = Us$. Now take a vector $e$ whose support meets $J$ in the set $A$. Then $UHe = e_I + \sum_{j \in A} H'_j$, so $He = s$ holds exactly when $e_I = s' + \sum_{j \in A} H'_j = t$. The candidate is a solution of weight $w$ when $\mathrm{wt}(t) = w - |A|$. Line L5 lists the sets $A$ in the order of size, and the implementation adds one column at a time, so one candidate costs at most $p$ additions of $r$-bit columns.

With $p = 0$, line L5 tries only $A = \emptyset$ and the algorithm is Prange's algorithm.

## Example

Take the $[7, 4]$ [Hamming code](/hamming-code/) with $w = 1$ and $p = 1$. Column $j$ of $H$ is the binary form of $j$ with the low bit in row 1:

$$H = \begin{pmatrix} 1&0&1&0&1&0&1 \\ 0&1&1&0&0&1&1 \\ 0&0&0&1&1&1&1 \end{pmatrix}, \qquad e^\ast = (0,0,0,0,1,0,0), \qquad s = He^\ast = (1, 0, 1)^T .$$

Suppose line L2 draws $I = \{1, 2, 4\}$ (1-based), so $J = \{3, 5, 6, 7\}$. The columns of $I$ are already the identity, so $U = \mathrm{Id}$, $H' = H$ and $s' = (1, 0, 1)$.

| $A$ | $t = s' + \sum_{j \in A} H'_j$ | $\mathrm{wt}(t)$ | target $w - \lvert A \rvert$ | result |
|---|---|---|---|---|
| $\emptyset$ | $(1, 0, 1)$ | 2 | 1 | no |
| $\{3\}$ | $(1,0,1) + (1,1,0) = (0, 1, 1)$ | 2 | 0 | no |
| $\{5\}$ | $(1,0,1) + (1,0,1) = (0, 0, 0)$ | 0 | 0 | $e = e_5$, success |

Prange's algorithm fails in this round, because the error at position 5 is outside $I$. Lee-Brickell with $p = 1$ finds it in the same round. With $w = 1$ and $p = 1$ every round succeeds, because the single error is either in $I$ or in $J$.

On a larger scale, for random $[60, 30]$ codes with $w = 6$, Prange needs $\binom{60}{6}/\binom{30}{6} \approx 84.3$ rounds, while Lee-Brickell with $p = 2$ needs about $1/0.3354 \approx 2.98$ rounds. Over 120 random instances with the seed 4242, the implementation below needs 3.26 rounds on average. On 40 random $[50, 25]$ instances with $w = 5$ and the seed 99, it needs 2.1 rounds with $p = 2$ and 40.7 rounds with $p = 0$, against the predicted 2.0 and 39.9.

## Correctness

Each output is a solution: by the identity $UHe = e_I + \sum_{j \in A} H'_j$, the vector built in line L8 has $UHe = t + \sum_{j \in A} H'_j + \sum_{j \in A} H'_j = s'$, so $He = s$, and its weight is $\mathrm{wt}(t) + |A| = w$. Conversely, if a solution $e^\ast$ has at most $p$ ones in $J$ and $H_I$ is invertible, the round reaches $A = \mathrm{supp}(e^\ast) \cap J$ or returns earlier, and for that $A$ the vector $t$ equals $e^\ast_I$. If the support of $e^\ast$ is a uniform random $w$-set, a round with an invertible $H_I$ succeeds with probability at least

$$P_p = \frac{\sum_{i=0}^{p} \binom{k}{i}\binom{n-k}{w-i}}{\binom{n}{w}} .$$

The full proof is in the correctness proof below.

## Complexity

**One round.** The elimination costs $O(r^2 n)$ bit operations, as in Prange. The loop of line L5 tries $\sum_{i \le p} \binom{k}{i} = O(k^p)$ sets, and each one costs $O(r)$ bit operations with the incremental sums. So a round costs $O(n^3 + n k^p)$.

**Number of rounds.** For a fixed instance the rounds are independent trials, and averaged over the error a round succeeds with probability $P_p$. The standard estimate of the number of rounds is $1/P_p$, and the expected time is

$$O\left((n^3 + n k^p) \cdot \frac{\binom{n}{w}}{\sum_{i=0}^{p} \binom{k}{i}\binom{n-k}{w-i}}\right).$$

**Why p = 2.** Going from $p - 1$ to $p$ multiplies the work per round by about $k$ once $k^p$ dominates the elimination, and it divides the number of rounds by about $\binom{k}{p}\binom{r}{w-p} / \binom{k}{p-1}\binom{r}{w-p+1}$. In a simple cost model for the Classic McEliece parameter set mceliece348864 ($n = 3488$, $k = 2720$, $w = 64$), with $r^2 n$ for the elimination and $r$ per added column, the total is about $2^{173.7}$ bit operations for $p = 0$, $2^{165.8}$ for $p = 1$, $2^{160.8}$ for $p = 2$ and $2^{164.4}$ for $p = 3$. The minimum is at $p = 2$, as Lee and Brickell found for the original parameters.

**Asymptotics.** For a constant $p$ the number of rounds changes only by a polynomial factor, so the exponent is the same as the one of Prange (about 0.1207 for full distance decoding at the worst rate). The first gain in the exponent comes from [Stern's algorithm](/stern-algorithm/).

**Space.** One copy of $H$ and $s$, and the $k$ columns of $H'$: $O(rn) = O(n^2)$ bits.

## Properties

- **Las Vegas.** Every output is correct. Only the running time is random.
- **Contains Prange.** The case $p = 0$ is Prange's algorithm, and for every $p$ the set of rounds that succeed contains the rounds that succeed for Prange.
- **Little memory.** The only extra storage is the reduced matrix. The algorithm keeps no lists, unlike Stern's algorithm, so it is easy to run in parallel.
- **Generic.** It uses no structure of the code, so it applies to any binary linear code.

## Variants and improvements

- **[Stern](/stern-algorithm/) (1989).** Split the information set in two halves, put $p$ errors in each, and require $\ell$ zero positions of $t$ so that a birthday collision finds the pairs. This gives a gain in the exponent.
- **Leon (1988).** Leon's algorithm for low weight codewords requires a window of $\ell$ positions of $t$ to be zero before it computes the full weight. It is the same early abort that Stern uses.
- **Lee-Brickell over $\mathbb{F}_q$.** Peters (2010) gives the algorithm and its cost for codes over larger fields, where each set $A$ also has $(q-1)^{|A|}$ choices of the nonzero values.
- **Quantum version.** [Grover search](/grover-search/) over the sets $I$ gives a square root of the number of rounds, as for Prange (Bernstein 2010).

## When to use it

Use the Lee-Brickell algorithm when you need a decoder that is a little faster than Prange and still needs no memory beyond the matrix, or as a quick and simple upper bound on the attack cost of a code-based scheme. For real security estimates, use the decoders with an exponential gain: Stern, MMT, BJMM and their successors (see [information set decoding](/information-set-decoding/)).

## Pitfalls

- **The target weight is w minus |A|.** Line L7 must compare $\mathrm{wt}(t)$ with $w - |A|$, not with $w$. Testing against $w$ finds a vector of the wrong weight.
- **Building the output from the wrong columns.** The ones of $t$ belong to the pivot columns $I$ in pivot order, and the ones of $A$ are columns of $J$. Mixing the two orders gives a vector with the right weight that is not a solution.
- **A large p.** The work per round grows as $k^p$, so $p > 2$ is slower for every parameter set of practical interest, even though each round succeeds more often.
- **Counting the singular draws as rounds.** As for Prange, count the draws with a singular $H_I$ apart from the rounds, or the measured number of rounds is too large by a constant factor.

## Implementations

The Python code below is for study only. It is not constant time, it uses the random module, and it must not be used to protect real data or to attack real systems. Use a FIPS 140 validated module or libsodium for real cryptography. The Lee-Brickell algorithm is an attack, not a standard, so there are no official test vectors. The tests compare the output with brute force on 500 small random codes, compare the mean number of rounds with $1/P_p$, and compare the rounds of $p = 2$ and $p = 0$ on the same instances.

## History

McEliece's 1978 report estimated the cost of decoding by guessing error-free positions. Lee and Brickell published their observation at Eurocrypt 1988: allowing a few errors among the guessed positions and correcting them by trial lowers the cost, with the best choice at two errors. In the same year Leon proposed a related algorithm for finding low weight codewords, and in 1989 Stern combined the two ideas with a birthday collision.

## References
