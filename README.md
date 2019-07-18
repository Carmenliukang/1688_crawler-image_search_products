# 1688_crawler-image_search_products
通过 1688 PC 端网址，上传图片查询类似的商品

1. 具体的流程如下：
    1. 获取 需要 b64 编码的时间戳
    2. 获取 必须传输的参数 signature policy 同时将生成的 图片 key 返回
    3. 上传图片
    4. 拼接查询的结果
   
这里整体的过程如下：
1. 由于 Chrome 对于跨域请求 通过检查 不能再次 查看具体的相关的 headers body 中的具体详细信息。所以 采用了 Postman Interceptor
 +  postman app 来获取相关请求的接口数据。

2. 确定整体的流程，1688 上传图片的接口。通过 postman app 看到可以就是 https://cbusearch.oss-cn-shanghai.aliyuncs.com/ 这些需要的参数如下：
   ------WebKitFormBoundaryQA6M8CbwWKaQlAKW
Content-Disposition: form-data; name="name"

666.jpg
------WebKitFormBoundaryQA6M8CbwWKaQlAKW
Content-Disposition: form-data; name="key"

cbuimgsearch/GAKxnFz2Gr1562504734000.jpg
------WebKitFormBoundaryQA6M8CbwWKaQlAKW
Content-Disposition: form-data; name="policy"

eyJleHBpcmF0aW9uIjoiMjAxOS0wNy0wN1QxODowNTowMC4wMTRaIiwiY29uZGl0aW9ucyI6W1siY29udGVudC1sZW5ndGgtcmFuZ2UiLDAsMTA0ODU3NjAwMF1dfQ==
------WebKitFormBoundaryQA6M8CbwWKaQlAKW
Content-Disposition: form-data; name="OSSAccessKeyId"

LTAIltWGJ0iXyZ4r
------WebKitFormBoundaryQA6M8CbwWKaQlAKW
Content-Disposition: form-data; name="success_action_status"

200
------WebKitFormBoundaryQA6M8CbwWKaQlAKW
Content-Disposition: form-data; name="callback"


------WebKitFormBoundaryQA6M8CbwWKaQlAKW
Content-Disposition: form-data; name="signature"

9av9qVLCwznoThXqlJxmHA89bQw=
------WebKitFormBoundaryQA6M8CbwWKaQlAKW
Content-Disposition: form-data; name="file"; filename="666.jpg"
Content-Type: image/jpeg

同时这里使用的格式是 multipart/form-data; boundary=----WebKitFormBoundaryQA6M8CbwWKaQlAKW

然后就可以 全局的查询相关的参数 是如何获取来的。在这里 是直接使用Chrome 查询 中的 全局的查询 signature 和 域名 ，找到，需要看的 js 文件 
https://astyle.alicdn.com/app/searchweb/products/imagesearch/htmlhead/pkg-a/js/plupload.js?_v=1a4ba5f5a7bda1cd15cc47a08ddee882.js
同时还有一个 URL 中返回的数据中也有  这些参数：
URL：https://open-s.1688.com/openservice/ossDataService?appName=pc_tusou&appKey=cGNfdHVzb3U7MTU2MjUwNDgzMTQyMQ==&&callback=jQuery183004849602880805359_1562504854360&_=1562504857087
结果：jQuery183004849602880805359_1562504854360(
{
    "data": {
        "policy": "eyJleHBpcmF0aW9uIjoiMjAxOS0wNy0wN1QxODowNzoxMy4zODhaIiwiY29uZGl0aW9ucyI6W1siY29udGVudC1sZW5ndGgtcmFuZ2UiLDAsMTA0ODU3NjAwMF1dfQ==",
        "expire": "1562522833",
        "enable": true,
        "accessid": "LTAIltWGJ0iXyZ4r",
        "signature": "M8y64G3r5E6hQdaklOFWi256XeQ=",
        "host": "https:\/\/cbusearch.oss-cn-shanghai.aliyuncs.com"
    },
    "msg": "OK",
    "time": 1,
    "code": 200,
    "encode": "GBK"
});
这里有的参数的是 policy  accessid signature
现在需要确定的就是 key 是如何生成的。key 这个是通过看 js 代码 看到的。现在回头再看这里，其实大概率是可以猜到的。 固定值 + 10位随机 + 毫秒级别时间戳

那么最后的我们需要看一下这个接口需要哪些 参数：
 https://open-s.1688.com/openservice/ossDataService
 参数：
  appName: pc_tusou
  appKey: cGNfdHVzb3U7MTU2MjUwNDgzMTQyMQ==
  (empty)
  callback: jQuery183004849602880805359_1562504854360
  _: 1562504857087
  
  可以看到 callback 最后几位是 毫秒级别时间戳 _ 也是时间戳 appName 在 js 代码中是 固定值 appKey这里在 service_v1.js  代码中有 简单的介绍，为 appName ; 时间戳 三者拼接 然后再次 b64 编码的结果
  
  然后就可以卡到  这里的时间戳和 _ 的时间戳是不一致的， 其实 是通过接口调用的。全局查询 这个 时间戳，然后 就可以看到调用的接口，这样就可以了。
  

重构了代码，增加配置文件，log 记录模块

 
