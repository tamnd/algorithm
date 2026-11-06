---
tag: 09FBBP
kind: algorithm
slug: useless-symbol-elimination
name: Useless symbol elimination
aliases:
- trimming a grammar
area: automata-and-parsing/context-free-parsing
level: core
summary: Removes nonterminals that generate nothing or are unreachable from the start symbol.
solves: [cfg-emptiness-problem, cfg-normal-form-conversion]
model: word-ram
complexity:
  vars: {G: the grammar size}
  time: {worst: O(G), best: O(G)}
  space: {extra: O(G)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1961
  people: [Yehoshua Bar-Hillel, Micha Perles, Eli Shamir]
  note: Bar-Hillel, Perles and Shamir showed in 1961 that the emptiness of a context-free language is decidable, by marking the nonterminals that derive terminal strings; removing the unmarked and the unreachable symbols became the standard first step of the normal forms.
prereqs: [context-free-grammar, derivation, parse-tree]
see_also: [cfg-emptiness-problem, epsilon-production-elimination, unit-production-elimination, chomsky-normal-form-conversion, nullable-symbol, graph-reachability, horn-sat-forward-chaining, cfg-finiteness-problem]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 7.1.1, Eliminating Useless Symbols, and Section 7.1.2, Computing the Generating and Reachable Symbols (including the example that shows why the generating symbols must be removed first)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 2.9, Hygiene in Context-Free Grammars (undefined, unreachable and non-productive non-terminals, and 2.9.5, Cleaning up a Context-Free Grammar)
  - paper: "Yehoshua Bar-Hillel, Micha Perles and Eli Shamir, On formal properties of simple phrase structure grammars, Zeitschrift für Phonetik, Sprachwissenschaft und Kommunikationsforschung 14 (1961)"
    locator: pp. 143 to 172 (the decidability of emptiness)
---

Useless symbol elimination removes from a [context-free grammar](/context-free-grammar/) every nonterminal that cannot take part in the derivation of a sentence, together with the productions that mention it. A symbol is useless if it derives no terminal string, or if no sentential form derived from the start symbol contains it. Two linear passes find them: a worklist marks the generating nonterminals, and a [graph search](/graph-reachability/) from the start symbol marks the reachable ones in what remains. The order of the passes matters. The result, called a reduced or trimmed grammar, generates the same language and has the same parse trees for every sentence. The first pass alone decides the [emptiness problem](/cfg-emptiness-problem/).

## In plain words

A grammar can contain rules that never help to build a sentence. Some placeholders can never be expanded into plain text: every rule for them leads to another such placeholder, or they have no rule at all. Other placeholders can never be reached: no chain of rules starting from the start placeholder ever mentions them.

The algorithm removes both kinds. First it marks every placeholder that can turn into plain text, starting from rules with plain text only and spreading backward through rules. It drops every rule that uses an unmarked placeholder. Then it starts from the start placeholder and follows the remaining rules forward, marking what it meets, and drops the rest. The grammar gets smaller but produces the same sentences.

Doing the two steps in the other order can leave useless rules behind.

## The problem

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size, here $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$.

Let $G = (V, \Sigma, P, S)$. A symbol $X \in V \cup \Sigma$ is

- **generating** if $X \Rightarrow^* w$ for some $w \in \Sigma^*$ (every terminal is generating);
- **reachable** if $S \Rightarrow^* \alpha X \beta$ for some $\alpha, \beta$;
- **useful** if $S \Rightarrow^* \alpha X \beta \Rightarrow^* w$ for some $w \in \Sigma^*$, and **useless** otherwise.

The output is a grammar $G'$ whose productions are those of $P$ in which every symbol is useful, so that $L(G') = L(G)$ and, if $L(G) \neq \emptyset$, every symbol of $G'$ is useful. If $L(G) = \emptyset$, then $S$ itself is useless and $G'$ has no production.

A nonterminal with no production is allowed; it is not generating. Terminals that occur in no remaining production can be dropped from $\Sigma$ as well.

## The algorithm

```pseudo id=main
TRIM(G = (V, Σ, P, S))
L1  for each p ∈ P do count[p] ← the number of nonterminal occurrences in its right side; record each occurrence of X in uses[X]
L2  Gen ← ∅; W ← the left sides of the productions p with count[p] = 0
L3  while W is not empty do
L4      X ← pop(W); if X ∈ Gen then skip to the next iteration
L5      add X to Gen
L6      for each p = (A → α) in uses[X] do count[p] ← count[p] − 1; if count[p] = 0 then push A on W
L7  P1 ← the productions A → α of P with A ∈ Gen and every nonterminal of α in Gen
L8  Reach ← {S}; W ← [S]
L9  while W is not empty do A ← pop(W)
L10     for each A → α in P1 and each nonterminal B of α with B ∉ Reach do add B to Reach; push B on W
L11 return (V, Σ, the productions A → α of P1 with A ∈ Reach, S)
```

**Lines L1 to L6: generating symbols.** A production $A \to \alpha$ makes $A$ generating as soon as all nonterminals of $\alpha$ are generating, since its terminals already are. The counter of $p$ is the number of nonterminal occurrences of $\alpha$ not yet known to be generating. When $X$ joins Gen, line L6 decreases the counter once for each occurrence of $X$; at 0, the left side is generating. This is the forward chaining of [Horn satisfiability](/horn-sat-forward-chaining/), with one Horn clause per production. The same worklist with terminals counted too computes the [nullable symbols](/nullable-symbol/).

**Line L7.** A production that mentions a nongenerating nonterminal derives no terminal string, so no derivation of a sentence uses it.

**Lines L8 to L10: reachable symbols.** This is a [graph search](/graph-reachability/) in the graph with an edge $A \to B$ for each occurrence of $B$ in a right side of $A$ in $P_1$. Any order of the worklist works; a stack gives depth-first order and a queue [breadth-first order](/breadth-first-search/).

**Why generating first.** In $S \to A B \mid a$, $A \to b$, with $B$ a nonterminal without productions, all symbols are reachable, but $B$ is not generating. Removing $B$ deletes $S \to A B$, and then $A$ is no longer reachable. Line L7 can make symbols unreachable, but removing unreachable symbols never makes a symbol nongenerating, since a derivation of a terminal string from $A$ uses only symbols reachable from $A$. So the order "generating, then reachable" is the one that leaves no useless symbol. The other order returns $S \to a$, $A \to b$.

## Example

Take the grammar of size 24

$$S \to A\,B \mid C\,a, \quad A \to a\,A \mid b, \quad B \to B\,b, \quad C \to c \mid D, \quad D \to d\,D, \quad E \to e\,S.$$

The counters are 2, 1, 1, 0, 1, 0, 1, 1, 1 in this order of the productions, so line L2 starts with $W = [A, C]$. With a stack:

| pop | Gen after | productions that reach 0 | $W$ after |
|---|---|---|---|
| $C$ | $C$ | $S \to C a$ | $A, S$ |
| $S$ | $C, S$ | $E \to e S$ | $A, E$ |
| $E$ | $C, S, E$ | none | $A$ |
| $A$ | $C, S, E, A$ | $A \to a A$ | $A$ |
| $A$ | already in Gen | | empty |

$B$ is not generating: its only production needs $B$ itself. $D$ is not either. Line L7 removes $S \to A B$, $B \to B b$, $C \to D$ and $D \to d D$, leaving $S \to C a$, $A \to a A \mid b$, $C \to c$, $E \to e S$.

From $S$, lines L8 to L10 reach only $C$. $A$ was reachable in $G$, through $S \to A B$, but not in $P_1$, and $E$ is reachable in neither. The result is

$$S \to C\,a, \qquad C \to c,$$

which generates $\{ca\}$, as $G$ does. These steps were checked by a script.

## Correctness

**Claim 1.** After line L6, Gen is the set of generating nonterminals.

*Only generating ones.* A nonterminal is pushed only when some production $A \to \alpha$ has all nonterminals of $\alpha$ in Gen. By induction on the order of insertion, each of them derives a terminal string, so $A \Rightarrow \alpha \Rightarrow^* w$.

*All generating ones.* If $A \Rightarrow^* w$, take a parse tree of minimum height $h$. By induction on $h$: the root uses some $A \to \alpha$ whose nonterminal children have trees of smaller height, so they are all in Gen, and each of their occurrences decreased the counter of this production. So the counter reached 0 and $A$ was pushed, and it entered Gen when popped.

**Claim 2.** Reach is the set of nonterminals reachable from $S$ in the grammar $(V, \Sigma, P_1, S)$. This is the correctness of graph search: a nonterminal is reachable exactly when there is a path of occurrence edges from $S$ to it, and the worklist adds every successor of every reached vertex.

**Claim 3.** The productions returned are exactly the productions of $P$ all of whose symbols are useful, and $L(G') = L(G)$. A production used in a derivation $S \Rightarrow^* w$ consists of useful symbols, so it survives line L7 (all its symbols generate parts of $w$) and line L11 (its left side is reachable inside that derivation, which uses only productions of $P_1$). Conversely, if $A \to \alpha$ survives, $A$ is reachable in $P_1$ by a derivation $S \Rightarrow^* \gamma A \delta$ over $P_1$, and every symbol of $\gamma A \delta$ and of $\alpha$ is generating, so the whole sentential form derives a terminal string: every symbol involved is useful. So the derivations of sentences in $G$ and in $G'$ are the same, and the languages and the parse trees of sentences are equal. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Time.** Line L1 visits every symbol of every right side once. Each nonterminal enters Gen once, and line L6 then visits each of its occurrences once, so all decrements together are bounded by the number of occurrences. Pushes onto $W$ are bounded by the number of productions, since each counter reaches 0 once. Line L7 is one more pass. Lines L8 to L10 visit each production of $P_1$ once, when its left side is popped. In total, $O(|G|)$, with hash maps or arrays indexed by symbol. The bound is the same in the best case, since the input must be read.

**Space.** The counters, the occurrence lists and the sets take $O(|G|)$.

**Quadratic versions.** The common textbook loop "repeat: mark every $A$ with a production whose symbols are all marked, until nothing changes" is correct but can need $|V|$ rounds over all of $P$, for $O(|V| \cdot |G|)$ time, as on the chain $A_1 \to A_2 a, \ldots, A_{k-1} \to A_k a$, $A_k \to b$ with the productions listed in this order.

## Properties

- **Preserves the language and the parse trees.** Every parse tree of a sentence uses only useful productions, so $G'$ has the same trees for every sentence. In particular, $G'$ is ambiguous exactly when $G$ is.
- **Idempotent.** Running TRIM on its own output changes nothing.
- **Decides emptiness.** $L(G) = \emptyset$ exactly when $S \notin$ Gen after line L6; the [emptiness problem](/cfg-emptiness-problem/) needs only this half.
- **Keeps the other normal-form properties.** It only deletes productions, so it creates no empty production, no unit production and no left recursion.
- **Not finer than the language.** A useful production can still be redundant: in $S \to a \mid A$, $A \to a$, both productions are useful although one would do.

## Variants and improvements

- **Only the generating pass.** For the emptiness test, or for a parser generator that warns about nonterminals deriving nothing.
- **Only the reachable pass.** Parser generators also warn about unused nonterminals; this needs the second pass on all of $P$.
- **Order with the other transformations.** [Epsilon-production elimination](/epsilon-production-elimination/) and [unit-production elimination](/unit-production-elimination/) can create unreachable nonterminals: after unit elimination of $S \to A$, $A \to a$, the nonterminal $A$ has its own productions but no occurrence. So the usual order for [Chomsky normal form](/chomsky-normal-form-conversion/) is: eliminate $\varepsilon$, eliminate unit productions, then remove useless symbols.
- **Finiteness.** On a trimmed grammar without empty and unit productions, the language is infinite exactly when the graph of occurrences has a cycle; see the [finiteness problem](/cfg-finiteness-problem/).
- **Automata.** For a finite automaton, the same two passes keep the states that are reachable from the start and can reach an accepting state, as before [DFA minimization](/dfa-minimization/).

## When to use it

Use it as the first cleaning step on a grammar written by hand or produced by another construction, such as the product of a grammar with an automaton, the conversion of a [pushdown automaton](/pushdown-automaton/) to a grammar, or a grammar after other normal-form steps. Many constructions assume a reduced grammar: LR parsing tables, the [SLR(1) grammar](/slr-grammar/) test and normal forms. It costs linear time, so there is little reason to skip it.

## Pitfalls

- **Reachable first.** The other order of the two passes leaves useless symbols, as the example $S \to A B \mid a$, $A \to b$ shows.
- **Nonterminals without productions.** If the nonterminals are taken to be the left sides only, a nonterminal with no production looks like a terminal and is treated as generating. Keep $V$ explicit, as the implementation does with an optional set of declared nonterminals.
- **Removing too little after the first pass.** Line L7 must remove every production with a nongenerating symbol anywhere on its right side, not only the productions of nongenerating left sides.
- **An empty language.** When $S$ is not generating, the output has no production. Code that assumes $S$ has at least one production fails; return an explicit empty grammar.
- **Counting occurrences.** In the generating pass, a production such as $A \to B B$ must be decremented twice when $B$ becomes generating, or once with a counter of distinct nonterminals. Mixing the two conventions leaves counters that never reach 0.
- **Recursion.** A recursive depth-first search for reachability overflows the stack on long chains of nonterminals in generated grammars; use a worklist.

## Implementations

## History

Bar-Hillel, Perles and Shamir proved in 1961 that it is decidable whether a context-free grammar generates any string, by the marking of generating nonterminals, in the same paper that gave the pumping lemma for context-free languages. Removing the nongenerating and the unreachable symbols became the standard preliminary step of the normal-form constructions; Hopcroft, Motwani and Ullman present it with the example that shows why the order of the two passes matters. Grune and Jacobs call the result a clean grammar and discuss it with loops and undefined nonterminals.

## References
