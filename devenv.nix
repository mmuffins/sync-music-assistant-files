{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  env.GREET = "Sync Music Assistant Files devenv environment";

  packages = [ pkgs.git ];
  cachix.pull = [ "nix-linter" ];

  languages.python = {
    enable = true;
    venv.enable = false;
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
