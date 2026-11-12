---
tag: R5HKAW
kind: problem
slug: marginal-inference
name: Marginal inference
aliases:
- posterior marginal computation
area: machine-learning/probabilistic-inference
level: core
summary: "Compute P(X_Q | e) in a graphical model by summing out all other variables. Easy on trees and small width, #P-hard in general."
prereqs: [bayesian-network, markov-random-field]
see_also: [map-inference, partition-function-computation, variable-elimination, junction-tree-algorithm, belief-propagation, cooper-theorem, dagum-luby-theorem, likelihood-weighting]
sources:
  - paper: doi:10.1016/0004-3702(94)00092-1
    title: "Dan Roth, On the hardness of approximate reasoning, Artificial Intelligence 82(1-2), 1996, pages 273 to 302"
    locator: computing probabilities in Bayesian networks is #P-complete, by a reduction from counting the satisfying assignments of a formula
  - paper: doi:10.1016/0004-3702(90)90060-D
    title: "Gregory F. Cooper, The computational complexity of probabilistic inference using Bayesian belief networks, Artificial Intelligence 42(2-3), 1990, pages 393 to 405"
    locator: the decision version of exact inference is NP-hard, by a reduction from 3SAT
  - paper: doi:10.1613/jair.1236
    title: "James D. Park and Adnan Darwiche, Complexity results and approximation strategies for MAP explanations, Journal of Artificial Intelligence Research 21, 2004, pages 101 to 133"
    locator: the decision version of computing the probability of evidence is PP-complete, next to the results for MPE and MAP
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 9, Section 9.1 (the complexity of exact and approximate inference) and Sections 9.2 to 9.4 (variable elimination)"
---

Marginal inference is the problem of computing the probability of some variables of a graphical model, after the values of other variables are observed: $P(X_Q \mid E = e)$. The model is a [Bayesian network](/bayesian-network/) or a [Markov random field](/markov-random-field/), so the joint distribution is a product of small factors. The answer is a sum of this product over all values of the variables that are neither queried nor observed, divided by the same sum over the query variables too. A direct sum has a number of terms exponential in the number of variables. On trees, and on graphs of small [treewidth](/treewidth/), message passing and elimination solve it in polynomial time. In general, computing it exactly is #P-hard (Roth 1996), and even deciding whether a probability is positive is NP-hard ([Cooper 1990](/cooper-theorem/)).

## In plain words

A model says how likely each full combination of values is. You see some of the values. You want to know how likely the other values are now.

To find out, you add up the chance of every full combination that fits what you saw, grouped by the value you ask about, and you rescale so the groups add up to one.

The number of full combinations grows very fast, so adding them one by one is too slow for large models. Good methods add them up in a clever order. When the model has the shape of a tree, or is close to a tree, this is fast. For some models, no fast method is known, and the theory says one is unlikely to exist.

## Definition

**Input.** Discrete variables $X_1, \ldots, X_n$ with finite domains of size at most $d$, a set of factors $\psi_c$ with nonnegative tables, which define
$$P(x) = \frac{1}{Z} \prod_c \psi_c(x_c), \qquad Z = \sum_x \prod_c \psi_c(x_c),$$
a set of query variables $Q$, and evidence $E = e$ on a set $E$ disjoint from $Q$. For a Bayesian network, the factors are the tables $P(X_i \mid \mathrm{Pa}(X_i))$ and $Z = 1$. Let $H$ be the other variables.

**Output.** The table
$$P(x_Q \mid e) = \frac{\sum_{x_H} \prod_c \psi_c(x_Q, x_H, e)}{\sum_{x_Q} \sum_{x_H} \prod_c \psi_c(x_Q, x_H, e)}$$
for all values $x_Q$, defined when the denominator is positive. The denominator is $P(e)$ times $Z$.

**Decision versions.** (a) Given a Bayesian network, a variable $X$ and a value $x$, is $P(X = x) > 0$? This is NP-complete. (b) Given also a rational $p$, is $P(X = x) > p$? This is PP-complete.

## Variants

- **One variable or all.** Many methods give the marginals of all single variables, or of all cliques, at about twice the cost of one.
- **Probability of evidence.** $P(e)$ alone, also called the likelihood of $e$; for a Markov random field it is the [partition function](/partition-function-computation/) with the evidence fixed. Learning uses it as the [marginal likelihood](/marginal-likelihood/).
- **Joint marginals.** $P(X_Q \mid e)$ for a set $Q$ of several variables, a table with $d^{|Q|}$ entries.
- **Approximate inference.** An estimate within an absolute error $\varepsilon$, or within a factor $1 \pm \varepsilon$. These are hard too in general; see the [Dagum-Luby theorem](/dagum-luby-theorem/).
- **Continuous variables.** For jointly Gaussian models the marginals come from linear algebra, in polynomial time. Mixed and nonlinear models usually need approximation.
- **The MAP problems.** Maximizing in place of summing gives [MAP inference](/map-inference/), a different problem with different answers.

## Examples

**The sprinkler network.** $C$ (cloudy), $S$ (sprinkler), $R$ (rain), $W$ (wet grass), with $C \to S$, $C \to R$, $S \to W$, $R \to W$, and $P(C{=}1) = 0.5$, $P(S{=}1 \mid C) = 0.5, 0.1$, $P(R{=}1 \mid C) = 0.2, 0.8$, $P(W{=}1 \mid S, R) = 0, 0.9, 0.9, 0.99$.

| query | value |
|---|---|
| $P(R{=}1)$ | 0.5 |
| $P(W{=}1)$ | 0.6471 |
| $P(R{=}1 \mid W{=}1)$ | $509/719 \approx 0.708$ |
| $P(S{=}1 \mid W{=}1)$ | $309/719 \approx 0.430$ |
| $P(S{=}1 \mid W{=}1, R{=}1)$ | $99/509 \approx 0.194$ |

Wet grass makes rain more likely, from 0.5 to 0.708. Once rain is known, the sprinkler becomes less likely, from 0.430 to 0.194: the rain *explains away* the wet grass. A table of all $2^4 = 16$ joint values gives these numbers; [variable elimination](/variable-elimination/) gives them with smaller tables.

**A formula.** Let $\varphi$ be a formula in conjunctive normal form over $n$ variables. Make each variable a fair coin, and add a node $Y$ that is 1 exactly when $\varphi$ is true, through deterministic nodes for the clauses and a chain of deterministic AND nodes with two parents each, whose last node is $Y$. Then $P(Y{=}1) \cdot 2^n$ is the number of satisfying assignments. This is the construction behind the hardness results.

## Known algorithms

Exact methods:

- **Enumeration** over all joint values: $O(d^n)$ time times the number of factors. A test reference only.
- **[Variable elimination](/variable-elimination/)** (Zhang and Poole 1994; Dechter 1996): $O(n\, d^{w+1})$ for an [elimination ordering](/elimination-ordering/) of induced width $w$, for one query.
- **[Junction tree algorithm](/junction-tree-algorithm/)** (Lauritzen and Spiegelhalter 1988): the same cost, for the marginals of all cliques.
- **[Belief propagation](/belief-propagation/)**: linear time on a factor graph that is a tree, all marginals.
- Conditioning and recursive conditioning, which trade time for memory, and compilation to arithmetic circuits, which answers each query in time linear in the circuit.

Approximate methods: [loopy belief propagation](/loopy-belief-propagation/), [mean-field](/mean-field-approximation/) and other [variational methods](/variational-inference/), and sampling: [ancestral sampling](/ancestral-sampling/) and [likelihood weighting](/likelihood-weighting/) for Bayesian networks, [Gibbs sampling](/gibbs-sampling/) and other Markov chain methods.

## Bounds

- **Upper bound.** $O(n\, d^{w^*+1})$ time, where $w^*$ is the treewidth of the moral graph, given an optimal order. Finding that order is NP-hard; heuristics give a larger $w$.
- **#P-hardness.** Computing $P(X = x)$ exactly is #P-complete for Bayesian networks with binary variables, by the formula example above, which counts the satisfying assignments of a CNF formula (Roth 1996). So a polynomial algorithm would give one for every problem in #P.
- **NP-hardness of the decision version.** Deciding $P(X = x) > 0$ is NP-complete, by a reduction from 3SAT ([Cooper 1990](/cooper-theorem/)). Deciding $P(X = x) > p$ is PP-complete (Park and Darwiche 2004 give this with their results on MAP).
- **Approximation.** With evidence, an estimate of $P(X = x \mid e)$ within absolute error less than $1/2$ is NP-hard, and so is any relative approximation ([Dagum and Luby 1993](/dagum-luby-theorem/)). Without evidence, an absolute error $\varepsilon$ is easy by sampling, with $O(\varepsilon^{-2} \log(1/\delta))$ samples.
- **Fixed parameter.** For bounded treewidth, the problem is polynomial; the exponential part is only in $w$.

## Reductions

- **From #SAT.** The formula example reduces counting the satisfying assignments of a CNF formula to computing one marginal, in polynomial time. With three literals per clause, each node has at most three parents.
- **From 3SAT.** The same network decides satisfiability: $\varphi$ is satisfiable if and only if $P(Y{=}1) > 0$. This is Cooper's theorem.
- **To the partition function.** $P(x_Q \mid e) = Z(x_Q, e) / Z(e)$, where $Z(\cdot)$ is the [partition function](/partition-function/) with some variables fixed. So marginals reduce to $d^{|Q|} + 1$ partition function computations, and the converse holds by self-reducibility: for any $x$ with $\prod_c \psi_c(x_c) > 0$, $Z = \prod_c \psi_c(x_c) / P(x)$, and $P(x)$ is a product of $n$ conditional marginals $P(x_i \mid x_1, \ldots, x_{i-1})$.
- **Weighted model counting.** A Bayesian network can be written as a CNF formula with weights on the literals, so that $P(e)$ is a weighted count of the [models](/model-counting/) of the formula. Counting solvers then do inference.

## Applications

- Diagnosis in medicine and in machines: the probability of each fault given the symptoms.
- Error-correcting codes: the probability of each sent bit given the received signal, as in [belief propagation decoding](/belief-propagation-decoding/).
- Speech and sequence models: the posterior of each hidden state of a [hidden Markov model](/hidden-markov-model/), by the [forward-backward algorithm](/forward-backward-algorithm/).
- Learning: the E-step of expectation maximization needs the marginals of the hidden variables, and the gradient of a log-likelihood needs the marginals of the features.

## References
