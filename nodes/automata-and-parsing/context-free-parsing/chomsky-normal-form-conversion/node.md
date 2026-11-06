---
tag: P1WQJZ
kind: algorithm
slug: chomsky-normal-form-conversion
name: Chomsky normal form conversion
aliases:
- CNF conversion
area: automata-and-parsing/context-free-parsing
level: core
summary: Transforms any context-free grammar into an equivalent grammar in Chomsky normal form.
solves: [cfg-normal-form-conversion]
model: word-ram
complexity:
  vars: {g: the grammar size}
  time: {worst: O(g^2)}
  space: {extra: O(g^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 1959
  people: [Noam Chomsky]
  note: Chomsky showed that every context-free grammar has an equivalent grammar with rules A → BC and A → a; the order of steps that keeps the output quadratic is the one analysed by Hopcroft, Motwani and Ullman.
prereqs: [chomsky-normal-form, nullable-symbol, epsilon-production-elimination, unit-production-elimination, useless-symbol-elimination]
see_also: [cfg-normal-form-conversion, greibach-normal-form-conversion, cyk-algorithm, cfg-membership-problem, cfl-pumping-lemma, inside-outside-algorithm, valiant-algorithm, probabilistic-context-free-grammar]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 7.1, Normal Forms for Context-Free Grammars (7.1.3 Eliminating ε-Productions, 7.1.4 Eliminating Unit Productions, 7.1.5 Chomsky Normal Form), and Section 7.4.2, Running Time of Conversion to Chomsky Normal Form
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 2.1, Chomsky Normal Form (Theorem 2.9, its proof, and Example 2.10)
  - paper: doi:10.1016/S0019-9958(59)90362-6
    title: Noam Chomsky, On certain formal properties of grammars, Information and Control 2(2) (1959)
    locator: pp. 137 to 167
---

Chomsky normal form conversion turns any [context-free grammar](/context-free-grammar/) $G$ into a grammar in [Chomsky normal form](/chomsky-normal-form/), with only productions $A \to BC$ and $A \to a$, plus $S_0 \to \varepsilon$ when the empty string is in the language. It runs five rewriting steps, START, TERM, BIN, DEL and UNIT, and then removes useless symbols. In this order the output has size $O(|G|^2)$ and is computed in $O(|G|^2)$ time; removing the $\varepsilon$-productions before splitting the long right sides can make it exponential.

## In plain words

The goal is a grammar where every rule turns one symbol into exactly two symbols, or into one letter. The conversion fixes the rules that break this, one kind at a time.

First it adds a new start symbol, so that the start never appears inside a rule. Then it gives each letter that appears in a long rule its own symbol. Then it cuts every long rule into a chain of rules with two symbols each.

Next it removes the rules that produce nothing. Wherever a symbol that can vanish appears in a rule, it adds a copy of the rule without that symbol. Last, it removes the rules that only rename one symbol to another, by giving the first symbol copies of all the rules of the second. Symbols that can no longer be used are dropped.

## The problem

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $S$ is the start symbol, and $|G|$, written $g$ in the front matter, is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$. A *unit production* is $A \to B$ with $B \in V$. A nonterminal $A$ is [nullable](/nullable-symbol/) if $A \Rightarrow^* \varepsilon$.

**Input.** A context-free grammar $G = (V, \Sigma, R, S)$ with $V \cap \Sigma = \emptyset$.

**Output.** A grammar $G' = (V', \Sigma, R', S_0)$ in Chomsky normal form with $L(G') = L(G)$: every production is $A \to BC$ with $B, C \in V' \setminus \{S_0\}$, or $A \to a$ with $a \in \Sigma$, or $S_0 \to \varepsilon$, and $S_0 \to \varepsilon \in R'$ exactly when $\varepsilon \in L(G)$.

## The algorithm

```pseudo id=main
CNF-CONVERT(G)
L1  add a new start symbol S0 and the production S0 → S                          ▷ START
L2  for each production A → X1 ⋯ Xk with k ≥ 2 do                               ▷ TERM
L3      replace each terminal a among the Xi by a new nonterminal Ta, with Ta → a added once per a
L4  for each production A → X1 ⋯ Xk with k ≥ 3 do                               ▷ BIN
L5      replace it by A → X1 A1, A1 → X2 A2, …, A(k−2) → X(k−1) Xk with new A1, …, A(k−2)
L6  N ← the set of nullable nonterminals                                         ▷ DEL
L7  for each production A → X Y do add A → X if Y ∈ N, and A → Y if X ∈ N
L8  remove every production A → ε, and add S0 → ε if S0 ∈ N
L9  for each nonterminal A do U(A) ← {B : A ⇒* B by unit productions}           ▷ UNIT
L10     for each B ∈ U(A) and each production B → β that is not a unit production do add A → β
L11 remove all unit productions, then the nonterminals that derive no terminal string, then those not reachable from S0
L12 return the grammar with start symbol S0
```

Each step keeps the language and removes one kind of bad production without creating an earlier kind again:

- **START** (L1) makes sure the start symbol is on no right side, so that $S_0 \to \varepsilon$ is allowed at the end.
- **TERM** (L2, L3) leaves terminals only in right sides of length 1.
- **BIN** (L4, L5) leaves right sides of length at most 2. It does not add terminals to long right sides.
- **DEL** (L6 to L8) removes $\varepsilon$-productions. Since every right side now has length at most 2, each production has at most 3 versions, one with each nullable symbol left out. The only new productions are unit productions $A \to X$ and productions $A \to a$, which are allowed. This is [$\varepsilon$-production elimination](/epsilon-production-elimination/).
- **UNIT** (L9, L10) removes unit productions by copying. This is [unit production elimination](/unit-production-elimination/). It copies only productions $A \to BC$ and $A \to a$, so no new $\varepsilon$-production or unit production appears.
- **USELESS** (L11) removes the [useless symbols](/useless-symbol-elimination/), first the nonterminals that are not generating, then the ones that are not reachable. It removes whole productions, so the form is kept.

## Example

Take the grammar
$$S \to A S A \mid a B, \qquad A \to B \mid S, \qquad B \to b \mid \varepsilon,$$
of size 14, which Sipser also uses as an example. The steps, as computed by the implementation:

| step | productions | size |
|---|---|---|
| START | $S_0 \to S$, plus the 6 productions of $G$ | 16 |
| TERM | $S \to a B$ becomes $S \to T_a B$; add $T_a \to a$ | 18 |
| BIN | $S \to A S A$ becomes $S \to A S_1$ and $S_1 \to S A$ | 20 |
| DEL | $N = \{A, B\}$; add $S \to S_1$ (drop $A$), $S_1 \to S$ (drop $A$), $S \to T_a$ (drop $B$); remove $B \to \varepsilon$ | 25 |
| UNIT | replace the 6 unit productions by copies | 50 |
| USELESS | nothing to remove | 50 |

$S_0$ is not nullable, since $S$ is not: every production of $S$ contains $S$ or the terminal $a$. In the UNIT step the unit closures are $U(S_0) = \{S_0, S, S_1, T_a\}$, $U(S) = \{S, S_1, T_a\}$, $U(S_1) = \{S_1, S, T_a\}$ and $U(A) = \{A, B, S, S_1, T_a\}$. The result has 19 productions:
$$\begin{aligned}
S_0 &\to A S_1 \mid T_a B \mid S A \mid a, &\qquad S &\to A S_1 \mid T_a B \mid S A \mid a,\\
S_1 &\to S A \mid A S_1 \mid T_a B \mid a, &\qquad A &\to A S_1 \mid T_a B \mid S A \mid a \mid b,\\
B &\to b, &\qquad T_a &\to a.
\end{aligned}$$
The tests check that it generates the same strings as $G$ up to length 7, with the [CYK algorithm](/cyk-algorithm/) on the output and a general fixpoint recognizer on $G$.

For $S \to a S b \mid \varepsilon$ the output is $S_0 \to \varepsilon \mid T_a S_1$, $S \to T_a S_1$, $S_1 \to S T_b \mid b$, $T_a \to a$, $T_b \to b$, of size 16. Here $S$ is nullable, so DEL adds $S_1 \to T_b$ and $S_0 \to \varepsilon$, and UNIT turns $S_1 \to T_b$ into $S_1 \to b$.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). It shows for each step that the language is unchanged and which shapes of productions remain.

- START and TERM add nonterminals that derive exactly $S$ and exactly $a$, so substituting back gives the old derivations.
- BIN: the chain $A_1, \ldots, A_{k-2}$ is used only in that chain, so $A \Rightarrow^* X_1 \cdots X_k$ in the new grammar exactly when $A \to X_1 \cdots X_k$ was a production.
- DEL: for every nonterminal $A$ and every nonempty $w$, $A \Rightarrow^* w$ before the step exactly when $A \Rightarrow^* w$ after it. This is an induction on derivation length in both directions: a parse tree before the step loses its subtrees with empty yield, and each node that lost a child uses one of the new shortened productions. $S_0 \to \varepsilon$ restores the empty string.
- UNIT: a derivation after the step expands each copied $A \to \beta$ into $A \Rightarrow^* B \Rightarrow \beta$ before it, and a leftmost derivation before the step groups each maximal run of unit steps $A \Rightarrow B_1 \Rightarrow \cdots \Rightarrow B$ followed by $B \to \beta$ into one copied production.
- USELESS: a parse tree from $S_0$ uses only nonterminals that are reachable and generating.

## Complexity

Let $m = |G|$.

- **START, TERM, BIN** take $O(m)$ time. A right side of length $k \ge 3$ becomes $k - 1$ productions of size 3, so after BIN the numbers of productions and nonterminals and the size are all $O(m)$.
- **DEL.** The nullable set is computed in linear time by a worklist with a counter per production: the counter of a production is the number of symbols of its right side that are not yet known to be nullable. Each production then gets at most 3 versions, so the size stays $O(m)$.
- **UNIT.** For each of the $O(m)$ nonterminals, a search in the graph of unit productions finds $U(A)$ in $O(m)$ time, and $A$ receives at most one copy of each of the $O(m)$ non-unit productions. So UNIT takes $O(m^2)$ time and the output has $O(m^2)$ productions, each of size at most 3.
- **USELESS** is linear in the size of its input, $O(m^2)$.

In total $O(|G|^2)$ time and space. The bound is tight: a chain $A_1 \to A_2 \to \cdots \to A_k$ of unit productions with $k$ binary productions on $A_k$, where all $A_i$ are used, gives every $A_i$ all $k$ binary productions, $k^2$ in total, from a grammar of size $O(k)$. The tests check this for $k = 30$.

**The order matters.** If DEL runs before BIN, a production $S \to A_1 \cdots A_k$ with all $A_i$ nullable gets one version for each nonempty subset of the $A_i$, $2^k - 1$ productions. With BIN first, the grammars $S \to A_1 \cdots A_k$, $A_i \to a \mid \varepsilon$ of size $4k + 1$ give outputs of size 10, 33, 68 and 115 for $k = 2, 4, 6, 8$.

## Properties

- **Language preserving, including $\varepsilon$.** $L(G') = L(G)$ exactly, with $S_0 \to \varepsilon$ as the only $\varepsilon$-production.
- **Deterministic and iterative.** Every step is a fixed rewriting with fixpoints computed by worklists; no recursion is needed, so large grammars are safe.
- **Parse trees map back.** Every parse tree of $G'$ maps to a parse tree of $G$ for the same string, by undoing TERM and BIN and putting back the removed unit chains and empty subtrees. So the conversion keeps the structure that semantic actions need, though not one to one: a string can have fewer trees in $G'$ than in $G$, for example when $G$ has a cycle $A \Rightarrow^+ A$ and so infinitely many trees.
- **Ambiguity.** If $G$ is unambiguous, so is $G'$: a tree of $G'$ is recovered from the tree of $G$ it maps to, by deleting the subtrees with empty yield, contracting the unit chains and redoing TERM and BIN, so two different trees of $G'$ for $w$ map to two different trees of $G$.
- **Not minimal.** The output is often much larger than necessary. In the example, $S_0$, $S$ and $S_1$ end up with the same four productions.

## Variants and improvements

- **Sipser's order.** Sipser's proof runs START, then DEL, then UNIT, then splits long rules and replaces terminals. It is simpler to state, and correct, but DEL on long right sides makes it exponential in the worst case.
- **Binary normal form only.** Many parsers need only right sides of length at most 2. START, TERM and BIN alone give such a grammar in $O(|G|)$ time and size. [CYK](/cyk-algorithm/) can then handle unit and $\varepsilon$-productions with a precomputed unit relation and nullable set, which avoids the square.
- **Keeping the trees.** Tools for natural language processing binarize treebank grammars with a binarization that records the original rule in each new nonterminal, so that parse trees can be turned back into trees of the original grammar after parsing.
- **Greibach normal form.** A further conversion from Chomsky normal form gives [Greibach normal form](/greibach-normal-form-conversion/).
- **Probabilities.** For a [probabilistic grammar](/probabilistic-context-free-grammar/), DEL and UNIT must move probability mass: the weight of a removed $\varepsilon$-subtree or unit chain is multiplied into the new productions, and unit cycles need the solution of a linear system instead of a closure.

## When to use it

Use it before an algorithm that needs binary productions without $\varepsilon$ or units: [CYK](/cyk-algorithm/), [Valiant's algorithm](/valiant-algorithm/), the [inside-outside algorithm](/inside-outside-algorithm/), or a proof such as the [pumping lemma](/cfl-pumping-lemma/). For a parser of a programming language, use a deterministic method on the original grammar instead, since the conversion changes the trees and grows the grammar. If only right sides of length 2 are needed, use binarization alone.

## Pitfalls

- **DEL before BIN.** The textbook order START, DEL, UNIT, BIN, TERM is correct but exponential on long right sides of nullable symbols. Split first.
- **Forgetting START.** If $S$ is nullable and appears on a right side, $S \to \varepsilon$ is not allowed in Chomsky normal form. Adding $S_0 \to S$ first solves this; without it the conversion must drop $\varepsilon$ from the language.
- **UNIT before DEL.** DEL creates new unit productions, such as $S \to S_1$ in the example. Removing unit productions first leaves these behind.
- **Unit cycles.** $A \to B$, $B \to A$ makes a naive "substitute until no unit productions remain" loop forever. Computing the closure $U(A)$ by a graph search handles cycles.
- **Useless removal order.** Remove nonterminals that are not generating first, then those that are not reachable; the other order can leave unreachable symbols.
- **Name clashes.** New nonterminals must not collide with existing symbols. The implementation picks fresh names that are not used anywhere in $G$.
- **Empty language.** If $S$ derives no terminal string, the output has no productions. Code that assumes a production for $S_0$ fails.

## Implementations

## History

Chomsky introduced the form in 1959 and showed that every context-free grammar has an equivalent grammar of this kind. The steps of the conversion are those of the textbooks: Hopcroft, Motwani and Ullman eliminate $\varepsilon$-productions, unit productions and useless symbols, then fix long right sides and terminals, and analyse in Section 7.4.2 how to keep the running time quadratic by splitting right sides before removing $\varepsilon$-productions. Sipser presents the version with START first.

## References
