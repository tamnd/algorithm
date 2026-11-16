---
tag: B9HS1Y
kind: technique
slug: discrepancy-method
name: Discrepancy method
aliases:
- discrepancy bound
area: complexity/communication-and-query-complexity
level: research
summary: "A lower bound on randomized communication. If every rectangle is nearly balanced between 0s and 1s under some distribution, a protocol with small error needs many rectangles."
prereqs: [randomized-communication-complexity, yao-minimax-principle]
see_also: [inner-product-problem, corruption-bound, fooling-set-method, log-rank-lower-bound, sign-rank, disjointness-problem, number-on-forehead-model, walsh-hadamard-transform]
sources:
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: Chapter 3, Randomization (distributional complexity and the discrepancy bound, with inner product as the example)
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 5, Discrepancy
  - paper: "László Babai, Péter Frankl and Janos Simon, Complexity classes in communication complexity theory, Proceedings of the 27th IEEE Symposium on Foundations of Computer Science (FOCS 1986), 337-347"
    locator: the discrepancy argument and the classes of communication complexity
  - paper: "Benny Chor and Oded Goldreich, Unbiased bits from sources of weak randomness and probabilistic communication complexity, SIAM Journal on Computing 17(2) (1988)"
    locator: the bias bound for inner product on rectangles and the randomized lower bound
  - paper: "László Babai, Noam Nisan and Mario Szegedy, Multiparty protocols, pseudorandom generators for logspace, and time-space trade-offs, Journal of Computer and System Sciences 45(2) (1992), 204-232"
    locator: discrepancy over cylinder intersections and the generalized inner product bound
---

The discrepancy method proves lower bounds on [randomized communication complexity](/randomized-communication-complexity/). It fixes a distribution $\mu$ on the inputs and shows that every rectangle of the [communication matrix](/communication-matrix/) has almost the same $\mu$-weight of 0-entries as of 1-entries. A protocol that sends $c$ bits splits the inputs into at most $2^c$ rectangles, and each one adds very little to the advantage over a random guess. So a protocol with advantage $\varepsilon$ needs about $\log_2(\varepsilon/\text{discrepancy})$ bits. The method gives $\Omega(n)$ for [inner product](/inner-product-problem/), and it bounds the cost even when the advantage is tiny.

## In plain words

A short talk between Alice and Bob sorts all possible input pairs into a few blocks, and the answer must be the same for all pairs in one block. If every large block holds about as many "yes" pairs as "no" pairs, then any fixed answer for a block is right on only about half of it.

The method finds a way to weigh the inputs so that every block is balanced in this sense. Then a short talk is right only a little more often than a coin toss. To be right much more often than a coin toss, the talk needs many blocks, so it must be long. Random choices do not help, because a random talk is a mix of fixed talks, and each of them has this weakness.

## When it applies

Use it for a lower bound on the distributional cost $D^{\mu}_{1/2 - \varepsilon}(f)$, the least cost of a deterministic protocol that errs on at most a $1/2 - \varepsilon$ fraction of the $\mu$-weight. By [Yao's minimax principle](/yao-minimax-principle/), this bounds the public-coin cost $R_{1/2-\varepsilon}(f)$, and so also the private-coin cost. The method works when $f$ looks random on every large rectangle: inner product, random functions, and functions built from Hadamard matrices.

It fails when $f$ has a large rectangle that is close to monochromatic under every distribution. Equality and greater-than have small randomized cost, so their discrepancy must be large for every $\mu$. [Disjointness](/disjointness-problem/) is the important case: its randomized cost is $\Theta(n)$, but the method gives only $O(\log n)$, as shown under Classic examples. For such functions use the [corruption bound](/corruption-bound/), which looks at one value of $f$ only.

## The template

**Definitions.** Let $\mu$ be a distribution on $X \times Y$. For a rectangle $R = A \times B$,

$$\operatorname{disc}_\mu(R, f) = \left| \mu(R \cap f^{-1}(1)) - \mu(R \cap f^{-1}(0)) \right|,$$

and $\operatorname{disc}_\mu(f)$ is the largest value over all rectangles. The discrepancy of $f$ is the least of $\operatorname{disc}_\mu(f)$ over all $\mu$.

**The bound.** For every $\mu$ and $0 < \varepsilon \le 1/2$,

$$D^{\mu}_{1/2 - \varepsilon}(f) \ge \log_2 \frac{2\varepsilon}{\operatorname{disc}_\mu(f)}.$$

*Proof.* Take a deterministic protocol with $c$ bits and $\mu$-error at most $1/2 - \varepsilon$. Its leaves give at most $2^c$ disjoint rectangles $R_\ell$ that cover $X \times Y$, and leaf $\ell$ outputs a value $o_\ell$. The probability of a correct answer minus the probability of a wrong answer is at least $(1/2 + \varepsilon) - (1/2 - \varepsilon) = 2\varepsilon$. This difference is

$$\sum_\ell \left( \mu(R_\ell \cap f^{-1}(o_\ell)) - \mu(R_\ell \cap f^{-1}(1 - o_\ell)) \right) \le \sum_\ell \operatorname{disc}_\mu(R_\ell, f) \le 2^c \operatorname{disc}_\mu(f).$$

So $2^c \ge 2\varepsilon / \operatorname{disc}_\mu(f)$. $\blacksquare$

```pseudo id=main
DISCREPANCY-BOUND(f, ε)
L1  choose a distribution ⟨μ⟩ on X × Y
L2  for every rectangle R = A × B, prove disc_μ(R, f) ≤ ⟨δ⟩      ▷ ⟨bias argument⟩
L3  a deterministic c-bit protocol has at most 2^c leaf rectangles
L4  its advantage 2ε is at most the sum of disc_μ over the leaves, so 2ε ≤ 2^c δ
L5  conclude D^μ_{1/2-ε}(f) ≥ log2(2ε / δ)
L6  by Yao's principle, R_{1/2-ε}(f) ≥ log2(2ε / δ) for public and private coins
```

The holes are the distribution $\langle \mu \rangle$, the bound $\langle \delta \rangle$, and the $\langle$bias argument$\rangle$. The usual bias argument is spectral. Let $S$ be the sign matrix with entries $S_{xy} = (-1)^{f(x,y)}$ and $\mu$ uniform. Then for $A \times B$,

$$\Big|\sum_{x \in A, y \in B} S_{xy}\Big| = |\mathbf{1}_A^{\mathsf T} S\, \mathbf{1}_B| \le \lVert S \rVert \sqrt{|A|\,|B|},$$

where $\lVert S \rVert$ is the largest [singular value](/singular-value-decomposition/). Dividing by $|X||Y|$ gives $\delta = \lVert S \rVert / \sqrt{|X|\,|Y|}$.

## Classic examples

**Inner product (Chor and Goldreich 1988; Babai, Frankl and Simon 1986).** Fill $\langle \mu \rangle$ with the uniform distribution on $\{0,1\}^n \times \{0,1\}^n$. The sign matrix is the Hadamard matrix $H_n$ with $H_n^{\mathsf T} H_n = 2^n I$, so $\lVert H_n \rVert = 2^{n/2}$ and $\langle \delta \rangle = 2^{n/2}/2^n = 2^{-n/2}$ (Lindsey's lemma). With error $1/3$, $\varepsilon = 1/6$ and line L5 gives $R(\mathrm{IP}_n) \ge n/2 - \log_2 3$. An exhaustive search for $n = 4$ gives the exact uniform discrepancy $7/64$ against the bound $1/4$, and the bound of line L5 becomes $\log_2(64/21) \approx 1.61$, so at least 2 bits. See the [inner product problem](/inner-product-problem/) for the full table.

**Random functions.** For a uniformly random $f$, the $2^n \times 2^n$ sign matrix has spectral norm $O(2^{n/2})$ with high probability, so $\delta = O(2^{-n/2})$ and most functions need $n/2 - O(1)$ bits even for a constant advantage.

**Generalized inner product with $k$ players (Babai, Nisan and Szegedy 1992).** In the [number-on-forehead model](/number-on-forehead-model/) the leaves are not rectangles but cylinder intersections. The same template, with "rectangle" replaced by "cylinder intersection" in lines L2 and L3, gives $\Omega(n/4^k)$ for the generalized inner product. The bias argument there uses $k - 1$ applications of Cauchy-Schwarz.

**Disjointness: where the method fails.** The 0-entries of $M_{\mathrm{DISJ}_n}$ lie in the $n$ rectangles $R_i = \{x_i = 1\} \times \{y_i = 1\}$, each of which holds only 0-entries. Fix any $\mu$ and let $p_0$ and $p_1$ be the weights of the 0-entries and the 1-entries. Each $R_i$ has discrepancy $\mu(R_i)$, so $p_0 \le \sum_i \mu(R_i) \le n \operatorname{disc}_\mu$. The full matrix has discrepancy $|p_1 - p_0|$, so $p_1 \le p_0 + \operatorname{disc}_\mu$. Adding, $1 = p_0 + p_1 \le (2n + 1)\operatorname{disc}_\mu$. So $\operatorname{disc}_\mu(\mathrm{DISJ}_n) \ge 1/(2n+1)$ for every $\mu$, and line L5 gives at most $\log_2(2\varepsilon(2n+1)) = O(\log n)$. For $n = 2$ and 200 random distributions (seed 3), the smallest discrepancy found was $0.2912$, above the bound $1/5$.

## Variations

- **Spectral form.** As in the template, $\operatorname{disc}_{\mathrm{unif}}(f) \le \lVert S \rVert / \sqrt{|X||Y|}$. This is the eigenvalue method; it needs only one number from linear algebra.
- **Weak advantage.** The bound grows only like $\log_2 \varepsilon$ as the advantage $\varepsilon$ shrinks. So it also bounds the cost of protocols with error $1/2 - 2^{-n/3}$, where other methods say nothing. This is how inner product is placed outside the class $\mathsf{PP}^{cc}$ of Babai, Frankl and Simon, the protocols with polylogarithmic cost and advantage at least $2^{-\mathrm{polylog}(n)}$.
- **Generalized discrepancy.** Replace $f$ by a function $g$ that is correlated with $f$ under $\mu$ and has small discrepancy. This handles some functions with large discrepancy, and it is the core of the pattern matrix method of Sherstov, which turns a lower bound on [approximate degree](/approximate-degree/) into a communication lower bound.
- **Multiparty.** Cylinder intersections take the place of rectangles, as in the example of Babai, Nisan and Szegedy.

## Pitfalls

- The method bounds distributional cost under one fixed $\mu$. A lower bound on $R(f)$ needs the step through Yao's principle, which holds for public coins; the private-coin bound follows because private coins are never cheaper.
- Small discrepancy under one $\mu$ is enough for a lower bound. Large discrepancy under one $\mu$ proves nothing; to show that the method fails, as for disjointness, one needs a large rectangle under every $\mu$.
- The error is $1/2 - \varepsilon$, not $\varepsilon$. With error $1/3$, put $\varepsilon = 1/6$.
- The bound counts leaves, not depth along one path, so it bounds the worst-case cost. It does not directly bound the expected cost of a protocol with variable length.
- Do not confuse the discrepancy of $f$ with the [sign rank](/sign-rank/). Small discrepancy gives a lower bound for protocols with a fixed advantage; sign rank characterizes protocols with any advantage above zero.

## Exercises

1. Show that for the uniform distribution, the equality function on $n$ bits has discrepancy at least $1 - 2^{1-n}$. Why does this not contradict its small randomized cost?
2. Prove that $\operatorname{disc}_\mu(f) \ge \mu(R)$ for every monochromatic rectangle $R$. Conclude that the discrepancy method can never beat the largest monochromatic rectangle bound by much.
3. Let $f$ have a $2^n \times 2^n$ sign matrix with orthogonal rows. Show that $R(f) \ge n/2 - O(1)$.
4. Use the discrepancy bound with $\varepsilon = 2^{-n/4}$ to show that every protocol for $\mathrm{IP}_n$ with error at most $1/2 - 2^{-n/4}$ sends at least $n/4 - O(1)$ bits.
5. Show that for $\mathrm{DISJ}_n$ the uniform distribution gives a discrepancy that does not even go to 0. Hint: most pairs of random sets intersect.

## References
