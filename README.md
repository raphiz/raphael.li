# raphael.li

Personal website/blog built with the [Eleventy](https://www.11ty.dev/) site generator - based on [eleventy-base-blog](https://github.com/11ty/eleventy-base-blog)

## Prerequisites

This project requires [Nix](https://nixos.org/) with [flakes](https://nixos.wiki/wiki/Flakes) support for both the development and the build process, ensuring a consistent and reproducible environment across all stages.

## Development Environment

```bash
# Manually start development environment ...
nix develop
# ... or let direnv do it for you
direnv allow
```

The development environment offers the following commands that are sufficient for most use cases:

- `nix build`: builds the site (as NIX derivation)
- `npm run serve`: serves the site locally
