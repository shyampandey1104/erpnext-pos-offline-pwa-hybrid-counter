# ERPNext Offline Progressive Web App (PWA) POS Retail Counter

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![POS](https://img.shields.io/badge/POS-Offline%20PWA%20Counter-blueviolet.svg)](https://frappe.io)

Zero-downtime offline retail point-of-sale counter for ERPNext, designed to keep checkouts ringing even when broadband connection drops during peak store rush.

## Features
- **Offline Barcode Scanner Listener:** Instant local cache lookup for EAN-13, UPC, and Code-128 barcodes.
- **Local Cart Calculation:** Real-time multi-rate GST, discounts, and cash drawer total calculation.
- **Queued Background Sync:** Automatically submits offline transactions to ERPNext Sales Invoices upon internet restoration.

## Tests
```bash
python3 -m unittest discover tests
```
