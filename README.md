# vyper-select
A tool to quickly switch between Vyper compiler versions. Motivated by [solc-select](https://github.com/crytic/solc-select) and [vvm](https://github.com/vyperlang/vvm). 


`vyper-select` is written simply to satisfy the needs of my own research project, which require compiling Vyper contracts with different versions of the compiler. It is not intended to be a full-featured Vyper version manager, but rather a simple tool to quickly switch between versions of the compiler.



The tool is split into two CLI utilities:
- `vyper-select`: manages installing and setting different `vyper` compiler versions
- `vyper`: wrapper around `vyper` which picks the right version according to what was set via `vyper-select`

The `vyper` binaries are downloaded from https://github.com/vyperlang/vyper/releases/ which contains official artifacts for many historical and modern `vyper` versions.

The downloaded binaries are stored in `~/.vyper-select/artifacts/`.

## Quickstart

```
pip3 install .
```

## Usage

The global version of `vyper` can be set with the `vyper-select use <version>` command:
```
$ vyper --version
0.2.2+commit.337c2ef
$ vyper-select use 0.3.6
Switched global version to 0.3.6
$ vyper --version
0.3.6+commit.4a2124d0
```

Use `VYPER_VERSION` environment variable to override the global version:
```
$ vyper --version
0.2.2+commit.337c2ef
$ VYPER_VERSION=0.3.6 vyper --version
0.3.6+commit.4a2124d0
```

You can list all available versions with `vyper-select install`:
```
$ vyper-select install
Available versions to install:
0.1.0-beta.16
0.1.0-beta.17
...
0.3.6
0.3.7
```

And install the one you need with `vyper-select install <version>`:
```
$ vyper-select install 0.3.6
Installing '0.3.6'...
Version '0.3.6' installed.
```

Display the currently installed versions:
```
$ vyper-select versions
0.3.7
0.3.6 (current, set by /home/zhiychen/.vyper-select/global-version)
0.3.4
0.3.3
```

## Getting Help



## FAQ

### vyper-version not changing after running `vyper-select use [version]` or setting `VYPER_VERSION`

Uninstall other installations of vyper on your machine. `vyper-select` re-installs vyper binaries for your operating system and acts as a wrapper for vyper. With duplicate vyper installations, this may result in your `vyper` version not being up to date.

### "Unsupported Platform" on Windows 

vyper-select is currently made only to satisfy my research needs. And Windows Support can be added if there is a need for it. 


```bash 
pip install .
```




## License

`vyper-select` is licensed and distributed under the [AGPLv3](LICENSE) license. Contact us if you’re looking for an exception to the terms.