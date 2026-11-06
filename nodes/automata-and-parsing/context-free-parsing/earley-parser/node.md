---
tag: X30PDD
kind: algorithm
slug: earley-parser
name: Earley parser
aliases:
- Earley's algorithm
area: automata-and-parsing/context-free-parsing
level: core
summary: Chart-based parser handling all context-free grammars in cubic time, linear for unambiguous ones.
solves: [context-free-language-recognition, cfg-membership-problem, cfg-parsing-problem]
model: word-ram
complexity:
  vars: {n: the length of the input string, G: the grammar size (the sum over all productions of the right side length plus one)}
  time: {worst: O(n^3 G), best: O(n G), unambiguous: O(n^2 G)}
  space: {extra: O(n^2 G)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1968
  people: [Jay Earley]
  note: Earley described the algorithm in his 1968 doctoral thesis at Carnegie Mellon University and published it in Communications of the ACM in 1970.
prereqs: [context-free-grammar, derivation, nullable-symbol]
see_also: [cyk-algorithm, chart-parsing, parse-chart, glr-parsing, shared-packed-parse-forest, lr-item, left-corner-parsing, valiant-algorithm]
sources:
  - paper: doi:10.1145/362007.362035
    title: Jay Earley, An efficient context-free parsing algorithm, Communications of the ACM 13(2) (1970)
    locator: pp. 94 to 102 (the recognizer, the time bounds n^3, n^2 for unambiguous grammars and linear on a large class)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 7.2, Earley Parsing (7.2.3 Handling Epsilon-Rules); Section 7.3, Chart Parsing
  - paper: doi:10.1093/comjnl/45.6.620
    title: John Aycock and R. Nigel Horspool, Practical Earley parsing, The Computer Journal 45(6) (2002)
    locator: pp. 620 to 630 (the nullable-prediction rule for empty productions)
  - paper: doi:10.1016/0304-3975(91)90180-A
    title: Joop M. I. M. Leo, A general context-free parsing algorithm running in linear time on every LR(k) grammar without using lookahead, Theoretical Computer Science 82(1) (1991)
    locator: pp. 165 to 176
  - paper: doi:10.1145/357103.357112
    title: Susan L. Graham, Michael A. Harrison and Walter L. Ruzzo, An improved context-free recognizer, ACM Transactions on Programming Languages and Systems 2(3) (1980)
    locator: pp. 415 to 462 (the relation between Earley's algorithm and CYK)
---

The Earley parser decides whether a string is in the language of any [context-free grammar](/context-free-grammar/), with no normal form required, and finds a [parse tree](/parse-tree/) when it is. It reads the input from left to right and keeps, for each position, a set of dotted productions called items, which record every way the input read so far can continue to a derivation. It takes $O(n^3)$ time in general, $O(n^2)$ on unambiguous grammars and $O(n)$ on many grammars of programming languages, so it is the usual choice of a general parser that is also fast on easy inputs.

## In plain words

The parser reads the input one symbol at a time. Before each symbol, it keeps a list of partial rules: "I am in the middle of this rule, I started it at that position, and this part of the rule is already matched". Three steps grow the lists.

Prediction: when a partial rule waits for a placeholder, start every rule of that placeholder at the current position.

Scanning: when a partial rule waits for the next input symbol and that symbol comes, move the rule past it into the next list.

Completion: when a rule is finished, go back to the list where it started, find every partial rule that waited for its placeholder, and move them past it.

The input is in the language when, at the end, a rule for the start symbol is finished and started at the beginning.

## The problem

The input is a grammar $G = (V, \Sigma, P, S)$ and a string $w = a_1 a_2 \cdots a_n \in \Sigma^*$. We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the input length, and $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$ the grammar size. The grammar may have empty productions, unit productions, left recursion, cycles $A \Rightarrow^+ A$ and ambiguity.

The recognizer outputs yes when $S \Rightarrow^* w$ and no otherwise ([membership problem](/cfg-membership-problem/)). The parser also outputs one parse tree ([parsing problem](/cfg-parsing-problem/)).

## The algorithm

An **item** $[A \to \alpha \bullet \beta,\ i]$ is a production $A \to \alpha\beta$ with a dot in its right side and an **origin** $i \in \{0, \ldots, n\}$. There are exactly $|G|$ dotted productions, one for each choice of production and dot position. The algorithm builds sets $E[0], \ldots, E[n]$ (the [parse chart](/parse-chart/)) so that

$$[A \to \alpha \bullet \beta,\ i] \in E[j] \iff \alpha \Rightarrow^* a_{i+1} \cdots a_j \text{ and } S \Rightarrow^* a_1 \cdots a_i\, A\, \gamma \text{ for some } \gamma.$$

The first condition says that the part before the dot matches the input between positions $i$ and $j$. The second says that $A$ can start at position $i$ in a derivation consistent with the input before it. A [nullable](/nullable-symbol/) nonterminal is one that derives $\varepsilon$.

```pseudo id=main
EARLEY(G, w)                                 ▷ w = a1 … an
L1  NULLABLE ← { A ∈ V : A ⇒* ε }
L2  E[0], …, E[n] ← ∅
L3  for each S → α in P do add [S → • α, 0] to E[0]
L4  for j ← 0 to n do
L5      for each item [A → α • β, i] in E[j], in the order of insertion, do   ▷ E[j] grows during the loop
L6          if β = ε then                    ▷ complete, once for each pair (A, i) in E[j]
L7              for each [B → γ • A δ, k] in E[i] do add [B → γ A • δ, k] to E[j]
L8          else if β = X β′ with X ∈ V then  ▷ predict
L9              if X is not yet predicted in E[j] then for each X → η in P do add [X → • η, j] to E[j]
L10             if X ∈ NULLABLE then add [A → α X • β′, i] to E[j]
L11         else if j < n and β = a_{j+1} β′ then   ▷ scan
L12             add [A → α a_{j+1} • β′, i] to E[j + 1]
L13 return true if [S → α •, 0] ∈ E[n] for some S → α in P, else false
```

"Add" does nothing when the item is already in the set. Line L1 computes the nullable nonterminals by the least fixed point: $A$ is nullable when some production $A \to X_1 \cdots X_k$ has every $X_i$ nullable, $k = 0$ included. Line L10 is the rule of Aycock and Horspool. Without it, line L7 with $i = j$ reads $E[j]$ while $E[j]$ still grows, and misses items $[B \to \gamma \bullet A \delta, k]$ that arrive after the completion of a nullable $A$.

To build a parse tree, each item keeps the reason for its first insertion: the item it came from, plus the scanned terminal (line L12), the completed item (line L7) or the nullable nonterminal (line L10). Following these pointers from an item $[S \to \alpha \bullet, 0] \in E[n]$ back to its dot-zero item lists the children of the root, and the completed items among them give the subtrees. Each pointer leads to an item inserted earlier, so the walk ends, even for grammars with cycles that have infinitely many trees. A nullable nonterminal gets a fixed tree for $\varepsilon$, built from the productions in the order in which line L1 found them nullable. The implementation walks the pointers with an explicit stack.

## Example

Take the grammar with productions numbered 0 to 3

$$E \to E + T \mid T, \qquad T \to a \mid \varepsilon,$$

which has left recursion and an empty production, and $w = a + a$, so $n = 3$. Both $E$ and $T$ are nullable. The sets, in the order of insertion, are:

| set | item | inserted by |
|---|---|---|
| $E[0]$ | $[E \to \bullet E + T,\ 0]$ | L3 |
| | $[E \to \bullet T,\ 0]$ | L3 |
| | $[E \to E \bullet + T,\ 0]$ | L10, $E$ nullable |
| | $[T \to \bullet a,\ 0]$ | L9, predict $T$ |
| | $[T \to \bullet,\ 0]$ | L9, predict $T$ |
| | $[E \to T \bullet,\ 0]$ | L10, $T$ nullable |
| $E[1]$ | $[T \to a \bullet,\ 0]$ | L12, scan $a$ |
| | $[E \to T \bullet,\ 0]$ | L7, complete $T$ from 0 |
| | $[E \to E \bullet + T,\ 0]$ | L7, complete $E$ from 0 |
| $E[2]$ | $[E \to E + \bullet T,\ 0]$ | L12, scan $+$ |
| | $[T \to \bullet a,\ 2]$ | L9, predict $T$ |
| | $[T \to \bullet,\ 2]$ | L9, predict $T$ |
| | $[E \to E + T \bullet,\ 0]$ | L10, $T$ nullable |
| | $[E \to E \bullet + T,\ 0]$ | L7, complete $E$ from 0 |
| $E[3]$ | $[T \to a \bullet,\ 2]$ | L12, scan $a$ |
| | $[E \to E + T \bullet,\ 0]$ | L7, complete $T$ from 2 |
| | $[E \to E \bullet + T,\ 0]$ | L7, complete $E$ from 0 |

In $E[0]$ the prediction of $E$ by the first item adds nothing new, because both productions of $E$ are already there. $E[2]$ shows that $a +$ is a prefix of the language and that $a +$ alone is a sentence, since $[E \to E + T \bullet, 0] \in E[2]$. Line L13 finds $[E \to E + T \bullet, 0] \in E[3]$, so $a + a$ is in the language. The back pointers give the tree $E \to E + T$ with $E \to T \to a$ on the left and $T \to a$ on the right.

## Correctness

**Claim.** When the loop of line L4 ends, each $E[j]$ is exactly the set of items described by the equivalence above. Then line L13 returns true if and only if some $S \to \alpha$ has $\alpha \Rightarrow^* a_1 \cdots a_n$, that is, if and only if $w \in L(G)$.

The proof has three parts. First, each line inserts only items that satisfy the two conditions, by a direct derivation argument for each of lines L3, L7, L9, L10 and L12. Second, the valid items are exactly the items generated from line L3 by the three rules predict, scan and complete, by induction on the length of a derivation that witnesses validity. Third, the sets are closed under these rules: every item of $E[j]$ is processed, $E[i]$ is final when a completion with $i < j$ reads it, and a completion with $i = j$ concerns a nullable nonterminal, which line L10 covers. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Items are hashed for the test "already in the set", and the items of each set are also indexed by the symbol after the dot, so line L7 reads only the items that wait for $A$.

**Size of the chart.** $E[j]$ holds at most $|G|\,(j + 1)$ items, one for each dotted production and origin $i \le j$. So the chart holds at most $|G|\,(n + 1)(n + 2)/2 = O(n^2 |G|)$ items, and the space is $O(n^2 |G|)$.

**Time.** Fix $j$. Lines L9 run at most once for each nonterminal $X$, and add at most $|G|$ items in total. Lines L10 to L12 take $O(1)$ for each item. Line L7 runs once for each pair $(A, i)$, and reads the items of $E[i]$ that wait for $A$. Summed over all $A$, these are at most all items of $E[i]$, so the completions in $E[j]$ cost at most $\sum_{i \le j} |G|\,(i + 1) = O(j^2 |G|)$. Summed over $j$, the time is $O(n^3 |G|)$. Line L1 takes $O(|G|^2)$ time with the plain fixed point and $O(|G|)$ with a worklist.

**Better bounds.** Earley proved $O(n^2)$ time for unambiguous grammars. Assume no symbol is useless, so every valid item extends to some sentence. If line L7 adds the same item $[B \to \gamma A \bullet \delta, k]$ to $E[j]$ from two different origins $i$ of $A$, the two splits of $a_{k+1} \cdots a_j$ give two parse trees of a sentence. So each item of $E[j]$ is added by completion at most once, apart from the one extra add of line L10, and the completions of a set cost $O(j |G|)$ instead of $O(j^2 |G|)$, for $O(n^2 |G|)$ in all. He also showed linear time for a large class of grammars, which includes most grammars of programming languages. Right recursion breaks the linear bound: for $S \to a S \mid \varepsilon$ and $w = a^n$, the set $E[j]$ holds $[S \to a S \bullet, i]$ for every $i < j$, about $n^2/2$ items in all, while the left-recursive $S \to S a \mid \varepsilon$ gives $2n + 3$ items. Leo's 1991 modification stores only the top of each such chain of completions and runs in $O(n)$ time on every [LR(k) grammar](/lr-grammar/).

## Properties

- **General.** It accepts every context-free grammar as it is. [CYK](/cyk-algorithm/) needs [Chomsky normal form](/chomsky-normal-form/), and LR or LL parsers need grammars without conflicts.
- **Online, with the prefix property.** $E[j]$ depends only on $a_1 \cdots a_j$. For a grammar without [useless symbols](/useless-symbol-elimination/), $E[j]$ is nonempty exactly when $a_1 \cdots a_j$ is a prefix of some word of the language. So the parser reports a syntax error at the first symbol that cannot continue any sentence.
- **Adaptive.** Its running time adjusts to the grammar and the input: linear on many deterministic grammars, quadratic on unambiguous ones, cubic only in the worst case.
- **Deterministic.** The sets are a function of the grammar and the input. The order of insertion depends on the order of the productions, but the sets do not.

## Variants and improvements

- **Lookahead.** Earley's paper attaches $k$ symbols of lookahead to the items to filter completions. A lookahead test at prediction time, against the [FIRST sets](/first-and-follow-sets/) of the predicted productions, is a common alternative that keeps the sets smaller.
- **Leo's right-recursion fix.** Leo's modification keeps, for each deterministic chain of completions, only the topmost item, and gives linear time on all LR(k) grammars and on the larger class of LR-regular grammars.
- **Practical Earley parsing.** Aycock and Horspool combine the nullable rule of line L10 with a precomputed LR(0)-like automaton whose states group items, which cuts the number of items per set.
- **Parse forests.** Keeping all reasons for each item instead of the first gives every parse. A [shared packed parse forest](/shared-packed-parse-forest/) stores them in $O(n^3)$ space for a fixed grammar.
- **Matrix form.** Graham, Harrison and Ruzzo write Earley's sets as an upper triangular matrix indexed by origin and position, which shows the link with [CYK](/cyk-algorithm/) and gives an $O(n^3 / \log n)$ bound with the Four Russians method. [Valiant's algorithm](/valiant-algorithm/) reaches $O(n^\omega)$ on the CYK form.
- **Chart parsing.** [Chart parsing](/chart-parsing/) generalizes the three rules to any order of processing, such as bottom-up or best-first agendas.

## When to use it

Use Earley's algorithm when the grammar is not under your control, when it is ambiguous or left-recursive, or when it changes at run time, as in grammar development tools, natural-language processing and parsers for domain-specific languages. It needs no grammar transformation, so the parse trees are in terms of the original grammar. For a fixed programming-language grammar in the [LALR(1)](/lalr-parsing/) or [LL(1)](/ll1-parsing/) class, a deterministic parser is faster by a constant factor and uses $O(n)$ space. For very ambiguous grammars where all parses are needed, consider [GLR parsing](/glr-parsing/), which is faster on near-deterministic grammars.

## Pitfalls

- **Empty productions.** Completing a nullable $A$ at its own origin while $E[j]$ still grows loses items. With $S \to A A a$ and $A \to \varepsilon$, the item $[S \to A \bullet A a, 0]$ enters $E[0]$ after $A$ was completed from 0, so without line L10 the input $a$ is rejected. Either keep line L10 or repeat the completions of $E[j]$ until nothing changes.
- **Iterating over a set while it changes.** Line L5 must also visit items added during the loop. A `for` loop over a copy of $E[j]$ misses them.
- **Deduplicating by production only.** Two items with the same dotted production but different origins are different items. Keying the set by the dotted production alone merges unrelated derivations.
- **Following all back pointers naively.** With cyclic grammars such as $S \to S \mid a$, a string has infinitely many trees. Use the pointers of first insertion for one tree, or build a forest with shared nodes.
- **Recursion depth.** The tree of $a^n$ under $S \to a S \mid a$ has depth $n$. Build trees with an explicit stack.

## Implementations

## History

Jay Earley gave the algorithm in his 1968 doctoral thesis at Carnegie Mellon University and published it in Communications of the ACM in 1970, with the bounds $n^3$ in general, $n^2$ for unambiguous grammars and linear time on a large class. Graham, Harrison and Ruzzo related it to CYK in 1980. Leo made it linear on all LR(k) grammars in 1991, and Aycock and Horspool gave the simple treatment of empty productions in 2002. The idea of a chart of partial constituents became the basis of [chart parsing](/chart-parsing/) in computational linguistics.

## References
