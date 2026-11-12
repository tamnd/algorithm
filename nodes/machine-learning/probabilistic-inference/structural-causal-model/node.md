---
tag: ZC6AXX
kind: model
slug: structural-causal-model
name: Structural causal model
aliases:
- SCM
area: machine-learning/probabilistic-inference
level: advanced
summary: Each variable is a function of its direct causes and an exogenous noise. Replacing equations gives interventions, and fixing the noise gives counterfactuals.
prereqs: [bayesian-network, d-separation]
see_also: [do-calculus, backdoor-criterion, bayesian-network, ancestral-sampling, directed-acyclic-graph, topological-sort, conditional-probability-table, d-separation-query]
sources:
  - book: isbn:9780521895606
    title: Judea Pearl, Causality, Models, Reasoning, and Inference, 2nd edition, Cambridge University Press, 2009
    locator: "Chapter 7, Section 7.1: causal models, submodels, the effect of an action, potential responses, probabilistic causal models, and counterfactuals computed by abduction, action and prediction; Chapter 3 for the truncated factorization"
  - book: isbn:9781119186847
    title: Judea Pearl, Madelyn Glymour and Nicholas P. Jewell, Causal Inference in Statistics, A Primer, Wiley, 2016
    locator: "Chapter 1 (structural causal models and their graphs), Chapter 3 (interventions) and Chapter 4 (counterfactuals)"
  - book: isbn:9780262037310
    title: Jonas Peters, Dominik Janzing and Bernhard Schölkopf, Elements of Causal Inference, MIT Press, 2017
    locator: "Chapter 6: structural causal models, interventions and counterfactuals in the multivariate case"
  - book: isbn:9780465097609
    title: Judea Pearl and Dana Mackenzie, The Book of Why, Basic Books, 2018
    locator: "Chapter 1: the ladder of causation with its three rungs"
---

A structural causal model (SCM) describes a system by one equation per variable. Each variable is set by a function of its direct causes and of an *exogenous* noise term that stands for everything outside the model. A probability distribution on the noise then gives a distribution on the variables. Because the equations are mechanisms, not just correlations, the model can also answer what happens when we force a variable to a value (an intervention), and what would have happened to one particular unit had something been different (a counterfactual). Pearl's book *Causality* (2000, second edition 2009) gives the standard account, and Chapter 7 states the definitions used here.

## The machine

**The model.** A structural causal model is a tuple $M = \langle U, V, F, P(u) \rangle$.

- $U = (U_1, \dots, U_m)$ are the *exogenous* variables. Nothing in the model explains them.
- $V = (V_1, \dots, V_n)$ are the *endogenous* variables.
- $F = (f_1, \dots, f_n)$ are the *structural equations*. Each one has the form $V_i := f_i(\mathrm{PA}_i, U^{(i)})$, where $\mathrm{PA}_i \subseteq V \setminus \{V_i\}$ are the direct causes of $V_i$ and $U^{(i)} \subseteq U$ is its noise.
- $P(u)$ is a distribution on the exogenous variables, usually a product of independent factors.

The symbol $:=$ means that the equation is an assignment. The right side determines the left side, and not the other way round.

**The induced graph.** Draw an arrow $V_j \to V_i$ for each $V_j \in \mathrm{PA}_i$. The model is *recursive* when this graph is a [directed acyclic graph](/directed-acyclic-graph/). Then each choice $u$ of the noise gives exactly one solution $V(u)$, which you compute by evaluating the equations in a [topological order](/topological-sort/). Two variables whose noises are dependent, or share a component, get a bidirected edge $V_i \leftrightarrow V_j$. This edge stands for an unmeasured common cause. A model with independent noises and no shared components is *Markovian*. A model with bidirected edges is *semi-Markovian*.

**Rung 1: observation.** The distribution of $V$ is the image of $P(u)$ under the solution map:

$$P(v) = \sum_{u \,:\, V(u) = v} P(u).$$

Sampling from it is [ancestral sampling](/ancestral-sampling/): draw $u$, then evaluate the equations in order.

**Rung 2: intervention.** The action $\mathrm{do}(X = x)$ on a set $X \subseteq V$ makes the *submodel* $M_x$. You delete the equation of each $V_i \in X$ and put the constant $V_i := x_i$ in its place. All other equations and $P(u)$ stay the same. Then

$$P(y \mid \mathrm{do}(x)) = P_{M_x}(Y = y).$$

In the graph, the action cuts every arrow into $X$.

**Rung 3: counterfactuals.** For a unit with noise $u$, the *potential response* $Y_x(u)$ is the value of $Y$ in $M_x$ at that $u$. The probability that $Y$ would have been $y$ had $X$ been $x$, given the evidence $e$ that was actually observed, is computed in three steps (Pearl 2009, Section 7.1).

1. **Abduction.** Replace $P(u)$ by the posterior $P(u \mid e)$.
2. **Action.** Change $M$ to $M_x$.
3. **Prediction.** Compute the distribution of $Y$ in $M_x$ under $P(u \mid e)$.

So $P(Y_x = y \mid e) = \sum_u P(u \mid e)\, [Y_x(u) = y]$. The evidence $e$ can contradict $x$. For example, we can observe that a patient was treated and ask about the same patient without treatment.

Pearl and Mackenzie (2018) call these three levels the *ladder of causation*: seeing, doing and imagining.

## What it counts

- **Size.** There are $n$ equations. With finite domains, each equation is a table with one entry for each joint value of its parents and its noise.
- **One solution.** Solving the model for one $u$ evaluates each equation once, in topological order, so it costs $n$ evaluations. One intervention costs the same, since it only replaces equations by constants.
- **Exact distributions.** Exact enumeration of $P(v)$, $P(v \mid \mathrm{do}(x))$ or a counterfactual visits every joint value of $U$, so it costs $\prod_k |\mathrm{dom}\, U_k|$ solutions. The reference code does this with exact fractions. In a Markovian model, $P(v)$ and every $P(v \mid \mathrm{do}(x))$ need only the conditional tables $P(v_i \mid \mathrm{pa}_i)$, and the general inference methods for [Bayesian networks](/bayesian-network/) apply.
- **What data can fix.** Data from the system without interventions fixes only rung 1. Whether a rung 2 quantity follows from rung 1 and the graph is the identification problem, solved by the [do-calculus](/do-calculus/). Rung 3 quantities often are not fixed even by all rung 2 data (see below).

## Relation to other models

- **Bayesian networks.** A Markovian SCM gives a [Bayesian network](/bayesian-network/) on its induced graph, with tables $P(v_i \mid \mathrm{pa}_i)$. A Bayesian network describes rung 1 only. A *causal* Bayesian network also claims that the truncated factorization below gives the effect of each intervention, which is rung 2. An SCM fixes the functions as well, which is what rung 3 needs.
- **Linear structural equation models.** Wright's path analysis (1921) and the simultaneous equation models of econometrics (Haavelmo 1943) are SCMs with linear equations and Gaussian noise. There, effects are products of path coefficients.
- **Potential outcomes.** The Neyman and Rubin framework starts from the variables $Y_x$ for each unit. In an SCM these are the potential responses $Y_x(u)$, so every SCM gives a consistent potential outcome model. Pearl (2009, Chapter 7) shows that the two languages prove the same statements when they make the same assumptions.
- **Graphical tests.** In the induced graph, [d-separation](/d-separation/) reads off conditional independences, and the graphs with cut arrows give the rules of the [do-calculus](/do-calculus/) and the [back-door criterion](/backdoor-criterion/).

## Known results in the model

**Markovian models factorize.** If $M$ is Markovian, then

$$P(v) = \prod_{i=1}^{n} P(v_i \mid \mathrm{pa}_i).$$

*Proof.* Order the variables topologically. Each $V_j$ before $V_i$ is a function of the noises of $V_1, \dots, V_{i-1}$ only. The noise $U_i$ is independent of those noises, so it is independent of $(V_1, \dots, V_{i-1})$, and given $\mathrm{PA}_i$ the variable $V_i = f_i(\mathrm{PA}_i, U_i)$ has the same distribution whatever the other earlier variables are. The chain rule then gives the product. $\square$

So the induced graph is a Bayesian network for $P(v)$, and every d-separation in it is a conditional independence. This is the *causal Markov condition*.

**Truncated factorization.** In a Markovian model, for every $v$ that agrees with $x$,

$$P(v \mid \mathrm{do}(x)) = \prod_{i \,:\, V_i \notin X} P(v_i \mid \mathrm{pa}_i),$$

and $P(v \mid \mathrm{do}(x)) = 0$ for the other $v$. The submodel $M_x$ is again Markovian. Its equations for $V_i \notin X$ and their noises are the same, so its tables for those variables are the same. Summing over everything except $X$, the parents and $Y$ gives the *adjustment for direct causes*: $P(y \mid \mathrm{do}(x)) = \sum_{\mathrm{pa}} P(y \mid x, \mathrm{pa}) P(\mathrm{pa})$ for a single variable $X$ with parents $\mathrm{PA}$. So in a Markovian model, every effect is fixed by the observational distribution.

**Doing is not seeing.** Take a severity $Z$, a treatment $X$ and a recovery $Y$, all binary:

$$Z := U_Z, \qquad X := [\,U_X < 1 + 2Z\,], \qquad Y := [\,U_Y < g(X, Z)\,],$$

with $U_Z$ a fair coin, $U_X$ uniform on $\{0, 1, 2, 3\}$, $U_Y$ uniform on $\{0, \dots, 9\}$, and $g(0,0) = 6$, $g(1,0) = 8$, $g(0,1) = 1$, $g(1,1) = 4$. Severe patients ($Z = 1$) are treated with probability $3/4$ and mild ones with probability $1/4$. The treatment raises the chance of recovery by $0.2$ in mild cases and by $0.3$ in severe ones. The induced graph has the arrows $Z \to X$, $Z \to Y$ and $X \to Y$. Exact enumeration gives:

| quantity | $x = 1$ | $x = 0$ | difference |
|---|---|---|---|
| $P(Y = 1 \mid X = x)$ (rung 1) | $0.5$ | $0.475$ | $0.025$ |
| $P(Y = 1 \mid \mathrm{do}(X = x))$ (rung 2) | $0.6$ | $0.35$ | $0.25$ |

Conditioning compares treated patients, who are mostly severe, with untreated ones, who are mostly mild. The intervention gives the treatment to everybody, so its effect is ten times larger. Adjusting for the parent $Z$ of $X$ gives the rung 2 numbers back: $0.5 \cdot 0.8 + 0.5 \cdot 0.4 = 0.6$. In this model, $Z$ satisfies the [back-door criterion](/backdoor-criterion/).

**A counterfactual.** In the same model, a patient was treated and recovered. Would the patient have recovered without treatment?

1. Abduction. $P(Z = 1, X = 1, Y = 1) = \frac12 \cdot \frac34 \cdot 0.4 = 0.15$ and $P(Z = 0, X = 1, Y = 1) = \frac12 \cdot \frac14 \cdot 0.8 = 0.1$. So the patient is severe with probability $0.6$. Recovery also says that $U_Y < g(1, Z)$, so $U_Y$ is uniform on $\{0, \dots, 7\}$ for a mild patient and on $\{0, 1, 2, 3\}$ for a severe one.
2. Action. Set $X := 0$.
3. Prediction. The patient recovers in $M_0$ when $U_Y < g(0, Z)$. This has probability $6/8$ for a mild patient and $1/4$ for a severe one.

The probability that the patient would *not* have recovered without treatment is $0.4 \cdot \frac28 + 0.6 \cdot \frac34 = 0.55$. This is the *probability of necessity* for this patient group. Since $g(1, z) \ge g(0, z)$, a treated patient who did not recover would not have recovered untreated either. The code returns probability $0$ for that case.

**Rung 2 does not fix rung 3.** Let $X$ be a fair coin and $U$ an independent fair coin. Compare $Y := U$ with $Y := X \oplus U$. Both models give independent fair coins for $(X, Y)$, and both give $P(Y = 1 \mid \mathrm{do}(X = x)) = \frac12$ for each $x$. They agree on every rung 1 and rung 2 quantity. But for a unit with $X = 1$ and $Y = 1$, the first model says $Y_0 = 1$ for sure and the second says $Y_0 = 0$ for sure. Bareinboim, Correa, Ibeling and Icard (2022) show that this gap between the rungs is the general case.

**Identification with hidden causes.** In a semi-Markovian model, $P(y \mid \mathrm{do}(x))$ may not follow from $P(v)$. In the *bow* graph $X \to Y$, $X \leftrightarrow Y$, two models with the same $P(x, y)$ can have different effects. The three rules of the [do-calculus](/do-calculus/) turn an interventional expression into an observational one whenever that is possible at all. The rules are complete (Huang and Valtorta 2006; Shpitser and Pearl 2006). The [back-door criterion](/backdoor-criterion/) is the most common special case.

**Checks in code.** The reference implementation stores a finite SCM as noise distributions and Python functions, and computes all three rungs by exact enumeration over the noise. The tests check:

- the table above and the counterfactual $0.55$;
- the factorization and the truncated factorization on random Markovian models;
- consistency: $P(Y_x = y \mid X = x, Y = y) = 1$;
- that $\mathrm{do}$ on a root is the same as conditioning on it;
- the two models above that agree on rungs 1 and 2 but not on rung 3.

## References
