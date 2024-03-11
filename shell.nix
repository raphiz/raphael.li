{
  system,
  inputs,
  pkgs ? import <nixpkgs> {},
}:
pkgs.mkShellNoCC {
  buildInputs = let
  in [
  ];
  shellHook = ''
    ${inputs.self.checks.${system}.pre-commit-check.shellHook}
    echo 👋
  '';
}
