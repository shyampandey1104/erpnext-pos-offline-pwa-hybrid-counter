"""Progressive Web App (PWA) Offline POS Retail Counter & Background Queue Sync Engine."""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class POSLineItem:
    item_code: str
    barcode: str
    item_name: str
    unit_price: float
    quantity: float
    tax_rate_pct: float = 18.0


@dataclass
class OfflinePOSInvoice:
    offline_id: str
    customer_id: str
    items: List[POSLineItem]
    subtotal: float
    tax_amount: float
    grand_total: float
    payment_mode: str  # CASH, UPI, CARD
    created_at_utc: str
    is_synced: bool = False


@dataclass
class SyncBatchResult:
    total_offline_invoices_received: int
    successfully_synced_count: int
    failed_sync_count: int
    total_sales_value_synced: float
    synced_erp_invoice_ids: List[str]


class OfflinePWAPOSEngine:
    """Manages offline retail cart operations, barcode lookups, and queued synchronization to ERPNext."""

    def __init__(self):
        self.item_catalog: Dict[str, POSLineItem] = {}  # barcode -> item

    def register_catalog_item(self, item: POSLineItem):
        self.item_catalog[item.barcode] = item

    def lookup_barcode(self, scanned_barcode: str) -> Optional[POSLineItem]:
        return self.item_catalog.get(scanned_barcode.strip())

    def create_offline_invoice(
        self,
        offline_id: str,
        customer_id: str,
        cart_items: List[POSLineItem],
        payment_mode: str,
        timestamp_utc: str
    ) -> OfflinePOSInvoice:
        subtotal = 0.0
        tax = 0.0

        for itm in cart_items:
            line_cost = itm.quantity * itm.unit_price
            line_tax = (line_cost * itm.tax_rate_pct) / 100.0
            subtotal += line_cost
            tax += line_tax

        subtotal = round(subtotal, 2)
        tax = round(tax, 2)
        grand = round(subtotal + tax, 2)

        return OfflinePOSInvoice(
            offline_id=offline_id,
            customer_id=customer_id,
            items=cart_items,
            subtotal=subtotal,
            tax_amount=tax,
            grand_total=grand,
            payment_mode=payment_mode,
            created_at_utc=timestamp_utc
        )

    def sync_offline_batch_to_erpnext(
        self,
        offline_invoices: List[OfflinePOSInvoice]
    ) -> SyncBatchResult:
        synced_ids = []
        sales_val = 0.0

        for inv in offline_invoices:
            inv.is_synced = True
            erp_id = f"SINV-POS-{inv.offline_id.replace('OFF-', '')}"
            synced_ids.append(erp_id)
            sales_val += inv.grand_total

        return SyncBatchResult(
            total_offline_invoices_received=len(offline_invoices),
            successfully_synced_count=len(offline_invoices),
            failed_sync_count=0,
            total_sales_value_synced=round(sales_val, 2),
            synced_erp_invoice_ids=synced_ids
        )
