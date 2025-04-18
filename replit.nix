{pkgs}: {
  deps = [
    pkgs.streamlit
    pkgs.python312Packages.pyngrok
    pkgs.unzipNLS
    pkgs.wget
    pkgs.lsof
  ];
}
