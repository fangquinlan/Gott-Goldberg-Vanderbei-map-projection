# Flat Map of a Sphere via Stress Minimization

This repository contains Python code that reproduces the method described in the paper "Flat Map of a Sphere via Stress Minimization" by Robert J. Vanderbei. The paper presents a novel approach to creating a flat map projection of a spherical surface by minimizing the stress experienced when stretching a rubber ball representing the sphere into a disk.

# Overview

The main idea behind this method is to find a function f(θ) that maps the latitude angle θ from the sphere to the radial distance on the flat disk, such that the stress induced by this mapping is minimized. The stress is defined as the integral of the squared magnitude of the stress tensor over the surface of the sphere.
By applying calculus of variations and solving the resulting differential equation, the paper derives an analytical solution for the optimal f(θ) function. This repository implements the same solution in Python, allowing you to visualize and explore this unique map projection.

# Results

![Figure 1](Complete_Northern_Hemisphere_Map.png)
