---
tag: 1E7DCT
kind: theorem
slug: macwilliams-identity
name: MacWilliams identity
aliases:
- MacWilliams transform
- MacWilliams identities
- MacWilliams theorem on weight enumerators
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "For a linear code C over GF(q), the weight enumerator of the dual code is W_C(x + (q - 1)y, x - y) divided by |C|."
prereqs: [linear-code, dual-code]
see_also: [delsarte-lp-bound, undetected-error-probability, hamming-code, simplex-code, golay-code, singleton-bound, walsh-hadamard-transform, fourier-analysis-of-boolean-functions]
sources:
  - paper: doi:10.1002/j.1538-7305.1963.tb04003.x
    title: F. J. MacWilliams, A theorem on the distribution of weights in a systematic code, Bell System Technical Journal 42(1), 1963
    locator: pp. 79 to 94 (the identity between the weight distributions of a code and its dual)
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 5 (dual codes and the MacWilliams identity, with the Krawtchouk form and the power moments)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Section 4.4 (MacWilliams' identities)
  - book: isbn:9780521782807
    title: W. Cary Huffman and Vera Pless, Fundamentals of Error-Correcting Codes, Cambridge University Press, 2003
    locator: Chapter 7 (weight distributions, the MacWilliams equations and the Pless power moments)
---

The MacWilliams identity gives the weight distribution of the [dual code](/dual-code/) of a [linear code](/linear-code/) from the weight distribution of the code itself. In terms of weight enumerators, $W_{C^\perp}(x, y) = \frac{1}{|C|} W_C(x + (q - 1)y, x - y)$. So a code with few words determines the weights of its large dual, and the [simplex code](/simplex-code/) with 8 words gives the weights of the [Hamming code](/hamming-code/) with 16. The identity is a discrete Fourier transform on the space GF($q$)$^n$, and it is the base of the [linear programming bound](/delsarte-lp-bound/).

## Statement

Notation. $C$ is a linear $[n, k]$ code over GF($q$). $A_i$ is the number of codewords of weight $i$, and the *weight enumerator* is the homogeneous polynomial

$$W_C(x, y) = \sum_{c \in C} x^{n - \mathrm{wt}(c)} y^{\mathrm{wt}(c)} = \sum_{i=0}^{n} A_i x^{n - i} y^i .$$

$C^\perp = \{u : u \cdot c = 0 \text{ for all } c \in C\}$ is the dual code, with weight distribution $B_0, \dots, B_n$. $K_k(x)$ is the Krawtchouk polynomial $\sum_j (-1)^j (q - 1)^{k - j} \binom{x}{j}\binom{n - x}{k - j}$.

**Theorem (MacWilliams).**

$$W_{C^\perp}(x, y) = \frac{1}{|C|} \, W_C\big(x + (q - 1) y, \; x - y\big).$$

**Krawtchouk form.** Equivalently, for $k = 0, \dots, n$,

$$B_k = \frac{1}{|C|} \sum_{i=0}^{n} A_i K_k(i) .$$

**One variable form.** With $A(z) = \sum_i A_i z^i$ and $B(z) = \sum_k B_k z^k$,

$$B(z) = \frac{1}{|C|} (1 + (q - 1) z)^n \, A\!\left(\frac{1 - z}{1 + (q - 1) z}\right).$$

## In plain words

Write down how many codewords have each weight. The identity turns this short list into the same list for the dual code, by a fixed formula that does not depend on which code you started with. So you do not need to list the dual code's words, which may be far too many. The reason is that the dual code is the set of frequencies where a Fourier transform of the code is large, and the weight of a word changes in a known way under that transform.

## Proof

*Characters.* Let $q = p^m$, and let $\chi$ be a nontrivial additive character of GF($q$), for example $\chi(a) = e^{2\pi i \operatorname{Tr}(a)/p}$, where Tr is the trace to GF($p$). For prime $q$ this is $\chi(a) = e^{2\pi i a/q}$. Two facts are used: $\sum_{a \in \mathrm{GF}(q)} \chi(a) = 0$, and, for a linear code $C$,

$$\sum_{c \in C} \chi(u \cdot c) = \begin{cases} |C| & \text{if } u \in C^\perp, \\ 0 & \text{otherwise.} \end{cases}$$

For the second, if $u \notin C^\perp$ the map $c \mapsto u \cdot c$ is a nonzero linear map onto GF($q$), so each value is taken $|C|/q$ times and the sum is $(|C|/q)\sum_a \chi(a) = 0$.

*Transform of one word.* Let $f(u) = x^{n - \mathrm{wt}(u)} y^{\mathrm{wt}(u)}$ and $\hat f(c) = \sum_{u \in \mathrm{GF}(q)^n} \chi(u \cdot c) f(u)$. The sum factors over positions. A position with $c_j = 0$ gives $x + (q - 1) y$. A position with $c_j \ne 0$ gives $x + y \sum_{a \ne 0} \chi(a c_j) = x - y$. So

$$\hat f(c) = (x + (q - 1)y)^{n - \mathrm{wt}(c)} (x - y)^{\mathrm{wt}(c)} .$$

*Summing over the code.*

$$\sum_{c \in C} \hat f(c) = \sum_{u} f(u) \sum_{c \in C} \chi(u \cdot c) = |C| \sum_{u \in C^\perp} f(u) = |C| \, W_{C^\perp}(x, y).$$

The left side is $W_C(x + (q - 1)y, x - y)$ by the formula for $\hat f$. Dividing by $|C|$ gives the theorem. The Krawtchouk form follows by expanding $(x + (q - 1)y)^{n - i}(x - y)^i$: its coefficient of $x^{n - k} y^k$ is $K_k(i)$. The one variable form is the theorem with $x = 1$ and $y = z$, after dividing by a power of $1 + (q - 1)z$. $\blacksquare$

## Consequences

**Hamming and simplex codes.** The binary [7, 3] simplex code has $W(x, y) = x^7 + 7x^3y^4$. The identity gives its dual, the [7, 4] Hamming code:

$$\tfrac18 \big[(x + y)^7 + 7 (x + y)^3 (x - y)^4\big] = x^7 + 7x^4y^3 + 7x^3y^4 + y^7 .$$

In general the simplex code of length $n = 2^r - 1$ has one nonzero weight $2^{r-1}$, and the identity gives the weight enumerator of the Hamming code of length $n$:

$$A(z) = \frac{1}{n + 1}\Big[(1 + z)^n + n (1 - z)(1 - z^2)^{(n - 1)/2}\Big].$$

For $n = 15$ this gives $A_3 = 35$, $A_4 = 105$, $A_5 = 168$. For $n = 31$ the Hamming code has $2^{26}$ words, and its weights come from the 32 words of the simplex code. The tests compare the closed form with the transform for $n = 7, 15, 31$.

**Self-dual codes.** If $C = C^\perp$, the weight enumerator is fixed by the transform. The extended [Golay code](/golay-code/) $[24, 12, 8]$ is self-dual with $W = x^{24} + 759x^{16}y^8 + 2576x^{12}y^{12} + 759x^8y^{16} + y^{24}$, and the ternary tetracode $[4, 2, 3]_3$ has $W = x^4 + 8xy^3$. Gleason's theorem describes all such invariant polynomials, and it limits the minimum distance of self-dual codes.

**MDS codes.** If $C$ is MDS, so is $C^\perp$, and $A_i = 0$ for $0 < i < n - k + 1$ and $B_i = 0$ for $0 < i < k + 1$. These zeros and the identity determine all $A_i$, so the weight distribution of an MDS code depends only on $n$, $k$ and $q$ (see the [Singleton bound](/singleton-bound/)).

**Undetected errors.** On a channel that flips each symbol with probability $p$, an error goes undetected when it is a nonzero codeword. The probability is a value of the weight enumerator, and the identity lets one compute it from the smaller of $C$ and $C^\perp$. See [undetected error probability](/undetected-error-probability/).

**Linear programming bound.** For a nonlinear code, the right side of the Krawtchouk form, applied to the distance distribution, is no longer a weight distribution, but Delsarte proved that it is still nonnegative. This gives the [Delsarte linear programming bound](/delsarte-lp-bound/).

**Power moments.** Taking repeated derivatives of the one variable form gives the Pless power moments, linear relations between $\sum_i i^r A_i$ and the first $B_k$ (Huffman and Pless, Chapter 7).

**Boolean functions.** For $q = 2$ the transform is the [Walsh-Hadamard transform](/walsh-hadamard-transform/), and the identity is the Poisson summation formula of the [Fourier analysis of Boolean functions](/fourier-analysis-of-boolean-functions/) applied to the indicator of $C$.

## Tightness

The identity is exact, so there is no gap to close. Its limits are of scope:

- It needs a linear code, or at least an additive one. For nonlinear codes the transform of the distance distribution need not be a distance distribution of any code, and only the inequalities of Delsarte remain.
- The weight distribution of $C$ does not determine $C$. Codes that are not equivalent can have the same weight enumerator, and then their duals also have the same enumerator.
- Computing the weight distribution itself is hard in general for large codes; the identity moves the work to the smaller of the two codes.

## History

MacWilliams proved the identity in her 1962 thesis at Harvard and published it in the Bell System Technical Journal in 1963. Delsarte (1972, 1973) used it to define the linear programming bound and placed it in the theory of association schemes. Gleason (1970) described the enumerators of self-dual codes. The identity is now a standard tool of coding theory and of the Fourier analysis of Boolean functions.

## References
