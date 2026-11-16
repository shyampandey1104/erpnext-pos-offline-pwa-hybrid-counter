import unittest
from pos_pwa.engine import OfflinePWAPOSEngine, POSLineItem

class TestOfflinePWAPOS(unittest.TestCase):
    def test_barcode_lookup_and_offline_invoice(self):
        engine = OfflinePWAPOSEngine()
        item = POSLineItem(
            item_code="SHIRT-COTTON-01",
            barcode="8901030998811",
            item_name="Men Slim Fit Cotton Shirt",
            unit_price=1200.0,
            quantity=1.0,
            tax_rate_pct=12.0
        )
        engine.register_catalog_item(item)

        scanned = engine.lookup_barcode("8901030998811")
        self.assertIsNotNone(scanned)
        self.assertEqual(scanned.item_code, "SHIRT-COTTON-01")

        inv = engine.create_offline_invoice(
            offline_id="OFF-2026-901",
            customer_id="WALK-IN-CUSTOMER",
            cart_items=[scanned],
            payment_mode="CASH",
            timestamp_utc="2026-11-16T10:00:00Z"
        )
        self.assertEqual(inv.subtotal, 1200.0)
        self.assertEqual(inv.tax_amount, 144.0) # 12% of 1200
        self.assertEqual(inv.grand_total, 1344.0)

        sync = engine.sync_offline_batch_to_erpnext([inv])
        self.assertEqual(sync.successfully_synced_count, 1)
        self.assertEqual(sync.total_sales_value_synced, 1344.0)
        self.assertTrue(inv.is_synced)

if __name__ == "__main__":
    unittest.main()
