# Much OfD - Qweb Updater

**Table of Contents**

- Features & Limitations
- Configuration
- Usage
- Issues & Bugs
- Development
- Tests
- Dependencies

## Features

- update the report layout `external_layout_din5008`
- Create `report_primary_color` and `report_secondary_color` on **Company**, the default value is the standard primary and secondary color.

## Configuration
- The module doesn't require any configuration

## Usage

1. User can print the report as per the Document layout of `external_layout_din5008_much`


## Dependencies

### Odoo modules dependencies

| Module       | Why used?          | Side effects    |
| ------------ | ------------------ | --------------- |
| l10n_din5008 | For layout changes | No side effects |

### Python library dependencies

The module doesn't require any external Python library


## Limitations, Issues & Bugs

The module doesn't require any Limitations, Issues & Bugs


## Development

1. `external_layout_din5008` inherit and add layout changes.
2. Created method `get_evaluated_val` to evaluate dynamic field from a Html field.
3. Added new fields `*` on **Setting**.
4. Created method `_check_report_header_text` to check validations **Sale, Purchase, Stock and Invoice**. 
5. Create `report_primary_color` and `report_secondary_color` on **Company**, the default value is the standard primary and secondary color.

## Tests

### Running Tests

To run all tests for this module:

```bash
odoo-bin -d <database> -i much_qweb_updater --test-enable --test-tags much_qweb_updater --stop-after-init
```

To run specific feature tests:

```bash
# Run all much_unit tagged tests
odoo-bin -d <database> --test-tags much_unit --stop-after-init

# Run only res_users tests
odoo-bin -d <database> --test-tags res_users --stop-after-init

# Run only res_company tests
odoo-bin -d <database> --test-tags res_company --stop-after-init

# Run only res_partner tests
odoo-bin -d <database> --test-tags res_partner --stop-after-init

# Run only res_config_settings tests
odoo-bin -d <database> --test-tags res_config_settings --stop-after-init

# Run only ir_actions_report tests
odoo-bin -d <database> --test-tags ir_actions_report --stop-after-init

# Run only contact_widget tests
odoo-bin -d <database> --test-tags contact_widget --stop-after-init
```

### Test Tags

| Tag | Description |
|-----|-------------|
| `much_unit` | All unit tests for much modules |
| `much_qweb_updater` | Tests specific to this module |
| `res_users` | Tests for dynamic field evaluation |
| `res_company` | Tests for company configuration fields |
| `res_partner` | Tests for vendor/customer reference fields and `_get_complete_name` |
| `res_config_settings` | Tests for settings interface |
| `ir_actions_report` | Tests for PDF rendering and report header computation |
| `contact_widget` | Tests for address rendering with company/contact name separation |

### Test Coverage

The module includes comprehensive tests for:

- **res.users**: Dynamic `${...}` field evaluation via `get_evaluated_val` method, including edge cases and security tests for `safe_eval`
- **res.company**: Logo configuration (dimensions and units), footer columns, font size, print settings, boolean field toggling, related color fields, configuration persistence, and bulk update method
- **res.partner**: `vendor_ref` and `customer_ref` CRUD and search operations, `_get_complete_name` method with `report_address_format` context
- **res.config.settings**: Related field synchronization with company settings, `execute()` behavior, `edit_paper_format` action
- **ir.actions.report**: `_render_qweb_pdf` override, `_compute_report_header_text` integration, data and res_ids parameter handling
- **ir.qweb.field.contact**: `_render_address` method with field options, `record_to_html` and `value_to_html` methods, German country hide behavior, company/contact name separation
