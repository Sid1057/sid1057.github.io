---
layout: post
title:  "Video review: How TRI Trains Better Computer Vision Models with PD Synthetic Data"
date:   2021-07-15
last_modified_at: 2021-07-15
categories: [review, interview]
tags: [video]
---
<br/>

Good interview on the use of synthetic data in computer vision problems for autonomous driving.

<br/>

[![2021-07-15-Video review: How TRI Trains Better Computer Vision Models with PD Synthetic Data](https://img.youtube.com/vi/QIYttoVxf2w/0.jpg)](https://www.youtube.com/watch?v=QIYttoVxf2w)

<br/>

**Key points:**
- Synthetics are extremely useful
- Case on how the tracker learned to work in conditions of a large number of closed objects on the simulator
- Simulators are photorealistic enough to give a boost, and in the case of heavy models without them it is almost impossible to collect the required amount of high-quality labeled data
- Very cool case of how they used multi-tasking deep learning to improve semantics where they took most of the data from the simulator and estimated the depth in real data using monocular depth network
- Idea: you can use real data only for validation, and depending on errors for some case / class, try to generate more synthetic data automatically to fix the error
- Gaidon is cool

