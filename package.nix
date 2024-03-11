{pkgs, ...}:
(pkgs.buildNpmPackage {
  src = pkgs.lib.cleanSourceWith {
    src = ./.;
    name = "raphael.li";
    filter = path: type: baseNameOf path != "node_modules" && baseNameOf path != "_site";
  };
  npmBuild = "npm run build";
  extraNodeModulesArgs = {
    buildInputs = [
      # required by sharp
      pkgs.pkg-config
      pkgs.vips
      pkgs.python3
    ];
  };
})
.overrideAttrs {
  installPhase = ''
    runHook preInstall
    mv _site $out
    runHook postInstall
  '';
}
