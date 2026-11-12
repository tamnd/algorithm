---
tag: C7013H
kind: concept
slug: protein-secondary-structure
name: Protein secondary structure
area: biology/structure-prediction
level: intro
summary: The local shape of a protein backbone, given as one state per residue. Helices and beta strands come from regular backbone hydrogen bonds; DSSP assigns 8 states, often cut to 3.
prereqs: [dihedral-angle]
see_also: [ramachandran-plot, protein-secondary-structure-prediction, rna-secondary-structure, contact-map, protein-structure-prediction, chou-fasman-method]
sources:
  - paper: doi:10.1073/pnas.37.4.205
    title: Linus Pauling, Robert B. Corey and H. R. Branson, The structure of proteins, two hydrogen-bonded helical configurations of the polypeptide chain, PNAS 37(4), 1951, pages 205 to 211
    locator: the alpha helix with about 3.7 residues per turn and the bond from each C=O to the N-H of the fourth residue along the chain
  - paper: doi:10.1002/bip.360221211
    title: Wolfgang Kabsch and Christian Sander, Dictionary of protein secondary structure, pattern recognition of hydrogen-bonded and geometrical features, Biopolymers 22(12), 1983, pages 2577 to 2637
    locator: the electrostatic hydrogen bond energy, n-turns, minimal helices, bridges, ladders and sheets, and the 8 one-letter states of DSSP
  - book: isbn:9780815323051
    title: Carl Branden and John Tooze, Introduction to Protein Structure, second edition, Garland, 1999
    locator: Chapter 1 (the peptide unit, the alpha helix, beta sheets and loops)
---

Protein secondary structure is the local shape of the backbone of a protein, given as one state for each residue. The two regular shapes are the alpha helix and the beta strand, and each is held by a fixed pattern of hydrogen bonds between backbone C=O and N-H groups. The program DSSP assigns the states from atom coordinates with 8 letters, and most prediction work cuts them to 3: helix, strand and coil. Secondary structure sits between the amino acid sequence and the full 3D fold, and it is the target of [protein secondary structure prediction](/protein-secondary-structure-prediction/).

## In plain words

A protein is a chain of amino acids. The chain has a regular backbone and a side group on each amino acid. Along the backbone, some atoms can bond weakly to atoms a few places further on, or to atoms of another part of the chain.

When each amino acid bonds to the one four places ahead, the chain winds into a spring. This is a helix. When two stretches of chain lie side by side and bond across the gap, they make a flat, pleated layer. Each stretch is a strand, and the layer is a sheet. Short tight bends between these parts are turns. Everything else is coil.

Secondary structure writes one letter for each amino acid to say which shape it is part of. It ignores where the parts sit in space relative to each other.

## The idea

A protein of $n$ residues has a backbone of repeated units N, $C_\alpha$, C. Each unit has a carbonyl group C=O and, except at proline, an amide group N-H. The local shape of the backbone is fixed by the [dihedral angles](/dihedral-angle/) $\phi$ and $\psi$ of each residue, and the regular shapes are the ones where many backbone hydrogen bonds form. The model here is full backbone atoms: N, $C_\alpha$, C, O and the amide H. Side chains play no part in the definition.

### Helices

In the alpha helix the C=O of residue $i$ bonds to the N-H of residue $i + 4$, for each $i$ along the helix. The helix is right-handed. It has about 3.6 residues per turn, a rise of about 1.5 Å per residue along the axis, and so a pitch of about 5.4 Å per turn. Pauling, Corey and Branson proposed it in 1951 from the planar peptide group and the geometry of the hydrogen bond, before any protein structure was solved; their model had about 3.7 residues per turn, and solved structures later gave the value 3.6. Two less common helices use other bond patterns: the $3_{10}$ helix bonds $i$ to $i + 3$ and is tighter, and the $\pi$ helix bonds $i$ to $i + 5$ and is wider. The side chains point out from the helix, so a helix can have one water side and one buried side.

### Strands and sheets

A beta strand is a stretch of nearly fully extended chain, about 3.3 to 3.5 Å per residue. A single strand has no bonds of its own. Two or more strands lie side by side, and the C=O and N-H groups of one strand bond to the groups of its neighbour. The set of strands is a beta sheet. In an antiparallel sheet the neighbours run in opposite directions; in a parallel sheet they run in the same direction; mixed sheets have both. The side chains alternate between the two faces of the sheet. Strands that are far apart in the sequence can pair, so a sheet is not a local pattern in the sequence, which is one reason why strands are harder to predict than helices.

### Turns and coil

A turn reverses the direction of the chain over a few residues. The beta turn has four residues, with a bond from the C=O of the first to the N-H of the fourth. Coil (also called loop) is every residue that is in no helix, strand or turn. Coil is not random: it has a fixed shape in the folded protein, but the shape does not repeat.

### The DSSP assignment

Secondary structure is not measured directly. It is computed from the atom coordinates by a rule, and the standard rule is DSSP of Kabsch and Sander (1983). DSSP gives each pair of backbone groups an electrostatic energy

$$E = q_1 q_2 \left( \frac{1}{r_{ON}} + \frac{1}{r_{CH}} - \frac{1}{r_{OH}} - \frac{1}{r_{CN}} \right) f,$$

with partial charges $q_1 = 0.42e$ on C and O, $q_2 = 0.20e$ on N and H, distances $r$ in Å and $f = 332$, so that $E$ is in kcal/mol. A hydrogen bond $\mathrm{Hbond}(i, j)$ from the C=O of residue $i$ to the N-H of residue $j$ exists when $E < -0.5$ kcal/mol. The other rules use only this bond list:

- An $n$-turn at $i$ is $\mathrm{Hbond}(i, i + n)$ for $n = 3, 4, 5$.
- Two $n$-turns in a row, at $i - 1$ and $i$, make a minimal helix on residues $i$ to $i + n - 1$. Helices are the union of the minimal helices: 4-helices give state H, 3-helices give G and 5-helices give I.
- A bridge between residues $i$ and $j$ is a pair of bonds: for a parallel bridge $\mathrm{Hbond}(i - 1, j)$ and $\mathrm{Hbond}(j, i + 1)$, or $\mathrm{Hbond}(j - 1, i)$ and $\mathrm{Hbond}(i, j + 1)$; for an antiparallel bridge $\mathrm{Hbond}(i, j)$ and $\mathrm{Hbond}(j, i)$, or $\mathrm{Hbond}(i - 1, j + 1)$ and $\mathrm{Hbond}(j - 1, i + 1)$. A run of consecutive bridges of one type is a ladder, and ladders that share residues make a sheet. Residues in a ladder get E, and a residue in an isolated bridge gets B.
- Residues inside an $n$-turn that are in no helix get T. Residues where the chain bends sharply get S, from the angle between $C_\alpha$ atoms. All others get a blank, often written C or a dash.

The 8 DSSP states are H (alpha helix), G ($3_{10}$ helix), I ($\pi$ helix), E (strand in a ladder), B (isolated bridge), T (turn), S (bend) and C (coil). For prediction they are cut to 3 states, but the cut is not standard. A common cut maps H, G and I to helix, E and B to strand, and the rest to coil. Other papers map only H to helix and only E to strand. The choice changes the measured accuracy of a predictor by a few points, so a reported accuracy must name its cut.

## Examples

**A short helix in DSSP.** Take 10 residues, numbered 1 to 10, with the bonds $\mathrm{Hbond}(i, i + 4)$ for $i = 1, \ldots, 6$ and no other bonds. These are 4-turns at residues 1 to 6. The pairs of 4-turns in a row are at $(1, 2), (2, 3), \ldots, (5, 6)$, and they give the minimal helices 2 to 5, 3 to 6, 4 to 7, 5 to 8 and 6 to 9. The union is residues 2 to 9, so DSSP writes

```
residue  1 2 3 4 5 6 7 8 9 10
state    C H H H H H H H H C
```

Six bonds make a helix of 8 residues. Residues 1 and 10 take part in bonds, but each is in only one turn, so they are not helix. A single 4-turn, for example only $\mathrm{Hbond}(1, 5)$, makes no helix at all: residues 2, 3 and 4 get T.

**An antiparallel bridge.** Let residues 3 and 20 have the bonds $\mathrm{Hbond}(3, 20)$ and $\mathrm{Hbond}(20, 3)$. That is the first antiparallel pattern, so 3 and 20 form a bridge. If 4 and 19 also form a bridge, and 5 and 18 too, the three bridges make a ladder, and residues 3 to 5 and 18 to 20 get E. The two strands run in opposite directions, so the partner of $i + 1$ is $j - 1$.

**The three-state cut.** The DSSP string `CHHHHGGGTTCEEEEBSC` has 18 states. With the common cut (H, G, I to helix; E, B to strand) it becomes `CHHHHHHHCCCEEEEECC`, with 7 helix, 5 strand and 6 coil residues. With the strict cut (only H and E) it becomes `CHHHHCCCCCCEEEECCC`, with 4 helix, 4 strand and 10 coil residues. The same structure gives two different targets.

## Where it is used

- **Prediction.** Secondary structure is the first target that was predicted from sequence alone, by the [Chou-Fasman method](/chou-fasman-method/), the [GOR method](/gor-method/) and [PSIPRED](/psipred/). The problem is on its own page.
- **Structure description and classification.** Folds are described by their helices and strands and the way the strands pair. Classifications of protein domains, such as all alpha, all beta and mixed alpha and beta, start from the DSSP states.
- **Structure prediction and checks.** Predicted states restrain the search in [protein structure prediction](/protein-structure-prediction/) and [protein threading](/protein-threading/). The backbone angles of the regular states sit in known regions of the [Ramachandran plot](/ramachandran-plot/), which is used to check a model.
- **Contact maps.** Helices show as bands next to the diagonal of a [contact map](/contact-map/), and sheets as bands parallel or perpendicular to it.

RNA also has a [secondary structure](/rna-secondary-structure/), but the word means a different thing there: a set of nested base pairs, not a state for each residue.

## References
