{ pkgs ? import <nixpkgs> {} }:
with pkgs;
let
  aprslib = pkgs.callPackage ./aprslib.nix { };
in stdenv.mkDerivation rec {
  name = "env";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = [
    (pkgs.python38.withPackages (ps: with ps; [
      aprslib
      paho-mqtt
      plac
      pyyaml
      setuptools
    ]))
  ];
  MQTT_HOST = "heron.home";
  MQTT_PORT = 1883;
  MQTT_USER = "aprs";
  shellHook = ''
    export MQTT_PASS="$(pass home/mqtt/aprs | head -n1)"
  '';
}
