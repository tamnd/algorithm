---
tag: 78EZEV
kind: concept
slug: ramachandran-plot
name: Ramachandran plot
aliases:
- Phi-psi plot
area: biology/structure-prediction
level: intro
summary: A map of the backbone angles phi and psi of each residue. Atom clashes leave only a few allowed regions, and the alpha helix and beta strand sit in two of them.
prereqs: [dihedral-angle, protein-secondary-structure]
see_also: [rotamer, protein-structure-prediction, energy-function, comparative-modeling, fragment-assembly]
sources:
  - paper: doi:10.1016/S0022-2836(63)80023-6
    title: G. N. Ramachandran, C. Ramakrishnan and V. Sasisekharan, Stereochemistry of polypeptide chain configurations, Journal of Molecular Biology 7(1), 1963, pages 95 to 99
    locator: the hard-sphere contact criteria and the map of allowed and outer-limit regions in the phi, psi plane
  - paper: doi:10.1002/prot.10286
    title: Simon C. Lovell, Ian W. Davis, W. Bryan Arendall III, Paul I. W. de Bakker, J. Michael Word, Michael G. Prisant, Jane S. Richardson and David C. Richardson, Structure validation by C-alpha geometry, phi, psi and C-beta deviation, Proteins 50(3), 2003, pages 437 to 450
    locator: the favored and allowed regions from high-resolution structures, with separate maps for glycine, proline and the residue before a proline
  - book: isbn:9780815323051
    title: Carl Branden and John Tooze, Introduction to Protein Structure, second edition, Garland, 1999
    locator: Chapter 1 (the phi and psi angles and the Ramachandran plot)
---

A Ramachandran plot is a map with the backbone [dihedral angle](/dihedral-angle/) $\phi$ on one axis and $\psi$ on the other, with one point for each residue of a protein. Ramachandran, Ramakrishnan and Sasisekharan showed in 1963 that clashes between backbone atoms forbid most of the $(\phi, \psi)$ plane, and that the allowed regions contain the alpha helix and the beta strand. The plot is the standard check of the backbone of a protein model: residues of good structures fall in a few dense regions, and points outside them usually show an error. Glycine and proline have their own maps.

## In plain words

Each amino acid in a protein chain has two joints in its backbone that can turn. For each amino acid you can write down the two turn angles and put a dot on a square chart, one angle across and one angle up.

Most pairs of angles are not possible, because some atoms would bump into each other. Only a few patches of the chart are free. When you plot a real protein, the dots crowd into those patches. One patch holds the amino acids of helices, and another holds those of the flat strands.

Glycine is the smallest amino acid, with a single hydrogen as its side chain, so it bumps into less and can sit in more places. Proline has a ring that locks one of its two joints, so it can sit in fewer places.

## The idea

### The map

The input is a protein backbone with full atoms N, $C_\alpha$, C and O, from which $\phi_i$ and $\psi_i$ are measured for each residue $i$ that has both neighbours. Both angles are in $(-180°, 180°]$, and the map is periodic in both directions: the left edge joins the right edge, and the top joins the bottom, so the plane is really a torus. The peptide angle $\omega$ is held at $180°$ and is not shown.

### Why regions are forbidden

Ramachandran and his coworkers modelled a short peptide with rigid planar peptide groups, fixed bond lengths and angles, and atoms as hard spheres. For each pair of atoms that are not bonded they set a normal contact distance and a smaller outer limit distance. A pair $(\phi, \psi)$ is fully allowed when no pair of atoms comes closer than the normal distance, allowed at the outer limit when no pair comes closer than the smaller distance, and forbidden otherwise. The clashes come from the backbone O and N-H groups of neighbouring residues and from the $C_\beta$ atom of the side chain. With $C_\beta$ present, positive $\phi$ is mostly forbidden.

### The regions

For a residue with a $C_\beta$ atom (every amino acid but glycine) the allowed area has these parts:

- **The alpha region**, around $\phi = -60°$, $\psi = -45°$. Right-handed alpha helices and $3_{10}$ helices sit here.
- **The beta region**, the broad upper left part, with $\phi$ from about $-180°$ to $-45°$ and $\psi$ from about $90°$ to $180°$. Beta strands sit here, and so does the polyproline II helix near $(-75°, 145°)$.
- **The left-handed region**, around $\phi = 60°$, $\psi = 45°$. It is allowed but small, and few non-glycine residues use it.
- **The bridge region** between the alpha and beta regions, near $\psi = 0°$ to $90°$ with negative $\phi$. It is narrow, and fewer residues sit there.

The hard-sphere map is a first model. Real data sets give smoother regions, shaped by hydrogen bonds and by the energy of the side chain. Lovell and coworkers (2003) drew favored and allowed contours from high-resolution structures; their favored region holds about 98 percent of the residues of that reference set, and the contours are what validation programs use today.

### Glycine and proline

- **Glycine** has no $C_\beta$, only a hydrogen atom. Its allowed area is much larger and includes large parts with positive $\phi$. Glycine is also the only amino acid that is not chiral, so its map is symmetric under $(\phi, \psi) \mapsto (-\phi, -\psi)$. Glycine is common in tight turns, where positive $\phi$ is needed.
- **Proline** has a ring that joins its side chain to its own backbone N. The ring fixes $\phi$ near $-65°$, so proline sits only in a narrow vertical band that crosses the alpha and beta regions. Proline also has no N-H group to give a hydrogen bond, so it breaks a helix inside it and is common at the first turn of a helix.
- **The residue before a proline** is also restricted, because the proline ring clashes with its backbone. Modern tools give it a separate map.

## Examples

**Points of the regular structures.** The table lists standard $(\phi, \psi)$ values and the helix that a chain with the same values at every residue makes ($\omega = 180°$). The last two columns come from a chain built with NeRF and the bond lengths N to $C_\alpha$ 1.458 Å, $C_\alpha$ to C 1.525 Å, C to N 1.329 Å, with the axis found from the rigid motion that maps one residue onto the next.

| structure | $\phi$ | $\psi$ | region | turn per residue | rise per residue |
|---|---|---|---|---|---|
| alpha helix | $-57°$ | $-47°$ | alpha | 99.4° (3.62 residues per turn) | 1.56 Å |
| $3_{10}$ helix | $-49°$ | $-26°$ | alpha | 120.5° (2.99 residues per turn) | 1.99 Å |
| $\pi$ helix | $-57°$ | $-70°$ | alpha | 84.4° (4.26 residues per turn) | 1.02 Å |
| antiparallel strand | $-139°$ | $135°$ | beta | 178.8° | 3.47 Å |
| parallel strand | $-119°$ | $113°$ | beta | 177.9° | 3.27 Å |
| polyproline II | $-75°$ | $145°$ | beta | 120.2° (2.99 residues per turn) | 3.08 Å |
| left-handed helix | $57°$ | $47°$ | left-handed | 99.4°, other hand | 1.56 Å |

The three helices of the alpha region differ mostly in $\psi$ and in how far the chain rises per residue. A strand has a turn of nearly $180°$ per residue, so its side chains point to alternate faces of the sheet. The fully extended chain $(-180°, 180°)$ gives exactly $180°$ and a rise of 3.64 Å. The left-handed helix is the mirror image of the alpha helix: its angles are the negatives, and its geometry is the same with the other hand.

**Reading one residue.** A residue with $(\phi, \psi) = (-65°, -40°)$ is in the alpha region. A residue with $(-120°, 130°)$ is in the beta region. A non-glycine residue at $(80°, -170°)$ is outside both regions; at that place a glycine is normal, so the first question for such a point in a model is whether the residue is a glycine.

## Where it is used

- **Structure validation.** Programs such as MolProbity and PROCHECK plot every residue of a new crystal structure or model and list the outliers. A good structure has very few. Outliers in a model of [protein structure prediction](/protein-structure-prediction/) or [comparative modeling](/comparative-modeling/) often show a wrong local fold or a wrong residue register.
- **Building models.** [Fragment assembly](/fragment-assembly/) and loop building pick backbone angles from the dense regions. Backbone-dependent [rotamer](/rotamer/) libraries index side chain shapes by the $(\phi, \psi)$ region.
- **Energy functions.** Statistical backbone terms in an [energy function](/energy-function/) are log frequencies over the plot.
- **Teaching secondary structure.** The plot links the [secondary structure](/protein-secondary-structure/) states to the local angles. It does not define them: DSSP uses hydrogen bonds, and a residue in the alpha region need not be in a helix.

## References
