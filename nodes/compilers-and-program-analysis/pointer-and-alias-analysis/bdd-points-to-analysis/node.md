---
tag: CQ8BKA
kind: technique
slug: bdd-points-to-analysis
name: BDD-based points-to analysis
aliases:
- bddbddb analysis
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: research
summary: Stores points-to relations and contexts as binary decision diagrams, which makes cloning-based context-sensitive analysis feasible.
prereqs: [andersen-analysis, context-sensitivity, reduced-ordered-bdd]
see_also: [binary-decision-diagram, variable-ordering, bdd-quantification, bdd-apply, datalog-program-analysis, semi-naive-evaluation, symbolic-model-checking, object-sensitivity]
sources:
  - paper: doi:10.1145/781131.781144
    title: Marc Berndl, Ondřej Lhoták, Feng Qian, Laurie Hendren and Navindra Umanee, Points-to analysis using BDDs, Proceedings of PLDI 2003
    locator: Andersen-style points-to analysis for Java with all relations as BDDs, relational products for the rules, incremental propagation and the study of variable orders
  - paper: doi:10.1145/996841.996859
    title: John Whaley and Monica S. Lam, Cloning-based context-sensitive pointer alias analysis using binary decision diagrams, Proceedings of PLDI 2004, 131 to 144
    locator: a clone of each method for every acyclic call path with strongly connected components merged, the context numbering, the Datalog rules and the bddbddb engine
  - paper: doi:10.1145/1640089.1640108
    title: Martin Bravenboer and Yannis Smaragdakis, Strictly declarative specification of sophisticated points-to analyses, Proceedings of OOPSLA 2009
    locator: the Doop framework, which runs the same kind of Datalog rules on explicit tuples with indexing and compares its speed with BDD-based tools
---

A BDD-based points-to analysis stores every relation of a pointer analysis as a [reduced ordered BDD](/reduced-ordered-bdd/). Examples are "variable $v$ may point to object $h$", "$v_1 = v_2$ appears in the program" and "in context $c$, call site $i$ calls method $m$". Each element of a domain gets a binary number, so a relation over several domains becomes a Boolean function of their bits. The rules of the analysis, such as those of [Andersen's analysis](/andersen-analysis/), turn into a few BDD operations on whole relations: conjunction, [existential quantification](/bdd-quantification/) and renaming of bits. A BDD can be much smaller than the set of tuples it stands for, when the tuples share structure. Berndl, Lhoták, Qian, Hendren and Umanee (2003) showed that this works for Andersen's analysis of Java. Whaley and Lam (2004) used it to make a [context-sensitive](/context-sensitivity/) analysis that clones every method for every acyclic call path feasible. They wrote the rules in Datalog and compiled them to BDD operations with their bddbddb engine.

## In plain words

A pointer analysis works with large tables, such as which variable may point to which object. With many contexts, these tables get far too big to store row by row. A binary decision diagram stores a table as a small graph that answers "is this row in the table?" one bit at a time. When many rows are alike, for example the same objects in a million contexts, the graph shares the common parts and stays small. The analysis rules then work on whole tables at once. "If a variable gets the value of another variable, it may point to everything that one points to" becomes one join of two tables. The analysis repeats these joins until the tables stop growing. The answer is the same as with plain tables. Only the storage and the speed change.

## When it applies

- The analysis is a set of rules over finite relations, as in [Datalog program analysis](/datalog-program-analysis/): every fact is a tuple of program elements and every rule joins a few relations.
- The relations are large but regular. Context-sensitive analyses are the main case: the facts of one method are often the same, or nearly the same, in many contexts.
- The domains can be numbered so that related elements get related numbers, for example variables of one method next to each other, or the contexts of one method as one range of numbers.
- A good order of the BDD variables can be found. The size of a BDD depends heavily on the [variable order](/variable-ordering/), and a bad order can make the BDDs larger than the plain tables.

## The template

Notation: a domain $D$, such as variables $V$, objects $H$ or contexts $C$, is encoded with $\lceil \log_2 |D| \rceil$ bits. A relation with attributes $(a_1, \ldots, a_r)$ is a BDD over the bits of these attributes. One domain can appear in several attributes, such as $V_1$ and $V_2$ for the two sides of a copy, and each attribute has its own bits. RENAME moves a BDD from the bits of one attribute to the bits of another. The holes are RULES, the Datalog rules of the analysis, and ORDER, the bit widths and the order of all bits.

```pseudo id=main
BDD-ANALYSIS(facts, RULES)
L1  ORDER: fix the bits of each attribute and one order of all bits
L2  encode each input relation as a reduced ordered BDD under ORDER
L3  for each derived relation R, set R to the union of its rules with no derived body relation, and set delta(R) = R
L4  repeat
L5      for each rule R(head) :- B1(...), B2(...) of RULES with B1 derived do
L6          T = RENAME(delta(B1), to the attributes that B1 has in the rule)
L7          T = EXISTS(the attributes of the body that are not in the head, T AND B2)
L8          T = RENAME(T, to the attributes of R)
L9          new(R) = new(R) OR (T AND NOT R)
L10     for each derived R do R = R OR new(R); delta(R) = new(R); new(R) = false
L11 until delta(R) is false for every derived R
L12 return the derived relations
```

Line L7 is the *relational product*: a conjunction followed by existential quantification of the join attributes. BDD packages do it in one pass, without building the conjunction first. Lines L9 and L10 are [semi-naive evaluation](/semi-naive-evaluation/): each round joins only the new tuples of the last round, kept in $delta(R)$. A rule with two derived body relations needs two versions, one with $delta(B_1)$ and the full $B_2$, and one the other way round. A rule with three body relations needs two relational products. The loop stops because every relation only grows inside a finite set of tuples, and the result is the least model of the rules, which is the same as with explicit tuples. Only the cost depends on ORDER.

For Andersen's analysis of Java, RULES are these four rules, with $vP$ for "variable points to object" and $hP$ for "field of object points to object":

| rule | meaning |
|---|---|
| $vP(v, h) \mathrel{:-} vP_0(v, h)$ | an allocation $v = $ `new` at site $h$ |
| $vP(v_1, h) \mathrel{:-} assign(v_1, v_2), vP(v_2, h)$ | a copy $v_1 = v_2$ |
| $hP(h_1, f, h_2) \mathrel{:-} store(v_1, f, v_2), vP(v_1, h_1), vP(v_2, h_2)$ | a store $v_1.f = v_2$ |
| $vP(v_2, h_2) \mathrel{:-} load(v_1, f, v_2), vP(v_1, h_1), hP(h_1, f, h_2)$ | a load $v_2 = v_1.f$ |

For the copy rule, line L6 renames $delta(vP)$ from $(V_1, H)$ to $(V_2, H)$. Line L7 conjoins it with $assign(V_1, V_2)$ and quantifies $V_2$ away, which leaves a BDD over $(V_1, H)$. Line L8 has nothing to rename, since the head is already over $(V_1, H)$.

## Classic examples

**A small copy chain.** Take this Java fragment, with two allocation sites.

```
p = new A();   // h0
q = new B();   // h1
r = p;
r = q;
s = r;
```

Encode $V$ with two bits $v_1 v_0$: $p = 00$, $q = 01$, $r = 10$, $s = 11$, and $H$ with one bit $b$: $h_0 = 0$, $h_1 = 1$. Then $vP_0$ is the function $(\lnot v_1 \land \lnot v_0 \land \lnot b) \lor (\lnot v_1 \land v_0 \land b)$. The first round of the copy rule joins $assign = \{(r, p), (r, q), (s, r)\}$ with $vP_0$ and finds $(r, h_0)$ and $(r, h_1)$. As a function this is $v_1 \land \lnot v_0$, with no test on $b$ at all, because $r$ points to both objects. The second round finds $s$ the same way, $v_1 \land v_0$. The third round finds nothing new, because no copy reads $s$. The final relation is $vP = vP_0 \lor v_1$: the four tuples of $r$ and $s$ are one test on one bit. In a real program the same effect, at a much larger scale, comes from many contexts or many variables that share the same objects.

**Andersen's analysis.** With the four rules above and no contexts, the template is [Andersen's analysis](/andersen-analysis/) for Java. Berndl and colleagues computed it this way, also building the call graph on the fly from virtual calls, and studied how the order of the bits of $V$, $H$ and the fields affects the size of the BDDs. Interleaving the bits of attributes that are often compared, such as $V_1$ and $V_2$, is a common choice.

**Cloning-based context sensitivity.** Whaley and Lam take the call graph from a context-insensitive run, merge each strongly connected component into one node, and give each acyclic path from the entry its own context. Large Java programs have more than $10^{14}$ such paths. They number the contexts of each method as one range, so that a call edge maps a range of caller contexts to a range of callee contexts by adding a constant. That mapping is a small BDD over $(C_1, C_2)$. With an extra attribute $C$ on each relation, the four rules above become a [context-sensitive](/context-sensitivity/) analysis, and the plain clones would never fit in memory.

**Object sensitivity.** The context attribute can hold receiver objects instead of call paths. Lhoták and Hendren's Paddle framework ran call-site and [object-sensitive](/object-sensitivity/) variants of the same rules on BDDs, to compare them on the same programs.

**Symbolic model checking.** The same template computes the reachable states of a transition system: the states are bit vectors, the transition relation is a BDD over current and next bits, and one round is a relational product followed by a rename. This is [symbolic model checking](/symbolic-model-checking/), where the technique comes from.

## Variations

- **Datalog front ends.** bddbddb compiles Datalog rules into BDD operations and chooses the order of the operations. Jedd, by Lhoták and Hendren, adds relations as a type to Java and compiles the operations on them to BDD calls.
- **Finding a good order.** The order of bits is found by trying candidates, by heuristics that interleave attributes that are joined together, or by machine learning over the orders tried. A fixed order that is good for one program can be bad for another.
- **Explicit tuples.** Bravenboer and Smaragdakis ran the same kind of rules for Java on explicit tuples with careful indexing in their Doop framework, and found it faster than the BDD-based tools on the analyses they compared. Later Datalog engines for analysis, such as Soufflé, use explicit tuples too. BDDs still win when the relations are huge and very regular.
- **Other decision diagrams.** Zero-suppressed decision diagrams store sparse sets more compactly than BDDs and have been tried for the same relations.

## Pitfalls

- **A bad variable order.** With all bits of $V$ before all bits of $H$, a relation that pairs each variable with an unrelated object needs a separate subgraph for each variable, and the BDD can be as large as the table. Pick an order in which bits of attributes that depend on each other are close, and measure several orders.
- **Forgetting the rename.** Without line L6, $delta(vP)$ stays over $(V_1, H)$, and the conjunction with $assign(V_1, V_2)$ joins on the wrong attribute: it pairs $v_1$ with its own objects. Each relation needs its own bits for each attribute it plays in a rule, and the rename puts them in place.
- **Joining full relations each round.** Using $R$ instead of $delta(R)$ at line L6 gives the same result but repeats all the old joins in every round. Keep the new tuples apart, as in lines L9 and L10.
- **Counting tuples by enumeration.** A context-sensitive relation with $10^{14}$ contexts cannot be listed. Ask the questions of the client, such as "may these two variables alias in some context?", as more BDD operations, and count tuples with the BDD satisfying count, not by listing.
- **Claiming soundness with reflection.** The result is the least model of the rules for the facts given. Code reached through reflection, native methods or dynamic class loading is not covered unless the facts model it.

## Exercises

1. In the copy chain example, add `t = s;` and the variable $t$ with code $100$, so $V$ needs three bits. Write $vP$ as a Boolean function after the fixed point and count its BDD nodes for the order $v_2, v_1, v_0, b$.
2. Write the four Andersen rules with an extra context attribute $C$ for cloning-based context sensitivity. Which relation maps caller contexts to callee contexts, and in which rules does it appear?
3. Contexts of a method $m$ are numbered $0$ to $k - 1$ in its range. A call edge from $m$ to $n$ maps context $i$ of $m$ to context $i + s$ of $n$. Show that the relation $\{(i, i + s) : 0 \le i < k\}$ has a BDD with $O(w)$ nodes for each fixed $s$ and $k$ when the bits of the two attributes are interleaved, where $w$ is the number of bits, and that it can need exponentially many nodes in $w$ when all bits of one attribute come first.
4. Show that the template with semi-naive evaluation computes the same relations as plain iteration of all rules on full relations.

## References
