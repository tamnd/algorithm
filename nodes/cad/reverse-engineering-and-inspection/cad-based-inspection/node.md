---
tag: NAZ6NR
kind: concept
slug: cad-based-inspection
name: CAD-based inspection
aliases:
- computer-aided inspection
area: cad/reverse-engineering-and-inspection
level: core
summary: Compares a measured part with its CAD model by planning the measurement from the model, aligning the data to the model, computing the deviations and evaluating the tolerances.
prereqs: [geometric-dimensioning-and-tolerancing]
see_also: [inspection-localization, cmm-probe-path-planning, hammersley-sampling-for-cmm, form-error-evaluation, least-squares-reference-feature, datum-reference-frame, point-projection-onto-a-surface, reverse-engineering-of-geometric-models]
sources:
  - paper: doi:10.1109/70.134279
    title: C.-H. Menq, H.-T. Yau and G.-Y. Lai, Automated precision measurement of surface profile in CAD-directed inspection, IEEE Transactions on Robotics and Automation 8(2), 1992, 268 to 278
    locator: the CAD-directed inspection of surface profiles, with the planning of points from the model, the localization of the measured points and the evaluation of the profile
  - paper: doi:10.1016/j.cad.2004.02.009
    title: Yadong Li and Peihua Gu, Free-form surface inspection techniques state of the art review, Computer-Aided Design 36(13), 2004, 1395 to 1417
    locator: the survey of the steps of free-form surface inspection, measurement planning, localization, comparison with the model and tolerance evaluation
  - paper: doi:10.1016/0010-4485(93)90054-R
    title: T. C. Woo and R. Liang, Dimensional measurement of surfaces and their sampling, Computer-Aided Design 25(4), 1993, 233 to 239
    locator: the choice of sampling points for the measurement of surfaces
  - url: https://www.iso.org/standard/66777.html
    title: ISO 1101:2017, Geometrical product specifications (GPS), Geometrical tolerancing, Tolerances of form, orientation, location and run-out, fourth edition
    locator: the standard as a whole (the tolerances that inspection evaluates); no clause is quoted
  - url: https://www.asme.org/codes-standards/find-codes-standards/y14-5-dimensioning-tolerancing
    title: ASME Y14.5-2018, Dimensioning and Tolerancing, The American Society of Mechanical Engineers, 2019
    locator: the standard as a whole (the tolerances and datum reference frames that inspection evaluates); no clause is quoted
---

CAD-based inspection is the check of a manufactured part against its nominal CAD model and the tolerances of its drawing, with the model as the reference for every step. The steps are: plan where and how to measure from the model, measure the part with a coordinate measuring machine or a scanner, place the measured points onto the model by a rigid motion, compute the deviation of each point from the nominal surface, and decide whether each tolerance is met. Each step is a separate problem with its own algorithms, linked below. The concept matters because the steps interact: the sampling decides what a form error can show, the alignment decides the deviations, and the reference feature decides the reported value.

## In plain words

A factory makes a part from a drawing kept in a computer. To check it, a machine measures many points on the real part. Then the computer lays these points over the drawing, sees how far each point is from where it should be, and checks the numbers against the limits written on the drawing.

The computer also plans the work: which points to touch, from which side, and in what order. Every choice changes the answer a little. Too few points can miss a bump. A different way of laying the points over the drawing can make a part pass or fail. So the plan, the fit and the check must all follow the same rules as the drawing.

## The idea

**The model is the reference.** In inspection without a model, each feature is measured and fitted alone, and the result is a list of sizes and form values. With the model, every measured point has a nominal place and a nominal normal, so the deviation of every point is defined, and a free-form surface can be checked as a whole by a profile tolerance.

**The steps.**

1. *Measurement planning.* From the model and the tolerances, choose the features to measure and the points on each, for example by [Hammersley sampling](/hammersley-sampling-for-cmm/) on each face. Choose the probe orientations, the order and the moves, which is [CMM probe path planning](/cmm-probe-path-planning/).
2. *Measurement.* The machine touches the points or scans the surfaces. Touch points are corrected for the radius of the stylus ball along the surface normal.
3. *Localization.* Place the points onto the model, by the datum features of the [datum reference frame](/datum-reference-frame/) or by a best fit over all surfaces, which is [localization for inspection](/inspection-localization/).
4. *Comparison.* For each point, find the closest point on the nominal surface by [point projection onto a surface](/point-projection-onto-a-surface/), and record the signed distance along the normal.
5. *Evaluation.* Evaluate each tolerance of the drawing on the deviations: form tolerances by [form error evaluation](/form-error-evaluation/) with a [least-squares reference feature](/least-squares-reference-feature/) or a minimum zone, sizes of holes by [circle fitting](/circle-fitting/), positions and profiles in the datum frame.

**The choices that change the result.**

- *Sampling* gives only a lower bound of a minimum zone form error, since every zone that holds the whole surface holds the sample.
- *The reference.* A least-squares reference is stable and simple, but its zone is never narrower than the minimum zone, so it can reject a part that the minimum zone accepts. The drawing or the standard decides which reference applies.
- *Localization.* A best fit over all surfaces and a fit to the datums give different deviations; only the datum fit follows a drawing with datums.
- *Uncertainty.* The measured deviations carry the uncertainty of the machine and of the probing, which decides how close to the limit a value can be and still be accepted.

## Examples

**A machined block.** The drawing gives the flatness of the top face, the position of four holes relative to datums A, B and C, and the diameter of each hole. The plan probes the datum faces first, then the top face and each hole at a few heights. The datum faces set the frame; the top face gives the flatness by [minimum zone flatness](/minimum-zone-flatness/); each hole gives a center and a diameter by a circle fit, and the centers are compared with their nominal positions in the frame.

**A turbine blade.** The drawing gives a profile tolerance of the airfoil. A scanner measures thousands of points on the blade. They are aligned to the model by a best fit or by the datums of the root, the deviation of every point from the airfoil surface is computed, and the result is shown as a color map. The blade passes if every deviation lies in the profile zone.

**A shaft.** The cylindricity of a bearing seat is checked from points on several sections. A least-squares cylinder gives a value that may exceed the limit. [Minimum zone cylindricity](/minimum-zone-cylindricity/), started from it, gives a value that is never larger, the width of a true zone at a local optimum, which is what the drawing asks for when it calls for the minimum zone.

## Where it is used

- **Coordinate measuring machines** in production and in the first article inspection of new parts, with programs written offline from the CAD model.
- **Optical and laser scanning** of free-form parts, castings and sheet metal, with color maps of the deviations.
- **Reverse engineering**, where a model rebuilt from scans is checked against the scans, as in [reverse engineering of geometric models](/reverse-engineering-of-geometric-models/).
- **Process control**, where the deviations of many parts are tracked to correct the machining.

## References
