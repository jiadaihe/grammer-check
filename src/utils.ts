// variable `apiUrl` can be removed if we use octokit
const apiUrl = 'https://api.github.com'


export const getReposByUser = async (username: string): Promise<{data: any, status: number}> => {
  const url = `${apiUrl}/users/${username}/repos`
  console.log(url)
  const options = {
    headers: {
      'X-GitHub-Api-Version': '2022-11-28'
    }
  }
  const res = await fetch(url, options)
  const linkHeader = res.headers.get('link')
  // const pagesRemaining = linkHeader !== null && linkHeader.includes(`rel=\"next\"`)
  // const pagesPrev = linkHeader !== null && linkHeader.includes(`rel=\"prev\"`)
  console.log({linkHeader: linkHeader})

  if (!res.ok) {
      console.error(`Status ${res.status}. Failed to get repos for user ${username}`)
      return {
        data: [],
        status: res.status
        // pagesRemaining: false,
        // pagesPrev: false
      }
  }
  return {
    data: await res.json(),
    status: res.status
    // pagesRemaining: pagesRemaining,
    // pagesPrev: pagesPrev
  }
}

export const getReposByOrg = async (orgname: string): Promise<{data: any, status: number}>  => {
  const url = `${apiUrl}/orgs/${orgname}/repos`
  const options = {
    headers: {
        'X-GitHub-Api-Version': '2022-11-28'
    }
  }
  const res = await fetch(url, options)
  // TODO: better error handling!
  if (!res.ok) {
    console.error(`Status ${res.status}. Failed to get repos for org ${orgname}`)
    return {
        data: [],
        status: res.status
      }
  }
  return {
    data: await res.json(),
    status: res.status
  }
}

export const getReposByUserOrOrg = async (name: string) => {
  let data = await getReposByUser(name)
  if(data.status === 404) {
    data = await getReposByOrg(name)
  }
  if(data.status === 404) {
    // TODO: add alert or pop window?
    console.error(`Status 404. Failed to get repos for user or org ${name}`)
  }
  return data.data
}
