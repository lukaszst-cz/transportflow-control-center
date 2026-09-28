import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from wsgiref.util import setup_testing_defaults

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import app


class TransportFlowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_database = app.DATABASE
        app.DATABASE = Path(self.temp_dir.name) / "transportflow-test.sqlite3"
        app.initialise_database()

    def tearDown(self):
        app.DATABASE = self.original_database
        self.temp_dir.cleanup()

    def call_api(self, path: str, query: str = ""):
        environ = {}
        setup_testing_defaults(environ)
        environ.update(PATH_INFO=path, REQUEST_METHOD="GET", QUERY_STRING=query)
        response = {}

        def start_response(status, headers):
            response["status"] = status
            response["headers"] = dict(headers)

        raw = b"".join(app.application(environ, start_response))
        response["body"] = raw
        if response["headers"].get("Content-Type", "").startswith("application/json"):
            response["json"] = json.loads(raw.decode("utf-8"))
        return response

    def test_fleet_and_drivers(self):
        data = app.dashboard()
        self.assertEqual(data["fleet"]["vehicles"], 20)
        self.assertEqual(data["fleet"]["active"], 18)
        self.assertEqual(data["drivers"]["drivers"], 26)
        self.assertGreater(data["fleet"]["monthly_lease"], 0)

    def test_driver_employment_distribution(self):
        db = app.connection()
        rows = db.execute(
            "SELECT employment_status, COUNT(*) count FROM drivers GROUP BY employment_status"
        ).fetchall()
        db.close()
        distribution = {row["employment_status"]: row["count"] for row in rows}
        self.assertEqual(distribution, {"Pracownik": 24, "Rezerwowy": 2})

    def test_margin_is_positive_and_below_one(self):
        for order in app.dashboard()["orders"]:
            margin = app.order_margin(order)
            self.assertGreater(margin, 0)
            self.assertLess(margin, 1)

    def test_required_documents_and_blocking_scenario(self):
        documents = app.dashboard()["documents"]
        types = {item["document_type"] for item in documents}
        self.assertIn("CKZ zarządzającego transportem", types)
        self.assertIn("Odczyt karty kierowcy", types)
        self.assertTrue(any(
            item["document_type"] == "Certyfikat mycia cysterny"
            and item["status"] == "Brak"
            and item["blocking_process"] == "Wyjazd"
            for item in documents
        ))

    def test_workflow_download_periods(self):
        workflow = json.loads((ROOT / "workflow.json").read_text(encoding="utf-8"))
        self.assertEqual(workflow["tachograph_download_days"], {"driver_card": 28, "vehicle_unit": 90})

    def test_workflow_fleet_distribution_matches_seed(self):
        workflow = json.loads((ROOT / "workflow.json").read_text(encoding="utf-8"))
        expected = {
            "reefer": "Chłodnia",
            "food_tanker": "Cysterna spożywcza",
            "adr_tanker": "Cysterna ADR",
            "curtainsider": "Plandeka",
        }

        db = app.connection()
        rows = db.execute(
            "SELECT vehicle_type, COUNT(*) count FROM vehicles GROUP BY vehicle_type"
        ).fetchall()
        db.close()
        actual = {row["vehicle_type"]: row["count"] for row in rows}

        self.assertEqual(sum(workflow["fleet"].values()), 20)
        for workflow_key, vehicle_type in expected.items():
            self.assertEqual(actual[vehicle_type], workflow["fleet"][workflow_key])

    def test_workflow_blocking_rules_cover_demo_document_block(self):
        workflow = json.loads((ROOT / "workflow.json").read_text(encoding="utf-8"))
        required = {
            "driver_time_invalid",
            "company_document_expired",
            "vehicle_document_expired",
            "specialist_document_missing",
            "pod_missing",
            "margin_below_floor",
        }
        self.assertTrue(required.issubset(set(workflow["blocking_rules"])))
        self.assertTrue(any(
            item["document_type"] == "Certyfikat mycia cysterny"
            and item["status"] == "Brak"
            and item["blocking_process"] == "Wyjazd"
            for item in app.dashboard()["documents"]
        ))

    def test_health_endpoint(self):
        response = self.call_api("/api/health")
        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(response["json"]["status"], "ok")
        self.assertEqual(response["json"]["service"], "transportflow-control-center")
        self.assertEqual(response["json"]["data_class"], "synthetic")

    def test_dashboard_endpoint_returns_json(self):
        response = self.call_api("/api/dashboard")
        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(response["json"]["fleet"]["vehicles"], 20)
        self.assertEqual(response["json"]["drivers"]["drivers"], 26)

    def test_orders_endpoint_returns_all_demo_orders(self):
        response = self.call_api("/api/orders")
        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(len(response["json"]), 3)
        self.assertTrue(all(item["order_code"].startswith("TF-") for item in response["json"]))

    def test_status_filter_returns_only_matching_orders(self):
        response = self.call_api("/api/orders", "status=W%20trasie")
        self.assertEqual(response["status"], "200 OK")
        self.assertGreaterEqual(len(response["json"]), 1)
        self.assertTrue(all(item["status"] == "W trasie" for item in response["json"]))

    def test_unknown_endpoint_returns_404(self):
        response = self.call_api("/api/not-existing")
        self.assertEqual(response["status"], "404 Not Found")
        self.assertEqual(response["body"], b"Not found")

    def test_demo_dataset_is_synthetic(self):
        serialised = json.dumps(app.dashboard(), ensure_ascii=False).lower()
        for forbidden in ("pesel", "@gmail.com", "@wp.pl", "@onet.pl"):
            self.assertNotIn(forbidden, serialised)

    def test_seed_is_repeatable_without_duplicates(self):
        app.initialise_database()
        data = app.dashboard()
        self.assertEqual(data["fleet"]["vehicles"], 20)
        self.assertEqual(data["drivers"]["drivers"], 26)
        self.assertEqual(len(data["orders"]), 3)


if __name__ == "__main__":
    unittest.main()
