# Odoo 18 Asset Management System

A comprehensive and highly customizable Asset Management module for Odoo 18. This module provides robust tracking for hardware and company assets, featuring automated composite QR code generation, compound asset hierarchies (parent/child components), detailed financial tracking, and integrated communication via Odoo Chatter.

## 🌟 Key Features

* **Smart QR Code Generation:** Automatically generates a customized, composite QR code image upon asset creation containing the company logo, QR matrix, asset category, and a sequenced QR number (e.g., `15-4880-00626`).
* **Compound Assets:** Group multiple sub-components (e.g., Monitor, CPU, Keyboard) under a single "Parent" Compound Asset. Prevents circular dependencies and ensures accurate grouping.
* **Detailed Lifecycle Tracking:** Manage asset states including Active, Broken, Faulty, Idle, and In Servicing.
* **Comprehensive Financials:** Track Asset Value, Registration, VAT, TDS, Installation, and Insurance costs with an auto-computed Total Value field.
* **Organizational Hierarchy:** Assign assets to specific Companies, Divisions, Districts, Departments, Units, Office Locations, and exact Floor Locations.
* **Strict Classification:** Lock down "Asset Class" after creation to preserve data integrity. Categorize by Class, Category, Item, Brand, and Model.
* **Built-in Communication:** Fully integrated with Odoo's mail thread and activity mixins (Chatter) for logging notes, scheduling activities, and tracking history.
* **Role-Based Security:**
    * **Maintainer:** Can create, read, and write asset records but cannot delete them.
    * **Administrator:** Full access to all asset management configurations and the ability to delete records.

## 🛠️ Prerequisites & Dependencies

This module requires a few external Python libraries to generate the custom QR code canvases.

Ensure the following libraries are installed on your Odoo server environment:

```bash
pip install qrcode pillow