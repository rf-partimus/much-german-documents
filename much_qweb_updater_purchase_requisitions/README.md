# much. Qweb Updater Purchase Requisition DIN5008

**Table of Contents**

- Features & Limitations
- Configuration
- Usage
- Issues & Bugs
- Development
- Tests
- Dependencies

## Features

- To extend the report template `report_purchaserequisition_document` of Purchase Agreements

## Configuration

- The module doesn't require any configuration

## Usage

1. Print the Purchase Agreements Report

## Dependencies

### Odoo modules dependencies

| Module                | Why used?                               | Side effects |
| --------------------- | --------------------------------------- | ------------ |
| Purchase Requisition  | To print the purchase agreements report | None         |
| much_qweb_updater | To apply the report layout              | None         |

### Python library dependencies

The module doesn't require any external Python library

## Limitations, Issues & Bugs

The module doesn't require any Limitations, Issues & Bugs

## Development

1. Added new report layout `report_purchaserequisitions_document_din5008` for **Purchase Agreements Report**
2. Added new report layout `report_purchaserequisitions_much_custom_din5008` for **Purchase Requisition**
3. Added new fields `*` on **Setting**

## Tests

### Running Tests

To run all tests for this module:

```bash
odoo-bin -d <database> -i much_qweb_updater_purchase_requisitions --test-enable --test-tags much_qweb_updater_purchase_requisitions --stop-after-init
```

To run specific feature tests:

```bash
# Run only purchase_requisition tests
odoo-bin -d <database> --test-tags purchase_requisition --stop-after-init

# Run only res_company tests
odoo-bin -d <database> --test-tags res_company --stop-after-init

# Run only res_config_settings tests
odoo-bin -d <database> --test-tags res_config_settings --stop-after-init
```

### Test Tags

| Tag | Description |
|-----|-------------|
| `much_unit` | All unit tests for much modules |
| `much_qweb_updater_purchase_requisitions` | Tests specific to this module |
| `purchase_requisition` | Tests for blanket order customization |
| `res_company` | Tests for requisition print settings |
| `res_config_settings` | Tests for requisition settings interface |

### Test Coverage

The module includes tests for:

- **purchase.requisition**: Report header text, order title, DIN5008 template data (ordering date, date end, origin), buyer information
- **res.company**: Buyer info print settings, existing RFQs printing, requisition description
- **res.config.settings**: Related field synchronization with company settings
