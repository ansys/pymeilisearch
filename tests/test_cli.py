from click.testing import CliRunner

from ansys.tools.meilisearch.cli import main

runner = CliRunner()


def test_version_command():
    # Test the 'version' command
    result = runner.invoke(main, ["version"])
    assert result.exit_code == 0
    assert "PyMeilisearch" in result.output


def test_upload_command_invalid_source(meilisearch_client):
    # Test the 'upload' command with an invalid source option
    result = runner.invoke(
        main,
        [
            "upload",
            "--template",
            "default",
            "--index",
            "test_index",
            "invalid_source",
            "location",
        ],
    )
    assert result.exit_code != 0
    assert "Invalid value for '{html|url|github}" in result.output
