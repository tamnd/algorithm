---
tag: 34EYNJ
kind: technique
slug: defeaturing
name: Defeaturing
aliases:
- CAD model simplification for analysis
- feature suppression
area: cad/cad-cae-integration
level: core
summary: Removes small features such as fillets, holes and chamfers that barely affect the analysis from a CAD model, to simplify meshing and speed up solves.
prereqs: [finite-element-method, feature-recognition]
see_also: [feature-based-modeling, midsurface-extraction, hausdorff-distance, mesh-quality-measures, hexahedral-mesh-generation, isogeometric-shape-optimization, galerkin-method, adjoint-sensitivity-analysis]
sources:
  - paper: doi:10.1016/j.cad.2008.11.009
    title: A. Thakur, A. G. Banerjee and S. K. Gupta, A survey of CAD model simplification techniques for physics-based simulation applications, Computer-Aided Design 41(2), 2009, 65 to 80
    locator: the whole survey (the kinds of simplification, feature based suppression, and the use of the analysis to decide what to remove)
  - paper: doi:10.1016/j.cad.2006.09.006
    title: S. H. Gopalakrishnan and K. Suresh, A formal theory for estimating defeaturing-induced engineering analysis errors, Computer-Aided Design 39(1), 2007, 60 to 68
    locator: the whole paper, the estimate of the change of a quantity of interest by an adjoint problem and integrals over the boundary of the feature
  - paper: doi:10.1016/j.cad.2011.08.006
    title: M. Li and S. Gao, Estimating defeaturing-induced engineering analysis errors for arbitrary 3D features, Computer-Aided Design 43(12), 2011, 1587 to 1597
    locator: the whole paper, the extension of the adjoint based estimate to general 3D features
  - paper: doi:10.1142/S0218202522500099
    title: A. Buffa, O. Chanon and R. Vázquez, Analysis-aware defeaturing, problem setting and a posteriori estimation, Mathematical Models and Methods in Applied Sciences 32(02), 2022, 359 to 402
    locator: the whole paper, the mathematical setting of defeaturing and an a posteriori estimator of the energy error due to removed features, with its proof of reliability for the Poisson equation
---

Defeaturing removes details of a CAD model that matter for manufacturing or looks but little for the analysis, such as small holes, fillets, chamfers, bosses, logos and tiny faces, before the model is meshed. A small feature forces small elements around it, so it can multiply the mesh size and the cost of the solve, or make meshing fail. Removing it changes the answer, and the question is by how much. The common rule, "remove what is small", is a heuristic: this page gives an exact model of the change for a stiffness quantity, shows that it is small for global quantities and not for local ones, and points to the adjoint based estimates that the literature proves. Thakur, Banerjee and Gupta (2009) survey the field.

## In plain words

A real part has many small details: rounded edges, small holes for screws, engraved text. A computer model for a strength check does not need most of them. Worse, each detail forces the mesh to use tiny pieces near it, which makes the computation slow or makes the mesh fail.

Defeaturing deletes such details and patches the gaps, so the mesh can be coarse and clean. The hard part is to decide which details are safe to delete. Size alone is a poor guide. A small hole far from the loads barely changes how much the part bends. But the same hole makes the stress next to it much higher, and if that stress is what you want to know, deleting the hole gives a wrong answer. Good tools estimate the effect of each detail on the result you need, not just its size.

## When it applies

- The model comes from CAD and holds features that are small compared with the part: fillets, chamfers, holes, bosses, ribs, text, sliver faces and short edges.
- The analysis goal is a global quantity, such as the stiffness, the mass, a natural frequency or the temperature far from the feature, rather than a peak value at the feature.
- A mesh of the full model is too costly, fails, or must be built for many design variants.
- The features can be recognized, by [feature recognition](/feature-recognition/) or from the history of a [feature-based model](/feature-based-modeling/), and removed while keeping a valid solid.

## The template

```pseudo id=main
DEFEATURE(solid M, quantity of interest Q, tolerance τ)
L1  recognize candidate features: holes, fillets, chamfers, bosses, small faces and short edges
L2  for each candidate, predict its effect on Q: by size rules, by a model as below, or by an adjoint estimate
L3  keep every feature near a load, a support or a point where Q is measured
L4  suppress the other candidates: delete their faces and heal the gap, or suppress them in the feature tree
L5  mesh and solve the simplified model
L6  estimate the effect of each suppressed feature with the solution of L5; restore those above τ and go back to L4
```

**Step L4, removal and healing.** A feature in a feature tree can be suppressed and the model rebuilt. A model without history, such as an imported boundary representation, needs face deletion: the faces of the feature are removed and the neighboring surfaces are extended until they close the solid again. Removing a hole closes a cylinder face, removing a fillet extends the two faces it joined until they meet in a sharp edge.

**Step L6, a posteriori control.** The simplified solution tells what the removed features would have done. Gopalakrishnan and Suresh (2007) estimate the change of a quantity of interest by the solution of an adjoint problem and integrals over the boundary of the removed feature, and Li and Gao (2011) extend this to general 3D features. Buffa, Chanon and Vázquez (2022) prove that an estimator built from boundary integrals over the features bounds the energy norm of the defeaturing error from above, up to a constant, for the Poisson equation with Neumann conditions on the features.

## Classic examples

**An exact model: the change of compliance.** This part is proved. Take a linear elastic body, or any problem with a symmetric positive definite stiffness, in two versions, the full model and the defeatured one. Model the feature as a change of the material in a region $\omega$: one version has the stiffness tensor $\mathbb{C}$ there and the other $\mathbb{C}'$, where $\mathbb{C}' \to 0$ models a hole. Let $K$ and $K'$ be the two stiffness matrices on a common mesh, so that $K - K'$ comes only from $\omega$. Let $K u = F$ and $K' u' = F$ with the same load $F$, and let the compliance be $C = F^T u$ and $C' = F^T u'$. Then

$$ C' - C = F^T u' - F^T u = (K u)^T u' - u^T (K' u') = u^T (K - K') u', $$

using the symmetry of $K$ and $K'$. In integral form,

$$ C' - C = \int_\omega \varepsilon(u) : (\mathbb{C} - \mathbb{C}') : \varepsilon(u') \, dx, \qquad |C' - C| \le \|\mathbb{C} - \mathbb{C}'\| \, \|\varepsilon(u)\|_{L^2(\omega)} \, \|\varepsilon(u')\|_{L^2(\omega)} . $$

The change is an integral over the feature only, of the product of the strains of the two solutions. So if both strain fields stay bounded near the feature, the change of compliance is at most a constant times the volume of the feature. That last step is a model, not a theorem: it assumes bounded strains, which fails near a crack or a re-entrant corner, and it says nothing about the size of the constant.

**The 1D bar.** A bar of length $L$, cross-section $A$ and modulus $E$ carries an end load $P$. A feature changes the section to $A'$ over a length $\ell$: a groove if $A' < A$, a boss if $A' > A$. The end displacement is $\delta = P(L - \ell)/(EA) + P\ell/(EA')$, and after defeaturing it is $\delta_0 = PL/(EA)$. So

$$ \delta - \delta_0 = P \ell \left( \frac{1}{EA'} - \frac{1}{EA} \right), \qquad \frac{\delta - \delta_0}{\delta_0} = \frac{\ell}{L} \left( \frac{A}{A'} - 1 \right). $$

The compliance identity gives the same result, with the defeatured model as the unprimed one, $\varepsilon(u) = P/(EA)$ and $\varepsilon(u') = P/(EA')$ over the length $\ell$, and $C = P \delta_0$, $C' = P \delta$. For $L = 100$, $\ell = 2$, $A = 1$ and $A' = 0.5$, the end displacement changes by $2\%$. But the stress in the groove is $P/A'$, twice the value $P/A$ of the defeatured model, and this factor $A/A'$ does not shrink with $\ell$. Defeaturing is safe here for the stiffness and wrong by a factor 2 for the peak stress.

**A small hole in a plate.** Kirsch's classical solution for a circular hole in a large plate under the remote tension $S$ gives the peak stress $3S$ at the edge of the hole, for every hole radius. A tiny hole changes the stiffness of the plate by an amount that goes to zero with its area, but it triples the local stress. So a hole can be removed for a stiffness or a deflection analysis and must be kept for a fatigue analysis at that spot.

**Fillets.** A fillet of radius $r$ at a re-entrant corner keeps the stress finite. Without it, the sharp corner gives a singular stress in linear elasticity, which grows without bound as the mesh is refined there. Removing a fillet at a re-entrant corner thus changes the local stress from finite to infinite, while a fillet on a convex edge carries almost no stress and is safe to remove.

## Variations

- **Feature based suppression.** Use the feature tree of the CAD system and suppress features by type and size. Fast, but it needs the history.
- **Geometric simplification.** Remove small faces, merge sliver faces and collapse short edges on a boundary representation or a mesh, without feature semantics. Measures such as the [Hausdorff distance](/hausdorff-distance/) control the geometric change, not the analysis error.
- **Analysis-aware defeaturing.** Decide by an estimate of the effect on the quantity of interest, with an adjoint problem as in Step L6, and refine the model adaptively by adding features back.
- **Dimensional reduction.** Replace thin regions by surfaces or beams, as in [midsurface extraction](/midsurface-extraction/). This is a stronger simplification of the same kind.
- **Virtual topology.** Merge faces for meshing only, without changing the CAD geometry, so the mesher can ignore the small faces between them.

## Pitfalls

- **Size is not effect.** In the bar, a groove with $A' \to 0$ has a tiny volume $\ell (A - A')$ but makes $\delta - \delta_0$ unbounded. A thin slit has almost no volume and can halve the stiffness. Judge features by their effect on the result, not by their volume or their [Hausdorff distance](/hausdorff-distance/) from the simplified model.
- **Local quantities.** Peak stresses, contact pressures and heat fluxes at or near a feature can change by a factor that does not shrink with the feature, as the hole and the groove show. Keep every feature where such a quantity is wanted.
- **Loads and supports on features.** A bolt hole that carries the load or a face that is clamped cannot be removed without changing the problem itself.
- **Invalid solids.** Face deletion can leave gaps or self-intersections when the extended neighbor surfaces do not meet cleanly. Check that the result is a closed, valid solid before meshing.
- **Interactions.** Features that are each harmless can matter together, for example a row of small holes that forms a perforation line. Estimate groups, not only single features.

## Exercises

1. Derive $\delta - \delta_0 = P \ell (1/(EA') - 1/(EA))$ for the bar, and check it against the compliance identity $C' - C = u^T (K - K') u'$ with $C = P \delta$.
2. A bar with $L = 200$ has a boss of length $\ell = 5$ with $A' = 2A$. By how much does removing it change the end displacement? *Answer:* the defeatured model is softer, $\delta_0 - \delta = \delta_0 \cdot (5/200)(1 - 1/2) = 1.25\%$ of $\delta_0$.
3. Show that $C' \ge C$ when the primed model is softer, that is when $K' \le K$ in the sense of quadratic forms. *Hint:* $C = F^T u = \max_v (2 F^T v - v^T K v)$, and the maximum grows when $K$ shrinks.
4. A plate is analyzed for its first natural frequency and for the stress at a bolt hole. Which features may be removed for each analysis?
5. Give a feature with a tiny volume that changes the stiffness of a part by more than half.

## References
