---
tag: PVN188
kind: algorithm
slug: generalized-cofactor
name: Generalized cofactor
aliases:
- constrain operator
- restrict operator
- Coudert-Madre operators
area: logic-and-constraints/binary-decision-diagrams
level: advanced
summary: The BDD operators constrain and restrict of Coudert and Madre. Given f and a care set c, each returns a function that agrees with f wherever c is 1, and is often smaller than f.
model: word-ram
complexity:
  vars: {f: the number of nodes of the BDD of f, c: the number of nodes of the BDD of c}
  time: {worst: O(f·c) expected}
  space: {extra: O(f·c)}
properties: {deterministic: true, exact: true, online: false, recursive: true, in_place: false}
history:
  year: 1989
  people: [Olivier Coudert, Christian Berthet, Jean Christophe Madre]
  note: Coudert, Berthet and Madre introduced constrain for the image computation of sequential circuits in 1989; Coudert and Madre added restrict in 1990.
prereqs: [cofactor, shannon-expansion, reduced-ordered-bdd, bdd-apply]
see_also: [dont-care-minimization, cofactor, bdd-apply, ite-operator, boolean-function-composition, bdd-quantification, symbolic-reachability, computed-table]
sources:
  - paper: "Olivier Coudert, Christian Berthet and Jean Christophe Madre, Verification of synchronous sequential machines based on symbolic execution, Automatic Verification Methods for Finite State Systems, Lecture Notes in Computer Science 407, 1989"
    title: Coudert, Berthet and Madre, Verification of synchronous sequential machines based on symbolic execution
    locator: the constrain operator and its use for the image of a set of states
  - paper: "Olivier Coudert and Jean Christophe Madre, A unified framework for the formal verification of sequential circuits, ICCAD 1990"
    title: Coudert and Madre, A unified framework for the formal verification of sequential circuits
    locator: the restrict operator
  - paper: "Hervé J. Touati, Hamid Savoj, Bill Lin, Robert K. Brayton and Alberto Sangiovanni-Vincentelli, Implicit state enumeration of finite state machines using BDDs, ICCAD 1990"
    title: Touati, Savoj, Lin, Brayton and Sangiovanni-Vincentelli, Implicit state enumeration of finite state machines using BDDs
    locator: the properties of the generalized cofactor (the closest-point map and the image of a function vector)
  - paper: "Thomas R. Shiple, Ramin Hojati, Alberto L. Sangiovanni-Vincentelli and Robert K. Brayton, Heuristic minimization of BDDs using don't cares, Design Automation Conference 1994"
    title: Shiple, Hojati, Sangiovanni-Vincentelli and Brayton, Heuristic minimization of BDDs using don't cares
    locator: the comparison of constrain, restrict and related operators, and examples where they make the BDD larger
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (the generalized cofactor and its exercises)
---

A generalized cofactor simplifies a [BDD](/reduced-ordered-bdd/) with a care set. The input is a function $f$ and a nonzero function $c$, the care set: we only need the values of $f$ at the points $x$ with $c(x) = 1$. The output is a function $g$ with $g(x) = f(x)$ wherever $c(x) = 1$, and the values elsewhere are chosen so that $g$ is often smaller. Coudert, Berthet and Madre (1989) gave the operator *constrain*, written $f \downarrow c$, and Coudert and Madre (1990) gave *restrict*. When $c$ is a cube, both give the ordinary [cofactor](/cofactor/). Both run in one recursive pass over the two BDDs, but neither finds the smallest such $g$, and either result can be larger than $f$. The optimization problem itself, find the smallest $g$, is a different thing: it is the NP-hard problem of [don't-care minimization](/dont-care-minimization/).

## In plain words

Suppose that you only care about the answers of a function in some cases, and you do not care what it says in the other cases. Then you can replace the function by a simpler one that gives the same answers in the cases that you care about. Constrain and restrict do this on a BDD. They walk down the BDD of the function and the BDD of the cases together. When all the cases you care about have the same answer to a question, they do not ask that question any more: they follow the branch that has cases in it. This often removes nodes. But the method is greedy, and sometimes it gives a bigger diagram than the one you started with.

## The problem

**Input:** a store of reduced ordered BDDs with the order $x_1 < \cdots < x_n$, a node $f$, and a node $c \ne 0$.

**Output:** a node $g$ with $g(x) = f(x)$ for each $x$ with $c(x) = 1$.

The output is not unique. The two operators fix a specific choice, defined by the algorithm. Constrain has an exact description by a closest point (see Correctness). Restrict has the extra property that $g$ uses only variables that $f$ uses.

## The algorithm

For a variable $v$ at or above the top of a node $u$, the cofactors $u_0$ and $u_1$ are the low and the high child of $u$ if $u$ tests $v$, and both are $u$ otherwise. MK is the node constructor with the unique table. Both procedures need $c \ne 0$, and both memoize their results on the pair $(f, c)$ in a [computed table](/computed-table/).

```pseudo id=main
CONSTRAIN(f, c)
L1  if c = 1 or f is a sink then return f
L2  if f = c then return 1
L3  v ← the top variable of f and c; (f0, f1) and (c0, c1) ← the cofactors by v
L4  if c0 = 0 then return CONSTRAIN(f1, c1)
L5  if c1 = 0 then return CONSTRAIN(f0, c0)
L6  return MK(v, CONSTRAIN(f0, c0), CONSTRAIN(f1, c1))

RESTRICT(f, c)
L7  if c = 1 or f is a sink then return f; if f = c then return 1
L8  if the top variable of c is above the top variable of f then return RESTRICT(f, c0 ∨ c1), with the cofactors of c by its top variable
L9  otherwise do lines L3 to L6 with v = the top variable of f, and RESTRICT in place of CONSTRAIN
```

Lines L4 and L5 are the source of the gain. If the care set has no point with $v = 0$, the value of $f$ for $v = 0$ is not needed, so the result does not test $v$: it is the result for $v = 1$ on both sides. Line L2 uses the fact that $f = c$ is 1 at every point of the care set.

The two operators differ at a variable $v$ that $c$ tests above the top of $f$. Constrain keeps such a $v$ and may put it into the result (line L3 takes the top of both). Restrict removes it from the care set by the existential quantification $c_0 \vee c_1$ at line L8, so the result never tests a variable that $f$ does not test.

## Example

Take the order $x_1, x_2, x_3$, the function $f = x_3$ (3 nodes with the sinks), and the care set

$$c = (x_2 \oplus x_3) \vee (x_1 \wedge x_2 \wedge x_3),$$

with 7 nodes. Its cofactors by $x_1$ are $c|_{x_1=0} = x_2 \oplus x_3$ and $c|_{x_1=1} = x_2 \vee x_3$. The calls of constrain:

| call | line | top | care cofactors | result |
|---|---|---|---|---|
| $(x_3, c)$ | L6 | $x_1$ | $x_2 \oplus x_3$, $x_2 \vee x_3$ | MK$(x_1, \neg x_2, \neg x_2 \vee x_3)$ |
| $(x_3, x_2 \oplus x_3)$ | L6 | $x_2$ | $x_3$, $\neg x_3$ | MK$(x_2, 1, 0) = \neg x_2$ |
| $(x_3, x_3)$ | L2 | | | 1 |
| $(x_3, \neg x_3)$ | L5 | $x_3$ | $1$, $0$ | CONSTRAIN$(0, 1) = 0$ |
| $(x_3, x_2 \vee x_3)$ | L6 | $x_2$ | $x_3$, $1$ | MK$(x_2, 1, x_3) = \neg x_2 \vee x_3$ |

The result is $f \downarrow c = \neg x_2 \vee (x_1 \wedge x_3)$, with 6 nodes, twice the size of $f$. It agrees with $f$ on the five points of $c$: $(0,0,1)$, $(0,1,0)$, $(1,0,1)$, $(1,1,0)$ and $(1,1,1)$, written as $(x_1, x_2, x_3)$.

Restrict does better here. The top variable of $c$ is $x_1$, above $x_3$, so line L8 replaces $c$ by $(x_2 \oplus x_3) \vee x_2 \vee x_3 = x_2 \vee x_3$, and then by $1$. The result is $f$ itself.

Restrict can also grow. A check of all 65,280 pairs $(f, c)$ with $n = 3$ and $c \ne 0$ found no case where restrict gives more nodes than $f$, and 2,956 cases where constrain does. With $n = 4$, the tests contain a case where restrict turns 6 nodes into 7. These counts come from the implementation.

## Correctness

**Agreement.** Both operators return a $g$ with $g(x) = f(x)$ wherever $c(x) = 1$. The proof is by induction on the recursion. At line L1 the result is $f$. At line L2, $f = c$, so $f(x) = 1$ on the care set. At line L4 every care point has $v = 1$, so it is a care point of $c_1$, where the recursive result agrees with $f_1$, and $f_1$ agrees with $f$ when $v = 1$. Lines L5 and L6 are the same. At line L8, $f$ does not depend on $v$, and $c_0 \vee c_1$ is 1 at each point where $c$ is 1, so agreement on the larger set gives agreement on $c$.

**Closest point (constrain).** For each $x$, let $\pi_c(x)$ be the point $y$ with $c(y) = 1$ that minimizes

$$d(x, y) = \sum_{i=1}^{n} |x_i - y_i| \, 2^{n-i}.$$

Then $(f \downarrow c)(x) = f(\pi_c(x))$. The weight of $x_1$ is larger than all the other weights together, so $\pi_c$ picks $y$ greedily from the top: keep $y_i = x_i$ if some care point extends the choices so far, and flip it otherwise. That is what lines L4 to L6 do. Two consequences follow. Constrain commutes with every Boolean operation, for example $(f \wedge g) \downarrow c = (f \downarrow c) \wedge (g \downarrow c)$, since all of them are composed with the same map $\pi_c$. And for a vector $F = (f_1, \ldots, f_m)$, the range of $F \downarrow c$ is the image $F(\{x : c(x) = 1\})$, since $\pi_c$ maps onto the care set. This is the property that Coudert, Berthet and Madre used for image computation.

**Restrict uses only the variables of $f$.** Every node that restrict makes tests the top variable of the current $f$.

The full proofs are in [the proof file](proofs/correctness.md).

## Complexity

**Constrain.** The arguments of each call are a node reachable from $f$ and a node reachable from $c$, since line L3 moves to children. With the computed table, each pair does real work at most once, so constrain makes $O(|f| \cdot |c|)$ calls and takes $O(|f| \cdot |c|)$ expected time with hash tables. The result has at most $|f| \cdot |c|$ nodes.

**Restrict.** Line L8 makes new care sets $c_0 \vee c_1$ that are not nodes of $c$. Each such OR is an [APPLY](/bdd-apply/) call. A chain of them computes an existential quantification of $c$ over the variables above $f$, and its size has no polynomial bound in general (see [BDD quantification](/bdd-quantification/)). In practice restrict costs about as much as constrain.

**Space.** The computed tables and the result take $O(|f| \cdot |c|)$ space for constrain. The recursion depth is at most $n + 1$.

## Properties

- **Agreement on the care set**, for both operators.
- **Cube cofactor.** If $c$ is a cube (a conjunction of literals), $f \downarrow c$ and restrict both equal the ordinary cofactor $f|_c$.
- **Special cases.** $f \downarrow 1 = f$, $f \downarrow f = 1$ and $f \downarrow \neg f = 0$.
- **Constrain is a composition** $f \circ \pi_c$, so it commutes with all Boolean operations, and it keeps the image of a function vector.
- **Constrain can add variables.** The example above adds $x_1$ and $x_2$ to a function of $x_3$ alone.
- **Restrict keeps the support.** Its result tests only variables that $f$ tests.
- **No size guarantee.** Both operators can return a larger BDD than $f$. Neither finds the smallest function that agrees with $f$ on $c$; that problem is NP-hard ([don't-care minimization](/dont-care-minimization/)).

## Variants and improvements

- **Safe minimization.** Return $f$ instead of the result when the result is larger. Hong, Beerel, Burch and McMillan (1997) gave operators that never increase the size by design.
- **Sibling substitution and other heuristics.** Shiple, Hojati, Sangiovanni-Vincentelli and Brayton (1994) compared constrain, restrict and several related operators, all based on the same recursion with different rules for lines L4 to L6 and L8.
- **The ordinary cofactor** is the special case where $c$ is a cube.
- **Image computation by range.** To get the image of a state set $S$ under a function vector $\delta$, compute $\delta \downarrow S$ and then the range of the result, which needs no transition relation.

## When to use it

Use restrict to simplify a BDD before more operations when the values outside a known set are irrelevant, for example the next-state functions of a circuit outside the reachable states, or $f$ outside the states that a model checker is still exploring in [symbolic reachability](/symbolic-reachability/). Use constrain when its algebraic properties are needed, for example the range property for image computation. In both cases, compare the size of the result with the size of $f$ and keep the smaller one.

## Pitfalls

- **Empty care set.** Both operators need $c \ne 0$. With $c = 0$, any function is a correct answer, and the recursion has no valid case.
- **Not a minimization.** The result is not the smallest function that agrees with $f$ on $c$, and it can be larger than $f$.
- **Not the same as a conjunction.** $f \downarrow c$ is not $f \wedge c$. Outside $c$ its values are the values of $f$ at the closest care point, not 0.
- **A smaller care set is not always better.** In the example above, $c$ gives 6 nodes, but the larger care set $1$ gives $f$ with 3 nodes.
- **Separate computed tables.** The two operators give different results for the same pair, so their caches must not be shared.

## Implementations

## History

Coudert, Berthet and Madre (1989) introduced the constrain operator to compute the image of a set of states of a sequential machine without a transition relation. Coudert and Madre (1990) added restrict, which avoids the new variables of constrain. Touati, Savoj, Lin, Brayton and Sangiovanni-Vincentelli (1990) studied the properties of constrain, among them the closest-point map and the image property, and used it for implicit state enumeration. Shiple, Hojati, Sangiovanni-Vincentelli and Brayton (1994) compared many related heuristics and showed that they can increase the size. Sauerhoff and Wegener (1996) proved that finding the smallest BDD that agrees with $f$ on $c$ is NP-hard, so these operators remain heuristics.

## References
