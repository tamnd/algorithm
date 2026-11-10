---
tag: RNZSW7
kind: theorem
slug: nemhauser-wolsey-fisher-theorem
name: Nemhauser-Wolsey-Fisher theorem
aliases:
- 1-1/e greedy guarantee
- greedy bound for submodular maximization
area: approximation/covering-and-packing
level: advanced
summary: For a monotone submodular function with f(∅) = 0, the greedy choice of k elements reaches at least 1 − (1 − 1/k)^k > 1 − 1/e of the best value of k elements.
prereqs: [submodular-function, greedy-algorithm, max-coverage]
see_also: [greedy-max-coverage, max-coverage, submodular-function, greedy-influence-maximization, matroid, uniform-matroid, max-coverage-inapproximability, facility-location-problem]
sources:
  - paper: doi:10.1007/BF01588971
    title: George L. Nemhauser, Laurence A. Wolsey and Marshall L. Fisher, An analysis of approximations for maximizing submodular set functions I, Mathematical Programming 14(1), 1978
    locator: pages 265 to 294 (the greedy bound under a cardinality constraint)
  - title: Marshall L. Fisher, George L. Nemhauser and Laurence A. Wolsey, An analysis of approximations for maximizing submodular set functions II, Mathematical Programming Study 8, 1978
    locator: pages 73 to 87 (the bound 1/2 for a matroid constraint)
  - title: George L. Nemhauser and Laurence A. Wolsey, Best algorithms for approximating the maximum of a submodular set function, Mathematics of Operations Research 3(3), 1978
    locator: pages 177 to 188 (no algorithm with polynomially many value queries beats 1 − 1/e)
  - paper: doi:10.1145/285055.285059
    title: Uriel Feige, A threshold of ln n for approximating set cover, Journal of the ACM 45(4), 1998
    locator: pages 634 to 652 (1 − 1/e + ε is NP-hard for maximum coverage)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 2, Section 2.5 (the same argument for maximizing float in bank accounts)
---

The Nemhauser-Wolsey-Fisher theorem says that the greedy algorithm is a $(1 - 1/e)$-approximation for maximizing a monotone [submodular function](/submodular-function/) under a cardinality constraint. Greedy adds, $k$ times, the element with the largest gain, and the result has at least $1 - (1 - 1/k)^k$ of the best value of $k$ elements. [Maximum coverage](/max-coverage/), facility location by coverage, sensor placement and [influence maximization](/greedy-influence-maximization/) are special cases. The bound is tight for greedy, it is the best possible for any algorithm that only queries the function values, and for maximum coverage it is the best possible in polynomial time unless P = NP.

## Statement

Let $V$ be a finite ground set and $F : 2^V \to \mathbb{R}$ a set function with these properties:

- *normalized:* $F(\emptyset) = 0$;
- *monotone:* $F(A) \le F(B)$ when $A \subseteq B \subseteq V$;
- *submodular:* $F(A \cup \{v\}) - F(A) \ge F(B \cup \{v\}) - F(B)$ when $A \subseteq B \subseteq V$ and $v \in V \setminus B$.

Write $\Delta(v \mid A) = F(A \cup \{v\}) - F(A)$ for the gain of $v$ at $A$. Fix an integer $k$ with $1 \le k \le |V|$, and let OPT $= \max \{ F(S) : S \subseteq V, |S| \le k \}$. The greedy algorithm starts with $G_0 = \emptyset$ and, for $i = 0, 1, \ldots, k - 1$, sets $G_{i+1} = G_i \cup \{v_{i+1}\}$, where $v_{i+1} \in V \setminus G_i$ has the largest gain $\Delta(v \mid G_i)$, with ties broken in any way.

**Theorem (Nemhauser, Wolsey and Fisher 1978).** For each $\ell = 0, 1, \ldots, k$,

$$F(G_\ell) \ge \left(1 - \left(1 - \frac{1}{k}\right)^\ell\right) \text{OPT}.$$

In particular, ALG $= F(G_k) \ge (1 - (1 - 1/k)^k)\,\text{OPT} \ge (1 - 1/e)\,\text{OPT}$, in the worst case. This is a maximization bound with the convention ALG $\ge \alpha \cdot$ OPT.

If $F(\emptyset) \ne 0$, apply the theorem to $F - F(\emptyset)$: then $F(G_k) - F(\emptyset) \ge (1 - 1/e)(\text{OPT} - F(\emptyset))$.

## In plain words

You choose a fixed number of things, and the value of a choice has two rules: adding a thing never lowers the value, and a thing adds less when you already have more. Coverage is the standard example: a new group adds fewer new items when you already cover many items.

Pick, each time, the thing that adds the most. While you are below the best value, the things of the best choice, added to what you have, would reach the best value. By the second rule, their single gains add up to at least the gap, so one of them closes at least an equal share of it. Your pick closes at least as much. So the gap shrinks by a fixed factor at each step, and at the end it is at most about 37 percent of the best value.

## Proof

**Lemma 1 (gains of a set).** For all $A, O \subseteq V$,

$$F(O) \le F(A) + \sum_{o \in O \setminus A} \Delta(o \mid A).$$

*Proof.* List $O \setminus A$ as $o_1, \ldots, o_r$, and let $A_t = A \cup \{o_1, \ldots, o_t\}$, so $A_0 = A$ and $A_r = A \cup O$. By monotonicity, $F(O) \le F(A \cup O)$. By telescoping,

$$F(A \cup O) = F(A) + \sum_{t=1}^{r} \left(F(A_t) - F(A_{t-1})\right) = F(A) + \sum_{t=1}^{r} \Delta(o_t \mid A_{t-1}).$$

Here $A \subseteq A_{t-1}$ and $o_t \notin A_{t-1}$, so submodularity gives $\Delta(o_t \mid A_{t-1}) \le \Delta(o_t \mid A)$. Combine the three facts. $\square$

**Lemma 2 (the step inequality).** Let $O$ be a set with $|O| \le k$ and $F(O) = \text{OPT}$. For each $i = 0, 1, \ldots, k - 1$,

$$\text{OPT} - F(G_{i+1}) \le \left(1 - \frac{1}{k}\right)\left(\text{OPT} - F(G_i)\right).$$

*Proof.* Apply Lemma 1 with $A = G_i$. The set $O \setminus G_i$ has at most $k$ elements, and each $o$ in it is a candidate of greedy at step $i + 1$, so $\Delta(o \mid G_i) \le \Delta(v_{i+1} \mid G_i) = F(G_{i+1}) - F(G_i)$. Gains are non-negative by monotonicity. So

$$\text{OPT} \le F(G_i) + k \left(F(G_{i+1}) - F(G_i)\right).$$

If $O \setminus G_i$ is empty, Lemma 1 gives $\text{OPT} \le F(G_i)$, and the same inequality holds because the gain is non-negative. Rearrange: $F(G_{i+1}) - F(G_i) \ge (\text{OPT} - F(G_i))/k$, and subtract both sides from $\text{OPT} - F(G_i)$. $\square$

*Proof of the theorem.* Induction on $\ell$. For $\ell = 0$, $F(G_0) = F(\emptyset) = 0$ and the bound is 0. If $\text{OPT} - F(G_\ell) \le (1 - 1/k)^\ell\,\text{OPT}$, Lemma 2 gives $\text{OPT} - F(G_{\ell+1}) \le (1 - 1/k)^{\ell+1}\,\text{OPT}$. This is the claim. For the last step, $1 - x \le e^{-x}$ for each real $x$, so $(1 - 1/k)^k \le e^{-1}$. $\blacksquare$

**A check on numbers.** On the instance of the [maximum coverage](/max-coverage/) page with $k = 3$ and OPT $= 11$, greedy reaches 5, 8 and 10 after one, two and three steps. The gaps are $11, 6, 3, 1$, and each is at most $2/3$ of the gap before it: $6 \le 22/3$, $3 \le 4$ and $1 \le 2$. The theorem promises $11 \cdot 19/27 = 209/27 \approx 7.74$ after three steps.

## Consequences

- **Maximum coverage.** The number of covered elements is monotone and submodular, so the [greedy maximum coverage](/greedy-max-coverage/) algorithm has ratio $1 - (1 - 1/k)^k$.
- **More steps, a better ratio.** If greedy runs for $\ell$ steps but is compared with the best $k$ elements, then $F(G_\ell) \ge (1 - e^{-\ell/k})\,\text{OPT}$. With $\ell = k \lceil \ln(1/\varepsilon) \rceil$ steps it reaches $(1 - \varepsilon)\,\text{OPT}$, a bicriteria guarantee.
- **Prefixes.** Each prefix $G_\ell$ is a $(1 - (1 - 1/\ell)^\ell)$-approximation for the budget $\ell$, so one run serves all budgets.
- **Submodular set cover.** Running greedy until $F$ reaches $F(V)$, with unit costs, uses at most $H_D \cdot$ OPT elements for integer-valued $F$, where $D = \max_v F(\{v\})$ and OPT is the size of a smallest $S$ with $F(S) = F(V)$ (Wolsey 1982). The [greedy set cover](/greedy-set-cover/) bound $H_d$ is the coverage case.
- **Influence maximization.** The expected spread under the independent cascade and linear threshold models is monotone submodular (Kempe, Kleinberg and Tardos 2003), so greedy seed selection is a $(1 - 1/e - \varepsilon)$-approximation when the spread is estimated by sampling; see [greedy influence maximization](/greedy-influence-maximization/).
- **Lazy evaluation.** Submodularity makes old gains upper bounds on new gains. This justifies lazy greedy, which recomputes only the top of a heap and gives the same output.

## Tightness

- **For greedy.** The bound $1 - (1 - 1/k)^k$ is exact for each $k$. The instance with $k$ rows of $k^k$ elements and greedy blocks of $k^{k-i}(k-1)^{i-1}$ columns, on the [greedy maximum coverage](/greedy-max-coverage/) page, makes greedy reach exactly $1 - (1 - 1/k)^k$ of OPT, with ties broken against the rows.
- **For value-query algorithms.** Nemhauser and Wolsey (1978) proved that any algorithm that sees $F$ only through value queries needs exponentially many queries to beat $1 - 1/e$ for large $k$. This holds without any complexity assumption.
- **For explicit coverage.** For maximum coverage given as an explicit list of sets, a $(1 - 1/e + \varepsilon)$-approximation is NP-hard for each $\varepsilon > 0$ (Feige 1998); see [max coverage inapproximability](/max-coverage-inapproximability/).
- **The hypotheses are needed.** Without monotonicity, the gains can be negative and Lemma 1 fails, and greedy has no constant ratio; non-monotone submodular maximization needs other algorithms. Without submodularity, the step inequality fails; for example, if $F(S) = 1$ only when $S$ holds both elements of a pair, each single gain is 0 and greedy can pick the wrong elements.
- **Other constraints.** For a [matroid](/matroid/) constraint in place of a cardinality constraint, greedy has the weaker ratio $1/2$ (Fisher, Nemhauser and Wolsey 1978), which is tight for greedy. A cardinality constraint is a [uniform matroid](/uniform-matroid/), where the better bound holds.

## History

Cornuéjols, Fisher and Nemhauser (1977) proved the bound for a location problem with a coverage structure. Nemhauser, Wolsey and Fisher (1978) proved it for each monotone submodular function under a cardinality constraint, and in a second paper Fisher, Nemhauser and Wolsey (1978) gave the bound $1/2$ for matroids. Nemhauser and Wolsey (1978) showed that $1 - 1/e$ is the best possible with polynomially many value queries. Feige (1998) showed the same limit for maximum coverage under P $\ne$ NP. Călinescu, Chekuri, Pál and Vondrák (2011) reached $1 - 1/e$ for a matroid constraint with the continuous greedy algorithm. Kempe, Kleinberg and Tardos (2003) brought the theorem to influence maximization, which made it widely used in data mining and machine learning.

## References
