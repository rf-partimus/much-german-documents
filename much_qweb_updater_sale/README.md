# much. Qweb Updater Sale DIN5008

**Table of Contents**

- Features & Limitations
- Configuration
- Usage
- Issues & Bugs
- Development
- Tests
- Dependencies

## Features
 
- To extend the report template `report_delivery_document` of Quotation/Order

## Configuration

- The module doesn't require any configuration

## Usage

1. Print the Quotation/Order Report

## Dependencies

### Odoo modules dependencies

| Module                | Why used?                           | Side effects    |
| --------------------- | ----------------------------------- | --------------- |
| sale_management       | To print the Quotation/Order report | No Side effects |
| much_qweb_updater | To apply the report layout          | No Side effects |
| l10n_din5008_sale     | To access method                    | No Side effects |

### Python library dependencies

The module doesn't require any external Python library

## Limitations, Issues & Bugs

The module doesn't require any Limitations, Issues & Bugs

## Development

1. extend the `report_saleorder_document` reports
2. Added new fields `*` on **Setting**

## Tests

### Running Tests

To run all tests for this module:

```bash
odoo-bin -d <database> -i much_qweb_updater_sale --test-enable --test-tags much_qweb_updater_sale --stop-after-init
```

To run specific feature tests:

```bash
# Run only sale_order tests
odoo-bin -d <database> --test-tags sale_order --stop-after-init

# Run only sale_order_template tests
odoo-bin -d <database> --test-tags sale_order_template --stop-after-init

# Run only res_company tests
odoo-bin -d <database> --test-tags res_company --stop-after-init

# Run only res_config_settings tests
odoo-bin -d <database> --test-tags res_config_settings --stop-after-init
```

### Test Tags

| Tag | Description |
|-----|-------------|
| `much_unit` | All unit tests for much modules |
| `much_qweb_updater_sale` | Tests specific to this module |
| `sale_order` | Tests for quotation/order customization |
| `sale_order_template` | Tests for sale order template fields |
| `res_company` | Tests for sales print settings |
| `res_config_settings` | Tests for sales settings interface |

### Test Coverage

The module includes tests for:

- **sale.order**: Report header text (state-dependent), order title, DIN5008 template data, DATEV identifier, vendor/customer refs, incoterm, template integration
- **sale.order.template**: Custom fields propagation to orders, translation support
- **res.company**: Salesperson print settings, DATEV identifier, taxes on line, quotation/order descriptions
- **res.config.settings**: Related field synchronization with company settings
