---
tag: MDKZMK
kind: definition
slug: long-code
name: Long code
aliases:
- Hadamard-based long code
- dictator code
area: approximation/hardness-of-approximation
level: research
summary: The code that writes a label a in a set of n labels as the truth table of the dictator function x maps to x_a, a word of length 2^n.
prereqs: [hadamard-code, fourier-analysis-of-boolean-functions, label-cover]
see_also: [dictatorship-test, hastad-3bit-pcp, linearity-test, max-cut-ugc-hardness, unique-games-conjecture, reed-muller-code, linear-code]
sources:
  - paper: "Mihir Bellare, Oded Goldreich and Madhu Sudan, Free bits, PCPs, and nonapproximability, towards tight results, SIAM Journal on Computing 27(3), 804 to 915, 1998"
    locator: the definition of the long code and its first tests
  - paper: doi:10.1145/502090.502098
    title: Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48(4), 798 to 859, 2001
    locator: the long code, folding, and the long code tests used for Max 3LIN and Max 3SAT
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 22, Section 22.6 (coordinate functions, the long code and its testing)
  - book: isbn:9781107038325
    title: Ryan O'Donnell, Analysis of Boolean Functions, Cambridge University Press, 2014
    locator: Chapter 7 (dictator testing and its use in hardness of CSPs)
---

The long code is the error-correcting code that encodes a label $a \in [n]$ as the truth table of the dictator function $x \mapsto x_a$ on $\{-1,1\}^n$. A code word lists the value $g(a)$ for every one of the $2^n$ functions $g : [n] \to \{-1,1\}$, so a label of $k$ bits becomes a word of $2^{2^k}$ bits. The code was introduced by Bellare, Goldreich and Sudan, and it is the inner code of the tight hardness results of [Håstad](/hastad-3bit-pcp/) and of the [unique games](/unique-games-conjecture/) reductions, because its code words can be tested with very few queries by a [dictatorship test](/dictatorship-test/).

## Definition

Let $[n] = \{1, \ldots, n\}$ be a set of labels. Identify a point $x \in \{-1,1\}^n$ with the function $g_x : [n] \to \{-1,1\}$, $g_x(i) = x_i$. The *long code* of $a \in [n]$ is the function

$$\mathrm{LC}(a) : \{-1,1\}^n \to \{-1,1\}, \qquad \mathrm{LC}(a)(x) = x_a ,$$

so $\mathrm{LC}(a)(g) = g(a)$ for every $g : [n] \to \{-1,1\}$. As a binary word (with $+1 \mapsto 0$ and $-1 \mapsto 1$) it has length $2^n$, one position for each $x$. The code has $n$ code words, the $n$ dictators $\chi_{\{a\}}$ in the notation of [Fourier analysis of Boolean functions](/fourier-analysis-of-boolean-functions/).

**Length.** If the labels are the strings of $k$ bits, then $n = 2^k$ and the code word has length $2^{2^k}$. The [Hadamard code](/hadamard-code/) of the same string has length $2^k$, one position for each linear function of the string. The long code has one position for every Boolean function of the string. This doubly exponential length is the reason for the name, and it is affordable in a PCP because the labels there have constant size, so each table has constant size.

**Distance.** Two distinct dictators $x_a$ and $x_b$ differ exactly when $x_a \ne x_b$, which happens for half of all $x$. So the relative [distance](/hamming-distance/) of the code is $1/2$.

**Relation to the Hadamard code.** The dictators are characters of size $1$, so the $n$ code words lie inside the Hadamard code of message length $n$, whose $2^n$ code words are all the characters $\chi_S$. From the other side, if $a$ is written as a string $\bar a \in \mathbb{F}_2^k$, then the positions $g$ of the long code that are linear functions of $\bar a$ form a copy of the Hadamard code of $\bar a$ inside $\mathrm{LC}(a)$.

**Folding.** A table $A : \{-1,1\}^n \to \{-1,1\}$ is *folded* if $A(-x) = -A(x)$ for all $x$. Every long code word is folded. A verifier can force folding by reading the table only on points with $x_1 = 1$ and defining $A(x) = -A(-x)$ when $x_1 = -1$. *Claim:* a folded table has $\hat A(S) = 0$ for every $S$ of even size, in particular $\mathbb{E}[A] = \hat A(\emptyset) = 0$. *Proof.* $A(-x) = \sum_S \hat A(S) (-1)^{|S|} \chi_S(x)$, and this equals $-A(x) = -\sum_S \hat A(S) \chi_S(x)$. By uniqueness of the expansion, $\hat A(S) ((-1)^{|S|} + 1) = 0$, so $\hat A(S) = 0$ when $|S|$ is even. $\square$ Folding rules out the constant tables, which would otherwise pass many tests.

**Checking a projection.** Let $\pi : [L] \to [R]$ be a map between two label sets, as in a constraint of [label cover](/label-cover/). For $y \in \{-1,1\}^R$ define $y \circ \pi \in \{-1,1\}^L$ by $(y \circ \pi)_i = y_{\pi(i)}$. If $A = \mathrm{LC}(a)$ and $B = \mathrm{LC}(\pi(a))$, then

$$B(y) = y_{\pi(a)} = (y \circ \pi)_a = A(y \circ \pi) \quad \text{for all } y .$$

So a verifier can test that two long code tables encode labels that satisfy the constraint by comparing them at related points, without decoding either label. This is the property that the [3-bit PCP](/hastad-3bit-pcp/) uses.

## Examples and non-examples

**The long code for three labels.** List $x \in \{0,1\}^3$ in the order $000, 001, \ldots, 111$, where bit $1$ stands for $-1$. The three code words are

| Label | Code word |
|---|---|
| $1$ | 00001111 |
| $2$ | 00110011 |
| $3$ | 01010101 |

Any two of them differ in $4$ of the $8$ positions, which is the distance $1/2$.

**Majority is not a code word.** The truth table of $\operatorname{Maj}_3$ in the same order is 00010111. It differs from each of the three code words in exactly $2$ positions, so it is at relative distance $1/4$ from the code and is equally close to all three labels. Its Fourier weight on the singletons is $3/4$, spread evenly, which is why a decoder cannot pick one label from it. Majority on many inputs is the main example of a function that is far from every code word but still passes some tests with high probability.

**A parity of two coordinates is not a code word.** The table of $x_1 x_2$ is 00111100. It is a Hadamard code word of message length $3$, but not a long code word, and it differs from every long code word in $4$ of $8$ positions.

**Constant tables.** The tables 00000000 and 11111111 are not code words and are not folded. Folding removes them.

**Lengths.** For labels of $k = 1, 2, 3, 4, 5$ bits the long code has length $4$, $16$, $256$, $65536$ and $4294967296$, while the Hadamard code has length $2$, $4$, $8$, $16$ and $32$.

## Related definitions

- **Dictator and junta.** A dictator is a function $x \mapsto x_a$, that is a long code word. A $J$-junta is a function that depends on at most $J$ coordinates. A [dictatorship test](/dictatorship-test/) accepts dictators and rejects functions that are far from every junta, or that have no coordinate of large low-degree influence.
- **Hadamard code.** The [Hadamard code](/hadamard-code/) of $\bar a \in \mathbb{F}_2^k$ lists all linear functions of $\bar a$. It is the long code restricted to the linear positions, and it is tested by the [linearity test](/linearity-test/).
- **Low-degree positions.** Keep only the positions $g$ that are polynomials over $\mathbb{F}_2$ of degree at most $d$ in the bits of $\bar a$. For $d = 1$ without constant terms this is the Hadamard code, and for $d = k$ it is the whole long code. Each position is a code word of the [Reed-Muller code](/reed-muller-code/) of degree $d$, and the encoding lists the values of all these code words at $\bar a$.
- **Folded table.** A table with $A(-x) = -A(x)$. It has no Fourier weight on sets of even size.
- **Label cover.** The outer [label cover](/label-cover/) instance assigns a label to each vertex, and the reduction replaces each label by its long code.

## References
