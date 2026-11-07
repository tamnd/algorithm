---
tag: 31877A
kind: concept
slug: bit-reversal-permutation
name: Bit-reversal permutation
aliases:
- bit-reversal ordering
- bit-reversed order
- revbin permutation
area: algebra/fast-transforms
level: core
summary: Reordering of indices by reversing their binary digits, used to run an iterative FFT in place.
prereqs: [permutation, bitwise-operations]
see_also: [fast-fourier-transform, iterative-fft, butterfly-operation, bit-reversal, in-place-permutation, dft-matrix, fast-walsh-hadamard-transform]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Section 30.3, Efficient FFT implementations (the order of the leaves of the recursion tree and the procedure that copies the input in bit-reversed order)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 1, Section 1.5, Bit Reversal and Transposition (the permutation P_n of the Cooley-Tukey factorization and algorithms that apply it)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 2, Section 2.6, The revbin permutation (in-place swapping, the count of fixed points, and fast ways to step through reversed indices)
  - paper: doi:10.1137/1038001
    title: Alan H. Karp, Bit reversal on uniprocessors, SIAM Review 38(1), 1996
    locator: pp. 1 to 26 (a survey and comparison of many bit-reversal algorithms and their memory behaviour)
---

The bit-reversal permutation of length $n = 2^t$ sends the index $j$ to the index $\mathrm{rev}_t(j)$ whose $t$ binary digits are those of $j$ in reverse order. For $n = 8$ it maps $0, 1, \ldots, 7$ to $0, 4, 2, 6, 1, 5, 3, 7$. It is the order in which the radix-2 [fast Fourier transform](/fast-fourier-transform/) visits its input: after the even and odd entries are split again and again, the entry $x_{\mathrm{rev}(j)}$ ends up in position $j$. Permuting the input once into this order lets the [iterative FFT](/iterative-fft/) run its [butterflies](/butterfly-operation/) in place, in $\lg n$ passes over one array.

## In plain words

Number the positions of a list from zero, and write each number in binary with the same number of digits. Now read each number backwards. The new number tells where the entry at that position goes. The first and the last entries stay where they are, and the others are swapped in pairs.

Why this odd order? The fast Fourier transform deals out the list like cards into two piles, even places and odd places, and then deals each pile out again, and so on. Each deal looks at the next binary digit of a position, from the right. When the dealing ends, the cards lie in the order of their positions read backwards.

## The idea

**Definition.** Let $n = 2^t$ with $t \ge 0$. For $0 \le j < n$ with binary digits $j = \sum_{s=0}^{t-1} j_s 2^s$, define

$$\mathrm{rev}_t(j) = \sum_{s=0}^{t-1} j_s \, 2^{t-1-s}.$$

The bit-reversal permutation $P_n$ maps a vector $x \in R^n$ to $y$ with $y_j = x_{\mathrm{rev}_t(j)}$. The length must be a power of two, and the reversal depends on $t$: $\mathrm{rev}_3(1) = 4$ but $\mathrm{rev}_4(1) = 8$.

**It is an involution.** Reversing twice gives the original digits, so $\mathrm{rev}_t(\mathrm{rev}_t(j)) = j$ and $P_n^{-1} = P_n$. So $P_n$ is a product of disjoint transpositions $(j, \mathrm{rev}_t(j))$ over the pairs with $j < \mathrm{rev}_t(j)$, and it can be applied in place by one pass with swaps:

for $j = 0, \ldots, n - 1$: if $j < \mathrm{rev}_t(j)$, swap $x_j$ and $x_{\mathrm{rev}_t(j)}$.

The test $j < \mathrm{rev}_t(j)$ makes each pair swap once. The fixed points are the indices whose digit string is a palindrome, and there are $2^{\lceil t/2 \rceil}$ of them, so the pass makes $\frac{1}{2}(n - 2^{\lceil t/2 \rceil})$ swaps.

**Why the FFT produces it.** The radix-2 split puts the entries with $j_0 = 0$ (even $j$) in the first half and those with $j_0 = 1$ in the second half, each half in increasing order of $j \gg 1$. *Claim:* after $t$ levels of this split, position $p$ holds $x_{\mathrm{rev}_t(p)}$. *Proof by induction on $t$.* For $t = 0$ there is one entry. For $t \ge 1$, position $p = p_{t-1} 2^{t-1} + p'$ with $p' < 2^{t-1}$ lies in the half chosen by $j_0 = p_{t-1}$, and inside that half the induction hypothesis puts there the entry whose index $j \gg 1$ is $\mathrm{rev}_{t-1}(p')$. So $j = 2 \, \mathrm{rev}_{t-1}(p') + p_{t-1} = \mathrm{rev}_t(p)$. $\square$ In matrix form this is the factorization $F_n = A_t \cdots A_1 P_n$ of the [DFT matrix](/dft-matrix/), where each $A_q$ is a stage of butterflies.

**Computing the reversed indices.**

- *Directly.* Reverse each index with a loop over its $t$ digits, or with the word tricks on the [bit reversal](/bit-reversal/) page: $O(n \log n)$ word operations in total.
- *By a recurrence.* $\mathrm{rev}_t(0) = 0$ and, for $j \ge 1$, $\mathrm{rev}_t(j) = (\mathrm{rev}_t(j \gg 1) \gg 1) \mid ((j \mathbin{\&} 1) \ll (t - 1))$. This fills a table of all $n$ values with $O(n)$ operations.
- *By a reversed counter.* Keep $r = \mathrm{rev}_t(j)$ and add $1$ "from the left": clear the leading ones of $r$ from the top digit down, and set the first zero digit. This takes amortized $O(1)$ operations per step, for the same reason that an ordinary binary counter does.

**Memory behaviour.** The swaps jump between distant positions, so for large $n$ a naive pass has poor cache locality, and on modern machines it can take a noticeable share of the FFT time. Blocked and cache-aware methods, compared in Karp's survey, reorganize the swaps. Many FFT libraries avoid the explicit permutation altogether: the Stockham form uses a second array and natural order, and a decimation-in-frequency forward transform followed by a decimation-in-time inverse transform cancels the two permutations, which is enough for [convolution](/convolution-via-fft/).

## Examples

- $n = 8$ ($t = 3$): $\mathrm{rev}_3 = (0, 4, 2, 6, 1, 5, 3, 7)$. For instance $j = 3 = 011_2$ becomes $110_2 = 6$. The fixed points are $0, 2, 5, 7$ (the palindromes $000, 010, 101, 111$), and the swaps are $(1, 4)$ and $(3, 6)$.
- $n = 16$ ($t = 4$): $\mathrm{rev}_4 = (0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15)$, with fixed points $0, 6, 9, 15$ and $6$ swaps.
- $n = 4$: $(x_0, x_1, x_2, x_3) \mapsto (x_0, x_2, x_1, x_3)$, a single swap. This is the order $(1, 3, 2, 4)$ used for $x = (1, 2, 3, 4)$ in the length-$4$ example on the [butterfly](/butterfly-operation/) page.
- $n = 1$ and $n = 2$: the permutation is the identity.
- Splitting $(0, 1, \ldots, 7)$ into even and odd places gives $(0, 2, 4, 6 \mid 1, 3, 5, 7)$, then $(0, 4 \mid 2, 6 \mid 1, 5 \mid 3, 7)$: the order $\mathrm{rev}_3$, as the claim says.

## Where it is used

- **The iterative radix-2 FFT**, in the form of CLRS and of most textbooks: permute the input by $P_n$, then run $\lg n$ stages of in-place butterflies. The [number-theoretic transform](/number-theoretic-transform/) uses the same layout.
- **Decimation in frequency.** The Gentleman-Sande FFT reads natural order and writes bit-reversed order, so the permutation is applied at the end instead.
- **The [Walsh-Hadamard transform](/fast-walsh-hadamard-transform/)** in the Walsh (sequency) ordering, which differs from the natural Hadamard ordering by a bit reversal combined with a Gray code.
- **Other transforms.** Radix-$r$ FFTs use the analogous digit reversal in base $r$. In the [quantum Fourier transform](/quantum-fourier-transform/), the output qubits come out in reversed order and are put back by swap gates.

## References
