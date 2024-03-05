## [4.0.1](https://github.com/alexschimpf/fastapi-versionizer/compare/v4.0.0...v4.0.1) (2024-03-05)


### Bug Fixes

* Fixed oauth2 redirect bug for versioned routes ([17f0172](https://github.com/alexschimpf/fastapi-versionizer/commit/17f0172bf1a6cf4d4f39f94107307557facbf4ff))

## [4.0.0](https://github.com/alexschimpf/fastapi-versionizer/compare/v3.0.4...v4.0.0) (2024-03-05)


### Breaking Changes

* Dropped support for python 3.7 ([00607b8](https://github.com/alexschimpf/fastapi-versionizer/commit/00607b8f1ae0db23b7e63666b0629307a3a631dc))

## [3.0.4](https://github.com/alexschimpf/fastapi-versionizer/compare/v3.0.3...v3.0.4) (2023-11-03)


### Bug Fixes

* Added Websocket support back ([211a66e](https://github.com/alexschimpf/fastapi-versionizer/commit/211a66e8aac56dbf2d5ffc94d6c65959044ca5dd))

## [3.0.3](https://github.com/alexschimpf/fastapi-versionizer/compare/v3.0.2...v3.0.3) (2023-11-02)


### Bug Fixes

* Fixed issue with OpenAPI tags for versioned docs ([dbc434c](https://github.com/alexschimpf/fastapi-versionizer/commit/dbc434c85170cbc1802ff167e33c8ab4204d64d3))

## [3.0.2](https://github.com/alexschimpf/fastapi-versionizer/compare/v3.0.1...v3.0.2) (2023-10-25)


### Bug Fixes

* Fixed OAuth issue for versioned Swagger pages ([94b7a37](https://github.com/alexschimpf/fastapi-versionizer/commit/94b7a37de66a3fe5304d26460371788f38c308ef))

## [3.0.1](https://github.com/alexschimpf/fastapi-versionizer/compare/v3.0.0...v3.0.1) (2023-10-17)


### Bug Fixes

* Fixed issue with root_path/servers in versioned doc pages ([a82a343](https://github.com/alexschimpf/fastapi-versionizer/commit/a82a343de350b7a323a8a46b023b1dc897c1302b))

## [3.0.0](https://github.com/alexschimpf/fastapi-versionizer/compare/v2.1.5...v3.0.0) (2023-10-14)


### Breaking Changes

* Versionizer now versions a FastAPI app in place ([8217e80](https://github.com/alexschimpf/fastapi-versionizer/commit/8217e80b3925a7d30ef77e6eb8693b271fe02247))

## [2.1.5](https://github.com/alexschimpf/fastapi-versionizer/compare/v2.1.4...v2.1.5) (2023-10-14)


### Bug Fixes

* Fixed issue with middleware stack support ([e96cf0d](https://github.com/alexschimpf/fastapi-versionizer/commit/e96cf0d004d20a65668d85f5ae46d427d958f5ef))

## [2.1.4](https://github.com/alexschimpf/fastapi-versionizer/compare/v2.1.3...v2.1.4) (2023-10-13)


### Bug Fixes

* Fixed issue with OpenAPI metadata not showing up for versioned doc pages ([87093b9](https://github.com/alexschimpf/fastapi-versionizer/commit/87093b95766efa0bbc49777fae75efc55e489747))

## [2.1.3](https://github.com/alexschimpf/fastapi-versionizer/compare/v2.1.2...v2.1.3) (2023-10-13)


### Bug Fixes

* Fixed issue with lifespan support ([ee40d11](https://github.com/alexschimpf/fastapi-versionizer/commit/ee40d11cba743c07216370715a7fbcd23f0a145e))

## [2.1.2](https://github.com/alexschimpf/fastapi-versionizer/compare/v2.1.1...v2.1.2) (2023-10-04)


### Bug Fixes

* Fixed issue where custom latest_prefix wasn't getting passed to callback correctly ([020d32b](https://github.com/alexschimpf/fastapi-versionizer/commit/020d32b13143c1a6d98b449fec17cf23d0d8ed86))

## [2.1.1](https://github.com/alexschimpf/fastapi-versionizer/compare/v2.1.0...v2.1.1) (2023-10-03)


### Bug Fixes

* Now using app's openapi_url field for OpenAPI URL ([e97d5f9](https://github.com/alexschimpf/fastapi-versionizer/commit/e97d5f95eb6b8d006c03fff0bfbfd8136c1b2eec))

## [2.1.0](https://github.com/alexschimpf/fastapi-versionizer/compare/v2.0.0...v2.1.0) (2023-10-03)


### Features

* Added include_versions_route parameter ([42dcaf7](https://github.com/alexschimpf/fastapi-versionizer/commit/42dcaf73bf2bff7d6b6d734c8c30137b73aa6f06))

## [2.0.0](https://github.com/alexschimpf/fastapi-versionizer/compare/v1.2.0...v2.0.0) (2023-10-02)


### Breaking Changes

* Redesigned FastAPI versionizer ([4cd0fd1](https://github.com/alexschimpf/fastapi-versionizer/commit/4cd0fd1d3e93eb1845439743ed907d562a508bb9))

## [1.2.0](https://github.com/alexschimpf/fastapi-versionizer/compare/v1.1.1...v1.2.0) (2023-09-28)


### Features

* Added enable_versions_route param ([e3afcce](https://github.com/alexschimpf/fastapi-versionizer/commit/e3afcce98b9422dc3f54d722fc9168030e1c7e75))

## [1.1.1](https://github.com/alexschimpf/fastapi-versionizer/compare/v1.1.0...v1.1.1) (2023-09-28)


### Bug Fixes

* Now using natural sorting for routes for sorted_routes=True ([d55af27](https://github.com/alexschimpf/fastapi-versionizer/commit/d55af275bbc5e55c7ee203b04aeff65e09893c93))

## [1.1.0](https://github.com/alexschimpf/fastapi-versionizer/compare/v1.0.1...v1.1.0) (2023-09-27)


### Features

* Added callback feature ([43a8e77](https://github.com/alexschimpf/fastapi-versionizer/commit/43a8e77eb1cf57ec00385a4ee5bfd3751e1fc9a0))

## [1.0.1](https://github.com/alexschimpf/fastapi-versionizer/compare/v1.0.0...v1.0.1) (2023-09-20)


### Bug Fixes

* Dummy commit to bump version ([020f393](https://github.com/alexschimpf/fastapi-versionizer/commit/020f3936f3cf101c2a7c0171ce6c656bca9993cf))

## 1.0.0 (2023-09-20)


### Bug Fixes

* Fixed package build error ([2f08334](https://github.com/alexschimpf/fastapi-versionizer/commit/2f083343b5a51c7ea3a0a10747250c4c123840c6))
