{ pkgs ? import <nixpkgs> {} }:
let
  aprslib = pkgs.callPackage ./aprslib.nix { };
in pkgs.python38Packages.buildPythonPackage rec {
  name = "aprs2mqtt";
  src = ./.;
  propagatedBuildInputs = [
    (pkgs.python38.withPackages(ps: with ps; [
      aprslib
      paho-mqtt
      plac
      pyyaml
    ]))
  ];
}
