---
tag: 97Z92V
kind: technique
slug: information-set-decoding
name: Information set decoding
aliases:
- ISD
area: cryptography/post-quantum
level: advanced
summary: A family of attacks on syndrome decoding. Guess positions that hold most of the error, solve a linear system, and enumerate the few remaining errors. Sets code-based key sizes.
prereqs: [syndrome-decoding-problem, gaussian-elimination]
see_also: [prange-algorithm, lee-brickell-algorithm, stern-algorithm, mceliece-cryptosystem, grover-search, representation-technique, birthday-paradox, code-based-cryptography]
sources:
  - paper: "Eugene Prange, The use of information sets in decoding cyclic codes, IRE Transactions on Information Theory 8(5), pages 5 to 9, 1962"
    locator: the whole paper (decoding with information sets)
  - paper: "Pil Joong Lee and Ernest F. Brickell, An observation on the security of McEliece's public-key cryptosystem, Eurocrypt 1988, LNCS 330, pages 275 to 280"
    locator: the whole paper (a few errors in the information set)
  - paper: "Jeffrey S. Leon, A probabilistic algorithm for computing minimum weights of large error-correcting codes, IEEE Transactions on Information Theory 34(5), pages 1354 to 1359, 1988"
    locator: the whole paper (a window of positions that must be error free)
  - paper: "Jacques Stern, A method for finding codewords of small weight, Coding Theory and Applications, LNCS 388, pages 106 to 113, Springer, 1989"
    locator: the whole paper (the collision of two halves)
  - paper: "Ilya Dumer, On minimum distance decoding of linear codes, Proceedings of the 5th Joint Soviet-Swedish International Workshop on Information Theory, Moscow, pages 50 to 52, 1991"
    locator: the whole paper (the split and merge form of the collision step)
  - paper: "Matthieu Finiasz and Nicolas Sendrier, Security bounds for the design of code-based cryptosystems, Asiacrypt 2009, LNCS 5912, pages 88 to 105"
    locator: Sections 3 and 4 (the generalized ISD algorithm and the lower bounds on its cost that are used to choose parameters)
  - paper: "Alexander May, Alexander Meurer and Enrico Thomae, Decoding random linear codes in O(2^(0.054n)), Asiacrypt 2011, LNCS 7073, pages 107 to 124"
    locator: the abstract and the main theorem (the representation technique, and the exponent 0.054 for half distance decoding)
  - paper: "Anja Becker, Antoine Joux, Alexander May and Alexander Meurer, Decoding random binary linear codes in 2^(n/20): how 1 + 1 = 0 improves information set decoding, Eurocrypt 2012, LNCS 7237, pages 520 to 536"
    locator: the abstract (the exponents 0.0556 for ball collision, 0.0537 for MMT and 0.0494 for BJMM, for half distance decoding)
  - paper: "Alexander May and Ilya Ozerov, On computing nearest neighbors with applications to decoding of binary linear codes, Eurocrypt 2015, LNCS 9056, pages 203 to 228"
    locator: the abstract (nearest neighbor search in place of the last collision step)
  - paper: "Daniel J. Bernstein, Grover vs. McEliece, PQCrypto 2010, LNCS 6061, pages 73 to 80"
    locator: the whole paper (Grover search over information sets, about the square root of the classical cost)
  - paper: "Ghazal Kachigar and Jean-Pierre Tillich, Quantum information set decoding algorithms, PQCrypto 2017, LNCS 10346, pages 69 to 89"
    locator: the introduction, Table 1 (worst case exponents for decoding at the Gilbert-Varshamov distance, classical and quantum)
  - paper: "Daniel J. Bernstein, Tanja Lange and Christiane Peters, Attacking and defending the McEliece cryptosystem, PQCrypto 2008, LNCS 5299, pages 31 to 46"
    locator: Sections 2 to 4 (the syndrome form of the template, and the break of the original McEliece parameters)
  - paper: "Daniel J. Bernstein, Tanja Lange and Christiane Peters, Smaller decoding exponents: ball-collision decoding, Crypto 2011, LNCS 6841, pages 743 to 760"
    locator: the whole paper (errors allowed inside the collision window)
  - paper: "Anne Canteaut and Florent Chabaud, A new algorithm for finding minimum-weight words in a linear code, IEEE Transactions on Information Theory 44(1), 1998"
    locator: the whole paper (the change of one column of the information set per round)
  - paper: "Rodolfo Canto Torres and Nicolas Sendrier, Analysis of information set decoding for a sub-linear error weight, PQCrypto 2016, LNCS 9606, pages 144 to 161"
    locator: the main theorem (for w = o(n) all the ISD variants have the same leading term)
  - paper: "Nicolas Sendrier, Decoding one out of many, PQCrypto 2011, LNCS 7071, pages 51 to 67"
    locator: the whole paper (the gain when any one of many syndromes may be decoded, as for quasi-cyclic codes)
  - url: "https://doi.org/10.6028/NIST.IR.8545"
    title: NIST IR 8545, Status Report on the Fourth Round of the NIST Post-Quantum Cryptography Standardization Process, March 2025
    locator: Section 3.3 (ISD as the main attack on the code-based candidates, and the Grover-like quantum speedup)
---

Information set decoding (ISD) is the family of generic attacks on the [syndrome decoding problem](/syndrome-decoding-problem/): given a parity check matrix $H$, a syndrome $s$ and a weight $w$, find $e$ with $He = s$ and $\mathrm{wt}(e) = w$. Every member of the family repeats the same round. It guesses a set of $n - k$ positions that should hold most of the error, makes the columns of $H$ at those positions the identity by [Gaussian elimination](/gaussian-elimination/), and then enumerates the few errors that the guess allows elsewhere. The members differ only in what they enumerate and how. ISD is the best known attack on the code-based schemes [McEliece](/mceliece-cryptosystem/), [BIKE](/bike/) and [HQC](/hqc/), and its cost sets their key sizes.

**Notation.** All vectors and matrices are over $\mathbb{F}_2$. The code has length $n$, dimension $k$ and rate $R = k/n$, and $r = n - k$. $H \in \mathbb{F}_2^{r \times n}$ has rank $r$, $s \in \mathbb{F}_2^r$, $w = \omega n$, and $\mathrm{wt}(x)$ is the [Hamming weight](/hamming-weight/). $I$ is a set of $r$ positions with $H_I$ invertible, and its complement $J$ (of size $k$) is an *information set*. $H_2$ is the binary entropy function, and a cost $2^{cn + o(n)}$ has *exponent* $c$. This page is about attacks, so there is no security game; costs are counted in bit operations.

## In plain words

A code-based secret is a short list of flipped bits hidden in a long string. You see only a short fingerprint of them, and the fingerprint is linear: each flipped bit adds a known column.

If you knew a set of positions that held all the flipped bits, and the set had as many positions as the fingerprint has bits, you could solve for them with plain linear algebra. You do not know that set, so you guess it. A guess is cheap to test.

All the methods in this family make such guesses again and again. The better ones allow a few flipped bits outside the guessed set, and they look for those few bits in a clever way: by trying all of them, or by matching two half lists. Their cost grows exponentially, but more slowly than plain guessing.

## When it applies

- The problem is to find a vector of low weight $w$ in a coset of a linear code: decoding $s$, or finding a low weight codeword (take $s = 0$ and exclude $e = 0$).
- The code looks random. ISD uses no structure, so it is the reference attack when no structural attack is known. If the code has structure (Reed-Solomon codes, many quasi-cyclic or quasi-dyadic variants), check for algebraic attacks first.
- The weight $w$ is below or near the [Gilbert-Varshamov distance](/gilbert-varshamov-bound/). Far above it, solutions are many and easy to find by linear algebra.

## The template

```pseudo id=main
ISD(H, s, w)                               ▷ H is r × n with r = n − k
L1  repeat
L2      I ← a random set of r column indices; J ← the other k indices
L3      H', s' ← U·H, U·s for an invertible U with U·H_I = identity
L4      if H_I is singular then go to L2
L5      for each candidate set A ⊆ J that the variant enumerates do
L6          t ← s' + Σ_{j ∈ A} H'_j
L7          if wt(t) = w − |A| then
L8              return e with e_I = t, e_j = 1 for j ∈ A, and zeros elsewhere
```

The template is correct for any rule in line L5. After the elimination, a vector $e$ whose support meets $J$ in the set $A$ satisfies $He = s$ exactly when $e_I = s' + \sum_{j \in A} H'_j$. So line L8 always returns a solution of weight $w$. The rule only decides which solutions a round can find, and how much one round costs.

The round succeeds when the true error has a support that the rule enumerates. If the support is uniform random, the success probability of a round is the fraction of $w$-sets that the rule covers, and the expected number of rounds is its inverse.

## Classic examples

The three algorithms on this site use the harness of the implementation below, so you can run them on the same random instances.

| algorithm | sets $A$ in line L5 | success probability of a round |
|---|---|---|
| [Prange](/prange-algorithm/) (1962) | only $\emptyset$ | $\binom{n-k}{w}/\binom{n}{w}$ |
| [Lee-Brickell](/lee-brickell-algorithm/) (1988) | all $A$ with $\lvert A \rvert \le p$ | $\sum_{i \le p}\binom{k}{i}\binom{n-k}{w-i}/\binom{n}{w}$ |
| [Stern](/stern-algorithm/) (1989) | $p$ columns in each half of $J$, matched on $\ell$ rows | $\binom{k/2}{p}^2\binom{n-k-\ell}{w-2p}/\binom{n}{w}$ |

On 40 random $[50, 25]$ codes with $w = 5$ (seed 7 in the tests), the harness measures 37.1 rounds for Prange (formula 39.9), 2.05 rounds and 447 candidates for Lee-Brickell with $p = 2$ (formula 2.0), and 7.7 rounds and 142 candidates for Stern with $p = 1$ and $\ell = 3$ (formula 8.8).

**The exponents.** The table gives the exponent $c$ of the cost $2^{cn}$ for two standard settings. *Full distance* means $w$ at the Gilbert-Varshamov distance $H_2^{-1}(1 - R)$, with the worst rate $R$; *half distance* means half of that, which is the setting of McEliece-type schemes.

| algorithm | full distance, worst $R$ | half distance, worst $R$ |
|---|---|---|
| Prange 1962 | 0.1207 | 0.0575 (computed) |
| Stern 1989 | 0.1166 (computed) | 0.0556 (computed) |
| Dumer 1991 | 0.1164 | |
| Ball collision, Bernstein, Lange and Peters 2011 | | 0.0556 |
| MMT 2011 | 0.1114 | 0.0537 |
| BJMM 2012 | 0.1019 | 0.0494 |
| May-Ozerov 2015 | 0.0966 | |
| quantum Prange, Bernstein 2010 | 0.06035 | |
| quantum, Kachigar and Tillich 2017 | 0.05869 | |

The full distance values are the ones that Kachigar and Tillich (2017) list. The half distance values for ball collision, MMT and BJMM are the ones in the abstract of the BJMM paper; the titles of MMT ($2^{0.054n}$) and BJMM ($2^{n/20}$) round them. The values marked "computed" come from a numerical optimization of the formulas on the Prange and Stern pages, not from a paper. For the parameters of real schemes, $w$ is much smaller than $n$, and then all these algorithms have the same leading term $2^{-w \log_2(1 - R)}$; the gains appear only in the lower order terms (Canto Torres and Sendrier 2016 make this precise).

## Variations

- **Reuse of the elimination.** Change one column of $I$ per round instead of drawing a new set (Canteaut and Chabaud 1998). A round then costs one pivot step.
- **Windows.** Ask $t$ to be zero on $\ell$ positions before the full check (Leon 1988). This lets a collision find the candidates (Stern, Dumer).
- **Representations.** Write the error part on $J$ as a sum of two vectors in many ways and fix one way by a constraint (MMT 2011). Allowing the two parts to overlap with $1 + 1 = 0$ gains more (BJMM 2012). See the [representation technique](/representation-technique/).
- **Nearest neighbors.** Replace the last collision by a search for pairs at a small distance (May and Ozerov 2015).
- **Quantum ISD.** [Grover search](/grover-search/) over the sets $I$ needs about the square root of the number of rounds (Bernstein 2010), which roughly halves the exponent. Quantum walks combined with the enumeration of the classical algorithms gain a little more (Kachigar and Tillich 2017). NIST IR 8545 notes that this is a Grover-like speedup, so the security levels of the code-based schemes take it into account.
- **Structured codes.** For a quasi-cyclic code with circulant blocks of size $r$, every cyclic shift of the target is also a target, which gains a factor of about $\sqrt{r}$ (Sendrier 2011, decoding one out of many). The BIKE specification takes this gain into account.

## Pitfalls

- **Counting singular draws as rounds.** About 71 percent of uniform random square binary matrices are singular. Count the rejected draws apart, or the rounds look 3.46 times too many.
- **Mixing the two orders.** The ones of $t$ belong to the pivot columns of $I$ in pivot order, and the ones of $A$ are columns of $J$. A mismatch gives a vector of the right weight that is not a solution.
- **Using the asymptotic exponent for real parameters.** For $w = o(n)$, as in McEliece, the exponents in the table overstate the gain of the advanced algorithms. Use concrete cost estimates, with memory cost, for real parameters.
- **Forgetting memory.** Stern and its successors need lists of exponential size. Many estimates assume free memory, which is optimistic for large instances.
- **Tiny codes.** On very small codes, a solution can use dependent columns and lie in no invertible $H_I$. Tests against brute force must allow for this.

## Exercises

1. Show that for $p = 0$ the Lee-Brickell rule is Prange's rule, and that for every $p$ a Lee-Brickell round succeeds whenever a Prange round with the same set $I$ succeeds.
2. For $[60, 30]$ and $w = 6$, compute the expected number of rounds of Prange, of Lee-Brickell with $p = 2$, and of Stern with $p = 1$ and $\ell = 4$. Then run the harness and compare. (The formulas give about 84.3, 2.98 and 14.88.)
3. Show that the exponent of Prange is $H_2(\omega) - (1 - R)H_2(\omega/(1 - R))$, and find the worst rate at the Gilbert-Varshamov distance numerically. (It is about $R = 0.45$, with $c \approx 0.1207$.)

## References
