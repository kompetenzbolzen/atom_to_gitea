# rss-to-gitea

## Usage

```
rsstogitea config.yml
```

## Configuration

```yaml
---
url: 'https://gitea.example.com'
token: 'env/GITEA_TOKEN'
owner: 'org'
repo: 'repo'
label: 'update'
feeds:
  - url: 'https://github.com/go-gitea/gitea/releases.atom'
    name: 'Gitea'
    assign: 'user'
    exclude:
      - dev
      - rc
    include: []
```
