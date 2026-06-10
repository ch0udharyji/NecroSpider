<div align="center">
  <img src="https://www.necrospider.net/wp-content/themes/necrospider/img/necrospider-wide.png" alt="NecroSpider Logo" width="500">
  <br><br>

  [![Rust](https://img.shields.io/badge/Rust-TUI_Launcher-orange.svg?style=for-the-badge&logo=rust)](https://crates.io/crates/necrospider-cli)
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://github.com/ch0udharyji/NecroSpider/blob/master/LICENSE)

</div>

# NecroSpider CLI

This package provides the blazing-fast interactive **Rust TUI Launcher** for [NecroSpider](https://github.com/ch0udharyji/NecroSpider).

**NecroSpider** is an advanced open source intelligence (OSINT) automation tool. It integrates with over 200 data sources and utilizes a range of methods for data analysis, making complex intelligence gathering easy to navigate.

## Overview
Instead of manually configuring environments or dealing with massive requirement lists, the `necrospider-cli` handles everything for you natively. When you run the CLI for the first time, it will automatically clone the NecroSpider Python engine into `~/.necrospider` and configure the complete environment.

### Features
- **Zero-Touch Setup**: Automatically installs Python 3 and pip if they are missing from your system.
- **Progress Tracking**: Features a beautiful `indicatif` spinner that tracks background compilation and setup directly in your terminal.
- **Premium Interface**: Replaces raw logging with an ultra-clean, double-lined interactive dashboard.

## Installation

You can install the CLI globally via Cargo:
```bash
cargo install necrospider-cli
```

## Usage

Simply type the command anywhere in your terminal:
```bash
necrospider-cli
```

You will be greeted by the hacker splash screen and prompted to choose an engine:
1. **Python (Local)**: Runs the engine directly on your host machine.

Select an option and watch as the CLI prepares the dashboard!

---
*Created by [ch0udharyji](https://ch0udharyji.com)*
