---
tag: PMQNYE
kind: concept
slug: multiscale-modeling
name: Multiscale modeling
area: scientific-computing/multiscale-methods
level: intro
summary: Links models at several length or time scales, passing information between a cheap coarse model and an accurate fine one where or when it is needed.
prereqs: [finite-element-method, molecular-dynamics]
see_also: [periodic-homogenization, heterogeneous-multiscale-method, fe2-method, quasicontinuum-method, qm-mm-method, coarse-projective-integration, kinetic-monte-carlo, mori-zwanzig-formalism]
sources:
  - book: isbn:9781107096547
    title: Weinan E, Principles of Multiscale Modeling, Cambridge University Press, 2011
    locator: Chapter 1 (introduction, sequential and concurrent coupling, type A and type B problems), Chapter 4 (the hierarchy of physical models) and Chapter 6 (capturing the macroscale behavior)
  - paper: doi:10.4310/CMS.2003.v1.n1.a8
    title: Weinan E and Bjorn Engquist, The heterogeneous multiscale methods, Communications in Mathematical Sciences 1(1), 2003, 87-132
    locator: the general framework of a macroscale solver with data from a microscale model, and the two types of multiscale problems
  - paper: doi:10.4310/CMS.2003.v1.n4.a5
    title: Ioannis G. Kevrekidis, C. William Gear, James M. Hyman, Panagiotis G. Kevrekidis, Olof Runborg and Constantinos Theodoropoulos, Equation-free, coarse-grained multiscale computation, Communications in Mathematical Sciences 1(4), 2003, 715-762
    locator: lifting, restriction and the coarse time stepper built from short runs of a microscopic simulator
  - book: isbn:9780387738284
    title: Grigorios A. Pavliotis and Andrew M. Stuart, Multiscale Methods, Averaging and Homogenization, Texts in Applied Mathematics 53, Springer, 2008
    locator: the introduction (scale separation, averaging and homogenization as the two classical reductions)
---

Multiscale modeling is the practice of computing a system with models at two or more scales of length or time, and of passing information between them. A fine model, such as [molecular dynamics](/molecular-dynamics/) or a fine mesh that resolves every fiber of a composite, is accurate but too costly on the whole problem. A coarse model, such as a continuum equation on a coarse mesh, is cheap but needs data it cannot compute: an effective coefficient, a stress-strain law, a reaction rate. A multiscale method takes these data from the fine model, either once before the coarse run or on the fly during it, and uses the fine model only where or when the coarse model fails. Its cost then depends on the coarse scale, not on the ratio of the scales.

## In plain words

Many things have detail at several sizes. A wing is made of fibers that are much thinner than a hair, and the fibers are made of atoms. A model of every atom of a wing is far too big for any computer. A model of the wing as one smooth material is small, but it must know how stiff that material is, and the answer depends on the fibers. Multiscale modeling joins the two views. You run the detailed model on a small piece, or only near a crack, and pass the result to the big model. The trick is to choose what to pass, and where and when the detailed model must run. Done well, you get the accuracy of the detailed model at a cost close to that of the simple one.

## The idea

**Scales and scale separation.** Let $\varepsilon$ be the fine length or time scale and $L$ the coarse one. A direct fine simulation in $d$ dimensions needs about $(L/\varepsilon)^d$ unknowns, or $L/\varepsilon$ time steps. A multiscale method is useful when $\varepsilon / L$ is small and the coarse behavior is described by a closed model whose data depend only on local fine behavior. This is scale separation. Without it, no small model exists, and the fine model must run everywhere.

**What is passed.** Upscaling (bottom-up) passes information from fine to coarse: an effective tensor, a constitutive law, a force, a rate, a coarse time derivative. Downscaling (top-down) passes the coarse state to the fine model as a boundary condition or an initial state, for example the macroscopic strain at a point, or the coarse density from which a microscopic state is built (lifting).

**Sequential and concurrent coupling.** In sequential coupling, the fine model runs before the coarse one, and its results are stored as parameters or tables: a homogenized coefficient from a cell problem, an interatomic potential fitted to quantum data, rates from [harmonic transition state theory](/harmonic-transition-state-theory/) for [kinetic Monte Carlo](/kinetic-monte-carlo/). In concurrent coupling, the fine model runs during the coarse run and gets its input from the current coarse state: the [FE2 method](/fe2-method/), the [heterogeneous multiscale method](/heterogeneous-multiscale-method/) and [coarse projective integration](/coarse-projective-integration/). Concurrent coupling is needed when the coarse law depends on states that cannot be listed in advance, for example on a strain history.

**Two types of problems.** E and Engquist separate two cases. In type A problems the coarse model is valid almost everywhere, and the fine model is needed only near isolated defects, cracks, contact lines or reaction sites; the [quasicontinuum method](/quasicontinuum-method/) and the [QM/MM method](/qm-mm-method/) are examples. In type B problems the coarse model is valid everywhere, but its constitutive data are not known in closed form, so the fine model is sampled at many coarse points; HMM and FE2 are examples. Many problems are of both types.

**Time scales.** Separation in time leads to the same ideas. A stiff system has fast modes that relax quickly to a slow manifold. Averaging and the [Mori-Zwanzig formalism](/mori-zwanzig-formalism/) give equations for the slow variables. When no such equation is known in closed form, projective methods estimate the slow time derivative from short fine runs.

## Examples

**A layered bar.** A bar is made of many thin layers of two materials with conductivities 1 and 4, in equal fractions. Heat that flows across the layers passes the layers in series, so the effective conductivity is the harmonic mean $1 / (\tfrac12 \cdot 1 + \tfrac12 \cdot \tfrac14) = 1.6$. Heat that flows along the layers passes them in parallel, so the effective conductivity is the arithmetic mean $\tfrac12 (1 + 4) = 2.5$. A coarse model that uses the plain average 2.5 in both directions is 56% too conductive across the layers. The correct values come from a small fine problem on one period, the cell problem of [periodic homogenization](/periodic-homogenization/).

**The cost of resolving all scales.** A part of size 1 m made of a composite with fibers spaced by 1 mm has $10^9$ periods in 3D. With 1000 cells per period, a direct fine mesh has $10^{12}$ cells. A coarse mesh of $10^6$ elements with one cell problem of 1000 unknowns at each integration point needs about $10^9$ unknowns in all, and the cell problems are independent, so they run in parallel. With a periodic material, one cell problem is enough for the whole part.

**Two time scales.** The linear system $y' = Ay$ with eigenvalues $-1$ and $-1000$ has a slow mode with time scale 1 and a fast mode that decays in about 0.005. The forward Euler method is stable only for steps $h < 2/1000 = 0.002$, so it needs 500 steps per unit of time to follow a solution that changes on a scale of 1. A method that resolves the fast mode only for a short time, and then takes a large step along the slow mode, needs far fewer steps; this is the idea of [coarse projective integration](/coarse-projective-integration/).

## Where it is used

- Materials: [periodic homogenization](/periodic-homogenization/), the [representative volume element](/representative-volume-element/), the [FE2 method](/fe2-method/), the [Cauchy-Born rule](/cauchy-born-rule/) and the [quasicontinuum method](/quasicontinuum-method/).
- Numerical homogenization of PDEs with rough coefficients: the [multiscale finite element method](/multiscale-finite-element-method/), [localized orthogonal decomposition](/localized-orthogonal-decomposition/) and the [heterogeneous multiscale method](/heterogeneous-multiscale-method/).
- Turbulence and stabilized methods: the [variational multiscale method](/variational-multiscale-method/) splits the solution into resolved and unresolved scales, as [large eddy simulation](/large-eddy-simulation/) does with a filter.
- Chemistry and biology: the [QM/MM method](/qm-mm-method/), coarse-grained particle models such as [dissipative particle dynamics](/dissipative-particle-dynamics/), and [kinetic Monte Carlo](/kinetic-monte-carlo/) with rates from atomistic models.
- Dynamics with slow and fast variables: [coarse projective integration](/coarse-projective-integration/) and the [Mori-Zwanzig formalism](/mori-zwanzig-formalism/).

## References
