---
tag: 450AQ5
kind: theorem
slug: dag-code-generation-np-completeness
name: NP-completeness of code generation for DAGs
aliases:
- Bruno-Sethi theorem
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Generating optimal code for an expression DAG on a register machine is NP-complete, unlike for trees.
prereqs: [instruction-selection-problem, expression-dag, np-complete, 3-sat]
see_also: [sethi-ullman-numbering, aho-johnson-code-generation, burs, register-allocation-np-completeness, register-allocation-problem, tree-dynamic-programming, cook-levin-theorem, maximal-munch]
sources:
  - paper: doi:10.1145/321958.321971
    title: John Bruno and Ravi Sethi, Code generation for a one-register machine, Journal of the ACM 23(3), 1976, 502-510
    locator: the one-register machine and the proof that its shortest program for a DAG is NP-complete to find
  - paper: doi:10.1145/321992.322001
    title: A. V. Aho, S. C. Johnson and J. D. Ullman, Code generation for expressions with common subexpressions, Journal of the ACM 24(1), 1977, 146-160
    locator: the NP-completeness for simple expressions and machines, the analysis of heuristics, and the algorithm for one-register machines that is exponential only in the amount of sharing
  - paper: doi:10.1137/0204020
    title: Ravi Sethi, Complete register allocation problems, SIAM Journal on Computing 4(3), 1975, 226-248
    locator: the NP-completeness of deciding whether a DAG can be computed with k registers and no stores
  - paper: doi:10.1145/292540.292562
    title: M. Anton Ertl, Optimal code selection in DAGs, Proceedings of the 26th ACM Symposium on Principles of Programming Languages (POPL 1999), 242-249
    locator: tree parsing on DAGs, and the grammars for which it gives an optimum
  - paper: doi:10.1145/1356058.1356065
    title: David Ryan Koes and Seth Copen Goldstein, Near-optimal instruction selection on DAGs, Proceedings of the 6th IEEE/ACM Symposium on Code Generation and Optimization (CGO 2008), 45-54
    locator: the proof that tiling a DAG is NP-complete, by a reduction from 3-SAT, and the NOLTIS heuristic
  - paper: "Todd A. Proebsting, Least-cost instruction selection in DAGs is NP-complete, unpublished note, 1995"
    locator: the reduction from satisfiability to tiling a DAG with tiles that may overlap
---

## Statement

A program for a basic block computes an expression DAG: a graph whose nodes are operations and whose shared nodes are common subexpressions. For trees, the cheapest code is easy to find. The [Sethi-Ullman numbering](/sethi-ullman-numbering/) gives the fewest registers, and the [Aho-Johnson algorithm](/aho-johnson-code-generation/) and [BURS](/burs/) give the cheapest tiling, in time linear in the tree for a fixed machine. For DAGs, several forms of the problem are NP-complete. Each result holds for a precise machine model, and the models differ.

**Theorem 1 (Bruno and Sethi, 1976).** Take a machine with one register, an accumulator, and unlimited memory. Its instructions load a memory word into the register, store the register into memory, and combine the register with one operand in memory, leaving the result in the register. The cost of a program is its number of instructions. Given a DAG whose leaves are in memory and an integer $K$, it is NP-complete to decide whether some program of at most $K$ instructions computes all the roots of the DAG.

**Theorem 2 (Sethi, 1975).** Take a machine with $k$ registers in which each operation reads its operands from registers and writes its result to a register, each node is computed exactly once, and no value is stored to memory. Given a DAG and $k$, it is NP-complete to decide whether the DAG can be computed in this way. This is the register sufficiency problem.

**Theorem 3 (Aho, Johnson and Ullman, 1977).** The problem of generating optimal code for expressions with common subexpressions stays NP-complete for simple expressions and simple machines. For the one-register machine they give an optimal algorithm whose time is linear in the size of the DAG and exponential only in the amount of sharing.

**Theorem 4 (tiling a DAG).** Take unlimited registers, a tree grammar that describes the instructions, and a cost for each rule. A value that is computed once can be used by all its parents. Given a DAG, the grammar and an integer $K$, it is NP-complete to decide whether the DAG has a cover of cost at most $K$. This holds even for the fixed grammar $\Gamma_0$ below, with 11 rules of cost 1, each of which covers one node.

Theorem 4 is the form of the [instruction selection problem](/instruction-selection-problem/) on DAGs. Proebsting gave a proof in 1995, and Koes and Goldstein gave one in 2008. The proof below uses its own gadget, and it is given in full. Theorems 1 to 3 are stated as in the papers.

## In plain words

When a compiler turns an expression into machine code, a value that is used in two places is a shared value. Without shared values, the expression is a tree, and the best code for a tree can be found quickly, piece by piece from the bottom.

With shared values, each shared piece must be computed in a way that suits every place that uses it. A choice that is good for one user can be bad for another. These choices interact across the whole expression, and in the worst case no method is known that avoids trying very many combinations.

This is true for several kinds of machines: a machine with one register, a machine with a fixed number of registers and no memory for temporary values, and a machine with as many registers as needed but with a menu of instructions to choose from.

## Proof

We prove Theorem 4. A *grammar* has nonterminals, a start nonterminal $S$, and rules $A \to p$ with a cost, where $p$ is a pattern: a tree of operators whose leaves are nonterminals. A *cover* of a DAG is a set of pairs $(v, r)$, where the pattern of rule $r$ matches at node $v$, such that:

1. each root of the DAG has a pair whose rule has the left side $S$;
2. for each pair $(v, r)$ and each nonterminal leaf $B$ of the pattern of $r$, matched at a node $u$, there is a pair $(u, r')$ whose rule has the left side $B$.

The cost of a cover is the sum of the costs of its rules. A node with two pairs is computed twice, once for each nonterminal, and a node with one pair is computed once and used by all its parents.

**The grammar $\Gamma_0$.** The nonterminals are $S$, $T$ and $F$. The operators are a leaf $x$, a unary NOT, and a ternary OR3. The rules, each of cost 1, are

$$T \to x, \qquad F \to x, \qquad F \to \mathrm{NOT}(T), \qquad T \to \mathrm{NOT}(F),$$

and $S \to \mathrm{OR3}(A_1, A_2, A_3)$ for each of the 7 triples $(A_1, A_2, A_3) \in \{T, F\}^3$ other than $(F, F, F)$.

**Membership in NP.** A cover never needs the same pair twice. A pattern that matches at $v$ is placed by $v$ alone, so there are at most $|V| \cdot |R|$ pairs for a DAG with $|V|$ nodes and a grammar with $|R|$ rules. A certificate is a set of pairs, and conditions 1 and 2 and the cost are checked in polynomial time.

**The reduction.** We reduce from 3-SAT with exactly three distinct variables in each clause, which is NP-complete. Let $\varphi$ have the variables $x_1, \ldots, x_n$, each of which occurs in some clause, and the clauses $C_1, \ldots, C_m$. Build the DAG $G_\varphi$:

- a node $X_i$ with the operator $x$, for each variable $x_i$;
- a node $N_i = \mathrm{NOT}(X_i)$, for each variable that occurs negated in some clause;
- a node $R_j = \mathrm{OR3}(L_{j1}, L_{j2}, L_{j3})$ for each clause, where the child for the literal $x_i$ is $X_i$ and the child for $\neg x_i$ is $N_i$.

Let $q$ be the number of nodes $N_i$, and let $K = n + q + m$, which is the number of nodes. The roots are the nodes $R_j$. The construction takes linear time.

**Lemma 1.** Each cover of $G_\varphi$ has cost at least $K$, with equality only if each node has exactly one pair.

*Proof.* Each $R_j$ is a root, so it has a pair by condition 1. Each $N_i$ is a child of some $R_j$, and every OR3 rule has a nonterminal at each child, so $N_i$ has a pair by condition 2. Each $X_i$ is a child of some $R_j$ or of $N_i$, and the rules of OR3 and NOT have a nonterminal at each child, so $X_i$ has a pair. So each of the $K$ nodes has at least one pair, and each pair costs 1. $\square$

**If $\varphi$ is satisfiable, there is a cover of cost $K$.** Let $\alpha$ be a satisfying assignment. Give $X_i$ the pair with the rule $T \to x$ if $\alpha(x_i)$ is true and $F \to x$ if it is false. Give $N_i$ the rule $F \to \mathrm{NOT}(T)$ if $\alpha(x_i)$ is true and $T \to \mathrm{NOT}(F)$ if it is false. Then each node $X_i$ or $N_i$ has the left side $T$ exactly when its literal is true, and the rule at $N_i$ finds the nonterminal that it needs at $X_i$. Give $R_j$ the rule $S \to \mathrm{OR3}(A_1, A_2, A_3)$, where $A_p$ is the left side at its $p$-th child. Since $\alpha$ satisfies $C_j$, some $A_p$ is $T$, so the triple is not $(F, F, F)$ and the rule exists. Conditions 1 and 2 hold, and there is one pair per node, so the cost is $K$.

**If there is a cover of cost at most $K$, then $\varphi$ is satisfiable.** By Lemma 1, each node has exactly one pair. Let $\alpha(x_i)$ be true if the rule at $X_i$ has the left side $T$, and false otherwise. The only pair at $N_i$ is $F \to \mathrm{NOT}(T)$ or $T \to \mathrm{NOT}(F)$. In the first case, condition 2 needs the left side $T$ at $X_i$, so $\alpha(x_i)$ is true, and $N_i$ has the left side $F$. In the second case, $X_i$ has $F$, so $\alpha(x_i)$ is false, and $N_i$ has $T$. So in both cases each literal node has the left side $T$ exactly when its literal is true under $\alpha$. The only pair at $R_j$ is $S \to \mathrm{OR3}(A_1, A_2, A_3)$, and by condition 2 each $A_p$ is the only left side at the $p$-th child. The triple is not $(F, F, F)$, so some literal of $C_j$ is true. So $\alpha$ satisfies every clause.

So $\varphi$ is satisfiable if and only if $G_\varphi$ has a cover of cost at most $K$. With membership in NP, this proves Theorem 4. $\blacksquare$

For example, the clause $x_1 \lor \neg x_2 \lor x_3$ alone gives the nodes $X_1$, $X_2$, $X_3$, $N_2$ and $R_1$, and $K = 5$. The assignment with $x_1$ true gives the cover $T \to x$ at $X_1$, any one rule at $X_2$ with the matching rule at $N_2$, any one rule at $X_3$, and the OR3 rule with $T$ first. If a second clause $\neg x_1 \lor x_2 \lor \neg x_3$ is added, $X_1$ is shared by both clauses through $N_1$, and the cover of cost $K$ must give it one left side that suits both.

## Consequences

- **No exact polynomial algorithm, unless P = NP.** The tree algorithms do not extend to DAGs. A compiler that wants the cheapest code for a block must accept exponential time in the worst case, or give up the optimum.
- **Splitting into trees.** The common answer is to cut the DAG at each shared node, store the shared value in a register, and tile each tree with the [tree dynamic program](/tree-dynamic-programming/). This is fast, but it fixes the form of each shared value in advance, which is exactly the choice that the proof shows to be hard.
- **Heuristics and exact search.** Koes and Goldstein give the NOLTIS heuristic, which tiles the DAG as if it were a tree, then fixes the shared nodes where overlap costs too much, and they report results close to the optimum. Integer programming finds the optimum for small blocks.
- **Register allocation inside a block.** Theorem 2 shows that the order of evaluation is already hard on a DAG when there is no memory for spills, while for a tree the Sethi-Ullman numbering finds it in linear time. The NP-completeness of [global register allocation](/register-allocation-np-completeness/) is a different result, about coloring the interference graph.

## Tightness

- **Trees are easy.** If the DAG is a tree, Theorem 4 is solved in linear time for a fixed grammar by the Aho-Johnson dynamic program or by BURS, and Theorem 2 by the Sethi-Ullman numbering. The hardness comes from the sharing.
- **Little sharing is easy.** The algorithm of Aho, Johnson and Ullman for the one-register machine is exponential only in the amount of sharing. So for DAGs with a bounded number of shared nodes, it runs in polynomial time.
- **Grammars matter.** With one nonterminal and rules that each cover one node, every cover with one pair per node is optimal, and the problem is trivial. The proof needs two nonterminals, $T$ and $F$, so that a shared node must make a choice that suits all its users. Ertl (1999) studied when running the tree dynamic program on the DAG, node by node, still gives an optimum, and gave a test on the grammar for this property. By Theorem 4, no such test can pass for $\Gamma_0$, unless P = NP.
- **Fixed grammar.** Theorem 4 holds for one fixed grammar of 11 rules, so the hardness does not come from a large machine description.

## History

Sethi proved the register sufficiency problem NP-complete in a paper at STOC 1973, and in the SIAM Journal on Computing in 1975. Bruno and Sethi proved the one-register result in the Journal of the ACM in 1976. Aho, Johnson and Ullman presented their results at POPL 1976 and in the Journal of the ACM in 1977, with the analysis of heuristics and the algorithm that is exponential only in the sharing. When code generator generators based on tree grammars spread in the late 1980s and early 1990s, the question came back in the form of tiling. Proebsting wrote a short proof for tiling DAGs in 1995, Ertl described the grammars for which the tree method is still optimal on DAGs in 1999, and Koes and Goldstein published a proof with a near-optimal heuristic in 2008.

## References
