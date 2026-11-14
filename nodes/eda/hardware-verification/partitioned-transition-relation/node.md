---
tag: NQG9VW
kind: technique
slug: partitioned-transition-relation
name: Partitioned transition relation
aliases:
- early quantification
- conjunctive partitioning
area: eda/hardware-verification
level: advanced
summary: Keeps the transition relation as a list of BDD conjuncts and quantifies each variable as soon as no later conjunct uses it, so image computation stays small.
prereqs: [reduced-ordered-bdd, bdd-quantification, symbolic-reachability]
see_also: [transition-function-image-computation, product-machine, symbolic-model-checking, sequential-equivalence-checking, variable-ordering, state-explosion-problem, bdd-apply, invariant-checking]
sources:
  - paper: "Jerry R. Burch, Edmund M. Clarke and David E. Long, Symbolic model checking with partitioned transition relations, Proceedings of the International Conference on Very Large Scale Integration (VLSI 91), IFIP Transactions A-1, North-Holland, 49 to 58, 1991"
    title: J. R. Burch, E. M. Clarke and D. E. Long, Symbolic model checking with partitioned transition relations, VLSI 91, Edinburgh, IFIP Transactions A-1, 49 to 58, 1991
    locator: conjunctive partitioning for synchronous circuits, disjunctive partitioning for asynchronous ones, and the early quantification of variables
  - paper: "Rajeev K. Ranjan, Adnan Aziz, Robert K. Brayton, Bernard Plessier and Carl Pixley, Efficient BDD algorithms for FSM synthesis and verification, International Workshop on Logic Synthesis (IWLS 1995), Lake Tahoe, 1995"
    title: R. K. Ranjan, A. Aziz, R. K. Brayton, B. Plessier and C. Pixley, Efficient BDD algorithms for FSM synthesis and verification, IWLS 1995
    locator: the heuristics that order the conjuncts and cluster them up to a size limit, and the measured results on benchmark circuits
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 6 (symbolic model checking, the relational product and partitioned transition relations)
---

A partitioned transition relation keeps the transition relation of a circuit as a list of small BDDs whose conjunction is the relation, instead of one large BDD. To compute an image, it conjoins the set of states with the parts one at a time, and it quantifies each present-state or input variable as soon as no remaining part uses it. This step, *early quantification*, is exact because $\exists v.\,(A \wedge B) = A \wedge \exists v.\,B$ when $A$ does not depend on $v$. Burch, Clarke and Long (1991) introduced it. Here "transition relation" means the relation $T(s, x, y)$ on present states, inputs and next states, not the next-state functions. The [transition-function method](/transition-function-image-computation/) uses those functions and builds no relation. [Symbolic reachability](/symbolic-reachability/) is the fixed-point loop that calls either one as its image step.

## In plain words

To find the states a circuit can reach in one clock tick, you combine the set of present states with a rule that links present states to next states, and then you forget the present states. For a big circuit the full rule is too large to write down. So keep one small rule for each register bit, and add the rules one by one. When no rule that is still to come mentions a present-state bit or an input, forget that bit at once. The pieces you carry along stay small, and at the end you get the same answer as with the full rule.

## When it applies

- The system is synchronous, so the relation is a conjunction: $T(s, x, y) = \bigwedge_{i=1}^{m} T_i$ with $T_i = (y_i \equiv \delta_i(s, x))$. Each $T_i$ has a BDD about as small as $\delta_i$, while the BDD of $T$ can be far larger.
- Each $\delta_i$ depends on few variables, so many variables are used by few parts and can be quantified early. Circuits with local next-state logic fit well; a circuit where every next-state function depends on every latch gains little.
- For asynchronous or interleaving systems, the relation is a disjunction of the moves of the components. Existential quantification distributes over disjunction with no condition, so the image is the union of the images of the parts; see the variations.

## The template

The set of states is $S(s)$, the parts are $T_1, \ldots, T_k$ (one per latch, or clusters of them), and $Q = s \cup x$ is the set of variables to quantify. The next-state variables $y$ are never quantified.

```pseudo id=main
IMAGE-PARTITIONED(S, T₁, ..., Tₖ)
1  order T₁, ..., Tₖ by a heuristic
2  for j ← 1 to k do
3      Eⱼ ← (variables of Q in Tⱼ) minus (variables in Tⱼ₊₁, ..., Tₖ) minus (E₁ ∪ ... ∪ Eⱼ₋₁)
4  E₀ ← variables of Q in no Tⱼ
5  R ← ∃E₀. S
6  for j ← 1 to k do
7      R ← ∃Eⱼ. (R ∧ Tⱼ)
8  return R with each yᵢ renamed to sᵢ
```

Line 7 is one relational product (AND-EXISTS), which a BDD package does in one pass without building $R \wedge T_j$; see [BDD quantification](/bdd-quantification/). Line 3 puts each variable of $Q$ in the set of the last part that uses it.

**Lemma (early quantification).** If $v \notin \mathrm{supp}(A)$, then $\exists v.\,(A \wedge B) = A \wedge \exists v.\,B$. The same holds for a set $V$ of variables with $V \cap \mathrm{supp}(A) = \emptyset$.

*Proof.* By the [Shannon expansion](/shannon-expansion/), $\exists v.\,F = F|_{v=0} \vee F|_{v=1}$. Since $A$ does not depend on $v$, $A|_{v=0} = A|_{v=1} = A$. So

$$\exists v.\,(A \wedge B) = (A \wedge B|_{v=0}) \vee (A \wedge B|_{v=1}) = A \wedge (B|_{v=0} \vee B|_{v=1}) = A \wedge \exists v.\,B.$$

For a set $V = \{v_1, \ldots, v_r\}$, write $\exists V$ as $\exists v_1 \cdots \exists v_r$ and apply the one-variable case $r$ times, from the inside out. Each $\exists v_i.\,B'$ again does not add $v_1, \ldots, v_r$ to the support of $A$. $\square$

**Theorem (same image as the monolithic relation).** IMAGE-PARTITIONED returns $\exists Q.\,\big(S \wedge T_1 \wedge \cdots \wedge T_k\big)$, with $y$ renamed to $s$, for every order of the parts.

*Proof.* Let $F_j = E_0 \cup E_1 \cup \cdots \cup E_j$. We show that after the $j$-th pass of line 7,

$$R = \exists F_j.\,(S \wedge T_1 \wedge \cdots \wedge T_j).$$

For $j = 0$ this is line 5. Assume it for $j - 1$. By line 3 and line 4, no variable of $F_{j-1}$ is in $T_j$: a variable in $E_0$ is in no part, and a variable in $E_l$ with $l < j$ is in no part after $T_l$. So the lemma, with $A = T_j$ and $V = F_{j-1}$, gives

$$R \wedge T_j = \big(\exists F_{j-1}.\,(S \wedge T_1 \wedge \cdots \wedge T_{j-1})\big) \wedge T_j = \exists F_{j-1}.\,(S \wedge T_1 \wedge \cdots \wedge T_j),$$

and line 7 adds $\exists E_j$ in front. After the last pass, $R = \exists F_k.\,(S \wedge T)$. Every variable of $Q$ is in $F_k$: if it is in no part, it is in $E_0$, and otherwise it is in $E_j$ for the last $j$ whose part uses it. So $F_k = Q$. The order of line 1 was arbitrary. $\blacksquare$

The theorem is all that is proved here. That the intermediate BDDs are smaller than the BDD of $T$ is measured, not proved: Burch, Clarke and Long, and Ranjan and coauthors, report it on benchmark circuits, and in the worst case an intermediate $R$ can be as large as the monolithic product.

## Classic examples

**A three-bit machine.** Take the machine of the [image computation](/transition-function-image-computation/) example: $\delta_1 = s_1 \oplus x$, $\delta_2 = s_1 \wedge s_2$, $\delta_3 = x \vee s_2$ and $S = (s_1 \oplus s_2) \wedge \neg s_3$. With the order $T_2, T_3, T_1$, line 3 gives $E_1 = \emptyset$, $E_2 = \{s_2\}$, $E_3 = \{s_1, x\}$, and line 4 gives $E_0 = \{s_3\}$.

| step | quantified | $R$ |
|---|---|---|
| line 5 | $s_3$ | $s_1 \oplus s_2$ |
| with $T_2$ | none | $(s_1 \oplus s_2) \wedge \neg y_2$ |
| with $T_3$ | $s_2$ | $\neg y_2 \wedge (y_3 \equiv x \vee \neg s_1)$ |
| with $T_1$ | $s_1, x$ | $\neg y_2 \wedge (y_1 \vee y_3)$ |

The result is $\{100, 101, 001\}$ as $y_1 y_2 y_3$, the same as the range method gives, and every step was checked by enumeration. No intermediate $R$ has more than 4 variables, while $S \wedge T$ has 7.

**Reachable states.** [Symbolic reachability](/symbolic-reachability/) iterates this image until the set of reached states stops growing. It is the setting in which Burch, Clarke and Long measured the method.

**Sequential equivalence.** The [product machine](/product-machine/) of two circuits has the parts of both, and its next-state logic is local to each circuit. So the parts of one circuit never mention the latches of the other, and early quantification separates them well. This is how BDD-based [sequential equivalence checking](/sequential-equivalence-checking/) computes reachable states.

**Model checking of CTL.** The preimage $\exists y, x.\,(S(y) \wedge T)$ behind $\mathsf{EX}$ in [symbolic model checking](/symbolic-model-checking/) uses the same schedule, with $y$ and $x$ quantified and $s$ kept.

## Variations

- **Clustering.** Conjoin neighbouring parts into clusters while the BDD of a cluster stays under a size limit. Fewer, larger parts mean fewer relational products. Ranjan and coauthors (1995) gave heuristics to order the parts and to form the clusters, and measured their effect on benchmark circuits.
- **Disjunctive partitioning.** For $T = T_1 \vee \cdots \vee T_k$, $\exists Q.\,(S \wedge T) = \bigvee_j \exists Q.\,(S \wedge T_j)$ with no condition on supports, because $\exists$ distributes over $\vee$. Burch, Clarke and Long used this for asynchronous systems, where one component moves at a time.
- **Preimage.** Quantify $y$ and $x$, keep $s$, with the same schedule over the parts.
- **The transition-function method.** Do not build any relation; constrain the next-state functions by $S$ and compute their range. See [transition function image computation](/transition-function-image-computation/).

## Pitfalls

- **Quantifying too early.** $\exists$ does not distribute over $\wedge$ in general. With $A = x$ and $B = \neg x$, $\exists x.\,(A \wedge B) = 0$, but $(\exists x.\,A) \wedge (\exists x.\,B) = 1$. A variable may be quantified only after the last part that uses it.
- **Quantifying $y$.** The next-state variables are the result. Quantifying any of them gives a projection of the image, not the image.
- **The variable order.** The BDD of $y_i \equiv \delta_i$ is small only if $y_i$ sits next to the support of $\delta_i$ in the order. The usual choice interleaves $s_i$ and $y_i$, which also makes the final renaming of line 8 cheap. See [variable ordering](/variable-ordering/).
- **The order of the parts.** Every order gives the same image, but a bad order keeps variables alive for long and gives large intermediate BDDs. The theorem says nothing about sizes.

## Exercises

1. Prove that $\exists v.\,(A \vee B) = (\exists v.\,A) \vee (\exists v.\,B)$ for all $A$ and $B$, and use it to show that disjunctive partitioning gives the exact image.
2. Find $A$ and $B$, with $v$ in the supports of both, such that $\exists v.\,(A \wedge B) \ne A \wedge \exists v.\,B$.
3. In the three-bit example, run the template with the order $T_1, T_2, T_3$. Give $E_0, \ldots, E_3$ and the largest number of variables of an intermediate $R$.
4. For parts with the supports $\{s_1, x_1\}$, $\{s_1, s_2\}$, $\{s_2, x_2\}$ and $\{s_3\}$ (besides their own $y_i$), find an order that quantifies a variable after every part.

## References
