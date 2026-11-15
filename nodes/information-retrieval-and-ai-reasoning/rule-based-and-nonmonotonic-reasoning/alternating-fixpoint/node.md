---
tag: 8YTFM5
kind: algorithm
slug: alternating-fixpoint
name: Alternating fixpoint computation
aliases:
- Van Gelder alternating fixpoint
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: Computes the well-founded model of a ground normal program by applying the reduct least model operator alternately, giving underestimates of the true atoms and overestimates of the non-false ones.
model: word-ram
complexity:
  vars: {n: the number of atoms, s: "the size of the program, the number of rules plus the number of body literals"}
  time: {worst: O(n · s), best: Θ(s)}
  space: {extra: Θ(n + s)}
properties: {deterministic: true}
history:
  year: 1989
  people: [Allen Van Gelder]
  note: Van Gelder presented the alternating fixpoint at PODS 1989 and published the full version in 1993. He showed that it gives the well-founded partial model defined by Van Gelder, Ross and Schlipf.
prereqs: [well-founded-semantics, gelfond-lifschitz-reduct, fixed-point, horn-sat-forward-chaining]
see_also: [slg-resolution, stable-model-semantics, stratified-logic-program, knaster-tarski-theorem, smodels-algorithm, datalog-evaluation]
sources:
  - paper: doi:10.1016/0022-0000(93)90024-Q
    title: Allen Van Gelder, The alternating fixpoint of logic programs with negation, Journal of Computer and System Sciences 47(1), 185 to 221 (1993)
    locator: the alternating fixpoint construction and the proof that it gives the well-founded partial model
  - paper: doi:10.1145/116825.116838
    title: Allen Van Gelder, Kenneth A. Ross and John S. Schlipf, The well-founded semantics for general logic programs, Journal of the ACM 38(3), 620 to 650 (1991)
    locator: unfounded sets, the operator W_P and the well-founded partial model
  - paper: "Michael Gelfond and Vladimir Lifschitz, The stable model semantics for logic programming, in Robert A. Kowalski and Kenneth A. Bowen (eds.), Logic Programming: Proceedings of the Fifth International Conference and Symposium, MIT Press, 1070 to 1080 (1988)"
    locator: the reduct and the operator that maps a set of atoms to the least model of the reduct
  - paper: doi:10.1016/0743-1066(84)90014-1
    title: William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 267 to 284 (1984)
    locator: the counter method that computes the least model of a definite program in linear time
  - paper: "Zbigniew Lonc and Mirosław Truszczyński, On the problem of computing the well-founded semantics, Theory and Practice of Logic Programming 1(5), 591 to 609 (2001)"
    locator: the cost of the alternating fixpoint and faster methods for classes of programs
---

The alternating fixpoint computes the [well-founded model](/well-founded-semantics/) of a finite ground normal program. It uses one operator, $S(J)$, the least model of the [Gelfond-Lifschitz reduct](/gelfond-lifschitz-reduct/) $P^J$. This operator is *antimonotone*: a larger $J$ blocks more negative literals and gives a smaller result. So the sequence $\emptyset, S(\emptyset), S(S(\emptyset)), \ldots$ alternates between underestimates of the true atoms and overestimates of the atoms that are not false. The underestimates grow and the overestimates shrink until both stop, after at most $n + 1$ rounds for $n$ atoms. Van Gelder (1993) proved that the limit is the well-founded model. Each application of $S$ is a [forward chaining](/horn-sat-forward-chaining/) pass in linear time, so the whole computation takes polynomial time.

## In plain words

Some rules have conditions of the form "if this is not known". The well-founded model sorts each fact into true, false or unknown. The method uses one tool again and again: take a guess of what is true, let every negative condition on a fact in the guess fail, and see what the rules then prove. Start with the guess that nothing is true. Then no negative condition fails, and the rules prove a lot: an overestimate. Use the overestimate as the next guess. Now many negative conditions fail, and the rules prove less: an underestimate, and each fact in it is surely true. Keep going. The underestimates grow, the overestimates shrink, and both soon stop. What the last overestimate leaves out is false, the last underestimate is true, and the facts between them are unknown.

## The problem

The input is a finite ground normal program $P$: a set of rules $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_k$ over a set $A$ of $n$ atoms. The output is the well-founded model, a pair $(T, F)$ of disjoint sets of atoms: $T$ is the set of true atoms, $F$ the set of false atoms, and the other atoms are undefined. Van Gelder, Ross and Schlipf (1991) defined it as the least fixpoint of an operator built from *unfounded sets*; the [well-founded semantics](/well-founded-semantics/) page gives the definition.

## The algorithm

For $J \subseteq A$, the reduct $P^J$ deletes each rule with some $c_i \in J$ and deletes the negative literals of the other rules. $S(J)$ is the least model of this definite program. Gelfond and Lifschitz write it $\Gamma_P(J)$; a set $M$ is a [stable model](/stable-model-semantics/) exactly when $S(M) = M$.

```pseudo id=main
ALTERNATING-FIXPOINT(P)          ▷ P is a finite ground normal program over the atoms A
L1  K ← ∅
L2  U ← S(P, K)                    ▷ an overestimate of the atoms that are not false
L3  loop
L4      K' ← S(P, U)               ▷ an underestimate of the true atoms
L5      if K' = K then return (K, A ∖ U)    ▷ true atoms, false atoms
L6      K ← K'
L7      U ← S(P, K)

S(P, J)                            ▷ the least model of the reduct P^J
L8  M ← ∅, Q ← an empty queue
L9  for each rule r = h ← pos, not neg of P do
L10     if neg ∩ J ≠ ∅ then count[r] ← −1           ▷ the reduct deletes r
L11     else count[r] ← |pos|; if count[r] = 0 and h ∉ M then add h to M and to Q
L12 while Q is not empty do
L13     b ← take the first atom of Q
L14     for each rule r with b ∈ pos(r) and count[r] > 0 do
L15         count[r] ← count[r] − 1
L16         if count[r] = 0 and head(r) ∉ M then add head(r) to M and to Q
L17 return M
```

Lines L8 to L17 are the counter method of Dowling and Gallier (1984): each kept rule counts its positive body atoms that are not yet derived. The index from each atom to the rules where it occurs positively is built once, before line L1.

## Example

The program describes a game: a position is won if some move leads to a position that is not won. The moves are $1 \to 2$, $2 \to 3$, $3 \to 4$, $5 \to 6$ and $6 \to 5$, and $w_i$ means that position $i$ is won. Position 4 has no move, and the rule $w_4 \leftarrow w_4$ only puts $w_4$ in the program.

```text
w1 ← not w2.   w2 ← not w3.   w3 ← not w4.   w4 ← w4.
w5 ← not w6.   w6 ← not w5.
```

| round | $K_i$ | $U_i = S(K_i)$ | why |
|---|---|---|---|
| 0 | $\emptyset$ | $\{w_1, w_2, w_3, w_5, w_6\}$ | $K_0$ blocks no negative literal, and nothing derives $w_4$ |
| 1 | $S(U_0) = \{w_3\}$ | $\{w_1, w_3, w_5, w_6\}$ | only $w_3 \leftarrow \mathit{not}\ w_4$ survives the reduct by $U_0$; then $w_3 \in K_1$ blocks the rule for $w_2$ |
| 2 | $S(U_1) = \{w_1, w_3\}$ | $\{w_1, w_3, w_5, w_6\}$ | $w_2 \notin U_1$, so the rule for $w_1$ survives |
| 3 | $S(U_2) = \{w_1, w_3\}$ | | equal to $K_2$: stop at line L5 |

The result is $T = \{w_1, w_3\}$ and $F = A \setminus U_2 = \{w_2, w_4\}$. The atoms $w_5$ and $w_6$ are undefined: the cycle $5 \to 6 \to 5$ is a draw. This matches the game: position 4 is lost because it has no move, so 3 is won, 2 is lost and 1 is won. The program has the two stable models $\{w_1, w_3, w_5\}$ and $\{w_1, w_3, w_6\}$, and both lie between $K$ and $U$.

## Correctness

The [correctness proof](proofs/correctness.md) has the details. $S$ is antimonotone, because a larger $J$ makes the reduct smaller. By induction, the $K_i$ increase, the $U_i$ decrease, and $K_i \subseteq U_i$. When the loop stops, $S(U) = K$ and $S(K) = U$. The proof that $(K, A \setminus U)$ is the well-founded model has two halves. First, it is closed under the operator $W_P$ of Van Gelder, Ross and Schlipf: a rule whose body is true in it survives the reduct by $U$, so its head is in $S(U) = K$; and no atom of $S(K) = U$ can be in an unfounded set, by induction on the stage of its derivation. So the least fixpoint of $W_P$ is below it. Second, for the well-founded model $(T^*, F^*)$, the atoms outside $S(T^*)$ form an unfounded set, and $S(A \setminus F^*) \subseteq T^*$. With antimonotonicity, an induction on $i$ gives $K_i \subseteq T^*$ and $A \setminus U_i \subseteq F^*$.

## Complexity

Let $s$ be the number of rules plus the number of body literals. One call of $S$ takes $\Theta(s)$ time: each rule is visited once at lines L9 to L11, and each positive body occurrence at most once at line L14, because each atom enters the queue at most once. The sets $K_i$ grow strictly until the last round, so there are at most $n + 1$ rounds and $O(n)$ calls of $S$. The total time is $O(n \cdot s)$, and the space is $\Theta(n + s)$ for the index, the counters and the sets. The bound is reached: on a chain $w_1 \leftarrow \mathit{not}\ w_2, \ldots, w_{n-1} \leftarrow \mathit{not}\ w_n$ each round adds one atom to $K$, starting from the end of the chain, so there are about $n/2$ rounds of cost $\Theta(n)$ each. If the first underestimate $S(S(\emptyset))$ is empty, the loop stops after two calls, in time $\Theta(s)$. The problem itself is in polynomial time, and for programs with variables and a fixed program it is P-complete in the size of the data.

## Properties

- **Deterministic and polynomial.** There is no search: the result is one three-valued model, computed in $O(n \cdot s)$ time.
- **Bounds on the stable models.** Every stable model $M$ satisfies $S(M) = M$, so by induction $K_i \subseteq M \subseteq U_i$ for every $i$. Atoms true in the well-founded model are in every stable model, and atoms false in it are in none.
- **Total on stratified programs.** For a [stratified program](/stratified-logic-program/), $K = U$, and the result is the perfect model, which is also the unique stable model.
- **Total means unique.** If $K = U$, then $K$ is a stable model, and by the bounds it is the only one.
- **Monotone in the double step.** $S \circ S$ is monotone, $K$ is its least fixpoint and $U = S(K)$ is its greatest fixpoint.

## Variants and improvements

- **Kripke-Kleene semantics.** Fitting (1985) iterates a three-valued version of the immediate consequence operator, without unfounded sets. It is cheaper but weaker: for $p \leftarrow p$ it leaves $p$ undefined, where the well-founded model makes $p$ false.
- **Component by component.** Split the program along the [strongly connected components](/strongly-connected-components/) of its dependency graph and compute the components in [topological order](/topological-sort/), with the atoms of the lower components already decided. On a stratified program each component then needs a single least model computation.
- **Faster methods.** Lonc and Truszczyński (2001) studied the cost of computing the well-founded model and gave faster algorithms for some classes of programs.
- **Goal-directed evaluation.** [SLG resolution](/slg-resolution/) computes the truth value of one query and evaluates only the part of the program that the query reaches.
- **Approximation fixpoint theory.** Denecker, Marek and Truszczyński generalized the construction to operators on any complete lattice, which gives well-founded semantics for [default logic](/default-logic/) and [autoepistemic logic](/autoepistemic-logic/) in the same way.

## When to use it

Use the alternating fixpoint to compute the whole well-founded model of a ground program bottom-up, for example after [grounding](/grounding/). It is also a cheap first step for stable model search: the true atoms must be in every stable model and the false atoms in none, and if the model is total the search is over. For one query on a large program, a goal-directed method such as SLG resolution evaluates less of the program.

## Pitfalls

- **Odd and even steps.** The sets $S(K_i)$ are overestimates and the sets $S(U_i)$ are underestimates. Returning an overestimate as the set of true atoms, or stopping at the first repeat of $U$ and pairing it with the wrong $K$, gives a wrong model.
- **Atoms with no rules.** The false atoms are $A \setminus U$, where $A$ contains every atom of the program, also the atoms that occur only in rule bodies. If $A$ holds only the heads, these false atoms are lost.
- **Undefined atoms can still follow.** For $a \leftarrow \mathit{not}\ b$, $b \leftarrow \mathit{not}\ a$, $c \leftarrow a$, $c \leftarrow b$, the atom $c$ is in both stable models $\{a, c\}$ and $\{b, c\}$, but it is undefined in the well-founded model, because $K = \emptyset$. The well-founded model is a sound approximation of cautious reasoning, not a replacement for it.
- **Recomputing from scratch.** A naive version reruns a full fixpoint over all rules for each call of $S$, and rescans all rules in each step of that fixpoint. This costs $O(n \cdot s)$ per call instead of $O(s)$.

## Implementations

## History

Van Gelder, Ross and Schlipf introduced the well-founded semantics at PODS 1988, with unfounded sets as the main tool, and published the journal version in 1991. In the same year, Gelfond and Lifschitz (1988) defined stable models with the reduct. Van Gelder (PODS 1989, journal version 1993) connected the two: the operator that maps a set to the least model of its reduct, applied twice, has the well-founded model as its least fixpoint. The construction later became the model for approximation fixpoint theory.

## References
