---
tag: MPCBDS
kind: technique
slug: abstract-interpretation
name: Abstract interpretation
aliases:
- Cousot framework
area: foundations/correctness-and-invariants
level: research
summary: Sound static analysis by computing over abstract domains that over-approximate concrete program behaviour.
prereqs: [loop-invariant, inductive-invariant, fixed-point, knaster-tarski-theorem]
see_also: [program-verification, rice-theorem, halting-problem, symbolic-execution, interval-arithmetic, hoare-logic]
sources:
  - paper: "Patrick Cousot and Radhia Cousot, Static determination of dynamic properties of programs, Proceedings of the Second International Symposium on Programming, Dunod, Paris (1976)"
    locator: pp. 106 to 130 (interval analysis, the first widening and narrowing operators)
  - paper: doi:10.1145/512950.512973
    title: Patrick Cousot and Radhia Cousot, Abstract interpretation, a unified lattice model for static analysis of programs by construction or approximation of fixpoints, POPL 1977
    locator: pp. 238 to 252 (abstraction and concretization maps, fixpoint approximation, widening and narrowing)
  - paper: doi:10.1145/567752.567778
    title: Patrick Cousot and Radhia Cousot, Systematic design of program analysis frameworks, POPL 1979
    locator: pp. 269 to 282 (Galois connections, the best abstract transformer, reduced product)
  - paper: doi:10.1145/512760.512770
    title: Patrick Cousot and Nicolas Halbwachs, Automatic discovery of linear restraints among variables of a program, POPL 1978
    locator: pp. 84 to 96 (the polyhedra domain)
  - paper: doi:10.1007/s10990-006-8609-1
    title: Antoine Mine, The octagon abstract domain, Higher-Order and Symbolic Computation 19(1) (2006)
    locator: pp. 31 to 100
  - paper: doi:10.1007/BFb0039704
    title: Francois Bourdoncle, Efficient chaotic iteration strategies with widenings, Formal Methods in Programming and Their Applications (FMPA 1993), LNCS 735, Springer
    locator: pp. 128 to 141 (iteration orders and the choice of widening points)
  - paper: doi:10.1145/512927.512945
    title: Gary A. Kildall, A unified approach to global program optimization, POPL 1973
    locator: pp. 194 to 206 (dataflow analysis over a lattice)
  - paper: doi:10.1145/781131.781153
    title: Bruno Blanchet, Patrick Cousot, Radhia Cousot, Jerome Feret, Laurent Mauborgne, Antoine Mine, David Monniaux and Xavier Rival, A static analyzer for large safety-critical software, PLDI 2003
    locator: pp. 196 to 207 (the Astree analyzer, its domains, widening with thresholds)
  - book: doi:10.1007/978-3-662-03811-6
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer (1999)
    locator: Chapter 2 (Data Flow Analysis) and Chapter 4 (Abstract Interpretation)
---

Abstract interpretation is a technique for sound static analysis. It runs the program on descriptions of sets of values, called abstract values, instead of on single values, and it computes an over-approximation of all the states that the program can reach. Cousot and Cousot gave interval analysis with widening in 1976, the general theory in 1977, and the systematic use of Galois connections in 1979. With a widening the analysis finishes. It never misses a reachable state, but it may report states that no run reaches.

## In plain words

Think of a program that adds numbers in a loop. You cannot try all inputs. But you can ask a coarser question: is the value always positive, or always between 0 and 100? Such an answer describes many values at once.

Abstract interpretation runs the program on descriptions. When the program adds two values that are "positive", the result is "positive". When it adds "positive" to "negative", the result is "unknown", because the answer could be anything. In a loop, the description grows pass after pass. To make the analysis stop, the tool jumps to a safe bound, such as "any value from 0 up", after a few passes.

The result holds in every run, but it may be weak. If the tool says that a division by zero cannot happen, you can trust it. If it says that it may happen, the program may still be correct.

## When it applies

Use it to compute facts that hold at each point of every run: the range of a variable, its sign, the absence of a division by zero, of an array index out of bounds, of an overflow, or of a null pointer use. It finds a [loop invariant](/loop-invariant/) with no help from the user.

It fits when an exact answer is not needed, and a sound answer with false alarms is acceptable. The exact question is out of reach: by [Rice's theorem](/rice-theorem/), no algorithm decides each nontrivial semantic property of programs, and the [halting problem](/halting-problem/) is undecidable. So the technique gives up completeness and keeps soundness.

It does not fit when each report of a possible error must be a true error. For that, use testing or [symbolic execution](/symbolic-execution/), which find real runs but do not cover all of them.

## The template

**Step 1: the concrete semantics.** Let $(C, \sqsubseteq)$ be a complete lattice of sets of states, for example $C = \mathcal{P}(\mathbb{Z})$ ordered by inclusion for the values of one variable. Let $\mathit{Init}$ be the set of initial states and $\mathit{post}(X)$ the set of states one step after a state in $X$. Let $F(X) = \mathit{Init} \cup \mathit{post}(X)$. This $F : C \to C$ is monotone, and the set of states that the program reaches is its least fixed point $\mathrm{lfp}\ F$, which exists by the [Knaster-Tarski theorem](/knaster-tarski-theorem/). Since $\mathit{post}$ preserves unions, $\mathrm{lfp}\ F = \bigcup_{k \ge 0} \mathit{post}^k(\mathit{Init})$: the states reached in $0, 1, 2, \ldots$ steps.

**Step 2: an abstract domain.** Choose a poset $(A, \sqsubseteq)$ of abstract values and a *concretization* $\gamma : A \to C$ that gives the set of states that an abstract value stands for. The pair $(\alpha, \gamma)$ with $\alpha : C \to A$ is a *Galois connection* when

$$ \forall c \in C,\ a \in A : \quad \alpha(c) \sqsubseteq a \iff c \sqsubseteq \gamma(a). $$

Then $\alpha(c)$ is the best abstract value for $c$: the least $a$ with $c \sqsubseteq \gamma(a)$. Two facts follow directly. The map $\gamma$ is monotone: let $a \sqsubseteq a'$. The connection with $c = \gamma(a)$ gives $\alpha(\gamma(a)) \sqsubseteq a$, so $\alpha(\gamma(a)) \sqsubseteq a'$, and the connection again gives $\gamma(a) \sqsubseteq \gamma(a')$. And $c \sqsubseteq \gamma(\alpha(c))$, from $\alpha(c) \sqsubseteq \alpha(c)$.

**Step 3: an abstract transformer.** Define a monotone $F^\# : A \to A$ that is *sound*:

$$ \forall a \in A : \quad F(\gamma(a)) \sqsubseteq \gamma(F^\#(a)). $$

With a Galois connection this is the same as $\alpha(F(\gamma(a))) \sqsubseteq F^\#(a)$. The best choice is $F^\# = \alpha \circ F \circ \gamma$.

**Step 4: compute an abstract post-fixed point.** Find $a \in A$ with $F^\#(a) \sqsubseteq a$.

**Soundness theorem.** If $F^\#$ is sound and $F^\#(a) \sqsubseteq a$, then $\mathrm{lfp}\ F \sqsubseteq \gamma(a)$.

*Proof.* By soundness, $F(\gamma(a)) \sqsubseteq \gamma(F^\#(a))$. Since $F^\#(a) \sqsubseteq a$ and $\gamma$ is monotone, $\gamma(F^\#(a)) \sqsubseteq \gamma(a)$. So $F(\gamma(a)) \sqsubseteq \gamma(a)$: the element $\gamma(a)$ is a pre-fixed point of $F$. The least fixed point of a monotone function on a complete lattice is below each pre-fixed point (Knaster-Tarski). So $\mathrm{lfp}\ F \sqsubseteq \gamma(a)$. $\square$

**Widening.** In a domain with infinite ascending chains, the iteration $\bot, F^\#(\bot), F^\#(F^\#(\bot)), \ldots$ may never stop. A *widening* is an operator $\nabla : A \times A \to A$ such that $a \sqsubseteq a \nabla b$ and $b \sqsubseteq a \nabla b$, and such that for each sequence $y_0, y_1, \ldots$ the sequence $x_0 = \bot$, $x_{k+1} = x_k \nabla y_k$ is stable from some $k$ on. (Cousot and Cousot ask this only for increasing sequences $y_k$; the interval widening below meets the stronger form.) The iteration $x_0 = \bot$, $x_{k+1} = x_k \nabla F^\#(x_k)$ then stops at some $x_m = x_{m+1}$. At that point $F^\#(x_m) \sqsubseteq x_m \nabla F^\#(x_m) = x_m$, so $x_m$ is a post-fixed point and the theorem applies.

**Decreasing iteration.** If $F^\#(a) \sqsubseteq a$, then $F^\#(F^\#(a)) \sqsubseteq F^\#(a)$ by monotonicity, so $F^\#(a)$ is also a post-fixed point, and it is smaller. Repeating the step gives a more precise sound result at each step. A *narrowing* operator makes this phase stop in general. In a program with many loops, the analysis needs a widening only at a set of points that cuts each cycle of the control flow graph, for example the loop heads. Bourdoncle (1993) gives iteration orders that choose these points.

## Classic examples

**The sign domain.** The abstract values are $\bot$, $\mathit{neg}$, $\mathit{zero}$, $\mathit{pos}$ and $\top$, with $\bot$ below everything, $\top$ above everything, and the three middle values unordered. The meaning $\gamma$ gives $\emptyset$, $\{x < 0\}$, $\{0\}$, $\{x > 0\}$ and $\mathbb{Z}$. The map $\alpha(X)$ is the least value whose meaning contains $X$. This is a Galois connection between $\mathcal{P}(\mathbb{Z})$ and the sign domain. The abstract addition $\oplus$ is:

- $\bot \oplus b = a \oplus \bot = \bot$.
- $\mathit{zero} \oplus b = b$ and $a \oplus \mathit{zero} = a$.
- $\mathit{pos} \oplus \mathit{pos} = \mathit{pos}$ and $\mathit{neg} \oplus \mathit{neg} = \mathit{neg}$.
- In each other case the result is $\top$, for example $\mathit{pos} \oplus \mathit{neg} = \top$.

This operation is the best abstract transformer for addition, $\alpha(\gamma(a) + \gamma(b))$, for all 25 pairs. A loop $x \leftarrow 1$ ; $\mathbf{while}\ c\ \mathbf{do}\ x \leftarrow x + 1$ with an unknown condition $c$ has the function $F^\#(s) = \mathit{pos} \sqcup (s \oplus \mathit{pos})$ at the loop head. The iteration gives $\bot$, $\mathit{pos}$, $\mathit{pos}$, so $x$ is positive at the head. The concrete set is $\{1, 2, 3, \ldots\}$.

**The interval domain.** The abstract values are $\bot$ and the pairs $[l, u]$ with $l \le u$, where $l \in \mathbb{Z} \cup \{-\infty\}$ and $u \in \mathbb{Z} \cup \{+\infty\}$. The meaning is $\gamma([l, u]) = \{x \in \mathbb{Z} : l \le x \le u\}$. The map $\alpha(X)$ is $[\inf X, \sup X]$, and $\alpha(\emptyset) = \bot$. This is a Galois connection, since $X \subseteq \gamma([l, u])$ holds exactly when $l \le \inf X$ and $\sup X \le u$. The join is the smallest interval that contains both, and the meet is the intersection. The widening is

$$ \bot \nabla I = I \nabla \bot = I, \qquad [a, b] \nabla [c, d] = [\,c < a ? -\infty : a,\ \ d > b ? +\infty : b\,]. $$

A bound that moves jumps to infinity, and a bound that does not move stays. Each of the two bounds can jump only once, so a sequence $x_{k+1} = x_k \nabla y_k$ changes at most three times: once from $\bot$ to an interval, and once for each bound. So $\nabla$ is a widening. It is monotone in its second argument but not in its first; see the pitfalls.

**A worked loop analysis.** Analyze

$$ x \leftarrow 0\ ;\quad \mathbf{while}\ x < 100\ \mathbf{do}\ x \leftarrow x + 1. $$

At the loop head the concrete function is $F(X) = \{0\} \cup \{x + 1 : x \in X,\ x < 100\}$. Its least fixed point is $\{0, 1, \ldots, 100\}$. The abstract function is

$$ F^\#(I) = [0, 0] \sqcup \bigl((I \sqcap [-\infty, 99]) + 1\bigr), $$

where $+1$ moves both bounds by 1, and $\bot + 1 = \bot$. It is sound and is the best transformer for the interval domain.

*Plain iteration.* $(F^\#)^k(\bot) = [0, k - 1]$ for $1 \le k \le 101$, and $(F^\#)^{102}(\bot) = (F^\#)^{101}(\bot) = [0, 100]$. The iteration needs 101 steps to reach the result. In general the plain iteration need not stop.

*Iteration with widening.*

| $k$ | $x_k$ | $F^\#(x_k)$ | $x_{k+1} = x_k \nabla F^\#(x_k)$ |
| --- | --- | --- | --- |
| 0 | $\bot$ | $[0, 0]$ | $[0, 0]$ |
| 1 | $[0, 0]$ | $[0, 1]$ | $[0, +\infty]$ |
| 2 | $[0, +\infty]$ | $[0, 100]$ | $[0, +\infty]$ |

The iteration stops at $x_2 = [0, +\infty]$, and $F^\#(x_2) = [0, 100] \sqsubseteq x_2$. At the loop exit the guard is false, so the state is $x_2 \sqcap [100, +\infty] = [100, +\infty]$.

*Decreasing iteration.* Start from $[0, +\infty]$. Then $F^\#([0, +\infty]) = [0, 100]$, and $F^\#([0, 100]) = [0, 0] \sqcup [1, 100] = [0, 100]$. The loop head is now $[0, 100]$, the exact set. The loop exit is $[0, 100] \sqcap [100, +\infty] = [100, 100]$. The program has $x = 100$ at the exit, and the analysis proves it. The widened result alone proves only $x \ge 100$.

## Variations

- *Relational domains.* The interval domain keeps one interval for each variable. The octagon domain (Mine 2006) keeps constraints $\pm x \pm y \le c$, at a cubic cost in the number of variables for its closure. The polyhedra domain (Cousot and Halbwachs 1978) keeps any linear inequalities, at a cost that can be exponential.
- *Products and powersets.* A *reduced product* (Cousot and Cousot 1979) combines two domains, for example signs and intervals, and lets each refine the other. A powerset domain keeps a set of abstract values, to separate cases.
- *Thresholds.* A widening with thresholds jumps to the next number in a fixed list instead of to infinity, for example to 100 in the loop above. Astree uses it (Blanchet and others 2003).
- *Other domains.* Domains exist for pointers and the shape of the heap, and for floating-point values.
- *Dataflow analysis.* Kildall (1973) computed facts for compiler optimization as a fixed point over a lattice. These classic dataflow analyses, such as constant propagation, are instances of abstract interpretation with a finite-height domain, where no widening is needed (Nielson, Nielson and Hankin, Chapters 2 and 4).
- *Tools.* Astree (Blanchet and others 2003) is an analyzer for safety-critical embedded C code. It combines intervals, octagons and other domains.

## Pitfalls

- **Soundness depends on the concrete semantics.** If the real machine wraps around at 32 bits and the transformers use unbounded integers, the result can be wrong. The abstract operations must follow the machine.
- **Loss of relations.** After $y \leftarrow x$ ; $z \leftarrow x - y$ with $x \in [0, 10]$, the interval domain gives $y \in [0, 10]$ and $z \in [-10, 10]$. The exact value is $z = 0$. The domain forgets that $y$ equals $x$.
- **Widening is not monotone in its first argument.** $[0, 1] \nabla [0, 2] = [0, +\infty]$, but $[0, 2] \nabla [0, 2] = [0, 2]$, although $[0, 1] \sqsubseteq [0, 2]$. The result depends on the order in which the iteration runs, and a better input does not always give a better output.
- **A false alarm is not a bug.** A sound analysis reports a possible error when it cannot rule one out. The report may be wrong. Only the absence of a report is a proof.
- **Do not confuse a sound result with an exact one.** $\gamma(a)$ contains $\mathrm{lfp}\ F$ and may be larger.

## Exercises

1. Analyze $x \leftarrow 0$ ; $\mathbf{while}\ x < 100\ \mathbf{do}\ x \leftarrow x + 2$ in the interval domain with widening, and then with decreasing iteration until stable. What is the exit state? What is the concrete exit state? *Answer.* The widened head is $[0, +\infty]$. Then $F^\#([0, +\infty]) = [0, 101]$ and $F^\#([0, 101]) = [0, 101]$. The exit state is $[100, 101]$. The concrete exit state is $\{100\}$. The interval domain does not know that $x$ is even.
2. Show that $\alpha \circ \gamma$ is the identity on the interval domain. *Answer.* For $[l, u]$ with $l \le u$, the set $\gamma([l, u])$ has the infimum $l$ and the supremum $u$, so $\alpha(\gamma([l, u])) = [l, u]$. For $\bot$ both sides are $\bot$.
3. In the sign domain, find the least fixed point of $F^\#(s) = \mathit{pos} \sqcup (s \oplus \mathit{pos})$ by iteration from $\bot$. *Answer.* $\bot$, $\mathit{pos}$, $\mathit{pos}$. The fixed point is $\mathit{pos}$.
4. Show that the interval widening is monotone in its second argument: if $J \sqsubseteq J'$, then $I \nabla J \sqsubseteq I \nabla J'$. *Answer.* If $I$ or $J$ is $\bot$ the claim follows from $\bot \nabla J = J$ and $I \nabla \bot = I \sqsubseteq I \nabla J'$. Let $I = [a, b]$, $J = [c, d]$, $J' = [c', d']$ with $c' \le c$ and $d \le d'$. If $c < a$ then $c' < a$, and both lower bounds are $-\infty$. Otherwise the lower bound for $J$ is $a$, and the one for $J'$ is $a$ or $-\infty$, which is no larger. The upper bounds are the same with the order reversed.
5. Use a widening with the threshold list $\{100\}$: a lower bound that moves goes to $-\infty$, and an upper bound that moves goes to the least threshold at or above the new bound, or to $+\infty$ if there is none. Analyze the loop $x \leftarrow 0$ ; $\mathbf{while}\ x < 100\ \mathbf{do}\ x \leftarrow x + 1$ again. *Answer.* $x_1 = [0, 0]$ and $F^\#(x_1) = [0, 1]$, so $x_2 = [0, 100]$. Then $F^\#([0, 100]) = [0, 100]$, so the iteration stops at $[0, 100]$ without a decreasing phase, and the exit state is $[100, 100]$.

## References
