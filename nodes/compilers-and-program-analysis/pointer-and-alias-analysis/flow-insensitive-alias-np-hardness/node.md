---
tag: XYGBP7
kind: theorem
slug: flow-insensitive-alias-np-hardness
name: NP-hardness of precise flow-insensitive alias analysis
aliases:
- Horwitz alias hardness
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: research
summary: Deciding precise flow-insensitive may-alias is NP-hard, even with no dynamic memory, when statements may dereference a pointer many times.
prereqs: [alias-analysis, np-hard, hamiltonian-path-problem]
see_also: [may-alias-undecidability, andersen-analysis, steensgaard-analysis, points-to-analysis, flow-sensitivity, polynomial-time-reduction, hamiltonian-path, np-complete]
sources:
  - paper: doi:10.1145/239912.239913
    title: Susan Horwitz, Precise flow-insensitive may-alias analysis is NP-hard, ACM Transactions on Programming Languages and Systems 19(1), 1 to 6 (1997)
    locator: whole paper (the NP-hardness proof for programs with arbitrary levels of pointers and arbitrary pointer dereferencing)
  - paper: doi:10.1145/604131.604142
    title: Venkatesan T. Chakaravarthy, New results on the computability and complexity of points-to analysis, Proceedings of the 30th ACM Symposium on Principles of Programming Languages (POPL 2003), 115 to 125
    locator: the results on flow-insensitive analysis (NP-hard with scalar variables and no dynamic memory, polynomial for programs with well-defined types)
  - paper: doi:10.1145/1353445.1353447
    title: Noam Rinetzky, G. Ramalingam, Mooly Sagiv and Eran Yahav, On the complexity of partially-flow-sensitive alias analysis, ACM Transactions on Programming Languages and Systems 30(3), Article 13 (2008)
    locator: the introduction and the discussion of earlier results (the number of memory accesses per statement in Horwitz's proof, and the PSPACE-completeness of flow-sensitive may-alias without dynamic allocation)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness (1979)
    locator: the Hamiltonian circuit and Hamiltonian path problems in the graph theory part of the appendix (GT37 to GT39)
---

Precise flow-insensitive may-alias analysis is [NP-hard](/np-hard/). A flow-insensitive analysis may run the statements of a program in any order, any number of times, and the precise question asks whether some such run makes two expressions name the same location. Horwitz proved in 1997 that this question is NP-hard even when the program has no dynamic memory. So the fast flow-insensitive analyses, [Andersen's](/andersen-analysis/) in cubic time and [Steensgaard's](/steensgaard-analysis/) in almost linear time, cannot be precise for this semantics unless P = NP. The proof needs statements that dereference a pointer many times. This page proves the theorem by its own short reduction from the [Hamiltonian path problem](/hamiltonian-path-problem/), not by Horwitz's construction.

## Statement

**Programs.** A program is a finite set of statements over a finite set $V$ of variables. There are no procedures and no dynamic allocation. At each moment a variable holds nothing or the address of one variable. Write $*^k p$ for $p$ with $k \ge 0$ stars in front. A statement has the form $*^i p = \&a$ or $*^i p = *^j q$ with $i, j \ge 0$. In a state $\sigma$, the expression $*^0 p = p$ names the location $p$, and $*^{k+1} p$ names the location $\sigma(\ell)$ held by the location $\ell$ that $*^k p$ names. If some location on the way holds nothing, the expression names nothing. The statement $*^i p = e$ writes the value of $e$ into the location that $*^i p$ names. Here the value of $\&a$ is $a$, and the value of $*^j q$ is the content of the location that $*^j q$ names.

**Flow-insensitive semantics.** A run starts in the state where no variable holds anything, and it executes any finite sequence of the statements, with repeats. A statement whose expressions name nothing, or whose right side has no value, does not run. Every path of a real control flow graph over these statements is such a sequence, so this semantics covers every order of the statements. It ignores the order; it does not ignore which statements the program has.

**The problem.** *Precise flow-insensitive may-alias:* given a program and two expressions $e_1$ and $e_2$, is there a run after which $e_1$ and $e_2$ name the same location? The points-to form asks whether $p$ may hold the address of $a$, which is the alias question for $*p$ and $a$.

**Theorem (Horwitz 1997).** Precise flow-insensitive may-alias is NP-hard. It is NP-hard even for programs where every statement but one has the form $u = \&v$, the remaining statement has the form $r = *^k s$, and the question is whether $r$ may point to a given variable $t$.

## In plain words

Pretend that the statements of a program can run in any order, as often as you like. Can two pointer expressions ever end up naming the same memory cell? With no memory allocation, the number of possible states is finite, so this question can be answered by a search. But the search can take a very long time. The theorem says that the question is as hard as the hardest search problems in NP, such as finding a route that visits every city once. The proof turns a route question into a program. Each road becomes a statement that makes one city point to the next. One long statement follows the pointers from the start city many times. It reaches the end city only when the pointers form a route through all the cities.

## Proof

**The source problem.** The *directed Hamiltonian path problem with fixed ends* asks, for a directed graph $G = (N, E)$ and distinct nodes $s$ and $t$, whether $G$ has a path from $s$ to $t$ that visits every node exactly once. It is NP-complete (Garey and Johnson, problems GT37 to GT39). For example, the directed Hamiltonian circuit problem reduces to it: pick a node $v$, split it into a node $v_{out}$ with the out-edges of $v$ and a node $v_{in}$ with the in-edges of $v$, and ask for a path from $v_{out}$ to $v_{in}$.

**The construction.** Let $n = |N| \ge 2$. Make one variable for each node, and one more variable $r$. The program has the statements

- $u = \&v$ for each edge $(u, v) \in E$ with $u \ne t$, and
- $r = *^{n-2} s$.

The question is whether $r$ may point to $t$. The program has $|E| + 1$ statements and size $O(|E| + n)$, so it is built in polynomial time.

In the state $\sigma$ where the last statement runs, put $y_0 = s$ and $y_{k+1} = \sigma(y_k)$. Then $*^k s$ names $y_k$, so the value of $*^{n-2} s$ is $y_{n-1}$, and the statement gives $r$ the value $y_{n-1}$.

**Claim.** Some run makes $r$ point to $t$ if and only if $G$ has a Hamiltonian path from $s$ to $t$.

*If.* Let $s = x_0, x_1, \ldots, x_{n-1} = t$ be a Hamiltonian path. For $i < n - 1$ the node $x_i$ is not $t$, so the program has the statement $x_i = \&x_{i+1}$. Run these $n - 1$ statements, and then $r = *^{n-2} s$. In that state $y_k = x_k$ for every $k \le n - 1$, so $r$ gets the value $x_{n-1} = t$.

*Only if.* The variable $r$ gets a value only from the last statement, and no statement takes the address of $r$. So in some run, the last statement runs in a state $\sigma$ with $y_{n-1} = t$, where $y_0, \ldots, y_{n-1}$ are all defined, and $y_1, \ldots, y_{n-1}$ are node variables. Each value $\sigma(u) = v$ of a node variable comes from a statement $u = \&v$, so $(y_k, y_{k+1}) \in E$ for every $k < n - 1$.

The nodes $y_0, \ldots, y_{n-1}$ are distinct. Suppose $y_i = y_j$ with $i < j \le n - 1$, and put $d = j - i$. Since $\sigma$ is a function, $y_{k+d} = y_k$ for every $k \ge i$ for which both are defined. Then $t = y_{n-1} = y_{n-1-d}$, and $i \le n - 1 - d < n - 1$, so $\sigma(t) = y_{n-d}$ is defined. But no statement gives $t$ a value, because the statements of the out-edges of $t$ were left out. This is a contradiction.

So $y_0, \ldots, y_{n-1}$ are the $n$ nodes in some order, joined by edges, from $s$ to $t$: a Hamiltonian path. $\square$

The claim gives a [polynomial-time reduction](/polynomial-time-reduction/) from an NP-complete problem, so precise flow-insensitive may-alias is NP-hard. The reduction makes only statements of the two forms in the theorem, and the question is a points-to question. $\square$

**An upper bound.** The problem is in PSPACE. A state maps each of the $n$ variables to one of $n + 1$ values, so there are at most $(n+1)^n$ states, and a state fits in $O(n \log n)$ bits. A nondeterministic search guesses the run one statement at a time, keeps only the current state, and checks the question at each step. By Savitch's theorem, nondeterministic polynomial space is the same as deterministic polynomial space. The theorem gives only the lower bound.

## Consequences

**Fast analyses are not precise.** Andersen's analysis takes $O(n^3)$ time and Steensgaard's analysis takes almost linear time. Both are sound for the flow-insensitive semantics, so unless P = NP, neither gives the precise answer on all programs. The loss is already visible with one dereference per statement. Take the program

```
s = &s
s = &t
s = &a
r = *s
```

Andersen's analysis gives $pts(s) = \{s, t, a\}$ and $pts(r) = pts(s) \cup pts(t) \cup pts(a) = \{s, t, a\}$, so it says that $r$ may point to $t$. No run does that. When $r = *s$ runs, $s$ holds one value. If it is $s$, then $*s$ is the value of $s$, which is $s$. If it is $t$ or $a$, then $*s$ has no value, because $t$ and $a$ never get one. So $r$ can only point to $s$. The analysis reads "$s$ points to $s$" and "$s$ points to $t$" as two independent facts, but a run sees one of them at a time.

**Splitting statements changes the problem.** A compiler usually breaks $r = **s$ into $u = *s$ and $r = *u$ with a new variable $u$. Under the flow-insensitive semantics the two new statements may run at different moments, with other statements between them, so the split program has more runs. Its precise answer can be larger than the precise answer of the original. Andersen's analysis is the inclusion analysis of the split form, which is one reason why it runs in polynomial time.

**Flow sensitivity costs more.** Without dynamic allocation, precise flow-sensitive may-alias is PSPACE-complete (Landi 1992 and Muth and Debray 2000, as cited by Rinetzky et al. 2008; Chakaravarthy 2003 states it too). With dynamic allocation it is [undecidable](/may-alias-undecidability/). So flow-insensitive analysis is easier in theory too, but even the precise flow-insensitive question needs approximation in practice.

## Tightness

**Many dereferences in one statement.** The reduction uses one statement with $n - 2$ stars. Rinetzky et al. (2008) point out that Horwitz's proof also uses statements with an unbounded number of memory accesses, and they study the complexity of the precise question under other limits. The theorem on this page says nothing about programs whose statements have at most one star on each side, which is the input of Andersen's analysis.

**Types.** The program of the reduction lets a variable point to a variable that points back, so its pointers have no fixed level of indirection. Chakaravarthy (2003) showed that the precise flow-insensitive question becomes polynomial when the variables have well-defined types, and that it stays NP-hard for programs with scalar variables only and no dynamic memory.

**Dynamic memory and order.** Adding the order of the statements, or adding dynamic allocation to a flow-sensitive analysis, makes the problem harder, as the consequences above say. Dropping the precision requirement makes it easy: Andersen's least solution is a sound answer in cubic time.

## History

Landi (1992) and Ramalingam (1994) showed that precise flow-sensitive may-alias is undecidable once a program can build recursive data structures, which focused attention on approximations. Flow-insensitive analyses such as Andersen's (1994) and Steensgaard's (1996) were the practical answer, and Horwitz (1997) showed that even their semantics has no fast precise solution unless P = NP. Chakaravarthy (2003) extended the hardness results and found a polynomial case for well-typed programs, and Rinetzky, Ramalingam, Sagiv and Yahav (2008) studied the space between flow-insensitive and flow-sensitive analysis.

## References
