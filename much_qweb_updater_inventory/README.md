# much. Qweb Updater Inventory DIN5008

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

1. Print the Delivery Slip Report.

## Dependencies

### Odoo modules dependencies

| Module                | Why used?                                        | Side effects    |
| --------------------- | ------------------------------------------------ | --------------- |
| stock_delivery        | To use fields and print the delivery slip report | No Side effects |
| much_qweb_updater | To apply the report layout                       | No Side effects |

### Python library dependencies

The module doesn't require any external Python library

## Limitations, Issues & Bugs

The module doesn't require any Limitations, Issues & Bugs

## Development

1. extend the `report_delivery_document`,`stock_report_delivery_has_serial_move_line` and `stock_report_delivery_aggregated_move_lines` reports
2. Added new fields `*` on **Setting**

## Tests

### Running Tests

To run all tests for this module:

```bash
odoo-bin -d <database> -i much_qweb_updater_inventory --test-enable --test-tags much_qweb_updater_inventory --stop-after-init
```

To run specific feature tests:

```bash
# Run only stock_picking tests
odoo-bin -d <database> --test-tags stock_picking --stop-after-init

# Run only res_company tests
odoo-bin -d <database> --test-tags res_company --stop-after-init

# Run only res_config_settings tests
odoo-bin -d <database> --test-tags res_config_settings --stop-after-init
```

### Test Tags

| Tag | Description |
|-----|-------------|
| `much_unit` | All unit tests for much modules |
| `much_qweb_updater_inventory` | Tests specific to this module |
| `stock_picking` | Tests for delivery document customization |
| `res_company` | Tests for inventory print settings |
| `res_config_settings` | Tests for inventory settings interface |

### Test Coverage

The module includes tests for:

- **stock.picking**: Report header text, order title, date formatting, DIN5008 template data, sale order reference integration
- **res.company**: COO/HS code print settings, weight printing, delivery description
- **res.config.settings**: Related field synchronization with company settings
