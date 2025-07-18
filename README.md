# Bird’s Eye View Transformation and Spatial Analysis

## Introduction

Understanding object locations and their spatial relationships is critical in applications such as surveillance, traffic analysis, and industrial safety monitoring. Conventional camera views often suffer from perspective distortion, making it difficult to accurately interpret spatial relationships between objects. Bird’s Eye View (BEV) transformation addresses this issue by providing a top-down perspective that approximates a real-world spatial layout. This report presents a methodology for applying BEV transformation using homography, followed by object segmentation application to facilitate spatial analysis.

## Problem Statement and Motivation

In real-world environments, especially in safety-critical domains such as construction sites or factories, accurately determining the position of workers, machinery, and equipment is essential. Standard camera perspectives may misrepresent distances and occlude key elements, limiting the reliability of automated spatial awareness systems.

BEV transformation helps mitigate these challenges by projecting the perspective image into a plane that simulates a top-down view. This transformation not only improves interpretability but also allows for more accurate spatial measurements and risk assessments.


## Advantages and Limitations

### Advantages

* **Improved spatial perception**: Objects are rendered without perspective distortion, making their relative positions clearer.
* **Enhanced safety analysis**: Proximity between workers and machinery can be estimated more reliably.
* **Compatibility with detection models**: BEV images can be processed by standard object detection and segmentation models with minimal adaptation.
* **Improved object tracking**: The top-down perspective reduces occlusions and simplifies motion analysis over time.
* **Integration with safety zones**: Spatial zones (e.g., danger or restricted areas) can be easily defined and monitored in BEV coordinates.

### Limitations

* **Calibration dependency**: Accuracy of the transformation heavily relies on the precision of selected calibration points.
* **Assumes flat planes**: Homography assumes the scene lies on a flat surface. Uneven terrain or 3D structures lead to distorted mappings.
* **Limited vertical information**: BEV is a 2D projection and does not capture vertical dimensions or elevation.
* **Not inherently scalable**: BEV is generally valid for a specific scene setup unless re-calibrated.

## Homography and Perspective Transformation

### Principle of Homography

Homography is a mathematical relationship that maps points from one plane to another using a projective transformation. Given four or more corresponding points between two planes, a homography matrix (3×3) can be computed. This matrix encodes the mapping necessary to transform the source image plane into a desired target plane.

### Mathematical Insight

A homography is represented by a matrix $H$ that satisfies the following relationship:

$$
x' = Hx
$$

Where:

* $x$ is a point in the original image (in homogeneous coordinates),
* $x'$ is the corresponding point in the transformed (top-down) view,
* $H$ is a 3×3 matrix with 8 degrees of freedom (since it is defined up to scale).

This transformation can model rotation, scaling, translation, and perspective distortion, making it ideal for BEV approximation.

### Parameters and Use Cases

To compute the homography, one must provide:

* At least four corresponding points from the image and the destination plane.
* Assumptions about the real-world layout (e.g., rectangular ground plane).

Homography is widely used in:

* Augmented reality
* Document scanning
* Scene rectification
* BEV transformation for autonomous systems

## Implementation Approach

The process begins with manual selection of four reference points on the image corresponding to the top-left, top-right, bottom-right, and bottom-left corners of a real-world rectangular area (e.g., a section of floor or ground).

A transformation matrix is computed using OpenCV's `getPerspectiveTransform` or `findHomography` functions. While both compute a 3×3 matrix, `findHomography` includes a robust estimation step (e.g., RANSAC) and is generally preferred when point correspondences are noisy or imperfect.

The transformation is then applied to the input image, producing a warped version approximating a top-down view.

<p align="center">
  <img src="images/BEV_test_4.jpg" alt="Base Image" width="45%" style="margin-right:10px;"/>
  <img src="images/image2.jpg" alt="BEV" width="45%"/>
</p>
<p align="center"><strong>Figure 1:</strong> Example of BEV-transformed image.</p>

## Spatial Analysis via Segmentation

After applying the bird’s eye view transformation, object detection and segmentation can be integrated to enhance spatial understanding of the scene. As an example, in this study, a YOLOv11 segmentation model trained in a prior phase was used to perform inference on a set of BEV-transformed images.

The resulting segmentations, when overlaid on the BEV view, allow for a clear spatial interpretation of objects such as workers and machinery. This facilitates higher-level spatial reasoning tasks, including:

* Proximity detection between dynamic or static entities
* Risk zone mapping based on predefined danger areas
* Tracking of object movement within constrained environments

Such insights are valuable for assessing safety conditions, monitoring compliance, and supporting decision-making in industrial or operational settings.

Example inference results are illustrated below using the YOLOv11 segmentation model applied to BEV images.

<p align="center">
  <img src="images/BEV_test_4.jpg" alt="Base Image" width="45%" style="margin-right:10px;"/>
  <img src="images/image2.jpg" alt="BEV Segmentation" width="45%"/>
</p>
<p align="center"><strong>Figure 2:</strong> Example segmentations using YOLOv11 on BEV-transformed images.</p>



## Conclusion and Outlook

Bird’s Eye View transformation is a powerful technique for improving spatial interpretability of visual data. When combined with semantic segmentation, it can enable robust safety analysis and monitoring in real-world environments. Future work could explore automatic calibration, dynamic scene adaptation, and integration with real-time analytics pipelines.



