---
tag: VZMJS0
kind: concept
slug: conditional-independence
name: Conditional independence
aliases:
- X independent of Y given Z
- semi-graphoid axioms
area: machine-learning/probabilistic-inference
level: intro
summary: "X is independent of Y given Z when p(x, y | z) = p(x | z) p(y | z) for every z with p(z) > 0. It obeys the semi-graphoid axioms; intersection needs positivity."
history:
  year: 1979
  people: [A. Philip Dawid, Judea Pearl]
  note: Dawid wrote conditional independence as a relation with its own calculus in 1979. Pearl and Paz used the same rules as axioms for graphs in the 1980s.
prereqs: [conditional-probability, independent-random-variables]
see_also: [bayes-theorem, graphical-model, bayesian-network, markov-random-field, d-separation, markov-blanket, markov-property, naive-bayes-classifier]
sources:
  - paper: doi:10.1111/j.2517-6161.1979.tb01052.x
    title: "A. P. Dawid, Conditional independence in statistical theory, Journal of the Royal Statistical Society, Series B 41(1), 1979"
    locator: pp. 1 to 15 (the notation, the basic properties and the factorization criterion)
  - book: isbn:9781558604797
    title: "Judea Pearl, Probabilistic Reasoning in Intelligent Systems, Morgan Kaufmann, 1988"
    locator: Chapter 3, Section 3.1 (the axioms of conditional independence, namely symmetry, decomposition, weak union, contraction, and intersection for strictly positive distributions)
  - book: isbn:9780262013192
    title: "Daphne Koller and Nir Friedman, Probabilistic Graphical Models, MIT Press, 2009"
    locator: Chapter 2, Section 2.1.4 (independence and conditional independence and their properties)
  - book: isbn:9780198522195
    title: "Steffen L. Lauritzen, Graphical Models, Oxford University Press, 1996"
    locator: Chapter 3, Section 3.1 (conditional independence and its properties)
  - paper: "Milan Studený, Conditional independence relations have no finite complete characterization, in Information Theory, Statistical Decision Functions and Random Processes, Transactions of the 11th Prague Conference, Kluwer, 1992"
    locator: pp. 377 to 396
---

Two random variables $X$ and $Y$ are conditionally independent given a third variable $Z$, written $X \perp\!\!\!\perp Y \mid Z$, when $p(x, y \mid z) = p(x \mid z)\,p(y \mid z)$ for every value $z$ with $p(z) > 0$. Once $Z$ is known, learning $Y$ tells you nothing more about $X$. It is the basic notion behind every [graphical model](/graphical-model/): a [Bayesian network](/bayesian-network/) or a [Markov random field](/markov-random-field/) is a compact list of conditional independences, and they are what make inference and learning cheap. The relation obeys four rules, the semi-graphoid axioms, and a fifth rule, intersection, that holds only when the distribution has no zeros.

## In plain words

Two facts can be related only because they share a cause. The number of ice creams sold and the number of sunburns on a day go up and down together, but both follow the weather. If you already know the weather, the ice cream count tells you nothing new about sunburns. The two counts are dependent, but they are independent once the weather is fixed. The reverse also happens. Two fair coins are independent, but if someone tells you whether they show the same face, then one coin tells you the other. Conditioning can remove a dependence or create one.

## The idea

**Definition.** Let $X$, $Y$ and $Z$ be discrete random variables (each may be a tuple of variables) with joint mass function $p$. Then $X \perp\!\!\!\perp Y \mid Z$ when

$$
p(x, y, z)\,p(z) = p(x, z)\,p(y, z) \qquad \text{for all } x, y, z.
$$

When $p(z) > 0$, divide by $p(z)^2$ to get $p(x, y \mid z) = p(x \mid z)\,p(y \mid z)$. When $p(z) = 0$, both sides are 0, so the product form needs no case split. For variables with a joint density the same equation with densities is the definition, up to sets of measure zero. With $Z$ constant, it is plain independence, $X \perp\!\!\!\perp Y$.

**Equivalent forms.** Each of these is equivalent to $X \perp\!\!\!\perp Y \mid Z$.

- $p(x \mid y, z) = p(x \mid z)$ whenever $p(y, z) > 0$.
- (Factorization criterion.) $p(x, y, z) = f(x, z)\,g(y, z)$ for some nonnegative functions $f$ and $g$.

*Proof of the factorization criterion.* If $X \perp\!\!\!\perp Y \mid Z$, take $f(x, z) = p(x, z)$ and $g(y, z) = p(y, z)/p(z)$ for $p(z) > 0$, and $g = 0$ otherwise. Conversely, let $F(z) = \sum_x f(x, z)$ and $G(z) = \sum_y g(y, z)$. Summing the product gives $p(x, z) = f(x, z)G(z)$, $p(y, z) = F(z)g(y, z)$ and $p(z) = F(z)G(z)$. So $p(x, z)\,p(y, z) = f(x,z)\,g(y,z)\,F(z)\,G(z) = p(x, y, z)\,p(z)$.

**The semi-graphoid axioms.** For all disjoint sets of variables $X, Y, W, Z$ and every distribution:

| name | rule |
|---|---|
| symmetry | $X \perp\!\!\!\perp Y \mid Z \;\Rightarrow\; Y \perp\!\!\!\perp X \mid Z$ |
| decomposition | $X \perp\!\!\!\perp (Y, W) \mid Z \;\Rightarrow\; X \perp\!\!\!\perp Y \mid Z$ |
| weak union | $X \perp\!\!\!\perp (Y, W) \mid Z \;\Rightarrow\; X \perp\!\!\!\perp Y \mid (Z, W)$ |
| contraction | $X \perp\!\!\!\perp Y \mid Z$ and $X \perp\!\!\!\perp W \mid (Z, Y) \;\Rightarrow\; X \perp\!\!\!\perp (Y, W) \mid Z$ |

*Proofs.* Write $p(\cdot)$ for marginals of the joint $p(x, y, w, z)$, and use the product form.

- Symmetry: the product form is symmetric in $x$ and $y$.
- Decomposition: the hypothesis is $p(x, y, w, z)\,p(z) = p(x, z)\,p(y, w, z)$. Sum over $w$.
- Weak union: by decomposition (with $W$ and $Y$ swapped), $p(x, w, z)\,p(z) = p(x, z)\,p(w, z)$. Multiply the hypothesis by $p(w, z)$: $p(x, y, w, z)\,p(z)\,p(w, z) = p(x, z)\,p(w, z)\,p(y, w, z) = p(x, w, z)\,p(z)\,p(y, w, z)$. If $p(z) > 0$, divide by it to get $p(x, y, w, z)\,p(w, z) = p(x, w, z)\,p(y, w, z)$, the product form of the conclusion. If $p(z) = 0$, all terms with this $z$ are 0.
- Contraction: the hypotheses are $p(x, y, z)\,p(z) = p(x, z)\,p(y, z)$ and $p(x, y, w, z)\,p(y, z) = p(x, y, z)\,p(y, w, z)$. If $p(y, z) = 0$, then $p(x, y, w, z) = 0 = p(y, w, z)$ and the conclusion holds at this point. Otherwise multiply the second equation by $p(z)$ and use the first: $p(x, y, w, z)\,p(y, z)\,p(z) = p(x, z)\,p(y, z)\,p(y, w, z)$. Divide by $p(y, z) > 0$.

**Intersection needs positivity.** If $p(x, y, w, z) > 0$ for all values, then

$$
X \perp\!\!\!\perp Y \mid (Z, W) \text{ and } X \perp\!\!\!\perp W \mid (Z, Y) \;\Rightarrow\; X \perp\!\!\!\perp (Y, W) \mid Z.
$$

*Proof.* All conditionals are defined. The hypotheses give $p(x \mid w, z) = p(x \mid y, w, z) = p(x \mid y, z)$ for all $x, y, w, z$. The left side does not depend on $y$ and the right side does not depend on $w$, so both equal some $h(x, z)$. Then $p(x \mid y, w, z) = h(x, z)$ for all $y, w$, which is $X \perp\!\!\!\perp (Y, W) \mid Z$. $\blacksquare$

Without positivity it fails. Let $B$ be a fair bit and $X = Y = W = B$, with $Z$ empty. Given $W$, the value of $X$ is fixed, so $X \perp\!\!\!\perp Y \mid W$; in the same way $X \perp\!\!\!\perp W \mid Y$. But $X$ is not independent of $(Y, W)$, since $Y$ reveals $X$. A relation that satisfies all five rules is a *graphoid*; the separation relations of undirected graphs are graphoids. Intersection is the step that makes the pairwise and the global Markov properties of a [Markov random field](/markov-random-field/) agree, so that equivalence also needs a positive distribution.

**No finite list is complete.** Pearl (1988) conjectured that the semi-graphoid axioms describe exactly the relations that come from probability distributions. Studený (1992) showed that no finite set of rules of this kind does.

## Examples

**A chain.** Let $A \to B \to C$ with $A$ a fair bit and the same transition table at each step: $p(b{=}1 \mid a{=}0) = 1/10$ and $p(b{=}1 \mid a{=}1) = 8/10$. Then $A \perp\!\!\!\perp C \mid B$ by the factorization criterion, since $p(a, b, c) = [p(a)p(b \mid a)]\,p(c \mid b)$. But $p(c{=}1 \mid a{=}0) = 17/100$ and $p(c{=}1 \mid a{=}1) = 33/50$, so $A$ and $C$ are dependent. A [hidden Markov model](/hidden-markov-model/) is a chain of this kind.

**A collider.** Let $A$ and $B$ be independent fair bits and $C = A \oplus B$. All three pairs are independent: each pair is uniform on four values. But given $C$, the bit $A$ fixes $B$, so $A$ and $B$ are dependent given $C$. Conditioning on a common effect creates a dependence; this is "explaining away", and [d-separation](/d-separation/) is the graph rule that predicts it.

**Pairwise is not joint.** In the collider, $A \perp\!\!\!\perp B$ and $A \perp\!\!\!\perp C$, but $A$ is not independent of $(B, C)$, since $A = B \oplus C$. So the converse of decomposition is false.

**The base rate with two tests.** If two medical tests are conditionally independent given the disease status, their likelihood ratios multiply, as in the worked example of [Bayes' theorem](/bayes-theorem/). The tests are not independent without the condition: both are more often positive in a sick person.

**Exhaustive check.** All $2^8 - 1 = 255$ nonzero 0/1 tables on three binary variables, with each choice of roles, satisfy the four semi-graphoid rules. Among the $3^8 - 1$ nonzero tables with entries in $\{0, 1, 2\}$, some violate intersection, and each of them has a zero entry; no table with entries in $\{1, 2\}$ violates it.

## Where it is used

- A [Bayesian network](/bayesian-network/) says that each variable is independent of its non-descendants given its parents; [d-separation](/d-separation/) reads off all the independences that follow.
- A [Markov random field](/markov-random-field/) says that a variable is independent of the rest given its neighbors, its [Markov blanket](/markov-blanket/). The global, local and pairwise forms of the [Markov property](/markov-property/) are equivalent for positive distributions because of intersection.
- The [naive Bayes classifier](/naive-bayes-classifier/) assumes the features are independent given the class, which turns $d$ features with $r$ values each into $d(r-1)$ parameters per class in place of $r^d - 1$.
- [Hidden Markov models](/hidden-markov-model/) and [state space models](/state-space-model/) assume the future is independent of the past given the present state.
- [Structural causal models](/structural-causal-model/) use conditional independences as testable consequences of a causal graph, for example in the [backdoor criterion](/backdoor-criterion/).

## References
