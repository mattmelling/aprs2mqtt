{ pkgs ? import <nixpkgs> { } }:
with pkgs.python38Packages; buildPythonPackage {
  name = "aprslib";
  src = fetchPypi {
    pname = "aprslib";
    version = "0.6.47";
    sha256 = "sha256-V10CX9vpWO5//ilhDfXP5kfLesUf4KdnCnhH1Wuxxgg=";
  };
  doCheck = false;
}
