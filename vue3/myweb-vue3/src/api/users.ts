import request from '@/utils/request'

type LoginInfo = {
  username: string
  code?: string
  password: string
}

type LoginResult = {
  success: boolean
  state: number
  message: string
  content: string
}

export const login = (loginInfo: LoginInfo) => {
  return request<LoginResult>({
    method: 'POST',
    url: '/users/login',
    data: `username=${loginInfo.username}&password=${loginInfo.password}`
  })
}
type registerResult={
  success: boolean
  state: number
  message: string
  content: string
}
export const register=(registerInfo)=>{
  return request<registerResult>({
    method:'POST',
    url:'/users/register',
    data:`username=${registerInfo.username}&password=${registerInfo.password}`
  })
}

export const logout = () => {
  return request({
    method: 'POST',
    url: '/users/logout'
  })
}
