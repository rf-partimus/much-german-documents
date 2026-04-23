# much. Qweb Updater Delivery Inventory DIN5008

**Table of Contents**

- Features & Limitations
- Configuration
- Usage
- Issues & Bugs
- Development
- Tests
- Dependencies

## Features

- To extend the report template `report_delivery_document` of Delivery Slip 

## Configuration

- The module doesn't require any configuration

## Usage

1. Print the "Delivery Slip" Report with HS Code and COO 

## Dependencies

### Odoo modules dependencies

| Module                           | Why used?                        | Side effects    |
| -------------------------------- | -------------------------------- | --------------- |
| much_qweb_updater_inventory  | To apply the report layout       | No Side effects |
| Delivery - Stock                 | To access the fields for report  | No Side effects |

### Python library dependencies

The module doesn't require any external Python library

## Limitations, Issues & Bugs

The module doesn't require any Limitations, Issues & Bugs

## Development

1. extend the `report_delivery_document` report and add `hs_code` and `country_of_origin` fields.