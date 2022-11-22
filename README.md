# vyper-select
A tool to quickly switch between Vyper compiler versions. Motivated by [solc-select](https://github.com/crytic/solc-select) and [vvm](https://github.com/vyperlang/vvm). 


`vyper-select` is written simply to satisfy the needs of my own research project, which require compiling Vyper contracts with different versions of the compiler. It is not intended to be a full-featured Vyper version manager, but rather a simple tool to quickly switch between versions of the compiler.



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
$ vyper-select use 0.4.24
Switched global version to 0.4.24
$ vyper --version
solc, the solidity compiler commandline interface
Version: 0.4.24+commit.e67f0147.Linux.g++
```

Use `VYPER_VERSION` environment variable to override the global version:
```
$ vyper --version
solc, the solidity compiler commandline interface
Version: 0.4.24+commit.e67f0147.Linux.g++
$ VYPER_VERSION=0.5.2 vyper --version
solc, the solidity compiler commandline interface
Version: 0.5.2+commit.1df8f40c.Linux.g++
```

You can list all available versions with `vyper-select install`:
```
$ vyper-select install
Available versions to install:
0.3.6
0.4.0
...
0.8.0
0.8.1
```

And install the one you need with `vyper-select install <version>`:
```
$ vyper-select install 0.8.1
Installing '0.8.1'...
Version '0.8.1' installed.
```

Display the currently installed versions:
```
$ vyper-select versions
0.8.0
0.4.2 (current, set by /Users/artur/.solc-select/global-version)
```

## Getting Help



## FAQ

### vyper-version not changing after running `vyper-select use [version]` or setting `VYPER_VERSION`

Uninstall other installations of solc on your machine. `solc-select` re-installs solc binaries for your operating system and acts as a wrapper for solc. With duplicate solc installations, this may result in your `solc` version not being up to date.

### "Unsupported Platform" on Windows 

vyper-select is currently made only to satisfy my research needs. And Windows Support can be added if there is a need for it. 


```bash 
pip install solc-select==1.0.0b1
```

Alternatively, for the most up-to-date version, clone this repository and run 
```bash 
pip install . --user
```





## License

`vyper-select` is licensed and distributed under the [AGPLv3](LICENSE) license. Contact us if you’re looking for an exception to the terms.