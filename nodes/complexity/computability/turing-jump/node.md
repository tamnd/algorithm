---
tag: 3WWAD8
kind: concept
slug: turing-jump
name: Turing jump
aliases:
- jump operator
area: complexity/computability
level: advanced
summary: "The jump A' of a set A is the halting problem for oracle machines with oracle A. It is c.e. in A and strictly harder than A, and iterating it from the empty set gives 0', 0'' and higher degrees."
prereqs: [turing-degrees, halting-problem]
see_also: [turing-degrees, oracle-turing-machine, halting-problem, arithmetical-hierarchy, posts-theorem, post-problem, relativization, diagonalization-argument]
sources:
  - paper: doi:10.2307/1969708
    title: "Stephen C. Kleene and Emil L. Post, The upper semi-lattice of degrees of recursive unsolvability, Annals of Mathematics 59(3) (1954)"
    locator: "pp. 379 to 407 (the jump as an operation on degrees)"
  - paper: doi:10.2307/2964177
    title: "Richard M. Friedberg, A criterion for completeness of degrees of unsolvability, Journal of Symbolic Logic 22(2) (1957)"
    locator: "pp. 159 to 160 (every degree above 0' is a jump)"
  - title: "Joseph R. Shoenfield, On degrees of unsolvability, Annals of Mathematics (2) 69 (1959)"
    locator: "pp. 644 to 653 (the limit lemma)"
  - book: isbn:9783642319327
    title: "Robert I. Soare, Turing Computability, Theory and Applications, Springer, 2016"
    locator: "Chapter 3, Turing Reducibility, and Chapter 4, The Arithmetical Hierarchy"
---

The Turing jump of a set $A$ is the halting problem for [oracle machines](/oracle-turing-machine/) that use $A$ as their oracle. It is written $A'$. With an oracle for $A$, a machine can list $A'$ but cannot decide it, so $A'$ is strictly harder than $A$. This is the diagonal proof that the [halting problem](/halting-problem/) is undecidable, run with an oracle. The jump respects Turing equivalence, so it is an operation on [Turing degrees](/turing-degrees/): $\mathbf{a}' = \deg(A')$ for any $A \in \mathbf{a}$. Starting from the decidable sets, it gives $\mathbf{0}' = \deg(K)$, then $\mathbf{0}''$, $\mathbf{0}'''$, and so on. These iterates measure the levels of the [arithmetical hierarchy](/arithmetical-hierarchy/): by [Post's theorem](/posts-theorem/), the sets definable with $n + 1$ alternating number quantifiers in the $\Sigma$ form are exactly the sets c.e. in $\emptyset^{(n)}$. Kleene and Post (1954) made the jump an operation on degrees.

## In plain words

Give a program access to a magic box that answers some hard question. Programs of this new kind still cannot decide, in general, whether one of them will stop. That stopping question for programs with the box is the jump of the box. It is always strictly harder than the box itself.

Repeat the step and you get a ladder of harder and harder questions. The first rung is the ordinary halting problem. The second is about as hard as asking whether a program stops on every input.

## The idea

**Definition.** Fix a computable numbering $\Phi_0, \Phi_1, \ldots$ of the oracle programs (the encoding is fixed and computable). For a set $A \subseteq \mathbb{N}$,
$$A' = \{ e : \Phi_e^A(e)\!\downarrow \}.$$
For $A = \emptyset$ this is the diagonal halting set $K$ in the form $K = \{e : \varphi_e(e)\!\downarrow\}$, so $\emptyset' = K$ up to the choice of numbering. The set $A'_0 = \{ \langle e, x \rangle : \Phi_e^A(x)\!\downarrow \}$, the analog of HALT, is one-one equivalent to $A'$, so either can serve as the definition.

**The jump theorem.** For all sets $A$ and $B$:

1. $A'$ is c.e. in $A$: a universal oracle machine with oracle $A$ runs $\Phi_e^A(e)$ and accepts if it halts.
2. $A' \not\le_T A$, so $A <_T A'$.
3. A set $B$ is c.e. in $A$ if and only if $B \le_1 A'$ (by a one-one reduction). So $A'$ is complete for the sets c.e. in $A$.
4. $A \le_T B$ implies $A' \le_1 B'$, and so $A \equiv_T B$ implies $A' \equiv_1 B'$.

*Proof of 2.* Suppose $A' = \{x : \Phi_i^A(x) = 1\}$ for an oracle program $\Phi_i^A$ that is total. Let $\Phi_e^A$ be the oracle program that on input $x$ computes $\Phi_i^A(x)$ and runs forever if the value is $1$, and halts otherwise. Then $e \in A'$ if and only if $\Phi_e^A(e)\!\downarrow$, if and only if $\Phi_i^A(e) \ne 1$, if and only if $e \notin A'$. This [diagonal argument](/diagonalization-argument/) is the proof for $K$, with every machine given the oracle $A$.

*Proof of 3 and 4.* If $B = W_j^A$, the [s-m-n theorem](/s-m-n-theorem/) for oracle programs gives a total computable injective $f$ such that $\Phi_{f(x)}^A$ ignores its input and halts exactly when $x \in W_j^A$; then $x \in B$ if and only if $f(x) \in A'$. For 4, $A'$ is c.e. in $A$ and so c.e. in any $B$ with $A \le_T B$, and part 3 gives $A' \le_1 B'$.

**Iterates.** $A^{(0)} = A$ and $A^{(n+1)} = (A^{(n)})'$. The degrees $\mathbf{0}^{(n)} = \deg(\emptyset^{(n)})$ form a strictly increasing chain. The set $\emptyset^{(\omega)} = \{ \langle n, x \rangle : x \in \emptyset^{(n)} \}$ computes every $\emptyset^{(n)}$, and its degree is above all arithmetical sets.

**The jump is not one-to-one on degrees.** Part 4 makes the jump monotone, but $A <_T B$ does not imply $A' <_T B'$. A set $A$ is *low* if $A' \equiv_T \emptyset'$, the least possible jump; there are noncomputable c.e. low sets, so different degrees can have the same jump. A c.e. set is *high* if $A' \equiv_T \emptyset''$, the largest possible jump for a set below $\emptyset'$. The low and high sets give a coarse map of the degrees below $\mathbf{0}'$ in terms of their jumps.

**Jump inversion.** Friedberg (1957) proved that every degree $\mathbf{b} \ge \mathbf{0}'$ is a jump: there is an $\mathbf{a}$ with $\mathbf{a}' = \mathbf{a} \vee \mathbf{0}' = \mathbf{b}$. So the range of the jump is exactly the cone above $\mathbf{0}'$.

**The limit lemma.** Shoenfield (1959) proved: $A \le_T \emptyset'$ if and only if there is a total computable $g(x, s)$ with values $0$ and $1$ such that, for every $x$, $g(x, s)$ is constant for all large $s$, with limit $A(x)$. So the sets computable from the halting problem are the sets that an algorithm can guess, changing its mind finitely often for each input, with no way to know when the last change has happened. Putnam and Gold found the same notion independently in 1965, as trial-and-error predicates and as learning in the limit.

## Examples

**The jump of the empty set.** $\emptyset' = K$. With $A = \emptyset$, the jump theorem says that $K$ is c.e., is not decidable, and is one-one complete for the c.e. sets. These are the basic facts of the [halting problem](/halting-problem/).

**A stage approximation.** The set $K$ has the approximation $K_s = \{ e < s : \varphi_e(e) \text{ halts within } s \text{ steps} \}$, and $K(e) = \lim_s K_s(e)$, as in the limit lemma, where each guess changes at most once, from $0$ to $1$. The same happens with any c.e. set. For example, for the set of $n$ whose Collatz sequence ($n \mapsto n/2$ for even $n$, $n \mapsto 3n + 1$ for odd $n$) reaches $1$, the guess "$n$ has reached $1$ within $s$ steps" is $0$ for $n = 27$ until stage $s = 111$ and $1$ from then on, and for $n = 97$ it changes at stage $118$. Before the change, the stage approximation gives no hint of when, or whether, it will come. For a set that is computable from $\emptyset'$ but not c.e., the guesses may change more than once, but finitely often for each input.

**Second and third jumps.** $\emptyset'' \equiv_T \mathrm{TOT} = \{ e : \varphi_e \text{ is total} \}$, and also $\emptyset'' \equiv_T \mathrm{FIN} = \{ e : W_e \text{ is finite} \}$. A program that decides totality with an oracle would decide halting with an oracle for $K$. $\emptyset''' \equiv_T \mathrm{COF} = \{ e : W_e \text{ is cofinite} \}$. The [arithmetical hierarchy](/arithmetical-hierarchy/) page gives the quantifier forms and the reductions.

**The halting problem for machines with a halting oracle.** A machine with an oracle for $K$ can decide whether an ordinary machine halts. It cannot decide whether a machine with an oracle for $K$ halts, since that set is $K' = \emptyset''$.

## Where it is used

- **Measuring the arithmetical hierarchy.** By [Post's theorem](/posts-theorem/), the $\Sigma_{n+1}$ sets are the sets c.e. in $\emptyset^{(n)}$, and the $\Delta_{n+1}$ sets are the sets computable from $\emptyset^{(n)}$. The jump gives the complete set of each level.
- **Classifying problems.** Showing that a set is Turing equivalent to $\emptyset''$ or $\emptyset'''$ shows how many quantifiers its definition needs and that it is not easier. Totality of programs, equivalence of programs and finiteness of languages are classified in this way.
- **Constructions below $\mathbf{0}'$.** The finite-extension arguments of Kleene and Post use $\emptyset'$ as the oracle that answers the question at each step, and the limit lemma turns a $\emptyset'$-computable construction into a computable sequence of guesses. This is the setting of [Post's problem](/post-problem/) and of the priority method.
- **Learning in the limit.** A program that changes its guess finitely often is the model of inductive inference of Gold. The limit lemma says that this model, for single yes or no answers, reaches exactly the sets computable from $\emptyset'$.
- **Complexity theory.** The polynomial hierarchy is built in the same way, with $\mathrm{NP}^{\mathrm{NP}}$ in the role of the jump, although there is no proof that its levels are different. The undecidability of the jump relativizes, which is the point of [relativization](/relativization/).

## References
