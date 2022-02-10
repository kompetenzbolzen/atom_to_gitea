# rss-to-gitea

Create Gitea-Issue for newest entry in Atom-Feed.
Can be used to automatically create Update-Tickets.

## Usage

```
rsstogitea config.yml
```

## Configuration

* **url** Gitea-URL
* **token** API-Token, either in plain or in an environment variable with `env/<VAR>`
* **owner** Owner of the repo to create issues in
* **repo** Name of the repo to create issues in
* **label** Label to add to created Issue
* **feeds** list of
	* **url** Atom-Feed URL
	* **name** Name of the Feed. Used as issue-name prefix
	* **assign** User to assign the issue to
	* **exclude** List. If name of item contains one or more, item is ignored. Not Regex.
	* **include** List. Item is ignored if title does not contain all strings. Not Regex.

### Example

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
