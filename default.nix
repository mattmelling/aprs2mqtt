with import <nixpkgs> {};
pkgs.python37Packages.buildPythonApplication rec {
  name = "aprs2mqtt";
  src = ./.;
  propagateBuildInputs = with pkgs.python37Packages; [
    paho-mqtt
    requests
  ];
}
