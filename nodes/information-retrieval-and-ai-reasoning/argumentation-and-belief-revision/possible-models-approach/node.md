---
tag: J9PKJ2
kind: algorithm
slug: possible-models-approach
name: Possible models approach
aliases:
- Winslett PMA
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: Updates each model of the old beliefs to the models of the new formula that differ from it in a minimal set of atoms.
solves: [belief-update]
model: word-ram
complexity:
  vars: {n: the number of atoms, k: the number of models of the base}
  time: {worst: Θ(k·n·2^n), best: Θ(2^n)}
  space: {extra: Θ(2^n)}
properties: {deterministic: true}
history:
  year: 1988
  people: [Marianne Winslett]
  note: Defined the effect of an action on each possible model separately, with change measured by the set of atoms that differ, as a syntax-independent answer to the frame problem.
prereqs: [belief-update, hamming-distance]
see_also: [dalal-revision, katsuno-mendelzon-revision, belief-revision, frame-problem, situation-calculus, sum-over-subsets-dp, polynomial-hierarchy]
sources:
  - paper: "Marianne Winslett, Reasoning about action using a possible models approach, Proceedings of the Seventh National Conference on Artificial Intelligence (AAAI-88), 89 to 93 (1988)"
    locator: p. 90, Section 3 (the definition of Incorporate(S, M) by set inclusion on the differing atoms, and the union over the models of the theory) and Section 4 (the frame problem example)
  - paper: "Hirofumi Katsuno and Alberto O. Mendelzon, On the difference between updating a knowledge base and revising it, in James Allen, Richard Fikes and Erik Sandewall (eds), Proceedings of the Second International Conference on Principles of Knowledge Representation and Reasoning (KR'91), Morgan Kaufmann, 387 to 394 (1991)"
    locator: the whole paper (the postulates U1 to U8, their representation by faithful assignments of partial preorders, and the possible models approach as an update operator)
  - paper: doi:10.1016/0004-3702(92)90018-S
    title: Thomas Eiter and Georg Gottlob, On the complexity of propositional knowledge base revision, updates, and counterfactuals, Artificial Intelligence 57(2-3), 227 to 270 (1992)
    locator: Section 3 (the model-based operators of Winslett, Forbus, Satoh and Borgida), Theorem 6.4 (the general case) and Theorem 7.2 (Horn formulas)
---

The possible models approach (PMA) of Marianne Winslett is the classic operator for [belief update](/belief-update/), the change of beliefs when the world itself has changed. It treats each model of the old beliefs as a possible state of the world and moves each one separately to the models of the new formula that change as little as possible. "As little as possible" is measured by the set of atoms that change, compared by set inclusion. The result is the union of what each old model becomes. Winslett (1988) defined it to reason about the effects of actions, and Katsuno and Mendelzon (1991) showed that it satisfies their update postulates U1 to U8. On model sets it takes $O(k \cdot n \cdot 2^n)$ time for $k$ old models over $n$ atoms. On formulas, deciding whether the result entails a given formula is $\Pi_2^P$-complete (Eiter and Gottlob 1992, Theorem 6.4).

## In plain words

You do not know exactly how the world is, so you keep a list of the states it could be in. Then an action happens, and afterwards some fact is true. For each state on your list, ask: what is the smallest change to this state that makes the fact true? Keep every answer that changes no more than it must, where "no more" means that no other answer changes only a part of the same things. Do this for each state on its own, and your new list is all the answers together.

Two answers that change different things, such as "the lamp moved" and "the chair and the table moved", are both kept. The method does not count the changes. It only throws out an answer when another answer changes a part of what it changes.

## The problem

Fix $n$ atoms. A world is a vector $w \in \{0,1\}^n$, which we also read as the set of its true atoms. For two worlds, $\mathrm{Diff}(w, v) = w \oplus v$ is the set of the atoms on which they differ. The input is $n$, the set $K = \mathrm{Mod}(\psi)$ of the models of the old beliefs and the set $P = \mathrm{Mod}(\mu)$ of the models of the new formula. The output is

$$\mathrm{Mod}(\psi \diamond_{\mathrm{PMA}} \mu) = \bigcup_{w \in K} \mathrm{Min}(w), \qquad \mathrm{Min}(w) = \{v \in P : \text{no } u \in P \text{ has } \mathrm{Diff}(w, u) \subsetneq \mathrm{Diff}(w, v)\}.$$

In Winslett's words, $\mathrm{Min}(w)$ is $\mathrm{Incorporate}(S, w)$: the models of the postconditions $S$ such that no other such model differs from $w$ on fewer atoms, "where 'fewer' is defined by set inclusion" (Winslett 1988, p. 90). Winslett also keeps a set of protected formulas that must hold after every action. Here they are part of $\mu$.

If $K$ is empty the result is empty, and if $P$ is empty the result is empty.

## The algorithm

Worlds and change sets are integers, with bit $i$ for atom $i$. For one world $w$, an array $C$ of $2^n$ bits records which change sets lead into $P$. Lines L6 and L7 close it upwards, one atom at a time, so that afterwards $C[x]$ is true when some model of $P$ differs from $w$ only on atoms inside $x$. This is the zeta transform of [sum over subsets](/sum-over-subsets-dp/) with "or" in place of "+".

```pseudo id=main
PMA(K, P, n)
L1  R ← ∅
L2  for each w in K do
L3      if w ∈ P then
L4          add w to R;  continue                   ▷ the empty change set is the least
L5      C[x] ← ((w xor x) ∈ P) for each x in 0 .. 2^n - 1
L6      for i ← 0 to n-1 do
L7          for each x that has bit i do C[x] ← C[x] or C[x xor 2^i]
L8      for each v in P do
L9          x ← w xor v;  if C[x xor 2^i] is false for every bit i of x then
L10             add v to R                          ▷ no change set inside x leads to P
L11 return R
```

A proper subset of $x$ lies inside $x$ minus one of its atoms. So line L9 needs only $|x| \le n$ lookups to find out whether a smaller change set exists.

## Example

The atoms are $a$, $b$ and $c$, and a world is written as the bit string $abc$. The old beliefs are $\psi = \neg a \wedge (b \leftrightarrow c)$, so $K = \{000, 011\}$. The new formula is $\mu = (a \wedge \neg b \wedge \neg c) \vee (\neg a \wedge b \wedge c)$, so $P = \{100, 011\}$.

| model $w$ of $K$ | change sets to $P$ | minimal ones | $\mathrm{Min}(w)$ |
|---|---|---|---|
| 000 | $\{a\}$ to 100, $\{b, c\}$ to 011 | both | $\{100, 011\}$ |
| 011 | $\emptyset$ to 011 | $\emptyset$ | $\{011\}$ (lines L3 and L4) |

For $w = 000$, line L5 marks $C[\{a\}]$ and $C[\{b, c\}]$. After lines L6 and L7, $C[x]$ is true for $\{a\}$, $\{a, b\}$, $\{a, c\}$, $\{b, c\}$ and $\{a, b, c\}$. For $v = 100$, line L9 looks at $C[\emptyset]$, which is false, so $v$ is kept. For $v = 011$, it looks at $C[\{c\}]$ and $C[\{b\}]$, which are both false, so $v$ is kept too. The result is $\{100, 011\}$, which is $\mu$ itself: the update has lost the fact $\neg a$.

Two other operators on the same input show what the choices do:

- **Forbus's update** counts the changed atoms instead of comparing them by inclusion. From $000$ it keeps only $100$, one atom away, and drops $011$, two atoms away.
- **[Dalal's revision](/dalal-revision/)** compares the distance to the whole set $K$. Since $011$ is in both $K$ and $P$, the revision is $K \cap P = \{011\}$, that is $\neg a \wedge b \wedge c$.

**Update against revision.** In the book and magazine example of Katsuno and Mendelzon (1991, KR), $b$ says that the book is on the table and $m$ that the magazine is. The agent knows that exactly one of them is there, $\psi = (b \wedge \neg m) \vee (\neg b \wedge m)$, and then learns $\mu = b$. The PMA moves the world $\neg b \wedge m$ to $b \wedge m$ and keeps the world $b \wedge \neg m$, so the update is $b$, with nothing known about the magazine. Dalal's revision gives $b \wedge \neg m$, because $\mu$ is consistent with $\psi$. The update is right if a robot was told to put the book on the table, and the revision is right if the agent only learned more about a room that did not change.

## Correctness

For $w \in P$, the empty change set is a subset of every other change set, so $\mathrm{Min}(w) = \{w\}$, which lines L3 and L4 return. For $w \notin P$, after round $i$ of lines L6 and L7 the entry $C[x]$ is true exactly when some change set $y$ to $P$ has $y \subseteq x$ and agrees with $x$ on the atoms above $i$. After the last round this is "some $y \subseteq x$". A change set $y \subsetneq x$ misses some atom $i$ of $x$, so $y \subseteq x \oplus 2^i$, and the test of line L9 finds it. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

For each model $w$ of $K$ outside $P$, line L5 costs $O(2^n)$, lines L6 and L7 cost $\Theta(n \cdot 2^n)$, and lines L8 to L10 cost $O(n \cdot |P|)$. With $k = |K|$ and $P$, $R$ and $C$ stored as bit arrays on the [word RAM](/word-ram/), the time is $\Theta(k \cdot n \cdot 2^n)$ in the worst case. The best case is $K \subseteq P$, where only the arrays are set up, in $\Theta(2^n)$ time. The extra space is $2^n$ bits for $C$, which is reused for each $w$.

The direct method compares all pairs of models of $P$ for each $w$, in $O(k \cdot |P|^2)$ subset tests. It is faster when $P$ is small. The transform wins when $P$ holds more than about $\sqrt{n \cdot 2^n}$ worlds.

On formulas the model sets can have $2^n$ members, and the question is whether $\psi \diamond_{\mathrm{PMA}} \mu$ entails a formula $q$. Eiter and Gottlob (1992) show that this is $\Pi_2^P$-complete (Theorem 6.4), the same as for Forbus's, Satoh's and Borgida's operators. A counterexample is a model $w$ of $\psi$ and a model $v$ of $\mu \wedge \neg q$ such that no model of $\mu$ has a smaller change set from $w$, which is one NP guess followed by one coNP check. When $\psi$, $\mu$ and $q$ are Horn, the problem drops to coNP-complete (Theorem 7.2). Both classes are in the [polynomial hierarchy](/polynomial-hierarchy/).

## Properties

- **It satisfies U1 to U8.** For each world $w$, define $v \le_w u$ when $\mathrm{Diff}(w, v) \subseteq \mathrm{Diff}(w, u)$. This is a partial order in which $w$ is below every other world, so the assignment $w \mapsto {\le_w}$ is faithful in the sense of Katsuno and Mendelzon, and $\mathrm{Min}(w)$ is the set of the $\le_w$-least models of $\mu$. By their representation theorem the operator satisfies the update postulates U1 to U8 (Katsuno and Mendelzon 1991, KR). The tests check all eight on random inputs.
- **It is not a revision.** In the book and magazine example, $\psi \wedge \mu$ is consistent but the update is not $\psi \wedge \mu$, so the revision postulate R2 fails. Dalal's revision fails U8 on the same input: updating the two models of $\psi$ one by one gives $b$, but revising the whole of $\psi$ gives $b \wedge \neg m$.
- **It depends only on the models.** Winslett notes that the PMA depends on the models of the theory and not on how its formulas are written, unlike the possible worlds approach of Ginsberg and Smith (Winslett 1988, p. 90).
- **It depends on the choice of atoms.** In the book and magazine example, use the atoms $x = b$ and $y = b \oplus m$. Then $\psi$ is $y$, and $\mu$ is $x$. The world $\neg b \wedge m$ is $\neg x \wedge y$. Its change sets are $\{x\}$ to $b \wedge \neg m$ and $\{x, y\}$ to $b \wedge m$, so only $b \wedge \neg m$ is kept, and the update becomes $b \wedge \neg m$, the same as the revision.
- **An inconsistent base stays inconsistent.** If $\psi$ has no model, the union is empty. This is what U2 asks, since an unsatisfiable $\psi$ entails every $\mu$.

## Variants and improvements

- **Forbus's update.** Measure the change from $w$ by the number of differing atoms, the [Hamming distance](/hamming-distance/), and keep the nearest models of $\mu$ for each $w$. The preorder $\le_w$ is then total.
- **Borgida's operator.** Return $\psi \wedge \mu$ when it is satisfiable and the PMA result otherwise. This is a revision operator built from the PMA (Eiter and Gottlob 1992, Section 3).
- **Satoh's revision.** Compare the change sets by inclusion, as the PMA does, but minimize over all pairs of a model of $\psi$ and a model of $\mu$ together, not for each model of $\psi$ on its own.
- **Protected formulas.** Winslett's integrity constraints must hold in every result. Add them to $\mu$, or keep them apart so that they need not be stated again for each action.
- **With a solver.** For formulas, the inner test "no model of $\mu$ has a smaller change set from $w$" is a [SAT](/sat/) question, so a two-level search, with an NP oracle inside an NP search, decides entailment.

## When to use it

Use the PMA when the new formula describes the result of a change in the world, such as an action, an event or a database update, and the old beliefs are a disjunction of possible states. Each possible state must then evolve on its own, and a state that was possible before must lead to some state after. If the new formula is only more information about an unchanged world, use a revision operator such as [Dalal's](/dalal-revision/). If the atoms are not equally important or changes should be counted, use Forbus's operator or a weighted variant. If actions have indirect effects, write them as protected formulas or use a richer action theory such as the [situation calculus](/situation-calculus/), since the PMA alone may let unrelated atoms change.

## Pitfalls

- **Minimal for each model, not over the set.** The minimum is taken for each model of $\psi$ on its own. Taking the closest models of $\mu$ to the whole set $K$ gives Satoh's revision, which fails U8.
- **Inclusion, not count.** A change of two atoms is kept when no other model of $\mu$ changes a subset of those atoms. Counting the atoms gives Forbus's operator, which can give a different result.
- **Lost facts.** The update keeps no fact of $\psi$ that $\mu$ could change. In the example, $\neg a$ is lost, because one old state moved to a world where $a$ is true.
- **Indirect effects.** Without constraints, the PMA lets only the atoms in $\mu$ change, and it may also make a disjunction where common sense expects one definite change. Winslett's frame problem example uses protected formulas so that moving one object updates the facts that depend on it.
- **Inconsistent base.** The result is empty, not $\mu$. This differs from Dalal's revision, which returns $\mu$.

## Implementations

## History

Winslett presented the PMA at AAAI-88 as a way to reason about actions. She contrasted it with the possible worlds approach of Ginsberg and Smith, which changes a set of formulas and so depends on how they are written. The PMA works on the models: each model is changed by as few atoms as set inclusion allows, and protected formulas state the laws of the domain. Katsuno and Mendelzon (1991) separated update from revision. They gave the postulates U1 to U8, proved a representation by faithful assignments of preorders, one for each world, and showed that the PMA is an update operator in their sense. Eiter and Gottlob (1992) found that its entailment problem is complete for the second level of the polynomial hierarchy, and coNP-complete for Horn formulas.

## References
