import axios from 'axios'

const api = axios.create({
  baseURL: 'https://counting-stars-ge5i.onrender.com/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

export const getClan = async () => {
  try {
    const response = await api.get('/clan')

    console.log('CLAN API RESPONSE:', response.data)

    return {
      code: 0,
      data: response.data
    }
  } catch (error) {
    console.error('Failed to fetch clan:', error)

    return {
      code: 1,
      data: null
    }
  }
}

export const getMembers = async () => {
  try {
    const response = await api.get('/members')

    console.log('MEMBERS API RESPONSE:', response.data)

    return {
      code: 0,
      data: response.data
    }
  } catch (error) {
    console.error('Failed to fetch members:', error)

    return {
      code: 1,
      data: null
    }
  }
}

export const getCurrentWar = async () => {
  try {
    const response = await api.get('/current-war')

    console.log('CURRENT WAR API RESPONSE:', response.data)

    return {
      code: 0,
      data: response.data
    }
  } catch (error) {
    console.error('Failed to fetch current war:', error)

    return {
      code: 1,
      data: null
    }
  }
}

export const getWarLog = async () => {
  try {
    const response = await api.get('/war-log')

    console.log('WAR LOG API RESPONSE:', response.data)

    return {
      code: 0,
      data: response.data
    }
  } catch (error) {
    console.error('Failed to fetch war log:', error)

    return {
      code: 1,
      data: null
    }
  }
}

export const getHealth = async () => {
  try {
    const response = await api.get('/health')

    return {
      code: 0,
      data: response.data
    }
  } catch (error) {
    console.error('Backend health check failed:', error)

    return {
      code: 1,
      data: null
    }
  }
}

export const getAnnouncements = async () => {
  try {
    const response = await api.get('/announcements')

    console.log(
      'ANNOUNCEMENTS API RESPONSE:',
      response.data
    )

    return {
      code: 0,
      data: response.data
    }
  } catch (error) {
    console.error(
      'Failed to fetch announcements:',
      error
    )

    return {
      code: 1,
      data: null
    }
  }
}

export const getClanSettings = async () => {
  try {
    const response = await api.get('/clan-settings')

    console.log(
      'CLAN SETTINGS API RESPONSE:',
      response.data
    )

    return {
      code: 0,
      data: response.data
    }
  } catch (error) {
    console.error(
      'Failed to fetch clan settings:',
      error
    )

    return {
      code: 1,
      data: null
    }
  }
}

export default api