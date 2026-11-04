---
tag: 81NEFR
kind: technique
slug: incompressibility-method
name: Incompressibility method
aliases:
- Kolmogorov complexity method
- Kolmogorov lower bounds
- incompressibility method
- incompressible strings argument
area: foundations/lower-bounds
level: research
summary: Proves a lower bound by fixing an input with no short description and showing that a fast algorithm on it would give a description that is too short.
prereqs: [kolmogorov-complexity, counting-argument, turing-machine]
see_also: [information-theoretic-bound, comparison-sort-lower-bound, pigeonhole-principle, palindrome, prime-number, universal-turing-machine, average-case-analysis, lower-bound]
sources:
  - book: isbn:9780387339986
    title: Ming Li and Paul Vitanyi, An Introduction to Kolmogorov Complexity and Its Applications, third edition, Springer (2008)
    locator: Chapter 6, The Incompressibility Method
  - paper: doi:10.1145/355483.355488
    title: "Tao Jiang, Ming Li and Paul Vitanyi, A lower bound on the average-case complexity of Shellsort, Journal of the ACM 47(5) (2000), 905-911"
    locator: the main theorem (the Omega(p n^(1+1/p)) average-case bound for p-pass Shellsort)
  - paper: doi:10.1016/s0019-9958(65)90399-2
    title: "F. C. Hennie, One-tape, off-line Turing machine computations, Information and Control 8(6) (1965), 553-578"
    locator: the crossing-sequence method for one-tape Turing machines
---

The incompressibility method proves a lower bound by choosing an input that has no description shorter than itself, in the sense of [Kolmogorov complexity](/kolmogorov-complexity/). If an algorithm were fast on that input, a record of its run, plus the algorithm, would describe the input in fewer bits than allowed. Since most strings are incompressible, the bound holds for most inputs, so the same argument gives average-case bounds. It is a [counting argument](/counting-argument/) in another form: the method fixes one typical object and reasons about it, instead of counting over all of them.

## In plain words

Most long bit strings cannot be squeezed: there are not enough short descriptions to go round. Pick one such string and use it as the input.

Now suppose some algorithm is very fast on it. Watch the run and write down only the few things that steered it, such as the answers to its comparisons or the states it was in at one spot on its tape. If those notes, together with the algorithm, let someone rebuild the input, the notes are a description of the input. A fast run gives short notes, and short notes would squeeze a string that cannot be squeezed. So the run cannot be fast.

The method shows that hard inputs exist and that they are the common case. It does not say which input is hard, because no program can test whether a string can be squeezed.

## When it applies

- The problem has many inputs of a given size, and the input can be encoded as a bit string or a number with a fixed encoding.
- A cheap run of the algorithm can be recorded in few bits, and the record, together with the algorithm and some small side information, lets a fixed decoder rebuild the input.
- The resource to bound is tied to the length of that record: comparisons for sorting, crossings of a tape boundary for a one-tape Turing machine, messages for a protocol.
- The goal is a bound for most inputs, or an average-case bound, and a matching worst-case bound follows for free.

It does not apply when the algorithm's run cannot be encoded compactly, or when the hard inputs are a small, structured set: an incompressible input is a typical input, so the method finds bounds that hold for typical inputs.

## The template

Fix a universal machine $U$ and write $C(x \mid y)$ for the length of a shortest program $p$ with $U(p, y) = x$. Two facts drive the method.

**Counting lemma.** For integers $n \ge 1$ and $t \ge 0$, fewer than $2^{t}$ strings $x$ have $C(x \mid y) < t$, for any $y$. There are $2^0 + 2^1 + \cdots + 2^{t-1} = 2^t - 1$ programs of length less than $t$, and each describes at most one $x$. In particular, among the $2^n$ strings of length $n$, at least $2^n - 2^{n-c} + 1$ have $C(x \mid n) \ge n - c$. So fewer than a $2^{-c}$ fraction can be compressed by $c$ bits. At least one string of each length has $C(x \mid n) \ge n$.

**Decoder bound.** For every computable decoder $D$ there is a constant $c_D$ such that if $D(q, y) = x$ then $C(x \mid y) \le |q| + c_D$. This follows from the invariance theorem: $U$ can simulate $D$ given a fixed prefix.

The proof then runs in five steps.

1. Fix the algorithm $A$ and the input size. Choose an input $x$ with $C(x \mid n) \ge n - c$ (or $\ge n$), where $n$ is the number of bits needed to encode an input.
2. Assume, for contradiction, that $A$ uses few resources on $x$.
3. Write a short string $q$ from the run of $A$ on $x$: the bits that determine the run, plus any small side information.
4. Give a fixed decoder $D$ that rebuilds $x$ from $q$ and $n$. It usually works by running $A$, or by trying all candidate inputs and keeping the one whose run matches $q$. Prove that the match is unique.
5. Conclude $n - c \le C(x \mid n) \le |q| + c_D$, which is a lower bound on $|q|$ and hence on the resource. Because the choice of $x$ covered all but a $2^{-c}$ fraction of inputs, the bound holds for that fraction too.

## Classic examples

### There are infinitely many primes

Suppose there are only $k$ [primes](/prime-number/) $p_1, \ldots, p_k$. Each integer $m \ge 2$ is $p_1^{e_1} \cdots p_k^{e_k}$ with each $e_i \le \log_2 m$. Take $\ell$ large and let $m$ be an $\ell$-bit number with $C(m) \ge \ell - 1$. Such an $m$ exists, since there are $2^{\ell - 1}$ numbers with exactly $\ell$ bits and fewer than $2^{\ell - 1}$ programs shorter than $\ell - 1$.

Describe $m$ as follows. Let $w = \lceil \log_2(\ell + 1) \rceil$, so each $e_i < 2^w$. Write $w$ in a self-delimiting way, by doubling each of its bits and ending with $01$, which takes $2\lceil\log_2(w+1)\rceil + 2$ bits. Then write $e_1, \ldots, e_k$ in $w$ bits each. A fixed decoder that knows the list of $k$ primes reads $w$, then the exponents, and multiplies. So

$$
\ell - 1 \le C(m) \le k w + 2\lceil \log_2(w+1) \rceil + 2 + c,
$$

and the right side is $O(\log \ell)$ for fixed $k$. This fails for large $\ell$, so the list of primes cannot be finite.

### Average-case comparison sorting

Fix a deterministic comparison sort $A$ (see [comparison sort lower bound](/comparison-sort-lower-bound/)). Model: inputs are the $n!$ permutations $\pi$ of $\{1, \ldots, n\}$, and the cost is the number $k(\pi)$ of comparisons $A$ makes on $\pi$.

Record the outcomes of the comparisons as a bit string $b(\pi)$ of length $k(\pi)$. A decoder given $n$ and $b(\pi)$ runs $A$, answering the $j$-th comparison with the $j$-th bit. The run is the same as on $\pi$, so at the end the decoder knows the sorted order, that is, where each position of the input goes, and it outputs $\pi$. With $\pi$ encoded by its index among the $n!$ permutations,

$$
C(\pi \mid n) \le k(\pi) + c_A .
$$

By the counting lemma with $t = \lfloor \log_2 n! \rfloor - c$, fewer than $2^{t} \le 2^{-c}\, n!$ permutations have $C(\pi \mid n) < t$. So for at least a $(1 - 2^{-c})$ fraction of permutations,

$$
k(\pi) \ge \lfloor \log_2 n! \rfloor - c - c_A ,
$$

and the average cost is at least $(1 - 2^{-c})(\lfloor \log_2 n! \rfloor - c - c_A)$. Taking $c = \lceil \log_2 n \rceil$ gives an average of $\log_2 n! - O(\log n) = n \log_2 n - O(n)$ comparisons.

| $n$ | $\log_2 n!$ | $\lfloor \log_2 n! \rfloor$ |
|---|---|---|
| 5 | 6.91 | 6 |
| 10 | 21.79 | 21 |
| 20 | 61.08 | 61 |
| 100 | 524.76 | 524 |

With $c = 10$, all but fewer than $1/1024$ of the $100!$ inputs need at least $514 - c_A$ comparisons.

### Palindromes on a one-tape Turing machine

**Model.** $M$ is a deterministic one-tape [Turing machine](/turing-machine/) with state set $Q$, $|Q| \ge 2$. The input is written on the tape, the head starts on its first cell, and $M$ halts on every input, accepting exactly the [palindromes](/palindrome/) over $\{0, 1\}$. The cost is the number of steps, in the worst case over inputs of length $N$.

**Claim.** $M$ takes $\Omega(N^2)$ steps on some input of each large length $N$.

*Crossing sequences.* Number the cells $1, 2, \ldots$ and call the boundary between cells $i$ and $i+1$ boundary $i$. The crossing sequence $\mathrm{CS}_i(w)$ is the list of states $M$ enters at the steps where the head moves across boundary $i$, in order. Each step crosses at most one boundary, so the running time on $w$ is at least $\sum_i |\mathrm{CS}_i(w)|$.

*Cut-and-paste lemma.* Let $M$ accept $uv$ and $u'v'$, with $|u|, |u'| \ge 1$, and suppose the crossing sequence at the boundary after $u$ in the run on $uv$ equals the crossing sequence at the boundary after $u'$ in the run on $u'v'$. Then $M$ accepts $uv'$.

*Proof.* Call the common sequence $(q_1, \ldots, q_r)$. Since the head starts on the left of each cut, odd crossings go from left to right and even crossings from right to left. Consider the run on $uv'$. Up to the first crossing it stays left of the cut and sees only $u$, so it matches the run on $uv$ and crosses in state $q_1$. From there until the second crossing it stays right of the cut, enters in state $q_1$ and sees $v'$ with the right part of the tape untouched, so it matches the run on $u'v'$ after its first crossing and comes back in state $q_2$. By induction on the crossings, each time segment on the left matches the run on $uv$ and each segment on the right matches the run on $u'v'$, with the same tape contents on that side. After the $r$-th crossing the run stays on one side until it halts: on the left if $r$ is even, matching the end of the run on $uv$, and on the right if $r$ is odd, matching the end of the run on $u'v'$. Both of those accept, so $M$ accepts $uv'$. $\square$

*The bound.* Let $n = \lfloor N/3 \rfloor$ and $k = N - 2n$, so $n \le k \le n + 2$. Choose $x \in \{0,1\}^n$ with $C(x \mid N) \ge n$ and consider $w = x\, 0^k\, x^R$, a palindrome of length $N$. Fix a boundary $i$ with $n \le i \le n + k$, inside or at the edge of the block of zeros, and let $S = \mathrm{CS}_i(w)$.

The decoder $D$ gets $N$ and the string $q$ made of $i - n$ written in exactly $\lceil \log_2(k+1) \rceil$ bits, followed by the states of $S$ written in $\lceil \log_2 |Q| \rceil$ bits each. From $N$ it computes $n$, $k$ and the width of the first field, so it can split $q$. It then runs $M$ on $y\, 0^k\, y^R$ for every $y \in \{0,1\}^n$ and outputs the first $y$ whose crossing sequence at boundary $i$ equals $S$.

The output is $x$. If $y \ne x$ had the same crossing sequence, the lemma with $u = x 0^{i-n}$, $v = 0^{n+k-i} x^R$, $u' = y 0^{i-n}$, $v' = 0^{n+k-i} y^R$ would make $M$ accept $x\, 0^k\, y^R$, which is not a palindrome. So

$$
n \le C(x \mid N) \le \lceil \log_2(k+1) \rceil + |S| \lceil \log_2 |Q| \rceil + c_D ,
$$

and since $k \le n + 2$,

$$
|\mathrm{CS}_i(w)| \ge \frac{n - \log_2(n + 3) - 1 - c_D}{\lceil \log_2 |Q| \rceil}
$$

for each of the $k + 1 \ge n + 1$ boundaries in the block. Summing, $M$ takes at least $(n+1)$ times this many steps on $w$, which is $\Omega(n^2) = \Omega(N^2)$, with the constant depending on $M$. A one-tape machine that walks back and forth comparing the outer symbols runs in $O(N^2)$ steps, so the bound is tight up to a constant factor.

## Variations

- **Average case for free.** In the sorting example the incompressible inputs are all but a $2^{-c}$ fraction, so a bound for them is a bound on the average. Jiang, Li and Vitanyi used this route to prove that every $p$-pass Shellsort takes $\Omega(p\, n^{1 + 1/p})$ time on average under the uniform distribution on permutations.
- **Prefix complexity.** Some arguments concatenate several descriptions. With prefix-free complexity $K$, descriptions can be joined without length fields. Since $K(x) \le C(x) + O(\log |x|)$ and $C(x) \le K(x) + O(1)$, switching between the two costs at most a logarithmic term. The primes example above uses plain complexity and writes the length field by hand.
- **Conditioning.** Conditioning on the input length $n$, or on other public data such as $N$ in the palindrome proof, removes the $O(\log n)$ bits otherwise needed to tell the decoder where the input ends.
- **Other objects.** Graphs, matrices and permutations are encoded as bit strings by a fixed rule. For a graph on $n$ vertices the incompressible string is its list of $\binom{n}{2}$ adjacency bits, and the template applies unchanged.

## Pitfalls

- **Existence only.** $C$ is not computable, so the method never exhibits a hard input. No algorithm decides whether a given string is incompressible, so the proof cannot be turned into a search for a hard input.
- **Constants.** $c_D$ depends on the universal machine and on the decoder, and the decoder contains the algorithm $A$ or the machine $M$. Bounds are asymptotic in $n$ for each fixed algorithm, and they say nothing for $n$ smaller than these constants.
- **Uniqueness of decoding.** The step that is easiest to get wrong is showing that the record determines the input. In the palindrome proof the cut-and-paste lemma is what rules out a second candidate; without such an argument the description is not a description.
- **Hidden side information.** Everything the decoder uses must be counted: positions such as the boundary $i$, the lengths of fields, the number of items. A field of unknown length needs a self-delimiting code or conditioning on public data.
- **Plain versus prefix.** Mixing $C$ and $K$, or forgetting that a concatenation of plain descriptions is not itself a description, introduces errors of order $\log n$. These are harmless for an $\Omega(N^2)$ bound but not for bounds that are tight up to additive terms.
- **Typical, not worst.** An incompressible input is typical. A problem whose hard instances are rare and structured needs a different technique, such as an [adversary argument](/adversary-argument/).

## Exercises

1. Show that at least half of the strings of length $n$ have $C(x \mid n) \ge n - 1$, and at least $1 - 2^{-c}$ of them have $C(x \mid n) \ge n - c$.
2. Show that if $x$ has length $2m$ and its two halves are equal, then $C(x \mid 2m) \le m + c$ for a constant $c$ that does not depend on $x$.
3. Use the sorting argument to show that every deterministic comparison sort makes at least $\lfloor \log_2 n! \rfloor - c_A$ comparisons on some input.
4. Adapt the palindrome proof to the language $\{\, x\, 0^{k}\, x : x \in \{0,1\}^{*},\ k \ge |x| \,\}$ and show that a one-tape machine needs $\Omega(N^2)$ steps on some input of each large length $N$.
5. Explain why the counting lemma gives a string with $C(x \mid n) \ge n$ for every $n$, but no program can output such a string for every $n$. (Hint: if one could, consider the length of that program as $n$ grows.)

## References
