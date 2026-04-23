# -*- coding: utf-8 -*-
"""
Integration tests for invoice portal page rendering with contact widget.

Verifies that the portal invoice page renders correctly when
invoice_user_id (res.users) is passed to the base.contact widget.
"""

from odoo.fields import Command
from odoo.tests import HttpCase, new_test_user, tagged


@tagged(
    "much_unit",
    "much_qweb_updater_account",
    "portal_invoice",
    "post_install",
    "-at_install",
)
class TestPortalInvoiceContactWidget(HttpCase):
    """
    Integration test hitting the actual portal invoice URL.

    The standard account.portal_invoice_page template renders:
        <div t-field="invoice.invoice_user_id"
             t-options='{"widget": "contact", "fields": ["city", "phone"]}'/>

    This passes a res.users record to the contact widget, which previously
    caused an AttributeError on _get_complete_name.
    """

    @classmethod
    def setUpClass(cls):
        """Set up portal user, salesperson, and posted invoices."""
        super().setUpClass()

        cls.portal_user = new_test_user(
            cls.env,
            login="portal_user_invoice_test",
            groups="base.group_portal",
            name="Portal Customer",
        )
        cls.portal_partner = cls.portal_user.partner_id

        cls.salesperson = new_test_user(
            cls.env,
            login="salesperson_invoice_test",
            groups="base.group_user",
            name="Sales Person",
        )
        cls.salesperson.partner_id.write(
            {
                "street": "Vertriebsweg 42",
                "city": "Frankfurt",
                "zip": "60311",
                "country_id": cls.env.ref("base.de").id,
                "phone": "+49 69 1234567",
            }
        )

        cls.invoice_with_salesperson = cls.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": cls.portal_partner.id,
                "invoice_user_id": cls.salesperson.id,
                "invoice_line_ids": [
                    Command.create({"name": "Test Line", "price_unit": 100.0})
                ],
            }
        )
        cls.invoice_with_salesperson.action_post()

        cls.invoice_no_salesperson = cls.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": cls.portal_partner.id,
                "invoice_user_id": False,
                "invoice_line_ids": [
                    Command.create({"name": "Test Line", "price_unit": 50.0})
                ],
            }
        )
        cls.invoice_no_salesperson.action_post()

    def test_portal_invoice_with_salesperson_renders(self):
        """Test that the portal invoice page loads when a salesperson is set.

        Previously crashed with:
            AttributeError: 'res.users' object has no attribute '_get_complete_name'
        """
        invoice = self.invoice_with_salesperson
        portal_url = invoice.get_portal_url()

        self.authenticate(self.portal_user.login, self.portal_user.login)
        response = self.url_open(portal_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Sales Person", response.text)
        self.assertIn("Frankfurt", response.text)

    def test_portal_invoice_without_salesperson_renders(self):
        """Test that the portal invoice page loads when no salesperson is set."""
        invoice = self.invoice_no_salesperson
        portal_url = invoice.get_portal_url()

        self.authenticate(self.portal_user.login, self.portal_user.login)
        response = self.url_open(portal_url)

        self.assertEqual(response.status_code, 200)

    def test_portal_invoice_with_access_token_renders(self):
        """Test portal invoice page via public access token with salesperson."""
        invoice = self.invoice_with_salesperson
        invoice._portal_ensure_token()
        url = f"/my/invoices/{invoice.id}?access_token={invoice.access_token}"

        # we clear any existing session to test true public access
        self.authenticate(None, None)
        response = self.url_open(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Sales Person", response.text)
