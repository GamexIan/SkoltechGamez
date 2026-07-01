# SkoltechGamez
This repository contains the source code and simulations developed for two areas of applied research: Optical Physics (digital signal processing and beam propagation) and Operations Engineering (supply chain management )



# Bessel Beam Generation and Superposition: Experimental and Numerical Characterization

This section describes the generation and numerical simulation of Bessel beams and their superposition, as presented in the work by Gámez et al. The methods and results cover both experimental setups and MATLAB-based computations.

---

## 1. Introduction

Bessel beams are particular solutions to the electromagnetic wave equation that exhibit the remarkable property of **diffraction-free** propagation. Unlike ordinary Gaussian beams, which spread with distance, a Bessel beam maintains a constant transverse intensity profile over a certain propagation length \( Z_{\text{max}} \). This behaviour arises from a specific transverse intensity distribution described by Bessel functions of the first kind.

The experimental generation of Bessel beams is commonly achieved using an **annular aperture mask** illuminated by a plane wave, followed by a converging lens placed at its focal distance. The light diffracted by the annular slit produces a Bessel beam.

To generate a superposition of two Bessel beams, a **Michelson interferometer** is used to split the beam intensity, with the beam splitter placed just after the lens to ensure operation within the diffraction-free region. By adjusting the optical path difference between the two arms, one can control the separation and relative phase of the two beams—parameters that are systematically characterised.

---

## 2. Experimental Setup

The key optical arrangement (see **Figure 1** in the original work) consists of:

- A plane wave \( P \) illuminating an annular mask (slit of diameter \( d \)).
- A converging lens of radius \( R \) and focal length \( f \), placed such that the mask is in the back focal plane.
- The diffracted light forms a Bessel beam \( B \) that propagates without diffraction up to a distance:

\[
Z_{\text{max}} \approx \frac{R}{ \tan \theta } \quad \text{with} \quad \tan \theta = \frac{d}{2f}
\]

where \( \theta \) is the cone angle of the beam.

For the superposition, the beam is split into two arms using a Michelson interferometer. The relative phase and lateral shift between the two beams are tuned by varying the arm lengths.

---

## 3. Mathematical Description of the Bessel Beam

The ideal electric field of a Bessel beam of order \( n \) is given by:

\[
E(r, \phi, z) = A_0 \, e^{i k_z z} \, J_n(k_r r) \, e^{\pm i n \phi}
\]

where:
- \( J_n \) is the Bessel function of the first kind of order \( n \),
- \( k_z \) and \( k_r \) are the longitudinal and radial wave numbers, respectively,
- \( k = \sqrt{k_z^2 + k_r^2} = 2\pi/\lambda \) is the total wave number.

The transverse intensity profile is proportional to \( |J_n(k_r r)|^2 \), which displays concentric rings.

---

## 4. Superposition of Two Bessel Beams

When two Bessel beams (with possibly different amplitudes, phases, and spatial offsets) are superposed, the resulting intensity distribution is obtained by adding their complex fields and taking the squared modulus:

\[
I_{\text{total}}(r, \phi, z) = \left| E_1(r, \phi, z) + E_2(r, \phi, z) \right|^2
\]

This superposition gives rise to characteristic interference patterns that depend on the relative phase and separation. The experimental cross‑sections (shown in **Figures 3a–3d**) and their corresponding numerical simulations (**Figures 4a–4d**) demonstrate excellent agreement.

---

## 5. Numerical Simulations in MATLAB

The numerical implementation in MATLAB replicates the experimental conditions:

- The annular aperture and lens are modelled as an optical system that produces the Bessel beam.
- The superposition is computed by adding two Bessel fields with adjustable parameters (offset, phase, amplitude).
- The intensity profiles are plotted in 2D cross‑sections and as line‑scans through the centre.

These simulations confirm:
- The formation of the expected interference fringes.
- The preservation of the non‑diffracting nature over the computed \( Z_{\text{max}} \).
- The ability to control the beam characteristics by varying the optical parameters.

