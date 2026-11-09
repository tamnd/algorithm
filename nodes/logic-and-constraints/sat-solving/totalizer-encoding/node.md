---
tag: MT2AEY
kind: technique
slug: totalizer-encoding
name: Totalizer encoding
aliases:
- Bailleux-Boufkhad totalizer
- totalizer
- unary adder tree
area: logic-and-constraints/sat-solving
level: advanced
summary: CNF encoding of cardinality constraints by a tree of unary adders, with O(n log n) new variables, O(n^2) clauses in full or O(nk) when cut at k + 1, and arc consistency by unit propagation.
prereqs: [conjunctive-normal-form, unit-propagation]
see_also: [sequential-counter-encoding, pseudo-boolean-sat, max-sat, core-guided-maxsat, sorting-network, arc-consistency]
sources:
  - paper: doi:10.1007/978-3-540-45193-8_8
    title: Olivier Bailleux and Yacine Boufkhad, Efficient CNF encoding of Boolean cardinality constraints, CP 2003, LNCS 2833, 108-122
    locator: the totalizer, its clauses C1 and C2, the size O(n log n) variables and O(n^2) clauses, and arc consistency by unit propagation
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 28 (Roussel and Manquinho, Pseudo-Boolean and Cardinality Constraints), the section on cardinality encodings; Chapter 24 (Bacchus, Järvisalo and Martins, Maximum Satisfiability), the use of totalizers in core-guided algorithms
  - paper: doi:10.1007/978-3-319-10428-7_39
    title: Ruben Martins, Saurabh Joshi, Vasco Manquinho and Inês Lynce, Incremental cardinality constraints for MaxSAT, CP 2014, LNCS 8656
    locator: the incremental totalizer, which keeps the tree and extends or tightens it between SAT calls
---

The totalizer encodes a cardinality constraint such as $x_1 + \cdots + x_n \le k$ in [CNF](/conjunctive-normal-form/). It builds a balanced binary tree over the inputs. Each inner node holds the number of true inputs below it as a unary number: output $r_t$ says "at least $t$ inputs below this node are true". The bound is one unit clause $\neg r_{k+1}$ on the root. In full form it uses $O(n \log n)$ new variables and exactly $\binom{n}{2} + V$ clauses, where $V$ is the number of new variables. Cut at $k + 1$ outputs per node, it uses $O(nk)$ clauses. [Unit propagation](/unit-propagation/) on it is [arc consistent](/arc-consistency/). Bailleux and Boufkhad gave it in 2003. Its root outputs serve every bound at once, which is why [MaxSAT](/max-sat/) solvers use it.

## In plain words

You want to say "at most $k$ of these switches are on". Pair up the switches, and for each pair write down how many are on, from 0 to 2. Pair up the pairs and add their counts, then pair up those, and so on, until one count at the top covers all switches. Each count is a row of lamps: the first lamp means "at least one", the second means "at least two", and so on.

The clauses only say "if the left part has at least $i$ and the right part has at least $j$, then the sum has at least $i + j$". The bound is one more clause: the top lamp number $k + 1$ is off. Because all counts stay at the top, a solver can try a different bound by switching off a different lamp.

## When it applies

Use it for "at most $k$", "at least $k$" and "exactly $k$" constraints over literals, when:

- the same sum is needed with several bounds, as in a MaxSAT search that lowers the bound step by step (the outputs $r_1, \ldots, r_n$ give every bound as a unit clause or an assumption);
- $k$ is large relative to $n$, so a structure of depth $O(\log n)$ is better than the chain of length $n$ in the [sequential counter](/sequential-counter-encoding/);
- unit propagation must enforce the full constraint.

## The template

Notation: $x_1, \ldots, x_n$ are the input literals, $c \ge 1$ is the number of outputs kept at each node, $0 \le k < n$ is the bound, $V$ is the number of new variables and $|F|$ is the number of clauses. For a node with children outputs $a_1, \ldots, a_p$ and $b_1, \ldots, b_q$, take $a_0$ and $b_0$ as true, so the literals $\neg a_0$ and $\neg b_0$ are left out of the clauses.

```pseudo id=main
TOTALIZER(x_1 .. x_n, c)              ▷ returns the outputs r_1 .. r_m of this subtree
L1  if n = 1 then return (x_1)
L2  a ← TOTALIZER(x_1 .. x_⌊n/2⌋, c);  b ← TOTALIZER(x_⌊n/2⌋+1 .. x_n, c)
L3  m ← min(|a| + |b|, c);  make new variables r_1 .. r_m
L4  for each i in 0 .. |a| and j in 0 .. |b| with 1 ≤ i + j ≤ m do
L5      add (¬a_i ∨ ¬b_j ∨ r_{i+j})
L6  return (r_1 .. r_m)

AT-MOST(x_1 .. x_n, k)                ▷ 0 ≤ k < n
L7  r ← TOTALIZER(x_1 .. x_n, k + 1)
L8  add (¬r_{k+1})
```

"At least $k$" is "at most $n - k$" on the negated inputs. Bailleux and Boufkhad also give the converse clauses $(a_{i+1} \vee b_{j+1} \vee \neg r_{i+j+1})$, which make "at least" direct and make $r_t$ equal to its meaning; "at most" alone needs only the clauses of line L5.

### Example

For $n = 4$ and $k = 2$, name the outputs of the node over $x_1, x_2$ as $u_1, u_2$, those over $x_3, x_4$ as $v_1, v_2$, and those of the root as $r_1, r_2, r_3$. There are 7 new variables and 14 clauses:

$$(\neg x_2 \vee u_1),\ (\neg x_1 \vee u_1),\ (\neg x_1 \vee \neg x_2 \vee u_2),\ (\neg x_4 \vee v_1),\ (\neg x_3 \vee v_1),\ (\neg x_3 \vee \neg x_4 \vee v_2),$$

$$(\neg v_1 \vee r_1),\ (\neg v_2 \vee r_2),\ (\neg u_1 \vee r_1),\ (\neg u_1 \vee \neg v_1 \vee r_2),\ (\neg u_1 \vee \neg v_2 \vee r_3),\ (\neg u_2 \vee r_2),\ (\neg u_2 \vee \neg v_1 \vee r_3),\ (\neg r_3).$$

The pair $(i, j) = (2, 2)$ is missing because the root keeps only $c = 3$ outputs. Set $x_1 = 1$ and $x_3 = 1$. Unit propagation sets $u_1$, $v_1$, $r_1$ and, by $(\neg u_1 \vee \neg v_1 \vee r_2)$, $r_2$. With $\neg r_3$, the clause $(\neg u_1 \vee \neg v_2 \vee r_3)$ sets $v_2 = 0$ and $(\neg u_2 \vee \neg v_1 \vee r_3)$ sets $u_2 = 0$. Then $(\neg x_1 \vee \neg x_2 \vee u_2)$ sets $x_2 = 0$ and $(\neg x_3 \vee \neg x_4 \vee v_2)$ sets $x_4 = 0$.

### Why it is correct

For a node $N$, let $\#N$ be the number of true inputs below $N$, under some assignment of the inputs.

**Lemma 1 (outputs are lower bounds).** In every model of the clauses of TOTALIZER, $\#N \ge t$ implies $r_t = 1$ for each output $r_t$ of $N$.

*Proof.* By induction on the height of $N$. A leaf is its own output $r_1 = x$. At an inner node with children $A$ and $B$, let $p = \#A$, $q = \#B$ and $p + q \ge t$, with $t \le m \le c$. Put $i = \min(p, t)$ and $j = t - i$. Then $i \le p$ and $i \le |a|$, as $|a| = \min(\text{leaves of } A, c)$ and $t \le c$. Also $j \le q$, and $j \le |b|$ in the same way. By the hypothesis $a_i = 1$ (or $i = 0$) and $b_j = 1$ (or $j = 0$), and the clause $(\neg a_i \vee \neg b_j \vee r_t)$ of line L5 gives $r_t = 1$. $\square$

**Theorem 1 (exact projection).** An assignment of the inputs extends to a model of AT-MOST if and only if at most $k$ inputs are true.

*Proof.* If more than $k$ are true, Lemma 1 at the root gives $r_{k+1} = 1$, against the clause of line L8. If at most $k$ are true, set every output $r_t$ of every node $N$ to $[\#N \ge t]$. A clause of line L5 holds because $\#A \ge i$ and $\#B \ge j$ give $\#N \ge i + j$. The unit clause holds because the root count is at most $k$. $\blacksquare$

As with the sequential counter, outputs may be true above the count, so the encoding does not keep the number of models unless the converse clauses are added.

**Theorem 2 (arc consistency).** Let $\rho$ assign some of the inputs, with $t$ of them true. If $t > k$, unit propagation reaches a conflict. If $t = k$, it sets every free input to false. If $t < k$, both values of each free input extend to a model, and unit propagation, being sound, sets no input.

*Proof.* *Upward.* Let $\tau(N)$ be the number of inputs below $N$ that $\rho$ sets true, capped at $|r^N|$. Unit propagation sets the outputs $r_1, \ldots, r_{\tau(N)}$ of every node $N$ to 1: at an inner node use the clause for $(i, j) = (\min(\tau(A), s), s - \min(\tau(A), s))$ for each $s \le \tau(N)$, as in Lemma 1. If $t > k$, the root gets $r_{k+1} = 1$, against $\neg r_{k+1}$.

*Downward.* Let $t = k$ and let $x$ be a free input. Along the path from the root to the leaf $x$, define for each node $N$ the budget $\beta(N) = k - (\text{true inputs not below } N)$, which is the number of true inputs below $N$. Unit propagation sets the output $r_{\beta(N)+1}$ of $N$ to 0. At the root this is the unit clause, as $\beta = k$. Let $N$ have this fact, with child $A$ on the path and sibling $B$, and let $q$ be the number of true inputs below $B$. Then $\beta(A) = \beta(N) - q$, and $B$ has $b_q = 1$ by the upward step (or $q = 0$). The index $\beta(A) + 1$ is at most the number of leaves of $A$, because $A$ holds the free input $x$, and at most $k + 1 = c$; so $a_{\beta(A)+1}$ exists. The clause $(\neg a_{\beta(A)+1} \vee \neg b_q \vee r_{\beta(N)+1})$ of line L5 then sets $a_{\beta(A)+1} = 0$. At the leaf, $\beta = 0$ and the output $r_1$ is $x$ itself, so $x = 0$. $\blacksquare$

### Size

Let every node keep all outputs ($c \ge n$). A node with children of $p$ and $q$ leaves gives $(p+1)(q+1) - 1 = pq + p + q$ clauses. Summed over the tree, $\sum pq = \binom{n}{2}$, because each pair of leaves meets at exactly one lowest common ancestor, and $\sum (p + q) = V$, the number of new variables. So $|F| = \binom{n}{2} + V$, plus one unit clause. The tree is balanced, so each level of the tree holds each input once, and $V \le n \lceil \log_2 n \rceil$; for $n = 2^d$, $V = nd$ exactly.

With the cut $c = k + 1$, a node at a level where nodes have $s \le c$ leaves still gives $O(s^2)$ clauses, and there are $n/s$ such nodes, so the level gives $O(ns)$; over the levels with $s = 2, 4, \ldots$ up to $c$ the sum is $O(nk)$. A node with more than $c$ leaves gives at most $(c+1)^2$ clauses, and there are $O(n/c)$ such nodes in total, for $O(nk)$ more. So the truncated totalizer has $O(nk)$ clauses and $O(n \log k)$ new variables. For "at most one" it has $4n - 4$ clauses, against $3n - 4$ for the sequential counter.

## Classic examples

- **Core-guided MaxSAT.** Algorithms such as OLL and MSU3 in [core-guided MaxSAT](/core-guided-maxsat/) build a totalizer over the relaxation literals of a core and then tighten the bound by asserting $\neg r_{k+1}$ for growing or shrinking $k$.
- **Linear search on the cost.** A model-improving [MaxSAT](/max-sat/) search adds $\neg r_{k}$ after each model of cost $k$; with one totalizer each step is one unit clause.
- **Pseudo-Boolean solving by translation.** Cardinality constraints in [pseudo-Boolean](/pseudo-boolean-sat/) problems are often translated with a totalizer.
- **Exactly $k$.** Adding $\neg r_{k+1}$ and the "at least $k$" side (from the converse clauses, or a second totalizer on the negations) encodes exactly $k$.

## Variations

- **Both directions.** With the converse clauses $(a_{i+1} \vee b_{j+1} \vee \neg r_{i+j+1})$ (where $a_{p+1}$ and $b_{q+1}$ are false and dropped), each output equals its meaning. Then "at least $k$" is the unit clause $r_k$, and models are kept one to one.
- **Incremental totalizer.** Martins, Joshi, Manquinho and Lynce keep the tree between SAT calls, add outputs only when the bound grows, and merge a new tree into an old one when a new core appears.
- **Generalized and weighted totalizers.** For $\sum w_i x_i \le K$, a node can keep one output per reachable sum of weights. The number of outputs can then grow up to $K$.
- **Sorting networks.** Odd-even merge networks and cardinality networks reach $O(n \log^2 n)$ and $O(n \log^2 k)$ clauses and also give arc consistency for "at most $k$"; the totalizer is simpler and has fewer variables for small $n$.

## Pitfalls

- **Truncation and later bounds.** If you cut at $c = k + 1$, the outputs above $c$ do not exist. A later, looser bound needs a new or extended tree.
- **The root outputs in assumptions.** Assuming $\neg r_{k+1}$ instead of adding it as a clause keeps the encoding reusable across calls of an [incremental solver](/incremental-sat/).
- **Counting models.** With the clauses of line L5 alone, a satisfying input can have several output values.
- **Quadratic growth in full form.** The full totalizer has $\binom{n}{2} + V$ clauses. For a constraint over many thousand literals with a small bound, truncate it or use the sequential counter.

## Exercises

1. Show that the full totalizer over $n = 2^d$ inputs has exactly $nd$ new variables and $\binom{n}{2} + nd$ clauses.
2. Add the converse clauses and prove that each output $r_t$ of each node equals "at least $t$ inputs below this node are true" in every model.
3. Show that for "at most one" the truncated totalizer has $4n - 4$ clauses, and give the 8 clauses for $n = 3$.

## References
