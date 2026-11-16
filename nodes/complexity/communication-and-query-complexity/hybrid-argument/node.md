---
tag: DZRE22
kind: technique
slug: hybrid-argument
name: Hybrid argument
aliases:
- hybrid method
area: complexity/communication-and-query-complexity
level: advanced
summary: "A proof technique: to bound the difference between two distributions or computations, put a chain of hybrids between them and bound the difference at each step of the chain."
prereqs: [computational-indistinguishability, total-variation-distance]
see_also: [pseudorandom-generator, pseudorandom-function, grover-optimality, semantic-security, ind-cpa-security, nisan-prg, trace-distance, quantum-query-model]
sources:
  - paper: doi:10.1016/0022-0000(84)90070-9
    title: "Shafi Goldwasser and Silvio Micali, Probabilistic encryption, Journal of Computer and System Sciences 28(2), 1984, pages 270-299"
    locator: the proof that semantic security for one message gives security for many messages, by a chain of hybrid message sequences
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 9, Cryptography (Yao's theorem that unpredictability gives pseudorandomness, proved with hybrids)
  - paper: doi:10.1137/S0097539796300933
    title: "Charles H. Bennett, Ethan Bernstein, Gilles Brassard and Umesh Vazirani, Strengths and weaknesses of quantum computing, SIAM Journal on Computing 26(5), 1997, pages 1510-1523"
    locator: the hybrid argument for quantum search (the change of the final state is at most the sum of the query magnitudes)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Chapter 6, Section 6.6 (the optimality proof of search, which sums the errors over the queries)
---

The hybrid argument is a proof technique that bounds the difference between two objects by a chain of intermediate objects, the hybrids. The two objects can be two probability distributions, two quantum states, or the runs of one algorithm with two different oracles. Each neighbour pair in the chain differs in one small part, so the difference of each pair is easy to bound. The triangle inequality then bounds the difference of the end points by the sum of the step differences. In cryptography the argument proves that pseudorandomness follows from unpredictability, and in the [quantum query model](/quantum-query-model/) it gave the first proof that [Grover search](/grover-search/) is optimal. This page gives the general method; [optimality of Grover search](/grover-optimality/) gives the full quantum proof for search.

## In plain words

You want to show that two things look almost the same. Comparing them at once is hard, because they differ in many places. So build a row of in-between things. The first is the first thing, the last is the second thing, and each one differs from the next in only one place. A change in one place is easy to study. If each single change is small, then the total change from the first to the last is at most the sum of the small changes. Read the other way, if someone can tell the first from the last, then at some step in the row they can tell two neighbours apart. That gives a way to break the one small change, which you know is not possible. So the large difference is not possible either.

## When it applies

Use the hybrid argument when:

- the two end points $D_0$ and $D_1$ can be joined by a chain $H_0 = D_0, H_1, \ldots, H_m = D_1$ in which $H_{j-1}$ and $H_j$ differ in one component, such as one block of output, one message, or one query;
- the quantity that you want to bound obeys the triangle inequality, or is a difference of probabilities that telescopes; and
- for a computational statement, an algorithm that tells $H_{j-1}$ from $H_j$ can be turned into an algorithm that breaks a one-step assumption. This needs the reduction to produce the other components of the hybrid by itself, which usually means that the distributions involved can be sampled efficiently.

The chain length $m$ must be small compared with $1/\varepsilon$, where $\varepsilon$ is the gap that you want to show. In cryptography $m$ must be polynomial in the security parameter.

## The template

Let $A$ be a test, that is, any algorithm with output 0 or 1. For a distribution $H$, write $p(H) = \Pr[A(H) = 1]$. The **advantage** of $A$ is $\varepsilon = |p(D_1) - p(D_0)|$.

```pseudo id=template
HYBRID(D0, D1, A)               ▷ A tells D0 from D1 with advantage ε
L1  H_0 ← D0; H_m ← D1             ▷ hole: the two end points
L2  H_1, ..., H_{m-1} ← CHAIN()    ▷ hole: H_{j-1} and H_j differ in one component
L3  ε ≤ Σ_{j=1..m} |p(H_j) - p(H_{j-1})|   ▷ telescoping sum and triangle inequality
L4  pick j with |p(H_j) - p(H_{j-1})| ≥ ε/m, or pick j at random
L5  B ← REDUCTION(A, j)             ▷ hole: B embeds its own challenge as component j
L6  return B breaks the one-step assumption with advantage ≥ ε/m
```

Line L3 holds because $p(H_m) - p(H_0) = \sum_{j=1}^{m} (p(H_j) - p(H_{j-1}))$. Line L4 has two forms. A **non-uniform** reduction fixes the best $j$, and so needs to know it. A **uniform** reduction picks $j$ at random from $\{1, \ldots, m\}$. Without absolute values the sum telescopes, so the expected step gap is exactly $(p(H_m) - p(H_0))/m$, and the random choice gives advantage $\varepsilon/m$ on average with no knowledge of $j$.

For a distance that is a norm, such as [total variation distance](/total-variation-distance/), the Euclidean distance of state vectors, or the [trace distance](/trace-distance/) of quantum states, line L3 is the triangle inequality $d(H_0, H_m) \le \sum_j d(H_{j-1}, H_j)$ and no reduction is needed.

## Classic examples

**Many samples.** Let $P$ and $Q$ be distributions with total variation distance $\delta$. Then $k$ independent samples have distance at most $k\delta$: the hybrid $H_j$ takes its first $j$ samples from $Q$ and the rest from $P$, and $H_{j-1}$ and $H_j$ differ in one independent sample. The computational form is the same. If $D_0$ and $D_1$ are [computationally indistinguishable](/computational-indistinguishability/) and can be sampled in polynomial time, then so are $k$ independent copies for each polynomial $k$, with a loss of a factor of $k$ in the advantage. The reduction samples the other $k - 1$ components itself. Goldwasser and Micali used this chain over messages to show that [semantic security](/semantic-security/) for one message gives security for many messages; see [IND-CPA security](/ind-cpa-security/).

**Next-bit unpredictability gives pseudorandomness.** Let $G$ map seeds of length $\ell$ to strings of length $m$. Yao's theorem says that if no efficient algorithm can predict bit $j$ of $G(s)$ from bits $1$ to $j - 1$ with probability noticeably above $1/2$, then $G$ is a [pseudorandom generator](/pseudorandom-generator/). The hybrid $H_j$ takes the first $j$ bits of $G(s)$ and fills the rest with uniform bits, so $H_0$ is uniform and $H_m = G(s)$. From a test $A$, the predictor for bit $j$ picks uniform bits $r_j, \ldots, r_m$, runs $A$ on $G(s)_{1..j-1} r_j \cdots r_m$, and outputs $r_j$ if $A$ says 1 and $1 - r_j$ if not. Its success probability is exactly $1/2 + p(H_j) - p(H_{j-1})$.

A small exact case. Let $G(s_1, s_2) = (s_1, s_2, s_1 \wedge s_2, s_1 \vee s_2)$, and let $A(z) = 1$ exactly when $z_3 \le \min(z_1, z_2)$ and $z_4 \ge \max(z_1, z_2)$. A computation over all seeds and fill bits gives:

| $j$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $p(H_j)$ | 3/8 | 3/8 | 3/8 | 5/8 | 1 |
| step gap $p(H_j) - p(H_{j-1})$ | | 0 | 0 | 1/4 | 3/8 |
| success of the predictor for bit $j$ | | 1/2 | 1/2 | 3/4 | 7/8 |

The total advantage is $5/8$, and it is the sum of the step gaps. The first two bits of $G(s)$ are uniform, so the predictors for them are no better than a coin. The predictors for bits 3 and 4 succeed with exactly $1/2$ plus the step gap.

**Longer output from one extra bit.** Suppose $G_1$ stretches $\ell$ bits to $\ell + 1$ bits. Apply $G_1$ again to the last $\ell$ output bits, output the first bit each time, and repeat $m$ times. The hybrid $H_j$ replaces the first $j$ rounds by uniform bits. Neighbours differ in one call of $G_1$ on a seed that is uniform, so an advantage $\varepsilon$ against the $m$-bit output gives advantage $\varepsilon/m$ against $G_1$. The same chain, over the levels of a tree, proves the security of the GGM [pseudorandom function](/pseudorandom-function/).

**Quantum search.** Let an algorithm make $T$ queries, with states $|\phi_t\rangle$ when the oracle is the identity (no marked item). Let $|\psi_t^{(i)}\rangle$ be its states when item $i$ is marked. The hybrid $H_t$ uses the oracle of item $i$ for the first $t$ queries and the identity for the rest. Neighbours differ in one query, which acts on $|\phi_t\rangle$, so

$$\big\| |\psi_T^{(i)}\rangle - |\phi_T\rangle \big\| \le \sum_{t=0}^{T-1} 2 \, \| \Pi_i |\phi_t\rangle \| ,$$

where $\Pi_i$ projects on the queries to index $i$. Sum over $i$ and use $\sum_i \|\Pi_i |\phi_t\rangle\|^2 \le 1$ with the Cauchy-Schwarz inequality: the right side, summed over all $N$ items, is at most $2T\sqrt N$. To find $i$ with constant probability, the left side must be at least a constant for most $i$, so the sum over $i$ is $\Omega(N)$ and $T = \Omega(\sqrt N)$. Bennett, Bernstein, Brassard and Vazirani gave this proof; the page on [optimality of Grover search](/grover-optimality/) has all the steps.

## Variations

- **Statistical hybrids.** With total variation distance or trace distance, the argument is only the triangle inequality, and it holds against all tests, not only efficient ones.
- **Random index.** In uniform reductions, $j$ is chosen at random, as in line L4. This is the usual form in proofs about [pseudorandom generators](/pseudorandom-generator/) and in the analysis of the [Nisan generator](/nisan-prg/) and the [Nisan-Wigderson generator](/nisan-wigderson-generator/).
- **Quantum hybrids.** For quantum query algorithms, the distance of state vectors replaces the probability, and each hybrid changes one oracle call. The bound counts the query magnitude, the weight that the state puts on the changed part of the oracle.
## Pitfalls

- **Too many hybrids.** The loss is a factor of $m$. With $m$ exponential in the security parameter, an advantage of $\varepsilon$ gives only $\varepsilon/m$ for one step, and this proves nothing. Build a chain of polynomial length.
- **The reduction must make the hybrid.** To turn a test for $H_{j-1}$ and $H_j$ into an attack, the reduction must produce all other components. If $D_0$ or $D_1$ cannot be sampled efficiently, the computational argument fails. The statistical form has no such need.
- **Uniform and non-uniform.** Fixing the best $j$ is a non-uniform step. For a uniform reduction, choose $j$ at random and use the telescoping sum without absolute values.
- **Absolute values in the average.** With absolute values, the step gaps can sum to more than $\varepsilon$, and the average of the absolute gaps is not the advantage of the random-$j$ reduction. Use signed gaps for the average.
- **Adaptive queries.** In the quantum query bound, the query magnitudes are for the run with the identity oracle. The argument works because every hybrid agrees with that run up to the changed query.

## Exercises

1. Show that $k$ samples of a coin with bias $1/2 + \delta$ have total variation distance at most $k\delta$ from $k$ fair coins.
2. Prove that the predictor in the second example succeeds with probability exactly $1/2 + p(H_j) - p(H_{j-1})$.
3. In the small exact case, change the test to $A(z) = 1$ exactly when $z_3 = z_1 \wedge z_2$. Compute all $p(H_j)$ and the step gaps.
4. A generator stretches $\ell$ bits to $2\ell$ bits. Use hybrids to build from it a generator that stretches $\ell$ bits to $\ell^2$ bits, and state the loss in advantage.
5. Explain why the hybrid argument cannot show that an exponential number of samples of a pseudorandom distribution is pseudorandom.
6. In the quantum search bound, find where the proof uses that the identity oracle and the oracle of item $i$ differ only on index $i$.

## References
