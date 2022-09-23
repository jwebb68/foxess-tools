{ pkgs ? import <nixpkgs> { } }:

# cant use poerty2nix on a fresh project,
# as I get
# ```
#$ nix-shell
#error: Missing suitable source/wheel file entry for pyparsing
#(use '--show-trace' to show detailed location information)
#```
# let
#   # pkgs2 = pkgs // {
#   #   permittedInsecurePackages = [
#   #     "python3.9-poetry-1.1.12"
#   #   ];
#   # };
#   env = pkgs.poetry2nix.mkPoetryEnv
#     {
#       projectDir = ./.;
#     };
# in
# env.env

# use poetry to manage python dependencies.
# use nix to manage the non-python deps
# ideally use nix to manage all deps..
# let
#   python = pkgs.python39Full;
#   #python = pkgs.python39;
#   ignoreVulns = x: x // { meta = (x.meta // { knownVulnerabilities = [ ]; }); };
#   poetry = (pkgs.poetry.overrideAttrs ignoreVulns).override {
#     python = python;
#   };
#   python_with_packages = python.withPackages (p: with p; [
#     #isort
#     #black
#   ]);
# in
# pkgs.mkShell {
#   # poetry in python39 has been marked with vuln CVE-2021-33503,
#   # which is prevening use.
#   # So remove this vuln, so it can be used.
#   nativeBuildInputs = [
#     python
#     poetry

#     pkgs.pkgconfig
#     pkgs.gnumake
#   ];
#   buildInputs = [
#   ];
# }

# python39 on nixos 22.04 doesn't require vulns to be ignored.
pkgs.mkShell {
  nativeBuildInputs = [
    pkgs.python3
    pkgs.poetry

    pkgs.pkgconfig
    pkgs.gnumake
  ];
  buildInputs = [
  ];
}
