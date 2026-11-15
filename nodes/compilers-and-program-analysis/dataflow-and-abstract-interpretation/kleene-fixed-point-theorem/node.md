---
tag: XVZ2Y8
kind: theorem
slug: kleene-fixed-point-theorem
name: Kleene fixed-point theorem
aliases:
- Kleene iteration theorem
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: A continuous function on a complete partial order with a bottom has a least fixed point, the limit of the iterates from bottom.
prereqs: [fixed-point]
see_also: [knaster-tarski-theorem, maximal-fixed-point-solution, mop-mfp-coincidence-theorem, abstract-interpretation, widening-operator, kahn-process-network, semi-naive-evaluation, banach-fixed-point-theorem]
sources:
  - paper: doi:10.1016/0020-0190(82)90065-5
    title: "Jean-Louis Lassez, V. L. Nguyen and Elizabeth A. Sonenberg, Fixed point theorems and semantics: a folk tale, Information Processing Letters 14(3), 1982, 112-116"
    locator: the whole note (the history of the fixed-point theorems used in semantics, and how the iteration theorem came to carry the names of Kleene and Tarski)
  - paper: doi:10.2140/pjm.1955.5.285
    title: Alfred Tarski, A lattice-theoretical fixpoint theorem and its applications, Pacific Journal of Mathematics 5(2), 1955, 285-309
    locator: Theorem 1 (fixed points of a monotone function on a complete lattice, the version without continuity)
  - paper: doi:10.2140/pjm.1979.82.43
    title: Patrick Cousot and Radhia Cousot, Constructive versions of Tarski's fixed point theorems, Pacific Journal of Mathematics 82(1), 1979, 43-57
    locator: the least fixed point of a monotone function as the limit of an iteration from the bottom element through the ordinals
  - book: isbn:9780521784511
    title: B. A. Davey and H. A. Priestley, Introduction to Lattices and Order, second edition, Cambridge University Press, 2002
    locator: Chapter 8 (fixpoint theorems, complete partial orders and continuous maps, and the iteration of a continuous map from the bottom element)
---

The Kleene fixed-point theorem says how to compute a least fixed point. Start from the least element $\bot$, apply the function again and again, and take the limit of the values. If the order is a complete partial order and the function is continuous, the limit is the least fixed point. This is the reason that iterative solvers for [dataflow analysis](/dataflow-analysis/) and [abstract interpretation](/abstract-interpretation/) give the right answer, and the reason that a recursive definition has a meaning. It is not the [Kleene recursion theorem](/kleene-recursion-theorem/) of computability, which is a different result about programs that can refer to their own code.

## Statement

**Orders.** A *partial order* $(D, \sqsubseteq)$ is a set with a reflexive, antisymmetric and transitive relation. A *chain* is a sequence $x_0 \sqsubseteq x_1 \sqsubseteq x_2 \sqsubseteq \cdots$. The *least upper bound* $\bigsqcup_i x_i$, when it exists, is an element above every $x_i$ and below every other element above every $x_i$. $D$ is a *complete partial order*, or cpo, if it has a least element $\bot$ and every chain has a least upper bound.

**Functions.** $f : D \to D$ is *monotone* if $x \sqsubseteq y$ implies $f(x) \sqsubseteq f(y)$. It is *continuous*, in the sense of Scott, if it keeps the least upper bounds of chains: $f(\bigsqcup_i x_i) = \bigsqcup_i f(x_i)$ for every chain. A *fixed point* is an $x$ with $f(x) = x$, and a *pre-fixed point* is an $x$ with $f(x) \sqsubseteq x$.

**Theorem.** Let $D$ be a cpo and $f : D \to D$ continuous. Then:

1. $f$ is monotone, and the iterates $\bot, f(\bot), f^2(\bot), \ldots$ form a chain.
2. $\mu f = \bigsqcup_{n \ge 0} f^n(\bot)$ is a fixed point of $f$.
3. $\mu f \sqsubseteq x$ for every pre-fixed point $x$. So $\mu f$ is the least pre-fixed point and the least fixed point of $f$.

**The dual.** Turn the order upside down. If $D$ has a greatest element $\top$, every chain $x_0 \sqsupseteq x_1 \sqsupseteq \cdots$ has a greatest lower bound, and $f$ keeps these bounds, then $\bigsqcap_n f^n(\top)$ is the greatest fixed point and the greatest post-fixed point, that is the greatest $x$ with $x \sqsubseteq f(x)$. Dataflow analysis in the meet convention of Kildall uses this form: the [maximal fixed-point solution](/maximal-fixed-point-solution/) is the limit of the iterates from $\top$.

## In plain words

Start with no knowledge at all. Apply one step of the definition and you know a little more. Apply it again and you know more again. The knowledge only grows, so the steps settle down to a limit.

The theorem says the limit is a solution, and that it is the smallest solution: it contains only what the definition forces and nothing else. This needs one condition. The function must not jump at the limit. Whatever it does to the limit must be the limit of what it does to the steps. When the set of possible values is finite, the condition always holds, and the steps stop after a finite number of rounds.

## Proof

**Part 1.** *Continuous implies monotone.* Let $x \sqsubseteq y$. The sequence $x, y, y, y, \ldots$ is a chain with least upper bound $y$. Continuity gives $f(y) = f(x) \sqcup f(y) \sqcup f(y) \sqcup \cdots$, the least upper bound of $f(x), f(y), f(y), \ldots$. So $f(y)$ is above $f(x)$. *The iterates form a chain.* $\bot \sqsubseteq f(\bot)$ because $\bot$ is least. If $f^n(\bot) \sqsubseteq f^{n+1}(\bot)$, monotonicity gives $f^{n+1}(\bot) \sqsubseteq f^{n+2}(\bot)$. By induction the sequence is a chain, and since $D$ is a cpo, $\mu f$ exists. $\square$

**Part 2.** By continuity, applied to the chain of part 1,

$$f(\mu f) = f\Big(\bigsqcup_{n \ge 0} f^n(\bot)\Big) = \bigsqcup_{n \ge 0} f^{n+1}(\bot) = \bigsqcup_{n \ge 1} f^n(\bot).$$

The last chain is the first one without its first element $\bot$. Adding $\bot$ to a set does not change its upper bounds, because every element is above $\bot$. So the two chains have the same least upper bound, and $f(\mu f) = \mu f$. $\square$

**Part 3.** Let $f(x) \sqsubseteq x$. We show $f^n(\bot) \sqsubseteq x$ for every $n$ by induction. For $n = 0$, $\bot \sqsubseteq x$. If $f^n(\bot) \sqsubseteq x$, monotonicity gives $f^{n+1}(\bot) \sqsubseteq f(x) \sqsubseteq x$. So $x$ is an upper bound of the chain, and $\mu f \sqsubseteq x$ because $\mu f$ is the least upper bound. Every fixed point is a pre-fixed point, and $\mu f$ is itself a fixed point by part 2, so it is the least fixed point and the least pre-fixed point. $\blacksquare$

**The dual.** Apply the theorem to $D$ with the order reversed. Its least element is $\top$, its chains are the decreasing chains of $D$, and their least upper bounds are the greatest lower bounds in $D$.

**A worked example.** Take the recursive definition `fact(n) = if n == 0 then 1 else n * fact(n - 1)` on the natural numbers. Let $D$ be the set of partial functions from $\mathbb{N}$ to $\mathbb{N}$, ordered by inclusion of their graphs, so $g \sqsubseteq g'$ when $g'$ agrees with $g$ wherever $g$ is defined. The least element is the empty function. A chain of partial functions agrees wherever two of them are defined, so the union of their graphs is a partial function, and it is the least upper bound. So $D$ is a cpo. The definition gives the function

$$\Phi(g)(n) = \begin{cases} 1 & n = 0, \\ n \cdot g(n - 1) & n > 0 \text{ and } g(n - 1) \text{ defined}, \\ \text{undefined} & \text{otherwise.} \end{cases}$$

$\Phi(g)(n)$ reads only one value of $g$, so $\Phi$ is continuous: that value is already in some element of a chain. The iterates are $\Phi^0(\bot)$, defined nowhere, $\Phi^1(\bot) = \{0 \mapsto 1\}$, $\Phi^2(\bot) = \{0 \mapsto 1, 1 \mapsto 1\}$ and $\Phi^3(\bot) = \{0 \mapsto 1, 1 \mapsto 1, 2 \mapsto 2\}$. By induction, $\Phi^k(\bot)$ is the factorial function restricted to $\{0, \ldots, k - 1\}$. Their union is the factorial function on all of $\mathbb{N}$, which is $\mu \Phi$. Each iterate is what a program can compute with at most $k - 1$ nested recursive calls.

## Consequences

- **Finite height makes every monotone function continuous.** If every chain in $D$ is eventually constant, its least upper bound is its last value, and a monotone $f$ maps it to the last value of the image chain. So the iteration stops after at most $h$ steps on a lattice of height $h$. This is the case of the [fixed point](/fixed-point/) page and of the classic dataflow problems. On a CFG with $n$ blocks, the product lattice has height $n h$, which bounds the number of rounds of the [maximal fixed-point solution](/maximal-fixed-point-solution/).
- **Dataflow analysis.** In the dual form, the [maximal fixed-point solution](/maximal-fixed-point-solution/) is $\bigsqcap_n F^n(\top)$, and the [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/) describes each iterate $F^n(\top)$ exactly. Any fair order of updates, such as the [worklist dataflow algorithm](/worklist-dataflow-algorithm/), reaches the same fixed point, because every value it computes stays above the greatest fixed point and it stops only at a fixed point.
- **Abstract interpretation.** An abstract interpreter computes the least fixed point of an abstract transformer. On a lattice with infinite chains, such as the [interval domain](/interval-domain/), the iteration from $\bot$ may not stop, and a [widening operator](/widening-operator/) jumps ahead to a pre-fixed point. By part 3, any pre-fixed point is above the least fixed point, so the result is safe.
- **Recursion and loops.** In denotational semantics, the meaning of a recursive function or a `while` loop is the least fixed point of a continuous function on partial functions, as in the factorial example. Recursion in the [lambda calculus](/lambda-calculus/) gets its meaning the same way.
- **Datalog.** The least model of a [Datalog](/datalog/) program is the least fixed point of its immediate-consequence function on sets of facts, which keeps unions of chains. [Semi-naive evaluation](/semi-naive-evaluation/) computes the Kleene iterates with less repeated work.
- **Process networks.** The output of a [Kahn process network](/kahn-process-network/) is the least fixed point of the continuous function that the processes define on the histories of the channels.
- **Proof by fixed-point induction.** Part 3 gives a proof rule: to show $\mu f \sqsubseteq x$, show $f(x) \sqsubseteq x$. Dataflow and abstract interpretation use it to check that a candidate result is safe without running the solver.

## Tightness

**Continuity is needed for the limit at $\omega$.** Let $D = \{0, 1, 2, \ldots\} \cup \{\omega, \omega + 1\}$ with the usual order, so $\omega$ is above every number and $\omega + 1$ is above $\omega$. Every chain has a least upper bound: an eventually constant chain has its last value, and a chain that grows without bound in $\mathbb{N}$ has $\omega$. Let $f(k) = k + 1$, $f(\omega) = \omega + 1$ and $f(\omega + 1) = \omega + 1$. Then $f$ is monotone, and the iterates are $0, 1, 2, \ldots$ with least upper bound $\omega$. But $f(\omega) = \omega + 1 \ne \omega$, so the limit is not a fixed point. The least fixed point is $\omega + 1$. Here $f$ is not continuous: $f(\bigsqcup_k k) = \omega + 1$ but $\bigsqcup_k f(k) = \omega$. For monotone functions in general, the iteration must go on through the ordinals; Cousot and Cousot (1979) gave this construction.

**A least element is needed.** Let $D$ be the integers $\le 0$ with the usual order. Every chain is bounded by 0 and has a least upper bound, but there is no least element. The identity function is continuous, every element is a fixed point, and there is no least fixed point.

**Completeness is needed.** Let $D = \mathbb{N}$ with $\bot = 0$, and $f(k) = k + 1$. The function keeps every least upper bound that exists, but the chain $0, 1, 2, \ldots$ has none, and $f$ has no fixed point at all.

**The iteration need not stop.** Let $D = [0, 1]$, the real numbers between 0 and 1, and $f(x) = (x + 1) / 2$. $D$ is a cpo, $f$ is continuous, and the iterates $0, 1/2, 3/4, \ldots, 1 - 2^{-n}$ never reach the least fixed point 1. They reach it only at the limit. The bound of $h$ steps needs finite height.

**Knaster-Tarski is a different trade.** The [Knaster-Tarski theorem](/knaster-tarski-theorem/) needs only monotonicity, but it needs a complete lattice and it gives the least fixed point as the meet of all pre-fixed points, a formula that does not suggest a computation. The Kleene theorem asks for more of the function and less of the order, and it gives a computation in $\omega$ steps.

## History

The theorem is named after Kleene because of his first recursion theorem (1952), which says that a recursive definition of a partial function has a least solution, the union of finite approximations. Tarski (1955) proved the existence of fixed points of monotone functions on complete lattices. In the 1970s, Scott made continuous functions on complete partial orders the basis of denotational semantics, and the iteration from $\bot$ became a standard tool, both there and in the dataflow analysis of Kildall. Lassez, Nguyen and Sonenberg (1982) wrote a short history of these fixed-point theorems and of how they came to carry their usual names. Cousot and Cousot (1979) extended the iteration to monotone functions with ordinal steps.

## References
