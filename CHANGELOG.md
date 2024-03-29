# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Fixed
### Changed
### Removed

## [0.6.3] - 2023-10-26
### Fixed
- Getting around 403 due to reuqests signature, replacing requests with cloudscraper 

## [0.6.2] - 2023-09-13
### Fixed
- lxml parser error on raspberry, dropping lxml dependency

## [0.6.0] - 2023-09-12
### Added
- Ochsner Sport Parser 

### Fixed
- Deal with None on price updates when no price is retrieved

## [0.5.0] - 2023-04-09
### Added
- Decathlon parser

## [0.4.1] - 2023-04-08
### Added
- More information on the readme

### Fixed
- Channel id parameter

## [0.4.0] - 2023-04-08
### Added
- Discord bot commands to control the prices that are being tracked
- Persistent storage for the products that are being tracked

### Changed
- The program only interfaces with discord

## [0.3.0] - 2022-12-16
### Added
- Flexible notification pattern
- Asynchronous notifiers

## [0.2.0] - 2022-11-29
### Added
- Users can now call script and pass arguments
- Users can pass a list of urls as parameters without respective parsers
- Users can pass a json file of parsers and their respective urls

## [0.1.0] - 2022-11-18
### Added
- Minimal solution, everything very static
- Writing prices in standard output and on discord

[unreleased]: https://github.com/pdMa2s/Scrappy/compare/0.5.0...HEAD
[0.6.0]: https://github.com/pdMa2s/Scrappy/compare/0.5.0...0.6.0
[0.5.0]: https://github.com/pdMa2s/Scrappy/compare/0.4.1...0.5.0
[0.4.1]: https://github.com/pdMa2s/Scrappy/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/pdMa2s/Scrappy/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/pdMa2s/Scrappy/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/pdMa2s/Scrappy/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/pdMa2s/Scrappy/releases/tag/0.1.0