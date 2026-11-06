---
tag: 0QNXET
kind: algorithm
slug: greibach-normal-form-conversion
name: Greibach normal form conversion
aliases:
- GNF conversion
area: automata-and-parsing/context-free-parsing
level: advanced
summary: Transforms a context-free grammar into an equivalent grammar in Greibach normal form.
solves: [cfg-normal-form-conversion]
model: word-ram
complexity:
  vars: {g: the size of the input grammar, N: the total size of all productions that the algorithm builds}
  time: {worst: O(N g), best: Ω(g)}
  space: {extra: O(N)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1965
  people: [Sheila Greibach]
  note: Greibach proved in 1965 that every context-free language without the empty string has a grammar in this form. Rosenkrantz gave a method based on matrix equations in 1967 and Blum and Koch a method with polynomial output size in 1999.
prereqs: [greibach-normal-form, left-recursion-elimination, useless-symbol-elimination]
see_also: [chomsky-normal-form-conversion, epsilon-production-elimination, unit-production-elimination, left-recursion, pushdown-automaton, cfg-to-pda-conversion, left-recursion-removal, context-free-grammar]
sources:
  - paper: doi:10.1145/321250.321254
    title: Sheila A. Greibach, A new normal-form theorem for context-free phrase structure grammars, Journal of the ACM 12(1) (1965)
    locator: pp. 42 to 52
  - book: isbn:9780201029888
    title: John E. Hopcroft and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, Addison-Wesley, 1979
    locator: Section 4.6, Greibach Normal Form (the substitution method with an ordering of the nonterminals, and its worked example)
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 21, Normal Forms
  - paper: doi:10.1145/321406.321412
    title: Daniel J. Rosenkrantz, Matrix equations and normal forms for context-free grammars, Journal of the ACM 14(3) (1967)
    locator: pp. 501 to 507
  - paper: doi:10.1006/inco.1998.2772
    title: Norbert Blum and Robert Koch, Greibach normal form transformation revisited, Information and Computation 150(1) (1999)
    locator: pp. 112 to 118 (output size O(|G|^3) before and O(|G|^4) after the removal of chain rules)
---

Greibach normal form conversion takes a [context-free grammar](/context-free-grammar/) and returns a grammar for the same language in which every production has the form $A \to a B_1 \cdots B_k$: one terminal, then zero or more nonterminals. The classical method cleans the grammar, puts the nonterminals in a fixed order, removes [left recursion](/left-recursion/) by substitution, and then substitutes from the last nonterminal back to the first. It always ends, but its output can be exponentially larger than its input.

## In plain words

We want rules that always start with a word. Then each step of a derivation writes exactly one word, and a reader that matches words from the left never loops. First we throw away empty rules, rules that only rename, and names that are never used. Then we number the names. We rewrite each rule so that a name can only start with a name that has a larger number. If a name starts with itself, we turn that loop into a new name that comes at the end. The last name now starts only with words. We put its rules into the rules of the name before it, and so on back to the first name. Each copy can multiply the number of rules.

## The problem

We use the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol, $n$ the input length, and the grammar size $|G| = \sum_{A \to \alpha} (|\alpha| + 1)$.

**Input.** A context-free grammar $G = (V, \Sigma, P, S)$.

**Output.** A grammar $G'$ with $L(G') = L(G)$ in [Greibach normal form](/greibach-normal-form/): every production is $A \to a B_1 \cdots B_k$ with $a \in \Sigma$, $k \ge 0$ and $B_i$ nonterminals, except that when $\varepsilon \in L(G)$ there is also $S_0 \to \varepsilon$ for a start symbol $S_0$ that is on no right side.

## The algorithm

The nonterminals that the algorithm adds are $T_a$ for terminals $a$ and $B_i$ for the left-recursive $A_i$. Substituting $A_j$ in $A \to A_j \gamma$ means replacing this production by $A \to \delta \gamma$ for every production $A_j \to \delta$.

```pseudo id=main
GREIBACH-NORMAL-FORM(G)
L1  E ← (S ⇒* ε)                                        ▷ the nullable test on G
L2  remove ε-productions, unit productions and useless symbols from G
L3  order the nonterminals A1, …, Am
L4  replace each terminal a that is not first on a right side by a new T_a, and add T_a → a
L5  for i ← 1 to m do
L6      for j ← 1 to i − 1 do
L7          substitute A_j in every production A_i → A_j γ
L8      if some production is A_i → A_i α then replace A_i → A_i α1 | … | A_i αp | β1 | … | βq by A_i → βk | βk B_i and B_i → αk | αk B_i
L9  for i ← m − 1 down to 1 do substitute A_j in every production A_i → A_j γ  (j > i)
L10 for each new B_i in increasing i do substitute the nonterminal that starts each production of B_i
L11 if E then add a new start symbol S0 with S0 → ε and S0 → α for every S → α
L12 return G
```

Line L1 is needed because line L2 removes $\varepsilon$ from the language. The new nonterminals $T_a$ of line L4 go at the end of the order; they already have the right form. After the loop of lines L5 to L8, every production of $A_i$ starts with a terminal or with an $A_j$ with $j > i$. So $A_m$ starts only with terminals, and the backward loop of line L9 brings each $A_i$ into the form, using the finished $A_j$ with $j > i$. Each production of a $B_i$ starts with some $A_k$ or with some $B_j$ with $j < i$, so line L10 finishes the $B_i$ in increasing order. In the implementation the $B_i$ wait in a queue, and a $B_i$ goes back to the end of the queue while a $B_j$ that starts one of its productions is still waiting.

## Example

Take the grammar of Hopcroft and Ullman's example, with the order $A_1, A_2, A_3$:

$$A_1 \to A_2 A_3, \qquad A_2 \to A_3 A_1 \mid b, \qquad A_3 \to A_1 A_2 \mid a.$$

It is already clean, and no terminal is in a non-first position. The steps are as follows.

- $i = 1$ and $i = 2$: the productions of $A_1$ and $A_2$ start with $A_2$, $A_3$ or a terminal, so nothing changes.
- $i = 3$, $j = 1$: $A_3 \to A_1 A_2$ becomes $A_3 \to A_2 A_3 A_2$.
- $i = 3$, $j = 2$: $A_3 \to A_2 A_3 A_2$ becomes $A_3 \to A_3 A_1 A_3 A_2 \mid b A_3 A_2$.
- Line L8: now $A_3 \to A_3 A_1 A_3 A_2 \mid b A_3 A_2 \mid a$, with one left-recursive alternative. It becomes

$$A_3 \to b A_3 A_2 \mid a \mid b A_3 A_2 B_3 \mid a B_3, \qquad B_3 \to A_1 A_3 A_2 \mid A_1 A_3 A_2 B_3.$$

- Line L9: $A_2 \to A_3 A_1$ takes the 4 productions of $A_3$, so $A_2$ has 5 productions, for example $A_2 \to b A_3 A_2 B_3 A_1$. Then $A_1 \to A_2 A_3$ takes the 5 productions of $A_2$, for example $A_1 \to b A_3$.
- Line L10: $B_3 \to A_1 A_3 A_2$ and $B_3 \to A_1 A_3 A_2 B_3$ each take the 5 productions of $A_1$, so $B_3$ has 10 productions, for example $B_3 \to b A_3 A_3 A_2$.

The result has 24 productions: 5 for $A_1$, 5 for $A_2$, 4 for $A_3$ and 10 for $B_3$. Its size is 134, against 13 for the input. The strings of length at most 5 in the language are $ba$, $abaa$ and $bbab$; the two grammars generate the same strings up to length 9. The implementation reproduces these counts, and the tests check them.

## Correctness

Each step keeps the language. Removing $\varepsilon$-productions, unit productions and useless symbols gives a grammar for $L(G) \setminus \{\varepsilon\}$. Adding $T_a \to a$ changes no language. Substituting $A_j$ in $A \to A_j \gamma$ is safe because every parse tree that uses $A \to A_j \gamma$ uses some $A_j \to \delta$ at the child, and the two nodes can be merged, and conversely split. Replacing the immediate left recursion of $A_i$ by $B_i$ is safe because in both grammars $A_i$ derives, by its own productions on the leftmost path, exactly the forms $\beta_k \alpha_{k_1} \cdots \alpha_{k_r}$.

The form follows from three facts. After line L4, every symbol after the first on a right side is a nonterminal, and every right side has length at least 2 or is one terminal; substitution keeps both properties. After the forward loop, $A_i$ starts only with terminals or with $A_j$, $j > i$, by induction on $i$. The backward loop and the queue for the $B_i$ end, because the "starts with" relation between the nonterminals is acyclic. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Output size.** The output can be exponentially larger than the input. Take $A_m \to A_{m-1} a \mid A_{m-1} b$, $A_1 \to a \mid b$ and $A_i \to A_{i-1} a \mid A_{i-1} b$ for $1 < i < m$, with $A_m$ first in the order. This grammar has size $6m - 2$, and its language is all strings of length $m$ over $\{a, b\}$. The forward loop substitutes $A_{i-1}$ into $A_i$, which doubles the number of productions at each level, and the output has $2^{m+1}$ productions. For $m = 8$ the input has size 46 and the output has 512 productions and size 4100. The grammar $C_1 \to a \mid b$, $C_i \to a C_{i-1} \mid b C_{i-1}$ is in Greibach normal form for the same language with size $O(m)$, so the blow-up comes from the method, not from the language.

**Time.** Let $N$ be the total size of all productions that the algorithm builds, counted each time one is built, including those that a later step replaces. Building or hashing a production costs time proportional to its length, with expected $O(1)$ time per symbol for the dictionaries that remove duplicates. Each production is read at most $m$ times by line L7, once by lines L8 and L9, and at most once per pass of the queue of line L10, which has at most $m$ passes. Removing $\varepsilon$-productions and unit productions also costs $O(m)$ per production built. So the time is $O(N |G|)$, and at least $\Omega(|G|)$ to read the input. In the worst case $N$ is exponential in $|G|$, as the family above shows.

**Space.** The grammar in use and the dictionaries hold $O(N)$ symbols.

## Properties

- **Deterministic.** With the nonterminals ordered by their first appearance, the output is a fixed function of the list of productions.
- **The order matters.** A different order of the nonterminals in line L3 gives a different grammar, which can have a different size.
- **No new ambiguity.** Every step maps each parse tree of the new grammar to a different parse tree of the old one, so a string never gets more parse trees, and an unambiguous grammar gives an unambiguous result. A string can get fewer trees: line L2 removes cycles $A \Rightarrow^+ A$, and two substitutions can give the same production.
- **Derivation length.** In the output, every derivation of a nonempty string $w$ has exactly $|w|$ steps, because each step writes one terminal.

## Variants and improvements

- **Rosenkrantz's method.** Write the productions as a system of equations $X = X R + S$ over vectors of nonterminals, and solve it with a new matrix of nonterminals for the closure $R^*$. This gives Greibach normal form without the backward substitutions of the classical method.
- **Polynomial size.** Blum and Koch transform an $\varepsilon$-free grammar into an extended Greibach normal form with chain rules of size $O(|G|^3)$, and after the removal of chain rules into Greibach normal form of size $O(|G|^4)$.
- **Double Greibach normal form.** Every right side starts and ends with a terminal (or is a single terminal); Rosenkrantz's construction also gives this form.
- **From a grammar to a pushdown automaton.** The [conversion of a grammar to a pushdown automaton](/cfg-to-pda-conversion/) from a grammar in Greibach normal form gives a one-state automaton that reads one input symbol at each move and has no $\varepsilon$-moves except possibly for the empty string.

## When to use it

Use it in proofs and constructions that need a terminal at the start of each production: real-time [pushdown automata](/pushdown-automaton/), the bound of $|w|$ steps for each derivation, or a top-down parser that can never loop. For parsing a language in practice, do not convert to Greibach normal form; the grammar grows, its trees no longer match the original structure, and [left recursion removal](/left-recursion-removal/) with an $\varepsilon$-production is enough for top-down parsing. When the size matters, use the method of Blum and Koch, whose output size is polynomial in $|G|$.

## Pitfalls

- **Forgetting the empty string.** Line L2 drops $\varepsilon$ from the language. Without lines L1 and L11 the output is wrong for grammars such as $S \to a S b \mid \varepsilon$.
- **Unit productions left in.** A unit production $A_i \to A_i$ gives a left-recursive alternative with an empty $\alpha$, and then $B_i \to \varepsilon$ is not in the form. Removing unit productions in line L2 prevents this.
- **Substituting in the wrong direction.** In the backward loop, $A_i$ must take the productions of $A_j$ with $j > i$ after $A_j$ is finished. Going forward copies productions that still start with nonterminals.
- **Forgetting the $B_i$.** The new nonterminals are not in the order, and their productions still start with nonterminals after line L9. Line L10 must finish them, and in the right order when one $B_i$ starts with another.
- **Quadratic duplicate removal.** Substitution produces the same right side many times. Removing duplicates by searching a list costs quadratic time in the number of productions, which is already large; use a hash table.
- **Unordered sets.** If the nonterminals come from an unordered set, the order in line L3 and so the output can change from run to run.

## Implementations

## History

Sheila Greibach proved in 1965 that every context-free language without the empty string has a grammar in which each right side is a terminal followed by nonterminals, and her proof uses substitution and the removal of left recursion. Daniel Rosenkrantz gave a construction by matrix equations in 1967, which also gives the double form. The ordered substitution method is the one of textbooks such as Hopcroft and Ullman (1979). Blum and Koch showed in 1999 how to get an output of polynomial size.

## References
