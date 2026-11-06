---
tag: A7NHS1
kind: problem
slug: cfg-normal-form-conversion
name: CFG normal form conversion
aliases:
- grammar normalization
area: automata-and-parsing/context-free-parsing
level: core
summary: Transform a context-free grammar into an equivalent one in a prescribed normal form.
model: word-ram
complexity:
  vars: {g: the grammar size}
  time: {worst: O(g^2)}
prereqs: [context-free-grammar, nullable-symbol, useless-symbol-elimination]
see_also: [chomsky-normal-form, chomsky-normal-form-conversion, greibach-normal-form, greibach-normal-form-conversion, epsilon-production-elimination, unit-production-elimination, left-recursion-elimination, cyk-algorithm]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 7.1, Normal Forms for Context-Free Grammars (7.1.1 to 7.1.5), and Section 7.4.2, Running Time of Conversion to Chomsky Normal Form
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 2.1, Chomsky Normal Form (Theorem 2.9 and its proof)
  - paper: doi:10.1145/321250.321254
    title: Sheila A. Greibach, A new normal-form theorem for context-free phrase structure grammars, Journal of the ACM 12(1) (1965)
    locator: pp. 42 to 52 (every grammar without the empty string has an equivalent grammar in Greibach normal form)
  - paper: doi:10.1145/321406.321412
    title: Daniel J. Rosenkrantz, Matrix equations and normal forms for context-free grammars, Journal of the ACM 14(3) (1967)
    locator: pp. 501 to 507 (Greibach normal form by solving a system of linear equations over languages)
  - paper: doi:10.1006/inco.1998.2772
    title: Norbert Blum and Robert Koch, Greibach normal form transformation revisited, Information and Computation 150(1) (1999)
    locator: pp. 112 to 118 (from Chomsky normal form to Greibach normal form with size O(|G|^3))
---

CFG normal form conversion is the task of turning a [context-free grammar](/context-free-grammar/) into an equivalent grammar whose productions all have a prescribed shape. The two classical targets are [Chomsky normal form](/chomsky-normal-form/), where every production is $A \to BC$ or $A \to a$, and [Greibach normal form](/greibach-normal-form/), where every production is $A \to a B_1 \cdots B_k$. Every grammar can be converted, apart from the empty string where the form forbids it, and the cost is polynomial in the size of the grammar, but the order of the steps decides whether it is $O(|G|^2)$ or exponential.

## In plain words

A grammar can use rules of any shape: long rules, rules that produce nothing, rules that only rename one symbol to another. Algorithms that read grammars are much simpler when every rule has one fixed shape, for example "one symbol becomes exactly two symbols, or one letter".

Conversion rewrites the rules into that shape without changing which strings the grammar describes. It splits long rules into chains of short ones, it removes rules that produce nothing by adding copies of the rules that used them, and it replaces renaming rules by copies of the rules they rename to.

Done in the right order, the grammar grows at most by a square. Done in the wrong order, removing the empty rules first, it can grow exponentially.

## Definition

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, and $|G|$, written $g$ in the front matter, is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$.

**Input.** A context-free grammar $G$ and a target normal form $\mathcal{F}$, a set of allowed shapes of productions.

**Output.** A grammar $G'$ in form $\mathcal{F}$ with $L(G') = L(G)$, or $L(G') = L(G) \setminus \{\varepsilon\}$ when $\mathcal{F}$ cannot derive $\varepsilon$.

The common targets are below. In each, a *unit production* is $A \to B$ with $B \in V$, and an *$\varepsilon$-production* is $A \to \varepsilon$.

| normal form | allowed productions | exists for |
|---|---|---|
| reduced | any, but every nonterminal is reachable from $S$ and derives a terminal string | every $G$ with $L(G) \ne \emptyset$ |
| proper | no [useless symbols](/useless-symbol-elimination/), no $\varepsilon$-productions except $S \to \varepsilon$, no cycles $A \Rightarrow^+ A$ | every $G$ |
| binary (2NF) | right sides of length at most 2 | every $G$ |
| [Chomsky](/chomsky-normal-form/) | $A \to BC$ and $A \to a$, plus $S \to \varepsilon$ if $S$ is on no right side | every $G$ |
| [Greibach](/greibach-normal-form/) | $A \to a B_1 \cdots B_k$ with $k \ge 0$ | every $G$, for $L(G) \setminus \{\varepsilon\}$ |
| quadratic Greibach | $A \to a$, $A \to aB$, $A \to aBC$ | every $G$, for $L(G) \setminus \{\varepsilon\}$ |
| no [left recursion](/left-recursion/) | no $A \Rightarrow^+ A \alpha$ | every $G$, for $L(G) \setminus \{\varepsilon\}$ |
| right-linear | $A \to a B$, $A \to a$, $A \to \varepsilon$ | only when $L(G)$ is regular |

## Variants

- **Equivalence up to the empty string.** Greibach normal form cannot derive $\varepsilon$, so it represents $L(G) \setminus \{\varepsilon\}$; whether $\varepsilon \in L(G)$ is a separate bit, given by whether $S$ is [nullable](/nullable-symbol/).
- **Strong equivalence.** Some uses need more than the same language: for example a parse tree of $G'$ should map back to a parse tree of $G$, so that the semantic actions still apply. A parse tree of the Chomsky normal form maps back to a parse tree of $G$ by undoing each step, since every new nonterminal stands for a known part of an old production. Greibach normal form conversion does not keep the tree shapes.
- **Conversion with bounded growth.** Ask for a conversion whose output has size $O(|G|)$, $O(|G|^2)$ or another bound. The binary form takes $O(|G|)$ and Chomsky normal form $O(|G|^2)$.
- **Right-linear target.** A right-linear grammar exists exactly when $L(G)$ is regular, and whether $L(G)$ is regular is undecidable. So this conversion is not computable, unlike all the others in the table.
- **Pushdown automata.** The analogous normal forms for a [pushdown automaton](/pushdown-automaton/), such as pushing at most two symbols per move, are obtained by the [conversion to a grammar](/cfg-pda-equivalence/) and back.

## Examples

**To Chomsky normal form.** Take $S \to a S b \mid \varepsilon$, of size 5. The steps START, TERM, BIN, DEL, UNIT and the removal of useless symbols give
$$S_0 \to A X \mid \varepsilon, \quad S \to A X, \quad X \to S B \mid b, \quad A \to a, \quad B \to b,$$
of size 16. START added $S_0 \to S$. TERM replaced $a$ and $b$ in the long right side by $A$ and $B$. BIN split $S \to A S B$ into $S \to A X$ and $X \to S B$. DEL removed $S \to \varepsilon$, added $X \to B$ because $S$ is nullable, and added $S_0 \to \varepsilon$ because $S_0$ is nullable. UNIT replaced $S_0 \to S$ by $S_0 \to A X$ and $X \to B$ by $X \to b$, and $B \to b$ stays because $S \to \ldots B$ still uses $B$.

**The order of the steps.** Let $G_k$ be $S \to A_1 A_2 \cdots A_k$ and $A_i \to a \mid \varepsilon$, of size $4k + 1$. If DEL runs before BIN, the production of $S$ is replaced by one production for each nonempty subset of the $A_i$, which is $2^k - 1$ productions of total size $(2^k - 1) + k\,2^{k-1}$. If BIN runs first, each binary production gets at most three versions. The sizes, computed by a script:

| $k$ | $\lvert G_k \rvert$ | after START, TERM, BIN, DEL, UNIT | $S$-productions if DEL comes first |
|---|---|---|---|
| 2 | 9 | 10 | 3 |
| 4 | 17 | 33 | 15 |
| 6 | 25 | 68 | 63 |
| 8 | 33 | 115 | 255 |

The middle column grows quadratically, because of the copies made by UNIT, and the right column exponentially.

## Known algorithms

- **Binary form**, $O(|G|)$. Replace $A \to X_1 \cdots X_k$ with $k \ge 3$ by $A \to X_1 A_1$, $A_1 \to X_2 A_2$, $\ldots$, $A_{k-2} \to X_{k-1} X_k$, with new nonterminals. The size grows by a factor of at most 3.
- **[Chomsky normal form conversion](/chomsky-normal-form-conversion/)**, $O(|G|^2)$ time and size. In order: START adds a new start symbol, TERM replaces terminals in long right sides, BIN splits long right sides, DEL removes [$\varepsilon$-productions](/epsilon-production-elimination/), UNIT removes [unit productions](/unit-production-elimination/), and then [useless symbols](/useless-symbol-elimination/) are removed. DEL after BIN at most triples each binary production. UNIT copies the productions of $B$ to every $A$ with $A \Rightarrow^* B$ by unit productions, which is where the square comes from.
- **[Greibach normal form conversion](/greibach-normal-form-conversion/).** The classical method orders the nonterminals, removes [left recursion](/left-recursion-elimination/) one nonterminal at a time, and substitutes back, with an exponential worst case. Rosenkrantz solved the grammar as a system of equations over languages, and Blum and Koch convert a grammar in Chomsky normal form into Greibach normal form with size $O(|G|^3)$.
- **Reduction**, $O(|G|)$. Remove the nonterminals that are not [generating](/cfg-emptiness-problem/), then those that are not reachable from $S$. The order matters: removing the nonterminals that are not generating can make others unreachable, so reachability must be computed second.

## Bounds

**Chomsky normal form.** The conversion above takes $O(|G|^2)$ time and gives a grammar of size $O(|G|^2)$. The square is reached by the conversion: a chain $A_1 \to A_2 \to \cdots \to A_k$ of unit productions over $k$ binary productions of $A_k$ makes $k^2$ binary productions after UNIT, if all $A_i$ are used elsewhere.

**Greibach normal form.** Polynomial size suffices: $O(|G|^3)$ from a grammar in Chomsky normal form (Blum and Koch), so $O(|G|^6)$ through Chomsky normal form from an arbitrary grammar, and Blum and Koch give a direct bound of $O(|G|^4)$.

**Not computable.** Conversion into a right-linear grammar, or any form that captures exactly the regular languages, is not computable, because it would decide whether $L(G)$ is regular.

## Reductions

- **Membership needs a normal form.** The [CYK algorithm](/cyk-algorithm/) needs Chomsky normal form or a binary form, so the conversion is the first step of [membership](/cfg-membership-problem/) testing, and its size enters the running time $O(n^3 |G'|)$.
- **Pumping and closure proofs.** The proof of the [pumping lemma](/cfl-pumping-lemma/) uses Chomsky normal form, so that a parse tree of height $h$ has a yield of length at most $2^{h-1}$.
- **Pushdown automata.** Greibach normal form gives a [pushdown automaton](/cfg-to-pda-conversion/) that reads one input symbol on every move and has no $\varepsilon$-moves, which shows that real-time pushdown automata accept all context-free languages without $\varepsilon$.

## Applications

- **Parsing algorithms.** [CYK](/cyk-algorithm/), [Valiant's algorithm](/valiant-algorithm/) and the [inside-outside algorithm](/inside-outside-algorithm/) work on Chomsky normal form or a binary form.
- **Top-down parsers.** [Left recursion elimination](/left-recursion-elimination/) and [left factoring](/left-factoring/) bring a grammar into a shape that an [LL(1)](/ll1-parsing/) or [recursive descent](/recursive-descent-parsing/) parser accepts.
- **Proofs about context-free languages.** Normal forms simplify the proofs of the pumping lemma, of [closure properties](/cfl-closure-properties/), and of the equivalence with [pushdown automata](/cfg-pda-equivalence/).
- **Grammar learning and natural language processing.** Treebank grammars are binarized before training a [probabilistic grammar](/probabilistic-context-free-grammar/) and parsing with a CKY chart.

## References
