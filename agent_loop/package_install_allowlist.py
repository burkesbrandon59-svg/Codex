"""Package-install internet allowlist utilities.

This module codifies domains that are allowed as package sources.
"""

from __future__ import annotations

from urllib.parse import urlparse

ALLOWED_PACKAGE_INSTALL_DOMAINS = {
    "alpinelinux.org",
    "anaconda.com",
    "apache.org",
    "apt.llvm.org",
    "archlinux.org",
    "azure.com",
    "bitbucket.org",
    "bower.io",
    "centos.org",
    "cocoapods.org",
    "continuum.io",
    "cpan.org",
    "crates.io",
    "debian.org",
    "docker.com",
    "docker.io",
    "dot.net",
    "dotnet.microsoft.com",
    "eclipse.org",
    "fedoraproject.org",
    "gcr.io",
    "ghcr.io",
    "github.com",
    "githubusercontent.com",
    "gitlab.com",
    "golang.org",
    "google.com",
    "goproxy.io",
    "gradle.org",
    "hashicorp.com",
    "haskell.org",
    "hex.pm",
    "java.com",
    "java.net",
    "jcenter.bintray.com",
    "json-schema.org",
    "json.schemastore.org",
    "k8s.io",
    "launchpad.net",
    "maven.org",
    "mcr.microsoft.com",
    "metacpan.org",
    "microsoft.com",
    "nodejs.org",
    "npmjs.com",
    "npmjs.org",
    "nuget.org",
    "oracle.com",
    "packagecloud.io",
    "packages.microsoft.com",
    "packagist.org",
    "pkg.go.dev",
    "ppa.launchpad.net",
    "pub.dev",
    "pypa.io",
    "pypi.org",
    "pypi.python.org",
    "pythonhosted.org",
    "quay.io",
    "ruby-lang.org",
    "rubyforge.org",
    "rubygems.org",
    "rubyonrails.org",
    "rustup.rs",
    "rvm.io",
    "sourceforge.net",
    "spring.io",
    "swift.org",
    "ubuntu.com",
    "visualstudio.com",
    "yarnpkg.com",
}


def _normalize_host(value: str) -> str:
    parsed = urlparse(value if "://" in value else f"https://{value}")
    return (parsed.hostname or "").lower().strip(".")


def is_allowed_package_source(value: str) -> bool:
    host = _normalize_host(value)
    if not host:
        return False
    return any(host == allowed or host.endswith(f".{allowed}") for allowed in ALLOWED_PACKAGE_INSTALL_DOMAINS)
