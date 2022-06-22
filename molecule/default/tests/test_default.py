def test_default_files(host):
    f = host.file("/opt/brew-3.5.2/bin/brew")
    assert f.is_file

    c = host.run("/opt/brew-3.5.2/bin/brew --version")
    assert "(shallow or no git repository)" in c.stdout
