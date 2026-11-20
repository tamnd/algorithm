---
tag: 8DKHA8
kind: definition
slug: costas-array
name: Costas array
aliases:
- Costas frequency hopping code
- Costas sequence
area: communications/radar-waveforms
level: advanced
summary: "A permutation of n frequencies over n time slots in which all displacement vectors between pairs of dots differ, which gives a frequency hopping pulse with a thumbtack ambiguity function."
prereqs: [permutation, primitive-root, ambiguity-function]
see_also: [barker-code, frank-code, frequency-hopping-spread-spectrum, golomb-ruler-problem, n-queens-problem, range-doppler-coupling, pulse-compression, stepped-frequency-waveform]
sources:
  - paper: doi:10.1109/PROC.1984.12967
    title: "J. P. Costas, A study of a class of detection waveforms having nearly ideal range-Doppler ambiguity properties, Proceedings of the IEEE 72(8), 1984"
    locator: pp. 996 to 1009 (frequency hopping pulses whose ambiguity function has at most one coincidence away from the origin)
  - paper: doi:10.1109/PROC.1984.12994
    title: "S. W. Golomb and H. Taylor, Constructions and properties of Costas arrays, Proceedings of the IEEE 72(9), 1984"
    locator: "pp. 1143 to 1163 (the Welch and the Lempel and Golomb constructions, and the counts for small orders)"
  - url: https://arxiv.org/abs/1102.5727
    title: "Konstantinos Drakakis, Open problems in Costas arrays, 2011"
    locator: "the list of open problems (orders 32 and 33 as the smallest orders with no known Costas array, and the state of exhaustive enumeration)"
---

A Costas array of order $n$ is a permutation $f$ of $n$ frequencies over $n$ time slots such that the vectors between all pairs of dots, $(j - i,\ f(j) - f(i))$, are distinct. A pulse that hops through the frequencies in this order has an ambiguity function close to a thumbtack: at every shift of whole slots and whole frequency steps, other than zero, at most one dot of the pattern meets a dot of the shifted pattern. A [Barker code](/barker-code/) and a [Frank code](/frank-code/) code the phase of each chip and have sidelobes only in delay, while a Costas array codes the frequency and controls the sidelobes in delay and Doppler together. A linear order of the frequencies gives a staircase approximation of a [chirp](/linear-frequency-modulation-pulse/) instead, with a ridge and [range-Doppler coupling](/range-doppler-coupling/).

## Definition

**Costas array.** A [permutation](/permutation/) $f$ of $\{1, \dots, n\}$ is a Costas permutation if for all $i < j$ and $i' < j'$ with $(i, j) \ne (i', j')$,

$$(j - i,\ f(j) - f(i)) \ne (j' - i',\ f(j') - f(i')).$$

The Costas array is the $n \times n$ array with a dot in column $i$ and row $f(i)$. Equivalently, for each distance $d = 1, \dots, n-1$, the $n - d$ differences $f(i + d) - f(i)$ are distinct. These differences form the rows of the difference triangle of $f$.

**The waveform.** A pulse of $n$ subpulses, each of length $t_b$, uses in slot $i$ the frequency $f_0 + f(i)\,\Delta f$ with $\Delta f = 1/t_b$. Its bandwidth is about $n\,\Delta f$, so it resolves about $t_b/n$ in delay, and its length $n t_b$ resolves about $1/(n t_b)$ in Doppler.

**Coincidences.** Shift the pattern by $k$ slots and $l$ frequency steps. The number of dots that land on dots is the number of pairs $i, j$ with $j - i = k$ and $f(j) - f(i) = l$. For a Costas array this is at most 1 for every $(k, l) \ne (0, 0)$, against $n$ at the origin. The ambiguity function at these grid points is roughly proportional to the number of coincidences, so its sidelobes there are about $1/n$ of the peak (a rule of thumb, since the sinc shape of each subpulse adds smaller terms between grid points).

**Welch construction (theorem).** Let $p$ be a prime and $g$ a [primitive root](/primitive-root/) modulo $p$. Then $f(i) = g^{i} \bmod p$ for $i = 1, \dots, p - 1$ is a Costas permutation of order $p - 1$.

*Proof.* The values $g^1, \dots, g^{p-1}$ are $1, \dots, p - 1$ in some order, so $f$ is a permutation. Suppose $f(i + d) - f(i) = f(j + d) - f(j)$ with $d \ge 1$. Then $(g^d - 1)(g^i - g^j) \equiv 0 \pmod p$. Since $1 \le d \le p - 2$ and $g$ has order $p - 1$, $g^d \not\equiv 1$, so $g^i \equiv g^j$ and $i = j$. $\square$

**Lempel and Golomb construction (theorem).** Let $q$ be a prime power and $\alpha, \beta$ primitive elements of the field with $q$ elements. For $1 \le i, j \le q - 2$, put $f(i) = j$ when $\alpha^i + \beta^j = 1$. This is a Costas permutation of order $q - 2$. With $\alpha = \beta$ it is the Lempel construction.

**Existence.** The two constructions and variants of them give Costas arrays for many orders, but not for all. No order is known for which Costas arrays are proved not to exist. The smallest orders with no known Costas array are 32 and 33, and exhaustive search has found all Costas arrays up to order 29.

## Examples and non-examples

**Welch, $p = 7$, $g = 3$.** The powers $3^1, \dots, 3^6$ modulo 7 give $f = (3, 2, 6, 4, 5, 1)$, a Costas array of order 6. Its 15 displacement vectors are distinct, and every shifted copy meets the original in at most one dot.

**Lempel and Golomb, $q = 7$.** With $\alpha = \beta = 3$, solving $3^i + 3^j \equiv 1 \pmod 7$ gives $f = (5, 3, 2, 4, 1)$ for $i = 1, \dots, 5$. With $\alpha = 3$ and $\beta = 5$ it gives $(1, 3, 4, 2, 5)$. Both are Costas arrays of order 5.

**Counts (computed by backtracking).** The numbers of Costas permutations of orders 1 to 9 are $1, 2, 4, 12, 40, 116, 200, 444, 760$.

**Non-example: the linear order.** $f(i) = i$ is a stepped approximation of a chirp. All $n - d$ pairs at distance $d$ have the same vector $(d, d)$, so a shift by one slot and one frequency step meets $n - 1$ dots. For $n = 6$ that is 5 coincidences, a strong ridge, against at most 1 for the Welch array.

**Non-example: a permutation that fails.** For $f = (1, 3, 2, 4)$, the pairs $(1, 3)$ and $(2, 4)$ both have the vector $(2, 1)$, so $f$ is not a Costas permutation.

**Non-example: a Golomb ruler.** A [Golomb ruler](/golomb-ruler-problem/) is a set of marks on a line with distinct differences. A Costas array asks for distinct differences in two dimensions at once, one condition for each distance $d$, on a permutation.

## Related definitions

- **Frequency hopping.** A Costas array is a hopping pattern for a single pulse. In [frequency hopping spread spectrum](/frequency-hopping-spread-spectrum/), hopping patterns are chosen for low collisions between users, a related but different condition.
- **N-queens.** A solution of the [n-queens problem](/n-queens-problem/) is also a permutation with a condition on pairs, but only on the diagonals. Costas permutations are found by the same kind of backtracking search.
- **Ambiguity function.** The [ambiguity function](/ambiguity-function/) of a Costas pulse has a narrow central peak and low sidelobes spread over the plane, which is close to the thumbtack that the volume property allows.
- **Phase codes.** A [Barker code](/barker-code/) has sidelobes of at most 1 in delay alone. A Costas array has at most one coincidence in delay and Doppler together, the two-dimensional analog.
- **Stepped frequency.** A [stepped frequency waveform](/stepped-frequency-waveform/) also uses a set of frequencies, but in linear order and over separate pulses, which gives coupling instead of a thumbtack.

## References
