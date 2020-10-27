with import <nixpkgs> {};
stdenv.mkDerivation rec {
  name = "env";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = with pkgs.python37Packages; [
    paho-mqtt
    requests
    setuptools
  ];
  MQTT_HOST = "heron.home";
  MQTT_PORT = 1883;
  MQTT_USER = "aprs";
  MQTT_PASSWORD = builtins.extraBuiltins.pass "home/mqtt/aprs";
  MQTT_TOPIC = "aprs/messages";
  APRSFI_KEY = builtins.extraBuiltins.pass "www/aprs.fi/api";
  APRS_CALLSIGNS = "M7AQT-5,M7AQT-9,M7AQT-10";
  LOCK_LOCATION = "/tmp";
}
