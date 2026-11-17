---
tag: CJ2F7W
kind: technique
slug: next-generation-matrix
name: Next-generation matrix
aliases:
- next-generation operator
- van den Driessche-Watmough method
area: biology/epidemic-and-ecological-models
level: core
summary: Compute R0 of a model with several infected classes as the spectral radius of F V^(-1), from new infection and transition terms.
prereqs: [basic-reproduction-number, spectral-radius, perron-frobenius-theorem]
see_also: [power-iteration, eigenvalue, seir-epidemic-model, ross-macdonald-model, metapopulation-epidemic-model, jacobian-linearization, herd-immunity-threshold, gershgorin-circle-theorem]
sources:
  - paper: doi:10.1007/BF00178324
    title: O. Diekmann, J. A. P. Heesterbeek and J. A. J. Metz, On the definition and the computation of the basic reproduction ratio R0 in models for infectious diseases in heterogeneous populations, Journal of Mathematical Biology 28(4), 1990
    locator: pages 365 to 382 (R0 as the dominant eigenvalue of the operator that maps one generation of cases to the next)
  - paper: doi:10.1016/S0025-5564(02)00108-6
    title: P. van den Driessche and James Watmough, Reproduction numbers and sub-threshold endemic equilibria for compartmental models of disease transmission, Mathematical Biosciences 180(1-2), 2002
    locator: pages 29 to 48 (the split into F and V, the conditions on the split, R0 = rho(F V^(-1)), Theorem 2 on the stability of the disease-free equilibrium, and the examples, among them a vector-host model)
  - paper: doi:10.1098/rsif.2009.0386
    title: O. Diekmann, J. A. P. Heesterbeek and M. G. Roberts, The construction of next-generation matrices for compartmental epidemic models, Journal of the Royal Society Interface 7(47), 2010
    locator: pages 873 to 885 (a recipe for the matrix, the next-generation matrix with large domain and with small domain, and the link between R0 and the growth rate)
  - paper: doi:10.1016/j.idm.2017.06.002
    title: P. van den Driessche, Reproduction numbers of infectious disease models, Infectious Disease Modelling 2(3), 2017
    locator: pages 288 to 303 (a review of the method with examples, and the square root in the R0 of vector-host models as a geometric mean of the two legs)
---

The next-generation matrix is the standard technique to compute the [basic reproduction number](/basic-reproduction-number/) $R_0$ of a [compartmental epidemic model](/compartmental-epidemic-model/) with more than one infected class. Write the equations of the infected classes near the disease-free state as new infections minus all other flows, take the two Jacobians $F$ and $V$, and form $K = F V^{-1}$. Entry $K_{ij}$ is the expected number of new infections in class $i$ caused by one individual that enters class $j$. Then $R_0 = \rho(K)$, the [spectral radius](/spectral-radius/). Diekmann, Heesterbeek and Metz (1990) gave the definition for general heterogeneous populations, and van den Driessche and Watmough (2002) gave the recipe with $F$ and $V$ for ODE models.

## In plain words

Sort the infected people by type: by age, by place, by stage of disease, or by host species. For each type, ask how many new cases of each type one case of that type makes during its whole infection, if everyone else can still catch the disease. Put these numbers in a square table. One generation of cases, listed by type, times the table gives the next generation. After a few generations, the mix of types settles down, and each generation is a fixed multiple of the one before. That multiple is the reproduction number. You find it as the largest eigenvalue of the table. The work is in filling the table: you must separate the events that make a new case from the events that only move a case from one type to another.

## When it applies

- The model is a system of ODEs, and some of its classes hold infected individuals, $x = (x_1, \ldots, x_m)$.
- There is a disease-free equilibrium $x_0$, with all infected classes at zero.
- The equations of the infected classes can be split as $dx/dt = \mathcal{F}(x) - \mathcal{V}(x)$, where $\mathcal{F}_i$ is the rate at which new infections appear in class $i$, and $\mathcal{V}_i = \mathcal{V}_i^- - \mathcal{V}_i^+$ is the rate of transfers out of class $i$ minus the rate of transfers into it by any other means.
- The conditions of van den Driessche and Watmough (2002) hold. In short: all rates are non-negative, nothing leaves an empty class, there are no new infections without infected individuals, and without new infections the infected classes decay to zero. The last condition makes $V$ invertible with $V^{-1} \ge 0$ entrywise.

The same idea works for discrete-time models, for models with continuous structure such as age or time since infection (where $K$ becomes an integral operator), and for networks of patches.

## The template

1. **List the infected classes.** These are all the classes with infected individuals, infectious or not: E and I in SEIR, infected humans and infected mosquitoes in a vector model.
2. **Split each equation.** For each infected class, write $\mathcal{F}_i$ (new infections only, from susceptibles) and $\mathcal{V}_i$ (deaths, recovery, progression from one infected class to another, travel).
3. **Linearize at the disease-free state.**
$$
F = \left[ \frac{\partial \mathcal{F}_i}{\partial x_j}(x_0) \right], \qquad V = \left[ \frac{\partial \mathcal{V}_i}{\partial x_j}(x_0) \right].
$$
$F$ is non-negative. $V$ has a positive diagonal and non-positive off-diagonal entries, and $V^{-1}$ is non-negative.
4. **Form the matrix.** $K = F V^{-1}$. Entry $(V^{-1})_{kj}$ is the expected time spent in class $k$ by an individual that enters infected class $j$, and $F_{ik}$ is the rate of new infections in class $i$ caused by an individual in class $k$; the sum over $k$ is $K_{ij}$.
5. **Take the spectral radius.** $R_0 = \rho(K)$. By the [Perron-Frobenius theorem](/perron-frobenius-theorem/), $\rho(K)$ is an [eigenvalue](/eigenvalue/) of $K$ with a non-negative eigenvector, the distribution of types in a growing epidemic. For a $2 \times 2$ matrix, $\rho(K) = \left(\operatorname{tr} K + \sqrt{(\operatorname{tr} K)^2 - 4 \det K}\right) / 2$. For larger matrices, use [power iteration](/power-iteration/) or a general eigenvalue solver.
6. **Read off the threshold.** Under the conditions above, the disease-free equilibrium is locally asymptotically stable if $R_0 < 1$ and unstable if $R_0 > 1$ (van den Driessche and Watmough 2002, Theorem 2).

**A quick bound.** For a non-negative matrix, $\rho(K)$ lies between the smallest and the largest column sum, and also between the smallest and the largest row sum. This is a useful check on a computed value.

## Classic examples

**SEIR with births.** The infected classes are $(E, I)$. New infections enter E at the rate $\beta S I / N$, which is $\beta I$ at $S = N$. Progression $\sigma E$ from E to I is a transfer, not a new infection.

$$
F = \begin{pmatrix} 0 & \beta \\ 0 & 0 \end{pmatrix}, \quad V = \begin{pmatrix} \sigma + \mu & 0 \\ -\sigma & \gamma + \mu \end{pmatrix}, \quad K = \begin{pmatrix} \dfrac{\beta \sigma}{(\sigma + \mu)(\gamma + \mu)} & \dfrac{\beta}{\gamma + \mu} \\ 0 & 0 \end{pmatrix}.
$$

$K$ is triangular, so $R_0 = \beta \sigma / ((\sigma + \mu)(\gamma + \mu))$. See the [SEIR model](/seir-epidemic-model/).

**Two groups, by power iteration.** Two groups of equal size mix unevenly, and $K = \begin{pmatrix} 3 & 1 \\ 1 & 0.5 \end{pmatrix}$ is given directly. The column sums are 4 and 1.5, so $1.5 \le R_0 \le 4$. Power iteration from $v = (1, 1)$, scaled so that the first entry is 1 after each step:

| step | $K v$ | estimate of $\rho$ | next $v$ |
|---|---|---|---|
| 1 | $(4, 1.5)$ | 4 | $(1, 0.375)$ |
| 2 | $(3.375, 1.1875)$ | 3.375 | $(1, 0.351852)$ |
| 3 | $(3.351852, 1.175926)$ | 3.351852 | $(1, 0.350829)$ |
| 4 | $(3.350829, 1.175414)$ | 3.350829 | $(1, 0.350784)$ |

The exact value is $(3.5 + \sqrt{10.25})/2 \approx 3.350781$. The second eigenvalue is about 0.149, so the error shrinks by a factor of about $0.149 / 3.351 \approx 0.045$ per step.

**A vector-borne disease.** In the [Ross-Macdonald model](/ross-macdonald-model/), with $H_I$ infected humans out of $H$ and $M_I$ infected mosquitoes out of $M = m H$, the infected classes are $(H_I, M_I)$:

$$
\frac{dH_I}{dt} = a b M_I \frac{H - H_I}{H} - r H_I, \qquad \frac{dM_I}{dt} = a c \frac{H_I}{H} (M - M_I) - g M_I .
$$

Here $a$ is the biting rate, $b$ and $c$ are the probabilities of transmission per bite from mosquito to human and from human to mosquito, $r$ is the human recovery rate and $g$ is the mosquito death rate. At the disease-free state,

$$
F = \begin{pmatrix} 0 & a b \\ a c m & 0 \end{pmatrix}, \quad V = \begin{pmatrix} r & 0 \\ 0 & g \end{pmatrix}, \quad K = \begin{pmatrix} 0 & a b / g \\ m a c / r & 0 \end{pmatrix}.
$$

So $R_0 = \rho(K) = \sqrt{m a^2 b c / (r g)}$. The entry $m a c / r$ counts mosquitoes infected by one human, and $a b / g$ counts humans infected by one mosquito. The square root appears because one generation in $K$ is one leg, from human to mosquito or from mosquito to human; van den Driessche (2017) describes it as the geometric mean of the two legs. The product $m a^2 b c / (r g)$, the diagonal entry of $K^2$, counts human cases per human case and is the classical $R_0$ of Macdonald. With $m = 2$, $a = 0.5$, $b = c = 0.5$, $r = 0.05$ and $g = 0.25$, the legs are 10 and 1, the product is 10 and $\rho(K) = \sqrt{10} \approx 3.162$.

**Two patches with travel.** In the [metapopulation epidemic model](/metapopulation-epidemic-model/) with two patches of equal size, local transmission rates $\beta_1 = 0.3$ and $\beta_2 = 0.15$, recovery rate $\gamma = 0.2$, and infected individuals moving between the patches at rate $m = 0.05$ each way,

$$
F = \begin{pmatrix} 0.3 & 0 \\ 0 & 0.15 \end{pmatrix}, \quad V = \begin{pmatrix} 0.25 & -0.05 \\ -0.05 & 0.25 \end{pmatrix}, \quad K = \begin{pmatrix} 1.25 & 0.25 \\ 0.125 & 0.625 \end{pmatrix}.
$$

With $\operatorname{tr} K = 1.875$ and $\det K = 0.75$, $R_0 = (1.875 + \sqrt{0.515625})/2 \approx 1.2965$. Travel is in $V$: it moves an infected individual, it does not make a new one.

## Variations

- **Small domain.** If new infections enter only some of the infected classes (only E in SEIR), $K$ has zero rows, and the nonzero block $E^\top K E$ on the classes that receive new infections has the same spectral radius. Diekmann, Heesterbeek and Roberts (2010) call these the next-generation matrices with small and large domain. In SEIR the small one is the $1 \times 1$ matrix $(R_0)$.
- **Direct construction.** In models with types such as age groups or risk groups, you can often write $K_{ij}$ down directly as the mean number of type $i$ cases caused by one type $j$ case, without $F$ and $V$.
- **Continuous types.** With age or time since infection as a continuous type, $K$ becomes an integral operator, and $R_0$ is its spectral radius (Diekmann, Heesterbeek and Metz 1990). A discretization on a grid gives an ordinary matrix.
- **Type reproduction numbers.** To ask how much control is needed when only one type can be targeted, such as only the mosquitoes, use a type reproduction number. It has the same threshold at 1, and the critical control effort on that type is $1 - 1/T$ where $T$ is that number.
- **Control reproduction numbers.** Apply the same template to the model with vaccination or treatment in place. The [herd immunity threshold](/herd-immunity-threshold/) is the coverage at which the control reproduction number is 1.

## Pitfalls

- **Transfers counted as new infections.** In SEIR without births, if you put $\sigma E$ into $F$ instead of $V$, you get $F = \begin{pmatrix} 0 & \beta \\ \sigma & 0 \end{pmatrix}$, $V = \operatorname{diag}(\sigma, \gamma)$ and $K = \begin{pmatrix} 0 & \beta/\gamma \\ 1 & 0 \end{pmatrix}$, with $\rho(K) = \sqrt{\beta / \gamma}$. This number has the same threshold at 1, but it is not $R_0$: an exposed individual is counted as a new generation. Only infections of susceptibles belong in $F$.
- **Power iteration that does not converge.** For a vector-borne model, $K = \begin{pmatrix} 0 & 1 \\ 10 & 0 \end{pmatrix}$ has the eigenvalues $\pm \sqrt{10}$, of equal absolute value. The matrix is irreducible but not primitive (it has period 2), and plain power iteration does not converge. From $v = (1, 1)$, scaled by the largest entry, the estimates alternate: 10, 1, 10, 1, and so on. Two fixes: iterate with $K^2$, whose dominant eigenvalue $10$ is the product of the legs, and take the square root; or iterate with $K + I$, which has the same eigenvectors and the dominant eigenvalue $1 + \sqrt{10}$, and is primitive. Every irreducible non-negative matrix whose directed graph has only cycles of length 2 has this problem, as in a host-vector model without direct transmission between hosts or between vectors.
- **Not at the disease-free state.** Evaluating $F$ at a state with fewer susceptibles gives an effective reproduction number, not $R_0$.
- **The product against the square root.** For vector-borne and other two-leg models, the spectral radius and the classical product are both called $R_0$. Their threshold is the same, but derived quantities are not: the fraction of control needed on one leg is $1 - 1/(\text{product})$, not $1 - 1/\rho(K)$. Always say which form you use.
- **Units in $F$.** With frequency-dependent transmission $\beta S I / N$, $F$ has no factor $N$. With density-dependent transmission $\beta S I$, the entry is $\beta N$, so $R_0$ grows with the population size.
- **Signs in $V$.** $V$ must have the transfers into a class as negative off-diagonal entries. If $V^{-1}$ has a negative entry, the split is wrong or a condition fails.

## Exercises

1. **SIR with deaths.** Infected individuals die at rate $\mu$ and recover at rate $\gamma$. Show that $R_0 = \beta / (\gamma + \mu)$. (Answer: one infected class, $F = \beta$, $V = \gamma + \mu$.)
2. **Two symmetric groups.** Show that $K = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ has $R_0 = 3$ with eigenvector $(1, 1)$, and that both column sums are 3. (Answer: when all column sums are equal, $\rho$ equals that sum.)
3. **The square of a two-leg matrix.** For $K = \begin{pmatrix} 0 & p \\ q & 0 \end{pmatrix}$ with $p, q > 0$, show that $K^2 = p q I$, so $\rho(K) = \sqrt{p q}$.
4. **Two stages of infection.** Infected individuals pass through I1 (rate $\gamma_1$) and then I2 (rate $\gamma_2$), with transmission rates $\beta_1$ and $\beta_2$. Show that $R_0 = \beta_1 / \gamma_1 + \beta_2 / \gamma_2$. (Answer: $F$ has the first row $(\beta_1, \beta_2)$ and zeros below, $V = \begin{pmatrix} \gamma_1 & 0 \\ -\gamma_1 & \gamma_2 \end{pmatrix}$, and $K_{11} = \beta_1/\gamma_1 + \beta_2/\gamma_2$.)
5. **The shift.** Show that for a non-negative matrix $K$ and $c > 0$, $\rho(K + c I) = \rho(K) + c$, and that $K + c I$ is primitive when $K$ is irreducible.

## References
