# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "pos_pwa"
app_title = "Erpnext Pos Offline Pwa Hybrid Counter"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Pos Offline Pwa Hybrid Counter for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/pos_pwa/css/pos_pwa.bundle.css"
app_include_js = "/assets/pos_pwa/js/pos_pwa.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "pos_pwa.engine.on_document_submit",
        "on_cancel": "pos_pwa.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "pos_pwa.engine.daily_scheduled_sync"
    ]
}
