---
tag: QDYQHJ
kind: algorithm
slug: unit-production-elimination
name: Unit-production elimination
aliases:
- chain rule removal
area: automata-and-parsing/context-free-parsing
level: core
summary: Removes productions of the form A→B by substituting the right sides of B.
solves: [cfg-normal-form-conversion]
model: word-ram
complexity:
  vars: {G: the grammar size, V: the number of nonterminals}
  time: {worst: O(V G), best: O(G)}
  space: {extra: O(V G)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1961
  people: [Yehoshua Bar-Hillel, Micha Perles, Eli Shamir]
  note: Bar-Hillel, Perles and Shamir showed in 1961 that the unit productions of a context-free grammar can be removed without changing its language, as part of their normal-form results.
prereqs: [context-free-grammar, derivation, transitive-closure]
see_also: [epsilon-production-elimination, useless-symbol-elimination, chomsky-normal-form-conversion, chomsky-normal-form, cfg-normal-form-conversion, cyk-algorithm, greibach-normal-form-conversion, strongly-connected-components]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 7.1.4, Eliminating Unit Productions (unit pairs, and the expression grammar as the example)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 4.2.3, Transforming a CF Grammar into Chomsky Normal Form (the removal of unit rules)
  - paper: "Martin Lange and Hans Leiß, To CNF or not to CNF? An efficient yet presentable version of the CYK algorithm, Informatica Didactica 8 (2009)"
    locator: Section 2 (the quadratic growth caused by unit productions, and a CYK variant that keeps them)
  - paper: "Yehoshua Bar-Hillel, Micha Perles and Eli Shamir, On formal properties of simple phrase structure grammars, Zeitschrift für Phonetik, Sprachwissenschaft und Kommunikationsforschung 14 (1961)"
    locator: pp. 143 to 172
---

Unit-production elimination turns a [context-free grammar](/context-free-grammar/) into an equivalent one with no production of the form $A \to B$, where $B$ is a single nonterminal. For every nonterminal $A$ it finds the nonterminals $B$ that $A$ can become by unit productions alone, the unit pairs, and gives $A$ a copy of every production $B \to \alpha$ that is not a unit production. The unit pairs are the reflexive [transitive closure](/transitive-closure/) of the unit productions, so cycles such as $A \to B$, $B \to A$ need no special care. It is a step of the [Chomsky normal form conversion](/chomsky-normal-form-conversion/), after [epsilon-production elimination](/epsilon-production-elimination/) and before [useless symbol elimination](/useless-symbol-elimination/). The output can be quadratic in the size of the input.

## In plain words

A rule that says only "this placeholder may be that other placeholder" does no real work: it renames. Such renaming rules can form long chains, such as "an expression may be a term, a term may be a factor", and even loops.

To remove them, take each placeholder in turn. Follow every chain of renaming rules from it and collect all the placeholders it can turn into, itself included. Then give it a copy of every real rule of every placeholder in that collection. Finally, drop all the renaming rules.

The new grammar produces the same sentences. Each chain of renamings in an old derivation is replaced by a single step with a copied rule. The grammar can grow, because one rule can be copied to many placeholders.

## The problem

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size, here $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$.

Let $G = (V, \Sigma, P, S)$. A **unit production** is a production $A \to B$ with $B \in V$; a production $A \to a$ with $a \in \Sigma$ is not one. A pair $(A, B)$ of nonterminals is a **unit pair** if $A \Rightarrow^* B$ using unit productions only; every $(A, A)$ is a unit pair, by the derivation with no step.

The output is a grammar $G' = (V, \Sigma, P', S)$ with no unit production and $L_{G'}(A) = L_G(A)$ for every nonterminal $A$, in particular $L(G') = L(G)$. The input may have empty productions and cycles of unit productions.

## The algorithm

```pseudo id=main
ELIMINATE-UNITS(G = (V, Σ, P, S))
L1  P′ ← ∅
L2  for each nonterminal A ∈ V do
L3      U ← {A}; W ← [A]                     ▷ U becomes the set of B with (A, B) a unit pair
L4      while W is not empty do
L5          B ← pop(W); for each unit production B → C in P with C ∉ U do add C to U and push C on W
L6      for each B ∈ U and each production B → α in P that is not a unit production do add A → α to P′
L7  return (V, Σ, P′, S)
```

**Lines L3 to L5.** This is a [graph search](/graph-reachability/) from $A$ in the unit graph, which has an edge $B \to C$ for each unit production $B \to C$. A cycle of unit productions is a cycle of this graph, and the search visits each vertex once, so it ends.

**Line L6.** "Add" ignores duplicates: if $A$ reaches $D$ by two chains, the productions of $D$ are copied once. The unit productions themselves are never copied, so $P'$ has none.

**Order with the other steps.** Epsilon-production elimination creates unit productions, such as $S \to A$ from $S \to A B$ with $B$ nullable, so it must run first. Unit-production elimination copies right sides, so it copies $B \to \varepsilon$ to $A$ when $A \Rightarrow^* B$: it creates empty productions only if the input has some. Afterwards some nonterminals may be unreachable, such as $A$ after $S \to A$, $A \to a$ becomes $S \to a$, $A \to a$, which is why useless symbols are removed last.

## Example

The expression grammar, of size 18,

$$E \to E + T \mid T, \qquad T \to T * F \mid F, \qquad F \to ( E ) \mid a,$$

has the unit productions $E \to T$ and $T \to F$. The searches of lines L3 to L5 give the unit pairs

| $A$ | $U$ |
|---|---|
| $E$ | $E, T, F$ |
| $T$ | $T, F$ |
| $F$ | $F$ |

and line L6 copies the productions that are not unit productions:

$$E \to E + T \mid T * F \mid ( E ) \mid a, \qquad T \to T * F \mid ( E ) \mid a, \qquad F \to ( E ) \mid a.$$

The result has 9 productions and size 30. The sentence $a * a$ had the parse tree with the chain $E \Rightarrow T \Rightarrow T * F \Rightarrow F * F \Rightarrow a * F \Rightarrow a * a$; in the new grammar it is $E \Rightarrow T * F \Rightarrow a * F \Rightarrow a * a$, where $E \to T * F$ replaces the step $E \Rightarrow T$ followed by $T \to T * F$, and $T \to a$ replaces $T \Rightarrow F \Rightarrow a$.

**A cycle.** For $S \to A \mid a\,b$, $A \to B \mid a$, $B \to S \mid b$, the unit graph is the cycle $S \to A \to B \to S$, so each of $S$, $A$, $B$ has all three in its unit pairs and gets the three productions $\to a\,b \mid a \mid b$: 9 productions in all. Then $A$ and $B$ are unreachable, and useless symbol elimination leaves $S \to a\,b \mid a \mid b$.

Both results were computed by the implementation.

## Correctness

**Claim.** For every nonterminal $A$ and every $w \in \Sigma^*$, $A \Rightarrow^*_G w$ if and only if $A \Rightarrow^*_{G'} w$.

*Unit pairs.* After lines L3 to L5, $U$ is the set of $B$ with $(A, B)$ a unit pair: the search adds $C$ only along a unit production from an element of $U$, and it adds every unit successor of every element it pops.

*If.* A production $A \to \alpha$ of $P'$ comes from a unit pair $(A, B)$ and $B \to \alpha \in P$, so $A \Rightarrow^*_G B \Rightarrow_G \alpha$. Replacing each step of a derivation in $G'$ by these steps gives a derivation in $G$.

*Only if.* Take a parse tree of $w$ from $A$ in $G$. Cut it into maximal chains of nodes linked by unit productions: a chain starts at a node $X_0$ whose production is a unit production, follows $X_0 \to X_1 \to \cdots \to X_m$ by unit productions, and ends at $X_m$, whose production $X_m \to \alpha$ is not a unit production. Then $(X_0, X_m)$ is a unit pair and $X_0 \to \alpha \in P'$, so the chain can be replaced by one node with this production. Every leaf of the tree is a terminal, so every chain ends at a non-unit production; doing this for every chain gives a parse tree of $w$ from $A$ in $G'$. The proof by induction on derivations is in [the correctness proof](proofs/correctness.md).

## Complexity

**Time.** Let $u$ be the number of unit productions. One search of lines L3 to L5 visits each nonterminal and each unit production at most once, in $O(|V| + u)$ time. Line L6 writes at most the total size of the non-unit productions, $O(|G|)$. Over all $|V|$ nonterminals, the time is $O(|V| (|V| + |G|))$, which is $O(|V| \cdot |G|)$ when every nonterminal occurs in some production. With no unit production, every $U$ is a single nonterminal and the total is $O(|G|)$.

**Output size.** $|G'| \le |V| \cdot |G|$, and the bound is reached up to a constant: for the chain $A_i \to A_{i+1} \mid t_i$ for $i < k$ and $A_k \to t_k$, with $k$ nonterminals and size $4k - 2$, the nonterminal $A_i$ gets the $k - i + 1$ productions $A_i \to t_i \mid \cdots \mid t_k$, for $k(k+1)/2$ productions in total. For $k = 300$ this is $45150$ productions, as the tests check.

**Space.** The output dominates, $O(|V| \cdot |G|)$, and the search needs $O(|V|)$ for $U$ and $W$.

## Properties

- **Language preserving, for every nonterminal.** Each nonterminal keeps its own language, not only $S$. This is why the step can run before other transformations that use the languages of nonterminals.
- **Fewer parse trees.** Collapsing the unit chains maps the trees of $G$ onto the trees of $G'$, so a sentence has at most as many trees in $G'$ as in $G$. A cycle of unit productions gives some sentences infinitely many trees; afterwards the number is finite. $S \to S \mid a$ has infinitely many trees for $a$, and the result $S \to a$ has one.
- **Removes the cycles.** A grammar is called cycle-free if no $A \Rightarrow^+ A$; after epsilon-production and unit-production elimination, every grammar is cycle-free, which many normal-form proofs and parsing algorithms assume.
- **No new nonterminals.** The set $V$ is unchanged.

## Variants and improvements

- **Strongly connected components.** Nonterminals in the same [strongly connected component](/strongly-connected-components/) of the unit graph have the same unit pairs. Computing the components and the closure on the condensation shares the work among them, but the output keeps its size.
- **Merge renaming cycles first.** All nonterminals of one unit cycle generate the same language, so they can be replaced by one nonterminal. This shrinks the grammar before the copies, and is a common cleaning step.
- **Keep the unit productions.** Lange and Leiß keep unit productions and let [CYK](/cyk-algorithm/) close each cell under the inverse unit relation, which avoids the quadratic growth of the grammar while keeping the cubic parsing time.
- **Parsers that accept them.** LR, LL and [Earley](/earley-parser/) parsers handle unit productions directly, and parse trees then keep the levels of the original grammar. Unit reductions can also be removed from an LR table to save moves, which changes the trees but not the language.

## When to use it

Use it when a normal form is needed: [Chomsky normal form](/chomsky-normal-form/) for CYK and for proofs, and [Greibach normal form](/greibach-normal-form-conversion/). Run [epsilon-production elimination](/epsilon-production-elimination/) first and [useless symbol elimination](/useless-symbol-elimination/) after. Do not use it to prepare a grammar for a parser that handles unit productions: the grammar grows, and the parse trees lose the levels, such as term and factor, that later phases use.

## Pitfalls

- **Wrong order with epsilon elimination.** If unit productions are removed first, epsilon elimination creates new ones. Remove $\varepsilon$-productions first.
- **Only one level of renaming.** Replacing $A \to B$ by the productions of $B$, once, keeps $A \to C$ when $B \to C$ is a unit production. Copy along the whole closure, or repeat until no unit production is left.
- **Naive substitution on cycles.** Substituting unit productions one by one until none is left loops forever on $A \to B$, $B \to A$ unless the substitution skips $A \to A$ and remembers what was already done. The closure handles cycles at once.
- **Copying the unit productions themselves.** Line L6 copies only the non-unit productions; copying a unit production $B \to C$ to $A$ would leave $A \to C$ in the output.
- **Terminals on their own.** $A \to a$ is not a unit production and must stay.
- **Recursion.** A recursive closure search overflows the stack on long chains. Use a worklist.
- **Size.** The quadratic growth matters for large grammars; consider keeping the unit productions and adapting the parser.

## Implementations

## History

Bar-Hillel, Perles and Shamir proved in 1961 that unit productions and empty productions can be removed from a context-free grammar, among the normal-form results of their paper. The formulation by unit pairs, with the expression grammar as the example, is the one of Hopcroft, Motwani and Ullman. Lange and Leiß showed in 2009 that the unit step is the source of the quadratic size of the Chomsky normal form and that CYK can keep the unit productions instead.

## References
