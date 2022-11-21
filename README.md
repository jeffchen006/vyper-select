# vyper-select
A tool to quickly switch between Vyper compiler versions. Motivated by [solc-select](https://github.com/crytic/solc-select) and [vvm](https://github.com/vyperlang/vvm). 

The tool is split into two CLI utilities:
- `vyper-select`: manages installing and setting different `vyper` compiler versions
- `vyper`: wrapper around `vyper` which picks the right version according to what was set via `vyper-select`

The `vyper` binaries are downloaded from https://pypi.org/project/vyper/ which contains
official artifacts for many historical and modern `vyper` versions.

The downloaded binaries are stored in `~/.vyper-select/artifacts/`.

## Quickstart

```
pip3 install vyper-select
```

## Usage

The global version of `vyper` can be set with the `vyper-select use <version>` command:
```
$ vyper --version
solc, the solidity compiler commandline interface
Version: 0.5.2+commit.1df8f40c.Linux.g++
$ solc-select use 0.4.24
Switched global version to 0.4.24
$ solc --version
solc, the solidity compiler commandline interface
Version: 0.4.24+commit.e67f0147.Linux.g++
```

Use `SOLC_VERSION` environment variable to override the global version:
```
$ solc --version
solc, the solidity compiler commandline interface
Version: 0.4.24+commit.e67f0147.Linux.g++
$ SOLC_VERSION=0.5.2 solc --version
solc, the solidity compiler commandline interface
Version: 0.5.2+commit.1df8f40c.Linux.g++
```

You can list all available versions with `solc-select install`:
```
$ solc-select install
Available versions to install:
0.3.6
0.4.0
...
0.8.0
0.8.1
```

And install the one you need with `solc-select install <version>`:
```
$ solc-select install 0.8.1
Installing '0.8.1'...
Version '0.8.1' installed.
```

Display the currently installed versions:
```
$ solc-select versions
0.8.0
0.4.2 (current, set by /Users/artur/.solc-select/global-version)
```

## Getting Help

Feel free to stop by our [Slack channel](https://empirehacking.slack.com/) for help on using or extending `solc-select`.

## FAQ

### solc-version not changing after running `solc-select use [version]` or setting `SOLC_VERSION`

Uninstall other installations of solc on your machine. `solc-select` re-installs solc binaries for your operating system and acts as a wrapper for solc. With duplicate solc installations, this may result in your `solc` version not being up to date.

### "Unsupported Platform" on Windows 

The solc-select version that supports Windows is currently in beta. Uninstall `solc-select` through `pip3 uninstall solc-select` and run 

```bash 
pip install solc-select==1.0.0b1
```

Alternatively, for the most up-to-date version, clone this repository and run 
```bash 
pip install . --user
```

## Known Issues

### `SSL: CERTIFICATE_VERIFY_FAILED` on running `solc-select` commands [investigation ongoing]

**OS X**
```bash
pip3 install certifi
/Applications/Python\ 3.8/Install\ Certificates.command
```

Python distributions on OS X has no certificates and cannot validate SSL connections, a breaking change introduced in Python 3.6. See [StackOverflow](https://stackoverflow.com/a/42334357) post for additional details.

### `Connection refused` [investigation ongoing]

```bash
pip3 uninstall solc-select 
pip3 install solc-select==0.2.0
solc-select install 
```

Try downgrading to `solc-select version 0.2.0`. 

Our `0.2.1` version of `solc-select` pulls older Linux binaries from [crytic/solc](https://github.com/crytic/solc) which seems to have introduced unexpected behavior in certain instances.

### `solc-select` version changes, but `solc --version does not match`

Users seem to be experiencing situations in which the following command is successful: 
```
solc-select use <version> 
```
However, when running the following command, it points to an older version of Solidity.
```
solc --version
```

`solc-select` is intended to work with custom binaries. This means that Solidity installed through other means (i.e: `brew install solidity`) will _not_ work!. 

Uninstall other versions Solidity from your computer.

## License

`solc-select` is licensed and distributed under the [AGPLv3](LICENSE) license. [Contact us](zhiychen@cs.toronto.edu) if you’re looking for an exception to the terms.