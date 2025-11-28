import { get } from "@/request"
import type Result from "@/request/Result"
import type { Ref } from "vue"



const prefix = '/article'
/**
 * 文章列表
 * @param param 
 * @param loading 
 * @returns 
 */
const getArticleList: (param?: any, loading?: Ref<boolean>) => Promise<Result<any>> = (
    param,
    loading,
) => {
    return get(`${prefix}/list`, param, loading)
}


export default {
    getArticleList
}