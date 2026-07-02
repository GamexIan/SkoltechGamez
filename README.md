# SkoltechGamez
This repository contains the source code and simulations developed for two areas of applied research: Optical Physics (digital signal processing and beam propagation) and Operations Engineering (supply chain management )



# Bessel Beam Generation and Superposition: Numerical Characterization

This section describes the generation and numerical simulation of Bessel beams and their superposition, as presented in the work by Gámez et al. The methods and results cover both experimental setups and MATLAB-based computations.

---

##  Introduction

Bessel beams are particular solutions to the electromagnetic wave equation that exhibit the remarkable property of **diffraction-free** propagation. Unlike ordinary Gaussian beams, which spread with distance, a Bessel beam maintains a constant transverse intensity profile over a certain propagation length \( Z_{\text{max}} \). This behaviour arises from a specific transverse intensity distribution described by Bessel functions of the first kind.

The experimental generation of Bessel beams is commonly achieved using an **annular aperture mask** illuminated by a plane wave, followed by a converging lens placed at its focal distance. The light diffracted by the annular slit produces a Bessel beam.

To generate a superposition of two Bessel beams, a **Michelson interferometer** is used to split the beam intensity, with the beam splitter placed just after the lens to ensure operation within the diffraction-free region. By adjusting the optical path difference between the two arms, one can control the separation and relative phase of the two beams—parameters that are systematically characterised.


##  Superposition of Two Bessel Beams

When two Bessel beams (with possibly different amplitudes, phases, and spatial offsets) are superposed, the resulting intensity distribution is obtained by adding their complex fields and taking the squared modulus:

$$ I_{\text{total}}(r, \phi, z) = \left| E_1(r, \phi, z) + E_2(r, \phi, z) \right|^2 $$

This superposition gives rise to characteristic interference patterns that depend on the relative phase and separation. The experimental cross‑sections  and their corresponding numerical simulations  demonstrate excellent agreement.

<img src="https://raw.githubusercontent.com/GamexIan/SkoltechGamez/2ad4dededf0504931ff66ec8555e5782915cb15f/interfe.png" alt="Patrón de interferencia de dos haces Bessel" width="450"/>

##  Numerical Simulations in MATLAB


The complete MATLAB script is available in this repository. You can view it online or download it directly using the links below:

- 📄 **[View the full code on GitHub](https://github.com/GamexIan/SkoltechGamez/blob/ec8e202388b58fda8247028848153173a5ad01f9/twobeams.m)** 


<img src="https://raw.githubusercontent.com/GamexIan/SkoltechGamez/ec8e202388b58fda8247028848153173a5ad01f9/interfeskol.png" alt="Numerical interference pattern of two Bessel beams" width="600"/>

<div align="center">
  <img src="https://raw.githubusercontent.com/GamexIan/SkoltechGamez/ec8e202388b58fda8247028848153173a5ad01f9/interfeskol.png" alt="Numerical interference pattern of two Bessel beams" width="600"/>
  <br>
  <em>Figure: Cross-section of the numerical superposition of two Bessel beams, showing the characteristic interference fringes.</em>
</div>




