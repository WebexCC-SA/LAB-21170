const encodedInfo = window.location.search.slice(1)

if (encodedInfo) {
  try {
    const info = JSON.parse(atob(encodedInfo))
    Object.keys(info).forEach((key) => {
      sessionStorage.setItem(key, info[key])
    })
    window.history.replaceState(
      {},
      document.title,
      window.location.pathname + window.location.hash,
    )
  } catch (error) {
    console.warn("Ignoring invalid lab context in URL")
  }
}
