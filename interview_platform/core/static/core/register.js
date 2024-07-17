document.getElementById('register-form').addEventListener('submit', function(event) {
    // 防止表單默認提交行為
    event.preventDefault();

    // 提交表單
    this.submit();
    
    // 等待一小段時間，確保訊息已經顯示
    setTimeout(function() {
        // 顯示跳轉訊息
        document.getElementById('redirect-message').style.display = 'block';
        // 執行跳轉
        setTimeout(function() {
            window.location.href = "{% url 'home' %}";
        }, 3000);
    }, 100);
});