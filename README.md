# Lovers Kernel BakaSU

**A custom Pixel kernel with adaptive tuning support.**

| Target family | Pixel 11 / Pixel 11 Pro / Pixel 11 Pro XL |
|---|---|

[English](README.md) | [日本語](README_ja.md)

Lovers Kernel BakaSU is designed for the **Pixel 11 series** and incorporates modifications related to CPU scheduling, memory management, storage, and networking. The project integrates **BakaSU** into the kernel, with optional learning and control features available through **Lovers Kernel Tuner**.

## Features

| Area | Included features |
|---|---|
| CPU scheduling | BORE on Android EEVDF, with a CASS CPU-placement port |
| IRQ balancing | SBalance with capacity-aware IRQ distribution and activity statistics |
| CPU frequency and idle | Schedutil adjustments, a TEO idle-prediction fix, and configurable CPU latency QoS |
| Memory management | DAMON/DAMOS adaptive reclaim, mTHP, and MGLRU tuning |
| ZRAM | Stock Google ZRAM and EH compression retained |
| Storage | ADIOS I/O scheduler, TMPFS support, and F2FS/EROFS fixes |
| Networking | BBRv3, CAKE, and fq_codel support |
| Power policy | RCU_LAZY and power-efficient workqueues |
| Root, SUSFS and protection | Built-in BakaSU, SUSFS, NoMount with UID isolation, and Baseband Guard (BBG) |
| Build | NoLTO with CFI retained |

Feature activity depends on the device, active CPUFreq governor, and runtime configuration. Schedutil controls apply to schedutil policies. CASS defaults to prioritizing valid Android vendor CPU selections, SBalance is disabled by default, and the idle QoS request is initially released. CAKE support does not automatically replace interface queues.

## Companion tools

### Lovers Kernel Tuner

**Lovers Kernel Tuner** provides learning, telemetry, and settings management for supported kernel interfaces.

Install the app, open it, and grant root access. Available controls depend on the running kernel, active governor, and interfaces exposed by the device. The stock Google ZRAM implementation is retained; this kernel does not activate the generic ZRAM recompression controls from the APatch variant.

The kernel provides the scheduling and tuning mechanisms; the app manages supported settings. Performance, FPS, and battery-life improvements have not been measured for this release.

## Using this project

| Artifact | How it is used |
|---|---|
| Kernel `boot.img` | Flash or boot the `boot.img` file while in fastboot mode. |
| BakaSU Manager | Install the compatible manager to manage root access |
| Lovers Kernel Tuner APK | Install as an Android app, open it, and grant root access |

The current changes are intended for Image-only replacement and do not require deploying replacement ko files. NoMount uses the matching v2.2.0 / protocol22 metamodule to configure rules.

## Credits and licensing

Thanks to the Linux kernel, Android Common Kernel, Google Pixel kernel, BakaSU, KernelSU, SUSFS, NoMount, Baseband Guard, BBR, BORE, ADIOS, and Sultan kernel contributors whose work this project builds on. Sultan-related changes are adapted for Android 6.12. Source files retain their respective copyright notices and licenses.
