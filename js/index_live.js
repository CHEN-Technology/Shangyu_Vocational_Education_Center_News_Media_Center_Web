const resourceUrl = 'http://10.1.10.111:8080/__defaultApp__/live.flv.flv'; // 资源地址
window.resourceIsValid = false; // 定义全局变量 resourceIsValid 并初始化为 false

function checkResourceValidity(url) {
  return new Promise((resolve) => {
    const timeoutMs = 1000; // 超时时间，单位为毫秒

    const timeoutPromise = new Promise((resolve) => {
      setTimeout(() => {
        resolve(false); // 返回 false，代表超时
      }, timeoutMs);
    });

    const responsePromise = new Promise((resolve) => {
      const controller = new AbortController();
      const signal = controller.signal;

      fetch(url, { method: 'HEAD', signal })
        .then((response) => {
          if (response.ok) {
            resolve(true); // 返回 true，代表资源有效
          } else {
            resolve(false); // 返回 false，代表资源无效
          }
        })
        .catch(() => resolve(false));

      setTimeout(() => {
        controller.abort();
      }, timeoutMs);
    });

    Promise.race([responsePromise, timeoutPromise])
      .then((result) => {
        window.resourceIsValid = result; // 将结果赋值给全局变量 resourceIsValid
        resolve(result); // 传递结果到函数外部
      });
  });
}

function startCheckingValidity() {
    checkResourceValidity(resourceUrl)
      .then((result) => {
        if (!window.resourceIsValid) {
          window.location.href = "http://10.1.10.111:8888";
        }
  
        console.log(result); // 输出资源的有效性
        // 5秒后进行下一轮实时异步查询
        setTimeout(startCheckingValidity, 1000);
      })
      .catch((error) => {
        console.error('查询资源有效性时出错', error);
      });
  }
  
  startCheckingValidity();

// 获取当前时间
var currentDate = new Date();

// 格式化时间为 "YYYY-MM-DD" 的格式
var formattedDate = currentDate.getFullYear() + "-" + (currentDate.getMonth() + 1) + "-" + currentDate.getDate();

// 将格式化后的时间插入到 <div class="title2"></div> 中
document.querySelector('.title2').textContent = formattedDate;