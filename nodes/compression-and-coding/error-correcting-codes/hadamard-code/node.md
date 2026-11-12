---
tag: AJ00FE
kind: definition
slug: hadamard-code
name: Hadamard code
aliases:
- Walsh-Hadamard code
- augmented Hadamard code
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "The code that writes an r-bit message x as the values of a . x for all 2^r vectors a. Relative distance 1/2, rate r/2^r, decoded by a fast Walsh-Hadamard transform."
history:
  year: 1867
  people: [James Joseph Sylvester, Jacques Hadamard, Raymond Paley]
  note: Sylvester built the doubling construction of the matrices in 1867, Hadamard studied them as matrices of maximal determinant in 1893, and Paley gave the quadratic residue construction in 1933. The codes came into use with the first order Reed-Muller codes in the 1950s and 1960s.
prereqs: [linear-code, minimum-distance, walsh-hadamard-transform]
see_also: [reed-muller-code, simplex-code, plotkin-bound, fast-walsh-hadamard-transform, locally-decodable-codes, list-decoding, linearity-test, hard-core-predicate]
sources:
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 2, Section 3 (Hadamard matrices and Hadamard codes), and Chapter 14 (first order Reed-Muller codes, the Hadamard transform and the Green machine decoder)
  - book: isbn:9780521845045
    title: Ron M. Roth, Introduction to Coding Theory, Cambridge University Press, 2006
    locator: Chapter 2 and Chapter 4 (the simplex code, the first order Reed-Muller code and the Plotkin bound)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Section 11.5 (the Walsh-Hadamard code, its local decoding and the linearity test in the exponential size PCP)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Section 4.3 (Reed-Muller codes; the first order code is the augmented Hadamard code)
---

The Hadamard code encodes an $r$-bit message $x$ as the list of all $2^r$ parities $a \cdot x$, one for each $a \in \mathrm{GF}(2)^r$. It is a [linear code](/linear-code/) with parameters $[2^r, r, 2^{r-1}]$: every nonzero codeword has weight exactly half the length. The augmented version adds the complements and has parameters $[2^r, r + 1, 2^{r-1}]$. Its codewords are the rows of a Sylvester Hadamard matrix and of its negative, and it is the first order [Reed-Muller code](/reed-muller-code/). The rate is very low, but the code has relative distance $1/2$, a decoder that runs in $O(n \log n)$ with the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/), and a local decoder that reads only 2 positions. These properties make it a basic tool in complexity theory as well as in coding.

## Definition

**Hadamard matrix.** An $n \times n$ matrix $H$ with entries $\pm 1$ is a Hadamard matrix if $H H^{\mathsf T} = n I$, that is, if any two distinct rows agree in exactly $n/2$ positions. Such a matrix can exist only for $n = 1$, $n = 2$ or $n$ a multiple of 4.

**Sylvester construction.** $H_1 = [1]$ and

$$H_{2m} = \begin{pmatrix} H_m & H_m \\ H_m & -H_m \end{pmatrix}.$$

With rows and columns indexed by $a, x \in \mathrm{GF}(2)^r$, the entry of $H_{2^r}$ is $(-1)^{a \cdot x}$. So $H_{2^r}$ is the matrix of the [Walsh-Hadamard transform](/walsh-hadamard-transform/).

**Hadamard code.** The Hadamard code of order $r$ is

$$\mathrm{Had}_r = \{\, (a \cdot x)_{a \in \mathrm{GF}(2)^r} : x \in \mathrm{GF}(2)^r \,\}.$$

The codeword of $x$ is the truth table of the linear function $a \mapsto a \cdot x$. If $x \ne 0$, the function $a \mapsto a \cdot x$ is onto GF(2), so it is 1 on exactly half of the $2^r$ inputs. So every nonzero codeword has weight $2^{r-1}$, and $\mathrm{Had}_r$ is an equidistant $[2^r, r, 2^{r-1}]$ code.

**Augmented Hadamard code.** Adding the all ones word gives

$$\mathrm{Had}^{+}_r = \{\, (a \cdot x + b)_{a} : x \in \mathrm{GF}(2)^r, \; b \in \mathrm{GF}(2) \,\},$$

a $[2^r, r + 1, 2^{r-1}]$ code with weights $0$, $2^{r-1}$ and $2^r$. Read $+1$ as bit 0 and $-1$ as bit 1. Then the $2^{r+1}$ codewords are the rows of $H_{2^r}$ and of $-H_{2^r}$. This code is the first order Reed-Muller code $\mathrm{RM}(1, r)$, and it is also called the biorthogonal code.

Both names are in use, so a source must say which code it means. In coding theory books "Hadamard code" often means the augmented code from rows of $\pm H$. In complexity theory it means the linear code $\mathrm{Had}_r$ with $r$ message bits.

### Hadamard codes from other Hadamard matrices

Any Hadamard matrix of order $n$ gives a binary code with $2n$ words, the rows of $H$ and $-H$ read as bits, length $n$ and minimum distance $n/2$. When $n$ is not a power of 2 the code is not linear. For a prime $q \equiv 3 \pmod 4$ the Paley construction gives a Hadamard matrix of order $q + 1$ from the quadratic residues modulo $q$, and so a $(12, 24, 6)$ code from $q = 11$. These codes meet the [Plotkin bound](/plotkin-bound/), and Levenshtein proved that, if Hadamard matrices of all orders divisible by 4 exist, the Plotkin bound is tight for all $d$ even with $2d > n$. The Hadamard conjecture states that such matrices exist for every multiple of 4. It is open, and 668 is the smallest order for which no construction is known.

### Decoding with the fast transform

For a received word $y$, let $s_x = (-1)^{y_x}$. The Walsh-Hadamard transform of $s$ is

$$F(a) = \sum_{x} (-1)^{a \cdot x} s_x = \sum_x (-1)^{y_x + a \cdot x} = n - 2\, d\big(y, (a \cdot x)_x\big).$$

So the codeword $a \cdot x + b$ nearest to $y$ has $|F(a)|$ largest, with $b = 0$ if $F(a) > 0$ and $b = 1$ if $F(a) < 0$. The fast Walsh-Hadamard transform computes all $n$ values of $F$ in $n \log_2 n$ additions and subtractions, against $n^2$ for a direct correlation with every codeword. This is the Green machine decoder. It is a maximum likelihood decoder, and it corrects every pattern of at most $n/4 - 1$ errors. With soft inputs, the same transform of the received real values gives maximum likelihood decoding on a Gaussian channel.

### Local decoding and list decoding

The Hadamard code is the simplest [locally decodable code](/locally-decodable-codes/). Suppose $y$ differs from the codeword of $x$ in at most a fraction $\delta$ of positions. To recover $x_i = e_i \cdot x$, choose $a$ at random and output $y_a + y_{a + e_i}$. Each of the two positions is uniform, so each is wrong with probability at most $\delta$, and the output is right with probability at least $1 - 2\delta$. A majority of a few such votes makes the error small for $\delta < 1/4$.

Beyond $1/4$, the code is [list decodable](/list-decoding/) up to a fraction $1/2 - \varepsilon$ of errors. The Goldreich-Levin algorithm finds every $x$ whose codeword agrees with $y$ on a fraction $1/2 + \varepsilon$ of positions, with $\mathrm{poly}(r, 1/\varepsilon)$ queries to $y$, and there are at most $1/(4\varepsilon^2)$ such $x$. This is the coding view of the [hard-core predicate](/hard-core-predicate/) $\langle x, a \rangle$. The [linearity test](/linearity-test/) checks with 3 queries whether a table is close to a Hadamard codeword, and this is the base of the exponential size proofs in the proof of the [PCP theorem](/pcp-theorem/).

## Examples and non-examples

**Order 2.** $H_4$ has rows $(1, 1, 1, 1)$, $(1, -1, 1, -1)$, $(1, 1, -1, -1)$, $(1, -1, -1, 1)$. As bits the rows are $0000$, $0101$, $0011$, $0110$, which is $\mathrm{Had}_2$: the codewords of $x = 0, 1, 2, 3$ in this order, with position $a$ read from $a = 0$ to $a = 3$ and bit $i$ of an integer as coordinate $i$. With the complements $1111$, $1010$, $1100$, $1001$ this is the $[4, 3, 2]$ even weight code.

**Decoding one error.** Take $r = 3$, $x = 5$ (bits $x_0 = 1$, $x_1 = 0$, $x_2 = 1$) and $b = 0$. The codeword at positions $a = 0, \dots, 7$ is $01011010$. Flip position 2 to get $y = 01111010$. The transform of $s = (-1)^{y}$ is

$$F = (-2, -2, 2, 2, -2, 6, 2, 2).$$

The largest value is $F(5) = 6 = 8 - 2 \cdot 1$, so the decoder returns $x = 5$, $b = 0$, at distance 1 from $y$.

**Two errors in length 8.** Flip position 7 of the last $y$ as well, to get $01111011$. Now $F = (-4, 0, 4, 0, 0, 4, 0, 4)$. Four codewords are at distance 2, so no decoder can find the sent word. This is the limit $n/4 - 1 = 1$ for $n = 8$.

**The simplex code.** In $\mathrm{Had}_r$ the position $a = 0$ is always 0. Removing it gives the $[2^r - 1, r, 2^{r-1}]$ [simplex code](/simplex-code/), the dual of the [Hamming code](/hamming-code/). In the same way $\mathrm{Had}^{+}_r = \mathrm{RM}(1, r)$ is the dual of the extended Hamming code.

**Non-example: length 6.** No Hadamard matrix of order 6 exists, since the order must be 1, 2 or a multiple of 4. So there is no Hadamard code of length 6 with 12 words and distance 3. In fact the Plotkin bound gives $A_2(6, 3) = A_2(7, 4) \le 8$.

**Non-example: the Paley code is not linear.** The $(12, 24, 6)$ code from the Paley matrix of order 12 has 24 words. A binary linear code has a power of 2 as its size, so this code is not linear, and a linear binary code of length 12 and distance 6 has at most 16 words. The tests check the Paley codes for $q = 3, 7, 11, 19, 23$.

## Related definitions

- [Reed-Muller code](/reed-muller-code/): $\mathrm{Had}^{+}_r$ is $\mathrm{RM}(1, r)$, the first order case.
- [Simplex code](/simplex-code/): the punctured linear Hadamard code.
- [Walsh-Hadamard transform](/walsh-hadamard-transform/): the transform whose matrix is $H_{2^r}$ and whose fast form decodes the code.
- [Plotkin bound](/plotkin-bound/): the bound that Hadamard codes meet.
- [Locally decodable codes](/locally-decodable-codes/) and [list decoding](/list-decoding/): the two decoding models in which the Hadamard code is the first example.
- [Long code](/long-code/): the code that lists all Boolean functions of the message, not only the linear ones.

## References
