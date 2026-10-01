# 🛰️ Mission 02 — Bring a Sensor to Life

**Difficulty:** ~4/10  
**Suggested working time:** 30–60 minutes

## 01. The situation

VEGA-01 needs another environmental measurement.

The sensor has already been chosen. The datasheet is available. What is missing is the part in between: figuring out how the sensor connects to the flight computer and getting a useful reading from it.

You have been given a few starting notes, but not a step-by-step guide.

Your job is to work out the rest.

## Your objective

Get a **BMP280** pressure and temperature sensor to a point where the avionics team could actually use it.

You should be able to answer:

> **What does the sensor need to operate?**
>
> **How does the flight computer talk to it?**
>
> **What does the sensor return?**
>
> **How do we know the readings make sense?**
>
> **What would you check if the sensor was not detected?**

You do not need to design a PCB or write a complete sensor driver.

If you have the hardware, use it. If you do not, you can complete the mission with a schematic, code, and documentation.

## Part A — Read the hardware

Start with the BMP280 datasheet and the official documentation.

Find the information you need to use the sensor:

- supply voltage,
- communication interface,
- important pins,
- I²C address,
- temperature range,
- pressure range.

You do not need to copy the whole datasheet. Find the parts that matter for this job.

## Part B — Connect it

Show how you would connect the BMP280 to a microcontroller or development board.

You may use an ESP32, Arduino, Raspberry Pi, or another suitable board.

Your diagram should show:

- power,
- ground,
- communication lines,
- any other connection you think is important.

A simple diagram is enough. It does not need to look like a finished PCB schematic.

## Part C — Read the sensor

Write a small program that reads at least:

- temperature,
- pressure.

If your platform makes it convenient, also calculate altitude.

Something like this is enough:

```text
VEGA-01 SENSOR
-------------------------
Temperature : 27.42 °C
Pressure    : 100812 Pa
Altitude    : 96.4 m
```

You may use an existing library.

We are not asking you to write a complete BMP280 driver from scratch. We do want you to understand what your code is doing well enough to explain it.

## Part D — Look one level deeper

Find **one** useful detail in the datasheet that your program or connection depends on.

This could be:

- an I²C address,
- a register,
- a configuration setting,
- a measurement mode,
- or another communication detail.

Write:

### What is it?

What does it do or represent?

### Why does it matter?

What could go wrong if it were incorrect?

### Where did you find it?

Give the datasheet section or documentation page you used.

The point is not to memorise registers. It is to see whether you can find your way through a datasheet when you need something.

## Part E — Something isn't working

Imagine your serial output says:

```text
BMP280: NOT FOUND
```

The program compiles, but the sensor does not respond.

Give **three things you would check**.

For each one, explain:

- what you would check,
- why you would check it,
- how you would check it.

Do not just write "check the wiring". Tell us what you would actually look for.

## Part F — Does it make sense?

Suppose the sensor reports:

```text
Temperature : 26.8 °C
Pressure    : 100923 Pa
```

How would you decide whether those readings are reasonable?

Give **two ways you could verify them**.

You could use another sensor, a known environmental condition, the datasheet, expected atmospheric values, repeated measurements, or another sensible method.

## Deliverables

```text
submission/mission-02/
├── hardware/
│   └── connection-diagram.png
├── firmware/
│   └── your-code
├── screenshots/
│   └── sensor-output.png
├── analysis.md
└── README.md
```

Your exact folder structure can be different if there is a good reason.

Your README should explain how to reproduce your setup.

If you could not test the hardware physically, say so. That is fine.

## Optional extra

If you have physical hardware available, try one small experiment.

For example:

- watch the temperature change,
- compare pressure with another source,
- move to a different height,
- read the sensor continuously,
- disconnect the sensor and see what your program reports.

Document what happened.

## What we want to see

You are not expected to know electronics already.

We are interested in how you approach something you have not used before.

A simple solution that you tested and understand is more useful than a complicated solution that you cannot explain.
