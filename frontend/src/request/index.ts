import axios, { AxiosHeaders, type InternalAxiosRequestConfig } from "axios";

const axiosConfig = {
    baseURL: "127.0.0.1/admin/api",
    withCredentials: false,
    timeout: 1800000, // 30分钟 timeout
    headers: {},      
}

const instance = axios.create(axiosConfig)

/** 设置请求拦截器 */
// instance.interceptors.request.use(
//     (config: InternalAxiosRequestConfig) => {
//         if (config.headers === undefined) {
//             config.headers = new AxiosHeaders()
//         }
//         return config
//     }
// )
