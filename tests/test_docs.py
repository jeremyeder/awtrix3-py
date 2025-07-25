"""Tests to validate documentation consistency and examples."""

import ast
import re
from pathlib import Path

import pytest

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent


class TestDocumentationConsistency:
    """Test that documentation is consistent with code."""

    def test_readme_ip_addresses_consistent(self):
        """Test that all IP addresses in README are consistent."""
        readme_path = PROJECT_ROOT / "README.md"
        with open(readme_path, "r") as f:
            content = f.read()

        # Find all IP addresses
        ip_pattern = r"192\.168\.1\.(\d+)"
        ips = re.findall(ip_pattern, content)

        # Should only contain 192.168.1.128 (and variants like .129, .130 for
        # multi-device examples)
        valid_ips = {"128", "129", "130"}  # Allow for multi-device examples
        invalid_ips = set(ips) - valid_ips

        assert (
            not invalid_ips
        ), f"Found inconsistent IP addresses: 192.168.1.{invalid_ips}"

    def test_backup_guide_ip_addresses_consistent(self):
        """Test that all IP addresses in backup guide are consistent."""
        backup_guide_path = PROJECT_ROOT / "BACKUP_RESTORE_GUIDE.md"
        with open(backup_guide_path, "r") as f:
            content = f.read()

        # Find all IP addresses
        ip_pattern = r"192\.168\.1\.(\d+)"
        ips = re.findall(ip_pattern, content)

        # Should only contain 192.168.1.128 and sequential IPs for multi-device examples
        valid_ips = {"128", "129", "130"}
        invalid_ips = set(ips) - valid_ips

        assert (
            not invalid_ips
        ), f"Found inconsistent IP addresses: 192.168.1.{invalid_ips}"

    def test_notification_messages_consistent(self):
        """Test that notification examples use consistent message."""
        files_to_check = [
            PROJECT_ROOT / "README.md",
            PROJECT_ROOT / "example.py",
            PROJECT_ROOT / "awtrix3.py",
            PROJECT_ROOT / "trixctl",
        ]

        expected_message = "Let's go Mets!"

        for file_path in files_to_check:
            if file_path.exists():
                with open(file_path, "r") as f:
                    content = f.read()

                # Find notification examples
                notify_patterns = [
                    r'notify\(["\']([^"\']+)["\']',
                    r'notify ["\']([^"\']+)["\']',
                ]

                for pattern in notify_patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        # Skip config file examples and generic examples
                        if match not in ["Hello World", "test", "Hi"]:
                            # Handle apostrophe encoding issues
                            if match in ["Let", "'s go Mets!"]:
                                continue
                            assert match == expected_message, (
                                f"Found inconsistent notification message in "
                                f"{file_path}: '{match}'"
                            )

    def test_claude_md_reflects_current_api(self):
        """Test that CLAUDE.md reflects current API structure."""
        claude_md_path = PROJECT_ROOT / "CLAUDE.md"
        with open(claude_md_path, "r") as f:
            content = f.read()

        # Check that it mentions the correct number of API endpoints
        assert "7 core API endpoints" in content

        # Check that it mentions the correct CLI structure
        assert "app create|delete|list" in content
        assert "backup|restore" in content

    def test_method_documentation_matches_implementation(self):
        """Test that documented methods match actual implementation."""
        readme_path = PROJECT_ROOT / "README.md"
        with open(readme_path, "r") as f:
            readme_content = f.read()

        # Extract method documentation from README
        method_section = re.search(
            r"### Available Methods\n\n(.*?)\n\n##", readme_content, re.DOTALL
        )
        assert method_section, "Could not find Available Methods section in README"

        documented_methods = re.findall(r"- `(\w+)\([^)]*\)`", method_section.group(1))

        # Check against actual implementation
        awtrix3_path = PROJECT_ROOT / "awtrix3.py"
        with open(awtrix3_path, "r") as f:
            code_content = f.read()

        tree = ast.parse(code_content)

        # Find Awtrix3 class methods
        actual_methods = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "Awtrix3":
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and not item.name.startswith(
                        "_"
                    ):
                        actual_methods.append(item.name)

        # Check that all documented methods exist
        for method in documented_methods:
            assert (
                method in actual_methods
            ), f"Documented method '{method}' not found in implementation"

        # Check that all public methods are documented
        for method in actual_methods:
            assert (
                method in documented_methods
            ), f"Implemented method '{method}' not documented in README"


class TestCodeExamples:
    """Test that code examples in documentation are syntactically correct."""

    def test_readme_python_examples_syntax(self):
        """Test that Python code examples in README are syntactically correct."""
        readme_path = PROJECT_ROOT / "README.md"
        with open(readme_path, "r") as f:
            content = f.read()

        # Extract Python code blocks
        python_blocks = re.findall(r"```python\n(.*?)\n```", content, re.DOTALL)

        for i, block in enumerate(python_blocks):
            try:
                ast.parse(block)
            except SyntaxError as e:
                pytest.fail(
                    f"Syntax error in README Python example {i+1}: {e}\nCode:\n{block}"
                )

    def test_backup_guide_python_examples_syntax(self):
        """Test Python examples in backup guide are syntactically correct."""
        backup_guide_path = PROJECT_ROOT / "BACKUP_RESTORE_GUIDE.md"
        with open(backup_guide_path, "r") as f:
            content = f.read()

        # Extract Python code blocks
        python_blocks = re.findall(r"```python\n(.*?)\n```", content, re.DOTALL)

        for i, block in enumerate(python_blocks):
            try:
                # Skip incomplete code blocks that are meant as examples
                if "..." in block or "# ..." in block:
                    continue
                ast.parse(block)
            except SyntaxError as e:
                pytest.fail(
                    f"Syntax error in backup guide Python example {i+1}: {e}\n"
                    f"Code:\n{block}"
                )

    def test_example_py_runs_without_syntax_errors(self):
        """Test that example.py has valid syntax."""
        example_path = PROJECT_ROOT / "example.py"

        with open(example_path, "r") as f:
            content = f.read()

        try:
            ast.parse(content)
        except SyntaxError as e:
            pytest.fail(f"Syntax error in example.py: {e}")


class TestCLIDocumentation:
    """Test CLI command documentation consistency."""

    def test_cli_commands_in_readme_match_implementation(self):
        """Test that CLI commands in README match actual implementation."""
        readme_path = PROJECT_ROOT / "README.md"
        with open(readme_path, "r") as f:
            readme_content = f.read()

        # Extract trixctl commands from README
        trixctl_commands = re.findall(r"trixctl ([a-z]+)", readme_content)

        # Get unique commands
        documented_commands = set(trixctl_commands)

        # Check against actual CLI implementation
        expected_commands = {
            "notify",
            "stats",
            "power",
            "app",
            "sound",
            "backup",
            "restore",
        }

        # Remove --generate-config as it's an option, not a command
        documented_commands.discard("--generate-config")

        assert documented_commands.issubset(expected_commands), (
            f"Documented commands not in implementation: "
            f"{documented_commands - expected_commands}"
        )

        # Check that all major commands are documented
        major_commands = {"notify", "stats", "power", "app", "sound"}
        missing_docs = major_commands - documented_commands
        assert (
            not missing_docs
        ), f"Major commands missing from documentation: {missing_docs}"

    def test_app_subcommands_documented(self):
        """Test that app subcommands are properly documented."""
        readme_path = PROJECT_ROOT / "README.md"
        with open(readme_path, "r") as f:
            content = f.read()

        # Check for app subcommands
        assert "app create" in content, "app create subcommand not documented"
        assert "app delete" in content, "app delete subcommand not documented"
        assert "app list" in content, "app list subcommand not documented"

    def test_bash_completion_reflects_current_commands(self):
        """Test that bash completion script includes current commands."""
        completion_path = PROJECT_ROOT / "trixctl-completion.bash"

        if completion_path.exists():
            with open(completion_path, "r") as f:
                content = f.read()

            # Check for main commands
            expected_commands = [
                "notify",
                "stats",
                "power",
                "app",
                "sound",
                "backup",
                "restore",
            ]
            for command in expected_commands:
                assert (
                    command in content
                ), f"Command '{command}' missing from bash completion"


class TestVersionConsistency:
    """Test version consistency across files."""

    def test_version_in_awtrix3_matches_pyproject(self):
        """Test that version in awtrix3.py matches pyproject.toml."""
        # Get version from awtrix3.py
        awtrix3_path = PROJECT_ROOT / "awtrix3.py"
        with open(awtrix3_path, "r") as f:
            content = f.read()

        version_match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
        assert version_match, "Could not find __version__ in awtrix3.py"
        awtrix3_version = version_match.group(1)

        # Get version from pyproject.toml
        pyproject_path = PROJECT_ROOT / "pyproject.toml"
        with open(pyproject_path, "r") as f:
            content = f.read()

        version_match = re.search(r'version = ["\']([^"\']+)["\']', content)
        assert version_match, "Could not find version in pyproject.toml"
        pyproject_version = version_match.group(1)

        assert awtrix3_version == pyproject_version, (
            f"Version mismatch: awtrix3.py={awtrix3_version}, "
            f"pyproject.toml={pyproject_version}"
        )


class TestLinkValidation:
    """Test that links and references are valid."""

    def test_github_urls_consistent(self):
        """Test that GitHub URLs are consistent across documentation."""
        files_to_check = [
            PROJECT_ROOT / "README.md",
            PROJECT_ROOT / "pyproject.toml",
            PROJECT_ROOT / "BACKUP_RESTORE_GUIDE.md",
        ]

        expected_repo = "jeremyeder/awtrix3-py"

        for file_path in files_to_check:
            if file_path.exists():
                with open(file_path, "r") as f:
                    content = f.read()

                # Find GitHub URLs
                github_urls = re.findall(r"github\.com/([^/]+/[^/\)\s]+)", content)

                for url in github_urls:
                    # Remove any trailing punctuation or whitespace
                    clean_url = re.sub(r"[^\w/-].*$", "", url)
                    # Allow references to the original Awtrix3 project
                    if clean_url in ["Blueforcer/awtrix3", "blueforcer/AWTRIX3"]:
                        continue
                    assert clean_url == expected_repo, (
                        f"Inconsistent GitHub URL in {file_path}: {clean_url} "
                        f"(expected {expected_repo})"
                    )
