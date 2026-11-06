---
tag: N6FNJ0
kind: technique
slug: dependency-pairs
name: Dependency pairs
aliases:
- dependency pair framework
- DP method
area: automata-and-parsing/term-rewriting
level: research
summary: A modular framework that proves termination by ordering pairs of defined symbols.
prereqs: [termination, well-founded-reduction-ordering, polynomial-interpretation, strongly-connected-components]
see_also: [matrix-interpretation, recursive-path-ordering, lexicographic-path-ordering, size-change-termination, termination-proof, innermost-reduction, undecidability-of-termination, tarjan-scc]
sources:
  - paper: doi:10.1016/S0304-3975(99)00207-8
    title: Thomas Arts and Jürgen Giesl, Termination of term rewriting using dependency pairs, Theoretical Computer Science 236(1-2) (2000)
    locator: pp. 133 to 178 (dependency pairs, chains, the chain criterion for termination and innermost termination, the estimated dependency graph, argument filterings)
  - paper: doi:10.1007/978-3-540-32275-7_21
    title: Jürgen Giesl, René Thiemann and Peter Schneider-Kamp, The dependency pair framework, combining techniques for automated termination proofs, Logic for Programming, Artificial Intelligence, and Reasoning (LPAR 2004), Lecture Notes in Computer Science 3452
    locator: pp. 301 to 331 (DP problems, processors and their soundness)
  - paper: doi:10.1016/j.ic.2004.10.004
    title: Nao Hirokawa and Aart Middeldorp, Automating the dependency pair method, Information and Computation 199(1-2) (2005)
    locator: pp. 172 to 199 (the subterm criterion, usable rules for full termination, and the computation of the graph)
  - paper: doi:10.1007/s10817-006-9057-7
    title: Jürgen Giesl, René Thiemann, Peter Schneider-Kamp and Stephan Falke, Mechanizing and improving dependency pairs, Journal of Automated Reasoning 37(3) (2006)
    locator: pp. 155 to 203 (usable rules with respect to an argument filtering, and the search for reduction pairs)
---

The **dependency pair** method proves that a [term rewriting system](/term-rewriting-system/) terminates by looking only at the recursive calls in its rules. For each rule $l \to r$ and each call $f(\ldots)$ in $r$ of a function that the rules define, it builds a pair $l^\sharp \to f^\sharp(\ldots)$, where $^\sharp$ marks the root with a new symbol. The system terminates if and only if there is no infinite **chain** of such pairs, connected by rewriting of the arguments. This changes the task: the pairs need to decrease only in a weak order, their arguments need not be compared under the symbols that surround the calls, and the pairs split into independent groups along the cycles of a graph. Arts and Giesl introduced the method in 2000. As the **dependency pair framework**, a set of rules that transform and split proof problems, it is the core of most automatic termination provers.

## In plain words

A program runs forever only if some function calls itself, directly or through other functions, forever. So look only at the calls. For each rule, write down the pairs "this call leads to that call" and ignore everything else on the right side.

Draw these pairs as a graph: a pair can follow another if the result of the first call can turn into the start of the second. An endless run must go around a cycle of this graph forever, so it is enough to check each cycle on its own.

For each cycle, find a measure that never grows on the rules and on the calls of the cycle, and drops on at least one call. That call cannot be used forever, so remove it and look at the rest. When nothing is left, the program always stops.

## When it applies

- The aim is a proof of [termination](/termination/), or of innermost termination, of a finite system. The method is complete in principle (a system terminates if and only if no infinite chain exists), but each proof step needs an order or a criterion, and termination is undecidable, so the search may fail.
- The system is not simply terminating. A rule such as $quot(s(x), s(y)) \to s(quot(minus(x, y), s(y)))$ has an instance whose left side embeds in its right side, so no simplification ordering (no [recursive path ordering](/recursive-path-ordering/), [lexicographic path ordering](/lexicographic-path-ordering/), [Knuth-Bendix ordering](/knuth-bendix-ordering/) or polynomial interpretation) proves it. Dependency pairs with a weakly monotone order do.
- The left side of each rule is not a variable, and each variable of a right side occurs in its left side. Otherwise the system does not terminate, and the definitions below assume these conditions.

## The template

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, rules $l \to r$, positions as sequences of positive integers, substitutions $\sigma$, $\to_R^*$ for the reflexive transitive closure, and $\rhd$ for the proper subterm relation.

**Definitions.** The **defined symbols** $D$ are the root symbols of the left sides; the other symbols are **constructors**. For each $f \in D$ add a new **tuple symbol** $f^\sharp$ of the same arity, and for $t = f(t_1, \ldots, t_n)$ with $f \in D$ write $t^\sharp = f^\sharp(t_1, \ldots, t_n)$. The **dependency pairs** of $R$ are

$$DP(R) = \{\, l^\sharp \to u^\sharp \;:\; l \to r \in R,\ u \text{ a subterm of } r \text{ with a defined root} \,\}.$$

A **chain** is a finite or infinite sequence of pairs $s_1 \to t_1, s_2 \to t_2, \ldots$ from a set $P$, with their variables renamed apart, and a substitution $\sigma$ such that $t_i\sigma \to_R^* s_{i+1}\sigma$ for all $i$. It is **minimal** if every $t_i\sigma$ is terminating with respect to $\to_R$. Since tuple symbols occur in no rule, the steps of $t_i\sigma \to_R^* s_{i+1}\sigma$ are all below the root.

**Theorem (Arts and Giesl).** $R$ terminates if and only if there is no infinite chain of pairs from $DP(R)$. Moreover, if $R$ does not terminate, there is an infinite minimal chain.

*Proof.* Suppose $R$ does not terminate. Call a term **minimal** if it does not terminate but all its proper subterms do. Some non-terminating term exists, and among its subterms a smallest non-terminating one is minimal. Let $u_1$ be minimal. In an infinite reduction from $u_1$, the steps below the root take place in its arguments, which terminate, so a root step must occur: $u_1 \to_R^* l\sigma \to r\sigma$ for a rule $l \to r$, where the steps before the root step are below the root. The root of $u_1$ is then the root of $l$, a defined symbol. The arguments of $l\sigma$ are reducts of the arguments of $u_1$, so they terminate, and so does $x\sigma$ for each variable $x$ of $l$, as a subterm of an argument (here we use that $l$ is not a variable). Some subterm of $r\sigma$ is minimal, because $r\sigma$ does not terminate. It is not inside some $x\sigma$, so it is $u\sigma$ for a non-variable subterm $u$ of $r$. Its root is defined: a term with a constructor root and terminating arguments terminates, because no step can occur at its root. So $l^\sharp \to u^\sharp$ is a dependency pair, $u_1^\sharp \to_R^* l^\sharp\sigma$, and $u\sigma$ is minimal. Repeating from $u_2 = u\sigma$ gives an infinite chain, after renaming the variables of each pair apart and joining the substitutions into one, and each $t_i\sigma$ is minimal, so the chain is minimal.

Conversely, suppose $s_1 \to t_1, s_2 \to t_2, \ldots$ is an infinite chain with $\sigma$. Each pair $s_i \to t_i$ comes from a rule $l \to r$ with $s_i = l^\sharp$ and $t_i = u^\sharp$ for a subterm $u$ of $r$ at some position $p$. Erase the marks: write $\bar s_i, \bar t_i$. Then $\bar s_i\sigma \to_R r\sigma = r\sigma[\bar t_i\sigma]_p$, and $\bar t_i\sigma \to_R^* \bar s_{i+1}\sigma$. So $\bar s_1\sigma$ has an infinite reduction, with at least one step for each pair, placed inside larger and larger contexts. $\blacksquare$

**Processors.** A **DP problem** is a set $P$ of pairs, and it is **finite** if there is no infinite minimal chain of pairs from $P$. The method starts from $DP(R)$ and replaces a problem by smaller ones until none is left. Three processors are standard.

- **The dependency graph.** Its nodes are the pairs, with an edge from $s \to t$ to $s' \to t'$ if $t\sigma \to_R^* s'\sigma$ for some $\sigma$, after renaming apart. An infinite chain is an infinite path, so from some point on it stays in one strongly connected component. So $P$ is finite if each nontrivial [strongly connected component](/strongly-connected-components/) is. The graph is undecidable, so tools compute a superset of its edges: replace in $t$ each subterm with a defined root, and each variable, by a new variable, and test whether the result [unifies](/most-general-unifier/) with $s'$. This is sound, because rewriting below the root cannot change the constructor part of $t$ above the defined subterms.
- **Reduction pairs.** A **reduction pair** $(\succsim, \succ)$ is a quasi-order $\succsim$ that is closed under contexts and substitutions, with a well-founded order $\succ$ that is closed under substitutions, and with $\succsim \circ \succ \subseteq \succ$. If $l \succsim r$ for every rule of $R$, and $s \succsim t$ or $s \succ t$ for every pair of $P$, remove the pairs with $s \succ t$. Proof: in an infinite chain, $s_i\sigma \succsim t_i\sigma$ or $s_i\sigma \succ t_i\sigma$, and $t_i\sigma \succsim s_{i+1}\sigma$ because $R \subseteq \succsim$. If strict pairs occurred infinitely often, compatibility would give an infinite descending chain of $\succ$. So a tail of the chain uses only the other pairs. A weakly monotone [polynomial interpretation](/polynomial-interpretation/) or [matrix interpretation](/matrix-interpretation/) gives a reduction pair: coefficients may be zero, so an argument can be ignored.
- **The subterm criterion** (Hirokawa and Middeldorp). Choose for each tuple symbol $f^\sharp$ an argument $\pi(f^\sharp) \in \{1, \ldots, n\}$, and write $\pi(f^\sharp(t_1, \ldots, t_n)) = t_{\pi(f^\sharp)}$. If $\pi(s) \unrhd \pi(t)$ for every pair, remove the pairs with $\pi(s) \rhd \pi(t)$. Proof: in a minimal chain, $\pi(t_i)\sigma \to_R^* \pi(s_{i+1})\sigma$, because the steps are below the root, so the chain gives a sequence of $\to_R$ and $\rhd$ steps from the terminating term $\pi(s_1)\sigma$. A strict pair is a $\rhd$ step, and $\rhd$ steps can be moved behind $\to_R$ steps, so infinitely many of them would give an infinite reduction of a subterm of $\pi(s_1)\sigma$. No order on $R$ is needed.

```pseudo id=main
DP-PROVE(R)
L1  P ← DP(R)
L2  Q ← the nontrivial strongly connected components of the estimated graph of P
L3  while Q is not empty do
L4      C ← remove a component from Q
L5      S ← the pairs of C removed by the subterm criterion, if some projection works
L6      if S = ∅ then S ← the pairs strictly oriented by a reduction pair for (C, R)       ▷ hole: the search
L7      if S = ∅ then return "unknown"
L8      add to Q the nontrivial strongly connected components of the graph of C \ S
L9  return "R terminates"
```

Each processor is sound, so when the queue is empty, $DP(R)$ has no infinite minimal chain, and $R$ terminates by the theorem. The hole is line L6: tools choose the shape of the interpretations or path orders, and solve the constraints with SAT or SMT solvers.

## Classic examples

The pairs, the graphs, the components and the orders below were computed by a program that generates the pairs, estimates the graph by unification, finds the components, and searches projections and linear interpretations with coefficients from 0 to 2.

**Division (Arts and Giesl).** The rules

$$minus(x, 0) \to x,\quad minus(s(x), s(y)) \to minus(x, y),\quad quot(0, s(y)) \to 0,\quad quot(s(x), s(y)) \to s(quot(minus(x, y), s(y)))$$

are not simply terminating. With $x := x$ and $y := s(x)$, the left side $quot(s(x), s(s(x)))$ embeds in the right side $s(quot(minus(x, s(x)), s(s(x))))$, because $s(x)$ is a subterm of $minus(x, s(x))$. The dependency pairs are

1. $MINUS^\sharp(s(x), s(y)) \to MINUS^\sharp(x, y)$,
2. $QUOT^\sharp(s(x), s(y)) \to MINUS^\sharp(x, y)$,
3. $QUOT^\sharp(s(x), s(y)) \to QUOT^\sharp(minus(x, y), s(y))$.

The graph has the edges $1 \to 1$, $2 \to 1$, $3 \to 2$ and $3 \to 3$, and the nontrivial components $\{1\}$ and $\{3\}$. Pair 2 lies on no cycle and needs no proof. For $\{1\}$ the subterm criterion with $\pi(MINUS^\sharp) = 1$ works: $s(x) \rhd x$. For $\{3\}$ the projection to argument 1 fails, because $minus(x, y)$ is not a subterm of $s(x)$. Take the weakly monotone interpretation $[0] = 0$, $[s](x) = x + 1$, $[minus](x, y) = x$, $[quot](x, y) = x$, $[QUOT^\sharp](x, y) = x$. The rules give $x \ge x$, $x + 1 \ge x$, $0 \ge 0$ and $x + 1 \ge x + 1$, and the pair gives $x + 1 > x$. So the system terminates. The interpretation of $minus$ ignores its second argument; it is not strictly monotone, which is why it can orient the rules weakly while the strict decrease happens only on the pair.

**A rule with no simplification ordering.** For $f(f(x)) \to f(g(f(x)))$ with the constructor $g$, the pairs are $F^\sharp(f(x)) \to F^\sharp(g(f(x)))$ and $F^\sharp(f(x)) \to F^\sharp(x)$. The first has no outgoing edge, because $g(\ldots)$ never rewrites to $f(\ldots)$. The second forms a cycle, and the subterm criterion removes it: $f(x) \rhd x$. No order on the rule was needed.

**Checks.** On 600 random small systems over $f/1$, $g/1$, $h/2$ and constants, including the empty system and non-linear rules, the program never proved a system for which random reductions ran for 3000 steps, and it did not prove the non-terminating systems $f(x) \to f(x)$, $f(g(x)) \to g(f(g(x)))$ and $h(x, a) \to h(a, x)$.

## Variations

- **Innermost termination.** For innermost rewriting, chains require $\sigma$ to make each $s_i\sigma$ a normal form, and only the **usable rules**, the rules of the functions that can be called from the right sides of the pairs, need to be oriented. Innermost termination implies termination for some classes, such as non-overlapping systems, so this is often the easier proof.
- **Usable rules for full termination.** Hirokawa and Middeldorp, and Giesl and others, showed that the usable rules suffice for full termination too, if the order is also compatible with the rules $c(x, y) \to x$ and $c(x, y) \to y$ for a new symbol $c$.
- **Argument filterings.** A path order such as [LPO](/lexicographic-path-ordering/) becomes weakly monotone if some arguments of some symbols are deleted before the comparison. The search chooses the filtering and the precedence together.
- **Other processors.** The framework adds many: rewriting, narrowing and instantiation of pairs, reduction of the rules to the usable ones, [size-change](/size-change-termination/) arguments, and processors that prove non-termination by finding a loop.
- **Fewer pairs.** Dershowitz noted that a subterm $u$ of $r$ that is also a proper subterm of $l$ needs no pair.
- **Complexity.** Variants for runtime complexity, with weak dependency pairs or dependency tuples, bound the number of innermost steps from terms whose arguments are constructor terms.

## Pitfalls

- **Strict monotonicity is not needed, but closure under contexts of $\succsim$ is.** The weak order must still be closed under contexts, because $t_i\sigma \to_R^* s_{i+1}\sigma$ rewrites inside the arguments. Coefficient 0 is fine; a negative coefficient is not.
- **Marking all symbols.** Only the root of a pair side is marked. Marking inner defined symbols changes the chains and makes the method unsound.
- **Forgetting the rules.** Orienting only the pairs proves nothing: the condition $R \subseteq \succsim$, or the usable rules in its refined form, is what connects one pair to the next.
- **Using the subterm criterion on non-minimal chains.** Its proof needs that each $t_i\sigma$ terminates. Processors that are only sound for arbitrary chains combine freely with it, but a new processor must say which kind of chain it assumes.
- **An unsound graph.** Testing whether $t$ itself unifies with $s'$, without replacing the defined subterms, misses edges, because $t\sigma$ can rewrite before it meets $s'$.

## Exercises

1. Compute the dependency pairs and the estimated graph for the Ackermann function: $ack(0, y) \to s(y)$, $ack(s(x), 0) \to ack(x, s(0))$, $ack(s(x), s(y)) \to ack(x, ack(s(x), y))$. Prove termination with the subterm criterion alone, used twice with different projections.
2. Show that $\{f(a) \to f(b),\ b \to a\}$ does not terminate, and find the infinite chain that the theorem gives.
3. Prove that a term with a constructor root and terminating arguments terminates.
4. Give a system and a set of pairs where the projection to the first argument shows that each pair is weakly decreasing, but no pair is strictly decreasing, and explain why nothing can be removed.

## References
