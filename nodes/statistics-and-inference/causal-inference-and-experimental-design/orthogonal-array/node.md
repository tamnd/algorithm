---
tag: 5Q12GA
kind: definition
slug: orthogonal-array
name: Orthogonal array
aliases:
- orthogonal array of strength t
- "OA(N, k, s, t)"
area: statistics-and-inference/causal-inference-and-experimental-design
level: advanced
summary: An N x k array over s symbols in which every N x t subarray has each t-tuple equally often. It is the combinatorial core of fractional designs.
prereqs: [factorial-design, latin-square-design]
see_also: [fractional-factorial-design, plackett-burman-design, linear-code, dual-code, hamming-code, macwilliams-identity, latin-hypercube-sampling, optimal-experimental-design]
sources:
  - paper: doi:10.2307/2983576
    title: "C. R. Rao, Factorial experiments derivable from combinatorial arrangements of arrays, Supplement to the Journal of the Royal Statistical Society 9(1), 1947"
    locator: pp. 128 to 139 (the arrays of strength t and the lower bound on the number of runs)
  - book: isbn:9780387987668
    title: A. S. Hedayat, N. J. A. Sloane and John Stufken, Orthogonal Arrays, Theory and Applications, Springer, 1999
    locator: Section 2.2 (Rao's inequalities, Chapter 2 on pp. 11 to 35) and Section 4.3 (linear codes and linear orthogonal arrays, starting on p. 65)
  - paper: "Philippe Delsarte, An algebraic approach to the association schemes of coding theory, Philips Research Reports Supplements 10, 1973"
    locator: the dual distance of a code and its strength as an orthogonal array, for codes that need not be linear (general locator)
---

An orthogonal array is a table of runs in which every choice of $t$ factors sees every combination of their levels equally often. Rao (1947) defined these arrays as a common frame for factorial experiments: a full [factorial design](/factorial-design/), a regular [fractional factorial design](/fractional-factorial-design/), a [Plackett-Burman design](/plackett-burman-design/) and a set of mutually orthogonal [Latin squares](/latin-square-design/) are all orthogonal arrays. Strength 2 makes the main effects orthogonal; higher strength protects them from more interactions. Rao also proved a lower bound on the number of runs. The same objects appear in coding theory: the codewords of a [linear code](/linear-code/) form an orthogonal array whose strength is one less than the minimum distance of the [dual code](/dual-code/).

## Definition

An **orthogonal array** $\mathrm{OA}(N, k, s, t)$ is an $N \times k$ array with entries from a set of $s$ symbols, such that in every $N \times t$ subarray each of the $s^t$ possible rows occurs exactly $\lambda = N/s^t$ times. $N$ is the number of runs, $k$ the number of factors, $s$ the number of levels, $t$ the **strength** and $\lambda$ the **index**. Strength $t$ implies strength $t - 1$, because each $(t-1)$-tuple extends to $s$ tuples on one more column. A full factorial $s^k$ design is an $\mathrm{OA}(s^k, k, s, k)$, and a regular two-level fraction of resolution $R$ is an orthogonal array of strength $R - 1$ (Theorem 3).

**Theorem 1 (strength gives orthogonal effects).** Let $\phi_0 = 1, \phi_1, \dots, \phi_{s-1}$ be real functions on the symbols that are orthonormal for the uniform distribution, so $\frac1s\sum_a \phi_i(a)\phi_j(a) = [i = j]$; they exist by Gram-Schmidt. For a set $S$ of columns and a map $\alpha$ from $S$ to $\{1, \dots, s-1\}$, let $v_{S,\alpha}$ be the vector of length $N$ whose entry in run $r$ is $\prod_{c \in S}\phi_{\alpha(c)}(r_c)$, an effect column of order $|S|$. In an array of strength $t$, two such vectors with $|S \cup T| \le t$ have $v_{S,\alpha}^\top v_{T,\beta} = N$ if $(S, \alpha) = (T, \beta)$ and $0$ otherwise.

*Proof.* The entry of run $r$ in the product depends only on the columns in $S \cup T$, at most $t$ of them. By strength $t$, these columns take every combination of levels equally often, so the sum over the runs is $N$ times the mean over independent uniform levels $X_c$, $c \in S \cup T$. That mean factors over the columns. A column in only one of the sets gives $\mathbb E\,\phi_i(X_c) = 0$ for $i \ge 1$, and a column in both gives $\mathbb E\,\phi_i(X_c)\phi_j(X_c) = [i = j]$. So the mean is 1 when $(S, \alpha) = (T, \beta)$ and 0 otherwise. $\square$

With $t = 2$, the main-effect columns of different factors are orthogonal, so the main effects are estimated independently when interactions are absent. In general, with $u = \lfloor t/2 \rfloor$, all effects of order at most $u$ are estimated independently when the interactions of order above $t - u$ are absent.

**Theorem 2 (the Rao bound).** An $\mathrm{OA}(N, k, s, t)$ with $t = 2u$ has

$$N \ge \sum_{i=0}^{u} \binom{k}{i}(s - 1)^i,$$

and one with $t = 2u + 1$ has

$$N \ge \sum_{i=0}^{u} \binom{k}{i}(s - 1)^i + \binom{k - 1}{u}(s - 1)^{u + 1}.$$

*Proof.* For even $t$, take all vectors $v_{S,\alpha}$ with $|S| \le u$. There are $\binom{k}{i}(s-1)^i$ of them with $|S| = i$. Any two have $|S \cup T| \le 2u = t$, so by Theorem 1 they are nonzero and pairwise orthogonal, hence linearly independent in $\mathbb R^N$, and $N$ is at least their number. For odd $t$, also take the vectors with $|S| = u + 1$ and $S$ containing column 1; there are $\binom{k-1}{u}(s-1)^{u+1}$ of them. Two sets of size $u + 1$ that both contain column 1 have a union of at most $2u + 1 = t$ columns, and a set of size $u + 1$ with a set of size at most $u$ also has a union of at most $t$ columns. So Theorem 1 again makes all the vectors orthogonal. $\square$

The bound counts the effects that the array can estimate, so it is the statistical statement "at least as many runs as parameters". It can be weak: since $\lambda = N/s^t$ is an integer, $N$ is also a multiple of $s^t$.

**Theorem 3 (code duality).** Let $C$ be a linear code of length $k$ over the field with $q$ elements, with $C^\perp \ne \{0\}$, and let $d^\perp$ be the minimum distance of the dual code $C^\perp$. The codewords of $C$, as the rows of a $|C| \times k$ array, form an orthogonal array of strength exactly $d^\perp - 1$.

*Proof.* Fix a set $T$ of $t$ columns. The projection $\pi_T$ of $C$ onto the columns $T$ is linear, so if it is onto, every $t$-tuple is hit by a coset of its kernel, that is, $|C|/q^t$ times. It fails to be onto exactly when a nonzero linear form on the coordinates $T$ vanishes on $\pi_T(C)$. Such a form is a nonzero vector $w$ supported inside $T$ with $w \cdot c = 0$ for every $c \in C$, that is, a nonzero dual codeword of weight at most $t$ supported in $T$. So the array has strength $t$ if and only if no nonzero dual codeword has weight at most $t$, that is, $t \le d^\perp - 1$. $\square$

Delsarte (1973) extended this to codes that are not linear, with the dual distance defined through the [MacWilliams identity](/macwilliams-identity/) transform of the distance distribution; that result is cited here, not proved. For a regular $2^{k-p}$ fraction, the runs (with level $+1$ written as bit 0 and $-1$ as bit 1) are the dual of the code of defining words, whose minimum distance is the resolution $R$. So Theorem 3 gives strength $R - 1$.

## Examples and non-examples

**Example: $\mathrm{OA}(4, 3, 2, 2)$.** The rows $000, 011, 101, 110$, the even-weight code of length 3, form the half fraction $I = ABC$ of a $2^3$ design. Every two columns show $00, 01, 10, 11$ once, so the strength is 2, and $N = 4$ meets the Rao bound $1 + 3$. The strength is not 3: only 4 of the 8 triples occur.

**Example: Latin squares.** From $m$ mutually orthogonal Latin squares $L_1, \dots, L_m$ of order $n$, the $n^2$ rows $(i, j, L_1(i, j), \dots, L_m(i, j))$ form an $\mathrm{OA}(n^2, m + 2, n, 2)$, and every such array of index 1 arises this way. The two orthogonal squares of order 3 give $\mathrm{OA}(9, 4, 3, 2)$, and the three squares of order 4 built over the field with 4 elements give $\mathrm{OA}(16, 5, 4, 2)$. Both meet the Rao bound, $1 + 4 \cdot 2 = 9$ and $1 + 5 \cdot 3 = 16$. In general $k \le n + 1$ for index 1 is the Rao bound $n^2 \ge 1 + k(n - 1)$, which is again the bound of at most $n - 1$ mutually orthogonal Latin squares.

**Example: the Hamming code.** The 16 codewords of the [7, 4] [Hamming code](/hamming-code/) form an $\mathrm{OA}(16, 7, 2, 3)$: the dual is the [7, 3] simplex code, whose nonzero words all have weight 4, so $d^\perp = 4$ and the strength is 3. The Rao bound for $k = 7$, $s = 2$, $t = 3$ is $1 + 7 + 6 = 14$, so the array is above the bound. But $N$ must be a multiple of $2^3 = 8$, so 16 is the smallest possible. Adding a parity bit gives the extended [8, 4, 4] code, which is its own dual: an $\mathrm{OA}(16, 8, 2, 3)$ that meets the Rao bound $1 + 8 + 7 = 16$. As a design it is the $2^{8-4}$ fraction of resolution IV.

**Example: the simplex code and the Plackett-Burman designs.** The 8 words of the [7, 3] simplex code form an $\mathrm{OA}(8, 7, 2, 2)$, the saturated $2^{7-4}$ design; its dual is the Hamming code with $d^\perp = 3$. The 12-run Plackett-Burman design is an $\mathrm{OA}(12, 11, 2, 2)$. Both meet the Rao bound $N \ge 1 + k$ for $s = 2$, $t = 2$. The 12-run array comes from no linear code, because 12 is not a power of 2.

**Non-example: 8 runs for 8 factors.** No $\mathrm{OA}(8, 8, 2, 2)$ exists, because the Rao bound is $1 + 8 = 9$. So no 8-run two-level design has 8 balanced, pairwise orthogonal factor columns.

**Non-example: a covering array.** The 5 rows $0000, 0111, 1011, 1101, 1110$ show every pair of levels in every pair of columns, but $11$ occurs twice and the other pairs once. This is a covering array of strength 2, which asks that every $t$-tuple occur at least once, not equally often. Pairwise testing of software often uses covering arrays. They are not orthogonal arrays (here 5 is not even a multiple of $2^2$), and their main-effect columns are not orthogonal.

The test file checks every array on this page, the Rao bounds, and Theorem 3 on random linear codes over the fields with 2 and 3 elements.

## Related definitions

- [Factorial design](/factorial-design/): the full $s^k$ design, the array of largest strength.
- [Fractional factorial design](/fractional-factorial-design/): a regular fraction of resolution $R$ is a linear orthogonal array of strength $R - 1$.
- [Plackett-Burman design](/plackett-burman-design/): two-level arrays of strength 2 that meet the Rao bound for every $N$ with a Hadamard matrix.
- [Latin square design](/latin-square-design/): mutually orthogonal Latin squares are the arrays of strength 2 and index 1.
- [Linear code](/linear-code/), [dual code](/dual-code/) and [MacWilliams identity](/macwilliams-identity/): the strength of a code as an array is its dual distance minus 1.
- [Singleton bound](/singleton-bound/): two rows of an array of index 1 and strength $t$ agree in at most $t - 1$ columns, so the rows form a code that meets the Singleton bound, such as a [Reed-Solomon code](/reed-solomon-code/).
- [Balanced incomplete block design](/balanced-incomplete-block-design/): balances pairs of treatments in blocks, as a strength-2 array balances pairs of levels in columns.
- [Latin hypercube sampling](/latin-hypercube-sampling/): orthogonal arrays give Latin hypercube samples that are also balanced in pairs of dimensions.

## References
