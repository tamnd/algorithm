---
tag: N9RYM5
kind: algorithm
slug: emerson-lei-algorithm
name: Emerson-Lei algorithm
aliases:
- Fair CTL model checking
- Emerson-Lei fixed-point evaluation
- Emerson-Lei fair cycle detection
area: logic-and-constraints/model-checking
level: advanced
summary: Evaluate nested mu-calculus fixed points and keep inner values when the signs agree, in time polynomial for each alternation depth. The name also covers its fixed-point formula for fair EG.
solves: [mu-calculus-model-checking]
model: word-ram
complexity:
  vars: {m: the number of states plus the number of transitions, f: the number of symbols of the formula, n: the number of states, k: the number of fixed-point operators, d: the alternation depth}
  time: {worst: O(m·f·(1+k·n)^d), best: O(m·f)}
  space: {extra: O(m + f·n)}
properties: {deterministic: true, exact: true, online: false, recursive: true, in_place: false}
history:
  year: 1986
  people: [E. Allen Emerson, Chin-Laung Lei]
  note: Emerson and Lei defined alternation depth, showed that inner fixed points of the same sign need not be restarted, and gave the fixed-point formula for fair EG.
prereqs: [modal-mu-calculus, fixed-point, mu-calculus-model-checking]
see_also: [mu-calculus-model-checking, modal-mu-calculus, fixed-point, fairness, ctl-labelling-algorithm, symbolic-model-checking, zielonka-algorithm, parity-game]
sources:
  - paper: "E. Allen Emerson and Chin-Laung Lei, Efficient model checking in fragments of the propositional mu-calculus, Proceedings of the First IEEE Symposium on Logic in Computer Science (LICS 1986), pages 267 to 278"
    locator: the definition of alternation depth, the evaluation of nested fixed points that keeps inner values of the same sign, its time bound, and the fixed-point characterization of fair EG
  - paper: doi:10.1016/0167-6423(87)90036-0
    title: E. Allen Emerson and Chin-Laung Lei, Modalities for model checking, branching time logic strikes back, Science of Computer Programming 8(3), 1987, pages 275 to 306
    locator: model checking of CTL with fairness constraints and its complexity
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 6 (symbolic model checking with fairness and the fixed-point formula for fair EG) and Chapter 7 (model checking the mu-calculus, the evaluation of fixpoint formulas and the improvement that reuses inner values)
  - book: "Julian Bradfield and Igor Walukiewicz, The mu-calculus and model checking, in Edmund M. Clarke, Thomas A. Henzinger, Helmut Veith and Roderick Bloem (eds.), Handbook of Model Checking, Springer, 2018"
    locator: Chapter 26 (fixed-point iteration, approximants, and the cost of nested fixed points)
  - paper: "David E. Long, Anca Browne, Edmund M. Clarke, Somesh Jha and Wilfredo R. Marrero, An improved algorithm for the evaluation of fixpoint expressions, CAV 1994, Lecture Notes in Computer Science 818, Springer, pages 338 to 350"
    locator: the refinement of the Emerson-Lei method that stores more intermediate values to halve the exponent
---

The Emerson-Lei algorithm decides [mu-calculus model checking](/mu-calculus-model-checking/): it computes the set of states of a [Kripke structure](/kripke-structure/) that satisfy a formula of the [modal mu-calculus](/modal-mu-calculus/). It evaluates each least or greatest fixed point by iteration, as on the [fixed point](/fixed-point/) page, with one improvement. When an inner fixed point has the same sign as the fixed points around it, its last value is a correct start for the next round, so it is not restarted. Only a change of sign forces a restart. As a result, the cost grows with the alternation depth $d$ of the formula, not with its nesting depth: the bodies are evaluated at most $k\,(1 + kn)^d$ times for $k$ fixed points and $n$ states. Emerson and Lei gave the method in 1986, in the paper that defined alternation depth. The same paper gave the fixed-point formula for fair $\mathsf{EG}$, and in work on symbolic model checking "the Emerson-Lei algorithm" usually means that formula; this page covers both.

## In plain words

The formula says "repeat this step until nothing changes", and some of these repeats sit inside other repeats. The simple method restarts every inner repeat from scratch each time the outer one moves on. That costs a lot when the repeats are deeply nested.

There are two kinds of repeat. One grows a set from nothing, and the other shrinks a set from everything. If an inner repeat is of the same kind as the outer one, the outer change only pushes the inner answer further in the direction it was already going. So the inner repeat can go on from where it stopped. Only when the kinds differ must the inner repeat start again.

The work then depends on how often the two kinds switch along the nesting, which is small in practice.

## The problem

Given a finite Kripke structure $M = (S, I, R, L)$ with $n = |S|$, and a closed formula $\varphi$ of the modal mu-calculus in positive normal form in which each variable is bound once, compute $[\![\varphi]\!] \subseteq S$. The size of the input is $|M| = |S| + |R|$ and $|\varphi|$. The formula has $k$ fixed-point operators and alternation depth $d$, the largest number of sign blocks on a chain of nested fixed points.

## The algorithm

The algorithm keeps a value $V[X] \subseteq S$ for each bound variable $X$. $\mathrm{START}(X)$ is $\emptyset$ when $X$ is bound by $\mu$ and $S$ when it is bound by $\nu$. For a fixed point $\sigma X.\, \alpha$, the list of *opposite* variables of $X$ holds the variables bound inside $\alpha$ by the other sign.

```pseudo id=main
EVAL(ψ)                                      ▷ returns [[ψ]] under the current values V
L1  case ψ of
L2  true, false, p, ¬p:   return the matching set of states
L3  X:                    return V[X]
L4  α ∧ β, α ∨ β:         return EVAL(α) ∩ EVAL(β), or EVAL(α) ∪ EVAL(β)
L5  ◇α, □α:               A ← EVAL(α); return { s : some t ∈ R(s) is in A }, or { s : R(s) ⊆ A }
L6  σX. α:                ▷ σ is μ or ν; go on from the stored value V[X]
L7      loop
L8          N ← EVAL(α)
L9          if N = V[X] then return N
L10         V[X] ← N
L11         for each opposite variable Y of X do
L12             V[Y] ← START(Y)

EMERSON-LEI(M, φ)                            ▷ φ closed, in positive normal form, each variable bound once
L13 for each bound variable X of φ do V[X] ← START(X)
L14 return EVAL(φ)
```

The plain nested iteration is the same code with one more line before L7: $V[X] \leftarrow \mathrm{START}(X)$, so that each fixed point restarts at each entry. The Emerson-Lei version drops it, and makes up for it with the resets of lines L11 and L12, which happen only when an outer value really changes.

## Example

**Infinitely often.** Take $\mathsf{E}\,\mathsf{G}\mathsf{F}\,p = \nu X.\, \mu Y.\, ((p \wedge \Diamond X) \vee \Diamond Y)$ on the states $0, 1, 2, 3$ with edges $0 \to 1$, $0 \to 2$, $1 \to 0$, $2 \to 3$, $3 \to 3$ and $p$ in $1$ and $2$. Line L13 sets $V[X] = S$ and $V[Y] = \emptyset$.

| round of $X$ | $V[X]$ | evaluations of the $Y$ body | $Y$ result | change |
|---|---|---|---|---|
| 1 | $\{0, 1, 2, 3\}$ | $\{1, 2\}$, $\{0, 1, 2\}$, $\{0, 1, 2\}$ | $\{0, 1, 2\}$ | $X$ shrinks, $Y$ reset |
| 2 | $\{0, 1, 2\}$ | $\{1\}$, $\{0, 1\}$, $\{0, 1\}$ | $\{0, 1\}$ | $X$ shrinks, $Y$ reset |
| 3 | $\{0, 1\}$ | $\{1\}$, $\{0, 1\}$, $\{0, 1\}$ | $\{0, 1\}$ | none, return |

The answer is $\{0, 1\}$ after $12$ body evaluations. The inner fixed point has the other sign, so it is reset each round, and plain nested iteration does the same $12$ evaluations.

**Reuse.** Take $\mu X.\, (\mu Y.\, r \vee (q \wedge \Diamond Y)) \vee (p \wedge \Diamond X)$ on the path $0 \to 1 \to 2 \to 3 \to 4 \to 5 \to 5$, with $p$ in $0, 1, 2$, $q$ in $3, 4$ and $r$ in $5$. Both fixed points are least. In the first round of $X$, the inner $Y$ needs $4$ evaluations to reach $\{3, 4, 5\}$. Then $X$ grows to $\{3, 4, 5\}$, $\{2, \ldots, 5\}$, $\{1, \ldots, 5\}$, $\{0, \ldots, 5\}$ and stops, $5$ evaluations of its body in all. In the four later rounds, $Y$ starts from $\{3, 4, 5\}$ and stops after $1$ evaluation each. The total is $4 + 4 + 5 = 13$ evaluations, against $5 \cdot 4 + 5 = 25$ for nested iteration.

**Why the reset is needed.** Take the states $2, 3, 4$ with edges $2 \to 4$, $3 \to 3$, $3 \to 2$, $4 \to 4$, and $p$ only in $2$, and the same $\mathsf{E}\,\mathsf{G}\mathsf{F}\,p$ formula. No path visits $p$ infinitely often, and the algorithm returns $\emptyset$. If line L12 were left out, $Y$ would keep its value $\{2, 3\}$ from the first round when $X$ shrinks to $\{2, 3\}$. The inner iteration would then stop at $\{3\}$, which is a fixed point of $\Diamond Y$ but not the least one, and the answer would wrongly be $\{3\}$.

## Correctness

Call the values $V$ *sound* for a variable $X$ bound by $\mu X.\, \alpha$ if $V[X] \subseteq f(V[X])$ and $V[X] \subseteq \mu f$, where $f(T) = [\![\alpha]\!]_{V[X \mapsto T]}$ depends on the current values of the variables around $X$. For $\nu$ the inclusions are reversed. The start values are sound. Every change made by lines L10 to L12 moves all changed variables in one direction: when a $\mu$ variable grows, the opposite variables inside it are reset to $S$, which is also growth. Growth of the variables around a $\mu$ fixed point keeps it sound by monotonicity, and growth of those around a $\nu$ fixed point is exactly the case that the reset covers. So soundness holds at all times. Under soundness, the loop of lines L7 to L10 starts below the least fixed point and climbs monotonically, so it stops exactly at $\mu f$; dually for $\nu$. By induction on $\psi$, EVAL returns $[\![\psi]\!]$. The full proof, with the cost bound, is in [the correctness proof](proofs/correctness.md).

## Complexity

Count body evaluations, that is, executions of line L8.

- Between two resets, the value of a variable changes only at line L10, and always in the same direction, so it changes at most $n$ times.
- A variable is reset once for each change of an enclosing variable of the other sign, and such a variable lies in an earlier sign block.
- Summing block by block, the total number of changes is less than $\prod_{\ell} (1 + k_\ell n) \le (1 + kn)^d$, where $k_\ell$ is the number of fixed points in block $\ell$.
- Each execution of line L8 for $X$ either changes $V[X]$ or ends an entry of $X$, and $X$ is entered once per body evaluation of the fixed point around it. So each fixed point is evaluated at most $(1 + kn)^d$ times, and all of them at most $k\,(1 + kn)^d$ times.

One body evaluation, without the nested fixed points it contains, costs $O(|\alpha|\,|M|)$: each $\Diamond$ or $\Box$ is one pass over the edges, and each $\wedge$, $\vee$ and comparison is one pass over the states. Each symbol of $\varphi$ belongs to the body of exactly one innermost enclosing fixed point, or to the top level, so the time is $O(|M|\,|\varphi|\,(1 + kn)^d)$. Since $1 + kn \le (k + 1)\,n$, this is at most $O(|M|\,|\varphi|\,(k + 1)^d\,n^d)$, polynomial for each fixed $d$. Plain nested iteration needs up to $k\,(n + 1)^q$ evaluations, where $q \ge d$ is the nesting depth, so its bound is exponential in the nesting even for a formula without alternation.

The space is $O(|M|)$ for the structure, $O(kn)$ for the stored values, and $O(|\varphi|\,n)$ for the sets held on the recursion stack.

## Properties

- **Global.** It computes $[\![\varphi]\!]$ for all states at once.
- **Symbolic-friendly.** It uses only $\cup$, $\cap$, the one-step operators and set equality, so each set can be a [BDD](/binary-decision-diagram/), which is how [symbolic model checkers](/symbolic-model-checking/) use it.
- **Alternation-free formulas.** With $d = 1$ the evaluation count is at most $k\,(1 + kn)$, so the time is $O(|M|\,|\varphi|\,kn)$. This is polynomial but not linear, because each fixed point is found by repeated passes. The [CTL labelling algorithm](/ctl-labelling-algorithm/) and the algorithm of Cleaveland and Steffen (1993) reach linear time by backward search instead of iteration.
- **Monotone approximants.** Between resets, each stored value is an approximant of its fixed point: a set of states that are known to satisfy a $\mu$ formula, or a set that contains all states that satisfy a $\nu$ formula.
- **Deterministic and exact.**

## Variants and improvements

- **Fair $\mathsf{EG}$.** Emerson and Lei expressed $\mathsf{E}_J\mathsf{G}\,p$, "some path keeps $p$ forever and visits each of $J_1, \ldots, J_r$ infinitely often", as
$$\nu Z.\, p \wedge \bigwedge_{i=1}^{r} \mathsf{EX}\,\mathsf{E}[p\,\mathsf{U}\,(Z \wedge J_i)],$$
an alternation-depth-$2$ formula, proved correct in [the correctness proof](proofs/correctness.md). Each round of $Z$ is $r$ backward searches, so on explicit graphs it costs $O(r\,n\,|M|)$, and symbolically $O(r\,n^2)$ image steps. The rest of fair CTL follows from it: $\mathit{fair} = \mathsf{E}_J\mathsf{G}\,\mathit{true}$, $\mathsf{E}_J\mathsf{X}\,\alpha = \mathsf{EX}(\alpha \wedge \mathit{fair})$ and $\mathsf{E}_J[\alpha\,\mathsf{U}\,\beta] = \mathsf{E}[\alpha\,\mathsf{U}\,(\beta \wedge \mathit{fair})]$. On explicit graphs the SCC method of the [fairness](/fairness/) page is faster; symbolic tools use this formula, or the lockstep method of Bloem, Gabow and Somenzi (2000) with $O(n \log n)$ image steps.
- **Fewer iterations.** Long, Browne, Clarke, Jha and Marrero (1994) store intermediate values for each tuple of outer values and need about $n^{\lceil d/2 \rceil + 1}$ iterations, at a large cost in space; Seidl (1996) gave a simpler method with a similar bound.
- **Local evaluation.** [Local model checking](/local-model-checking/) evaluates only the pairs (state, subformula) that a given state needs.
- **Through games.** Building the [parity game](/parity-game/) of the formula and solving it with [Zielonka's algorithm](/zielonka-algorithm/), small progress measures or a quasi-polynomial method gives better worst-case bounds; see [mu-calculus model checking](/mu-calculus-model-checking/).
- **Closed subformulas.** A fixed-point subformula with no free variable has a value that never changes. Evaluating it once and then treating it as an atomic proposition removes it from the count, so that nested closed subformulas, as in CTL, no longer raise the alternation depth.

## When to use it

Use it for formulas of small alternation depth, which covers CTL, fair CTL and most hand-written mu-calculus properties, and in particular in symbolic model checkers, where each step is a BDD operation. For explicit structures and CTL, the [CTL labelling algorithm](/ctl-labelling-algorithm/) is linear and simpler. For formulas of high alternation depth, or for large explicit structures, reduce to a [parity game](/parity-game/) and use a game solver.

## Pitfalls

- **Forgetting the reset.** Without lines L11 and L12, an inner fixed point of the other sign keeps a value that is too large (for $\mu$) or too small (for $\nu$), and the result is wrong; the example above shows it.
- **Resetting only the direct children.** The reset must reach every opposite fixed point inside the body, also those nested below a fixed point of the same sign.
- **Formulas not in positive normal form.** The monotone climb needs each variable to occur positively. Push negations to the atoms first, using $\neg \mu Z.\, \alpha = \nu Z.\, \neg \alpha[\neg Z / Z]$.
- **Reused variable names.** If one name is bound twice, the stored values clash. Rename first; the implementation rejects such formulas.
- **States without successors.** $\Box \alpha$ holds at a state with no successor, so translations from CTL that assume a total relation give wrong answers there.
- **Two meanings of the name.** "Emerson-Lei" also names the Emerson-Lei acceptance condition of omega-automata, a Boolean combination of "infinitely often" and "finitely often" conditions, which is a different subject.

## Implementations

## History

Kozen defined the modal mu-calculus in 1983, and evaluation by nested iteration was the obvious method. In 1986, at the first LICS, Emerson and Lei defined alternation depth and showed that only a change of sign forces an inner fixed point to restart, which made the cost polynomial for each fixed alternation depth. In the same paper they expressed fair $\mathsf{EG}$ as a fixed point, and their 1987 paper studied model checking with fairness in detail. Burch, Clarke, McMillan, Dill and Hwang (1990) computed such fixed points with BDDs, and the fair $\mathsf{EG}$ formula became the standard fair cycle test in symbolic model checkers. Later work by Long et al. (1994), Seidl (1996) and the parity game algorithms lowered the bounds for high alternation depth.

## References
