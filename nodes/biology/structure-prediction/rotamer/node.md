---
tag: TE4RF4
kind: concept
slug: rotamer
name: Rotamer
aliases:
- Rotamer library
- Side-chain rotamer
area: biology/structure-prediction
level: intro
summary: A preferred, discrete conformation of an amino acid side chain, given by its chi angles. Rotamer libraries list them with their frequencies, often as a function of the backbone angles phi and psi.
prereqs: [dihedral-angle]
see_also: [side-chain-packing, dead-end-elimination, protein-design, ramachandran-plot, comparative-modeling]
sources:
  - paper: doi:10.1016/0022-2836(78)90408-4
    title: Joel Janin, Shoshanna Wodak, Michael Levitt and Bernard Maigret, Conformation of amino acid side-chains in proteins, Journal of Molecular Biology 125(3), 1978, 357-386
    locator: the clustering of observed chi angles near the staggered values
  - paper: doi:10.1016/0022-2836(87)90358-5
    title: Jay W. Ponder and Frederic M. Richards, Tertiary templates for proteins, use of packing criteria in the enumeration of allowed sequences for different structural classes, Journal of Molecular Biology 193(4), 1987, 775-791
    locator: the rotamer library of the paper (a backbone-independent library of side-chain conformations)
  - paper: doi:10.1006/jmbi.1993.1170
    title: Roland L. Dunbrack Jr. and Martin Karplus, Backbone-dependent rotamer library for proteins, application to side-chain prediction, Journal of Molecular Biology 230(2), 1993, 543-574
    locator: the rotamer frequencies as a function of the backbone angles phi and psi
  - paper: doi:10.1016/j.str.2011.03.019
    title: Maxim V. Shapovalov and Roland L. Dunbrack Jr., A smoothed backbone-dependent rotamer library for proteins derived from adaptive kernel density estimates and regressions, Structure 19(6), 2011, 844-858
    locator: the smoothed library (adaptive kernel density estimates for the probabilities, kernel regression for the mean chi angles)
  - paper: "doi:10.1002/1097-0134(20000815)40:3<389::AID-PROT50>3.0.CO;2-2"
    title: Simon C. Lovell, J. Michael Word, Jane S. Richardson and David C. Richardson, The penultimate rotamer library, Proteins 40(3), 2000, 389-408
    locator: the p, t and m names of the chi angles, and the library filtered by data quality
---

A rotamer is one of the few preferred conformations of an amino acid side chain, given by the values of its side-chain [dihedral angles](/dihedral-angle/) $\chi_1, \chi_2, \ldots$. Observed side chains cluster near the staggered values of each bond, so a short list of rotamers, a *rotamer library*, describes most of them. Rotamers turn the continuous problem of placing side chains into a discrete one, which is the form used by [side-chain packing](/side-chain-packing/), [dead-end elimination](/dead-end-elimination/) and [protein design](/protein-design/).

## In plain words

A side chain is a small branch that hangs off the backbone of a protein. Some of its bonds can turn, like the joints of an arm. In principle each joint can take any angle. In real proteins, though, each joint prefers a few angles where the atoms are as far from each other as possible, much like a three-way switch.

A rotamer is one setting of all the switches of a side chain. A rotamer library is a table, built from many known protein structures, that lists the common settings and how often each one occurs. The table can also depend on the shape of the backbone at that residue, because the backbone changes which settings fit. Programs that build protein models pick side chains from this table instead of trying every angle.

## The idea

**The chi angles.** The side-chain dihedral angles are $\chi_1$ (about the bond $C_\alpha$-$C_\beta$, defined by the atoms N, $C_\alpha$, $C_\beta$ and the next heavy atom), $\chi_2$ (about $C_\beta$-$C_\gamma$), and so on outward. The number of heavy-atom $\chi$ angles depends on the amino acid:

| $\chi$ angles | amino acids |
|---|---|
| 0 | Gly, Ala |
| 1 | Ser, Cys, Thr, Val |
| 2 | Asp, Asn, His, Phe, Tyr, Trp, Leu, Ile, Pro |
| 3 | Met, Glu, Gln |
| 4 | Lys, Arg |

Proline is a special case: its ring closes on the backbone nitrogen, so its $\chi$ angles are tied to each other and take two main ring puckers.

**Why they are discrete.** About a single bond between two $sp^3$ atoms, the energy has three minima, the staggered positions near $+60°$, $180°$ and $-60°$. Bonds to a flat ($sp^2$) group, such as $\chi_2$ of Phe or Asp, have other preferred values and a twofold symmetry. Steric clashes with the backbone and within the side chain remove some of the combinations. So the observed $\chi$ values form a few clusters. Lovell et al. (2000) name the $\chi$ values near $+60°$, $180°$ and $-60°$ as p (plus), t (trans) and m (minus). Older names such as g+ and g- were used with opposite meanings in different papers, so a name must come with its sign convention.

**Rotamer libraries.** A library lists, for each amino acid, its rotamers with the mean and the spread of each $\chi$ angle and the probability of the rotamer.

- A *backbone-independent* library gives one probability per rotamer. Ponder and Richards (1987) gave an early library of this kind.
- A *backbone-dependent* library gives the probabilities $P(r \mid \phi, \psi)$ and the mean angles as functions of the backbone dihedral angles $\phi$ and $\psi$ of the residue (Dunbrack and Karplus 1993). The backbone changes which rotamers clash with it, so these probabilities differ a lot between, for example, a helix and a strand.
- The library of Shapovalov and Dunbrack (2011) estimates these functions with adaptive kernel density estimates and kernel regression, so that they vary smoothly with $\phi$ and $\psi$, also in regions with few observations.

**Rotamers as an energy.** In packing and design, the term $-\ln P(r \mid \phi, \psi)$ often enters the self energy $E_i(r)$ of rotamer $r$ at residue $i$. A rotamer that is rare for that backbone then costs more, even when it makes no clash.

**The cost of the discrete view.** A rotamer is an idealized point. A real side chain can sit between library values, and a tight core can need an off-rotamer angle. Programs often add extra rotamers at $\pm$ one standard deviation around each library mean, or minimize the angles after the discrete search.

## Examples

- **Classifying $\chi_1$.** With the three bins $[0°, 120°)$ for p, $[120°, 240°)$ for t and $[240°, 360°)$ for m, after reducing the angle modulo $360°$: $62°$ is p, $-65°$ (that is $295°$) is m, $178°$ and $-170°$ ($190°$) are t, and $95°$ is p, although it is far from the center $60°$ of its bin.
- **Counting combinations.** If each $\chi$ about an $sp^3$-$sp^3$ bond takes 3 values, Val has at most 3 rotamers, Leu at most $3^2 = 9$, Met at most $3^3 = 27$ and Lys at most $3^4 = 81$. Libraries list fewer, because some combinations clash. The tetrapeptide Val-Leu-Met-Lys then has at most $3 \cdot 9 \cdot 27 \cdot 81 = 59049$ combinations.
- **The growth.** A protein of 100 residues with 3 rotamers at each residue has $3^{100} \approx 5.15 \times 10^{47}$ combinations of rotamers. This is why packing needs pruning such as [dead-end elimination](/dead-end-elimination/) and exact methods that use the sparse contacts.
- **Non-examples.** Glycine and alanine have no rotamers, because they have no rotatable side-chain bond with heavy atoms on both sides. The backbone angles $\phi$ and $\psi$ are not rotamer angles; their preferred regions are shown in the [Ramachandran plot](/ramachandran-plot/).

## Where it is used

- **Side-chain packing.** SCWRL and most other packers choose one rotamer per residue from a backbone-dependent library ([side-chain packing](/side-chain-packing/)).
- **Protein design.** The rotamer set of a designed position holds rotamers of several amino acid types, so choosing a rotamer also chooses the amino acid ([protein design](/protein-design/)).
- **Comparative modeling.** Residues that differ between target and template get their side chains from a library ([comparative modeling](/comparative-modeling/)).
- **Structure validation.** Validation tools flag side chains whose $\chi$ angles are far from any common rotamer, as a sign of an error in an experimental model.

## References
