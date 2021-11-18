# [1.0.1](https://github.com/johnnymillergh/home_guardian/compare/1.0.0...1.0.1) (2021-11-18)


### Build
* **$GitHub:** migrate to the container registry from the Docker registry ([e23a8af](https://github.com/johnnymillergh/home_guardian/commit/e23a8afa115f08761c7239259b74de5aa030b4f8))



# 1.0.0 (2021-11-17)


### Features

* **$common:** refine [@debounce](https://github.com/debounce) and [@throttle](https://github.com/throttle) decorators ([46dce1d](https://github.com/johnnymillergh/home_guardian/commit/46dce1d0b53b2b9522bf7e03e31e00492722771b))
* **$conf:** support dynamic environment variable configuration ([0a00573](https://github.com/johnnymillergh/home_guardian/commit/0a005736e425a603614482faedab7c25ad228857))
* **$Decorator:** create elapsed time decorator ([0c18b70](https://github.com/johnnymillergh/home_guardian/commit/0c18b70d9210aeb41e6aa97f1f44e33b7c0fe8f9))
* **$loguru:** integrate loguru for logging ([180f824](https://github.com/johnnymillergh/home_guardian/commit/180f824140adc65871c77c0daa15f5ec6948507c))
* **$Loguru:** set default log level as "INFO" ([1b71e45](https://github.com/johnnymillergh/home_guardian/commit/1b71e4585c88237d70f7d1a2ae9f81b72182ba01))
* **$message:** send warning email when detecting face ([7e7450a](https://github.com/johnnymillergh/home_guardian/commit/7e7450aa40b34a59aced003129e431eec80e8695))
* **$message:** support configurable muting email ([5894748](https://github.com/johnnymillergh/home_guardian/commit/589474819c463a301ceaa8f6be040149a32a5a2f))
* **$Message:** support sending email ([e101760](https://github.com/johnnymillergh/home_guardian/commit/e101760f4dc4b2ec67238070a35dbf3e0fa80aec))
* **$message:** support sending redered HTML in email ([f423fec](https://github.com/johnnymillergh/home_guardian/commit/f423fec3bd3b7f4c2bd004674b92176c1f7e7ccb))
* **$OpenCV:** detect face and save the image asynchronously ([4651abb](https://github.com/johnnymillergh/home_guardian/commit/4651abb90277fe467bb1d08c12f9e93e095334ef))
* **$opencv:** persistence detected face info ([1bec964](https://github.com/johnnymillergh/home_guardian/commit/1bec964080c7eb3931f3132133b9b9f52722a269))
* **$OpenCV:** support face training and recognition ([9fd983d](https://github.com/johnnymillergh/home_guardian/commit/9fd983d5851aed81769cc82451de3ec1b1016c35))
* **$OpenCV:** tell headless or not ([b3097eb](https://github.com/johnnymillergh/home_guardian/commit/b3097eb6fee51a00f7fc2daee954634ac027b757))
* **$startup:** define multiple startup mode identified by runtime arguments ([a19bf5e](https://github.com/johnnymillergh/home_guardian/commit/a19bf5e2b2a98a92e5caa6a7d8a37f5c8e883f26))
* **$template:** add Jinjia2 dependency ([6f63176](https://github.com/johnnymillergh/home_guardian/commit/6f631768db36556e197dc28ee94ee4ef1ab983cc))
* integrate peewee as ORM library ([ae56fe5](https://github.com/johnnymillergh/home_guardian/commit/ae56fe5fa3076059a15912322064abe37c489790))
* new startup mode for collecting data ([01872b5](https://github.com/johnnymillergh/home_guardian/commit/01872b53df72cd82ac5891a86aff5cdfbc0e7a0c))


### Performance Improvements

* **$Async:** add async debounce decorator ([661f1ac](https://github.com/johnnymillergh/home_guardian/commit/661f1ac88e8675054ef9a623daf0e670ba4044c9))
* **$db:** refine ORM log when initializing db ([5fd5b1f](https://github.com/johnnymillergh/home_guardian/commit/5fd5b1f3f3d81f9dc46eb55d5448fb5c75f140e0))
* **$email:** only login and logout from the email server once ([cef9cf9](https://github.com/johnnymillergh/home_guardian/commit/cef9cf926eb9868f59f2d26552018c4310a869bf))
* **$Executor:** cleanup thread pool executor when exiting program ([b254d41](https://github.com/johnnymillergh/home_guardian/commit/b254d418f4eddde5aff63fa494243170402df5a9))
* **$loguru:** abstract function for loguru configuration ([b1433d1](https://github.com/johnnymillergh/home_guardian/commit/b1433d19fabc1f127f33f4acadab8975c6c51b88))
* **$loguru:** override default console log format ([71181d5](https://github.com/johnnymillergh/home_guardian/commit/71181d590ad346610d99fcb26117e0a813279a40))
* **$OpenCV:** change dependency to opencv-python-headless==4.5.4.58 ([fe471dd](https://github.com/johnnymillergh/home_guardian/commit/fe471dd2adbb8f3a6bc2de8175c2d6351fdac63b))
* **$OpenCV:** multi-threading for OpenCV ([bbfecda](https://github.com/johnnymillergh/home_guardian/commit/bbfecda78cd71ee6a86f9830a856544dfd988c00))
* **$OpenCV:** read embedded xml resource ([a0c818e](https://github.com/johnnymillergh/home_guardian/commit/a0c818eb461f4367dff96fa6d0272fadd8f328c6))
* **$Python:** support pooled multi thread ([cc27bce](https://github.com/johnnymillergh/home_guardian/commit/cc27bce3aa884262ab0f7b89d99661e1ecb3be34))
* support function's debounce and throttle ([e3aa552](https://github.com/johnnymillergh/home_guardian/commit/e3aa552488669be85172f1b29b04ca6eb074681b))
* upgrade dependencies ([a07af6a](https://github.com/johnnymillergh/home_guardian/commit/a07af6a94b1c324705ac82a3c6bf916bc6d73c8f))


### BREAKING CHANGES

* **$OpenCV:** if it's not headless, show capture window
* **$OpenCV:** support face training and recognition
* **$OpenCV:** use parallelism (multi-thread) to work with CPU bound operation
* **$message:** support sending redered HTML in email
* **$template:** support template rendering
