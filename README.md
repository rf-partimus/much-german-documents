# **Much QWeb Updater**

This module enhances Odoo's reporting capabilities by providing extensive customization options for QWeb reports, conforming to the German DIN 5008 standard. It allows for detailed adjustments of report layouts, headers, footers, and adds various fields and settings to improve the clarity and information density of your business documents. This base module is extended by several other modules to provide these features across different Odoo applications like Sales, Purchasing, Accounting, and Inventory.

**Table of Contents**

* [Features](#features)  
* [Configuration](#configuration)  
* [Usage](#usage)  
* [Dependencies](#dependencies)  
* [Limitations, Issues & Bugs](#limitations-issues--bugs)  
* [Support](#support)  
* [Development](#development)  
* [Tests](#tests)

## **Features**

* **Customizable Report Layout:** Modifies the standard report layout to be compliant with the DIN 5008 standard.  
* **Dynamic Header and Footer:** Allows for extensive customization of report footers with free text and up to four columns.  
* **Logo Adjustment:** Provides options to adjust the height and width of the company logo in reports.  
* **Additional Fields:** Adds new fields to various models, such as "Order Title" and "Description before Table," to provide more context in documents.  
* **Configurable Visibility:** Many of the new features can be enabled or disabled through settings, giving you full control over your document layouts.  
* **Multi-Language Support:** Includes translations for German.  
* **Modular Architecture:** The core functionality is provided by the much\_qweb\_updater module, with additional modules extending these features to specific Odoo applications.

## **Configuration**

To configure the module, you will need the appropriate access rights (typically "Administration / Settings").

1. Go to **Settings \> Qweb Updater**.  
2. Here you will find several tabs for configuring the different modules:  
   * **Much Qweb Updater:** Configure general report settings like the footer, logo, and company country.  
   * **Much Qweb Updater Account:** Settings for invoices and credit notes.  
   * **Much Qweb Updater Inventory:** Settings for delivery slips.  
   * **Much Qweb Updater Purchase:** Settings for purchase orders and RFQs.  
   * **Much Qweb Updater Purchase Requisition:** Settings for blanket orders.  
   * **Much Qweb Updater Sale:** Settings for sales orders and quotations.

## **Usage**

Once installed, the module automatically applies the new report layouts. You can further customize the reports and documents through the settings menu. Additionally, when creating or editing documents like sales orders, invoices, or delivery slips, you will find new fields such as "Order Title" and "Description before Table" that you can use to add extra information to the printed reports.

## **Dependencies**

### **Odoo modules dependencies**

| Module | Why used? | Side effects |
| :---- | :---- | :---- |
| l10n\_din5008 | For the base DIN 5008 report layout. | None |
| l10n\_de\_reports | For German-specific reporting features. | None |
| account | To modify accounting reports and documents. | None |
| purchase | To modify purchase orders and RFQs. | None |
| purchase\_requisition | To modify purchase agreements/blanket orders. | None |
| sale\_management | To modify sales orders and quotations. | None |
| stock | To modify inventory documents like delivery slips. | None |
| stock\_delivery | To extend delivery slip reports with additional info. | None |

### **Python library dependencies**

| Package | Why used? | URL doc |
| :---- | :---- | :---- |
|  |  |  |

## **Limitations, Issues & Bugs**

There are no known issues or bugs at the moment. If you find any, please report them through the appropriate channels.

## **Support**

For support, please visit the much. products tab on this [page](https://muchconsulting.com/managed-services-portal) or open a ticket directly using this [form](https://erp.muchconsulting.de/open-product-ticket).

## **Development**

### **Technical Architecture**

The "Much QWeb Updater" is not a single module but a suite of modules designed with a modular and extensible architecture. The core of this suite is the much\_qweb\_updater module, which provides the foundational functionalities for report customization. Several other modules then extend this base to provide application-specific features for different Odoo business areas like Sales, Purchasing, Accounting, and Inventory.

#### **Core Module: much\_qweb\_updater**

This is the central module of the suite and provides the following key functionalities:

* **Base Report Layout:** It inherits from the l10n\_din5008.external\_layout\_din5008 template to provide a DIN 5008 compliant report layout. This serves as the foundation for all other reports in the suite.  
* **Centralized Configuration:** It introduces a new settings page under **Settings \> Qweb Updater** where users can configure general report settings. This includes options for a free-text footer with multiple columns, logo size adjustments, and more.  
* **Customizable Company and Partner Data:** It extends the res.company and res.partner models to include new fields for report customization, such as report\_primary\_color, report\_secondary\_color, free\_text\_footer, logo\_width, logo\_height, etc..  
* **Dynamic Content Evaluation:** A key feature of this module is the get\_evaluated\_val method in the res.users model. This utility function allows for the evaluation of dynamic expressions within HTML fields, enabling highly flexible and data-driven report content.

#### **Extension Modules**

The core module is extended by several other modules, each targeting a specific Odoo application:

* **much\_qweb\_updater\_account:** This module integrates with the Odoo Accounting application. It adds new fields to the account.move model for things like an "Order Title" and a "Description before Table," which can be printed on invoices and credit notes. It also provides its own settings page to configure accounting-specific report options.  
* **much\_qweb\_updater\_inventory:** This module extends the functionality to the Inventory application. It customizes the delivery slip report to include additional information like the country of origin, HS codes, and product weights. It also adds new fields to the stock.picking model for a "Delivery Title" and a pre-table description.  
* **much\_qweb\_updater\_purchase:** For the Purchasing application, this module customizes the Request for Quotation (RFQ) and Purchase Order reports. It adds fields for an "Order Title" and "Description before Table" to the purchase.order model and provides settings for purchase-related reports.  
* **much\_qweb\_updater\_purchase\_requisitions:** This module enhances the Purchase Requisition functionality, specifically for blanket orders. It allows for the addition of an "Order Title" and a description to purchase agreement reports.  
* **much\_qweb\_updater\_sale:** This module focuses on the Sales application. It adds custom fields to sale.order and sale.order.template for an "Order Title" and a description, which are then printed on quotations and sales orders. It also provides a dedicated settings page for sales-related report customizations.  
* **Integration Modules (much\_qweb\_updater\_account\_inventory & much\_qweb\_updater\_delivery\_inventory):** These are bridge modules that ensure seamless integration between the other modules. For example, much\_qweb\_updater\_account\_inventory adds inventory-related information, such as HS codes and country of origin, to accounting documents like invoices.

### **Development Guidelines**

When extending the functionality of this module suite, please adhere to the following principles:

* **Modularity:** If you are adding a feature that is specific to a single Odoo application (e.g., a new field on the CRM opportunity form), it should be implemented in a new extension module (e.g., much\_qweb\_updater\_crm). Core functionalities that can be used across multiple applications should be added to the base much\_qweb\_updater module.  
* **Configuration over Code:** Whenever possible, make new features configurable through the settings panel. This empowers users to customize their reports without needing to modify the code.  
* **Use Existing Mechanisms:** Leverage the existing architecture, such as the get\_evaluated\_val method for dynamic content and the centralized settings pages, to ensure consistency and maintainability.  
* **Translations:** Remember to include translations for any new user-facing strings, especially for German.  
* **Code Style:** The project uses black for code formatting and flake8 for linting. Please ensure your contributions adhere to these standards by using the provided pre-commit hooks.

## **Tests**

Currently, there are no automated tests for this module. Manual testing should be performed after any changes to ensure that the reports are generated correctly and that all configurations are applied as expected.