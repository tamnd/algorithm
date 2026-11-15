---
tag: DNSBMF
kind: definition
slug: default-extension
name: Default extension
aliases:
- default logic extension
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: An extension of a default theory is a set of beliefs that is a fixed point of Reiter's operator, so it contains the facts and every default conclusion it does not block.
prereqs: [default-logic, fixed-point]
see_also: [default-logic-complexity, nonmonotonic-reasoning, autoepistemic-logic, stable-model-semantics, gelfond-lifschitz-reduct, system-p]
sources:
  - paper: doi:10.1016/0004-3702(80)90014-4
    title: Raymond Reiter, A logic for default reasoning, Artificial Intelligence 13(1-2), 81 to 132 (1980)
    locator: Section 2 (the operator Gamma, the definition of an extension and Theorem 2.1) and Section 3 (normal default theories always have extensions, semi-monotonicity, orthogonality)
  - paper: doi:10.1016/0004-3702(90)90101-5
    title: Sarit Kraus, Daniel Lehmann and Menachem Magidor, Nonmonotonic reasoning, preferential models and cumulative logics, Artificial Intelligence 44(1-2), 167 to 207 (1990)
    locator: Section 3.1 (Makinson's observation that default logic, even with normal defaults, fails Cautious Monotonicity)
  - paper: doi:10.1093/logcom/2.3.397
    title: Georg Gottlob, Complexity results for nonmonotonic logics, Journal of Logic and Computation 2(3), 397 to 425 (1992)
    locator: the Sigma2P-completeness of deciding whether a finite propositional default theory has an extension
---

An extension is what a [default theory](/default-logic/) lets you believe. A default $\alpha : \beta / \gamma$ says "if $\alpha$ is believed and $\beta$ can be consistently assumed, believe $\gamma$". The trouble is that "can be consistently assumed" refers to the final set of beliefs, which the defaults are still building. Reiter (1980) solved this with a [fixed point](/fixed-point/): guess the final set $E$, use $E$ only for the consistency tests, derive everything that the facts and the applicable defaults give, and accept $E$ when the result is $E$ again. A theory can have one extension, several, or none.

## Definition

A *default theory* is a pair $(W, D)$. Here $W$ is a set of formulas (the facts) and $D$ is a set of *defaults* $\alpha : \beta_1, \ldots, \beta_n / \gamma$ with a *prerequisite* $\alpha$, *justifications* $\beta_1, \ldots, \beta_n$ and a *conclusion* $\gamma$. This page uses the propositional case: finitely many atoms, $W$ and $D$ finite. $\mathrm{Th}(S)$ is the set of the classical consequences of $S$, and $\mathrm{cons}(G)$ is the set of the conclusions of the defaults in $G$.

For a set of formulas $S$, let $\Gamma(S)$ be the smallest set $T$ of formulas with these three properties.

1. $W \subseteq T$.
2. $\mathrm{Th}(T) = T$.
3. For each default $\alpha : \beta_1, \ldots, \beta_n / \gamma$ in $D$: if $\alpha \in T$ and $\neg\beta_i \notin S$ for each $i$, then $\gamma \in T$.

A set $E$ is an *extension* of $(W, D)$ if $\Gamma(E) = E$ (Reiter 1980, Section 2). The argument $S$ is used only in the consistency test $\neg\beta_i \notin S$. The rest of the construction is a least set, so every formula of an extension has a derivation from $W$ by classical steps and default steps whose justifications are consistent with the extension.

**Iterative form.** Reiter's Theorem 2.1 gives an equivalent test. Put $E_0 = W$ and

$$E_{i+1} = \mathrm{Th}(E_i) \cup \{\gamma : \alpha : \beta_1, \ldots, \beta_n / \gamma \in D,\ \alpha \in E_i,\ \neg\beta_j \notin E \text{ for each } j\}.$$

Then $E$ is an extension exactly when $E = \bigcup_i E_i$. The candidate $E$ appears on the right side, so this is a test of a guess, not a way to build $E$ from nothing.

**Generating defaults.** If $E$ is an extension, then $E = \mathrm{Th}(W \cup \mathrm{cons}(G))$, where $G$ is the set of the defaults whose prerequisite is in $E$ and whose justifications are all consistent with $E$. So a finite theory has at most $2^{|D|}$ extensions, and each is found by trying the subsets of $D$:

```pseudo id=main
EXTENSIONS(W, D)
L1  found ← ∅
L2  for each subset S of D do
L3      E ← Th(W ∪ cons(S))                      ▷ the candidate
L4      G ← ∅
L5      repeat                                    ▷ the least G that E allows
L6          G' ← {d ∈ D : pre(d) ∈ Th(W ∪ cons(G)) and ¬β ∉ E for each justification β of d}
L7          if G' = G then leave the loop
L8          G ← G'
L9      if Th(W ∪ cons(G)) = E then add E to found          ▷ Γ(E) = E
L10 return found
```

Lines L4 to L8 compute $\Gamma(E)$ as $\mathrm{Th}(W \cup \mathrm{cons}(G))$. The sets $G$ grow, so the loop stops after at most $|D|$ rounds. The implementation keeps each theory as its set of models over the atoms, so a membership test $\varphi \in \mathrm{Th}(X)$ is a check that every model of $X$ satisfies $\varphi$. This takes time exponential in both $|D|$ and the number of atoms. That is expected: deciding whether an extension exists is $\Sigma_2^p$-complete for finite propositional theories (Gottlob 1992), as the page on [the complexity of default logic](/default-logic-complexity/) shows.

**Normal defaults.** A default is *normal* if it has the form $\alpha : \gamma / \gamma$. Reiter (1980, Section 3) proved three facts about theories whose defaults are all normal. Every such theory has an extension. Adding a normal default keeps each old extension inside some new one (semi-monotonicity). Two different extensions contradict each other (orthogonality).

## Examples and non-examples

- **Tweety.** $W = \{\mathit{bird}\}$ and $D = \{\mathit{bird} : \mathit{flies} / \mathit{flies}\}$. The only extension is $\mathrm{Th}(\{\mathit{bird}, \mathit{flies}\})$. If $W$ also contains $\neg\mathit{flies}$, the justification fails, and the only extension is $\mathrm{Th}(W)$.
- **Nixon diamond, two extensions.** $W = \{q, r\}$ (a Quaker and a Republican) and $D = \{q : p / p,\ r : \neg p / \neg p\}$. Each default blocks the other. $\mathrm{Th}(\{q, r, p\})$ and $\mathrm{Th}(\{q, r, \neg p\})$ are extensions. A credulous reasoner may believe either $p$ or $\neg p$. A skeptical reasoner believes only what is in both, and so neither.
- **Non-example: the facts alone.** For the Nixon diamond, $E = \mathrm{Th}(\{q, r\})$ is not an extension. Both $p$ and $\neg p$ are consistent with $E$, so $\Gamma(E)$ contains both and is inconsistent, which is not $E$.
- **No extension.** $W = \emptyset$ and $D = \{\top : \neg a / a\}$. If $a \in E$, the justification $\neg a$ fails and $\Gamma(E) = \mathrm{Th}(\emptyset)$, which does not contain $a$. If $a \notin E$, the default applies and $a \in \Gamma(E)$. In both cases $\Gamma(E) \neq E$. The default is not normal, so this does not contradict Reiter's existence theorem.
- **Non-example: an ungrounded belief.** $W = \emptyset$ and $D = \{a : a / a\}$. The set $\mathrm{Th}(\{a\})$ is not an extension, because the prerequisite $a$ is not derivable from $W$ without already having $a$, so $\Gamma(\mathrm{Th}(\{a\})) = \mathrm{Th}(\emptyset)$. The only extension is $\mathrm{Th}(\emptyset)$. In [autoepistemic logic](/autoepistemic-logic/) the similar premise $La \supset a$ has the expansion that contains $a$.
- **Inconsistent facts.** If $W$ is inconsistent, $\Gamma(E)$ always contains all formulas, so the set of all formulas is the unique extension.
- **Cumulativity fails.** Makinson's example, reported by Kraus, Lehmann and Magidor (1990, Section 3.1), uses two normal defaults $\top : a / a$ and $a \vee b : \neg a / \neg a$. With $W = \emptyset$ the only extension is $\mathrm{Th}(\{a\})$, so $a$ and $a \vee b$ are both skeptical consequences. Add the consequence $a \vee b$ to $W$. Now $\mathrm{Th}(\{\neg a, b\})$ is a second extension, because the second default applies before the first, so $a$ is no longer a skeptical consequence. Adding a conclusion that you already believed changed your beliefs, so skeptical default logic fails Cautious Monotonicity, one of the rules of [System P](/system-p/).

## Related definitions

- [Default logic](/default-logic/) is the logic in which extensions are the semantics, with credulous and skeptical consequence defined from them.
- [The complexity of default logic](/default-logic-complexity/) gives the exact complexity of existence, credulous and skeptical reasoning for finite propositional theories.
- A *stable expansion* in [autoepistemic logic](/autoepistemic-logic/) is the corresponding fixed point for a modal belief operator.
- A [stable model](/stable-model-semantics/) of a normal logic program is an extension in disguise: the rule $p \leftarrow q, \mathit{not}\ r$ reads as the default $q : \neg r / p$, and the [Gelfond-Lifschitz reduct](/gelfond-lifschitz-reduct/) plays the role of $\Gamma$.
- $\Gamma$ is antimonotone: a larger $S$ blocks more defaults and gives a smaller $\Gamma(S)$. So the [Knaster-Tarski theorem](/knaster-tarski-theorem/) does not apply, which is why a fixed point may fail to exist. $\Gamma \circ \Gamma$ is monotone, and its least and greatest fixed points give the well-founded semantics of default logic, in the same way as the [alternating fixpoint](/alternating-fixpoint/) does for programs.
- [Nonmonotonic reasoning](/nonmonotonic-reasoning/) places extensions among the other ways of drawing defeasible conclusions.

## References
