---
tag: 8532GG
kind: algorithm
slug: system-z
name: System Z
aliases:
- Pearl's System Z
- Z-ranking
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: Ranks defaults by tolerance into layers and ranks worlds by the highest layer they violate, computing rational closure.
model: word-ram
complexity:
  vars: {r: the number of conditionals, s: the total size of the conditionals, P: "the cost of one satisfiability test on a formula of size O(s), exponential in the worst case"}
  time: {worst: O(r^2 · P)}
  space: {extra: O(s)}
properties: {deterministic: true}
history:
  year: 1990
  people: [Judea Pearl, Moisés Goldszmidt]
  note: Pearl introduced System Z at TARK 1990. In the same year Goldszmidt and Pearl showed that it agrees with the rational closure of Lehmann and Magidor.
prereqs: [rational-closure, ordinal-conditional-functions, sat]
see_also: [system-p, nonmonotonic-reasoning, default-logic, tseitin-transformation, dpll, horn-sat, belief-revision]
sources:
  - paper: "Judea Pearl, System Z: a natural ordering of defaults with tractable applications to nonmonotonic reasoning, in Rohit Parikh (ed.), Proceedings of the Third Conference on Theoretical Aspects of Reasoning about Knowledge (TARK 1990), Morgan Kaufmann, 121 to 135 (1990)"
    locator: tolerance, the partition of the defaults, the ranking of worlds and the entailment relation
  - paper: "Moisés Goldszmidt and Judea Pearl, On the relation between rational closure and System Z, Proceedings of the Third International Workshop on Nonmonotonic Reasoning, South Lake Tahoe, 130 to 140 (1990)"
    locator: the proof that System Z entailment and rational closure coincide
  - paper: doi:10.1016/0004-3702(92)90041-U
    title: Daniel Lehmann and Menachem Magidor, What does a conditional knowledge base entail?, Artificial Intelligence 55(1), 1 to 60 (1992)
    locator: Section 2.6 (exceptional formulas), Lemma 33 and Corollary 6 (exceptionality by the material counterpart), Section 5.8 (the decision procedure for rational closure)
  - paper: doi:10.1016/0004-3702(95)00090-9
    title: Moisés Goldszmidt and Judea Pearl, Qualitative probabilities for default reasoning, belief revision, and causal modeling, Artificial Intelligence 84(1-2), 57 to 112 (1996)
    locator: ranking functions for default reasoning, and System Z+ with strengths on the defaults
  - paper: doi:10.1016/S0004-3702(00)00073-4
    title: Thomas Eiter and Thomas Lukasiewicz, Default reasoning from conditional knowledge bases, complexity and tractable cases, Artificial Intelligence 124(2), 169 to 241 (2000)
    locator: the complexity of entailment in System Z and related semantics, and the tractable cases
  - paper: doi:10.1007/BF01535841
    title: Daniel Lehmann, Another perspective on default reasoning, Annals of Mathematics and Artificial Intelligence 15(1), 61 to 82 (1995)
    locator: the lexicographic closure
  - paper: doi:10.1109/34.204904
    title: Moisés Goldszmidt, Paul Morris and Judea Pearl, A maximum entropy approach to nonmonotonic reasoning, IEEE Transactions on Pattern Analysis and Machine Intelligence 15(3), 220 to 232 (1993)
    locator: the maximum entropy ranking of defaults
---

System Z reasons with a finite set $R$ of propositional conditionals $\alpha \to \beta$, read "if $\alpha$ then normally $\beta$". It splits $R$ into layers by *tolerance*: the first layer holds the rules that can be satisfied without breaking any rule, the next layer holds the rules that can be satisfied without breaking the rules that remain, and so on. A world then gets the rank $1 +$ the highest layer of a rule that it breaks, or $0$ if it breaks none. A query $\alpha \mathrel{|\!\sim} \beta$ is accepted when the best worlds of $\alpha$ satisfy $\beta$. This ranking is the least ranking that respects every rule, and the relation that it defines is exactly the [rational closure](/rational-closure/) of Lehmann and Magidor. Every step is a satisfiability test, so the whole method is a polynomial number of [SAT](/sat/) calls.

## In plain words

You have rules of thumb such as "birds fly", "penguins are birds" and "penguins do not fly". Some rules can be followed in a situation that breaks no rule at all: a flying bird that is no penguin follows "birds fly" and breaks nothing. Those rules are the most general, and they go in the bottom layer. Other rules cannot be followed without breaking a general rule: any penguin breaks "birds fly". Those rules are more specific, and they go in a higher layer. A situation is as abnormal as the most specific rule that it breaks. To answer "do penguins fly?", look at the least abnormal penguins and see whether they fly. They do not, so the answer is no, and the specific rule wins over the general one.

## The problem

**Logic and semantics.** The language is propositional logic over a finite set of atoms. A conditional is a pair $\alpha \to \beta$ of formulas. A *ranking* $\kappa$ maps each world to a natural number or $\infty$, with some world of rank $0$, and gives a formula $\varphi$ the rank $\kappa(\varphi) = \min\{\kappa(w) : w \models \varphi\}$, with $\min \emptyset = \infty$. These are the [ordinal conditional functions](/ordinal-conditional-functions/) of Spohn. A ranking *admits* $\alpha \to \beta$ if $\kappa(\alpha \wedge \beta) < \kappa(\alpha \wedge \neg\beta)$: the best $\alpha$ worlds satisfy $\beta$. $R$ is *consistent* if some ranking admits all its rules.

**Task.** Given $R$ and a query $\alpha \mathrel{|\!\sim} \beta$, decide whether the query holds in System Z, that is, in the Z-ranking $\kappa_Z$ defined below. By the theorem of Goldszmidt and Pearl (1990), this is the same as deciding whether the query is in the rational closure of $R$. The input is propositional. With $R = \emptyset$ the query holds exactly when $\alpha \models \beta$, so the problem is [co-NP](/co-np/)-hard. The algorithm below makes polynomially many calls of a SAT oracle, so the problem is in $\mathrm{P}^{\mathrm{NP}}$, a class at the second level of the [polynomial hierarchy](/polynomial-hierarchy/). Eiter and Lukasiewicz (2000) studied the exact complexity of this problem and of related semantics, and the cases that are tractable. When the rules and the query are Horn, each test is a [Horn-SAT](/horn-sat/) test, and the whole decision takes polynomial time (Lehmann and Magidor 1992, Section 5.8).

## The algorithm

A world *verifies* $\alpha \to \beta$ if it satisfies $\alpha \wedge \beta$ and *falsifies* it if it satisfies $\alpha \wedge \neg\beta$. For a set $S$ of rules, $M(S)$ is the conjunction of the material implications $\alpha \supset \beta$ over $S$. A rule $r$ is *tolerated* by $S$ if some world verifies $r$ and falsifies nothing in $S$, that is, if $\alpha_r \wedge \beta_r \wedge M(S)$ is satisfiable.

```pseudo id=main
PARTITION(R)                       ▷ returns the layers R0, R1, ... and the rules that have no rank
L1  rest ← R; layers ← []
L2  while rest is not empty do
L3      layer ← {α → β ∈ rest : α ∧ β ∧ M(rest) is satisfiable}     ▷ the rules that rest tolerates
L4      if layer is empty then return (layers, rest)                  ▷ R is not consistent
L5      append layer to layers
L6      rest ← rest ∖ layer
L7  return (layers, ∅)

KAPPA(φ)                           ▷ k layers; R≥i is the union of layers i to k - 1 and rest
L8  if φ ∧ M(R≥k) is unsatisfiable then return ∞
L9  lo ← 0; hi ← k
L10 while lo < hi do
L11     mid ← ⌊(lo + hi) / 2⌋
L12     if φ ∧ M(R≥mid) is satisfiable then hi ← mid else lo ← mid + 1
L13 return lo

ENTAILS(R, α, β)
L14 (layers, rest) ← PARTITION(R)
L15 a ← KAPPA(α ∧ β); b ← KAPPA(α ∧ ¬β)
L16 return a < b or b = ∞
```

The Z-rank of a rule in layer $i$ is $Z(r) = i$. The Z-ranking of a world is $\kappa_Z(w) = 0$ if $w$ falsifies no rule, $\infty$ if it falsifies a rule without rank, and otherwise $1 + \max\{Z(r) : w \text{ falsifies } r\}$. KAPPA never lists the worlds. A world has rank at most $i$ exactly when it satisfies $M(R_{\ge i})$, so $\kappa_Z(\varphi) \le i$ exactly when $\varphi \wedge M(R_{\ge i})$ is satisfiable. This test is monotone in $i$, so a [binary search](/binary-search/) finds the rank. The implementation decides satisfiability with the [Tseitin transformation](/tseitin-transformation/) and a small [DPLL](/dpll/) solver.

## Example

Take the atoms $b$ (bird), $f$ (flies) and $p$ (penguin), and the rules $r_1 = b \to f$, $r_2 = p \to b$ and $r_3 = p \to \neg f$.

- Round 0, rest $= \{r_1, r_2, r_3\}$. The world $b, f, \neg p$ verifies $r_1$ and falsifies nothing, so $r_1$ is tolerated. A world that verifies $r_2$ or $r_3$ is a penguin. If it flies it falsifies $r_3$, and if it is a bird that does not fly it falsifies $r_1$. So $R_0 = \{r_1\}$.
- Round 1, rest $= \{r_2, r_3\}$. The world $b, \neg f, p$ verifies both and falsifies neither. So $R_1 = \{r_2, r_3\}$, and the set is consistent.

| world $(b, f, p)$ | falsifies | $\kappa_Z$ |
|---|---|---|
| any world with $\neg p$ and not $b \wedge \neg f$ | nothing | 0 |
| $b, \neg f, \neg p$ | $r_1$ | 1 |
| $b, \neg f, p$ | $r_1$ | 1 |
| $b, f, p$ | $r_3$ | 2 |
| $\neg b, \neg f, p$ | $r_2$ | 2 |
| $\neg b, f, p$ | $r_2, r_3$ | 2 |

Then $\kappa_Z(p \wedge \neg f) = 1 < 2 = \kappa_Z(p \wedge f)$, so penguins normally do not fly, and $\kappa_Z(p \wedge b) = 1 < 2 = \kappa_Z(p \wedge \neg b)$, so penguins are normally birds. Also $\kappa_Z(b \wedge \neg p) = 0 < 1 = \kappa_Z(b \wedge p)$: birds are normally not penguins.

Add $r_4 = b \to w$ (birds have wings). Now $R_0 = \{r_1, r_4\}$. The best penguins break $r_1$, which has rank $0$, whether or not they also break $r_4$. So $\kappa_Z(p \wedge w) = \kappa_Z(p \wedge \neg w) = 1$, and System Z does not conclude that penguins have wings. This is the *drowning problem*: one broken rule of a layer hides all the other rules of that layer.

For the Nixon diamond, $q \to p$ and $r \to \neg p$ are tolerated at once and form one layer. The worlds with $q \wedge r$ break one of the two rules, both with rank $0$, so $\kappa_Z(q \wedge r \wedge p) = \kappa_Z(q \wedge r \wedge \neg p) = 1$, and neither $p$ nor $\neg p$ follows from $q \wedge r$.

## Correctness

The [correctness proof](proofs/correctness.md) has the details. It shows four things. First, a world has rank at most $i$ exactly when it satisfies $M(R_{\ge i})$, which justifies lines L8 to L13. Second, $\kappa_Z$ admits every rule: a rule of layer $i$ is verified by a world of rank at most $i$ and falsified only by worlds of rank at least $i + 1$. Third, $\kappa_Z$ is the least admissible ranking: for any admissible $\kappa'$, an induction on $i$ shows that every world verifying a rule of $R_{\ge i}$ has $\kappa'$ at least $i$, because such a rule is not tolerated by $R_{\ge i - 1}$ and so each such world breaks a rule of that set. The same induction shows that no ranking admits a set with rules left over at line L4. Fourth, a rule is tolerated by a set that contains it exactly when its antecedent is not *exceptional* in the sense of Lehmann and Magidor. So the layers are their sequence $C_0, C_1, \ldots$ of exceptional subsets, and line L16 gives the same answer as their decision procedure for rational closure.

## Complexity

Let $r = |R|$ and let $s$ be the total size of the rules. PARTITION runs at most $r$ rounds, because each round removes at least one rule, and round $i$ tests each remaining rule once. So it makes at most $r(r + 1)/2$ satisfiability tests, each on a formula of size $O(s)$. After the partition, one query needs two calls of KAPPA, each with $O(\log r)$ tests. The total time is $O(r^2 \cdot P)$, where $P$ is the cost of one test. The space outside the solver is $O(s)$ for the formula and the layers. In the worst case $P$ is exponential, because SAT is NP-complete, but the number of oracle calls is polynomial. For Horn rules each test runs in linear time, so the whole method is polynomial.

## Properties

- **Least admissible ranking.** $\kappa_Z(w) \le \kappa'(w)$ for every world $w$ and every ranking $\kappa'$ that admits all rules. The rules are believed as weakly as possible, which is Pearl's idea of default reasoning with minimal surprise.
- **Rational closure.** The relation $\alpha \mathrel{|\!\sim}_Z \beta$ is rational closure, so it satisfies the rules of [System P](/system-p/) and Rational Monotonicity.
- **Consistency test for free.** The set has an admissible ranking exactly when PARTITION uses up all the rules.
- **Specificity.** A rule whose antecedent is exceptional for the others gets a higher layer and wins over them, as in the penguin example.
- **Irrelevance.** Atoms that occur in no rule do not change ranks: with only $a \to b$, also $a \wedge c \mathrel{|\!\sim} b$.
- **Deterministic and syntax independent.** The layers depend only on the models of the formulas, not on how the rules are written or ordered.

## Variants and improvements

- **System Z+.** Goldszmidt and Pearl gave each default a strength, and the ranking then uses the strengths in place of the layer numbers.
- **Lexicographic closure.** Lehmann (1995) compares worlds by the number of broken rules in each layer, from the highest layer down. This solves the drowning problem in the example above: the penguin that keeps its wings breaks fewer rules of layer $0$.
- **Maximum entropy.** Goldszmidt, Morris and Pearl (1993) rank worlds by the limit of the maximum entropy distributions, which also counts broken rules.
- **Inconsistent sets.** The implementation keeps the rules left over at line L4 and gives every world that breaks one of them the rank $\infty$. Then every formula of rank $\infty$ entails every formula, which is what rational closure does for such sets.
- **Compiled ranks.** The partition does not depend on the query. Compute it once, and answer each query with $O(\log r)$ satisfiability tests.

## When to use it

Use System Z when you have propositional rules of thumb with exceptions, you want answers that respect specificity, and you want a semantics with clear properties: it is rational closure, it satisfies System P and Rational Monotonicity, and it has a polynomial number of SAT calls. If you need rules in the same layer to keep working after one of them is broken, use the lexicographic closure or maximum entropy. If you need priorities among defaults that do not come from specificity, use System Z+ or a [default logic](/default-logic/) with priorities.

## Pitfalls

- **The drowning problem.** One broken rule of a layer blocks all rules of that layer for the exceptional worlds. Do not expect penguins to inherit wings from birds.
- **Material implication is not the conditional.** $\alpha \to \beta$ is not $\alpha \supset \beta$. The material counterpart is used only inside the tolerance test and the rank test.
- **Tolerance uses the remaining rules.** A rule of round $i$ must be tolerated by all rules that are still left, not by the whole set. Testing against the whole set at every round gives wrong layers.
- **Strict test at line L16.** $\kappa_Z(\alpha \wedge \beta) \le \kappa_Z(\alpha \wedge \neg\beta)$ would accept both $\beta$ and $\neg\beta$ for the Nixon diamond.
- **Unsatisfiable antecedents.** If $\alpha$ has rank $\infty$, every $\beta$ follows. Without the case $b = \infty$ at line L16, the test fails for such $\alpha$.

## Implementations

## History

Adams' probabilistic semantics for conditionals gave the notion of a consistent set of defaults. Pearl (1990) turned the consistency test into an ordering of the defaults, defined the ranking of worlds from it, and called the result System Z. In the same year Goldszmidt and Pearl showed that System Z agrees with the rational closure that Lehmann and Magidor had defined from a different starting point, the KLM rules and ranked models; the journal version of Lehmann and Magidor appeared in 1992. Later work on maximum entropy (1993), the lexicographic closure (1995) and System Z+ addressed the drowning problem and defaults of different strengths. Eiter and Lukasiewicz (2000) mapped the complexity of these semantics.

## References
