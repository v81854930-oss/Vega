# 🛰️ Mission 01 — Wake the Ground Station

**Difficulty:** ~5/10  
**Suggested working time:** 2–3 hours

## 01. The situation

VEGA-01 is producing telemetry.

The radio team says the link is alive. The flight software team says packets are being generated. But the operator's screen is basically useless.

You have been given a telemetry dataset and starter notes for **YAMCS** and **Open MCT**.

Your job is to turn raw information into something a ground operator could actually work with.

## Your objective

Build a small VEGA-01 ground-station view.

An operator should be able to answer:

> **Where is the payload?**
>
> **How high is it?**
>
> **How is the battery doing?**
>
> **What is happening to temperature and pressure?**
>
> **Are GNSS and the IMU behaving normally?**
>
> **Does the radio link look healthy?**

You do not need to make it look like a commercial mission-control room. Make it clear and useful.

## Part A — Understand the data

Start with `telemetry.csv` and `data_dictionary.md`.

Work out which values are slow-changing, fast-changing, status values, operator-critical, and mainly useful as trends.

## Part B — YAMCS + Open MCT

Use the starter material and official documentation to make the supplied data usable in the ground-station tools.

Parameter names and units should be understandable to someone who did not write your configuration.

## Part C — Build the operator view

Include at least:

- a current-value view for important health parameters,
- an altitude plot,
- a battery plot,
- a temperature or pressure plot,
- GPS status,
- a basic indication of overall system status.

There is no prescribed dashboard layout.

## Part D — Find something interesting

The dataset contains a few changes worth noticing. We are not telling you where they are.

Pick **at least one** and investigate it.

Write:

### What changed?

Give the approximate time.

### Why did it catch your attention?

Describe the evidence.

### What are two possible explanations?

Do not assume the first explanation is correct.

### What would you check next?

Think about additional telemetry, logs, or bench tests.

## Deliverables

```text
submission/mission-01/
├── dashboard/
├── screenshots/
│   ├── overview.png
│   └── plots.png
├── analysis.md
└── README.md
```

Your README should explain how to reproduce your setup. If a component could not be made to work locally, document the attempt.

## Optional extra

Add one small operator aid such as a low-battery warning, stale-GPS indication, IMU-invalid indication, or another useful alarm/derived parameter.
