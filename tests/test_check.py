"""Tests for scripts/check.py: shared contract schema and example fixtures."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location("backend_core_check", ROOT / "scripts" / "check.py")
assert _SPEC is not None and _SPEC.loader is not None
check = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(check)


class BackendCoreCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.root = Path(self._temp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.schema_path = self.root / check.PLATFORM_SCHEMA

    def tearDown(self) -> None:
        self._temp.cleanup()

    def load_schema(self) -> dict:
        return json.loads(self.schema_path.read_text(encoding="utf-8"))

    def test_repository_passes(self) -> None:
        self.assertEqual(check.validate(ROOT), [])

    def test_each_invalid_example_is_rejected_for_a_reason(self) -> None:
        schema = self.load_schema()
        for path in sorted((ROOT / "contracts/examples/invalid").glob("*.json")):
            with self.subTest(example=path.name):
                document = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(check.validate_schema(document, schema, schema))

    def test_unsupported_keyword_is_reported(self) -> None:
        schema = self.load_schema()
        schema["properties"]["status"] = {"oneOf": [{"const": "scaffolded"}]}
        self.schema_path.write_text(json.dumps(schema), encoding="utf-8")
        errors = check.validate(self.root)
        self.assertTrue(any("$.properties.status.oneOf is not supported" in error for error in errors), errors)

    def test_invalid_pattern_is_reported(self) -> None:
        schema = self.load_schema()
        schema["properties"]["api_version"]["pattern"] = "("
        self.schema_path.write_text(json.dumps(schema), encoding="utf-8")
        errors = check.validate(self.root)
        self.assertTrue(any("pattern is not a valid regular expression" in error for error in errors), errors)

    def test_loosened_schema_fails_invalid_fixture(self) -> None:
        schema = self.load_schema()
        schema["additionalProperties"] = True
        self.schema_path.write_text(json.dumps(schema), encoding="utf-8")
        errors = check.validate(self.root)
        self.assertIn("contracts/examples/invalid/extra-top-level-key.json is accepted but must be rejected", errors)

    def test_valid_example_must_pass(self) -> None:
        example = self.root / "contracts/examples/valid/scaffold-new-boundary.json"
        document = json.loads(example.read_text(encoding="utf-8"))
        document["status"] = "unknown"
        example.write_text(json.dumps(document), encoding="utf-8")
        errors = check.validate(self.root)
        self.assertTrue(any("scaffold-new-boundary.json: $.status must be one of" in error for error in errors), errors)

    def test_missing_baseline_file_is_reported(self) -> None:
        (self.root / "LICENSE").unlink()
        self.assertIn("LICENSE is missing or empty", check.validate(self.root))

    def test_main_exit_codes(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(check.main([str(self.root)]), 0)
            (self.root / "README.md").write_text("", encoding="utf-8")
            self.assertEqual(check.main([str(self.root)]), 1)
        self.assertIn("FAIL: README.md is missing or empty", output.getvalue())


if __name__ == "__main__":
    unittest.main()
