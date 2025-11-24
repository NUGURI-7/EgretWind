import { MsgError } from "@/utils/message";
import axios, { AxiosHeaders, type InternalAxiosRequestConfig } from "axios";
import router from '@/router'

const axiosConfig = {
    baseURL: "127.0.0.1/admin/api",
    withCredentials: false,
    timeout: 1800000, // 30分钟 timeout
    headers: {},
}

const instance = axios.create(axiosConfig)

/* 设置请求拦截器 */
instance.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        if (config.headers === undefined) {
            config.headers = new AxiosHeaders()
        }
        if (config.url && config.url.startsWith('http')) {
            return config
        }
        // const { user, login } = useStore()
        // const token = login.getToken()
        // const language = user.getLanguage()
        // config.headers['Accept-Language'] = `${language}`
        // if (token) {
        //   config.headers['AUTHORIZATION'] = `Bearer ${token}`
        // }
        return config
    },
    (err: any) => {
        return Promise.reject(err)
    },
)

//设置响应拦截器
instance.interceptors.response.use(
    (response: any) => {
        if (response.data) {
            if (response.data.code !== 200 && !(response.data instanceof Blob)) {
                if (response.config.url.includes('/application/authentication')) {
                    return Promise.reject(response.data)
                }
                MsgError(response.data.message || '请求失败')
                return Promise.reject(response.data)
            }
        }
        return response
    },
    (err: any) => {
        if (err.code === 'ECONNABORTED') {
            MsgError('请求超时，请重试')
        } else if (!err.response) {
            // 没有响应说明网络有问题
            MsgError('网络连接失败')
        } else {
            // HTTP 状态码错误
            const status = err.response.status
            if (status === 401) {
                // token 过期
                localStorage.removeItem('token')
                window.location.href = '/login'
            } else if (status === 500) {
                MsgError('服务器错误')
            }
        }
        return Promise.reject(err)
    }
)