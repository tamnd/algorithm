---
tag: JYYPDZ
kind: technique
slug: sequential-counter-encoding
name: Sequential counter encoding
aliases:
- Sinz encoding
- LTseq encoding
- sequential counter
area: logic-and-constraints/sat-solving
level: advanced
summary: CNF encoding of the cardinality constraint x_1 + ... + x_n ≤ k with k(n-1) new variables and 2nk + n - 3k - 1 clauses, on which unit propagation is arc consistent.
prereqs: [conjunctive-normal-form, unit-propagation]
see_also: [totalizer-encoding, pseudo-boolean-sat, tseitin-transformation, max-sat, unit-propagation, arc-consistency]
sources:
  - paper: doi:10.1007/11564751_73
    title: Carsten Sinz, Towards an optimal CNF encoding of Boolean cardinality constraints, CP 2005, LNCS 3709, 827-831
    locator: the encoding LTseq (sequential counter), its clause and variable counts, and the statement that unit propagation keeps arc consistency
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 2 (Prestwich, CNF Encodings) and Chapter 28 (Roussel and Manquinho, Pseudo-Boolean and Cardinality Constraints), the sections on cardinality encodings
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability, the clauses of Sinz for the constraint "at most r"
---

The sequential counter encoding writes the cardinality constraint $x_1 + \cdots + x_n \le k$ as a [CNF](/conjunctive-normal-form/). It adds a unary counter $s_{i,j}$ that is forced true when at least $j$ of the first $i$ inputs are true, and it forbids the counter to pass $k$. For $1 \le k < n$ it uses $k(n-1)$ new variables and exactly $2nk + n - 3k - 1$ clauses, so its size is $O(nk)$, and [unit propagation](/unit-propagation/) on it is [arc consistent](/arc-consistency/): as soon as $k$ inputs are true, it sets every other input false. Carsten Sinz gave it in 2005. It is one of the standard ways to give "at most one", "at most $k$" and "exactly $k$" constraints to a SAT solver.

## In plain words

You want to say "at most two of these ten switches are on" with clauses only. Listing every forbidden group of three switches works, but there are 120 such groups, and the number explodes for larger counts.

Instead, walk along the switches from left to right and keep a tally on a small abacus with two beads. A new variable for each position and each bead says "by this point, at least this many switches were on". The clauses say how the tally moves: it never goes down, and it moves up one bead when a switch is on. One more clause says that a switch may not be on when the tally is already full. The total number of clauses grows like the number of switches times the bound.

## When it applies

Use it when a problem has a constraint "at most $k$ of these literals are true", "at least $k$" or "exactly $k$", and the solver accepts only clauses. Signals:

- $k$ is small compared with $n$, so $O(nk)$ clauses are cheap. For "at most one" ($k = 1$) it gives $3n - 4$ clauses with $n - 1$ new variables.
- You want unit propagation to do the full reasoning of the constraint, with no search inside it.
- The bound is fixed. If the bound changes during the search (as in [MaxSAT](/max-sat/) with a decreasing bound), the [totalizer](/totalizer-encoding/) lets you tighten it with unit clauses on its outputs.

## The template

Notation: $x_1, \ldots, x_n$ are the input literals and $1 \le k < n$. (For $k \ge n$ no clause is needed; for $k = 0$ use the unit clauses $\neg x_i$.) The new variables are $s_{i,j}$ for $1 \le i \le n-1$ and $1 \le j \le k$. The intended meaning is "$s_{i,j}$ is true if at least $j$ of $x_1, \ldots, x_i$ are true".

```pseudo id=main
SEQ-AT-MOST(x_1 .. x_n, k)                       ▷ 1 ≤ k < n
L1  add (¬x_1 ∨ s_{1,1})
L2  add (¬s_{1,j}) for 1 < j ≤ k
L3  for i ← 2 to n − 1 do
L4      add (¬x_i ∨ s_{i,1})                       ▷ x_i alone counts as 1
L5      add (¬s_{i−1,1} ∨ s_{i,1})                 ▷ the tally never goes down
L6      add (¬x_i ∨ ¬s_{i−1,j−1} ∨ s_{i,j}) for 1 < j ≤ k   ▷ x_i moves j − 1 to j
L7      add (¬s_{i−1,j} ∨ s_{i,j}) for 1 < j ≤ k
L8      add (¬x_i ∨ ¬s_{i−1,k})                    ▷ no x_i when the tally is full
L9  add (¬x_n ∨ ¬s_{n−1,k})
```

"At least $k$" is "at most $n - k$" on the negated literals $\neg x_1, \ldots, \neg x_n$. "Exactly $k$" is the conjunction of the two encodings.

**Counts.** Lines L1 and L2 give $1 + (k-1) = k$ clauses. Each of the $n - 2$ rounds of line L3 gives $2 + 2(k-1) + 1 = 2k + 1$ clauses. Line L9 gives 1. The total is $k + (n-2)(2k+1) + 1 = 2nk + n - 3k - 1$. There are $k(n-1)$ new variables. With $\ell$ the literal occurrences, at most $3$ per clause, the size is $|F| = O(nk)$, and the time is $\Theta(nk)$.

### Example

For $n = 4$ and $k = 2$ the encoding has 6 new variables and 13 clauses:

$$(\neg x_1 \vee s_{11}),\ (\neg s_{12}),\ (\neg x_2 \vee s_{21}),\ (\neg s_{11} \vee s_{21}),\ (\neg x_2 \vee \neg s_{11} \vee s_{22}),\ (\neg s_{12} \vee s_{22}),\ (\neg x_2 \vee \neg s_{12}),$$

$$(\neg x_3 \vee s_{31}),\ (\neg s_{21} \vee s_{31}),\ (\neg x_3 \vee \neg s_{21} \vee s_{32}),\ (\neg s_{22} \vee s_{32}),\ (\neg x_3 \vee \neg s_{22}),\ (\neg x_4 \vee \neg s_{32}).$$

*Forward propagation.* Set $x_1 = 1$, $x_3 = 1$. Unit propagation sets $s_{11}$, then $s_{21}$, then $s_{31}$, and $(\neg x_3 \vee \neg s_{21} \vee s_{32})$ sets $s_{32}$. Then $(\neg x_4 \vee \neg s_{32})$ sets $x_4 = 0$, and $(\neg x_3 \vee \neg s_{22})$ sets $s_{22} = 0$, which with $(\neg x_2 \vee \neg s_{11} \vee s_{22})$ sets $x_2 = 0$.

*Backward propagation.* Set $x_3 = 1$, $x_4 = 1$ instead. The last clause sets $s_{32} = 0$. Then $(\neg x_3 \vee \neg s_{21} \vee s_{32})$ sets $s_{21} = 0$, $(\neg s_{11} \vee s_{21})$ sets $s_{11} = 0$, $(\neg x_2 \vee s_{21})$ sets $x_2 = 0$ and $(\neg x_1 \vee s_{11})$ sets $x_1 = 0$.

For $n = 10$ and $k = 3$, the encoding has 60 clauses and 27 new variables. The direct encoding without new variables forbids each set of $k + 1$ inputs and has $\binom{10}{4} = 210$ clauses of width 4.

### Why it is correct

Let $c_i$ be the number of true literals among $x_1, \ldots, x_i$, and let $S$ be the encoding.

**Lemma 1 (the counter is a lower bound).** In each model of $S$, $c_i \ge j$ implies $s_{i,j} = 1$, for all $1 \le i \le n-1$ and $1 \le j \le k$.

*Proof.* By induction on $i$. For $i = 1$: $c_1 \ge j$ needs $j = 1$ and $x_1 = 1$, and line L1 gives $s_{1,1}$. For $i \ge 2$ and $c_i \ge j$: either $c_{i-1} \ge j$, and then $s_{i-1,j}$ holds by the hypothesis and line L5 or L7 gives $s_{i,j}$; or $c_{i-1} = j - 1$ and $x_i = 1$. If $j = 1$, line L4 gives $s_{i,1}$. If $j > 1$, the hypothesis gives $s_{i-1,j-1}$, and line L6 gives $s_{i,j}$. $\square$

**Theorem 1 (exact projection).** An assignment of $x_1, \ldots, x_n$ extends to a model of $S$ if and only if $c_n \le k$.

*Proof.* If $c_n > k$, let $i$ be the position of the $(k+1)$-th true literal. Then $c_{i-1} = k$, so $s_{i-1,k} = 1$ by Lemma 1, and the clause $(\neg x_i \vee \neg s_{i-1,k})$ of line L8 or L9 is false. ($i \ge 2$ because $k \ge 1$.) If $c_n \le k$, set $s_{i,j} = 1$ exactly when $c_i \ge j$. Lines L1 and L4 to L7 hold because the count after step $i$ is at least the count before it and grows by $x_i$. Line L2 holds because $c_1 \le 1$. Lines L8 and L9 hold: if $x_i = 1$ and $s_{i-1,k} = 1$ then $c_i \ge k + 1$, which is false. $\blacksquare$

The registers are not determined by the inputs: with $c_i < j$, the value $s_{i,j} = 1$ is allowed when nothing later forbids it. So the encoding does not preserve the number of models.

**Theorem 2 (arc consistency).** Let $\rho$ be a partial assignment of the inputs only, with $t$ true literals. If $t > k$, unit propagation on $S$ under $\rho$ reaches a conflict. If $t = k$, it sets every unassigned input to false. If $t < k$, no input value is excluded by the constraint, and unit propagation sets no input, because it is sound and both values of each free input extend to a model.

*Proof.* Let $i_1 < \cdots < i_t$ be the positions of the true inputs.

*Forward facts.* Unit propagation sets $s_{i,j} = 1$ for every $j \le \min(t, k)$ and every $i$ with $i_j \le i \le n - 1$. For $j = 1$ this comes from line L4 or L1 at $i_1$, then line L5. For $j > 1$, line L6 at $i_j$ fires because $s_{i_j - 1, j-1} = 1$ (as $i_j - 1 \ge i_{j-1}$), then line L7 carries it forward. If $t > k$, the clause $(\neg x_{i_{k+1}} \vee \neg s_{i_{k+1}-1, k})$ is falsified: a conflict.

Now let $t = k$, and let $x_\ell$ be unassigned. Let $p$ be the number of true inputs before $\ell$. If $p = k$, then $s_{\ell - 1, k} = 1$ by the forward facts, and line L8 or L9 at $\ell$ sets $x_\ell = 0$.

*Backward facts.* If $p < k$, unit propagation sets $s_{i,j} = 0$ for every $j$ with $p < j \le k$ and every $i \le i_j - 1$. For $j = k$: line L8 or L9 at $i_k$ sets $s_{i_k - 1, k} = 0$, and the clauses of lines L5 and L7, read backwards, set $s_{i,k} = 0$ for all smaller $i$. For $p < j < k$: the clause of line L6 at position $i_j$ for the register $j + 1$ is $(\neg x_{i_j} \vee \neg s_{i_j - 1, j} \vee s_{i_j, j+1})$. Here $x_{i_j} = 1$, and $s_{i_j, j+1} = 0$ by the case $j + 1$, as $i_j \le i_{j+1} - 1$. So $s_{i_j - 1, j} = 0$, and lines L5 and L7 carry it back. Finally at $\ell$, with $i_p < \ell < i_{p+1}$: if $p = 0$, the clause $(\neg x_\ell \vee s_{\ell,1})$ and $s_{\ell, 1} = 0$ give $x_\ell = 0$. If $p \ge 1$, the clause $(\neg x_\ell \vee \neg s_{\ell-1,p} \vee s_{\ell,p+1})$ with $s_{\ell-1,p} = 1$ (forward) and $s_{\ell,p+1} = 0$ (backward) gives $x_\ell = 0$. $\blacksquare$

## Classic examples

- **At most one.** With $k = 1$ the encoding is the "sequential" or "ladder" form of at most one, with $3n - 4$ clauses. The direct pairwise form has $\binom{n}{2}$ binary clauses, which is smaller only for small $n$.
- **Scheduling and timetabling.** Constraints such as "at most $k$ tasks in each slot" or "each nurse works exactly 5 shifts in a week" become sequential counters.
- **Pseudo-Boolean constraints.** A constraint with unit coefficients is a cardinality constraint, and solvers that translate [pseudo-Boolean](/pseudo-boolean-sat/) problems to SAT use this encoding or the [totalizer](/totalizer-encoding/) for it.
- **MaxSAT with a fixed bound.** "At most $k$ soft clauses are false" is a cardinality constraint on the relaxation variables of [MaxSAT](/max-sat/).

## Variations

- **Sequential weight counter.** For $\sum w_i x_i \le K$ with positive integer weights, let $s_{i,j}$ count weights up to $K$. The size becomes $O(nK)$, which is pseudo-polynomial.
- **Two directions.** Adding the converse clauses makes $s_{i,j}$ equal to $[c_i \ge j]$. Then the registers are determined by the inputs, which helps with model counting, at the cost of more clauses.
- **Other cardinality encodings.** The [totalizer](/totalizer-encoding/) uses $O(n \log n)$ variables and $O(n^2)$ clauses in its full form, or $O(nk)$ when truncated at $k + 1$. Sorting networks and cardinality networks use $O(n \log^2 k)$ clauses. All of them give arc consistency by unit propagation for "at most $k$".

## Pitfalls

- **The edge cases of $k$.** The template needs $1 \le k < n$. For $k = 0$ it would refer to registers that do not exist; for $k \ge n$ the constraint is always true.
- **Counting models.** The encoding is one-sided, so a satisfying input can have several register values. Do not count models of the encoded formula to count solutions.
- **Literals, not variables.** The inputs can be negated literals. "At least $k$" uses the negated inputs with the bound $n - k$; using $\neg x_i$ with the bound $k$ is a different constraint.
- **Shared registers.** Each constraint needs its own registers. Two constraints over different input sets cannot share them.

## Exercises

1. Prove that the direct encoding with all $\binom{n}{k+1}$ clauses is also arc consistent under unit propagation, and compare the sizes for $n = 20$ and $k = 2, 5, 10$.
2. Write the clauses that make $s_{i,j} \leftrightarrow (c_i \ge j)$ and show that the resulting encoding has exactly one extension for each input with $c_n \le k$.
3. Use two sequential counters to encode "exactly $k$" and check that unit propagation sets all free inputs to true when only $n - k$ inputs can still be false.

## References
