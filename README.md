# Github activity

Get a timeline of all activity for a github repository.

This includes:

* repository creation date
* commits
* issue comments
* issue creation
* pull request comments
* pull request creation

## Implementation

This code uses the Github GraphQL API to make queries for the associated information.

The GraphQL queries are:

* fetch list of pull requests
* fetch comments for a pull request
* fetch branches
* fetch commits for a branch
* fetch issues
* fetch comments on issues
