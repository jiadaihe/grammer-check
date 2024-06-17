
## About
It is an application to search Github repos by user name or organization name. You can get quick summary of each repo and its statistics, such as number of stars and main language. You can further sort repos and filter repos by certain criteria. Enjoy and have fun!

## Start the App

- `npm start`

## Component Tree

- root:
    - App:
        - ListRepositories (states: repos, currentPage)
            - SearchForm (states: username)
            - Table (states: repos)
            - ClientSidePagination (states: currentPage)
## Deployment
Whispter requires the command-line tool `ffmpeg` to be installed on your system, which is available from most package managers


## Reference

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
Scaffolded by `npx create-react-app my-app --template typescript` (https://create-react-app.dev/docs/adding-typescript/)

For pagination, I first implemented client side pagination. But later found out that `react-table` can achieve it. This could be a future improvement.

For filtering and sorting, I found an example from `react-table` documentation https://tanstack.com/table/latest/docs/framework/react/examples/filters, and used code from there. 


## Future Improvements
1. Use react-table's pagination feature.
2. Use Github's API JS package `octokit`, so we don't need to maintain API URL.
3. Even though the number of repos is very unlikely to be high and client side pagination is performant. It would be nice to implement server side pagination component to handle large response data.
4. Better error handling and use alert or message to inform user, so we can provide better user experience.
