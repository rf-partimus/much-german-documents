# much. Qweb Updater Purchase DIN5008

**Table of Contents**

- Features & Limitations
- Configuration
- Usage
- Issues & Bugs
- Development
- Tests
- Dependencies

## Features

- To extend the report template `report_purchaseorder_documentreport_purchaseorder_document` of Purchase Order
- To extend the report template `report_purchasequotation_document` of Request for Quotation

## Configuration

- The module doesn't require any configuration

## Usage

1. Print the Purchase Order Report
2. Print the Request for Quotation Report

## Dependencies

### Odoo modules dependencies

| Module                | Why used?                          | Side effects    |
| --------------------- | ---------------------------------- | --------------- |
| Purchase              | To print the Purchase Order report | No Side effects |
| much_qweb_updater | To apply the report layout         | No Side effects |
| l10n_din5008_purchase | To access method                   | No Side effects |

### Python library dependencies

The module doesn't require any external Python library

## Limitations, Issues & Bugs

The module doesn't require any Limitations, Issues & Bugs

## Development

1. extend the `report_purchasequotation_document` and `report_purchasequotation_document` report
2. Added new fields `*` on **Setting**

## Tests

### Running Tests

To run all tests for this module:

```bash
odoo-bin -d <database> -i much_qweb_updater_purchase --test-enable --test-tags much_qweb_updater_purchase --stop-after-init
```

To run specific feature tests:

```bash
# Run only purchase_order tests
odoo-bin -d <database> --test-tags purchase_order --stop-after-init

# Run only res_company tests
odoo-bin -d <database> --test-tags res_company --stop-after-init

# Run only res_config_settings tests
odoo-bin -d <database> --test-tags res_config_settings --stop-after-init
```

### Test Tags

| Tag | Description |
|-----|-------------|
| `much_unit` | All unit tests for much modules |
| `much_qweb_updater_purchase` | Tests specific to this module |
| `purchase_order` | Tests for RFQ/PO customization |
| `res_company` | Tests for purchase print settings |
| `res_config_settings` | Tests for purchase settings interface |

### Test Coverage

The module includes tests for:

- **purchase.order**: Report header text (state-dependent RFQ vs PO), order title, DIN5008 template data, buyer info, customer ref, partner ref, DATEV supplier identifier, incoterm
- **res.company**: Buyer info print settings, DATEV identifier, RFQ/PO descriptions
- **res.config.settings**: Related field synchronization with company settings
