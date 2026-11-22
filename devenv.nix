{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  env.GREET = "Sync Music Assistant Files devenv environment";

  packages = with pkgs; [ ];
  cachix.pull = [ "nix-linter" ];

  languages.python = {
    enable = true;

    venv.enable = true;
    uv = {
      enable = true;
      sync.enable = true;
    };
  };

  enterShell = ''
    git --version
    python --version
    uv --version
  '';

}
