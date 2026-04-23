# much. Qweb Updater Account DIN5008

**Table of Contents**

- Features & Limitations
- Configuration
- Usage
- Issues & Bugs
- Development
- Tests
- Dependencies

## Features

- To extend the report template `report_invoice_document` of Invoice

## Configuration

- The module doesn't require any configuration

## Usage

1. Print the Invoice Report

## Dependencies

### Odoo modules dependencies

| Module                | Why used?                                             | Side effects    |
| --------------------- | ----------------------------------------------------- | --------------- |
| Account               | To print the Invoices/Invoices without Payment report | No Side effects |
| much_qweb_updater | To apply the report layout                            | No Side effects |
| Sale                  | To access some methods                                | No Side effects |

### Python library dependencies

The module doesn't require any external Python library

## Limitations, Issues & Bugs

The module doesn't require any Limitations, Issues & Bugs

## Development

1. extend the `report_invoice_document` report.
2. Added new fields `*` on **Setting**

## Tests

### Running Tests

To run all tests for this module:

```bash
odoo-bin -d <database> -i much_qweb_updater_account --test-enable --test-tags much_qweb_updater_account --stop-after-init
```

To run specific feature tests:

```bash
# Run only account_move tests
odoo-bin -d <database> --test-tags account_move --stop-after-init

# Run only account_move_line tests
odoo-bin -d <database> --test-tags account_move_line --stop-after-init

# Run only ir_actions_report tests
odoo-bin -d <database> --test-tags ir_actions_report --stop-after-init

# Run only sale_order invoice tests
odoo-bin -d <database> --test-tags sale_order --stop-after-init

# Run only account_move_reversal tests
odoo-bin -d <database> --test-tags account_move_reversal --stop-after-init

# Run only res_company tests
odoo-bin -d <database> --test-tags res_company --stop-after-init

# Run only res_config_settings tests
odoo-bin -d <database> --test-tags res_config_settings --stop-after-init
```

### Test Tags

| Tag | Description |
|-----|-------------|
| `much_unit` | All unit tests for much modules |
| `much_qweb_updater_account` | Tests specific to this module |
| `account_move` | Tests for invoice delivery dates, header text, template data |
| `account_move_line` | Tests for invoice line delivery dates |
| `ir_actions_report` | Tests for VAT removal in report rendering |
| `sale_order` | Tests for sale order to invoice date propagation |
| `account_move_reversal` | Tests for credit note description handling |
| `res_company` | Tests for accounting print settings |
| `res_config_settings` | Tests for accounting settings interface |

### Test Coverage

The module includes tests for:

- **account.move**: Delivery date fields, date validation, report header text, print time frame, DIN5008 template data
- **account.move.line**: Delivery date synchronization with move header
- **ir.actions.report**: VAT element removal via XPath processing
- **sale.order**: Invoice delivery date propagation, narration blocking
- **account.move.reversal**: Credit note description preparation
- **res.company**: Accounting print settings, description fields
- **res.config.settings**: Related field synchronization
