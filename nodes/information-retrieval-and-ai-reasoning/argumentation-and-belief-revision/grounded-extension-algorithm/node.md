---
tag: XNWEB6
kind: algorithm
slug: grounded-extension-algorithm
name: Grounded extension computation
aliases:
- grounded labelling algorithm
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: core
summary: Computes the grounded extension in linear time. Count the attackers of each argument that are not yet out, accept an argument when its count is 0, and reject every argument it attacks.
solves: [argument-acceptance-problem]
model: word-ram
complexity:
  vars: {n: the number of arguments, m: the number of attacks}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true}
history:
  year: 2021
  people: [Samer Nofal, Katie Atkinson, Paul E. Dunne]
  note: Published the counter-based method with a proof of the O(|V| + |E|) bound, and compared it with the labelling loop that earlier implementations took from Modgil and Caminada (2009).
prereqs: [grounded-extension, queue]
see_also: [argument-labelling, complete-extension, argument-acceptance-problem, horn-sat-forward-chaining, unit-propagation, retrograde-analysis, well-founded-semantics, preferred-extension]
sources:
  - paper: doi:10.1093/comjnl/bxz138
    title: Samer Nofal, Katie Atkinson and Paul E. Dunne, Computing grounded extensions of abstract argumentation frameworks, The Computer Journal 64(1), 54 to 63 (2021)
    locator: Algorithm 3 with Theorems 1 and 2 (the counter method and its O(|V| + |E|) bound), and Algorithm 2 with Theorem 3 (the earlier labelling loop and its O(|V| + |S||E|) bound)
  - paper: doi:10.1016/0004-3702(94)00041-X
    title: Phan Minh Dung, On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games, Artificial Intelligence 77(2), 321 to 357 (1995)
    locator: Section 2, Definitions 16 and 20, Lemma 24, Theorem 25 and Lemma 28 (pp. 328 to 330, the characteristic function and the grounded extension)
  - paper: "Sanjay Modgil and Martin Caminada, Proof theories and algorithms for abstract argumentation frameworks, in Guillermo Simari and Iyad Rahwan (eds), Argumentation in Artificial Intelligence, Springer (2009)"
    locator: pp. 105 to 129 (labelling algorithms, including the one for the grounded extension)
  - book: isbn:9781848902756
    title: Wolfgang Dvořák and Paul E. Dunne, Computational problems in formal argumentation and their complexity, in Pietro Baroni, Dov Gabbay, Massimiliano Giacomin and Leendert van der Torre (eds), Handbook of Formal Argumentation, volume 1, College Publications (2018)
    locator: Section 3.3, Table 1 and Reduction 3.8 (grounded acceptance is P-complete)
  - paper: doi:10.1016/0743-1066(84)90014-1
    title: William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 267 to 284 (1984)
    locator: the whole paper (the same counter method for Horn formulas)
---

This algorithm computes the [grounded extension](/grounded-extension/) of a finite framework in time linear in the number of arguments plus the number of attacks. It keeps, for each argument, the number of its attackers that are not yet rejected. An argument whose count is 0 is accepted, and the arguments it attacks are rejected, which lowers the counts of the arguments they attack. The output is the grounded labelling: the grounded extension, the arguments it attacks, and the rest. The [grounded extension](/grounded-extension/) page gives the definition and its properties; this page gives the algorithm, its proof and its cost. For the complexity of the decision problems, see [argument acceptance](/argument-acceptance-problem/).

## In plain words

Each argument starts as undecided. An argument that nobody attacks is safe, so accept it. Each argument that an accepted argument attacks is now beaten, so reject it. A beaten argument can no longer hurt anybody, so each argument it attacks has one attacker fewer to worry about. When all the attackers of an argument are beaten, that argument is safe too, so accept it and go on.

To do this fast, keep a counter on each argument: the number of its attackers that are not beaten yet. Put the arguments with a counter of zero in a queue. Take them out one at a time. When the queue is empty, stop. The accepted arguments are the grounded extension. The arguments that stay undecided are the ones that depend on a cycle of attacks that nothing breaks.

## The problem

The input is a finite framework $(A, R)$: a set $A$ of $n$ arguments and a set $R \subseteq A \times A$ of $m$ attacks, where $(a, b) \in R$ means that $a$ attacks $b$. Self-attacks are allowed. For a set $S$, $S^+$ is the set of the arguments that $S$ attacks, and the characteristic function $F(S)$ is the set of the arguments that $S$ defends. The grounded extension $G$ is the least fixed point of $F$ (Dung 1995, Definition 20), which is also the least [complete extension](/complete-extension/) (Theorem 25). The output is the labelling that maps each member of $G$ to in, each member of $G^+$ to out, and every other argument to undec.

## The algorithm

For each argument $a$, the list $succ[a]$ holds the arguments that $a$ attacks. One pass over $R$ builds these lists and the counts.

```pseudo id=main
GROUNDED(A, R)
L1  for each a in A do count[a] ← the number of attackers of a
L2  for each a in A do label[a] ← undec
L3  Q ← a queue of the arguments a with count[a] = 0
L4  while Q is not empty do
L5      a ← take the first argument out of Q
L6      label[a] ← in                           ▷ all attackers of a are out
L7      for each b in succ[a] do
L8          if label[b] = undec then
L9              label[b] ← out                  ▷ b is attacked by an in argument
L10             for each c in succ[b] do
L11                 count[c] ← count[c] - 1
L12                 if count[c] = 0 then put c in Q
L13 return label
```

Line L3 starts with the arguments that have no attacker. Line L8 skips an argument that is already out, so each argument is labelled out once and its attacks are scanned once. An argument that line L5 takes out of $Q$ is never out, and an argument that line L7 reaches is never in, so line L8 needs only the one test. A self-attacking argument never reaches count 0, because it is its own attacker and it is never out. The queue can be a stack: the order does not change the result.

## Example

Take seven arguments and eight attacks: $a \to b \to c \to d \to e$, the cycle $e \leftrightarrow f$, and an argument $g$ that attacks itself and $d$. So $R = \{(a,b), (b,c), (c,d), (d,e), (e,f), (f,e), (g,g), (g,d)\}$.

| argument | a | b | c | d | e | f | g |
|---|---|---|---|---|---|---|---|
| attackers | none | a | b | c, g | d, f | e | g |
| count at the start | 0 | 1 | 1 | 2 | 2 | 1 | 1 |

The run, with the counts of $a, \ldots, g$ after each step:

| step | taken from Q | in | out | counts | Q after |
|---|---|---|---|---|---|
| start | | | | 0 1 1 2 2 1 1 | $a$ |
| 1 | $a$ | $a$ | $b$ | 0 1 0 2 2 1 1 | $c$ |
| 2 | $c$ | $c$ | $d$ | 0 1 0 2 1 1 1 | empty |

In step 1, $a$ is labelled in, its target $b$ is labelled out, and the scan of the attack $(b, c)$ brings the count of $c$ to 0. In step 2, $c$ is labelled in, $d$ is labelled out, and the scan of $(d, e)$ brings the count of $e$ from 2 to 1. Then the queue is empty. The result is $G = \{a, c\}$ with $G^+ = \{b, d\}$, and $e$, $f$ and $g$ stay undec. The run takes 2 queue steps and scans 4 of the 8 attacks: $(a, b)$, $(b, c)$, $(c, d)$ and $(d, e)$.

The iteration of the characteristic function gives the same set: $F(\emptyset) = \{a\}$, $F(\{a\}) = \{a, c\}$ and $F(\{a, c\}) = \{a, c\}$. The argument $e$ is not in $G$: its attacker $d$ is out, but its other attacker $f$ is attacked only by $e$, and nothing breaks the cycle. The argument $g$ attacks itself, so it is never in, and it stays undec. The framework has two other complete extensions, $\{a, c, e\}$ and $\{a, c, f\}$, and both contain $G$.

## Correctness

Five invariants hold at line L4. Each count is the number of attackers that are not out. Each argument in $IN$ or in $Q$ has all its attackers out. Each out argument has an in attacker. The in, out and queued arguments are disjoint. Each argument is pushed at most once. Two lemmas follow. First, by induction on the run, each in argument is in every complete extension $E$, because $E$ defends it and $E = F(E)$. Second, when the queue is empty, the in set $IN$ is conflict-free, $IN^+$ is exactly the out set, and $IN = F(IN)$: an argument that $IN$ defends has count 0, so it was pushed and later labelled in. So $IN$ is a complete extension that is contained in every complete extension, and that is the grounded extension.

## Complexity

Lines L1 to L3 take $\Theta(n + m)$ time. Each argument is pushed at most once, so lines L5 and L6 run at most $n$ times, in fact exactly $|G|$ times. Line L7 scans the attacks that leave an argument when it becomes in, and line L10 scans the attacks that leave an argument when it becomes out. No argument becomes both, so each attack is scanned at most once in the whole run, and lines L7 to L12 run at most $m$ times. The total is $\Theta(n + m)$ time in the worst case and in the best case on the [word RAM](/word-ram/), because the input must be read. The extra space is $\Theta(n + m)$ for the lists, the counts, the labels and the queue. The tests count the queue steps and the scanned attacks on random frameworks and on a chain of 3000 arguments, and check that the steps equal $|G| \le n$ and the scans are at most $m$.

For comparison, the direct iteration $\emptyset, F(\emptyset), F(F(\emptyset)), \ldots$ computes each $F(S)$ in $\Theta(n + m)$ time and can need about $n/2$ rounds: on the chain $x_1 \to x_2 \to \cdots \to x_n$ each round adds one argument. That is $\Theta(n(n + m))$ time. The labelling loop of Modgil and Caminada, as implemented before 2021, runs in $O(n + |G| \cdot m)$ time (Nofal, Atkinson and Dunne 2021, Theorem 3).

The decision problem "is $a$ in the grounded extension" is P-complete (Dvořák and Dunne, Table 1), so a linear-time sequential algorithm is the best one can hope for, and a fast parallel algorithm is unlikely.

## Properties

- **Exact and deterministic.** The result does not depend on the order of the arguments or on the order in which the queue hands them out. The tests rename the arguments at random and compare.
- **Gives the labelling, not only the set.** The out arguments are exactly $G^+$, so the run also gives the range $G \cup G^+$ and the undec part, at no extra cost. This is the grounded [labelling](/argument-labelling/).
- **Sceptical and credulous at once.** The grounded extension is unique, so an argument is credulously accepted under grounded semantics exactly when it is sceptically accepted, and both questions are answered by one run.
- **Not incremental.** One new attack can change the result far away. In the chain $y \to z \to w \to x$ the grounded extension is $\{y, w\}$. Add the attack $(x, y)$: now the four arguments form a cycle and the grounded extension is empty. So after a change to $R$, run the algorithm again.
- **The same pattern as Horn forward chaining.** Line L3 is the set of facts, an in argument is a derived fact, and a count is the number of body atoms not yet derived. The difference is the two-step update: an argument becomes in, then its targets become out, and only out arguments lower the counts.

## Variants and improvements

- **Fixed-point iteration.** Compute $F(\emptyset)$, $F^2(\emptyset)$, and so on, until two steps agree. This is the definition of Dung (1995) for finite frameworks and it is easy to check, but it is quadratic in the worst case. The tests use it as the reference.
- **Labelling loop.** Modgil and Caminada (2009) label in the undec arguments whose attackers are all out, then label out the arguments that an in argument attacks, and repeat. Each round scans all arguments, which gives the $O(n + |G| \cdot m)$ bound above.
- **Recursive form.** Nofal, Atkinson and Dunne (2021) also give a recursive version (their Algorithm 4) with the same idea: accept an argument, reject its targets, and recurse on the arguments whose last open attacker was just rejected.
- **Stop at the query.** To decide whether one argument $q$ is in $G$, stop when $q$ is labelled in or out. In the worst case the bound does not change.
- **Games and logic programs.** If a move from $a$ goes to an attacker of $a$, then the in, out and undec labels are the lost, won and drawn positions of [retrograde analysis](/retrograde-analysis/) for the player to move, and the algorithm is that analysis. The grounded extension of the framework built from a normal logic program corresponds to its [well-founded](/well-founded-semantics/) model (Dung 1995, Section 4), but a general program needs more than this algorithm, for example the [alternating fixpoint](/alternating-fixpoint/).

## When to use it

Use it whenever the grounded extension or the grounded labelling of a finite framework is needed: as the sceptical answer of a reasoner, as the first step of a search for [preferred](/preferred-extension/) or other complete extensions (every complete extension contains $G$, and every argument in $G^+$ is out in each of them), and as a fast filter before a call to a SAT solver. It reads the input once, so it is optimal up to a constant factor. It does not compute other semantics: the preferred and stable extensions need search, and the acceptance problems for them are NP-hard or harder.

## Pitfalls

- **Lowering counts when an argument becomes in.** The count of $c$ must drop when an attacker of $c$ becomes out, not when it becomes in. A program that lowers the count of the targets of an in argument accepts wrong arguments.
- **Repeated attacks.** If the input is a list with the same attack twice, line L1 counts it twice. Either remove duplicates first or keep one list entry for each copy, so that the count can still reach 0. The Python version takes $R$ as a set.
- **Labelling an argument out twice.** Without the test of line L8, an argument attacked by two in arguments lowers the counts of its targets twice, and a count can reach 0 too early or go below 0.
- **Self-attacks.** An argument that attacks itself must count itself as an attacker. If the program drops self-loops, the argument is accepted, and the result is not even conflict-free.
- **Rescanning all arguments after each change.** A loop that looks for a new zero-count argument by scanning the whole framework is correct but quadratic.
- **Unknown arguments.** An attack that names an argument outside $A$ breaks the counts. The Python version rejects such input with an error.

## Implementations

## History

Dung defined the grounded extension in 1995 as the least fixed point of the characteristic function, and showed that for finitary frameworks it is the limit of the iteration from the empty set. Modgil and Caminada described labelling algorithms for the main semantics in 2009, and the early solvers implemented their loop for the grounded case. Nofal, Atkinson and Dunne published the counter method with a proof of the linear bound in 2021. The same counting idea is older in logic: it is the linear-time Horn satisfiability algorithm of Dowling and Gallier (1984).

## References
