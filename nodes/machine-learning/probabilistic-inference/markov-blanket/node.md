---
tag: 7QYGND
kind: concept
slug: markov-blanket
name: Markov blanket
aliases:
- Markov boundary
- Markov blanket of a node
area: machine-learning/probabilistic-inference
level: core
summary: "A set of variables that makes one variable independent of all the others. In a Bayesian network: parents, children, co-parents. In a Markov random field: neighbours."
prereqs: [conditional-independence, bayesian-network, markov-random-field]
see_also: [d-separation, markov-property, gibbs-sampling, feature-selection, bayesian-network-structure-learning, conditional-probability-table]
sources:
  - book: isbn:9781558604797
    title: Judea Pearl, Probabilistic Reasoning in Intelligent Systems, Networks of Plausible Inference, Morgan Kaufmann, 1988
    locator: "Chapter 3: the definitions of Markov blanket and Markov boundary, the uniqueness of the boundary for strictly positive distributions, and the blanket of a node in a Bayesian network"
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 3 (the Markov blanket in a Bayesian network) and Chapter 4 (the Markov blanket in a Markov network)"
  - book: isbn:9780198522195
    title: Steffen L. Lauritzen, Graphical Models, Oxford University Press, 1996
    locator: "Chapter 3: the local Markov property, in which the boundary of a vertex separates it from the rest"
  - paper: "Daphne Koller and Mehran Sahami, Toward optimal feature selection, Proceedings of the 13th International Conference on Machine Learning (ICML 1996), pages 284 to 292"
    title: Koller and Sahami 1996
    locator: feature selection by removing features that have a Markov blanket inside the remaining features
---

A Markov blanket of a variable $X$ is a set $S$ of other variables such that, once you know $S$, the remaining variables tell you nothing more about $X$. Judea Pearl named it in 1988. In a [Bayesian network](/bayesian-network/) the parents, the children and the children's other parents of $X$ form a blanket. In a [Markov random field](/markov-random-field/) the neighbours of $X$ form one. A *Markov boundary* is a blanket with no smaller blanket inside it, and it is unique when the distribution is positive.

## In plain words

Think of a person in a town full of rumours. If you know what everyone close to this person knows, then listening to anyone else in the town tells you nothing new about the person. The close people form a shield around the person. In a network of causes and effects, the shield is the direct causes of the variable, its direct effects, and the other causes of those effects. The last group is easy to forget. It is needed because when an effect is known, its other causes help explain whether this variable was the cause. A smallest shield is the boundary of the variable.

## The idea

**Definition.** Let $V$ be a finite set of random variables with a joint distribution $P$, and let $X \in V$. A set $S \subseteq V \setminus \{X\}$ is a *Markov blanket* of $X$ if

$$X \perp V \setminus (S \cup \{X\}) \mid S,$$

that is, if [conditional independence](/conditional-independence/) holds between $X$ and the rest given $S$. The set of all other variables is always a blanket. A *Markov boundary* is a blanket that has no proper subset that is also a blanket.

**The blanket in a Bayesian network.** Let $P$ factorize over a DAG $G$ as $P(x) = \prod_{v} P(x_v \mid x_{\mathrm{Pa}(v)})$. Put

$$\mathrm{MB}(X) = \mathrm{Pa}(X) \cup \mathrm{Ch}(X) \cup \bigcup_{c \in \mathrm{Ch}(X)} \mathrm{Pa}(c) \setminus \{X\}.$$

Then $\mathrm{MB}(X)$ is a blanket. To see it, write the conditional of $X$ given all the other variables. The factors that do not mention $x_X$ cancel between the numerator and the denominator, so

$$P(x_X \mid x_{V \setminus X}) = \frac{P(x_X \mid x_{\mathrm{Pa}(X)}) \prod_{c \in \mathrm{Ch}(X)} P(x_c \mid x_{\mathrm{Pa}(c)})}{\sum_{x'_X} P(x'_X \mid x_{\mathrm{Pa}(X)}) \prod_{c \in \mathrm{Ch}(X)} P(x_c \mid x_{\mathrm{Pa}(c)})\big|_{x_X = x'_X}}.$$

Every variable in this formula is $X$ or in $\mathrm{MB}(X)$, so the conditional does not depend on the rest. The same set is the smallest one that [d-separates](/d-separation/) $X$ from all other nodes: a parent or a child is adjacent to $X$ and cannot be blocked, and a co-parent $w$ of a child $c$ is joined to $X$ by the trail $X \to c \leftarrow w$, which is active because $c$ is in the set.

**The blanket in a Markov random field.** Let $P(x) = \frac{1}{Z} \prod_{C} \psi_C(x_C)$ over the cliques $C$ of an undirected graph $H$. In $P(x_X \mid x_{V \setminus X})$ only the factors whose clique contains $X$ remain, and those cliques lie inside $X$ and its neighbours. So the neighbours $N(X)$ form a blanket. This is the local [Markov property](/markov-property/) of $H$.

**Uniqueness of the boundary.** If $P$ is strictly positive, then the intersection of two blankets is a blanket. Let $S_1$ and $S_2$ be blankets, $U = V \setminus \{X\}$, $A = S_1 \setminus S_2$, $B = U \setminus S_1$ and $C = S_1 \cap S_2$. The blanket $S_1$ gives $X \perp B \mid A \cup C$. The blanket $S_2$ gives $X \perp U \setminus S_2 \mid S_2$, and since $A \subseteq U \setminus S_2$, weak union gives $X \perp A \mid B \cup C$. A positive distribution has the intersection property, which turns these two statements into $X \perp A \cup B \mid C$, and $A \cup B = U \setminus C$. So the intersection of all blankets is a blanket, and it is the unique boundary (Pearl 1988). Without positivity the boundary can fail to be unique, as the third example shows.

**When the graph blanket is the boundary.** In a Bayesian network, $\mathrm{MB}(X)$ always contains a boundary. If $P$ is faithful to the DAG, which holds for almost all parameters, then $\mathrm{MB}(X)$ is the boundary. For special parameters it can be too large: a child whose table ignores $X$ is in the graph blanket but is not needed.

## Examples

**A five node network.** Take $A \to B$, $A \to C$, $B \to D$, $C \to D$, $D \to E$.

| node | parents | children | co-parents | blanket |
|---|---|---|---|---|
| $A$ | none | $B, C$ | none | $\{B, C\}$ |
| $B$ | $A$ | $D$ | $C$ | $\{A, C, D\}$ |
| $D$ | $B, C$ | $E$ | none | $\{B, C, E\}$ |
| $E$ | $D$ | none | none | $\{D\}$ |

The blanket of $B$ needs $C$: given $A$ and $D$ but not $C$, the trail $B \to D \leftarrow C$ is active, and the value of $C$ changes how much of $D$ the variable $B$ must explain.

**A grid.** In an [Ising model](/ising-model/) or a [Potts model](/potts-model/) on a grid, the blanket of an inside site is its four neighbours. A Gibbs sampler updates a site from a distribution that reads only these four values.

**A boundary that is not unique.** Let $X_0$ be a fair coin, $X_1 = X_0$, and let $X_2$ depend on $X_0$, with $P(X_2 = 1 \mid X_0) = 1/5$ or $4/5$. Then $\{X_0\}$ and $\{X_1\}$ are both boundaries of $X_2$, since each one fixes the other. Their intersection is empty and is not a blanket, because $X_2$ depends on $X_0$. The distribution is not positive, so the uniqueness proof does not apply.

## Where it is used

- **Gibbs sampling.** [Gibbs sampling](/gibbs-sampling/) draws each variable from its conditional given all the others, which by the formula above needs only the tables of the variable and of its children.
- **Feature selection.** A feature that has a Markov blanket inside the other features carries no extra information about the class. Koller and Sahami (1996) used this to remove features, and later methods search for the Markov boundary of the class variable directly. See [feature selection](/feature-selection/).
- **Structure learning.** Local methods for [Bayesian network structure learning](/bayesian-network-structure-learning/) first find the boundary of each variable by independence tests and then join the pieces.
- **Inference.** The [d-separation](/d-separation/) view of the blanket tells which observations make a variable irrelevant to the rest, and the formula above is the local update in many message passing methods.

## References
