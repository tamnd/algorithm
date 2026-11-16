---
tag: KJ06DP
kind: technique
slug: corruption-bound
name: Corruption bound
aliases:
- Yao's corruption bound
area: complexity/communication-and-query-complexity
level: research
summary: "A lower bound on randomized communication. If every large rectangle has a fixed fraction of 0-inputs under a distribution, a protocol with small error needs many rectangles for the 1-inputs."
prereqs: [randomized-communication-complexity, yao-minimax-principle, discrepancy-method]
see_also: [disjointness-problem, gap-hamming-distance, discrepancy-method, fooling-set-method, information-complexity, nondeterministic-communication-complexity, direct-sum-communication]
sources:
  - paper: "Andrew Chi-Chih Yao, Lower bounds by probabilistic arguments, Proceedings of the 24th IEEE Symposium on Foundations of Computer Science (FOCS 1983), 420-428"
    locator: the first use of the argument with nearly monochromatic rectangles
  - paper: "Alexander A. Razborov, On the distributional complexity of disjointness, Theoretical Computer Science 106(2) (1992), 385-390"
    locator: the corruption lemma for disjointness under the hard distribution
  - paper: "László Babai, Péter Frankl and Janos Simon, Complexity classes in communication complexity theory, Proceedings of the 27th IEEE Symposium on Foundations of Computer Science (FOCS 1986), 337-347"
    locator: the Omega(sqrt n) bound for disjointness under a product distribution
  - paper: "Alexander A. Sherstov, Communication complexity theory: thirty-five years of set disjointness, Mathematical Foundations of Computer Science (MFCS 2014)"
    locator: the corruption bound in the form used on this page (Theorem 6), with the bounds of Babai, Frankl and Simon (Theorem 7) and of Razborov
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 3, Randomized Protocols (section Nearly Monochromatic Rectangles)
  - paper: "Paul Beame, Toniann Pitassi, Nathan Segerlind and Avi Wigderson, A strong direct product theorem for corruption and the multiparty communication complexity of disjointness, Computational Complexity 15(4) (2006), 391-432"
    locator: the direct product theorem for the corruption bound
---

The corruption bound proves lower bounds on [randomized communication complexity](/randomized-communication-complexity/) by looking at one output value only. It fixes a distribution $\mu$ and shows that every rectangle of the [communication matrix](/communication-matrix/) with noticeable weight is "corrupted": a fixed fraction of its weight lies on inputs with $f = 0$. A protocol with small error must then cover most of the weight of the 1-inputs with rectangles that are almost free of 0-inputs, and these rectangles are all small, so it needs many of them. Unlike the [discrepancy method](/discrepancy-method/), it works for [disjointness](/disjointness-problem/), where it gives Razborov's $\Omega(n)$ bound.

## In plain words

A short talk sorts all input pairs into a few blocks and gives one answer for each block. A block that answers "yes" must hold mostly "yes" pairs, or the talk makes too many mistakes.

The method shows that every large block holds a fair share of "no" pairs. So every block that may answer "yes" is small. To answer "yes" on most of the "yes" pairs, the talk needs many small blocks, and so it must be long.

The difference from the discrepancy method is that only one answer counts. Large blocks full of "no" pairs are allowed. This matters for the question of a common element, where large blocks with only "no" pairs exist.

## When it applies

Use it for a lower bound on $R_\varepsilon(f)$, the public-coin cost with error $\varepsilon$, when one value of $f$ (here 1) is hard to certify: every large rectangle mixes in a constant fraction of 0-inputs. It works with a small constant error $\varepsilon$ below a threshold set by the corruption constant, and standard amplification then gives the bound for error $1/3$ up to a constant factor. Private-coin costs are at least public-coin costs, so the bound holds for both.

It is the method of choice when the discrepancy is large because of big monochromatic rectangles of the other value, as for disjointness. It does not help when both values have large nearly monochromatic rectangles, as for equality, whose randomized cost is $O(1)$.

## The template

**Corruption bound (as stated in Sherstov's survey, Theorem 6).** Let $\mu$ be a distribution on $X \times Y$, and let $0 < \alpha \le 1$ and $\beta > 0$. Suppose that every rectangle $R$ satisfies

$$\mu(R \cap f^{-1}(0)) \ge \alpha\, \mu(R) - \beta.$$

Then $R_\varepsilon(f) \ge \log_2 \dfrac{\alpha\, \mu(f^{-1}(1)) - \varepsilon}{\beta}$.

*Proof.* By [Yao's minimax principle](/yao-minimax-principle/) it is enough to bound a deterministic protocol with $c$ bits and $\mu$-error at most $\varepsilon$. Let $R_1, \ldots, R_t$ be the leaf rectangles with output 1, so $t \le 2^c$. Let $\varepsilon_1$ be the weight of 1-inputs that reach 0-leaves, and $w = \sum_j \mu(R_j \cap f^{-1}(0))$ the weight of 0-inputs that reach 1-leaves; then $\varepsilon_1 + w \le \varepsilon$. The 1-leaves hold the rest of the 1-inputs, so $\sum_j \mu(R_j) \ge \mu(f^{-1}(1)) - \varepsilon_1$. By the hypothesis on each $R_j$,

$$w \ge \alpha \sum_j \mu(R_j) - t\beta \ge \alpha\,(\mu(f^{-1}(1)) - \varepsilon_1) - t\beta.$$

Since $\alpha \le 1$, we get $t\beta \ge \alpha\,\mu(f^{-1}(1)) - \varepsilon_1 - w \ge \alpha\,\mu(f^{-1}(1)) - \varepsilon$. So $2^c \ge t \ge (\alpha\,\mu(f^{-1}(1)) - \varepsilon)/\beta$. $\blacksquare$

```pseudo id=main
CORRUPTION-BOUND(f, ε)
L1  choose the value ⟨z⟩ to certify (here 1) and a distribution ⟨μ⟩ with μ(f^{-1}(z)) = Ω(1)
L2  prove, for every rectangle R: μ(R ∩ f^{-1}(1 - z)) ≥ ⟨α⟩ μ(R) - ⟨β⟩      ▷ ⟨corruption lemma⟩
L3  a deterministic c-bit protocol with μ-error ε has t ≤ 2^c leaves with output z
L4  those leaves hold weight at least μ(f^{-1}(z)) - ε of z-inputs, and at most ε of the other inputs
L5  combine with L2: t β ≥ α μ(f^{-1}(z)) - ε
L6  return R_ε(f) ≥ log2((α μ(f^{-1}(z)) - ε) / β); amplify to error 1/3
```

The holes are the value $\langle z \rangle$, the distribution $\langle \mu \rangle$, the constants $\langle \alpha \rangle$ and $\langle \beta \rangle$, and the $\langle$corruption lemma$\rangle$. All the work is in the lemma. The bound is useful when $\beta$ is exponentially small, since the result is about $\log_2(1/\beta)$.

## Classic examples

**Disjointness under Razborov's distribution (Razborov 1992).** Let $m = \lfloor n/4 \rfloor$. Fill $\langle z \rangle = 1$ (disjoint) and let $\langle \mu \rangle$ put weight $3/4$ on uniformly random disjoint pairs with $|x| = |y| = m$, and $1/4$ on uniformly random pairs with $|x| = |y| = m$ and $|x \cap y| = 1$. Razborov proved the corruption lemma with a constant $\alpha > 0$ and $\beta = 2^{-\delta n}$ for a constant $\delta > 0$: every rectangle of weight above $2^{-\delta n}$ has a constant fraction of its weight on intersecting pairs. Line L6 gives $R_\varepsilon(\mathrm{DISJ}_n) \ge \delta n + \log_2(3\alpha/4 - \varepsilon) = \Omega(n)$ for small constant $\varepsilon$. The proof of the lemma is an entropy argument on the random partition of $[n]$ into the parts that hold $x$, $y$ and the rest.

**Disjointness under a product distribution (Babai, Frankl and Simon 1986).** Let $x$ and $y$ be independent uniform subsets of size $\sqrt{n}$. Two such sets meet with constant probability, and every rectangle of weight above $2^{-\Omega(\sqrt{n})}$ has a constant fraction of intersecting pairs. This gives $\Omega(\sqrt{n})$. No product distribution can give more than $O(\sqrt{n} \log n)$, so the step to Razborov's correlated distribution is needed.

**Why small sets fail.** Take $n = 4$ and sets of size 1: weight $3/4$ spread over the 12 disjoint pairs $(\{i\}, \{j\})$ with $i \ne j$, and $1/4$ over the 4 pairs $(\{i\}, \{i\})$. The rectangle $\{\{1\}, \{2\}\} \times \{\{3\}, \{4\}\}$ has weight $4 \cdot (3/4)/12 = 1/4$ and no intersecting pair. For general $n$, the same rectangle with halves of $[n]$ has weight $3n/(16(n-1))$, which tends to $3/16$. So $\beta$ must be a constant and the bound gives only $O(1)$. This is equality in disguise, and its randomized cost is indeed $O(1)$.

**Gap Hamming distance (Sherstov 2012).** A corruption bound with a concentration inequality of Talagrand gives a short proof of the $\Omega(n)$ bound for the [gap Hamming distance problem](/gap-hamming-distance/), first proved by Chakrabarti and Regev.

## Variations

- **The rectangle bound.** Ask for $\mu(R \cap f^{-1}(0)) \ge \alpha\mu(R)$ only for rectangles with $\mu(R) \ge \beta$. This is the same bound up to constants.
- **Nondeterministic and fooling sets.** With $\alpha = 1$ and $\varepsilon = 0$, the hypothesis says that every 1-rectangle has weight at most $\beta$. Then the bound counts rectangles in a cover of the 1-inputs, which is the weighted form of the [fooling set method](/fooling-set-method/).
- **Strong direct product.** Beame, Pitassi, Segerlind and Wigderson (2006) proved that the corruption bound obeys a strong direct product theorem: solving $k$ copies with success probability $2^{-\Omega(k)}$ needs $\Omega(k)$ times the bound. Compare [direct sum for communication](/direct-sum-communication/).
- **Information.** The [information complexity](/information-complexity/) method of Bar-Yossef, Jayram, Kumar and Sivakumar gives a second proof of the disjointness bound that also yields the exact constant.

## Pitfalls

- The hypothesis is for every rectangle, not only for the leaves of one protocol. A bound for rectangles of one shape proves nothing.
- The bound needs $\varepsilon < \alpha\,\mu(f^{-1}(1))$. Prove it for a small constant error, then amplify.
- The value matters. Corruption of the 1-rectangles by 0-inputs bounds the number of 1-leaves. For disjointness the 0-inputs (intersecting pairs) have large monochromatic rectangles, so the argument must count the 1-leaves.
- For disjointness, no product distribution gives more than $O(\sqrt{n} \log n)$. A linear bound needs a correlated distribution.
- The bound is for public-coin protocols through Yao's principle. Private-coin protocols are at least as costly, so the bound transfers.

## Exercises

1. Show that if every 1-rectangle $R$ has $\mu(R) \le \beta$, then $N^1(f) \ge \log_2(\mu(f^{-1}(1))/\beta)$.
2. Prove the version of the theorem with $\varepsilon = 0$ and explain why it then becomes a bound on deterministic covers.
3. For two independent uniform subsets of $[n]$ of size $\sqrt{n}$, compute the limit of the probability that they are disjoint as $n$ grows.
4. In the example "Why small sets fail", compute the weight of the rectangle built from the two halves of $[n]$ for even $n$, and check the limit $3/16$.
5. Put weight $1/2$ uniformly on the diagonal of $\mathrm{EQ}_n$ and $1/2$ uniformly off it. Use the rectangles $A \times A$ with $|A| = c \cdot 2^n$ to show that, for any fixed $\alpha$, the constant $\beta$ in the corruption lemma for the value 1 cannot go to 0. So the bound gives only $O(1)$, as it must.

## References
