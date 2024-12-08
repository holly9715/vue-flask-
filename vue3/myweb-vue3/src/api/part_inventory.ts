import request from '@/utils/request'

export const getPartData = () => {
  return request({
    method: 'GET',
    url: '/users/part_inventory/data'
  })
}
export const getShareData=()=>{
  return request({
    method: 'GET',
    url: '/users/share/getfiles'
  })
}

export const getModel = () => {
  return request({
    method: 'GET',
    url: '/users/getModel'
  })
}
export const downloadModel = () => {
  return request({
    method: 'POST',
    url: '/users/getModel',
    responseType: 'blob'
  })
}
