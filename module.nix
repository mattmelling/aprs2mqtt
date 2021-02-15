{ lib, pkgs, config, ... }:
let
  cfg = config.services.aprs2mqtt;
  settingsFormat = pkgs.formats.yaml {};
  consumerOpts = { name, ... }: with lib; {
    options = {
      filter = mkOption {
        type = types.str;
        description = "User defined filter";
        example = "t/m";
      };
      topic = mkOption {
        type = types.str;
        description = "MQTT topic";
        example = "aprs/message";
      };
    };
  };
  configFile = settingsFormat.generate "aprs2mqtt-config.yml" cfg;
in
{
  options.services.aprs2mqtt = with lib; {
    enable = mkEnableOption "aprs2mqtt";
    aprs = {
      host = mkOption {
        type = types.str;
        description = "APRS-IS host";
        default = "rotate.aprs2.net";
      };
      port = mkOption {
        type = types.int;
        description = "APRS-IS port number";
        default = 14580;
      };
      login = mkOption {
        type = types.str;
        description = "APRS-IS login";
      };
    };
    mqtt = {
      host = mkOption {
        type = types.str;
        description = "MQTT hostname";
        default = "localhost";
      };
      port = mkOption {
        type = types.int;
        description = "MQTT port";
        default = 1883;
      };
      user = mkOption {
        type = types.str;
        description = "MQTT username";
      };
      pass = mkOption {
        type = types.str;
        description = "MQTT password";
      };
    };
    consumers = mkOption {
      default = [ ];
      type = with types; listOf (submodule consumerOpts);
      example = [
        { filter = "t/m"; topic = "aprs/message"; }
      ];
    };
  };
  config = lib.mkIf cfg.enable {
    systemd.services.aprs2mqtt = {
      description = "aprs2mqtt";
      enable = true;
      wantedBy = [ "multi-user.target" ];
      after = [ "network.target" ];
      serviceConfig = {
        ExecStart = "${pkgs.aprs2mqtt}/bin/aprs2mqtt ${configFile}";
      };
    };
  };
}
