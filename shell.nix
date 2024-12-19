{
  system,
  inputs,
  pkgs ? import <nixpkgs> {},
}:
pkgs.mkShellNoCC {
  buildInputs = let
  in [
    pkgs.nodejs
  ];
  shellHook = ''
    ${inputs.self.checks.${system}.pre-commit-check.shellHook}
    echo 👋
  '';
}
