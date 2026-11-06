---
tag: N1FWS5
kind: technique
slug: syntax-directed-translation
name: Syntax-directed translation
aliases:
- SDT
- semantic actions
- syntax-directed definition
area: automata-and-parsing/context-free-parsing
level: core
summary: Attaches translation actions to grammar productions to compute output during parsing.
prereqs: [parse-tree, recursive-descent-parsing, shift-reduce-parsing]
see_also: [attribute-grammar, abstract-syntax-tree, topological-sort, left-recursion-elimination, slr-parsing, lalr-parsing, yacc, pratt-parsing]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 2.3, Syntax-Directed Translation (infix to postfix); Chapter 5, Syntax-Directed Translation (5.1 definitions, 5.2 evaluation orders, S-attributed and L-attributed definitions, 5.3 construction of syntax trees, 5.4 translation schemes, including the elimination of left recursion, 5.5 implementing L-attributed definitions)
  - paper: doi:10.1007/BF01692511
    title: Donald E. Knuth, Semantics of context-free languages, Mathematical Systems Theory 2(2) (1968)
    locator: pp. 127 to 145 (synthesized and inherited attributes, the binary numeral example, and the test for circularity)
  - paper: doi:10.1145/366062.366083
    title: Edgar T. Irons, A syntax directed compiler for ALGOL 60, Communications of the ACM 4(1) (1961)
    locator: pp. 51 to 55 (a compiler driven by the productions of the grammar, with a translation attached to each)
  - paper: doi:10.1145/361227.361231
    title: Mehdi Jazayeri, William F. Ogden and William C. Rounds, The intrinsically exponential complexity of the circularity problem for attribute grammars, Communications of the ACM 18(12) (1975)
    locator: pp. 697 to 706 (the test whether some parse tree has a circular dependency needs exponential time)
---

Syntax-directed translation computes the meaning of a program, or any output, from its [parse tree](/parse-tree/) by rules attached to the productions of the grammar. Each grammar symbol carries attributes, such as a value, a type or a piece of code, and each production says how the attributes of its nodes are computed from the attributes of their neighbors in the tree. The parser drives the computation. When the attributes flow only upward, a [shift-reduce parser](/shift-reduce-parsing/) computes them on its stack as it reduces; when they also flow from left to right, a [recursive descent parser](/recursive-descent-parsing/) passes them as arguments; in the general case they are evaluated in a [topological order](/topological-sort/) of their dependencies. Calculators, compilers and the actions of [yacc](/yacc/) all work this way.

## In plain words

A grammar says how a sentence is built from parts. Syntax-directed translation adds to each grammar rule a short instruction that says what the part means, given what its smaller parts mean.

For a calculator, the rule for "an expression plus a term" adds the value of the expression to the value of the term. The parser finds the parts in some order, and each time it completes a part, it runs that part's instruction. When the parser reaches the whole input, the meaning of the whole input is ready.

Sometimes information must go the other way too, from a larger part into its pieces. In a declaration such as "float x, y", the type comes first and every name after it must learn it. The pieces then receive values from their parent and left neighbors, and the order in which the instructions run matters.

## When it applies

- **The output follows the structure of the input.** Values of expressions, types of declarations, code for statements and nodes of an [abstract syntax tree](/abstract-syntax-tree/) are all computed part by part, so the rules fit on the productions.
- **The grammar is already used for parsing.** The translation reuses the parser's work: no second recognizer of the structure is needed.
- **A single pass is enough, or a tree pass is acceptable.** If every rule depends only on the children (S-attributed) or on the parent and left siblings (L-attributed), the translation runs during parsing. Otherwise the parser builds a tree first and the attributes are evaluated on it afterwards.
- **Side effects can follow the parse.** Printing output or filling a symbol table from an action works when the actions run in a known order, which the parsing method fixes.

## The template

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size.

**Attributes and rules.** Each grammar symbol $X$ has a fixed set of attributes, written $X.a$. A **syntax-directed definition** (SDD) attaches to each production $A \to X_1 \cdots X_k$ a set of semantic rules $b = f(c_1, \ldots, c_m)$, where $b$ and every $c_j$ are attributes of $A, X_1, \ldots, X_k$. When the same nonterminal occurs twice, the occurrences are numbered, as in $E \to E_1 + T$. An attribute is

- **synthesized** if, at a node for $A$, it is defined by a rule of the production at that node; it depends on the attributes of the children and of the node itself;
- **inherited** if, at a node for $X_i$, it is defined by a rule of the production at the parent; it depends on the parent and the siblings.

Terminals have synthesized attributes only, given by the lexical analyzer, for example $\mathtt{digit}.\mathit{lexval}$. On a given parse tree, each node has one instance of each attribute of its symbol, and each rule gives one equation per node.

A **translation scheme** (SDT) writes the rules as actions in braces inside the right sides, for example $E \to E_1 + T\ \{\, \mathit{print}(\text{'+'}) \,\}$. An action runs when the parser has recognized the symbols to its left. A translation scheme with all actions at the right ends is called postfix.

**The dependency graph.** For a parse tree $T$, the dependency graph has one vertex per attribute instance and an edge $c \to b$ whenever some rule computes $b$ from $c$. Any [topological order](/topological-sort/) of this graph is an evaluation order. If the graph has a cycle, the definition is circular on $T$ and has no evaluation order.

```pseudo id=main
EVALUATE-SDD(T)                                  ▷ T: a parse tree, each node labeled with its production
L1  for each node x of T and each attribute a of the symbol at x do
L2      create the instance x.a, with in-degree 0
L3  for each node x of T and each rule b = f(c1, ..., cm) of the production at x do
L4      add the edges c1 → b, ..., cm → b and raise the in-degree of b by m
L5  R ← the instances with in-degree 0
L6  while R is not empty do
L7      remove an instance b from R and set b ← f(values of its arguments)   ▷ hole: the semantic functions
L8      for each edge b → d do lower the in-degree of d by 1; if it is 0, add d to R
L9  if some instance was not computed then report "circular"
L10 return the attributes of the root
```

This general method needs the whole tree before it starts. Two restrictions remove that need, and they cover most practical uses.

**S-attributed definitions.** All attributes are synthesized. Then the children of a node are evaluated before the node, so a postorder traversal works. An LR parser visits the nodes in exactly this order: it reduces by $A \to \beta$ after it has built all subtrees of $\beta$. So it keeps a value stack next to its state stack. To reduce by $A \to X_1 \cdots X_r$, it reads the values of $X_1, \ldots, X_r$ from the top $r$ entries, pops them, and pushes the value of $A$. Yacc writes these values as `$1`, ..., `$r` and `$$`.

**L-attributed definitions.** Every inherited attribute of $X_i$ in $A \to X_1 \cdots X_k$ depends only on the inherited attributes of $A$ and on attributes of $X_1, \ldots, X_{i-1}$, and synthesized attributes are as before. Then a single depth-first traversal that visits the children from left to right works: it computes the inherited attributes of a node on the way down and the synthesized ones on the way up. A recursive descent parser makes this traversal: the function for a nonterminal takes the inherited attributes as arguments and returns the synthesized ones. Every S-attributed definition is L-attributed.

**Why the orders are correct.** In EVALUATE-SDD, an instance enters $R$ only when all its arguments are computed, so each rule is applied to computed values; if the graph is acyclic, every instance eventually enters $R$, since a topological sort of an acyclic graph lists all vertices. In the S-attributed case, every edge goes from a child to its parent or stays at one node (from a terminal's lexical value, for example), so postorder respects all edges. In the L-attributed case, every edge into an inherited attribute of $X_i$ comes from the parent's inherited attributes, computed when the traversal entered the parent, or from a left sibling, whose subtree the traversal has finished; every edge into a synthesized attribute comes from the node's children, which are finished when the traversal leaves the node.

**Cost.** For a fixed grammar, each node has a bounded number of instances and rules, so EVALUATE-SDD takes time linear in the size of the parse tree, plus the time of the semantic functions. The S-attributed and L-attributed methods add $O(1)$ work per reduction or per call to the parser. Testing whether an SDD is circular on some parse tree, rather than on one given tree, is decidable but needs exponential time in the worst case (Jazayeri, Ogden and Rounds, 1975).

## Classic examples

The values below were computed by a script that runs each definition on the input.

- **Desk calculator (S-attributed).** With the grammar $L \to E\ \mathtt{n}$, $E \to E_1 + T \mid T$, $T \to T_1 * F \mid F$, $F \to ( E ) \mid \mathtt{digit}$ and the rules $E.\mathit{val} = E_1.\mathit{val} + T.\mathit{val}$, $T.\mathit{val} = T_1.\mathit{val} \times F.\mathit{val}$, $F.\mathit{val} = \mathtt{digit}.\mathit{lexval}$ and copies for the unit productions, an [SLR parser](/slr-parsing/) reads $3 * 5 + 4\ \mathtt{n}$ and makes the reductions $F = 3$, $T = 3$, $F = 5$, $T = 15$, $E = 15$, $F = 4$, $T = 4$, $E = 19$, $L = 19$, each computed from the top of the value stack.
- **Infix to postfix (a postfix translation scheme).** $E \to E_1 + T\ \{\mathit{print}(\text{'+'})\} \mid E_1 - T\ \{\mathit{print}(\text{'-'})\} \mid T$, $T \to 0\ \{\mathit{print}(\text{'0'})\} \mid \cdots \mid 9\ \{\mathit{print}(\text{'9'})\}$. Each action runs after its operands have been printed, so $9 - 5 + 2$ prints $95\!-\!2\!+$, its [reverse Polish](/reverse-polish-notation/) form.
- **Declarations (L-attributed).** $D \to T\ L$ with $L.\mathit{inh} = T.\mathit{type}$; $T \to \mathtt{int} \mid \mathtt{float}$ with $T.\mathit{type}$ set to the keyword; $L \to L_1 , \mathtt{id}$ with $L_1.\mathit{inh} = L.\mathit{inh}$ and the action $\mathit{addType}(\mathtt{id}, L.\mathit{inh})$; $L \to \mathtt{id}$ with $\mathit{addType}(\mathtt{id}, L.\mathit{inh})$. The type flows down the list, and `float id1, id2, id3` gives all three names the type float.
- **Syntax tree construction.** Each rule builds a node from the nodes of its children, for example $E.\mathit{node} = \mathit{new\ Node}(\text{'+'}, E_1.\mathit{node}, T.\mathit{node})$. This is how most parsers produce an [abstract syntax tree](/abstract-syntax-tree/), on which later passes run.
- **Binary numerals (neither S- nor L-attributed).** Knuth's example: $N \to L_1 . L_2 \mid L$, $L \to L_1\ B \mid B$, $B \to 0 \mid 1$. Each bit has a scale $s$, its position, and the value $B.v = 2^{B.s}$ for the bit 1 and $0$ for the bit 0. The rules are $L.v = L_1.v + B.v$, $B.s = L.s$, $L_1.s = L.s + 1$, $L.l = L_1.l + 1$ (the length), $L.l = 1$ for $L \to B$, and at the root $N.v = L_1.v + L_2.v$, $L_1.s = 0$, $L_2.s = -L_2.l$. The scale of the fraction depends on its length, which is synthesized from below, so the fraction subtree must be visited twice: up for $l$, then down for $s$ and up for $v$. EVALUATE-SDD on $1101.01$ orders 31 instances and returns $13.25$.

## Variations

- **Attribute grammars.** Knuth's formalism allows only rules without side effects, which makes the meaning independent of the evaluation order; see [attribute grammar](/attribute-grammar/). Evaluators generated from it compute a static visit sequence per production, for classes such as the ordered attribute grammars.
- **Translation during an LR parse.** Yacc and Bison run the action of a production when they reduce by it. An action in the middle of a right side, as in $A \to B\ \{a\}\ C$, becomes a fresh marker $A \to B\ M\ C$, $M \to \varepsilon\ \{a\}$, and inherited attributes of $C$ are read below the marker on the value stack.
- **Translation during an LL parse.** A [recursive descent parser](/recursive-descent-parsing/) or an [LL(1) parser](/ll1-parsing/) runs actions at any position of a right side, because it predicts the production before reading it. A table-driven LL(1) parser pushes action records on its stack next to the symbols.
- **Removing left recursion from a scheme.** [Left recursion elimination](/left-recursion-elimination/) changes the shape of the tree, so the rules must change too. For $E \to E_1 + T \mid E_1 - T \mid T$ with $E.\mathit{val}$, the new grammar $E \to T\ R$, $R \to + T\ R_1 \mid - T\ R_1 \mid \varepsilon$ uses an inherited attribute: $R.\mathit{inh} = T.\mathit{val}$ in $E \to T\ R$, $R_1.\mathit{inh} = R.\mathit{inh} \pm T.\mathit{val}$, $R.\mathit{syn} = R_1.\mathit{syn}$, and $R.\mathit{syn} = R.\mathit{inh}$ for $R \to \varepsilon$. On $9 - 5 + 2$ this gives $6$, as the left-recursive definition does.
- **Operator precedence parsers.** [Pratt parsing](/pratt-parsing/) and the [shunting-yard algorithm](/shunting-yard-algorithm/) have no grammar productions, but they apply the same idea: each operator, when it is reduced, combines the values of its operands.
- **Parser combinators.** In [parser combinators](/parser-combinators/), every parser returns a value, and a combinator such as "map" attaches the semantic function to the parser of a production.

## Pitfalls

- **Wrong associativity after rewriting.** Turning $E \to E - T$ into the right-recursive $E \to T - E$ and keeping $E.\mathit{val} = T.\mathit{val} - E_1.\mathit{val}$ computes $9 - (5 + 2) = 2$ instead of $6$. Rewrite the rules with inherited attributes, as in the variation above, or parse with a loop and combine from the left.
- **Actions in the middle of a production in an LR parser.** The marker $M \to \varepsilon$ added for the action must be reduced before the parser knows which production it is in. Two productions with the same prefix and different mid-rule actions then give a [reduce-reduce conflict](/reduce-reduce-conflict/) or a [shift-reduce conflict](/shift-reduce-conflict/) that the grammar without actions does not have.
- **Reading below the stack frame.** In yacc, `$0` and negative positions read values of symbols to the left of the production. This works only if every context of the nonterminal has the same symbols there; a new production that uses the nonterminal elsewhere silently breaks it.
- **Side effects in a general evaluation order.** With EVALUATE-SDD, any topological order is valid, so actions that print or update a table can run in an unexpected order. Keep side effects in S- or L-attributed definitions, where the order is fixed, or make the rules pure.
- **Circular definitions.** A rule that makes an attribute depend on itself through a path of rules, such as an inherited attribute computed from a synthesized attribute of the same node that in turn needs the inherited one, has no evaluation order. Check the dependency graph, or check the definition once with a circularity test.
- **Backtracking parsers.** A parser that tries one alternative and backs up runs the actions of the abandoned alternative. Either defer the actions until the parse is known, or make them free of side effects.
- **Error recovery.** After a syntax error the parser may pop states or insert tokens, so actions can run with missing operands. Give the value stack a defined error value.
- **Deep recursion.** An L-attributed evaluation by recursive descent recurses once per nesting level. For long lists, write the list productions as loops that carry the inherited attribute in a variable.

## Exercises

1. Give an S-attributed definition that computes the number of `(` in a string of the grammar $S \to ( S ) S \mid \varepsilon$, and the maximum nesting depth. *Answer:* $S.c = S_1.c + S_2.c + 1$ and $S.d = \max(S_1.d + 1, S_2.d)$ for $S \to ( S_1 ) S_2$, and $S.c = S.d = 0$ for $S \to \varepsilon$.
2. Write a translation scheme that prints the prefix (Polish) form of an expression with $+$ and $*$ and digits. *Hint:* move each action to just before the first operand.
3. Show that the definition $E \to T\ R$, $R \to - T\ R_1 \mid \varepsilon$ with $R_1.\mathit{inh} = R.\mathit{inh} - T.\mathit{val}$ is L-attributed but not S-attributed, and evaluate $8 - 3 - 1$ with it. *Answer:* $R.\mathit{inh}$ is inherited; the value is $4$.
4. Convert the declaration example to an S-attributed definition by changing the grammar. *Hint:* use $D \to D_1 , \mathtt{id} \mid T\ \mathtt{id}$ and pass the type up as a synthesized attribute of $D$.
5. For Knuth's binary numerals, give the dependency graph of $10.1$ and a topological order of its instances, and show that the value is $2.5$.
6. Give an SDD that is circular on some tree but not on others. *Hint:* make the cycle pass through a rule of a production that occurs only in some trees.

## References
