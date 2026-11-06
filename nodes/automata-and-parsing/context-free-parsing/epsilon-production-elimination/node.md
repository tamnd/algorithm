---
tag: YT0RZM
kind: algorithm
slug: epsilon-production-elimination
name: Epsilon-production elimination
aliases:
- null production removal
area: automata-and-parsing/context-free-parsing
level: core
summary: Removes ε-productions from a grammar while preserving the language minus the empty string.
solves: [cfg-normal-form-conversion]
model: word-ram
complexity:
  vars: {G: the grammar size, r: the largest number of nullable symbols in one right side}
  time: {worst: O(2^r G), best: O(G)}
  space: {extra: O(2^r G)}
properties: {deterministic: true, recursive: false}
history:
  year: 1961
  people: [Yehoshua Bar-Hillel, Micha Perles, Eli Shamir]
  note: Bar-Hillel, Perles and Shamir showed in 1961 that the empty productions of a context-free grammar can be removed without changing the nonempty strings of its language.
prereqs: [context-free-grammar, nullable-symbol, derivation]
see_also: [unit-production-elimination, useless-symbol-elimination, chomsky-normal-form-conversion, chomsky-normal-form, greibach-normal-form-conversion, cfg-normal-form-conversion, earley-parser]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 7.1.3, Eliminating epsilon-Productions
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 4.2.3, Transforming a CF Grammar into Chomsky Normal Form (the removal of epsilon-rules)
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 21, Normal Forms
  - paper: "Yehoshua Bar-Hillel, Micha Perles and Eli Shamir, On formal properties of simple phrase structure grammars, Zeitschrift für Phonetik, Sprachwissenschaft und Kommunikationsforschung 14 (1961)"
    locator: pp. 143 to 172
  - paper: "Martin Lange and Hans Leiß, To CNF or not to CNF? An efficient yet presentable version of the CYK algorithm, Informatica Didactica 8 (2009)"
    locator: Section 2 (the size of the grammar under each order of the normal-form steps)
---

Epsilon-production elimination turns a [context-free grammar](/context-free-grammar/) into one with no production $A \to \varepsilon$ that generates the same nonempty strings. It first finds the [nullable](/nullable-symbol/) nonterminals, then replaces each production by all its versions with some nullable symbols left out. It is a step of the conversion to [Chomsky normal form](/chomsky-normal-form-conversion/) and to [Greibach normal form](/greibach-normal-form-conversion/), and it can blow the grammar up exponentially unless right sides are short.

## In plain words

Some rules let a placeholder produce nothing. Such rules are awkward for many parsers and proofs, so we want to remove them without changing what the grammar produces.

First find every placeholder that can vanish, directly or through other placeholders that can vanish. Then look at each rule. Wherever a placeholder in the rule can vanish, make one copy of the rule that keeps it and one copy that leaves it out. Do this for every combination. Then throw away the rules that produce nothing.

The new grammar produces every nonempty sentence of the old one, and nothing else. If the old grammar could also produce the empty sentence, a new start placeholder with one empty rule keeps it.

## The problem

The input is a grammar $G = (V, \Sigma, P, S)$ in the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, and $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$ the grammar size. A nonterminal $A$ is **nullable** when $A \Rightarrow^* \varepsilon$.

The output is a grammar $G'$ with no production $A \to \varepsilon$ and $L(G') = L(G) \setminus \{\varepsilon\}$. In the variant that keeps the empty string, when $\varepsilon \in L(G)$ the output gets a fresh start symbol $S'$, on no right side, with the productions $S' \to S \mid \varepsilon$, so that $L(G') = L(G)$ and $S' \to \varepsilon$ is the only empty production.

## The algorithm

```pseudo id=main
ELIMINATE-EPSILON(G, keep_empty)
L1  N ← { A ∈ V : A ⇒* ε }                   ▷ nullable nonterminals, by a worklist
L2  P′ ← ∅
L3  for each production A → X1 X2 … Xk in P do
L4      for each choice, for every i with Xi ∈ N, of keeping or dropping Xi do
L5          α′ ← the kept symbols, in their order
L6          if α′ ≠ ε then add A → α′ to P′
L7  if keep_empty and S ∈ N then add S′ → S | ε with a fresh S′, and return (V ∪ {S′}, Σ, P′, S′)
L8  return (V, Σ, P′, S)
```

**Line L1.** Keep for each production a counter of the symbols of its right side not yet known to be nullable, and for each nonterminal the list of the productions where it occurs. Start the worklist with the left sides of empty productions. When a nonterminal $X$ leaves the worklist, decrease the counter of each production at each occurrence of $X$; when a counter reaches 0, its left side is nullable and joins the worklist if it is new. A terminal is never nullable, so a production with a terminal never reaches 0. Each occurrence of a symbol is handled once, so line L1 takes $O(|G|)$ time.

**Lines L3 to L6.** A production with $m$ nullable symbols on its right side gives $2^m$ choices, and all of them are added except the empty one. Two choices can give the same right side, as with $A \to a A A$, where dropping either $A$ gives $A \to a A$; "add" keeps one copy.

**Cleanup.** A nonterminal whose only productions were empty has no production in $P'$, but may still occur in the new right sides. It derives no string in $G'$, so the productions that mention it are never used; the implementation removes them, and repeats while this leaves another nonterminal without productions. This is a cheap special case of [useless-symbol elimination](/useless-symbol-elimination/).

## Example

Take

$$S \to A B, \qquad A \to a A A \mid \varepsilon, \qquad B \to b B B \mid \varepsilon,$$

whose language is $a^* b^*$, with $|G| = 13$. Line L1 finds $A$ and $B$ nullable from their empty productions, then $S$ from $S \to A B$. Lines L3 to L6 give:

- from $S \to A B$: $S \to A B \mid A \mid B$ (the empty choice is dropped);
- from $A \to a A A$: $A \to a A A \mid a A \mid a$, where the two ways of dropping one $A$ give the same production;
- from $B \to b B B$: $B \to b B B \mid b B \mid b$;
- from $A \to \varepsilon$ and $B \to \varepsilon$: nothing.

Since $S$ is nullable, line L7 adds $S' \to S \mid \varepsilon$. The result has 11 productions and size 28. Without $S'$, it generates $a^* b^* \setminus \{\varepsilon\}$.

## Correctness

**Claim.** For every nonterminal $A$ of $G$ and every nonempty $w \in \Sigma^+$, $A \Rightarrow^*_G w$ if and only if $A \Rightarrow^*_{G'} w$. Since every production of $P'$ has a nonempty right side, every string derived in $G'$ from a nonterminal of $G$ is nonempty, so $L(G') = L(G) \setminus \{\varepsilon\}$. With line L7, $S' \Rightarrow S$ adds the nonempty strings and $S' \to \varepsilon$ adds $\varepsilon$, so $L(G') = L(G)$.

*If.* Each production $A \to \alpha'$ of $P'$ comes from some $A \to \alpha$ of $P$ by dropping nullable symbols, so $A \Rightarrow \alpha \Rightarrow^* \alpha'$ in $G$, by deriving $\varepsilon$ from each dropped symbol. Replacing each step of a $G'$-derivation by these $G$-steps gives a $G$-derivation.

*Only if.* By induction on the length of a $G$-derivation $A \Rightarrow^m w$ with $w \neq \varepsilon$. The first step uses some $A \to X_1 \cdots X_k$, and by the splitting lemma of [derivations](/derivation/), $w = w_1 \cdots w_k$ with $X_i \Rightarrow^{m_i} w_i$ and $m_i < m$. Drop exactly the $X_i$ with $w_i = \varepsilon$; each of them is nullable, and they are not all of the $X_i$, because $w \neq \varepsilon$. So $A \to \alpha'$, with $\alpha'$ the $X_i$ with $w_i \neq \varepsilon$, is in $P'$. Each kept $X_i$ is a terminal equal to $w_i$, or a nonterminal with $X_i \Rightarrow^*_{G'} w_i$ by the induction hypothesis. So $A \Rightarrow_{G'} \alpha' \Rightarrow^*_{G'} w$. The cleanup removes only productions that no derivation of a terminal string uses, so it keeps this. The proofs for line L1 and the cleanup are in [the correctness proof](proofs/correctness.md).

## Complexity

**Time and output size.** Line L1 takes $O(|G|)$ time. A production $A \to \alpha$ with $m$ nullable symbols produces at most $2^m - 1$ new productions of size at most $|\alpha| + 1$ each, in $O(2^m (|\alpha| + 1))$ time. So the time and the size of $G'$ are $O(2^r |G|)$, where $r$ is the largest $m$, and $O(|G|)$ when no right side has a nullable symbol.

**The exponential case is real.** $S \to A_1 A_2 \cdots A_k$ with every $A_i \to a \mid \varepsilon$ gives $2^k - 1$ productions for $S$, of total size $\Theta(k\, 2^k)$, while $|G| = \Theta(k)$.

**Binarize first.** If every right side has length at most 2, a production of size 3 gives at most the three productions $A \to XY \mid X \mid Y$, of total size at most 7, and a production of size 2 gives at most one. So $|G'| \le 3 |G|$, plus 3 for line L7. Splitting long right sides first, with new nonterminals $A \to X_1 \langle X_2 \cdots X_k \rangle$, costs $O(|G|)$ and makes the whole step linear. This is why the order "binarize, eliminate $\varepsilon$, eliminate unit productions" keeps the [Chomsky normal form conversion](/chomsky-normal-form-conversion/) polynomial (Lange and Leiß).

**Space.** The output dominates: $O(2^r |G|)$, and $O(|G|)$ for binarized input.

## Properties

- **Language preserving up to $\varepsilon$.** $L(G') = L(G) \setminus \{\varepsilon\}$, or $L(G)$ with the new start symbol.
- **New unit productions.** Dropping symbols can create unit productions, such as $S \to A$ in the example. So [unit-production elimination](/unit-production-elimination/) must come after this step, not before.
- **Parse trees change.** A tree of $G'$ corresponds to a tree of $G$ in which some subtrees for $\varepsilon$ are cut away. Several trees of $G$ can map to one tree of $G'$, so the number of parse trees of a string can change.
- **No new left recursion is hidden.** Left recursion through a nullable prefix, as in $A \to B A c$ with $B$ nullable, becomes the direct left recursion $A \to A c$, which makes it visible to [left-recursion elimination](/left-recursion-elimination/).

## Variants and improvements

- **Without the empty string.** With keep_empty false, the output generates $L(G) \setminus \{\varepsilon\}$, which is the form used in most textbook proofs.
- **Binarize first.** As above, this keeps the output linear in $|G|$.
- **Keep $\varepsilon$ and adapt the parser.** The [Earley parser](/earley-parser/) handles nullable symbols with the rule of Aycock and Horspool, and LR and LL parsers handle them through [FIRST and FOLLOW sets](/first-and-follow-sets/), so parsers often keep the empty productions to keep the trees close to the grammar.
- **Nullable sets with other data.** The same worklist computes FIRST sets and the generating symbols of [useless-symbol elimination](/useless-symbol-elimination/).

## When to use it

Use it when a normal form is needed: for [Chomsky normal form](/chomsky-normal-form/) before [CYK](/cyk-algorithm/), for [Greibach normal form](/greibach-normal-form/), or in proofs about grammars, where empty productions make induction on string length fail. Do not use it to prepare a grammar for a parser that supports empty productions: the grammar grows, unit productions appear, and the trees no longer match the original rules.

## Pitfalls

- **Only direct empty productions.** Treating as nullable only the nonterminals with a production $A \to \varepsilon$ misses $S$ in the example, which derives $\varepsilon$ through $A B$. Use the full fixed point of line L1.
- **Adding the empty choice.** If all symbols of a right side are nullable, the choice that drops all of them gives $A \to \varepsilon$ again. Line L6 skips it.
- **Losing the empty string.** If $\varepsilon \in L(G)$ and the task asks for the same language, add $S' \to S \mid \varepsilon$ with $S'$ fresh. Adding $S \to \varepsilon$ to the old start symbol keeps the language, but when $S$ occurs on a right side it leaves an empty production inside other derivations, which the normal forms forbid.
- **Exponential output.** Long right sides with many nullable symbols blow up. Binarize first.
- **Dangling nonterminals.** A nonterminal whose productions were all empty disappears from the left sides. Code that treats every symbol without productions as a terminal then misreads it; remove the productions that mention it.

## Implementations

## History

Bar-Hillel, Perles and Shamir proved in 1961 that every context-free language without the empty string has a grammar without empty productions, among other normal-form results in the same paper. The construction by nullable symbols is in all textbooks; Hopcroft, Motwani and Ullman present it with the proof by splitting derivations used here. Lange and Leiß analyzed in 2009 how the order of this step and the other normal-form steps affects the size of the grammar.

## References
