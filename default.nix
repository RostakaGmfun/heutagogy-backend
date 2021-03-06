{ pkgs ? import <nixpkgs> { } }:
let
  python = import ./requirements.nix { inherit pkgs; };
in python.mkDerivation {
  name = "heutagogy-1.0";

  buildInputs = [
    pkgs.python3Packages.flake8
    pkgs.python3Packages.psycopg2
  ];

  propagatedBuildInputs = [
    python.packages.Flask
    python.packages.Flask-JWT
    python.packages.Flask-Login
    python.packages.Flask-Migrate
    python.packages.Flask-RESTful
    python.packages.Flask-SQLAlchemy
    python.packages.Flask-User
  ];

  checkPhase = ''
    ./tests.py

    flake8 . --exclude=migrations
  '';

  # This sets FLASK_APP environment variable, so you don't have to.
  FLASK_APP = "heutagogy";
}
