---
tag: HA6A5G
kind: algorithm
slug: prange-algorithm
name: Prange's algorithm
aliases:
- Prange's information set decoding
- plain information set decoding
area: cryptography/post-quantum
level: advanced
summary: The first information set decoder. Pick n - k random positions, make them the identity by Gaussian elimination, and win when all w errors lie there. Expected C(n, w)/C(n - k, w) rounds.
solves: [syndrome-decoding-problem]
model: word-ram
complexity:
  vars: {n: the code length, k: the code dimension, w: the error weight, N: "the expected number of rounds, binomial(n, w) over binomial(n - k, w)"}
  time: {expected: O(n^3 N), best: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: false, randomized: true}
history:
  year: 1962
  people: [Eugene Prange]
  note: Prange described decoding with information sets for cyclic codes in the IRE Transactions on Information Theory in 1962. It is the base of all later information set decoders.
prereqs: [information-set-decoding, linear-system-modulo-2, binomial-coefficient]
see_also: [lee-brickell-algorithm, stern-algorithm, syndrome-decoding-problem, mceliece-cryptosystem, grover-search, gaussian-elimination]
sources:
  - paper: "Eugene Prange, The use of information sets in decoding cyclic codes, IRE Transactions on Information Theory 8(5), pages 5 to 9, 1962"
    locator: the whole paper (decoding by a choice of information sets that are free of errors)
  - paper: "Daniel J. Bernstein, Tanja Lange and Christiane Peters, Attacking and defending the McEliece cryptosystem, PQCrypto 2008, LNCS 5299, pages 31 to 46"
    locator: Section 2 (the information set decoding framework in syndrome form that this page follows)
  - paper: "Daniel J. Bernstein, Grover vs. McEliece, PQCrypto 2010, LNCS 6061, pages 73 to 80"
    locator: the whole paper (Grover search over information sets takes about the square root of the classical number of iterations)
  - paper: "Ghazal Kachigar and Jean-Pierre Tillich, Quantum information set decoding algorithms, PQCrypto 2017, LNCS 10346, pages 69 to 89"
    locator: the introduction (the worst case exponent 0.1207 of Prange for decoding at the Gilbert-Varshamov distance, and 0.06035 for the quantum version)
  - paper: "Anne Canteaut and Florent Chabaud, A new algorithm for finding minimum-weight words in a linear code, IEEE Transactions on Information Theory 44(1), 1998"
    locator: the whole paper (the change of one column of the information set per round)
  - paper: "Robert J. McEliece, A public-key cryptosystem based on algebraic coding theory, DSN Progress Report 42-44, Jet Propulsion Laboratory, 1978"
    locator: the security discussion (the attack that guesses k error-free positions)
  - book: isbn:9783540887010
    title: Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009
    locator: the chapter Code-based cryptography by Raphael Overbeck and Nicolas Sendrier (decoding attacks and information set decoding)
---

Prange's algorithm is the first and simplest [information set decoding](/information-set-decoding/) algorithm for the [syndrome decoding problem](/syndrome-decoding-problem/): given a parity check matrix $H$, a syndrome $s$ and a weight $w$, find $e$ with $He = s$ and $\mathrm{wt}(e) = w$. In each round it picks $n - k$ random positions, uses [Gaussian elimination](/linear-system-modulo-2/) to turn the columns of $H$ at those positions into the identity, and reads off $e$ if all $w$ errors happen to lie there. A round succeeds with probability $\binom{n-k}{w}/\binom{n}{w}$, so the expected number of rounds is the inverse of that. Eugene Prange proposed the idea in 1962, and every later decoder in the family ([Lee-Brickell](/lee-brickell-algorithm/), [Stern](/stern-algorithm/) and their successors) is a refinement of it.

**Notation.** All vectors and matrices are over $\mathbb{F}_2$. The code has length $n$ and dimension $k$, and $r = n - k$. $H \in \mathbb{F}_2^{r \times n}$ has full rank $r$, $s \in \mathbb{F}_2^{r}$, and $\mathrm{wt}(x)$ is the [Hamming weight](/hamming-weight/). For a set $I$ of positions, $H_I$ is the $r \times |I|$ submatrix of the columns in $I$, and $x_I$ is the restriction of $x$ to $I$. An *information set* is a set $J$ of $k$ positions whose complement $I$ has an invertible $H_I$. This page is about an attack; there is no security game, and the cost is in operations on bits or on machine words of the [word RAM](/word-ram/).

## In plain words

You must find a few flipped bits in a long string, and you only see a short fingerprint of them. If you knew which handful of positions contained all the flipped bits, the fingerprint would give them to you by plain equation solving, because the equations then have as many unknowns as there are equations.

You do not know those positions. So you guess a large random group of positions, about half of them, and assume that all the flipped bits are inside the group. You solve the equations. If the answer has exactly the right number of flipped bits, you are done. If not, the guess was wrong, and you guess again.

Each guess is cheap. The catch is that a lucky guess is rare when there are many flipped bits, and the number of guesses grows exponentially. That number sets the key sizes of code-based cryptography.

## The problem

Input: a full rank matrix $H \in \mathbb{F}_2^{(n-k) \times n}$, a syndrome $s \in \mathbb{F}_2^{n-k}$ and a weight $w$ with $0 \le w \le n - k$. Output: a vector $e \in \mathbb{F}_2^n$ with $He = s$ and $\mathrm{wt}(e) = w$. In cryptanalysis the instance has a planted solution: $H$ is a public key or a random matrix, and $s = He^\ast$ for a secret $e^\ast$ of weight $w$. This is the search form of the [syndrome decoding problem](/syndrome-decoding-problem/).

## The algorithm

```pseudo id=main
PRANGE(H, s, w)                            ▷ H is r × n with r = n − k
L1  repeat
L2      I ← a uniform random set of r column indices
L3      U ← an invertible r × r matrix with U·H_I = identity, by Gaussian elimination
L4      if H_I is singular then go to L2       ▷ not a valid information set
L5      s' ← U·s
L6      if wt(s') = w then
L7          e ← the vector with e_I = s' and zeros elsewhere
L8          return e
```

Line L3 does not build $U$ as a matrix. It runs Gauss-Jordan elimination on the rows of $H$ with $s$ as an extra column, and pivots only on the columns in $I$. When it ends, row $i$ has a 1 in column $I_i$ and a 0 in every other column of $I$, and the extra column holds $s' = Us$. If a column of $I$ has no pivot, $H_I$ is singular, and line L4 draws a new set. The equation $He = s$ holds if and only if $UHe = s'$, because $U$ is invertible. For a vector $e$ that is zero outside $I$, $UHe = UH_I e_I = e_I$. So the only candidate supported on $I$ is $e_I = s'$, and it is a solution of the right weight exactly when $\mathrm{wt}(s') = w$.

The test of line L6 is all the algorithm can check. The same set $I$ that holds all errors gives $\mathrm{wt}(s') = w$; a set $I$ that misses an error gives a vector $s'$ of some other weight in almost all cases, and if it gives weight $w$ anyway, that vector is still a correct solution.

## Example

Take the $[7, 4]$ [Hamming code](/hamming-code/). Column $j$ of $H$ (for $j = 1, \ldots, 7$) is the binary form of $j$ with the low bit in row 1:

$$H = \begin{pmatrix} 1&0&1&0&1&0&1 \\ 0&1&1&0&0&1&1 \\ 0&0&0&1&1&1&1 \end{pmatrix}, \qquad e^\ast = (0,0,0,0,1,0,0), \qquad s = He^\ast = (1, 0, 1)^T .$$

Here $n = 7$, $k = 4$, $r = 3$ and $w = 1$.

| round | $I$ (1-based) | elimination | $s'$ | $\mathrm{wt}(s')$ | result |
|---|---|---|---|---|---|
| 1 | $\{1, 2, 4\}$ | $H_I$ is already the identity, $U = 1$ | $(1, 0, 1)$ | 2 | fail |
| 2 | $\{1, 2, 5\}$ | pivot on column 5 in row 3, then row 1 ← row 1 + row 3 | $(0, 0, 1)$ | 1 | $e_5 = 1$, success |

In round 1 the error at position 5 is outside $I$, and the candidate $(1,0,0,1,0,0,0)$ supported to $I$ has weight 2, so it is rejected. In round 2 the error is inside $I$, and the third row, whose pivot is column 5, gives $e_5 = 1$. The chance of success in one round is $\binom{3}{1}/\binom{7}{1} = 3/7$, so the expected number of rounds is $7/3 \approx 2.33$.

On a larger scale, for random $[60, 30]$ codes with $w = 4$ the formula gives $\binom{60}{4}/\binom{30}{4} = 487635/27405 \approx 17.79$ rounds. Over 150 random instances with the seed 12345, the implementation below needs 18.09 rounds on average, within the sampling error of about 8 percent for this many instances. For $[60, 30]$ with $w = 6$ the formula gives 84.3 rounds, and for $[100, 50]$ with $w = 8$ it gives 346.6 rounds.

## Correctness

Each output is a solution: line L7 builds $e$ with $e_I = s'$ and zero elsewhere, so $UHe = s'$, so $He = s$, and $\mathrm{wt}(e) = \mathrm{wt}(s') = w$. Conversely, if some solution $e^\ast$ has its support inside $I$ and $H_I$ is invertible, then $s' = e^\ast_I$ and the round returns $e^\ast$. If $e^\ast$ has a uniform random support of size $w$ that is independent of the choice of $I$, a round with an invertible $H_I$ succeeds with probability at least $\binom{n-k}{w}/\binom{n}{w}$, with equality when $e^\ast$ is the only solution. The full proof is in the correctness proof below.

## Complexity

**One round.** Gauss-Jordan elimination on an $r \times n$ matrix takes at most $r^2$ row additions, each on $n + 1$ bits, so $O(r^2 n) = O(n^3)$ bit operations, or $O(r^2 n / b)$ word operations with $b$-bit words. The rows are $n$-bit integers in the implementation, so one row addition is one XOR of big integers.

**Number of rounds.** For a uniform random $H$ the matrix $H_I$ is invertible with probability $\prod_{i=1}^{r}(1 - 2^{-i}) > 0.288$, so the rejected draws of line L4 cost at most a constant factor. For a fixed instance the accepted rounds are independent trials with the same success probability, so their number is geometric. Averaged over the error, one round succeeds with probability $P = \binom{n-k}{w}/\binom{n}{w}$, and the standard estimate of the number of rounds is $1/P$. The expected time is therefore

$$O\left(n^3 \cdot \frac{\binom{n}{w}}{\binom{n-k}{w}}\right).$$

For the Classic McEliece parameter set mceliece348864 ($n = 3488$, $k = 2720$, $w = 64$) the number of rounds is $\binom{3488}{64}/\binom{768}{64} \approx 2^{142.8}$.

**Asymptotics.** Let $R = k/n$ and $w = \omega n$, and let $H_2$ be the binary entropy function. Since $\binom{n}{\omega n} = 2^{n H_2(\omega) + o(n)}$, the number of rounds is $2^{c n + o(n)}$ with $c = H_2(\omega) - (1-R) H_2\left(\frac{\omega}{1-R}\right)$. For full distance decoding, $\omega$ is the relative [Gilbert-Varshamov distance](/gilbert-varshamov-bound/) $H_2^{-1}(1-R)$, and the worst rate gives $c \approx 0.1207$ at $R \approx 0.45$ (Kachigar and Tillich 2017 give 0.1207). For half that distance, the worst case is $c \approx 0.0575$.

**Space.** The algorithm stores one copy of $H$ and $s$: $O(rn) = O(n^2)$ bits.

## Properties

- **Las Vegas.** The output is always correct. Only the running time is random, and an unlucky run can take any number of rounds.
- **No memory beyond the matrix.** Unlike [Stern's algorithm](/stern-algorithm/) it keeps no lists, so it parallelizes with no communication: each processor tries its own sets $I$.
- **Generic.** It uses no structure of the code. It attacks a [McEliece](/mceliece-cryptosystem/) public key, a quasi-cyclic code of [BIKE](/bike/) or [HQC](/hqc/), and a random code in the same way.
- **Finds only spread solutions.** A solution whose columns are linearly dependent, for example one that uses a zero column of $H$, lies inside no invertible $H_I$, so this form of the algorithm cannot return it. For random codes of cryptographic size this case does not occur in practice, but the tests must allow for it on tiny codes.

## Variants and improvements

- **[Lee-Brickell](/lee-brickell-algorithm/) (1988).** Allow $p$ errors in the information set and enumerate them. With $p = 2$, the cost drops by a polynomial factor.
- **[Stern](/stern-algorithm/) (1989).** Split the information set in two halves and match on $\ell$ bits with a birthday collision. This gives the first exponential gain in the exponent.
- **Reuse of the elimination.** Canteaut and Chabaud (1998) change one column of $I$ at a time, so a round costs one pivot step, $O(rn)$, instead of a full elimination.
- **Quantum Prange.** [Grover search](/grover-search/) over the sets $I$ needs about $\sqrt{1/P}$ evaluations of the round, which halves the exponent to about 0.06035 (Bernstein 2010).
- **Representations and nearest neighbors.** MMT, BJMM and May-Ozerov refine the enumeration further; see [information set decoding](/information-set-decoding/) for the table of exponents.

## When to use it

Use Prange's algorithm as the baseline estimate of the security of a code-based scheme, and as the first decoder to implement, because it has no parameters to tune and it is easy to prove correct. For a real estimate of the attack cost, use the later algorithms: Lee-Brickell gains a polynomial factor, and Stern and its successors gain in the exponent. When memory is very limited, Prange and Lee-Brickell remain the decoders of choice, because they need no lists.

## Pitfalls

- **Testing the weight wrong.** Line L6 must compare $\mathrm{wt}(s')$ with $w$. A program that instead checks $He = s$ for a vector built from the wrong columns, or that reads $e$ from $s$ instead of $s' = Us$, returns garbage.
- **Counting the singular draws.** If line L4 counts a singular $H_I$ as a failed round, the measured number of rounds is larger than $1/P$ by the factor $1/\Pr[H_I \text{ invertible}] \approx 3.46$. Count the rejected draws apart from the rounds.
- **A rank deficient $H$.** If $H$ has rank less than $r$, no $H_I$ is invertible and the loop of lines L1 to L4 never ends. Check the rank first, or bound the number of draws, as the implementation does.
- **Choosing $I$ from a non-uniform rule.** Taking the first $r$ pivot columns of a column-permuted matrix gives a set that is not uniform. The algorithm still works, but the success probability no longer equals the formula.

## Implementations

The Python code below is for study only. It is not constant time, it uses the random module, and it must not be used to protect real data or to attack real systems. Use a FIPS 140 validated module or libsodium for real cryptography.

## History

Prange published the method in 1962 to decode cyclic codes with a computer of the time. McEliece's 1978 report already estimated the cost of an attack that guesses $k$ error-free positions of a ciphertext, and Lee and Brickell analyzed it as an attack in 1988. Bernstein, Lange and Peters used its refinements in 2008 to break the original McEliece parameters ($n = 1024$, $t = 50$) in practice. Bernstein showed in 2010 that Grover search gives a square root speedup of the number of rounds.

## References
