{
  description = "talculate";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        packages = {
          default = pkgs.callPackage ./package.nix { };
        };

        apps = {
          default = {
            type = "app";
            program = "${self.packages.${system}.default}/bin/talc";
          };
        };

        devShells = {
          default = pkgs.mkShell {
            packages = with pkgs; [
              black
              nixfmt-rfc-style

              gnumake
              poetry
              python3
              treefmt
            ];
            shellHook = ''
              export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
            '';
          };
        };
      }
    );
}
