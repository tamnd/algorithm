---
tag: ANAZS1
kind: concept
slug: nullable-symbol
name: Nullable symbol
aliases:
- nullable nonterminal
area: automata-and-parsing/context-free-parsing
level: core
summary: A nonterminal that can derive the empty string; needed for FIRST and FOLLOW computation.
prereqs: [context-free-grammar, derivation]
see_also: [first-and-follow-sets, epsilon-production-elimination, ll-parse-table, earley-parser, left-recursion, useless-symbol-elimination, chomsky-normal-form-conversion]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 7.1.3, Eliminating epsilon-Productions (the definition of nullable symbols, their inductive computation, and the proof that it finds exactly the nullable symbols)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.4.2, FIRST and FOLLOW
  - book: isbn:9780521820608
    title: Andrew W. Appel and Jens Palsberg, Modern Compiler Implementation in Java, second edition
    locator: Section 3.2, Predictive Parsing (the joint computation of nullable, FIRST and FOLLOW)
---

A nullable symbol is a nonterminal $A$ of a [context-free grammar](/context-free-grammar/) that can derive the empty string, $A \Rightarrow^* \varepsilon$. The set of nullable symbols is the least solution of a simple system of equations, and it can be computed in time linear in the size of the grammar. Almost every grammar algorithm needs it first: [FIRST and FOLLOW sets](/first-and-follow-sets/), [LL parse tables](/ll-parse-table/), [epsilon-production elimination](/epsilon-production-elimination/), the detection of hidden [left recursion](/left-recursion/), and the completion step of the [Earley parser](/earley-parser/).

## In plain words

Some grammar rules can produce nothing at all, like an optional sign before a number. A symbol is nullable when some sequence of rules turns it into nothing. A rule that produces nothing makes its left symbol nullable at once. A rule whose right side consists only of nullable symbols also makes its left symbol nullable, because each of those symbols can vanish in turn.

You find all nullable symbols by repeating this test until nothing new turns up. A rule with a real word in it never helps, because a word cannot vanish. A symbol that can vanish only if it already vanishes is not nullable: the search starts from "nothing is nullable" and only adds symbols that it can prove.

## The idea

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area.

**Definition.** A nonterminal $A$ is *nullable* if $A \Rightarrow^* \varepsilon$. A string $\alpha \in (V \cup \Sigma)^*$ is nullable if $\alpha \Rightarrow^* \varepsilon$. Let $\mathrm{Null} \subseteq V$ be the set of nullable nonterminals. A string is nullable exactly when it consists only of nullable nonterminals: by the splitting lemma of the [derivation](/derivation/) page, $X_1 \cdots X_k \Rightarrow^* \varepsilon$ if and only if $X_i \Rightarrow^* \varepsilon$ for each $i$, and a terminal derives only itself. In particular $\varepsilon$ is nullable, and $\varepsilon \in L(G)$ if and only if $S$ is nullable.

**Least fixed point.** Define the operator $F$ on subsets of $V$ by

$$F(N) = \{ A \in V : A \to X_1 \cdots X_k \in R \text{ for some } k \ge 0 \text{ with } X_1, \ldots, X_k \in N \}.$$

$F$ is monotone: $N \subseteq N'$ implies $F(N) \subseteq F(N')$. Let $N_0 = \emptyset$ and $N_{i+1} = F(N_i)$. Then $N_0 \subseteq N_1 \subseteq \cdots$, and the chain is constant from some $i \le |V|$ on, because each strict step adds a nonterminal.

> **Proposition.** $\mathrm{Null} = \bigcup_i N_i$, and this is the least set $N$ with $F(N) \subseteq N$.

*Proof.* ($\bigcup_i N_i \subseteq \mathrm{Null}$.) By induction on $i$: $N_0$ is empty, and if $A \in N_{i+1}$ by the production $A \to X_1 \cdots X_k$ with each $X_j \in N_i$, then each $X_j \Rightarrow^* \varepsilon$ by the induction hypothesis, so $A \Rightarrow X_1 \cdots X_k \Rightarrow^* \varepsilon$.

($\mathrm{Null} \subseteq \bigcup_i N_i$.) If $A \Rightarrow^* \varepsilon$, take a [parse tree](/parse-tree/) with root $A$ and yield $\varepsilon$; all its leaves are $\varepsilon$. By induction on the height $h$ of the tree, $A \in N_h$: the root uses a production $A \to X_1 \cdots X_k$, each $X_j$ is a nonterminal whose subtree has yield $\varepsilon$ and height less than $h$, so $X_j \in N_{h-1}$ by the induction hypothesis and the monotonicity of the chain, and then $A \in F(N_{h-1}) = N_h$. (For $k = 0$ the root has the single child $\varepsilon$, $h = 1$, and $A \in F(\emptyset) = N_1$.)

(Least.) If $F(N) \subseteq N$, then $N_i \subseteq N$ for all $i$ by induction, since $N_{i+1} = F(N_i) \subseteq F(N) \subseteq N$. $\blacksquare$

The word *least* matters. The equation $F(N) = N$ can have larger solutions: in the second example below, $N = \{S, A, B, C\}$ satisfies it, but only $B$ derives $\varepsilon$. An algorithm that starts from "all symbols are nullable" and removes symbols finds such a wrong answer.

**A linear-time algorithm.** The plain iteration does up to $|V| + 1$ passes over the grammar, so it takes $O(|V| \cdot |G|)$ time. A worklist with counters takes $O(|G|)$ time, in the style of linear-time Horn satisfiability:

1. For each production $p$, set $\mathit{count}[p]$ to the length of its right side. For each nonterminal $X$, list the productions in which $X$ occurs on the right side, once for each occurrence.
2. Put each $A$ with a production $A \to \varepsilon$ into $\mathrm{Null}$ and into a queue.
3. While the queue is not empty, remove $X$. For each occurrence of $X$ in a right side of a production $p = B \to \beta$, decrease $\mathit{count}[p]$ by 1. If it reaches 0 and $B \notin \mathrm{Null}$, add $B$ to $\mathrm{Null}$ and to the queue.

A production that contains a terminal never reaches 0, because only occurrences of nonterminals are decreased. Each nonterminal enters the queue at most once, and each occurrence in a right side is decreased at most once, so the total work is $O(|G|)$. When $\mathit{count}[p] = 0$, every symbol of the right side of $p$ has been removed from the queue, so all are nullable and the left side is nullable; conversely the proof above shows that every nullable symbol is eventually reached.

## Examples

**A chain that needs several passes.** Take $S \to AB$, $A \to CC$, $B \to \varepsilon$, $C \to B$, and scan the productions in this order in each pass.

| pass | added |
|---|---|
| 1 | $B$ (by $B \to \varepsilon$), then $C$ (by $C \to B$) |
| 2 | $A$ (by $A \to CC$) |
| 3 | $S$ (by $S \to AB$) |
| 4 | nothing, so the iteration stops |

All four nonterminals are nullable, and $\varepsilon \in L(G)$. The worklist version finds the same set with one decrement for each of the 5 occurrences of nonterminals on the right sides.

**A cycle that is not nullable.** Take $S \to AB \mid c$, $A \to a \mid BC$, $B \to b \mid \varepsilon$, $C \to AB \mid c$. Only $B$ is nullable. $A$ would be nullable if $C$ were, and $C$ would be nullable if $A$ were, but neither has a derivation of $\varepsilon$ to start from. So $S$ is not nullable either, and $\varepsilon \notin L(G)$.

**The LL(1) expression grammar.** In $E \to T E'$, $E' \to + T E' \mid \varepsilon$, $T \to F T'$, $T' \to * F T' \mid \varepsilon$, $F \to ( E ) \mid id$, the nullable symbols are $E'$ and $T'$. $E$ and $T$ are not nullable, because $F$ always produces a token. So $\mathrm{FIRST}(T E') = \mathrm{FIRST}(T)$, while $\mathrm{FIRST}(E' \, \$)$ has to look past $E'$ to the end marker.

**Non-examples.** A terminal is never nullable. A nonterminal with no production, or one that derives no terminal string at all, is not nullable. The string $A b$ is not nullable even when $A$ is.

## Where it is used

- **FIRST and FOLLOW.** $\mathrm{FIRST}(X_1 \cdots X_k)$ includes $\mathrm{FIRST}(X_{i+1})$ exactly when $X_1 \cdots X_i$ is nullable, and $\mathrm{FOLLOW}(A)$ gets $\mathrm{FOLLOW}(B)$ when $B \to \alpha A \beta$ with $\beta$ nullable. See [FIRST and FOLLOW sets](/first-and-follow-sets/) and the [LL parse table](/ll-parse-table/), which puts $A \to \alpha$ in the column of each token of $\mathrm{FOLLOW}(A)$ when $\alpha$ is nullable.
- **Removing empty productions.** [Epsilon-production elimination](/epsilon-production-elimination/) replaces each production by all versions with some nullable symbols left out. It is the first step of the [Chomsky normal form conversion](/chomsky-normal-form-conversion/).
- **Hidden left recursion.** $A \to B A c$ with $B$ nullable gives $A \Rightarrow^+ A c$. Tests for [left recursion](/left-recursion/) follow the edge from $A$ to each right-side symbol that has only nullable symbols before it.
- **Earley parsing.** The [Earley parser](/earley-parser/) can miss completions of nullable nonterminals; the standard fix advances the dot over a nullable symbol at prediction time, which needs the set $\mathrm{Null}$.
- **LR items with empty right sides.** In [LR(0) parsing](/lr0-parsing/) a production $A \to \varepsilon$ gives the complete item $A \to \cdot$ in every state that predicts $A$, a common source of conflicts.

## References
