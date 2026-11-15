---
tag: WXMFTE
kind: algorithm
slug: dalal-revision
name: Dalal's revision operator
aliases:
- Hamming distance revision
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: Revises by the models of the new formula that are at minimum Hamming distance from some model of the old beliefs.
solves: [belief-revision]
model: word-ram
complexity:
  vars: {n: the number of atoms}
  time: {worst: Θ(n·2^n), best: Θ(2^n)}
  space: {extra: Θ(2^n)}
properties: {deterministic: true}
history:
  year: 1988
  people: [Mukesh Dalal]
  note: Defined revision by the least number of atom changes and showed that it satisfies the Gardenfors postulates for revision.
prereqs: [hamming-distance, belief-revision, agm-postulates]
see_also: [katsuno-mendelzon-revision, grove-spheres, possible-models-approach, belief-update, belief-merging, multi-source-bfs, max-sat, polynomial-hierarchy]
sources:
  - paper: "Mukesh Dalal, Investigations into a theory of knowledge base revision: preliminary report, Proceedings of the Seventh National Conference on Artificial Intelligence (AAAI-88), 475 to 479 (1988)"
    locator: p. 476 (the operator G on models and the definition of revision by the least k) and p. 477 (the syntactic form of G and the check of the Gardenfors postulates)
  - paper: doi:10.1016/0004-3702(91)90069-V
    title: Hirofumi Katsuno and Alberto O. Mendelzon, Propositional knowledge base revision and minimal change, Artificial Intelligence 52(3), 263 to 294 (1991)
    locator: Section 3 (the postulates R1 to R6 and the representation by faithful assignments) and the discussion of Dalal's operator as an instance
  - paper: doi:10.1016/0004-3702(92)90018-S
    title: Thomas Eiter and Georg Gottlob, On the complexity of propositional knowledge base revision, updates, and counterfactuals, Artificial Intelligence 57(2-3), 227 to 270 (1992)
    locator: Section 3 (Example 3.3, and which operators satisfy R1 to R6), Theorem 6.9 (the general case), Theorem 7.4 (the Horn case) and Theorems 8.1 and 8.3 (bounded new formula)
  - paper: "Thomas Eiter and Georg Gottlob, On the complexity of propositional knowledge base revision, updates, and counterfactuals, Proceedings of the Eleventh ACM Symposium on Principles of Database Systems (PODS 1992)"
    locator: the extended abstract of the journal paper
---

Dalal's operator is the best known concrete [belief revision](/belief-revision/) operator for a finite propositional language. To revise a belief base $K$ by a formula $p$, it keeps the models of $p$ that change as few atoms as possible in some model of $K$. The number of changed atoms is the [Hamming distance](/hamming-distance/) between two worlds. Mukesh Dalal defined it in 1988, and Katsuno and Mendelzon (1991) showed that it fits their characterization of the [AGM postulates](/agm-postulates/): it satisfies R1 to R6. On sets of models it is a breadth-first search over the cube $\{0,1\}^n$ that starts from all models of $K$ at once. On formulas the same question is complete for $\mathrm{P}^{\mathrm{NP}[O(\log n)]}$ (Eiter and Gottlob 1992, Theorem 6.9).

## In plain words

A world is one way of making each atom true or false. Your beliefs allow some worlds. New information allows some worlds too, and you must now believe it. If some world is allowed by both, keep exactly those worlds. If not, look for the allowed worlds of the new information that are nearest to your old worlds, where the distance between two worlds is the number of atoms on which they disagree. Keep only the nearest ones. So you give up as few separate facts as you can, and you count each atom as one fact.

The search goes outwards in rings. Ring 0 is your old worlds. Ring 1 is every world that you get by changing one atom, ring 2 by changing two, and so on. Stop at the first ring that contains a world of the new information.

## The problem

Fix $n$ atoms $x_0, \ldots, x_{n-1}$. A world is a vector $w \in \{0,1\}^n$, and $h(u, v)$ is the number of positions where $u$ and $v$ differ. The input is $n$, the set $K = \mathrm{Mod}(\psi)$ of the models of the base and the set $P = \mathrm{Mod}(\mu)$ of the models of the new formula. For nonempty $K$ let $\mathrm{dist}(w, K) = \min_{u \in K} h(w, u)$. The output is

$$\mathrm{Mod}(\psi \circ_D \mu) = \{w \in P : \mathrm{dist}(w, K) = d^*\}, \qquad d^* = \min_{w \in P} \mathrm{dist}(w, K),$$

with $\psi \circ_D \mu \equiv \mu$ when $\psi$ is unsatisfiable, and the empty set when $\mu$ is unsatisfiable. Dalal states it through an operator $G$ on formulas: $\mathrm{Mod}(G(\psi))$ is the set of the worlds that differ from some model of $\psi$ in at most one atom, and $\psi \circ_D \mu$ is $G^k(\psi) \wedge \mu$ for the least $k$ that makes this satisfiable (Dalal 1988, p. 476). The two forms agree because $\mathrm{Mod}(G^k(\psi)) = \{w : \mathrm{dist}(w, K) \le k\}$.

## The algorithm

$S$ is the set of the worlds reached so far and $L$ is the current ring. Worlds are stored as integers, with bit $i$ for atom $x_i$.

```pseudo id=main
DALAL(K, P, n)
L1  if P = ∅ then return ∅
L2  if K = ∅ then return P                        ▷ no model to be near
L3  L ← K;  S ← K;  d ← 0
L4  while L ∩ P = ∅ do
L5      N ← ∅
L6      for each w in L do
L7          for i ← 0 to n-1 do
L8              v ← w xor 2^i                     ▷ change atom i
L9              if v ∉ S then add v to S and to N
L10     L ← N;  d ← d + 1
L11 return L ∩ P  (and d)
```

This is [multi-source BFS](/multi-source-bfs/) on the hypercube graph, in which two worlds are adjacent when they differ in one atom. Ring $d$ is $\mathrm{Mod}(G^d(\psi))$ minus $\mathrm{Mod}(G^{d-1}(\psi))$. The loop stops at $d = d^*$, so it never builds the rings beyond the answer.

## Example

This is Example 3.3 of Eiter and Gottlob (1992). The atoms are $a, b, c, d$, and a world is written as the bit string $abcd$. The base is $\psi = a \wedge b \wedge c$ and the new formula is

$$\mu = (\neg a \wedge d) \vee (a \wedge \neg b \wedge \neg c \wedge \neg d).$$

So $K = \{1110, 1111\}$ and $P = \{0001, 0011, 0101, 0111, 1000\}$. $K \cap P$ is empty, so the old beliefs and $\mu$ conflict.

| ring $d$ | new worlds in the ring | meets $P$ |
|---|---|---|
| 0 | 1110, 1111 | no |
| 1 | 0110, 1010, 1100, 0111, 1011, 1101 | 0111 |

Line L8 tries $2 \cdot 4 = 8$ changes of one atom. Two of them lead back into $K$, and six give the new worlds of ring 1. The run stops with $d = 1$ and the result $\{0111\}$, that is $\psi \circ_D \mu \equiv \neg a \wedge b \wedge c \wedge d$. The distances of all five models of $\mu$ confirm it:

| model of $\mu$ | 0001 | 0011 | 0101 | 0111 | 1000 |
|---|---|---|---|---|---|
| $\mathrm{dist}(w, K)$ | 3 | 2 | 2 | 1 | 2 |

The world $1000$ shows what a count does. It differs from $1110$ in $b$ and $c$, two atoms, while $0111$ differs from $1111$ only in $a$. Satoh's operator compares the sets of changed atoms by inclusion instead of by size, and $\{a\}$ and $\{b, c\}$ are not comparable, so it keeps both worlds (Eiter and Gottlob 1992, Example 3.3).

A smaller case from Dalal (1988): revising $a \wedge \neg b$ by $b$ gives $a \wedge b$. The fact $a$ survives because the change to $b$ alone is enough.

## Correctness

At the test of line L4, $L$ is exactly the set of the worlds at distance $d$ from $K$, and $S$ is the set at distance at most $d$. The induction step uses one fact of the hypercube: a world at distance $j \ge 1$ has a neighbour at distance $j - 1$, and neighbours differ in distance by at most 1. So line L9 adds exactly the worlds at distance $d + 1$. The loop runs while no world of $P$ is in the ring, which means $d < d^*$, and it stops at $d = d^*$ with $L \cap P$ equal to the required set. Since all distances are at most $n$, it stops after at most $n$ rounds. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Each world enters $S$ once, so lines L7 to L9 run at most $n \cdot |S| \le n \cdot 2^n$ times. With $K$, $P$ and $S$ as bit arrays of $2^n$ bits on the [word RAM](/word-ram/), each step is $O(1)$, so the time is $\Theta(n \cdot 2^n)$ in the worst case and $\Theta(2^n)$ in the best case, where the bit arrays are set up and $K \cap P$ is already nonempty. The worst case is reached when $K = \{0^n\}$ and $P = \{1^n\}$: then $d^* = n$ and every world is visited. The extra space is $2^n$ bits for $S$. The Python version uses hash sets, so its cost is $O(|K| + |P| + n \cdot |S|)$ expected time, which is small when the answer is near $K$.

The brute-force method computes $\mathrm{dist}(w, K)$ for each $w \in P$ in $O(|K| \cdot |P|)$ distance computations, each a [population count](/population-count/) of $u \oplus w$. It wins when $K$ and $P$ are small and $d^*$ is large, and the ring method wins when $K$ is large or $d^*$ is small.

When $\psi$ and $\mu$ are formulas, the model sets can have $2^n$ members, and the right measure is the cost of the decision problem "does $\psi \circ_D \mu$ entail $q$". It is $\mathrm{P}^{\mathrm{NP}[O(\log n)]}$-complete, and hard already when $\psi$ is a conjunction of atoms (Eiter and Gottlob 1992, Theorem 6.9). The upper bound is a [binary search](/binary-search/) on $k \in \{0, \ldots, n\}$. Each step asks one [SAT](/sat/) question: is there a model of $\mu$ within distance $k$ of a model of $\psi$? Then one more question decides whether some model of $\mu \wedge \neg q$ is at distance $d^*$. Hardness stays when $\psi$, $\mu$ and $q$ are Horn (Theorem 7.4, which uses a base of literals). If the size of $\mu$ is bounded by a constant, a constant number of NP calls suffices (Theorem 8.1), and with Horn formulas as well the problem is solvable in time $O(|\psi| \cdot |q|)$ (Theorem 8.3). These classes sit in the [polynomial hierarchy](/polynomial-hierarchy/) below $\Sigma_2^P$. Most other model-based operators, including Satoh's and the [possible models approach](/possible-models-approach/) of Winslett, are $\Pi_2^P$-complete (Theorem 6.4).

## Properties

- **It satisfies R1 to R6.** The ranks $\mathrm{dist}(\cdot, K)$ form a total preorder on worlds in which the models of $K$ are exactly the worlds of rank 0. This is a faithful assignment, so by the [Katsuno and Mendelzon theorem](/katsuno-mendelzon-revision/) the operator satisfies R1 to R6, and so the AGM postulates K*1 to K*8 for belief sets over a finite language.
- **It is a system of spheres.** Sphere $k$ is $\mathrm{Mod}(G^k(\psi))$. These sets are nested, the smallest is $\mathrm{Mod}(\psi)$, and the largest is every world, as in [Grove's model](/grove-spheres/).
- **It depends only on the models.** Equivalent bases and equivalent new formulas give the same result, so the syntax does not matter (R4).
- **It depends on the choice of atoms.** Rename the language and the distance changes. Take $\psi = a \wedge b$ and $\mu = \neg(a \wedge b)$: the result is $(a \wedge \neg b) \vee (\neg a \wedge b)$. Now use the atoms $x = a$ and $y = a \oplus b$, which describe the same worlds. Then $\psi$ is $x \wedge \neg y$, the worlds $\neg a \wedge \neg b$ and $a \wedge \neg b$ are at distance 1, and the result is $\neg b$.
- **It is a revision, not an update.** It takes the models of $\mu$ nearest to the whole set $K$. An [update](/belief-update/) takes the nearest models of $\mu$ for each model of $K$ separately.

## Variants and improvements

- **Weighted distance.** Give each atom a positive weight and add the weights of the changed atoms. The ring method becomes Dijkstra's algorithm on the cube, or a bucket queue for small integer weights. The postulates still hold, since the ranks are still a total preorder with the models of $K$ alone at rank 0.
- **Satoh's operator.** Compare the sets of changed atoms by inclusion. This gives a partial preorder, and the operator satisfies R1 to R5 but fails R6 (Eiter and Gottlob 1992, Section 3).
- **Model-wise distance.** Winslett's possible models approach and Forbus's operator use the same kind of distance, but for each model of $K$ separately. They are update operators.
- **Merging.** Summing the Hamming distances to several bases gives a distance-based operator for [belief merging](/belief-merging/).
- **With a SAT solver.** For formulas, ask for a model of $\mu$ and a copy of $\psi$ with at most $k$ disagreeing atoms, using a cardinality constraint, and search on $k$. Or minimise the number of disagreements with a [MaxSAT](/max-sat/) solver, where each "atom $i$ is the same in both copies" is a soft clause.

## When to use it

Use it when the beliefs are a small propositional theory, the atoms are independent facts of the same weight, and the new information must be accepted. Examples are repairs of a configuration, of a database row, or of a sensor reading, where each atom is one value that can be wrong. With at most 20 or 25 atoms, the ring method on bit arrays is direct. With more atoms, work on formulas with a SAT or MaxSAT solver. If the facts have different weights, use the weighted variant. If the world has changed, rather than your knowledge of it, use an update operator. If several revisions follow one another, one total preorder per base is not enough, and the [Darwiche and Pearl postulates](/darwiche-pearl-postulates/) apply.

## Pitfalls

- **Distance from the set, not from each model.** The minimum is over all pairs of a model of $K$ and a model of $\mu$. Taking the nearest models of $\mu$ for each model of $K$ and their union gives an update operator, which fails R2.
- **Stopping one ring too late.** Test the ring against $P$ before building the next one. Otherwise the result mixes two distances.
- **Inconsistent base.** If $K$ has no model, there is no first ring. Return $P$, as line L2 does.
- **Unsatisfiable new formula.** The result is empty, and R3 does not apply.
- **Worlds outside the cube.** An integer that is not below $2^n$ is not a world. The Python version rejects it with an error.
- **Treating the result as unique to the language.** The operator answers for one fixed set of atoms. Adding defined atoms or recoding values changes the result, as shown in the properties.

## Implementations

## History

Dalal presented the operator at AAAI-88, defined by the iterated operator $G$. He also gave $G$ on formulas: for each atom, take $\psi$ with that atom set to true or to false, which forgets the atom (a construction from Weber 1987), and join the results for all atoms with "or". He gave six principles for revision, among them the persistence of prior knowledge, and checked his operator against the Gardenfors postulates. Katsuno and Mendelzon (1991) gave the semantic characterization of the AGM postulates by faithful assignments and showed that Dalal's operator is an instance. Eiter and Gottlob (1992) placed it in the polynomial hierarchy. Its entailment problem is in $\mathrm{P}^{\mathrm{NP}[O(\log n)]}$, while for the other operators of their study the general problem is $\Pi_2^P$-hard.

## References
