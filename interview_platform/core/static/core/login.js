document.addEventListener('DOMContentLoaded', function() {    
    document.getElementById('login-form').addEventListener('submit', function(event) {
        // 防止表單默認提交行為
        event.preventDefault();

        // 提交表單
        this.submit();
    });
});
