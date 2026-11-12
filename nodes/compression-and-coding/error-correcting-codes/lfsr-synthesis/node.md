---
tag: FQKAS9
kind: problem
slug: lfsr-synthesis
name: Linear feedback shift register synthesis
aliases:
- LFSR synthesis
- shift-register synthesis
- linear complexity computation
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Find a shortest linear recurrence, or LFSR, that generates a given finite sequence over a field. Its length is the linear complexity of the sequence.
prereqs: [linear-feedback-shift-register, polynomial-ring]
see_also: [berlekamp-massey, lfsr, stream-cipher, reed-solomon-decoding, polynomial-extended-euclidean-algorithm, linear-recurrence-nth-term, toeplitz-system-solving, wiedemann-algorithm]
sources:
  - paper: doi:10.1109/TIT.1969.1054260
    title: J. L. Massey, Shift-register synthesis and BCH decoding, IEEE Transactions on Information Theory 15(1), 1969
    locator: pp. 122 to 127 (the synthesis problem, the length change theorem, and the uniqueness of the shortest register when 2L is at most N)
  - paper: doi:10.1090/S0025-5718-1975-0369276-7
    title: W. H. Mills, Continued fractions and linear recurrences, Mathematics of Computation 29(129), 1975
    locator: pp. 173 to 180 (the continued fraction algorithm that finds the shortest linear recurrence)
  - book: isbn:9780387168708
    title: Rainer A. Rueppel, Analysis and Design of Stream Ciphers, Springer-Verlag, 1986
    locator: The chapter on linear complexity (the linear complexity profile, the number of sequences of each linear complexity and the expected value for random sequences)
  - paper: doi:10.1137/0214038
    title: J. A. Reeds and N. J. A. Sloane, Shift-register synthesis (modulo m), SIAM Journal on Computing 14(3), 1985
    locator: The extension of shift-register synthesis to sequences over the integers modulo m
---

Linear feedback shift register synthesis asks for the shortest linear recurrence $s_j = -(c_1 s_{j-1} + \cdots + c_L s_{j-L})$ that generates a given finite sequence $s_0, \ldots, s_{N-1}$ over a field. The least such $L$ is the *linear complexity* of the sequence. The [Berlekamp-Massey algorithm](/berlekamp-massey/) solves the problem in $O(N^2)$ field operations, and the extended Euclidean algorithm gives an equivalent method. The problem appears in two places: in the decoding of [BCH](/bch-code/) and [Reed-Solomon](/reed-solomon-decoding/) codes, where the shortest recurrence of the syndromes is the error locator, and in the analysis of [stream ciphers](/stream-cipher/), where a short recurrence means a weak keystream.

## In plain words

A shift register holds a few numbers. At each step it puts out the oldest number, mixes the numbers it holds with fixed weights to make a new number, and pushes the new number in. Each output is then a fixed mix of the few outputs just before it. Now turn this around. You see some outputs, and you want the smallest register, with its weights, that could have produced them. The size of that smallest register measures how predictable the outputs are. A truly random list needs a register about half as long as the list. A list with hidden structure can need a much shorter one, and then the register predicts all later outputs.

## Definition

Let $F$ be a field and $s = (s_0, \ldots, s_{N-1}) \in F^N$. An LFSR of length $L \ge 0$ is a connection polynomial $C(x) = 1 + c_1 x + \cdots + c_L x^L \in F[x]$; the top coefficient $c_L$ may be zero. It *generates* $s$ if

$$s_j + c_1 s_{j-1} + \cdots + c_L s_{j-L} = 0 \qquad \text{for } L \le j < N.$$

**Input.** A field $F$ and a sequence $s \in F^N$.

**Output.** The *linear complexity* $L_N(s)$, the least $L$ such that an LFSR of length $L$ generates $s$, and one such $C(x)$.

The *linear complexity profile* is the list $L_1(s), L_2(s), \ldots, L_N(s)$ of the linear complexities of the prefixes.

**Polynomial form.** Write $S(x) = \sum_{i<N} s_i x^i$. Then $(L, C)$ generates $s$ if and only if

$$C(x)\, S(x) \equiv P(x) \pmod{x^N} \quad \text{for some } P \text{ with } \deg P < L,$$

because the coefficient of $x^j$ in $C S$ for $L \le j < N$ is the left side of the recurrence. So the problem asks for the rational function $P/C$ with the least $\max(\deg C, \deg P + 1)$ whose power series agrees with $S$ up to $x^{N-1}$: a Padé approximation problem.

## Variants

- **Infinite periodic sequences.** For a sequence of period $T$, the linear complexity is $T - \deg \gcd(S_T(x), x^T - 1)$, where $S_T$ is the polynomial of one period. This takes one GCD computation.
- **The profile.** Compute $L_1, \ldots, L_N$ for all prefixes. The [Berlekamp-Massey](/berlekamp-massey/) algorithm gives it at no extra cost.
- **The key equation of decoding.** Find $\Lambda$ and $\Omega$ with $\Lambda(x) S(x) \equiv \Omega(x) \pmod{x^{2t}}$, $\deg \Omega < \deg \Lambda \le t$. This is the problem for the syndrome sequence with the extra degree conditions of [Reed-Solomon decoding](/reed-solomon-decoding/).
- **Rings that are not fields.** Reeds and Sloane (1985) solve the problem over $\mathbb{Z}/m\mathbb{Z}$.
- **Other complexity measures.** The $k$-error linear complexity is the least linear complexity after at most $k$ changes of terms. The 2-adic complexity uses feedback with carry shift registers instead of LFSRs.

## Examples

**A maximal length sequence.** Over $\mathrm{GF}(2)$, the recurrence $s_j = s_{j-3} + s_{j-4}$ with $C(x) = 1 + x^3 + x^4$, the reciprocal of the primitive polynomial $x^4 + x + 1$, gives from the state $1, 0, 0, 0$ the sequence

$$1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, \ldots$$

of period $15 = 2^4 - 1$. Its first 8 terms already have linear complexity 4 with the unique register $C(x) = 1 + x^3 + x^4$, and then the whole sequence follows. The profile of the first 8 terms is $1, 1, 1, 1, 4, 4, 4, 4$: the register $C = 1$ of length 1 explains $1, 0, 0, 0$, and the term $s_4 = 1$ forces the length up to $5 - 1 = 4$.

**Extreme cases.** The zero sequence has linear complexity 0. The sequence $0, \ldots, 0, a$ with $a \ne 0$ in position $N - 1$ has linear complexity $N$: a register of length $L < N$ would give $s_{N-1} = 0$. A constant nonzero sequence has linear complexity 1 with $C(x) = 1 - x$.

**Uniqueness and non-uniqueness.** Over $\mathrm{GF}(2)$, the sequence $1, 0$ has $N = 2$ and $L = 1$, and only $C = 1$ generates it: $C = 1 + x$ predicts $s_1 = 1$. Here $2L \le N$. The one-term sequence $1$ also has $L = 1$, but both $C = 1$ and $C = 1 + x$ generate it, because there is no term to check. Here $2L > N$. In general, when $2L > N$ there are exactly $q^{2L - N}$ shortest registers over $\mathrm{GF}(q)$.

## Known algorithms

| algorithm | operations | notes |
|---|---|---|
| Solve the Hankel systems for $L = 0, 1, \ldots$ by [Gaussian elimination](/gaussian-elimination/) | $O(N^4)$ | the direct method from the definition |
| [Berlekamp-Massey](/berlekamp-massey/) (Berlekamp 1968, Massey 1969) | $O(N^2)$ | online; gives the whole profile |
| Extended Euclidean algorithm on $x^N$ and the reversed sequence, continued fractions (Mills 1975; Sugiyama et al. 1975 for decoding) | $O(N^2)$ | the same polynomials as Berlekamp-Massey |
| Half-GCD form of the Euclidean method | $O(M(N) \log N)$ | $M(N)$ is the cost of a polynomial product; fast for long sequences |

**The Euclidean method.** Let $A(x) = \sum_{k<N} s_k x^{N-1-k}$, the reversed sequence. Run the [extended Euclidean algorithm](/polynomial-extended-euclidean-algorithm/) on $r_{-1} = x^N$ and $r_0 = A$, and keep the cofactors $v_i$ with $v_i A \equiv r_i \pmod{x^N}$, $v_{-1} = 0$ and $v_0 = 1$. Stop at the first $i$ with $\deg r_i < \deg v_i$. Then $L_N(s) = \deg v_i$, and the monic $f = v_i / \mathrm{lc}(v_i)$ is a characteristic polynomial of degree $L$: $C(x) = x^L f(1/x)$. The reversed form avoids the condition $C(0) = 1$, because a monic polynomial of degree $L$ always gives a register of length $L$.

## Bounds

- **Trivial bounds.** $0 \le L_N(s) \le N$, and $L_N(s)$ does not decrease with $N$.
- **Length change (Massey).** If a register of length $L$ generates $s_0, \ldots, s_{N-1}$ but not $s_N$, every register for $s_0, \ldots, s_N$ has length at least $N + 1 - L$. So $L_{N+1} = L_N$ or $L_{N+1} = \max(L_N, N + 1 - L_N)$.
- **Uniqueness.** If $2 L_N(s) \le N$, the shortest register is unique. So $2L$ terms of a sequence of linear complexity $L$ fix the register and all later terms.
- **Lower bound for any method.** An algorithm must read every term: changing $s_{N-1}$ alone can change $L_N$. So $\Omega(N)$ operations are necessary.
- **Random sequences.** Over $\mathrm{GF}(2)$, the number of sequences of length $N$ with linear complexity $L \ge 1$ is $2^{\min(2N - 2L,\, 2L - 1)}$, and the mean linear complexity is
$$\frac{N}{2} + \frac{4 + (N \bmod 2)}{18} - 2^{-N}\Bigl(\frac{N}{3} + \frac{2}{9}\Bigr)$$
(Rueppel, 1986). So a random sequence has linear complexity close to $N/2$.

## Reductions

- **To a linear system.** For a fixed $L$, the coefficients $c_1, \ldots, c_L$ solve the $(N - L) \times L$ Hankel system $\sum_{i=1}^{L} c_i s_{j-i} = -s_j$. The linear complexity is the least $L$ for which it is consistent. With $2L = N$ the matrix is square and the problem is a [Toeplitz system](/toeplitz-system-solving/) after the order of the columns is reversed.
- **To rational reconstruction.** The polynomial form is a Padé approximation of $S(x)$ modulo $x^N$, which the extended Euclidean algorithm solves. The same reduction gives Berlekamp-Massey from Euclid and back (Dornstetter, 1987).
- **From decoding.** Bounded distance decoding of a BCH or Reed-Solomon code with $2t$ syndromes reduces to this problem on $S_b, \ldots, S_{b+2t-1}$, followed by a root search.
- **From minimal polynomials.** The minimal polynomial of a matrix $A$ is, with high probability, the shortest recurrence of $u^T A^i v$ for random $u$ and $v$. The [Wiedemann algorithm](/wiedemann-algorithm/) uses this reduction.

## Applications

- **Decoding.** The error locator of [Reed-Solomon decoding](/reed-solomon-decoding/) and BCH decoding.
- **Stream ciphers.** A keystream of linear complexity $L$ is predictable from $2L$ consecutive bits, so a keystream generator must have a high linear complexity and a profile close to $N/2$. This rules out a single [LFSR](/lfsr/) as a keystream generator.
- **Sparse linear algebra.** Minimal polynomials, determinants and solutions of sparse systems over finite fields, through the [Wiedemann algorithm](/wiedemann-algorithm/).
- **Sequence guessing.** Find the recurrence of a [linear recurrence](/linear-recurrence-nth-term/) from its first terms, then compute far terms fast.

## References
