{
  description = "aprs2mqtt";
  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
        overlays = [ self.overlay ];
      };
    in {
      overlay = final: prev: {
        aprs2mqtt = prev.callPackage ./default.nix { };
      };
      nixosModules.aprs2mqtt = {
        imports = [ ./module.nix ];
        nixpkgs.overlays = [
          self.overlay
        ];
      };
    };
}
