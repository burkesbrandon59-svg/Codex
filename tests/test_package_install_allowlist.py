from agent_loop.package_install_allowlist import (
    ALLOWED_PACKAGE_INSTALL_DOMAINS,
    is_allowed_package_source,
)


def test_allowlist_contains_expected_domains() -> None:
    assert "pypi.org" in ALLOWED_PACKAGE_INSTALL_DOMAINS
    assert "github.com" in ALLOWED_PACKAGE_INSTALL_DOMAINS
    assert "apt.llvm.org" in ALLOWED_PACKAGE_INSTALL_DOMAINS


def test_is_allowed_package_source_accepts_exact_and_subdomain() -> None:
    assert is_allowed_package_source("https://pypi.org/simple") is True
    assert is_allowed_package_source("files.pythonhosted.org") is True
    assert is_allowed_package_source("registry.npmjs.org") is True


def test_is_allowed_package_source_rejects_unknown_domains() -> None:
    assert is_allowed_package_source("example.com") is False
    assert is_allowed_package_source("https://malicious.invalid/pkg") is False
    assert is_allowed_package_source("") is False
