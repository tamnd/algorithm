---
tag: 806R02
kind: technique
slug: reduced-product
name: Reduced product
aliases:
- reduced product of abstract domains
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: Combines two abstract domains into a product where each component is refined by the facts of the other, as precise as both.
prereqs: [abstract-domain, galois-connection]
see_also: [interval-domain, octagon-domain, polyhedra-domain, sparse-conditional-constant-propagation, nelson-oppen, widening-operator, narrowing-operator, constant-propagation-problem]
sources:
  - paper: doi:10.1145/567752.567778
    title: "Patrick Cousot and Radhia Cousot, Systematic design of program analysis frameworks, POPL 1979, pages 269 to 282"
    locator: Section 10, the sum, product and power of analysis frameworks, with the reduced product as the product in which pairs with the same meaning are identified
  - paper: doi:10.1007/978-3-642-19805-2_31
    title: "Patrick Cousot, Radhia Cousot and Laurent Mauborgne, The reduced product of abstract domains and the combination of decision procedures, FoSSaCS 2011, LNCS 6604, pages 456 to 472"
    locator: the reduction as a fixed point of local reductions between pairs of domains, its approximation by a bounded number of rounds, and the Nelson-Oppen procedure seen as a reduced product
  - book: isbn:9780262043410
    title: Xavier Rival and Kwangkeun Yi, Introduction to Static Analysis, An Abstract Interpretation Perspective, MIT Press, 2020
    locator: Chapter 3 (the combination of abstract domains by products and the reduction between them)
---

A reduced product runs two [abstract domains](/abstract-domain/) side by side and lets each one sharpen the other. A state is a pair $(a_1, a_2)$, and it means the states that both components allow. The plain product of two domains already has this meaning, but its components never talk to each other, so a fact that one domain knows cannot help the other. A *reduction* operator $\rho$ moves such facts across: it replaces $(a_1, a_2)$ by a pair $(b_1, b_2)$ with the same meaning in which each component is as small as the other allows. The analyzer applies $\rho$ after transfer functions and joins. Cousot and Cousot defined the reduced product in 1979. It is the standard way to build a strong analyzer from small domains, each with its own data structure.

## In plain words

Two people look at the same loop. One only tracks the range of `x`, and says "`x` is between 0 and 99". The other only tracks whether `x` is even, and says "`x` is even". Each statement alone is true. Put together, they say more: `x` is at most 98, because 99 is odd. A product of the two analyses keeps both statements but never draws this conclusion. A reduced product makes the two talk after every step, so the range becomes $[0, 98]$, and the next step starts from the better range. Over a whole loop the small gains add up.

## When it applies

- Two or more domains describe the same states, and each loses facts that another keeps: ranges and parity, ranges and relations, constants and reachability.
- The meaning is an intersection: $\gamma(a_1, a_2) = \gamma_1(a_1) \cap \gamma_2(a_2)$. So any pair can be shrunk without changing its meaning.
- There is a cheap way to move a fact from one domain to the other. The best one moves everything that the meaning allows, but a partial one is still sound.
- Both domains have their own transfer functions, joins and widenings, and these are kept unchanged.

## The template

Let $D_1$ and $D_2$ be abstract domains with meanings $\gamma_1$ and $\gamma_2$. A *local reduction* $\rho_{12}(a_1, a_2)$ returns some $b_1 \sqsubseteq_1 a_1$ with $\gamma_1(b_1) \cap \gamma_2(a_2) = \gamma_1(a_1) \cap \gamma_2(a_2)$: it tightens $a_1$ with what $a_2$ says. $\rho_{21}$ is the same in the other direction. $K$ bounds the number of rounds.

```pseudo id=main
REDUCE(a1, a2)
L1  for round ← 1 to K do
L2      b1 ← ρ12(a1, a2)                  ▷ tighten a1 with the facts of a2
L3      b2 ← ρ21(b1, a2)                  ▷ tighten a2 with the facts of b1
L4      if b1 = ⊥1 or b2 = ⊥2 then return (⊥1, ⊥2)
L5      if (b1, b2) = (a1, a2) then return (a1, a2)
L6      (a1, a2) ← (b1, b2)
L7  return (a1, a2)

TRANSFER(f, (a1, a2))
L8  return REDUCE(f1♯(a1), f2♯(a2))

JOIN((a1, a2), (c1, c2))
L9  return REDUCE(a1 ⊔1 c1, a2 ⊔2 c2)

WIDEN((a1, a2), (c1, c2))
L10 return (a1 ∇1 c1, a2 ∇2 c2)            ▷ no reduction of the result
```

The order, the meet and the test for inclusion work component by component. The holes are the local reductions, the bound $K$, and the choice of where to call REDUCE.

**Why it is sound.** Every line of REDUCE keeps the meaning: $\gamma(b_1, a_2) = \gamma(a_1, a_2)$ by the definition of $\rho_{12}$, and the same for $\rho_{21}$. A pair with $\bot$ in one component means the empty set, so line L4 is exact. So REDUCE can be called anywhere, as often as the analyzer likes, or stopped after any round, and the [abstract domain](/abstract-domain/) soundness argument for each $f_i^\sharp$ carries over to the pair.

**The best reduction.** If both domains have [Galois connections](/galois-connection/) $\alpha_1, \gamma_1$ and $\alpha_2, \gamma_2$ with the concrete sets, the best reduction is

$$ \rho^*(a_1, a_2) = \bigl(\alpha_1(S), \alpha_2(S)\bigr), \qquad S = \gamma_1(a_1) \cap \gamma_2(a_2). $$

It gives the least pair with the meaning $S$. The pairs that it leaves fixed form the *reduced product* in the strict sense: the product with all pairs of the same meaning identified, with the Galois connection $\alpha(S) = (\alpha_1(S), \alpha_2(S))$. Since $\alpha_1$ and $\alpha_2$ preserve joins, the join of two pairs that $\rho^*$ leaves fixed is again fixed, so line L9 matters only when its inputs are not fully reduced, for example after a capped REDUCE or when a domain has no best abstraction. The meet, and so every guard, does need the reduction. Computing $\rho^*$ directly is often as hard as the analysis itself. Cousot, Cousot and Mauborgne (2011) show that iterating the local reductions, as in lines L1 to L6, converges to it in many cases, and that stopping after a few rounds is a sound approximation.

**Why the bound $K$.** The rounds can go on forever. Let $D_1$ be intervals and let $D_2$ be a relational domain that holds $x < y$ and $y < x$, a pair that means the empty set. From $x \ge 0$ and $y \ge 0$, one round gives $y \ge 1$, then $x \ge 2$, then $y \ge 3$, and so on: each round is a strict step, and no round reaches $\bot$. The cap of line L1 makes REDUCE stop, and the result is still sound.

## Classic examples

**Parity and intervals.** The parity domain has $\bot$, *even*, *odd* and $\top$; the [interval domain](/interval-domain/) has the ranges $[l, u]$. The best reduction moves an end to the right parity: if the parity is *even* and $l$ is odd, set $l \leftarrow l + 1$; if $u$ is odd, set $u \leftarrow u - 1$; the same for *odd*. If then $l > u$, the pair is $\bot$. If $l = u$, the parity becomes the parity of $l$. One round is enough, since the second rule cannot undo the first. Take this program.

```
entry:
  x = 0
  jump head
head:
  t = x < 100
  br t body exit
body:
  x = x + 2
  jump head
exit:
  ret x
```

The analysis widens at `head` and then runs one narrowing step, with and without REDUCE after each transfer function and join.

| point | product | reduced product |
|---|---|---|
| `head`, after widening | even, $[0, +\infty]$ | even, $[0, +\infty]$ |
| `body`, after the guard $x \le 99$ | even, $[0, 99]$ | even, $[0, 98]$ |
| `body`, after `x = x + 2` | even, $[2, 101]$ | even, $[2, 100]$ |
| `head`, after narrowing | even, $[0, 101]$ | even, $[0, 100]$ |
| `exit`, after the guard $x \ge 100$ | even, $[100, 101]$ | even, $[100, 100]$ |

Both rows of `exit` have the meaning $\{100\}$, but only the reduced product says so in its interval part. A later check that reads the interval only, such as a bound check `x <= 100` for an array of 101 cells, is proved by the reduced product and not by the plain one. Granger (1989) used the same reduction between intervals and congruences $x \equiv c \pmod m$, which generalize parity.

**Constants and reachability.** [Sparse conditional constant propagation](/sparse-conditional-constant-propagation/) runs [constant propagation](/constant-propagation-problem/) together with an analysis of which edges can be taken. A branch on a known constant makes one edge dead, and a dead edge adds nothing to the join at its target, so more names stay constant. Run one after the other, the two analyses miss this in loops. Run together, they act as a reduced product of the constant domain with a domain of reachable edges.

**Octagon closure.** The strong closure of the [octagon domain](/octagon-domain/) is a reduction inside one domain: each constraint is tightened with the facts of the others, by shortest paths and one extra step. The rule that the octagon widening must not close its left argument is the same rule as line L10.

**Decision procedures.** The [Nelson-Oppen](/nelson-oppen/) method decides formulas in a combination of logical theories by passing equalities between the decision procedures until none is new. Cousot, Cousot and Mauborgne (2011) show that this is an iterated reduction between the theories, seen as abstract domains.

**Intervals and polyhedra in practice.** Analyzers that use [polyhedra](/polyhedra-domain/) on small groups of names keep intervals on all names, and move bounds both ways between the two.

## Variations

- **Partial reductions.** Move only some facts, for example only bounds that are cheap to compute, and accept a less precise result.
- **Reduce once or to a fixed point.** One round is enough for parity and intervals. For other pairs the rounds help, but each costs time; a small $K$ is common.
- **Reduce lazily.** Call REDUCE only before a transfer function that would profit, such as a guard or a division, instead of after every step.
- **More than two domains.** With $n$ domains, run the local reductions between every pair in turn, or between each domain and a shared store of facts, such as the equalities of Nelson-Oppen.
- **The plain product.** With no reduction at all, the product is still sound, and it is exactly as precise as running the two analyses on their own.
- **Granger's product.** Granger (1992) refined the reduction inside the transfer functions with local decreasing iterations, so that each test and assignment gives a more precise pair.

## Pitfalls

- **No reduction.** Writing line L8 as $(f_1^\sharp(a_1), f_2^\sharp(a_2))$ gives the plain product, which is only as precise as the two separate analyses. The table above shows the loss. Line L8 must reduce.
- **Reducing after the widening.** Writing line L10 as REDUCE$(a_1 \nabla_1 c_1, a_2 \nabla_2 c_2)$ can undo the widening: a bound that $\nabla_1$ has just dropped to $+\infty$ can come back from $D_2$, and the chain of iterates may then never stop. The same thing happens with the closure of octagons. Line L10 must return the widened pair as it is. The right argument may be reduced before the widening.
- **An unbounded loop of reductions.** Writing line L1 as "repeat until no change" can run forever, as the example with $x < y$ and $y < x$ shows. Line L1 must cap the rounds.
- **Expecting more precision than both.** Widening is not monotone, so a reduced analysis with widening is not always at least as precise as each analysis alone at every point. Without widening, on monotone transfer functions, it is.

## Exercises

1. In the product of the sign domain ($\bot$, *neg*, *zero*, *pos*, $\top$) with intervals, compute the best reduction of (*pos*, $[-3, 5]$), (*zero*, $[2, 4]$) and ($\top$, $[0, 0]$).
2. Prove that the reduction of parity and intervals given above is the best reduction $\rho^*$, and that one round of it is enough.
3. For the pair $x < y$ and $y < x$ with intervals, show that no finite number of rounds of lines L2 and L3 reaches $\bot$. Then give a reduction for this pair that does.
4. Replace `x = x + 2` by `x = x + 3` in the program above, and parity by the congruences modulo 3. Run the reduced product and find the value of `x` at `exit`.
5. Show that, with monotone transfer functions and no widening, every iterate of the reduced product is below the matching iterate of the plain product.

## References
