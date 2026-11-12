---
tag: N3VQH1
kind: concept
slug: hydrophobic-effect
name: Hydrophobic effect
aliases:
- Hydrophobic collapse
area: biology/structure-prediction
level: intro
summary: Nonpolar groups in water cluster together and away from the water. In proteins this buries the nonpolar side chains in the core, and it is a main driving force of folding.
prereqs: [thermodynamic-hypothesis]
see_also: [hp-model, energy-function, energy-landscape, protein-structure-prediction, protein-secondary-structure, rosetta]
sources:
  - paper: doi:10.1016/S0065-3233(08)60608-7
    title: Walter Kauzmann, Some factors in the interpretation of protein denaturation, Advances in Protein Chemistry 14, 1959, 1-63
    locator: the hydrophobic bond as a main force that holds the native fold together
  - paper: doi:10.1126/science.653353
    title: Charles Tanford, The hydrophobic effect and the organization of living matter, Science 200(4345), 1978, 1012-1018
    locator: the free energy of transfer of nonpolar groups to water and its role in membranes and proteins
  - paper: doi:10.1038/nature04162
    title: David Chandler, Interfaces and the driving force of hydrophobic assembly, Nature 437, 2005, 640-647
    locator: the different behaviour of small and large nonpolar solutes, with a crossover near 1 nm
  - paper: doi:10.1016/0022-2836(82)90515-0
    title: Jack Kyte and Russell F. Doolittle, A simple method for displaying the hydropathic character of a protein, Journal of Molecular Biology 157(1), 1982, 105-132
    locator: the hydropathy scale of the 20 amino acids and the moving window average
  - paper: doi:10.1021/bi00327a032
    title: Ken A. Dill, Theory for the folding and stability of globular proteins, Biochemistry 24(6), 1985, 1501-1509
    locator: the model in which the hydrophobic effect drives the collapse and the stability of the fold
---

The hydrophobic effect is the tendency of nonpolar molecules, or nonpolar parts of molecules, to cluster together in water and to keep away from it. In a protein, it pushes the nonpolar side chains into a core and leaves the polar ones on the surface. Kauzmann (1959) proposed it as a main force that holds the native fold together, and most later work agrees that it is the largest single driving force of folding. The [HP model](/hp-model/) keeps only this force.

## In plain words

Oil and water do not mix. Drops of oil in water join into larger drops, because this reduces the area where oil touches water. Water molecules hold on to each other by weak bonds, and an oily surface gets in the way of these bonds.

A protein chain has oily building blocks and water-loving ones along its length. In water, the chain folds so that the oily blocks meet in the middle and the water-loving blocks stay on the outside. This first fast step is often called hydrophobic collapse: the chain becomes a compact ball long before every part is in its final place. The rest of the folding then happens inside this compact ball.

## The idea

**Transfer free energy.** Move a nonpolar solute, such as a small hydrocarbon, from a nonpolar liquid into water. The free energy change $\Delta G_{\text{tr}}$ of this transfer is positive, so the solute prefers the nonpolar liquid. For small solutes near room temperature, the enthalpy change is small and the unfavourable part comes mostly from a loss of entropy, $-T \Delta S > 0$. The water near the solute has fewer ways to arrange its hydrogen bonds. The transfer also has a large positive change of heat capacity, so the enthalpy and the entropy terms both change with temperature (Kauzmann 1959, Tanford 1978).

**Size matters.** Chandler (2005) explains that a small solute fits into the hydrogen bond network of water, which rearranges around it without breaking bonds. Its solvation free energy grows with its volume. A large nonpolar surface cannot be wrapped this way, so water loses hydrogen bonds near it, and the free energy grows with the area. The crossover is near 1 nm. When many small nonpolar groups come together into a large cluster, the second regime applies, and this gives a strong force for their assembly.

**In a protein.** Burying a nonpolar side chain in the core removes it from water, which lowers the free energy. The polar groups of the backbone must still form hydrogen bonds inside the core, which is one reason for the regular patterns of [secondary structure](/protein-secondary-structure/). The balance is delicate: the folded state of a small protein is usually more stable than the unfolded state by only a small free energy, much less than the sum of the separate terms. So an energy function must get the large terms right to get their small difference right.

**As an energy term.** The simplest model counts contacts between nonpolar residues. In the HP model, each residue is H (hydrophobic) or P (polar), and the energy of a fold is minus the number of contacts between H residues that are not chain neighbours. More detailed [energy functions](/energy-function/) use a term proportional to the nonpolar surface area that is exposed to the solvent, or a statistical term for the burial of each residue type.

## Examples

**A hydropathy profile.** Kyte and Doolittle (1982) gave each amino acid a hydropathy value, for example 4.5 for isoleucine, 3.8 for leucine, 1.8 for alanine, $-0.4$ for glycine and $-4.5$ for arginine. A moving average over a window of residues shows the nonpolar segments of a sequence. Take this synthetic sequence of 35 residues, with a nonpolar stretch in the middle:

```
KDESTKRQ LAIVGFLSALLGIVAMLTW KRDESQNK
```

With a window of 19 residues there are 17 windows. Their averages rise from 0.25 for the first window to a maximum of 2.28 for window 9, which covers exactly the 19 middle residues, and fall to $-0.18$ for the last window. Four windows have an average above 1.6. Kyte and Doolittle used a window of 19 and this kind of threshold to find segments that can cross a cell membrane, where the same effect holds the segment inside the nonpolar core of the membrane.

**How much a small protein can bury.** Place a chain of $L^3$ residues on the cubic lattice as a full cube of side $L$. Only the $(L - 2)^3$ sites inside the cube have no face on the surface.

| side $L$ | residues $L^3$ | inner sites $(L-2)^3$ | fraction inside |
|---|---|---|---|
| 3 | 27 | 1 | 0.037 |
| 5 | 125 | 27 | 0.216 |
| 10 | 1000 | 512 | 0.512 |
| 20 | 8000 | 5832 | 0.729 |

A small protein cannot hide all of its nonpolar residues, so its surface also has some. This is one reason why small proteins are only marginally stable, and why the HP model in 2D, where almost all sites are near the surface, gives a weak picture of a core.

**A lattice fold.** In the 2D HP model, the sequence HPHPPHHPHH has minimum energy $-4$: the best fold makes 4 contacts between H residues. In one optimal fold, the last residue (an H) sits at the centre, and its four lattice neighbours are all H residues. Three of these four pairs are contacts, and the fourth pair is a chain bond.

## Where it is used

- **Lattice models.** The [HP model](/hp-model/) of Dill (1985) and Lau and Dill (1989) reduces folding to the hydrophobic effect and chain connectivity.
- **Energy functions.** Implicit solvent terms, burial terms and statistical contact terms in [energy functions](/energy-function/) and in [Rosetta](/rosetta/) model the effect without explicit water.
- **Folding kinetics.** Fast hydrophobic collapse into a compact state is one of the ways in which the search of [Levinthal's paradox](/levinthal-paradox/) becomes short: the compact chain has far fewer conformations than the open chain.
- **Sequence analysis.** Hydropathy profiles find candidate membrane segments, and the pattern of nonpolar residues every three or four positions suggests an amphipathic helix.
- **Protein design.** Designers put nonpolar residues at the buried positions of a target fold and polar residues at the surface. See [protein design](/protein-design/).

## References
