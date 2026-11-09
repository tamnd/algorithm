---
tag: 7XSPN7
kind: algorithm
slug: two-sat-algorithm
name: 2-SAT algorithm
aliases:
- Aspvall-Plass-Tarjan algorithm
- implication graph algorithm for 2-SAT
area: logic-and-constraints/sat-solving
level: intro
summary: Solve 2-SAT in linear time. Find the strongly connected components of the implication graph; UNSAT when a variable and its negation share one, else read a model from their order.
solves: [2-sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of clauses}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true}
history:
  year: 1979
  people: [Bengt Aspvall, Michael F. Plass, Robert E. Tarjan]
  note: Published as a linear-time test for quantified 2-CNF formulas, with 2-SAT as the case where all quantifiers are existential.
prereqs: [2-sat, strongly-connected-components, tarjan-scc]
see_also: [implication-graph, kosaraju-sharir, condensation-graph, horn-sat-forward-chaining, xor-gaussian-elimination, schoning-algorithm, max-2-sat, qbf]
sources:
  - paper: doi:10.1016/0020-0190(79)90002-4
    title: Bengt Aspvall, Michael F. Plass and Robert E. Tarjan, A linear-time algorithm for testing the truth of certain quantified Boolean formulas, Information Processing Letters 8(3), 121 to 123 (1979)
    locator: the whole paper (the implication graph, the test on strong components and the construction of a model)
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: the section on strongly connected components
  - paper: "Shimon Even, Alon Itai and Adi Shamir, On the complexity of timetable and multicommodity flow problems, SIAM Journal on Computing 5(4), 691 to 703 (1976)"
    locator: the section on 2-SAT and limited backtracking
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2 (2022)
    locator: Section 7.2.2.2, Satisfiability (the discussion of 2SAT and implication digraphs)
---

The 2-SAT algorithm of Aspvall, Plass and Tarjan decides a formula of [2-SAT](/2-sat/) in $\Theta(n + m)$ time. It builds the [implication graph](/implication-graph/), finds its [strongly connected components](/strongly-connected-components/) with [Tarjan's algorithm](/tarjan-scc/), and answers UNSAT exactly when a variable and its negation are in the same component. Otherwise it reads a model from the order of the components. The [2-SAT](/2-sat/) page covers the problem; this page covers the algorithm.

## In plain words

A clause with two parts, "a or b", says two things. If a is false, then b must be true. If b is false, then a must be true. Draw one dot for each variable and one for its opposite, and draw an arrow for each of these "if, then" rules. A chain of arrows is a chain of forced choices.

If the arrows lead from a variable to its opposite and back again, then both values of the variable lead to a contradiction, and no answer exists. Otherwise an answer exists. To find it, group the dots that can reach each other, and visit the groups from the end of the arrows backward. Make each dot in a group true when its opposite is not yet decided. Tarjan's search finds the groups in exactly this order.

## The problem

The input is a CNF formula $F$ over the variables $x_1, \ldots, x_n$ with $m$ clauses, each with at most two literals. We use the notation of the area: a clause is a set of literals, and a literal is $x_v$ or $\neg x_v$. The output is UNSAT when $F$ has no model, and else an assignment $x \in \{0,1\}^n$ that makes each clause true. This is the [2-SAT](/2-sat/) problem.

The *implication graph* $G$ has $2n$ vertices, one for each literal. Each clause $(a \vee b)$ gives the two arcs $\neg a \to b$ and $\neg b \to a$. A unit clause $(a)$ is the clause $(a \vee a)$, so it gives the arc $\neg a \to a$.

## The algorithm

Line L5 numbers the components in the order in which Tarjan's algorithm finishes them. This is a reverse [topological order](/topological-sort/) of the [condensation](/condensation-graph/): an arc $u \to w$ implies $comp[u] \ge comp[w]$.

```pseudo id=main
TWO-SAT(F, n)
L1  if F has an empty clause then return UNSAT
L2  G ← a graph with one vertex for each of the 2n literals, and no arcs
L3  for each clause (a ∨ b) of F do              ▷ a unit clause (a) is (a ∨ a)
L4      add the arcs ¬a → b and ¬b → a to G
L5  comp ← the component numbers of G from Tarjan's algorithm
L6  for v ← 1 to n do
L7      if comp[x_v] = comp[¬x_v] then return UNSAT
L8  for v ← 1 to n do x_v ← (comp[x_v] < comp[¬x_v])
L9  return x
```

Lines L2 to L4 build the graph. Line L7 is the test for a contradiction: if $x_v$ and $\neg x_v$ are in one component, each value of $x_v$ forces the other value. Line L8 makes a literal true when its component is finished first, that is, when it is nearer to a sink of the condensation than its complement. A literal with a smaller number cannot reach its complement, so making it true forces nothing false.

## Example

Take $n = 4$ and

$$F = (x_1 \vee x_2) \wedge (\neg x_1 \vee x_3) \wedge (\neg x_2 \vee x_3) \wedge (\neg x_3 \vee x_4) \wedge (\neg x_4 \vee \neg x_1).$$

Lines L3 and L4 give 10 arcs, two for each clause:

| clause | arcs |
|---|---|
| $x_1 \vee x_2$ | $\neg x_1 \to x_2$, $\neg x_2 \to x_1$ |
| $\neg x_1 \vee x_3$ | $x_1 \to x_3$, $\neg x_3 \to \neg x_1$ |
| $\neg x_2 \vee x_3$ | $x_2 \to x_3$, $\neg x_3 \to \neg x_2$ |
| $\neg x_3 \vee x_4$ | $x_3 \to x_4$, $\neg x_4 \to \neg x_3$ |
| $\neg x_4 \vee \neg x_1$ | $x_4 \to \neg x_1$, $x_1 \to \neg x_4$ |

The cycle $x_2 \to x_3 \to x_4 \to \neg x_1 \to x_2$ puts four literals in one component, and its mirror image $\neg x_2 \to x_1 \to \neg x_4 \to \neg x_3 \to \neg x_2$ puts the other four in a second component. Tarjan's algorithm, started at the vertex $x_1$, finishes the components in this order:

| comp | literals |
|---|---|
| 0 | $\neg x_1$, $x_2$, $x_3$, $x_4$ |
| 1 | $x_1$, $\neg x_2$, $\neg x_3$, $\neg x_4$ |

No variable has both literals in one component, so line L7 does not return. Line L8 compares the numbers: $comp[x_1] = 1 > 0 = comp[\neg x_1]$, so $x_1$ is false, and $x_2$, $x_3$, $x_4$ are true. The model $x = (0, 1, 1, 1)$ makes each clause true. The arc $x_1 \to x_3$ goes from component 1 to component 0, and the path $x_1 \to x_3 \to x_4 \to \neg x_1$ shows why $x_1$ must be false.

Now add the clause $(x_1 \vee \neg x_2)$. It gives the arcs $\neg x_1 \to \neg x_2$ and $x_2 \to x_1$. Then $x_1 \leadsto \neg x_1 \to \neg x_2 \to x_1$, so all 8 literals are in one component, and line L7 returns UNSAT. A check of all 16 assignments agrees.

## Correctness

Two facts carry the proof. First, each arc is an implication: if a model makes $u$ true and $G$ has a path from $u$ to $w$, the model makes $w$ true. So when $x_v$ and $\neg x_v$ reach each other, no model exists. Second, Tarjan's numbering satisfies $comp[u] \ge comp[w]$ on each arc $u \to w$. If the assignment of line L8 made a clause $(a \vee b)$ false, then

$$comp[a] > comp[\neg a] \ge comp[b] > comp[\neg b] \ge comp[a],$$

which is impossible. The full proof is in the proof file below.

## Complexity

$G$ has $2n$ vertices and $2m$ arcs, so lines L2 to L4 take $\Theta(n + m)$ time. Tarjan's algorithm takes $\Theta(V + E) = \Theta(n + m)$ time on this graph. Lines L6 to L8 take $\Theta(n)$ time. So the time is $\Theta(n + m)$ in the worst case and also in the best case, on the [word RAM](/word-ram/). The input has size $|F| \le 2m$, so the time is linear in the size of the input plus the number of variables.

The extra space is $\Theta(n + m)$: the adjacency lists hold $2m$ arcs, and Tarjan's algorithm keeps $\Theta(n)$ numbers and a stack.

## Properties

- **Deterministic and exact.** It always answers, and its answer is always right.
- **Gives more than one model.** Each literal $\ell$ with a path $\ell \leadsto \neg\ell$ is false in each model. A literal is in the [backbone](/backbone/) of a satisfiable $F$ exactly when its complement has such a path.
- **Certificate of UNSAT.** The two paths $x_v \leadsto \neg x_v \leadsto x_v$ are a short proof. Each arc is a clause, and the chain of arcs gives a [resolution](/robinson-resolution/) refutation of length $O(n)$ from these clauses.

## Variants and improvements

- **Kosaraju's algorithm.** [Kosaraju's algorithm](/kosaraju-sharir/) also finds the components in linear time. Its second pass finds them in topological order, not in reverse order, so the comparison of line L8 must be reversed.
- **Limited backtracking.** Set a variable, apply [unit propagation](/unit-propagation/), and if this gives a conflict, undo it and set the other value. On a 2-CNF formula a conflict-free propagation never has to be undone. Even, Itai and Shamir used this idea in 1976. A simple version takes $O(n (n + m))$ time.
- **Random walk.** Start from any assignment and flip a random variable of a false clause. On a satisfiable 2-CNF formula this finds a model after at most $n^2$ flips in expectation, by Papadimitriou's 1991 analysis. The proof is on the page on [Schöning's algorithm](/schoning-algorithm/), which uses the same walk for $k \ge 3$.
- **Quantified 2-CNF.** Aspvall, Plass and Tarjan solved the more general [QBF](/qbf/) with a 2-CNF matrix in linear time, with the same graph.

## When to use it

Use it when each constraint links at most two Boolean choices: two-choice scheduling, the placement of labels, and the 2-SAT steps inside larger solvers. For a formula with longer clauses it does not apply, because [3-SAT](/3-sat/) is NP-complete. For a [Horn formula](/horn-sat/) use [forward chaining](/horn-sat-forward-chaining/), and for parity constraints use [Gaussian elimination](/xor-gaussian-elimination/). To maximize the number of true 2-clauses, which is [MAX-2-SAT](/max-2-sat/), the problem is NP-hard and this algorithm does not help.

## Pitfalls

- **One arc per clause.** Line L4 must add both arcs, $\neg a \to b$ and $\neg b \to a$. With one arc the graph loses the contrapositive, and line L7 misses contradictions.
- **The direction of line L8.** With Tarjan's numbering the rule is $comp[x_v] < comp[\neg x_v]$. The rule $>$ gives a wrong assignment, for example $x_1$ true in the example above. With Kosaraju's numbering the rule is reversed.
- **Unit clauses.** A clause $(a)$ must give the arc $\neg a \to a$. A program that skips clauses of length 1 answers SAT on $(x_1) \wedge (\neg x_1)$.
- **Deep recursion.** A recursive depth-first search goes $2n$ calls deep on a chain of implications. Use an explicit stack, as the Python version does.

## Implementations

## History

Krom studied formulas with two literals per clause in 1967, which is why 2-CNF formulas are also called Krom formulas. Even, Itai and Shamir gave a polynomial-time method based on limited backtracking in 1976. Aspvall, Plass and Tarjan published the linear-time algorithm with the implication graph in 1979. They built it on Tarjan's 1972 linear-time algorithm for strongly connected components, and solved quantified 2-CNF formulas with it.

## References
